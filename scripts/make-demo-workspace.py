#!/usr/bin/env python3
"""Build a staged demo workspace for the README screenshots.

Clones the *shape* of a real .agentflow task/chat (so every field the UI reads
is present and correctly typed) and replaces the content with a curated demo
narrative: one product feature carried end-to-end by three CLIs.
"""

import json
import os
from pathlib import Path

DEMO = Path(os.path.expanduser("~/Demo/orbit-dashboard"))
AF = DEMO / ".agentflow"
TASK_ID = "20260803-094120-stripe-checkout"
TASK = AF / "tasks" / TASK_ID
LOGS = TASK / "logs"

D = "2026-08-03"  # display date


def t(hhmm, ss="00"):  # ISO timestamp (UTC); +4h so it renders as morning local time
    h, m = hhmm.split(":")
    return f"{D}T{int(h) + 4:02d}:{m}:{ss}+00:00"


for p in (LOGS,):
    p.mkdir(parents=True, exist_ok=True)

# --- a small, believable project so the tree and status bar read well --------
(DEMO / "src" / "components").mkdir(parents=True, exist_ok=True)
(DEMO / "src" / "lib").mkdir(parents=True, exist_ok=True)
(DEMO / "server" / "routes").mkdir(parents=True, exist_ok=True)
(DEMO / "package.json").write_text(
    json.dumps(
        {
            "name": "orbit-dashboard",
            "version": "2.4.1",
            "private": True,
            "scripts": {"dev": "vite", "build": "vite build", "test": "vitest run"},
        },
        indent=2,
    )
    + "\n"
)
(DEMO / "README.md").write_text("# Orbit Dashboard\n\nAnalytics for small teams.\n")
(DEMO / "src" / "components" / "PricingTable.tsx").write_text("export function PricingTable() {\n  return null;\n}\n")
(DEMO / "src" / "lib" / "billing.ts").write_text("export const PLANS = ['starter', 'team', 'scale'] as const;\n")
(DEMO / "server" / "routes" / "checkout.ts").write_text("export async function createCheckoutSession() {}\n")

