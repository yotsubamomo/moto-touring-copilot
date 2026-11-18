# Issue #16 — cycle 1 Alternate Independent Review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，接受版本 `873e37a`）→ SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md` 第 4 節 DD-R1-2、CL-R1-5～CL-R1-9，第 5 節 R1-4 與 E-1～E-6）＋`decision-20261118-issue13-c131.md`、`decision-20261118-issue14-c141.md`、`decision-20261118-issue14-qalt1.md`、`decision-20261118-issue15-c151.md`、`decision-20261118-issue16-c161.md` → Issue #16（原文 SHA-256 `105fdc981b1087b60b419690168d205064853a1a41ccde4a6cb092b6ffa8ede1`，本 review 自行核對相符） |
| Subject | Branch `oc1-run2-b1-ui0-r1-routing`；BASE `bc7024b24b968e2dfb04dc38e822781dd5fb5425`；受審 HEAD `07996828afaa0db3a7d477a05528fe993dc46d49`（R2 subject）。實作 commits `7cb4b0c`、`f6810d2`、`65aa00c`。主 checkout 的 HEAD `eb0b6e6` 相對 `0799682` 只多 `docs/governance/records/**`（`git diff --name-only 0799682..HEAD`：R2 record 與 run record） |
| Audit kind | **Alternate Independent Review，cycle 1**（治理 §4.4；本 cycle 唯一一次）。不是 R1、不是 R3，不是 Spec Integration Audit，不是 Final Adjudication |
| Role | `alternate_reviewer`（`gov-alternate-reviewer`）；本 record 由本 review 自行以 Write 寫入 |
| 日期 | 2026-11-18（Asia/Taipei） |
| Records | R1：`docs/governance/records/audit/issue-16-c1-r1.md`（SHA-256 `32d43f3a…430c2472`）；R2：`docs/governance/records/audit/issue-16-c1-r2.md`（SHA-256 `a88e9ebe…4d4ad58f`）；worklog：`docs/governance/records/worklog/issue-16.md` 第 11 節；run record：`docs/governance/records/run/run-20261117-oc1-run2.md` 第 6 節事件 89～94 |
| 結果 | **R1-F1：已解決。R2-F1：有效、未解決、blocking 的分類成立、不是 design／requirement issue。** R2-F1 的 root cause 是 `adoption.py` 的 `_real`，自 `7cb4b0c` 起就存在，HTTP 200 的路徑也有同一個未捕捉例外；R2 把它描述為「correction 直接產生」只對了一半（見第 2.2 節） |

## 1. Assurance

### (a) Context independence（治理 §2.3 四項 properties）

| Property | 本次的滿足方式與證據界限 |
| --- | --- |
| Independent context | Fresh subagent context，沒有繼承 Executor、Primary Reviewer 或派工者的對話。從派工內容的路徑與識別開始，自行讀契約、R1／R2 record、worklog、run record、原始碼、diff 與測試。R1、R2 與 worklog 的結論都當作待驗證主張，下文每項判斷都附本 review 自己取得的證據 |
| Verifiable binding | 以 `gov-alternate-reviewer` 派工；有效 mapping 是 `claude-fable-5-2`／`high`（Bindings m3 第 3.1 節，O-5；E-AR 不採用）。本 context 的 runtime 聲明 model ID 為 `claude-fable-5-2`；這是自我觀測，不是 binding 證據。**全部 assistant 訊息的 (model, effort) 由派工者依 Bindings 第 3.6 節以 transcript 核對並記入 run record**；本 review 無法自行觀測 effort |
| Autonomous access | 自行以 `git show 0799682:<path>`、`git diff`、`git log` 讀受審版本與歷史；在 worktree `C:/Users/yotsu/AppData/Local/Temp/cx16r2`（`git rev-parse HEAD` = `0799682…`）自行執行全套測試與 stdin 探測。沒有讀取、列出或搜尋 `data/`，沒有讀或執行 `experiments/`，沒有讀 `.env`，沒有網路請求（探測中另把 `socket.socket`、`create_connection`、`getaddrinfo` 換成拒絕函式） |
| Self-written record | 本檔是本 review 唯一新建的檔案。沒有修改、stage 或 commit 任何實作、測試、契約或 gate。探測只用合成值、經 stdin 在記憶體內執行（`PYTHONDONTWRITEBYTECODE=1`）；暫存目錄建在派工指定的 `.venv/tmp`（git-ignored）並於結束時移除。寫本檔前主 checkout `git status --porcelain` 為空，worktree 只有 Codex 留下的 `?? docs/governance/records/audit/issue-16-c1-r2.md` |

