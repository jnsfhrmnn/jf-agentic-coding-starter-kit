#!/usr/bin/env python3
"""Context-sensitive safe sync with origin - one command for both sides.

The user intention is identical everywhere ("bring me up to date with
origin/<base>"); only the context decides the mechanics. The mode is
detected from the current branch:

- Mode A - on the default branch (main/master): update it strictly by
  fast-forward from origin. Never switches the branch, never creates a
  merge commit.
- Mode B - on a protected worker branch (name ends in `-workbench`, or
  listed in `.csk/worktrees.json`): re-sync the branch onto the new
  origin/<base> (`merge --ff-only`), then fast-forward-push the branch so
  the remote ref follows - this also restores a remote ref that the host
  auto-deleted after the pull-request merge.
- A protected branch with local commits that are not on origin/<base> is
  blocked fail-closed: integrate through a pull request first
  (finish-branch), then re-sync. No silent merge.
- Any other branch: blocked without changes.

Both modes refuse uncommitted tracked changes (untracked files are fine)
and both apply the MERGE-COMMIT-GATE (exit code 2): when the incoming
range contains no merge commit, the commits did not arrive through a
pull-request merge and must be confirmed deliberately with
`--allow-non-merge-ff`.

Exit codes: 0 success or already up to date, 1 blocked/error, 2 gate.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


class GitError(RuntimeError):
    """A git command failed; the message is already user-readable."""


def run_git(args: list[str], failure: str) -> str:
    """Run git and return stdout. Git writes progress to stderr even on
    success, so success is judged only by the exit code."""
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
    """Exit-code probe for commands where a non-zero code is a valid 'no'."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.returncode == 0


def detect_base_branch(repo: str, requested: str | None) -> str:
    if requested:
        if not git_succeeds(
            ["-C", repo, "show-ref", "--verify", "--quiet", f"refs/heads/{requested}"]
        ):
            raise GitError(
                f"Blocked: the requested base branch '{requested}' does not exist "
                "locally. Nothing was changed."
            )
        return requested
    for candidate in ("main", "master"):
        if git_succeeds(
            ["-C", repo, "show-ref", "--verify", "--quiet", f"refs/heads/{candidate}"]
        ):
            return candidate
    raise GitError(
        "Blocked: neither a local 'main' nor 'master' branch exists. "
        "Nothing was changed."
    )


def protected_branches(repo: str) -> set[str]:
    """Branch names protected via .csk/worktrees.json (name rule is separate)."""
    config_path = Path(repo) / ".csk" / "worktrees.json"
    if not config_path.is_file():
        return set()
    try:
        config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return set()
    if not isinstance(config, dict):
        return set()
    names: set[str] = set()
    listed = config.get("protectedBranches")
    if isinstance(listed, list):
        names.update(n for n in listed if isinstance(n, str))
    workers = config.get("workers")
    if isinstance(workers, list):
        for entry in workers:
            if isinstance(entry, dict) and isinstance(entry.get("branch"), str):
                names.add(entry["branch"])
    return names


def is_protected(branch: str, repo: str) -> bool:
    return branch.endswith("-workbench") or branch in protected_branches(repo)