# --- task.json ---------------------------------------------------------------
task = {
    "id": TASK_ID,
    "title": "stripe-checkout",
    "goal": "Add Stripe Checkout to the pricing page: a hosted checkout session per plan, "
    "a webhook that upgrades the workspace on payment, and tests for both paths.",
    "createdAt": t("09:41"),
    "status": "done",
    "steps": {
        "codex_spec": {
            "status": "succeeded",
            "provider": "codex",
            "runId": "a71f0c93be22",
            "updatedAt": t("09:44", "18"),
            "exitCode": 0,
            "artifactsWritten": ["01_CODEX_SPEC.md", "02_CODEX_IMPLEMENTATION_PLAN.md"],
            "codeChanged": [],
            "promptFile": f"{D.replace('-', '')}-094120-codex_spec.prompt.txt",
            "logFile": f"{D.replace('-', '')}-094120-codex_spec.log",
        },
        "claude_implement": {
            "status": "succeeded",
            "provider": "claude",
            "runId": "5c2e8d10a447",
            "updatedAt": t("09:51", "36"),
            "exitCode": 0,
            "artifactsWritten": ["04_CLAUDE_IMPLEMENTATION_SUMMARY.md"],
            "codeChanged": [
                "src/components/PricingTable.tsx",
                "src/lib/billing.ts",
                "server/routes/checkout.ts",
                "server/routes/webhook.ts",
            ],
            "promptFile": f"{D.replace('-', '')}-094432-claude_implement.prompt.txt",
            "logFile": f"{D.replace('-', '')}-094432-claude_implement.log",
        },
        "gemini_qa": {
            "status": "succeeded",
            "provider": "antigravity",
            "runId": "9b4a17ee0c85",
            "updatedAt": t("09:55", "02"),
            "exitCode": 0,
            "artifactsWritten": ["05_QA_RESULTS.md"],
            "codeChanged": [],
            "promptFile": f"{D.replace('-', '')}-095136-gemini_qa.prompt.txt",
            "logFile": f"{D.replace('-', '')}-095136-gemini_qa.log",
        },
        "codex_review": {
            "status": "succeeded",
            "provider": "codex",
            "runId": "3f8d55c1907b",
            "updatedAt": t("09:57", "44"),
            "exitCode": 0,
            "artifactsWritten": ["07_CODEX_FINAL_REVIEW.md"],
            "codeChanged": [],
            "promptFile": f"{D.replace('-', '')}-095502-codex_review.prompt.txt",
            "logFile": f"{D.replace('-', '')}-095502-codex_review.log",
        },
        "claude_fix": {"status": "idle", "provider": "claude"},
    },
    "fullSequence": {"status": "idle", "currentStep": None},
    "orchestrated": True,
    "consults": 4,
    "orchestratorVerdict": {
        "verdict": "done",
        "reason": "Checkout session and webhook are implemented behind the existing plan config, "
        "QA passed 18 tests including both webhook paths, and final review found no blocking issues.",
        "at": t("09:57", "51"),
    },
    "events": [
        {
            "time": t("09:41"),
            "type": "task_created",
            "step": None,
            "provider": None,
            "detail": f"task created — handoff files written to .agentflow/tasks/{TASK_ID}/ (9 files)",
        },
        {
            "time": t("09:41", "02"),
            "type": "queued",
            "step": None,
            "provider": None,
            "detail": "orchestrator queued 1 step(s): Write Spec→codex — the system will cue each agent in order",
        },
        {
            "time": t("09:41", "20"),
            "type": "step_started",
            "step": "codex_spec",
            "provider": "codex",
            "detail": "orchestrator routed Write Spec → codex (sent 812 chars; reads: 00_USER_GOAL.md)",
        },
        {
            "time": t("09:44", "18"),
            "type": "step_finished",
            "step": "codex_spec",
            "provider": "codex",
            "detail": "codex finished Write Spec: succeeded (exit 0, 178.2s, 1,204 chars out), "
            "wrote 01_CODEX_SPEC.md, 02_CODEX_IMPLEMENTATION_PLAN.md",
        },
        {
            "time": t("09:44", "30"),
            "type": "queued",
            "step": None,
            "provider": None,
            "detail": "orchestrator queued 1 step(s): Implement→claude — the system will cue each agent in order",
        },
        {
            "time": t("09:44", "32"),
            "type": "step_started",
            "step": "claude_implement",
            "provider": "claude",
            "detail": "orchestrator routed Implement → claude (sent 1,940 chars; reads: 01_CODEX_SPEC.md, 02_CODEX_IMPLEMENTATION_PLAN.md)",
        },
        {
            "time": t("09:51", "36"),
            "type": "step_finished",
            "step": "claude_implement",
            "provider": "claude",
            "detail": "claude finished Implement: succeeded (exit 0, 424.1s, 2,860 chars out), "
            "wrote 04_CLAUDE_IMPLEMENTATION_SUMMARY.md · 4 files changed",
        },
        {
            "time": t("09:51", "36"),
            "type": "queued",
            "step": None,
            "provider": None,
            "detail": "orchestrator queued 1 step(s): QA / Test→antigravity — the system will cue each agent in order",
        },
        {
            "time": t("09:51", "40"),
            "type": "command",
            "step": None,
            "provider": "antigravity",
            "detail": "orchestrator ran `npm test` → succeeded (exit 0)",
        },
        {
            "time": t("09:55", "02"),
            "type": "step_finished",
            "step": "gemini_qa",
            "provider": "antigravity",
            "detail": "antigravity finished QA / Test: succeeded (exit 0, 206.4s, 918 chars out), wrote 05_QA_RESULTS.md",
        },
        {
            "time": t("09:55", "02"),
            "type": "queued",
            "step": None,
            "provider": None,
            "detail": "orchestrator queued 1 step(s): Final Review→codex — the system will cue each agent in order",
        },
        {
            "time": t("09:57", "44"),
            "type": "step_finished",
            "step": "codex_review",
            "provider": "codex",
            "detail": "codex finished Final Review: succeeded (exit 0, 162.0s, 640 chars out), wrote 07_CODEX_FINAL_REVIEW.md",
        },
        {
            "time": t("09:57", "51"),
            "type": "final_report",
            "step": None,
            "provider": "claude",
            "detail": "controller declared the task complete: checkout session and webhook implemented, "
            "18 tests passing, final review clean",
        },
    ],
}
(TASK / "task.json").write_text(json.dumps(task, indent=2) + "\n")

