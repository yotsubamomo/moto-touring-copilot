# AR-2026-10-12_minimal-governance-v2.2_A1-ALT — Alternate Independent Review（A1，cycle 1）

本 record 由 `alternate_reviewer` assignment 自行寫入（Minimal v2.1 §2.3 第 4 項）。Executor、Primary Reviewer 或派工者的結論都只當作待驗證主張。

## Metadata

| 欄位 | 內容 |
|---|---|
| audit | A1：Minimal Operational Governance v2.2 Candidate 的 independent review（Acceptor 指示第 2 項） |
| round／cycle | Alternate Independent Review（Minimal v2.1 §4.4 的 exactly one Alternate Review）／cycle 1 |
| contract | [WC-2026-10-12_minimal-governance-v2.2-adoption](../outcome-contracts/WC-2026-10-12_minimal-governance-v2.2-adoption.md)（Acceptor 指示原文；A1 必查項見第 2 項，第 36–46 行） |
| 前序 records | R1：[AR-2026-10-12_minimal-governance-v2.2_A1-R1](AR-2026-10-12_minimal-governance-v2.2_A1-R1.md)；R2：[AR-2026-10-12_minimal-governance-v2.2_A1-R2](AR-2026-10-12_minimal-governance-v2.2_A1-R2.md)。兩份 record 的 Codex 原文與 `governance/records/evidence/` 中 companion job JSON 的 `rendered` 欄位逐字相同；JSON 的 sha256 與 record header 所記相符（R1 `e4ade673…`，R2 `19147bb2…`） |
| subject commit | `1c5c50e82d0b87dd2e4e3c3a0399683a2a68565f`（branch `adopt/minimal-governance-v2.2-2026-10-12` 的 head，開始審查時工作目錄乾淨；檔案與該 commit 的 blob 相同） |
| subject 檔案 | `master_governance/Minimal_Operational_Governance_v2.2_Candidate.md`：sha256 `01a9542a6d254b3a3469429144503d8167385e650c0d799dd03c858ae84078b9`（blob `392c4673`）；`master_governance/references/orchestrator-contracts/default-v2.2.md`：sha256 `91f509179a2004a09eee9a8fd9f8630cbc98d77782abb081088757b1571d8c4d`（blob `88cb59a2`）。兩個值與 adoption worklog §9 所記相同 |
| 比較基線 | `governance/upstream/master_governance/references/orchestrator-contracts/default-v2.1.md`；Minimal v2.1（`governance/upstream/master_governance/Minimal_Operational_Governance_v2.1_Candidate.md`） |
| 有效治理（審查期間） | Minimal v2.1、`bindings-v0.3`、Profile `default` v2.7 |
| reviewer | `alternate_reviewer`（definition `.claude/agents/alternate-reviewer.md`） |
| escalation／substitution | 無。Profile E-AR (D1) 的條件不成立：剩餘 finding 可以由現有證據判定，沒有能力缺口 |
| 日期 | 2026-10-12 |

## 1. 範圍與方法

範圍依 Minimal v2.1 §2.1（Alternate 列）與 §4.4：判定 R2 後仍未解的 blocking finding A1R2-F1 是有效、已解決、分類錯誤，還是 design issue；A1R1-F2、F3 只在發現問題時改判；檢查 R2 之後的定點修正直接產生或暴露的 blocking defect。不作新的無限制全面 audit。

我自行取得並核對了以下材料（不限於派工包）：

