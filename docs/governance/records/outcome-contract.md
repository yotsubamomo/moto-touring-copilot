# Outcome Contract OC-1 — Moto Touring Copilot MVP

> **狀態：已接受（2026-11-17）。** acceptor 針對 commit `873e37a` 接受，接受紀錄在第 10 節。本檔由無角色 session 依 acceptor 2026-11-17 的指示（原文「開始起草」）起草（Project Bindings m2 第 2.3 節、第 3.5 節）；第 9 節 D-1～D-5 與第 4.1 節、第 8 節、AB-9 的修正由 acceptor 同日裁決。
>
> 契約內容以 commit `873e37a` 的本檔為準。之後在本檔加入的只有本狀態欄與第 10 節的接受紀錄，是接受之後的轉錄，沒有改動任何條文。

本檔依治理 §3.1 的七項 properties 組織：1 Intent（第 1 節）、2 Scope（第 2 節）、3 Acceptance（第 3 節）、4 Authority（第 4 節）、5 Context（第 5 節）、6 Assurance（第 6 節）、7 Stable reference（第 7 節）。

## 1. Intent and outcome

完成 Moto Touring Copilot 的 MVP：一個 Domain AI Agent，依騎士自己的歷史 GPX 配速，加上天氣、日照、加油與路況，規劃重機一日行程，驗證整份計畫是否可行，並說明每項建議的依據。

預期產出是一套可以端到端操作的系統與它的交付文件，讓老師與下一位開發者能透過 GitHub、`README.md` 與 `DESIGN.md` 理解、執行、驗證並繼續開發（`docs/requirement/requirements_proposal.txt` 第六節 B）。判準是課程的 ①–⑧ Domain AI Agent 架構與基本要求（Bindings 第 2.2 節「最終判準」），不是 Agent 的數量。

## 2. Scope and boundaries

### 2.1 範圍內

以 `DESIGN.md` 在第 7 節所列 commit 的內容為準：

1. **Must 模組**：`DESIGN.md` §9.1 範圍標為 Must 的全部列（`ingest`、`routing`、`routes`、`pace`、`sources`、`planner`、`validator`、`kb`、`app/`、`experiments/e1_lite/`、`experiments/e2/`、`tests/`），功能細節依 §2.1 FR1–FR7、§2.2 NFR1–NFR5 與 §2.3 Scope Matrix 的 Must 欄。
2. **資料契約與 Spec**：把 `contracts` 更新到 v0.3（`DESIGN.md` §5），以及完成這些模組所需的 Spec 修訂與 Spec Blockers 的解決。既有的 `docs/spec/SPEC-001-plan-schema.md`、`SPEC-RESOLUTION-001-sb2-sb8-sb9.md` 與 GitHub Issues #7–#12 是輸入，由 Design Authority 引用或修訂（Bindings 第 8.1 節）。
3. **Pre-Spec Spike 的收編**：既有的 `ingest`、`routes`、`pace` Spike 依 Spec 與 Tickets 檢視，符合的納入，不符合的返工（`DESIGN.md` §9.3）。
4. **UI Gate**：UI-0 Mock-data Skeleton 與它之後的正式介面整合（`DESIGN.md` §9.6）。UI Delta Review 由 acceptor 進行。
5. **實驗的程式與凍結**：E1 Lite 與 E2 的程式、題庫、Oracle、凍結清單與分析計畫（`DESIGN.md` §6.2、§6.3、§9.3 的 12/5 凍結）。**正式執行不在本授權內**，見第 4.2 節。
6. **交付文件中屬於 repo 的部分**：`README.md`（專題介紹、Installation、How to Run、Demo）、`DESIGN.md` 各章（含 Results、Limitations、Conclusion 的 Contributions 與 Future Work）依實際狀態維護（D-4）。

### 2.2 範圍外（non-scope）

- `DESIGN.md` §2.3 的 Should 與 Won't 全部項目。做任何一項 Should 都需要 acceptor 另外授權（D-2）。
- 恢復已接受的 Scope Reduction（多 Agent、LightGBM、P90、Google Maps、279 趟資料與部分實驗），或加入老師沒有提出的要求（Bindings 第 2.4 節）。
- 修改 `docs/requirement/`、`docs/proposal/`、G1 裁決紀錄、G3 Frozen Baseline（`prototype/index.html` 與 `docs/ui/` 中標示 G3 Frozen 的文件）。UI 差異只寫在 `docs/ui/UI_CR01_DELTA.md`。
- Final PPT 與 Final Video 的製作，以及任何繳交與對外發布（D-4；RB-2）。
- 修改 GitHub Issues #7–#12 的內容或狀態（含關閉）（D-3）。

