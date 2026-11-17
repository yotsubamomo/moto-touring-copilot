# Reference Model Profile — default v2.5

**Profile ID：`default`**  
**Version：`v2.5`**  
**Status：Adopted／Frozen（2026-10-11，Acceptor 決定 A-2；採用基礎為驗證過的 Candidate，sha256 `006ac8df8fbfda8bac2362ae6f2e6e3310b590d9f85e1a7f6024fe8319e12790`；見 [ADOPTION-2026-10-11](../../records/ADOPTION-2026-10-11.md)）**  
**Governance：Minimal Operational Governance v2.1（Adopted／Frozen 2026-10-01）**  
**Base：`default`／`v2.4`（Adopted／Frozen 2026-10-02；本 Profile 不修改 v2.4，v2.4 檔案 md5 `5bc265e535a6e3983851b675795375cc` 不變）**  
**Supersedes for new adoption：`default`／`v2.4`（v2.4 保留為 frozen baseline；已 pin v2.4 者不自動改用）**  
**Revision type：mapping revision ＋ 新增 capability escalation 層 ＋ 三個 bounded assignments（reusable Subagents）。不修改 Minimal、role authority、independence properties、audit flow 或 audit bounds。**  
**存放位置：** 上游 `D:\momo\17 - Model Governance\master_governance\` 於 2026-10-11 不存在於本機，本 Candidate 暫存於採用專案 `governance/candidates/model-profiles/`；上游恢復可用並經採用後，以 `references/model-profiles/default-v2.5.md` 承載。

角色定義與權限以 Minimal Operational Governance v2.1 §2.1 為準（[upstream copy](../../upstream/master_governance/Minimal_Operational_Governance_v2.1_Candidate.md)）。本 Profile 只提供 role／model mapping、effort、capability escalation、availability fallback 與 binding verification 的預設（Minimal §2.2）。專案採用 `default`＋`v2.5` 時在 Project Bindings 記錄 overrides（無則明記 `none`）；本版不自動影響已採用 v2.4 或更早版本的專案。模型名稱與 IDs 是設定依據，不代表當前平台的可用性或 binding 已驗證（§6）。

## 1. 值的四種狀態

與 v2.4 §1 相同：**具體值**（預設，Bindings MAY override 並記錄理由）、**`PROJECT_BINDING`**（只能由專案提供）、**`N/A`**、**`TBD`**（本版無 `TBD`）。另：**qualification-gated** 指該 mapping 須先由 Bindings 記錄通過的 qualification 才成為有效 mapping；未通過前依 §2 指定的 resolution 解析（Codex 與 Haiku 適用，§6、§7）。

## 2. Default mapping

### 2.1 Governance roles（Minimal §2.1 六角色）

| identifier | role | default model | model id | effort | capability escalation（§3） | availability fallback（§4） | binding verification |
|---|---|---|---|---|---|---|---|
| `design_authority` | Design Authority | Opus 5.5 | `claude-opus-5-5` | `high` | E-DA → Fable 5.1／`xhigh` | F-DA | §6 |
| `executor` | Executor | Sonnet 5.5 | `claude-sonnet-5-5` | `medium` | E-EX → Opus 5.5／`high` | F-EX | §6 |
| `primary_reviewer` | Primary Independent Reviewer | **Codex（preferred，qualification-gated，§7）**；Claude path 首項 Opus 5.5 | Codex：`PROJECT_BINDING`；Opus 5.5：`claude-opus-5-5` | Codex：`PROJECT_BINDING`；Claude path：`xhigh` | 無（§3.2） | R-PR（與 v2.4 相同） | Codex：`PROJECT_BINDING`；Claude：§6 |
| `alternate_reviewer` | Alternate Independent Reviewer | Opus 5.5（固定預設，不隨 Primary／Executor 的 model 改變） | `claude-opus-5-5` | `xhigh` | E-AR → Fable 5.1／`xhigh`（僅限具體能力缺口） | F-AR | §6 |
| `final_adjudicator` | Final Adjudicator | Opus 5.5 | `claude-opus-5-5` | `xhigh` | E-FA → Fable 5.1／`xhigh` | F-FA | §6 |
| `orchestrator` | Orchestrator | Opus 5.5 | `claude-opus-5-5` | `medium` | E-OR → Opus 5.5／`high` | F-OR | §6（root role session，Minimal §2.2） |

`primary_reviewer` 的 Codex-preferred resolution、條件 1–4、resolution／substitution 區分與 Claude path，與 v2.4 §2、§3 R-PR、§6 相同（§7）。DA、Alternate、FA 與 Orchestrator 預設同為 Opus 5.5，所行使的 authority MUST 可區別（Minimal §2.1），review／adjudication 各自使用獨立 context（Minimal §2.3）；同 model 不使 Orchestrator 取得其他角色的 authority。

### 2.2 Bounded assignments（reusable Subagents，Minimal §2.1 第二段）

以下三個 identifier 是可重用的 **bounded assignments**：依其 definition 在呼叫者委派的範圍內工作，**不是 governance role，不取得任何 governance authority**。其輸出是呼叫者的輸入與待驗證主張，不構成 finding、verdict、ruling、decision、derivation、acceptance 或 audit record；呼叫者對使用其輸出負全責。正式 review／adjudication 不得由 bounded assignment 代行，Executor 使用它們屬 self-verification（Minimal §2.3）。

| identifier | 用途 | 允許的呼叫者 | default | effort | capability escalation | availability fallback |
|---|---|---|---|---|---|---|
| `bounded_worker` | 有界、可由呼叫者核對的工作：搜尋、擷取、格式轉換、依明確樣式的機械修改、log／diff 摘要 | 任一治理角色 | 依 task class：`mechanical` → Haiku（qualification-gated；未通過時 Sonnet 5.5）；`standard` → Sonnet 5.5 | `mechanical`：`low`；`standard`：`medium` | E-BW：`mechanical` → `standard` | F-BW |
| `investigator` | 唯讀調查：跨檔案追查、root-cause 假設、證據蒐集 | 任一治理角色 | Sonnet 5.5（`claude-sonnet-5-5`） | `medium` | E-IN → Opus 5.5／`medium` | F-IN |
| `advisor` | 諮詢第二意見（方案比較、風險提示）；不作決定 | DA、Executor、Primary／Alternate Reviewer、FA（不含 Orchestrator：Orchestrator 只 route，Minimal §2.4） | Opus 5.5（`claude-opus-5-5`） | 呼叫者為 DA、Alternate、FA 時 `high`，其餘 `medium` | E-AD → Fable 5.1／`xhigh` | F-AD |

Haiku 的 model id：Claude API reference（cached 2026-10-06）列 Haiku 5.5 為 `claude-haiku-5-5`。本 Profile **不假設其已在採用平台發布或可用**：`mechanical` class 的 Haiku mapping 為 qualification-gated，Bindings 未記錄通過的 qualification probe（實際 `message.model` 等於宣告 id）時，`mechanical` 解析為 Sonnet 5.5／`low`（resolution，不記 substitution）。Task class 由呼叫者在派工時指定並記錄；無法明確歸為 `mechanical` 者一律 `standard`。

選型依據（non-normative）：Claude API reference（cached 2026-10-06）列價 Opus 5.5 $4／$20、Sonnet 5.5 $2／$10、Haiku 5.5 $0.10／$0.50、Fable 5.1 $10／$50（per MTok input／output）；Sonnet 5.5 對 agentic coding 建議自 `medium` 起；Opus 5.5 API 預設 effort 為 `medium`。成本只影響 default 的選擇，不得作為削弱 verification 或 independent audit 的理由（§3.1 E-9）。

## 3. Capability escalation

### 3.1 共同規則

- **E-1 觸發。** Escalation 只在 §3.2 宣告的 trigger 成立時發生，且 MUST 引用具體證據：(M) mechanical trigger——可由紀錄機械判定的條件（derivation／decision record 的標記、Bindings assurance policy 類別、audit record 中的 model 事實）；(D) declared trigger——具相應 authority 的角色在紀錄中寫明的具體能力需求或能力不足證據。成本、偏好、「保險起見」、先前 session 的印象，都不是 trigger。
- **E-2 決定者。** Orchestrator（或 direct-execution session）只機械套用 trigger 並派工；不自行判斷能力是否足夠（Minimal §2.4：Orchestrator 不裁決 evidence sufficiency）。D trigger 由 §3.2 指定的角色提出。
- **E-3 範圍。** Escalation 只適用於紀錄所指的 work item、design question 或 audit cycle；不延續到其他工作。Trigger 不再成立時，下一次派工回到 default mapping。
- **E-4 單步。** 每個 identifier 只有一個 escalation target；不串接。Escalated mapping 仍不足時，依 Minimal §2.4／§3.6 route（DA 或 FA），不再升級。
- **E-5 Fable 5.1 的界線。** Fable 5.1 只作為 `design_authority`、`alternate_reviewer`、`final_adjudicator`、`advisor` 的 escalation target，且每次只處理一個紀錄中指名的 bounded question、decision 或 Alternate／Adjudication instance。Fable 5.1 **不是** `executor`、`orchestrator`、`bounded_worker`、`investigator` 的 escalation 或 fallback，也不是任何一般 escalation chain 的終點。Fable 5.1 在 §4 只作為 DA、`primary_reviewer`、FA fallback 列的末項（可用性替代，記錄其證據）；不因 model diversity 或成本而派工。
- **E-6 Authority 與 independence 不變。** Escalation 不改變 authority（Minimal §1.3、§2.2）、不新增 audit round、不構成 cycle reset（Minimal §4.5：換 model 不是 reset）。Review／adjudication 的 escalation 是新的派工，MUST 為 fresh context（Minimal §2.3）；R2 延續 R1 context 的規則不因 escalation 擴張。
- **E-7 Binding。** Escalation record 存在時，escalated mapping 即為該次派工的有效 mapping；實際 assignment 以它核對（Minimal §2.2，§6）。
- **E-8 記錄。** 每次 escalation 依 §8 記錄。
- **E-9 不降級。** 本 Profile 不提供低於 default 的 mapping 語義。Bindings 依 Minimal §2.2 仍可 override；以成本為唯一理由降低 `primary_reviewer`、`alternate_reviewer`、`final_adjudicator` 的 model 或 effort SHOULD NOT。
- **E-10 與 fallback 的關係。** Escalation 回答「需要更強能力」，依據是能力；fallback（§4）回答「指定 model 當次不可用」，依據是當次可用性證據。兩者分開記錄。Escalated mapping 當次不可用時，沿該 escalated mapping 自己的 fallback 列（§4 標 `*` 者）替代。

### 3.2 各 identifier 的 escalation

| ID | identifier | escalated mapping | Trigger（任一成立） | 提出者 |
|---|---|---|---|---|
| **E-DA** | `design_authority` | Fable 5.1／`xhigh` | (D1) DA 在 decision／derivation record 中，就一個指名的 design question 寫明：兩個以上合理設計的後果實質不同，且以現有證據無法裁決；(D2) 同一 design question 的先前 DA decision 被 FA ruling 或經 route 的 Reviewer finding 以證據推翻或實質爭議；(M1) Bindings assurance policy 宣告該類別的 DA 決定使用 Fable | DA；(M1) 機械 |
| **E-EX** | `executor` | Opus 5.5／`high` | (M1) DA derivation／decision record 將該 Ticket／work item 標為 `complexity: high` 並附理由；(M2) work item 屬 Bindings 宣告的高風險類別；(M3) 同一 root cause 的 blocking finding 在一次 targeted correction 後仍以 implementation defect 存在 → 下一次 correction 派工；(D1) Executor 以 `BLOCKED`／`NEEDS_CONTEXT` 回報能力限制並附證據（缺少資訊不屬此項，依 Minimal §2.4 route） | DA／機械／Executor |
| — | `primary_reviewer` | 無 | Primary 的 model 由 §7 的 resolution 決定；R1／R2 中途不升級 reviewer，以免改變 audit subject 以外的條件 | — |
| **E-AR** | `alternate_reviewer` | Fable 5.1／`xhigh` | 只有 (D1)：Opus 5.5 Alternate 在作出 verdict 前，於自身 record 就一項指名的剩餘 finding 或爭議面向寫明**具體能力缺口**（為何現有證據與分析不足以判定），並不作 verdict；Orchestrator 以 escalated mapping 派新的 fresh Alternate，該 cycle 仍只產生一份 Alternate verdict（提出 escalation 的派工記為 escalation record，不算第二次 Alternate Review）。三項條件須同時成立：具體能力缺口紀錄、本 trigger 屬已採用的 Profile 且 Bindings 未停用、該 Profile／Bindings 已由 Acceptor 採用（授權依據）。**Primary 或 Executor 使用 Opus 5.5、model diversity、成本與高風險類別都不是本 trigger** | Alternate |
| **E-FA** | `final_adjudicator` | Fable 5.1／`xhigh` | (M1) Bindings 高風險類別宣告；(M2) 同一 root cause 在新 cycle 再次進入 Final Adjudication（Minimal §4.5 進展條件的情境）；(D1) FA 在作出 ruling 前，於自身 record 寫明需要升級的具體爭議面向並不作 ruling；Orchestrator 以 escalated mapping 派新的 fresh FA，只產生一份 ruling | 機械／FA |
| **E-OR** | `orchestrator` | Opus 5.5／`high`（effort escalation） | (M1) Bindings 為該 run 宣告並行度 > 1，或 run 的 derived contract set 含兩份以上 Spec；(D1) Orchestrator 在 run record 記錄控制面能力失誤（re-ground 無法由權威紀錄重建狀態，或 DA／FA 認定的 routing 錯誤）。Root role session 的 escalation 於 activation 或 checkpoint／rollover 的 successor session 生效，並於 run record 記錄（orch-default §8、§11） | 機械／Orchestrator |
| **E-BW** | `bounded_worker` | `standard`（Sonnet 5.5／`medium`） | (D1) 呼叫者核對後記錄 `mechanical` 輸出不足或錯誤。`standard` 不再升級；超出 bounded 範圍的工作由呼叫者自行處理或改派 `investigator`／`advisor` | 呼叫者 |
| **E-IN** | `investigator` | Opus 5.5／`medium` | (D1) 呼叫者記錄調查跨多個子系統且原因交互作用；(D2) Sonnet 5.5 investigator 回報 inconclusive 並附理由 | 呼叫者 |
| **E-AD** | `advisor` | Fable 5.1／`xhigh` | 只在呼叫者為 DA 或 FA，且該問題符合 E-DA (D1) 或 E-FA (D1) 的條件時；其他呼叫者無 escalation | DA／FA |

## 4. Availability fallback（deterministic replacement）

### 4.1 共同規則

沿用 v2.4 §3 共同規則 1–5，語義不變：

1. **觸發依據**：當次 dispatch 的錯誤（含 classifier refusal：記錄 `stop_details.category` 後替代，不對同一 model 重試同一 dispatch），或當下可用性檢查證據；overload／rate-limit（例如 HTTP 529／429）在 Bindings 宣告的 bounded retry 用盡後構成可用性證據。不得憑記憶或先前 session／run 的不可用狀態跳過指定 model。
2. **順序**：先 Bindings override 的 fallback 列，再本節列，逐項取第一個可用者；不跳序、不猜。
3. **每次替代 MUST**：維持 Minimal §2.3 四項 properties；不新增 audit round；不改變 authority；記錄 substitution（§8）；替代使 §5 任一 diversity 關係不再成立時記 `diversity_lost`。
4. **Fallback 列耗盡**：進入 Minimal §1.5 recovery。
5. **替代不重新觸發任何初始化詢問。**

新增：

6. **適用對象**：fallback 列屬於當次有效的 mapping。default mapping 用不帶 `*` 的列；escalated mapping 用帶 `*` 的列。
7. **Fallback 不是 escalation**：fallback 列中較高 tier 的 model（例如 DA 列末項 Fable 5.1）只因可用性而使用，不記為 escalation；每次派工仍先嘗試有效 mapping。

### 4.2 各 identifier 的 fallback 列

| Policy | 有效 mapping | Fallback 列（依序） | 附加規則 |
|---|---|---|---|
| **F-DA** | Opus 5.5／`high` | Opus 4.8／`high` → Fable 5.1／`high` | 合格替代 DA 的有效 decision 即為 DA decision（authority 屬角色，同 v2.4 R-DA） |
| **F-DA\*** | Fable 5.1／`xhigh`（E-DA） | Opus 5.5／`xhigh` → Opus 4.8／`xhigh` | 同上 |
| **F-EX** | Sonnet 5.5／`medium` | Opus 5.5／`medium` → Opus 4.8／`medium` | 接手 Executor 沿同一 worklog identity（impl-default §10）。不含 Haiku、Fable |
| **F-EX\*** | Opus 5.5／`high`（E-EX） | Opus 4.8／`high` | 同上 |
| **R-PR** | Codex（§7）或 Opus 5.5／`xhigh` | 單一 Claude path：Opus 5.5／`xhigh` → Opus 4.8／`xhigh` → Fable 5.1／`xhigh` | 替代順序、R1／R2 context 規則與 Codex 恢復規則同 v2.4 §3 R-PR 列。v2.4 該列中「Primary 替代為 Fable 5.1 時 Alternate 依 R-AR 替代」及其 `diversity_lost` 判定**不沿用**（v2.4 的 Alternate 預設為 Fable；本版 Alternate 固定為 Opus 5.5，diversity 依 §5）。Codex 不在任何 fallback 列 |
| **F-AR** | Opus 5.5／`xhigh` | Opus 4.8／`xhigh` | 仍 exactly one Alternate；不因替代重跑 R1／R2。不含 Fable：Alternate 只經 E-AR 使用 Fable |
| **F-AR\*** | Fable 5.1／`xhigh`（E-AR） | Opus 5.5／`xhigh` → Opus 4.8／`xhigh` | 同上 |
| **F-FA** | Opus 5.5／`xhigh` | Opus 4.8／`xhigh` → Fable 5.1／`xhigh` | 替代 FA 的 ruling 即為有效 ruling（同 v2.4 R-FA） |
| **F-FA\*** | Fable 5.1／`xhigh`（E-FA） | Opus 5.5／`xhigh` → Opus 4.8／`xhigh` | 同上 |
| **F-OR** | Opus 5.5／`medium` | Opus 4.8／`medium` → Sonnet 5.5／`high` | Successor 以同一 run identity 從權威紀錄 bootstrap（orch-default §8）。不含 Fable、Codex |
| **F-OR\*** | Opus 5.5／`high`（E-OR） | Opus 4.8／`high` → Sonnet 5.5／`high` | 同上 |
| **F-BW** | `mechanical`：Haiku／`low`（已 qualify）或 Sonnet 5.5／`low`；`standard`：Sonnet 5.5／`medium` | `mechanical`：Sonnet 5.5／`low`（若有效 mapping 為 Haiku）→ Opus 5.5／`low`；`standard`：Opus 5.5／`medium` | 不含 Fable |
| **F-IN** | Sonnet 5.5／`medium` | Opus 5.5／`medium` → Opus 4.8／`medium` | 與 E-IN 同 target 但依據不同（可用性 vs 能力），分開記錄 |
| **F-IN\*** | Opus 5.5／`medium`（E-IN） | Opus 4.8／`medium` → Sonnet 5.5／`high` | — |
| **F-AD** | Opus 5.5／`medium` 或 `high` | Opus 4.8（同 effort）→ Sonnet 5.5／`high` | — |
| **F-AD\*** | Fable 5.1／`xhigh`（E-AD） | Opus 5.5／`xhigh` → Opus 4.8／`xhigh` | — |

每列皆不以其有效 mapping 為首項、無重複項、只含本 Profile 已列出的 model。Fable 5.1 作為 fallback 項只出現在 F-DA、R-PR、F-FA 列。各列是跨專案的 Profile 預設；採用專案的 runtime 若無法派工某 model，由 Project Bindings 以 override 處理，不改變本列。

## 5. Assurance defaults：independence 與 diversity

**Context independence 與 model diversity 是兩件事，分開記錄。**

- **Context independence**：只由 Minimal §2.3 四項 properties 定義，每次正式 review／adjudication MUST 成立。同 model 的 fresh-context review 是合法 independent review；不同 model 也不自動構成 independent review。
- **Model diversity**：assurance 觀察，不是 independence 的條件。只能以 binding 證據顯示的**實際 model** 主張；兩個 assignment 的實際 model 相同時，不得主張其間有 model diversity。

**本版宣告的 diversity 關係**（以該 cycle 的實際 mapping 判定）：

1. **D1**（恆有）`alternate_reviewer` model ≠ 產生受審 subject 的每個 `executor` model。預設成立：Opus 5.5 對 Sonnet 5.5。
2. **D2**（條件性）`alternate_reviewer` model ≠ 有效 `primary_reviewer` model——**只在 Codex 為有效 Primary 時宣告**（Codex 對 Opus 5.5）。
3. **D3**（恆有）`primary_reviewer` model ≠ `executor` model。預設成立：Codex 或 Opus 5.5 對 Sonnet 5.5。
4. **D4**（條件性）`primary_reviewer` 與 `executor` 跨 vendor（family diversity）——只在 Codex 為有效 Primary 時宣告（同 v2.4 §4 第 3 條）。

**預設拓樸允許的同 model 組合**（不記 `diversity_lost`，audit record 記為「無 model diversity」）：§7 條件 1–3 使 Primary 解析為 Opus 5.5 時，Primary＝Alternate＝Opus 5.5；DA＝Alternate＝FA＝Orchestrator＝Opus 5.5。此時 Alternate 維持 Opus 5.5／`xhigh`，不因同 model 切換 Fable；其 independence 由四項 properties 成立。

**Audit record 的兩個欄位（可驗證）**：Primary 與 Alternate 的 record 分別記載
- (a) **context independence**：四項 properties 各自的滿足方式（新的派工、binding 證據引用、自主取得 subject、record 由本角色寫入的位置）；
- (b) **model diversity**：Executor、Primary、Alternate 的實際 model（引用 §6 binding 證據），D1–D4 各記「成立／不成立／未宣告」，未宣告的同 model 組合記「無」。

(b) 的任何結果都不改變 (a)。

**`diversity_lost`**：只在某次 substitution（§4）或 escalation（§3）使「依該 cycle 的 resolved mapping 原本成立的宣告關係」不再成立時記錄。本版預設下會觸發的情況：
- `executor` escalation（E-EX）或 fallback（F-EX）為 Opus 5.5 → D1 不成立（Alternate 為 Opus 5.5）；有效 Primary 也是 Opus 5.5 時，D3 也不成立。Profile 不為此改派 Alternate 或 Primary；Bindings MAY 為高風險類別要求 Codex（D4）恢復後再 audit。
- Codex 被 Claude path 替代（§7 條件 4）→ D4 不成立；替代 model 與 Alternate 相同（例如 Opus 5.5）時 D2 也不成立。
- Alternate 依 F-AR 替代為與 Executor 相同的 model，或在 D2 有宣告時替代為與 Primary 相同的 model → D1 或 D2 不成立。

不觸發：§7 條件 1–3 的 resolution（Primary＝Alternate＝Opus 5.5 是預設拓樸，D2 未宣告）；`mechanical` 未 qualify 而解析為 Sonnet 5.5；DA、FA、Orchestrator、bounded assignments 的任何替代或 escalation（仍 MUST 記錄 substitution／escalation 本身）。

`diversity_lost` 不使替代違法，只記入 audit record 的 (b) 欄位（Minimal §4.6），不影響 (a)。

## 6. Binding verification

規範依據：Minimal §2.2、§2.3、§5.1。

**Claude Code harness 預設機制（SHOULD）**，沿用 v2.4 §5 並補充：

- **被派工的 assignment（default mapping）**：definition frontmatter 綁定完整 model id 與 `effort`；Agent tool dispatch 同時套用兩者（v2.4 §5 記錄的 harness 事實）。
- **被派工的 assignment（escalated／fallback mapping）**：以 (a) 綁定該 mapping 的 variant definition，或 (b) 同一 definition 加 Agent tool 的 per-dispatch `model`／`effort` 參數派工；採用哪一種是 `PROJECT_BINDING`。(b) 的 `model` 參數是 alias（例如 `opus`、`sonnet`、`haiku`、`fable`），alias 對應的實際 model 可能隨平台更新改變，因此每次派工 MUST 以 transcript 核對。
- **Root role session**（Orchestrator、Lightweight direct-execution Executor；Minimal §2.2）：`claude --agent <name>` 只套用 frontmatter `model`，**不套用 `effort`**，MUST 同時帶 `--effort <mapped effort>`（v2.4 §5）。使用者層的 per-model effort 設定（例如 settings 的 `modelSettings.<model>.effortLevel`）會在缺少 `--effort` 時生效，可能湊巧等於或不等於 mapping，不構成 binding 證據。Orchestrator 在核對成立前不得派工。
- **證據**：harness transcript 每則 assistant message 的 `model` 與 `effort` 欄位；Definition 新建或變更對進行中 session 不可見，binding 驗證 MUST 在新 process 進行（v2.4 §5）。證據位置與 probe 紀錄為 `PROJECT_BINDING`。
- 不設會覆寫角色綁定的全域 subagent model override。
- 會繼承呼叫者 context 的派工形態（例如 fork 型 subagent）不得用於 review／adjudication（Minimal §2.3 第 1 項）。

**Model id 與 effort 支援（文件依據：Claude API reference，cached 2026-10-06）**：

| Model | model id | 文件列出的 effort | 本 Profile 用到的 effort | 平台可用性與 binding |
|---|---|---|---|---|
| Opus 5.5 | `claude-opus-5-5` | `low`–`max`（API 預設 `medium`） | `low`、`medium`、`high`、`xhigh` | `PROJECT_BINDING` |
| Sonnet 5.5 | `claude-sonnet-5-5` | `low`–`max`（API 預設 `high`，levels 已重新校準） | `low`、`medium`、`high` | `PROJECT_BINDING` |
| Haiku 5.5 | `claude-haiku-5-5` | `low`–`max`（API 預設 `medium`） | `low` | qualification-gated（§2.2） |
| Fable 5.1 | `claude-fable-5-1` | `low`–`max` | `high`、`xhigh` | `PROJECT_BINDING` |
| Opus 4.8 | `claude-opus-4-8` | `low`–`max` | `medium`、`high`、`xhigh` | `PROJECT_BINDING` |
| Codex | `PROJECT_BINDING` | `PROJECT_BINDING` | `PROJECT_BINDING` | qualification-gated（§7） |

文件列出的 id 與 effort 只是設定依據；採用專案以自身 transcript 證據驗證。Prompt 自稱、設定存在、model 名稱相同，皆不構成 binding 證據。

## 7. Codex：僅作為 `primary_reviewer` 的 preferred／effective mapping

與 v2.4 §5（Codex 段的四項 `PROJECT_BINDING` 宣告）及 §6（條件 1–4、resolution 與 substitution、恢復可用時自下一次 `primary_reviewer` dispatch 起回到 Codex、不重開已完成輪次、Codex 不列入其他角色）**完全相同**，本版不改動。Bindings 未完成四項宣告或 qualification 未通過時，`primary_reviewer` 解析為 Claude path 首項 Opus 5.5／`xhigh`。

## 8. Records

- **Substitution record**（§4；同 v2.4）：identifier、原 mapping、替代 mapping、可用性證據引用、`diversity_lost`（若有，標明 D1–D4 哪一條）。
- **Escalation record**（§3，新增）：identifier、default mapping、escalated mapping、trigger ID（例如 `E-EX/M3`）、證據或提出者紀錄的引用、範圍（work item／question／cycle）、時間；若使 D1–D4 任一不成立，另標 `diversity_lost`。
- **Resolution 註記**：Codex（§7 條件 1–3）與 Haiku（§2.2）的 qualification-gated resolution，記錄所適用的條件；不記為 substitution。
- **Audit record 的 assurance 欄位**：context independence 與 model diversity 分兩欄（§5）。

記錄位置由 Bindings 的 Work records 宣告（worklog、run record 或 audit record）。

## 9. Change record

| Version | Date | Status | Basis | Change |
|---|---|---|---|---|
| `v2.4` | 2026-10-02 | Adopted／Frozen | 見 v2.4 §8 | 本 Candidate 的基線，未修改 |
| `v2.5` | 2026-10-11 | **Candidate** | Operator 指示（2026-10-11，"Minimal Governance v2.1 Adoption + Model Profile Update" 任務）：將 Sonnet 5.5、Haiku、Opus 5.5、Fable 5.1 與 Codex 納入派工策略，capability escalation 與 availability fallback 分開定義，Fable 只處理必要且有界的高難度問題，Primary 為 Opus 5.5 時 Alternate 不得僅因同 model 主張 diversity | **Mapping**：`design_authority` Fable 5.1／`xhigh` → Opus 5.5／`high`；`executor` Opus 5.5／`high` → Sonnet 5.5／`medium`；`alternate_reviewer` Fable 5.1 → Opus 5.5（`xhigh` 不變）；`final_adjudicator` Fable 5.1 → Opus 5.5（`xhigh` 不變）；`orchestrator` effort `high` → `medium`；`primary_reviewer` 不變。**新增** §2.2 三個 bounded assignments（`bounded_worker`、`investigator`、`advisor`；v2.4 §7 預留的擴充點）、§3 capability escalation、§4 規則 6–7 與 `*` 列、§5 context independence／model diversity 分欄與 D1–D4、§6 per-dispatch alias 與 root session 補充、§8 escalation record。**不變**：R-PR 替代順序與 R1／R2 規則、Codex 語義（§7 ＝ v2.4 §5–§6）、v2.4 §3 共同規則 1–5、Minimal 全部條文。**Semantic diff 重點**：(a) Fable 5.1 由三個角色的預設改為四個 identifier 的有界 escalation target；(b) `diversity_lost` 可由 escalation 觸發；(c) v2.4 的「DA＝Alternate＝FA 同 model」預設拓樸改為「DA＝Alternate＝FA＝Orchestrator 同為 Opus 5.5」；Alternate 固定為 Opus 5.5，與預設 Executor（Sonnet 5.5）不同，Primary 解析為 Opus 5.5 時 Primary＝Alternate 是預設拓樸，不主張 model diversity。未經 independent review；採用需 operator 依 Minimal §5.3 明確授權並記錄 |
| `v2.5` Candidate correction | 2026-10-11 | **Candidate** | Operator bounded correction 指示（2026-10-11）：Alternate 不因 Primary／Executor 為 Opus 5.5 自動改用 Fable；model diversity 與 context independence 分開記錄；Opus 4.8 的派工限制只屬專案 runtime | E-AR 由「diversity resolution（M1）＋高風險類別（M2）」改為只有能力缺口 trigger（D1，含三項條件）；F-AR 改為 Opus 4.8／`xhigh`（移除 Fable 與排除條件），新增 F-AR\*；§5 改為 independence／diversity 兩欄、D2 改為條件性（只在 Codex 為有效 Primary 時宣告）、`diversity_lost` 只看 substitution／escalation 使原本成立的宣告關係失效；R-PR 不再沿用 v2.4「Primary 替代為 Fable 時 Alternate 改派」；§4.2 註明 runtime 限制由 Bindings override 處理；§2.1、§3.1 E-5、§8 相應更新。Mapping、effort 與其他 identifier 不變 |

| `v2.5` adoption／freeze | 2026-10-11 | **Adopted／Frozen** | Acceptor（Momo Dai）2026-10-11 決定 A-2：「Adopt Reference Model Profile `default` v2.5, using the verified Candidate as the adoption basis. Preserve frozen v2.4 unchanged.」（[ADOPTION-2026-10-11](../../records/ADOPTION-2026-10-11.md)） | **`default / v2.5` formally Adopted／Frozen**；只更新 header（標題、Status、Supersedes）與本列；§1–§8 與 Candidate（sha256 `006ac8df8fbfda8bac2362ae6f2e6e3310b590d9f85e1a7f6024fe8319e12790`，§1–§8 sha256 `6416fb948619f7e9ae464fefff3f81f43fc439b6980f50b24151344d9ef4443b`）相同。v2.4 保留為 frozen baseline |

本 Profile 之後的變更依 Minimal §5.3 留下版本、依據與授權；新版本不自動適用既有專案。
