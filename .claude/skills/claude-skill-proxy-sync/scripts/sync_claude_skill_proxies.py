#!/usr/bin/env python3
"""Generate portable, repository-local Codex proxies for Claude skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


MARKER = "CODEX-CLAUDE-SKILL-PROXY"
SCHEMA_VERSION = 1
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FRONTMATTER_RE = re.compile(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
INTERFACE_KEYS = ("display_name", "short_description", "default_prompt")


class SyncError(RuntimeError):
    """Raised for invalid or unsafe repository state."""


@dataclass(frozen=True)
class SkillContract:
    name: str
    description: str
    display_name: str
    short_description: str
    default_prompt: str
    canonical_path: str
    contract_hash: str


@dataclass
class PlanItem:
    name: str
    action: str
    canonical_path: str | None = None
    target_path: str | None = None
    detail: str | None = None


def _yaml_scalar(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _parse_simple_yaml(text: str, keys: Iterable[str]) -> dict[str, str]:
    """Parse the small scalar subset used by skill frontmatter and UI metadata."""
    wanted = set(keys)
    lines = text.splitlines()
    result: dict[str, str] = {}
    index = 0
    while index < len(lines):
        match = re.match(r"^[ \t]*([A-Za-z_][A-Za-z0-9_-]*):(?:[ \t]*(.*))?$", lines[index])
        if not match or match.group(1) not in wanted:
            index += 1
            continue
        key, raw = match.group(1), (match.group(2) or "").strip()
        if raw in {">", ">-", ">+", "|", "|-", "|+"}:
            block: list[str] = []
            index += 1
            while index < len(lines) and (not lines[index].strip() or lines[index][0].isspace()):
                block.append(lines[index].strip())
                index += 1
            value = "\n".join(block).strip() if raw.startswith("|") else " ".join(x for x in block if x).strip()
            result[key] = value
            continue
        if len(raw) >= 2 and raw[0] == raw[-1] == '"':
            try:
                raw = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise SyncError(f"Invalid quoted YAML scalar for {key}: {exc}") from exc
        elif len(raw) >= 2 and raw[0] == raw[-1] == "'":
            raw = raw[1:-1].replace("''", "'")
        result[key] = raw
        index += 1
    return result


def _title(name: str) -> str:
    words = [(word.upper() if word in {"csk", "qa", "ui", "api"} else word.capitalize()) for word in name.split("-")]
    return " ".join(words)


def _short_description(name: str, description: str) -> str:
    first = re.split(r"(?<=[.!?])\s+", description.strip(), maxsplit=1)[0].rstrip(".")
    if 25 <= len(first) <= 64:
        return first
    fallback = f"Run the repo-local {_title(name)} workflow"
    if len(fallback) <= 64:
        return fallback
    return f"Use the repo-local {name[:43]} skill"[:64]


def _interface_metadata(skill_dir: Path, name: str, description: str) -> dict[str, str]:
    metadata = {
        "display_name": _title(name),
        "short_description": _short_description(name, description),
        "default_prompt": f"Use ${name} and follow its canonical repository-local Claude skill.",
    }
    openai_yaml = skill_dir / "agents" / "openai.yaml"
    if openai_yaml.is_file():
        parsed = _parse_simple_yaml(openai_yaml.read_text(encoding="utf-8-sig"), INTERFACE_KEYS)
        metadata.update({key: value for key, value in parsed.items() if value})
    return metadata


def read_contract(repo: Path, skill_dir: Path) -> SkillContract:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8-sig")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise SyncError(f"Missing YAML frontmatter: {skill_file}")
    frontmatter = _parse_simple_yaml(match.group(1), ("name", "description"))
    name = frontmatter.get("name", "").strip()
    description = frontmatter.get("description", "").strip()
    if not NAME_RE.fullmatch(name):
        raise SyncError(f"Invalid skill name {name!r}: {skill_file}")
    if skill_dir.name != name:
        raise SyncError(f"Skill directory {skill_dir.name!r} does not match frontmatter name {name!r}")
    if not description:
        raise SyncError(f"Missing skill description: {skill_file}")
    canonical_path = skill_file.relative_to(repo).as_posix()
    if not canonical_path.startswith(".claude/skills/"):
        raise SyncError(f"Canonical skill escaped .claude/skills: {skill_file}")
    interface = _interface_metadata(skill_dir, name, description)
    payload = {"name": name, "description": description, "interface": interface}
    contract_hash = hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    return SkillContract(
        name=name,
        description=description,
        display_name=interface["display_name"],
        short_description=interface["short_description"],
        default_prompt=interface["default_prompt"],
        canonical_path=canonical_path,
        contract_hash=contract_hash,
    )


def render_proxy(contract: SkillContract) -> str:
    return f'''---
name: {contract.name}
description: {_yaml_scalar(contract.description)}
---

<!--
{MARKER}
canonical_claude_skill: {contract.canonical_path}
contract_sha256: {contract.contract_hash}
source_kind: repo
proxy_schema_version: {SCHEMA_VERSION}
generated_by: .claude/skills/claude-skill-proxy-sync/scripts/sync_claude_skill_proxies.py
-->

# Claude Skill Proxy: {contract.display_name}

This is a generated thin Codex proxy. The canonical implementation remains in
`{contract.canonical_path}` inside this repository.

## Runtime Instructions

1. Resolve the current Git repository root; do not use the proxy generator's
   machine or path.
2. Read `<repo>/{contract.canonical_path}` completely before taking task action.
3. Follow that canonical skill as the authoritative workflow.
4. Resolve its relative scripts, references, and assets from
   `<repo>/.claude/skills/{contract.name}/`.
5. Keep all kit skills repository-local. Never install, copy, or fall back to a
   user-global Claude or Codex skill directory.
6. If the canonical file is absent, stop and report the missing repo file.

Ordinary canonical body and resource changes are live. Regenerate this proxy only
after inventory, frontmatter trigger, or interface metadata changes.
'''


def render_openai_yaml(contract: SkillContract) -> str:
    return (
        "interface:\n"
        f"  display_name: {_yaml_scalar(contract.display_name)}\n"
        f"  short_description: {_yaml_scalar(contract.short_description)}\n"
        f"  default_prompt: {_yaml_scalar(contract.default_prompt)}\n"
    )


def _assert_repo(repo: Path) -> Path:
    resolved = repo.resolve()
    if not (resolved / ".claude" / "skills").is_dir():
        raise SyncError(f"Repository-local source missing: {resolved / '.claude' / 'skills'}")
    return resolved


def discover_repo(start: Path) -> Path:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(start), "rev-parse", "--show-toplevel"],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise SyncError(f"Cannot resolve Git repository from {start}") from exc
    return _assert_repo(Path(output))


def _inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _is_generated(skill_dir: Path) -> bool:
    skill_file = skill_dir / "SKILL.md"
    return skill_file.is_file() and MARKER in skill_file.read_text(encoding="utf-8-sig", errors="replace")


def _unexpected_target_entries(skill_dir: Path) -> list[str]:
    allowed_files = {"SKILL.md", "agents/openai.yaml"}
    allowed_dirs = {"agents"}
    unexpected: list[str] = []
    for path in skill_dir.rglob("*"):
        relative = path.relative_to(skill_dir).as_posix()
        if path.is_symlink():
            unexpected.append(relative)
        elif path.is_dir() and relative not in allowed_dirs:
            unexpected.append(relative + "/")
        elif path.is_file() and relative not in allowed_files:
            unexpected.append(relative)
    return sorted(unexpected)


def plan_sync(repo: Path, selected: set[str] | None = None) -> tuple[list[PlanItem], dict[str, tuple[str, str]]]:
    repo = _assert_repo(repo)
    source_root = repo / ".claude" / "skills"
    target_root = repo / ".codex" / "skills"
    if not _inside(source_root, repo) or not _inside(target_root, repo):
        raise SyncError("Skill roots must stay inside the repository")

    contracts: list[SkillContract] = []
    for skill_dir in sorted((path for path in source_root.iterdir() if path.is_dir()), key=lambda p: p.name):
        if not (skill_dir / "SKILL.md").is_file():
            continue
        if selected is not None and skill_dir.name not in selected:
            continue
        contracts.append(read_contract(repo, skill_dir))

    discovered = {contract.name for contract in contracts}
    if selected is not None and (missing := selected - discovered):
        raise SyncError(f"Unknown canonical skill(s): {', '.join(sorted(missing))}")

    plan: list[PlanItem] = []
    expected: dict[str, tuple[str, str]] = {}
    for contract in contracts:
        target_dir = target_root / contract.name
        target_file = target_dir / "SKILL.md"
        target_agent = target_dir / "agents" / "openai.yaml"
        proxy_text = render_proxy(contract)
        agent_text = render_openai_yaml(contract)
        expected[contract.name] = (proxy_text, agent_text)
        item = PlanItem(
            name=contract.name,
            action="ok",
            canonical_path=contract.canonical_path,
            target_path=target_file.relative_to(repo).as_posix(),
        )
        unexpected = _unexpected_target_entries(target_dir) if target_dir.exists() else []
        if target_dir.exists() and not _is_generated(target_dir):
            item.action = "conflict"
            item.detail = "target exists without generated marker"
        elif unexpected:
            item.action = "conflict"
            item.detail = "generated target contains unmanaged entries: " + ", ".join(unexpected)
        elif not target_file.is_file() or not target_agent.is_file():
            item.action = "create"
        elif target_file.read_text(encoding="utf-8-sig") != proxy_text or target_agent.read_text(encoding="utf-8-sig") != agent_text:
            item.action = "update"
        plan.append(item)

    if selected is None and target_root.is_dir():
        for target_dir in sorted((path for path in target_root.iterdir() if path.is_dir()), key=lambda p: p.name):
            if target_dir.name not in discovered and _is_generated(target_dir):
                unexpected = _unexpected_target_entries(target_dir)
                plan.append(
                    PlanItem(
                        name=target_dir.name,
                        action="conflict" if unexpected else "stale",
                        target_path=target_dir.relative_to(repo).as_posix(),
                        detail=(
                            "stale generated target contains unmanaged entries: " + ", ".join(unexpected)
                            if unexpected
                            else "canonical repo-local Claude skill no longer exists"
                        ),
                    )
                )
    return plan, expected


def apply_plan(repo: Path, plan: list[PlanItem], expected: dict[str, tuple[str, str]], prune: bool) -> None:
    repo = _assert_repo(repo)
    target_root = (repo / ".codex" / "skills").resolve()
    for item in plan:
        target_dir = target_root / item.name
        if not _inside(target_dir, target_root):
            raise SyncError(f"Unsafe target path: {target_dir}")
        if item.action in {"create", "update"}:
            proxy_text, agent_text = expected[item.name]
            (target_dir / "agents").mkdir(parents=True, exist_ok=True)
            (target_dir / "SKILL.md").write_text(proxy_text, encoding="utf-8", newline="\n")
            (target_dir / "agents" / "openai.yaml").write_text(agent_text, encoding="utf-8", newline="\n")
        elif item.action == "stale" and prune:
            if not _is_generated(target_dir):
                raise SyncError(f"Refusing to prune unmanaged target: {target_dir}")
            shutil.rmtree(target_dir)


def _print_plan(plan: list[PlanItem], as_json: bool) -> None:
    if as_json:
        print(json.dumps([asdict(item) for item in plan], ensure_ascii=False, indent=2))
        return
    for item in plan:
        detail = f" - {item.detail}" if item.detail else ""
        print(f"{item.action:8} {item.name}{detail}")
    counts = {action: sum(item.action == action for item in plan) for action in ("ok", "create", "update", "stale", "conflict")}
    print("summary  " + " ".join(f"{key}={value}" for key, value in counts.items()))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, help="Repository root; defaults to the current Git repository")
    parser.add_argument("--name", action="append", help="Synchronize one named canonical skill; repeatable")
    parser.add_argument("--apply", action="store_true", help="Write safe creates and updates")
    parser.add_argument("--prune", action="store_true", help="With --apply, delete stale generated proxies")
    parser.add_argument("--json", action="store_true", help="Print the plan as JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.prune and not args.apply:
        print("error: --prune requires --apply", file=sys.stderr)
        return 2
    try:
        repo = _assert_repo(args.repo) if args.repo else discover_repo(Path.cwd())
        plan, expected = plan_sync(repo, set(args.name) if args.name else None)
        _print_plan(plan, args.json)
        if any(item.action == "conflict" for item in plan):
            return 2
        if args.apply:
            apply_plan(repo, plan, expected, args.prune)
            unresolved_stale = any(item.action == "stale" for item in plan) and not args.prune
            return 1 if unresolved_stale else 0
        return 1 if any(item.action != "ok" for item in plan) else 0
    except (OSError, SyncError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