def count_range(repo: str, spec: str, merges_only: bool = False) -> int:
    args = ["-C", repo, "rev-list", "--count"]
    if merges_only:
        args.insert(3, "--merges")
    return int(run_git(args + [spec], "Blocked: commit counting failed."))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=None,
        help="Base branch to sync from (default: local 'main', else 'master').",
    )
    parser.add_argument(
        "--allow-non-merge-ff",
        action="store_true",
        help=(
            "Deliberately fast-forward even when the incoming range contains "
            "no merge commit (direct push, squash merge, or rebase merge)."
        ),
    )
    args = parser.parse_args(argv)

    repo = run_git(
        ["rev-parse", "--show-toplevel"],
        "Blocked: the current directory is not inside a Git repository.",
    )
    print(f"Repository: {repo}\n")

    base = detect_base_branch(repo, args.base)

    branch = run_git(
        ["-C", repo, "branch", "--show-current"],
        "Blocked: the current branch could not be read.",
    )
    if not branch:
        raise GitError(
            "Blocked: the repository is in detached-HEAD state. "
            "This tool never switches branches. Nothing was changed."
        )

    if branch == base:
        mode = "A"
        print(f"Context: default branch '{base}' - fast-forward pull mode.\n")
    elif is_protected(branch, repo):
        mode = "B"
        print(
            f"Context: protected worker branch '{branch}' - re-sync mode "
            f"(onto origin/{base}).\n"
        )
    else:
        raise GitError(
            f"Blocked: the current branch is '{branch}' - neither the default "
            f"branch '{base}' nor a protected worker branch (*-workbench or "
            "listed in .csk/worktrees.json). This tool never switches "
            "branches. Nothing was changed."
        )

    # Only tracked changes block the sync. Untracked files do not prevent a
    # fast-forward and are deliberately ignored.
    porcelain = run_git(
        ["-C", repo, "status", "--porcelain=v1", "--untracked-files=no"],
        "Blocked: the working-tree status could not be read.",
    )
    if porcelain:
        raise GitError(
            "Blocked: the working tree has uncommitted tracked changes. "
            "Commit or set them aside first. Nothing was changed.\n" + porcelain
        )

    run_git(
        ["-C", repo, "remote", "get-url", "origin"],
        "Blocked: the remote 'origin' is not configured.",
    )

    head_before = run_git(
        ["-C", repo, "rev-parse", "HEAD"],
        "Blocked: the current commit (HEAD) could not be read.",
    )

    # Step 1: fetch only. The working tree does not move yet, which allows
    # inspecting the incoming commits BEFORE the fast-forward (merge gate).
    # The target commit is then pinned as an exact SHA: FETCH_HEAD lives in
    # the SHARED .git of all worktrees, so a concurrent fetch from another
    # session (the normal level-3 setup) could change it between inspection
    # and merge. Pinning the SHA makes gate and merge act on the same commit.
    print(f"Fetching origin/{base} ...")
    run_git(
        ["-C", repo, "fetch", "origin", base],
        f"Blocked: 'git fetch origin {base}' failed. Nothing was changed.",
    )
    if git_succeeds(
        ["-C", repo, "rev-parse", "--verify", f"refs/remotes/origin/{base}"]
    ):
        fetch_head = run_git(
            ["-C", repo, "rev-parse", f"refs/remotes/origin/{base}"],
            "Blocked: the fetched origin state could not be read.",
        )
    else:
        fetch_head = run_git(
            ["-C", repo, "rev-parse", "FETCH_HEAD"],
            "Blocked: FETCH_HEAD could not be read after the fetch.",
        )

    incoming = count_range(repo, f"{head_before}..{fetch_head}")
    outgoing = count_range(repo, f"{fetch_head}..{head_before}")

    if mode == "B" and outgoing > 0:
        raise GitError(
            f"Blocked: the worker branch '{branch}' has {outgoing} local "
            f"commit(s) that are not on origin/{base} yet. Integrate that "
            "work through a pull request first (finish-branch), THEN "
            "re-sync. No silent merge was performed. Nothing was changed."
        )

    if mode == "A" and incoming == 0:
        if outgoing > 0:
            print(
                f"Done: nothing to pull, but note - the local '{base}' is "
                f"{outgoing} commit(s) AHEAD of origin/{base} (unpushed local "
                "work). Nothing was changed."
            )
        else:
            print(
                f"Done: '{base}' was already up to date "
                f"(HEAD {head_before[:12]} == origin/{base}). Nothing was changed."
            )
        return 0

    if mode == "A" and outgoing > 0:
        raise GitError(
            f"Blocked: '{base}' and 'origin/{base}' have diverged - no "
            "fast-forward is possible. No merge commit was created and no "
            "branch was switched. Inspect the divergence manually."
        )

    merge_commits = count_range(
        repo, f"{head_before}..{fetch_head}", merges_only=True
    )
    if incoming > 0 and merge_commits == 0 and not args.allow_non_merge_ff:
        print("=== MERGE-COMMIT-GATE: confirmation required - NOTHING was changed ===")
        print(
            f"The incoming fast-forward covers {incoming} commit(s) but contains "
            "NO merge commit."
        )
        print(
            "Expected workflow: a feature or worker branch is merged into "
            f"'{base}' through a pull request, which creates a merge commit."
        )
        print(
            "No merge commit points to a direct push, a squash merge, or a "
            "rebase merge.\n"
        )
        print(f"Incoming commits (HEAD..origin/{base}):")
        print(
            run_git(
                [
                    "-C",
                    repo,
                    "log",
                    "--oneline",
                    "--max-count=30",
                    f"{head_before}..{fetch_head}",
                ],
                "The incoming commits could not be listed.",
            )
        )
        print(
            "\nTo continue deliberately, rerun this script with "
            "--allow-non-merge-ff."
        )
        return 2

    if incoming > 0:
        print(f"Applying fast-forward (git merge --ff-only {fetch_head[:12]}) ...")
        run_git(
            ["-C", repo, "merge", "--ff-only", fetch_head],
            "Blocked: 'git merge --ff-only' failed. No merge commit was "
            "created and no branch was switched.",
        )
    head_after = run_git(
        ["-C", repo, "rev-parse", "HEAD"],
        "The sync succeeded, but the new HEAD could not be read.",
    )

    note = (
        f"{merge_commits} merge commit(s) included"
        if merge_commits > 0
        else "WITHOUT a merge commit - confirmed via --allow-non-merge-ff"
        if incoming > 0
        else "no new commits"
    )

    if mode == "A":
        print(
            f"Done: '{base}' updated strictly by fast-forward - "
            f"{head_before[:12]} -> {head_after[:12]} "
            f"({incoming} new commits, {note})."
        )
        return 0

    # Mode B: fast-forward-push the worker branch so the remote ref follows.
    # This is a plain push (never force) and also restores a remote ref the
    # host auto-deleted after the pull-request merge.
    remote_ref_before = run_git(
        ["-C", repo, "ls-remote", "--heads", "origin", f"refs/heads/{branch}"],
        "The remote refs could not be listed.",
    )
    push = subprocess.run(
        ["git", "-C", repo, "push", "origin", branch],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if push.returncode != 0:
        details = (push.stdout + "\n" + push.stderr).strip()
        raise GitError(
            f"The local re-sync succeeded ('{branch}' is now at "
            f"{head_after[:12]} == origin/{base}), but pushing the branch "
            f"failed:\n{details}\nNothing local was lost - rerun once the "
            "remote is reachable to update the remote ref."
        )
    remote_ref_after = run_git(
        ["-C", repo, "ls-remote", "--heads", "origin", f"refs/heads/{branch}"],
        "The remote ref could not be verified after the push.",
    )
    if head_after not in remote_ref_after:
        raise GitError(
            f"The push reported success, but 'origin/{branch}' does not show "
            f"the expected tip {head_after[:12]}. Verify the remote manually."
        )
    healed = " (remote ref restored - it had been deleted)" if not remote_ref_before else ""
    if incoming > 0:
        print(
            f"Done: worker branch '{branch}' re-synced onto origin/{base} - "
            f"{head_before[:12]} -> {head_after[:12]} ({incoming} commits, "
            f"{note}) and the remote ref was updated{healed}."
        )
    else:
        print(
            f"Done: worker branch '{branch}' was already at origin/{base} "
            f"(HEAD {head_after[:12]}); remote ref verified{healed}. "
            "Nothing else was changed."
        )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GitError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
