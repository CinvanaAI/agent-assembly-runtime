import runpy
from pathlib import Path

import pytest

from agent_assembly_runtime import AssemblyManager


@pytest.mark.parametrize("location", ["agent", "group", "task", "workflow", "package", "logic", "prompt", "memory", "default_return", "replacement", "argument", "return"])
def test_unknown_authored_fields_are_rejected_before_writing(tmp_path, location):
    raw = runpy.run_path(str(Path(__file__).with_name("test_runtime.py")))["fixture"]()
    group = raw["groups"][1]
    task = group["tasks"][0]
    package = {
        "name": "Echo", "package_status": "Ready", "logic": {"logic_source": "return payload"},
        "required_replacements": [{"to_be_replaced": "LABEL", "value": "example"}],
        "arguments": [{"argument_question": "Text?", "argument_value_name": "text", "argument_fallback": "", "argument_hidden": False, "task_argument_mapping": {"source_type": "input"}}],
        "returns": [{"return_value_name": "text", "return_description": "Echo", "visible": True, "friendship": False}],
    }
    task["packages"] = [package]
    task["prompts"] = [{"name": "Prompt", "prompt_source": "Summarize"}]
    task["memory"] = [{"name": "Notes", "has_file": True, "file_path": "", "content": "synthetic"}]
    raw["default_returns"] = [{"return_value_name": "done", "return_description": "Result", "return_value": ""}]
    targets = {"agent": raw, "group": group, "task": task, "workflow": task["workflow"], "package": package, "logic": package["logic"], "prompt": task["prompts"][0], "memory": task["memory"][0], "default_return": raw["default_returns"][0], "replacement": package["required_replacements"][0], "argument": package["arguments"][0], "return": package["returns"][0]}
    targets[location]["mystery"] = True
    destination = tmp_path / "assemblies"
    manager = AssemblyManager(destination)
    with pytest.raises(ValueError, match="unknown field"):
        manager.save_agent("Example Agent", raw)
    assert not [p for p in destination.rglob("*") if p.is_file()]
