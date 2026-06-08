---
name: specify
description: >-
  Phase 1 · Idea → spec.md (EARS requirements). Pauses for approval.
  Use this whenever the user wants to specify a feature in the spec-driven
  pipeline, or types /specify. Part of the spec-flow workflow defined in AGENTS.md.
disable-model-invocation: true
---

# /specify

Execute **Phase** `specify` of the spec-driven pipeline.

1. Read the canonical procedure in [`flow/specify.md`](../../../flow/specify.md) and follow it exactly.
2. Honour [`memory/constitution.md`](../../../memory/constitution.md).
3. Delegate the heavy lifting to the **`spec-writer`** subagent in a forked context
   so the main thread stays clean (`/agents` → `spec-writer`), passing only the
   inputs that phase needs.
4. Respect the human gate at the end of the phase — summarise and stop; do not
   auto-advance to the next phase.

> This file is a thin wrapper. The behaviour is defined in `flow/specify.md`;
> edit that, not this.
