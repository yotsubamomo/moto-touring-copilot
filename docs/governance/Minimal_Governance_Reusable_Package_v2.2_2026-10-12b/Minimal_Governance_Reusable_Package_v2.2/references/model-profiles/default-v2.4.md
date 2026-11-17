# Reference Model Profile — default v2.4

**Profile ID：`default`**  
**Version：`v2.4`**  
**Status：Adopted／Frozen（2026-10-02，operator 明確授權「採用」）**  
**Governance：Minimal Operational Governance v2.1（Adopted／Frozen 2026-10-01）**  
**Supersedes for new adoption：`default`／`v2.3`**（[default-v2.3.md](default-v2.3.md)、[default-v2.2.md](default-v2.2.md)、[default-v2.1.md](default-v2.1.md) 與 [default-v2.md](default-v2.md) 保留為 frozen baseline；已 pin 者不自動改用）  
**Revision type：`primary_reviewer` fallback 單一 Claude path（Opus 5.5／`xhigh` → Opus 4.8／`xhigh` → Fable 5.1／`xhigh`）＋ Codex 自所有 fallback 列與其他角色的 Profile 層 override 移除，Codex 只作為 `primary_reviewer` 的 preferred／effective mapping；resolution／substitution／`diversity_lost` 語義、其他五個 identifier 的 model 與 effort、role authority、independence、audit bounds 不變；header 的 Governance 標籤更新為 v2.1（§2.1、§2.3 所引條文與 v2.0 byte-identical）**  
**定位：新專案的參考預設。所有可 dispatch identifier 皆有可解析的預設值與 deterministic replacement policy；binding verification 的實作證據仍由採用專案提供。**

角色定義與權限以 [Minimal Operational Governance v2.1](../../Minimal_Operational_Governance_v2.1_Candidate.md) §2.1 為準。本 Profile 不改變任何 role authority、independence requirement 或 audit bounds（Minimal §2.2）。專案採用 `default`＋`v2.4`，在 Project Bindings 記錄 overrides（無則明記 `none`）；後續版本不自動影響已採用專案。模型名稱與 IDs 是設定依據，不代表已完成當前平台的可用性或 binding 驗證。

## 1. 值的四種狀態

| 標記 | 意義 | 處理方式 |
|---|---|---|
| **具體值** | 本 Profile 的預設 | 直接採用；Bindings MAY override 並記錄理由 |
| **`PROJECT_BINDING`** | 依本質只能由專案提供（例如特定 harness 的 binding verification 證據位置） | 不是問題、不是缺漏。Bindings 在對應執行／activation／audit 前填入；本 Profile 對 Claude Code harness 於 §5 給出預設機制 |
| **`N/A`** | 該平台／角色不適用 | 明記不適用 |
| **`TBD`** | 沒有足以指定該值的依據 | **本版無 `TBD`。** 日後出現時依 Minimal §2.2 不構成有效設定 |

v1 的 `USER_SELECTION_REQUIRED` 已移除：`primary_reviewer` 有預設值。使用者只在需要 override 時透過 Project Bindings 介入；initialization 不再詢問任何 model 選擇。

## 2. Default mapping（operator S-1 決定 2026-09-22；model migration 與 `primary_reviewer` Codex-preferred 決定 2026-09-29；`primary_reviewer` 單一 Claude path 與 Codex 範圍收斂 2026-10-02）

| identifier | role / subagent | model | model id／resolution policy | effort／mode | replacement policy | binding verification |
|---|---|---|---|---|---|---|
| `design_authority` | Design Authority | Fable 5.1 | `claude-fable-5-1`；當次解析結果須驗證 | `xhigh`；design decision／clarification／derivation／phase acceptance | R-DA（§3） | §5 |
| `executor` | Executor | Opus 5.5 | `claude-opus-5-5`；不依 parent model 隱性解析 | `high`；implementation＋self-verification | R-EX（§3） | §5 |
| `primary_reviewer` | Primary Independent Reviewer | **Codex（preferred／effective mapping，只在本 identifier）**；Claude path 首項：Opus 5.5 | Codex：model／version ＝ `PROJECT_BINDING`（Bindings 依 §6 授權並完成 binding qualification 後即為有效 mapping；未授權、明確禁用或無法 qualify 時，有效 mapping 即為 Claude path 首項 Opus 5.5；當次不可用時依 R-PR 沿 Claude path 替代）。Opus 5.5：`claude-opus-5-5`；不依 parent model 隱性解析 | Codex：effort／mode ＝ `PROJECT_BINDING`；Claude path 全程 `xhigh`。independent review-only：R1／R2、Spec Integration Audit（Minimal §4.7） | R-PR（§3）：單一 Claude path Opus 5.5／`xhigh` → Opus 4.8／`xhigh` → Fable 5.1／`xhigh`；Codex 不在 fallback 列 | Codex：`PROJECT_BINDING`（§5）；Opus 5.5：§5 |
| `alternate_reviewer` | Alternate Independent Reviewer | Fable 5.1 | `claude-fable-5-1` | `xhigh`；fresh independent review-only；exactly one Alternate | R-AR（§3） | §5 |
| `final_adjudicator` | Final Adjudicator | Fable 5.1 | `claude-fable-5-1` | `xhigh`；independent adjudication | R-FA（§3） | §5 |
| `orchestrator` | Orchestrator | Opus 5.5 | `claude-opus-5-5`；不依 parent model 隱性解析 | `high`；control plane／routing／run-to-completion | R-OR（§3） | §5 |

