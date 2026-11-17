# Implementation Profile — default v2

**Profile ID: `impl-default`**  
**Version: `v2`**  
**Status: Adopted／Frozen（2026-09-22，operator S-5）**  
**Governance: Minimal Operational Governance v2.0（Adopted／Frozen 2026-09-22）**  
**Revision type: semantic revision of `impl-default / v1.1`：§6 新增 Spec Integration Audit dispatch HOW、§8 authorization 改核對 Outcome Contract、§12 新增 property E；§3、§5、§7、§9、§10 implementation method 不變**  
**Supersedes for new adoption: `impl-default / v1.1`（[default-v1.1.md](default-v1.1.md) 與 [default-v1.md](default-v1.md) 保留為 frozen 歷史 baseline；已 pin 者不自動改用）**  
**Type: reusable implementation / HOW profile**

## 1. Purpose, precedence and adoption

> This Profile defines implementation HOW only. It is subordinate to Minimal Operational Governance v2.0, Project Bindings, and the Accepted Work Contract（Outcome Contract 及其 derived contracts）. Matt, Addy and Superpowers material is used only as implementation-pattern input; adopting a pattern adopts none of the source framework's workflow, stop, review-round, approval or authority rules.

衝突時，依各自 authority，以 [Minimal v2.0](../../Minimal_Operational_Governance_v2.0_Candidate.md) §5.3、effective Project Bindings 與 Accepted Work Contract 為準。本 Profile 不授予權限，也不使 Binding 得以覆寫 Minimal 的 MUST。

本文件可獨立提供 Executor method；不要求安裝 Matt、Addy 或 Superpowers，不要求呼叫任何來源 skill。來源只供 attribution 與追溯，不是 Runtime dependency。本文件的 13 sections 是可重用參考，不是 13 個 gates 或每項工作需產生的 artifacts。

專案透過 Minimal §5.1 的 **Skills and runtime** binding 選用 `impl-default`＋`v2`，記錄 overrides（無則記 `none`）。可引用既有工作環境設定，不需每項工作重建。Profile 更新不自動適用既有專案或進行中工作；變更依 Minimal §5.3 留下版本、依據與授權。

以下 MUST／MUST NOT 是既有治理 properties 在執行上的表達；SHOULD 是依適用性使用的 Profile defaults，可由 Project Bindings／Runtime 調整並記錄理由。Override 不得弱化治理 properties；格式、工具、測試順序、session 與 Git 方法均不因採用本 Profile 成為 universal requirement。

| Lane | 執行方式與必要邊界 |
|---|---|
| **Lightweight** | 可 direct execution；依 accepted Work Contract、適用授權、task-applicable self-verification、durable worklog、適用 gates 與 authority routing 完成。Audit 僅依 Minimal §4.1／assurance policy 觸發。 |
| **Formal** | Outcome Contract 一次接受＋授權 → DA derive Spec＋Tickets → Orchestrator；implementation、verification、mandatory independent audit（per Ticket）、Spec Integration Audit（per Spec，Minimal §4.7）與 completion 依 Minimal §3–§4。 |

Lightweight **不因採用 Profile** 而要求 full Orchestrator activation、fresh worker dispatch、Git diff package、Matt subagent review、full suite 或 formal audit。Grill 不必產生 Spec／Tickets；DA decision record 能合法釐清時可留在 Lightweight。是否需設計基線、多 execution units／dependencies 或跨 session orchestration 而進 Formal，仍由 Minimal §3.6 決定；本 Profile 不另建第三條 lane。

## 2. Control-plane boundary

保留我們現有 Orchestrator 角色作唯一 orchestration control plane。可重用的 control-plane reference 為 [Reference Orchestrator Contract `orch-default`／`v2`](../orchestrator-contracts/default-v2.md)（Adopted／Frozen 2026-09-22）：新 Minimal 專案以它為 Orchestrator reference，透過 Bindings 記錄採用與 overrides。採用專案引用自己的有效 contract／implementation。歷史／來源出處見本檔 Appendix A.1。

Orchestrator 管理 work／ticket graph、frontier、dispatch、routing、progression、continuation、recovery coordination、rollover coordination 與 completion reporting。依 Minimal §2.1／§2.4：implementation HOW 交 Executor；finding／evidence sufficiency 交 Reviewer；design semantics 交 Design Authority；review dispute／合法 disposition 交 Final Adjudicator。Routing 依 Minimal §2.4 的 authority table 與五種 deterministic cases；Orchestrator 不自行改分類。

Orchestrator 啟動後依 Minimal §1.4–§1.5 自主完成：判斷、rework、review escalation、phase progression、agent replacement 或 context rollover 是 routing／recovery 事項，不是例行 operator checkpoint。取得有權裁決後繼續合法工作；只有真正 external／non-delegable boundary 才停止受影響路徑。

