# Minimal Operational Governance — v2.2

**狀態：Adopted／Frozen（2026-10-12，operator 明確授權；independent review A1 closure 後採用，見 Appendix D.8、D.9）**  
**版本：v2.2**（全名一律寫「Minimal Operational Governance v2.2」，與歷史「Model-Agnostic Development Governance 新專案開工標準 v2」無關）  
**Drafted：2026-10-12 · Adopted／Frozen：2026-10-12**  
**適用範圍：Lightweight 與 Formal／SDD execution**

**基線：** Minimal Operational Governance v2.1（Adopted／Frozen 2026-10-01；2026-10-02 header metadata update）。權威基礎為 Notion 上的「Minimal Operational Governance — v2.1」；其原檔 `Minimal_Operational_Governance_v2.1_Candidate.md` 整檔 md5 `d4d458eeb6d571f1f4f3f0cc607feac9`（sha256 `2283796846e825195720eb74a6139e8f1be407ebc7cc64201235537760cca101`），§1–§5 body md5 `9113074ad8f7a586ae9a77c4a80ac5d1`。本版由該檔逐位元複製後，只作 Appendix D 所列修改；v2.1 本身不因本版改變。v2.1 → v2.2 的變更、來源與理由見 Appendix D；v2.0 → v2.1 見 Appendix C；v1.0 baseline 與 v2.0 design provenance 見 Appendix B.0。

**本檔採用後為 authoritative source。** 本版不自動適用任何專案；已採用 v2.1 或更早版本的專案依第 5.3 節明確改採。對應的 visualization 是加日期的 non-normative HTML（master repository 的 `minimal_governance_map_v2.2_zh-TW_2026-10-12.html`）；與本檔不一致時以本檔為準。

**標示。** 本 header 之後的引言與第 1–5 節中，以〔v2.2 新增 V22-nn〕或〔v2.2 修改 V22-nn〕起頭的段落、表列或項目是本版的新增或修改，ID 對應 Appendix D.2；未標示者與 v2.1 逐字相同。標示是 non-normative 註記，採用時保留作為逐條追溯；移除不改變語義。

**Reusable package references（non-normative）：** Reference Model Profile default v2.5（Adopted／Frozen 2026-10-11；以引用方式沿用 default v2.4 的部分章節，v2.4 一併保留）、Implementation Profile impl-default v2（Adopted／Frozen 2026-09-22）、Reference Orchestrator Contract orch-default v2.2（Adopted／Frozen 2026-10-12，與本版同日；v2.1 保留為 frozen baseline）。在 master repository 中分別位於 `references/model-profiles/default-v2.5.md`（與 `default-v2.4.md`）、`references/implementation-profiles/default-v2.md`、`references/orchestrator-contracts/default-v2.2.md`。三者分別提供可替換的 role／model mapping defaults 與 deterministic replacement policies、可重用的 implementation HOW、可重用的 control-plane HOW，皆從屬於本治理，由 Project Bindings 依第 5.1 節選用／採用，不修改任何 authority 或 normative semantics；較早版本的 profiles 與 contracts 保留為 frozen baseline。本段為 metadata：reference 版本更替時只更新本段，不構成本治理的版本變更；Project Bindings 仍直接 pin 各 reference 的版本（第 5.1 節）。具體 model 的參考分類見 non-normative Appendix E。

> **Human approves the outcome contract once; authorized Agents autonomously design, decompose, implement, review, correct and complete within that boundary.**

人類 acceptor 一次接受並授權 Outcome Contract（第 1.2 節）。之後正常的 Spec／Ticket derivation、implementation、technical clarification／question routing、verification、review／independent audit、findings、rework／re-verification、Alternate Review／Final Adjudication、Spec Integration Audit 及 phase progression／completion，MUST 由具有相應 authority 的 AI Agents 自主執行、裁決、留下 durable records 並繼續。Operator interaction 是第 1.5 節的 exceptional boundary，不是正常 workflow gate。

本治理定義工作所需的 authority、contract、verification、assurance、traceability 與 recovery，不假設所有工作都必須經過 Spec-Driven Development（SDD）。

> **Use the lightest workflow that preserves sufficient contract clarity, authority, traceability, verification and assurance.**

〔v2.2 修改 V22-02〕本稿經明確採用後，與 Project Bindings 構成獨立有效的治理契約。Minimal v2.1、v2.0、v1.0 及更早版本、v2 母版僅供歷史參考，不補充本稿未定義的義務；已採用 v2.1、v2.0 或 v1.0 的專案在依第 5.3 節明確改採本版前，仍以其採用的版本為 frozen baseline。

**規範用語：**

- **MUST／MUST NOT**：必要要求，不得由 Skill、Runtime 或 Project Binding 豁免。
- **SHOULD／SHOULD NOT**：預設遵守；偏離須記錄理由，且不得違反 MUST。
- **MAY**：可選做法。

---

## 1. Governing Principles & Autonomous Execution

### 1.1 Five common invariants

以下五項適用於所有 execution paths；其完整規範以所引條文為唯一 authoritative definition：

1. **Autonomous orchestration** — 第 1.4、1.5、3.8 節。
2. 〔v2.2 修改 V22-03〕**Explicit roles and verifiable bindings** — 第 2.1–2.3、2.5–2.7 節。
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

- 〔v2.2 修改 V22-04〕Model replacement 或 capability escalation、lane selection、promotion、委派 bounded assignment，或 session 是否擔任角色，MUST NOT 改變角色權限（第 2.5–2.7 節）。

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

〔v2.2 修改 V22-05〕每個實際使用的治理 Agent 或 reusable Subagent MUST 有明確 definition，至少包含 responsibility／intended use、authority、prohibited authority，以及適用的 context／independence requirement。Definition 定義穩定權責；model assignment 由第 2.2 節的 Profile 提供，不以模型名稱或能力層（第 2.5 節）定義權限。

〔v2.2 修改 V22-06〕以下六個 governance roles MUST 保留。Reusable Subagents 依其 definition 在委派範圍內工作，不構成新增 governance role，也不因 reusable 或更換 model 取得新的 authority。在呼叫者委派的有界範圍內為其工作的 reusable Subagents（bounded assignments）另依第 2.6 節。

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
- 〔v2.2 新增 V22-07〕Capability escalation 的 trigger、escalated mapping 與範圍（Profile 宣告 escalation 時；第 2.5 節）。
- Binding verification mechanism 及證據位置。

Profile MAY 共用預設或引用既有設定，但每個可 dispatch identifier 的有效 mapping MUST 明確可解析。Project Bindings MUST 指定採用的 Profile 及 mapping 變更 authority；不強制另建 Profile 檔案或 schema。

〔v2.2 修改 V22-08〕Governance MAY 附版本化 Reference Model Profiles；新專案 MAY 直接採用某個 Profile＋version，例如 Reference Model Profile `default` v2（master repository 的 `references/model-profiles/default-v2.md`）。Project Bindings MUST 記錄採用的 Profile、版本與 overrides（無則明記無）；Profile 更新不自動影響既有專案。Profile 不改變任何 role authority 或 independence requirement，採用後的有效 mapping 仍須符合本節與第 5.1 節；Reference 中的 `TBD` 不構成有效設定。

實際 assignment 分兩種，核對的內容不同。

**被派工的 assignment。** 除下述兩種 root role session 外，每個實際 assignment——治理 Agent 與 reusable Subagent，不論由 operator、Orchestrator、direct-execution session 或 Harness 機制派工——MUST 透過可驗證機制綁定至宣告的 definition、model 及適用 effort／mode。

**Root role session。** 直接擔任治理角色、而不是被派工產生的 session。本治理只承認兩種：Orchestrator，以及 Lightweight direct execution 中擔任 Executor 的 session；其他直接擔任治理角色的 session 依前段為被派工的 assignment。Root role session MUST 具備：

