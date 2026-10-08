---
name: cto
description: Evidence-based technical advice, focused reviews, multi-lens architecture/security/performance/quality audits, plan review, incident diagnosis, forward decision lists, and delta verification of prior findings.
---

# CTO technical advisor

Produce a durable, evidence-based recommendation at `.cto/review-{date}-{slug}.md`. This skill advises; an executor in a separate context implements only within the user's authorization. A verdict is never permission to merge, deploy, publish, or change a live service.

Resolve this skill's installed directory once, then resolve reference paths absolutely before giving them to agents working in another directory. Load only the references needed for the current scope.

## 1. Load context and establish freshness

Read the user's question, `cto-requirements.md` if present, repository instructions, relevant test reports, and `.cto/ledger.json`. An optional project memory or notes search can supply prior decisions. Include open in-scope finding IDs and checks in analyst prompts: report their current status rather than re-reporting them as new.

For a Git change, resolve the actual target/default branch, fetch the relevant remote when authorized, and record the reviewed base and head. If fetching is unavailable, state that freshness is unconfirmed. A stale branch can make already-merged work appear new or revert it. Review against current target state, not just the branch's original baseline.

Triage in a fixed sequence: load context, confirm freshness, execute trusted in-scope ledger checks, scan the change or new evidence, then apply forward-call discriminators. A failed check, new gated finding, or tripped discriminator is an item. An open unverified finding prevents a clean pass.

## 2. Select the mode

Honor an explicit `sequential` or `swarm` request. Otherwise check in this order:

1. `delta`, `re-review`, or a prior `.cto/review-*`/`.cto/workplan-*` handed back after implementation: ledger-driven **delta**, no fresh audit.
2. Infrastructure/estate/host scope: **infra**, using the user-supplied inventory and [infra-security.md](references/infra-security.md).
3. Full audit, launch review, incident diagnosis, or a plan spanning multiple concerns: **swarm**.
4. One scoped question or one-domain plan: **sequential**.
5. No scope: sequential over the most recent change set, explicitly stating that assumption.

For a set of forward choices, add the **decision-list overlay** to either analysis mode. Emit one `"YES" | "NO" | "DEFER" | "OUT"` decision per option, with reversibility and concrete planning fields for code-grounded YES entries. Use the [artifact contract](references/report-templates.md).

### Escalation gate

For a non-security contested slice, escalate once to the sibling [cto-fable skill](../cto-fable/SKILL.md) if any applies: **(a)** more than five files/subsystems, **(b)** applicable discriminators conflict or the same finding fingerprint received conflicting verdicts, **(c)** conservative checks clamp a holistic YES to DEFER, or **(d)** the caller declares unattended downstream execution.

The payload must include the question, options, absolute evidence paths, relevant revisions and ledger IDs, draft decisions, and trigger. Never rely on parent-conversation state. Split mixed security scope out to the baseline security review. If a stronger separate context is unavailable, record the escalation as unavailable and leave contested choices deferred; do not claim it ran.

## 3. Build the context block and scope manifest

Read stack manifests, directory layout, test/lint configuration, and relevant requirements. Precompute key paths and file lists for each lens; optional semantic search supplements actual file reads. Before spawning any analyst, require a **non-empty context block**: stack, target paths, requirements, scope, prior findings, and budget. If absent, stop and report the missing context rather than starting blind discovery in every agent.

Compute the complete scope manifest once: changed files for a diff, enumerated source areas for a full/focused review, or inventory entries for infrastructure. Capture each command's status; failure is not an empty set. An unresolved base, truncated API list, count mismatch, or inaccessible enumeration means `coverage: null`, never zero or clean. Narrow an oversized scope explicitly rather than truncating its denominator. Details: [discovery.md](references/discovery.md).

## 4. Execute the review

Sequential: read the relevant lens and answer the question directly. Forward calls also load [decision-discriminators.md](references/decision-discriminators.md) and name the applicable checks in the rationale.

Swarm: prefer four independent native-agent analysts, security, architecture, performance, and quality. Assign files and output paths, supply the precomputed context and full manifest, and include the intent-versus-implementation question for each lens. Agents do not implement, edit live inputs, or grade their own evidence. Use [synthesis.md](references/synthesis.md) for prompts, checks, and accounting. If agent tools are absent, apply all four lenses sequentially and record the independence limitation.