### (b) 實際 model

| Assignment | 實際 model | 證據 |
| --- | --- | --- |
| Executor | `claude-opus-5-5`／`high` | Run record 第 6 節事件 89、91、93（agentId `a1e2cfa52290d496f`；事件 93 記全部 202 則 assistant 訊息只有此一值，派工者判定符合） |
| Primary Reviewer（R1、R2） | Codex `gpt-6.1-sol`／`high` | Run record 事件 92（R1，thread `01a1ecfa-…`）與事件 94（R2，thread `01a1ed0d-…`）：`turn_context` 集合都只有 (`gpt-6.1-sol`, `high`, `workspace-write`)。這是派工者的核對紀錄；本 review 沒有讀 rollout |
| Alternate Reviewer（本 review） | `claude-fable-5-2`（runtime 聲明；effort 未能自行觀測） | 待派工者核對並記入 run record |

三個 assignment 紀錄的 model 互不相同。Bindings 第 5 節沒有宣告任何 diversity 關係，本 record 不以 model diversity 作為 assurance 的主張；independence 只依 (a)。

## 2. 對 R2 後剩餘 finding 的判斷

### 2.1 R1-F1（R1：Medium／blocking；R2：NOT RESOLVED）— 判斷：**已解決**

R1-F1 的缺陷是「非 200 的路線／道路屬性回應在讀取本文的國道訊號之前就離開」（R1 record 第 2 節；`e1ef580` 的 `adoption.py:367`、`:382`）。本 review 對 Required fix 逐項核對：

| Required fix | 本 review 的證據 | 判斷 |
| --- | --- | --- |
| 回應是否成功與訊號收集分開；非 200 保留 `engine_error`／`trace_failed` | `0799682` 的 `adoption.py:368`～`373`、`:387`～`392`；`git diff e1ef580..0799682 -- src/`：只有 `adoption.py`，12 additions／3 deletions | 成立 |
| R1 的三類反例改為 `highway_in_route` | 自行經 `get_route`（`plan` helper、來回行程、去程非 200）重現：route 503＋`has_highway` → `highway_in_route`，reasons `('outbound:has_highway', 'outbound:engine_error')`；trace 503＋`motorway` → reasons 含 `outbound:motorway_edge`、`outbound:trace_failed`；trace 503＋名稱 `Freeway` → 含 `outbound:freeway_name`、`outbound:trace_failed`。另試回程 route 500＋`has_highway`、route 502 只有 leg summary 的旗標：都是 `highway_in_route` | 成立 |
| 無訊號的非 200 仍是 `routing_unavailable` | route 503、trace 503 無訊號：`routing_unavailable`，reasons 分別只有 `outbound:engine_error`、`outbound:trace_failed` | 成立 |
| 非 200 永不採用、不存快照、不跟隨轉址、不重試、不以錯誤回應的 shape 發查詢 | 上列各例 `stored=[]`；請求序列為 `route, route, trace_attributes` 或 `route, trace_attributes, route, trace_attributes`，沒有第二次同類請求、沒有 `status`；逐欄位代換探測（第 3 節 P4）3 828 例中非 200 而有 leg 的為 0；`git diff --exit-code e1ef580..0799682` 對 `valhalla.py`、`http_transport.py`、`source.py`、`store.py`、`snapshot.py`、`tests/test_routing_transport.py`、`tests/test_routing_store.py` 為空、exit 0 | 成立 |
| 200 的既有行為不變 | 200 分支的程式沒有改（diff 只把條件式改寫成等價的 `has_trip` 形式，並在 trace 非 200 的分支加訊號收集）；`tests/` 的 diff 是 116 additions／0 deletions，沒有刪改既有測試；全套 `2015 passed` | 成立 |
| 回歸案例與 worklog | `tests/test_routing_engine.py` 新增的 `test_r1_f1_*`；worklog 第 11 節 | 成立 |

