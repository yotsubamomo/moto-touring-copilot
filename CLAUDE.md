# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 專案用途

Moto Touring Copilot（重機旅遊規劃顧問）：NCHU AIoT 課程的期末專題，一人進行。它是一個 Domain AI Agent，依騎士自己的歷史 GPX 配速、天氣、日照、加油與路況，規劃重機一日行程並說明每項建議的依據。

Claude 從本 repo 的根目錄啟動。Root 的 `AGENTS.md` 是給 Codex 用的指示檔，內容是本檔的投影；兩者不一致時以本檔為準。

目前的進度、未完成事項與單次 session 的交接不寫在本檔，見 `docs/handoff/` 中日期最新的一份。

## 治理

**整個 repo 都適用 Minimal Operational Governance v2.2，沒有 governance flag。** 開始任何 work item 之前，先讀 `docs/governance/project-bindings.md`，再依其指示讀治理本文與 references。

- 治理的 MUST／SHOULD／MAY 全部生效；本檔的其他規則視為 Project Bindings 的一部分，與治理 MUST 衝突時以治理為準。
- 工作的輕重由 lane 決定，不由範圍決定。Bindings 採 Lightweight 優先：契約清楚、一個 execution unit 能完成的工作走 Lightweight；需要多個 execution units／dependencies，或需要建立新的設計基線時，才走 Formal（Spec＋Tickets＋Orchestrator）。MVP 的模組實作屬於 Formal。
- 治理角色與 bounded assignments 的 agent definitions 在 `.claude/agents/gov-*.md`，只依 Bindings 派工。
- 主 session 預設不擔任任何治理角色（Bindings 第 3.5 節）。與使用者對話、Grill、查詢、說明不是 work item。
- Bindings 目前的版本與是否已生效，以 `docs/governance/project-bindings.md` 檔首為準。生效前它只是提案，不構成任何授權。

使用 Matt Pocock 的 skills（`grilling`、`/to-spec`、`/to-tickets` 等）時，依該 skill 自己的流程進行，不另外疊加治理的框架。Skill 只提供做法；它的產出要成為契約，仍須經 acceptor 接受或由 Design Authority 依 Bindings 引用。

## 上位契約與判準

- `docs/requirement/` 是老師提供的期末專題規範與講義，是本專案的上位契約，唯讀，不改寫。
- 最終判準是 `docs/requirement/requirements_proposal.txt` 定義的 ①–⑧ Domain AI Agent 架構，以及課程的基本要求：完整的 Agent 工作流程、真正取得資料、執行 Analytics、整合 Domain Knowledge、提出可追溯的建議、以 Streamlit 完成端到端互動、具備 System Architecture、Flowchart、行號 Pseudocode 與可重現的實驗證據。重點是工作流程完整，不是 Agent 的數量。
- `docs/proposal/` 的原始 Proposal 不是上位契約。相對於它的 Scope Reduction（多 Agent、LightGBM、P90、Google Maps、279 趟資料與部分實驗）是已接受的決定，不需要恢復，也不得寫成「不符合老師的架構」。紀錄在 `DESIGN.md` §13 與 `docs/cr/CR-01-proposal-alignment.md`。
- Repository 裡找不到的課程資訊視為未知，向使用者確認；不要自行補出老師沒有提出的要求。
- 不擴張 Must 範圍。Must 以 `DESIGN.md` §9.1 為準。

## 目錄與文件的效力

| 位置 | 內容 | 效力 |
| --- | --- | --- |
| `DESIGN.md` | 系統設計文件（課程必繳）：Problem、Requirements、Architecture、Components、Data、AI／Analytics、Domain Knowledge、Algorithm、Implementation Mapping、How to Run、Results、Limitations、Change Log | 持續維護；內容以各段落自己標示的狀態為準 |
| `README.md` | 專題介紹、安裝、執行、Demo（課程必繳） | 持續維護 |
| `docs/requirement/` | 老師的規範與講義 | 上位契約，唯讀 |
| `docs/proposal/` | Proposal 階段交出的文件與其原始稿（`source/`） | 已交出，只作參考 |
| `docs/grill/` | G1 Grill 的輸入與裁決 | G1 已凍結 |
| `docs/ui/`、`prototype/index.html` | UI 設計文件與 HTML 原型 | G3 Frozen Baseline，不修改；之後的 UI 差異寫在 `docs/ui/UI_CR01_DELTA.md` |
| `docs/cr/` | Change Request 與其附錄（研究、審查、技術檢查結果、裁決） | 紀錄 |
| `docs/spec/` | Spec | 以各檔的狀態列為準；未 Freeze 的 Draft 不是已接受的契約 |
| `docs/ticket/` | 票的索引。票本體在 GitHub Issues | 索引，不複製票的內容 |
| `docs/review/` | 專案狀態審查報告與其引用證據 | 紀錄 |
| `docs/governance/` | 治理 package、Project Bindings、工作紀錄（`records/`） | 見 Bindings |
| `docs/handoff/` | Session 之間的交接文件 | 以日期最新的一份為準 |
| `src/moto_copilot/` | 實作 | — |
| `tests/` | 測試與合成的 fixtures | — |
| `experiments/` | 技術檢查與實驗腳本 | 部分腳本會讀私有資料，見下一節 |
| `data/` | 私有騎乘資料 | 見下一節 |

