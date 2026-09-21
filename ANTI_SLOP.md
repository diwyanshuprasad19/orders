# Anti-slop / aislop (mandatory for PRs)

This service is gated by `platform-ops` like kafka/redis:

```bash
cd ../platform-ops
make anti-slop REPO=<inventory|orders|distributed-tracing>   # aislop ≥ 80
make local-gate REPO=<name>
make auto REPO=<name> TITLE="…"
```

## Rules
- No narrative comments that restate the next line
- No banner `# ===` section comments or apologetic TODOs
- No bare `except:` / empty `except Exception: pass`
- No leftover `pass  # implement later`
- Prefer clear names over `data` / `result` / `temp` / `helper2`
- Run `ruff format` / `ruff check --fix` when configured
- Tools: **aislop**, **sloplint**, **agent-slop-lint**, **ruff**

Do not open a raw `gh pr create` that skips these gates unless `ALLOW_SLOP=1`.
