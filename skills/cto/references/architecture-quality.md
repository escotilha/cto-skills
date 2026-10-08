# Architecture and quality lenses

These roles share a reference because boundaries, conventions, and testability overlap; they retain distinct findings and scope accounting.

## Architecture

Own the structural layout, module boundaries, public interfaces, data flow, and design requirements. Inspect internals only as needed to trace those boundaries; security and performance retain their specialist paths.

Check cohesion, cycles, shared mutable state, oversized responsibilities, presentation/business/data mixing, accidental database-schema exposure, contract/version drift, and ownership of state transitions. A large file is a prioritization hint rather than a finding by itself. Ask what breaks first at the requested growth factor and whether the current abstraction is verified sound before recommending a rewrite.

For major decisions, use primary code evidence, authoritative pattern/documentation research where useful, credible opposing arguments, and an explicit account of failure modes. Separate hard requirements from preferences and compare the least-complex viable alternatives. Apply [decision-discriminators.md](decision-discriminators.md) to fix/rewrite, build/buy, sequencing, and policy-transfer calls.

For technology choices, a default evaluation matrix is Fit 25%, Maturity 20%, Team fit 20%, Scalability 15%, Ecosystem 10%, Cost 10%. Score each 0–10, then compute the weighted sum. Adjust and register weights before scoring when the task's constraints differ. A score ranks tradeoffs; a failed hard requirement disqualifies an option regardless of its total. Verify current claims from primary sources.

## Quality

Own tests, CI/lint/type-check configuration, documented conventions, dependency policy, and recurrence guards. Map critical behaviors and acceptance criteria to meaningful checks. A tests/source-file ratio or line coverage percentage does not establish enforcement.

Inspect swallowed exceptions, unhandled async errors, logging of sensitive data, dead exports/flags, complex control flow, unexplained linter suppressions, weak type boundaries, drifted schemas, and known-vulnerable dependencies. Correctly narrowed `unknown` is a type-safety tool, not automatically debt. A framework's newer pattern alone is not a reason to migrate working code.

## Guard verification

- Seed at least one excluded-class case for every exclusion predicate. Deleting the predicate must make its test fail.
- Assert a safety flag's effect, including writes suppressed in dry run. Parser defaults alone do not prove enforcement.
- For meta-guards, test behavioral enforcement or an explicit allowed surface. Try at least two unnamed evasions using different APIs/aliases/raw SQL shapes when applicable; forbidden-spelling grep is incomplete by construction.
- Fakes must carry the actual fields the guard reads. Derive error/payload fixtures from real metadata or provoke the real driver error, and validate that derivation.
- Execute positive and negative string-match claims. Driver-added statement text and different database index/column naming can invert a supposedly rare match.

When reviewing guard-bearing changes, establish a scratch base, then mutation-test applicable classes: predicate deletion, enforcement forcing, and contract evasion. Record mutant, actual test output, caught/SURVIVED, and restore verification. Never leave mutants in the working tree or use whole-tree restore to destroy another session's work. A surviving realistic mutant is a finding; coverage cannot substitute for this check.

Both lenses emit the complete [canonical analyst finding schema](synthesis.md), optionally extending it with contract/declaration evidence. Name adjacent lenses when a quality pattern affects auth or resource behavior. Identify systemic patterns across ≥3 files, but avoid multiplying one root cause into many independent findings.