R2 把 R1-F1 記為 NOT RESOLVED 的唯一理由是 R2-F1，並明寫不重複計算。本 review 的判斷是兩者 root cause 不同：R1-F1 是「提早離開」，已由 `65aa00c` 修正；剩下的失敗來自 `_real` 對超出浮點範圍的整數拋例外，這在 R1-F1 不涉及的 200 路徑上同樣存在（第 2.2 節）。因此 **R1-F1 應記為已解決，殘餘問題全部歸在 R2-F1**；R2 對 R1-F1 的 NOT RESOLVED 標示屬分類有誤（歸屬），但不改變本 cycle 仍有未解 blocking 的結果。

### 2.2 R2-F1（R2：Medium／blocking，owner #16 Executor）— 判斷：**有效、未解決；blocking 成立；不是 design issue；起源的描述需更正**

**(1) 有效性：重現成立。** 本 review 以真實的位元組本文（401 位數的整數字面值，經產品自己的 `_parse_json` 解析成 `int`）重現 R2 的四例，並經 `get_route` 確認：

| 去程回應（來回行程） | `0799682` 經 `get_route` 的結果 |
| --- | --- |
| route 503，無訊號，`trip.summary.length = 10**400` | 未捕捉的 `OverflowError: int too large to convert to float`；`stored=[]`；請求只有 `route` |
| route 503，`has_highway = true`，同上 | 同上（預期 `highway_in_route`） |
| trace 503，無訊號，`edges[0].length = 10**400` | 未捕捉的 `OverflowError`；`stored=[]`；請求 `route, trace_attributes`，回程沒有送出 |
| trace 503，`motorway`，同上 | 同上（預期 `highway_in_route`） |

來源：`adoption.py:118` `_real` 的 `math.isfinite(value)` 對 Python `int` 先轉成 `float`；`:187`、`:191`（`summary.length`、`summary.time`）與 `:276`（edge `length`）呼叫它。觀測到的界線：`2**1023` 不拋，`2**1024 - 1`、`2**1024`、`10**400`、`-(10**400)` 都拋（負數也拋，因為 `isfinite` 先於 `>= 0` 執行）。`summary.time` 有同樣的行為，R2 沒有列出。

**(2) 契約依據成立，不需要補寫語義。**

- R1-4 範圍 (f)：共用介面回傳「採用的路線」或「路線錯誤代碼」。契約明列可以傳出例外的情形是嚴格模式的停止（CL-R1-4）、快照存放與選取的錯誤（CL-R1-17、CL-R1-21）、目標 GPX 沒有給行程型態與呼叫端輸入錯誤（CL-R1-24）；引擎回應的內容不在其中。
- CL-R1-8（`derivation-spec-r1.md:73`）：「引擎有回應時，先檢查所有可取得的國道訊號，再決定代碼」；SPEC-001 4.13：引擎「回傳錯誤」是 `routing_unavailable`，同時有國道訊號時是 `highway_in_route`。四例都是引擎有回應而沒有決定出代碼。
- H-4 最低核對範圍（`decision-20261117-high-risk-categories.md` 第 5 節）：失敗的每條路徑的結果是明確錯誤。
- Correction 自己的要求：worklog 第 11.2 節 D-16-26「欄位型別錯誤……不拋例外」與 R2 派工的同一要求，在這一類數值上不成立；worklog 第 11.5 節「每一種非 200 的情形都是明確的路線錯誤代碼」與上表不符。