Matt `/implement-spec`、Superpowers SDD controller 或其他 framework controller **MUST NOT acquire orchestration authority**。可取用其 implementation patterns，不導入第二個 lifecycle owner、controller adjudication、額外 audit rounds 或人類逐階段核准。Lightweight 透過已配置機制做 authority routing，不因此啟動完整 Formal run。

既有 v2 adopters 的 migration constraints 見本檔 Appendix A；不適用於新專案的正常 activation。

## 3. Executor implementation method

以下 method 從 Matt `/implement` 實際內容抽取並改寫，直接由本 Profile 提供；Executor 不需讀取或執行來源 skill。

1. **建立工作依據。** 讀取 accepted Work Contract、適用上位契約、verification expectations、授權與既有 decisions。Formal 使用 Ticket 及其引用 Spec；Lightweight 使用 accepted brief／prompt／其他契約，不要求補造 Spec。
2. **先理解受影響材料。** 修改前檢查相關程式、產物、測試、介面與專案慣例，確認現況及影響範圍。採 targeted read，必要時自行擴展；不以 Executor 報告或過往對話取代來源。
3. **漸進實作。** 在 accepted scope 內以可驗證的小幅變更推進，優先沿既有邊界整合。Executor 自主選擇 HOW；不得靜默改 requirement、AC、invariant 或 gate。
4. **邊做邊驗證。** Executor 使用 accepted verification contract、affected behavior 與 material introduced risk 決定適用驗證。SHOULD 在適用時執行 focused tests／typecheck；TDD 可用於能清楚表達行為的 seams，不要求 everywhere。結束前 SHOULD 做涵蓋影響面的較廣驗證；full suite 僅在其 coverage 適用或契約／gates 要求時執行。
5. **檢查自己的工作。** Return 前 SHOULD 比對實際產物與 accepted scope、適用標準、失敗行為及 verification evidence，確認遺漏、非預期變更與風險。可由自己完成，不要求另一個 Agent 或獨立 self-review artifact。
6. **留下可接手結果。** 更新同一 worklog，依 §4 回報實際完成、證據、限制與剩餘工作。需要 commit／其他保存操作時，依 Project Bindings 的工具、權限及 Git 慣例執行；不預設 current branch、merge、push 或 release。

Accepted contract 已定義的 oracle／seam 語義與 evidence sufficiency 不由下游重新定義。HOW 的 seam selection 不觸發執行中 operator approval；material ambiguity 交 DA，涉及契約語義改變則走 Minimal 的 acceptance／authorization。未受影響且可合法執行的工作繼續。

## 4. Executor result contract

Executor → caller／Orchestrator 使用精簡 return；自由文字或既有工具格式均可。以下 status 是 **Profile HOW 的報告用語，不是 Governance lifecycle state machine**，不要求存入新欄位或固定 JSON。

| Suggested status | 意義與接續 |
|---|---|
| `DONE` | Executor 所受派工作及 self-verification 已完成；caller 仍依適用 audit／completion gates 決定後續，不等於 formal closure、phase acceptance 或 release。 |
| `DONE_WITH_CONCERNS` | Executor 工作已完成，有明列限制／concerns 待有權角色處理；不代表可豁免 gate。已知尚未完成的必要實作或驗證不得藏在此狀態。 |
| `BLOCKED` | 目前受派工作有具體阻擋；指出 required authority、reason、remaining work 與可行下一步。Caller route／repair／replace，而非自動回 operator。 |
| `NEEDS_CONTEXT` | 缺少繼續所需的具體材料或需 context replacement；說明缺什麼、已查來源與剩餘工作，供 caller 補足或 recovery。不得只因偏好 fresh session 而停止 run。 |

Return 至少表達：

- Result／work performed，及適用的 subject／artifact version 或 bounded state。
- 實際 verification 方法、結果與 evidence reference；未執行、失敗或無法確認者明記。
- Worklog reference。
- Unresolved concerns 與 remaining work；無則明記無。
- 有阻擋時的 required authority＋reason（SHOULD 指明）。其後 routing 依 Minimal §2.4。Executor 對 boundary 的疑義以 `BLOCKED`＋required authority = Design Authority 提出（Minimal §1.2），不直接指向 acceptor。

可引用既有 worklog／evidence，無須重複完整內容或另建 report file。Executor 的 return 不是 independent audit record，也不能自行裁決 review dispute。

## 5. Self-verification and quality floor

兩 lane 的 self-verification 依 Minimal §3.5，涵蓋適用正常／失敗行為及變更引入的實質風險；不僅是 acceptance tests 綠燈。

