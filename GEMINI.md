# GEMINI.md

This project uses the spec-driven pipeline defined in **[AGENTS.md](./AGENTS.md)**
and **[memory/constitution.md](./memory/constitution.md)**. Follow those.

Gemini CLI / Google Antigravity specifics:
- Behaviour rules live in `.agents/rules/spec-flow.md` (auto-loaded).
- Phase commands are workflows in `.agents/workflows/<phase>.md`, triggered with
  `/specify`, `/plan`, `/tasks`, `/implement`, `/verify` in agent chat.
- The canonical procedure for every phase is `flow/<phase>.md`.
