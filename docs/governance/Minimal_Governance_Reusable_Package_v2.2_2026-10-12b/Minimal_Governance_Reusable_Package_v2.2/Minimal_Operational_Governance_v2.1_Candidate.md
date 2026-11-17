# Minimal Operational Governance — v2.1

**狀態：Adopted／Frozen（2026-10-01，operator 明確授權）**  
**版本：v2.1**（全名一律寫「Minimal Operational Governance v2.1」，與歷史「Model-Agnostic Development Governance 新專案開工標準 v2」無關）  
**Drafted：2026-10-01 · Adopted／Frozen：2026-10-01**  
**適用範圍：Lightweight 與 Formal／SDD execution**

**基線／設計依據：** v2.0 frozen baseline 與 v2.0 → v2.1 的變更見 Appendix C；v1.0 baseline 與 v2.0 design provenance 見 Appendix B.0。

**本檔採用後為 authoritative source。** 對應的 visualization 是加日期的 non-normative HTML（最新：[minimal_governance_map_v2.1_zh-TW_2026-10-02.html](minimal_governance_map_v2.1_zh-TW_2026-10-02.html)；較早日期的檔案保留為快照）；日後新版 HTML 一律在檔名加日期，與本檔不一致時以本檔為準。

**Reusable package references（non-normative）：** [Reference Model Profile default v2.4](references/model-profiles/default-v2.4.md)（Adopted／Frozen 2026-10-02；[default v2.3](references/model-profiles/default-v2.3.md) 保留為 frozen baseline）· [Implementation Profile impl-default v2](references/implementation-profiles/default-v2.md)（Adopted／Frozen 2026-09-22）· [Reference Orchestrator Contract orch-default v2.1](references/orchestrator-contracts/default-v2.1.md)（Adopted／Frozen 2026-10-01，與本檔同步採用）。三者分別提供可替換的 role／model mapping defaults 與 deterministic replacement policies、可重用的 implementation HOW、可重用的 control-plane HOW；由 Project Bindings 依第 5.1 節選用／採用，皆從屬於本治理，不修改任何 authority 或 normative semantics。較早版本的 profiles 與 contracts 保留為 frozen baseline。本段為 metadata：reference 版本更替時只更新本段（2026-10-02：default v2.3 → v2.4，operator 明確授權），不構成本治理的版本變更，第 1 節起的 normative 本文 byte-identical；Project Bindings 仍直接 pin 各 reference 的版本（第 5.1 節）。

> **Human approves the outcome contract once; authorized Agents autonomously design, decompose, implement, review, correct and complete within that boundary.**

人類 acceptor 一次接受並授權 Outcome Contract（第 1.2 節）。之後正常的 Spec／Ticket derivation、implementation、technical clarification／question routing、verification、review／independent audit、findings、rework／re-verification、Alternate Review／Final Adjudication、Spec Integration Audit 及 phase progression／completion，MUST 由具有相應 authority 的 AI Agents 自主執行、裁決、留下 durable records 並繼續。Operator interaction 是第 1.5 節的 exceptional boundary，不是正常 workflow gate。

本治理定義工作所需的 authority、contract、verification、assurance、traceability 與 recovery，不假設所有工作都必須經過 Spec-Driven Development（SDD）。

> **Use the lightest workflow that preserves sufficient contract clarity, authority, traceability, verification and assurance.**

本稿經明確採用後，與 Project Bindings 構成獨立有效的治理契約。Minimal v2.0、v1.0 及更早版本、v2 母版僅供歷史參考，不補充本稿未定義的義務；已採用 v2.0 或 v1.0 的專案在依第 5.3 節明確改採本版前，仍以其採用的版本為 frozen baseline。

**規範用語：**

- **MUST／MUST NOT**：必要要求，不得由 Skill、Runtime 或 Project Binding 豁免。
- **SHOULD／SHOULD NOT**：預設遵守；偏離須記錄理由，且不得違反 MUST。
- **MAY**：可選做法。

---

## 1. Governing Principles & Autonomous Execution

### 1.1 Five common invariants

以下五項適用於所有 execution paths；其完整規範以所引條文為唯一 authoritative definition：

1. **Autonomous orchestration** — 第 1.4、1.5、3.8 節。
2. **Explicit roles and verifiable bindings** — 第 2.1–2.3 節。
3. **Independent audit integrity** — 第 2.3、4.1–4.7 節。
4. **Agent-autonomous decisions** — 第 1.3、2.4 節。
5. **Mandatory durable worklog** — 第 3.7 節。

### 1.2 Accepted Work Contract

**Accepted Work Contract** 是本治理的第一級 abstraction：由適當 authority source 接受，足以界定預期工作、邊界與完成條件，並具有穩定引用的工作契約。

契約的成立依據是第 3.1 節的 properties，不是文件形式。Prompt、Task Brief、Jira description、Spec／Tickets，以及引用既有 accepted decisions 的工作要求，均可承載契約。

Work Contract MUST 有可持久引用的內容或版本；若原始來源可變，MUST 保存足以辨識當次 accepted scope 的內容或快照。

**接受工作要求、授權執行、確認設計語義，是三種不同權限。** 同一有效指令可以一併完成接受與授權，但不得由 Agent 推定超出該指令及既有 authority 的效果。接受與授權屬於 Project Bindings 宣告的人類 acceptor（operator 或其明確指定的人類代理），亦可由其已記錄的 standing authorization 涵蓋；設計語義屬於 Design Authority。任一角色處理另一種權限的問題時，只能 route，不能代行。

**Outcome Contract 與 derived contracts。** 由人類 acceptor 接受並授權的 Work Contract 稱 **Outcome Contract**：一次確認 goal、scope、constraints 與 acceptance boundary，並授權具相應 authority 的 Agents 在此邊界內規劃、分解、實作、審查、修正至完成。Lightweight 下，被接受的 prompt、brief 或 Jira item 即為 Outcome Contract。Formal 下，Spec 與 Tickets 是 Design Authority 在 Outcome Contract 內產生的 **derived contracts**：其接受與授權來自 Outcome Contract，不來自 Design Authority；每份 derived contract MUST 可追溯至其 Outcome Contract 條款，並附 Design Authority 的 **derivation record**（依據、boundary determination、該 Spec 所分配的 Outcome Contract acceptance boundary 部分、受影響工作）。Derived contract 的成立不需 acceptor 逐份核准。

本治理所稱 **accepted 語義**，專指 acceptor 接受的 Outcome Contract 之 intent、scope、constraints 與 acceptance semantics；derived contract 的內容是 Design Authority 的設計，其變更依第 5.3 節區分。本治理所稱 **accepted Work Contract／accepted contract**，涵蓋 Outcome Contract 及其有效 derived contracts；finding、gate 與 completion 所對照的契約條款包含 derived contract 的 AC、invariant 與 gate。

**Re-authorization 與 boundary。** 只有下列情況 MUST 重新取得 acceptor 的接受／授權：預期結果超出 Outcome Contract 的 scope 或 constraints；改變 accepted 語義；Project Bindings 依第 5.2 節列為 reserved boundary 的動作。Executor 或 Reviewer 對 boundary 的疑義 MUST 先依第 2.4 節 route 至 Design Authority；Design Authority MUST 以 derivation record 確立所提 derived contract 或變更是否仍在 Outcome Contract boundary 內。**Design Authority 無法確立其在 boundary 內時，受影響路徑 MUST fail-closed：route 至 acceptor，只停止該路徑（第 1.5 節）。** Design Authority 不因此取得接受或授權權限。獨立 Reviewer（含第 4.7 節 Spec Integration Audit）提出 boundary 符合性 finding 時，Design Authority MUST 先評估該 finding；Design Authority 確立所涉 derived contract／變更在已接受的 Outcome Contract boundary 內，且 Reviewer 在其 record 中撤回或關閉該 finding 者，正常繼續。Design Authority 作出 determination 後該 boundary finding 仍有爭議者，該 boundary 對執行與 closure 而言視為未確立：即屬 Design Authority 無法確立其安全在已接受 boundary 內，受影響路徑依本段 fail-closed 至 acceptor。Final Adjudicator MAY 裁決相關 routing／process 爭議，但 MUST NOT 代 acceptor dismiss 或裁決該 Outcome Contract boundary 問題本身。本段限於 boundary 爭議；boundary determination 仍屬 Design Authority，Reviewer 仍只擁有 findings／blocking，Final Adjudicator 不因此取得實質 boundary authority，acceptor 保有 Outcome Contract scope／授權權限，本段不使 Reviewer 取得覆寫 Design Authority 其他設計決定的一般權限。

Agents MUST NOT 自行發起 Outcome Contract；derived contracts 依本節在已接受的 Outcome Contract 內產生，不屬自行發起。Follow-up、deferred disposition 與 non-blocking finding 所產生的後續事項，在 acceptor 接受並授權前，只是 tracked items，不得作為新工作執行。

已明確涵蓋於有效 standing authorization 的工作可依該授權執行，不需重複請求；契約內必要的 rework／re-verification 不是新工作接受 gate。

有效治理、accepted contracts、授權、裁決及必要證據 MUST 有可持久保存、可識別的權威紀錄。

### 1.3 Authority separation

各角色的 responsibility、authority 與 prohibited authority 以第 2.1 節角色表為唯一權威定義；問題的 substantive decision owner 與 routing 以第 2.4 節為準。

- Model replacement、lane selection 或 promotion MUST NOT 改變角色權限。

**Strong contract, loose execution。** 契約須清楚，實作方法由 Executor 自主選擇。

### 1.4 Autonomous continuation

Orchestrator 啟動後，下列事項本身 MUST NOT 成為等待 operator 的理由：

- Work item／Ticket 完成或 phase boundary。
- 需要新的 Executor／Reviewer session 或 agent replacement。
- Findings、implementation rework 或 audit escalation。
- Design Authority decision、Final Adjudication 或 phase adjudication。
- Context／session rollover。
- Promotion 所需的授權內設計與規劃工作。