1. **Activation basis。** Orchestrator：由 acceptor／operator 指定（designation），或由同一 run 中已啟動的 Orchestrator 依 rollover 交接的 successor 繼承該 designation 與 run identity；Orchestrator 不得自行假定。Direct-execution Executor：已成立的 Outcome Contract 接受與執行授權（第 1.2、3.5 節），並依其 assurance path 以 Lightweight lane 執行（第 3.1 節第 6 項、第 3.3 節）。Activation basis MUST 有可持久引用的紀錄。
2. **Model／effort runtime verification。** 該 session 實際的 model／version 與適用 effort／mode 等於其角色 identifier（`orchestrator`／`executor`）的有效 mapping，並可由 Runtime／Harness 證據核對。Orchestrator 在本項核對成立前不得派工。
3. **Role-definition grounding。** 以該角色的 definition（第 2.1 節）與適用契約為行事依據；re-ground 或 successor 接手時重新取得。
4. **Work identity and records。** Orchestrator：run identity（未啟動 run 時，為其 routing／派工所服務的 work item identity）與授權紀錄（第 3.4、5.1 節）。Direct-execution Executor：work item identity、第 3.7 節的 worklog 及其他適用的治理紀錄。

Root role session 如何建立——由 definition instantiate、一般 session 經 activation，或其他機制——屬 Runtime／Harness HOW；由 definition instantiate 不是必要條件。Project Bindings MAY 指定所採機制及其證據。第 3 項不證明第 2 項：讀取或載入 definition 不構成 model／effort 的核對。Root role session 派出的每個治理 Agent 與 reusable Subagent 都是被派工的 assignment。

〔v2.2 新增 V22-09〕不擔任任何治理角色的 session，以及 session 進入與離開角色，依第 2.7 節。

Prompt 中自稱角色、model 或「已綁定」，不構成 binding 證據；僅有設定存在也不等於實際 assignment 已符合。Designation 與 Outcome Contract 的接受／授權是 acceptor／operator 的 authority 行為，不是自稱。Designation 不構成 Outcome Contract 的接受或授權；兩者決定哪個 session 擔任該角色，不證明其 model／effort，也不授予第 2.1 節以外的權限。Runtime／Harness 或等效可觀察執行證據 MUST 足以核對實際 assignment，並可由工作或 audit records 引用。

〔v2.2 新增 V22-10〕核對的對象是 assignment 執行期間的實際 model／version 與 effort／mode，不只是開始時的狀態或設定值。以別名（alias）、預設值或其他可能隨平台更新而改變對應的方式指定 model 時，以該次執行的證據核對。平台可能在執行中自動切換 model 或 effort 時，核對 MUST 涵蓋該 assignment 產生的全部工作；自改變點起，未依第 2.5 節記錄 escalation、也未依本節記錄替代者，屬不符。

無法核對或不符的 binding MUST 修復或依授權替代；不得將該 assignment 冒充符合要求的 execution、review、adjudication 或 orchestration。

因不可用或執行失敗採取 replacement／substitution 時，MUST 引用當次嘗試的錯誤或當下可用性檢查證據，不得只憑記憶、先前 session／run 的不可用狀態跳過指定 Agent／model。主動更新 Profile 的依據與授權依第 5.3 節記錄。

替換 Profile 或 model 不改 definition 的 authority、independence、acceptance 或 audit bounds。Executor 與 Reviewer 是否使用不同 model，是採用的 Model Mapping Profile／Project Bindings 的 assurance policy 預設，不是第 2.3 節的 independence property；不同 model 不自動構成 independent review。依本節替代 model 時 MUST 維持第 2.3 節四項 properties，MAY 改變 model diversity 並記錄。

〔v2.2 新增 V22-11〕**Context independence 與 model diversity 分開陳述。** 前者只由第 2.3 節四項 properties 定義；後者是 assurance 觀察。Model diversity 只能依 binding 證據所示的實際 model 主張：兩個 assignment 的實際 model 相同時，MUST NOT 主張其間有 model diversity；同 model 的 fresh-context review 仍可以是合法的 independent review。陳述 model diversity 的紀錄 SHOULD 與 independence 的滿足方式分開記載（第 4.6 節），diversity 的任何結果都不改變 independence 的判定。依本節替代或依第 2.5 節 escalation 使原本成立的 model diversity 不再成立時，SHOULD 一併記錄。

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
- 〔v2.2 新增 V22-12〕Bounded assignment（第 2.6 節）所作的審查、驗證或意見，即使該 assignment 已依第 2.2 節綁定。

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

### 2.5 Model capability tiers, selection and escalation

〔v2.2 新增 V22-13〕本節規定 Model Mapping Profile 如何選擇 model 與 effort／mode、何時升級、何時替代。具體 model、能力層的實際分類與價格屬 Profile 與 non-normative Appendix E；本節與 model 及平台無關。

**能力層。** Profile MAY 將可用 model 歸入能力層（capability tier），並寫明各層的參考職責類別，作為選型依據。能力層與職責類別只是選型工具：model 或能力層 MUST NOT 定義或改變角色權限（第 1.3、2.1 節）；同一角色改用其他能力層，authority、independence requirement 與 audit bounds 不變（第 2.2 節）。

**選型原則。** Profile 為每個 identifier 選擇預設 model 與 effort／mode 時 SHOULD 考量：

1. **決策後果與可捕捉性。** 後果大、頻率低、錯誤難由後續步驟發現的判斷（設計語義、boundary determination、review 與裁決），優先配置較高能力；頻率高、錯誤可由 self-verification 與 independent audit 捕捉的工作（契約內實作、有界或機械工作），以足夠能力且成本較低的配置為預設，例外以 capability escalation 處理。
2. **Task class 與契約明確度。** Effort 主要影響 verification 的深度與邊界情況的處理；契約越明確，不同 effort 的產出差距通常越小。
3. **成本與延遲。**

成本與延遲 MAY 影響預設的選擇，但 MUST NOT 作為弱化 self-verification、必要 audit、第 2.3 節四項 properties 或任何 gate 的理由（第 1.5、5.2 節）。以成本為唯一理由降低 independent review 或 adjudication 角色的 model 或 effort，SHOULD NOT。

**能力不代替 routing。** 提高 model 能力或 effort 不能補齊契約缺口。語義、接受／授權或 boundary 的缺口 MUST 依第 2.4、3.3、3.6 節 route，不得以 escalation 代替。

**Capability escalation。** Profile MAY 為 identifier 宣告 capability escalation：指定條件成立時，以較高能力的 model 或較高 effort／mode 作為該次派工的有效 mapping。宣告時 MUST 寫明 trigger、escalated mapping 與適用範圍，使每次派工的有效 mapping 可依紀錄解析（第 2.2 節）。適用規則：

1. Trigger MUST 引用具體證據：可由紀錄機械判定的條件（例如 derivation／decision record 的標記、assurance policy 的類別、audit record 中的事實），或 Profile 指定的角色在自身紀錄寫明的具體能力需求。成本、偏好、「保險起見」或先前 session 的印象不是 trigger。
2. Orchestrator 或 direct-execution session 只機械套用 trigger 並派工，MUST NOT 自行判斷能力是否足夠（第 2.4 節）。
3. Escalation MUST NOT 改變 authority、新增 audit round 或構成 cycle reset（第 1.3、4.4、4.5 節）。以 escalated mapping 重派的 review 或 adjudication 是新的派工，MUST 使用 fresh context（第 2.3 節），且該輪仍只產生一份 verdict 或 ruling（第 4.4、4.5 節）。Review 或 adjudication 角色在作出 verdict 或 ruling 前，於自身紀錄提出 Profile 指定的 trigger 並因此不作 verdict 或 ruling 時，該次派工記為 escalation 紀錄，不計為第 4.4 節的 Alternate Review 或第 4.5 節的 Final Adjudication；以 escalated mapping 重派的 fresh assignment 所作的 verdict 或 ruling，才是該輪唯一的 Alternate Review 結論或 Final Adjudication 裁決。已作出 verdict 或 ruling 後，同一輪不再以 escalation 重派。
4. Escalation 紀錄存在時，escalated mapping 即為該次派工的有效 mapping，實際 assignment 依第 2.2 節以它核對。
5. Escalation SHOULD 有界：只適用於紀錄所指的 work item、question 或 audit cycle；每個 identifier 只有一個 escalation target，不串接；trigger 不再成立時，下一次派工回到預設。Escalated mapping 仍不足時，依第 2.4、3.6 節 route，不再升級。
6. 成本最高的能力層 SHOULD 以有界問題為單位使用（指名的 design question、Alternate Review 或 adjudication instance），不作為一般 execution 或控制面的預設，也不作為一般 escalation chain 的終點。

