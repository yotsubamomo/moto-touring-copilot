# Project Bindings — moto-touring-copilot

本檔是本 repo 依 Minimal Operational Governance v2.2 §5.1 宣告的 Project Bindings：治理的適用範圍，以及權限來源、角色與模型、lane、assurance、工具與紀錄位置。

- **Bindings 版本**：m2（2026-11-17，**待接受**）。m2 相對 m1 只新增 O-4（Fable mapping 改為 Fable 5.2，第 3.1、3.2 節）；m2 生效前，生效的是 m1（2026-11-17 針對 commit `39e77ec` 接受），O-4 不生效，任何 Fable 路徑都不得使用。第 8.2 節的狀態欄是紀錄轉錄，不是規則變更。
- **來源**：由 `aiot-classwork` 的 Project Bindings b5（2026-10-14）移植。第 3 節（角色與模型）照原樣沿用；第 0、2、4、5、7、8 節依本專案改寫。兩個 repo 的 Bindings 各自獨立，之後的變更不互相連動。
- **生效條件**：acceptor 明確接受本版，方式是下列之一：(a) 把引入本版的 PR 合併進 `main`；(b) 在對話中針對含本版的 commit SHA 明確表示接受，原文與日期記入第 9 節。生效前本檔只是提案，不構成任何授權（含第 2.5 節的 standing authorization）。**m1 已依 (b) 生效**，接受紀錄在第 9 節。
- **優先順序**（治理 §5.3；orch-default §1）：治理本文 ＞ 本檔 ＞ Accepted Work Contract ＞ Implementation Profile ＞ Orchestrator Contract ＞ Runtime 工具。Root `CLAUDE.md` 的其他規則視為本檔的一部分；與治理 MUST 衝突時以治理為準。
- **整體取向：Lightweight 優先。** 本專案是一人進行的課程期末專題。在治理允許的範圍內一律選最輕的做法：預設 Lightweight lane（第 4 節）、Lightweight 預設不做 independent audit（第 5 節）、bounded assignments 只採用 `investigator` 與 `bounded_worker` 兩種（第 3.4 節）、不宣告額外的 escalation trigger 或 diversity 要求。治理的 MUST 不因此放寬。

下文的 `PKG/` 指 [`Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/)。

## 0. 適用範圍

**整個 repo 都適用治理，沒有 governance flag。** `aiot-classwork` 以 flag 區分作業（on）與課堂實作（off）；本專案不作這個區分。

- 本 repo 內的每個 work item 都適用治理本文全部的 MUST／SHOULD／MAY 與本檔，不論它動到的是程式、測試、文件、實驗腳本、原型或設定檔。
- 沒有「部分關閉」的狀態。工作的輕重由 lane（Lightweight／Formal）決定，依治理 §3.3、§3.6 與第 4 節判定。
- 與 acceptor 對話、Grill、查詢、說明、狀態回報不是 work item，由無角色 session 進行（第 3.5 節）；它不取得任何 authority。
- 縮小適用範圍是 Bindings 變更：只在 work item 之間進行，並在第 9 節留下版本、依據與授權（治理 §5.3）。

## 1. Governance adoption

採用 **Minimal Governance — Reusable Package v2.2**（package 說明見 [`PKG/README.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/README.md)）：

| Artifact | 採用版本 | Overrides | 生效檔案 |
| --- | --- | --- | --- |
| Minimal Operational Governance（normative authority） | v2.2（Adopted／Frozen 2026-10-12） | — | [`PKG/Minimal_Operational_Governance_v2.2_Candidate.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/Minimal_Operational_Governance_v2.2_Candidate.md)（檔名沿用 Candidate 字樣，狀態以 header 為準） |
| Reference Model Profile | `default` `v2.5`（Adopted／Frozen 2026-10-11），連同其以引用方式沿用的 `default` `v2.4` 章節 | 見第 3 節（O-1、O-2、O-3、O-4） | [`PKG/references/model-profiles/default-v2.5.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/model-profiles/default-v2.5.md)、[`default-v2.4.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/model-profiles/default-v2.4.md) |
| Implementation Profile | `impl-default` `v2`（Adopted／Frozen 2026-09-22） | none | [`PKG/references/implementation-profiles/default-v2.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/implementation-profiles/default-v2.md) |
| Reference Orchestrator Contract | `orch-default` `v2.2`（Adopted／Frozen 2026-10-12） | none | [`PKG/references/orchestrator-contracts/default-v2.2.md`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/references/orchestrator-contracts/default-v2.2.md) |

- **權威位置**：package 的權威來源是 package 作者工作區的 `master_governance/`（見 `PKG/README.md`），不在本 repo。`PKG/` 是位元複本，2026-11-17 自 `aiot-classwork` 的 `docs/governance/` 複製（只取該 repo 追蹤中的檔案），以 `PKG/MD5SUMS`、`PKG/SHA256SUMS` 核對全部 OK。上一層的 `.gitattributes`（`* -text`）一併複製，避免 checkout 時換行被轉換而使 hash 失效。發現與權威來源不一致時，以權威來源為準，重新放入複本並核對 hash。`PKG/` 內的檔案不在本 repo 修改。
- **只有上表的檔案是本專案生效的規範。** `PKG/` 中其他檔案——Minimal v2.1 與 orch-default v2.1 等 frozen baselines、visualization HTML、`records/` 內的採用與 review 紀錄——只供參考與追溯，不構成本專案的規則或 fallback authority。
- **版本化陳述**：impl-default v2 的 header 標 Minimal v2.0、§11 引用 Profile `default` v2；orch-default v2.2 §2 引用 Profile `default` v2.3；`default` v2.5 的 header 標 Minimal v2.1。這些是凍結當時的陳述（`PKG/README.md`「已知未處理」），本專案的實際 mapping 以第 3 節為準。
- **變更 authority**：acceptor（第 2.1 節）。Governance、本檔、profiles 與 definitions 的任何變更都依治理 §5.3 留下版本、依據與授權，記在第 9 節。

## 2. Authority sources

### 2.1 Acceptor

本 repo 擁有者（GitHub `yotsubamomo`）是唯一的人類 acceptor，沒有指定其他人類代理。Outcome Contract 的接受與授權、boundary re-authorization、第 2.6 節的 reserved boundaries，都只能由 acceptor 在對話中明確指示或在紀錄上簽署。Agent 代寫的接受紀錄不等於取得授權（治理 §5.3）。