Executor MAY 用 own reasoning、subagents、Standards／Contract 雙軸檢查、doubt-driven checks、static analysis 或 tests。對非顯然且後果重大的假設，SHOULD 在可用且適合時使用 fresh-context doubt check；這是 self-verification 方法，不是固定 review hop，也不要求每 cycle 向 operator 提供跨模型選擇。

> A review inheriting Executor context MUST NOT be represented as formal independent audit.

Self-review 結果作為 worklog 的 verification 資訊或引用，與正式 audit 狀態區別。Fresh context 或不同 model 單獨都不把 self-check 升格為正式 audit；正式 audit 必須走 §6 的 separately bound path。不禁止 Executor 使用 subagents；實際使用者仍受 Minimal 的 definition／binding 與 delegated authority 限制。

> An implementation MUST NOT obtain a passing result by weakening the accepted verification or quality floor.

SHOULD 以適用的 diff-scoped quality floor guard 檢查新 suppressions、skipped／deleted tests、降低 thresholds、placeholder／stub substitutions 是否掩蓋未完成工作或削弱已接受保證。這些是檢查線索，不是對合法 test doubles、測試替換或合理工具例外的全面禁止。

例外必須有 accepted contract／authorized decision 的有效依據；Executor 自寫理由不等於授權。若實際改變 accepted verification／quality 語義，仍依 Minimal §5.3 走 contract change。具體規則、thresholds 與工具屬 **Project Assurance Policy／Runtime**，不要求 `CONSTRAINTS.md`、新 validator 或安裝特定工具。

## 6. Formal independent audit

> Executor self-verification ≠ Formal Independent Audit.

Formal mandatory audit；Lightweight 是否 audit 僅依 Minimal §4.1、accepted contract 與 assurance policy。Applicability 未配置或有實質爭議時 route 至 DA，不默認省略。正式 audit 一旦觸發，兩 lane 使用同一 semantics。

R1／R2 由 **separately bound Primary Independent Reviewer** 執行，依 Minimal §2.3 同時滿足：

1. **Independent context**：R1、Alternate 與 Final Adjudication 使用 fresh independent context，不繼承 Executor 的對話／推理／結論；R2 可延續 Reviewer 自己的 R1 context，但重讀修正後證據。Alternate 亦不繼承 Primary Reviewer 對話。
2. **Verifiable binding**：實際角色、model／version 及適用 effort／mode 可核對。
3. **Autonomous access**：自主取得 subject 與原始材料，不被預先挑選的 diff／摘要限制 coverage。
4. **Self-written record**：Reviewer／Final Adjudicator 自行寫入其 findings／verdict／ruling，Executor 不代寫、改寫、篩選或決定是否記錄。

派工使用 Orchestrator 或 Project Bindings 宣告且可驗證滿足四項 properties 的 Harness 機制；direct execution session 透過該機制發起亦合法。能力不足時依 Minimal §2.3 的 configured dispatch boundary，不把 ad-hoc subagent 冒充正式 Reviewer，也不新增 operator approval。

```text
R1 — full independent audit of accepted work scope
  ├─ no blocking → audit closure
  └─ blocking → targeted correction → R2 scoped closure review
                                      ├─ no unresolved blocking → audit closure
                                      └─ blocking → exactly one Alternate Review
                                                      ├─ no unresolved blocking → audit closure
                                                      └─ unresolved → Final Adjudication
```

Reviewer HOW 可採 Standards／Contract／風險檢查、don't-trust-report、verify-the-verification：依實際產物驗證 Executor 主張及測試證據，而非接受敘述作為證明。Reviewer 自主判定 findings、severity／blocking 與 evidence sufficiency，不取得 Design Authority。Reviewer 對受審 implementation、tests、contract 與 gates 唯讀，可自主執行必要檢查；不導入來源 framework 對測試重跑或 source access 的限制。

Targeted correction 聚焦 blocking findings並提供 closure／regression evidence。R2 核對原 blocking、修正造成的回歸，以及修正直接產生或暴露的 blocking defects，不成為第二次無限制 full audit；逐 finding 的 addressed／not addressed 是可選呈現法，不是新 grammar。

Non-blocking 不延長 cycle；design issue 隨時 route DA。Final Adjudicator 依 Minimal §4.5 處理爭議、disposition 與合法新 cycle，裁決後繼續；本 Profile 不額外授權 deferral 或 cycle reset。Audit closure 不取代 Minimal §3.8 的其他 completion 條件；Lightweight full audit 指完整 accepted scope，不要求 Spec artifacts。

