# Final Adjudication ruling — Issue #16（SPEC-R1 R1-4 `routing`）cycle 1

| 欄位 | 內容 |
| --- | --- |
| Ruling ID | `ruling-20261118-issue16-c1` |
| 日期 | 2026-11-18（Asia/Taipei） |
| 角色 | `final_adjudicator`（`gov-final-adjudicator`），治理 §4.5 |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record §6 事件 95：「#16 R2 仍 blocking（R2-F1）」→ Alternate `VERDICT: UNRESOLVED (R2-F1)`） |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-R1 v1（`derivation-spec-r1.md` 第 4 節 DD-R1-2、CL-R1-5～CL-R1-9〔特別是 CL-R1-8〕，第 5 節 R1-4 列與 E-1～E-6）＋ `decision-20261118-issue13-c131.md`、`decision-20261118-issue14-c141.md`、`decision-20261118-issue14-qalt1.md`、`decision-20261118-issue15-c151.md`、`decision-20261118-issue16-c161.md` → GitHub Issue #16。Issue 原文：派工所附 scratchpad 檔，本 FA 實測 SHA-256 `105fdc981b1087b60b419690168d205064853a1a41ccde4a6cb092b6ffa8ede1`，與派工、run record 第 4 節相同 |
| 高風險類別 | R1-4 標示 **H-1、H-2、H-4**（`derivation-spec-r1.md` 第 5 節 R1-4 列；`decision-20261117-high-risk-categories.md` 第 3、5 節）。R2-F1 所在路徑是 H-4 判定第 4 項（路線採用的檢查） |
| 受審 subject（cycle 1） | `07996828afaa0db3a7d477a05528fe993dc46d49`（branch `oc1-run2-b1-ui0-r1-routing`；BASE `bc7024b24b968e2dfb04dc38e822781dd5fb5425`）。實作 commits `7cb4b0c`、`f6810d2`，correction `65aa00c`。主 checkout HEAD `e1e7d32` 相對 `0799682` 只多 `docs/governance/records/**`（本 FA 以 `git diff --name-only 0799682..e1e7d32` 核對：R2 record、Alternate record、run record） |
| 讀過的 records | R1 `docs/governance/records/audit/issue-16-c1-r1.md`（SHA-256 `32d43f3a…430c2472`）、R2 `issue-16-c1-r2.md`（`a88e9ebe…4d4ad58f`）、Alternate `issue-16-c1-alt.md`（`315457c7…bae18af5`）；三者的 hash 由本 FA 重算，與 run record 事件 92、94、95 相同。Worklog `docs/governance/records/worklog/issue-16.md`（第 10、11 節及相關前節）；run record §6 事件 89～95；前例 `ruling-20261117-issue9-c1.md`（格式參考）。三份 audit record 與 worklog 的結論都當成待驗證主張；本 ruling 採用的事實都另行重讀原始檔或重現 |
| 依據的條文 | 治理 §1.2（boundary 段）、§2.4、§2.5、§4.3、§4.4、§4.5、§4.6；orch-default v2.2 §6（新 cycle）、§7（P3–P6）；Bindings m3 §2.6 RB-7、§3.2 E-FA／E-EX、§3.6、§3.7、§5、§7；高風險 decision 第 3.4、5 節 |

## Assurance

### (a) Context independence（治理 §2.3）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Fresh 的 `gov-final-adjudicator` subagent，沒有繼承 Executor、Primary Reviewer、Alternate Reviewer 或 Orchestrator 的對話；派工內容只有路徑與識別 |
| Verifiable binding | 有效 mapping 為 Opus 5.5／`xhigh`（F-FA；Bindings §3.1）。本 FA 無法自證全部 assistant 訊息的實際 (model, effort)；依 Bindings §3.6 由派工者在採用本 ruling 前核對 transcript，記入 run record §6 本次 FA 派工事件 |
| Autonomous access | 自行讀取契約、`git show 0799682:<path>` 的原始碼、三個版本的 `_real`、git 歷史；在 worktree `C:/Users/yotsu/AppData/Local/Temp/cx16r2`（`git rev-parse HEAD` = `0799682…`，detached）以該 worktree 的 `.venv` 執行 pytest 與探測程式（程式檔放在 session scratchpad，只用合成值、記憶體內執行）。沒有讀取、列出或搜尋 `data/`，沒有讀取或執行 `experiments/`，沒有讀 `.env`，沒有網路請求（探測在匯入後把 `socket.socket`、`create_connection`、`getaddrinfo` 換成拒絕函式；pytest 沿用測試檔的 autouse socket 封鎖），沒有從 repo root 搜尋 |
| Self-written record | 本 ruling 由本 FA 以 Write 工具寫入，是本 FA 在 repo 內唯一新建的檔案。沒有修改實作、測試、契約、gates 或其他紀錄，沒有 stage／commit。Worktree 的 `git status --porcelain` 在本 FA 執行前後相同（只有 `?? docs/governance/records/audit/issue-16-c1-r2.md`）；探測的暫存目錄建在 git-ignored 的 `.venv/tmp` 下，結束時已移除 |

### (b) 實際 model

| 角色 | Model（證據） |
| --- | --- |
| Executor | `claude-opus-5-5`／`high`（run record 事件 89、91、93，agentId `a1e2cfa52290d496f`；派工者核對） |
| Primary Reviewer（R1、R2） | Codex `gpt-6.1-sol`／`high`（事件 92、94 的 rollout `turn_context` 核對） |
| Alternate Reviewer | `claude-fable-5-2`／`high`（事件 95，agentId `aa0cbc2d140007ba4`） |
| Final Adjudicator | 有效 mapping `claude-opus-5-5`／`xhigh`；實際觀測由派工者記入 run record |

Bindings §5 沒有宣告 diversity 關係；本 ruling 不主張 model diversity。FA 與 Executor 的有效 mapping 是同一個 model。

### Capability escalation

E-FA：Bindings §3.2 採用 (M2)、(D1)。(M2)「同一 root cause 在新 cycle 再次進入 FA」不成立：本次是 cycle 1，也沒有先前的 FA record。(D1)：本 FA 沒有需要升級的具體爭議面向——缺陷可以用合成值直接重現，契約條款明確，R2 與 Alternate 對有效性、severity 與 blocking 判定一致，爭議只在處置的種類與 rework 的範圍。不提出 trigger，作出 ruling。

---

## 1. 爭議

Alternate Review 之後仍未解的是 **R2-F1**（Alternate record 最後一行：`VERDICT: UNRESOLVED (R2-F1)`）。各 record 的立場：