- WC、R1、R2 records 與兩份 companion job JSON（hash 與 `rendered` 欄位比對）。
- Subject 兩檔全文；`default-v2.2` 與 `default-v2.1` 的逐行比對（13 處差異：header、v2.2 說明、§1 兩行、§3 第 58 行、§4 第 66 行、§8 第 154 行、§11 第 197 行、§15 一列、狀態句與 source 表一行，與 v2.2 說明及 §15 所列範圍一致，無範圍外的修改）；`ec7ed76..1c5c50e` 對 subject 的 diff（`default-v2.2` 第 12、58、197、256 行；Candidate 只在 D.8 加兩列，第 1–5 節條文不變）。
- Candidate §2.2–§2.7、§4.4–§4.6、§5.1、Appendix D；impl-default v2 §11–§12；Profile `default` v2.5 §3、§6 與 v2.7 §2、§5；`bindings-v0.3` §3。
- Adoption worklog §0–§9 與 candidate worklog §2、§10、§12；Executor session（`514c5b0c-595d-4711-b987-863a804d8a4d`）transcript 的 `message.model`／`effort`；Codex `~/.codex/logs_2.sqlite` 的唯讀副本（複製到本 session 的 scratchpad 查詢後刪除，原檔未動）。

## 2. A1R2-F1 的判定：RESOLVED

**R2 的主張**（R2 record 第 33–35 行）：`orch-default` v2.2 把全程核對寫成 SHOULD；checkpoint 本身是 SHOULD；§11 只 SHOULD 要求 Bindings 宣告逐筆證據來源；root session 可能在 activation 後切換 model，然後在沒有必經核對的情況下作 routing 或 gate；「偵測到改變點」的 MUST NOT 抓不到未偵測到的切換。R2 的建議：採用 return 前、以及 root session 自上次核對以來的工作被用作 routing、gate、persist 或 completion 依據前，MUST 核對全部執行證據；adopting Bindings MUST 宣告可觀察的證據來源；無法確立涵蓋時 fail closed。

**修正後的 subject 逐項對照**（`default-v2.2.md`）：

| R2 指出的缺口 | 修正後條文 | 判定 |
|---|---|---|
| 採用 dispatched assignment 的 return 前只 SHOULD 核對 | 第 58 行：「被派工的 assignment 的 return 被採用前，MUST 核對該 assignment 的全部執行證據，不只第一筆」；第 66 行（§4 步驟 3）引用之 | 已解決 |
| Root session 的核對掛在可省略的 checkpoint 上 | 第 58 行：觸發點改為「本 session 自上次核對以來的工作被用作 routing、gate、persist（checkpoint、commit）、rollover 交接或 completion 的依據前」，MUST 核對該段期間的全部執行證據。觸發點是工作被使用的時點，不依賴 checkpoint 是否執行（第 150 行的 checkpoint 仍是 SHOULD，已不影響本義務） | 已解決 |
| 未偵測到的切換 | 上一列使每個 routing、gate、persist、交接與 completion 之前都必須掃過自上次核對以來的全部證據，未偵測的切換會在第一個使用點前被發現；之後適用第 58 行的改變點規則（自改變點起不是合格產出，修復或替代，由符合 mapping 的 assignment 重新核對或重作，記入 run record），這也回應了 R1 對「post-switch work 的隔離與重驗」的要求 | 已解決 |
| 無法確立涵蓋時的處理 | 第 58 行：無法取得涵蓋該段工作的證據時「不是合格產出（fail closed）：MUST NOT 以之作上述依據，依 Minimal §2.2 修復或替代」；修復不成時進入 Minimal §1.5 recovery | 已解決 |
| §11 證據來源只是 SHOULD | 第 197 行：「Bindings MUST 宣告可逐筆觀察實際 model 與 effort／mode 的證據來源，供 §3 的全程核對使用」 | 已解決 |

**這些 MUST 有 Minimal 依據，不是 contract 自創的義務**（`default-v2.2.md` 第 22 行要求本 contract 的 MUST 都是 Minimal 條款的表達）：Candidate 第 184 行（V22-10：核對 MUST 涵蓋 assignment 產生的全部工作）、第 182 行（可觀察執行證據 MUST 足以核對實際 assignment）、第 186 行（不符 MUST 修復或替代，不得冒充合格 orchestration）、第 174 行（Orchestrator 核對成立前不得派工）、第 668 行（V22-18：Bindings 宣告 root role session 的核對方式與證據位置）。第 58 行的 MUST 不以「平台可能自動切換」為條件，比第 184 行第三句寬；但第 184 行第一句本身就是無條件的（核對對象是執行期間的實際 model／effort），平台不會切換時兩者結果相同，所以不構成新增義務或矛盾。

