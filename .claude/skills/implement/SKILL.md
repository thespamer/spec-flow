---
name: implement
description: >-
  Phase 4 · Execute tasks; one isolated worker + one commit per task (TDD).
  Use this whenever the user wants to implement a feature in the spec-driven
  pipeline, or types /implement. Part of the spec-flow workflow defined in AGENTS.md.
disable-model-invocation: true
---

# /implement

Execute **Phase** `implement` of the spec-driven pipeline.

1. Read the canonical procedure in [`flow/implement.md`](../../../flow/implement.md) and follow it exactly.
2. Honour [`memory/constitution.md`](../../../memory/constitution.md).
3. Delegate the heavy lifting to the **`developer`** subagent in a forked context
   so the main thread stays clean (`/agents` → `developer`), passing only the
   inputs that phase needs.
4. Respect the human gate at the end of the phase — summarise and stop; do not
   auto-advance to the next phase.

> This file is a thin wrapper. The behaviour is defined in `flow/implement.md`;
> edit that, not this.
