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
