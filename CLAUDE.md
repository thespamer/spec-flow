# CLAUDE.md

This project uses the spec-driven pipeline defined in **[AGENTS.md](./AGENTS.md)**
and **[memory/constitution.md](./memory/constitution.md)**. Read both first.

Claude Code specifics:
- Each phase is a **skill** in `.claude/skills/<phase>/` — run with `/specify`,
  `/plan`, `/tasks`, `/implement`, `/verify`. Side-effecting phases have
  `disable-model-invocation: true`, so they only run when you call them.
- Phase work is delegated to **subagents** in `.claude/agents/`
  (`spec-writer`, `architect`, `task-decomposer`, `developer`, `reviewer`).
- Hooks in `.claude/settings.json` run lint/tests after edits.
- The canonical procedure for every phase is still `flow/<phase>.md` — the skill
  is a thin wrapper. Edit `flow/*.md`, not the wrappers.
