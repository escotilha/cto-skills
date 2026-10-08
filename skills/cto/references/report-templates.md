# Review artifacts and handoff contract

Write under the project's `.cto/` or another user-approved output directory. Never overwrite a prior run: add a numeric suffix or run ID. Artifacts can contain sensitive evidence; tracking/publishing them is a separate decision.

## Required review core

This is a schema illustration, not a runnable configuration:

```yaml
project: "example-project"
scope: "full" # full|security|architecture|performance|quality|plan|incident|infra
mode: "sequential" # sequential|swarm|delta
model_actual: "operator-selected model or unknown"
harness: "actual runtime/version or unknown"
escalated: "none" # or {from/to: cto-fable, trigger: a|b|c|d, slice: [ids]}
date: "{date}"
reviewed_base: "revision or input-version"
reviewed_head: "revision or input-version"
freshness_confirmed: false
verdict: "BLOCK_ON_CRITICAL"
verdict_note: "One critical issue blocks proceeding"
findings: {critical: 1, high: 0, medium: 0, low: 0}
confidence_gate: 8
evidence_gate: {ran: true, skipped: false, coverage: "1/1", fullCoverage: true, demoted: [], ungraded: []}
scope_coverage: {manifest: 4, covered: 4, coverage: true, gaps: [], highRiskGaps: [], analystsMissing: [], looseMatches: []}
```

Include `## Verdict` and a concise rationale. Keep `verdict` a canonical bare enum string; qualifiers belong in `verdict_note`. Model aliases/pins do not prove which model actually ran. If unavailable, record unknown, not an invented version.

Canonical verdicts:

- **APPROVE:** no CRITICAL or HIGH blockers under the severity ladder; complete evidence and scope are needed to call it clean.
- **APPROVE_WITH_CHANGES:** HIGH, no CRITICAL, concrete blocking changes enumerated.
- **BLOCK_ON_CRITICAL:** CRITICAL fixable items or review coverage gaps; fix/review before proceeding.
- **REJECT:** substantive evidence invalidates the approach and requires redesign.
- **DIAGNOSTIC:** incident root-cause assessment, no approval semantics.

The body adapts to the task. An audit generally includes executive priorities, severity-sorted findings, candidates, cross-concern patterns, dependency-aware fix order, assumptions/unknowns, and next actions. A decision or incident can use a focused argument instead of empty severity tables. Never pad unknown sections with guesses.

Each ordinary finding retains **all** fields of the [canonical analyst schema](synthesis.md): `id,title,source,severity,confidence,file,line,claim,recommendation,verify`. The lead adds `evidenceChecked,evidenceNote,effort,dependencies` after grading/synthesis; these are final-artifact additions, not competing analyst requirements. Tables are a human rendering of the same records, never an excuse to omit ID/title/confidence from machine-readable rows. Orchestrator-computed coverage blockers are the documented arithmetic exception: `confidence:null`, `evidenceChecked:n/a`, and recorded reconciliation provenance/manifest.

`source` distinguishes independent corroboration from repeated wording by one lens. Preserve raw notes separately rather than pasting full transcripts or secrets into a public-facing summary.

## Decision-list overlay

Quote all decision strings, especially YES/NO, because YAML 1.1 parses bare forms as booleans. A boolean is a schema error: require quoting, rather than silently coercing it to a decision.

Synthetic example:

```yaml
decisions:
  - id: batch-summary-reads
    question: "Batch the summary reads?"
    decision: "YES" # YES|NO|DEFER|OUT
    rationale: "Independent existing-record checks make this slice verifiable"
    reversibility: "reversible" # reversible|irreversible
    caveat: "Keep authorization predicates on every batched query"
    discriminatorChecks: [{id: A1, status: satisfied}, {id: A2, status: satisfied}]
    spec: "Replace the per-record read in loadSummaries() with a scoped batch read"
    files: [src/summary/service.ts]
    dependsOn: []
    risk: "solid" # solid|frontier|moonshot
    acceptanceCheck: "Same scoped results, bounded query count on seeded records"
```

Required: ID, question, decision, rationale, reversibility. A code-grounded YES also carries spec, files, dependencies, risk, and acceptance check. YES recommends implementation; NO rejects on merits; DEFER names a missing condition; OUT is outside the goal. No value authorizes execution.

Unknown decision strings clamp to DEFER with the raw value recorded. Unknown reversibility clamps to irreversible; unknown risk to moonshot. Missing/unknown dependency IDs are a planning error: mark the dependent DEFER until reconciled rather than silently making it independent. Cycles are invalid. Nothing depends on a moonshot; move it off the critical path or defer dependent scope. Downstream consumers must independently validate these rules, not trust prose.

## Workplan

Write `.cto/workplan-{date}-{slug}.md` for concrete actionable findings or ≥1 YES. Its frontmatter includes source review, project/date, and items:

```yaml
items:
  - id: fix-token-algorithm
    title: "Restrict the verification algorithm"
    source: sec-token
    severity: "CRITICAL" # null for a decision-derived item
    effort: "QUICK_WIN"
    risk: "solid"
    reversibility: "reversible"
    batch: 1
    dependsOn: []
    files_modify: [src/auth/token.ts]
    files_create: []
    verify: "Isolated mismatched-algorithm test returns unauthorized"
    spec: "In verifyToken(), restrict configured algorithms before verification"
```

Specs come from source actually read, naming functions and constraints. Carry synthesis dependencies into workplan IDs without loss. Compute topological batches; same-batch items are independent and file-disjoint. Effort is QUICK_WIN <1 hour/one file/low risk, MODERATE 1–4 hours, SIGNIFICANT 1–2 days, MAJOR ≥3 days. A MAJOR unresolved design gets a research seed with established architecture, data flow, key paths, constraints, revision, and real open questions, not an invented detailed spec.

Authorized plan annotations use `> NOTE(/cto): [severity] finding; concrete change. (review path #id)`. Without authorization to change the plan, include proposed annotations in the report instead.

## Completion object

Return `{status,analysisType,summary,artifact,verdict,findings,topPriorities,limitations}`. Status is complete/partial/blocked/failed. When handing off actionable work, add:

```json
{
  "recommendedDispatch": {
    "action": "separate-executor",
    "target": ".cto/workplan-{date}-{slug}.md",
    "reason": "Concrete verified checks and dependency-aware specs",
    "alternatives": [{"action": "report-only", "note": "Keep artifacts for manual action"}],
    "gated": ["authorization-sensitive-item"]
  }
}
```

A consumer must check the verdict, evidence completeness, freshness, coverage gaps, decision schema, and its own authorization before acting. Reversibility is not authority. If synthesis did not finish, return partial with `verdict:null`, raw-output paths, and the exact missing phase; do not emit a fabricated review enum. A true child advisor returns and stops; the calling context owns human questions and subsequent execution.

## Optional project configuration

`cto-requirements.md` can declare mode, focus areas, constraints, known issues, excluded scope, and priority questions. Explicit task instructions outrank defaults. Optional HTML must render the same counts/limitations/citations, escape untrusted text, and avoid silently opening a browser or publishing the report.