正常模式 MUST 為：

```text
problem
→ identify required authority
→ dispatch responsible Agent
→ receive traceable decision or ruling
→ continue authorized execution
```

> **Need for judgement is not a stop condition. It is a routing condition.**

Lightweight direct execution 不要求先啟動完整 Orchestrator run。直接執行 session 仍 MUST 遵守 authority routing：自行處理 Executor authority 內的事項；需要其他 authority 時，透過配置的角色派工機制或交由 Orchestrator routing，不得自行兼任未授權的決定者。

涉及 independent review／adjudication 的派工，MUST 遵守第 2.3 節。

### 1.5 Legitimate boundaries and recovery limits

只有以下情況可請求 operator 並停止受影響路徑。本清單是 non-delegable acts 的唯一權威清單，第 3.4、5.2 節引用之，不另行定義：

1. Outcome Contract 的接受與授權本身（第 1.2 節）。
2. 依第 1.2 節需要 re-authorization 的 boundary 變更，包括 Design Authority 無法確立在 boundary 內而 fail-closed 的路徑。
3. Project Bindings 依第 5.2 節明確列舉的 reserved boundaries。
4. 必要外部權限、能力、資源或證據無法由現有授權內的 Agent／工具取得，且無合法替代。

工具失敗、context 問題或 Agent 不可用 MUST 先走已授權的 recovery／replacement 路徑。

**Recovery 何時成為 boundary。** 狀態、authority 或證據不可靠時，MUST 暫停受影響的變更，先核對與恢復；不得為了保持進度而猜測。恢復義務在條件持續期間持續存在，並在每個可用的 checkpoint 重新嘗試；不以次數或門檻計算。只有在 **完成以下三項之後，繼續執行仍屬 unsafe 或 indeterminate** 時，該路徑才可停止並轉交 operator：

1. 從權威紀錄（contract、worklog、產物、裁決、原始 evidence）重新 re-ground；
2. 依 Project Bindings 的 replacement policy 完成已授權的替代或修復；
3. 適用的 authority routing（Design Authority／Final Adjudicator）已作出裁決或確認無法裁決。

進行中 assignment 的結果無法確認、且該 assignment 可能已產生不可逆副作用時，該路徑即為 unsafe；其他不受影響的路徑不因此停止。

停止紀錄 MUST 說明現況、缺少事項、已嘗試的 re-ground／replacement／routing 及其結果、所需 authority 與下一步。無關且不會預判或影響該決定的工作 SHOULD 繼續。

Run-to-completion 不授權弱化 gate、捏造 evidence、隱性縮減 scope，或跨越保留權限。

---

## 2. Agent / Subagent Definitions & Model Mapping Profiles

### 2.1 Required roles

每個實際使用的治理 Agent 或 reusable Subagent MUST 有明確 definition，至少包含 responsibility／intended use、authority、prohibited authority，以及適用的 context／independence requirement。Definition 定義穩定權責；model assignment 由第 2.2 節的 Profile 提供，不以模型名稱定義權限。

以下六個 governance roles MUST 保留。Reusable Subagents 依其 definition 在委派範圍內工作，不構成新增 governance role，也不因 reusable 或更換 model 取得新的 authority。

Definitions 可重用，不要求每個 work item 重建。下表的 identifier 由 Model Mapping Profile 對應至實際 assignment；definition 的檔名、目錄、frontmatter、載入與 spawn 方法屬 Runtime／Harness HOW。

| Agent | Responsibility／authority | Prohibited authority | Profile identifier | Independence requirement |
|---|---|---|---|---|
| **Design Authority** | 釐清 Work Contract 語義、判斷設計語義、lane eligibility／promotion、在 Outcome Contract 內 derive Formal Spec／Tickets 並作 boundary determination（第 1.2 節）、規劃、phase acceptance。 | 不得豁免必要 audit；不得代行 acceptor 的接受與授權，或明確保留的 operator 核准；不得在無法確立 boundary 時自行放行。 | `design_authority` | 依原始 contract、證據與有效授權判斷，不將 Executor／Reviewer 結論當作既定設計。 |
| **Executor** | 執行 accepted work、自主選擇 HOW、self-verification、targeted correction、維護 worklog。 | 不得自行改 requirement／AC／invariant、豁免 gate，或裁決自己的 review dispute。 | `executor` | 正式 review context MUST 與執行 context 獨立。**同一執行 context 不得轉名成 Reviewer。** |
| **Primary Independent Reviewer** | 執行 R1／R2，自主判定 findings、blocking、evidence 與 closure。 | 不得修改 implementation、tests、contract 或 gates；不得作 design decision；不得 promote。 | `primary_reviewer` | R1 使用獨立於 Executor 的 context；R2 MAY 延續自己的 R1 context，但 MUST 重讀修正後證據。 |
| **Alternate Independent Reviewer** | 獨立評估 R2 後剩餘 blocking 與爭議。 | 不得修改受審物、重新設計或自行作 Final Adjudication。 | `alternate_reviewer` | MUST 使用 fresh context，不繼承 Executor 或 Primary Reviewer 的對話；可讀其正式 records 與 evidence。 |
| **Final Adjudicator** | 裁決 review dispute、合法 disposition、targeted rework、cycle reset 與 authority routing 爭議。 | 不得虛報 gate PASS、覆寫原 review，或取得 Design Authority／acceptor／operator 保留權限。 | `final_adjudicator` | MUST 使用獨立裁決 context，依契約、原始 findings 與證據判斷。 |
| **Orchestrator** | 管理 state、dependencies、dispatch、routing、gates、continuation、recovery 與 completion reporting。 | 不得實作產品變更、決定設計語義、降級 finding 或裁決 evidence sufficiency。控制面操作不在此限。 | `orchestrator` | 維持 control-plane context；implementation 與 review 由相應角色執行。 |

Design Authority 與 Final Adjudicator MAY 使用同一 model，但所行使的 authority MUST 可區別。

六角色必須可被配置及使用，不代表每項工作都要呼叫六角色。

### 2.2 Model Mapping Profiles and verifiable assignment

每個實際可 dispatch 的 Agent／Subagent MUST 在採用的 Model Mapping Profile 中有明確 mapping，包括：

- Agent／Subagent identifier，對應已存在的 definition。
- Model。
- Model version 或 resolution policy。
- Effort／mode（若該平台與角色需要）。
- Replacement policy。
- Binding verification mechanism 及證據位置。

Profile MAY 共用預設或引用既有設定，但每個可 dispatch identifier 的有效 mapping MUST 明確可解析。Project Bindings MUST 指定採用的 Profile 及 mapping 變更 authority；不強制另建 Profile 檔案或 schema。

Governance MAY 附版本化 Reference Model Profiles；新專案 MAY 直接採用某個 Profile＋version，例如 [default v2](references/model-profiles/default-v2.md)。Project Bindings MUST 記錄採用的 Profile、版本與 overrides（無則明記無）；Profile 更新不自動影響既有專案。Profile 不改變任何 role authority 或 independence requirement，採用後的有效 mapping 仍須符合本節與第 5.1 節；Reference 中的 `TBD` 不構成有效設定。

實際 assignment 分兩種，核對的內容不同。

**被派工的 assignment。** 除下述兩種 root role session 外，每個實際 assignment——治理 Agent 與 reusable Subagent，不論由 operator、Orchestrator、direct-execution session 或 Harness 機制派工——MUST 透過可驗證機制綁定至宣告的 definition、model 及適用 effort／mode。

**Root role session。** 直接擔任治理角色、而不是被派工產生的 session。本治理只承認兩種：Orchestrator，以及 Lightweight direct execution 中擔任 Executor 的 session；其他直接擔任治理角色的 session 依前段為被派工的 assignment。Root role session MUST 具備：

1. **Activation basis。** Orchestrator：由 acceptor／operator 指定（designation），或由同一 run 中已啟動的 Orchestrator 依 rollover 交接的 successor 繼承該 designation 與 run identity；Orchestrator 不得自行假定。Direct-execution Executor：已成立的 Outcome Contract 接受與執行授權（第 1.2、3.5 節），並依其 assurance path 以 Lightweight lane 執行（第 3.1 節第 6 項、第 3.3 節）。Activation basis MUST 有可持久引用的紀錄。
2. **Model／effort runtime verification。** 該 session 實際的 model／version 與適用 effort／mode 等於其角色 identifier（`orchestrator`／`executor`）的有效 mapping，並可由 Runtime／Harness 證據核對。Orchestrator 在本項核對成立前不得派工。
3. **Role-definition grounding。** 以該角色的 definition（第 2.1 節）與適用契約為行事依據；re-ground 或 successor 接手時重新取得。
4. **Work identity and records。** Orchestrator：run identity（未啟動 run 時，為其 routing／派工所服務的 work item identity）與授權紀錄（第 3.4、5.1 節）。Direct-execution Executor：work item identity、第 3.7 節的 worklog 及其他適用的治理紀錄。

Root role session 如何建立——由 definition instantiate、一般 session 經 activation，或其他機制——屬 Runtime／Harness HOW；由 definition instantiate 不是必要條件。Project Bindings MAY 指定所採機制及其證據。第 3 項不證明第 2 項：讀取或載入 definition 不構成 model／effort 的核對。Root role session 派出的每個治理 Agent 與 reusable Subagent 都是被派工的 assignment。

Prompt 中自稱角色、model 或「已綁定」，不構成 binding 證據；僅有設定存在也不等於實際 assignment 已符合。Designation 與 Outcome Contract 的接受／授權是 acceptor／operator 的 authority 行為，不是自稱。Designation 不構成 Outcome Contract 的接受或授權；兩者決定哪個 session 擔任該角色，不證明其 model／effort，也不授予第 2.1 節以外的權限。Runtime／Harness 或等效可觀察執行證據 MUST 足以核對實際 assignment，並可由工作或 audit records 引用。