Use [security.md](references/security.md), [performance.md](references/performance.md), and [architecture-quality.md](references/architecture-quality.md). The cross-cutting [intended-vs-implemented.md](references/intended-vs-implemented.md) compares declared contracts with actual paths.

Set finite time/call/spend limits before dispatch. Use completion notifications when available; a timeout or failed analyst contributes no scope coverage. Preserve partial output and state which phase did not finish.

## 5. Grade evidence, reconcile coverage, synthesize

Confidence is the minimum of reproducibility and correctness, each out of ten: **≥8** main findings; **6–7** candidates; **<6** excluded. A behavior claim without actual source support caps at five. Every gated finding carries a concrete `verify` check or explicitly names the runtime evidence needed.

When any gated finding exists, use **one independent evidence grader** in a separate context. Give only `{finding_id,title,claim,file,line,verify}`, not the author's severity, confidence, proposed fix, or reasoning. The grader reopens every cited file from current disk and returns `GROUNDED|UNGROUNDED` and `RUNNABLE|NOT_RUNNABLE` with evidence.

Join against the canonical finding list in three states: explicit `GROUNDED` + `RUNNABLE` passes; explicit negative demotes to candidates; omitted, malformed, duplicate, unavailable, or timed-out grades remain **ungraded** at their original severity. A grader failure never erases findings. Without an independent grader, record the degraded gate; same-context rereading cannot satisfy independence. An approval with ungraded findings is not clean.

Reconcile the scope manifest with actual `reviewed` accounting. `not-applicable`, `cannot-access`, and crashed analysts do not count. Each unreviewed high-risk item, or an unknown manifest, becomes an orchestrator-generated **CRITICAL coverage finding**, appended after evidence grading and never demoted. Low-risk gaps are recorded without blocking. Coverage findings indicate an incomplete review, never grounds for redesign. Full procedure and reserved-ID handling: [synthesis.md](references/synthesis.md).

Normalize severity, reconcile contradictions and duplicates, identify cross-concern/root-cause patterns, then estimate effort and dependencies. Do these rubrics even in a small inline synthesis; raw sorting is insufficient.

Compute the verdict: incident → `DIAGNOSTIC`; else any CRITICAL → `BLOCK_ON_CRITICAL`; else any HIGH → `APPROVE_WITH_CHANGES`; else `APPROVE`. Upgrade to `REJECT` only when actual substantive CRITICALs show the approach itself needs redesign. Coverage CRITICALs do not establish that. Keep qualifiers in `verdict_note`, not the enum.

## 6. Write artifacts and update the ledger

Write the [required artifact core](references/report-templates.md), including evidence and scope coverage even on a zero-finding pass. A clean fast path requires confirmed freshness, no unresolved in-scope findings, no new gated issue, and complete known coverage; still write the short artifact.

For actionable findings or any YES decision, write a companion workplan with source IDs, file-level specs, checks, effort, dependencies, and file-disjoint topological batches. A major unresolved design gets a research seed rather than an invented implementation spec. Annotate a plan only when the user authorized editing it; otherwise attach proposed annotations to the review.

Upsert `.cto/ledger.json` using content fingerprints, not moving line numbers. Persist orchestrator-computed coverage blockers too, with their manifest/provenance and `confidence:null`; they do not pass through analyst confidence grading. A finding becomes fixed only through a passing check, and that check must fail on the original faulty state. An independently disproven finding becomes `refuted`, with evidence and a reason, never `fixed`; refuted entries retain history and are not open blockers. Do not execute arbitrary ledger commands without first reviewing them and using an appropriate trusted or isolated test environment. See [ledger.md](references/ledger.md).

## 7. Complete and hand off

Emit the completion object with status, artifact path, canonical verdict, counts, coverage limitations, and `recommendedDispatch` when a workplan/decisions exists. Its shape is `{action,target,reason,alternatives,gated}`; `gated` contains irreversible or otherwise authorization-sensitive item IDs. The recommendation carries no authority to act.

Return the artifact and stop when serving as a real advisory child. A parent owns implementation and any human interaction. If end-to-end execution was already authorized, it may dispatch a separate executor within that scope; this advisor never implements its own recommendation. After execution, run delta verification of the dispatched items and report closed versus still open.

Optional HTML is an additional rendering of the same artifact, using a user-supplied renderer; it must preserve counts, limitations, and citations. Do not open a browser in an unattended run.
