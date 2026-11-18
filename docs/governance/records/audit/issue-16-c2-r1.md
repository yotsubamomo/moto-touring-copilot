# Audit record — Issue #16（SPEC-R1 R1-4 `routing`）cycle 2 R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37a`）→ SPEC-R1 v1（`derivation-spec-r1.md` 第 4 節 DD-R1-2、CL-R1-1、CL-R1-5～CL-R1-9；第 5 節 R1-4 列與 E-1～E-6）＋ `decision-20261118-issue13-c131.md`（CL-R1-13）、`decision-20261118-issue14-c141.md`（CL-R1-14、17、19）、`decision-20261118-issue14-qalt1.md`（CL-R1-20、21）、`decision-20261118-issue15-c151.md`（CL-R1-24）、`decision-20261118-issue16-c161.md`（CL-R1-25～27）→ GitHub Issue #16。Issue 原文：派工所附 scratchpad 檔 `issue-16-body.md`，本 reviewer 實測 SHA-256 `105fdc981b1087b60b419690168d205064853a1a41ccde4a6cb092b6ffa8ede1`，與派工、run record 第 4 節相同 |
| 授權 | Final Adjudication ruling `ruling-20261118-issue16-c1.md`（R2-F1：targeted rework，授權 cycle 2，自 R1 起） |
| 受審 subject | worktree `C:/Users/yotsu/AppData/Local/Temp/cl16c2r1`，detached HEAD **`fb6210dbceab4b04651380d8bc23ee82d4896484`**（branch `oc1-run2-b1-ui0-r1-routing` 的同一 commit）；BASE **`bc7024b`**。實作 commits `7cb4b0c`、`f6810d2`、`65aa00c`（cycle 1）與 `022f629`（cycle 2 rework）；其餘 commits 只動 `docs/governance/records/**`（`git diff --name-only 022f629..fb6210d` 只有 run record 與 worklog）。Cycle 1 最終 subject `0799682` |
| Audit 種類 | Ticket R1，**cycle 2**，完整 independent audit（治理 §4.4）。**不是** Spec Integration Audit（SPEC-R1 有四張 Ticket，不適用單 Ticket fast path） |
| 角色 | `primary_reviewer`（`gov-primary-reviewer`，Claude path）。依 run record 事件 98、99：Codex 當次回報 usage limit，依 Profile §6 條件 4 與 Bindings 第 3.1 節 R-PR 替代為 Opus 5.5／`high`；事件 99 記 `diversity_lost` |
| 高風險類別 | H-1、H-2、H-4（R1-4 列；`decision-20261117-high-risk-categories.md` 第 5 節的最低核對範圍逐項見第 4 節） |

## 1. Assurance

### (a) Context independence（治理 §2.3 四項 properties）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Fresh、非 fork 的 `gov-primary-reviewer` subagent，沒有繼承 Executor、cycle 1 各 reviewer、FA 或 Orchestrator 的對話。派工內容是路徑、識別與範圍；其中對 cycle 1 結果的描述、worklog、三份 audit record 與 ruling 的結論都當成待驗證主張，本 record 採用的事實都另行讀原始檔、git 歷史或重現 |
| Verifiable binding | 本 reviewer 的 runtime model 是 `claude-opus-5-5`；effort 依 definition 為 `high`，本 reviewer 無法自證全部 assistant 訊息的 (model, effort)，依 Bindings 第 3.6 節由派工者在採用本 record 前核對 transcript 並記入 run record |
| Autonomous access | 自行在 worktree 讀取原始碼、測試、契約與紀錄（只限 worktree 內追蹤中的檔案與 scratchpad 的 Issue 檔），以 `git diff`／`git show`／`git log` 讀歷史，自行執行 pytest 與 stdin 的記憶體內探測（合成值）。沒有讀取、列出或搜尋 `data/`；沒有讀 `.env` 或憑證；沒有讀取或執行 `experiments/`；沒有使用 `git status --ignored`；沒有網路請求（探測在匯入後把 `socket.socket`、`create_connection`、`getaddrinfo` 換成拒絕函式；pytest 沿用測試檔的 autouse 封鎖） |
| Self-written record | 本檔由本 reviewer 以 Write 寫入主 checkout，是本次唯一新建的檔案。沒有修改、stage 或 commit 任何東西。Worktree 的 `git status --short` 在開始時、每次測試與探測之後都為空；探測的暫存目錄建在 worktree 的 `.venv/tmp` 之下，結束時已刪除 |

### (b) Model diversity

| 角色 | 實際 model（證據） |
| --- | --- |
| Executor | `claude-opus-5-5`／`high`（run record 事件 89、91、93、97，agentId `a1e2cfa52290d496f`；派工者的核對，本 reviewer 沒有獨立讀 transcript） |
| Primary Reviewer（本 record） | `claude-opus-5-5`（runtime 自述；effort 由派工者核對） |