無法核對或不符的 binding MUST 修復或依授權替代；不得將該 assignment 冒充符合要求的 execution、review、adjudication 或 orchestration。

因不可用或執行失敗採取 replacement／substitution 時，MUST 引用當次嘗試的錯誤或當下可用性檢查證據，不得只憑記憶、先前 session／run 的不可用狀態跳過指定 Agent／model。主動更新 Profile 的依據與授權依第 5.3 節記錄。

替換 Profile 或 model 不改 definition 的 authority、independence、acceptance 或 audit bounds。Executor 與 Reviewer 是否使用不同 model，是採用的 Model Mapping Profile／Project Bindings 的 assurance policy 預設，不是第 2.3 節的 independence property；不同 model 不自動構成 independent review。依本節替代 model 時 MUST 維持第 2.3 節四項 properties，MAY 改變 model diversity 並記錄。

### 2.3 Independent dispatch boundary

正式 independent review／adjudication 的 independence 由以下四項 properties 定義，四項 MUST 同時成立：

1. **Independent context。** R1、Alternate Review 與 Final Adjudication 使用 fresh context，不繼承 Executor 的對話、推理或結論；可讀其正式 records、產物與 evidence，並視其結論為待驗證主張。R2 依第 2.1 節 MAY 延續 Reviewer 自己的 R1 context，但不得繼承 Executor context，且 MUST 重讀修正後證據。
2. **Verifiable binding。** Assignment 依第 2.2 節綁定至宣告的角色與 model，且有證據可核對。
3. **Autonomous access。** Reviewer MUST 能自主取得受審產物與原始材料，不受限於 Executor 挑選或摘要的輸入。
4. **Self-written record。** Reviewer 的 findings／verdict 及 Final Adjudicator 的裁決由各自角色寫入自身 record；Executor 不得代寫、改寫、篩選或決定是否記錄。Closure 以有效原始 record 為依據，不以 Executor 對 review／裁決結果的敘述為依據。

滿足四項 properties 的派工來源可以是 operator、Orchestrator，或 **Project Bindings 宣告的可驗證 Harness 機制**。Bindings 宣告的機制若能保證上述四項，由 direct execution session 透過該機制發起的派工亦屬合法 independent dispatch；Bindings MUST 明示該機制如何滿足四項。

以下一律屬於 **self-verification**，不得記錄為正式 audit，也不得滿足 independent audit gate：

- Executor session 內繼承其 context 的 sub-agent review，包括 code-review 類 Skill 產生者。
- 對通用 agent 的 ad-hoc「請審查」指令，未經第 2.2 節綁定。
- 由 Executor 轉述或整理的 review 結論。

Harness 無法提供滿足四項 properties 的機制時，Lightweight 的正式 audit MUST 由 operator 或 Orchestrator 派工；這是 Bindings 層的一次宣告，不是每項工作的個別決定。

此邊界不要求新增 approval stage。

### 2.4 Routing responsibility

| 問題 | 決定者 |
|---|---|
| 契約內 HOW、一般實作選擇 | Executor |
| Findings、blocking、review evidence sufficiency | Reviewer |
| Contract 語義是否足夠、material ambiguity、設計與 promotion 判斷、derived contract 的 derivation 與 boundary determination | Design Authority |
| Outcome Contract 的接受、執行授權、boundary re-authorization、authority／authorization 缺口 | Acceptor（Project Bindings 宣告；預設為 operator 或其人類代理） |
| Review dispute、合法 accepted disposition、authority routing 爭議 | Final Adjudicator |
| 依既定條件派工、推進、啟動 promotion 流程 | Orchestrator |

Lane policy 提供預設分類，但不得取代第 3.3 節的 contract-assumption boundary。需要補充契約語義或判斷適用性時，MUST route 至 Design Authority；需要補充接受或授權時，MUST route 至 acceptor。

Design Authority 的 contract-sufficiency authority 依第 1.2、2.1 節；不得因此取得接受或授權權限。

Executor 或 Reviewer 提出問題時 SHOULD 指明所需 authority 與理由。Orchestrator MUST 依下表決定派工並記錄所適用的情況；在任何情況下 MUST NOT 判斷設計語義、finding severity 或 evidence sufficiency，MUST NOT 重新分類 finding，也 MUST NOT 默默覆寫任一來源：

| 情況 | Orchestrator 動作 |
|---|---|
| 已指明 authority，且與本節規則一致 | 直接派工 |
| 未指明，但依事件的來源與種類本節規則能唯一決定 | 直接派工，記錄所用規則 |
| 已指明，但與本節規則衝突 | 屬 routing 爭議：交 Final Adjudicator 釐清 routing |
| Authority 真正模糊：兩個角色主張不同 authority，或被派工角色以非其 authority 為由退回 | 交 Final Adjudicator 釐清 routing |
| 屬契約語義或 sufficiency 的分類，無法以規則機械判定 | Route 至 Design Authority（DA-first）；Design Authority 依本節把接受／授權缺口再 route 至 acceptor，不因此取得該權限 |

缺少 routing label 本身不是爭議，不觸發 Final Adjudication。Final Adjudicator 釐清 routing 時 **不因此取得該問題的實質決定權**。

---

## 3. Development Flow, Work Contracts & Mandatory Worklog

### 3.1 Minimum Work Contract properties

Lightweight 與 Formal Work Contract 都 MUST 足以確認：

1. **Intent and outcome**：要解決什麼問題，預期產出或行為為何。
2. **Scope and boundaries**：可變更範圍、重要 non-scope 與適用限制。
3. **Acceptance and verification**：對每條需要 verification 的 AC，Work Contract MUST 定義或引用可觀察的 PASS／FAIL 語義與充分證據要求。對 Outcome Contract，acceptance boundary MUST 可觀察到足以判定每份 derived Spec 的 AC 是否涵蓋其 derivation record 所分配的部分，以及全部 derived Specs 合起來是否涵蓋它；Spec 的具體 AC 由 Design Authority 在該 boundary 內 derive。Tickets、Executors 與下游 Skills MUST NOT 自行重新定義；需變更時依相應 authority 及第 5.3 節處理。具體 test cases、frameworks 與 fixtures 屬 HOW。
4. **Authority and authorization**：誰接受此要求、允許哪些執行與決定。對 Outcome Contract，授權 MUST 明示涵蓋規劃、分解、實作、審查、修正至完成，或明示依第 5.2 節保留的動作。
5. **Relevant context**：必要依賴、適用既有契約與已知風險。
6. **Assurance path**：採用何種 lane，以及依第 4.1 節確定的 audit 與其他 gate 要求。
7. **Stable reference**：可識別、可持久追溯的 accepted 內容或版本。

這些 properties 可以由短 prompt、既有 accepted decisions 與專案預設共同滿足，不要求每項各設欄位，也不要求新增文件。

未明示的例行 implementation detail 可由 Executor 決定。契約 properties 的缺口不得以 implementation choice 名義補齊。

### 3.2 Grill

Grill 是可選的契約釐清 methodology；方法說明見 Appendix A.4。

**Grill 不創造 authority。** 其發現須由相應角色依第 2.4 節裁決；不得把詢問與討論本身當成接受、授權或核准。

### 3.3 Lightweight eligibility

**Lightweight 成立的條件，是 Executor 能在不對第 3.1 節 properties 1–4——intent、scope、acceptance、authority——作出任何假設的前提下完成工作。**

第一個必須作出的此類假設，即為 **routing condition**，不是可自行採用的 default：

- 缺口屬於 **語義**（scope 的邊界、acceptance 的判準、intent 的合理解讀）→ MUST route 至 Design Authority，依第 3.6 節處理。
- 缺口屬於 **接受或授權**（是否真的要做、property 4 未明）→ MUST route 至 acceptor。在 Orchestrator run 內，這是第 1.5 節的合法 boundary，只停止受影響路徑；在 direct execution 中，這是與 acceptor 的正常 Grill。
- 缺口屬於 **boundary**（是否允許動到某範圍、所提變更是否仍在 Outcome Contract 內）→ 依第 1.2 節先 route 至 Design Authority 作 boundary determination；Design Authority 無法確立在 boundary 內時，fail-closed 至 acceptor。

Lane policy 提供預設分類；上述 invariant 處理未被 policy 明確涵蓋的情況。Acceptor 的直接指令可以同時構成接受與授權，但不能替 Executor 填補語義缺口。

**Lane eligibility MUST 依預期的整體結果判定，不依本次增量判定。** 不得把需要 Formal 管理的整體工作拆成多個 Lightweight prompts，以避開適用要求；累積 scope 與 remaining work MUST 可由 worklog 追溯。

凡結果會改變 accepted 語義（第 1.2 節），或改變其他工作所依賴的設計基線——即產品／系統行為、介面、invariant 或 gate，不含符合第 3.6 節 B 所述條件的行政作業慣例——者，**不是 Lightweight work item**；它依第 5.3 節處理。

Audit applicability 依第 4.1 節判定。

### 3.4 Formal／SDD path

```text
Work request / Grill when needed
→ Outcome Contract：acceptor 一次接受＋授權（goal／scope／constraints／acceptance boundary）
→ Design Authority：Spec derivation（derivation record）or reference to applicable effective Spec
→ Design Authority：Ticket derivation
→ Start Orchestrator
→ [per Ticket] Implementation → Self-verification + applicable gates → Audit under Section 4 → Close / Rework / Route
→ [per Spec] all Tickets closed → Spec Integration Audit（Section 4.7）→ Design Authority phase acceptance
→ continue to run completion
```

Formal lane 一律包含 **Spec＋Tickets＋Orchestrator**。即使只有一張 Ticket，也不另設 Formal-lite 或第三條 lane。

Formal execution MUST 具備：

