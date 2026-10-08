# CTO skills

Three related skills for evidence-based technical decisions: review a system, escalate a hard forward call, and evaluate improvements to the review method. They share review artifacts, decision discriminators, and a findings ledger so a second opinion or later verification does not discard prior work.

This is a portable public export of skill instructions and supporting methods. It does **not** include a private automation engine, scheduler, historical decision corpus, stored memory, or live configuration. No performance superiority is claimed for the exported bundle.

## Choose a skill

- **cto:** a focused technical question, architecture or plan review, multi-lens audit, infrastructure assessment, incident diagnosis, or delta verification after a fix.
- **cto-fable:** an escalated architecture or direction decision with credible arguments both ways, more than five files/subsystems, conflicting earlier verdicts, or an unattended downstream consumer. The name is retained; it does not require a model named `fable`.
- **cto-evolution:** rank new methods, inspect the top three candidates, and produce a measured improvement proposal for the first two skills.

Example invocations: `/cto review docs/design.md`, `/cto decide cache-or-queue`, `/cto-fable <self-contained hard decision>`, or `$cto-evolution evaluate improvements`. Slash-command and dollar-prefix syntax depend on the host.

## Installation

Clone or download this repository to a local directory. Copy **all three directories together**, preserving their names and relative locations. `cto-fable` and `cto-evolution` use the references in their sibling `cto` directory.

For Claude Code, use a project installation under `.claude/skills/` or a personal installation under `~/.claude/skills/`. For Codex, use `~/.codex/skills/` or the skill directory configured by your host. Install the three `skills/*` folders into that directory, keeping `SKILL.md` at each folder's root. If a destination already exists, compare it and back it up before replacement. Do not overwrite a working private installation as part of trying this export.

These entrypoints use only `name` and `description` frontmatter, avoiding private agent aliases and model pins. Select models through your host's supported controls. If your host supports forked skill execution, run advisory work in a separate context; otherwise retain the advisor/executor separation described in the skills.

## Capabilities and limits

Required for useful reviews: project-file reads, a writable review-output directory, access to the stated requirements and relevant tests, and honest reporting of missing evidence. Git is required for freshness checks on Git-based changes; for other inputs, record their version and freshness explicitly. Executing project tests requires a trusted or isolated test environment.

Native agent tools are preferred for independent analysts and evidence grading. Without them, the lead can apply the four lenses sequentially. This fallback is functional, but **same-context evidence grading is not independent**: findings remain `ungraded`, and the artifact is not a clean approval. Use a separate reviewer session to complete that gate.

Optional: web search and primary-source fetching, semantic file search, static analyzers, dependency audits, a project memory search, read-only infrastructure transport, and an HTML renderer. Missing optional tools are recorded as limitations rather than silently assumed available. Live infrastructure work needs a user-supplied inventory and authorization; the repository contains neither.

The review writes `.cto/review-*.md`, plus a ledger and actionable workplans when applicable. These may contain sensitive project evidence. Keep them in a user-approved output directory and do not publish them by default. An advisory verdict grants no implementation, merge, deployment, or external-publication permission.

## Evolution is proposal-first

**Installing `cto-evolution` does not schedule runs or mechanically enforce adoption gates.** Its default output is a staged, measured proposal; it does not modify installed skills. Scheduling and automatic application require an operator-supplied evaluation/runner integration that recomputes gates from raw records, enforces budgets and write boundaries, binds independent approval to the exact edit, and provides verified rollback.

The method preserves an estate snapshot, ranking and top-three examination, at least **10 usable runs per arm**, **strictly greater than 20% relative weighted error reduction**, an A/A noise check, regression checks, independent review, bounded spending, and rollback. A hash is identity, not a quality score. No evaluation fixtures or scores from the private installation are included. See the [evaluation contract](skills/cto-evolution/references/evaluation-contract.md) before building an integration.

## Validate the package

Run `python3 scripts/validate_bundle.py` with **Python 3.9 or later** from the repository root. It checks the fixed package inventory, skill frontmatter, local Markdown resources, and a small public-footprint screen. It is a packaging check, not a security boundary or proof of review quality. Every publishable file still needs a human or independent privacy review. The validator belongs to the repository package; copying only the skill directories does not install it.

All illustrative scenarios in this bundle are synthetic. The [MIT license](LICENSE) retains the required source attribution.