### 2.3 限制（constraints）

- Root `CLAUDE.md` 的「私有資料」「憑證與付費」「實驗與陳述的誠信」各節與用語規則，以及 Bindings 第 2.6 節的 RB-1～RB-7，全部適用。
- **私有資料**：讀取 `data/` 只限 acceptor 針對該 work item 以明確路徑授權的檔案；保留行程在分析方法與模型設定凍結前不得讀取；測試只用合成資料（RB-7）。
- **付費**：目前已授權的 API 支出只有 C3 的真實 API smoke test，上限 US$3（RB-4）。開發期間的 LLM 呼叫、Pilot 與正式 E2 的支出都尚未授權；需要它們的路徑在授權前依治理 §1.5 停止，不以 mock 結果代替真實結果。
- **憑證**：Anthropic API key 與中央氣象署授權碼由 acceptor 申請並填入本機 `.env`（RB-3）。沒有憑證時，相關檢查與功能如實標示 BLOCKED／NOT RUN。
- **時程**：`DESIGN.md` §9.3 的已接受規則適用，特別是 12/5 之後不加功能、落後時的捨棄順序，以及捨棄順序第 2 項（詞彙表改為下拉選取）要先由 acceptor 裁決。
- **技術選擇**：依 `DESIGN.md` §9.1 末段（Python、Streamlit 1.67.0、Anthropic 官方 SDK）。模型選定依 PD-5 的程序，在 C3 之後進行。

## 3. Acceptance and verification

### 3.1 Acceptance boundary

本契約的 acceptance boundary 由下列 AB-1～AB-13 組成。每項寫出可觀察的完成條件與證據要求；各 Spec 的具體 AC 由 Design Authority 在這個 boundary 內 derive，derivation record 必須寫明該 Spec 分配到哪幾項 AB（或其中哪些部分）。全部 derived Specs 合起來必須涵蓋 AB-1～AB-13。

| ID | 完成條件（可觀察） | 依據 | 證據要求 |
| --- | --- | --- | --- |
| AB-1 | 在 Streamlit 上，以一條來回行程完成 ①–⑧ 的端到端流程：輸入行程描述與表單 → 路線快照上的實際道路路線 → 依個人配速的典型與保守 ETA → 天氣、日照、加油、路況 → Validator 逐條判定 → Planner 的建議與說明 → 介面呈現狀態與來源 | `requirements_proposal.txt` 第一、六節；`DESIGN.md` §3、§4.3、§9.3 M3 完成條件 | 依 `README.md` 的指令重現的操作紀錄（畫面擷取或 log），以及對應的 commit。外部 API 不可用時，Snapshot Mode 的結果須標示為 snapshot，不得記為真實資料的執行 |
| AB-2 | FR1：行程描述、追問、來回與單向、期限的語意 | `DESIGN.md` §2.1 FR1 | derived Spec 的 AC 與測試 |
| AB-3 | FR2：歷史 GPX 多檔上傳、合併去重複、Profile 更新、涵蓋度摘要；資料不足時 UNKNOWN 並說明 | FR2 | 同上；測試只用合成 GPX |
| AB-4 | FR3：各路段的典型估計與加上安全餘裕的保守估計，含停等寬放；介面與文件不稱為 P90 或百分位數 | FR3、`DESIGN.md` §6.1 | 同上 |
| AB-5 | FR4：依抵達時間查氣象署預報與民用暮光終；規則 3 的範圍依 2026-11-15 定案 | FR4、`DESIGN.md` §4.2 | 同上，加上至少一次以真實授權碼取得的預報回應紀錄（不含授權碼）。沒有授權碼時標示 BLOCKED，AB-5 不得記為完成 |
| AB-6 | FR5：沿線加油站與檢查點自動產生、依出發油量逐段檢查、封路情境標示來源 | FR5、NFR5 | derived Spec 的 AC 與測試 |
| AB-7 | FR6：規則 1–5 三值判定、計畫狀態、重新規劃與無可行解的說明；`validator` 不匯入 `planner` 或任何 LLM client | FR6、`DESIGN.md` §4.2、§9.2 | 同上，加上匯入限制的測試 |
| AB-8 | FR7：Profile 區塊與三個畫面；UI-0 Skeleton 通過 acceptor 的 UI Delta Review 之後才開始正式整合 | FR7、`DESIGN.md` §9.6 | UI Delta Review 的 acceptor 紀錄；derived Spec 的 AC |
| AB-9 | 最小領域知識庫（關鍵字檢索、附出處）與公路與地標詞彙表，**且有實際整合**：至少一個合成的 Demo 情境中，Planner 使用知識庫的檢索結果，產生附來源的說明。只有詞彙表或靜態知識庫檔案不算 PASS。範圍限於關鍵字檢索，不擴張為進階 RAG（進階知識檢索是 Should） | `DESIGN.md` §7、§9.1 `kb`、§2.3 知識列 | derived Spec 的 AC 與測試，加上該 Demo 情境的執行紀錄：可追溯到被檢索的知識庫條目與它的出處，以及 Planner 輸出中引用該出處的位置 |
| AB-10 | NFR1–NFR5：每個時間、距離、機率可追溯到工具輸出；私有資料不進版控、不送第三方；資料缺漏時 UNKNOWN；模擬資料有來源標記 | `DESIGN.md` §2.2 | 各 derived Spec 的 AC；release gate 的私有資料檢查 |
| AB-11 | E1 Lite 與 E2 的程式、題庫、Oracle、凍結清單與分析計畫完成並在凍結日有 commit 可查；Oracle 不匯入產品模組 | `DESIGN.md` §6.2、§6.3、§9.2、§9.3 | 凍結清單與其 commit。正式執行的結果不是本項的完成條件（第 4.2 節） |
| AB-12 | `README.md` 與 `DESIGN.md` 依實際狀態更新：Installation、How to Run 實際跑過；Architecture、Flowchart、行號 Pseudocode 與實作一致；Results 只寫真實執行所得，未執行者標 NOT RUN | `requirements_proposal.txt` 第六節 B；root `CLAUDE.md` 的誠信規則 | 實際執行的紀錄；文件與程式的對照 |
| AB-13 | 整合條件：`.venv/Scripts/python.exe -m pytest -q` 全數通過；Bindings 第 5 節 release gate 的機密與私有資料檢查通過；每份 Spec 的 Spec Integration Audit 已 closure，且 Design Authority phase acceptance 已完成 | Bindings 第 5 節 | pytest 輸出、`git ls-files` 檢查輸出、audit records 與 phase acceptance 紀錄 |

