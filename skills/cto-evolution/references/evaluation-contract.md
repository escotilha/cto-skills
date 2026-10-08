# Evaluation and optional runner contract

This document specifies what an operator integration must implement; **it is not such an implementation**. Default cto-evolution writes staged proposals. No scheduled execution, enforcement service, corpus, or automatic applier is bundled.

## Identity and raw records

Use a unique run ID and frozen registered plan: discovery window, candidates, target allowlist, profiles, fixture IDs/weights, expected outcomes, held-out split, model/settings/runtime/instruction identities, evaluation batch size, noise rule, and budgets. Hash the actual text/context supplied, not merely a version label. Snapshot drift invalidates prior baseline status until remeasured.

Adoption error, regression, covered-gain, and A/A/A/B calculations use the registered **held-out evaluation corpus**; do not pool training/tuning cases into it. The edit author and coverage assessor may see held-out scenarios and IDs but not their expected outcomes. The independent grader alone receives those frozen expectations. Exposing answers to the author invalidates that split and requires a new frozen corpus and baseline.

A raw sweep record contains profile, arm, candidate ID, context hash, fixture hash, actual model/settings/runtime, run index/time, raw decision output, raw independent comparison output, per-ID boolean match results, typed error (if any), usage, and measured process adherence. Preserve outputs as produced and enough audit data to inspect failures; redact secret values.

Blind decision workers see scenarios and the relevant skill text, not expected outcomes. Comparison graders see the scenario, produced output, and frozen outcome/assertions, not the skill label or author-controlled transcript. Independent verification reopens evidence. Asking for a concise conclusion/evidence is different from extracting hidden reasoning; never ask workers to transcribe private reasoning traces.

Invalid weights, missing/duplicate/unknown fixture IDs, nonboolean matches, refused/timed-out/incomplete calls, and nonfinite values make a sweep unusable. Exclude unusable sweeps from both numerator and denominator **for reported scores only**, and report counts. Adoption eligibility separately requires every registered sweep to be usable; a usable subset, even >=10 sweeps, cannot pass an incomplete batch. **Do not top up or repeatedly retry an incomplete registered batch into an apparent win.** A complete new preregistered batch is a new attempt subject to the total cap, not a way to hide the first outcome.

## Error and improvement

For a usable sweep with weights `w_i>0` and binary match `m_i`:

```text
error = sum(w_i * (1 - m_i)) / sum(w_i)
accuracy = 1 - error
relative_reduction = (mean_baseline_error - mean_candidate_error) / mean_baseline_error
```

Both arms require ≥10 usable complete sweeps and equal counts; every registered sweep is usable. Baseline error must be positive. Relative reduction must be **strictly >0.20**, and mean candidate accuracy **≥0.90**. A synthetic example: baseline error 0.10 to candidate 0.08 is exactly 20% reduction and **fails**; 0.10 to 0.075 is 25% reduction and passes this threshold only, not the remaining gates. Hashes and inferred scores never substitute for measured runs.

## Fixture coverage and regressions

An independent coverage assessment must identify fixture IDs that exercise the exact proposed edit. Empty coverage stages the proposal. The assessment and its IDs are bound to the edit digest; an applier recomputes/validates that binding, not a caller's hand-written list.

For balanced `n` runs, fixture pass rate is passed runs/n. A regression is:

```text
candidate_pass_rate < baseline_pass_rate - 1/n
```

The strict comparison permits a drop of exactly one run as the source method's noise allowance; it does **not** promise zero individual failed cases. Report every drop, including those within allowance, and require an operator's stricter safety-critical constraints where registered. No fixture may regress beyond this allowance. At least one edit-covered fixture must show a positive pass-rate gain. For shared references, all affected profiles must independently pass.

## Noise gate

Pre-register the deployed-versus-itself (A/A) procedure and record its observed spread before comparing edits. Candidate improvement must exceed that registered noise envelope. Small samples underrepresent tails; ten runs is a floor, not a guarantee of adequate power. Report uncertainty and the run count needed for the effect of interest when an inconclusive comparison cannot support adoption.

Separately, perform the **A/B significance/effect test** on accuracy-score arrays for balanced baseline/candidate arms. Each array element is the weighted accuracy of **one complete sweep**, not one fixture result; array length is the number of usable sweeps in that arm. Require candidate mean > baseline mean; a two-sided tie-corrected Mann–Whitney U result with **p<0.05**; and **Cohen's d≥0.2** in the improvement direction. These thresholds do not apply to the A/A comparison. Use average ranks for ties. Cohen's d is candidate mean minus baseline mean over pooled sample standard deviation; if variance is zero, equal means fail and a positive difference has unbounded standardized effect. A zero-variance or malformed statistical calculation must be represented explicitly, never accepted from a string sentinel.

The source statistical recipe uses a normal approximation with tie correction and no continuity correction for U. A runner choosing another estimator/exact test must register it and recalibrate against seeded controls rather than silently changing the gate. Do not call a significant A/B test alone a completed A/A baseline measurement; they answer different questions.

Track process adherence independently of decision correctness. Verify phases by their artifacts/tool evidence; a worker's final claim that it followed the procedure is insufficient.

## Independent verifier and content screen

Give a separate verifier the exact bounded patch, fetched source, measured gate records, snapshot identities, and limitations. It can approve only coherent decision guidance that does not weaken safety or change authority. It sees the produced artifact, not the author's persuasive transcript. Record its context/run identity and explicit APPROVE bound to the edit digest. Reject or unavailable is no-adoption.

Allowed targets are the two entrypoints and shared decision-discriminator file, supplied as an exact operator path allowlist. Reject traversal, symlink escapes, mismatched preimages, multihit exact-match patches, and out-of-bound changes. Do not modify credentials, model policy, permissions, hooks, scheduler/configuration, or global rules in a skill-content trial. Screens and allowed-tools prose are not the write boundary; an integration needs actual filesystem/process restrictions.

## Optional mechanical application

An integration must enforce, rather than merely prompt for:

1. One pass and ≤1 adoption per configured day, a single-run lock, a finite timeout/call/cost budget, no-progress stop, and ≤3 candidates. Defaults are 40 changed lines and 4,000 replacement characters per exact allowlisted edit.
2. Operator-authorized execution and a STOP primitive read before each model call and immediately before applying. Absence/errors in required gate state fail toward no-write.
3. Recalculation from raw records of this candidate's arms, coverage, all affected profiles, statistics, and bound independent verdict. A caller-supplied score or APPROVE string cannot bypass the gate.
4. Current preimage, corpus, profile context and runtime identity checks immediately before write. A changed source after review invalidates approval.
5. Verified byte-exact backup, atomic replacement, expected postimage verification, and append-only adoption record. A failed postimage restores its own verified backup and reports failure.
6. Rollback only when current hash matches the recorded adoption postimage and the backup matches the preimage. Later changes require reconciliation, not forced overwrite. Preserve both adoption and rollback events.
7. Fresh-process validation of startup-loaded skill state. In-session success can reflect a stale cache.

Before unattended arming, replay a seeded dry run with randomized ordering/faults and observe every cap, lock, STOP, stale-context refusal, gate-error path, and rollback boundary fire. A single happy-path run or a prompt promising enforcement is insufficient. Report exact seed and failed condition on faults.

## Scope of the claim

Blind fixture decisions from skill text are a **proxy**, not end-to-end measurement of source reads, security depth, severity calibration, parallel synthesis, report usability, latency, or spend. Extend independent fixtures to those dimensions before claiming improvement in them. No fresh expected outcome can be inferred from the candidate being tested. Keep rejected candidates and their reasons so the same losing edits are not continually rediscovered.