# --- handoff artifacts -------------------------------------------------------
ART = {
    "00_USER_GOAL.md": f"# Goal\n\n{task['goal']}\n",
    "01_CODEX_SPEC.md": """# Spec — Stripe Checkout

## Scope
- One hosted Checkout session per plan in `PLANS` (starter, team, scale).
- `POST /api/checkout` returns the session URL; the client redirects.
- `POST /api/stripe/webhook` upgrades the workspace on `checkout.session.completed`.

## Constraints
- Reuse the existing `PLANS` config in `src/lib/billing.ts` — do not introduce a
  second source of truth for pricing.
- The webhook must be idempotent: Stripe retries, and a replayed event must not
  double-upgrade a workspace.
- Secret key stays server-side; the client only ever sees the session URL.

## Acceptance
- A test for each plan producing a session.
- A test asserting a replayed webhook event is a no-op.
""",
    "02_CODEX_IMPLEMENTATION_PLAN.md": """# Implementation Plan

1. `server/routes/checkout.ts` — build the session from `PLANS[plan]`, 400 on unknown plan.
2. `server/routes/webhook.ts` — verify the signature, then upgrade on
   `checkout.session.completed`; store the event id and skip ids already seen.
3. `src/components/PricingTable.tsx` — plan buttons POST to `/api/checkout`, redirect on 200,
   surface the error inline on failure.
4. Tests alongside each route.

No pricing values in the components — read them from `PLANS`.
""",
    "04_CLAUDE_IMPLEMENTATION_SUMMARY.md": """# Implementation Summary

- **server/routes/checkout.ts** — creates the session from `PLANS[plan]`; unknown plan → 400.
- **server/routes/webhook.ts** — new; verifies the signature and upgrades the workspace on
  `checkout.session.completed`. Processed event ids are recorded, so a Stripe retry is a no-op.
- **src/lib/billing.ts** — added `priceIdFor(plan)` so the price map has one home.
- **src/components/PricingTable.tsx** — each plan button posts to `/api/checkout` and redirects;
  failures render inline instead of throwing.

Followed the spec's idempotency requirement rather than assuming Stripe delivers once.
""",
    "05_QA_RESULTS.md": """# QA Results

`npm test` → **18 passed**, 0 failed.

Checked beyond the suite:
- Unknown plan returns 400, not a 500.
- Replayed `checkout.session.completed` leaves the workspace tier unchanged.
- No secret key reaches the client bundle (`grep` over `dist/`).

No blocking issues.
""",
    "07_CODEX_FINAL_REVIEW.md": """# Final Review

Implementation matches the spec. Idempotency is handled where it belongs — in the
webhook, keyed on the event id — and pricing stayed in `PLANS`.

Optional, not blocking:
- Consider a typed error for the 400 path so the client can distinguish it.

**Verdict: ship it.**
""",
    "03_CLAUDE_PROMPT.md": "See logs/ for the exact prompt sent to claude.\n",
    "06_BUGS_FOR_CLAUDE.md": "# Bugs for Claude\n\nNone — QA passed with no blocking issues.\n",
    "ROUTING_DECISIONS.md": """# Routing Decisions

| Step | Agent | Why |
| --- | --- | --- |
| Write Spec | codex | Planning and product judgment. |
| Implement | claude | Implementation and fixes. |
| QA / Test | antigravity | Tool-running and broad checks. |
| Final Review | codex | Review is a spec-side judgment call. |
""",
}
for name, body in ART.items():
    (TASK / name).write_text(body)


# --- run logs (the UI shows the STDOUT section as the step's reply) ----------
def log(cmd: str, stdout: str) -> str:
    return f"# Command Line Interface Controller run\n# command: {cmd}\n\n--- STDOUT ---\n{stdout}\n\n--- STDERR ---\n"


REPLIES = {
    "094120-codex_spec": (
        "codex exec --model gpt-5.6-sol",
        """Wrote the two handoff docs:

- `01_CODEX_SPEC.md` — scope, constraints, acceptance criteria
- `02_CODEX_IMPLEMENTATION_PLAN.md` — file-by-file plan

Two things worth calling out before implementation:

1. Stripe retries webhooks. The upgrade path has to be idempotent or a retry
   double-upgrades the workspace — I made that an acceptance criterion.
2. `PLANS` already exists in `src/lib/billing.ts`. The plan reuses it instead of
   adding a second price map, which is where this usually rots.

No production code touched.""",
    ),
    "094432-claude_implement": (
        "claude -p --permission-mode acceptEdits --model claude-opus-5",
        """Done. Implemented the plan across 4 files:

- `server/routes/checkout.ts` — session built from `PLANS[plan]`, unknown plan → 400
- `server/routes/webhook.ts` — new; signature verified, upgrade on
  `checkout.session.completed`, processed event ids recorded so retries no-op
- `src/lib/billing.ts` — added `priceIdFor(plan)` so the price map has one home
- `src/components/PricingTable.tsx` — plan buttons post and redirect; errors render inline

Tests added next to both routes, including the replayed-event case the spec asked for.""",
    ),
    "095136-gemini_qa": (
        "agy --sandbox -p",
        """`npm test` → 18 passed, 0 failed.

Checked three things the suite doesn't:
- unknown plan returns 400, not a 500
- a replayed `checkout.session.completed` leaves the tier unchanged
- no secret key in the built client bundle

No blocking issues. Wrote `05_QA_RESULTS.md`.""",
    ),
    "095502-codex_review": (
        "codex exec --model gpt-5.6-sol",
        """Reviewed the diff against the spec.

Idempotency is handled in the webhook keyed on event id — the right place — and
pricing stayed in `PLANS`. Implementation matches the plan.

One optional follow-up: a typed error for the 400 path so the client can tell it
apart from a network failure. Not blocking.

Verdict: ship it.""",
    ),
}
for stem, (cmd, out) in REPLIES.items():
    (LOGS / f"{D.replace('-', '')}-{stem}.log").write_text(log(cmd, out))
    (LOGS / f"{D.replace('-', '')}-{stem}.prompt.txt").write_text(f"(prompt for {stem})\n")