| 項目 | R1 | R2 | Alternate |
| --- | --- | --- | --- |
| R1-F1（非 200 回應在讀取國道訊號前就離開，違反 CL-R1-8） | Medium／blocking | NOT RESOLVED；原三個重現已通過，殘餘「集中記為 R2-F1，不重複計算」 | 已解決；root cause（提早離開）已由 `65aa00c` 修正，殘餘全部歸 R2-F1 |
| R2-F1（`_route_facts`／`_trace_facts` 解析長度時，`_real` 的 `math.isfinite` 對超出浮點範圍的 `int` 拋 `OverflowError`，中斷非 200 的訊號收集） | — | Medium／blocking；correction 直接產生的 regression；只依非 200 行為判定，200 的同類問題「不是本次另外展開的 finding」 | 有效、未解、Medium／blocking 成立、不是 design issue；root cause `_real` 自 `7cb4b0c` 未變，200 路徑也有同一個未捕捉例外，`summary.time` 亦同；「correction 直接產生」只描述了一半；只修兩個新增呼叫處會讓 200 路徑照樣拋例外 |

要裁決的是：R2-F1 的處置（dismiss、defer、交 DA，或 rework 並授權新 cycle）；若是 rework，範圍是否以 root cause 為準（含 200 路徑與 `summary.time`）；新 cycle 的實質改變、條件與限制。

## 2. 依據的證據（本 FA 自行取得）

### 2.1 契約條款

- **R1-4 範圍 (f)**（`derivation-spec-r1.md` 第 5 節 R1-4 列）：共用的路線介面「由同一個函式回傳『採用的路線（…）』或『路線錯誤代碼』」。契約明定可以向上傳出例外的情形是嚴格模式的停止（CL-R1-4）、快照選取的 `SnapshotIntegrityError` 與存放錯誤（CL-R1-17；`decision-20261118-issue14-c141.md` 第 5 節；CL-R1-21）、目標 GPX 與呼叫端輸入的錯誤（CL-R1-24）、凍結清單未搭配 Snapshot Mode 的 `ValueError`（`decision-20261118-issue16-c161.md` 第 4.4 節）。引擎回應的內容不在其中。
- **CL-R1-8**（`derivation-spec-r1.md` 第 73 行）：「引擎有回應時，先檢查所有可取得的國道訊號，再決定代碼。來回行程兩個方向都送出並檢查（引擎完全無法連線時除外）」；任一方向有國道訊號 → `highway_in_route`；否則任何不採用的原因（含引擎錯誤、道路屬性查詢失敗或長度不符）→ `routing_unavailable`。
- **SPEC-001 4.13**：`routing_unavailable` 包含引擎「回傳錯誤」與「國道檢查無法驗證」；`highway_in_route`「優先於 `routing_unavailable` 的各種原因」。**SPEC-001 7.11 第 5 項**：有任何國道訊號就是 `fail`，「優先於其他原因（警告、偏移、無法驗證）」；沒有訊號但無法驗證時不採用、不產生 `freeway_check` 的值、不存快照。**第 6 項**：採用條件「沒有例外」。
- **R1-4 的「另加」AC**：「國道訊號與其他不採用的原因同時出現時是 `highway_in_route`」。
- **H-4 最低核對範圍**（高風險 decision 第 5 節）：「缺漏、失敗……的每條路徑都有測試顯示結果是 UNKNOWN 或明確錯誤」；「路線採用的檢查在訊號矛盾或無法驗證時不採用」。
- **既有已接受的方向**：非布林的真值旗標仍記為訊號（c161 第 4.3 節）；道路屬性回應有警告時其國道訊號照樣計入（CL-R1-27 第 2 項）。

### 2.2 程式（subject `0799682`）

- `src/moto_copilot/routing/adoption.py:117–118`：`_real(value)` = `isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)`。`math.isfinite` 對 Python `int` 先轉 `float`，絕對值超過浮點範圍時拋 `OverflowError`。
- 呼叫處：`:187`（`trip.summary.length`）、`:191`（`trip.summary.time`）、`:276`（道路屬性 `edges[n].length`）。這三處都在 `_route_facts`／`_trace_facts` 內，200 與非 200 兩條路徑都經過（`:372`、`:375`、`:392`、`:394`）。
- 三個版本的 `_real` 逐字相同：`7cb4b0c`（第 111–112 行）、`e1ef580`（第 116–117 行）、`0799682`（第 117–118 行）；三個版本的呼叫處都是 summary `length`、`time` 與 edge `length`（本 FA 以 `git show <rev>:src/moto_copilot/routing/adoption.py` 核對）。
- `source.py` 的 `_ask_engine`（第 219–227 行）直接呼叫 `evaluate_direction`，`get_route` 沒有在外層捕捉這個例外。
- 對其他無效值（字串、負數、`null`、JSON 字面值 `1e400`〔`json.loads` 讀成 `inf`〕、清單、物件），`_real` 回傳 `False`，結果是 `response_malformed`，國道訊號照樣保留（第 2.3 節 D 列）。只有超出浮點範圍的 `int` 走不同路徑，原因是 `math.isfinite` 的型別轉換，不是任何設計選擇。

### 2.3 本 FA 的獨立重現（合成值，記憶體內）

探測程式 `<session scratchpad>/fa16/probe_fa16.py`（SHA-256 `1ad6a2c1d5e1c487ae47b46d3062302e371c9a3f2084f7e06bedff321c1aeee2`）在 worktree 根目錄以 `PYTHONPATH=src;tests`、`.venv/Scripts/python.exe -B -X utf8` 執行；斷言匯入的 `adoption` 模組位於 worktree 內，`git rev-parse HEAD` 為 `0799682…`。使用 `tests/test_routing_engine.py` 的合成產生器（`route_body`、`trace_body`、`FakeEngine`、`plan`，位置由 `at(x, y)` 在 0°N、0°E 附近換算），經真正的 `get_route`（來回行程、一般模式、`SnapshotStore` 在 `.venv/tmp` 下的暫存目錄）。`10**400` 經 `json.dumps` 成為 401 位數的 JSON 整數，再由產品的 `_parse_json` 解析成 `int`。只改去程的一個回應，其餘回應正常。

| 列 | 去程的回應 | 結果 | 請求序列 | 快照 |
| --- | --- | --- | --- | --- |
| A1 | route 503，`has_highway: true` | `highway_in_route`，reasons `outbound:has_highway`、`outbound:engine_error` | route, route, trace_attributes | 無 |
| A2 | trace 503，`motorway` | `highway_in_route`，`outbound:motorway_edge`、`outbound:trace_failed` | route, trace, route, trace | 無 |
| A3 | trace 503，名稱 `Freeway` | `highway_in_route`，`outbound:freeway_name`、`outbound:trace_failed` | route, trace, route, trace | 無 |
| B（6 例） | **503**；`summary.length`、`summary.time` 或 edge `length` = `10**400`；有、無訊號 | 全部是未捕捉的 `OverflowError: int too large to convert to float` | route 的 4 例只有 `route`；trace 的 2 例只有 `route, trace_attributes`（回程沒有送出） | 無 |
| C（6 例） | **200**；同上三個欄位 = `10**400`；有、無訊號 | 全部是未捕捉的 `OverflowError` | 同 B | 無 |
| D（6 例） | 200，`has_highway: true`，`summary.length` 為 `"abc"`、`-1`、`null`、`1e400` 字面值、`[]`、`{}` | 全部 `highway_in_route`，reasons 含 `has_highway`、`response_malformed`、`trace_length_mismatch`；沒有例外 | route, trace, route, trace | 無 |
| E | `_real` 的界線 | `2**1023` → `True`；`2**1024 - 1`、`2**1024`、`-(10**400)` → `OverflowError` | — | — |