**Escalation 與替代分開。** Escalation 回答「需要更強的能力」，依據是能力證據；替代（第 2.2 節的 replacement／substitution）回答「指定 model 當次不可用」，依據是當次錯誤或可用性證據。兩者 MUST 分開記錄其依據，不得互相充當：可用性問題不是 escalation 的理由；替代規則中出現較高能力的 model，也不因此記為 escalation。Escalated mapping 當次不可用時，依 Profile 為該 escalated mapping 宣告的替代規則處理；替代規則用盡時，依第 1.5 節 recovery。

**Qualification-gated mapping。** 對尚未確認在採用平台可用或可正確綁定的 model，Profile MAY 將其 mapping 標為 qualification-gated，並宣告通過 qualification 前的 resolution。Resolution 使有效 mapping 明確可解析（第 2.2 節），MUST 記錄所適用的條件；它不是替代，不需要當次不可用的證據。

**Effort／mode 的變更。** Effort／mode 是有效 mapping 的一部分。已綁定的 assignment 只能經 Profile 宣告的 escalation 或新的派工改變 effort／mode，並記錄之；未記錄的變更即屬第 2.2 節的不符。需要「較低 effort 實作、較高 effort 驗證」的效果時，以角色分離（Executor 的 self-verification 與 independent review 各有 mapping）或宣告的 escalation 達成。

### 2.6 Bounded assignments

〔v2.2 新增 V22-14〕**Bounded assignment** 是在呼叫者委派的有界範圍內為其工作的 reusable Subagent（第 2.1 節）。常見類型包括：worker（有界、可由呼叫者核對的執行、擷取、轉換或機械修改）、investigator（唯讀調查與證據蒐集）與 advisor（方案比較、風險提示等第二意見，不作決定）。類型名稱、identifier 與 mapping 由 Profile 與 Project Bindings 決定；本節規定其治理地位。

1. **沒有 authority。** Bounded assignment 不是 governance role，不取得任何 governance authority（第 2.1 節），也不因 reusable、能力層較高或更換 model 而取得。
2. **Definition 與 binding。** 每個 bounded assignment MUST 有第 2.1 節的 definition 與第 2.2 節的明確 mapping，實際 assignment 依第 2.2 節綁定與核對。Definition SHOULD 另寫明委派範圍的邊界與允許的呼叫者。
3. **輸出是待驗證的輸入。** Bounded assignment 的輸出是呼叫者的輸入與待驗證主張，MUST NOT 構成 finding、verdict、ruling、design decision、derivation、boundary determination、接受、授權或 audit record。呼叫者 MUST 自行核對後才使用，並對據以作出的決定與其紀錄負全責。
4. **決定不外包。** 呼叫者 MAY 以 bounded assignment 的輸出作為參考，但需要 authority 的決定 MUST 由呼叫者以自己的角色作出並寫入自身紀錄（第 1.3、2.3 節），不得讓 bounded assignment 代為作成。
5. **不構成正式 review 或裁決。** 正式 independent review 與 adjudication 只能由依第 2.2、2.3 節綁定的 Reviewer 或 Final Adjudicator 執行；Executor 使用 bounded assignment 屬 self-verification（第 2.3 節）。Reviewer 或 Final Adjudicator 使用 bounded assignment 時 MUST 維持第 2.3 節四項 properties：自行取得受審產物，不以 Executor 挑選或摘要的輸入限制範圍，結論由本角色判斷並寫入。
6. **Orchestrator 的使用。** Orchestrator MAY 以 bounded assignment 處理控制面工作（例如狀態擷取、紀錄整理），MUST NOT 藉以取得第 2.4 節禁止 Orchestrator 作的判斷。Profile MAY 進一步限制 Orchestrator 可呼叫的類型。
7. **範圍。** Bounded assignment MUST NOT 自行擴大委派範圍、派工治理角色，或以任何角色的名義作成其紀錄；超出範圍的需要回報呼叫者，由呼叫者處理或依第 2.4 節 route。
8. **紀錄。** Bounded assignment 的動作是呼叫者所屬 work item 的執行證據，不另成 work item（第 3.7 節）。呼叫者 SHOULD 在其 worklog 或 record 引用所用的 bounded assignment、其 binding 證據與輸出的採用方式。

### 2.7 Session role activation and role-less sessions

〔v2.2 新增 V22-15〕Session 是否擔任治理角色，由 activation basis 與 binding 決定，不由 session 的位置（例如使用者直接開啟的 main session）或自稱決定。