### 2.2 上位契約

[`docs/requirement/`](../requirement/) 內老師提供的期末專題規範與講義是本專案的上位契約，對所有 Agent 唯讀：

| 檔案 | 內容 |
| --- | --- |
| `requirements_proposal.txt` | 期末專題提案作業規範：Domain AI Agent 的基本要求、①–⑧ 架構、三種技術表示（System Architecture、Flowchart、行號 Pseudocode）、AI 使用規範、Final Handover Package |
| `Part_3._課程專題說明.pdf` | 課程專題說明：工作流程、六項能力、Level 1–3 |
| `L4-1_期末計劃Proposal_寫作方法_.pdf` | Proposal 寫作方法 |
| `期未計劃-架構圖建議.png` | 老師建議的架構圖 |

Outcome Contract 不得超出上位契約。

**版控**（acceptor 2026-11-17 決定）：只有 `requirements_proposal.txt` 進版控。兩份講義 PDF 與架構圖是老師的教材，本 repo 是公開的，所以只留在本機並列入 `.gitignore`；本機的 Agents 仍可讀取。在沒有這三份檔案的環境（另一台電腦、雲端 session）工作時，需要引用它們的判斷記為未驗證，不以記憶或轉述代替。

**最終判準**（acceptor 2026-11-16 的指示，原文）：「這次 Project Review 的最終判準請收斂為老師在 requirements_proposal.txt 定義的 ①～⑧ Domain AI Agent 架構，以及課程的基本要求。」

**原始 Proposal 不是上位契約。** [`docs/proposal/`](../proposal/) 的 Proposal 是本專案在 Proposal 階段交出的文件。相對於它的 Scope Reduction 是 acceptor 已接受的決定（2026-11-16 原文）：「原始 Proposal 中的多 Agent、LightGBM、P90、Google Maps、279 趟資料與部分實驗，因期末時間限制進行 Scope Reduction，這是已知且接受的決策，不需要重新恢復。」審查與稽核不得把已接受的 Scope Reduction 記為不符合上位契約；它只是紀錄（`DESIGN.md` §13、`docs/cr/CR-01-proposal-alignment.md`）。

### 2.3 Outcome Contract

- **Lightweight**：acceptor 在對話中的直接指示就是 Outcome Contract（治理 §1.2、§3.5），條件是它不需要對 intent、scope、acceptance、authority 作任何假設（治理 §3.3）。Executor 在 worklog 的 Contract reference 原文引用該指示與日期。
- **Formal**，或直接指示不足以確定上述四項時：開始實作前先有一份 `docs/governance/records/outcome-contract.md`（多份時加後綴），內容滿足治理 §3.1 七項 properties，檔尾附**接受紀錄**：acceptor 的原始指示（引用原文）、日期、所接受的檔案 commit SHA。沒有接受紀錄的 Outcome Contract 不得啟動 Formal run，也不得開始實作。
- Agents 不自行發起 Outcome Contract（治理 §1.2）。起草只在 acceptor 指示下進行，草稿在 acceptor 接受前不是契約。

### 2.4 範圍與契約邊界

- **Must 範圍以 `DESIGN.md` §9.1 為準**（已接受的 Outcome Contract 另有界定時，以 Outcome Contract 為準）。新增 Must 項目、恢復已接受的 Scope Reduction、或加入老師沒有提出的要求，都超出 Outcome Contract scope，依治理 §1.2 由 acceptor 重新授權。
- acceptor 明確授權的 Should／Optional 範圍可以超出老師的要求，但必須維持明確標示，且不得取代、弱化或被呈現為老師要求的行為。
- 老師的要求有多種解讀、且選擇會改變交付內容或評分對象時，屬於 scope 問題：在 Outcome Contract 接受前與 acceptor 確認，寫進 Outcome Contract。執行中才發現的，先 route 至 Design Authority 作 boundary determination；DA 無法確立在 boundary 內時 fail-closed 至 acceptor（治理 §1.2、§1.5）。
- 已接受範圍內、只影響實作的語義問題，由 Design Authority 以 decision record 裁決（治理 §3.6-A），不回問 acceptor。
- Repository 裡找不到的課程資訊（例如期末繳交期限、評分比重、是否必須包含 IoT 感測器）視為未知，由 acceptor 向老師確認；Agents 不自行補出。

### 2.5 Standing authorizations

以下由 acceptor 宣告，隨本檔生效；撤銷方式是修改本節並記入第 9 節。只在有已接受的 Outcome Contract 時適用。

| ID | 涵蓋 | 排除 |
| --- | --- | --- |
| SA-1 | 依 `docs/conventions/git-commit-rules.md` 建立 topic branch，並在 topic branch 上作本機 commit。 | 在 `main` 上 commit；push 任何分支（RB-1）；force push；刪除或改寫既有歷史（RB-6）。 |

`aiot-classwork` 的 SA-1（含 push）、SA-2（開 PR）與 SA-3（自主合併）**沒有移植**：本 repo 是公開的，而本專案到目前為止的指示是 push、PR 與合併都逐次由 acceptor 授權。要開放其中任何一項，在本表加一列並記入第 9 節。

### 2.6 Reserved boundaries

治理 §5.2 採 opt-in；本專案保留下列決定與動作給 acceptor，Agent 遇到時只停止受影響路徑並依治理 §1.5 寫 stop report：

| ID | 保留的決定／動作 |
| --- | --- |
| RB-1 | Push 任何分支到 `origin`、開 Pull Request、合併任何分支進 `main`。本 repo 是公開的，push 即公開。 |
| RB-2 | 繳交期末專題或任何對外提交與發布（課程平台、YouTube、簡報上傳等）。 |
| RB-3 | 申請、輪替或填寫憑證（Anthropic API key、中央氣象署授權碼等）；第三方帳號操作。金鑰只能放在未追蹤的本機 `.env`，只由 acceptor 親自填入；Agents 不得讀出、印出、複製或匯出其值。金鑰任何時候都不得進 git、log、文件、evidence 或送往外部服務的內容。 |
| RB-4 | 任何需要付費的動作。呼叫 Anthropic API 會計費：只能在 acceptor 明確授權的額度內執行。目前已授權的只有一項——C3 的真實 API smoke test，上限 US$3；正式 E2 與其他用量尚未授權。 |
| RB-5 | 修改下列檔案：`docs/requirement/` 的上位契約；治理檔案（`docs/governance/` 的 `PKG/`、本檔、`binding-verification.md`，`.claude/agents/gov-*.md`，root `CLAUDE.md` 與 `AGENTS.md`）；已凍結的基線（G1 的裁決紀錄、G3 Frozen Baseline `prototype/index.html` 與 `docs/ui/` 內標示 G3 Frozen 的文件）。`docs/governance/records/` 是工作紀錄，不在此列。 |
| RB-6 | 破壞性或不可逆的 git 操作：force push、改寫歷史、刪除非本次 run 建立的分支。 |
| RB-7 | 私有騎乘資料。(1) 讀取、列出或搜尋 `data/`（含 `data/private/`），或執行會讀取私有資料的 `experiments/` 腳本，只限 acceptor 針對該 work item 以明確路徑授權的檔案；不以泛用搜尋掃描，不從 repo root 搜尋。(2) 保留行程（holdout，4 趟）在分析方法與模型設定凍結前不得讀取；解封由 acceptor 決定。(3) 私有資料及由它導出的位置資訊不得進 git、log、文件、evidence，也不得放進送往外部 API 的內容，除非 acceptor 明確授權其範圍。 |

