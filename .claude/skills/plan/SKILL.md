---
name: plan
description: >-
  Phase 2 · Approved spec → plan.md (architecture/decisions). Pauses for approval.
  Use this whenever the user wants to plan a feature in the spec-driven
  pipeline, or types /plan. Part of the spec-flow workflow defined in AGENTS.md.
disable-model-invocation: true
---

# /plan

Execute **Phase** `plan` of the spec-driven pipeline.

1. Read the canonical procedure in [`flow/plan.md`](../../../flow/plan.md) and follow it exactly.
2. Honour [`memory/constitution.md`](../../../memory/constitution.md).
3. Delegate the heavy lifting to the **`architect`** subagent in a forked context
   so the main thread stays clean (`/agents` → `architect`), passing only the
   inputs that phase needs.
4. Respect the human gate at the end of the phase — summarise and stop; do not
   auto-advance to the next phase.

> This file is a thin wrapper. The behaviour is defined in `flow/plan.md`;
> edit that, not this.