Design Authority、Alternate Independent Reviewer 與 Final Adjudicator 使用同一 model；所行使的 authority MUST 可區別（Minimal §2.1），且各自使用獨立 context（Minimal §2.3）。`primary_reviewer` 採 **Codex-preferred resolution**（§6）：Project Bindings 授權 Codex 且當次可用時，Primary Independent Reviewer 即為 Codex；Codex 未授權、被 operator／專案明確禁用、無法完成 binding qualification，或當次不可用時，才進入 R-PR 的單一 Claude path（Opus 5.5／`xhigh` → Opus 4.8／`xhigh` → Fable 5.1／`xhigh`）；前三種情況是 resolution（有效 mapping ＝ Opus 5.5／`xhigh`），第四種是 substitution（§6）。Codex 不出現在任何 identifier 的 fallback 列。Bindings 未授權 Codex 的專案，Executor、Primary Independent Reviewer 與 Orchestrator 使用同一 model（Opus 5.5）：Executor 與 Primary Reviewer 的 independence 由 Minimal §2.3 四項 properties 成立，與 model 是否相同無關；Orchestrator 不因與 Executor 同 model 取得任何 Executor、Reviewer、Design Authority 或 Final Adjudicator authority。Effort 值是預設，Bindings MAY 以 explicit override 調整並記錄理由；本版 effort 與 v2.2 相同。Orchestrator 自身 effort 依 orch-default §11 於 activation 設定並記錄。

Opus 4.8（`claude-opus-4-8`）自本版起不再是任何 identifier 的預設 model，保留於 §3 各 replacement 列作為 conservative fallback。

## 3. Deterministic replacement policies

共同規則（Minimal §2.2、§2.3）：

1. **觸發依據**：當次 dispatch 的錯誤，或當下的可用性檢查證據；不得憑記憶或先前 session／run 的不可用狀態跳過指定 model。dispatch 錯誤包括 harness／API 回傳的 **classifier refusal**（`stop_reason: refusal`，含 `stop_details.category`）：記錄 category 後依 fallback 列替代，不對同一 model 重試同一 dispatch。Overload／rate-limit 回應（例如 HTTP 529／429）在 Project Bindings 宣告的 bounded retry 用盡後構成當次可用性證據（未宣告時即構成）；Bindings SHOULD 宣告該 bounded retry（次數與時間窗屬 Runtime HOW，Minimal §5.4）。
2. **順序**：先依 Project Bindings override 的 fallback 列，再依本節 fallback 列，逐項嘗試第一個可用者；不跳序、不猜。
3. **每次替代 MUST**：維持 Minimal §2.3 四項 properties（review／adjudication 角色的 fresh context 不因替代而繼承任何既有對話）；不新增 audit round；不改變 authority；在 worklog／run record 記錄 substitution（原 mapping、替代 mapping、證據引用）；替代使 §4 定義的任一 diversity 關係（含 Bindings 宣告者）不再成立時，另標 `diversity_lost`（定義見 §4）。**§3 各列附加規則與 §4 列舉的觸發／不觸發情況，以其他 identifier 維持有效預設 mapping（`primary_reviewer` 依 §6 解析後者）、且 Project Bindings 未另行宣告 diversity 關係為前提；多個 identifier 同時處於替代狀態（例如 `executor` 與 `alternate_reviewer` 皆替代為 Opus 4.8），或 §4 第三條關係（Codex 為有效 Primary 時的 family diversity）、Bindings 另行宣告的關係因替代而不再成立時，一律依 §4 定義以該 cycle 的實際 mapping 判定。** Bindings 未授權 Codex、明確禁用 Codex，或 Codex 未完成 binding qualification（§6 條件 1–3）而使 `primary_reviewer` 解析為 Opus 5.5，是 resolution，不是 substitution，不記錄替代、不記 `diversity_lost`。
4. **Fallback 列耗盡**：該路徑進入 Minimal §1.5 recovery；三步完成後仍 unsafe／indeterminate 才停止該路徑。
5. **替代不重新觸發任何初始化詢問**（Minimal §2.2；v1 的 Primary Reviewer initialization 節已不存在）。