結論：
1. R1 record 的三類反例在 `0799682` 都是 `highway_in_route`（A 列），與 R2、Alternate 的觀測相同。
2. R2-F1 的非 200 重現成立（B 列）；Alternate 所說的 200 路徑與 `summary.time` 也成立（B、C 列）。去程有回應而回程沒有送出、也沒有決定代碼，直接抵觸 CL-R1-8「兩個方向都送出並檢查」與 R1-4 範圍 (f)。
3. 所有例子都沒有採用路線、沒有存快照：沒有 fail-open 的證據，與 Alternate 一致。
4. D 列顯示同一個函式對其他無效長度已經是「無法驗證、訊號照樣優先」；超出浮點範圍的整數是唯一的例外情形，與 Alternate 第 2.2 節 (3)、(6) 的觀測一致。

非產品的失敗，如實記錄：第一次執行在 D 列第四例中止，原因是本 FA 把含 `:` 的列標籤當成 Windows 目錄名稱（`NotADirectoryError`，harness 錯誤）；改用編號目錄、刪除殘留的暫存目錄後重跑，上表取自重跑的同一次完整輸出（exit 0，結束時暫存目錄已移除）。

### 2.4 Regression 基準（觀測，不是 gate 判定）

在 worktree（`0799682`）執行 `PYTEST_DEBUG_TEMPROOT=<worktree>/.venv/tmp .venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider -rxXs`：`2015 passed in 41.28s`，exit 0，沒有 skipped／xfailed／xpassed 摘要；與 R2、Alternate 的觀測相同。既有測試全數通過不涵蓋超出浮點範圍的整數。E-1 是否成立由 Reviewer 判定，本 ruling 不作判定。

## 3. 裁決

### 3.1 R2-F1：不 dismiss、不 defer、不是 design／requirement issue；要求 targeted rework，並以它授權新的 bounded cycle（cycle 2）

**不 dismiss。** Dismiss 需要推翻 finding 主張的證據。本 FA 以合成值獨立重現：引擎有回應時，`get_route` 以未捕捉例外中止，既沒有回傳採用的路線，也沒有回傳路線錯誤代碼；已有可讀國道訊號時也拿不到 `highway_in_route`；去程有回應時回程沒有送出。這直接抵觸第 2.1 節的 R1-4 範圍 (f)、CL-R1-8、SPEC-001 4.13 與 7.11 第 5 項，以及 R1-4 的「另加」AC。沒有任何已接受的條款把「數值欄位超出浮點範圍」排除在這些條款之外，也沒有任何 DA record 把引擎回應的內容列為可以傳出例外的情形。

**不 defer。** 治理 §4.5 的四個條件須同時成立：

| # | 條件 | 本 finding |
| --- | --- | --- |
| 1 | 不主張違反 accepted contract 條款 | **不成立。** R2-F1 主張、並經 R2、Alternate 與本 FA 證實違反 R1-4 範圍 (f)、CL-R1-8、SPEC-001 4.13／7.11 第 5 項與 R1-4 的 AC。這類 finding 只能 dismiss、要求 rework，或作為 contract change 交 DA 與 acceptor |
| 2 | 殘餘風險在宣告的 operating scope 與 assurance policy 之內 | 條件 1 已不成立，未評估 |
| 3 | 有 owner 與 tracked item | 同上，未評估 |
| 4 | 記錄理由且不把任何 gate 標為 PASS | 同上，未評估 |

另外，R2-F1 屬 H-4（判定第 4 項，路線採用的檢查）；依治理 §4.5 與高風險 decision 第 5 節，deferral 須另有 Design Authority 確認，FA 不得單獨 defer。條件 1 已不成立，所以沒有向 DA 請求 deferral 確認。

**不是 design／requirement issue。** 同意 Alternate 第 2.2 節 (3) 的分類，依據：
- 契約已經定義這類回應的結果：數值欄位無法使用時是「無法驗證」，不採用；有國道訊號時 `highway_in_route` 優先；沒有時 `routing_unavailable`（第 2.1 節）。不需要新的語義。
- 同一個函式對其他所有無效值都已依這個語義處理（第 2.3 節 D 列、第 2.2 節末項）；超出浮點範圍的整數走不同路徑，是 `math.isfinite` 的型別轉換造成的 implementation defect。
- 即使採較窄的讀法（長度荒謬的回應整體不可信、不取訊號），無訊號的情形本來就該是 `routing_unavailable`，而結果是例外；finding 依然成立。
- 修正的做法屬 Executor 的 HOW（治理 §2.4）。
所以不 route 至 Design Authority（rework 中出現語義問題時的處理見第 3.2 節第 4 項）。

**Severity。** R2 與 Alternate 都評 Medium／blocking，blocking status 與 severity 都沒有爭議。本 ruling 不另行評定。

**起源的描述。** R2 稱「correction 直接產生的 regression」，Alternate 稱這只描述了一半（root cause 自 `7cb4b0c` 存在，非 200 路徑是 correction 擴大了可達範圍）。本 FA 的證據（第 2.2 節：三個版本的 `_real` 逐字相同；第 2.3 節 C 列）支持 Alternate 的描述；但 R2 的分類在 R2 的範圍內成立（治理 §4.4 R2 第 2、3 項：修正引入或暴露的 defect），R2 也沒有主張 200 路徑沒有問題，只是不在 R2 範圍內另立 finding。兩者沒有互相否定，本 ruling 不覆寫任何一方的結論。

**R1-F1。** Alternate 的 verdict 只把 R2-F1 列為未解；R2 對 R1-F1 的 NOT RESOLVED 明寫唯一理由是 R2-F1，並「不重複計算」。兩方對事實一致：R1 的三個重現已通過（本 FA 第 2.3 節 A 列亦同），剩下的問題全部在 R2-F1。本 ruling 不另行處置 R1-F1，也不在「已解決」與「NOT RESOLVED」兩個標示間作選擇（處置不因此不同）。R1-F1 的回歸測試在 cycle 2 必須保留並通過（第 3.2 節 closure 證據第 3 項）。

**為什麼是新 cycle，而不是在 cycle 1 內修正。** Cycle 1 已用完 R1、R2 與唯一一次 Alternate Review（治理 §4.4，不得有 R3／R4）。修正後的 subject 需要 independent audit 才能 closure，唯一合法的路徑是 FA 授權的新 bounded cycle（治理 §4.5「Cycle 起點與進展」；orch-default §6「新 cycle」）。實質理由：一個已重現、契約依據明確、可在 #16 範圍內以 HOW 修正的 implementation defect；它的 root cause 尚未經過任何新 cycle，治理 §4.5 的進展限制還沒有觸及。