**我另外尋找的殘留缺口，結論都是不構成 blocking：**

1. **Dispatch 本身不在第 58 行的清單中。** 切換後的 root session 仍可能派工。但派出的 assignment 的 return 被採用前、以及 Orchestrator 自己據以作 gate（§4 步驟 6）、route（步驟 8）、persist（步驟 10）或 completion 前，都要核對自上次核對以來的全部證據；切換會在派工結果產生任何效力之前被發現，改變點之後的工作（含該次派工）依改變點規則重新核對或重作。派工的第一次核對另有第 58 行與 Candidate 第 174 行的「先於第一次 dispatch」。
2. **改變點規則只列 routing、gate、completion，fail-closed 規則另列 persist 與 rollover 交接。** 兩者不矛盾：改變點之後的工作已被定為「不是合格產出」並須修復或重作；改變點本身必須能被記入 run record（第 58 行），所以不禁止 persist 該紀錄是合理的。
3. **Lightweight 與 impl-default v2。** `orch-default` 只管 Formal 的控制面。impl-default v2 第 177 行（§11）「Observed assignment MUST 符合 effective adopted mapping」與第 185 行（§12-A）都沒有限定核對時點，不像 `orch-default` v2.1 那樣把核對收窄成「第一次 dispatch 前」；依 Candidate 第 184 行對「實際 model」的定義讀，與 V22-10 相容。Profile `default` v2.5 第 156 行（§6）的證據也已是「每則 assistant message 的 `model` 與 `effort`」。Executor 在 adoption worklog §7 第 97 行的同一判斷成立。
4. **R1 原 finding 的範圍。** R1 的 F1 指向 companion procedures 與 Project Bindings。Companion 部分（`orch-default`）已由本修正處理；impl-default 依上一項不需修改；Project Bindings 部分見下一段與 A1ALT-F1。

**不是分類錯誤，也不是 design issue。** F1 在 R2 時是有效的 high finding：reference procedure 沒有必經的核對 gate，會讓 V22-10 在採用 package 的專案中失去執行程序。修正只在 HOW 層（companion contract）補上 gate，Candidate 第 1–5 節條文不變，不需要 Design Authority 決定新的語義；Acceptor 指示第 1 項（WC 第 29 行）已授權對 impl／orch 作「最小必要修正」。

**Project Bindings 部分。** `bindings-v0.3` 第 102–103 行只規定 root role session 在第一次派工前／開始受治理的工作前核對；第 125 行宣告的 Codex 證據是 rollout 檔，而 companion 路徑實際上沒有產生（R1 record 第 16 行；adoption worklog 第 89 行）。這部分的缺口仍然存在，但它不是 A1 的 subject：WC 第 2 項把 A1 定為 v2.2 Candidate 與 impl／orch 相容性的審查，Project Bindings 的 pin 與 runtime 屬第 3 項的 migration；本工作區在依 Minimal §5.3 改採 v2.2 之前，V22-10 尚未生效。我同意 R2 的看法：交由 A2（adoption worklog 第 69 行已把 `bindings-v0.4` 列入 A2 的 subject）審查是合法的，且 `orch-default` v2.2 第 197 行與 Candidate 第 668 行現在給了 A2 可以直接核對的 MUST 依據。記為 A1ALT-F1（non-blocking for A1，見 §5）。

## 3. A1R1-F2、A1R1-F3

R2 判定兩者 RESOLVED。我的檢查沒有發現問題，不改判。核對摘要：