**不保留**（依治理 §5.2 預設，由 Outcome Contract 的授權涵蓋）：Spec review、獨立的 implementation authorization。要改成保留，在本表加一列並記入第 9 節。

## 3. Agent definitions 與 Model Mapping Profile

### 3.1 有效 mapping

採用 `default` `v2.5`，overrides 為 O-1、O-2、O-3（O-3 見第 3.4 節）、O-4（m2，見本節「Fable alias」）。六個治理角色與 `executor` fallback 的 definition 放在 `.claude/agents/`：

| Identifier | Definition | Model | Effort | 依據 |
| --- | --- | --- | --- | --- |
| `design_authority` | [`gov-design-authority`](../../.claude/agents/gov-design-authority.md) | `claude-opus-5-5` | `high` | Profile 預設 |
| `executor` | [`gov-executor`](../../.claude/agents/gov-executor.md) | `claude-opus-5-5` | `high` | **O-1** |
| `executor`（fallback） | [`gov-executor-fallback`](../../.claude/agents/gov-executor-fallback.md) | `claude-opus-4-8` | `high` | O-1 的 fallback（＝Profile F-EX\* 列） |
| `primary_reviewer` | [`gov-primary-reviewer`](../../.claude/agents/gov-primary-reviewer.md) | `claude-opus-5-5` | `xhigh` | Profile Claude path 首項；Codex 未宣告，屬 resolution（Profile §7＝v2.4 §6 條件 1），不記 substitution |
| `alternate_reviewer` | [`gov-alternate-reviewer`](../../.claude/agents/gov-alternate-reviewer.md) | `claude-opus-5-5` | `xhigh` | Profile 預設 |
| `final_adjudicator` | [`gov-final-adjudicator`](../../.claude/agents/gov-final-adjudicator.md) | `claude-opus-5-5` | `xhigh` | Profile 預設 |
| `orchestrator` | [`gov-orchestrator`](../../.claude/agents/gov-orchestrator.md)（root role session，不以 subagent 派工） | `claude-opus-5-5` | `medium` | Profile 預設 |

**O-1 `executor` mapping override**：Profile 預設 Sonnet 5.5／`medium` 改為 `claude-opus-5-5`／`high`。依據：沿用 `aiot-classwork` Bindings 的 O-1（acceptor 2026-09-24 決定：Executor 用 Opus 5.5／`high`、fallback Opus 4.8／`high`），並使主 session 以 Opus 5.5／`high` 執行時能直接擔任 Lightweight Executor（第 3.5 節），不必另派 subagent。Fallback 只有 `claude-opus-4-8`／`high`（`gov-executor-fallback`）；Profile 不允許 Executor 用 Fable，列耗盡即依治理 §1.5 recovery。Profile 的 E-EX 不適用：其 escalated mapping 等於 O-1。要改回 Profile 預設，刪除 O-1 並記入第 9 節。

**O-2 fallback 列的 runtime override**（Profile §4.2 末句：runtime 無法派工某 model 時由 Bindings override）：Agent tool 只能以 definition frontmatter 或 `model` alias（`opus`、`sonnet`、`haiku`、`fable`）指定 model，沒有對應 Opus 4.8 的 alias。因此被派工角色的 fallback 列略過 Opus 4.8（`executor` 除外，它有 `gov-executor-fallback`）。有效 fallback 列：

| Policy | 有效 mapping | Fallback（依序） | 派工方式 |
| --- | --- | --- | --- |
| F-DA | Opus 5.5／`high` | Fable 5.2／`high` | `gov-design-authority`＋`model: fable`、`effort: high` |
| F-DA\* | Fable 5.2／`xhigh`（E-DA） | Opus 5.5／`xhigh` | `gov-design-authority`＋`effort: xhigh` |
| F-EX\*（O-1） | Opus 5.5／`high` | Opus 4.8／`high` | `gov-executor-fallback` |
| R-PR | Opus 5.5／`xhigh` | Fable 5.2／`xhigh` | `gov-primary-reviewer`＋`model: fable` |
| F-AR | Opus 5.5／`xhigh` | 無（列耗盡 → 治理 §1.5 recovery） | — |
| F-AR\* | Fable 5.2／`xhigh`（E-AR） | Opus 5.5／`xhigh` | `gov-alternate-reviewer`（frontmatter 即此 mapping） |
| F-FA | Opus 5.5／`xhigh` | Fable 5.2／`xhigh` | `gov-final-adjudicator`＋`model: fable` |
| F-FA\* | Fable 5.2／`xhigh`（E-FA） | Opus 5.5／`xhigh` | `gov-final-adjudicator`（frontmatter 即此 mapping） |
| F-OR／F-OR\* | Opus 5.5／`medium`（`high`） | 依 Profile 列：Opus 4.8 → Sonnet 5.5／`high` | Root session 以完整 model id 啟動（`claude --model claude-opus-4-8 --effort <effort>` 或 `/model`、`/effort`），不受 alias 限制 |
| F-BW（`standard`，O-3） | Sonnet 5.5／`high` | Opus 5.5／`high` | `gov-bounded-worker`＋`model: opus` |
| F-BW（`mechanical`，O-3） | Haiku 5.5／`high`（qualification 通過後；之前依 `standard` 派工） | Sonnet 5.5／`high` → Opus 5.5／`high` | `gov-bounded-worker`（Sonnet）；`gov-bounded-worker`＋`model: opus` |
| F-IN（O-3） | Sonnet 5.5／`high` | Opus 5.5／`high` | `gov-investigator`＋`model: opus`、`effort: high` |
| F-IN\* | Opus 5.5／`high`（E-IN，O-3） | Sonnet 5.5／`high` | `gov-investigator`（frontmatter 即此 mapping） |

