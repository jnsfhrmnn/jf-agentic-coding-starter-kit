#!/usr/bin/env python3
"""Update the local default branch strictly by fast-forward from origin.

Safety contract:
- never switches the branch;
- never creates a merge commit (`--ff-only` only);
- refuses to run with uncommitted tracked changes (untracked files are fine);
- stops with the MERGE-COMMIT-GATE marker (exit code 2) when the incoming
  range contains no merge commit, because the expected workflow is a
  pull-request merge into the default branch. A direct push, squash merge,
  or rebase merge must be confirmed deliberately with
  `--allow-non-merge-ff`.

Exit codes: 0 success or already up to date, 1 blocked/error, 2 gate.
"""

from __future__ import annotations

import argparse
import subprocess
import sys


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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default=None,
        help="Base branch to update (default: local 'main', else 'master').",
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
            f"Expected branch '{base}'. Nothing was changed."
        )
    if branch != base:
        raise GitError(
            f"Blocked: the current branch is '{branch}', not '{base}'. "
            "This tool never switches branches. Nothing was pulled."
        )
    print(f"Current branch: {branch}\n")

    # Only tracked changes block the fast-forward. Untracked files do not
    # prevent an ff-pull and are deliberately ignored.
    porcelain = run_git(
        ["-C", repo, "status", "--porcelain=v1", "--untracked-files=no"],
        "Blocked: the working-tree status could not be read.",
    )
    if porcelain:
        raise GitError(
            "Blocked: the working tree has uncommitted tracked changes. "
            "Commit or set them aside first. Nothing was pulled.\n" + porcelain
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
    print(f"Fetching origin/{base} ...")
    run_git(
        ["-C", repo, "fetch", "origin", base],
        f"Blocked: 'git fetch origin {base}' failed. Nothing was changed.",
    )
    fetch_head = run_git(
        ["-C", repo, "rev-parse", "FETCH_HEAD"],
        "Blocked: FETCH_HEAD could not be read after the fetch.",
    )

    incoming = int(
        run_git(
            ["-C", repo, "rev-list", "--count", f"{head_before}..{fetch_head}"],
            "Blocked: the incoming commits could not be determined.",
        )
    )
    ahead = int(
        run_git(
            ["-C", repo, "rev-list", "--count", f"{fetch_head}..{head_before}"],
            "Blocked: the local-ahead commits could not be determined.",
        )
    )
    if incoming == 0:
        if ahead > 0:
            print(
                f"Done: nothing to pull, but note - the local '{base}' is "
                f"{ahead} commit(s) AHEAD of origin/{base} (unpushed local "
                "work). Nothing was changed."
            )
        else:
            print(
                f"Done: '{base}' was already up to date "
                f"(HEAD {head_before[:12]} == origin/{base}). Nothing was changed."
            )
        return 0

    if not git_succeeds(
        ["-C", repo, "merge-base", "--is-ancestor", head_before, fetch_head]
    ):
        raise GitError(
            f"Blocked: '{base}' and 'origin/{base}' have diverged - no "
            "fast-forward is possible. No merge commit was created and no "
            "branch was switched. Inspect the divergence manually."
        )

    merge_commits = int(
        run_git(
            ["-C", repo, "rev-list", "--merges", "--count", f"{head_before}..{fetch_head}"],
            "Blocked: the merge-commit check failed.",
        )
    )
    if merge_commits == 0 and not args.allow_non_merge_ff:
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

    print("Applying fast-forward (git merge --ff-only FETCH_HEAD) ...")
    run_git(
        ["-C", repo, "merge", "--ff-only", "FETCH_HEAD"],
        "Blocked: 'git merge --ff-only' failed. No merge commit was created "
        "and no branch was switched.",
    )
    head_after = run_git(
        ["-C", repo, "rev-parse", "HEAD"],
        "The fast-forward succeeded, but the new HEAD could not be read.",
    )

    note = (
        f"{merge_commits} merge commit(s) included"
        if merge_commits > 0
        else "WITHOUT a merge commit - confirmed via --allow-non-merge-ff"
    )
    print(
        f"Done: '{base}' updated strictly by fast-forward - "
        f"{head_before[:12]} -> {head_after[:12]} "
        f"({incoming} new commits, {note})."
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except GitError as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
