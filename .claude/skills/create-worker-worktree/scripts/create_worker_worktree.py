#!/usr/bin/env python3
"""Create one permanent worker worktree next to the current repository.

The worktree lives at `<parent>/<reponame>-<worker>` on the new branch
`<worker>-workbench`, created from the local default branch. The branch is
registered as protected in `.csk/worktrees.json` so `finish-branch` re-syncs
it after a merge instead of deleting it.

Safety contract:
- runs only from a clean default-branch checkout (tracked changes block);
- never reuses an existing branch ref, folder, or registered worktree;
- the only mutating git command is `git worktree add`;
- verifies root, branch, and cleanliness of the created worktree;
- prints a JSON result between WORKER_WORKTREE_RESULT_BEGIN/END markers.

Exit codes: 0 success, 1 blocked/error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WORKER_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,30}$")
CONFIG_RELATIVE = Path(".csk") / "worktrees.json"


class GitError(RuntimeError):
    """A blocked precondition or failed git command; message is readable."""


def run_git(args: list[str], failure: str) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        details = (result.stdout + "\n" + result.stderr).strip()
        raise GitError(f"{failure}\n{details}" if details else failure)
    return result.stdout.strip()


def git_succeeds(args: list[str]) -> bool:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode == 0


def detect_base_branch(repo: str) -> str:
    for candidate in ("main", "master"):
        if git_succeeds(
            ["-C", repo, "show-ref", "--verify", "--quiet", f"refs/heads/{candidate}"]
        ):
            return candidate
    raise GitError(
        "Blocked: neither a local 'main' nor 'master' branch exists. "
        "Nothing was changed."
    )


def load_config(config_path: Path) -> dict:
    if not config_path.is_file():
        return {"schema_version": 1, "workers": [], "protectedBranches": []}
    try:
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as error:
        raise GitError(
            f"Blocked: '{config_path}' exists but could not be parsed as JSON "
            f"({error}). Repair it manually first. Nothing was changed."
        )
    if not isinstance(config, dict):
        raise GitError(
            f"Blocked: '{config_path}' must contain a JSON object. "
            "Nothing was changed."
        )
    config.setdefault("schema_version", 1)
    config.setdefault("workers", [])
    config.setdefault("protectedBranches", [])
    if not isinstance(config["workers"], list) or not isinstance(
        config["protectedBranches"], list
    ):
        raise GitError(
            f"Blocked: '{config_path}' has an invalid shape - 'workers' and "
            "'protectedBranches' must be lists. Nothing was changed."
        )
    return config


def save_config(config_path: Path, config: dict) -> None:
    config_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        dir=str(config_path.parent), prefix=".worktrees-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(config, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, config_path)
    except OSError:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--worker",
        required=True,
        help=(
            "Short lowercase worker name (e.g. 'codex', 'worker2'). Becomes "
            "the folder suffix '<repo>-<worker>' and branch "
            "'<worker>-workbench'."
        ),
    )
    args = parser.parse_args(argv)

    worker = args.worker.strip().lower()
    if not WORKER_NAME_PATTERN.match(worker):
        raise GitError(
            f"Blocked: invalid worker name '{args.worker}'. Use 1-31 "
            "characters: lowercase letters, digits, hyphens; must start with "
            "a letter or digit. Nothing was changed."
        )

    repo_root = Path(
        run_git(
            ["rev-parse", "--show-toplevel"],
            "Blocked: the current directory is not inside a Git repository.",
        )
    ).resolve()
    repo_name = repo_root.name
    repo_parent = repo_root.parent
    if repo_parent == repo_root:
        raise GitError(
            "Blocked: the repository root has no parent directory to place "
            "the worktree in. Nothing was changed."
        )

    base_branch = detect_base_branch(str(repo_root))
    worker_branch = f"{worker}-workbench"
    worktree_path = (repo_parent / f"{repo_name}-{worker}").resolve()

    current_branch = run_git(
        ["-C", str(repo_root), "branch", "--show-current"],
        "Blocked: the current branch could not be read.",
    )
    if not current_branch:
        raise GitError(
            "Blocked: the repository is in detached-HEAD state. Expected "
            f"branch '{base_branch}'. Nothing was changed."
        )
    if current_branch != base_branch:
        raise GitError(
            f"Blocked: the current branch is '{current_branch}', expected "
            f"'{base_branch}'. Switch back to the default branch first. "
            "Nothing was changed."
        )

    porcelain = run_git(
        ["-C", str(repo_root), "status", "--porcelain=v1", "--untracked-files=no"],
        "Blocked: the working-tree status could not be read.",
    )
    if porcelain:
        raise GitError(
            "Blocked: the working tree has uncommitted tracked changes. "
            "Commit or set them aside first. Nothing was changed.\n" + porcelain
        )

    refs = run_git(
        [
            "-C",
            str(repo_root),
            "for-each-ref",
            "--format=%(refname)",
            f"refs/heads/{worker_branch}",
            f"refs/remotes/*/{worker_branch}",
        ],
        "Blocked: existing refs could not be checked.",
    )
    if refs:
        raise GitError(
            f"Blocked: a branch ref named '{worker_branch}' already exists "
            f"({', '.join(refs.split())}). The worker worktree is created "
            "exactly once and then reused; open the existing worktree instead. "
            "Nothing was changed."
        )

    if worktree_path.exists():
        raise GitError(
            f"Blocked: the target path already exists: '{worktree_path}'. "
            "Nothing was changed."
        )

    registered = run_git(
        ["-C", str(repo_root), "worktree", "list", "--porcelain"],
        "Blocked: registered worktrees could not be read.",
    )
    for line in registered.splitlines():
        if line.startswith("worktree "):
            existing = Path(line[len("worktree "):].strip()).resolve()
            if str(existing).lower() == str(worktree_path).lower():
                raise GitError(
                    "Blocked: the target path is already registered as a "
                    f"worktree: '{worktree_path}'. Nothing was changed."
                )

    config_path = repo_root / CONFIG_RELATIVE
    config = load_config(config_path)

    # The only mutating git command in this script.
    create = subprocess.run(
        [
            "git",
            "-C",
            str(repo_root),
            "worktree",
            "add",
            "-b",
            worker_branch,
            str(worktree_path),
            base_branch,
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if create.returncode != 0:
        # Best-effort cleanup so a half-registered worktree does not block a
        # retry.
        subprocess.run(
            ["git", "-C", str(repo_root), "worktree", "prune"],
            capture_output=True,
            text=True,
        )
        details = (create.stdout + "\n" + create.stderr).strip()
        raise GitError(
            "Creating the worker worktree failed:\n"
            + details
            + "\nA partial worktree may have been registered; 'git worktree "
            f"prune' was run. If the folder '{worktree_path}' still exists, "
            "remove it manually before retrying."
        )

    created_root = Path(
        run_git(
            ["-C", str(worktree_path), "rev-parse", "--show-toplevel"],
            "Verification failed: the created worktree root could not be read.",
        )
    ).resolve()
    if str(created_root).lower() != str(worktree_path).lower():
        raise GitError(
            f"Verification failed: expected worktree root '{worktree_path}', "
            f"got '{created_root}'."
        )
    created_branch = run_git(
        ["-C", str(worktree_path), "branch", "--show-current"],
        "Verification failed: the created branch could not be read.",
    )
    if created_branch != worker_branch:
        raise GitError(
            f"Verification failed: expected branch '{worker_branch}', got "
            f"'{created_branch}'."
        )
    created_status = run_git(
        ["-C", str(worktree_path), "status", "--porcelain=v1", "--untracked-files=no"],
        "Verification failed: the created worktree status could not be read.",
    )
    if created_status:
        raise GitError(
            "Verification failed: the created worktree has tracked changes."
        )

    # Register the worker and protect its branch. Only names go into the
    # config - worktree paths are machine-specific and derived at runtime.
    if not any(
        isinstance(entry, dict) and entry.get("name") == worker
        for entry in config["workers"]
    ):
        config["workers"].append({"name": worker, "branch": worker_branch})
    if worker_branch not in config["protectedBranches"]:
        config["protectedBranches"].append(worker_branch)
    try:
        save_config(config_path, config)
    except OSError as error:
        raise GitError(
            f"The worktree '{worktree_path}' was created successfully, but "
            f"writing '{config_path}' failed ({error}). Add "
            f"'{worker_branch}' to 'protectedBranches' there manually; until "
            "then the branch stays protected by its '-workbench' name."
        )

    result = {
        "status": "success",
        "originalRepoPath": str(repo_root),
        "originalRepoName": repo_name,
        "originalBranch": base_branch,
        "workerName": worker,
        "workerWorktreePath": str(worktree_path),
        "workerWorktreeName": worktree_path.name,
        "workerBranch": worker_branch,
        "configPath": str(config_path),
    }
    print()
    print("WORKER_WORKTREE_RESULT_BEGIN")
    print(json.dumps(result, ensure_ascii=False))
    print("WORKER_WORKTREE_RESULT_END")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GitError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
