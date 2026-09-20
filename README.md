# Agent Assembly Runtime

Author an agent once; let its group and task files follow that definition.

This small Python library stores a canonical agent document and writes readable group/task projections from it. It came out of the historical Python Agent Foundry workbench, where an agent's tasks, groups, prompts and memory needed a clear owner. The public extraction accepts your storage directory directly; you can use it without the original application. [Origin and extraction boundary](ORIGIN.md).

Use it when building an editor or local workflow runner that needs to save and reload agent definitions. Embedded Python is stored as text. This package does not execute an agent, call a model, or schedule tasks.

## Follow one edit from input to files

Python 3.11 or newer, from this checkout:

```sh
python -m pip install -e .
python -m examples.walkthrough
```

The offline example reads [agent.json](examples/agent.json), saves Review Bot, rejects a misspelled task field, then moves Summarize from Research into Review by editing the canonical document. A fresh manager reads the edited definition. The generated Review group contains Summarize, and the obsolete Research projection is removed. Everything happens in a disposable temporary directory.

[Executable walkthrough](examples/walkthrough.py) · [Captured synthetic output](examples/result.txt)

Expected observations include `groups_after_edit_and_restart: ["Outcasts", "Review"]`, `projected_task: "Summarize"`, and `stale_research_projection_removed: true`. These are file-management checks, not evidence that the embedded workflow ran.

## Use the library

```python
import json
from pathlib import Path
from agent_assembly_runtime import AssemblyManager

agent = json.loads(Path("examples/agent.json").read_text(encoding="utf-8"))
manager = AssemblyManager(Path("./my-assemblies"))
manager.save_agent(agent["name"], agent)
task = manager.load_task_data(agent["name"], "Summarize")
print(task["workflow"]["workflow_source"])
```

This recipe writes to the directory you select. Change the canonical `groups[].tasks[]` structure and call `save_agent` again; a generated group/task file is an inspection surface, not an independent editing source. Task names must be unique across an agent. `Outcasts` is the required first group, even when empty.

| Step | What owns the behavior |
| --- | --- |
| Fill defaults and reject unknown authored keys | [AgentNormalizer](agent_assembly_runtime/agent_normalizer.py) |
| Check the whole structure and generated names before memory writes | [AgentValidator](agent_assembly_runtime/agent_validator.py), called by [save_agent](agent_assembly_runtime/assembly_manager.py) |
| Create or migrate explicitly configured memory files | [MemoryFileManager](agent_assembly_runtime/memory_file_manager.py) |
| Write the canonical document and regenerate/remove stale projections | [AssemblyManager](agent_assembly_runtime/assembly_manager.py), [AgentProjectionWriter](agent_assembly_runtime/agent_projection_writer.py) |

The public continuation validates the complete structure before touching memory files. A mismatched group filename now fails without creating a memory file or moving a referenced existing one; [regression cases](tests/test_rejected_save.py) cover both paths.

## Reuse and limits

Keep your UI and execution adapter outside this library. A consumer can load a validated task and choose how to interpret its workflow source. Introducing an executor would require its own execution, permission and failure contract; the current library supplies none of those.

Use trusted authored definitions and one writer per directory. A memory entry with `has_file: true` and an existing `file_path` can move that file into the managed location. The whole save spans several files and is not a crash-atomic transaction. Generated group/task projections can be recreated; keep a backup of your canonical documents and meaningful memory files. Renaming/removing an agent is a separate explicit operation.

An inspect-only save plan or transactional multi-file writer could be useful future extensions. Neither is implemented here.

```sh
python -m pip install pytest
python -m pytest -q
```

[Detailed schema/reference](docs/REFERENCE.md) · [MIT license](LICENSE.md) · [Security boundary](SECURITY.md)
