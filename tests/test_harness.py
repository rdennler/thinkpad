"""Harness checks. Run: python3 -m unittest discover tests"""

import tempfile
import unittest
from datetime import date
from pathlib import Path

from thinkpad import config, lint
from thinkpad.schedule import today_block
from thinkpad.spec import EnvSpec, load_env, load_skill, parse_frontmatter
from thinkpad.substrate import ClaudeCode, COMPONENTS, Substrate


class Skills(unittest.TestCase):
    def test_every_skill_manifest_is_valid(self):
        self.assertEqual(lint.lint_skills(), [])
        self.assertEqual(lint.lint_docs(), [])

    def test_lint_catches_leaks_and_bad_refs(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "bad"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: bad\ndescription: x\nmetadata:\n  api: 1\n  kind: engine\n"
                "  mode: infra\n  terminal: forbidden\n---\nSee /Users/me and tp:nope"
            )
            problems = lint.lint_skills(Path(t))
            self.assertTrue(any("personal" in p for p in problems))
            self.assertTrue(any("tp:nope" in p for p in problems))

    def test_lint_keeps_shipped_skills_subject_neutral(self):
        with tempfile.TemporaryDirectory() as t:
            for name, body in (("neutral", "Do a Python kata."), ("media", "Convert with Python.")):
                d = Path(t) / name
                d.mkdir()
                (d / "SKILL.md").write_text(
                    f"---\nname: {name}\ndescription: x\nmetadata:\n  api: 1\n  kind: engine\n  mode: infra\n  terminal: forbidden\n---\n{body}"
                )
            problems = lint.lint_skills(Path(t))
            self.assertEqual([p.split(":")[0] for p in problems], ["neutral/SKILL.md"])

    def test_frontmatter_parser(self):
        fm = parse_frontmatter('---\nname: a\ndescription: x: y\nmetadata:\n  triggers: ["a b", "c"]\n---\n')
        self.assertEqual(fm["description"], "x: y")
        self.assertEqual(fm["metadata"]["triggers"], ["a b", "c"])

    def test_learning_skills_forbid_unbounded_terminal(self):
        for d in config.SKILLS.iterdir():
            m = load_skill(d)
            if m.kind == "engine" and m.mode == "socratic":
                self.assertNotEqual(m.terminal, "allowed", d.name)


class Envs(unittest.TestCase):
    def test_examples_load(self):
        for d in config.EXAMPLES.iterdir():
            if d.name == "_template":
                continue
            self.assertEqual(load_env(d).name, d.name)

    def test_bad_specs_fail(self):
        with self.assertRaises(ValueError):
            EnvSpec(name="x", title="x", tier="sprint")  # sprint needs expires
        with self.assertRaises(ValueError):
            EnvSpec(name="x", title="x", mode="project", terminal="forbidden")
        with self.assertRaises(ValueError):
            EnvSpec(name="x", title="x", cadence=("funday",))

    def test_tutor_md_is_linted(self):
        with tempfile.TemporaryDirectory() as t:
            env = Path(t) / "e"
            env.mkdir()
            (env / "env.toml").write_text('name = "e"\ntitle = "e"\n')
            (env / "tutor.md").write_text("   \n")
            self.assertTrue(any("empty" in p for p in lint.lint_envs(Path(t))))
            (env / "tutor.md").write_text("x" * (lint.MAX_TUTOR_CHARS + 1))
            self.assertTrue(any("loads every session" in p for p in lint.lint_envs(Path(t))))
            (env / "tutor.md").write_text("## Voice\nCalm.\n")
            self.assertEqual(lint.lint_envs(Path(t)), [])

    def test_default_voice_is_pure_socratic_and_wired_in(self):
        ref = (config.SKILLS / "learn" / "references" / "tutor-voice.md").read_text()
        self.assertIn("## Default voice: pure Socratic", ref)
        self.assertIn("never give the answer", ref)
        self.assertIn("default voice", (config.SKILLS / "learn" / "SKILL.md").read_text())

    def test_examples_ship_a_tutor_file(self):
        for d in config.EXAMPLES.iterdir():
            self.assertTrue((d / "tutor.md").exists(), d.name)

    def test_sprint_expires(self):
        s = EnvSpec(name="x", title="x", tier="sprint", expires="2026-01-10")
        self.assertTrue(s.is_active(date(2026, 1, 10)))
        self.assertFalse(s.is_active(date(2026, 1, 11)))


class Substrates(unittest.TestCase):
    def test_surface_covers_all_eight_components_on_disk(self):
        sub = ClaudeCode()
        self.assertIsInstance(sub, Substrate)
        surface = sub.surface(config.ROOT)
        self.assertEqual(set(surface), set(COMPONENTS))
        self.assertEqual(lint.lint_components(), [])

    def test_materialise_is_pure(self):
        cmds = ClaudeCode().materialise(config.ROOT).commands
        self.assertEqual(cmds[1], ("claude", "plugin", "install", "tp@thinkpad"))


class Schedule(unittest.TestCase):
    MON, TUE = date(2026, 1, 5), date(2026, 1, 6)

    def test_routing_rules(self):
        a = EnvSpec(name="a", title="a", tier=1, cadence=("mon",))
        b = EnvSpec(name="b", title="b", tier=1, cadence=("mon-pm",))
        c = EnvSpec(name="c", title="c", tier=2, cadence=("mon",))
        s = EnvSpec(name="s", title="s", tier="sprint", expires="2026-01-31", cadence=("mon",))
        old = EnvSpec(name="o", title="o", tier=1, status="paused", cadence=("mon",))
        self.assertEqual(today_block([c, a], {}, self.MON).name, "a")  # lower tier wins
        self.assertEqual(today_block([a, b], {"a": "2026-01-02", "b": "2026-01-01"}, self.MON).name, "b")  # older bookmark
        self.assertEqual(today_block([a, s], {}, self.MON).name, "s")  # sprint outranks
        self.assertIsNone(today_block([old], {}, self.MON))  # paused is never routed
        self.assertIsNone(today_block([a], {}, self.TUE))  # rest day


class Shipping(unittest.TestCase):
    def test_user_dirs_ship_empty(self):
        for d in ("envs", "media", "tracker", "memory"):
            self.assertEqual([p.name for p in (config.ROOT / d).iterdir()], [".gitkeep"], d)


if __name__ == "__main__":
    unittest.main()
