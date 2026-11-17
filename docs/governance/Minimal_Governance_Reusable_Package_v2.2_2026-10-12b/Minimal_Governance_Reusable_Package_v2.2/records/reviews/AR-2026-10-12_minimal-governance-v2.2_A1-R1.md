# AR-2026-10-12_minimal-governance-v2.2_A1-R1 — Codex independent review（R1）

## Metadata header（由派工的無角色 main session 加上；以下 Codex 輸出原文未改動）

| 欄位 | 內容 |
|---|---|
| audit | A1：v2.2 Candidate 的 independent review（Acceptor 指示第 2 項要求） |
| round／cycle | R1／cycle 1 |
| contract | [WC-2026-10-12_minimal-governance-v2.2-adoption](../outcome-contracts/WC-2026-10-12_minimal-governance-v2.2-adoption.md) |
| subject | `master_governance/Minimal_Operational_Governance_v2.2_Candidate.md` @ `dfe7c91`（sha256 `832391d6be18febc7ff41cdd387f0d01a511d4b05d0a8f1c0d132c37605c2329`）；branch `adopt/minimal-governance-v2.2-2026-10-12` @ `209d5c4`，scope `branch`，base `303ef29` |
| reviewer | `codex`（`primary_reviewer`，Bindings O-2、§3.5） |
| mechanism | 使用者層 skill `codex-adversarial-audit` → codex plugin 1.0.5 companion `adversarial-review`（Codex CLI 0.161.0），`--background --scope branch --base 303ef29` |
| companion job id | `review-mv4m38fv-2togd1`（created 2026-10-12T02:07:09.691Z，completed 2026-10-12T02:13:34.149Z，status completed） |
| Codex thread | `01a12ddd-3094-7f33-8da8-7944e16d4e4a`（turn `01a12ddd-3a8a-7a12-9c62-667a859855ae`）；另有兩個 Codex 子 thread `01a12ddd-ded0-7bc1-b55c-d5363365a694`、`01a12ddd-ef95-7d31-8c45-e43b6555f4aa` |
| observed model／effort | 三個 thread 都是 `gpt-6-sol`／`xhigh`（`~/.codex/logs_2.sqlite` 的 `logs` 表，`thread_id` 篩選：主 thread `model=gpt-6-sol` 1213 筆、`reasoning_effort=xhigh` 624 筆、`effort=Some(XHigh)` 40 筆；兩個子 thread 同樣只有 `gpt-6-sol`／`xhigh`，無其他 model 值）。符合 Bindings §3.5 宣告的 mapping |
| binding 證據位置的偏差 | Bindings §3.5 宣告的證據是 `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl`；本次 companion（app-server 路徑）未產生該 thread 的 rollout 檔（`find ~/.codex -name '*01a12ddd*'` 無結果），改以上列 log 資料庫核對。宣告的證據位置需在 Bindings 更新 |
| substitution | 無 |
| 四項 properties（Minimal v2.1 §2.3） | (1) independent context：獨立 Codex process，不含 Claude 對話，focus 只放紀錄引用與 Acceptor 指定的檢查項；(2) verifiable binding：上列證據；(3) autonomous access：Codex 以 git scope 自行讀取 repository（self-collect 模式）；(4) self-written record：下列為 companion 輸出原文，派工者只加本 header |
| model diversity | Codex（`gpt-6-sol`）與 v2.2 Candidate 起草 session（`claude-opus-5-5`）不同 vendor：D4 成立（family diversity） |
| 原文來源 | companion job record `Local/Temp/codex-companion/SpeCoda_Local_DEV_v2-5c4942d6e0c28369/jobs/review-mv4m38fv-2togd1.json`（sha256 `e4ade6738d305130e9dc638de34517377d4e684f31f1f0caf0c4fe936589ce72`）的 `rendered` 與 `result.rawOutput` 欄位 |
| severity／blocking | 依 Codex 標示：F1 high BLOCKING、F2 high BLOCKING、F3 medium BLOCKING |

## Codex 輸出原文（companion `rendered`）

````text
# Codex Adversarial Review

Target: branch diff against 303ef29
Verdict: needs-attention

NO SHIP: V22-10 lacks a compatible verification procedure, the Alternate Review escalation rule has conflicting count semantics, and the drafting worklog records an unrepaired Executor binding failure.

Findings:
- [high] A1R1-F1 [BLOCKING] V22-10 outstrips the adopted binding checks (master_governance/Minimal_Operational_Governance_v2.2_Candidate.md:184-186)
  V22-10 requires evidence of the actual model and effort across all work in an assignment. The frozen orchestrator contract checks its root session before first dispatch (§3, line 56; §11, line 195), and current Project Bindings check root sessions before work starts (lines 102–103). A later automatic model switch could therefore leave work treated as valid although V22-10 makes its binding noncompliant. This is a companion and migration gap, rather than a contradiction in the candidate text.
  Recommendation: Before adoption, update the companion procedures and Project Bindings to check model and effort throughout root and dispatched assignments, and specify how post-switch work is isolated and reverified.