**Spec Integration Audit dispatch（Minimal §4.7；Formal 每份 Spec MUST）。** 一份 Spec 的全部 implementation Tickets 結案後、DA phase acceptance 前，透過同一 §2.3 機制以 fresh context 派 `primary_reviewer`（或 Bindings 宣告的同角色 mapping）審查**整合後的最終 subject**。Dispatch pack（SHOULD）：Outcome Contract 引用；Spec 及其 derivation record；全部 Ticket audit records 與 closure evidence 的引用；integration verification evidence 引用；最終 subject identity（§7）。Pack 是入口不是上限。Reviewer 的 record MUST 逐項記載五個範圍的結論：跨 Ticket invariants、Spec-level AC coverage（含 Spec AC 整體是否涵蓋其 derivation record 所分配的 Outcome Contract acceptance boundary 部分；該 Spec 為同一 Outcome Contract 最後一份未結 Spec 時，另核對全部 derived Specs 的分配合起來涵蓋整個 acceptance boundary）、整合行為、最終 subject coverage、Spec／Tickets 對 Outcome Contract 的 traceability 與 boundary 符合性。Findings 依 Minimal §4.3–4.6 同一套 R1／R2／一次 Alternate／FA 處理，自成 cycle；不重開已閉合 Ticket finding，除非新 integration-level evidence。修正是契約內 rework：依 §7 識別 delta、派 Executor targeted correction、審後驗證，不需新授權。

**單 Ticket fast path 的核對（Bindings 宣告採用時）。** Orchestrator 只核對該 Ticket audit record 是否**明文**逐項涵蓋上述五個範圍且 subject 為最終整合 subject；缺任一項即另派 Spec Integration Audit。不得把既有 Ticket R1 record 事後重新標示或補註為 Spec Integration Audit。

## 7. Evidence and subject identity

**Every verification／audit result MUST identify the subject version or bounded artifact state it covers.** 可透過可靠 evidence 引用識別，不要求每份記錄重複欄位。工作邊界、適用契約及實際產物須可對應；Executor report 是待驗證主張，不單獨構成充分 evidence。

在適用的變更工作中，SHOULD 於 dispatch 前確立 BASE／subject boundary，並在 review 前確認實際受審版本與範圍。Git 可用 base..head、commit SHA、merge SHA；其他產物可用 content hash、version、snapshot 或等效 stable identity。DA clarification 等非產物變更派工不需憑空建立 BASE。

Git diff review package 是適用時的 SHOULD default，可含實際 diff、變更範圍及 evidence refs；非 Git 工作直接提供 artifact subject。Package 是入口，不限制 Reviewer 自主探索，也不要求額外 package file。

> The final closed subject MUST have valid verification and, where required, audit coverage.

Audit 後有變更，須識別 delta 並核對既有 coverage；依 Minimal §3.8 執行相應 post-review verification。可能影響原 review 結論者，由 Reviewer／DA 判斷必要後續 audit／verification，不能由 Orchestrator 自行宣稱 evidence 足夠。後續沿 Minimal §4 既有 audit semantics，不新增 round 或自動重開 full audit。

Literal SHA equality 可作 Git Runtime fast-path check，但不是 universal semantic rule；相同 SHA 也不單獨證明原 audit 有效、coverage 充分或環境證據仍適用。跨 Ticket 整合依 Minimal §3.8 做適用 integration verification。

## 8. Authorization

Formal implementation／rework dispatch 前，**effective authorization MUST exist and cover the intended scope**（Minimal §1.2、§3.4）。核對內容：(a) Outcome Contract 的接受與授權紀錄存在、有效，且其授權涵蓋 implementation（或 Bindings 依 Minimal §5.2 保留 implementation authorization 時，另有該授權紀錄）；(b) 被派工的 Ticket 引用其 Spec、Spec 引用其 Outcome Contract，且 Spec／Ticket 附 DA derivation record（含 boundary determination）；(c) accepted contract 的適用版本對應。某個 authorization file 或 derivation record 存在本身不充分；Orchestrator 只核對存在與對應，不判斷 boundary determination 的內容。

此項不將 implementation authorization 誤套到 planning、DA derivation／design work 或其他非 implementation dispatch；那些工作依 Outcome Contract 對規劃與設計的授權執行。已有有效授權的契約內 rework／re-verification 不新增 operator gate；改變 accepted 語義的 contract change 及受其影響的實作仍依 Minimal §5.3。

Lightweight 依 Minimal §1.2 的 direct acceptor instruction 或明確 standing authorization；該指令即 Outcome Contract。一次指令可同時接受與授權其涵蓋工作，但不得推定未宣告範圍、代理 intent 或新 follow-up 已被接受。Merge／push／release 是否授權依 Project Bindings；work item completion 不授予 release permission。

## 9. Worklog and handoff

Worklog identity、必要內容、authority boundary 與跨 session continuity 以 Minimal §3.7 為唯一規範定義。

實作 expectation：

