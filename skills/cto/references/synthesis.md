# Analyst execution, evidence gate, and synthesis

## Analyst prompt contract

Use native agent tools when available; no custom agent definition is required. Give each analyst a self-contained prompt with absolute project/reference paths, precomputed context, assigned files, prior finding IDs, full manifest, and finite time/call/spend budget. Its writable output is a unique `.cto/raw/{run-id}/{lens}.md`; the lead alone owns the final artifact. No analyst implements, grades its own evidence, or spawns further analysts.

Specify the selected model through supported host controls. Use a security-capable reviewer for security and live infrastructure; a stronger decision model should not silently replace that security role. Mechanical formatting can use cheaper settings, but independent evidence judgment must have enough budget to open every cited source. Record actual model/runtime rather than a declared alias. No cost or quality benefit from a model tier is assumed without local measurement.

## Canonical analyst finding schema

This schema is required for every ordinary finding in **all lenses and sequential/swarm paths**. Lens-specific fields are extensions, never replacements for these keys:

```json
{
  "id": "unique-stable-finding-id",
  "title": "Concise issue title",
  "source": "security|architecture|performance|quality|orchestrator",
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "confidence": 8,
  "file": "project-relative/source.ts",
  "line": 42,
  "claim": "Actual behavior, concrete trigger, reachable impact, and evidence",
  "recommendation": "Concrete remedy",
  "verify": "Concrete command/test/observable, or named runtime evidence plan"
}
```

Values above illustrate types/allowed choices, not literal enum strings joined by pipes. IDs are unique across the run, confidence is numeric 0–10, and line is a positive integer citation. Optional extensions include CWE/rule ID, intended contract/declaration, workload, measurement, or probe status. The lead adds effort, dependencies, evidence-grade state, and other final-synthesis fields **later**; analysts need not invent them. The grader payload maps canonical `id` to `finding_id`, preserving identity.

Append the relevant intent-gap question from [intended-vs-implemented.md](intended-vs-implemented.md). Every finding states trigger, reachable impact, and evidence. Cross-domain observations name the adjacent lens in the explanation. Analysts remain independent; discuss overlaps during synthesis rather than converging early on a shared conclusion.

Require a `scopeAccounted` section with exactly one line per manifest item:

```text
<item> | reviewed
<item> | not-applicable
<item> | cannot-access: <specific reason>
```

`reviewed` means actually opened and examined through this lens. Outside ownership is not-applicable only if another lens owns it; a budget/permission/tool failure is cannot-access. Analysts cannot mint reserved `cov-*` coverage findings. File an ordinary evidence-based observation instead.

Prefer completion events over polling. A finite timeout produces partial output, never assumed success. The lead verifies output files exist and contain parseable accounting. For sequential fallback, record the four lens passes and their reads honestly; it provides no cross-context independence.

## Confidence gate

Confidence is `min(reproducibility, correctness)` on 0–10 scales. Reproducibility needs a specific trigger and reachable impact; correctness needs current source reads and caller tracing. ≥8 enters findings, 6–7 enters candidates, <6 is excluded. Claims based only on names, comments, or a grep pattern cap at five.

Each gated finding has an actionable `verify`: a concrete test/command/observable that fails before a fix and proves retirement of the risk afterward. If it needs runtime data, name the required environment, observable, and reason it cannot run now. Such a plan is checkable downstream, but is not a completed proof.

## Independent evidence grading

Run once whenever gated findings exist, irrespective of review size or verdict. Give a separate context only `{finding_id,title,claim,file,line,verify}` and read access. Exclude confidence, severity, analyst reasoning, and fix to reduce anchoring. Its task:

> Reopen every cited source on current disk this turn. Inspect callers/surroundings needed to test the claim. A prompt quotation or memory is insufficient. For each ID return `claim_grounded: GROUNDED|UNGROUNDED`, `verify_runnable: RUNNABLE|NOT_RUNNABLE`, and a note showing what your read established. A concrete named runtime test plan can be RUNNABLE without having run; a vague re-review cannot. Do not implement or judge severity.

Return JSON `{ "verdicts": [{ "finding_id": "...", "claim_grounded": "...", "verify_runnable": "...", "note": "..." }] }`.

Join on the canonical gated list, never the grader's returned list. Unknown IDs credit nothing; duplicate finding IDs or ambiguous grader rows are unresolved. Only an exact GROUNDED+RUNNABLE pair with a valid citation and unique ID is **graded-pass**. Exact UNGROUNDED or NOT_RUNNABLE on an unambiguous row is **graded-demote**, moved to candidates with its note. Everything else is **ungraded**, retained at original severity with a reason.

