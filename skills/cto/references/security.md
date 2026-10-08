# Security lens

Own auth, authorization, sessions, API/middleware input handling, secrets boundaries, dependency manifests, and security-relevant callers. Coordinate file ownership through the lead. Scan patterns to choose reads; never emit a vulnerability solely because a token matched.

## Trace the enforcement path

- **Authentication and authorization:** trace every access-granting path, server-side role/permission validation, token/session revocation, MFA/password-reset state transitions, and ownership checks on resource IDs. Exercise skipped, replayed, reordered, and exception paths in isolation.
- **Tenant isolation:** follow context bootstrap for requests and workers, explicit query predicates, joins, writes, raw SQL, and bypass flags. Distinguish logs/warnings from enforcement. A hook name does not prove a query is scoped.
- **Mass assignment:** identify input objects spread into ORM create/update calls. Verify explicit field selection and separate permission checks for privileged fields. Inspect output schemas for internal fields as well.
- **Injection:** trace untrusted data to SQL, shell, headers, logs, filesystem paths, template/HTML sinks, and deserializers. Parameterization of SQL values does not protect dynamically constructed identifiers, order clauses, or JSON paths.
- **Cryptography:** check token algorithm restrictions, signature validation, issuer/audience/expiry, cryptographic randomness, appropriate password hashing, constant-time secret comparisons, and key rotation behavior. Equality on nonsecret enum values is not a timing finding.
- **SSRF:** inspect every tenant/user-controlled URL fetch, redirects, DNS resolution/rebinding, destination allowlists, private/link-local destinations, and actual network controls. Determine which defense is the sole effective one in each environment.
- **Public edges:** verify rate limits on login/reset/OTP and expensive endpoints; CSRF where ambient cookie authentication permits it; browser headers where HTML is served; and CORS against the intended origin model. JSON-only CSP absence is not an HTML exposure.
- **Secrets:** inspect configuration and tracked sources without copying values into outputs. Record location/category and remediation, not credentials. Build arguments, logs, model prompts, and error messages can cross the secret boundary.

## Fail-open and default behavior

Read catches and missing-config branches around permission checks. An auth exception followed by continued execution, default-admin role, `.catch(() => true)` authorization, or a truthy string used as a boolean can open the path. Confirm actual reachability before rating severity. Compare missing, null, empty, false, and malformed states; they may have different intended polarity.

Check deployed CORS, debug mode, session-cookie flags, container users, exposed debug ports, and middleware wiring. Installed middleware is not necessarily applied. Do not rate every configuration choice HIGH without a concrete impact path.

## AI and agent surfaces

- AI endpoints need the intended auth and resource controls. Reachability of a cheap public endpoint is not automatically a breach; trace privilege, spend, and data access.
- RAG/vector retrieval must preserve document ownership and tenant scope. Inspect filters and joins, not only the prompt.
- Administrative system-prompt/tool/model configuration changes need the declared authorization. Separate intended user customization from privileged guard/config mutation.
- Treat model inputs and retrieved/web/tool text as untrusted data. Deterministic runtime supplies credentials; raw secrets do not enter model context. Sanitizing text alone does not prove injection resistance.
- Audit outbound agent actions, scope tools, and inspect sandbox/approval boundaries. Review project hook and MCP configuration as executable supply-chain input; endpoint/proxy overrides may redirect credentials. Frontmatter tool declarations are not enforcement.

## Code archaeology

Select 3–5 security-critical, highly reused, or rarely changed files. History helps identify assumptions worth testing, but age alone never determines severity. Trace trust transitions from untrusted source through validation to privileged sink, including newly added callers that violate older assumptions.

Inspect size/allocation arithmetic, FFI bounds, resource lifetime, parser depth/encoding/null cases, coercion in guards, async TOCTOU gaps, cleanup/error branches, and mutually assumed validation between functions. Read task/change intent alongside the actual behavior. A longstanding bug is still rated by reachable impact rather than an automatic age-based CRITICAL floor.

## Optional tools and noise control

Use installed static analyzers and dependency audits when useful, with the project's rules and output formats. Record absent tools, environment failures, and truncated output as not-run, not zero findings. A scanner result is a lead requiring source validation; clean scanning is not full coverage.

Common false positives: nonsecret equality; random UI jitter/test salts; obvious dummy credentials; trusted literals in HTML/navigation; debug-only logging behind a verified environment guard; bearer-only APIs lacking cookie CSRF; wildcard CORS on public health/docs; trusted JSON parsing; cosmetic deprecation without a vulnerability; `unknown` types narrowed correctly; and uploads whose actual validation/storage chain closes the attack path. Development tooling can still be a real supply-chain risk, so context determines whether an exclusion applies.

Rate confidence as the minimum of concrete exploitability/reproducibility and correctness. Require source plus caller/guard tracing. Emit the complete [canonical analyst finding schema](synthesis.md), optionally extending it with CWE/rule ID, and one accounting line for every manifest item. Use safe synthetic fixtures and isolated tests; live exploit attempts require separate explicit authorization.