- 有效且涵蓋預期 scope 的 Outcome Contract 接受與授權（第 1.2 節）；Project Bindings 依第 5.2 節保留 implementation authorization 時，另有該授權紀錄。
- 由 Design Authority 在 Outcome Contract 內 derive、可識別版本且 implementation-ready 的 Spec／Tickets，附 derivation record。
- 明確 dependencies、AC、invariants 與充分證據要求。
- Orchestrator run-to-completion。
- 適用整合驗證、第 4.7 節 Spec Integration Audit 與 Design Authority phase acceptance。

**Parent Spec 若仍將必要設計留待下游決定，不得單憑 parent 已成立就視為 implementation-ready。**

Tickets MUST 引用或衍生自有效 Spec 的 verification contract，不得自行重新定義 AC 的 PASS／FAIL 語義或充分證據要求；Executor 不得藉選擇測試方法改變該契約。

**Spec／Ticket 的變更依第 5.3 節；reserved boundaries 依第 5.2 節。** 本節不另行定義變更分類或核准邊界。

`to-spec`、`to-ticket`、Matt implementation 與其他 Skills 屬 HOW。它們 MUST 保留 accepted contract 的語義，不得因被呼叫而取得設計、接受或核准權。

### 3.5 Lightweight path

```text
Accepted Work Contract
→ Direct execution
→ Self-verification + applicable gates
→ Audit applicability and flow under Section 4
→ Close / Rework / Escalate
```

Lightweight 可直接使用足夠明確的 prompt、brief、Jira description，或其引用的 accepted decisions，不要求產生 Spec／Tickets。

Executor MUST 在有效 execution authorization 內工作，完成 self-verification 與適用 gates，並維護第 3.7 節的 worklog。

**兩條 lane 的共同 self-verification 義務。** Executor MUST 驗證適用的正常與失敗行為，以及變更引入的實質風險，不得只證明 acceptance tests 通過。Failure-surface checklist 與具體測試方法屬 Skills／HOW。

直接而明確的使用者指令 MAY 同時構成工作接受及執行授權，但僅限指令與既有 authority 實際涵蓋的範圍。Lightweight 不授權修改上位 accepted contract；相關變更依第 5.3 節處理。

### 3.6 Design Authority assessment and promotion

Material ambiguity、未預期 scope growth、設計問題或 assurance 爭議 MUST route 至 Design Authority。以下情況 MUST 直接 route，不必耗盡 R1／R2：

- Contract 存在兩種或以上會影響實作的合理解讀。
- 實作必須猜測尚未確定的 measurement／lifecycle／identity／ownership 語義。
- 修正 finding 需要改變 invariant。
- Reviewer disagreement 實質上是 architecture／requirement decision。

需要判斷，不等於自動需要 SDD；接受與授權缺口仍依第 2.4 節交 acceptor，不由 Design Authority 代行。

**只有 Design Authority、適用的 Project Binding 或有效裁決可以 promote。** Reviewer 或 Final Adjudicator 認為契約不足時，只能 route 至 Design Authority；Reviewer session 的存在、finding 的數量或「缺少 Spec」本身，都不構成 promotion。

Design Authority MUST 區分以下需求：

#### A. 可在不改變任何 accepted 語義的前提下裁決：decision record，留在 Lightweight

若所需契約語義可以在 **不改變任何 accepted requirement／AC／invariant／gate，且不建立其他工作將依賴的新設計基線** 的前提下裁決——包括既有來源只有一種合理解讀而尚未寫下，以及既有來源容許多種解讀但選擇僅影響本 work item——Design Authority MUST 產出持久 clarification／decision record，作為 Work Contract 的引用。

**這是 promotion assessment 的預設結果**，前提是工作仍符合第 3.3 節 Lightweight eligibility。

不得以口頭 clarification 或只寫入 Executor 假設，取代有效 decision record。Decision record 不得隱性改變 baseline；若裁決實際改變了 accepted 語義，它是第 5.3 節的 contract change，不是 decision record。

#### B. 語義必須被設計：Spec，進入 Formal

若符合下列任一情況，契約語義即屬「必須被設計」，MUST 由 Design Authority 準備 Spec，並進入第 3.4 節的完整 Formal lane：

- 工作引入的產品／系統行為、介面、invariant 或 gate **沒有 accepted baseline** 可以錨定，且其他工作將依賴它。通知、進度同步、結果摘要、文件維護等行政作業慣例，若不改變產品行為、驗收標準、完成條件、角色權限、安全控制與必要 assurance，不屬本項；其新增或調整是第 5.1 節 Bindings 內容的變更，依第 5.3 節留下版本、依據與授權，不依承載檔名觸發任何 lane 或 audit。
- 所需裁決 **會改變 accepted 語義**（此時同時是第 5.3 節的 contract change，須先經 acceptor；Spec 為其後的載體）。
- Parent 將必要選擇留待下游決定，屬尚未完成的設計，不構成 implementation readiness。

需要 Spec 的判準是契約語義需要設計，不是工作篇幅、檔案數量，或單純需要一次 Design Authority 判斷。

#### C. 需要多 execution units／dependencies／跨 session run-to-completion：完整 Formal

若預期整體工作需要分解為多個 execution units、管理其 dependencies，或需要跨多個 Executor／Reviewer sessions 協調 run-to-completion，MUST 進入完整 Formal：**Spec＋Tickets＋Orchestrator**。

語義已存在時可引用適用的有效 Spec，不要求為了協調而重新設計語義。此項是 Formal 協調需求，不建立第三條 lane；單次獨立 audit 的觸發仍依第 4.1 節，不單憑需要 Reviewer session 就要求 SDD。

Promotion MUST：

- 保存原 contract、worklog、產物、verification 與 findings。
- 記錄理由及有權決定。
- 將已完成與未完成內容對應至 Formal Spec／Tickets。
- 由相應 authority 確認既有 evidence 的可用範圍。
- 保留未解 findings，不藉換 lane、換 ID 或建新 Ticket 清空 audit history。

Promotion 不要求丟棄有效工作。Promote 後的 Spec 是原 Outcome Contract 內的 derived contract，其 derivation 與授權涵蓋依第 1.2、3.4 節；超出原 Outcome Contract boundary 者依第 1.2 節 re-authorization。Contract change 仍依第 5.3 節處理。

### 3.7 Work item and mandatory durable worklog

**Work item＝一個 accepted Work Contract 的一次執行。**

- Formal 下，以 Ticket 及其引用的 Spec 構成該 execution unit 的契約。
- Lightweight 下，以被接受的 brief、prompt 或 Jira item 等構成契約。

此定義有三項直接效果：

1. Sub-agent action、command、file edit 是 worklog 可引用的執行證據，不各自成為 work item。
2. 同一契約執行的續接 session 更新同一 worklog identity，不因 session replacement／rollover 另開工作身分。
3. 契約被接受並進入執行時，才產生 mandatory worklog 義務；包括隨即中斷、失敗、取消或無產物變更。純詢問、尚未成為 accepted execution 的探索與未被接受的請求，不因此產生 worklog。

Worklog 義務跟著 work item，不跟著執行者類型：由 Orchestrator 派工、由 direct execution session 執行，或由任何其他 session 接手，義務相同。

每個已執行 work item MUST 有足以支援 traceability、handoff 與 recovery 的 durable worklog，至少可追溯：

| Property | 必要內容 |
|---|---|
| **Work performed** | 實際做了什麼，以及目前結果。 |
| **Contract reference** | Accepted Work Contract、適用版本及重要變更。 |
| **Executing role and binding reference** | 執行角色與實際 binding 證據引用；不要求複製 Harness 日誌。 |
| **Decisions and assumptions** | 重要實作決定、假設，以及需要 authority 的決定所引用的 ruling。 |
| **Artifacts** | 主要新增、修改或移除的產物及可識別版本。 |
| **Verification** | Verification／test 方法、結果、限制及 evidence 引用。 |
| **Audit status** | 是否 required／elected／not required、其依據與實際進度；有 audit 時引用 records、findings 與 dispositions。 |
| **Remaining work** | 累積 scope、未完成事項、阻擋原因、負責者／authority 與下一步。 |

Worklog MUST 在足以支援 handoff／recovery 的時間點更新，不得只依賴成功結案後回憶補寫。中斷後補建的內容 MUST 區別可驗證事實與未知事項。

Worklog：

- 不取代 Work Contract、Spec、Ticket、audit record 或原始 evidence。
- 不創造 authority，不使未核准假設成為 accepted requirement。
- 不把 Executor 的「已修正」變成 Reviewer closure。
- MAY 以引用連結證據，無須複製完整 logs。
- MUST 可由接手 session、Orchestrator 或 Reviewer 取得並理解。

本節是 worklog 要求的唯一規範定義。治理不指定檔名、schema、storage、更新工具，也不要求一個 worklog identity 必須對應一個實體檔案。

### 3.8 Completion, integration and recovery

任一 lane 的 work item 結案前，MUST 確認：

- 符合有效 accepted Work Contract。
- Self-verification、必要 gates 與 evidence requirements 已滿足。
- 必要 audit／adjudication 已完成。
- 無未解且未經合法處置的 blocking finding。
- 無影響完成的未決 design ambiguity。
- 最終產物受到相應 verification／review coverage。
- Worklog 已反映實際結果與 follow-up。

Executor 的完成敘述不能單獨滿足 evidence requirement。Orchestrator 依有效的 Reviewer、Design Authority、Final Adjudicator 判斷及機器結果推進，不自行裁決 evidence sufficiency。

Review、verification 與結案版本 MUST 可對應。審後變更需要相應驗證；可能影響原 review 結論者，由 Reviewer／Design Authority 判定必要後續。

**跨 Ticket 整合 MUST 有適用的整合驗證；單張 Ticket 的 PASS 不自動證明整合產物符合跨 Ticket invariants。**

Design Authority 負責 Formal 的適用 phase acceptance，包括跨 Ticket invariants、整合行為、累積 evidence 與未結 follow-up；phase acceptance MUST 引用已 closure 的第 4.7 節 Spec Integration Audit record，不得豁免或取代它。Phase adjudication 是自主派工，不是 operator checkpoint。