This gate deliberately retains unresolved findings: a crashed grader must not refute every CRITICAL and accidentally create APPROVE. It fails open **for finding retention**, but blocks any claim of clean evidence. Record `{ran,skipped,coverage,fullCoverage,demoted,ungraded}`. `skipped:true` means zero findings to grade; `ran:false` means missing/degraded execution. Start `fullCoverage:false`; set it only after reconciliation. An unavailable independent context leaves all findings ungraded.

## Scope reconciliation

Scope coverage asks whether the requested inputs were examined, not whether produced findings were graded. Reconcile after analyst/evidence work:

1. Credit an item when at least one completed analyst explicitly marked it reviewed. Not-applicable, cannot-access, absent accounting, crashes, and timeouts credit nothing. Carry cannot-access reasons into coverage gaps and the verdict note.
2. Normalize quoted/backticked, `./`, git diff prefixes, and project-root path variants. Suffix matches must be unique and on path-segment boundaries; ambiguous basenames credit neither path. Record unresolved matches.
3. `coverage` starts null. A computed manifest and completed accounting yield true for complete scope, false for gaps. `manifest:0` differs from unknown `manifest:null`.
4. Append every gap to `gaps`. Each high-risk gap, or null coverage, becomes a CRITICAL `cov-*` finding, generated by lead reconciliation after both gates. Persist these blockers in the ledger as open, with `category:coverage`, `source:scope-coverage`, the manifest/review revision, missing items, and `confidence:null`; arithmetic has no analyst confidence score. Low-risk gaps remain notes and do not block. `coverage:false` with only low-risk gaps may leave APPROVE, but must say incomplete scope; it is not a fully clean review.
5. These arithmetic findings have `evidenceChecked: n/a`, a concrete coverage rerun check, and do not enter the evidence gate denominator. Their recorded lead-reconciliation provenance, not their ID prefix, allows ledger admission without the analyst >=8 gate. They cannot be demoted or used to justify REJECT. An analyst-written `cov-*` is not arithmetic: rename as ordinary, retain its evidence/severity, and grade normally. If that shape lacks confidence, retain it as unscored for grading rather than silently removing a possible CRITICAL. Delta can close a persisted arithmetic blocker only by recorded reconciliation proof that the missing items were reviewed, or the unknown manifest was computed and reconciled, under the blocker’s stated scope and current reviewed revision.

Report `scope_coverage: {manifest,covered,coverage,gaps,highRiskGaps,analystsMissing,looseMatches}`. Unknown counts/gap lists are null, never invented zero. This catches honest abstention and missing results; a dishonest all-reviewed claim still needs corroboration from a tool trail. Do not describe self-reported accounting as proof of every read.

## Three synthesis rubrics

**Severity:** normalize by reachable impact. CRITICAL is outage/data loss/security breach/auth bypass; HIGH is major degradation/security/integrity risk; MEDIUM is moderate performance or maintainability impact; LOW is minor debt/hygiene. Where uncertain, preserve the higher concern until tracing the enforcement path resolves it. A verified guard can cap impact; a decorative guard cannot.

**Cross-concern:** same file flagged by two independent lenses is a possible severity elevation, not a blind rule to multiply duplicate claims. Trace shared impact and consolidate the same root cause. The same issue type in ≥3 files is an emerging pattern. Resolve contradictions against source and record the evidence. Corroboration from one lens repeating itself is not independent. Under the source rubric, confirmed compound cross-concern impact elevates one severity level, with justification.

**Effort and dependency:** QUICK_WIN <1 hour, one file, low risk; MODERATE 1–4 hours; SIGNIFICANT 1–2 days; MAJOR ≥3 days/cross-cutting design. Estimates are planning assumptions, not promises. Output per finding `{effort,dependencies,quickWin}`. Preserve stronger verification checks when consolidating duplicates.

For ≥10 gated findings, separate synthesis agents may apply the rubrics concurrently. Below ten, use one combined pass; absent tools, the lead applies all three sequentially. Zero findings skips only empty synthesis, never coverage reconciliation. Do not substitute raw sorting for severity normalization or cross-concern analysis.

Sort by severity, then quick wins/dependencies and confidence. Copy dependencies into workplan `dependsOn` mechanically. Recompute counts after consolidations, demotions, and appended coverage findings.

## Verdict ladder

Incident scope → DIAGNOSTIC, no approval semantics. Otherwise CRITICAL → BLOCK_ON_CRITICAL; otherwise HIGH → APPROVE_WITH_CHANGES; otherwise APPROVE. The lead may upgrade substantive structural CRITICALs to REJECT if the approach needs redesign, not merely independent fixes. Coverage holes are defects in the review, never evidence the design is unsound.

If the lead's budget expires before synthesis, preserve raw files and return partial status with `verdict:null`. Do not forge a canonical review verdict from unsynthesized self-assessments. If synthesis completed but analysts were missing, write the partial artifact with actual coverage and findings. A consumer must reject ungraded evidence or unknown/high-risk coverage even if the visible enum reads APPROVE.
