"""Ontology engine checks. Run: python3 -m unittest discover tests"""

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from thinkpad import config, lint

spec = importlib.util.spec_from_file_location("ontology", config.HARNESS / "scripts" / "ontology.py")
onto = importlib.util.module_from_spec(spec)
spec.loader.exec_module(onto)


class Engine(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.graph = Path(self.tmp.name) / "graph.jsonl"
        self.schema = onto.load_schema(None)
        onto.create_entity("Env", {"name": "e", "path": "envs/e"}, self.graph, self.schema, "env:e")
        onto.create_entity("Concept", {"name": "c", "domain": "d"}, self.graph, self.schema, "concept:c")

    def tearDown(self):
        self.tmp.cleanup()

    def refused(self, fn, *a):
        with self.assertRaises(SystemExit) as cm:
            fn(*a)
        return str(cm.exception)

    def test_writes_are_validated_and_nothing_is_appended_on_refusal(self):
        before = self.graph.read_text()
        msg = self.refused(onto.create_entity, "Concept", {"name": "x"}, self.graph, self.schema, "concept:x")
        self.assertIn("missing required property 'domain'", msg)
        self.assertIn("unknown type", self.refused(onto.create_entity, "Nope", {}, self.graph, self.schema))
        self.assertIn("undeclared", self.refused(onto.create_entity, "Env", {"name": "n", "path": "p", "zzz": 1}, self.graph, self.schema, "env:n"))
        self.assertIn("already exists", self.refused(onto.create_entity, "Env", {"name": "e", "path": "p"}, self.graph, self.schema, "env:e"))
        self.assertEqual(self.graph.read_text(), before)

    def test_enum_is_enforced(self):
        msg = self.refused(onto.create_entity, "Resource", {"name": "r", "kind": "scroll"}, self.graph, self.schema, "resource:r")
        self.assertIn("must be one of", msg)

    def test_relation_endpoint_types(self):
        onto.create_relation("concept:c", "part_of", "env:e", {}, self.graph, self.schema)
        self.assertIn("expected one of", self.refused(onto.create_relation, "env:e", "part_of", "concept:c", {}, self.graph, self.schema))
        self.assertIn("unknown relation", self.refused(onto.create_relation, "concept:c", "loves", "env:e", {}, self.graph, self.schema))
        self.assertIn("missing entity", self.refused(onto.create_relation, "concept:c", "part_of", "env:ghost", {}, self.graph, self.schema))
        self.assertEqual([r["entity"]["id"] for r in onto.get_related("concept:c", "part_of", self.graph)], ["env:e"])

    def test_acyclic_supersedes(self):
        for i in "ab":
            onto.create_entity("Learning", {"summary": i, "source": "s"}, self.graph, self.schema, f"learning:{i}")
        onto.create_relation("learning:a", "supersedes", "learning:b", {}, self.graph, self.schema)
        self.assertIn("cyclic", self.refused(onto.create_relation, "learning:b", "supersedes", "learning:a", {}, self.graph, self.schema))

    def test_update_and_query_use_last_state(self):
        onto.update_entity("concept:c", {"definition": "d2"}, self.graph, self.schema)
        self.assertEqual(onto.query_entities("Concept", {"name": "c"}, self.graph)[0]["properties"]["definition"], "d2")
        self.assertIn("undeclared", self.refused(onto.update_entity, "concept:c", {"bogus": 1}, self.graph, self.schema))
        self.assertEqual(onto.validate_graph(self.graph, self.schema), [])

    def test_overlay_extends_schema(self):
        overlay = Path(self.tmp.name) / "schema.toml"
        overlay.write_text('[types.Question]\nrequired = ["text"]\n')
        schema = onto.load_schema(overlay)
        onto.create_entity("Question", {"text": "why?"}, self.graph, schema, "question:1")
        self.assertIn("unknown type", self.refused(onto.create_entity, "Question", {"text": "x"}, self.graph, self.schema, "question:2"))

    def test_migrate_legacy_format(self):
        legacy = Path(self.tmp.name) / "old.jsonl"
        lines = [
            {"id": "concept:old", "type": "Concept", "props": {"name": "o", "domain": "d"}, "relations": [{"rel": "part_of", "to": "env:e"}], "created": "2026-01-01"},
            {"id": "concept:old", "type": "Concept", "props": {"name": "o2", "domain": "d"}, "relations": [{"rel": "part_of", "to": "env:e"}], "created": "2026-01-02"},
        ]
        legacy.write_text("\n".join(json.dumps(x) for x in lines))
        self.assertEqual(onto.migrate_legacy(legacy, self.graph), 1)
        self.assertEqual(onto.load_graph(self.graph)[0]["concept:old"]["properties"]["name"], "o2")
        self.assertEqual(onto.validate_graph(self.graph, self.schema), [])


class Manifests(unittest.TestCase):
    def test_graph_types_must_exist(self):
        with tempfile.TemporaryDirectory() as t:
            d = Path(t) / "s"
            d.mkdir()
            (d / "SKILL.md").write_text(
                "---\nname: s\ndescription: x\nmetadata:\n  api: 1\n  kind: engine\n  mode: infra\n"
                "  terminal: forbidden\n  graph_writes: [\"Ghost\"]\n---\n"
            )
            self.assertTrue(any("Ghost" in p for p in lint.lint_skills(Path(t))))

    def test_shipped_graph_skills_declare_valid_types(self):
        self.assertEqual(lint.lint_skills(), [])


if __name__ == "__main__":
    unittest.main()