### 3.2 PASS／FAIL 語義

- AB 的 PASS：分配給它的全部 derived Spec AC 都依 orch-default §7 結案，第 3.1 節的證據都存在且可追溯；AB-1、AB-5、AB-9、AB-12 另須有實際執行的證據。
- AB 的 FAIL 或未完成：任一分配到的 AC 未結案、證據缺漏，或證據來自 mock／self-test 而該項要求真實執行。
- 因憑證、付費授權或私有資料授權未到位而無法完成的 AB，記為 BLOCKED 並寫明缺少什麼，不記為 PASS，也不以推測補上。
- 依 `DESIGN.md` §9.3 的捨棄順序放掉的項目，只能放掉 Should 與該節列出的項目；放掉 Must 的第 2 項須先有 acceptor 裁決並記錄。

## 4. Authority and authorization

### 4.1 授權

acceptor（GitHub `yotsubamomo`，Bindings 第 2.1 節）接受本契約時，同時授權具相應 authority 的 Agents 在第 2 節的範圍與限制內：

- **規劃與分解**：Design Authority derive Spec 與 Tickets（含 `routing`、`routes`、`sources`、`planner`、`validator`、`kb`、`app/`、E1 Lite、E2 等目前沒有票的工作），寫 derivation record 並作 boundary determination。
- **實作**：Executor 在 implementation-ready 的 Tickets 內實作、self-verification、targeted correction。
- **本機 commit**：本契約正式接受後，Agents 可以在 topic branch 上作範圍內必要的本機 commit（Bindings SA-1）。這項授權取代先前「#7 的實作暫不 commit」的一次性限制。Push、PR、合併與破壞性 git 操作仍保留給 acceptor（RB-1、RB-6），不在 `main` 上 commit。
- **審查與裁決**：Reviewer、Alternate Reviewer、Final Adjudicator 依 Bindings 第 3.7 節與治理 §4 進行。
- **修正至完成**：契約內必要的 rework 與 re-verification。
- **Orchestrator run**：acceptor 指定主 session 為 Orchestrator 時，依 orch-default v2.2 run-to-completion。
- **GitHub Issues**：為 derived Tickets 建立必要的 Issues，並管理這些新建 Issues 的狀態（D-3）。建立前先檢查是否已有重複的 Issue；每個新 Issue 都要對應到明確的 Spec、AB 與 AC。#7–#12 不在此列。