1. **無角色 session。** Session MAY 不擔任任何治理角色，只作為一般互動、工作入口（接收請求、與 acceptor 釐清、查詢與說明）或派工協調介面。
2. **不取得 authority。** 無角色 session MUST NOT 被推定為 Executor、Design Authority、Orchestrator 或任何其他角色，也不取得或行使任何治理 authority：不接受或授權工作（第 1.2 節），不作設計或 boundary 決定，不作 findings 或裁決，也不行使第 2.4 節的 routing 決定。
3. **派工。** 無角色 session MAY 作為派工介面；它派出的治理 Agent 與 reusable Subagent 仍 MUST 各自符合第 2.2 節，independent review 與 adjudication 的派工另 MUST 符合第 2.3 節（含派工來源）。這類派工不構成任何角色的 activation basis，也不使該 session 成為 Orchestrator；Formal run 的派工與 routing 仍屬 Orchestrator（第 2.4、3.4 節）。
4. **受治理的工作以角色進行。** 執行 accepted Work Contract 的工作 MUST 由相應角色進行：該 session 依第 2.2 節成為 root role session（只限 Orchestrator 與 Lightweight direct-execution Executor），或派工相應角色。無角色狀態 MUST NOT 被用來繞過接受與授權、worklog（第 3.7 節）、binding、audit applicability（第 4.1 節）或其他治理要求。
5. **進入角色。** Session 進入角色 MUST 明確為之，自進入時起適用該角色的規範。Root role session 在開始角色工作前 MUST 具備第 2.2 節四項；進入點 SHOULD 記入該角色的紀錄（Orchestrator 的 run record、Executor 的 worklog）。Session 實際的 model／effort 不等於該角色的有效 mapping 時，不能藉進入角色成為合格的 root role session，依第 2.2 節修復，或改由符合 mapping 的 session 擔任。
6. **一次一個角色。** Root role session 擔任角色期間，MUST NOT 同時行使其他角色的 authority；需要其他 authority 時依第 1.4、2.4 節派工或 route。同一執行 context 不得轉名為 Reviewer（第 2.1 節）。
7. **離開角色。** Work item 結束、activation basis 失效或 run 結束時，該 session 的角色隨之結束；之後的互動不再是該角色的工作，除非依第 5 項重新進入。
8. **紀錄。** 無角色 session 寫下的內容不構成任何角色的治理紀錄。它 MAY 依 acceptor 或 operator 的明確指示轉錄其決定，紀錄 MUST 標明決定者；轉錄不使該 session 取得該 authority（第 5.3 節）。純詢問與尚未成為 accepted execution 的探索不產生 worklog 義務（第 3.7 節）。

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
| 〔v2.2 修改 V22-16〕**Executing role and binding reference** | 執行角色與實際 binding 證據引用，含適用的 escalation 與替代紀錄（第 2.2、2.5 節）；不要求複製 Harness 日誌。 |
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
- 〔v2.2 新增 V22-17〕陳述 model diversity 時，其所依據的各 assignment 實際 model（第 2.2 節）。
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
| 〔v2.2 修改 V22-18〕**Agent／Subagent definitions and Model Mapping Profile** | 六治理角色與所有實際使用的 reusable Subagent definitions（含 bounded assignments，第 2.6 節）；採用的 Profile、每個可 dispatch identifier 的有效 mapping 與驗證機制（含 root role session 依第 2.2 節核對 model／effort 的方式與證據位置）；採用的 capability escalation 與 qualification-gated resolution（若有，第 2.5 節）；符合第 2.3 節四項 properties 的 independent dispatch 機制及其滿足方式。 |
| **Lane policy** | 預設分類、適用 Formal 要求及模糊情況的決定者；不得取代第 3.3、3.6 節。 |
| 〔v2.2 修改 V22-19〕**Assurance policy** | Lightweight audit 預設與觸發條件、高風險類別（第 4.5 節 disposition 邊界所引用）、適用 integration／release gates、第 4.7 節單 Ticket fast path 是否採用及其核對方式、model diversity 預設（第 2.2 節）、以 assurance 類別作為 capability escalation trigger 時的宣告（若有，第 2.5 節）。 |
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
- 〔v2.2 新增 V22-20〕讓 bounded assignment 或無角色 session 取得治理 authority，或以其產出代替必要的 independent audit、裁決或其他角色的決定（第 2.6、2.7 節）。
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
- 〔v2.2 新增 V22-21〕具體 model、能力層的實際分類、價格、effort／mode 等級名稱、alias、escalation trigger 的具體條件與替代順序，以及 bounded assignment 的具體類型與 identifier（屬 Profile、Project Bindings 與 non-normative Appendix E）。

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
| v2.2 | 2026-10-12 | Adopted／Frozen | operator 2026-10-12 指示起草的通用母版：延續 v2.1，整合模型能力分層與選型、capability escalation、bounded assignments、session 角色啟用與無角色 session；independent review A1（Codex R1 → targeted correction → R2 → correction → Alternate Review：CLOSED）→ operator 授權採用（詳 Appendix D.8、D.9） |

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

本附錄自 v2.1 原樣保留；其中的「本檔」「本版」指 v2.1。

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

## Appendix D · v2.1 → v2.2 change ledger 與 Candidate record（non-normative）

本附錄不新增規則；規範以第 1–5 節為準。

### D.0 Baseline, sources and drafting

**基線：** Minimal Operational Governance v2.1（Adopted／Frozen 2026-10-01；2026-10-02 header metadata update）。權威基礎為 Notion 上的「Minimal Operational Governance — v2.1」（所屬 package 頁「Minimal Governance — Reusable Package v2.1」）。起草使用其原檔的位元複本：整檔 md5 `d4d458eeb6d571f1f4f3f0cc607feac9`，與 Notion package 頁公布的值相同；§1–§5 body（自「## 1.」起至 Appendix A 標題前，含其後的空行）md5 `9113074ad8f7a586ae9a77c4a80ac5d1`，與 C.4 公布的值相同。本 Candidate 由該檔逐位元複製後，只作 D.2 所列修改；v2.1 檔案與 Notion 頁面都未改動。

**設計來源：**

| ID | 來源 | 取用的內容 | 不取用 |
|---|---|---|---|
| S-0 | Minimal v2.1 本身 | 新增規範用語所依據的既有條文（D.3） | — |
| S-A | Reference Model Profile `default` v2.5（Adopted／Frozen 2026-10-11）§1、§2.2、§3.1、§4.1、§5、§6、§8 | Bounded assignments 的地位與輸出性質；capability escalation 的 trigger 類型（機械／宣告）、決定者、範圍、單步、與 availability fallback 分開；qualification-gated resolution；context independence 與 model diversity 分開、同 model 不主張 diversity；以 alias 派工時逐次核對 | 具體 mapping、effort、identifier 名稱、trigger 與 fallback 的編號和內容、diversity 關係的編號、價格（價格只在 Appendix E 作參考） |
| S-B | 官方模型使用建議：Anthropic《Using Claude Code: Spending your effort》（2026-09-25）、《The new rules of context engineering for Claude 5 generation models》（2026-07-24）、《Getting the most out of Opus 5.5 in Claude and Claude Code》（2026-09-22），以及據此整理的 operating guidance reference v1（2026-10-05） | Effort 主要提升 verification 與邊界情況的處理，不修正錯誤方向；契約越明確，effort 差距越小；平台在訊息被 flag 時自動切換 model 的 binding 風險；subagent 的輸出須核對證據；同 session 內的 review 屬 self-verification | 作者個人的經驗法則與範例不升格為規範；Claude Code 的指令、設定與 mods 屬 Runtime HOW |
| S-C | 目前有效治理設計中的通用原則：一個採用 v2.1 的專案於 2026-10-12 依其 acceptor 指示，在 Project Bindings 加入的「無角色 session」釐清；同期 Profile 修訂對「同 model 組合不主張 diversity」的處理 | 無角色 session 可作互動入口、不取得 authority、其派工不構成 activation basis、受治理的工作須以角色進行、不得繞過授權與 audit | 該專案的 Bindings 條文、路徑、啟動指令、definitions、hooks、scripts、實際 mapping 與決策紀錄 |
| S-D | Artificial Analysis Intelligence Index（第三方 benchmark，擷取 2026-10-06） | 只用於 Appendix E 的能力與成本參考 | 不作為規範依據 |

**起草：** 2026-10-12，Opus 5.5（`claude-opus-5-5`）session，依 operator 指示。指示要點：以 v2.1 為權威基礎；延續其結構、規範風格與核心原則；整合模型能力分層與 Fable／Opus／Sonnet／Haiku 的參考職責分類、model／effort selection、escalation 與成本品質權衡、workers／advisors 的有界委派、role binding、independent review 與 session role activation、無治理角色的 main session；只納入通用原則；具體模型放 non-normative 附錄；保留 v2.1 全部要求；逐條標明新增、修改與繼承並附來源與理由，不把專案實作升格為 MUST；v2.2 暫不採用。未經 independent review。

### D.1 分類

| 狀態 | 意思 |
|---|---|
| 繼承 | 與 v2.1 逐字相同 |
| 修改 | 改寫或增補 v2.1 的段落、表列或項目；原文見 v2.1 |
| 新增 | v2.1 沒有的段落、表列、項目或小節 |
| Metadata | 非規範的 header 與附錄 |

### D.2 逐條帳

