# Worklog — SPEC-R1 Spec Integration Audit 的 targeted correction（SIA-R1-F1）

| 欄位 | 內容 |
| --- | --- |
| Work item | SPEC-R1 Spec Integration Audit cycle 1 R1（`docs/governance/records/audit/spec-SPEC-R1-c1-r1.md`）的 blocking finding **SIA-R1-F1** 的 targeted correction；OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **Executor 工作完成，待 SIA cycle 1 R2。** 新增的整合測試在 `4cbc71b`；pytest `2244 passed`；contracts CLI exit 0。Closure 由 SIA 的 R2 與 Orchestrator 判定，本 worklog 不宣告 closure |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；派工時的 HEAD `c2cd52d`（`804362d` 之後的 SIA R1 record commit）；implementation（測試）commit **`4cbc71bdc63f63e80a6295ada32b67ce2c5e5e77`**（`4cbc71b`）。worklog 在另一個 record-only commit |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Finding**：SIA-R1-F1（Medium／blocking；`audit/spec-SPEC-R1-c1-r1.md` 第 158 行起；本 Executor 重算 record 的 SHA-256 前 16 碼 `47193632ee493b3d`）。SR1-AC2（`decisions/derivation-spec-r1.md:145`）要求：以合成的引擎回應走一般模式（第一次呼叫引擎並存快照、第二次重用）、Snapshot Mode、嚴格模式，以及以合成 GPX 走目標 GPX 的單向與來回，都經 R1-4 的共用介面；產生的 `route_id`、`snapshot_id`、`checkpoint_id` 樣式通過 R1-1 的契約檢查，`RS-` 的十六進位部分等於 `snapshot_id`。既有測試分別驗證各行為，契約測試用手寫的 ID，沒有測試把 `get_route` 的實際輸出接到契約檢查。
- **Required fix**（record 原文的要點）：可由 pytest 收集的整合測試涵蓋上述各模式；使用 `get_route` 真正回傳的 ID、行程型態、來源與快照參照；驗證首次存檔、重用與 Snapshot／嚴格模式不發引擎請求；GPX 含單向、來回與騎士指定落在兩點之間的折返（passthrough）；以最小合成的契約資料承載對應的 `checkpoint_id`，經 R1-1 的驗證函式（含 checkpoint 前綴、來源參照、RS／SN hex）實質斷言無違反；參數化時每一列都實際走驗證；G-RTE（產生與編號規則）維持排除；需要改變契約語義時交 DA。
- **派工的限制**：只新增測試檔；不修改 `src/`（需要產品修改時停止並回報 `NEEDS_DA`）；本 worklog；測試與 worklog 分開 commit；不 push；不讀 `data/`、不執行 `experiments/`、不讀 `.env`、不連網、只用合成資料。
- 上位：OC-1；SPEC-R1 v1（`derivation-spec-r1.md` 第 6 節 SR1-AC2）；R1-1 的契約 2（`contracts/validate.py` 的 `validate_route_catalog`）；R1-4 的 `get_route`（#16 最終 subject `9cc566a`）；CL-R1-24（目標 GPX 原樣帶出）。

## 2. Executing role and binding reference

- 角色：`executor`（SPEC-R1 整合 rework 的 Executor），由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以訊息派給同一個 `gov-executor` assignment（agentId `a1e2cfa52290d496f`，`#16` 的 Executor）。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Executor 自行觀測（`4cbc71b` 之後、寫本 worklog 之前）：(`claude-opus-5-5`, `high`) 352 則，集合只有一個元素。**這是自我觀測，不是派工者的核對。**
- Bounded assignments：沒有使用；沒有派工任何 subagent。

## 3. Work performed

1. 讀 SIA-R1-F1（record 第 158 行起，含同節的 N1 與 tracked items 表）、`derivation-spec-r1.md` 第 6 節、`contracts/validate.py` 的 `validate_route_catalog` 與 `_route_source_errors`、`contracts/schemas.py` 的契約 2 schema 與 ID 樣式、`tests/test_routing_engine.py` 的合成產生器。
2. 新建 `tests/test_integration_r1.py`（3 個測試函式，6 個案例）。沒有修改 `src/` 或其他測試檔。
3. 自我驗證：新測試、全套 pytest 兩次（`-q`、`-q -rxX`）、contracts CLI、5 個 ID 連結的突變。
4. 依 SA-1 本機 commit `4cbc71b`（只含新測試檔）。沒有 push、沒有碰 GitHub；沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有執行 `experiments/`；沒有網路請求。

## 4. Decisions and assumptions

