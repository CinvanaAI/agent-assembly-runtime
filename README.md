# Agent Assembly Runtime

Author an agent once; keep its group and task files in sync.

Keep an authored agent/task definition as one canonical document while exposing inspectable group, task, and memory files.

## See it work

**Input:** Review Bot with Outcasts and Research groups and one Summarize task.

**Result:** Four JSON files, successful reload, and an explicit rejection of task_staus.

[Read the captured output](examples/result.txt) | [Inspect the example](examples/walkthrough.py)

Python 3.11 or newer. From the repository root:

```sh
python -m pip install -e .
python -m examples.walkthrough
```

The example uses synthetic material and runs offline. The captured output comes from executing this example, not a hand-written mockup.

## How it works

The canonical agent JSON owns each task's group membership. The normalizer checks authored field names before filling defaults, the validator checks the resulting structure, and the projection writer produces inspectable files. A misspelled task field now fails before any file is written.

Implementation: [agent_assembly_runtime/assembly_manager.py](agent_assembly_runtime/assembly_manager.py), [agent_assembly_runtime/agent_normalizer.py](agent_assembly_runtime/agent_normalizer.py), [agent_assembly_runtime/agent_validator.py](agent_assembly_runtime/agent_validator.py).

## Limits

This runtime manages configured documents. Embedded workflow and package source remains data; this package does not run an agent or execute those tasks.

[Reference and CLI details](docs/REFERENCE.md) | [Origin](ORIGIN.md) | [MIT license](LICENSE.md)
