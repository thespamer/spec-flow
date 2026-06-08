---
name: verify
description: >-
  Phase 5 · Traceability matrix spec↔tests↔code; full suite green.
  Use this whenever the user wants to verify a feature in the spec-driven
  pipeline, or types /verify. Part of the spec-flow workflow defined in AGENTS.md.
---

# /verify

Execute **Phase** `verify` of the spec-driven pipeline.

1. Read the canonical procedure in [`flow/verify.md`](../../../flow/verify.md) and follow it exactly.
2. Honour [`memory/constitution.md`](../../../memory/constitution.md).
3. Delegate the heavy lifting to the **`reviewer`** subagent in a forked context
   so the main thread stays clean (`/agents` → `reviewer`), passing only the
   inputs that phase needs.
4. Respect the human gate at the end of the phase — summarise and stop; do not
   auto-advance to the next phase.

> This file is a thin wrapper. The behaviour is defined in `flow/verify.md`;
> edit that, not this.
