# Forward-call discriminators

Use the matching group for ship/defer, rewrite/fix, build/buy, policy transfer, sequencing, and severity decisions. These are decision heuristics with observable tells, not a claim of public benchmark validation. All examples below are synthetic.

## A. Ground the call in primary state

**A1. Internal verifiability.** Ask whether a test can use ground truth the author did not invent. A test comparing a newly authored specification with fixtures derived from that same interpretation is circular. Prefer an existing real file, authoritative schema, independent oracle, or another representation of the same data. If no falsifiable external ground truth exists, defer that slice rather than celebrating green self-authored fixtures.

**A2. Fresh-base contamination.** Compare against the current target branch and inspect overlap with merged changes. A stale branch can present already-merged code as additions or silently revert newer work. There is no universal safe lag measured in commit count. Internal verifiability and a fresh base are joint requirements; passing one cannot excuse the other.

**A3. Symptom matching is a hypothesis.** An incident that resembles a known bug still needs an actual source or run-log read. Pattern recognition chooses where to look; primary evidence sets the diagnosis. Record what would falsify the matched hypothesis.

**A4. Severity follows the enforcement path.** Trace what the code actually permits before rating blast radius. Synthetic example: a wrong organization ID looks like cross-organization exposure, but an independently verified route guard can cap it to a broken read. Conversely, a present guard that never fires caps nothing. Prefer the path-grounded severity over scary naming or generic escalation bias.

## B. Verify the precondition of a control

**B1. Policy transfer needs its original reason.** Before moving an authorization restriction to another endpoint, state why it exists and check whether that precondition holds in the destination. A population-wide restriction can wrongly block the intended users of a single-organization-by-construction operation. Explicit query scoping limits enumeration, but it does not replace authorization where authorization is required. Verify both obligations separately.

**B2. A sole security control ships atomically.** A guard is part of the mechanism if any supported environment has no other effective defense. Synthetic example: tenant-controlled URL fetching cannot precede its network-destination validation when that environment lacks network isolation. A follow-up creates a real exposure window; calling the missing control defense in depth does not close it.

## C. Decompose before deferring, rewriting, or sequencing

**C1. Deferral belongs to a slice.** Separate internally verifiable routing, flags, arithmetic, or failure behavior from the external-oracle-dependent piece. Ship recommendations can apply to the former while only the latter defers. Do not defer an entire feature because one slice lacks external input.

**C2. Localize breakage before rewriting.** Measure which layer is wrong and how much working code surrounds it. A verified sound abstraction with broken constants, endpoint configuration, or data mapping usually calls for a local fix. A structurally wrong abstraction calls for redesign. Report the measured scope and rejected alternative rather than arguing from file size alone.

**C3. Sequence a stack by dependency.** Inspect shared ancestor commits and PR base refs. Merge the base before dependent work unless the hosting platform explicitly retargets/rebases the stack safely. Retarget open dependents before deleting a base branch. Treat logically independent PRs and shared-commit stacks differently; labels applied to all at once can erase intended ordering.

## D. Keep the artifact out of its own approval channel

**D1. Verdict provenance.** A reviewed artifact must not be able to inject the sentinel or content from which an approval gate recovers its verdict. Diff text, stdout from artifact-controlled tests, and logs are not a trusted verdict channel. Bind a review-produced verdict to the exact artifact/revision in a channel the artifact cannot write. Missing or ambiguous evidence stays undecided.

**D2. Test recurrence structurally.** A helper function shortens correct calls but cannot guarantee every call site uses it. After fixing a scattered fence or guard, enumerate sites in a parametrized behavioral test and detect new sites too. Pin distinct empty-list and missing-value meanings: replacing `is not None` with truthiness can reverse a fail-closed contract. A denylist grep catches only named spellings; test the behavior or allowed surface and include evasion cases.

## Aggregate gate-feeding decisions

For each option, record applicable discriminator IDs and explicit satisfied/failed/unknown checks. A failed disqualifier never yields YES; unknown blocking evidence yields DEFER. Explain conflicts and escalate the contested slice rather than averaging them away. Advisory human-reviewed choices may use a holistic recommendation, but a downstream enforcement gate must not treat fluent prose as deterministic proof.