| # | 決定 | 依據 |
| --- | --- | --- |
| D-SIA-1 | 每一個 `get_route` 結果以 `catalog_for(route)` 轉成最小的契約 2 資料：一筆路線紀錄（`route_id`、`route_source`、`snapshot_id`、`trip_type` 都是 `get_route` 回傳的值；`source_trip_id = null`）、每個方向一個路段（長度＝該方向的里程，`end_lat`／`end_lon`＝該方向最後一點，類別 `C1`）、檢查點 `<route_id>-CP01`、`-CP02`…（起點、來回行程的折返點在第 1 段之後、終點）。這些列只是承載 ID 的**測試資料**，不是產品的路線目錄，也不定義路段切法或檢查點編號（G-RTE 仍排除）；`src/` 沒有修改 | SIA-R1-F1 required fix；`derivation-spec-r1.md` 第 2 節「不屬於本 Spec」 |
| D-SIA-2 | 驗證以 R1-1 的 `validate_route_catalog`（schema 的 ID 樣式、主鍵、檢查點前綴、不變條件 1、2、4、5、`route_id`／`route_source`／`snapshot_id` 一致與 RS／SN hex）斷言 `== []`；另以樣式與前綴的直接斷言補充。一個自我檢查的測試證明這個驗證不是空的：錯誤的 hex、來源與前綴都被回報 | SIA-R1-F1「實質斷言無違反」 |
| D-SIA-3 | 引擎路線的每一種模式在同一個存放目錄中依序執行（來回、單向各一列）：一般模式第一次 → 存一個快照；第二次（隔一天）→ 重用，`FakeEngine()` 沒有任何請求；Snapshot Mode、嚴格模式 → 傳輸層被呼叫就失敗。四個結果都等於第一次的結果，而且各自經 `catalog_for` 驗證 | SR1-AC2 |
| D-SIA-4 | 目標 GPX：單向、來回（自動判定）、來回（騎士指定的位置不是任何軌跡點的累計距離，`turnaround_source == "rider"`，`turnaround_m` 是實際採用的點而不是請求的公尺數），都經 `get_route`；結果與直接呼叫 R1-3 相同（passthrough，CL-R1-24）；存放替身不被碰到 | SR1-AC2；CL-R1-22、CL-R1-24 |

沒有需要改變契約語義之處，所以沒有 `NEEDS_DA`。

## 5. Artifacts

| 檔案 | 變更（`c2cd52d` → `4cbc71b`） |
| --- | --- |
| `tests/test_integration_r1.py` | 新檔（174 行）：`catalog_for`、`assert_contract_identity`、3 個測試函式 |

`git diff --stat c2cd52d 4cbc71b`：1 file changed, 174 insertions(+)。`src/` 沒有變更。

## 6. Verification

### 6.1 新測試與 SR1-AC2 的對應

| SR1-AC2 的項目 | 測試 | 結果 |
| --- | --- | --- |
| 一般模式：第一次呼叫引擎並存快照 | `test_sr1_ac2_engine_routes_in_every_mode_carry_a_valid_contract_identity[round_trip/one_way]`：請求序列 `route, trace_attributes`（每方向）＋ `status`；存放目錄只有 `<snapshot_id>.json`；快照的 `request_key`、`trip_type` 符合請求；結果經契約驗證 | PASS |
| 一般模式：第二次重用 | 同一測試：`FakeEngine()` 沒有任何請求；結果等於第一次；經契約驗證 | PASS |
| Snapshot Mode | 同一測試：傳輸層被呼叫即失敗；結果等於第一次；經契約驗證 | PASS |
| 嚴格模式 | 同一測試：凍結清單列出 `request_key`、`snapshot_id` 與檔案的 SHA-256；傳輸層被呼叫即失敗；結果等於第一次；經契約驗證；最後仍只有一個快照檔 | PASS |
| 目標 GPX 單向與來回（含騎士指定、落在兩點之間的折返） | `test_sr1_ac2_target_gpx_routes_carry_a_valid_contract_identity[one_way/round_trip_detected/round_trip_rider_between_points]`：與直接呼叫 R1-3 的 `route_id`、`target_gpx_ref`、`turnaround_m`、`turnaround_source` 與各方向的點相同；來回的兩段共用分界點；沒有存檔；經契約驗證 | PASS |
| ID 樣式通過 R1-1 的契約檢查；`RS-` hex 等於 `snapshot_id` hex；檢查點前綴 | 上列 5 個案例都經 `assert_contract_identity`：`validate_route_catalog(...) == []`、`ROUTE_ID_PATTERN`／`CHECKPOINT_ID_PATTERN`／`SNAPSHOT_ID_PATTERN`、`checkpoint_id` 的前綴等於 `route_id`、`route_id[3:] == snapshot_id[3:]`（routing）、`RG-` 與 64 位的 `target_gpx_ref`、`snapshot_id is None`（target_gpx） | PASS |
| 驗證不是空的 | `test_the_catalog_check_rejects_a_broken_identity`：hex 不符、來源與 ID 格式不符、檢查點前綴錯誤都被 `validate_route_catalog` 回報 | PASS |

E-3：位置、引擎回應與 GPX 全部由 `tests/test_routing_engine.py` 的合成產生器在測試中產生（0°N、0°E 附近；`tests/routing_synthetic.py` 的 `SYN-` 代號）；契約資料的名稱與版本是虛構字串。E-4：autouse fixture 封鎖 `socket.socket`、`socket.create_connection`、`socket.getaddrinfo`；傳輸層是 `FakeEngine` 或 `refusing_transport`；沒有網路請求。E-5：沒有修改既有測試。