資料夾在真的產出該類文件時才建立，不預先建空的。不要為了整理而新增 framework、package layout 或 tooling。

## 私有資料

`data/` 內是騎士的 GPX 與由它導出的位置資訊，含住家附近的座標。本 repo 是公開的。

- **不讀取、不列出、不搜尋 `data/`**（含 `data/private/`）。只有使用者針對當次工作以明確路徑授權的檔案例外。
- 每一次搜尋都指定明確的路徑：`DESIGN.md`、`README.md`、`docs/`、`src/`、`tests/`、`experiments/`、`prototype/`。**不從 repo root 搜尋。**
- 派 sub-agent 時，在派工內容寫明這項禁令，並逐一列出它可以讀的檔案。
- `experiments/` 下會讀私有資料的腳本，沒有使用者的明確授權不執行。
- 保留行程（holdout，4 趟）在分析方法與模型設定凍結之前不得讀取。
- 私有資料與由它導出的位置資訊不得進 git、log、文件、測試 fixture，也不得放進送往外部 API 的內容，除非使用者明確授權其範圍。測試只用合成資料。
- 查證某件事需要私有資料而沒有授權時，寫 NOT VERIFIED，不自行取得。

## 憑證與付費

- 不讀取、不輸出、不複製、不提交任何憑證。金鑰只放在未追蹤的本機 `.env`，由使用者親自填入。
- 呼叫 Anthropic API 會計費。只在使用者明確授權的額度內執行；目前只授權了 C3 的真實 API smoke test，上限 US$3。
- 申請金鑰、第三方帳號操作、任何付費動作，都由使用者進行。

## 實驗與陳述的誠信

- 不虛構、不模擬實驗結果。真實 API 沒有執行，就寫 NOT RUN 或 BLOCKED，不以推測或本地 self-test 的結果代替。
- 技術檢查、預覽或 Spike 的結果，不得寫成 E1 Lite 或 E2 的結果。正式 E1 Lite／E2 只在使用者指示下執行。
- 設計文件寫定的功能不等於已完成。回報狀態時，現況與預期分開寫；沒有實作與驗收證據的項目不標 PASS。
- 用語規則：
  - `ETA_safe` 不稱為 P90，也不稱為任何百分位數。
  - 降雨機率 ≥70% 的規則不稱為官方警特報。
  - 不宣稱個人配速比 Google Maps 準確。
  - 折返判斷的啟發式規則不描述為已驗證。
  - 隱私說明不得宣稱檔案只留在使用者的電腦上。

## Commands

在 repo 根目錄、Git Bash 下（環境建立與其他可執行項目見 `DESIGN.md` §10）：

```bash
.venv/Scripts/python.exe -m pytest -q
```

```bash
PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json
```

以上兩項不需要金鑰，也不讀取任何 GPX。產品功能實作後，啟動 Streamlit、匯入 GPX、執行實驗的指令補在 `DESIGN.md` §10 與 `README.md`，確認長期有效後再補到這裡。

## Git workflow

Branch 與 commit message 的完整規則見 `docs/conventions/git-commit-rules.md`，重點如下：

- 每個 feature 或 fix 都開新 branch，名稱依實際修改內容取描述性的名字，不直接在 `main` 上 commit。
- Commit message 用英文。第一行是 `[Modify] – 主要變更的摘要`（分隔符是 en-dash `–`），接一行空白，之後每項變更各一行，以 `[Additions]`、`[Modification]`、`[Fix]` 三種前綴分類。
- Commit message、PR description 與 Issue 都不加任何 Claude 標記：不寫 `Co-Authored-By: Claude`，也不寫 `🤖 Generated with Claude Code`。此規則優先於工具預設的 attribution 提示。
- **Commit、push、開 PR、合併都要有使用者的明確授權。** 本 repo 是公開的，push 即公開。Bindings 生效後，本機 commit 依其 SA-1；push、PR 與合併仍保留給使用者（RB-1）。
- Commit 前確認暫存的內容不含 `.env`、GPX 或 `data/` 下的私有檔案。
- 描述聚焦在實際改了什麼與為什麼，清楚且技術上精確。

## 語言

回覆與交付文件用繁體中文，關鍵術語保留英文。程式碼、識別字與 commit message 用英文。

## Agent skills

### Issue tracker

Issue 與票放在 GitHub Issues（`yotsubamomo/moto-touring-copilot`），以 `gh` CLI 操作。見 `docs/agents/issue-tracker.md`。新增、修改或關閉 Issue 要有使用者的指示或在已接受的契約內。

### Triage labels

沿用五個預設標籤名稱，但標籤尚未在 GitHub 上建立。見 `docs/agents/triage-labels.md`。

### Domain docs

單一 context：詞彙以 `DESIGN.md` 與 `docs/spec/` 為準，尚無 `CONTEXT.md`。見 `docs/agents/domain.md`。

## 維護本檔

本檔只記錄長期有效的資訊。進度、TODO、單次 session 的工作內容與尚未確認的推測，不寫入此檔，寫在 `docs/handoff/` 或治理的工作紀錄。
