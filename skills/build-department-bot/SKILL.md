---
name: build-department-bot
description: Create safe, minimal, testable, and rollback-ready internal department bots from approved FAQ, Excel, Word, PDF, policy, or process materials. Use when a support or business department wants to launch, rebuild, standardize, audit, or migrate an enterprise knowledge bot; generate its knowledge-base package, prompt, workflow blueprint, test matrix, release checklist, pilot plan, or operating SOP; or configure the bot in an enterprise platform after explicit approval.
---

# Build Department Bot

Create a bot package that is narrower than the source materials, explicit about risk, and easy to test and roll back. Default to an exact-FAQ bot unless the approved use case requires more.

## Non-negotiable principles

1. Treat approved knowledge as the only source of business truth.
2. Prefer “do not answer” over synthesis, guessing, or policy interpretation.
3. Keep knowledge, prompt, and workflow responsibilities separate.
4. Start from the smallest viable architecture.
5. Change one behavior at a time from a named stable version.
6. Test before publishing; preserve a rollback version.
7. Never publish, delete, detach, message users, or upload sensitive materials without the authority required by the active tool policy.

## Choose the operating mode

- **Exact FAQ (default):** one approved question maps to one approved answer; broad queries return up to N real question titles; no match uses a fixed fallback.
- **Guided retrieval:** use when users need category navigation or controlled clarification before exact FAQ lookup.
- **Action workflow:** use only when the bot must call a system, submit a request, or perform a business action. Keep answering and acting in separate branches.

Do not add a workflow merely because the platform supports one. A prompt plus approved FAQ knowledge is sufficient when no deterministic branching or action is needed.

## End-to-end workflow

### 1. Establish the contract

Collect or infer a draft for department, bot name, owner, approved sources, target users, channels, allowed topics, sensitive topics, fallback destination, candidate count, and success criteria.

Stop before production publication if no accountable content owner or approved knowledge source exists. Draft artifacts may still be produced with clearly marked assumptions.

Use `assets/project-intake.yaml` as the intake contract. For the full governance process, read `references/playbook.md`.

### 2. Inventory and normalize knowledge

Inspect all supplied files. Use the appropriate spreadsheet, document, PDF, or knowledge-retrieval skill when the materials require it.

Normalize each answer into one atomic, approved item. Preserve the approved answer verbatim unless the owner explicitly authorizes rewriting. Follow `references/knowledge-schema.md` and copy `assets/knowledge-base-template.md` into the project package.

Flag contradictions, missing owners, stale dates, region-specific rules, personal data, and answers that combine multiple intents. Do not silently resolve them.

### 3. Design the response contract

Generate a prompt from `assets/prompt-template.md` with these behaviors:

- exact match → approved answer only;
- ambiguous query → up to the configured number of real knowledge questions;
- no match, sensitive request, or out-of-scope request → fixed fallback;
- no external knowledge, answer merging, internal IDs, keywords, confidence, or reasoning;
- quoted selections and concrete follow-up questions remain anchored to the quoted message;
- group-chat users must quote or restate the full question when context could be ambiguous.

Read `references/platform-patterns.md` before introducing multi-turn routing or group-chat behavior.

### 4. Design the minimum workflow

Start with:

`Start → Classify → Exact knowledge answer | Greeting | Fixed fallback → End`

Only add a clarification branch if broad queries demonstrably need candidates. Only add an action branch when the business process requires an external operation.

Represent the design using `assets/workflow-blueprint.md`. Keep every output field explicit and use one final user-visible response whenever the platform permits.

### 5. Generate the package

For a new project, run:

```bash
python3 scripts/bootstrap_bot_project.py \
  --department "HRSSC" \
  --bot-name "小H" \
  --owner "HRSSC" \
  --candidate-count 5 \
  --output ./bot-projects/hrssc
```

Replace or populate the generated knowledge base with approved source content. Then run:

```bash
python3 scripts/validate_bot_package.py ./bot-projects/hrssc
```

The generated package must contain the intake, knowledge base, prompt, workflow blueprint, test matrix, release checklist, operations runbook, and manifest.

### 6. Test in layers

Use `references/acceptance.md` and the generated test matrix. At minimum test:

- exact FAQ and common paraphrases;
- broad keywords returning the configured number of real candidates when available;
- no match and non-domain requests;
- sensitive and adversarial requests;
- multiple intents;
- quoted selection and unquoted numeric replies;
- concrete follow-up questions;
- two or more simultaneous group-chat users;
- latency and rollback.

Record expected text before running the test. Do not accept “semantically similar” output where an approved fixed answer is required.

### 7. Pilot and release

Pilot with a small named group. Freeze knowledge during the pilot except for tracked corrections. Classify every incident as content, retrieval, prompt, workflow, platform, or channel-context error.

Publish only after the content owner signs off and a stable rollback version exists. When controlling a UI, read and follow the relevant computer-use or browser-control skill first.

### 8. Operate and improve

Track exact-answer success, fallback rate, wrong-answer rate, latency, unresolved questions, group-context incidents, and changes by version.

For each fix:

1. Restore or branch from the last accepted version.
2. Change one behavior.
3. Run the focused test plus regression suite.
4. Publish a named version.
5. Retain rollback instructions.

## Output contract

Produce both:

1. a human-readable decision summary covering scope, assumptions, risks, and approvals;
2. a machine-usable bot package created from the bundled templates.

If the user asks only for advice or review, do not configure or publish a live bot. If the user asks to build or configure, complete the package first, validate it, then proceed with platform changes within granted authority.

## Resource routing

- Read `references/playbook.md` for governance, roles, phases, and operational metrics.
- Read `references/knowledge-schema.md` when transforming source materials.
- Read `references/platform-patterns.md` when choosing prompt, knowledge, workflow, or group-chat patterns.
- Read `references/acceptance.md` before testing or approving release.
- Copy files from `assets/` rather than recreating the templates.

