# Credential axis

Compare how an agent integration carries a delegated credential.

The question is not which interface uses fewer tokens. It is who holds the credential when the agent acts for someone else: can the credential be scoped to one person and one tool, revoked while the task is still running, and named in the audit record of the effect.

This repository is the harness. It runs one delegated task through three stand-in adapters:

- `mcp_oauth` — a token minted for one subject and one tool
- `cli_token` — a process token that is not bound to the delegating person
- `skill_cli` — the same process token, reached through a skill wrapper

The stand-ins encode those structural differences so the scorecard and the tests can run without a live identity provider. They are not a measurement of production MCP, CLI, or Skills products. Swap in real adapters before treating a row as a result.

```bash
PYTHONPATH=src python3 -m credential_axis
PYTHONPATH=src python3 -m unittest discover -s tests
```