- **F3。** Candidate 第 263 行（§2.5 規則 3）已寫明：作出 verdict／ruling 前提出 trigger 而不作 verdict 的派工記為 escalation 紀錄，不計為第 4.4 節的 Alternate Review；escalated 的 fresh assignment 所作的才是該輪唯一的結論；已作 verdict 後不再重派。Profile `default` v2.5 第 69 行與 v2.7 的 E-AR 列寫法一致。
- **F2。** Candidate worklog 第 5 行與 §12（第 137–144 行）記錄承接，第 15–17 行的原始不符照實保留。Executor session transcript：進入點後的 120 筆 assistant entries（`2026-10-12T02:44:09.219Z`–`03:05:44.963Z`）全為 `claude-opus-5-5`／`high`；之前的 988 筆為 `xhigh`，屬進入角色前的無角色 session（adoption worklog §0、§2）。`ec7ed76`（02:51:08Z）與 `1c5c50e`（02:59:33Z）兩個 commit 都在 `high` 區間內。E-EX/M2 的 escalation record（adoption worklog 第 13–24 行）以 H-1 為 trigger，可由紀錄機械判定。

## 4. R2 之後的定點修正：回歸與直接產生或暴露的缺陷

- **修正範圍。** `ec7ed76..1c5c50e` 對 subject 的變更只在 `default-v2.2` 第 12、58、197、256 行與 Candidate D.8 兩列（第 1048–1049 行），都對準 A1R2-F1；沒有夾帶其他修改。`grep "SHOULD 核對"` 在 `default-v2.2` 中為 0，與 worklog 所記相符。
- **程序。** Executor 在 R2 之後、Alternate Review 之前作了修正。Minimal v2.1 §4.4 限制的是審查輪次與派工次數（不得有 R3／R4），沒有禁止 Executor 在 Alternate Review 前修正；本次沒有多派任何審查，Alternate Review 仍是 exactly one。Alternate 的判定項包括「已解決」（Candidate 第 578 行，與 v2.1 同文），而 Minimal §3.8 要求審查與結案版本可對應，所以本 Alternate Review 以修正後的 `1c5c50e` 為 subject。
- **沒有發現修正產生或暴露的 blocking defect。** 兩項 non-blocking 觀察記為 A1ALT-F2、A1ALT-F3。

## 5. Findings

| ID | Severity | Blocking | 證據 | 內容 | Disposition／owner |
|---|---|---|---|---|---|
| **A1ALT-F1** | medium | **non-blocking**（理由：不屬 A1 subject；V22-10 在本工作區改採 v2.2 前不生效；改採由 A2 審查，且判準現已是 MUST） | `governance/Project_Bindings.md` 第 102–103 行、第 125 行；R1 record 第 16 行；adoption worklog 第 69、89、97 行 | A1R1-F1 的 Project Bindings 部分仍未處理：root role session 只在開始時核對；宣告的 Codex 證據來源（rollout 檔）不是實際可得的來源 | 依同一 accepted contract 的 migration（WC 第 3 項）處理，不是新工作。Owner：`WL-2026-10-12_minimal-governance-v2.2-adoption` 的 Executor。`bindings-v0.4` 須符合 `default-v2.2.md` 第 58、197 行與 Candidate 第 184、668 行（全程核對與逐筆可觀察的證據來源，含 Codex 的實際證據位置），由 A2 Reviewer 核對。A1 closure 不證明 Project Bindings 符合 |
| **A1ALT-F2** | low | non-blocking | Candidate 第 14 行（package references 仍列 `orch-default` v2.1）、第 1038 行（D.7 待決 4：本 Candidate 不修改 companion）、第 1047、1049 行（D.8：F1 由 `orch-default` v2.2 處理）；`default-v2.2.md` 第 5 行（Status：Candidate，「隨 v2.2 採用」）；`master_governance/` 目前只有 Candidate、README 與 `default-v2.2`，`default-v2.2` 的相對連結（例如 `default-v2.1.md`、Minimal v2.1、impl-default、model profiles）在該目錄下尚無對象 | F1 的修正放在 `orch-default` v2.2，不在 Candidate 本文。採用時若 package references 或 package 仍指向 `orch-default` v2.1，已採用的 package 就沒有全程核對 gate，F1 會重新出現 | 已在 adoption worklog §6 第 3 步（第 77 行）規劃，屬採用與 package 組裝，由 A2 審查（A2 subject 含 package，第 69 行）。Owner：同上 Executor。採用時 header 的 package references（metadata，D.7 待決 2）與 package 須指向 `orch-default` v2.2，並與 Minimal v2.2 一起採用 |
| **A1ALT-F3** | low | non-blocking | `default-v2.2.md` 第 197 行的括號「activation、checkpoint、rollover、completion report 前，以及採用被派工 assignment 的 return 前」與第 58 行修正後的觸發點清單（另含 routing、gate、commit） | §11 的時點摘要沒有跟著 §3 更新。該句明寫「核對時點依 §3」，MUST 在 §3，所以不會弱化義務 | 不需處理即可 closure；Executor 可在採用時以編輯方式對齊或保留，不構成新工作 |