| Policy | Fallback 列（依序） | 附加規則 |
|---|---|---|
| **R-DA** `design_authority` | Opus 5.5／`xhigh` → Opus 4.8／`xhigh` | 合格替代者以 Design Authority 身分派工即行使 Design Authority 權限；其有效 decision 即為 DA decision（authority 屬角色，不屬 model；Minimal §1.3、§2.2），不需 preferred／default DA model 事後確認；preferred model 恢復可用本身不重開、不使先前 decision 失效。日後任何變更依 Minimal §5.3 一般規則，以角色權限與新證據為依據、依變更實際性質適用第 1 或第 2 類，不以 model 身分為依據。替代 DA 不得修改 norm，不擴張為 Final Adjudication 權限。DA 無 §4 diversity 關係；替代不記 `diversity_lost` |
| **R-EX** `executor` | Opus 4.8／`high` → Fable 5.1／`high` | 接手 Executor 沿同一 worklog identity（impl-default §10）。替代為 Opus 4.8 不改變 §4 兩條恆有關係（Executor 與 Alternate 仍不同 model）；替代為 Fable 5.1 時 Executor 與 `alternate_reviewer` 同 model，記錄 `diversity_lost`。Codex 不列入（§6） |
| **R-PR** `primary_reviewer` | **單一 Claude path：Opus 5.5／`xhigh` → Opus 4.8／`xhigh` → Fable 5.1／`xhigh`**。§6 條件 1–3（resolution）：有效 mapping ＝ 本列首項 Opus 5.5／`xhigh`，其後依 rule 1 沿本列替代。§6 條件 4（Codex 當次不可用，substitution）：自本列第一個可用者起替代。Codex 不在本列 | **Codex 為有效 Primary 時**：只有當次 dispatch 錯誤、當下可用性檢查證據（rule 1），或當次無法取得 Bindings 宣告的 binding qualification 證據，才進入 Claude path；Codex 恢復可用不重開已完成的 audit。Codex 被任一 Anthropic model 替代時 §4 第三條關係（family diversity）不再成立，記錄 `diversity_lost`；替代為 Opus 5.5 或 Opus 4.8 時兩條恆有關係仍成立。**Opus 5.5 為有效 Primary 時**：替代為 Opus 4.8 不記 `diversity_lost`（Primary 與 Alternate 仍不同 model）。兩種情況下替代為 Fable 5.1 時，該 cycle 的 `alternate_reviewer` 依 R-AR 列替代（R-AR 列中無 Fable 5.1），使 Alternate 與 Primary 維持不同 model；Alternate 仍 MUST 為 fresh context（Minimal §2.1、§2.3），同 model 與否不影響此點。`diversity_lost` 依 Alternate 的替代結果判定：替代為 Opus 4.8 時 §4 兩條恆有關係仍成立，不記（Codex 為有效 Primary 時仍因 §4 第 3 條記錄）；替代為 Opus 5.5 時依 R-AR 記錄。R1 前已替代者：Codex 為有效 Primary 且 R2 dispatch 時 Codex 可用者，R2 MUST 由 Codex 以 fresh context 執行並重讀 R1 record 與修正後證據（§6）；其他情況 R2 由同一替代 reviewer 延續其 R1 context（Minimal §2.3）。**R1 與 R2 之間發生替代者（含 Codex R1 後 Codex 當次不可用），R2 MUST 為 fresh context 並重讀 R1 record 與修正後證據**（不同 model 無法延續前一 model 的 context） |
| **R-AR** `alternate_reviewer` | Opus 4.8／`xhigh` → Opus 5.5／`xhigh` | 仍 exactly one Alternate；不因替代重跑 R1／R2。替代為 Opus 4.8 不記 `diversity_lost`（與 Executor、Primary 皆不同 model）。替代為 Opus 5.5 時 Alternate 與 Executor 同 model（Opus 5.5 為有效 Primary 時亦與 Primary 同 model），記錄 `diversity_lost`。Codex 不列入（§6） |
| **R-FA** `final_adjudicator` | Opus 5.5／`xhigh` → Opus 4.8／`xhigh` | 替代 FA 的 ruling 即為有效 ruling（authority 屬角色，不屬 model；Minimal §2.2）；不採 provisional。FA 無 §4 diversity 關係；替代不記 `diversity_lost` |
| **R-OR** `orchestrator` | Opus 4.8／`high` → Fable 5.1／`high` | Successor 以同一 run identity 從權威紀錄 bootstrap（orch-default §8）；替代於 run record 記錄。Orchestrator 無 §4 diversity 關係；替代不記 `diversity_lost`。Codex 不列入：control plane 是 harness session 本身，須承接 orch-default 的 binding、checkpoint 與 successor bootstrap |

六個 policy 的 fallback 列皆不以該 identifier 的有效預設 model 為首項，無重複項，只含 §2（含 Opus 4.8 說明段）已出現的 Anthropic model，且**不含 Codex**；R-PR 是單一 Claude path，同時涵蓋 `primary_reviewer` 的兩種有效 mapping（Codex 或 Opus 5.5）：前者自首項起替代，後者的有效 mapping 即首項、自第二項起替代。

## 4. Assurance defaults