**無 model diversity**：Executor 與本 review 同為 `claude-opus-5-5`。`diversity_lost` 已記於 run record 事件 99。Bindings 第 5 節沒有宣告 diversity 關係；本 record 不主張 diversity，diversity 不影響 independence 的判定。

## 2. Findings

### C2R1-F1 — 路線回應的 shape 解碼出超出浮點範圍的值時，`get_route` 拋出未捕捉的 `OverflowError`（Medium，**blocking**）

**證據。**
- `src/moto_copilot/routing/valhalla.py:218-233`：`decode_polyline6` 以無上限的整數累加每個值（`result |= (b & 0x1F) << shift`），再以 `point = (lat / 1e6, lon / 1e6)`（`:233`）轉成浮點數；`int / float` 對絕對值超出浮點範圍的整數拋 `OverflowError`（不是 `ValueError`，也不是 `PolylineError`）。範圍檢查 `:234` 在轉換之後，來不及攔下。
- `src/moto_copilot/routing/adoption.py:241-245`：`_route_facts` 只捕捉 `PolylineError`。`_route_facts` 在 HTTP 200（`:388`）與非 200 而有 `trip`（`:385`，自 `65aa00c`）兩條路徑都會執行。`git diff 7cb4b0c fb6210d -- valhalla.py` 只有模組說明的改動：`decode_polyline6` 自 `7cb4b0c` 未變。
- 重現（stdin、合成值、經真正的 `get_route` 來回行程；shape 是 212 個字元的合法 JSON 字串 `"~"*210 + "??"`，只替換去程 `trip.legs[0].shape`，其餘回應正常）：

| 去程回應 | 結果 | 請求序列 | 快照 |
| --- | --- | --- | --- |
| 200，`has_highway: false` | 未捕捉 `OverflowError: int too large to convert to float` | `route` | 無 |
| 200，`has_highway: true` | 同上（國道訊號遺失） | `route` | 無 |
| 503，`has_highway: false`／`true` | 同上 | `route` | 無 |
| 對照：短的壞 shape `"~~~"`，`has_highway: true` | `highway_in_route`（`has_highway`、`response_malformed`） | `route, route, trace_attributes` | 無 |
| 去程 200 `has_highway: true`，**回程** shape 同上 | 未捕捉 `OverflowError`；去程已有的國道訊號也拿不到 `highway_in_route` | `route, trace_attributes, route` | 無 |

**契約依據。** R1-4 範圍 (f)（共用介面回傳「採用的路線」或「路線錯誤代碼」）；CL-R1-8（引擎有回應時先檢查所有可取得的國道訊號再決定代碼；兩個方向都送出並檢查）；SPEC-001 4.13（`highway_in_route` 優先於 `routing_unavailable`）、7.11 第 5 項；R1-4「另加」AC「國道訊號與其他不採用的原因同時出現時是 `highway_in_route`」；H-4 最低核對範圍（缺漏、失敗的每條路徑都是明確錯誤）。`ruling-20261118-issue16-c1.md` 第 2.1 節已明定：可以傳出例外的情形不包含引擎回應的內容。

**Severity 與 blocking。** Medium／blocking，理由與 R2-F1 相同：沒有 fail-open 的證據（沒有採用、沒有存檔），但它直接違反上列 accepted 條款，而且已有國道訊號時拿不到 `highway_in_route`、回程沒有送出。屬 H-4（判定第 4 項）。

**與 R2-F1 root cause 的關係（ruling 第 3.3 節要求 Reviewer 判斷）。** 本 reviewer 判斷**不是**同一個 root cause：ruling 把 R2-F1 的 root cause 界定為「`adoption.py` 對引擎回應數值欄位（`trip.summary.length`、`trip.summary.time`、`edges[n].length`）的讀取與檢查」；本 finding 是 `valhalla.py` 的 polyline 解碼對字串欄位 `shape` 的處理，不經 `_real`，R2-F1 的 rework 也沒有觸及它（ruling 的封閉清單不含 `valhalla.py`）。兩者機制同類（無上限的整數轉成浮點數），所以如實記下；R2-F1 本身已解決（第 3 節）。對此判斷有爭議時由 Final Adjudicator 決定。

**Required fix（結果，不是做法）。** 對任何可由 `_parse_json` 解析出的本文，`shape` 不論內容為何，`evaluate_direction`／`get_route` 都不拋未捕捉例外：解不出範圍內點位的 shape（含解出超出浮點範圍的值）與其他壞 shape 同樣記為讀不到（`response_malformed`，國道檢查無法驗證）；同一回應其他可讀的國道訊號照樣收集；另一方向照樣送出並檢查；非 200 仍保留 `engine_error`、永不採用、不存快照、不以錯誤回應的 shape 送查詢。回歸證據：200 與非 200 × 有、無國道訊號 × 去程與回程的合成案例（含上表最後一列），以及至少一個會被抓到的突變（恢復目前的行為）。Owner：#16 Executor。

