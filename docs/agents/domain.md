# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`DESIGN.md`** at the repo root: the system design document the course requires. It carries the project's vocabulary (for example `ETA_safe`, Profile, Validator, RouteSnapshot, plan status) together with requirements, architecture, data contracts and the algorithm. Read the sections relevant to the topic.
- **`docs/spec/`**: the specs derived from `DESIGN.md`. Check each file's status line first; a Draft that is not frozen is not an accepted contract.
- **`CONTEXT.md`** and **`docs/adr/`**: neither exists yet. If they don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The `/domain-modeling` skill creates them lazily when terms or decisions actually get resolved.

## File structure

This is a single-context repo: one product, one glossary.

```text
/
├── DESIGN.md          ← design document and current source of vocabulary
├── CONTEXT.md         ← glossary (create only when needed)
├── docs/adr/          ← decisions (create only when needed)
├── docs/spec/         ← specs
└── src/moto_copilot/  ← implementation
```

## Use the project's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as `DESIGN.md` and the specs define it. Don't drift to synonyms, and follow the wording rules in the root `CLAUDE.md` (for example, `ETA_safe` is never called a P90).

If the concept you need isn't defined yet, that's a signal: either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/domain-modeling`).

## Private data

Never read, list or search `data/`. Give every search an explicit path (`DESIGN.md`, `README.md`, `docs/`, `src/`, `tests/`, `experiments/`, `prototype/`); never search from the repo root. See the root `CLAUDE.md`.

## Flag ADR conflicts

If your output contradicts an existing decision record, surface it explicitly rather than silently overriding.