**(3) 「CL-R1-8 是否要求長度欄位無效時仍取得訊號」：是，由已接受的契約可以直接判定，不屬 design／requirement issue。** 依據：

- SPEC-001 7.11 第 5 項：有任何國道訊號就是 `fail`，「優先於其他原因（警告、偏移、無法驗證）」；長度不符是其中列舉的「無法驗證」。無法使用的長度只會使長度比對無法成立，不影響 `has_highway`、`motorway`、名稱是否可讀。
- DA 已接受的 disposition 都採同一方向：非布林的真值旗標仍記為訊號（`decision-20261118-issue16-c161.md` 第 4.3 節）；道路屬性回應有警告時其國道訊號照樣計入（CL-R1-27）。
- 實作本身對其他所有無效長度都這樣處理。本 review 的探測（第 3 節 P3）：`length` 為 `"abc"`、`-1`、`null`、`true`、`1e400`、`-1e400`、`[]`、`{}` 時，route 503／200 都保留 `has_highway` 訊號，trace 503／200 都保留 `motorway_edge` 訊號，沒有例外。唯一不同的是超出浮點範圍的整數，原因是 `math.isfinite` 的轉換，不是設計選擇。
- 即使採較窄的讀法（長度荒謬的回應整體不可信、不取訊號），R2-F1 仍然有效：無訊號的兩例本來就該是 `routing_unavailable`，而結果是例外。

所以這是 implementation defect。**Required authority = Design Authority：不適用。**

**(4) 起源：R2 的「correction 直接產生的 regression」只描述了一半。** 本 review 把 `7cb4b0c`、`e1ef580`、`0799682` 三個版本的 `adoption.py` 以 `git show` 載入記憶體，對同一組輸入執行 `evaluate_direction`：

| 輸入（單方向） | `7cb4b0c` | `e1ef580`（R1 subject） | `0799682`（R2 subject） |
| --- | --- | --- | --- |
| route **503**，`length` 或 `time` = `10**400`（有、無訊號） | `('engine_error',)`，無例外 | `('engine_error',)`，無例外 | `OverflowError` |
| trace **503**，edge `length` = `10**400`（有、無訊號） | `('trace_failed',)`，無例外 | `('trace_failed',)`，無例外 | `OverflowError` |
| route **200**，`length` 或 `time` = `10**400`（有、無訊號） | `OverflowError` | `OverflowError` | `OverflowError` |
| trace **200**，edge `length` = `10**400`（有、無訊號） | `OverflowError` | `OverflowError` | `OverflowError` |

- 非 200 路徑：行為確實由 `65aa00c` 改變（明確錯誤 → 未捕捉例外）。這是 correction 把既有缺陷的可達範圍擴大到新路徑，屬治理 §4.4 R2 第 2、3 項（修正引入的回歸；修正直接產生或暴露的 blocking defect），在 R2 的合法範圍內。這部分 R2 的分類成立。
- Root cause（`_real`）不是 correction 產生的：三個版本的 `_real` 逐字相同，200 路徑自本 Ticket 的第一個實作 commit `7cb4b0c` 起就會拋同一個例外，經 `get_route` 也一樣（第 3 節 P2-C：四例都是未捕捉的 `OverflowError`，`stored=[]`）。這是本 Ticket accepted work scope 內的既有缺陷，R1 沒有發現；它**不是** R1-4 契約未規定的情形——200 回應的欄位無法讀取時，契約的結果同樣是 `routing_unavailable`（有訊號時 `highway_in_route`），既有測試 `test_a_route_reply_that_cannot_be_read_is_routing_unavailable_with_no_freeway_check` 也是這個語義。
- 本 review 不為 200 路徑另立 finding 編號，也不開新的 round：它與 R2-F1 是同一個 root cause。但必須記明：**R2 的 Required fix 只寫非 200 的訊號收集；只在兩個新增呼叫處處理而不處理 `_real` 的修正，會讓 200 路徑照樣拋例外。** 未解決的範圍是「`_real` 對合法 JSON 整數不是全域函式」，涵蓋 `summary.length`、`summary.time`、edge `length`，200 與非 200 兩條路徑。修正的 HOW 屬 Executor；是否與如何要求 rework 屬 Final Adjudicator。