| 條文 | 狀態 | ID | 變更 | 來源 | 理由 |
|---|---|---|---|---|---|
| 文首 header | Metadata | V22-01 | 標題、狀態、版本、日期、基線（含 hash）、Candidate 的效力、標示說明、package references；移除 v2.1 的 visualization 句 | — | Candidate 身分與可攜性：不依賴 master repository 的相對連結 |
| 文首兩段引言、規範用語 | 繼承 | — | — | — | — |
| 文首「本稿經明確採用後…」 | 修改 | V22-02 | 歷史版本列入 v2.1；「已採用 v2.0 或 v1.0 的專案」改為「已採用 v2.1、v2.0 或 v1.0 的專案」 | S-0（v2.1 同段） | 版本更替；語義同 v2.1 該段 |
| §1.1 | 修改 | V22-03 | Invariant 2 的引用加入第 2.5–2.7 節 | — | 新小節屬 explicit roles and verifiable bindings |
| §1.2 | 繼承 | — | — | — | — |
| §1.3 | 修改 | V22-04 | 第一項加入 capability escalation、委派 bounded assignment、session 是否擔任角色 | S-0 §1.3、§2.1、§2.2；S-A §2.2、§3.1；S-C | 把「換 model 不改權限」延伸到本版新增的三種機制，避免它們被讀成 authority 的來源 |
| §1.4、§1.5 | 繼承 | — | — | — | — |
| §2.1 第一段 | 修改 | V22-05 | 「不以模型名稱定義權限」加「或能力層（第 2.5 節）」 | S-A §2.1 | 能力層是本版新增的選型概念，明示它不定義權限 |
| §2.1 第二段 | 修改 | V22-06 | 段末加一句：bounded assignments 另依第 2.6 節 | S-A §2.2 | Bounded assignments 是 reusable Subagents 的一類 |
| §2.1 角色表與其後各段 | 繼承 | — | — | — | — |
| §2.2 mapping 內容清單 | 新增項目 | V22-07 | 新增「capability escalation 的 trigger、escalated mapping 與範圍（Profile 宣告時）」 | S-A §3.1 E-7 | Escalation 使有效 mapping 隨紀錄而定；列入 mapping 才能依 v2.1「有效 mapping MUST 明確可解析」解析 |
| §2.2 Reference Profiles 段 | 修改（編輯） | V22-08 | `default v2` 的相對連結改為不依賴位置的寫法，語義不變 | — | 可攜性 |
| §2.2 root role session 段後 | 新增 | V22-09 | 一句：不擔任角色的 session 與進出角色依第 2.7 節 | S-C | 指向新小節 |
| §2.2 binding 證據段後 | 新增 | V22-10 | 核對涵蓋執行期間的實際 model 與 effort／mode；alias、預設值與平台自動切換的處理 | S-A §6；S-B（Opus 5.5 文章的 flagged message 自動切換；operating guidance F-01） | 自動切換與 alias 漂移是 v2.1 binding 要求下已知的失效方式 |
| §2.2 model diversity 段後 | 新增 | V22-11 | Independence 與 model diversity 分開；同 model 不得主張 diversity；分開記載與記錄 diversity 的失去（SHOULD） | S-A §5；S-C | Diversity 只能以實際 model 主張；同 model 的 fresh-context review 仍是合法的 independent review |
| §2.2 其餘各段 | 繼承 | — | 含 mapping 內容清單其餘項、Profile 採用、兩種 assignment、root role session 四項、prompt 自稱、修復／替代、替代證據、model diversity 原段 | — | — |
| §2.3 self-verification 清單 | 新增項目 | V22-12 | Bounded assignment 的審查、驗證或意見，即使已綁定 | S-A §2.2；S-0 §2.1、§2.3 第 2 項 | Bounded assignment 不是 Reviewer，明列以免被當成正式 audit |
| §2.3 四項 properties 與其他各段 | 繼承 | — | — | — | — |
| §2.4 | 繼承 | — | — | — | — |
| §2.5 | 新增 | V22-13 | 能力層；選型原則三項；成本不得用來弱化 assurance；能力不代替 routing；capability escalation 與六項規則；與替代分開；qualification-gated mapping；effort／mode 的變更 | S-A §1、§2.2、§3.1、§3.2、§4.1；S-B | 指示要求的模型能力分層、model／effort selection、escalation 與成本品質權衡；用語推導見 D.3。規則 3 末三句（作 verdict／ruling 前提出 trigger 的派工如何計數）是 A1 R1 finding F3 的修正（D.8），只把第 4.4 節「exactly one Alternate Review」與第 4.5 節單一 ruling 套用到 escalation，未新增 round |
| §2.6 | 新增 | V22-14 | Bounded assignment 的定義、常見類型與八項 | S-A §2.2；S-B（subagent 的輸出須核對證據） | 指示要求的 workers／advisors 有界委派；用語推導見 D.3 |
| §2.7 | 新增 | V22-15 | Session 角色啟用與無角色 session 八項 | S-C；S-0 §1.4、§2.2、§3.7 | 指示要求的 session role activation 與無角色 main session；用語推導見 D.3 |
| §3.1–§3.6 | 繼承 | — | — | — | — |
| §3.7 worklog 表 | 修改 | V22-16 | 「Executing role and binding reference」加「含適用的 escalation 與替代紀錄」 | S-A §8 | Escalation 改變該次的有效 mapping；binding 引用須能指出依哪個 mapping 核對 |
| §3.7 其餘、§3.8 | 繼承 | — | — | — | — |
| §4.1–§4.5 | 繼承 | — | — | — | — |
| §4.6 | 新增項目 | V22-17 | Audit record 陳述 model diversity 時，記下所依據的實際 model | S-A §5 | 使 V22-11 可由紀錄核對 |
| §4.7 | 繼承 | — | — | — | — |
| §5.1 表 | 修改 | V22-18、V22-19 | Definitions／Profile 列加入 bounded assignments、capability escalation 與 qualification-gated resolution（若有）；Assurance policy 列加入以 assurance 類別作 escalation trigger 的宣告（若有） | S-A §2.2、§3.2 | 新機制在 Bindings 中有宣告的位置；條件性項目，未採用者不需宣告 |
| §5.1 其餘 | 繼承 | — | — | — | — |
| §5.2 Bindings 禁止清單 | 新增項目 | V22-20 | Bindings 不得讓 bounded assignment 或無角色 session 取得 authority，或以其產出代替必要 audit、裁決或其他角色的決定 | S-0 §5.2 | 與既有「不得擴張 authority」「不得將 self-verification 冒充 independent audit」同類 |
| §5.2 其餘、§5.3 | 繼承 | — | — | — | — |
| §5.4 | 新增項目 | V22-21 | 治理不規定具體 model、能力層分類、價格、effort 名稱、alias、trigger 條件、替代順序與 bounded assignment 類型 | 指示第 2 項 | 核心規範與 model 及平台無關 |
| Appendix A.1 | Metadata | V22-22 | 新增 v2.2 Candidate 列 | — | 版本沿革 |
| Appendix A 其餘、Appendix B | 繼承 | — | — | — | — |
| Appendix C | Metadata | V22-23 | 標題下新增一行說明（本附錄自 v2.1 原樣保留） | — | 與 Appendix B 的處理一致；C 的正文繼承 |
| Appendix D | Metadata | V22-24 | 本附錄 | — | — |
| Appendix E | Metadata | V22-25 | 模型能力分層與參考職責分類 | S-A、S-B、S-D | 指示第 2 項：具體模型與建議分類放 non-normative 附錄 |

### D.3 新增規範用語的推導

「推論」表示該句是 v2.1 既有 MUST 的直接推論，不新增獨立義務；「設計建議」與「設計選項」是本版新增的 SHOULD 或 MAY，來自 S-A 或 S-B。本版沒有把任何專案實作寫成 MUST。