替代規則見 Profile §4.1（＝v2.4 §3 共同規則 1–5 加規則 6–7）：只能依當次錯誤或當下可用性證據替代，不得憑記憶或前次 session 跳過；每次替代記錄原 mapping、替代 mapping、證據引用（Profile §8）。Overload／rate-limit 不另宣告 bounded retry：harness 自身重試後仍回傳的 429／529 即構成當次可用性證據。Mapping 變更 authority 為 acceptor。

**Fable alias 與 O-4 Fable mapping override**（m2）：Profile 所列的 Fable 5.1，在本專案一律改為 Fable 5.2（`claude-fable-5-2`），effort 不變；上表與第 3.2 節已改寫。涵蓋 E-DA、E-AR、E-FA，以及 F-DA、R-PR、F-FA 的 fallback。
- 依據：第 8.2 節的 dry-run（2026-11-17，[`binding-verification.md`](binding-verification.md) 第 10 列）觀測到 `model: fable` 解析為 `claude-fable-5-2`，不是 Profile 所列的 `claude-fable-5-1`；Agent tool 沒有能指定 Fable 5.1 的 alias（同 O-2 的理由）。
- 授權：acceptor 2026-11-17 決定（原文）：「gov-alternate-reviewer＋model: fable ，改為Fable 5.2」。
- 派工方式不變，仍以 `model: fable` 派工，每次都以 transcript 核對實際 model 是 `claude-fable-5-2`（第 3.6 節）。alias 之後解析到其他 model 時，該次派工不是合格產出，依本節的替代規則處理，並在下一次使用 Fable 路徑前由 acceptor 決定是否修改 O-4。
- 要改回 Profile 的 Fable 5.1，刪除 O-4 並記入第 9 節。

### 3.2 Capability escalation

採用 Profile §3，限於下列 identifier；trigger、範圍與規則依 Profile §3.1 E-1～E-10 與治理 §2.5。Orchestrator 或派工的 session 只機械套用 trigger，不判斷能力是否足夠。

| ID | Identifier | Escalated mapping | 本專案採用的 trigger | 派工方式 |
| --- | --- | --- | --- | --- |
| E-DA | `design_authority` | Fable 5.2／`xhigh` | (D1)、(D2)。(M1) 不採用：本檔不宣告任何類別的 DA 決定使用 Fable | `gov-design-authority`＋`model: fable`、`effort: xhigh` |
| E-AR | `alternate_reviewer` | Fable 5.2／`xhigh` | (D1)，含 Profile 所列三項條件 | `gov-alternate-reviewer`＋`model: fable`（fresh context） |
| E-FA | `final_adjudicator` | Fable 5.2／`xhigh` | (M2)、(D1)。(M1) 不採用：本檔不宣告以高風險類別觸發 Fable | `gov-final-adjudicator`＋`model: fable`（fresh context） |
| E-OR | `orchestrator` | Opus 5.5／`high` | (M1)、(D1)；於 activation 或 successor session 生效，記入 run record | Root session 以 `--effort high`（或 `/effort high`）啟動 |
| E-BW | `bounded_worker` | `mechanical` → `standard`（Sonnet 5.5／`high`，O-3） | (D1)：呼叫者核對後記錄 `mechanical` 輸出不足或錯誤；`standard` 不再升級 | `gov-bounded-worker`（frontmatter 即 `standard`） |
| E-IN | `investigator` | Opus 5.5／`high`（O-3） | (D1) 呼叫者記錄調查跨多個子系統且原因交互作用；(D2) investigator 回報 inconclusive 並附理由 | `gov-investigator`＋`model: opus` |

E-EX 不適用（O-1）；E-AD 不適用（`advisor` 未採用，第 3.4 節）。Escalation record 依 Profile §8 寫在派工者的 worklog 或 run record；review／adjudication 角色提出 D trigger 時寫在自己的 record，並且不作 verdict 或 ruling（治理 §2.5 規則 3）。

### 3.3 Codex

Codex **未宣告**：不作任何角色的 mapping 或 override，也不在任何 fallback 列。`primary_reviewer` 因此解析為 Opus 5.5／`xhigh`（resolution）。要讓 Codex 擔任 `primary_reviewer`，先在本節完成 Profile v2.4 §5 的四項宣告與 qualification，並記入第 9 節。

### 3.4 Bounded assignments 與其他 subagents

採用 Profile §2.2 的兩個 bounded assignments（治理 §2.6）。它們**不是治理角色，沒有任何 authority**；輸出是呼叫者待核對的輸入，不構成 finding、verdict、ruling、decision、derivation、接受、授權或 audit record。`advisor` 不採用。

| Identifier | Definition | Model | Effort | 用途 | 允許的呼叫者 |
| --- | --- | --- | --- | --- | --- |
| `investigator` | [`gov-investigator`](../../.claude/agents/gov-investigator.md) | `claude-sonnet-5-5` | `high`（O-3） | 唯讀調查：跨檔案追查、root-cause 假設、證據蒐集 | Executor；Orchestrator（只限控制面，例如狀態擷取） |
| `bounded_worker`（`standard`） | [`gov-bounded-worker`](../../.claude/agents/gov-bounded-worker.md) | `claude-sonnet-5-5` | `high`（O-3） | 有界、呼叫者可核對的工作：搜尋、擷取、格式轉換、依明確樣式的機械修改、log／diff 摘要 | Executor；Orchestrator（只限控制面，例如紀錄整理） |
| `bounded_worker`（`mechanical`） | `gov-bounded-worker`＋`model: haiku` | `claude-haiku-5-5`（O-3；qualification-gated，見下） | `high`（O-3） | 同上，可由呼叫者機械核對者 | 同上 |

