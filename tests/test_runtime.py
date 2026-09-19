from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from agent_assembly_runtime import AgentNormalizer, AgentValidator, AssemblyManager


def fixture() -> dict:
    return {
        "name": "Example Agent",
        "default_returns": [],
        "groups": [
            {
                "name": "Outcasts",
                "default_returns": [],
                "tasks": [],
            },
            {
                "name": "Research",
                "default_returns": [],
                "tasks": [
                    {
                        "name": "Summarize",
                        "task_status": "On Demand",
                        "workflow": {"workflow_source": "def run_workflow(payload):\n    return payload"},
                        "Triggers": "",
                        "default_returns": [],
                        "packages": [],
                        "prompts": [],
                        "memory": [],
                    }
                ],
            },
        ],
    }


class RuntimeTests(unittest.TestCase):
    def test_normalizes_and_validates_canonical_agent(self) -> None:
        normalized = AgentNormalizer().normalize_agent(fixture())
        AgentValidator().validate_agent(normalized)
        self.assertEqual(normalized["groups"][1]["tasks"][0]["task_file"], "Summarize.task.json")

    def test_manager_writes_canonical_and_projection_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manager = AssemblyManager(Path(tmp) / "assemblies")
            path = Path(manager.save_agent("Example Agent", fixture()))
            self.assertTrue(path.exists())
            loaded = manager.load_agent_data("Example Agent")
            self.assertEqual(loaded["name"], "Example Agent")
            folder = path.parent
            self.assertTrue((folder / "Research.group.json").exists())
            self.assertTrue((folder / "Summarize.task.json").exists())

    def test_stale_unknown_fields_fail_closed(self) -> None:
        raw = fixture()
        raw["groups"][1]["tasks"][0]["mystery"] = True
        with self.assertRaisesRegex(ValueError, "unknown field"):
            AgentNormalizer().normalize_agent(raw)

    def test_saved_json_is_plain_portable_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            manager = AssemblyManager(Path(tmp) / "assemblies")
            path = Path(manager.save_agent("Example Agent", fixture()))
            parsed = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(parsed["groups"][1]["name"], "Research")


if __name__ == "__main__":
    unittest.main()