**(5) Severity／blocking：同意 Medium／blocking。**

- Blocking 的依據是 accepted contract 的結果語義（上列 (2)）與 correction 引入的回歸，不是偏好；本 review 無法提出推翻該主張的證據，反而重現了它。
- 風險的實際大小（供後續裁決參考，不改變上述判斷）：沒有 fail-open 的證據。所有重現例都沒有採用路線、沒有存快照；逐欄位代換探測中非 200 而被採用的為 0。例外訊息是固定文字 `int too large to convert to float`，不含座標或本文。觸發條件是回應中出現 309 位數以上的整數長度或時間，真實伺服器是否可能回傳未經驗證（NV-1）。後果是整次規劃以未捕捉例外中止，而不是契約規定的路線錯誤；有訊號時也拿不到 `highway_in_route`。

**(6) 其他例外類別（有界探測，非新 finding）。** 為判斷 R2-F1 的範圍是否完整，本 review 對合成的路線與道路屬性本文做逐欄位代換（每個欄位路徑 × 22 種 JSON 值 × 狀態 200、302、500；route 2 970 例、trace 858 例）。唯一出現的例外是 `OverflowError`，只出現在 `trip.summary.length`、`trip.summary.time`、`edges[n].length` 為超出浮點範圍的整數時，三種狀態都有。這個探測有界，不等於窮舉，也不是重跑 R1。

另一個邊界觀察，不是 finding：本文含超過 Python 整數字串轉換上限的字面值（實測 5 001 位數）時，`_parse_json` 回傳 `None`，結果是 `engine_error`、沒有訊號、沒有例外。這與「不是 JSON 的本文」的既有處理一致，結果是明確錯誤。

## 3. 實際執行

全部在 worktree `C:/Users/yotsu/AppData/Local/Temp/cx16r2`（detached `0799682`）或主 checkout 以唯讀 git 指令執行；Python 3.11.2。

| # | 命令／檢查 | 結果 |
| --- | --- | --- |
| C1 | `PYTEST_DEBUG_TEMPROOT=<worktree>/.venv/tmp`；`<worktree>/.venv/Scripts/python.exe -m pytest -q -rxXs` | exit 0，**2015 passed in 39.24s**；沒有 skipped／xfailed／xpassed 摘要 |
| C2 | `git diff --numstat e1ef580..0799682 -- src/ tests/` | `12 3 adoption.py`、`116 0 tests/test_routing_engine.py`；tests diff 的刪除行數 0 |
| C3 | `git diff --exit-code e1ef580..0799682 --` 傳輸層、client、`source.py`、`store.py`、`snapshot.py` 與兩個既有測試檔 | 空 diff，exit 0 |
| C4 | `git show <rev>:src/moto_copilot/routing/adoption.py` 中的 `_real`（`7cb4b0c`、`e1ef580`、`0799682`） | 三者逐字相同 |
| P1 | stdin 探測：三個版本的 `adoption.py` × （狀態 503／200）×（有／無訊號）×（`summary.length`、`summary.time`、edge `length` = `10**400`），共 12 組輸入 | 第 2.2 節 (4) 的表；`_parse_json` 把 401 位數字面值解析為 `int` |
| P2 | stdin 探測，經 `get_route`：A. R1-F1 的三類反例與四個相關案例；B. R2-F1 四例；C. 同值在 HTTP 200 的四例 | A 全部符合契約（第 2.1 節）；B、C 八例都是未捕捉的 `OverflowError`，`stored=[]` |
| P3 | stdin 探測：有訊號的回應配其他無效長度值，以及整數界線值，route／trace × 503／200 | 第 2.2 節 (1)、(3) |
| P4 | stdin 探測：逐欄位代換，3 828 例 | 第 2.2 節 (6) |
| C5 | 結束時 `git status --porcelain`（主 checkout、worktree） | 主 checkout 空；worktree 只有 R2 派工留下的 `?? …/issue-16-c1-r2.md` |

