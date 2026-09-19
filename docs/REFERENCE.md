# Agent Assembly Runtime


A strict, platform-neutral runtime for canonical configured-agent documents.

The canonical agent JSON is the source of truth. Groups, tasks, and memory files are inspectable projections rebuilt from that document. The implementation normalizes known fields, rejects unknown or structurally invalid state, enforces one-group ownership for each task, and writes projections atomically enough for a local authoring workbench.

```powershell
python -m unittest discover -s tests -v
```

## Included mechanisms

- canonical agent/group/task/package/prompt/memory schemas;
- strict normalization and validation;
- deterministic filenames and contained storage root;
- canonical save/load plus group and task projections;
- memory-file creation and synchronization;
- read-only facade for consumers.

This defines configured workflow actors; it does not make claims about autonomous planning. Embedded workflow/package source is data here and becomes executable only when handed to a runner.

GitHub Actions repeats the tests, source compilation, and package build on
pushes and pull requests.

See [ORIGIN.md](../ORIGIN.md) and [SECURITY.md](../SECURITY.md).
