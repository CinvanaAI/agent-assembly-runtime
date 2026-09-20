import copy
import json
from pathlib import Path

import pytest

from agent_assembly_runtime import AssemblyManager


@pytest.mark.parametrize('existing_memory', [False, True])
def test_invalid_projection_name_does_not_create_or_move_memory(tmp_path, existing_memory):
    raw = json.loads((Path(__file__).parents[1] / 'examples' / 'agent.json').read_text())
    original = tmp_path / 'existing-memory.json'
    if existing_memory:
        original.write_text('{"preserved":true}\n')
    raw['groups'][1]['group_file'] = 'wrong.group.json'
    raw['groups'][1]['tasks'][0]['memory'] = [
        {'name': 'Notes', 'has_file': True, 'file_path': str(original) if existing_memory else '', 'content': ''}
    ]
    before = copy.deepcopy(raw)
    destination = tmp_path / 'assemblies'
    with pytest.raises(ValueError, match='group_file'):
        AssemblyManager(destination).save_agent(raw['name'], raw)
    assert not [p for p in destination.rglob('*') if p.is_file()]
    assert raw == before
    if existing_memory:
        assert original.read_text() == '{"preserved":true}\n'