### 3.2 Rework 的範圍與 closure 所需的證據

Owner：**#16 Executor**（`gov-executor`，同一 worklog identity `docs/governance/records/worklog/issue-16.md`）。

**範圍以 root cause 為準，涵蓋 200 與非 200 兩條路徑、`summary.time`。** 採用 Alternate record 第 2.2 節 (4) 對未解範圍的界定：root cause 在 `adoption.py` 的 `_real`，涵蓋 `trip.summary.length`、`trip.summary.time`、`edges[n].length`，路線回應與道路屬性回應，HTTP 200 與非 200。理由：
- 這是同一個 root cause，不是無關的 scope expansion（治理 §4.4 targeted correction 的限制）；200 路徑的行為屬 R1-4 範圍 (b)、(c)、(f) 的 accepted work scope，既有測試 `test_a_route_reply_that_cannot_be_read_is_routing_unavailable_with_no_freeway_check` 也已表明 200 回應讀不到欄位時的語義。
- 只修 R2 點名的兩個新增呼叫處（`:372`、`:392`）會留下已重現的 200 路徑例外（第 2.3 節 C 列）；cycle 2 的 R1 是完整 audit，會以同一 root cause 再次 blocking，而依治理 §4.5 屆時不得再以 rework 授權 cycle 3。
- 這是 R2 Required fix 的超集合，不覆寫 R2：R2 要求的非 200 訊號收集、保守拒收、保留 `engine_error`／`trace_failed`、四類回歸證據都包含在內。

**要達成的結果（不是做法；做法由 Executor 決定）：**
1. **不拋未捕捉例外。** 對任何可由產品的 `_parse_json` 解析出的本文，`trip.summary.length`、`trip.summary.time` 與 `edges[n].length` 的值不論為何，`evaluate_direction` 與 `get_route` 都不因它拋出未捕捉的例外；結果是採用的路線或路線錯誤代碼（R1-4 範圍 (f)）。適用於 HTTP 200 與非 200、路線回應與道路屬性回應。
2. **保守拒收。** 這些欄位的值無法作為有限數值用於檢查時（已知成員：絕對值超出浮點範圍的整數，例如 `2**1024`、`10**400`、`-(10**400)`），該方向不採用、不存快照；沒有國道訊號時不產生 `freeway_check` 的值，結果是 `routing_unavailable`；同一回應或任一方向有國道訊號時是 `highway_in_route`（CL-R1-8；7.11 第 5 項；R2 Required fix）。非 200 時仍保留 `engine_error`／`trace_failed`。
3. **訊號收集與兩方向檢查不中斷。** 同一回應中其他可讀的國道訊號照樣收集；去程得到回應時，回程照樣送出並檢查（CL-R1-8）。
4. **不改變其他行為。** 非 200 永不採用；不以非 200 回應的 shape 送道路屬性查詢；不重試、不跟隨轉址、不改用過期快照、不存快照；200 的既有採用與拒收行為不變；rework 前已被視為有效數值的值（例如 `2**1023`）與其他無效值（第 2.3 節 D 列）的結果不變；R1-F1 的修正保留。若 Executor 認為達成結果 2 需要決定第 2.1 節契約沒有涵蓋的語義（例如對長度或時間另設上限），停止並依治理 §2.4 route 至 Design Authority，不自行決定。

**可以修改的檔案（封閉清單）：** `src/moto_copilot/routing/adoption.py`；`tests/test_routing_engine.py`；`docs/governance/records/worklog/issue-16.md`。其他檔案都不改，包括 `source.py`、`valhalla.py`、`http_transport.py`、`canonical.py`、`request_key.py`、`snapshot.py`、`store.py`、`target_gpx.py`、`__init__.py`、`contracts/`、`ingest/`、其他測試檔與 `pyproject.toml`；不加入任何 xfail／skip；不發出網路請求；不讀 `data/`、不執行 `experiments/`（CL-R1-1、RB-7）。結果 1～4 無法只在 `adoption.py` 內達成時，停止並回報，不自行擴大修改範圍。既有測試函式不刪改；Executor 判斷非改不可時，依 E-5 在 worklog 逐項寫明理由，由 cycle 2 的 R1 判定。

**範圍界定（不是 finding，也不是判斷）：** `routing/` 內其他使用 `math.isfinite` 的位置——`valhalla.py:104`（呼叫者給的請求位置）、`canonical.py:45`（只處理 `float`，#14）、`target_gpx.py:166`、`:173`（#15）——處理的是呼叫者輸入或內部計算值，不是引擎回應的內容，不屬 R2-F1 的 root cause，不在本 rework 範圍。本 ruling 不對它們的行為作任何判斷；cycle 2 的 R1 依其完整 audit 的範圍自行判斷。

**Closure 證據（cycle 2 的 Reviewer 據此判定，本 ruling 不預判結果）：**
1. **合成的回歸測試**（`tests/test_routing_engine.py`，經 `get_route` 的來回行程）：三個欄位（`trip.summary.length`、`trip.summary.time`、`edges[n].length`）× HTTP 200 與非 200（至少 503；建議沿用 R1-F1 測試的 302、400、429、500、503）× 有、無國道訊號 × 至少 `2**1024`、`10**400`、`-(10**400)`。每一例斷言：沒有例外；代碼依結果 2；非 200 的 reasons 含 `engine_error`／`trace_failed`；沒有路線（`assert_no_route`）；沒有快照檔；請求序列（回程照樣送出、沒有重試、沒有依錯誤回應的 shape 送查詢）。另以至少一例確認 `2**1023` 的結果與 rework 前相同。
2. **其他無效值不變**：worklog 記錄 rework 前後，第 2.3 節 D 列（或 Alternate record 第 2.2 節 (3)）所列其他無效值的結果相同。
3. **無回歸**：R1-F1 的回歸測試（`test_r1_f1_*`）與既有測試保留並通過；`tests/` 的 diff 沒有刪改既有測試函式（或依上段以 E-5 列明理由）。
4. **突變**：至少一個突變「恢復 cycle 1 的行為（對 `int` 先轉成 `float` 再檢查有限性）」被新測試抓到；原始碼的還原方式與第 10.7、11.5 節相同（記憶體中的原文寫回，結束時 SHA-256 相同）。
5. **E-1～E-6**：E-1 在 cycle 2 的最終 subject 重跑，完整輸出記在 worklog；E-2 的對照表加入新測試；E-3 合成資料的來源；E-4 沒有網路請求；E-5 如適用；E-6 依高風險 decision 第 5 節更新 H-1、H-2、H-4 的 self-verification。
6. **陳述與證據相符**：worklog 第 11.2 節 D-16-26（「欄位型別錯誤……不拋例外」）與第 11.5 節 H-4 的「每一種非 200 的情形都是明確的路線錯誤代碼」，以及 `adoption.py` 的模組說明，改為與實際行為及證據一致（root `CLAUDE.md`「實驗與陳述的誠信」；治理 §3.7）。
7. **Commit**：一個與 record commits 分開的 implementation commit，只含封閉清單中的程式與測試檔，message 註明 R2-F1 與本 ruling；worklog 另以 record-only commit。