### C2R1-F2 — 引擎回應中不是合法 Unicode 的字串（孤立 surrogate）使採用路徑在組成快照時拋出未捕捉的 `SnapshotValidationError`（Medium，**blocking**）

**證據。**
- `valhalla.py:155-159`：`_parse_json` 接受 JSON 跳脫 `\ud800` 這類孤立 surrogate，解析成 Python `str`。
- `adoption.py:157-172`：轉向的道路名稱只檢查是 `str`，原樣放進 `road_names`；`source.py:250-252`：狀態回應的 `version` 只檢查是非空 `str`。
- `canonical.py:86-91`：`canonical_bytes` 以 UTF-8 編碼時遇到 surrogate 拋 `CanonicalError`；`snapshot.py:320-323`：`build_snapshot` 轉成 `SnapshotValidationError`；`source.py:179-187`：`get_route` 沒有處理它。
- 重現（stdin、合成值；本文以 ASCII JSON 送出，其中一個字串是 `\ud800` 或 `\udfff` 跳脫；其他回應正常）：

| 情形 | 結果 | 請求序列 | 快照 |
| --- | --- | --- | --- |
| 去程轉向名稱含孤立 surrogate，其餘全部通過 | 未捕捉 `SnapshotValidationError` | `route, trace_attributes, route, trace_attributes, status` | 無 |
| 回程轉向名稱同上 | 同上 | 同上 | 無 |
| 單向行程同上 | 同上 | — | 無 |
| 狀態回應的 `version` 含孤立 surrogate | 同上 | 同上 | 無 |
| 對照：同一名稱而 `has_highway: true` | `highway_in_route`（沒有例外） | `route, trace_attributes, route, trace_attributes` | 無 |
| 對照：同一名稱而路線回應有警告 | `routing_unavailable`（沒有例外） | 同上 | 無 |
| 對照：道路屬性回應的名稱含孤立 surrogate（不寫入快照） | 採用並存檔一個快照 | 含 `status` | 1 |

**契約依據。** R1-4 範圍 (f)；`ruling-20261118-issue16-c1.md` 第 2.1 節列出的可傳出例外（嚴格模式停止、`SnapshotIntegrityError`、CL-R1-21 的 `put` 與 `SnapshotStore` 建構錯誤、CL-R1-24 的呼叫端與目標 GPX 錯誤、凍結清單未搭配 Snapshot Mode 的 `ValueError`）不含 `build_snapshot` 因引擎回應內容而失敗的情形；CL-R1-6（`road_names` 取自轉向名稱）；DD-R1-2／CL-R1-26（`engine_version` 沒有回報時是 `unreported`）；H-4。

**Severity 與 blocking。** Medium／blocking。沒有 fail-open（沒有存檔、沒有回傳路線，國道訊號的優先順序不受影響，所以比 C2R1-F1 輕），但共用介面對一個合法可解析的引擎回應既不回傳路線也不回傳代碼，違反範圍 (f)；依 ruling 第 3.1 節對同類條款的適用，不能以 non-blocking 帶過。屬 H-4。不是 R2-F1 的 root cause（不同欄位、不同機制）。

**Required fix（結果）。** 對任何可由 `_parse_json` 解析出的本文，`get_route` 不因引擎回應的字串內容拋出未捕捉例外：要寫入快照的道路名稱不是合法 Unicode 時，該方向記為讀不到、不採用、不存快照（有國道訊號時仍是 `highway_in_route`）；狀態回應的版本不是合法 Unicode 時，結果是採用的路線或路線錯誤代碼之一。版本的處置若 Executor 認為需要決定契約沒有涵蓋的語義（例如記為 `unreported` 或使路線不採用），停止並依治理 §2.4 route 至 Design Authority。回歸證據：去程、回程、單向的名稱與狀態版本各至少一例，以及一個會被抓到的突變。Owner：#16 Executor。

**修正的檔案範圍（routing 提示，不是 finding）。** C2R1-F1、F2 的修正可能需要 `valhalla.py`、`source.py`，不在 ruling 第 3.2 節為 R2-F1 rework 定的封閉清單內。本 reviewer 讀治理 §4.4：cycle 2 R1 的 targeted correction 以本 record 的 blocking findings 為範圍；那份清單是否仍約束本 cycle 的 correction，由 Orchestrator 依 run 的派工處理，有疑義時交 Final Adjudicator。

### C2R1-F3 — `ssl.create_default_context()` 依環境變數 `SSLKEYLOGFILE` 寫出 TLS session keys（Low，non-blocking；routing signal → Design Authority）