- **Task class**：呼叫者派工時指定 `standard` 或 `mechanical` 並記錄；無法明確歸為 `mechanical` 者一律 `standard`。
- **Haiku 是 qualification-gated**（Profile §2.2；`aiot-classwork` 已於 2026-10-14 通過，**本專案須在第 8.2 節的 dry-run 重新觀測**）：第 8.2 節的 qualification probe 觀測到實際 model 為 `claude-haiku-5-5`、effort 為 `high`，並記入 `binding-verification.md` 之後，`mechanical` 才以 Haiku 派工；在那之前 `mechanical` 依 `standard` 派工（Sonnet 5.5／`high`，resolution，不記 substitution）。
- **O-3 effort／model override**（沿用 `aiot-classwork` Bindings；acceptor 2026-10-14 決議）：`investigator` 與 `bounded_worker`（`standard`）由 Profile 的 Sonnet 5.5／`medium` 改為 Sonnet 5.5／`high`；`bounded_worker`（`mechanical`）由 Haiku 5.5／`low` 改為 Haiku 5.5／`high`。Fallback 依同一 effort（第 3.1 節 F-BW、F-IN）。E-IN 的 escalated mapping 由 Profile 的 Opus 5.5／`medium` 改為 Opus 5.5／`high`。
- **呼叫者限制**：Design Authority、Reviewers 與 Final Adjudicator 的 definition 沒有 Agent tool，不呼叫 bounded assignments，審查與裁決的證據一律自己取得。Orchestrator 不得藉 bounded assignment 取得治理 §2.4 禁止它作的判斷（治理 §2.6 第 6 項）。
- **呼叫者的責任**（治理 §2.6）：自行核對輸出後才使用；需要 authority 的決定由呼叫者以自己的角色作出並寫入自己的紀錄。Executor 使用 bounded assignment 屬 self-verification，不算 independent audit。呼叫者在 worklog 或 run record 記下所用的 bounded assignment、task class、binding 證據（第 3.6 節）與輸出的採用方式；它的動作不另成 work item。
- **範圍**：bounded assignment 不得擴大委派範圍、派工任何 subagent，或以任何角色的名義作成紀錄；`investigator` 唯讀，不修改任何檔案。
- 在 governance on 的 work item 中，治理角色只派工第 3.1 節與本節的 `gov-*` definitions；不派 `Explore`、`Plan`、`general-purpose`、fork 型或其他未在本檔宣告的 subagent。

### 3.5 Session 的角色（治理 §2.2、§2.7）

- **無角色 session**：主 session 預設不擔任任何治理角色。它可以與 acceptor 對話、Grill、查詢、說明，也可以作為派工介面派 `gov-*`（派工仍須符合第 3.6、3.7 節），但不取得任何 authority，派工也不構成任何角色的 activation basis。它寫的內容不是治理紀錄；依 acceptor 明確指示轉錄決定時，紀錄標明決定者。
- **Lightweight direct-execution Executor**：主 session 明確進入 Executor 角色前，須同時具備：(1) activation basis——acceptor 已接受的 Outcome Contract（第 2.3 節）且 lane 為 Lightweight；(2) 該 session transcript 的 model／effort 為 `claude-opus-5-5`／`high`（第 3.6 節）；(3) 讀過 `.claude/agents/gov-executor.md`；(4) 該 work item 的 worklog。進入點記入 worklog。Model／effort 不符時，主 session 不得擔任 Executor，改派 `gov-executor` subagent，自己只負責派工與 routing。
- **Orchestrator**：acceptor 在主 session 指定（designation），session 以 `claude-opus-5-5`、effort `medium`（E-OR 成立時 `high`）執行，先讀 `.claude/agents/gov-orchestrator.md`，以 run record 為 work identity。`gov-orchestrator` 不以 subagent 派工。
- 一次只擔任一個角色；work item 或 run 結束時角色隨之結束（治理 §2.7 第 6、7 項）。同一執行 context 不得轉名成 Reviewer。

### 3.6 Binding verification

- 每個 definition 的 frontmatter 綁定完整 model id 與 effort，不使用 `inherit`。不設定會覆寫角色綁定的全域 subagent model（例如 `CLAUDE_CODE_SUBAGENT_MODEL`）。
- Escalated 或 fallback mapping 以同一 definition 加 Agent tool 的 per-dispatch `model`／`effort` 參數派工（Profile §6 (b)），`gov-executor-fallback` 除外。`model` 參數是 alias，每次都以 transcript 核對實際 model。
- **證據來源**（orch-default v2.2 §11；可逐筆觀察）：
  - 被派工的 assignment：`~/.claude/projects/<專案 slug>/<session-id>/subagents/` 內，`agent-<agentId>.meta.json` 的 `agentType` 是 definition 名稱，`agent-<agentId>.jsonl` 每一則 assistant 訊息的 `message.model` 與 `effort` 是實際 model 與 effort。
  - Root role session（Orchestrator、direct-execution Executor）：`~/.claude/projects/<專案 slug>/<session-id>.jsonl` 每一則 assistant 訊息的 `message.model` 與 `effort`。
- **全程核對**（治理 §2.2 V22-10；orch-default v2.2 §3）：核對對象是 assignment 的全部 assistant 訊息，不只第一則。觀測到的 (model, effort) 集合必須只有一個元素，且等於該次派工的有效 mapping（含已記錄的 escalation 或替代）。出現第二個元素即是改變點；自改變點起的工作不是合格產出，依治理 §2.2 修復或替代。時點：
  - 採用被派工 assignment 的 return 之前。
  - Root role session 的工作被用作 commit、gate、routing、rollover 交接或 completion 的依據之前，核對自上次核對以來的該段 transcript；direct-execution Executor 至少在結案前核對一次。
  - 無法取得涵蓋該段工作的證據時 fail closed：該段工作不作上述依據。
- 核對結果以「agentId（或 session-id）＋觀測到的 (model, effort) 與則數」寫進 worklog、audit record 或 run record 的 binding 欄位。

核對指令（`<session-dir>` 換成 `~/.claude/projects/<專案 slug>/<session-id>`）：

```bash
python - "<session-dir>" <<'EOF'
import json, pathlib, sys
from collections import Counter
root = pathlib.Path(sys.argv[1])
def scan(path):
    seen = Counter()
    for line in path.open(encoding="utf-8"):
        d = json.loads(line)
        m = d.get("message")
        if d.get("type") == "assistant" and isinstance(m, dict) and m.get("model"):
            seen[(m["model"], d.get("effort"))] += 1
    return dict(seen)
session = root.with_suffix(".jsonl")
if session.exists():
    print("root-session", root.name, scan(session))
for meta in sorted(root.joinpath("subagents").glob("agent-*.meta.json")):
    agent_type = json.loads(meta.read_text(encoding="utf-8")).get("agentType")
    print(meta.name.replace(".meta.json", ""), agent_type,
          scan(meta.with_name(meta.name.replace(".meta.json", ".jsonl"))))
EOF
```