### 6.2 突變（scratchpad 的 `mutate_sia.py`；在 `source.py` 的記憶體中替換一段、執行、以原本的位元組寫回；結束時 `routing/` 下全部 `.py` 的 SHA-256 與開始時相同，`sources restored: True`）

| # | 破壞 ID 連結的突變 | 新測試（只跑 `tests/test_integration_r1.py`） | 其他測試（routing、snapshot、target GPX、contracts 共 6 檔） |
| --- | --- | --- | --- |
| L1 | `RS-` 的 hex 與 `snapshot_id` 的 hex 不同 | **KILLED**（2 failed） | KILLED（1 failed） |
| L2 | 快照路線回報為 `route_source = target_gpx` | **KILLED**（2 failed） | KILLED（1 failed） |
| L3 | 目標 GPX 路線回報為 `route_source = routing` | **KILLED**（3 failed） | KILLED（4 failed） |
| L4 | 快照路線沒有 `snapshot_id` | **KILLED**（2 failed） | KILLED（34 failed） |
| L5 | 快照路線一律回報為 `one_way` | **KILLED**（1 failed） | KILLED（4 failed） |

新測試單獨就抓到全部 5 個突變；既有測試也因為各自的行為斷言抓到它們，但沒有一個既有測試把 `get_route` 的輸出接到 R1-1 的契約檢查——那是本 finding 的缺口，現在由新測試承載。

### 6.3 E-1 pytest（subject `4cbc71b`）

`.venv/Scripts/python.exe -m pytest -q`，在 commit 之後、工作目錄乾淨時執行，exit 0，完整輸出：

```text
........................................................................ [  3%]
........................................................................ [  6%]
........................................................................ [  9%]
........................................................................ [ 12%]
........................................................................ [ 16%]
........................................................................ [ 19%]
........................................................................ [ 22%]
........................................................................ [ 25%]
........................................................................ [ 28%]
........................................................................ [ 32%]
........................................................................ [ 35%]
........................................................................ [ 38%]
........................................................................ [ 41%]
........................................................................ [ 44%]
........................................................................ [ 48%]
........................................................................ [ 51%]
........................................................................ [ 54%]
........................................................................ [ 57%]
........................................................................ [ 60%]
........................................................................ [ 64%]
........................................................................ [ 67%]
........................................................................ [ 70%]
........................................................................ [ 73%]
........................................................................ [ 77%]
........................................................................ [ 80%]
........................................................................ [ 83%]
........................................................................ [ 86%]
........................................................................ [ 89%]
........................................................................ [ 93%]
........................................................................ [ 96%]
........................................................................ [ 99%]
............                                                             [100%]
2244 passed in 44.11s
```

`.venv/Scripts/python.exe -m pytest -q -rxX`，exit 0，摘要：

```text
............                                                             [100%]
2244 passed in 42.64s
```

`2238`（`9cc566a`）＋ `6` ＝ `2244`。`grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。測試後 `git status --short` 為空。`git ls-files` 不含 `data/`、`.gpx`、`.fit`、`.env`、`*.key`（0 筆）。

### 6.4 contracts CLI

`PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`，exit 0：

```text
data contracts v0.3: tests\fixtures\contract_v02\mock_dataset.json
  derived_segments: OK
  route_catalog: OK
  pace_table: OK
  eta_output: OK
```

## 7. Audit status

- SIA cycle 1 R2 是必要的（治理 §4.4、§4.7），由 Orchestrator 派工；R2 核對 SIA-R1-F1 的 closure 與回歸。本 worklog 的 self-verification 不是 audit。
- SIA-R1-N1（#16 的 NV-PY 沒有具名 owner；Low，non-blocking）：record 的 disposition 是 owner＝Orchestrator（補登），required authority＝Design Authority；不在本次派工範圍，本 worklog 沒有修改 `worklog/issue-16.md`。

## 8. Remaining work

1. Orchestrator 核對本 Executor 的 binding，派 SIA cycle 1 R2（受審 subject 以 `4cbc71b` 之後的 HEAD 為準）。
2. 不在本次：SIA-R1-N1 的補登（Orchestrator／DA）；record 中 tracked items 表的各項沿用各自的 owner（TI-C13-2、RV-6～RV-14、TI-C14-1、TI-C14-5、TI-C15-1、TI-C16-2、TI-C16-3、TI-C165-1、TI-C2R1F3-1 屬 Design Authority；NV-1、NV-PRIVATE 屬 acceptor；NV-PY313／NV-PY、NV-SYMLINK 由 Orchestrator 安排、契約 scope 屬 DA）。真實請求與私有資料下的行為維持 NOT RUN／NOT VERIFIED；本測試只用合成資料，不把它們記為已涵蓋。