**證據。** `http_transport.py:76` 依 CL-R1-25 第 2 項 (d) 呼叫 `ssl.create_default_context()`。Python 3.11.2 的原始碼（`inspect.getsource(ssl.create_default_context)`）讀 `SSLKEYLOGFILE`：有設定時把 TLS session keys 寫到該檔，所有平台皆然（含 Windows）。本機目前沒有設定（`keylog_filename` 為 `None`）。它不改變連線的主機與埠，也不關閉驗證，所以不違反 H-1「端點不可被轉向」；但它使一個環境變數能影響傳輸層（可解密被截取的請求內容：公開地標座標與 User-Agent）。

**判斷。** CL-R1-25 第 2 項 (b) 寫「不讀任何環境變數」，同時第 2 項 (d) 指定使用 `ssl.create_default_context()`；DA 在 (d) 已把 `SSL_CERT_FILE` 記為「觀測，不是要求」，但沒有提到 `SSLKEYLOGFILE`。這是契約語義的不足，不是對實作的 blocking finding（治理 §4.2）。**Required authority：Design Authority**——決定是否要求傳輸層在建立 context 之後把 `keylog_filename` 設為 `None`，或與 `SSL_CERT_FILE` 同樣記為觀測。Disposition：tracked，owner Design Authority；不延長本 cycle。

### C2R1-F4 — 快照的 shape 解碼只把 `PolylineError` 轉成 `SnapshotIntegrityError`（Low，non-blocking）

**證據。** `source.py:268-271`：`_from_snapshot` 只捕捉 `PolylineError`。名稱、內容雜湊都一致、但 shape 會解出超出浮點範圍值的快照檔（需要有人刻意製作並重算雜湊；產品只存解碼成功的 shape），在選取後會拋 `OverflowError` 而不是 CL-R1-17 的 `SnapshotIntegrityError`。仍是停止（fail closed），只是例外種類不同。

**Disposition。** Non-blocking。C2R1-F1 的修正若放在 `decode_polyline6`（使它對這類值拋 `PolylineError`），本項隨之消失；放在其他地方時，Executor 在 worklog 記下本項的狀態即可。Owner：#16 Executor（隨 C2R1-F1 處理）；不另立 work item。

## 3. Ruling 的 rework 範圍與 cycle 1 findings 的核對

| 項目（ruling 第 3.2 節） | 證據 | 結論 |
| --- | --- | --- |
| Root cause `adoption.py` 的 `_real` | `adoption.py:119-131`：非 `int`／`float` 或 `bool` → `False`；`math.isfinite` 拋 `OverflowError` → `False`。呼叫處 `:200`、`:204`（`summary.length`、`summary.time`）、`:289`（edge `length`）沒有改 | 已修正 |
| 結果 1：不拋未捕捉例外（200 與非 200，路線與道路屬性回應） | `test_r2_f1_a_route_summary_number_beyond_the_float_range`（72 例：`length`、`time` × 200、302、400、429、500、503 × 有無訊號 × `2**1024`、`10**400`、`-(10**400)`）；`test_r2_f1_a_road_attribute_edge_length_beyond_the_float_range`（36 例）；回程 9 例；`evaluate_direction` 6 例；全部 PASS | 成立 |
| 結果 2：保守拒收；代碼依訊號；非 200 保留 `engine_error`／`trace_failed` | 同上測試斷言代碼、`response_malformed`／`engine_error`／`trace_failed`、`assert_no_route`、沒有快照檔 | 成立 |
| 結果 3：訊號收集與兩方向檢查不中斷 | 同上測試斷言請求序列（200：`route, trace_attributes, route, trace_attributes`；非 200：`route, route, trace_attributes`）與 `has_highway`／`motorway_edge` 的 reasons | 成立 |
| 結果 4：其他行為不變（`2**1023`、其他無效值、R1-F1） | `test_r2_f1_the_largest_float_range_int_keeps_its_earlier_result`、`test_r2_f1_other_invalid_lengths_keep_their_results`；`git diff --numstat 0799682..fb6210d -- src tests`：`adoption.py` 15／2、`tests/test_routing_engine.py` 118／0（沒有刪改既有測試）；`test_r1_f1_*` 保留並通過 | 成立 |
| 突變（closure 證據第 4 項） | 本 reviewer 在記憶體內把 `adoption._real` 換回 cycle 1 的寫法（`isinstance(...) and not bool and math.isfinite(value)`），以 `pytest.main` 只跑 `-k r2_f1`：**123 failed, 10 passed**，與 worklog 第 12.6 節 C2a 的 123 相同。沒有修改任何檔案 | 成立 |
| 陳述更正（closure 證據第 6 項） | worklog 第 11.2 節 D-16-26 與第 11.5 節 H-4 都標為「已被第 12 節取代」並寫明對 `65aa00c` 不成立的原因；第 12.6 節 H-4 明寫只涵蓋三個欄位、不宣稱窮舉；`adoption.py` 模組說明 `:18-20` 已更新 | 成立 |
| Commit（closure 證據第 7 項） | `022f629` 只含 `adoption.py`、`tests/test_routing_engine.py`，message 註明 R2-F1 與 ruling；worklog 另以 record-only commits（`197d664`、`925df23`、`2ce329b`） | 成立 |
| **R2-F1** | 上列全部成立 | **已解決，沒有再出現** |
| **R1-F1**（非 200 回應在讀取國道訊號前離開） | `adoption.py:382-386`、`:400-405` 在決定代碼前收集非 200 本文的訊號；`test_r1_f1_*` 全部通過 | **沒有再出現** |
| 新 finding 是否屬 R2-F1 root cause | 見 C2R1-F1、F2 的說明 | 否（本 reviewer 判斷） |