恢復時 MUST 核對 contract、worklog、產物、裁決及原始 evidence。對話 context 或摘要不單獨建立 authority；未知 assignment 結果不得視為成功；重派前 MUST 處理既有執行及重複副作用風險。恢復失敗何時成為 boundary，依第 1.5 節。

Run 在授權工作完成，或剩餘工作皆受第 1.5 節真正 boundary 阻擋且已記錄時，才可結束。Run completion、work item completion、phase acceptance 與 release authorization MUST 分別陳述，不得互相冒充。

---

## 4. Independent Audit & Autonomous Adjudication

### 4.1 Audit applicability

本節是 audit applicability 的唯一規範定義：

- **Formal／SDD：每個 work item 的 independent audit MUST 執行；每份 Spec 另 MUST 執行第 4.7 節的 Spec Integration Audit。**
- **Lightweight：依 accepted contract、Project assurance policy、使用者要求或有權裁決決定。**
- 使用者明確要求 audit 時，MUST 執行。
- 已宣告的必要 audit 不得由 Executor 或 Orchestrator 取消。
- Assurance 是否足夠有實質爭議時，MUST route 至 Design Authority；涉及保留權限者仍依該 boundary 處理。

Project Bindings MUST 提供 Lightweight audit 的預設與觸發條件。未配置或無法確認適用性時，MUST route 至 Design Authority，不得靜默選擇不審查。

工作大小或缺少 Spec 不是免除 audit 的充分理由。**Audit applicability 與 SDD eligibility 是不同問題：需要 independent audit，不代表需要 Spec／Tickets。**

任何正式 audit 一旦被要求或選擇，均適用本節同一套流程，不另設 lightweight review。

未要求 audit 的 Lightweight 工作 MUST 如實標示「完成且依 policy 未要求 independent audit」，不得標為 audit PASS。未執行、未完成或失敗的 audit，不得視為通過；self-verification 不得冒充 independent audit。

### 4.2 Review access and contract sufficiency

Reviewer MUST 能取得 accepted contract、受審版本、worklog 與必要證據。

缺少 Spec 檔案本身不構成治理失敗。契約語義不足時，Reviewer MUST 提出具體 ambiguity 並 route 至 Design Authority，不得自行補寫 requirement。**契約不足是 routing signal，不是對 implementation 的 blocking finding，也不觸發 promotion**；是否 promote 依第 3.6 節由 Design Authority 判定。

精簡 dispatch inputs 不得限制必要 review coverage；具體 dispatch pack 由 Skills／Runtime 實現。

### 4.3 Independence and findings

所有正式 audit MUST 遵守第 2.3 節四項 independence properties（含將 Executor 結論當成待驗證主張），對受審 implementation、tests、contract 與 gates 唯讀（第 2.1 節），並保留獨立可識別的 review 結論（第 4.6 節）。

每項 finding MUST 有可追溯識別、證據、severity 與 blocking 判定。Blocking MUST 依 accepted contract 或宣告 operating scope 內的具體實質風險，不得以個人偏好創造需求。

預設 Critical／High 為 blocking；Medium 由 Reviewer 明確依風險與契約影響分類；Low 為 non-blocking。

Non-blocking findings MUST 記錄 disposition；需後續處理者須有 owner，但不得延長當前 audit cycle。後續工作仍受第 1.2 節的接受與授權要求約束。

Blocking status 或 review evidence 有爭議時，MUST route 至 Final Adjudicator；爭議實質涉及設計語義時，先交 Design Authority 判斷。

### 4.4 R1／R2／Alternate flow

```text
R1 — full independent audit of accepted work scope
    ├─ no blocking → audit closure
    └─ blocking → targeted correction
                       ↓
                  R2 — closure review
                       ├─ no unresolved blocking → audit closure
                       └─ blocking remains
                              ↓
                    exactly one Alternate Review
                              ├─ no unresolved blocking → audit closure
                              └─ unresolved → Final Adjudication
```

**R1** MUST 完整審查 accepted work scope、適用 invariants、變更風險與 acceptance evidence。Lightweight 的「full」指完整工作範圍，不要求建立 SDD artifacts。

**Targeted correction** MUST 聚焦 blocking findings，不夾帶無關 scope expansion 或重新設計。修正 MUST 提供可驗證的 closure 與回歸證據。

**R2** MUST：

1. 驗證待修 blocking findings 真正解決。
2. 驗證修正未引入回歸。
3. 檢查修正直接產生或暴露的 blocking defects。

R2 MUST NOT 變成第二次無限制全面 audit。新 non-blocking findings 不得延長 cycle。

R2 仍 blocking 時，MUST dispatch **exactly one Alternate Independent Review**，使用 fresh independent context；不得增加 R3／R4。

Alternate Reviewer 獨立判斷剩餘 findings 是否有效、已解決、分類有誤或屬 design issue。無未解 blocking 時可 audit closure；仍有未解問題時進 Final Adjudication。

Audit closure 不豁免第 3.8 節的其他完成條件。

### 4.5 Autonomous adjudication

Alternate Review 後仍未解的問題 MUST 進 Final Adjudication。

Final Adjudicator MAY：

- 依證據及理由 dismiss finding。
- 要求 targeted rework。
- 在下述 disposition 邊界內接受具 owner 的 deferred disposition。
- 將 design／requirement issue 交 Design Authority。
- 有實質理由時授權新的 bounded cycle。

Final Adjudicator MUST NOT：

- 虛報 verification 或 gate PASS。
- 以 disposition 隱性修改 requirement／AC／invariant。
- 覆寫原 Reviewer 結論。
- 取得其他 authority 的保留權限。
- 只因需要判斷就要求 operator 介入。

**Disposition 邊界。** Blocking finding 可被 deferred，僅限以下條件同時成立：

1. 該 finding **不主張違反 accepted contract 條款**（requirement／AC／invariant／gate）。主張契約違反的 finding 只能 dismiss（附推翻該主張的證據）、要求 rework，或作為 contract change 交 Design Authority 與 acceptor；不能 defer。
2. 殘餘風險在宣告的 operating scope 與 assurance policy 之內，或 finding 所指風險條件在宣告 operating envelope 之外。
3. 有 owner 與 tracked item；tracked item 依第 1.2 節在被接受前不是新工作。
4. Disposition 記錄理由，且不將任何 gate 標為 PASS。

Assurance policy 宣告為高風險類別的 blocking finding，deferral MUST 另有 Design Authority 的確認並記入 disposition；Final Adjudicator 不得單獨 defer。

真正 design／requirement issue MUST 隨時直接 route 至 Design Authority，不必耗盡 R1／R2。

**Cycle 起點與進展。** 裁決後 MUST 繼續合法執行。新的 bounded cycle 一律從 R1 開始，且只有兩個合法起點：

- Final Adjudicator 授權的 material rework，授權 MUST 指明相對於前一 cycle **受審 subject 有何實質改變**；
- Design Authority 的 contract change 使受審 subject 或其契約失效，新 cycle 依該 ruling 開始，不需另經 Final Adjudicator 授權。

Subject 與契約皆未改變時，不得開新 cycle。改 lane、換 model 或重命名 work item 不構成 reset 理由。**同一 root cause 的 blocking finding 在新 cycle 的 R2 之後仍未解時，該問題不再視為 rework 可解的 implementation defect**：Final Adjudicator MUST 將其作為 design／requirement issue 交 Design Authority，或在 disposition 邊界內處置；MUST NOT 以 rework 為理由再授權 cycle。本治理不設 cycle 總數上限；上述進展條件即為 bound。

### 4.6 Audit traceability

Audit records MUST 可識別：

- Work Contract 與受審版本／範圍。
- Reviewer role、binding 證據與 independence（第 2.3 節四項 properties 的滿足方式）。
- Round／cycle、findings、verdict 與 closure evidence。
- 後續 adjudication、disposition 及其 authority。

正式 Reviewer 結論與後續裁決 MUST 保持可區別。Executor 提供修正證據不等於自行確認 formal closure。

Worklog 依第 3.7 節引用 audit 狀態；audit records 的格式與儲存位置不受本治理限定。

### 4.7 Spec Integration Audit

Formal 下，一份 Spec 的全部 implementation Tickets 結案後、Design Authority phase acceptance 前，MUST 對整合後的最終 subject 執行一次 independent **Spec Integration Audit**。它是獨立的 audit instance，subject 為整合結果，不是任何 Ticket audit 的 R3。

審查範圍 MUST 涵蓋：

- 跨 Ticket invariants。
- Spec-level AC coverage：每條 Spec AC 有對應 evidence 與 PASS／FAIL 判定，且 Spec AC 整體涵蓋其 derivation record 所分配的 Outcome Contract acceptance boundary 部分（第 1.2 節、第 3.1 節第 3 項）。
- 整合行為。
- 最終 subject 的 verification／audit coverage（第 3.8 節）。
- Spec／Tickets 對 Outcome Contract 的 traceability 與 boundary 符合性（第 1.2 節），含對所分配 boundary 部分的 traceability 完整。Outcome Contract 或適用 phase 最終 closure 前，全部 derived Specs MUST 合起來涵蓋整個 acceptance boundary；同一 Outcome Contract 最後一份未結 Spec 的 Spec Integration Audit MUST 另核對全部 derived Specs 的分配合起來涵蓋整個 acceptance boundary。分配缺口或造成歧義的重疊是 finding，屬設計事項者依第 2.4 節 route Design Authority；不因此新增 audit instance、round 或角色。

