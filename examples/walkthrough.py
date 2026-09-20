"""Save, reload, inspect projections, and reject a misspelled authored field."""
import copy
import json
import tempfile
from pathlib import Path
from agent_assembly_runtime import AssemblyManager

payload = json.loads(Path(__file__).with_name("agent.json").read_text())
with tempfile.TemporaryDirectory(prefix="assembly-example-") as temporary:
    root = Path(temporary)
    manager = AssemblyManager(root)
    manager.save_agent(payload["name"], payload)
    loaded = manager.load_agent_data(payload["name"])
    files = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    invalid = copy.deepcopy(payload)
    invalid["groups"][1]["tasks"][0]["task_staus"] = "On Demand"
    try:
        manager.save_agent(payload["name"], invalid)
    except ValueError as error:
        rejection = str(error)
    else:
        raise AssertionError("Unknown authored field was accepted")
    # Edit the canonical definition, not a generated task/group file.
    moved = copy.deepcopy(payload)
    moved['groups'][1]['name'] = 'Review'
    manager.save_agent(moved['name'], moved)
    reloaded = AssemblyManager(root).load_agent_data(moved['name'])
    projected = json.loads(manager.get_group_file_path(moved['name'], 'Review').read_text())
    assert projected['tasks'][0]['name'] == 'Summarize'
    assert not manager.get_group_file_path(moved['name'], 'Research').exists()
    assert manager.load_task_data(moved['name'], 'Summarize')['workflow']['workflow_source'] == payload['groups'][1]['tasks'][0]['workflow']['workflow_source']
    print(json.dumps({"name": loaded["name"], "groups": [g["name"] for g in loaded["groups"]], "files": files, "rejected_typo": rejection, "embedded_source_executed": False,
                      'groups_after_edit_and_restart': [g['name'] for g in reloaded['groups']],
                      'projected_task': projected['tasks'][0]['name'], 'stale_research_projection_removed': True}, indent=2))