- 在 meaningful handoff-capable points 更新，特別是裁決、驗證、audit 狀態或 remaining work 改變時；不等成功後才補記。失敗、中斷或取消的 execution 同樣保留紀錄。
- Executor return 引用 worklog；接手 session、Reviewer 與 Orchestrator 能取得並理解。
- 已有 project record 滿足 properties 時直接重用；允許引用原始 evidence，不要求第二套 ledger、固定 layout、schema 或一個 identity 對應一個實體檔案。

Worklog-existence machine check 是適用時 SHOULD；worklog 本身仍是 MUST。

## 10. Context replacement and recovery

對已選擇 worker dispatch 的工作，fresh Executor per work item 是 SHOULD default；Project Bindings／Runtime 可選 resume 或其他合適 context 方法。Lightweight direct execution 不因此必須派新 worker。正式 Reviewer／Adjudicator 的 independence 則不是可 override 的 freshness 偏好。

接手 Executor 使用同一 worklog identity，行動前從 contract、worklog、產物、裁決與原始 evidence 重新理解 authority、status、verification／audit coverage 與 remaining work。Conversation summary 不單獨建立 authority；不把未知 assignment 當成功，重派前處理既有 worker 與重複副作用風險（Minimal §3.8）。

Recovery 依 Minimal §1.5：先 authoritative re-ground、已授權 replacement／repair、適用 DA／Final Adjudicator routing；三者完成後仍 unsafe／indeterminate，才可轉交 operator。恢復義務持續，不以固定 retry 次數、context threshold 或 capability label 自動結束 run。受影響的 unsafe 變更暫停；無關且合法工作繼續。

在有並行寫入或 Git 整合需求時，worktree isolation／serialized merge 是適用的 SHOULD defaults；Runtime 可選等效做法。它們不授予 merge／release authority，不強制 branch topology。Checkpoint、rollover、heartbeat、orphan reconciliation、retry algorithms 均屬 Runtime HOW，本 Profile 不重定義。

## 11. Model and role binding reference

Model defaults 引用 [Reference Model Profile `default`／`v2`](../model-profiles/default-v2.md)（Adopted／Frozen 2026-09-22）；專案可明確選擇其他 Profile 或合法 overrides。本文件不複製 mapping table，也不新增與之競爭的角色設定。

Minimal §2.1–§2.2 的六角色維持：Design Authority、Executor、Primary Independent Reviewer、Alternate Independent Reviewer、Final Adjudicator、Orchestrator。每個實際使用的 Agent／reusable Subagent 都須有 definition，且每個可 dispatch identifier 有有效 mapping；具體 loading、spawn、檔名與 frontmatter 屬 Runtime HOW。

Observed assignment MUST 符合 effective adopted mapping，包括合法 overrides、resolved model／version、適用 effort／mode。用現有 Runtime evidence 核對 definition 與 assignment，不以 prompt 自述或設定存在代替。不可用時引用當次錯誤或當下 availability evidence，依已授權 policy 修復／替代；替換 model 不改 authority。

`default-v2` 對每個 identifier 提供預設值與 deterministic replacement policy（其 §3）；resolution 順序為 Bindings override → Profile default → replacement fallback，全程不詢問使用者；使用者只透過 Bindings override record 介入。替代 MUST 引用當次錯誤或可用性證據，MUST 維持 Minimal §2.3 四項 properties，並記錄 model diversity 是否改變（其 §4）。`PROJECT_BINDING` 項（binding verification 證據位置）在對應執行／activation／audit 前由 Bindings 填入；本 Profile 不猜驗證機制，也不把採用宣告當實際 binding 證明。

## 12. Mandatory properties and optional enforcement

| Property | Requirement | Governance basis |
|---|---|---|
| **A. Binding integrity — MUST** | 實際 assignment 與 effective adopted mapping 一致，含合法 overrides、resolved version 及適用 effort／mode；可由 evidence 核對。 | Minimal §2.2、§5.1 |
| **B. Audit independence classification — MUST** | Executor-context review 不記錄或計算為 formal audit；正式 path 滿足全部四項 independence properties。 | Minimal §2.3、§4 |
| **C. Final-subject coverage — MUST** | 最終 closed subject 有有效 verification 及適用 audit coverage；依 §7 處理審後變更，不要求 literal version equality。 | Minimal §3.8 |
| **D. Authorization — MUST** | Formal implementation／rework dispatch 前，有有效且涵蓋 scope 的 Outcome Contract 接受與授權（或 Bindings 保留時的 implementation authorization）；文件存在不等於授權有效。 | Minimal §1.2、§3.4、§5.2、§5.3 |
| **E. Traceability presence — MUST** | 每個 Ticket 引用其 Spec，每份 Spec 引用其 Outcome Contract，每份 derived contract 附 DA derivation record（含 boundary determination）；核對存在與版本對應，不核對語義。 | Minimal §1.2、§3.4、§4.7 |