- **Intended diversity（預設拓樸）**：本 Profile 宣告的 diversity 關係有兩條恆有、一條條件性：
  1. `alternate_reviewer` model ≠ `executor` model（恆有；Fable 5.1 vs Opus 5.5，tier diversity）；
  2. `alternate_reviewer` model ≠ `primary_reviewer` model（恆有；Fable 5.1 vs Codex 或 Opus 5.5）；
  3. `primary_reviewer` model ≠ `executor` model，且為跨 vendor（family diversity）——**只在 Codex 為有效 Primary 時成立**（§2、§6）。
  Bindings 未授權 Codex 時，Executor（Opus 5.5）與 Primary（Opus 5.5）同 model 是預設，不是異常，第 3 條不存在。三條都是 assurance 偏好，不是 Minimal §2.3 independence 的條件；independence 只由四項 properties 定義，同 model 的 fresh-context review 是合法 independent review，不同 model 也不自動構成 independent review（Minimal §2.2、§2.3）。
- **`diversity_lost` 的定義**：某次 replacement 使上一 bullet 宣告的任一關係（含第 3 條，若 Codex 為有效 Primary），或 Project Bindings 另行宣告的 diversity 關係，不再成立。只在該情況記錄；預設拓樸本身允許的同 model 組合（未授權 Codex 時 Executor＝Primary＝Orchestrator；DA＝Alternate＝FA）不記；§6 條件 1–3 使 `primary_reviewer` 解析為 Opus 5.5 是 resolution，不是 substitution，不記。替代仍合法；記入該 audit record 的 independence 說明（Minimal §4.6）。本版預設下會觸發的情況：`alternate_reviewer` 替代為 Opus 5.5（含 `primary_reviewer` 替代為 Fable 5.1 而 Alternate 依 R-AR 落到 Opus 5.5 的情形）；`executor` 替代為 Fable 5.1；**Codex 為有效 Primary 時**另有：`primary_reviewer` 被任一 Anthropic model 替代。不觸發：`executor` 替代為 Opus 4.8；`primary_reviewer` 替代為 Opus 4.8（Opus 5.5 為有效 Primary 時）；`primary_reviewer` 替代為 Fable 5.1 且 Alternate 依 R-AR 替代為 Opus 4.8（Codex 為有效 Primary 時仍因第 3 條記錄）；`orchestrator`、`design_authority`、`final_adjudicator` 的任何替代（仍 MUST 記錄 substitution 本身）。**上述列舉以其他 identifier 維持有效預設 mapping（`primary_reviewer` 依 §6 解析後者）、且 Project Bindings 未另行宣告 diversity 關係為前提；多個 identifier 同時處於替代狀態，或 Bindings 宣告的關係因替代而不再成立時，一律依本 bullet 的定義以該 cycle 的實際 mapping 判定。** Project Bindings MAY 宣告特定高風險類別要求恢復 diversity 後再 audit；此為 assurance policy 宣告，不是新 audit round。
- **Tier diversity 與 family diversity**：本 Profile 預設 model 皆為同一 vendor；Fable 5.1、Opus 5.5、Opus 4.8 之間的差異是 tier diversity。跨 vendor 的 family diversity 只在 Project Bindings 依 §6 授權 Codex 時存在（Codex 為有效 `primary_reviewer` 時即為第一 bullet 的第 3 條關係）。兩者都不是 independence。Bindings MAY 對高風險類別宣告要求 family diversity（例如要求 Codex 恢復可用後再 audit）。
- Reviewer-tier diversity（Primary vs Alternate）不是要求（Final Architecture Review G-1 ruling：NON-MATERIAL）；本 Profile 預設以 Fable 5.1 擔任 Alternate 只是偏好，即第一 bullet 的兩條恆有關係。

## 5. Binding verification

規範依據：Minimal §2.2、§2.3、§5.1。

**Claude Code harness 預設機制（SHOULD）**：角色 definition 檔綁定完整 model id 與 effort；每次 dispatch 以 harness 記錄的 `message.model` 與 `effort` 對照 definition；結果引用於 worklog／audit record。不設會覆寫角色綁定的全域 subagent model override。兩項 harness 事實（採用專案於 Claude Code 2.1.274／2.1.280 實測）：

- **Agent tool dispatch 形態**同時套用 definition frontmatter 的 `model` 與 `effort`（frontmatter effort 覆蓋使用者層設定）。
- **`claude --agent <name>` 主 session 形態只套用 frontmatter `model`，不套用 `effort`**；此形態 MUST 同時帶 `--effort <mapped effort>`，缺少即為 binding mismatch，依 Minimal §2.2 修復，不得冒充符合。

Definition 新建或變更對進行中 session 不可見；binding 驗證 MUST 在新 process 進行（definition 變更後 SHOULD checkpoint 重載，orch-default §11）。