## 4. 完整 audit：範圍、AC 與 clarifications

### 4.1 測試與 gate

| 指令（worktree，`PYTEST_DEBUG_TEMPROOT=C:/Users/yotsu/AppData/Local/Temp/cl16c2r1/.venv/tmp`，`.venv/Scripts/python.exe`，Python 3.11.2） | 結果 |
| --- | --- |
| `-m pytest -q` | `2148 passed in 30.76s`，exit 0 |
| `-m pytest -q -rxX` | `2148 passed in 35.11s`，exit 0；沒有 xfailed／xpassed 摘要 |
| `grep -rnE "mark\.(xfail\|skip\|skipif)\|pytest\.(skip\|xfail\|importorskip)\|__test__" tests/` | 0 筆 |
| `git status --short`（測試、探測前後） | 空 |
| `git ls-files \| grep -iE "(^\|/)\.env\|\.gpx$\|\.fit$\|\.key$\|^data/raw/\|^data/private/\|^data/bmw/"` | 0 筆 |

E-1 成立（全數通過，與 worklog 第 12.3 節的 2148 相同）；但 C2R1-F1、F2 表示既有測試不涵蓋兩條未捕捉例外的路徑。

### 4.2 範圍 (a)～(f)

| 範圍 | 證據 | 結論 |
| --- | --- | --- |
| (a) client 與傳輸層（CL-R1-5、9、25） | `valhalla.py`：端點常數、`_ENDPOINT` 檢查、每次呼叫一個請求、固定 routing params、trace 只送引擎自己的 shape；`http_transport.py`：只用 `http.client`＋`ssl`、URL 再檢查、header 封閉清單、固定逾時 30 s、失敗轉 `TransportError` `from None`；T-1～T-10（`tests/test_routing_transport.py`）通過 | PASS（真實連線 NOT RUN）；C2R1-F3 為 DA routing |
| (b) 採用檢查：警告、四項國道訊號、method、偏移與順序 | `adoption.py:175-359`；S30、S39、S40、S68～S70、CL-R1-7、CL-R1-19、CL-R1-27 的測試 | 檢查邏輯 PASS；**C2R1-F1**（壞 shape 的一類值使檢查以例外中止） |
| (c) 錯誤代碼（CL-R1-8） | `decide_code`（`adoption.py:449-459`）；`_ask_engine`（`source.py:219-230`）只在完全無法連線時不送另一方向 | 一般情形 PASS；**C2R1-F1** 違反 |
| (d) RouteLeg 與存檔（CL-R1-6、DD-R1-2、CL-R1-26） | `adoption.py:425-446`；`source.py:178-189`、`:237-260`；`test_cl_r1_6_*`、`test_dd_r1_2_*` | 一般情形 PASS；**C2R1-F2** |
| (e) 取得順序（7.11 第 3 項） | `source.py:155-174`：Snapshot Mode 只經 `select_strict`／`select_snapshot_mode`；一般模式先 `find_reusable`；引擎失敗回代碼，不改用過期快照；S17、S35、S15 測試 | PASS |
| (f) 共用介面 | `get_route` 與 `_from_snapshot`、`_target_gpx`；CL-R1-24 測試 | 形狀 PASS；**C2R1-F1、F2** 使部分合法回應既不回傳路線也不回傳代碼 |

### 4.3 AC（R1-4 列；SPEC-001 第 9 節 S 編號）

本 reviewer 逐一確認 worklog 第 6 節 E-2 表所列的測試存在於 `tests/test_routing_engine.py`、斷言內容與 AC 對應，並在 4.1 的執行中通過。