本 audit 適用第 2.3 節四項 properties，以及第 4.3–4.6 節同一套 findings、R1／R2／一次 Alternate Review／Final Adjudication 與 traceability 規則；不新增 round。MUST NOT 重開已閉合的 Ticket finding，除非有新的 integration-level evidence；此時它是對整合 subject 的新 finding。修正屬契約內 rework，依第 3.8 節作審後驗證。揭露的設計缺陷依第 2.4 節 route Design Authority；boundary 疑義依第 1.2 節處理，本 audit 的 boundary 符合性 finding 在 Design Authority determination 後仍有爭議時，依第 1.2 節視為 Design Authority 無法確立而 fail-closed。

Design Authority、Orchestrator 與 Project Bindings 均不得豁免本 audit（第 2.1、4.1、5.2 節）。

**單 Ticket fast path。** Spec 只有一張 Ticket 時，該 Ticket 的 independent audit record MAY 同時滿足本節，但僅限該 audit 實際審查了最終整合 subject、Outcome Contract boundary、所分配部分的 Spec-level AC coverage、整合行為、最終 evidence 與必要 traceability（含該 Spec 為同一 Outcome Contract 最後一份未結 Spec 時的全部 derived Specs 分配涵蓋核對），且其 record 明確如此記載。MUST NOT 將既有 Ticket R1 record 事後重新標示為 Spec Integration Audit。Project Bindings assurance policy 宣告採用 fast path 時，MUST 同時宣告上述範圍的核對方式。

Lightweight 無 Spec，不適用本節；assurance policy MAY 對特定類別要求等效的 outcome-level audit。

---

## 5. Project Bindings & Reserved Boundaries

### 5.1 Required bindings

以下 bindings 與所需 Agent／Subagent definitions MUST 在 Orchestrator activation 前，以及 Lightweight work item 第一次正式 audit 前就緒且可驗證；不得啟動後才以 prompt 自述角色代替尚未成立的 bindings；root role session 的 activation basis 依第 2.2 節，不屬此處所稱的 prompt 自述。每個 Agent／Subagent 首次執行前，其 definition 與明確 mapping MUST 已存在，實際 assignment 依第 2.2 節核對。

Bindings 可由專案或可重用工作環境 profile 提供；Lightweight 工作可引用既有 profile，不需重新初始化專案。此要求不規定 Harness 的 session 啟動順序、definition loading 或 spawn 方法。

| Binding | 必要內容 |
|---|---|
| **Governance adoption** | 採用版本、權威位置與變更 authority。 |
| **Authority sources** | Outcome Contract acceptor、執行授權來源、上位 contracts、operator／人類代理、standing authorizations，以及依第 5.2 節保留的 reserved boundaries（含是否保留 Spec review、獨立 implementation authorization、merge／push／release）。 |
| **Agent／Subagent definitions and Model Mapping Profile** | 六治理角色與所有實際使用的 reusable Subagent definitions；採用的 Profile、每個可 dispatch identifier 的有效 mapping 與驗證機制（含 root role session 依第 2.2 節核對 model／effort 的方式與證據位置）；符合第 2.3 節四項 properties 的 independent dispatch 機制及其滿足方式。 |
| **Lane policy** | 預設分類、適用 Formal 要求及模糊情況的決定者；不得取代第 3.3、3.6 節。 |
| **Assurance policy** | Lightweight audit 預設與觸發條件、高風險類別（第 4.5 節 disposition 邊界所引用）、適用 integration／release gates、第 4.7 節單 Ticket fast path 是否採用及其核對方式、model diversity 預設（第 2.2 節）。 |
| **Skills and runtime** | 選用工作 Skills、direct-execution／orchestration 與 recovery 能力。 |
| **Work records** | Outcome Contract、derived contracts 與 derivation records、worklog、audit、decisions 與 evidence 的權威位置。 |

Policy MUST 使 lane 與 assurance 決定可追溯。Agent／Subagent mapping 與必要機制不得只以 prompt 自述取代。

Design Authority MUST 決定專案適用的高風險分類及 assurance 要求；Orchestrator 依宣告與有權判定執行，不得自行降級。

**Standing authorizations。** Acceptor MAY 在 Authority sources 中預先宣告某些類別的工作或動作視為已接受並授權（例如 operator 對特定範圍的常設指令）。該宣告本身是 acceptor 的行為，其範圍與撤銷方式 MUST 明確；Agent 不得推定未宣告的預授權。

### 5.2 Reserved boundaries and overrides

Project Bindings MUST 明確列舉其保留的 non-delegable 決定／動作（第 1.5 節第 3 項），不得由 Agent 臨時增加「保險起見問 operator」的 gate。

**Reserved boundaries 採 opt-in。** Spec review 與獨立的 implementation authorization 預設不保留：Bindings 未列為 reserved boundary 時，由 Outcome Contract 的授權涵蓋（第 1.2、3.4 節）；Bindings 明確列舉時即為第 1.5 節第 3 項的 boundary。Merge／push／release 是否授權由 Bindings 決定。在已接受的 Outcome Contract 內產生 derived contract 是 Design Authority 的設計行為，不是接受或授權行為。

Bindings MAY 具體化工具、storage、模型、路徑及風險要求，但 MUST NOT：

- 取消 mandatory worklog。
- 將 self-verification 冒充 independent audit。
- 弱化第 2.3 節四項 properties、context independence、已觸發 audit 的流程，或豁免第 4.7 節 Spec Integration Audit。
- 擴張 Executor／Reviewer／Orchestrator authority，或讓 Design Authority 取得接受／授權權限。
- 讓 promotion 清除 findings 或授權限制。
- 取消 autonomous routing 與 adjudication 後的 continuation。
- 以 Lightweight 增量執行繞過整體工作的 contract-change 或 Formal 要求。

需要 release 的專案 MUST 宣告 release authority、必要 gates 與 evidence；work item completion 不授予 release permission。

### 5.3 Contract changes and precedence

本治理決定 authority 與必要 properties；Project Bindings 在其範圍內具體化；Accepted Work Contract 定義工作要求；Skills／Runtime 不得修改上述權限與義務。

凡預期結果改變 accepted 語義（第 1.2 節：Outcome Contract 的 intent、scope、constraints 與 acceptance semantics），或改變其他工作所依賴的設計基線（第 3.3 節），MUST 作為 **contract change** 處理：

- Route 至具有該設計權限的 Design Authority，判定其性質與影響。
- 走該 Outcome Contract 原本的 acceptance authority（acceptor）。
- 記錄變更內容、決定者、接受／授權狀態，以及對進行中工作、dependencies 與既有 evidence 的影響。
- 在必要接受與授權成立前，不執行依賴變更後語義的 implementation。

改變 accepted 語義者仍由 acceptor 重新核准，不因請求由 prompt 或 Jira description 承載而消失；已有有效核准紀錄時，不得重複要求核准。

**變更只有兩類；本段是兩類劃分的唯一規範定義，第 3.3、3.4、3.6 節引用之。**

1. **改變 accepted 語義**：contract change，如上。
2. **不改變 accepted 語義的 derived contract 設計、修訂與 clarification**：由 Design Authority 以 derivation／decision record 決定，MUST 記錄對進行中工作、dependencies 與既有 evidence 的影響，並依第 3.8 節處理受影響的 verification／audit coverage；不觸發 acceptor 核准。Tickets 與 Executors 仍不得自行重新定義 AC（第 3.1、3.4 節）。第 3.6 節 A 的 decision record 是本類在 Lightweight 的形式，不冒充語義變更，也不以 decision record 隱性改變 baseline。

本治理不設第三類「additive」amendment：判準是是否改變 accepted 語義，不是變更的大小或方向；新增了 Outcome Contract 未涵蓋的 requirement、AC 或 scope，即屬第 1 類。需要獨立接受的新增工作，以新的 Outcome Contract 承載。

Worklog 記下新假設，不等於 contract 已變更。代理寫入接受或核准紀錄，不等於取得該 authority。

Governance、bindings（含 definitions／Model Mapping Profiles）與 accepted contracts 的變更 MUST 留下版本、依據與授權。新版本不自動適用既有工作；採用時 MUST 明確處理進行中 assignments、audit 與 evidence coverage。

### 5.4 Implementation boundary

本治理要求的 properties MUST 有實際能力支援，但不規定：

- Ticket lifecycle state machine。
- `gov_state` 或其他特定 validator。
- Worklog／audit／timeline schema。
- Git branch、merge、commit trailer。
- Transcript parser 或 Agent loading。
- Context rollover、worker timeout、heartbeat 與 orphan reconciliation 的具體演算法。
- 恢復重試的次數或門檻。

既有 tracker、文件、CI、Runtime 或簡單持久紀錄能滿足要求時，MAY 直接使用。

若必要 property 已可由既有 tooling 檢查，Project Bindings SHOULD 引用並使用該 check，而非只依賴 prompt discipline。此偏好不要求新增 validator、artifact、approval gate 或 workflow。

**不得為了採用治理而強制建立另一套 workflow engine，也不得只以文字宣稱尚未具備的 isolation、binding 或 recovery 能力。**

---

## Appendix A · History and rationale（non-normative）

本附錄不新增規則；操作要求以第 1–5 節為準。v1.0 的 Final Validation Summary、Adoption record 與 Interpretation record IR-1 原文保存於 [Minimal Operational Governance v1.0](Minimal_Operational_Governance_Final_Candidate.md) 文末，不在此複製。

### A.1 Version lineage