- [high] A1R1-F2 [BLOCKING] The candidate drafting assignment was never qualified (governance/records/worklogs/WL-2026-10-12_minimal-governance-v2.2-candidate.md:15-17)
  The candidate worklog records a required Opus 5.5/medium Executor, an observed Opus 5.5/xhigh session, and no repair (lines 15–17), yet marks the drafting work completed (line 114). Frozen v2.1 §2.2 requires a mismatched binding to be repaired or replaced and prohibits presenting that assignment as compliant execution. Independent R1 review cannot retroactively qualify the drafting assignment; adopting its completion record would leave a known governance violation in the provenance.
  Recommendation: Have a correctly bound Executor take responsibility for a recorded continuation that checks the full candidate against the accepted drafting contract, corrects any defects, and resolves the worklog’s noncompliant completion status before adoption closure.
- [medium] A1R1-F3 [BLOCKING] Escalation leaves the one-Alternate-Review limit undefined (master_governance/Minimal_Operational_Governance_v2.2_Candidate.md:263)
  Section 2.5 permits a fresh escalated review dispatch while requiring only one verdict. Inherited §4.4 (line 576) requires dispatching exactly one Alternate Independent Review. The cited default v2.5 Profile (line 69) has an Opus Alternate assess the remaining finding, then dispatches a fresh Fable Alternate after a capability-gap record. The candidate does not say whether the first substantive, no-verdict assignment consumes the one-review allowance. This blocks adoption because runtimes can either reject the intended escalation or count an additional review outside the mandatory audit cycle.
  Recommendation: Define how a pre-verdict Alternate withdrawal and replacement counts under §4.4, then align the Profile’s E-AR procedure with that rule.

Next steps:
- Resolve the three blocking findings, then perform the required R2 and closure before adoption.
- Read-only audits performed: git diff against 303ef29, frozen v2.1 and pinned dfe7c91 hash checks, and clause and companion-contract review. No runtime probe was performed; mid-session switch handling remains unverified.
- Changed files: none. Runtime wildcards, _master.txt, production routes, negative prompts, workflow/ComfyUI files, and references/** were unchanged.
````

## Codex 輸出原文（`result.rawOutput`，JSON）

````json
{"verdict":"needs-attention","summary":"NO SHIP: V22-10 lacks a compatible verification procedure, the Alternate Review escalation rule has conflicting count semantics, and the drafting worklog records an unrepaired Executor binding failure.","findings":[{"severity":"high","title":"A1R1-F1 [BLOCKING] V22-10 outstrips the adopted binding checks","body":"V22-10 requires evidence of the actual model and effort across all work in an assignment. The frozen orchestrator contract checks its root session before first dispatch (§3, line 56; §11, line 195), and current Project Bindings check root sessions before work starts (lines 102–103). A later automatic model switch could therefore leave work treated as valid although V22-10 makes its binding noncompliant. This is a companion and migration gap, rather than a contradiction in the candidate text.","file":"master_governance/Minimal_Operational_Governance_v2.2_Candidate.md","line_start":184,"line_end":186,"confidence":0.94,"recommendation":"Before adoption, update the companion procedures and Project Bindings to check model and effort throughout root and dispatched assignments, and specify how post-switch work is isolated and reverified."},{"severity":"high","title":"A1R1-F2 [BLOCKING] The candidate drafting assignment was never qualified","body":"The candidate worklog records a required Opus 5.5/medium Executor, an observed Opus 5.5/xhigh session, and no repair (lines 15–17), yet marks the drafting work completed (line 114). Frozen v2.1 §2.2 requires a mismatched binding to be repaired or replaced and prohibits presenting that assignment as compliant execution. Independent R1 review cannot retroactively qualify the drafting assignment; adopting its completion record would leave a known governance violation in the provenance.","file":"governance/records/worklogs/WL-2026-10-12_minimal-governance-v2.2-candidate.md","line_start":15,"line_end":17,"confidence":0.91,"recommendation":"Have a correctly bound Executor take responsibility for a recorded continuation that checks the full candidate against the accepted drafting contract, corrects any defects, and resolves the worklog’s noncompliant completion status before adoption closure."},{"severity":"medium","title":"A1R1-F3 [BLOCKING] Escalation leaves the one-Alternate-Review limit undefined","body":"Section 2.5 permits a fresh escalated review dispatch while requiring only one verdict. Inherited §4.4 (line 576) requires dispatching exactly one Alternate Independent Review. The cited default v2.5 Profile (line 69) has an Opus Alternate assess the remaining finding, then dispatches a fresh Fable Alternate after a capability-gap record. The candidate does not say whether the first substantive, no-verdict assignment consumes the one-review allowance. This blocks adoption because runtimes can either reject the intended escalation or count an additional review outside the mandatory audit cycle.","file":"master_governance/Minimal_Operational_Governance_v2.2_Candidate.md","line_start":263,"line_end":263,"confidence":0.86,"recommendation":"Define how a pre-verdict Alternate withdrawal and replacement counts under §4.4, then align the Profile’s E-AR procedure with that rule."}],"next_steps":["Resolve the three blocking findings, then perform the required R2 and closure before adoption.","Read-only audits performed: git diff against 303ef29, frozen v2.1 and pinned dfe7c91 hash checks, and clause and companion-contract review. No runtime probe was performed; mid-session switch handling remains unverified.","Changed files: none. Runtime wildcards, _master.txt, production routes, negative prompts, workflow/ComfyUI files, and references/** were unchanged."]}
````