既有機制證據：10-ASPICE_auto（dry-run 4／4、run 20／20、21／21 MATCH）與專案 19 init-probe，皆為 `claude-opus-4-8`／`claude-opus-5`／`claude-fable-5-1` 的證據；`claude-opus-5-5` 作為 `primary_reviewer`／`alternate_reviewer` 的綁定已由專案 19 於 2026-09-23 驗證。**`claude-opus-5-5` 作為 `executor` 與 `orchestrator` 的 binding 證據由採用專案提供**（與 v2.1 對 reviewer 的處理相同）；本 Profile 的採用不代表任何專案已完成該綁定。

**Codex（`primary_reviewer` preferred，§6）**：`PROJECT_BINDING`。Claude Code transcript 機制不適用於 Codex；Bindings MUST 宣告 (1) 呼叫機制、model／version 與 effort／mode，以及每次 dispatch 核對實際 model／version／effort 的 binding 證據與其位置（Minimal §2.2），並明示該機制如何滿足 Minimal §2.3 四項 properties（含 autonomous access 與 self-written record）、(2) 當次可用性的 live 證據來源（例如 CLI 自身的 status／limit 輸出或 invocation 的錯誤原文）、(3) 每次 audit record 引用該證據的方式、(4) 進入 Claude path 時 substitution 的記錄位置。已知機制範例：10-ASPICE_auto `harness_binding.md` D.4（`/codex:adversarial-review` 或 operator 授權的 wrapper skill；audit header `substitution` 欄位）；該專案把 operator override 記為 substitution，依本 Profile §6 條件 2 屬 resolution。未完成此四項宣告即為「無法完成 binding qualification」，`primary_reviewer` 解析為 Opus 5.5（§2）。

**其他 harness**：`PROJECT_BINDING`。

Prompt 自稱、設定存在、model 名稱相同，皆不構成 binding 證據。不同 model 不自動構成 independent review。

## 6. Codex：僅作為 `primary_reviewer` 的 preferred／effective mapping

**`primary_reviewer` 的 Codex-preferred resolution。** Codex（OpenAI）是 `primary_reviewer` 的 preferred model：Project Bindings 授權 Codex（宣告可用性、model／version、effort／mode 對應與 §5 的四項 binding verification 內容）且當次可用時，Primary Independent Reviewer MUST 使用 Codex（fresh context；R1／R2 與 Spec Integration Audit 同）。只有下列情況才進入 R-PR 的單一 Claude path（Opus 5.5／`xhigh` → Opus 4.8／`xhigh` → Fable 5.1／`xhigh`）：

1. Bindings 未授權 Codex（新專案未宣告即屬此類）；
2. operator 或專案明確禁用 Codex（Bindings 或其引用的 decision record 記載，含撤銷方式）；
3. 無法完成 binding qualification（§5 四項宣告未齊，或 Bindings 記錄的 qualification probe 未通過）；
4. 當次不可用（§3 rule 1 的當次錯誤或可用性證據，或當次無法取得 §5 宣告的 binding 證據）。

1–3 是 resolution：有效 mapping 即為 Claude path 首項 Opus 5.5／`xhigh`，不記 substitution；其後的替代依 §3 rule 1 沿 Claude path 進行（Opus 4.8／`xhigh` → Fable 5.1／`xhigh`）。4 是 substitution：自 Claude path 第一個可用者起替代並記錄，且因 §4 第 3 條關係消失而記 `diversity_lost`。不得憑先前不可用狀態預先排除 Codex（Minimal §2.2）；Codex 恢復可用不重開已完成的 audit 輪次（既有 R1／R2／Alternate 結論不因此重做；Minimal §4.5 換 model 不構成 reset），自下一次 `primary_reviewer` dispatch（含進行中 cycle 的 R2）起回到 Codex。

**其他角色。** 本 Profile 只在 `primary_reviewer` 使用 Codex：Codex 不列入 `design_authority`、`executor`、`alternate_reviewer`、`final_adjudicator`、`orchestrator` 的預設或任何 fallback 列，本 Profile 亦不提供其他角色的 Codex override 語義。Project Bindings 依 Minimal §2.2 仍可記錄自己的 overrides；若 Bindings 以 Codex 作為其他角色的 override，其 binding verification 與對 §4 diversity 關係的影響由該 Bindings 自行宣告並記錄，不屬本 Profile 的預設拓樸。

Codex 不因是不同 provider 而自動構成 independence；仍須滿足 Minimal §2.3。

## 7. Reusable subagents

同 v1：`master_governance` 中無已採用且有明確獨立 definition 的 reusable subagents，本版不新增推測性 rows。日後採用時依 Minimal §2.1–§2.2 在 Profile 或 Project overrides 中列明 identifier 與 mapping。

## 8. Change record

