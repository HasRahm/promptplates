#!/usr/bin/env python3
"""promptplates assembler — concatenate numbered modules + a role overlay into one system prompt.

Zero dependencies. Usage:
    python build_prompt.py --role reviewer --set agent_name=MyAgent --exclude 30,40
    python build_prompt.py --list
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parent
MODULES = ROOT / "modules"
ROLES = ROOT / "roles"


def module_files(exclude: set[str]) -> list[Path]:
    files = sorted(p for p in MODULES.glob("[0-9]*.md"))
    return [p for p in files if p.name.split("-")[0] not in exclude]


def build(role: str | None, fields: dict[str, str], exclude: set[str]) -> str:
    parts = []
    for p in module_files(exclude):
        text = p.read_text(encoding="utf-8")
        for k, v in fields.items():
            text = text.replace("{" + k + "}", v)
        parts.append(text.strip())
    if role:
        overlay = ROLES / f"{role}.md"
        if not overlay.exists():
            sys.exit(f"unknown role '{role}' (available: "
                     f"{', '.join(p.stem for p in ROLES.glob('*.md'))})")
        parts.append(overlay.read_text(encoding="utf-8").strip())
    return "\n\n".join(parts) + "\n"


def main() -> int:
    # Windows consoles default to cp1252, which can't encode the arrows/dashes
    # in the modules; force UTF-8 on the way out.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--role", help="role overlay from roles/ (planner, executor, reviewer, mechanical)")
    ap.add_argument("--set", action="append", default=[], metavar="KEY=VALUE",
                    help="fill a {placeholder} field (repeatable)")
    ap.add_argument("--exclude", default="", help="comma-separated module number prefixes to drop, e.g. 30,40")
    ap.add_argument("--out", help="write to file instead of stdout")
    ap.add_argument("--list", action="store_true", help="list modules and roles")
    args = ap.parse_args()

    if args.list:
        for p in sorted(MODULES.glob("[0-9]*.md")):
            print("module:", p.name)
        for p in sorted(ROLES.glob("*.md")):
            print("role:  ", p.stem)
        return 0

    fields = dict(kv.split("=", 1) for kv in getattr(args, "set"))
    exclude = {x.strip() for x in args.exclude.split(",") if x.strip()}
    prompt = build(args.role, fields, exclude)
    if args.out:
        Path(args.out).write_text(prompt, encoding="utf-8")
        print(f"wrote {len(prompt)} chars to {args.out}", file=sys.stderr)
    else:
        print(prompt, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