### 3.7 Independent dispatch 機制（治理 §2.3）

正式 audit 與裁決由 Orchestrator 或主 session 透過 Claude Code 的 Agent tool 派工，`subagent_type` 指定 `gov-primary-reviewer`、`gov-alternate-reviewer` 或 `gov-final-adjudicator`。四項 properties 的滿足方式：

1. **Independent context**：非 fork 的 subagent 從空白 context 開始，不繼承派工者的對話。派工內容只放 bounded pack：Outcome Contract、Spec／Ticket、worklog、受審 subject（branch 與 commit SHA）的**路徑與識別**，不放 Executor 的結論或摘要。審查與裁決一律不得使用 fork 型 subagent。R2 可延續同一 reviewer 的 R1 context（以 SendMessage 續派同一個 agent），但 MUST 重讀修正後的檔案與 diff；以 escalated mapping 重派的 review 或 adjudication 一律是新的 fresh 派工。
2. **Verifiable binding**：依第 3.6 節核對。
3. **Autonomous access**：reviewer 與 adjudicator 有 Read、Grep、Glob、Bash，可自行讀取 repo、git 歷史並執行測試；bounded pack 只是入口。RB-7 對 reviewer 與 adjudicator 同樣適用：`data/` 只能讀 acceptor 以明確路徑授權、並列在派工內容的檔案；需要其他私有資料才能核對的項目，在 record 寫明並回報 required authority = acceptor，不得記為已驗證，派工者也不得為此放寬 RB-7。
4. **Self-written record**：reviewer／adjudicator 以自己的 Write 工具把 record 寫到第 7 節的位置；派工者只能原樣 commit，不得改寫、刪減或決定是否記錄。Subagent transcript 內的 Write 呼叫即為作者證據。

Claude Code 的自動記憶（memory）不是權威紀錄：不得以它代替 re-ground，也不把 review、裁決或 Executor 的結論寫進自動記憶，以免被之後的 context 繼承。

以下一律只算 self-verification，不得記為正式 audit：Executor session 內的 fork 型 subagent 或 code-review 類 skill、未綁定 `gov-*` definition 的一般 agent、由 Executor 轉述的 review 結論。

## 4. Lane policy

| 工作 | 預設 lane |
| --- | --- |
| 實作、修正或文件，契約清楚，且能在一個 execution unit 內完成 | **Lightweight** |
| 需要分解成多個 execution units、管理其 dependencies，或需要跨多個 Executor／Reviewer session 協調完成（治理 §3.6-C）。MVP 的模組實作（`DESIGN.md` §9.1 的 Must 模組與 §9.2 的關鍵路徑）屬於這一類 | **Formal**（Spec＋Tickets＋Orchestrator） |
| 需要為產品行為、介面、資料契約、invariant 或 gate 建立其他工作將依賴的新設計基線（治理 §3.6-B） | **Formal** |
| 已結案工作之後的單點修正 | Lightweight，作為新的 work item；以 acceptor 的直接指示作為其 Outcome Contract |
| 通知、進度同步、文件維護等行政作業慣例 | Lightweight（治理 §3.6-B 的條件） |

- Lane 依預期的**整體**結果判定，不依本次增量；不得把需要 Formal 的工作拆成多個 Lightweight 指示來執行（治理 §3.3）。
- 模糊或有爭議的分類由 Design Authority 判定，並留 decision record。
- 預設分類不取代治理 §3.3 的 eligibility：Lightweight 工作中第一個需要對 intent、scope、acceptance、authority 作假設之處，就是 routing condition。
- Lightweight 不產生 Spec／Tickets，也不啟動 Orchestrator run（治理 §3.5；orch-default §1）；需要其他 authority 時，由 direct-execution session 依第 3.7 節派工。

## 5. Assurance policy

- **Formal**：每個 Ticket 的 independent audit 與每份 Spec 的 Spec Integration Audit 都必須執行（治理 §4.1、§4.7）。
- **單 Ticket fast path**（治理 §4.7）：**採用**。Spec 只有一張 Ticket 時，該 Ticket 的 R1 可同時滿足 Spec Integration Audit，條件是派工時就指定該 R1 兼作 Spec Integration Audit，且 record 逐項記載治理 §4.7 的五個範圍並明寫「本 record 同時是 Spec Integration Audit」。核對方式：Orchestrator 依 orch-default §6 逐項核對 record 是否載明五個範圍、subject 是否為最終整合 subject，缺任一項即另派。不得事後重新標示既有 R1 record。
- **Lightweight audit 預設**：不要求 independent audit。worklog 如實標示「完成且依 policy 未要求 independent audit」，不得寫成 audit PASS。
- **Lightweight audit 觸發條件**：acceptor 要求；變更涉及 Design Authority 確認的高風險類別；Design Authority 裁決要求。
- **高風險類別**：治理 §5.1 規定由 Design Authority 決定，以 decision record 承載（`docs/governance/records/decisions/`）。初始候選如下，第一次正式 audit 或 Formal activation 前由 Design Authority 確認或修改。本檔不以任何高風險類別作為 capability escalation trigger。
  - **H-1 憑證與機密**：API key 是否可能進入 git、log、文件、evidence 或前端可見的內容。
  - **H-2 私有騎乘資料**：GPX 與由它導出的位置資訊（含住家附近的座標）是否可能進入 git、log、文件、evidence、測試 fixture，或送往外部 API 的內容。
  - **H-3 實驗與宣稱的誠信**：保留行程的隔離；E1 Lite／E2 的結果是否為真實執行所得；未執行的檢查是否如實標為 NOT RUN 或 BLOCKED；產品與文件的用語是否超出證據（root `CLAUDE.md` 的用語規則）。
- **Integration／release gates**：release 指合併進 `main`（公開的預設分支）。合併由 acceptor 進行（RB-1）。合併前須具備：
  - Formal：全部 Ticket 依 orch-default §7 結案、每份 Spec 的 Spec Integration Audit 已 closure、Design Authority phase acceptance 已完成。
  - `.venv/Scripts/python.exe -m pytest -q` 全數通過，輸出記在 worklog 或 run record。
  - `README.md` 的安裝與執行步驟有變動時，已實際跑過，結果與證據記在 worklog。
  - 沒有追蹤中的機密或私有資料：`git ls-files` 不含 `.env`、`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/`；diff 內沒有金鑰字串。