| AC | 主要測試 | 結論 |
| --- | --- | --- |
| S15 路線部分 | `test_s35_s15_engine_failure_with_only_an_expired_snapshot_is_routing_unavailable`、`test_s15_a_snapshot_checked_with_another_method_is_not_used_when_the_engine_fails`、`test_s35_s38_one_direction_failing_stores_nothing_and_has_no_route` | PASS |
| S17 | `test_s17_snapshot_mode_does_not_call_the_engine`、`test_s17_snapshot_mode_without_a_snapshot_returns_snapshot_missing`、strict mode 兩項 | PASS |
| S23 行為部分 | `test_s23_each_direction_has_its_own_request_shape_and_fetched_at_and_return_is_not_reversed` | PASS |
| S24 第一句 | `test_s24_a_fail_in_either_direction_stores_nothing_and_is_highway_in_route` | PASS（`leg_length_diff_flag` 排除） |
| S30 | `test_s30_route_request_is_motorcycle_with_use_highways_0_and_no_exclusion_or_elevation`、`test_s30_a_reply_with_any_warning_is_routing_unavailable` | PASS |
| S35 引擎部分 | `test_s35_*` 四項 | PASS |
| S38 路線部分 | `test_s23_*`、`test_s35_s38_*[return]` | PASS；回程 shape 的 C2R1-F1 情形不符「回程的請求失敗時是路線錯誤」 |
| S39 合成部分 | `test_s39_*` 四項、`test_maneuver_names_and_highway_flags_are_freeway_signals` | PASS；「五條參考路線」排除，NOT RUN |
| S40 合成部分 | `test_s40_an_end_offset_of_several_kilometres_is_rejected`、`test_s40_s68_*` | PASS；參考路線與詞彙表部分排除，NOT RUN |
| S68、S69、S70 | `test_s40_s68_*`、`test_s69_*`、`test_s70_*` | PASS |
| 另加：沒有回報 `has_highway`、2% 長度差 → `routing_unavailable` 且無 `freeway_check` | `test_has_highway_not_reported_*`、`test_the_road_attribute_length_must_be_within_2_percent`、`test_the_2_percent_check_is_exact_at_the_boundary`、`test_a_failed_road_attribute_query_gives_no_freeway_check_value` | PASS |
| 另加：國道訊號與其他原因同時出現 → `highway_in_route` | `test_a_freeway_signal_with_another_reason_is_highway_in_route` 等三項、`test_r1_f1_*`、`test_r2_f1_*` | 既測情形 PASS；**C2R1-F1 的情形 FAIL** |
| 另加：中間位置沿線里程相等時拒收 | `test_cl_r1_7_vias_with_equal_along_shape_distance_are_out_of_order` | PASS |
| 另加：User-Agent 與內容不含個人識別資訊 | `test_user_agent_and_request_content_hold_no_personal_information`、T-6 | PASS |
| 另加：端點不受環境變數影響 | `test_h1_the_endpoint_is_not_affected_by_env_variables`、T-2 | PASS |

### 4.4 Clarifications

| 條款 | 核對 | 結論 |
| --- | --- | --- |
| CL-R1-1 | 測試只用 `at(x, y)` 在 0°N、0°E 附近的合成點；`git diff bc7024b..fb6210d` 新增行中沒有台灣範圍的高精度經緯度（0 筆），高精度數字 5 筆都是合成值（`0.0123456789` 等） | PASS |
| CL-R1-5 | `test_cl_r1_5_*`、`test_no_request_is_retried_after_an_error_reply`、unreachable 兩項 | PASS |
| CL-R1-6、CL-R1-7、CL-R1-19 | 對應測試；`offset_reasons` 以原值判定（`adoption.py:348-359`） | PASS |
| CL-R1-8 | 見範圍 (c) | **C2R1-F1** |
| CL-R1-9 | 端點常數、通用 UA `route-client/1.0`；`grep -rn "environ\|getenv\|logging\|print(" src/moto_copilot/routing/` 只命中 `place_fingerprint(` | PASS |
| CL-R1-13 | `test_cl_r1_13_the_ids_on_the_engine_path_follow_the_contract_patterns` | PASS |
| CL-R1-14 | 未修改 `canonical.py`；存檔經 `build_snapshot` | PASS |
| CL-R1-17、20、21 | `source.py` 的 `except` 只有 `TransportError`（`:247`）、`fromtimestamp` 錯誤（`:258`）與快照 shape 的 `PolylineError`→`SnapshotIntegrityError`（`:270`）；沒有攔下 `SnapshotIntegrityError`、`SnapshotStoreError`、`SnapshotConflictError`、`StrictModeStop`；CL-R1-21 (i)(ii)(iii) 測試通過 | PASS（C2R1-F4 Low） |
| CL-R1-24 | `test_cl_r1_24_*` 四項 | PASS |
| CL-R1-25 | 第 2.3 節第 1～6 項逐項讀 `http_transport.py`；`tests/test_routing_store.py` 的 diff 只改 DA 准許的一個函式（遞迴掃描、單一豁免、`http_transport.py` 必須存在、其他模組不得引用、`environ`／`getenv` 照舊禁止） | PASS（C2R1-F3 為 DA routing） |
| CL-R1-26、DD-R1-2 | `_engine_info`；`test_dd_r1_2_*` | PASS；C2R1-F2 的版本情形 |
| CL-R1-27 | `_trace_facts:259-263`；`test_cl_r1_27_*` 五項 | PASS |