> Mandatory property ≠ mandatory custom checker.

依 Minimal §5.4，已存在且適用的 machine checks **SHOULD 使用**；平台提供充分資料時 MAY 建立機械檢查，但不因 property 是 MUST 就要求每個專案新增 validator。沒有 checker 不豁免 property；無可驗證能力時依有效 repair／replacement／routing 解決，不能靠文字宣稱已通過。

Check 可核對 identity、記錄引用或已授權的判斷，不把「檔案存在」「SHA 相同」「fresh 標籤」「derivation record 存在」當成 authorization、coverage、independence 或 boundary 符合性的全部證明。Evidence sufficiency、finding severity、design semantics、boundary determination 與 disposition 仍由有權 Agent 判斷。

本 Profile 的 SHOULD patterns 只在適用時使用：focused tests、final broader verification、self-review、fresh-context doubt check、fresh Executor（已選用 dispatch 時）、BASE-before-dispatch、Git diff package、worktree isolation、serialized merge、worklog-existence machine check、diff-scoped quality floor guard。Project Bindings／Runtime 可調整 HOW；不減少必需 evidence、不改 authority，也不為 Lightweight 增加 Formal ceremony。

## 13. Change record and source attribution

| Version | Date | Basis and authorization | Change |
|---|---|---|---|
| `v1` | 2026-09-17 | Fable Architecture Review 的 KEEP／HOW-profile 決定；本對話 Astra focused regression review；使用者明確指示建立並採用 Final Implementation Profile v1，納入列明修正。 | 初版：自足 Executor method、dual-lane applicability、四項 mandatory properties、replaceable HOW defaults，以及尚待執行的 Orchestrator semantic reconciliation。 |
| `v1` freeze | 2026-09-17 | [Fable 5.1 Final Independent Acceptance Review](<../../../Governance Implementation Profile v1 Acceptance Review(Fable-5.1).md>)：**ADOPT**；所有 acceptance criteria PASS，無 BLOCKER／MATERIAL findings。使用者授權本次 final freeze。 | **`impl-default / v1` formally frozen / adopted**；僅更新 acceptance metadata，§1–§12 與既有 method semantics 不變。 |
| `v1.1` | 2026-09-17 | 依據：(1) [Fable Architecture Review](<../../../Governance Implementation Architecture Review(Fable-5.1).md>) §2 的 KEEP 與 re-citation 決定；(2) [Fable Implementation Profile v1 Acceptance Review](<../../../Governance Implementation Profile v1 Acceptance Review(Fable-5.1).md>)：ADOPT；(3) 已 Adopted／Frozen 的 [`orch-default／v1`](../orchestrator-contracts/default-v1.md)；(4) [Opus 5 Reference Orchestrator Contract Acceptance Review](<../../../Governance Reference Orchestrator Contract v1 Acceptance Review(Opus-5).md>)：M-1～M-3 CLOSED、targeted regression PASS、final **ADOPT**；(5) 使用者對本次 finalization 的明確授權。 | **Metadata／dependency revision only**：§2 的 reusable Orchestrator reference 由歷史外部 v2 contract 改為 `orch-default／v1`；migration note 改為既有 v2 adopters 適用；header、§1 版本識別、§13 記錄與來源表相應更新。§1–§12 implementation semantics 未重新設計；`impl-default／v1` 保留為 frozen 歷史 accepted 版本。 |
| `v2` | 2026-09-22 | **Candidate**。依據：[Governance vNext Architecture Analysis](<../../../Governance vNext Architecture Analysis(Fable-5.1).md>) §B.2（P-2）；operator S-1 決定與兩項 refinement（2026-09-22）；Minimal Operational Governance v2.0 Candidate。 | **Semantic revision**：§1 governance 改指 Minimal v2.0；§2 control-plane reference 改指 `orch-default／v2`；§4 `BLOCKED` 的 routing 說明改為 §2.4 五情況與 boundary 疑義 DA-first；§6 新增 Spec Integration Audit dispatch HOW 與單 Ticket fast path 核對；§8 authorization 改核對 Outcome Contract 接受／授權＋derivation record＋引用鏈；§11 改指 `default-v2` 與其 deterministic replacement；§12 D 改寫、新增 E. Traceability presence；§13 本列。§3、§5、§7、§9、§10 未變。待 independent acceptance review 與使用者採用。S-4（2026-09-22，依 Opus 5 S-3 review）：§2 第二段末句由 v1.1「缺漏／爭議 → FA」改為 Minimal §2.4 五種情況（M-1）；§6 Spec-level AC coverage 改為所分配 boundary 部分＋最後一份未結 Spec 核對全部分配（M-3）。 |
| `v2` adoption／freeze | 2026-09-22 | S-3 [Opus 5 acceptance review](<../../../Governance v2.0 Candidate Independent Acceptance Review(Opus-5).md>)：ADOPT WITH REQUIRED CHANGES；S-4 M-1／M-3 correction；[Opus 5 closure](<../../../Governance v2.0 Candidate S-4 Closure Review(Opus-5).md>)：CLOSED、targeted regression PASS；pruning P-07、P-11、P-12（[Pruning Pass Report](<../../../Governance v2.0 Candidate Pruning Pass Report(Fable-5.1).md>)）；[Astra final regression](<../../../Governance v2.0 Final Pruning Regression Check(Astra).md>)：PASS；operator S-5 明確授權（[Adoption and Freeze Record](<../../../Governance v2.0 Adoption and Freeze Record.md>)）。 | **`impl-default / v2` formally Adopted／Frozen**；僅更新 header、§2／§11 package-status 括號、§13 本列與狀態段、來源表狀態括號；§1–§12 operative HOW 與 Appendix A 不變。 |

