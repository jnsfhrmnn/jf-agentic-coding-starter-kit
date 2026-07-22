#!/usr/bin/env python3
"""Lightweight second-session guard for one working copy.

Two agent sessions sharing one working copy share files, index, and HEAD -
a known source of corrupted work. This guard implements the timestamp
lockfile pattern: the first session claims `.csk/session.lock` (gitignored);
a second session sees the fresh lock, is warned, and is routed to a
dedicated worker worktree instead of silently continuing.

Commands:
  check                 report lock state: free / active / stale
  claim [--label NAME]  claim or refresh the lock; refuses a fresh foreign
                        lock unless --takeover is given
  release               remove the lock

The lock is advisory and identifies sessions only by label: a claim with the
same label refreshes silently, so two sessions using an identical label do
not detect each other. Use one distinct label per session (e.g. the agent
name plus a suffix for a second same-agent session). Staleness (default 360
minutes) decides whether a lock still counts as active; a crashed session
therefore never blocks a working copy forever. Exit codes: 0 ok/free/stale,
2 = a fresh lock is present (`check`: any fresh lock; `claim`: a fresh lock
with a different label), 1 error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

LOCK_RELATIVE = Path(".csk") / "session.lock"
DEFAULT_STALE_MINUTES = 360


def repo_root() -> Path:
    import subprocess

    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        print(
            "Error: the current directory is not inside a Git repository.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    return Path(result.stdout.strip()).resolve()


def read_lock(lock_path: Path) -> dict | None:
    if not lock_path.is_file():
        return None
    try:
        data = json.loads(lock_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return {"label": "unreadable", "claimed_at": None}
    return data if isinstance(data, dict) else {"label": "unreadable", "claimed_at": None}


def lock_age_minutes(lock: dict) -> float | None:
    claimed_at = lock.get("claimed_at")
    if not isinstance(claimed_at, str):
        return None
    try:
        stamp = datetime.fromisoformat(claimed_at)
    except ValueError:
        return None
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    return (datetime.now(timezone.utc) - stamp).total_seconds() / 60.0


def write_lock(lock_path: Path, label: str) -> None:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "label": label,
        "pid": os.getpid(),
        "claimed_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    fd, temp_name = tempfile.mkstemp(
        dir=str(lock_path.parent), prefix=".session-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_name, lock_path)
    except OSError:
        try:
            os.unlink(temp_name)
        except OSError:
            pass
        raise


def describe(lock: dict, age: float | None, stale_minutes: int) -> str:
    label = lock.get("label") or "unknown"
    if age is None:
        return f"lock by '{label}' with unreadable timestamp (treated as stale)"
    state = "stale" if age >= stale_minutes else "active"
    return f"{state} lock by '{label}', claimed {age:.0f} minute(s) ago"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "claim", "release"])
    parser.add_argument(
        "--label",
        default="agent-session",
        help="Session label stored in the lock (e.g. 'claude', 'codex').",
    )
    parser.add_argument(
        "--stale-minutes",
        type=int,
        default=DEFAULT_STALE_MINUTES,
        help="Age in minutes after which a lock no longer counts as active.",
    )
    parser.add_argument(
        "--takeover",
        action="store_true",
        help="Claim even over a fresh foreign lock (only after the user "
        "confirmed no second session is running).",
    )
    args = parser.parse_args(argv)

    lock_path = repo_root() / LOCK_RELATIVE
    lock = read_lock(lock_path)
    age = lock_age_minutes(lock) if lock else None
    is_active = lock is not None and age is not None and age < args.stale_minutes

    if args.command == "check":
        if lock is None:
            print("SESSION-GUARD: free - no other session holds this working copy.")
            return 0
        print(f"SESSION-GUARD: {describe(lock, age, args.stale_minutes)}.")
        return 2 if is_active else 0

    if args.command == "claim":
        if is_active and lock.get("label") != args.label and not args.takeover:
            print(
                "SESSION-GUARD: SECOND SESSION DETECTED - "
                + describe(lock, age, args.stale_minutes)
                + ". Two sessions on one working copy share files, index, and "
                "HEAD. Recommended: give this session its own worker worktree "
                "(create-worker-worktree). To continue here anyway, rerun "
                "with --takeover after confirming no other session is active."
            )
            return 2
        write_lock(lock_path, args.label)
        print(f"SESSION-GUARD: claimed for '{args.label}'.")
        return 0

    # release
    if lock is None:
        print("SESSION-GUARD: nothing to release.")
        return 0
    try:
        lock_path.unlink()
    except OSError as error:
        print(f"Error: could not release the lock: {error}", file=sys.stderr)
        return 1
    print("SESSION-GUARD: released.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