## 6. Verdict：CLOSED

A1（cycle 1）沒有未解的 blocking finding：A1R2-F1 RESOLVED；A1R1-F2、A1R1-F3 依 R2 為 RESOLVED；本次沒有新的 blocking finding。A1 達成 audit closure，不需要 Final Adjudication。

Closure 的範圍與限制：

- 涵蓋 commit `1c5c50e` 的兩個 subject 檔案（sha256 見 Metadata）。之後若修改這兩檔，依 Minimal §3.8 須識別 delta 並作相應驗證；採用時 metadata-only 的修改（D.7 待決 2）也須能對應到本 subject。
- 不涵蓋本工作區的 Project Bindings 改採、package 組裝與採用紀錄（A1ALT-F1、F2；屬 A2）。
- 依 Minimal §4.4 末段，audit closure 不豁免第 3.8 節的其他完成條件。

## 7. Assurance（a）：context independence（Minimal v2.1 §2.3 四項）

**實際的派工方式（依 transcript 觀察，與派工包的描述不同）。** 派工包說本 assignment 由 operator 以新的 `claude -p --agent alternate-reviewer --effort xhigh` process 啟動。Transcript 顯示的實際情形是：operator 於 `2026-10-12T03:08:04Z` 在新的 Claude desktop session `ec7cd0a6-157f-497d-bad5-d21a9e16b7eb`（entrypoint `claude-desktop`；該 session 的 transcript 為 `claude-opus-5-5`／`high`）指示該 session 作為無角色派工介面，以 Agent tool 派工：`subagent_type: alternate-reviewer`、`model: opus`、`effort: xhigh`，prompt 為 [DISPATCH-2026-10-12_minimal-governance-v2.2_A1-ALT](DISPATCH-2026-10-12_minimal-governance-v2.2_A1-ALT.md) 的全文，不加其他內容。本 assignment 是該 session 的 subagent `agent-a4676f18cf193cc10`（meta：`agentType alternate-reviewer`、`model opus`、`effort xhigh`）。這是 `bindings-v0.3` §3.4 宣告的 Claude path 機制（第 84、94 行：以 definition 名稱派工並帶 `model`／`effort`，以 subagent transcript 核對），由 operator 經無角色 session 發起（第 107 行起的無角色 session 規定允許其作派工介面）。派工來源與機制都符合 Minimal v2.1 §2.3。adoption worklog 第 141 行所述的 CLI 機制沒有被使用；後續紀錄引用本次 Alternate Review 時，宜以實際機制為準。