### 3.3 新 bounded cycle（cycle 2）的授權

- **相對 cycle 1 受審 subject 的實質改變**（cycle 1：`0799682`，程式與測試 subject `65aa00c`）：
  1. `src/moto_copilot/routing/adoption.py`：引擎回應數值欄位（`trip.summary.length`、`trip.summary.time`、`edges[n].length`）的檢查改變，達成第 3.2 節的結果 1～4。
  2. `tests/test_routing_engine.py`：第 3.2 節 closure 證據第 1 項的合成回歸測試。
  3. worklog 與模組說明的陳述更正（closure 證據第 6 項）。
  只有 record-only 的 delta（`docs/governance/records/**`）而沒有第 1、2 項的程式與測試 delta 時，不構成實質改變，**不得**開始 cycle 2（治理 §4.5：「Subject 與契約皆未改變時，不得開新 cycle」）。
- **起點與流程**：cycle 2 從 **R1** 開始，是完整的 independent audit（治理 §4.4：完整審查 #16 的 accepted work scope——R1-4 與其 AC、E-1～E-6、DD-R1-2、CL-R1-5～CL-R1-9、CL-R1-13、14、17、19、20、21、24～27，以及 H-1、H-2、H-4 的最低核對範圍——不限於本 ruling 的 finding），之後依 R2、exactly one Alternate、FA 的順序。`primary_reviewer` 依 Bindings O-6／§3.3 的當次可用性解析；fresh context。R1 的 bounded pack 加入本 ruling 與 cycle 1 的 R1、R2、Alternate records 的路徑。Cycle 2 的 R1 不兼作 SPEC-R1 的 Spec Integration Audit（SPEC-R1 有四張 Ticket，Bindings §5 的單 Ticket fast path 不適用）。
- **派工時點**：本 ruling 沒有 route 任何 DA 問題，Executor 的 rework 可在本 ruling 由派工者採用並 commit 之後開始；cycle 2 R1 在第 1、2 項的 delta 存在之後派工。
- **進展限制**（治理 §4.5）：本 ruling 為進展限制界定的 root cause 是「`adoption.py` 對引擎回應數值欄位（`trip.summary.length`、`trip.summary.time`、`edges[n].length`）的讀取與檢查，對合法的 JSON 數值拋出未捕捉的例外，而不是依 CL-R1-8 與 7.11 第 5 項把它當作無法驗證、收集其餘國道訊號並決定代碼」（cycle 1 已知的機制：`_real` 的 `math.isfinite` 對 `int` 先轉 `float`）。若這個 root cause 的 blocking finding 在 cycle 2 的 R2 之後仍未解，它不再視為 rework 可解的 implementation defect：之後的 FA 必須把它作為 design／requirement issue 交 DA，或在 disposition 邊界內處置，**不得**再以 rework 授權 cycle 3。因為它主張違反契約條款並屬 H-4，屆時 deferral 的條件 1 同樣不成立。同一 root cause 在新 cycle 再次進入 FA，構成 E-FA (M2)，由派工者機械套用（Bindings §3.2）。Cycle 2 的 findings 是否屬此 root cause，由 cycle 2 的 Reviewer 判斷。
- **Executor 的 mapping**：Bindings §3.2 宣告 E-EX 不適用（O-1：escalated mapping 等於有效 mapping），Executor 仍是 `claude-opus-5-5`／`high`。這只是提醒，不是本 ruling 的決定。

### 3.4 Routing

- **Design Authority**：不需要。本 ruling 沒有語義問題交 DA；rework 中出現的語義問題依第 3.2 節第 4 項 route。
- **Acceptor**：不需要。本 finding 沒有 boundary 問題、沒有 reserved boundary 的動作、沒有外洩（高風險 decision 第 5 節「已實際外洩」的處理不適用：例外訊息是固定文字 `int too large to convert to float`，不含座標或本文；沒有任何資料送出）。
- 既有的 tracked items（TI-C16-2、TI-C16-3、RV-12～RV-14）與 NV 項目沿用 DA 的 disposition 與 owner，本 ruling 沒有觸及。

## 4. 每條未解 blocking finding 的處置

| Finding | 處置 | Owner | 依據 | 後續 authority |
| --- | --- | --- | --- | --- |
| R2-F1（root cause：`adoption.py` 的 `_real` 對超出浮點範圍的 `int` 拋 `OverflowError`；涵蓋 `summary.length`、`summary.time`、edge `length`，200 與非 200） | **要求 targeted rework，並以它授權新的 bounded cycle（cycle 2，自 R1 起）**。不 dismiss（證據支持違反）；不 defer（條件 1 不成立；H-4）；不是 design issue | #16 Executor（rework）；Orchestrator（派工與 cycle 2） | 第 2 節證據；第 3.1～3.3 節 | Cycle 2 的 Primary Reviewer（R1 完整 audit）；同一 root cause 在 cycle 2 R2 後仍未解時，依治理 §4.5 交 DA 或在 disposition 邊界內處置 |

R1-F1 不在未解的 blocking findings 中（第 3.1 節「R1-F1」）；本 ruling 不另行處置。

## 5. 本 ruling 沒有做的事

- 沒有把任何 gate 標為 PASS；沒有判定 E-1～E-6、SR1-AC3 或 H-1／H-2／H-4 的核對結果。第 2.4 節的 pytest 只是重現的基準。
- 沒有修改或隱性放寬任何 requirement、AC、invariant 或 gate：第 3.2 節的結果 1～4 都是既有條款（R1-4 範圍 (f)、CL-R1-8、SPEC-001 4.13、7.11 第 5、6 項、H-4）在已重現情形下的適用；closure 證據引用既有的 E-1～E-6 與高風險 decision 第 5 節。
- 沒有覆寫任何 Reviewer 的結論：R2 與 Alternate 對有效性、severity、blocking 的判定一致；起源描述與 R1-F1 標示的差異不影響處置，本 ruling 不在其間選擇。
- 沒有裁決 Outcome Contract boundary，沒有取得 Design Authority 或 acceptor 保留的權限。
- 沒有指定修正的做法，也沒有重新設計。

## 6. NOT VERIFIED

| # | 項目 | Required authority |
| --- | --- | --- |
| NV-1 | 真實 Valhalla 伺服器是否可能回傳超出浮點範圍的整數長度或時間、非 200 回應本文的實際形狀：**NOT VERIFIED／NOT RUN**。不影響本 ruling：契約的結果語義適用於任何回應 | acceptor；之後獲授權的整合 work item（c161 第 2.7 節） |
| NV-2 | 本 FA 全部 assistant 訊息的實際 (model, effort) | 派工者（Bindings §3.6），記入 run record |
| NV-3 | Executor、Codex、Alternate 的 binding 證據（transcript、rollout）。本 FA 沒有獨立讀取，第 (b) 欄引用 run record 的核對紀錄 | — |
| NV-4 | 只在 Python 3.11.2 執行；`math.isfinite` 對過大 `int` 的行為在其他版本沒有實測 | — |
| NV-5 | Worklog 第 10.7、11.5 節的突變檢查沒有重跑（本 FA 不得修改來源） | Executor 的 self-verification 紀錄 |
| NV-PRIVATE | 真實 GPX、保留行程與私有位置資料下的行為：**NOT VERIFIED**。本 run 沒有 RB-7 的路徑授權，沒有嘗試取得；本 ruling 也不需要 | acceptor |

