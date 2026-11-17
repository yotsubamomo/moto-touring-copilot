# AR-2026-10-12_minimal-governance-v2.2_A1-R2 — Codex closure review（R2）

## Metadata header（由派工的 Executor（root role session，Opus 5.5／high）加上；以下 Codex 輸出原文未改動）

| 欄位 | 內容 |
|---|---|
| audit | A1：v2.2 Candidate 的 independent review（Acceptor 指示第 2 項要求） |
| round／cycle | R2（closure review，Minimal v2.1 §4.4）／cycle 1 |
| contract | [WC-2026-10-12_minimal-governance-v2.2-adoption](../outcome-contracts/WC-2026-10-12_minimal-governance-v2.2-adoption.md)；R1：[AR-2026-10-12_minimal-governance-v2.2_A1-R1](AR-2026-10-12_minimal-governance-v2.2_A1-R1.md) |
| subject | targeted correction commit `ec7ed76`（scope `branch`，base `080114e`）：`master_governance/Minimal_Operational_Governance_v2.2_Candidate.md`（sha256 `462812d2…`）、`master_governance/references/orchestrator-contracts/default-v2.2.md`（sha256 `66072e68…`）、兩份 worklog |
| reviewer | `codex`（`primary_reviewer`，Bindings O-2、§3.5） |
| mechanism | 使用者層 skill `codex-adversarial-audit` → codex plugin 1.0.5 companion `adversarial-review`（Codex CLI 0.161.0），`--background --scope branch --base 080114e`；派工者：本 work item 的 Executor（經 Bindings §3.5 宣告的機制） |
| companion job id | `review-mv4no3q6-vgy4jt`（created 2026-10-12T02:51:22.975Z，completed 2026-10-12T02:55:59.684Z，status completed） |
| Codex thread | `01a12e05-aa16-7430-b9d2-27569c106221`（turn `01a12e05-b26a-79b1-a682-f496d7f8a910`）；審查期間無其他 Codex thread |
| observed model／effort | `gpt-6-sol`／`xhigh`（`~/.codex/logs_2.sqlite` 的 `logs` 表，審查期間全部紀錄：`model=gpt-6-sol` 990 筆、`reasoning_effort=xhigh` 517 筆、`effort=Some(XHigh)` 34 筆，無其他值）。符合 Bindings §3.5 宣告的 mapping。未產生 rollout 檔（同 R1 record 所記） |
| substitution | 無 |
| 四項 properties（Minimal v2.1 §2.3） | (1) independent context：新的 Codex process 與 thread，不含 Claude 對話，focus 只放紀錄引用與 R2 範圍；(2) verifiable binding：上列證據；(3) autonomous access：Codex 以 git scope 自行讀取 repository；(4) self-written record：下列為 companion 輸出原文，派工者只加本 header |
| model diversity | Codex（`gpt-6-sol`）與 Executor（`claude-opus-5-5`）不同 vendor：D4 成立 |
| 原文來源 | companion job record（位元複本見 `governance/records/evidence/`，sha256 `19147bb242dda3a72eb82320852923458e315972e1545fbbf155cb24b4e454e5`）的 `rendered` 與 `result.rawOutput` 欄位 |
| severity／blocking | 依 Codex 標示：A1R1-F1 UNRESOLVED、A1R1-F2 RESOLVED、A1R1-F3 RESOLVED；新 finding A1R2-F1 high BLOCKING（即 F1 的剩餘部分） |

## Codex 輸出原文（companion `rendered`）

````text
# Codex Adversarial Review

Target: branch diff against 080114e
Verdict: needs-attention

NO SHIP for A1 R2. A1R1-F1 UNRESOLVED; A1R1-F2 RESOLVED; A1R1-F3 RESOLVED. No separate blocking regression found. Deferring workspace Project Bindings verification to A2 is acceptable as a separate migration audit, but it does not close F1’s reference-contract gap.

