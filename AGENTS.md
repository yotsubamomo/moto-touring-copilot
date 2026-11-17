# AGENTS.md

## 指示來源與專案範圍

- Root `CLAUDE.md` 是本專案的主要 project instruction source；本檔是其中適用於 Codex 的長期規則投影。兩者不一致時以 `CLAUDE.md` 為準。
- 本專案是 Moto Touring Copilot（重機旅遊規劃顧問）：NCHU AIoT 課程的期末專題，一人進行。它是一個 Domain AI Agent，依騎士自己的歷史 GPX 配速、天氣、日照、加油與路況，規劃重機一日行程並說明每項建議的依據。
- 目前的進度與交接事項不在本檔，見 `docs/handoff/` 中日期最新的一份。

## Governance

整個 repo 都適用 Minimal Operational Governance v2.2，沒有 governance flag。Package 的位元複本與 Project Bindings 在 `docs/governance/`，生效的 package 檔案以 `docs/governance/project-bindings.md` 第 1 節為準。

- **Codex 只在 Project Bindings 第 3.3 節（O-6）宣告的範圍內擔任 `primary_reviewer`**：依該節的機制被派工時，在指定的 worktree 內做 R1、R2 或 Spec Integration Audit，並自己寫 audit record。只在 Bindings 生效、且 Codex qualification 已通過時適用。
- 在那個範圍之外，Codex 不在本 repo 執行 work item（實作、裁決、設計決定），只做唯讀協助：閱讀、說明、查詢、提出建議；這些輸出不是治理紀錄，不構成 finding、verdict、decision 或接受。
- 擔任 `primary_reviewer` 時：不修改 audit record 以外的任何檔案；不讀取 worktree 以外的路徑，特別是 `data/` 與 `.env`。
- Lightweight 或 Formal 由治理與 Bindings 第 4 節判定（Lightweight 優先）。

## 上位契約與判準

- `docs/requirement/` 是老師提供的期末專題規範與講義，唯讀，不改寫。
- 最終判準是 `docs/requirement/requirements_proposal.txt` 定義的 ①–⑧ Domain AI Agent 架構，以及課程的基本要求。重點是 Agent 工作流程完整，不是 Agent 的數量。
- `docs/proposal/` 的原始 Proposal 不是上位契約。相對於它的 Scope Reduction 是已接受的決定，不需要恢復，也不得寫成「不符合老師的架構」。
- Repository 中找不到的課程資訊視為未知，向使用者確認，不自行補出老師未提出的要求。
- 不擴張 Must 範圍；Must 以 `DESIGN.md` §9.1 為準。

## Layout

| 位置 | 內容 |
| --- | --- |
| `DESIGN.md`、`README.md` | 課程必繳的設計文件與說明文件，持續維護 |
| `docs/requirement/` | 上位契約，唯讀 |
| `docs/proposal/` | Proposal 階段交出的文件與原始稿，只作參考 |
| `docs/grill/`、`docs/ui/`、`prototype/index.html` | 已凍結的 G1、G3 基線，不修改 |
| `docs/cr/`、`docs/review/` | Change Request、審查報告與其附錄，紀錄 |
| `docs/spec/` | Spec；以各檔的狀態列為準，未 Freeze 的 Draft 不是已接受的契約 |
| `docs/ticket/` | 票的索引；票本體在 GitHub Issues |
| `docs/governance/` | 治理 package、Project Bindings、工作紀錄 |
| `src/moto_copilot/`、`tests/` | 實作與測試（測試只用合成資料） |
| `experiments/` | 技術檢查與實驗腳本，部分會讀私有資料 |
| `data/` | 私有騎乘資料 |

資料夾在真的產出該類文件時才建立。不為整理目的新增 framework、package layout 或 tooling。

## Private data

`data/` 內是騎士的 GPX 與由它導出的位置資訊。本 repo 是公開的。

- 不讀取、不列出、不搜尋 `data/`（含 `data/private/`）。只有使用者以明確路徑授權的檔案例外。
- 每一次搜尋都指定明確的路徑（`DESIGN.md`、`README.md`、`docs/`、`src/`、`tests/`、`experiments/`、`prototype/`），不從 repo root 搜尋。
- 不執行 `experiments/` 下會讀私有資料的腳本。
- 保留行程（holdout）在分析方法與模型設定凍結之前不得讀取。
- 私有資料不得進 git、log、文件、測試 fixture，也不得送往外部服務。
- 查證需要私有資料而沒有授權時，寫 NOT VERIFIED。

## Credentials and cost

- 不讀取、不輸出、不複製、不提交任何憑證；金鑰只放在未追蹤的本機 `.env`，由使用者親自填入。
- 付費 API 只在使用者明確授權的額度內呼叫。

## Integrity

- 不虛構、不模擬實驗結果；沒有執行的檢查寫 NOT RUN 或 BLOCKED。
- 技術檢查或 Spike 的結果不得寫成 E1 Lite 或 E2 的結果。
- 現況與預期分開寫；沒有實作與驗收證據的項目不標 PASS。
- 用語規則：`ETA_safe` 不稱為 P90；降雨機率 ≥70% 的規則不稱為官方警特報；不宣稱個人配速比 Google Maps 準確；折返判斷的啟發式規則不描述為已驗證；隱私說明不得宣稱檔案只留在使用者的電腦上。

## Commands

在 repo 根目錄、Git Bash 下（環境建立見 `DESIGN.md` §10）：

```bash
.venv/Scripts/python.exe -m pytest -q
```

未確認的 command 不做假設。

## Git workflow

Branch 與 commit message 的完整規則見 `docs/conventions/git-commit-rules.md`，重點如下：

- 每個 feature 或 fix 都開新 branch，不直接在 `main` 上 commit。
- Commit message 用英文。第一行是 `[Modify] – 主要變更的摘要`（分隔符是 en-dash `–`），接一行空白，之後每項變更各一行，以 `[Additions]`、`[Modification]`、`[Fix]` 三種前綴分類。
- Commit message、PR description 與 Issue 都不加任何 Claude 標記；Codex 自身的署名或產生標記同樣不加。
- Commit、push、開 PR、合併都要有使用者的明確授權。本 repo 是公開的，push 即公開。

## Language

回覆與交付文件用繁體中文，關鍵術語保留英文。程式碼、識別字與 commit message 用英文。

## Agent skills

- **Issue tracker**：GitHub Issues（`yotsubamomo/moto-touring-copilot`），以 `gh` CLI 操作。見 `docs/agents/issue-tracker.md`。
- **Triage labels**：見 `docs/agents/triage-labels.md`；標籤尚未在 GitHub 上建立。
- **Domain docs**：單一 context，詞彙以 `DESIGN.md` 與 `docs/spec/` 為準。見 `docs/agents/domain.md`。

本檔只保留跨 session 仍成立的資訊，不記錄進度、TODO、單次 session 內容或未確認的推測。