| Version | Date | Status | Basis | Change |
|---|---|---|---|---|
| `v1` | 2026-09-16／17 | Adopted | Final Architecture Review：ADOPT | 初版；`primary_reviewer` = `USER_SELECTION_REQUIRED`；`orchestrator` 與三項 replacement policy = `TBD` |
| `v2` | 2026-09-22 | **Candidate** | [vNext Architecture Analysis](<../../../Governance vNext Architecture Analysis(Fable-5.1).md>) §B.1、條件 C-5；operator S-1 決定 3（2026-09-22） | 全部 identifier 有預設值；deterministic replacement policies R-DA～R-OR；assurance defaults（cross-model 為預設、非 independence）；Codex override／replacement；`PROJECT_BINDING` 取代 `USER_SELECTION_REQUIRED`；無 `TBD`。S-4（M-4，2026-09-22）：R-DA 移除 provisional decision 與 primary-model 追認；替代 DA 的有效 decision 即為 DA decision，與 R-FA 同理由 |
| `v2` adoption／freeze | 2026-09-22 | **Adopted／Frozen** | S-3 [Opus 5 acceptance review](<../../../Governance v2.0 Candidate Independent Acceptance Review(Opus-5).md>)：ADOPT WITH REQUIRED CHANGES；S-4 M-4 correction；[Opus 5 closure](<../../../Governance v2.0 Candidate S-4 Closure Review(Opus-5).md>)：M-4 CLOSED；pruning P-13；[Astra final regression](<../../../Governance v2.0 Final Pruning Regression Check(Astra).md>)：PASS；operator S-5 明確授權（[Adoption and Freeze Record](<../../../Governance v2.0 Adoption and Freeze Record.md>)） | **`default / v2` formally Adopted／Frozen**；僅更新 header 與本列 metadata；mapping、replacement policies、assurance defaults、binding verification 不變 |
| `v2.1` | 2026-09-23 | **Candidate** | Operator 指示（2026-09-23）：官方新 model Opus 5.5（`claude-opus-5-5`）發布，預設 Opus 5 改為 Opus 5.5 | **Model-id revision only**：§2 `primary_reviewer` 由 Opus 5／`claude-opus-5` 改為 Opus 5.5／`claude-opus-5-5`；§3 R-DA、R-EX、R-PR、R-AR、R-FA、R-OR fallback 列中的 Opus 5 改為 Opus 5.5；§4 cross-model 預設說明相應更新。Opus 4.8、Fable 5.1 mapping、effort、replacement 順序、assurance policy、binding verification 不變。採用專案須以自身 §5 證據驗證 `claude-opus-5-5` binding |
| `v2.1` adoption／freeze | 2026-09-23 | **Adopted／Frozen** | Operator 於 2026-09-23 對「直接以 model-id 小改採用」回覆「可以」並指示更新 HTML 與 sync Notion；變更僅為 model id，不觸及 role authority、independence、audit bounds，未另行 independent review | **`default / v2.1` formally Adopted／Frozen**；僅更新 header 與本列 metadata；mapping、replacement policies、assurance defaults、binding verification 與 Candidate 內容相同；同一採用動作中修正 Candidate 漏改的自我版本引用（本檔導言「專案採用 `default`＋`v2`」→「`v2.1`」） |
| `v2.2` | 2026-09-23 | **Adopted／Frozen** | Operator 指示（2026-09-23）：review 時 effort 升一級；operator 選定「新 Model Profile 版本」方案（Option A）並明確授權；effort-only revision，不觸及 role authority、independence、audit bounds，未另行 independent review | **Effort-only revision**：§2 `primary_reviewer` effort 由 `high` 改為 `xhigh`；§3 R-PR 最後一個 fallback Opus 4.8 由 `high` 改為 `xhigh`，使替代 Primary Reviewer 不低於預設 effort。Model mapping、其他角色 effort、replacement 順序、assurance policy、binding verification 不變。預期成本：Primary Reviewer 承擔 R1／R2 與每份 Spec 的 Spec Integration Audit，token 與時間成本相應增加 |
| `v2.3` | 2026-09-29 | **Candidate** | Operator 決定（2026-09-29）：所有 Opus 4.8 production default 改為 Opus 5.5，Opus 4.8 保留於 fallback，Fable 5.1 roles 與所有 effort 不變，不修改 Minimal v2.0／impl-default v2／orch-default v2；依據 [Production Confirmation and Future Direction Analysis](<../../../Governance v2.0 Production Confirmation and Future Direction Analysis(Fable-5.1).md>) §2.4、§4.5 與 [Production Mapping Migration Review](<../../../Governance Model Profile Production Mapping Migration Review(Fable-5.1).md>) D-1～D-20；operator 於同日核准起草 | **Production mapping migration**：§2 `executor` 與 `orchestrator` 由 Opus 4.8／`claude-opus-4-8` 改為 Opus 5.5／`claude-opus-5-5`（effort `high` 不變）；§2 加 Executor／Primary／Orchestrator 同 model 說明。§3 rule 1 明列 classifier refusal 為 dispatch 錯誤、overload 的 bounded retry 交 Bindings 宣告；rule 3 的 `diversity_lost` 錨定至 §4 定義。§3 六條 fallback 列重排：R-EX 與 R-OR 首項改 Opus 4.8（原首項為 Opus 5.5 本身）；**`primary_reviewer` 改為 Codex-preferred resolution（operator 第二次 clarification，2026-09-29）**：§2 該列 model ＝ Codex（preferred；version／effort／verification ＝ `PROJECT_BINDING`），Claude fallback Opus 5.5／`xhigh`；未授權、明確禁用或無法 qualify 時有效 mapping 即為 Opus 5.5（resolution，非 substitution）；R-PR 分兩條列（Codex 有效：Opus 5.5 → Opus 4.8 → Fable 5.1；Opus 5.5 有效：Opus 4.8 → Fable 5.1），Fable 替代時 Alternate 依 R-AR 列、R1／R2 之間替代者（含 Codex R1 後不可用）R2 fresh context；§5 加 Codex 的四項 `PROJECT_BINDING` 宣告內容（範例 10-ASPICE_auto D.4）；§6 改寫為 Codex-preferred 條件 1–4；R-AR 改為 Opus 4.8 → Codex → Opus 5.5（原 Opus 5.5 → Codex）；R-DA 與 R-FA 各加 Opus 4.8／`xhigh` 為末位。§4 改寫：intended diversity 兩條恆有（Alternate ≠ Executor、Alternate ≠ Primary）加一條條件性（Codex 為有效 Primary 時 Primary ≠ Executor 且為 family diversity）；未授權 Codex 時 Executor＝Primary 同 model 是預設；`diversity_lost` 定義為「替代使宣告關係不再成立」並列出觸發／不觸發情況；新增 tier diversity vs family diversity 說明。§5 加主 session 形態需 `--effort`、definition 變更需新 process 驗證、`claude-opus-5-5` 作 executor／orchestrator 的 binding 證據由採用專案提供。§6 保留 Codex 作 `executor`／`alternate_reviewer` override 的語義。§2 `orchestrator` 列的 resolution policy 與其他 Opus 5.5 列一致（不依 parent model 隱性解析）；§2 末段明記 Opus 4.8 僅保留於 fallback；§3 末加六列自我檢查句；R-DA／R-FA／R-OR 附加規則各加「無 §4 diversity 關係」句；§5「SHOULD checkpoint 重載」為 orch-default §11 之轉述。**Effort 全部不變；未引入任何 Sonnet 5.5 或 effort recalibration；不改任何 role authority、independence、audit bounds。** 註一：`orch-default / v2` §2 所引「default v2 給 `orchestrator` 預設 Opus 4.8／high」為對 default v2 的版本化陳述，仍為真；採 v2.3 的專案以 Bindings 記錄 Profile 版本即可，orch-default 不需改版。註二：`impl-default / v2` §11 所述「記錄 model diversity 是否改變」屬 default v2 §3 rule 3；v2.3 以原／替代 mapping 兩欄加 `diversity_lost` 承載同一義務，impl-default 不需改版。**Targeted independent consistency check**（fresh-context subagent，transcript 核對為 `claude-opus-5-5`／`high`；record [Targeted Consistency Check (Opus)](<../../../Governance Model Profile v2.3 Targeted Consistency Check(Opus).md>)）：初審 **REQUIRES CORRECTION**（2 MATERIAL、9 NON-MATERIAL）。M-1（§3／§4「不記」陳述無條件）→ §3 rule 3 與 §4 加前提與判定句；M-2（Migration Review D-9 的 Fable 替代觸發無法由 §4 兩條關係推導）→ R-PR 附加規則與 §4 觸發列舉改為依 Alternate 替代結果判定；N-1、N-2、N-3、N-4、N-5、N-7、N-8、N-9 一併套用；N-6（AR swap 時 R-AR 列耗盡的處理）為新語義，本版不採，留 operator 日後決定。Closure check（同一 reviewer，限 M-1／M-2 與 §3／§4 regression）：**M-1 CLOSED、M-2 CLOSED、regression PASS、final verdict PASS**（record 末段「Closure check」）。**其後 operator 第二次 clarification（2026-09-29）**：原「Keep Opus 5.5／xhigh as the default Primary Reviewer」之意為 Claude fallback，`primary_reviewer` 應為 Codex-preferred；§2、§3 rule 3、R-EX、R-PR、R-AR、§4、§5、§6 依此改寫（本列前段已反映）。第二次 targeted check（同一 reviewer；record 段「Second targeted check」）：**REQUIRES CORRECTION**（3 MATERIAL、6 NON-MATERIAL）→ M2-1（「當次無法取得 qualification 證據」同時被歸為 resolution 與 substitution）：§6 條件 3／4 重劃——常設 qualification 不成立為 resolution，當次證據取不到為 substitution；rule 3 與 §4 的 resolution 句改引 §6 條件 1–3。M2-2（R1 由替代 reviewer 執行、R2 時 Codex 恢復）：依 operator「當次可用即 MUST 使用 Codex」，R2 由 Codex fresh context 執行並重讀 R1 record；§6 明記「不重開已完成輪次、自下一次 dispatch（含 R2）起回到 Codex」——operator 若偏好 R2 一律延續替代 reviewer，此句反向改寫即可。M2-3（§5 Codex 宣告未含 binding 證據與 §2.3 四項 properties 的滿足方式）：§5 (1) 擴為含 effort、每次 dispatch 的 binding 證據與位置、四項 properties 說明。N2-1～N2-6 一併套用。Closure check（second，同一 reviewer）：**M2-1、M2-2、M2-3 CLOSED，regression PASS，final verdict PASS**（record 段「Closure check（second）」）。 |
| `v2.3` adoption／freeze | 2026-09-29 | **Adopted／Frozen** | Operator 明確授權（2026-09-29）：(1) Codex-preferred `primary_reviewer` 語義依現文核准；(2) M2-2 維持現文——R1 由替代 reviewer 執行而 R2 dispatch 時 Codex 可用者，R2 回到 Codex，fresh context 並 MUST 重讀 R1 record 與修正後證據，不改為「R2 一律延續替代 reviewer」；(3) N-6 維持 DEFERRED，Alternate replacement 列耗盡沿用 §3 rule 4 → Minimal §1.5 recovery，不另設語義。兩次 targeted independent consistency check 與 closure（[record](<../../../Governance Model Profile v2.3 Targeted Consistency Check(Opus).md>)）皆 PASS | **`default / v2.3` formally Adopted／Frozen**；僅更新 header Status 與本列 metadata；§1–§7 normative 內容與 closure 通過的 Candidate（md5 `f5796a0609758c1500eb577f3e4f1c3f`）相同。v2.2、v2.1、v2 保留為 frozen baseline；已 pin 者不自動改用；採用專案依 Minimal §5.3 記錄版本、依據與授權，並提供自身 §5 binding 證據 |
| `v2.4` | 2026-10-02 | **Candidate** | Operator 指示（2026-10-02）：只調整 `primary_reviewer` 的 model／fallback 定義——Codex 只作為 `primary_reviewer` 的 preferred／effective mapping、不得出現在任何 fallback chain、Claude path 單一化為 Opus 5.5／`xhigh` → Opus 4.8／`xhigh` → Fable 5.1／`xhigh`、保留 resolution／substitution／`diversity_lost` 語義；不修改 Minimal、audit flow、role authority 或其他 identifier 的 mapping。背景：[Package v2.1 Architecture Review](<../../../Governance Package v2.1 Architecture Review(Fable-5.1).md>) §2、§4（Codex 矩陣語義不變） | **`primary_reviewer` fallback 單一化與 Codex 範圍收斂**：§2 `primary_reviewer` 列與其下段落改寫為單一 Claude path；§3 R-PR 由兩條列改為一條（resolution 落在首項、substitution 自第一個可用者起），R-EX 與 R-AR 移除 `Codex（Bindings 宣告可用時）` 項及其 Codex 子規則，§3 末自我檢查句改為「不含 Codex」；§4 `diversity_lost` 觸發／不觸發列舉移除 `executor`／`alternate_reviewer` 替代為 Codex 的情況（Codex 不再是它們的 fallback，此類情況不再由 Profile 定義）；§6 標題與「其他角色」段改為 Codex 僅限 `primary_reviewer`，Bindings 若自行以 Codex override 其他角色，其 diversity 影響由 Bindings 宣告。**Semantic diff 摘要**：(a) `executor`／`alternate_reviewer` 的 fallback 列各少一項（Codex）；(b) R-PR 的實際替代順序不變（Codex 有效：Opus 5.5 → Opus 4.8 → Fable；Opus 5.5 有效：Opus 4.8 → Fable），只是以單一列表達；(c) §4 兩條恆有關係與第三條條件關係不變，`diversity_lost` 定義不變，Codex-with-Codex-Primary 的兩個觸發情況因 Codex 不再可作 Executor／Alternate fallback 而消失；(d) 其他五個 identifier 的 model、effort、replacement 順序不變；§5 binding verification、§6 條件 1–4、§7 不變。Header Governance 標籤由 v2.0 更新為 v2.1（metadata） |
| `v2.4` adoption／freeze | 2026-10-02 | **Adopted／Frozen** | Operator 於 2026-10-02 對 Candidate 與其 semantic diff 回覆「採用」並明確授權；變更只涉 `primary_reviewer` fallback 表達與 Codex 範圍，不觸及 role authority、independence、audit bounds，未另行 independent review（與 v2.1、v2.2 的 model-id／effort-only 採用慣例相同） | **`default / v2.4` formally Adopted／Frozen**；僅更新 header Status 與 Supersedes 兩行及本列；§1–§7 與 Candidate 相同（Candidate md5 `fd5898c8f8dc6bbc0d7934ef0b92e3ba`）。v2.3、v2.2、v2.1、v2 保留為 frozen baseline；已 pin 者不自動改用；採用專案依 Minimal §5.3 記錄版本、依據與授權 |

本 Profile 之後的變更依 Minimal §5.3 留下版本、依據與授權；新版本不自動適用既有專案。