### 4.2 保留給 acceptor 的動作

- Bindings 第 2.6 節的 RB-1～RB-7 全部保留：push、PR、合併、對外提交與發布、憑證、付費、修改上位契約與治理檔案與凍結基線、破壞性 git 操作、私有資料。
- **E1 Lite 與 E2 的正式執行**只在 acceptor 的指示下進行（root `CLAUDE.md`）；保留行程的解封由 acceptor 決定。
- **UI Delta Review** 由 acceptor 實際檢視並作決定。
- 修改 GitHub Issues #7–#12 的內容或狀態（含關閉）（D-3）。這些 Tickets 在 Formal run 中結案時，結案紀錄寫在 worklog 與 audit record；Issue 本身維持原狀，由 acceptor 決定是否更新。
- 任何超出第 2 節範圍、改變本契約 accepted 語義、或放掉 Must 的變更：依治理 §1.2、§5.3 重新取得 acceptor 的接受。

## 5. Relevant context

- **既有產出**（Bindings 第 8.1 節）：`DESIGN.md`、G1、G3、CR-01 與其裁決、SPEC-001 Draft v0.2、SPEC-RESOLUTION-001、Issues #7–#12、Spike 程式與 100 個 v0.2 契約測試。它們是輸入，不重新詢問已裁決的事。
- **未 implementation-ready 的範圍**：SB-3（路段對應鄉鎮）、SB-4（預報時段欄位）、SB-5（C3 真實 API 驗證，BLOCKED／NOT RUN）、SB-6（行程描述的輸入保護）、SB-10（尚未逐項審查的內容）涵蓋的部分，在 Blocker 關閉前不得納入 Formal run 的 Tickets。
- **外部依賴**：Anthropic 憑證（C3 與 `planner`）、中央氣象署授權碼（`sources`）、公開的 Valhalla 伺服器（`routing`，有條件批准）。
- **時程**：`DESIGN.md` §9.3。acceptor 2026-11-17 決定（原文「先定12/20」）：先以 2026-12-20 作為完成期限；老師尚未公布正式的繳交期限（PD-6），公布後若早於 12/20，依第 4.2 節處理；剩餘工作量估計 23–32.5 人日當量，除 M5 最後兩天外沒有緩衝。治理增加的 audit 成本沒有估進時程。
- **已知風險**：高風險類別 H-1～H-4（`decision-20261117-high-risk-categories.md`）；Fable alias 已改為 Fable 5.2（Bindings m2 O-4）。
- **課程資訊**（acceptor 2026-11-17 的決定，原文「評分其實沒有寫，先不管，IoT 先預設不必含。目前是3人一組，不過我會全做。」）：
  - 評分比重：課程文件沒有寫，先不處理。
  - IoT 感測器：預設不必包含，與 `DESIGN.md` §2.3 的 IoT 列（Won't）一致。老師若要求包含，屬範圍變更，依第 4.2 節處理。
  - 組別：3 人一組，全部工作由 acceptor 一人完成。
  - 仍未確認：最小知識庫（關鍵字檢索）的深度是否足夠。由 acceptor 向老師確認；Agents 不自行補出（Bindings 第 2.4 節）。確認結果若改變範圍，依第 4.2 節處理。

## 6. Assurance path

- **Lane**：Formal（Spec＋Tickets＋Orchestrator），依 Bindings 第 4 節（MVP 的模組實作屬 Formal）。之後的單點修正可依 Bindings 第 4 節走 Lightweight，作為新的 work item。
- **Audit**：每張 Ticket 一次 independent audit；每份 Spec 一次 Spec Integration Audit；Spec 只有一張 Ticket 時可用單 Ticket fast path（Bindings 第 5 節）。
- **高風險類別**：H-1～H-4 依 decision record 判定與處理；Design Authority 在 derivation record 中逐張 Ticket 標示。
- **Gate**：AB-13 的整合條件；UI Gate（AB-8）；12/5 的凍結（AB-11）。
- **Phase acceptance**：每份 Spec 由 Design Authority 依其 Spec Integration Audit record 作 phase acceptance。
- **並行度**：1（Bindings 第 6 節）。

## 7. Stable reference

