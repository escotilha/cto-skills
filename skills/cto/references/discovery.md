# Discovery and scope accounting

Compute shared context before a multi-analyst review. The lead pays for stack discovery once rather than having every analyst rediscover the repository.

Read relevant manifests, dependency locks, entrypoints, test/lint configuration, architecture docs, and a bounded directory map. Use `rg --files` and targeted searches before recursive dumps. Generated, vendor, build, and cache directories ordinarily stay outside source scope. Optional semantic search produces candidate file lists; it does not prove their contents.

The context block contains the target root, actual review base/head, stack, important paths, domain ownership, intended behavior, open finding IDs, and output/time limits. Non-empty means useful domain context, not merely a repository name.

## Manifest construction

- **Diff review:** resolve the actual target/default branch from repository metadata or the explicit task. Never silently guess `origin/main`. Fetch if authorized and record base and head. Capture `git diff --name-only <base>...<head>` and its exit code separately; a pipeline to a counter can hide failure. A missing/unresolved base is uncomputable before invoking the diff.
- **Hosted PR review:** use a paginated file-list API, and cross-check the returned count against the PR's declared changed-file count. Different APIs may use `filename` versus `path`; confirm actual fields. Successful partial pagination is still incomplete.
- **Full/focused review:** enumerate the requested source areas, declared high-risk components, and relevant supporting configuration. Record exclusions. Scope narrowing changes the stated scope, never secretly shortens the denominator.
- **Infra review:** inventory entries supplied by the operator are the manifest, including unreachable entries. Reachability does not remove them from accounting.

Unknown enumeration yields `manifest: null`, `covered: null`, `coverage: null`. A computed empty set yields zero; these are different states. An uncomputable manifest need not stop useful analysis, but cannot support approval.

Mark risk before assigning analysts. High-risk classes include auth, tenant isolation, migrations, CI/CD, infrastructure, approval/merge gates, and secrets handling. Do not reclassify a skipped item as low-risk to make coverage pass.

Each analyst reports one status per manifest item: `reviewed`, `not-applicable`, or `cannot-access: reason`. The final reconciliation uses [synthesis.md](synthesis.md), not the analyst's self-reported overall verdict.

## Isolation for executable checks

A reviewer executing code or mutations creates a scratch copy containing only the needed inputs and routes the tested code to it. Read-only intent is not isolation. Never write fake fixtures or mutated configuration into a shared live root. Establish restorable backups before mutations, restore only those copies, and verify the original bytes afterward. Avoid whole-tree restore/stash/reset commands in a tree containing other sessions' uncommitted work.