| 位置 | 用語與內容 | 依據 | 性質 |
|---|---|---|---|
| §1.3（V22-04） | MUST NOT：escalation、委派 bounded assignment、session 的角色狀態不改變角色權限 | §1.3；§2.1 第二段；§2.2「替換 Profile 或 model 不改 definition 的 authority」 | 推論 |
| §2.2（V22-07） | MUST：Profile 宣告的 escalation 列入 mapping | §2.2「有效 mapping MUST 明確可解析」 | 推論 |
| §2.2（V22-10） | MUST：核對涵蓋 assignment 產生的全部工作；未記錄的改變屬不符 | §2.2：實際 assignment MUST 綁定；證據 MUST 足以核對；不符 MUST 修復或替代 | 推論 |
| §2.2（V22-11） | MUST NOT：同 model 不主張 diversity | §2.2「不同 model 不自動構成 independent review」「Prompt 中自稱…不構成 binding 證據」；§4.5「不得虛報」 | 推論（陳述須真實） |
| §2.2（V22-11） | SHOULD：分開記載；記錄 diversity 的失去 | S-A §5、§8 | 設計建議 |
| §2.3（V22-12） | 清單新項：屬 self-verification | §2.1 第二段；§2.3 清單第 2 項 | 推論 |
| §2.5 能力層 | MAY：Profile 定義能力層；MUST NOT：model 或能力層定義權限 | §1.3、§2.1 | MAY 為設計選項；MUST NOT 為推論 |
| §2.5 選型原則 | SHOULD：考量決策後果與可捕捉性、task class 與契約明確度、成本與延遲 | S-A §2.2 選型依據；S-B effort 文章 | 設計建議 |
| §2.5 成本 | MAY：影響預設；MUST NOT：作為弱化 assurance 的理由 | §1.5 末段；§5.2「不得弱化…」 | MAY 為設計選項；MUST NOT 為推論 |
| §2.5 成本 | SHOULD NOT：只因成本降低 review／adjudication 的 model 或 effort | S-A §3.1 E-9 | 設計建議（沿用 S-A 的強度） |
| §2.5 routing | MUST：缺口依第 2.4、3.3、3.6 節 route，不以 escalation 代替 | §2.4、§3.3、§3.6 | 推論 |
| §2.5 escalation | MAY：宣告 escalation；MUST：寫明 trigger、mapping、範圍 | §2.2 有效 mapping 可解析 | MAY 為設計選項；MUST 為推論 |
| §2.5 escalation 第 1 項 | MUST：trigger 引用具體證據 | §2.2 替代 MUST 引用當次證據、不得只憑記憶；同一證據原則用於有效 mapping 的另一種改變 | 推論 |
| §2.5 escalation 第 2 項 | MUST NOT：Orchestrator 判斷能力是否足夠 | §2.4：Orchestrator MUST NOT 判斷 evidence sufficiency | 推論 |
| §2.5 escalation 第 3 項 | MUST NOT：改變 authority、新增 round、cycle reset；MUST：fresh context、一份 verdict／ruling | §1.3；§2.3 第 1 項；§4.4 exactly one Alternate、不得增加 R3／R4；§4.5「換 model 不構成 reset 理由」 | 推論 |
| §2.5 escalation 第 5、6 項 | SHOULD：有界、單步、回到預設、不再升級；成本最高的能力層以有界問題為單位 | S-A §3.1 E-3、E-4、E-5 | 設計建議 |
| §2.5 替代 | MUST：escalation 與替代分開記錄依據 | §2.2 替代 MUST 引用當次證據；§5.3 變更 MUST 留下依據 | 推論 |
| §2.5 qualification | MAY：qualification-gated；MUST：記錄所適用的條件 | §2.2「`TBD` 不構成有效設定」、有效 mapping 可解析 | MAY 為設計選項；MUST 為推論 |
| §2.5 effort／mode | 未記錄的變更屬不符（無新用語） | §2.2 | 推論 |
| §2.6 第 1、2 項 | 無 authority；MUST：definition 與 mapping；SHOULD：寫明範圍與呼叫者 | §2.1、§2.2；S-A §2.2 | 推論；SHOULD 為設計建議 |
| §2.6 第 3、4 項 | MUST NOT：輸出構成 finding 等；MUST：呼叫者核對、負責、以自己的角色決定與記錄；MAY：作為參考 | §1.3；§2.1 第二段；§2.3 第 1、4 項 | 推論 |
| §2.6 第 5 項 | 正式 review／裁決只由綁定的角色執行；MUST：維持四項 properties | §2.3 | 推論 |
| §2.6 第 6 項 | MAY：Orchestrator 用於控制面；MUST NOT：取得禁止的判斷；MAY：Profile 限制呼叫者 | §2.1 Orchestrator 列；§2.4 | 推論；MAY 為設計選項 |
| §2.6 第 7 項 | MUST NOT：擴大範圍、派工治理角色、以角色名義作成紀錄 | §2.1 第二段：在委派範圍內工作、不取得 authority | 推論 |
| §2.6 第 8 項 | SHOULD：在 worklog 或 record 引用 | §3.7；S-A §8 | 設計建議 |
| §2.7 第 1 項 | MAY：session 不擔任角色 | §3.7 第 3 項（純詢問不產生 worklog，表示不受治理的互動本來就存在）；S-C | 設計選項（釐清） |
| §2.7 第 2 項 | MUST NOT：被推定為角色、取得或行使 authority | §1.3；§2.1；§2.2（root role session 只有兩種；activation basis 是 acceptor／operator 的行為，不得自行假定） | 推論 |
| §2.7 第 3 項 | MAY：作為派工介面；MUST：派工符合第 2.2、2.3 節；不構成 activation basis | §2.2、§2.3、§2.4 | MAY 為設計選項；其餘為推論 |
| §2.7 第 4 項 | MUST：受治理的工作以角色進行；MUST NOT：以無角色繞過要求 | §1.2；§1.4；§3.7「worklog 義務跟著 work item，不跟著執行者類型」；§4.1 | 推論 |
| §2.7 第 5 項 | MUST：明確進入、具備四項；SHOULD：記錄進入點 | §2.2 第 1–4 項 | 推論；SHOULD 為設計建議 |
| §2.7 第 6 項 | MUST NOT：同時行使其他角色的 authority | §1.4「不得自行兼任未授權的決定者」；§2.1 | 推論 |
| §2.7 第 8 項 | MAY：依指示轉錄；MUST：標明決定者 | §1.2 權威紀錄；§5.3「代理寫入接受或核准紀錄，不等於取得該 authority」 | MAY 為設計選項；MUST 為推論 |
| §3.7（V22-16） | MUST（worklog 表內容）：binding 引用含 escalation 與替代紀錄 | §2.2、§3.7 | 推論 |
| §4.6（V22-17） | MUST（audit record 可識別）：陳述 diversity 時記下實際 model | §2.2（V22-11）、§4.6 | 推論 |
| §5.1（V22-18、V22-19） | MUST（bindings 就緒）：條件性項目，若有則宣告 | §5.1 | 推論 |
| §5.2（V22-20） | MUST NOT：Bindings 讓 bounded assignment 或無角色 session 取得 authority 或代替 audit | §5.2 既有清單 | 推論 |

### D.4 未變更

D.2 標為「繼承」的條文與 v2.1 逐字相同。v2.1 的每一句 MUST／MUST NOT、SHOULD／SHOULD NOT、MAY 都保留，沒有刪除或弱化；修改只增補或改寫引用，不改變原有義務。本版未新增 governance role、lane、audit round、approval layer 或 operator gate，也未新增任何特定 model、平台、harness 或 CLI 的要求。

繼承的 Appendix A–C 中的連結是 master repository 的相對路徑，只在 master repository 中可解析；它們指向歷史紀錄，不承載規範內容。

### D.5 刻意不納入的內容

- 任何專案的 Project Bindings 內容：reserved boundaries、overrides、高風險類別、standing authorizations、採用紀錄與其編號。
- Agent definitions 的檔名、內容與 frontmatter；hooks；runtime scripts；路徑；啟動指令與參數。
- 任何專案的實際 mapping（哪個角色使用哪個 model 與 effort）、歷史決策與 acceptor 指示原文。
- 具體 model 與版本：只出現在 non-normative 的 Appendix E 與本附錄的來源欄。
- 官方文章中作者個人的經驗法則與範例：只在 Appendix E 作參考，不升格為規範。

### D.6 一致性檢查