### 4.5 E-1～E-6

| 項目 | 結論 |
| --- | --- |
| E-1 | 成立（4.1） |
| E-2 | Worklog 第 6、10.5、11.4、12.4 節逐條列出；本 reviewer 抽核測試名稱與斷言相符。C2R1-F1、F2 修正後需補列 |
| E-3 | 成立（4.4 CL-R1-1；worklog 第 6、12.4 節的來源說明與 diff 一致） |
| E-4 | 成立：`FakeEngine` 與 `HTTPSConnection` 替身；兩個測試檔都有 autouse 的 socket 封鎖；T-2 的子直譯器以替身取代連線 |
| E-5 | 成立：`tests/test_routing_store.py` 的修改依 c161 第 2.4 節第 2 列；cycle 2 沒有刪改既有測試 |
| E-6 | Worklog 第 6、10.6、11.5、12.6 節有 H-1、H-2、H-4 的 self-verification，第 12.6 節如實限定範圍；H-4 因 C2R1-F1、F2 不能整體記 PASS |

### 4.6 高風險類別的最低核對範圍（高風險 decision 第 5 節）

- **H-1**：diff 與新檔沒有憑證值（`git diff bc7024b..fb6210d` 新增行對 `sk-ant`、`api_key =`、`authorization:` 0 筆）；沒有 log；例外訊息是固定文字。端點不可被轉向：端點是常數或明確傳入且以 `_ENDPOINT` 檢查；傳輸層再以 `_URL` fullmatch 檢查並只連到該主機與埠（`http_transport.py:45-59`、`:80`）；不跟隨轉址（`http.client` 沒有轉址處理，每次呼叫一個連線一個請求，T-1）；不用代理（沒有 `set_tunnel`；本 reviewer 以 `inspect.getsource(http.client)` 確認不含 `environ`、`getproxies`；T-2 在子直譯器設定 13 個代理與端點變數）；不讀環境變數（靜態測試與 grep）；TLS 驗證不得關閉（`ssl.create_default_context()`：`check_hostname=True`、`verify_mode=2`，沒有關閉參數，T-3）。付費呼叫：不適用（公開伺服器、沒有憑證）。`git ls-files` 不含 `.env`、`*.key`。結論：**PASS**；附 C2R1-F3（Low，DA routing）。
- **H-2**：`git ls-files` 不含 release gate 所列路徑；diff、fixture 與紀錄中的座標都是合成值（4.4 CL-R1-1）；送往第三方的內容：路線請求只有位置的 `lat`、`lon`、`type` 與固定參數，道路屬性查詢只有引擎自己的 shape，狀態請求是空物件，User-Agent 通用（T-6、`test_user_agent_*`）；錯誤與 traceback 不含合成座標（T-5、`test_bad_positions_are_refused_without_the_coordinates_in_the_message`）。本次重現的 `OverflowError`、`SnapshotValidationError` 訊息都是固定文字，不含座標或本文。送出的位置是否為公開地標、隱私裁切與錨點代換屬 G-RREQ（TI-C16-3），不在本 Ticket。結論：**PASS**（在本 Ticket 的範圍內）；真實資料下的行為 NOT VERIFIED（NV-PRIVATE）。
- **H-4**：國道檢查在訊號矛盾或無法驗證時不採用（S39、CL-R1-27、`has_highway` 未回報、2%）；偏移與順序 fail closed（S40、S68～S70、CL-R1-7、CL-R1-19 的 200.04 m）；警告不採用（S30）；CL-R1-8 的優先順序在已測情形成立（含 R1-F1、R2-F1 的回歸）；沒有攔下 `SnapshotIntegrityError`；非 200 與 3xx 永不採用。沒有 fail-open 的證據。但「失敗的每條路徑都是明確錯誤」不成立：**C2R1-F1、C2R1-F2**。結論：**FAIL（blocking）**。

## 5. NOT VERIFIED

