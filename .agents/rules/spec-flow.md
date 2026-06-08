# Spec-flow rules

This repository follows the spec-driven pipeline in @/AGENTS.md and the
principles in @/memory/constitution.md (always in effect).

- No production code before an approved `spec.md` and `plan.md`.
- Each task is one small, reversible, tested, separately-committed change.
- Stop at every human gate: `spec→plan`, `plan→tasks`, `tasks→implement`.
- Workers operate only within their task's declared file scope.

Phase workflows: `/specify`, `/plan`, `/tasks`, `/implement`, `/verify`.