起草完成時執行：

| # | 檢查 | 結果 |
|---|---|---|
| 1 | 與 v2.1 逐行比對：v2.1 的每行文字在本檔逐字存在，或在 D.2 標為修改 | PASS：v2.1 的 813 行中 16 行不是逐字存在，即文首 header 7 行（V22-01）與 9 行修改（V22-02～V22-06、V22-08、V22-16、V22-18、V22-19） |
| 2 | v2.1 §1–§5 的每一句 MUST／SHOULD／MAY 在本檔保留 | PASS：只有兩句不是逐字存在：§1.3 第一項（V22-04，只擴大列舉，MUST NOT 不變）與 §2.2 Reference Profiles 段的 MAY 句（V22-08，只改連結寫法）。逐字差異只有刪去一個「或」與連結符號 |
| 3 | 每個〔v2.2 …〕標示在 D.2 有對應列，D.2 的每個 ID 在本文或附錄存在 | PASS：本文 20 個標示（V22-02～V22-21）各有對應列，無重複；其餘 5 個 ID（V22-01、V22-22～V22-25）是 metadata |
| 4 | 文首與第 1–5 節的「第 x.y 節」與「§x.y」引用都指向存在的小節 | PASS：全部可解析。Appendix D 中標 S-A 的 §x.y 指 Reference Model Profile `default` v2.5 的章節 |
| 5 | 本文不含任何專案名稱、專案路徑、專案 ID 或實際 mapping | PASS：以專案名稱、本機路徑、專案紀錄與 Bindings 的編號格式、agent definition 路徑、專案 Profile 的 trigger／fallback 編號搜尋，沒有命中 |
| 6 | 本檔的連結：文首與第 1–5 節沒有相對連結；附錄的外部來源為完整 URL | PASS：連結只在繼承的 Appendix A–C（master repository 的相對路徑，見 D.4）；Appendix E 的來源是完整 URL |

### D.7 Candidate 狀態與待採用決定

| 項目 | 內容 |
|---|---|
| 狀態 | **Adopted／Frozen**（2026-10-12；D.9）。本表的待決事項已由 operator 2026-10-12 的指示決定，見 D.9 |
| 待決 1 | 採用前是否執行 independent review（v2.0、v2.1 都在 independent review 與修正後才採用） |
| 待決 2 | 是否採用 v2.2：operator 依第 5.3 節明確授權。Adoption edits 建議只限 metadata／record：header 狀態、A.1 v2.2 列、本附錄的採用紀錄，並可一併移除〔v2.2 …〕標示 |
| 待決 3 | Package references：是否把 Reference Model Profile `default` v2.5 或其後的 Profile 納入 master package，並讓其 header 標示的治理版本改為 v2.2 |
| 待決 4 | Implementation Profile 與 Reference Orchestrator Contract 是否需要配合修訂（例如 Orchestrator 如何套用 escalation trigger、Executor 如何使用 bounded assignments）。本 Candidate 不修改它們 |
| 待決 5 | 對應的 visualization（加日期的 HTML） |
| 採用效果 | 依第 5.3 節：新版本不自動適用既有工作；已採用 v2.1 的專案須明確 re-pin，並處理進行中 assignments、audit 與 evidence coverage |

### D.8 Independent review 與修正紀錄

| 日期 | 事件 |
|---|---|
| 2026-10-12 | A1 R1：Codex（`gpt-6-sol`／`xhigh`）adversarial review，verdict needs-attention，三項 blocking：F1（V22-10 的全程核對在 companion 與專案 Bindings 中沒有對應程序）、F2（起草 assignment 的 binding 不符且未修復）、F3（第 2.5 節 escalation 與「exactly one Alternate Review」的計數未定義） |
| 2026-10-12 | Targeted correction（合格的 Executor：Opus 5.5／`high`）：F3 → 第 2.5 節規則 3 補充計數規則（V22-13）；F1 → 本檔條文不變，Reference Orchestrator Contract 另出 `orch-default` v2.2，把 model／effort 核對延伸到整個 assignment 與 root role session 的全程；採用專案的 Bindings 在改採時對應；F2 → 合格的 Executor 依起草 contract 重新核對全文（D.6 六項重跑，結果與起草時相同），並在起草 worklog 補記承接 |
| 2026-10-12 | A1 R2：Codex（`gpt-6-sol`／`xhigh`）closure review，verdict needs-attention：F2、F3 RESOLVED；F1 UNRESOLVED（A1R2-F1：`orch-default` v2.2 的全程核對只是 SHOULD，不構成 gate）。依第 4.4 節不另開 R3，進入一次 Alternate Review |
| 2026-10-12 | A1R2-F1 的定點修正：`orch-default` v2.2 §3 的核對設為採用 return 與作 routing、gate、persist、completion 依據前的 MUST gate，無法確立涵蓋時 fail closed；§11 要求 Bindings 宣告可逐筆觀察的證據來源。本檔條文不變 |

### D.9 Adoption／Freeze record

| 項目 | 內容 |
|---|---|
| 狀態 | **Adopted／Frozen**（2026-10-12，operator 明確授權） |
| Operator 決定 | 2026-10-12 指示「Minimal Governance v2.2 Full Adoption & Workspace Migration」：確認採用完整的 v2.2 變更方向（含第 2.5–2.7 節與其他全部新增或修訂）；independent review 由 Codex 擔任，closure 後正式採用並凍結；Reference Model Profile default v2.5 納入 Reusable Package v2.2 作為跨專案參考預設；impl-default v2、orch-default v2.1 檢查相容性，實質衝突時作最小必要修正 |
| D.7 待決事項的決定 | 1：執行 independent review（A1）。2：採用。3：package Profile 為 default v2.5（以引用方式沿用的 default v2.4 一併保留）。4：impl-default v2 相容、不修改；orch-default 出 v2.2（A1 F1 的修正）。5：建立 v2.2 visualization |
| Independent review | A1：Codex（`gpt-6-sol`／`xhigh`）R1 needs-attention（F1、F2、F3 blocking）→ targeted correction → R2（F2、F3 RESOLVED，F1 剩餘）→ correction → Alternate Independent Review（Opus 5.5／`xhigh`）：**CLOSED**，無未解 blocking，不需 Final Adjudication（D.8） |
| Closure subject | 本檔 sha256 `01a9542a6d254b3a3469429144503d8167385e650c0d799dd03c858ae84078b9`；§1–§5 body（自「## 1.」起至 Appendix A 標題前，含其後的空行）md5 `5a407bebc0a50299b08371418d854c81` |
| Adoption edits | 限 metadata／record：標題與文首狀態、版本、日期、效力段（含 visualization 檔名）、標示段的一句、package references 段（改指 default v2.5、impl-default v2、orch-default v2.2）、Appendix A.1 v2.2 列、D.7 狀態列與本節。〔v2.2 …〕標示保留。§1–§5 body 與 closure subject 逐位元相同（body md5 `5a407bebc0a50299b08371418d854c81`） |
| Companion | Reference Orchestrator Contract orch-default v2.2（同日 Adopted／Frozen；A1 F1 的修正）。Reference Model Profile default v2.5、v2.4 與 impl-default v2 不變 |
| 權威位置 | 原 master repository 自 2026-10-11 起不在起草環境的本機；Reusable Package v2.2 暫以起草所在工作區的 `master_governance/` 為權威位置，Notion 為發布／導航副本。原 repository 恢復時以 hash 比對後放回 |
| 採用效果 | 依第 5.3 節：不自動適用任何專案；已採 v2.1 或更早版本的專案須明確 re-pin，並處理進行中 assignments、audit 與 evidence coverage。本檔 frozen；之後任何變更依第 5.3 節留下版本、依據與授權，以新版本承載 |

## Appendix E · Reference model capability tiers and responsibility classes（non-normative）

