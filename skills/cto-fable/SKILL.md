---
name: cto-fable
description: Escalated technical decision review for hard architecture/direction choices, more than five files or subsystems, conflicting earlier verdicts, or unattended downstream decisions. Uses the shared CTO artifact contract; security audits stay with the baseline security reviewer.
---

# Hard-call escalation

This is the hard-tail decision path over [cto](../cto/SKILL.md), not a default replacement. The retained name `cto-fable` is a skill name, **not a required model alias**. Choose a stronger reasoning-capable model through the host's supported controls and record the model actually used. If you cannot obtain a distinct stronger review context, say so rather than claim escalation.

## Entry gate

Programmatic intake uses exactly the baseline mapping: **a** = more than five files/subsystems; **b** = conflicting applicable discriminators or conflicting prior verdicts for the same finding fingerprint; **c** = conservative checks clamp a holistic YES to DEFER; **d** = declared unattended downstream execution. Accept any of these mapped triggers for a non-security slice; do not impose a second manual-entry predicate or reinterpret their letters. No other event gets an a/b/c/d code.

Human direct invocation may additionally request a hard-ambiguous second opinion: credible expert-divergent arguments with costly wrong choices, a stalled decision, or a long dependency chain. Record `entry: manual` and its reason; record the mapped trigger only if one actually applies, otherwise `trigger: none`. With neither mapped trigger nor an explicit manual hard-call reason, use baseline cto.

Programmatic intake must name its mapped trigger and carry a self-contained slice: question, options, draft decisions, absolute evidence paths, current revisions, requirements, prior findings, and ledger IDs. A separate context may not inherit the parent conversation. Do not reconstruct missing discussion; return the exact missing payload for re-invocation.

Security and exploit-adjacent slices remain on the baseline security-capable reviewer. Split mixed scopes so a direction escalation cannot erase security findings. This routing is a design boundary of this bundle, not a claim that a particular public model is incapable of security work.

## Intent and constraints

The recommendation may feed a downstream executor: a wrong YES creates risk; a wrong DEFER stalls useful work. Ground calls in actual code, requirements, revisions, and check results. Freshness and internal verifiability are joint gates; decompose before deferring and trace enforcement before assigning severity.

When information suffices, make a recommendation rather than repeatedly relitigating settled facts. Before reporting, audit each rationale claim against evidence read this session; name uncertainty instead of assuming it. Report conclusion and supporting evidence, not internal hidden reasoning or transcribed reasoning traces.

## Workflow

Resolve the sibling cto reference directory absolutely before delegating. Reuse its context/freshness triage, deterministic mode selection, manifest, confidence/evidence gates, synthesis, artifact/ledger, and completion contract, **excluding its escalation step**. Recursive escalation from cto-fable is prohibited; return the current assessment or unresolved slice to the original caller. Load per need, never every reference by default.

1. **Load:** requirements, current source state, open ledger entries, and optional prior notes. For a long call, write a notes file containing structural anchors such as file→role and decision→dependency. Notes are memory aids, not new authority or measured performance claims.
2. **Mode:** sequential for a focused decision, swarm for a multi-concern plan/audit, delta for returned fixes, decision-list overlay for multiple choices. Keep the baseline artifact semantics identical.
3. **Adjudicate:** read [decision-discriminators.md](../cto/references/decision-discriminators.md) and the relevant non-security lens. For a gate-feeding choice, record explicit satisfied/failed/unknown checks and conservatively aggregate to DEFER/NO where needed. Name the discriminator and observable tell in the rationale.
4. **Swarm if needed:** build the precomputed context first. Prefer native analysts and [synthesis.md](../cto/references/synthesis.md), leaving specialist models separate from the expensive lead. Do not add agents for work the lead can finish directly without reducing evidence independence. Sequential fallback keeps all lenses, but cannot impersonate an independent grader.
5. **Write:** use [report-templates.md](../cto/references/report-templates.md), [ledger.md](../cto/references/ledger.md), and the baseline workplan/completion object. Record escalation from/to, trigger, slice, actual model/runtime, graded evidence, and coverage. Implementations belong to a separate authorized executor, never this advisory context.

One escalation per baseline run, restricted to the contested slice. The completion object recommends a handoff and lists gated IDs; it grants no implementation/merge/publish authority. A real child advisor returns and stops. The parent handles human interaction and later delta verification.

## Failure handling

A refusal, rate limit, dead analyst, or unavailable tool is a typed incomplete result, never clean success. Preserve partial output and return to baseline cto for the same self-contained question if authorized and within the call/spend cap. Do not retry a provider refusal until it becomes an answer. Record the failed escalation and fresh fallback evidence; do not transfer an unfinished verdict as if reviewed.

The public bundle includes no benchmark proving this tier is faster or more accurate. Any model/effort choice needs local evaluation; changing model policy and skill content simultaneously confounds that comparison. Improvements to this entrypoint follow the same measured proposal method as the sibling [cto-evolution](../cto-evolution/SKILL.md).
