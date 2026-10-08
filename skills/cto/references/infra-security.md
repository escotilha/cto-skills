# Infrastructure scope

The analyst unit is an operator-supplied host or service, not a repository lens. This file contains methods, no live inventory, connection targets, credential locations, or standing permission to access anything.

## Preflight and boundaries

Require an explicitly authorized inventory containing asset ID, role, OS, approved transport, deployed applications, and relevant policy exceptions. Keep the inventory outside publishable artifacts by default; report asset IDs where addresses are sensitive. Never seek credentials: use an already authorized transport or record cannot-access.

Prefer an operator-controlled read-only transport with an actual command allowlist and audit log. Raw shell/SSH is not read-only by virtue of this prompt. Use it only when authorized; do not bypass a refused command silently. Frontmatter and prose do not mechanically enforce this boundary.

Load prior risks and accepted exceptions. Probe reachability once per asset within the stated timeout, recording failures as coverage gaps. Network membership alone does not establish access permission. Build the context block before analysts; unreachable assets remain in the manifest. Default budget is 15 minutes per asset over the 3–5 most security-critical paths, plus at most five minutes for separately authorized confirmation probes.

Review is observational: no installs, writes, restarts, privilege escalation, key changes, firewall/sysctl changes, or cleanup. Secret-bearing files are assessed by mode/category/location without displaying contents. Redact secrets or personal data from command output before retention. Proposed fixes go to a separate executor workplan.

## Per-asset checklist

**macOS:** disk encryption, system integrity, application firewall/stealth, login/lock policy, updates, administrative users, SSH policy, listeners/bindings, sharing services, package state, sensitive file modes, launch agents/daemons, scheduled jobs, containers, and agent processes. The application firewall is not a complete packet-filter view.

**Linux:** OS/kernel updates, hardening values, root/sudo users, SSH policy, failed-login controls, firewall rules, listeners, service identities, container network/resource limits, proxy/TLS/header configuration, SUID/SGID files, sensitive-file modes, temporary secret artifacts, and scheduler payloads. Container DNAT may bypass the firewall layer being inspected.

**Applications:** follow [security.md](security.md) paths for auth, isolation, untrusted inputs, state transitions, serialization, secrets, and errors. Installed middleware is not evidence of deployed enforcement. Resolve intent versus implementation from actual service configuration.

**AI/agent estate:** model/agent endpoint auth and binding; expensive request limits; assistant/tool configuration permissions; RAG ownership filters; runtime credential boundaries; action audit logs; executable hooks/MCP entries; model/proxy overrides; remote dispatch authorization; launcher permission bypass; and service identity. No brand-specific agent stack is assumed.

## Optional empirical confirmation

Confirmation is off by default. It requires a user/operator-approved probe allowlist naming exact command shapes, target scope, timeout, expected positive artifact, output redaction, and attempt limit. This public export provides no automatic live probe permission or enforcement implementation.

For authorized read-only probes, status is **proven** if the specified positive artifact is observed; **probe-failed** if blocked, errored, ambiguous, or absent; **reasoning-only** if no authorized probe applies; **n/a** for directly observed facts. Preserve exact command and sanitized positive evidence. One attempt per allowed probe; never retry a defended endpoint into success.

Empty stdout, a missing listener row, a timeout, or a permission error is not proof of safety. Conversely, an auth challenge can be evidence a defense worked, but does not prove every route/path is defended. A failed inference probe does not automatically remove a source-grounded concern; report the uncertainty and have independent grading assess the claim.

Examples of low-impact confirmation shapes, **synthetic and still authorization-dependent**: read a service's listener binding; inspect a relevant explicit firewall row; request only a status code from an approved metadata endpoint; test an existing permitted network hop with bounded connection timeout. Never dump response bodies containing prompts/data, generate expensive workloads, pull a model, execute payloads, replay sessions, race writes, create keys, or open a rule to make the test succeed.

## Cross-asset synthesis

Map existing trust edges: key/identity reuse, firewall permissions, reachable services, data access, and dispatch paths. Each chain describes entry point → authorized/observed hop → privilege/data consequence and the link to break first. Do not manufacture severity from a hypothetical hop.

Compound elevation requires evidence of the link and resulting impact. When optional confirmation is enabled, an unproven traversal stays a hypothesis at the higher component severity, naming the missing hop. The same finding on ≥2 assets suggests a shared setup/root cause; compare hardened versus unhardened assets without assuming why they differ.

Infra output includes per-asset summaries, reviewed/skipped status, severity counts, probe-state counts, cross-asset chains, and dependency-aware workplan. Ordinary findings use the [canonical analyst schema](synthesis.md), extended with asset ID and probe status. For directly observed configuration evidence without a source file, set `file` to an asset-qualified evidence-record path and `line` to the cited record line; the grader independently checks the approved observation evidence/transport rather than assuming repository source exists. Probe-state totals sum to the applicable findings; n/a is excluded. Use canonical severity/effort enums and fingerprints based on asset ID, category, and mechanism. Host/service changes remain subject to the executor's authorization and service-impact gate, even if reversible.
