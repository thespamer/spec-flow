---
name: tasks
description: >-
  Phase 3 · Approved plan → tasks.md (ordered, dependency-aware). Pauses for approval.
  Use this whenever the user wants to tasks a feature in the spec-driven
  pipeline, or types /tasks. Part of the spec-flow workflow defined in AGENTS.md.
disable-model-invocation: true
---

# /tasks

Execute **Phase** `tasks` of the spec-driven pipeline.

1. Read the canonical procedure in [`flow/tasks.md`](../../../flow/tasks.md) and follow it exactly.
2. Honour [`memory/constitution.md`](../../../memory/constitution.md).
3. Delegate the heavy lifting to the **`task-decomposer`** subagent in a forked context
   so the main thread stays clean (`/agents` → `task-decomposer`), passing only the
   inputs that phase needs.
4. Respect the human gate at the end of the phase — summarise and stop; do not
   auto-advance to the next phase.

> This file is a thin wrapper. The behaviour is defined in `flow/tasks.md`;
> edit that, not this.