本附錄不新增規則，也不是任何專案的 mapping。內容反映 2026-10-12 以前可取得的資料；model、平台或價格更新後須重新核對。專案的實際 mapping 由其採用的 Profile 與 Project Bindings 決定（第 2.2、5.1 節），binding 以專案自身的 runtime 證據驗證。

### E.1 能力層與參考職責分類（Anthropic Claude 5 世代）

| 層 | Model（model id） | 定位與已知特性 | 參考職責類別 | 不建議用於 |
|---|---|---|---|---|
| 困難推理（有界使用） | Fable 5.1（`claude-fable-5-1`） | 官方定位為 demanding reasoning、long-horizon agentic work；Terminal-Bench 3.0 中，effort 提升對 security、hardware、ML 類任務的增益最大；四者中價格最高；在 Claude 產品中，safeguards 會把部分 security 請求轉給 Opus | 以現有證據無法裁決的指名 design question；寫明具體能力缺口的 Alternate Review 或 adjudication instance；Design Authority 或 Final Adjudicator 對這類問題的諮詢。以 capability escalation 的有界問題為單位 | 一般 execution、控制面、機械工作的預設；只為 model diversity 或「保險起見」而派工 |
| 高能力通用 | Opus 5.5（`claude-opus-5-5`） | 官方指出它最大的進步在多步驟工作一路做到完成；always-on thinking，以 effort 調整深度；API 預設 effort `medium`；在第三方綜合指數中，`high`、`xhigh`、`max` 三點位於 Pareto 線上 | Design Authority；independent review（同 vendor 的 Primary 路徑、Alternate）與 Final Adjudication（高 effort）；Orchestrator；高複雜度或高風險的實作；advisor | 以最低 effort 執行 verification 關鍵的工作 |
| 平衡 | Sonnet 5.5（`claude-sonnet-5-5`） | 單價約為 Opus 5.5 的一半；agentic coding 建議自 `medium` 起；API 預設 effort `high`（等級已重新校準）；第三方指數中，需較高 effort 才接近 Opus 5.5，每題總成本因此未必較低 | 契約明確的實作；唯讀調查（investigator）；標準的有界工作（worker）；可用性替代 | Independent review、裁決與設計決定的預設 |
| 輕量 | Haiku 5.5（`claude-haiku-5-5`） | 價格最低（單價約為 Sonnet 5.5 的 1/20）；API 預設 effort `medium` | 可由呼叫者機械核對的有界工作：搜尋、擷取、格式轉換、依明確樣式的修改、log／diff 摘要。宜先通過 qualification 再成為有效 mapping | 需要判斷的治理角色；結果無法機械核對的工作 |
| 前一代 | Opus 4.8（`claude-opus-4-8`） | 前一代高能力 model | 可用性替代的項目 | 預設 mapping |

其他 vendor 的 model（例如 OpenAI Codex 系列）可作為 Primary Independent Reviewer 的 family diversity 來源，前提是 Profile 的 qualification 與 Project Bindings 的授權。

**分層不等於單一 benchmark 的排名。** 第三方綜合指數中，Opus 5.5 的 `xhigh` 高於 Fable 5.1 的 `xhigh`，Opus 5.5 的 `high` 與之相當而成本約三分之一；官方資料與 Terminal-Bench 3.0 則顯示 Fable 5.1 在特定困難類別的優勢。把成本最高的層保留給有界的困難問題（第 2.5 節），是成本與能力的權衡；實際配置宜以角色工作的本地評估補充。

### E.2 Effort 參考

- Effort 近似於希望投入的運算量；effort 越高，model 越常自行判斷，也做更多 verification。
- 主要的效果在 verification 與邊界情況：Fable 5.1 的 Terminal-Bench 3.0 數據中，自 `low` 至 `max`，「測試漏掉的 bug」與「錯誤或不完整的修正」大幅減少，「領域規則錯誤」只小幅減少，「選錯解讀」反而增加。契約缺口要 route，不靠 effort（第 2.5 節）。
- 契約越明確，不同 effort 的產出越相近；規格不足時，effort 越高，model 代為作出的選擇越多。
- 作者的經驗法則（不是一般要求）：`low` 用於快速互動與簡單修改；`medium` 用於一般軟體工程；`high` 用於 verification 關鍵或邊界情況多的工作；`max` 用於完全自主的困難問題。`xhigh` 沒有對應的建議。
- 成本與時間：作者的範例任務中，自 `low` 至 `max` 的時間增加數倍到約 20 倍；benchmark 中每升一級，分數與 tokens 同時增加。第三方指數中，Opus 5.5 自 `medium` 至 `high` 指數 +2.3、成本約 ×1.37；`high` 至 `xhigh` +2.4、約 ×1.90；`xhigh` 至 `max` +1.7、約 ×1.73。
- 「較低 effort 實作、較高 effort 驗證」在本治理中以角色分離達成（第 2.5 節），不在已綁定的 session 內未經記錄地切換 effort。

### E.3 價格參考

Claude API reference（cached 2026-10-06），每百萬 tokens 的 input／output：

| Model | Input | Output |
|---|---|---|
| Fable 5.1 | $10 | $50 |
| Opus 5.5 | $4 | $20 |
| Sonnet 5.5 | $2 | $10 |
| Haiku 5.5 | $0.10 | $0.50 |

訂閱方案的用量與限額不同於 API 價格。成本只影響預設的選擇，不是弱化 verification 或 independent audit 的理由（第 2.5 節）。

### E.4 Binding 風險與核對做法（Runtime HOW 參考）

- **Flagged message 自動切換。** Opus 5.5 帶有與 Fable 同級的 bio／cyber safeguards；在 Claude Code 中，被 flag 的訊息會把 session 切到較舊的 model 並繼續執行，也可設定為先詢問。核對 assignment 的每一筆 assistant 紀錄，不只第一筆（第 2.2 節）。
- **Alias。** 以 `opus`、`sonnet`、`haiku`、`fable` 等 alias 派工時，alias 的對應可能隨平台更新改變；每次以 transcript 的實際 model 核對。
- **Root session 的 effort。** 有些啟動方式只套用 definition 的 model、不套用 effort（例如 Claude Code 的 `claude --agent` 須另帶 `--effort`）；使用者層的預設 effort 可能湊巧相同，不構成 binding 證據。
- **繼承 context 的派工。** 會繼承呼叫者 context 的 subagent 形態（例如 fork 型）不可用於 review 與 adjudication（第 2.3 節第 1 項）。
- **自動記憶。** 平台的自動記憶可能把執行期間的結論帶進之後的 context；採用專案宜確認其 independent dispatch 機制如何維持第 2.3 節第 1 項。
- **Fast mode。** 來源未說明 fast mode 是否改變紀錄中的 model；在已綁定的 session 中使用時，核對 binding 證據。

### E.5 來源

| 來源 | 日期 | 位置 |
|---|---|---|
| Anthropic，Thariq Shihipar，《Using Claude Code: Spending your effort》 | 2026-09-25 | https://claude.dev/blog/spending-your-effort/ |
| Anthropic，Thariq Shihipar，《The new rules of context engineering for Claude 5 generation models》 | 2026-07-24 | https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/ |
| Anthropic，Addy Osmani，《Getting the most out of Opus 5.5 in Claude and Claude Code》 | 2026-09-22 | https://claude.dev/blog/getting-the-most-out-of-opus-5-5/ |
| Claude API reference（model ids、effort、價格） | cached 2026-10-06 | 經 Reference Model Profile `default` v2.5 §2.2、§6 引用 |
| Artificial Analysis Intelligence Index（第三方；由截圖量測的近似值） | 擷取 2026-10-06 | artificialanalysis.ai |
| Reference Model Profile `default` v2.5 | Adopted／Frozen 2026-10-11 | 見文首 package references |