- **Model diversity**（治理 §2.2 V22-11；Profile §5）：因 O-1，Executor、Primary Reviewer、Alternate Reviewer 預設同為 `claude-opus-5-5`，Profile §5 的 D1、D3 在本專案的拓樸下不成立；本檔不宣告任何 diversity 關係（D1–D4 皆記「未宣告」），所以不記 `diversity_lost`。Audit record 分兩欄記載：(a) context independence 四項 properties 的滿足方式；(b) Executor、Primary、Alternate 的實際 model（引用第 3.6 節證據），相同時記「無 model diversity」，不得主張 diversity。Diversity 不影響 independence 的判定；本專案沒有要求恢復 diversity 才能 audit 的類別。

## 6. Skills and runtime

- **Implementation HOW**：`impl-default` `v2`，overrides none。
- **Control-plane HOW**（只在 Formal）：`orch-default` `v2.2`，overrides none。並行度 1（逐張 Ticket 執行）。
- **Harness**：Claude Code（desktop app 或 CLI），Windows。派工用 Agent tool，角色 definition 在 `.claude/agents/gov-*.md`。新增或修改 definition 後要重開 session 才會載入，binding 驗證也必須在新 session 進行（Profile §6）。Session 要從本 repo 的根目錄啟動，definitions 才會載入。
- **工作 skills**：`/to-spec`、`/to-tickets`、Grill、`gh` CLI（見 `docs/agents/issue-tracker.md`）與其他已安裝的 skills 只提供 HOW，不因被呼叫而取得設計、接受或核准權（治理 §3.4）。
- **測試**：`.venv/Scripts/python.exe -m pytest -q`（設定在 `pyproject.toml`；環境建立方式見 `DESIGN.md` §10）。
- **Git**：依 `docs/conventions/git-commit-rules.md`；commit message 與 PR 描述不加 Claude 標記。
- **Recovery**：依 orch-default §8 與治理 §1.5，從第 7 節的紀錄 re-ground；對話 context 與自動記憶只是 cache。

## 7. Work records

```text
docs/
├── requirement/            # 上位契約（老師原文），唯讀
├── spec/                   # Spec（derived contract）
├── ticket/                 # Ticket 索引；Ticket 本體在 GitHub Issues
├── acceptance/             # 驗收對照（產出時才建立）
└── governance/
    ├── project-bindings.md
    ├── binding-verification.md
    ├── Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/   # PKG，位元複本
    └── records/
        ├── outcome-contract.md  # Outcome Contract 與 acceptor 接受紀錄
        ├── decisions/           # DA 的 derivation／decision records、FA 的 rulings
        ├── worklog/             # 每個 work item 一份
        ├── audit/               # Reviewer 自寫的 audit records
        └── run/                 # Orchestrator run records
```

| 紀錄 | 位置與命名 |
| --- | --- |
| Outcome Contract | `docs/governance/records/outcome-contract.md`；多份時加後綴。Lightweight 的直接指示原文記在 worklog |
| Spec | `docs/spec/`（沿用既有位置） |
| Ticket | GitHub Issues（`yotsubamomo/moto-touring-copilot`）；Issue 內引用所屬 Spec 與 worklog 路徑。`docs/ticket/` 只放索引 |
| Derivation record | `docs/governance/records/decisions/derivation-<spec>.md`（Spec 與其 Tickets 的 derivation 都記在這裡） |
| Decision record | `docs/governance/records/decisions/decision-<YYYYMMDD>-<slug>.md` |
| FA ruling | `docs/governance/records/decisions/ruling-<YYYYMMDD>-<slug>.md` |
| Worklog | Formal：`docs/governance/records/worklog/issue-<n>.md`；Lightweight：`docs/governance/records/worklog/<YYYYMMDD>-<slug>.md`。續接 session 更新同一份 |
| Audit record | Ticket：`docs/governance/records/audit/issue-<n>-c<cycle>-<r1\|r2\|alt>.md`；Spec Integration Audit：`docs/governance/records/audit/spec-<spec>-c<cycle>-<r1\|r2\|alt>.md`；Lightweight：`docs/governance/records/audit/<YYYYMMDD>-<slug>-c<cycle>-<r1\|r2\|alt>.md`（與其 worklog 同名） |
| Run record | `docs/governance/records/run/run-<YYYYMMDD>-<slug>.md` |
| Escalation／substitution record | 派工者的 worklog（Lightweight）或 run record（Formal）；review／adjudication 角色提出的 escalation 記在自己的 audit record 或 ruling（Profile §8） |

- 資料夾在真的產出該類紀錄時才建立。
- `docs/governance/records/**` 是 **record-only paths**：只改這些路徑的 delta 不影響受審 subject 的 identity（orch-default §7 P7）。
- 紀錄只放文件；實作、資料與測試留在既有位置。紀錄不得含憑證或私有資料（RB-3、RB-7）。

## 8. 採用時的處理

### 8.1 採用前的既有產出（治理 §5.3）

本專案在 m1 之前不適用治理。下列產出是在治理之外、由 acceptor 逐項裁決的流程中完成的，保持原樣，不重新審查、不改寫：

| 產出 | 狀態 |
| --- | --- |
| `DESIGN.md`（Agent-first MVP，Level 2 Lite） | acceptor 核准的 Scope Reduction 與 CR-01 方向已寫入 |
| G1（`docs/grill/g1-grill-input.md`） | APPROVED／FROZEN 2026-11-14 |
| G3（`prototype/index.html`、`docs/ui/`） | APPROVED／FROZEN 2026-11-15 |
| CR-01（`docs/cr/`） | 方向 APPROVED 2026-11-15；Review Disposition P-1～P-11 已裁決 |
| `docs/spec/SPEC-001-plan-schema.md`、`SPEC-RESOLUTION-001-sb2-sb8-sb9.md` | SPEC-001 未 Freeze；Spec Blockers 已關閉 SB-1、2、7、8、9，未關閉 SB-3、4、5、6、10 |
| GitHub Issues #7–#11（BATCH-1）、#12（UI-0） | OPEN，未開始；索引在 `docs/ticket/` |
| `src/`、`tests/`（Spike，100 個測試通過，只針對資料契約 v0.2） | Pre-Spec Spike |
| 技術檢查 C1 PASS、C2 FAIL、C3 BLOCKED／NOT RUN、C4 FAIL、C4b PASS | 紀錄在 `docs/cr/CR-01-appendix/` |