| # | 項目 | 理由 | Required authority |
| --- | --- | --- | --- |
| NV-1 | 真實 Valhalla 伺服器的連線、TLS、轉址、回應形狀，以及它是否可能回傳本 record 的兩類內容；S39／S40 的參考路線與詞彙表 | **NOT RUN**：派工禁止網路請求；CL-R1-1、c161 第 2.7 節排除 | acceptor；之後獲授權的整合 work item |
| NV-PRIVATE | 真實 GPX、保留行程與私有位置資料下的行為 | 本 run 沒有 RB-7 的路徑授權，沒有嘗試取得 | acceptor |
| NV-MUT | Worklog 第 10.7、11.5、12.6 節的 39 個突變（`mutate16b.py`） | 不得修改來源；只以記憶體內替換重做了 C2a 的等價突變（123 failed），其餘沒有重跑 | — |
| NV-PY | Python 3.11.2 以外的版本 | 只有這個直譯器 | — |
| NV-BIND | Executor 的 transcript 與本 review 的 effort | 本 reviewer 沒有讀 transcript；第 1 (b) 節引用 run record 的派工者核對 | 派工者（Bindings 第 3.6 節） |
| NV-12.5 | Worklog 第 12.5 節的 `probe_c2.py`（132 組前後比對） | 腳本不在 repo；本 reviewer 以 `test_r2_f1_other_invalid_lengths_keep_their_results` 與突變結果代替核對 | — |
| — | `experiments/cr01_checks/` 的兩個參考原始碼 | CL-R1-1 允許閱讀，本次判斷不需要，沒有讀 | — |

## 6. Routing 與下一步

- **#16 Executor**（targeted correction，治理 §4.4）：C2R1-F1、C2R1-F2；C2R1-F4 隨 C2R1-F1 處理。之後由 R2（本 cycle）核對。
- **Design Authority**：C2R1-F3（CL-R1-25 第 2 項 (b) 與 (d) 對 `SSLKEYLOGFILE` 的語義）；C2R1-F2 中狀態版本的處置若 Executor 回報需要新語義。
- **Final Adjudicator**：只在 C2R1-F1 是否屬 R2-F1 root cause 的判斷、或 correction 的檔案範圍有爭議時。
- **Acceptor**：不需要（沒有 reserved boundary 的動作，沒有外洩：重現只用合成值，例外訊息不含座標或本文）。

## 7. 執行紀錄

| 指令／動作 | 結果 |
| --- | --- |
| `sha256sum` scratchpad 的 `issue-16-body.md` | `105fdc98…ffa8ede1`，相符 |
| `git rev-parse HEAD`、`git log --oneline bc7024b..fb6210d`、`git diff --stat bc7024b..fb6210d`、`git diff --stat 0799682..fb6210d`、`git show --stat 022f629`、`git diff --name-only 022f629..fb6210d`、`git diff --numstat 0799682..fb6210d -- src tests`、`git diff 7cb4b0c fb6210d -- valhalla.py` | 第 1、3 節所述 |
| 閱讀 | Bindings m3（第 0～7 節）；治理 §2.3、§4.1～§4.7；impl-default v2 §6、§7；ruling 全文；`derivation-spec-r1.md` 第 4、5、6 節；c131 CL-R1-13；c141 第 2.2、5、7.2 節；qalt1 CL-R1-20、21；c151 CL-R1-24；c161 全文；高風險 decision 第 3、5 節；SPEC-001 4.13、4.14、7.11；`routing/` 的 `adoption.py`、`valhalla.py`、`http_transport.py`、`source.py` 全文與 `canonical.py`、`snapshot.py` 相關段；`tests/test_routing_engine.py` 的 helpers 與新測試、`tests/test_routing_transport.py`、`tests/test_routing_store.py` 的 diff；worklog 第 6、11、12 節；cycle 1 三份 audit record 的相關段；run record 事件 89～99 |
| pytest（4.1） | 2148 passed，兩次，exit 0 |
| stdin 探測 1：`decode_polyline6("~"*210+"??")` 與經 `get_route` 的 200／503 × 有無訊號、短壞 shape 對照；`inspect.getsource(ssl.create_default_context)` | C2R1-F1 表；`SSLKEYLOGFILE` 為 `True` |
| stdin 探測 2、3：孤立 surrogate 在去程、回程、單向名稱、狀態版本、道路屬性名稱，以及有訊號與有警告的對照；回程 shape 溢位而去程有訊號 | C2R1-F1、F2 表（第一次執行時探測腳本自己的字串跳脫寫錯而在建構回應時中止，改以 `chr(92)` 組成跳脫後重跑；這是 harness 錯誤，不是產品行為） |
| stdin 探測 4：記憶體內把 `adoption._real` 換回 cycle 1 版本後 `pytest.main(["-q","-p","no:cacheprovider","tests/test_routing_engine.py","-k","r2_f1"])` | 123 failed, 10 passed |
| stdin 探測 5：`inspect.getsource(http.client)` 的 `environ`／`getproxies`；`ssl.create_default_context()` 的屬性 | `False`／`False`；`check_hostname=True`、`verify_mode=2`、`keylog_filename=None` |
| `git status --short`（worktree，各步驟之後） | 空 |

沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有讀取或執行 `experiments/`；沒有使用 `git status --ignored`；沒有網路請求；沒有修改、stage 或 commit 任何檔案；沒有派工任何 subagent。

Verdict: BLOCKING (C2R1-F1, C2R1-F2)
