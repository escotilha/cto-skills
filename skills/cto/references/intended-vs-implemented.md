# Intended versus implemented behavior

Apply this lens inside the existing analysts' domains. It compares declared contracts with implementation; it is not a fifth analyst and does not invent undocumented product intent.

## Three passes

1. Derive intent from the task, requirements, repository instructions, architecture docs, public schemas, route/permission declarations, and function contracts. Record who may do what, data isolation, documented flows, and invariants.
2. Follow the implementing path: middleware, dependencies, guards, context initialization, query predicates, worker bootstrap, error branches, and callers. A declaration is not evidence a hook fires.
3. Emit only gaps with both an intent-source citation and implementation evidence. If intent is ambiguous, record a question or candidate rather than asserting the author's preferred behavior as a requirement.

Architecture asks whether promised flows and boundaries exist. Security asks whether the declared permission model and secrets boundary are enforced. Quality maps each acceptance criterion to tests that exercise the effect. Performance checks whether documented latency, resource, and scaling requirements correspond to the actual journey and workload.

High-value gap shapes:

- **Decorative enforcement:** the guard exists, but callers never establish its precondition or its matcher never matches. Synthetic example: an ORM isolation hook depends on a context value no request/worker sets.
- **Documented but unimplemented:** a promised flow has no executable path.
- **Implemented but undocumented:** behavior expands scope without an intent source.
- **Unverified rule:** tests exercise lines but never assert the stated effect.
- **Inconsistent enforcement:** some entrypoints obey the rule; other routes or background tasks bypass it.

Emit the complete [canonical analyst finding schema](synthesis.md), extending it with intended-contract and declaration citations; divergent behavior is the canonical claim. Rate by reachable impact after tracing defenses. Two citations improve grounding; they do not independently prove runtime behavior.