**狀態**：`impl-default／v1` 與 `v1.1` 均為 Adopted 並凍結，保留為歷史 accepted 版本。**`impl-default／v2`**（本檔）於 2026-09-22 Adopted／Frozen（S-5）。各專案仍需透過有效 Bindings 採用；Profile acceptance 不等於任何專案 Runtime／Orchestrator migration 已完成驗證。

### Evidence and adaptations

| Source | 採用／修正 |
|---|---|
| [Minimal Operational Governance v2.0](../../Minimal_Operational_Governance_v2.0_Candidate.md)（Adopted／Frozen 2026-09-22；[v1.0](../../Minimal_Operational_Governance_Final_Candidate.md) 為 frozen baseline） | Authoritative properties；本 Profile 不修改、不補造治理權限。 |
| [Reference Model Profile default v2](../model-profiles/default-v2.md)（Adopted／Frozen 2026-09-22；[v1](../model-profiles/default-v1.md) frozen） | 引用 mapping、deterministic replacement 與 assurance defaults，不複製或猜補設定。 |
| [Fable Architecture Review](<../../../Governance Implementation Architecture Review(Fable-5.1).md>) §2、§4–§8 | 保留 Orchestrator、13-section HOW reference 與 separately bound audit；依 Astra review 修正 literal equality、blanket worker ban、checker mandate 與舊語義 migration。 |
| Astra focused regression review（本對話，verdict：PASS WITH MINOR ADJUSTMENTS；未找到獨立 Markdown artifact） | 納入五項 corrections：Orchestrator predicates reconciliation、final-subject coverage、property／checker 分離、正確 independent dispatch boundary、conditional／replaceable recurring HOW。使用者在本次 implementation request 中明確接受並具體化這些修正。 |
| [原始 GPT-6 assessment F06](<../../../Governance Optimization Independent Assessment(GPT-6).md>) | Property／mechanism 分層依據；非本次 Astra regression review 的替代文件。 |
| [Matt `/implement`](../../../skills_references/matt_skills/skills/skills/engineering/implement/SKILL.md) | 原文依 Spec／Tickets 實作、適用時 TDD、持續 typecheck／focused tests、最後 full suite、code-review、current-branch commit；改寫為 §3 的 accepted-contract method、task-applicable verification、自選 self-review、依 Binding 保存，不依賴 skill。 |
| [Matt `/code-review`](../../../skills_references/matt_skills/skills/skills/engineering/code-review/SKILL.md) | 採 Standards／Contract 雙軸；不導入安裝／tracker／Spec 強制要求或兩 subagents 義務，結果只算 self-verification。 |
| [Addy doubt-driven checks](../../../skills_references/addy_skills/agent-skills/skills/doubt-driven-development/SKILL.md)／[constraint floor](../../../skills_references/addy_skills/agent-skills/skills/constraint-driven-development/SKILL.md) | 採 adversarial self-check 與不弱化 accepted floor；不導入逐次 human offer、`CONSTRAINTS.md`、固定 thresholds 或工具安裝。 |
| [Superpowers task reviewer](../../../skills_references/superpowers/skills/subagent-driven-development/task-reviewer-prompt.md)／[worktree method](../../../skills_references/superpowers/skills/using-git-worktrees/SKILL.md) | 採 bounded subject、report-as-claim 與適用 isolation 方法；不採 source-access／test-rerun 限制、controller authority 或 universal Git topology。Result status 與 scoped R2 patterns 依 Fable §4–§5，沿 Minimal semantics 改寫。 |
| [Reference Orchestrator Contract `orch-default`／`v2`](../orchestrator-contracts/default-v2.md)（Adopted／Frozen 2026-09-22；[`v1`](../orchestrator-contracts/default-v1.md) Adopted／Frozen 2026-09-17） | 本版採用的 reusable control-plane reference。Minimal v2.0-aligned；其 §14 保留六項 v2 母版 reconciliation。 |
| [Opus 5 Reference Orchestrator Contract Acceptance Review](<../../../Governance Reference Orchestrator Contract v1 Acceptance Review(Opus-5).md>) | `orch-default／v1` 的 durable independent acceptance record：初審 ADOPT WITH REQUIRED CHANGES、M-1～M-3 CLOSED、targeted regression PASS、final ADOPT。 |
| [10-ASPICE_auto v2 Orchestrator contract](../../../../10-ASPICE_auto/docs/governance/orchestrator_contract.md) | 歷史／來源證據與既有 v2 adopters 的 migration reference；不是新專案的有效 reusable reference；未在本次修改。 |