## 7. 下一步

1. **Orchestrator**：核對本 FA 的 binding（Bindings §3.6），記入 run record §6，並原樣 commit 本 ruling。
2. **Orchestrator → #16 Executor**（`gov-executor`，同一 worklog identity）：派第 3.2 節的 rework，派工內容引用本 ruling。
3. **Orchestrator → Primary Reviewer**：subject 含第 3.3 節第 1、2 項的 delta 之後，派 cycle 2 R1（fresh，完整 audit），pack 引用本 ruling 與 cycle 1 的三份 audit records。
4. #16 結案仍依 orch-default §7（P3：失敗的 gate 不因本 ruling 而視為滿足；P4、P5：cycle 2 的 closure 或其後 FA 對每條未解 blocking 的合法處置）。

## 8. 執行紀錄

| 指令／動作 | 結果 |
| --- | --- |
| `sha256sum` Issue #16 原文（scratchpad） | `105fdc98…ffa8ede1`，與派工、run record 第 4 節相同 |
| `git rev-parse 0799682 bc7024b e1e7d32`；`git log --oneline bc7024b..e1e7d32`；`git diff --name-only 0799682..e1e7d32`（主 checkout） | subject、BASE、HEAD 如檔首；`0799682..e1e7d32` 只有三個 record 檔 |
| `sha256sum` R1、R2、Alternate records | 與 run record 事件 92、94、95 相同 |
| `git show <rev>:src/moto_copilot/routing/adoption.py`（`7cb4b0c`、`e1ef580`、`0799682`）的 `_real` 與呼叫處 | 三版逐字相同（第 2.2 節） |
| `git show 0799682:src/moto_copilot/routing/adoption.py` 全文；`source.py` 的 `get_route`、`_ask_engine`、`_engine_info`；worktree 內 `grep -n "isfinite\|OverflowError\|_parse_json\|json.loads" src/moto_copilot/routing/*.py` | 第 2.2 節；第 3.2 節的範圍界定 |
| Worktree：`git rev-parse HEAD`、`git status --porcelain`（前後） | `0799682…`；前後都只有 `?? docs/governance/records/audit/issue-16-c1-r2.md` |
| Worktree：`PYTEST_DEBUG_TEMPROOT=<worktree>/.venv/tmp .venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider -rxXs` | `2015 passed in 41.28s`，exit 0 |
| Worktree：`PYTHONPATH=src;tests PYTHONDONTWRITEBYTECODE=1 .venv/Scripts/python.exe -B -X utf8 <scratchpad>/fa16/probe_fa16.py` | 第一次在 D 列第四例因 harness 的目錄名稱錯誤中止（第 2.3 節末段）；修正後重跑 exit 0，第 2.3 節的表 |
| 閱讀 | 本 definition；Bindings m3（全文）；治理本文 §1.2、§2.4、§2.5、§4.3–§4.6；orch-default v2.2 §6、§7；Profile default v2.5 的 E-FA、E-EX 列；OC-1 鏈上的 `derivation-spec-r1.md` 第 4、5、6 節；c161 的檔首與第 1、2.4–2.7、4–10 節；c141 第 5 節（CL-R1-17）；c151 第 5 節（CL-R1-24）；高風險 decision 第 3.4、4、5 節；SPEC-001 4.13、7.11；R1、R2、Alternate records 全文；worklog 第 11 節；run record §6 事件 89～95；前例 ruling；`tests/test_routing_engine.py` 的 helpers 與 `_malformed` 測試 |

沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有讀取或執行 `experiments/` 下的任何檔案；沒有使用 `git status --ignored`；沒有網路請求；沒有修改受審檔案、契約或其他紀錄；沒有派工任何 subagent；沒有 commit。

Ruling: R2-F1 — targeted rework（範圍以 root cause `_real` 為準，涵蓋 `summary.length`、`summary.time`、edge `length`，HTTP 200 與非 200），授權 cycle 2（自 R1 起）；不 dismiss、不 defer、不交 DA。

---

## Addendum A（2026-11-18）— cycle 2 targeted correction 的檔案範圍；C2R1-F1 與 R2-F1 root cause 的關係

本 addendum 只釐清本 ruling 的適用範圍與 routing（治理 §2.4、§4.5；FA 的 routing／process 權限），不改變上文第 1～8 節的任何裁決，不另作 finding、severity 或 closure 的判斷。

| 欄位 | 內容 |
| --- | --- |
| 日期 | 2026-11-18（Asia/Taipei） |
| 提問者 | Orchestrator，run `run-20261117-oc1-run2`（主 checkout HEAD `f2728d8395d3a1527f1bb5e9ea95c3430f8e7259`；run record §6 事件 96～100） |
| 角色與 context | 同一個 `final_adjudicator` assignment（作出本 ruling 的同一 context），沒有新的派工；binding 依 Bindings §3.6 由派工者核對本段工作的 transcript |
| 讀過的 records | Cycle 2 R1 `docs/governance/records/audit/issue-16-c2-r1.md`（本 FA 重算 SHA-256 `5a8943995c16a586bd4678925ff07d09fb05e1ce33f4251bad7be79226e51d92`，與事件 100 相同；`Verdict: BLOCKING (C2R1-F1, C2R1-F2)`）；run record 事件 96～100。Record 的結論都當成待驗證主張；下文採用的事實由本 FA 另行讀原始碼或重現 |
| 受審 subject（cycle 2 R1） | `fb6210dbceab4b04651380d8bc23ee82d4896484`；cycle 2 的實作 commit `022f629`。`git diff --stat 0799682 fb6210d -- src tests`：只有 `adoption.py`（17 行）與 `tests/test_routing_engine.py`（118 行）；`git diff --name-only fb6210d f2728d8`：只有 cycle 2 R1 record 與 run record |
| Capability escalation | 不提出 E-FA/D1：兩個問題都可以由本 ruling 的文字、治理 §4.4／§4.5 與原始碼直接回答 |

### A.1 問題

1. 本 ruling 第 3.2 節的封閉檔案清單（`adoption.py`、`tests/test_routing_engine.py`、worklog）只約束 R2-F1 的 rework，還是也約束 cycle 2 中針對新 findings 的 targeted correction？具體地說，#16 Executor 能否在 `valhalla.py`、`source.py` 與測試中對 C2R1-F1、C2R1-F2（以及 Low 的 C2R1-F4）作 cycle 2 的 targeted correction，之後進 cycle 2 R2？還是需要另一份 ruling 或其他 route？
2. 本 FA 是否對「C2R1-F1 不是 R2-F1 的 root cause」這個 Reviewer 判斷有異議（它影響本 ruling 第 3.3 節的 cycle 3 限制）？