這些產出在治理下的地位：

- 它們是**輸入**，不是在治理下成立的 accepted contract。既有的 acceptor 裁決仍是 acceptor 的決定，寫 Outcome Contract 時引用，不重新詢問。
- m1 生效後開始的每個 work item 適用治理。Formal 實作開始前，須依治理 §3.4 具備：已接受的 Outcome Contract；Design Authority 的 derivation record，其中寫明引用哪些既有 Spec 段落與 Issues、它們是否 implementation-ready、boundary determination。既有的 Spec 與 Issues 可以被引用（治理 §3.4「reference to applicable effective Spec」），不必重寫；Design Authority 判定不足之處才修訂。
- 未關閉的 Spec Blockers 所涵蓋的範圍，在關閉前不是 implementation-ready，不得納入 Formal run 的 Tickets。

### 8.2 第一次正式 audit 或 Orchestrator activation 前

治理 §5.1：bindings 與 definitions 須在 Orchestrator activation 前、以及 Lightweight work item 第一次正式 audit 前就緒且可驗證。

| # | 項目 | 狀態 |
| --- | --- | --- |
| 1 | m1（本檔、`PKG/`、`gov-*` definitions、root `CLAUDE.md`）經 acceptor 接受並生效 | 完成（2026-11-17，commit `39e77ec`） |
| 2 | 從本 repo 根目錄開新的 Claude Code session，確認九個 `gov-*` definitions 已載入 | 完成（2026-11-17，session `6ccb50de-5234-4a2d-8637-7a94bc585260`：九個 definitions 都在該 session 的可用 agent 清單，dry-run 觀測到的 `agentType` 涵蓋全部九個） |
| 3 | Binding dry-run：對九個 `gov-*` definition 各派一次不做事的任務；另以 per-dispatch 參數各派一次，核對 alias 的實際 model：`model: fable`、`gov-investigator`＋`model: opus`（E-IN）、`gov-bounded-worker`＋`model: haiku`（Haiku qualification probe）。以第 3.6 節指令核對，結果記在 [`binding-verification.md`](binding-verification.md) | 完成（2026-11-17）：12 列中 11 列符合 m1；第 10 列觀測為 `claude-fable-5-2`，acceptor 決定改為 Fable 5.2（O-4，m2）。Fable 路徑在 m2 生效後才可使用。Haiku qualification probe 通過 |
| 4 | 高風險類別由 Design Authority 確認（第 5 節 H-1～H-3） | 未完成 |
| 5 | Outcome Contract 有 acceptor 接受紀錄（第 2.3 節） | 未完成 |
| 6 | Design Authority 的 derivation record（第 8.1 節） | 未完成 |

## 9. 變更紀錄

| 版本 | 日期 | 變更 | 依據 | 授權 |
| --- | --- | --- | --- | --- |
| m1 | 2026-11-17 | 初版：整個 repo 採用 Minimal Governance — Reusable Package v2.2，沒有 governance flag。由 `aiot-classwork` Bindings b5 移植：第 1 節 package 與版本相同；第 3 節角色、模型、overrides（O-1、O-2、O-3）、escalation 與 dispatch 機制相同，只改了檔案路徑、Haiku qualification 改為在本專案重新觀測、reviewer 的 autonomous access 排除 `data/`。依本專案改寫：第 0 節適用範圍；第 2.2 節上位契約與最終判準；第 2.4 節範圍邊界；第 2.5 節只保留本機 commit 的 SA-1，未移植 push、SA-2、SA-3；第 2.6 節 RB-1 擴及 push 與 PR、RB-3 只允許本機 `.env`、RB-4 記載 API 額度、RB-5 改為上位契約＋治理檔案＋已凍結基線、新增 RB-7 私有騎乘資料；第 5 節高風險類別候選 H-1～H-3、release gates 改為 pytest 與私有資料檢查，移除 Vercel 與 GitHub Pages 的內容；第 7 節紀錄位置改為 `docs/governance/records/`；第 8 節採用前產出的處理。 | acceptor 2026-11-17 指示（原文）：「我們要把治理原則從這邊搬到新專案去，然後原本這邊是只用在homework ，在final project 的話就是不設限。」 | **已接受並生效（2026-11-17）。** acceptor 在對話中針對 commit `39e77ec` 回覆原文「接受 39e77ec」；該 commit 含本檔 m1、`PKG/`、九個 `gov-*` definitions、root `CLAUDE.md` 與 `AGENTS.md`。本列與檔首、第 8.2 節 #1 的狀態更新是在接受之後由無角色 session 依 acceptor 指示轉錄的，沒有改動任何規則內容。接受前的內容確認：起草時所作的選擇（未移植 push、SA-2、SA-3；RB-7；H-1～H-3 候選；Fable alias 以 dry-run 觀測為準；Codex 未宣告）於 2026-11-17 向 acceptor 逐項列出，acceptor 回覆原文「照草稿」；第 2.2 節的版控決定（講義 PDF 與架構圖不進版控）同日另行決定，已含在 `39e77ec`。m1 不適用生效前已完成的產出（第 8.1 節）；生效時沒有進行中的 work item。 |
| m2 | 2026-11-17 | 新增 O-4：Profile 所列的 Fable 5.1 改為 Fable 5.2（`claude-fable-5-2`），effort 不變；改寫第 3.1 節 fallback 表的 F-DA、F-DA\*、R-PR、F-AR\*、F-FA、F-FA\* 列、「Fable alias」段，以及第 3.2 節的 E-DA、E-AR、E-FA 列；第 1、3.1 節的 overrides 清單加入 O-4；檔首改為 m2。其他規則不變。同時轉錄第 8.2 節 #2、#3 的狀態（紀錄，不是規則變更）。 | 第 8.2 節 #3 的 binding dry-run（2026-11-17，`binding-verification.md` 第 10 列）觀測到 `model: fable` 解析為 `claude-fable-5-2`；第 3.1 節「Fable alias」規定此時由 acceptor 決定。 | acceptor 2026-11-17 在對話中的決定（原文）：「gov-alternate-reviewer＋model: fable ，改為Fable 5.2」。本列由無角色 session 依該指示轉錄。**m2 尚未生效**：依檔首生效條件，須 acceptor 針對含 m2 的 commit SHA 明確接受（或合併引入 m2 的 PR）。 |