以上是來源與版本記錄，不是額外操作 gates。來源 frameworks 的後續更新不自動改變本 Profile；獨立使用本 Profile 時無須安裝或載入來源材料。

## Appendix A · Control-plane provenance and v2-adopter migration constraints

本附錄保存自 §2 移出的歷史／來源材料與既有 v2 adopters 的 migration constraints。A.2 的適用性與規範狀態與其原在 §2 時相同：對既有 v2 adopters 仍是 operative migration 範圍，不因移至附錄成為單純歷史敘述；不適用於新專案的正常 activation。

### A.1 Control-plane reference provenance

`orch-default` 的 `v1` 為 Adopted／Frozen 2026-09-17，依 [Opus 5 Acceptance Review](<../../../Governance Reference Orchestrator Contract v1 Acceptance Review(Opus-5).md>)；新 Minimal 專案以 `orch-default／v2` 為 Orchestrator reference，不再需要外部 v2 contract 作為 reusable control-plane reference。[10-ASPICE_auto 的 v2 `orchestrator_contract.md`](../../../../10-ASPICE_auto/docs/governance/orchestrator_contract.md) 只保留為歷史／來源證據，以及既有 v2 adopters 的 migration reference；該路徑是來源位置，不是新專案必備路徑。

### A.2 v2 Orchestrator implementation migration note（既有 v2 adopters 適用）

`orch-default／v1` 已在 reusable reference contract 層套用下列六項 reconciliation semantics（見其 §14；`orch-default／v2` 原樣保留）；它們**不是 reference contract 的未完成工作**。下表保留給仍宣告 v2 的既有專案 Orchestrator／Runtime 實作（例如 10-ASPICE_auto）在採用 Minimal 時使用。本 Profile 更新**不使任何既有 v2 專案自動 migration**；是否採用及何時採用，依 Minimal §5.3 由各專案留下版本、依據與授權。Profile 的 Adopted 狀態不證明任何專案實作已完成 Minimal migration。下列是 migration 範圍，不是新增 workflow：

| Migration 項目 | 歸屬與 Minimal 對齊方式 |
|---|---|
| **Additive amendment exception** | **Governance property**：移除新增 requirement／AC 卻免 re-approval 的例外；依 Minimal §3.4／§5.3 區分 clarification 與 semantic change。 |
| **Legacy SO-2／authority assumptions** | **Project policy／authority bindings**：只保留 acceptor 已有效宣告、涵蓋範圍明確的 standing authorizations；不複製歷史委派作為新專案授權。DA 與 Final Adjudicator 的權限仍須可區別。 |
| **ESCALATED／STOP／operator-assisted termination** | **Governance property＋Runtime HOW**：標籤或 capability declaration 本身不構成 lawful stop；依 Minimal §1.5／§3.8 判定合法替代、recovery、routing 與真正 natural terminus。 |
| **High-risk ADJ／v2 DONE predicates** | **Project policy＋Runtime HOW**：適用高風險 assurance 由 DA 決定；Git ancestry、固定 ADJ 欄位等不可冒充 universal completion。對齊 Minimal §3.8 的 coverage 與完成條件。 |
| **Deferred disposition／cycle bounds** | **Governance property**：依 Minimal §4.5 的 deferral 限制、兩個合法新 cycle 起點與同 root cause 進展條件；舊 ACCEPT／disposition 字面值不自動證明合法 closure。 |
| **v2 normative citations** | **Profile／Runtime migration**：改指有效 Minimal authority，並核對實際 gate／checker predicates；不能只換 citation，或藉舊引用帶回 universal state、schema、provenance、Git／release、rollover 義務。 |

**Preserve useful Runtime machinery; remove or re-express only semantics that conflict with Minimal.** 已有 state engine、ledger、worktree 或 recovery implementation 可繼續作專案明確選用的 HOW；不得讓衝突的舊規則判定 Minimal authority、audit closure 或 stop。實作完成 reconciliation 前，不宣稱其已全面符合 Minimal。