- 本檔在 acceptor 接受時的 commit SHA，記在第 10 節。
- 本檔引用的 `DESIGN.md`、`docs/spec/`、`docs/ticket/`、`docs/cr/` 與 decision records，以同一個 commit 的內容為準。之後這些文件的修改若改變 Must 範圍或第 3 節的 acceptance boundary，是本契約的變更（治理 §5.3），須 acceptor 接受；只影響 derived contract 的設計細節者，依治理 §5.3 由 Design Authority 處理。

## 8. 與既有指示的關係

本契約正式接受後，改變一項既有指示：

- **本機 commit**：先前「#7 的實作暫不 commit」的一次性限制，由第 4.1 節的本機 commit 授權取代。Push、PR、合併與破壞性 git 操作仍保留給 acceptor。

下列既有指示仍然有效，本契約不改變它們：

- BATCH-1 的五張 Issues 不修改、不重建；#7–#12 的內容與狀態不由 Agents 修改（D-3）。
- 不宣告完整的 SPEC-001 Freeze；只關閉有實際完成規格與驗收條件的 Blockers。
- C3 維持 BLOCKED／NOT RUN，直到真的用真實 API 執行過。
- 盡量避免增加審查循環：治理要求的 audit 照做，不另外增加 Bindings 沒有要求的審查。

## 9. 起草時的選擇（acceptor 2026-11-17 裁決）

| # | 選擇 | 裁決 |
| --- | --- | --- |
| D-1 | 本契約的範圍 | 採用預設：整個 MVP 的 Must（第 2.1 節） |
| D-2 | Should 項目 | 採用預設：全部不在範圍內，要做時逐項另外授權 |
| D-3 | GitHub Issues | 採用預設：允許建立必要的 derived Issues 並管理新建 Issues 的狀態；建立前檢查重複，每個新 Issue 對應明確的 Spec、AB 與 AC；#7–#12 的內容與狀態不得修改（第 4.1、4.2 節） |
| D-4 | 交付文件 | 採用預設：`README.md`、`DESIGN.md`、Conclusion 在範圍內；Final PPT、Final Video 與正式繳交不在範圍內 |
| D-5 | LLM 與實驗的支出 | 採用預設：不新增 API 支出授權，只維持 C3 的 US$3。缺額度時標示 BLOCKED，不以 mock 代替正式執行 |

同一則指示另外要求兩處修正：第 4.1 節與第 8 節的本機 commit 授權；AB-9 的實際整合驗收。其他 AB-1～AB-13、RB-1～RB-7、Formal lane、audit 與並行度維持草稿。

### 9.1 一致性檢查留下的事項（2026-11-17，起草者）

這兩項不是條文之間的矛盾，條文已規定如何處理；列出來是因為它們會影響本契約能否全部 PASS，由 acceptor 決定是否在接受前處理：

| # | 事項 | 目前條文的結果 |
| --- | --- | --- |
| C-1 | AB-1（端到端流程）與 AB-9（Planner 使用知識庫的 Demo）都需要 Planner 實際呼叫 LLM。D-5 沒有開發或 Demo 的 API 額度；C3 的 US$3 只限 smoke test | 依第 3.2 節與 D-5，在另有額度授權前，AB-1 與 AB-9 只能記為 BLOCKED；以 scripted model 執行的結果不算實際執行。本契約要全部 PASS，之後需要 acceptor 另外授權額度 |
| C-2 | 第 4.1、8 節所說「#7 的實作暫不 commit」的一次性限制，在本 repo 的 `docs/` 中找不到書面紀錄 | 依 acceptor 2026-11-17 指示的文字記載；不影響其他條文 |

## 10. 接受紀錄

| 欄位 | 內容 |
| --- | --- |
| Acceptor | 本 repo 擁有者（GitHub `yotsubamomo`，Bindings 第 2.1 節） |
| 原始指示（原文） | 「接受 873e37a」 |
| 日期 | 2026-11-17 |
| 所接受的 commit | `873e37ae98d701c076b1bc533c7993ca62c2dd6c`（本檔在該 commit 的內容） |
| 第 9 節的最終選擇 | D-1～D-5 全部採用預設，內容如第 9 節表格；第 4.1 節、第 8 節的本機 commit 授權與 AB-9 的實際整合驗收依 acceptor 2026-11-17 的指示加入 |
| 接受前已知的事項 | 第 9.1 節 C-1（AB-1、AB-9 在另有 API 額度授權前只能 BLOCKED）與 C-2，以條文現狀接受 |
| 轉錄者 | 無角色 session，依 acceptor 的指示轉錄；本列不改動任何條文 |