# --- queue -------------------------------------------------------------------
def q(qid, step, label, provider, start, end):
    return {
        "id": qid,
        "taskId": TASK_ID,
        "step": step,
        "label": label,
        "provider": provider,
        "status": "done",
        "source": "orchestrator",
        "enqueuedAt": t(start),
        "note": None,
        "runId": qid + "aa11",
        "attempt": 1,
        "providerOverride": None,
        "startedAt": t(start),
        "finishedAt": t(end),
    }


(AF / "queue.json").write_text(
    json.dumps(
        {
            "items": [
                q("7c1a44f0", "codex_spec", "Write Spec", "codex", "09:41", "09:44"),
                q("2e90bb31", "claude_implement", "Implement", "claude", "09:44", "09:51"),
                q("d5f31a08", "gemini_qa", "QA / Test", "antigravity", "09:51", "09:55"),
                q("91be6c27", "codex_review", "Final Review", "codex", "09:55", "09:57"),
            ]
        },
        indent=2,
    )
    + "\n"
)

# --- controller conversation -------------------------------------------------
messages = [
    {"role": "user", "content": "add stripe checkout to the pricing page", "time": t("09:40", "44")},
    {
        "role": "assistant",
        "provider": "claude",
        "durationMs": 11240,
        "time": t("09:41"),
        "content": "Queuing it as one task, routing each step to whichever CLI is best at it.\n\n"
        "| Step | Agent | Target |\n| :--- | :--- | :--- |\n"
        "| `codex_spec` | Codex | Scope, constraints, acceptance criteria |\n"
        "| `claude_implement` | Claude | Checkout route, webhook, pricing buttons |\n"
        "| `gemini_qa` | Antigravity | Run the suite and probe the failure paths |\n"
        "| `codex_review` | Codex | Final review against the spec |\n\n"
        "```agentflow-task\ntitle: stripe-checkout\n"
        "goal: Add Stripe Checkout to the pricing page: a hosted checkout session per plan, "
        "a webhook that upgrades the workspace on payment, and tests for both paths.\n"
        "queue: codex_spec\n```",
    },
    {
        "role": "system",
        "provider": "claude",
        "time": t("09:41", "02"),
        "content": "Created “stripe-checkout” · queued codex_spec",
    },
    {
        "role": "system",
        "provider": "codex",
        "time": t("09:44", "18"),
        "content": "codex finished Write Spec: succeeded (exit 0, 178.2s) — wrote 01_CODEX_SPEC.md, 02_CODEX_IMPLEMENTATION_PLAN.md",
    },
    {
        "role": "system",
        "provider": "claude",
        "time": t("09:51", "36"),
        "content": "claude finished Implement: succeeded (exit 0, 424.1s) · 4 files changed",
    },
    {
        "role": "system",
        "provider": "antigravity",
        "time": t("09:55", "02"),
        "content": "antigravity finished QA / Test: succeeded (exit 0, 206.4s) — 18 passed, 0 failed",
    },
    {
        "role": "system",
        "provider": "codex",
        "time": t("09:57", "44"),
        "content": "codex finished Final Review: succeeded (exit 0, 162.0s) — verdict: ship it",
    },
    {
        "role": "assistant",
        "provider": "claude",
        "durationMs": 9130,
        "time": t("09:57", "51"),
        "content": "**Task complete.** Checkout and the webhook are in, 18 tests pass, review came back clean.\n\n"
        "One optional follow-up it flagged: a typed error for the 400 path so the client can tell it "
        "apart from a network failure. Want that queued?",
    },
]
(AF / "chat.json").write_text(
    json.dumps({"messages": messages, "updatedAt": t("09:57", "51"), "channels": {}}, indent=2) + "\n"
)

(AF / "config.json").write_text(
    json.dumps(
        {
            "routing": {"orchestrator": "claude", "pm": "codex", "engineer": "claude", "qa": "antigravity"},
        },
        indent=2,
    )
    + "\n"
)
(AF / ".gitignore").write_text("*\n")
(AF / "usage.json").write_text(json.dumps({"localSteps": 26, "expensiveCallsAvoided": 9}, indent=2) + "\n")

print("demo workspace:", DEMO)
print("task:", TASK_ID, "| messages:", len(messages))
