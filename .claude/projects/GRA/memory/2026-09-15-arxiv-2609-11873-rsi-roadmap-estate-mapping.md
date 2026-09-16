# arXiv 2609.11873 — RSI roadmap paper: read-through + estate mapping

_Created: 15-09-2026 · Last updated: 15-09-2026_

**Paper:** "The Last AI Built by Humans: Toward Genuine Recursive Self-Improvement" — Yi Duan + 32 co-authors (incl. Zhiyuan Liu, Bowen Zhou, Conghui He), arXiv 2609.11873, submitted 10-09-2026. Position/survey/roadmap — no new algorithm to adopt.

## What it defines

- **HCI (Headroom-Closed Index):** normalized 0–100 score of how much benchmark headroom a domain has closed (0 = entry-year frontier, 100 = perfect). Key finding: knowledge/math domains at 77–86 by 2026, but **interactive agentic domains lag**: software engineering 52.6, search/terminal agents 56.8, tool agents 39.9 → the remaining headroom — and hence the value of self-improvement loops — concentrates exactly in long, stateful agent workflows.
- **Autonomy ladder:** B0 (in-task improvement, nothing persists) → L1 (AI executes a human-defined improvement procedure, results persist) → L2 (AI picks improvement strategy) → L3 (AI acquires its own experience) → L4 (adapts environment/deployment) → L5 (recursive meta-improvement: improving the improvement process itself). Core RSI criterion: has a *persistent* loop formed around the system, and how much authority over it is endogenous.

## Estate mapping (Uprava/GRA, as of 15-09-2026)

- The estate already runs a de-facto **L1–L2 loop with L3 elements**: handoffs = prescribed improvement procedures; memory_recall = persistent state; drift-tripwire + re-stamp = regression testing for instructions; verification blanket (MG 14-09-2026) = validation gate; /reflect + skill-mine (H3968) = experience capture; H4022 retrieval KPIs = "activation failure" measurement. Human authority explicitly retained (@DECIDE rows, votes are MG's) — matches the paper's "which decisions remain human-controlled" framing, i.e. deliberate L1–L2 ceiling, not a gap.
- Paper-validated failure modes the estate already defends against: **Library Drift** (expanding skill library degrades retrieval — the drift injector found 12 stale command copies on 15-09-2026 and offers `--stamp` re-stamp) and **activation failure** (relevant skill exists but is never retrieved — the `/skill-token anywhere` rule + context packs + H4022 KPIs).

## Actionable deltas suggested by the paper

1. Failure attribution at handoff-close: record WHICH component failed (tier vs handoff text vs harness vs data) — the paper's "cross-component diagnosis" gap; a small LANE_REPORT/handoff-close schema addition would enable controlled comparisons.
2. Keep the drift re-stamp on a routine cadence (e.g. inside /tidy) rather than ad-hoc — Library Drift is named as a stall mode.
3. HCI-style normalized trajectory for own lanes (drain success rate, verification pass rate, retrieval hit rate vs entry baseline) — extends H4022's KPI sketch.
4. Do NOT chase L4/L5 autonomy — paper explicitly states greater autonomy, durable gains, and a better improvement process are distinct properties; our human-gated structure is consistent with current field consensus.

_Гасунс_