### A.2 本 FA 自行取得的證據

- `git show fb6210d:src/moto_copilot/routing/valhalla.py` 第 209～237 行：`decode_polyline6` 以無上限的 Python `int` 累加每個值（第 226 行），在第 233 行 `point = (lat / 1e6, lon / 1e6)` 轉成浮點數，第 234 行才做範圍檢查。`git diff 0799682 fb6210d -- src` 沒有 `valhalla.py`；Reviewer 所述自 `7cb4b0c` 起只改過模組說明，與此一致。
- `git show fb6210d:src/moto_copilot/routing/adoption.py` 第 240～245 行：`_route_facts` 呼叫 `decode_polyline6(shape)`，只捕捉 `PolylineError`。第 119～131 行：cycle 2 的 `_real` 在 `math.isfinite` 拋 `OverflowError` 時回傳 `False`；`shape` 不經過 `_real`。
- 本 FA 的記憶體內探測（worktree `cx16r2`，`0799682`；`valhalla.py` 的程式在 `0799682` 與 `fb6210d` 相同；合成字串，socket 封鎖）：`decode_polyline6("~"*210 + "??")` → `OverflowError: int too large to convert to float`（不是 `ValueError`，也不是 `PolylineError`）；`"~"*60 + "??"` → `PolylineError`（超出範圍，第 234 行攔下）；`"~~~"` → `PolylineError`。Worktree 的 `git status --porcelain` 前後不變。
- 本 ruling 第 3.2 節的範圍界定列出 `routing/` 內使用 `math.isfinite` 的其他位置，沒有列出 `decode_polyline6`：它的溢位來自除法，不是 `math.isfinite`，本 FA 當時以 `isfinite` 搜尋而沒有找到它。這是本 FA 範圍界定的遺漏，不改變第 3.3 節對 root cause 的定義。

### A.3 問題 1：封閉清單只約束 R2-F1 的 rework；cycle 2 的 targeted correction 不需要另一份 ruling

**釐清。** 第 3.2 節的封閉檔案清單屬於「Rework 的範圍」一節，只約束 R2-F1 的 material rework，也就是作為 cycle 2 起點、第 3.3 節第 1～3 項所列的那一個 delta（`022f629` 與其 worklog）。它不約束 cycle 2 中針對 cycle 2 新 findings 的 targeted correction。理由：

1. 該清單的作用是讓 R2-F1 的 rework 不夾帶無關的範圍（治理 §4.4 targeted correction 的限制），並界定第 3.3 節所說的「實質改變」。它的對象是本 FA 裁決的那一個 finding。
2. 治理 §4.5：新 cycle「一律從 R1 開始」，之後依 §4.4 的 R1 → targeted correction → R2 →（仍 blocking 時）exactly one Alternate → FA 進行。Cycle 2 R1 的 blocking findings 由 cycle 2 的 Reviewer 擁有（治理 §2.4），它們的 targeted correction 範圍由該 R1 record 的 findings 與 required fix 界定（§4.4：「聚焦 blocking findings」）。本 FA 沒有裁決這些 findings，也沒有權限預先限制合法的 §4.4 流程。
3. 契約內必要的 rework 與 re-verification 不是新工作的接受關卡（治理 §1.2）；orch-default §6 的 audit 流程不要求 cycle 內的 targeted correction 另有 FA 授權。

**結論。** #16 Executor 可以在 cycle 2 內對 C2R1-F1、C2R1-F2 作 targeted correction，之後進 **cycle 2 R2**。不需要另一份 ruling，也不開新 cycle：cycle 2 仍以本 ruling 為起點的引用；在 cycle 2 的 Alternate Review 之前開 cycle 3 是不合法的（治理 §4.5 只有兩個起點）。派工依治理 §2.4 的表：cycle 2 R1 record 已指明 owner（#16 Executor）與 required fix，屬「已指明 authority」，直接派工。

**Correction 的界限**（都是既有規則或既有 routing 的重述，不是新要求）：

1. **聚焦**：以 cycle 2 R1 record 中 C2R1-F1、C2R1-F2 的 required fix 為範圍，不夾帶無關的範圍或重新設計，並提供可驗證的 closure 與回歸證據（治理 §4.4）。R2-F1 的回歸測試（`test_r2_f1_*`）與 R1-F1 的回歸測試（`test_r1_f1_*`）保留並通過。
2. **檔案**：限於 #16 自己的 routing 模組（`valhalla.py`、`adoption.py`、`source.py`；`http_transport.py` 與 F1／F2 無關）、#16 的測試檔（`tests/test_routing_engine.py`，必要時 `tests/test_routing_transport.py`）與 worklog。
3. **已結案 Ticket 與受保護的檔案**：`canonical.py`、`request_key.py`、`snapshot.py`、`store.py`、`target_gpx.py`、`routing/__init__.py`、`contracts/`、`ingest/`、`tests/routing_synthetic.py`、`tests/test_routing_snapshot.py`、`tests/test_routing_store.py`、`tests/test_target_gpx.py`、`pyproject.toml`。若 correction 需要改動其中任何一個（例如 C2R1-F2 牽涉 `build_snapshot`／`canonical_bytes` 的行為），Executor 停止並 route 至 Design Authority，由 DA 判斷是否在 #16 的範圍內、以及對已結案 Ticket（#14、#15、R1-1）的影響（先例：`decision-20261118-issue16-c161.md` 第 2.2、2.4、10 節）。Executor 不自行修改。
4. **語義**：C2R1-F2 中狀態回應 `version` 的處置等契約沒有涵蓋的語義，依 cycle 2 R1 record 的 required fix，停止並依治理 §2.4 route 至 Design Authority。
5. **C2R1-F3**（Low，DA routing）不屬這次 correction；Design Authority 作成決定之前不實作。
6. **C2R1-F4**（Low，non-blocking）：Reviewer 的 disposition（owner #16 Executor，隨 C2R1-F1 處理，不另立 work item）成立，本 FA 不覆寫。它在 #16 的既有契約內（CL-R1-17：快照的完整性問題是 `SnapshotIntegrityError`），與 C2R1-F1 是同一個解碼路徑，不是無關的範圍。所以可以在同一次 correction 中處理，但只限於與 C2R1-F1 共用的 shape 解碼與 `_from_snapshot` 的例外轉換，不得以 F4 的名義作其他改動。它不延長 cycle：R2 不必把它當作 blocking；沒有處理時，依 Reviewer 的 disposition 在 worklog 記下狀態。
7. **其他**：不加入 xfail／skip；不發出網路請求；不讀 `data/`、不執行 `experiments/`（CL-R1-1、RB-7）；實作 commit 與 record commits 分開。