1. **Independent context。** 本 assignment 的 transcript 第一筆是派工 prompt（`parentUuid` 為 null），與 DISPATCH 檔逐字相同（3,820 字元）；沒有 fork／prefix context。派工的 session 是新開的，只有 operator 的一則指示與一次讀取 DISPATCH 檔。本 assignment 不繼承 Executor session `514c5b0c…` 或任何 Codex thread 的對話、推理或結論；派工包只含 record 引用。Harness 自動載入的 CLAUDE.md 與 git status（含近期 commit 標題）屬 repository 內容，與其他紀錄一樣當作待驗證主張。
2. **Verifiable binding。** Definition `.claude/agents/alternate-reviewer.md` 的 frontmatter 為 `claude-opus-5-5`／`xhigh`；有效 mapping 為 Profile `default` v2.7 第 27 行的 Opus 5.5／`xhigh`（無 override、無 escalation、無 substitution）。證據：`~/.claude/projects/P--AI-WorkFlows-SpeCoda-Local-DEV-v2/ec7cd0a6-157f-497d-bad5-d21a9e16b7eb/subagents/agent-a4676f18cf193cc10.jsonl`。寫入本 record 前的最後一次核對：自 `2026-10-12T03:08:25.236Z` 起的全部 assistant entries 都是 `claude-opus-5-5`／`xhigh`，沒有其他值（筆數與結束時間見本節末）。
3. **Autonomous access。** 我自行以 git 與檔案工具讀取 repository、subject、基線、companions、Bindings、worklogs、Executor 與派工 session 的 transcript，以及 Codex log 資料庫的唯讀副本；範圍超出派工包所列。
4. **Self-written record。** 本檔由本 assignment 寫入。我在 repository 內只寫了本檔；暫存的資料庫副本與比對輸出放在本 session 的 scratchpad（repository 之外），資料庫副本用後已刪除。

Binding 證據的筆數：寫入本 record 前為 80 筆 assistant entries（`03:08:25.236Z`–`03:17:11.184Z`），全部 `claude-opus-5-5`／`xhigh`；寫入後的核對見文末。

## 8. Assurance（b）：model diversity

| Assignment | 實際 model／effort | 證據 |
|---|---|---|
| Executor（產生 subject） | 起草：`claude-opus-5-5`／`xhigh`（session `514c5b0c…` 至 `02:18:13Z`；不合格的 assignment，由合格 Executor 承接，見 F2）。修正：`claude-opus-5-5`／`high`（同一 session 進入 Executor 角色後，120 筆，`02:44:09.219Z`–`03:05:44.963Z`）。兩段的 model 都是 `claude-opus-5-5` | Executor session transcript `message.model`／`effort` |
| Primary Reviewer | Codex `gpt-6-sol`／`xhigh`（R1：三個 thread `01a12ddd-3094…`、`01a12ddd-ded0…`、`01a12ddd-ef95…`；R2：`01a12e05-aa16…`） | `~/.codex/logs_2.sqlite` 唯讀副本：上述 thread 的 model 欄位只有 `gpt-6-sol`，effort 只有 `xhigh`／`Some(XHigh)`；唯一的 `model: None` 是 turn override 欄位為空，不是其他 model |
| Alternate Reviewer（本 assignment） | `claude-opus-5-5`／`xhigh` | §7 第 2 項 |

依 Profile `default` v2.7 §5（第 125–128 行）：

| 關係 | 宣告 | 結果 |
|---|---|---|
| D1：Alternate ≠ Executor | 未宣告（v2.6 起不預設宣告） | 無：Alternate 與 Executor 同為 `claude-opus-5-5`，**沒有 model diversity** |
| D2：Alternate ≠ Primary | 宣告（Codex 為有效 Primary，O-2） | 成立：`claude-opus-5-5` 對 `gpt-6-sol` |
| D3：Primary ≠ Executor | 宣告（Codex 為有效 Primary） | 成立：`gpt-6-sol` 對 `claude-opus-5-5` |
| D4：Primary 與 Executor 跨 vendor | 宣告（Codex 為有效 Primary） | 成立：OpenAI 對 Anthropic |

`diversity_lost`：無（本次沒有 substitution 或 escalation）。以上結果不改變（a）欄的 independence 判定。

## 最終 binding 核對

寫入本檔之後以同一 transcript 再次核對：88 筆 assistant entries（`2026-10-12T03:08:25.236Z`–`03:19:43.332Z`），全部 `claude-opus-5-5`／`xhigh`，沒有其他 model 或 effort 值。此後只有本行的補記與回報訊息。Repository 在本 assignment 期間只新增本檔（`git status`：唯一的變更是本檔，untracked）；HEAD 仍為 `1c5c50e`。
