import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent


def run(*args):
    return subprocess.run([sys.executable, str(ROOT / "build_prompt.py"), *args],
                          capture_output=True, text=True, encoding="utf-8")


def test_base_assembly_contains_all_modules_in_order():
    out = run().stdout
    idx = [out.index(tag) for tag in
           ("<identity>", "<safety>", "<tone>", "<wellbeing>", "<evenhandedness>",
            "<memory>", "<tool_routing>", "<content_limits>", "<files_and_skills>",
            "<runtime_reminders>")]
    assert idx == sorted(idx)


def test_role_overlay_appended_last():
    out = run("--role", "reviewer").stdout
    assert "<role_reviewer>" in out
    assert out.index("<role_reviewer>") > out.index("<runtime_reminders>")
    assert "VERDICT: APPROVE" in out


def test_fields_are_filled():
    out = run("--set", "agent_name=TestBot", "--set", "host_surface=a test rig").stdout
    assert "TestBot" in out
    assert "{agent_name}" not in out.split("Template fields")[0]


def test_exclude_drops_modules():
    out = run("--exclude", "30,40").stdout
    assert "<wellbeing>" not in out
    assert "<evenhandedness>" not in out
    assert "<safety>" in out


def test_unknown_role_errors():
    r = run("--role", "nonexistent")
    assert r.returncode != 0
    assert "unknown role" in (r.stdout + r.stderr)


def test_all_four_roles_build():
    for role in ("planner", "executor", "reviewer", "mechanical"):
        r = run("--role", role)
        assert r.returncode == 0 and f"<role_{role}>" in r.stdout


import re

MODULES = ROOT / "modules"
SKILLS = ROOT / "skills"


def test_module_anatomy():
    """Every numbered module carries the full 5-part anatomy, at least one worked
    good/bad example pair, and at least one numeric limit."""
    for mod in sorted(MODULES.glob("[0-9]*.md")):
        text = mod.read_text(encoding="utf-8")
        for section in ("## RULES", "## WHY", "## EXAMPLES", "## EXPECTED", "## SELF-CHECK"):
            assert section in text, f"{mod.name} missing {section}"
        assert "<example>" in text and "<good>" in text and "<bad>" in text, \
            f"{mod.name} missing a good/bad example pair"
        assert re.search(r"\b\d+\b", text), f"{mod.name} has no numeric limit"


def test_skills_have_verdict_contracts():
    """The review and verify skills must state their exact final-line contracts,
    and every skill must have frontmatter, a preamble, and numbered steps."""
    contracts = {
        "pp-review": "VERDICT: APPROVE",
        "pp-verify": "VERDICT: PASS",
    }
    for name, marker in contracts.items():
        text = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
        assert marker in text, f"{name} missing verdict contract {marker!r}"

    for skill in SKILLS.glob("*/SKILL.md"):
        text = skill.read_text(encoding="utf-8")
        assert text.startswith("---"), f"{skill.parent.name} missing frontmatter"
        assert "## Preamble" in text, f"{skill.parent.name} missing preamble"
        assert "## Steps" in text, f"{skill.parent.name} missing numbered steps"
        assert "## Important rules" in text, f"{skill.parent.name} missing rules"


def test_skill_listing():
    out = run("--list").stdout
    for name in ("pp-plan", "pp-build", "pp-review", "pp-verify"):
        assert f"skill:  {name}" in out