非產品的失敗，如實記錄：P1 第一次執行時，本 review 在匯入測試模組之前就把 `socket.socket` 換成函式，使標準函式庫 `ssl` 的匯入失敗（`TypeError: function() argument 'code' must be code, not str`）；改為匯入後再封鎖 socket，重跑得到上表結果。這是 harness 的錯誤，不是產品 finding。

未重跑的他人證據：R2 的「195 組 200 outcome 一致」比對、R2 的記憶體 pytest plugin、Executor 的 37 次突變。本 review 以 C2～C4、P1（200 路徑三版本結果一致）與 C1 取代前兩項；突變見 NV-MUTATION。

## 4. NOT VERIFIED 與 required authority

| ID | 未驗證事項／原因 | Required authority／owner |
| --- | --- | --- |
| NV-1 | 真實 Valhalla 伺服器的行為，含它是否可能回傳超出浮點範圍的整數長度或時間、非 200 回應本文的實際形狀：**NOT VERIFIED／NOT RUN**。派工禁止網路請求；CL-R1-1、CL-R1-25 第 2.7 節也排除 | acceptor；之後獲授權的整合 work item |
| NV-PRIVATE | 真實 GPX、保留行程與私有位置資料下的行為：**NOT VERIFIED**。沒有 RB-7 的路徑授權，沒有嘗試取得；本次判斷也不需要 | acceptor |
| NV-BIND | 本 review 的全程 (model, effort)：**NOT VERIFIED by Reviewer**，由派工者依 Bindings 第 3.6 節核對。Executor 與 Primary 的 model 是引用 run record 的核對紀錄，本 review 沒有讀 transcript 或 rollout | 派工者／Orchestrator |
| NV-MUTATION | Worklog 第 11.5 節的突變檢查沒有重跑（本 review 不得修改來源） | Executor 的 self-verification 紀錄 |
| NV-VERSION | 只在 Python 3.11.2 執行。`math.isfinite` 對過大的 `int` 拋 `OverflowError` 在其他版本的行為沒有實測 | — |

範圍界限：本 review 只判斷 R2 後剩餘的 blocking finding，沒有重做 R1 的逐項 AC 核對、H-1／H-2 的最低核對，也沒有作 Spec Integration Audit、phase acceptance 或 Ticket completion 的判斷。TI-C16-2、TI-C16-3、RV-12～RV-14 沿用 DA 的 disposition，本 review 沒有觸及。

## 5. Routing

- R1-F1：已解決，不需要後續 authority。
- R2-F1：有效且未解決。依治理 §4.4、§4.5，Alternate Review 後仍未解的問題進 **Final Adjudication**；本 review 不作裁決、不指定 disposition、不授權新 cycle。供裁決使用的事實：這項 finding 主張並經本 review 證實違反 accepted contract 條款（R1-4 範圍 (f)、CL-R1-8、SPEC-001 4.13），所在路徑屬 H-4；root cause 涵蓋 200 與非 200 兩條路徑（第 2.2 節 (4)）。
- Design Authority：本 review 判斷不需要（第 2.2 節 (3)）。沒有 capability escalation（Bindings 第 3.2 節：E-AR 不採用）；證據與分析足以判定兩項 finding。

VERDICT: UNRESOLVED (R2-F1)