| 版本 | 日期 | 狀態 | 依據 |
|---|---|---|---|
| v0.1 Candidate A／B | 2026-09-16 | historical | [A／B Adjudication](<../Governance Candidate A-B Adjudication Review(Fable-5.1).md>)：ADOPT B WITH CHANGES |
| v0.2 → v0.3 | 2026-09-16 | historical | [v0.2 Closure Review](<../Governance v0.2 Closure Review(Fable-5.1).md>) Q1–Q4；[v0.3 vs v2 Final Analysis](<../Governance v0.3 vs v2 Final Analysis(Fable-5.1).md>) L-1～L-9 |
| v1.0 | 2026-09-17 | Adopted／Frozen | [Final Architecture Review](<../Governance Final Architecture Review(Fable-5.1).md>)：ADOPT |
| IR-1 | 2026-09-18 | folded into v2.0 §3.3、§3.6-B | 行政作業慣例 ≠ 設計基線；六條件已寫入正文 |
| v2.0 | 2026-09-22 | Adopted／Frozen | [vNext Architecture Analysis](<../Governance vNext Architecture Analysis(Fable-5.1).md>)：DESIGN VIABLE WITH CONDITIONS；operator S-1 決定；S-3 → S-4 → closure → pruning → Astra regression → S-5 adoption（同日；詳 B.4） |
| v2.1 | 2026-10-01 | Adopted／Frozen | [Orchestrator Runtime Architecture Review](<../Governance Orchestrator Runtime Architecture Review(Fable-5.1).md>)：GOVERNANCE SEMANTIC DRIFT；operator 2026-10-01 決定；independent review → correction → closure → final-md5 acknowledgement → adoption（同日；詳 Appendix C） |

### A.2 Resolved questions（v0.2 Closure rulings 與 v2.0 對照）

| # | 問題 | v1.0 裁決位置 | v2.0 狀態 |
|---|---|---|---|
| 1 | Non-delegable approval 的範圍 | §3.4、§5.1、§5.3 | **重新錨定**：acceptor 保留 Outcome Contract 的接受／授權與 boundary re-authorization（§1.2、§1.5）；Spec review 與獨立 implementation authorization 改為 Bindings opt-in（§5.2）；仍無 additive 類（§5.3）；standing authorization 仍為 acceptor 行為（§5.1） |
| 2 | Final Adjudicator disposition 邊界 | §4.5 | 不變 |
| 3 | Bounded cycle 是否無限循環 | §4.5 | 不變；§4.7 Spec Integration Audit 自有 cycle，適用同規則 |
| 4 | Recovery failure 何時是 boundary | §1.5 | 不變（三步 recovery 段 byte-identical） |

### A.3 v2 母版 → Minimal：Continuity Reference（v1.0 表，原樣保留）

| 保留的 property | 下放的 mechanism |
|---|---|
| Autonomous run-to-completion、合法停止邊界、recovery 停止條件 | 詳細 execution loop、checkpoint／rollover 演算法、retry policy、capability class 記錄格式 |
| 穩定六角色／reusable Subagent definitions、可替換 Model Mapping Profiles、可驗證 assignment 與 independent dispatch 四項 properties | Definition 檔案與載入、model-id parser、環境變數、invocation |
| Independent audit、R1／R2／Alternate／Final Adjudication、disposition 邊界、cycle 進展條件 | Audit filename、header schema、verdict／classification grammar |
| Completion evidence、最終版本 coverage 與整合驗證 | Commit binding 演算法、merge topology、ledger 路徑白名單 |
| 授權、findings、裁決與結果可追溯 | Commit trailers、timeline grammar、DISPATCH／RETURN 格式 |
| 持久狀態、worklog 與安全恢復 | Ticket state engine、`gov_state`、worklog layout、heartbeat／orphan mechanics |
| 專案風險、phase 與 release assurance | Wave planning、風險清單、release tooling、Git 慣例 |

v2 母版與 v1.0 不構成隱性 fallback authority。

### A.4 Grill methodology note

自第 3.2 節移入的 methodology（HOW）說明，語義與適用性不變：

Grill 是釐清 Work Contract 的 methodology（HOW）：用於在接受前收斂 Outcome Contract 的 intent、scope、acceptance boundary 與 authorization，或在執行中揭露需要其他 authority 決定的事項；不必產生 Spec／Tickets，也不是所有工作的必經儀式。

## Appendix B · v1.0 → v2.0 change log 與 Adoption record（non-normative）

本附錄自 v2.0 原樣保留；其中的「本檔」「本版」指 v2.0。

### B.0 Baseline and design provenance

自文首移入，內容不變：

**基線：** [Minimal Operational Governance v1.0](Minimal_Operational_Governance_Final_Candidate.md)（Adopted／Frozen 2026-09-17；§1–§5 body md5 `4c23bbefd4f091e9669d95f48cec0d2f`，本版起草時 byte-unchanged）。**設計依據：** [Governance vNext Architecture Analysis](<../Governance vNext Architecture Analysis(Fable-5.1).md>)（Fable-5.1，2026-09-22，verdict DESIGN VIABLE WITH CONDITIONS）＋ operator S-1 決定（2026-09-22：版本名、reserved-boundary opt-in、Model Profile v2 預設值）＋ 兩項 refinement（boundary 疑義 DA-first、routing 衝突視為爭議）。本版改變 §1.2、§2.4、§3.4、§5.3 的 normative semantics 並新增 §4.7；完整 MUST／SHOULD／MAY diff 見 Appendix B 所引報告。

### B.1 Semantic changes

| ID | 條文 | 變更 |
|---|---|---|
| N-1 | §1.2、§2.1（DA 列）、§2.4（兩列）、§3.1(3)(4)、§3.4、§3.6 promotion 段、§5.1、§5.2 | Outcome Contract 為人類接受的契約；Spec／Tickets 為 DA derived contracts，附 derivation record 與 boundary determination；derived contract 不需逐份核准；「accepted 語義」專指 Outcome Contract 語義；「accepted contract」涵蓋 derived contracts |
| N-1／R-A | §1.2、§3.3 | Boundary 疑義：Executor／Reviewer 先 route DA；DA 無法確立在 boundary 內時受影響路徑 fail-closed 至 acceptor；DA 不取得接受／授權。S-4（M-2，2026-09-22）：§1.2 加 Reviewer boundary 符合性 finding 的 closure rule——DA 先評估；DA 確立且 Reviewer 撤回／關閉 → 繼續；DA determination 後仍有爭議 → 視為 DA 無法確立、fail-closed 至 acceptor；FA 只裁 routing／process，不代 acceptor 裁決 boundary；§4.7 第三段末句同步 |
| N-2／R-B | §2.4 | 五種情況表：explicit＋consistent → 派工；no label＋unique rule → 派工並記錄；explicit＋conflicting → FA；authority 真正模糊 → FA；契約語義／sufficiency 無法機械判類 → DA-first。缺 label 不是爭議；Orchestrator 不默默覆寫任一來源；提出者義務 MUST → SHOULD |
| N-3 | §3.4、§3.8、§4.1、§4.7（新）、§5.2 | Spec Integration Audit：Formal 每份 Spec MUST；獨立 audit instance，不是 R3；範圍五項；不重開已閉合 finding 除非新 integration-level evidence；DA phase acceptance MUST 引用；DA／Orchestrator／Bindings 不得豁免；單 Ticket fast path 僅限 audit 實際涵蓋全部範圍且 record 明載，不得事後重標。S-4（M-3，2026-09-22）：§1.2 derivation record 載明該 Spec 所分配的 acceptance boundary 部分；§3.1(3) 與 §4.7 第二 bullet 的 coverage 判準改為所分配部分；§4.7 第五 bullet 加全部 derived Specs 合起來涵蓋整個 boundary、最後一份未結 Spec 的 audit 核對分配完整；fast path 同步 |
| N-4 | §2.2 | Cross-model 由 core SHOULD 改為 Profile／Bindings assurance default；替代 MUST 維持 §2.3 四項，MAY 改變 diversity 並記錄 |
| N-5 | §1.5、§3.4、§5.2、§5.3 | Reserved acts 單一清單於 §1.5（四項）；contract change 判準錨定 Outcome Contract 語義；兩類劃分唯一定義於 §5.3；Spec review／implementation authorization opt-in（S-1 決定 2） |

### B.2 Editorial（semantics-preserving）

| ID | 動作 |
|---|---|
| E-1 | 兩類劃分只在 §5.3 定義；§3.3、§3.4、§3.6 引用 |
| E-3 | §4.3 五 bullets 縮為一句引用 §2.3、§2.1、§4.6 |
| E-4 | §3.3、§3.6、§4.7 的 route 語句加「依第 2.4 節」 |
| E-5 | §3.2 Grill 縮為 methodology 兩句，保留「不創造 authority」 |
| E-6 | IR-1 併入 §3.3、§3.6-B(1) |
| E-7 | 文首歷史敘述與文末四表移至 Appendix A（v1.0 records 以引用保存）；新增 Appendix B |
| E-8 | header 縮短；§5.4 未改 |

E-2（self-verification 定義集中）僅作最小處理：§2.3 仍為唯一清單，§3.5、§4.1 原句保留。

### B.3 完整 MUST／SHOULD／MAY diff

逐句 diff 與註解見 [Governance v2.0 Candidate S-2 Drafting Report](<../Governance v2.0 Candidate S-2 Drafting Report(Fable-5.1).md>)。

### B.4 Adoption／Freeze record

