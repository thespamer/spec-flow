# Copilot instructions

This repository follows the spec-driven pipeline in [AGENTS.md](../AGENTS.md) and
the principles in [memory/constitution.md](../memory/constitution.md). Read both.

Do not write production code before an approved `spec.md` and `plan.md`. Drive the
work with the prompt files in `.github/prompts/` (`/specify`, `/plan`, `/tasks`,
`/implement`, `/verify`), each of which follows the matching `flow/<phase>.md`.
Keep tasks small and test-first; stop at every human gate.