Findings:
- [high] A1R2-F1 [BLOCKING] Whole-run binding verification remains optional in the reference procedure (master_governance/references/orchestrator-contracts/default-v2.2.md:58)
  Minimal v2.2 §2.2 requires evidence covering all work when a platform may switch model or effort (Candidate:184–186). The new orchestrator contract makes checks at checkpoints, rollover, completion, and before using a dispatched assignment’s return SHOULD rather than MUST; checkpoints themselves are optional, and §11:197 only SHOULD require Bindings to name a per-entry evidence source. A root session can switch after activation and route or gate work without a required intervening check. The MUST NOT rule for work after a detected switch does not catch an undetected one. A2 can audit this workspace’s Bindings during migration, but that later audit cannot repair the reusable contract’s missing verification gate.
  Recommendation: Require full execution-evidence verification before a dispatched return is used and before root-session work since the last check is used for routing, gates, persistence, or completion. Require an observable evidence source in adopting Bindings and fail closed when coverage cannot be established.

Next steps:
- Correct the verification gate, then repeat the scoped A1 R2 closure check. Keep the workspace v2.2 re-pin subject to A2 verification.
- Read-only audits: inspected the 080114e..ec7ed76 diff, compared orch-default v2.2 with v2.1, verified the recorded document hashes, and checked the referenced Executor transcript’s model/effort entries. No files were edited.
- Changed files: the adoption and candidate worklogs, Minimal v2.2 Candidate, and master_governance/references/orchestrator-contracts/default-v2.2.md. Runtime wildcards: no; _master.txt: no; production routes: no; negative prompts: no; workflow/ComfyUI: no; references/**: yes, the new orchestrator reference.
````

## Codex 輸出原文（`result.rawOutput`，JSON）

````json
{
  "verdict": "needs-attention",
  "summary": "NO SHIP for A1 R2. A1R1-F1 UNRESOLVED; A1R1-F2 RESOLVED; A1R1-F3 RESOLVED. No separate blocking regression found. Deferring workspace Project Bindings verification to A2 is acceptable as a separate migration audit, but it does not close F1’s reference-contract gap.",
  "findings": [
    {
      "severity": "high",
      "title": "A1R2-F1 [BLOCKING] Whole-run binding verification remains optional in the reference procedure",
      "body": "Minimal v2.2 §2.2 requires evidence covering all work when a platform may switch model or effort (Candidate:184–186). The new orchestrator contract makes checks at checkpoints, rollover, completion, and before using a dispatched assignment’s return SHOULD rather than MUST; checkpoints themselves are optional, and §11:197 only SHOULD require Bindings to name a per-entry evidence source. A root session can switch after activation and route or gate work without a required intervening check. The MUST NOT rule for work after a detected switch does not catch an undetected one. A2 can audit this workspace’s Bindings during migration, but that later audit cannot repair the reusable contract’s missing verification gate.",
      "file": "master_governance/references/orchestrator-contracts/default-v2.2.md",
      "line_start": 58,
      "line_end": 58,
      "confidence": 0.94,
      "recommendation": "Require full execution-evidence verification before a dispatched return is used and before root-session work since the last check is used for routing, gates, persistence, or completion. Require an observable evidence source in adopting Bindings and fail closed when coverage cannot be established."
    }
  ],
  "next_steps": [
    "Correct the verification gate, then repeat the scoped A1 R2 closure check. Keep the workspace v2.2 re-pin subject to A2 verification.",
    "Read-only audits: inspected the 080114e..ec7ed76 diff, compared orch-default v2.2 with v2.1, verified the recorded document hashes, and checked the referenced Executor transcript’s model/effort entries. No files were edited.",
    "Changed files: the adoption and candidate worklogs, Minimal v2.2 Candidate, and master_governance/references/orchestrator-contracts/default-v2.2.md. Runtime wildcards: no; _master.txt: no; production routes: no; negative prompts: no; workflow/ComfyUI: no; references/**: yes, the new orchestrator reference."
  ]
}
````