| 項目 | 內容 |
|---|---|
| 狀態 | **Adopted／Frozen**（2026-09-22，operator S-5 明確授權） |
| S-2 draft | 2026-09-22，Fable 5.1，依 operator S-1 決定與兩項 refinement；[S-2 Drafting Report](<../Governance v2.0 Candidate S-2 Drafting Report(Fable-5.1).md>) |
| 基線 | v1.0 §1–§5 body md5 `4c23bbefd4f091e9669d95f48cec0d2f`；v1.0 檔 byte-unchanged（S-5 重算 `387547cdc5e0b7d2ff2f32d851b0bb4c`） |
| S-3 acceptance review | [Independent Acceptance Review (Opus-5)](<../Governance v2.0 Candidate Independent Acceptance Review(Opus-5).md>)：**ADOPT WITH REQUIRED CHANGES**（0 BLOCKER、4 MATERIAL M-1～M-4、8 NON-MATERIAL） |
| S-4 targeted correction | [S-4 Targeted Correction Report (Fable-5.1)](<../Governance v2.0 Candidate S-4 Targeted Correction Report(Fable-5.1).md>)：M-1～M-4 限 review §6 edit sites，18 hunks；NON-MATERIAL 未動 |
| S-4 closure | [S-4 Closure Review (Opus-5)](<../Governance v2.0 Candidate S-4 Closure Review(Opus-5).md>)：M-1、M-2、M-3、M-4 **CLOSED**；targeted regression **PASS**；無 S-4.1 |
| Pruning pass | [Pruning Pass Report (Fable-5.1)](<../Governance v2.0 Candidate Pruning Pass Report(Fable-5.1).md>)：Astra spec P-01～P-15，套用 11 項（P-01–05、07、11–15）、deferred 4 項（P-06、08、09、10），23 hunks，語義不變；§1.1／§1.3 改為索引、A.4／B.0 新增 |
| Astra final regression | [Final Pruning Regression Check (Astra)](<../Governance v2.0 Final Pruning Regression Check(Astra).md>)：AUTHORIZED PRUNING、SEMANTIC PRESERVATION、DEFERRED REGIONS、CLOSED FINDINGS REGRESSION、REFERENCE／MOVE SAFETY 全 **PASS**；flagged pointers SAFE AS-IS |
| S-5 adoption | 2026-09-22 operator 明確授權 Adopted／Frozen。Adoption edits 限 metadata／record（header 狀態、A.1 v2.0 列、本節、Appendix B 標題）；§1–§5 body 與 Astra 核可的 pruned baseline byte-identical。記錄：[Adoption and Freeze Record](<../Governance v2.0 Adoption and Freeze Record.md>) |
| 採用效果 | 依 §5.3：不自動適用任何專案；已採 v1.0 的專案需明確 re-pin 並處理進行中 assignments、audit 與 evidence coverage。本檔 frozen；之後任何變更依 §5.3 留下版本、依據與授權，以新版本承載 |

## Appendix C · v2.0 → v2.1 change log 與 Adoption record（non-normative）

### C.0 Baseline and design provenance

**基線：** [Minimal Operational Governance v2.0](Minimal_Operational_Governance_v2.0_Candidate.md)（Adopted／Frozen 2026-09-22；整檔 md5 `5d258fd3e4b5cd0894f7f7cd1175eca6`，§1–§5 body md5 `b44f23bb155a601ae7518465a9f7f3f4`；本版起草時 byte-unchanged）。本版由 v2.0 逐位元複製後只作 C.1 所列修改。

**設計依據：** [Orchestrator Runtime Architecture — Architecture Review／Ruling](<../Governance Orchestrator Runtime Architecture Review(Fable-5.1).md>)（Fable 5.1，2026-10-01；verdict：GOVERNANCE SEMANTIC DRIFT — Orchestrator assignment model changed）。該 review 認定 v1.0 §2.2 的「每個實際 assignment（包括 Orchestrator 自身…）MUST…綁定至宣告的 definition」把被指定的 root control-plane session 與被派工的 assignment 併成同一 abstraction，而歷史母版與參考實作從未要求 root Orchestrator 由 agent definition instantiate。

**Operator 決定（2026-10-01）：** 採用該 review 的 verdict 與 §9.1 architecture；治理區分 root role session activation 與 dispatched Agent／Subagent assignment；root role session 不因治理要求而必須由 agent definition instantiate；Lightweight direct-execution root session 擔任 Executor 時適用同一區分；root session 派出的治理 Agent／reusable Subagent 維持 definition＋explicit mapping＋effort／mode＋deterministic harness binding＋runtime evidence。原文見 [v2.1 Candidate Drafting Report](<../Governance v2.1 Candidate Drafting Report(Fable-5.1).md>)。

### C.1 Semantic changes

| ID | 條文 | v2.0 | v2.1 |
|---|---|---|---|
| R-1 | §2.2 第 5 段（binding 句） | 單一 predicate：每個實際 assignment（包括 Orchestrator 自身與 reusable Subagent）MUST 綁定至宣告的 definition、model 及適用 effort／mode | 分兩種。**被派工的 assignment**：predicate 原樣保留，範圍為兩種 root role session 以外的所有 assignment。**Root role session**（只限 Orchestrator 與 Lightweight direct-execution Executor；其他直接擔任治理角色的 session 仍屬被派工的 assignment）：activation basis、model／effort runtime verification、role-definition grounding、work identity and records 四項；Orchestrator 在 model／effort 核對成立前不得派工；建立方式屬 Runtime／Harness HOW，由 definition instantiate 不是必要條件；grounding 不證明 model／effort |
| R-2 | §2.2 同段（prompt 自稱句） | Prompt 中自稱角色、model 或「已綁定」不構成 binding 證據 | 原句保留；新增：designation／接受與授權是 acceptor／operator 的 authority 行為，不是自稱；designation 不構成 Outcome Contract 的接受或授權 |
| R-3 | §5.1 首段 | 不得啟動後才以 prompt 自述角色代替尚未成立的 bindings | 原句保留；加限定：root role session 的 activation basis 依 §2.2，不屬此處的 prompt 自述 |
| R-4 | §5.1 表 Agent／Subagent definitions and Model Mapping Profile 列 | 每個可 dispatch identifier 的有效 mapping 與驗證機制 | 同上，另明列 root role session 核對 model／effort 的方式與證據位置 |
| R-5 | §2.2 修復／替代句 | 不得將該 assignment 冒充符合要求的 execution、review 或 adjudication | 列舉加入 orchestration，使 Orchestrator 的 model／effort 不符有明文後果 |

保留的強化（不是本版變更）：`orchestrator` 是 Profile identifier，Orchestrator 的 model／version／effort 須有有效 mapping 並可由 Runtime／Harness 證據核對（v0.1 起）。

### C.2 未變更

§1（含 §1.4、§1.5）、§2.1 角色表與 definition 要求、§2.2 其餘各段（mapping 內容、Profile 採用、replacement、model diversity；修復／替代句只有 R-5 一詞之差）、§2.3 四項 independence properties 與 self-verification 清單、§2.4、§3、§4、§5.1 其餘、§5.2–§5.4，以及 Appendix A.2–A.4 與 Appendix B 正文（標題下的說明行見 C.3），皆與 v2.0 byte-identical。未新增角色、lane、audit round、approval layer、operator gate 或任何特定 harness／CLI 的要求。

### C.3 Metadata edits

文首 header（標題、狀態、版本、日期、基線指標、package references、歷史版本句）、Appendix A.1 新增 v2.1 列、Appendix B 標題下一行說明、本附錄。2026-10-02 另有一次 metadata-only 更新（header 的 package references 與 visualization 句；見 C.4「Metadata update」列）。

### C.4 Adoption／Freeze record

| 項目 | 內容 |
|---|---|
| 狀態 | **Adopted／Frozen**（2026-10-01，operator 明確授權） |
| Candidate draft | 2026-10-01，Fable 5.1，依 C.0 的設計依據與 operator 決定；[v2.1 Candidate Drafting Report](<../Governance v2.1 Candidate Drafting Report(Fable-5.1).md>)（含決定原文、hunk 清單與 architecture regression） |
| Independent review | [v2.1 Candidate Independent Review (Opus)](<../Governance v2.1 Candidate Independent Review(Opus).md>)：初審 **ADOPT WITH REQUIRED CHANGES**（0 BLOCKER、3 MATERIAL M-1～M-3、9 NON-MATERIAL）→ 定點修正 → closure check **ADOPT**（M-1、M-2、M-3 CLOSED）→ CC-1 依 reviewer 指定修正 → **final-md5 acknowledgement：ACKNOWLEDGED**（Candidate 整檔 md5 `3abaa4058bdd9233274f1ad850e9ed34`） |
| Operator acceptance | 2026-10-01：ACCEPT。確認三點：(1) Orchestrator root role session 不限 Formal run；(2) root role session 是封閉的兩種（Orchestrator、Lightweight direct-execution Executor），其他治理角色的 session 仍是 definition-bound assignment；(3) 在不符 assignment 的禁止句加入 orchestration，作為 M-1 的必要 closure |
| Adoption edits | 限 metadata／record：文首狀態、日期、package references 中 orch-default v2.1 的狀態、Appendix A.1 v2.1 列、本附錄標題與本節。§1–§5 body 與 reviewer 確認的 Candidate byte-identical（body md5 `9113074ad8f7a586ae9a77c4a80ac5d1`）。記錄：[v2.1 Adoption and Freeze Record](<../Governance v2.1 Adoption and Freeze Record.md>) |
| Companion | [Reference Orchestrator Contract orch-default v2.1](references/orchestrator-contracts/default-v2.1.md)（同日 Adopted／Frozen）。Model Profile default v2.3 與 impl-default v2 不變 |
| 採用效果 | 依 §5.3：不自動適用任何專案；已採 v2.0 的專案需明確 re-pin 並處理進行中 assignments、audit 與 evidence coverage。本檔 frozen；之後任何變更依 §5.3 留下版本、依據與授權，以新版本承載 |
| Metadata update（2026-10-02） | operator 明確授權「Minimal v2.1 檔頭可以調整」後，只更新文首 header 兩段：package references 中 Model Profile 由 [default v2.3](references/model-profiles/default-v2.3.md) 改為 [default v2.4](references/model-profiles/default-v2.4.md)（v2.4 Adopted／Frozen 2026-10-02，`primary_reviewer`-only revision，見其 §8；v2.3 保留為 frozen baseline），visualization 句改指加日期的 HTML（最新 2026-10-02 版）；另在 C.3 與本列留下紀錄。不是本治理的版本變更：§1–§5 body 與 2026-10-01 凍結時 byte-identical（body md5 `9113074ad8f7a586ae9a77c4a80ac5d1` 不變）；整檔 md5 自 `8d2012ca3b021e598be71e382ab7b00b` 變為本次更新後的值（記於 Notion package 頁與 HTML 追溯段）。Project Bindings 仍直接 pin Model Profile 版本，本段不影響任何已採用專案 |
