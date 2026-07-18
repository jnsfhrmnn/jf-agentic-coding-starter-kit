#!/usr/bin/env python3
"""Deterministic, repository-local state and task operations for CSK Start."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse, urlunparse


MIN_PYTHON = (3, 10)
STATE_REL = Path(".csk/project-state.json")
TASKS_REL = Path("tasks/INDEX.md")
LOCK_REL = Path(".csk/csk-start.lock")
TASK_HEADER = (
    "| ID | Status | Priority | Related | Expected branch | Resume skill | "
    "Task | Next action | Blocker | Updated |"
)
TASK_SEPARATOR = "|---|---|---|---|---|---|---|---|---|---|"
NEXT_ID_RE = re.compile(r"<!--\s*next-id:\s*TASK-(\d{3,})\s*-->")
TASK_ID_RE = re.compile(r"^TASK-(\d{3,})$")
SKILL_RE = re.compile(r"^(?:[a-z0-9]+(?:-[a-z0-9]+)*|direct|n/a)$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
EVIDENCE_RE = re.compile(r"^(?:commit|file|test|url|artifact):\S.*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FEATURE_ID_RE = re.compile(r"^PROJ-\d+$")
FEATURE_ROW_RE = re.compile(r"^\|\s*(PROJ-\d+)\s*\|", re.MULTILINE)
TASK_ROW_RE = re.compile(r"^\s*\|\s*TASK-[^|]+\|")
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_STATUSES = {"open", "blocked"}
STATE_COMBINATIONS = {
    ("pending", "not-assessed"),
    ("greenfield", "not-applicable"),
    ("adopt", "pending"),
    ("adopt", "complete"),
    ("adopt", "blocked"),
}
SOURCE_REMOTE_MARKERS = ("alexpeclub/ai-coding-starter-kit",)
INITIAL_TEMPLATE_STATE = {
    "schema_version": 1,
    "repository_role": "template",
    "onboarding": {
        "mode": "pending",
        "adoption_status": "not-assessed",
        "decided_at": None,
        "scaffold_evidence": None,
    },
}

KIT_EXCLUDED_PREFIXES = (
    ".git/",
    ".claude/",
    ".codex/",
    ".csk/",
    "tasks/",
    "docs/production/",
    "docs/kit-history/",
)
KIT_EXCLUDED_FILES = {
    "AGENTS.md",
    "CHANGELOG.md",
    "CLAUDE.md",
    "LICENSE",
    "README.md",
    "UPSTREAM.md",
    "docs/audits/2026-07-10-csk-kit-fix-round.md",
    "docs/audits/2026-07-10-open-large-goal-audit.md",
    "docs/audits/2026-07-11-skill-consolidation.md",
    "docs/plans/2026-07-18-csk-workflow-hardening.md",
    "features/README.md",
}
CODE_SUFFIXES = {
    ".c", ".cc", ".cpp", ".cs", ".go", ".h", ".hpp", ".java", ".js",
    ".jsx", ".kt", ".kts", ".lua", ".m", ".mm", ".php", ".ps1", ".py",
    ".rb", ".rs", ".sh", ".swift", ".ts", ".tsx", ".vue", ".svelte",
}
MANIFEST_NAMES = {
    "CMakeLists.txt", "Cargo.toml", "Gemfile", "Makefile", "Package.swift",
    "build.gradle", "build.gradle.kts", "composer.json", "go.mod", "package.json",
    "pom.xml", "pyproject.toml", "requirements.txt",
}
EVIDENCE_NAME_RE = re.compile(
    r"(?:^|[-_. /])(architecture|audit|backlog|brief|plan|prd|requirements|roadmap|"
    r"feature|features|spec|strategy|vision|workflow)(?:[-_. /]|$)",
    re.IGNORECASE,
)


class CskError(RuntimeError):
    """Fail-closed validation or mutation error."""


def validate_runtime(version: tuple[int, int] | None = None) -> None:
    current = version or (sys.version_info.major, sys.version_info.minor)
    if current < MIN_PYTHON:
        raise CskError(
            f"CSK tooling requires Python {MIN_PYTHON[0]}.{MIN_PYTHON[1]}+; "
            f"found {current[0]}.{current[1]}"
        )


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _today() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _validate_timestamp(value: Any, field: str) -> None:
    if not isinstance(value, str):
        raise CskError(f"{field} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CskError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise CskError(f"{field} must include a timezone")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _run_git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _display_remote_url(value: str | None) -> str | None:
    if not value or "://" not in value:
        return value
    parsed = urlparse(value)
    hostname = parsed.hostname or ""
    try:
        port = parsed.port
    except ValueError:
        port = None
    if port:
        hostname = f"{hostname}:{port}"
    return urlunparse((parsed.scheme, hostname, parsed.path, "", "", ""))


def resolve_repo(start: Path) -> Path:
    candidate = start.resolve()
    result = _run_git(candidate, "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        raise CskError(f"Not a Git repository: {candidate}")
    repo = Path(result.stdout.strip()).resolve()
    if not (repo / ".claude" / "skills" / "csk-start" / "SKILL.md").is_file():
        raise CskError(f"Repository-local csk-start skill is missing: {repo}")
    return repo


def safe_path(repo: Path, relative: Path, *, must_exist: bool = False) -> Path:
    if relative.is_absolute():
        raise CskError(f"Absolute paths are not allowed: {relative}")
    if ".." in relative.parts:
        raise CskError(f"Parent traversal is not allowed: {relative}")
    lexical = repo
    for part in relative.parts:
        if part in {"", "."}:
            continue
        lexical /= part
        if lexical.is_symlink():
            raise CskError(f"Symlink paths are not accepted for CSK state: {relative.as_posix()}")
    candidate = lexical.resolve(strict=False)
    try:
        candidate.relative_to(repo)
    except ValueError as exc:
        raise CskError(f"Path escapes repository: {relative}") from exc
    if must_exist and not candidate.exists():
        raise CskError(f"Required repository path is missing: {relative.as_posix()}")
    return candidate


@contextmanager
def repository_lock(repo: Path) -> Iterable[None]:
    lock_path = safe_path(repo, LOCK_REL)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError as exc:
        raise CskError(
            f"Another CSK state mutation is active or left a lock: {LOCK_REL.as_posix()}"
        ) from exc
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps({"pid": os.getpid(), "created_at": _now()}) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        yield
    finally:
        try:
            lock_path.unlink()
        except FileNotFoundError:
            pass


def read_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise CskError(f"Cannot read {path}: {exc}") from exc


def durable_replace(repo: Path, target: Path, content: bytes, expected_digest: str) -> None:
    if _sha256(read_bytes(target)) != expected_digest:
        raise CskError(f"Concurrent change detected; refusing to overwrite {target.relative_to(repo)}")
    temp_root = safe_path(repo, Path(".csk"))
    temp_root.mkdir(parents=True, exist_ok=True)
    descriptor, temp_name = tempfile.mkstemp(prefix="csk-start-", suffix=".tmp", dir=temp_root)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        if _sha256(read_bytes(target)) != expected_digest:
            raise CskError(f"Concurrent change detected before replace: {target.relative_to(repo)}")
        os.replace(temp_path, target)
        if os.name != "nt":
            directory_fd = os.open(target.parent, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


def load_state(repo: Path) -> tuple[dict[str, Any], bytes]:
    path = safe_path(repo, STATE_REL, must_exist=True)
    raw = read_bytes(path)
    try:
        state = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CskError(f"Malformed {STATE_REL.as_posix()}: {exc}") from exc
    validate_state(repo, state)
    return state, raw


def load_state_snapshot(repo: Path, snapshot: str) -> dict[str, Any]:
    if snapshot == "HEAD":
        spec = f"HEAD:{STATE_REL.as_posix()}"
    elif snapshot == "index":
        tracked = _run_git(repo, "ls-files", "--error-unmatch", "--", STATE_REL.as_posix())
        if tracked.returncode != 0:
            raise CskError(f"Distribution state is not tracked in the Git index: {STATE_REL.as_posix()}")
        spec = f":{STATE_REL.as_posix()}"
    else:
        raise CskError(f"Unsupported distribution snapshot: {snapshot}")
    result = _run_git(repo, "show", spec)
    if result.returncode != 0:
        raise CskError(f"Distribution state is missing from Git snapshot {snapshot}: {STATE_REL.as_posix()}")
    try:
        state = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CskError(f"Malformed distribution state in Git snapshot {snapshot}: {exc}") from exc
    validate_state(repo, state)
    return state


def validate_coverage_report(repo: Path, relative: Path) -> dict[str, Any]:
    report_path = safe_path(repo, relative, must_exist=True)
    if not report_path.is_file():
        raise CskError("Adoption coverage report must be a file")
    try:
        report = json.loads(read_bytes(report_path).decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CskError(f"Malformed adoption coverage report: {exc}") from exc
    if not isinstance(report, dict) or report.get("schema_version") != 1:
        raise CskError("Adoption coverage report schema_version must be 1")
    feature_value = report.get("feature_index")
    if not isinstance(feature_value, str) or not feature_value.strip():
        raise CskError("Adoption coverage report requires feature_index")
    feature_relative = Path(feature_value)
    feature_path = safe_path(repo, feature_relative, must_exist=True)
    if not feature_path.is_file():
        raise CskError("Adoption feature index must be a file")
    feature_text = feature_path.read_text(encoding="utf-8-sig", errors="replace")
    feature_ids = set(FEATURE_ROW_RE.findall(feature_text))
    if not feature_ids:
        raise CskError("Adoption feature index requires at least one PROJ row")

    sources = report.get("sources")
    if not isinstance(sources, list) or not sources:
        raise CskError("Adoption coverage report requires at least one mapped source")
    source_paths: set[str] = set()
    source_records: dict[str, dict[str, Any]] = {}
    for index, source in enumerate(sources, start=1):
        if not isinstance(source, dict):
            raise CskError(f"Coverage source {index} must be an object")
        source_value = source.get("path")
        if not isinstance(source_value, str) or not source_value.strip():
            raise CskError(f"Coverage source {index} requires path")
        source_path = safe_path(repo, Path(source_value), must_exist=True)
        if not source_path.is_file():
            raise CskError(f"Coverage source is not a file: {source_value}")
        canonical = source_path.relative_to(repo).as_posix()
        if canonical in source_paths:
            raise CskError(f"Duplicate coverage source: {canonical}")
        source_paths.add(canonical)
        source_records[canonical] = source
        mapped_ids = source.get("feature_ids")
        non_feature = source.get("non_feature_reason")
        has_features = isinstance(mapped_ids, list) and bool(mapped_ids)
        has_reason = isinstance(non_feature, str) and bool(non_feature.strip())
        if has_features == has_reason:
            raise CskError(
                f"Coverage source {canonical} requires feature_ids or non_feature_reason, exclusively"
            )
        if has_features:
            if any(not isinstance(item, str) or not FEATURE_ID_RE.fullmatch(item) for item in mapped_ids):
                raise CskError(f"Coverage source {canonical} has invalid feature_ids")
            if len(mapped_ids) != len(set(mapped_ids)):
                raise CskError(f"Coverage source {canonical} has duplicate feature_ids")
            missing_features = sorted(set(mapped_ids) - feature_ids)
            if missing_features:
                raise CskError(
                    f"Coverage source {canonical} references missing features: {', '.join(missing_features)}"
                )

    candidates = {
        item["path"] for item in inventory(repo)["candidates"]
        if item["path"] != feature_path.relative_to(repo).as_posix()
    }
    missing_sources = sorted(candidates - source_paths)
    if missing_sources:
        raise CskError(
            "Adoption coverage is incomplete; unmapped inventory candidates: "
            + ", ".join(missing_sources)
        )
    for extra_source in sorted(source_paths - candidates):
        reason = source_records[extra_source].get("manual_relevance_reason")
        if not isinstance(reason, str) or not reason.strip():
            raise CskError(
                f"Non-inventory coverage source requires manual_relevance_reason: {extra_source}"
            )
    inventory_digest = _sha256("\n".join(sorted(candidates)).encode("utf-8"))
    return {
        "coverage_report": report_path.relative_to(repo).as_posix(),
        "coverage_sha256": _sha256(read_bytes(report_path)),
        "feature_index": feature_path.relative_to(repo).as_posix(),
        "source_count": len(sources),
        "mapped_count": len(sources),
        "inventory_sha256": inventory_digest,
    }


def validate_state(repo: Path, state: dict[str, Any]) -> None:
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        raise CskError("project-state schema_version must be 1")
    role = state.get("repository_role")
    if role not in {"template", "project"}:
        raise CskError("repository_role must be template or project")
    onboarding = state.get("onboarding")
    if not isinstance(onboarding, dict):
        raise CskError("onboarding must be an object")
    mode = onboarding.get("mode")
    adoption = onboarding.get("adoption_status")
    if (mode, adoption) not in STATE_COMBINATIONS:
        raise CskError(f"Invalid onboarding state combination: {mode}/{adoption}")
    if role == "template" and (mode, adoption) != ("pending", "not-assessed"):
        raise CskError("template repositories must remain pending/not-assessed")
    decided_at = onboarding.get("decided_at")
    if mode == "pending" and decided_at is not None:
        raise CskError("pending onboarding must not have decided_at")
    if mode != "pending" and not isinstance(decided_at, str):
        raise CskError("completed first-open decisions require decided_at")
    if isinstance(decided_at, str):
        _validate_timestamp(decided_at, "decided_at")
    evidence = onboarding.get("scaffold_evidence")
    if adoption == "complete":
        if not isinstance(evidence, dict):
            raise CskError("adopt/complete requires scaffold_evidence")
        required = {
            "coverage_report", "coverage_sha256", "feature_index",
            "source_count", "mapped_count", "inventory_sha256", "verified_at",
        }
        if not required.issubset(evidence):
            raise CskError("scaffold_evidence is incomplete")
        if (
            type(evidence["source_count"]) is not int
            or type(evidence["mapped_count"]) is not int
            or evidence["source_count"] <= 0
            or evidence["source_count"] != evidence["mapped_count"]
        ):
            raise CskError("adopt/complete requires complete source mapping")
        _validate_timestamp(evidence["verified_at"], "scaffold_evidence.verified_at")
        safe_path(repo, Path(str(evidence["feature_index"])))
        safe_path(repo, Path(str(evidence["coverage_report"])))
        if not SHA256_RE.fullmatch(str(evidence["coverage_sha256"])):
            raise CskError("scaffold_evidence.coverage_sha256 is invalid")
        if not SHA256_RE.fullmatch(str(evidence["inventory_sha256"])):
            raise CskError("scaffold_evidence.inventory_sha256 is invalid")
    elif adoption == "blocked":
        if not isinstance(evidence, dict) or not isinstance(evidence.get("reason"), str):
            raise CskError("adopt/blocked requires a recorded reason")
        _clean_cell(evidence["reason"], "reason")
        _validate_timestamp(evidence.get("blocked_at"), "scaffold_evidence.blocked_at")
    elif evidence is not None and adoption not in {"blocked"}:
        raise CskError("scaffold_evidence is only valid for complete or blocked adoption")


def state_drift(repo: Path, state: dict[str, Any]) -> list[str]:
    onboarding = state["onboarding"]
    if onboarding["adoption_status"] != "complete":
        return []
    evidence = onboarding["scaffold_evidence"]
    feature_index = safe_path(
        repo,
        Path(str(evidence["feature_index"])),
    )
    report = safe_path(repo, Path(str(evidence["coverage_report"])))
    drift: list[str] = []
    if not feature_index.is_file():
        drift.append(f"Recorded adoption feature index is missing: {feature_index.relative_to(repo)}")
    if not report.is_file():
        drift.append(f"Recorded adoption coverage report is missing: {report.relative_to(repo)}")
    elif _sha256(read_bytes(report)) != evidence["coverage_sha256"]:
        drift.append(f"Recorded adoption coverage report changed: {report.relative_to(repo)}")
    return drift


def state_distribution(repo: Path) -> dict[str, Any]:
    state_path = STATE_REL.as_posix()
    dirty = _run_git(repo, "status", "--short", "--", state_path)
    commit_result = _run_git(repo, "log", "-1", "--format=%H", "--", state_path)
    commit = commit_result.stdout.strip() if commit_result.returncode == 0 else ""
    remotes = _run_git(repo, "remote").stdout.split()
    origin_url_result = _run_git(repo, "remote", "get-url", "origin")
    origin_url = origin_url_result.stdout.strip() if origin_url_result.returncode == 0 else None
    upstream_url_result = _run_git(repo, "remote", "get-url", "upstream")
    upstream_url = upstream_url_result.stdout.strip() if upstream_url_result.returncode == 0 else None
    default_ref = None
    symbolic = _run_git(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
    if symbolic.returncode == 0:
        default_ref = symbolic.stdout.strip()
    else:
        for candidate in ("refs/remotes/origin/main", "refs/remotes/origin/master"):
            exists = _run_git(repo, "show-ref", "--verify", "--quiet", candidate)
            if exists.returncode == 0:
                default_ref = candidate
                break
    origin_state_role = None
    if default_ref:
        remote_state = _run_git(repo, "show", f"{default_ref}:{state_path}")
        if remote_state.returncode == 0:
            try:
                remote_value = json.loads(remote_state.stdout)
                if isinstance(remote_value, dict):
                    origin_state_role = remote_value.get("repository_role")
            except json.JSONDecodeError:
                origin_state_role = None
    normalized_origin = (origin_url or "").lower().replace("\\", "/").removesuffix(".git")
    normalized_upstream = (upstream_url or "").lower().replace("\\", "/").removesuffix(".git")
    if not origin_url:
        origin_role = "missing"
    elif any(marker in normalized_origin for marker in SOURCE_REMOTE_MARKERS) or (
        normalized_upstream and normalized_origin == normalized_upstream
    ):
        origin_role = "source-template"
    elif origin_state_role == "project":
        origin_role = "project"
    elif origin_state_role == "template":
        origin_role = "unconfirmed-template"
    else:
        origin_role = "unconfirmed"
    reachable = False
    if commit and default_ref:
        reachable = _run_git(repo, "merge-base", "--is-ancestor", commit, default_ref).returncode == 0
    if dirty.stdout.strip():
        status = "uncommitted"
    elif reachable and origin_role == "project":
        status = "origin-default"
    elif "origin" not in remotes:
        status = "committed-local-no-origin"
    else:
        status = "committed-not-on-origin-default"
    return {
        "status": status,
        "state_commit": commit or None,
        "origin_default_ref": default_ref,
        "origin_url": _display_remote_url(origin_url),
        "origin_role": origin_role,
        "projectwide": reachable and origin_role == "project",
    }


def write_state(repo: Path, state: dict[str, Any], original: bytes) -> None:
    validate_state(repo, state)
    content = (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    durable_replace(repo, safe_path(repo, STATE_REL, must_exist=True), content, _sha256(original))


def inventory_paths(repo: Path) -> list[str]:
    result = _run_git(repo, "ls-files", "--cached", "--others", "--exclude-standard")
    if result.returncode == 0:
        return sorted({line.replace("\\", "/") for line in result.stdout.splitlines() if line.strip()})
    paths: list[str] = []
    for path in repo.rglob("*"):
        if path.is_file():
            paths.append(path.relative_to(repo).as_posix())
    return sorted(paths)


def is_kit_template(path: str, repo: Path) -> bool:
    if path in KIT_EXCLUDED_FILES or path.startswith(KIT_EXCLUDED_PREFIXES):
        return True
    if path in {"docs/PRD.md", "docs/master-feature.md", "docs/architecture.md", "features/INDEX.md"}:
        try:
            text = (repo / path).read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            return False
        template_markers = ("_Describe what", "Draft template", "Not chosen yet", "<!-- Add features")
        return any(marker in text for marker in template_markers)
    return False


def inventory(repo: Path) -> dict[str, Any]:
    candidates: list[dict[str, str]] = []
    for relative in inventory_paths(repo):
        if is_kit_template(relative, repo):
            continue
        path = Path(relative)
        if path.name in MANIFEST_NAMES or path.suffix.lower() in CODE_SUFFIXES:
            candidates.append({"path": relative, "class": "implementation"})
        elif EVIDENCE_NAME_RE.search(relative):
            candidates.append({"path": relative, "class": "project-evidence"})
    counts = {
        kind: sum(item["class"] == kind for item in candidates)
        for kind in ("implementation", "project-evidence")
    }
    return {"candidate_count": len(candidates), "counts": counts, "candidates": candidates}


def _clean_cell(value: str, field: str, *, allow_blank: bool = False) -> str:
    cleaned = value.strip()
    if not cleaned and not allow_blank:
        raise CskError(f"Task field {field} is required")
    if "|" in cleaned or "\n" in cleaned or "\r" in cleaned:
        raise CskError(f"Task field {field} contains an unsupported table character")
    return cleaned


def parse_tasks(raw: bytes) -> dict[str, Any]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise CskError(f"Malformed {TASKS_REL.as_posix()}: {exc}") from exc
    markers = list(NEXT_ID_RE.finditer(text))
    if len(markers) != 1:
        raise CskError("tasks index must contain exactly one next-id marker")
    lines = text.splitlines()
    header_indices = [index for index, line in enumerate(lines) if line.strip() == TASK_HEADER]
    if len(header_indices) != 1:
        raise CskError("tasks index must contain exactly one required table header")
    header_index = header_indices[0]
    if header_index + 1 >= len(lines) or lines[header_index + 1].strip() != TASK_SEPARATOR:
        raise CskError("tasks index separator does not match the required schema")
    rows: list[dict[str, str]] = []
    cursor = header_index + 2
    while cursor < len(lines) and lines[cursor].strip().startswith("|"):
        line = lines[cursor].strip()
        cells = [cell.strip() for cell in line[1:-1].split("|")]
        if len(cells) != 10:
            raise CskError(f"Task row {cursor + 1} must have exactly 10 cells")
        row = dict(zip(
            ("id", "status", "priority", "related", "expected_branch", "resume_skill", "task", "next_action", "blocker", "updated"),
            cells,
        ))
        rows.append(row)
        cursor += 1
    for index, line in enumerate(lines):
        if TASK_ROW_RE.match(line) and not (header_index + 2 <= index < cursor):
            raise CskError(f"Task-like row outside the task table at line {index + 1}")
    seen: set[str] = set()
    max_id = 0
    for row in rows:
        match = TASK_ID_RE.fullmatch(row["id"])
        if not match or row["id"] in seen:
            raise CskError(f"Invalid or duplicate task ID: {row['id']}")
        seen.add(row["id"])
        max_id = max(max_id, int(match.group(1)))
        if row["status"] not in VALID_STATUSES:
            raise CskError(f"Invalid task status for {row['id']}: {row['status']}")
        if row["priority"] not in VALID_PRIORITIES:
            raise CskError(f"Invalid task priority for {row['id']}: {row['priority']}")
        if not SKILL_RE.fullmatch(row["resume_skill"]):
            raise CskError(f"Invalid resume skill for {row['id']}: {row['resume_skill']}")
        if not DATE_RE.fullmatch(row["updated"]):
            raise CskError(f"Invalid Updated date for {row['id']}: {row['updated']}")
        try:
            datetime.strptime(row["updated"], "%Y-%m-%d")
        except ValueError as exc:
            raise CskError(f"Invalid Updated date for {row['id']}: {row['updated']}") from exc
        for field in ("related", "expected_branch", "task", "next_action"):
            _clean_cell(row[field], field)
        if row["status"] == "blocked" and row["blocker"] in {"", "-"}:
            raise CskError(f"Blocked task {row['id']} requires a blocker")
    next_id = int(markers[0].group(1))
    if next_id <= max_id or f"TASK-{next_id:03d}" in seen:
        raise CskError("next-id must be unused and greater than all task IDs")
    return {
        "text": text,
        "lines": lines,
        "header_index": header_index,
        "row_end": cursor,
        "rows": rows,
        "next_id": next_id,
    }


def render_tasks(parsed: dict[str, Any], rows: list[dict[str, str]], next_id: int) -> bytes:
    lines = list(parsed["lines"])
    rendered_rows = [
        "| " + " | ".join(
            row[key] for key in
            ("id", "status", "priority", "related", "expected_branch", "resume_skill", "task", "next_action", "blocker", "updated")
        ) + " |"
        for row in rows
    ]
    start = parsed["header_index"] + 2
    lines[start:parsed["row_end"]] = rendered_rows
    text = "\n".join(lines) + "\n"
    text, count = NEXT_ID_RE.subn(f"<!-- next-id: TASK-{next_id:03d} -->", text)
    if count != 1:
        raise CskError("Could not update the unique next-id marker")
    return text.encode("utf-8")


def validate_task_references(repo: Path, parsed: dict[str, Any]) -> None:
    for row in parsed["rows"]:
        resume_skill = row["resume_skill"]
        if resume_skill not in {"direct", "n/a"}:
            canonical = safe_path(
                repo,
                Path(".claude") / "skills" / resume_skill / "SKILL.md",
                must_exist=True,
            )
            proxy = safe_path(
                repo,
                Path(".codex") / "skills" / resume_skill / "SKILL.md",
                must_exist=True,
            )
            if not canonical.is_file() or not proxy.is_file():
                raise CskError(
                    f"Resume skill for {row['id']} requires canonical Claude skill and Codex proxy: {resume_skill}"
                )
        related = row["related"]
        if related not in {"none", "n/a"} and ("/" in related or "\\" in related or "." in Path(related).name):
            target = safe_path(repo, Path(related), must_exist=True)
            if not target.is_file():
                raise CskError(f"Related path for {row['id']} is not a file: {related}")
        expected = row["expected_branch"]
        if expected not in {"n/a", "any"}:
            checked = _run_git(repo, "check-ref-format", "--branch", expected)
            if checked.returncode != 0:
                raise CskError(f"Invalid expected branch for {row['id']}: {expected}")


def verify_closure_evidence(repo: Path, evidence: str, evidence_record: str | None) -> dict[str, str]:
    if not EVIDENCE_RE.fullmatch(evidence):
        raise CskError("Closure evidence must use commit:, file:, test:, url:, or artifact:")
    kind, value = evidence.split(":", 1)
    result = {"evidence": evidence}
    if kind == "commit":
        verified = _run_git(repo, "rev-parse", "--verify", "--quiet", f"{value}^{{commit}}")
        if verified.returncode != 0:
            raise CskError(f"Closure commit does not exist: {value}")
        result["resolved"] = verified.stdout.strip()
    elif kind in {"file", "artifact"}:
        path_value = value
        line_number = None
        if kind == "file":
            line_match = re.fullmatch(r"(.+):(\d+)", value)
            if line_match:
                path_value = line_match.group(1)
                line_number = int(line_match.group(2))
        target = safe_path(repo, Path(path_value), must_exist=True)
        if kind == "file" and not target.is_file():
            raise CskError(f"Closure file evidence is not a file: {path_value}")
        if line_number is not None:
            line_count = len(target.read_text(encoding="utf-8-sig", errors="replace").splitlines())
            if line_number < 1 or line_number > line_count:
                raise CskError(f"Closure file evidence line is out of range: {value}")
        result["resolved"] = target.relative_to(repo).as_posix()
    else:
        if not evidence_record:
            raise CskError(f"{kind}: evidence requires --evidence-record with a local proof file")
        record = safe_path(repo, Path(evidence_record), must_exist=True)
        if not record.is_file():
            raise CskError("Closure evidence record must be a file")
        record_text = record.read_text(encoding="utf-8-sig", errors="replace")
        if kind == "url":
            parsed_url = urlparse(value)
            if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                raise CskError(f"Closure URL is invalid: {value}")
        if value not in record_text:
            raise CskError(f"Closure evidence record does not contain {value!r}")
        result["record"] = record.relative_to(repo).as_posix()
    return result


def load_tasks(repo: Path) -> tuple[dict[str, Any], bytes]:
    path = safe_path(repo, TASKS_REL, must_exist=True)
    raw = read_bytes(path)
    parsed = parse_tasks(raw)
    validate_task_references(repo, parsed)
    return parsed, raw


def branch_warnings(repo: Path, rows: list[dict[str, str]]) -> list[str]:
    branch = _run_git(repo, "branch", "--show-current").stdout.strip()
    warnings: list[str] = []
    for row in rows:
        expected = row["expected_branch"]
        if expected not in {"n/a", "any", branch}:
            warnings.append(
                f"{row['id']} expects branch {expected!r}, current branch is {branch or 'detached HEAD'!r}"
            )
    return warnings


def mutate_tasks(repo: Path, operation: str, args: argparse.Namespace) -> dict[str, Any]:
    with repository_lock(repo):
        parsed, raw = load_tasks(repo)
        rows = [dict(row) for row in parsed["rows"]]
        result: dict[str, Any]
        if operation == "add":
            task_id = f"TASK-{parsed['next_id']:03d}"
            row = {
                "id": task_id,
                "status": args.status,
                "priority": args.priority,
                "related": _clean_cell(args.related, "related"),
                "expected_branch": _clean_cell(args.expected_branch, "expected_branch"),
                "resume_skill": _clean_cell(args.resume_skill, "resume_skill"),
                "task": _clean_cell(args.task, "task"),
                "next_action": _clean_cell(args.next_action, "next_action"),
                "blocker": _clean_cell(args.blocker or "-", "blocker"),
                "updated": _today(),
            }
            if row["status"] == "blocked" and row["blocker"] == "-":
                raise CskError("Blocked tasks require --blocker")
            rows.append(row)
            next_id = parsed["next_id"] + 1
            result = {"created": task_id, "row": row}
        else:
            target = next((row for row in rows if row["id"] == args.id), None)
            if target is None:
                raise CskError(f"Unknown task ID: {args.id}")
            next_id = parsed["next_id"]
            if operation == "update":
                mapping = {
                    "status": args.status,
                    "priority": args.priority,
                    "related": args.related,
                    "expected_branch": args.expected_branch,
                    "resume_skill": args.resume_skill,
                    "task": args.task,
                    "next_action": args.next_action,
                    "blocker": args.blocker,
                }
                for key, value in mapping.items():
                    if value is not None:
                        target[key] = _clean_cell(value, key)
                target["updated"] = _today()
                result = {"updated": args.id, "row": target}
            elif operation == "block":
                target["status"] = "blocked"
                target["blocker"] = _clean_cell(args.reason, "blocker")
                target["next_action"] = _clean_cell(args.next_action, "next_action")
                target["updated"] = _today()
                result = {"blocked": args.id, "row": target}
            elif operation == "close":
                closure = verify_closure_evidence(
                    repo,
                    args.evidence,
                    getattr(args, "evidence_record", None),
                )
                rows = [row for row in rows if row["id"] != args.id]
                result = {"closed": args.id, **closure}
            else:
                raise CskError(f"Unsupported task operation: {operation}")
        rendered = render_tasks(parsed, rows, next_id)
        validated = parse_tasks(rendered)
        validate_task_references(repo, validated)
        durable_replace(repo, safe_path(repo, TASKS_REL, must_exist=True), rendered, _sha256(raw))
        result["warnings"] = branch_warnings(repo, rows)
        return result


def command_state(repo: Path, args: argparse.Namespace) -> dict[str, Any]:
    if args.operation == "inventory":
        return inventory(repo)
    if args.operation == "check-template-distribution":
        snapshot = getattr(args, "snapshot", "HEAD")
        state = load_state_snapshot(repo, snapshot)
        if state != INITIAL_TEMPLATE_STATE:
            raise CskError(
                f"Starter-kit distribution snapshot {snapshot} requires exact "
                "template/pending/not-assessed project state"
            )
        return {
            "valid": True,
            "distribution_template": True,
            "snapshot": snapshot,
            "state": state,
        }
    if args.operation == "check":
        state, _ = load_state(repo)
        drift = state_drift(repo, state)
        return {
            "valid": not drift,
            "schema_valid": True,
            "drift": drift,
            "state": state,
            "distribution": state_distribution(repo),
        }
    with repository_lock(repo):
        state, raw = load_state(repo)
        onboarding = state["onboarding"]
        if args.operation == "decide":
            if onboarding["mode"] != "pending":
                raise CskError("The first-open decision was already recorded; use state recheck explicitly")
            state["repository_role"] = "project"
            onboarding["mode"] = args.mode
            onboarding["adoption_status"] = "not-applicable" if args.mode == "greenfield" else "pending"
            onboarding["decided_at"] = _now()
            onboarding["scaffold_evidence"] = None
        elif args.operation == "recheck":
            state["repository_role"] = "project"
            onboarding.update({
                "mode": "pending",
                "adoption_status": "not-assessed",
                "decided_at": None,
                "scaffold_evidence": None,
            })
        elif args.operation == "adoption-complete":
            if onboarding["mode"] != "adopt" or onboarding["adoption_status"] not in {"pending", "blocked"}:
                raise CskError("Only adopt/pending or adopt/blocked can become complete")
            coverage = validate_coverage_report(repo, Path(args.coverage_report))
            onboarding["adoption_status"] = "complete"
            onboarding["scaffold_evidence"] = {
                **coverage,
                "verified_at": _now(),
            }
        elif args.operation == "adoption-block":
            if onboarding["mode"] != "adopt":
                raise CskError("Only adopt mode can be blocked")
            onboarding["adoption_status"] = "blocked"
            onboarding["scaffold_evidence"] = {"reason": _clean_cell(args.reason, "reason"), "blocked_at": _now()}
        else:
            raise CskError(f"Unsupported state operation: {args.operation}")
        write_state(repo, state, raw)
        return {"updated": True, "state": state, "distribution": state_distribution(repo)}


def command_tasks(repo: Path, args: argparse.Namespace) -> dict[str, Any]:
    if args.operation in {"check", "list"}:
        parsed, _ = load_tasks(repo)
        return {
            "valid": True,
            "next_id": f"TASK-{parsed['next_id']:03d}",
            "rows": parsed["rows"],
            "warnings": branch_warnings(repo, parsed["rows"]),
        }
    return mutate_tasks(repo, args.operation, args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="Repository root or path within it")
    areas = parser.add_subparsers(dest="area", required=True)

    state = areas.add_parser("state")
    state_ops = state.add_subparsers(dest="operation", required=True)
    state_ops.add_parser("check")
    distribution_check = state_ops.add_parser("check-template-distribution")
    distribution_check.add_argument("--snapshot", choices=("HEAD", "index"), default="HEAD")
    state_ops.add_parser("inventory")
    decide = state_ops.add_parser("decide")
    decide.add_argument("--mode", choices=("greenfield", "adopt"), required=True)
    state_ops.add_parser("recheck")
    complete = state_ops.add_parser("adoption-complete")
    complete.add_argument("--coverage-report", required=True)
    blocked = state_ops.add_parser("adoption-block")
    blocked.add_argument("--reason", required=True)

    tasks = areas.add_parser("tasks")
    task_ops = tasks.add_subparsers(dest="operation", required=True)
    task_ops.add_parser("check")
    task_ops.add_parser("list")
    add = task_ops.add_parser("add")
    add.add_argument("--status", choices=sorted(VALID_STATUSES), default="open")
    add.add_argument("--priority", choices=sorted(VALID_PRIORITIES), required=True)
    add.add_argument("--related", default="none")
    add.add_argument("--expected-branch", default="n/a")
    add.add_argument("--resume-skill", default="direct")
    add.add_argument("--task", required=True)
    add.add_argument("--next-action", required=True)
    add.add_argument("--blocker")
    update = task_ops.add_parser("update")
    update.add_argument("id")
    update.add_argument("--status", choices=sorted(VALID_STATUSES))
    update.add_argument("--priority", choices=sorted(VALID_PRIORITIES))
    update.add_argument("--related")
    update.add_argument("--expected-branch")
    update.add_argument("--resume-skill")
    update.add_argument("--task")
    update.add_argument("--next-action")
    update.add_argument("--blocker")
    block = task_ops.add_parser("block")
    block.add_argument("id")
    block.add_argument("--reason", required=True)
    block.add_argument("--next-action", required=True)
    close = task_ops.add_parser("close")
    close.add_argument("id")
    close.add_argument("--evidence", required=True)
    close.add_argument("--evidence-record")
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        validate_runtime()
        args = build_parser().parse_args(argv)
        repo = resolve_repo(args.repo)
        result = command_state(repo, args) if args.area == "state" else command_tasks(repo, args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        if args.area == "state" and args.operation == "check" and result.get("valid") is False:
            return 3
        return 0
    except (CskError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
