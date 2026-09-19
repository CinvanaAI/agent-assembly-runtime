# Security

- The assemblies directory is explicit and resolved before use.
- Names are reduced to safe filename stems.
- Unknown schema fields and invalid statuses fail closed.
- Projection files are derived evidence; canonical agent JSON remains authoritative.
- Embedded source is never executed by this package.

Local filesystem permissions remain the access-control boundary. This package is not a multi-user database or sandbox.