**之後的流程**：cycle 2 R2 依治理 §4.4 核對 C2R1-F1、F2 是否解決、correction 是否引入回歸，以及 correction 直接產生或暴露的 blocking defects；不是第二次全面 audit。R2 仍 blocking 時，派 exactly one cycle 2 Alternate Review；仍未解時進 FA。R2 由哪個 mapping 執行，依 Bindings §3.1、§3.3 解析，不在本 addendum 的範圍。

### A.4 問題 2：本 FA 對「C2R1-F1 不是 R2-F1 的 root cause」沒有異議

本 ruling 第 3.3 節把進展限制所指的 root cause 界定為「`adoption.py` 對引擎回應數值欄位（`trip.summary.length`、`trip.summary.time`、`edges[n].length`）的讀取與檢查，對合法的 JSON 數值拋出未捕捉的例外」，已知機制是 `_real` 的 `math.isfinite`，並寫明 cycle 2 的 findings 是否屬此 root cause 由 cycle 2 的 Reviewer 判斷。Cycle 2 R1 的判斷（C2R1-F1、F2 都不是）與這個定義一致：

1. **欄位與位置不同。** C2R1-F1 是字串欄位 `trip.legs[0].shape`，溢位發生在 `valhalla.py:233` 的 polyline 解碼，不經過 `_real`，也不在三個數值欄位之列（A.2）。
2. **它不在 rework 的範圍內。** 第 3.2 節的封閉清單不含 `valhalla.py`，R2-F1 的 rework 不可能、也不被允許修正它。治理 §4.5 的進展限制針對的是「經過新 cycle 的 rework 之後仍未解」的 root cause，用來判斷它已不是 rework 可解的 implementation defect。把一個從未進入過任何 rework 範圍的缺陷算作同一 root cause，不符合這個用意。Profile 的 E-FA (M2) 也寫「同一 root cause 在新 cycle **再次**進入 Final Adjudication」。
3. **機制相近，如實記下。** 兩者都是「無上限的 Python `int` 轉成浮點數時溢位」。這只是同類機制，不是同一 root cause。C2R1-F1 自 `7cb4b0c` 起存在，cycle 1 的 R1、R2、Alternate 與本 FA 都沒有發現；它由 cycle 2 的完整 R1 發現，正是治理 §4.5「新 cycle 從 R1 開始」所要求的完整 audit 的結果。
4. **C2R1-F2**（孤立 surrogate 使 `build_snapshot` 拋 `SnapshotValidationError`）的機制是字串編碼，與 R2-F1 無關；本 FA 同樣沒有異議。

**對 cycle 3 限制的影響：**
- 第 3.3 節的 cycle 3 限制只綁定 R2-F1 的 root cause。Cycle 2 R1 記錄 R2-F1 已解決、沒有再出現；本 FA 不確認也不覆寫這個 Reviewer 結論，cycle 2 R2 依 §4.4 核對 correction 是否使它回歸。若 R2-F1 的 root cause 在 cycle 2 的 R2 之後再次出現而未解，第 3.3 節的限制照常適用。
- C2R1-F1、F2 是 cycle 2 才提出、尚未進入過 FA 的 findings，第 3.3 節的限制不適用於它們。若它們在 cycle 2 的 Alternate Review 之後仍未解，屆時是它們第一次進入 FA，由該次 FA 依治理 §4.5 決定處置（包括是否授權指明實質改變的新 cycle）；此時 E-FA (M2) 不因它們而成立。本 addendum 不預先決定該次裁決。

### A.5 本 addendum 沒有做的事

- 沒有改變上文第 1～8 節的任何裁決；第 3.2 節的封閉清單對 R2-F1 rework 的約束照舊。
- 沒有判斷 C2R1-F1～F4 的有效性、severity、blocking 或 disposition（Reviewer 的權限）；沒有判斷 R2-F1 是否 closure。
- 沒有把任何 gate 標為 PASS；沒有指定修正的做法；沒有授權新 cycle；沒有處理 C2R1-F3 的語義（Design Authority）。

### A.6 下一步

1. **Orchestrator**：核對本段工作的 binding（Bindings §3.6），記入 run record，並原樣 commit 本 addendum。
2. **Orchestrator → #16 Executor**（同一 worklog identity）：派 C2R1-F1、C2R1-F2 的 cycle 2 targeted correction（C2R1-F4 依 Reviewer 的 disposition），派工內容引用 cycle 2 R1 record 與本 addendum A.3。
3. **Orchestrator → Design Authority**：C2R1-F3；以及 Executor 依 A.3 第 3、4 項回報的問題（若有）。
4. **Orchestrator → Primary Reviewer**：correction 完成後派 cycle 2 R2。

### A.7 執行紀錄

| 指令／動作 | 結果 |
| --- | --- |
| `git rev-parse HEAD`、`git log --oneline e1e7d32..HEAD`、`git diff --stat e1e7d32..HEAD`（主 checkout） | `f2728d8`；8 個 commits；產品與測試的改動只有 `022f629` 的 `adoption.py`、`tests/test_routing_engine.py` |
| `sha256sum` 本 ruling（addendum 之前）與 `issue-16-c2-r1.md` | `b7c0fc24…cbf50aae`（與事件 96、commit `d9061c5` 相同）；`5a894399…6e51d92`（與事件 100 相同） |
| `git diff --stat 0799682 fb6210d -- src tests`；`git diff --name-only fb6210d f2728d8`；`git log … bc7024b..f2728d8 -- src/moto_copilot/routing/__init__.py` | A.2 表頭；`__init__.py` 只在 `7cb4b0c` 改過 |
| `git show fb6210d:src/moto_copilot/routing/valhalla.py`（第 205～237 行）、`git show fb6210d:src/moto_copilot/routing/adoption.py`（第 115～132、236～250 行） | A.2 |
| Worktree `cx16r2`：stdin 探測 `decode_polyline6` 的三個合成字串（`-B`、`PYTHONDONTWRITEBYTECODE=1`、socket 封鎖） | A.2；`git status --porcelain` 前後都只有 `?? docs/governance/records/audit/issue-16-c1-r2.md` |
| 閱讀 | `issue-16-c2-r1.md` 全文；run record 事件 96～100 |

沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有讀取或執行 `experiments/`；沒有網路請求；沒有讀取派工範圍以外的 worktree（`cl16c2r1` 沒有開啟）；沒有修改受審檔案或其他紀錄；沒有 stage 或 commit。

Addendum A: 封閉檔案清單只約束 R2-F1 的 rework；C2R1-F1、F2（與依 Reviewer disposition 的 F4）的 cycle 2 targeted correction 依治理 §4.4 進行、之後進 cycle 2 R2，不需要另一份 ruling；修改已結案 Ticket 的檔案或需要新語義時 route 至 DA。本 FA 對 C2R1-F1（及 F2）不是 R2-F1 root cause 的判斷沒有異議；第 3.3 節的 cycle 3 限制只綁定 R2-F1 的 root cause。
