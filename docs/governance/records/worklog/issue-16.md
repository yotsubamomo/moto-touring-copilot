# Worklog — Issue #16（SPEC-R1 R1-4）`routing`：路線引擎的請求與採用、共用的路線介面

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #16（SPEC-R1 R1-4），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **Executor 回報 `NEEDS_DA`。** 範圍 (a)～(f) 中不需要真實網路傳輸的部分全部完成，pytest `1843 passed`（第 6 節 E-1）。**C-16-1（blocking，範圍 (a) 的一部分）**：真實的 HTTP 傳輸層（實際把請求送到公開 Valhalla 伺服器的程式）沒有實作，因為 #14 的既有測試禁止 `routing/` 的任何模組 import 網路模組，而契約沒有寫它應該放在哪裡、或是否屬於本 Ticket；client 目前要求呼叫者傳入傳輸層。**C-16-2**：`map_data_date` 取自狀態回應的 `tileset_last_modified`，請 DA 確認這個讀法。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `bc7024b`（含已結案的 #13、#14、#15）；實作 commit **`7cb4b0cabcccb6541f395f999fe5b43e1b905e91`**（`7cb4b0c`）。worklog 在另一個 record-only commit |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：Issue #16 的內文。Orchestrator 提供的 scratchpad 原文檔（`issue-16-body.md`）以 `sha256sum` 重算為 `105fdc981b1087b60b419690168d205064853a1a41ccde4a6cb092b6ffa8ede1`，等於派工內容所述 run record 第 4 節的值。沒有呼叫 GitHub，沒有修改 Issue。
- **Spec**：SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md`）：第 2 節引用段落；第 4 節 DD-R1-2、CL-R1-1、**CL-R1-5～CL-R1-9**；第 5 節 R1-4 列（範圍 (a)～(f)、AC、排除、依賴、高風險類別 H-1、H-2、H-4）與 E-1～E-6。
- **DA clarifications**（全文閱讀）：
  - `decision-20261118-issue13-c131.md`：CL-R1-13（ID 樣式是 ASCII 的完整字串）。
  - `decision-20261118-issue14-c141.md`：CL-R1-14（正規化取位）、CL-R1-16、**CL-R1-17**、**CL-R1-19**（第 7.2 節：採用的檢查以原值判定；`request` 的經緯度是浮點數；`fetched_at` 不晚於實際收到回應）。
  - `decision-20261118-issue14-qalt1.md`：CL-R1-20、**CL-R1-21**（不依成因分辨或攔下 `SnapshotIntegrityError`；只經三個選取函式取得快照；`put` 與建構的錯誤向上傳遞）。
  - `decision-20261118-issue15-c151.md`：**CL-R1-24**（目標 GPX 原樣帶出、不重算、不套用引擎路線的處理、錯誤原樣傳出）。
- **規格來源**：`docs/spec/SPEC-001-plan-schema.md` §2（ID、雜湊與正規化、隱私）；4.12（跨欄位規則、國道檢查的用語）；4.13（六個代碼）；4.14（RouteSnapshot、RouteLeg）；5.4（30 天、200 m、2%）；7.11 第 1～8 項；第 9 節 S15、S17、S23、S24、S30、S35、S38、S39、S40、S68、S69、S70。
- **高風險類別**：`decision-20261117-high-risk-categories.md` §3.1、§3.2、§3.4、§5；R1-4 標為 H-1、H-2、H-4（第 6 節 E-6）。
- **參考原始碼**（CL-R1-1，只讀、沒有執行）：`experiments/cr01_checks/routing_client.py`、`experiments/cr01_checks/routing_c4_snapshots.py`。只以 Read 指定這兩個完整路徑；沒有搜尋、列出或讀取 `experiments/` 的其他檔案，也沒有跟隨它們引用的 `data/` 路徑。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-a1e2cfa52290d496f.{meta.json,jsonl}`；`meta.json` 的 `agentType` 是 `gov-executor`，`description` 是「Executor: implement Issue #16 R1-4」。
- Executor 自行觀測（實作 commit `7cb4b0c` 之後、寫本 worklog 之前，以第 3.6 節的掃描方式）：agentId `a1e2cfa52290d496f`，(`claude-opus-5-5`, `high`) 105 則，集合只有一個元素。**這是自我觀測，不是派工者的核對**；之後的訊息不在這個數字內，Orchestrator 採用本 return 前須自行核對全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 Bindings m3（全文）、治理本文 §3.5、§3.7、§3.8、impl-default v2 §3–§5、§9、derivation-spec-r1（全文）、四份 DA clarification records（全文）、高風險類別 record（全文）、Issue #16 原文（核對雜湊）、SPEC-001 §2、4.12～4.14、5.4、7.11、第 9 節的相關 S 編號、`routing/` 的全部既有模組（`__init__.py`、`canonical.py`、`request_key.py`、`snapshot.py`、`store.py`、`target_gpx.py`）、`ingest/geometry.py` 的 `GeoPoint`、`ingest/segments.py` 的 `haversine_m`、`contracts/schemas.py` 的樣式、`tests/routing_synthetic.py`、`tests/conftest.py`、`tests/test_routing_store.py` 與 `tests/test_target_gpx.py` 中的網路與路徑測試、worklog `issue-15.md`（格式參考）、`docs/conventions/git-commit-rules.md`、`pyproject.toml`，以及第 1 節的兩個參考原始碼。
2. 基準：`bc7024b` 上 `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider` 為 `1678 passed`。
3. 新建 `src/moto_copilot/routing/valhalla.py`（範圍 (a)）：常數 `VALHALLA_ENDPOINT`、`USER_AGENT`、`ENGINE_NAME`；`routing_params()`（機車設定加 `use_highways: 0`、`units: kilometers`）；`Position` 與 `position_from`（輸入檢查，經緯度轉成 `float`）；`route_body`、`trace_body`；`ValhallaClient(transport, *, endpoint=VALHALLA_ENDPOINT, clock=None)` 的 `route`、`trace_attributes`、`status`（各送一次，不重試）；`HttpResponse`、`TransportError`、`EngineReply`；`decode_polyline6`。
4. 新建 `src/moto_copilot/routing/adoption.py`（範圍 (b)、(c)、(d)）：`evaluate_direction`（一個方向的路線請求、道路屬性查詢與全部檢查，回傳 `DirectionOutcome`；只有通過時才組成 RouteLeg）、`decide_code`（CL-R1-8）、`offsets`／`offset_reasons`／`nearest_on_shape`（CL-R1-7）、`FREEWAY_CHECK_METHOD`。
5. 新建 `src/moto_copilot/routing/source.py`（範圍 (e)、(f)）：`get_route(request, *, store, client, snapshot_mode, frozen_entries, now)`，對 `EngineRouteRequest` 與 `TargetGpxRequest` 回傳 `AdoptedRoute` 或 `RouteFailure`。
6. `src/moto_copilot/routing/__init__.py`：只加上新模組的 import、`__all__` 的新名稱與說明文字；#14、#15 既有的匯出與行為不變。
7. 新建 `tests/test_routing_engine.py`（76 個測試函式，165 個案例）：以 `FakeEngine` 替身取代傳輸層，autouse fixture 封鎖 socket。
8. 自我驗證：全套 pytest、23 個突變檢查（第 6 節 E-6）、子行程中的環境變數測試、`git ls-files` 檢查。
9. 依 SA-1 在 topic branch 作本機 commit `7cb4b0c`；commit 前以 `git diff --cached --name-only` 確認暫存的只有上列 5 個檔案，不含 `.env`、GPX、FIT、`data/` 或測試產生的暫存檔。
10. 沒有 push、沒有開 PR、沒有碰 GitHub；沒有讀取、列出或搜尋 `data/`；沒有使用 `git status --ignored`；沒有讀 `.env`；沒有執行 `experiments/` 下的任何腳本；沒有發出任何網路請求。

## 4. Decisions and assumptions

| # | 決定 | 依據 |
| --- | --- | --- |
| D-16-1 | 傳輸層由呼叫者傳入：`transport(url, body_bytes, headers) -> HttpResponse`，沒有回應時拋 `TransportError`。client 負責 URL（端點＋`/route`、`/trace_attributes`、`/status`）、JSON 內容與 header（`Content-Type`、`User-Agent`），三種請求都是 POST。**本 Ticket 沒有提供真實的 HTTP 傳輸層**（C-16-1） | 範圍 (a)「傳輸層可替換，測試不連網」；CL-R1-9 |
| D-16-2 | 端點：模組常數 `https://valhalla1.openstreetmap.de`（與 `routing_client.py` 相同）。可以由呼叫者以 `endpoint=` 明確傳入，但只接受 `https://` 加主機（可帶埠），不可帶路徑、查詢、帳號或結尾換行。程式中沒有讀取任何環境變數的程式碼 | CL-R1-9「常數或明確傳入的設定值」；H-1 |
| D-16-3 | User-Agent 是 `route-client/1.0`。`routing_client.py` 的 `route-snapshot-check/0.1 (course project; low volume)` 帶有「course project」的描述，這裡不用 | CL-R1-9「通用的名稱，不含姓名、email 或專案名稱」 |
| D-16-4 | 路線請求只送 `locations`（每個位置只有 `lat`、`lon`、`type`）與 `routing_params()`；代號、角色與地名不送出。起點與終點的 `type` 是 `break`，中間位置是 `via`（不分段、允許迴轉），所以一個方向的回應應只有一個 leg、一條 shape；不是剛好一個 leg 時不採用（`response_malformed`）。**這是依 Valhalla API 文件的位置型態所作的選擇，真實伺服器的行為 NOT VERIFIED**（沒有真實請求，CL-R1-1） | CL-R1-5；4.14 的 `shape`（一個方向一條折線） |
| D-16-5 | `routing_params` ＝ `{"costing": "motorcycle", "costing_options": {"motorcycle": {"use_highways": 0}}, "units": "kilometers"}`，它就是快照的 `routing_params` 與 `request_key` 的 `routing_params`（R1-4 自己計算 `request_key`，呼叫者不能給不同的參數）。沒有 `exclude_*`、沒有高度 | CL-R1-5；P-1；Q-3 第 7 項；4.14「快照記錄實際送出的值」 |
| D-16-6 | RouteLeg 的 `request` ＝ `{"locations": [{ref_id, role, lat, lon, type}...], "routing_params": ...}`，依這個方向的順序；經緯度是 `float` | 4.14 `request`；CL-R1-5；CL-R1-19 第 2 項 |
| D-16-7 | 道路屬性查詢只送 `encoded_polyline`（引擎自己回傳的 shape）、`costing`、`shape_match: walk_or_snap`、`filters`（`edge.names`、`edge.length`、`edge.road_class`）。與 C4 的做法相同 | 7.11 第 5 項「只送出引擎自己回傳的折線」 |
| D-16-8 | 國道訊號（任一個就是 `fail`）：trip 或 leg summary 的 `has_highway` 為 true（或是非布林的真值）；任何轉向的 `highway` 不是 `None`／`False`；道路屬性任何一段的 `road_class` 是 `motorway`（只要出現，不論長度）；轉向的 `begin_street_names`／`street_names` 或道路屬性的 `names` 中有名稱符合 `國道\|高速公路\|freeway`（不分大小寫）。比字面略嚴：`Freeway` 不分大小寫、motorway 以出現判定（S39「含 `motorway` 路段」）、leg summary 的旗標也算。都是 fail closed 方向 | 7.11 第 5 項；修正 B（訊號矛盾時 fail closed）；H-4 |
| D-16-9 | 無法驗證（沒有訊號時不產生 `freeway_check`）：trip summary 沒有布林值的 `has_highway`；道路屬性查詢 HTTP 不是 200、沒有回應、`edges` 不是非空清單、任何一段的 `length` 不是非負有限數、`road_class` 不是字串、`names` 不是字串清單；長度不符；路線回應中檢查需要的欄位讀不到（`response_malformed`） | 7.11 第 5 項；4.14 `has_highway`、`freeway_check` |
| D-16-10 | 2% 的判定：`|Σ edge.length − trip.summary.length| ≤ trip.summary.length × 0.02`，全部以 `Decimal(repr(x))` 精確計算，不用浮點數、不用存入快照的整數公尺（CL-R1-19 第 1 項） | 7.11 第 5 項第 (1) 款；CL-R1-19 |
| D-16-11 | 警告：回應最上層或 `trip` 中的 `warnings` 有任何項目（形式正確與否），或不是清單，就不採用。道路屬性查詢回應中的警告不算 7.11 第 7 項的「回應的警告」（第 7 項與 4.14 `warnings` 指路線回應） | 7.11 第 7 項；4.14 `warnings` |
| D-16-12 | 偏移（CL-R1-7）：起點、終點用 haversine（`ingest.segments.haversine_m`，地球半徑 6,371,000 m）到折線的第一點、最後一點；中間位置是到每個線段的最近點，在以該位置為中心的局部平面上計算（點到線段），最近點相同時取第一個線段；沿線里程＝之前各段的 haversine 長度加上最近線段的比例。判定 `≤ 200 m`（以計算出的原值），沿線里程**嚴格**遞增 | CL-R1-7；CL-R1-19 第 1 項；7.11 第 8 項 |
| D-16-13 | `distance_m` ＝ `trip.summary.length`（km）×1000、`engine_time_s` ＝ `trip.summary.time`，都以最短十進位表示 `ROUND_HALF_UP` 取整數；`road_names` 依 CL-R1-6（每個轉向的 `begin_street_names` 再 `street_names`，第一次出現的順序、去重複；空字串略過，不是字串時 `response_malformed`） | 4.14；CL-R1-6；CL-R1-18 的取整原則（同一種「四捨五入」） |
| D-16-14 | `fetched_at` ＝ client 在傳輸層回傳之後立刻讀取的時鐘，轉成 +08:00、捨去到秒（`replace(microsecond=0)`），是路線回應（不是道路屬性查詢）的收到時間 | CL-R1-19 第 3 項；4.14 `fetched_at` |
| D-16-15 | 請求次數與順序（CL-R1-5、CL-R1-8）：每個方向送一次路線請求；回應有可解碼的 shape 時，**即使其他檢查已不通過**也送一次道路屬性查詢，以取得全部國道訊號。來回行程的兩個方向都送出並檢查；只有在某個請求完全沒有回應（`TransportError`）時停止後續的請求，其餘方向記為 `not_sent`。不重試。兩個方向都通過之後才送一次狀態請求，然後組成快照並存檔 | CL-R1-5；CL-R1-8 |
| D-16-16 | 引擎資訊（DD-R1-2）：`engine_name` ＝ `Valhalla`；`engine_version` ＝ 狀態回應的 `version`（非空字串），沒有回報、HTTP 錯誤、不是 JSON 或沒有回應時 ＝ `unreported`；`map_data_date` ＝ 狀態回應的 `tileset_last_modified`（Unix 秒，整數）在 +08:00 的日期，沒有回報或格式不對時 ＝ `null`，不以取得日期代替。**`tileset_last_modified` 是否等於 4.14 的「圖資日期」請 DA 確認（C-16-2）** | DD-R1-2；4.14 `map_data_date`；C4 記錄的欄位 |
| D-16-17 | 取得順序（範圍 (e)）：Snapshot Mode（`snapshot_mode=True`）只呼叫 `select_snapshot_mode`，或在給了凍結清單時只呼叫 `select_strict`，不使用 client；一般模式先 `find_reusable`，沒有時才呼叫引擎；引擎失敗或任何方向不通過時回傳 `RouteFailure`，不改用任何快照。凍結清單只能與 `snapshot_mode=True` 一起給，否則 `ValueError`（不在一般模式下默默忽略清單） | 7.11 第 3 項；CL-R1-4；lead 寫定「指定了凍結清單就是嚴格模式」 |
| D-16-18 | 存放的例外都不攔下（CL-R1-17、CL-R1-21）：`find_reusable`、`select_snapshot_mode`、`select_strict`、`SnapshotStore.put` 的例外原樣向上傳遞；只有 `put` 成功後才回傳路線，回傳的是 `put` 回來的快照（內容相同時是既有檔案，保留它自己的 `fetched_at`）。從已驗證的快照解碼 shape 失敗時拋 `SnapshotIntegrityError`（訊息只含 `snapshot_id`），不是路線錯誤代碼 | CL-R1-17；CL-R1-21；7.11 第 1、3 項 |
| D-16-19 | 共用介面（範圍 (f)）：`AdoptedRoute(route_id, route_source, trip_type, snapshot_id, target_gpx_ref, turnaround_m, turnaround_source, legs)`，`AdoptedLeg(direction, points, distance_m, road_names)`；`RouteFailure(code, case, reasons)`，`reasons` 只是 `方向:代碼` 的字串。`routing`：幾何是各方向自己的 shape 解碼後的點（不反轉）、里程是快照的整數公尺。`target_gpx`：原樣帶出 R1-3 的結果（點是同一組物件、長度是 `length_m` 原值、道路名稱是空的 tuple、`snapshot_id` 是 `None`），錯誤的 `code`、`case` 原樣，`TripTypeRequiredError`、`ValueError`、`TypeError` 照原樣傳出 | 範圍 (f)；CL-R1-24 |
| D-16-20 | 一般模式在開始時就檢查請求位置：方向的集合必須剛好是行程型態的方向，每個方向至少兩個位置，每個位置的代號、角色是非空字串，經緯度是有限的數字且在 ±90／±180 內。錯誤訊息不含座標。位置與 `request_key` 的地點（`origin`、`destination`、`via`）是否對應不檢查（C-16-3） | CL-R1-5；CL-R1-9 |
| D-16-21 | 新模組不 log、不 `print`，不 import 網路模組；原始碼不含 `environ`／`getenv`（#14 的既有測試也掃描整個 `routing/` 的頂層模組） | CL-R1-9；H-1、H-2 |

## 5. Artifacts

| 檔案 | 變更（`bc7024b` → `7cb4b0c`） |
| --- | --- |
| `src/moto_copilot/routing/valhalla.py` | 新檔：client（範圍 (a)） |
| `src/moto_copilot/routing/adoption.py` | 新檔：一個方向的採用檢查與錯誤代碼（範圍 (b)、(c)、(d)） |
| `src/moto_copilot/routing/source.py` | 新檔：取得順序與共用的路線介面（範圍 (e)、(f)） |
| `src/moto_copilot/routing/__init__.py` | 加上新名稱的 import、`__all__` 與說明文字 |
| `tests/test_routing_engine.py` | 新檔：本 Ticket 的測試 |

`git diff --stat bc7024b 7cb4b0c`：5 files changed, 2221 insertions(+), 2 deletions(-)。`git diff bc7024b 7cb4b0c` 對 `routing/` 的 `canonical.py`、`snapshot.py`、`store.py`、`request_key.py`、`target_gpx.py`、`contracts/`、`ingest/`、`tests/test_routing_store.py`、`tests/test_routing_snapshot.py`、`tests/test_target_gpx.py`、`tests/routing_synthetic.py` 為空。

## 6. Verification

### E-1 pytest（subject `7cb4b0c`）

`.venv/Scripts/python.exe -m pytest -q`，在 commit 之後、工作目錄乾淨時執行，exit 0，完整輸出：

```text
........................................................................ [  3%]
........................................................................ [  7%]
........................................................................ [ 11%]
........................................................................ [ 15%]
........................................................................ [ 19%]
........................................................................ [ 23%]
........................................................................ [ 27%]
........................................................................ [ 31%]
........................................................................ [ 35%]
........................................................................ [ 39%]
........................................................................ [ 42%]
........................................................................ [ 46%]
........................................................................ [ 50%]
........................................................................ [ 54%]
........................................................................ [ 58%]
........................................................................ [ 62%]
........................................................................ [ 66%]
........................................................................ [ 70%]
........................................................................ [ 74%]
........................................................................ [ 78%]
........................................................................ [ 82%]
........................................................................ [ 85%]
........................................................................ [ 89%]
........................................................................ [ 93%]
........................................................................ [ 97%]
...........................................                              [100%]
1843 passed in 41.76s
```

`1678`（基準）＋ `165`（新測試）＝ `1843`。`.venv/Scripts/python.exe -m pytest -q -rxXs tests/test_routing_engine.py`：`165 passed`。`grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。#14、#15 的測試檔（`test_routing_store.py`、`test_routing_snapshot.py`、`test_target_gpx.py`）沒有修改並照常通過（含 `test_the_routing_package_imports_no_network_or_environment_modules`，它也掃描三個新模組）。測試後 `git status --short` 為空。

### E-2 AC 對 S 編號

測試檔：`tests/test_routing_engine.py`（以下省略檔名）。E-1 中全部 PASS；「結果」欄寫的是 AC 的狀態。

| AC | 測試 | 結果 |
| --- | --- | --- |
| S15 中屬於路線的部分（引擎失敗或國道檢查沒通過時沒有路線、里程與道路名稱；一般模式不改用已失效的快照） | `test_s35_s15_engine_failure_with_only_an_expired_snapshot_is_routing_unavailable`、`test_s15_a_snapshot_checked_with_another_method_is_not_used_when_the_engine_fails`、`test_s24_a_fail_in_either_direction_stores_nothing_and_is_highway_in_route`、`test_s35_s38_one_direction_failing_stores_nothing_and_has_no_route`（`assert_no_route`：`RouteFailure` 沒有路線、里程與道路名稱的欄位） | PASS（路線的部分；Planner 的部分不在本 Ticket） |
| S17（Snapshot Mode 不呼叫引擎） | `test_s17_snapshot_mode_does_not_call_the_engine`（傳輸層替身被呼叫即失敗；400 天後仍可用）、`test_s17_snapshot_mode_without_a_snapshot_returns_snapshot_missing`、`test_strict_mode_uses_the_frozen_snapshot_and_never_the_engine`、`test_strict_mode_stop_propagates_and_nothing_else_is_used` | PASS |
| S23 中屬於行為的部分（兩個方向各有自己的 `request`、`shape`、`fetched_at`；`return` 不是 `outbound` 的反轉） | `test_s23_each_direction_has_its_own_request_shape_and_fetched_at_and_return_is_not_reversed`、`test_cl_r1_5_each_direction_gets_its_own_positions_one_route_and_one_trace_request`、`test_a_round_trip_is_adopted_and_stored_once` | PASS |
| S24 第一句（任一方向 `fail` → 整條不存、`highway_in_route`） | `test_s24_a_fail_in_either_direction_stores_nothing_and_is_highway_in_route[outbound/return]` | PASS |
| S30（`use_highways: 0`、不帶硬性排除；有警告 → `routing_unavailable`） | `test_s30_route_request_is_motorcycle_with_use_highways_0_and_no_exclusion_or_elevation`、`test_s30_a_reply_with_any_warning_is_routing_unavailable`（最上層、`trip` 內、形式不正確、不是清單、空物件）、`test_an_empty_warning_list_is_no_warning` | PASS |
| S35 中屬於引擎的部分（第二次不呼叫引擎；31 天後重新取得；引擎失敗而只有過期快照 → `routing_unavailable`；回程沒通過時去程也不存檔） | `test_s35_the_same_request_a_second_time_does_not_call_the_engine`、`test_s35_after_31_days_the_route_is_fetched_again_and_the_same_content_keeps_the_old_file`、`test_s35_after_31_days_a_different_reply_is_a_new_snapshot_and_the_old_one_stays`、`test_s35_s15_engine_failure_with_only_an_expired_snapshot_is_routing_unavailable`、`test_s35_s38_one_direction_failing_stores_nothing_and_has_no_route[return]` | PASS |
| S38 中屬於路線的部分（回程不是去程的反轉；回程請求失敗 → 路線錯誤，沒有里程與道路名稱） | `test_s23_...`（去回不同路的合成回應）、`test_s35_s38_one_direction_failing_stores_nothing_and_has_no_route[return]` | PASS（`turnaround` 檢查點屬 G-RTE，不在本 Ticket） |
| S39 中以合成回應可以驗證的部分 | `test_s39_has_highway_true_with_no_freeway_in_the_road_attributes_is_fail`、`test_s39_has_highway_true_in_the_trip_or_the_leg_summary_is_fail`、`test_s39_road_attributes_with_a_motorway_or_a_freeway_name_are_fail`、`test_maneuver_names_and_highway_flags_are_freeway_signals`、`test_s39_a_failed_road_attribute_query_is_routing_unavailable_with_no_snapshot`（8 種失敗） | PASS。「五條參考路線的 10 段都是 `pass`」：排除項目，**NOT RUN**（需要真實請求） |
| S40 中以合成回應可以驗證的部分 | `test_s40_an_end_offset_of_several_kilometres_is_rejected`（終點偏移 6.8 km）、`test_s40_s68_a_via_more_than_200_m_from_the_shape_is_rejected`（200.5、250、5000 m） | PASS。「五條參考路線都通過」「詞彙表每個地標的偏移不超過 100 m」：排除項目，**NOT RUN** |
| S68 | `test_s40_s68_a_via_more_than_200_m_from_the_shape_is_rejected` | PASS |
| S69 | `test_s69_two_vias_within_200_m_but_passed_in_reverse_order_are_rejected`（反序拒收；同兩點依序則採用） | PASS |
| S70 | `test_s70_the_road_entry_position_also_has_a_via_offset`（途經點＋公路進入端 → `via_offset_m` 兩筆） | PASS |
| 另加：沒有回報 `has_highway` → `routing_unavailable`，不產生 `freeway_check` | `test_has_highway_not_reported_is_routing_unavailable_with_no_freeway_check_value`（缺欄位、`null`、`0`；`1`、`"true"`、`"false"` 是非布林的真值，另記為國道訊號） | PASS |
| 另加：道路屬性長度與路線里程相差超過 2% → `routing_unavailable`，不產生 `freeway_check` | `test_the_road_attribute_length_must_be_within_2_percent`（1.0、±2% 通過；1.0201、0.9799、1.5 拒收）、`test_the_2_percent_check_is_exact_at_the_boundary`、`test_a_failed_road_attribute_query_gives_no_freeway_check_value` | PASS |
| 另加：國道訊號與其他不採用的原因同時出現 → `highway_in_route` | `test_a_freeway_signal_with_another_reason_is_highway_in_route`（警告、偏移、長度不符、查詢失敗、另一方向錯誤）、`test_a_freeway_signal_is_highway_in_route_even_when_the_other_direction_is_unreachable`、`test_the_freeway_check_runs_even_when_the_offsets_already_fail` | PASS |
| 另加：中間位置的沿線里程相等時拒收 | `test_cl_r1_7_vias_with_equal_along_shape_distance_are_out_of_order` | PASS |
| 另加：User-Agent 與請求內容不含個人識別資訊 | `test_user_agent_and_request_content_hold_no_personal_information`、`test_the_road_attribute_query_sends_only_the_engines_own_shape`、`test_s30_route_request_...`（每個位置只有 `lat`、`lon`、`type`） | PASS |
| 另加：端點不受環境變數影響 | `test_h1_the_endpoint_is_not_affected_by_env_variables`（新的直譯器，設定 `VALHALLA_URL`、`HTTPS_PROXY` 等 11 個變數）、`test_the_endpoint_is_the_constant_and_every_request_goes_to_it`、`test_an_explicit_endpoint_must_be_a_bare_https_host`、`test_the_new_modules_do_not_read_env_log_print_or_import_network_modules` | PASS（client 層。真實傳輸層的代理與轉址處理屬 C-16-1，NOT VERIFIED） |
| CL-R1-5（每個方向一次路線請求與一次道路屬性查詢，不重試） | `test_cl_r1_5_each_direction_gets_its_own_positions_one_route_and_one_trace_request`、`test_no_request_is_retried_after_an_error_reply`、`test_an_unreachable_engine_stops_further_requests`、`test_an_unreachable_engine_during_the_outbound_trace_does_not_send_the_return` | PASS |
| CL-R1-6（道路名稱） | `test_cl_r1_6_road_names_follow_the_maneuvers_in_order_without_repeats` | PASS |
| CL-R1-19 第 1 項（原值判定；200.04 m 拒收） | `test_cl_r1_19_an_offset_just_above_200_m_is_rejected_on_the_raw_value[start/end/via]`（200.04 m 拒收；199.96 m 採用且存入 199.9） | PASS |
| CL-R1-19 第 2、3 項 | `test_cl_r1_19_coordinates_in_the_stored_request_are_floats`、`test_cl_r1_19_fetched_at_is_cut_to_the_second_and_not_after_receipt`、`test_a_snapshot_stored_this_second_is_reused_right_away` | PASS |
| CL-R1-21 (i)(ii)(iii) | `test_cl_r1_21_i_a_selection_error_in_normal_mode_propagates_and_the_engine_is_not_called`、`test_cl_r1_21_a_listed_entry_that_is_a_directory_stops_normal_mode`、`test_cl_r1_21_ii_a_selection_error_in_snapshot_mode_is_not_snapshot_missing`、`test_cl_r1_21_iii_a_put_error_propagates_and_no_route_is_returned[SnapshotStoreError/SnapshotConflictError]`、`test_cl_r1_21_iii_a_real_write_failure_propagates_without_a_path`、`test_strict_mode_stop_propagates_and_nothing_else_is_used` | PASS |
| CL-R1-24 第 1～6 項 | `test_cl_r1_24_a_target_gpx_route_is_carried_as_it_is`（單向、自動判定的來回、落在兩點之間的騎士指定、單向帶 km；欄位等於直接呼叫 R1-3；store 與傳輸層替身被碰到即失敗）、`test_cl_r1_24_a_target_gpx_path_is_read_and_carried_as_it_is`、`test_cl_r1_24_target_gpx_errors_pass_through_with_their_case`（`too_few_points`、`unreadable`、`end_not_at_start`、`turnaround_unconfirmed`）、`test_cl_r1_24_caller_errors_of_the_target_gpx_propagate` | PASS |
| DD-R1-2 | `test_dd_r1_2_engine_version_and_map_data_date`（8 種狀態回應） | PASS（`map_data_date` 的讀法待 C-16-2） |
| CL-R1-13（S58 中 `RS-`／`SN-` 在引擎路徑上的部分） | `test_cl_r1_13_the_ids_on_the_engine_path_follow_the_contract_patterns` | PASS |

### E-3 合成資料的來源

- 位置與折線：`at(x, y)` 把「離 0°N、0°E 向東 x m、向北 y m」換成經緯度（開放海域）；去程是 y = 0 的東向直線、回程是 y = 30 m 的西向直線，每 100 m 一點。沒有真實的軌跡、地名、住家附近的座標或私有路線，也沒有公開地標的座標。
- 引擎回應：測試中手寫成 Valhalla 回應的形狀（`trip.legs[0].shape`、`maneuvers`、`summary`；道路屬性的 `edges`；狀態的 `version`、`tileset_last_modified`）；shape 由測試中的獨立編碼器 `encode6` 從合成點產生。道路名稱（`Synthetic Road 1` 等）、版本字串、日期都是虛構的；國道名稱的測試字串（`國道3號`、`Synthetic 高速公路`）只用來觸發名稱檢查，沒有對應任何位置。
- 地點代號與座標定義沿用 `tests/routing_synthetic.py`（`SYN-...`，0°N、0°E 附近的虛構值）。目標 GPX 在測試中產生成字串；寫檔只在 pytest 的 `tmp_path`。

### E-4 沒有網路請求

- autouse fixture `no_network`：本檔每個測試都把 `socket.socket`、`socket.create_connection`、`socket.getaddrinfo` 換成會報錯的替身；165 個案例全部照常完成。
- 傳輸層一律是 `FakeEngine`（記錄每個請求、依序回答）或 `refusing_transport`（被呼叫即失敗）。`test_h1_the_endpoint_is_not_affected_by_env_variables` 的子行程使用只回傳 503 的替身，沒有網路。
- 靜態檢查：`test_the_new_modules_do_not_read_env_log_print_or_import_network_modules`；#14 的 `test_the_routing_package_imports_no_network_or_environment_modules` 也照常通過。

### E-5 修改的既有測試

無。`tests/` 中只新增 `tests/test_routing_engine.py`；`tests/routing_synthetic.py` 與 #14、#15 的測試檔沒有修改。

### E-6 高風險類別的 self-verification（`decision-20261117-high-risk-categories.md` 第 5 節）

**H-1（判定 3.1 第 2 項：決定請求端點的方式；沒有憑證）**
- 端點是 `valhalla.py` 的常數；唯一的另一個來源是 `ValhallaClient(endpoint=...)` 明確傳入的值，並限制為 `https://` 加主機。程式中沒有 `environ`／`getenv`（兩個靜態測試）；在新的直譯器中設定 11 個與端點、代理有關的環境變數，送出的 URL 仍是常數（子行程測試）。
- 沒有憑證、header 中沒有金鑰；diff 中沒有任何金鑰字串；`git ls-files` 不含 `.env`、`*.key`（0 筆）。
- 限制：**真實傳輸層不存在（C-16-1）**，所以「不跟隨 HTTP 轉址」「不使用環境變數中的代理」這兩項屬於傳輸層的轉向風險，目前 NOT VERIFIED；client 層無法轉向已由測試證明。

**H-2（判定 3.2 第 3 項：送往第三方的內容與 User-Agent）**
- 路線請求每個位置只有 `lat`、`lon`、`type`；代號、角色、地名不送出；道路屬性查詢只送引擎自己回傳的 shape。User-Agent 是 `route-client/1.0`，不含姓名、email、`@` 或專案名稱（測試列舉 `moto`、`copilot`、`touring`、`nchu`、`aiot`、`course`、`project`）。
- 錯誤訊息與 `RouteFailure` 不含座標：位置的錯誤訊息只寫欄位名稱（測試以特定值確認 traceback 中沒有它）；`reasons` 只是小寫代碼；存放錯誤經 `traceback.format_exception` 確認不含合成的目錄名稱。新模組不 log、不 `print`。
- 送出的位置是否只是公開地標，由呼叫者（G-RREQ、詞彙表）負責；本 Ticket 不判定位置的來源。`git ls-files` 不含 `data/`、`.gpx`、`.fit`、`.env`（0 筆）；diff 中的座標全部是第 E-3 節的合成值。

**H-4（判定 3.4 第 4 項：國道檢查、偏移、警告、途經點順序）**
- 每條失敗路徑都有測試顯示是明確的路線錯誤代碼或例外，不是採用、不是預設值：引擎無回應、HTTP 錯誤、不是 JSON、沒有 `trip`、回應讀不到（8 種）、警告（5 種）、`has_highway` 沒有回報、道路屬性查詢失敗（8 種）、長度不符、偏移（起點、終點、中間）、順序（反序、相等）、存放錯誤（傳遞）。無法驗證時不產生 `freeway_check`；訊號矛盾時 `fail`。
- 突變檢查：以 scratchpad 的腳本（`mutate16.py`）在原始碼中替換一段字串、執行 `tests/test_routing_engine.py`、在 `finally` 中寫回記憶體中的原文（不以 git 還原，不會連帶還原未 commit 的修改）；結束時各檔 SHA-256 與開始時相同（`sources restored: True`）。23 個突變全部被抓到：

| # | 突變 | 失敗的案例數 |
| --- | --- | --- |
| M1 | 偏移以捨去到一位小數後的值判定 | 3 |
| M2 | 沿線里程相等時接受 | 1 |
| M3 | `routing_unavailable` 優先於 `highway_in_route` | 8 |
| M4 | 只在沒有其他原因時才送道路屬性查詢 | 5 |
| M5 | 沒有回報 `has_highway` 當成 false | 6 |
| M6 | 長度門檻改為 5% | 3 |
| M7 | motorway 只在長度大於 0 時算 | 1 |
| M8 | 第一個方向不通過就不送第二個方向 | 3 |
| M9 | 選取的 `SnapshotIntegrityError` 被攔下後改呼叫引擎 | 2 |
| M10 | `put` 失敗時回傳未存檔的路線 | 3 |
| M11 | 忽略形式不正確的警告 | 3 |
| M12 | 回程幾何改用去程的反轉 | 1 |
| M13 | `fetched_at` 進位到下一秒 | 2 |
| M14 | 國道名稱區分大小寫 | 1 |
| M15 | Snapshot Mode 找不到時改呼叫引擎 | 1 |
| M16 | 經緯度不轉成浮點數 | 1 |
| M17 | 目標 GPX 的回程去掉共用的分界點 | 2 |
| M18 | 空的、非清單的警告被略過 | 1 |
| M19 | 引擎無回應後仍送出另一個方向 | 4 |
| M20 | 忽略轉向的 highway 旗標 | 1 |
| M21 | 忽略道路屬性查詢的 HTTP 錯誤 | 2 |
| M22 | 忽略 trip summary 的 `has_highway: true` | 2（第一次執行時存活：合成回應的 leg summary 也帶同一個旗標；之後補上 `test_s39_has_highway_true_in_the_trip_or_the_leg_summary_is_fail` 分開兩個來源） |
| M23 | User-Agent 含專案名稱 | 1 |

- 附記：Windows 的 `Path.write_text` 會寫出 CRLF。本 repo 是 `core.autocrlf=true`（工作目錄 CRLF、index LF），新檔在工作目錄中本來就是 CRLF，所以還原後內容與 commit 的內容相同；第一次執行時腳本因子行程輸出的編碼錯誤中止，中止前的那個突變也已由 `finally` 還原（之後重跑確認）。

**其他 self-verification**
- 新模組的說明文字寫明國道檢查「不是對道路主管機關資料的獨立驗證」（`test_the_freeway_check_method_names_the_method_and_thresholds`），沒有把它稱為已驗證（SR1-AC5）。
- 沒有在 3.13 以後的直譯器上執行（本機只有 3.11.2／3.12）：**NOT RUN**。新程式沒有使用會因版本改變語義的判斷式（例如 `Path.is_file()`）。

## 7. Concerns

| # | 內容 | 建議的 owner／authority | 狀態 |
| --- | --- | --- | --- |
| **C-16-1**（blocking，範圍 (a) 的一部分） | **真實的 HTTP 傳輸層沒有實作。** 範圍 (a) 是「公開 Valhalla 伺服器的 client（…；傳輸層可替換，測試不連網）」。#14 的既有測試 `test_the_routing_package_imports_no_network_or_environment_modules`（`tests/test_routing_store.py`，派工禁止修改）對 `routing/` 的每一個頂層 `.py` 禁止 import `socket`、`http`、`urllib`、`requests`、`httpx`、`ssl`、`subprocess`；任何真實的 HTTP 傳輸都需要其中之一。契約沒有寫真實傳輸層是否屬於本 Ticket，也沒有寫它的位置。可行的做法：(i) 放在 `routing/` 的子套件（例如 `routing/transport/http.py`）：該測試的 `glob("*.py")` 不遞迴，所以不會掃到；但這等於繞過那個測試的字面，Executor 不自行採用；(ii) 修改 #14 的測試，明定只有一個指名的傳輸模組可以 import 網路模組（需要修改 #14 測試的授權）；(iii) 放在 `routing/` 以外的套件（超出派工可修改的範圍）；(iv) 判定真實傳輸層屬之後的整合 Ticket（與 R1-3 的「CLI 的接線」同類），R1-4 只交付可替換傳輸層的 client。無論哪一種，真實傳輸層都要：不跟隨 HTTP 轉址、不使用環境變數中的代理（H-1「不可被轉向」）、設定逾時、把連線失敗轉成 `TransportError`、錯誤訊息不含請求內容 | Design Authority（契約的範圍與位置；若選 (ii)，DA 判定是否需要其他授權） | 待裁決；其餘範圍已完成，不受影響 |
| **C-16-2**（需要確認） | `map_data_date` 取自 Valhalla 狀態回應的 `tileset_last_modified`（圖磚建置的時間，Unix 秒）在 +08:00 的日期（D-16-16）。另一種合理讀法是 Valhalla 沒有回報「圖資日期」本身，所以一律 `null`。這個值在快照的雜湊範圍內，決定 `snapshot_id`；目前沒有任何已存的快照，改變不影響既有資料 | Design Authority | 待確認；改動只在 `source.py` 的 `_engine_info` 與一個測試 |
| C-16-3（tracked item 建議） | R1-4 不檢查各方向的請求位置與 `request_key` 的地點（`origin`、`destination`、`via` 的代號）是否對應：組成規則屬 G-RREQ（7.11 第 2 項的去程／回程組成、公路的進入端與另一端）。呼叫者若給了不一致的兩者，快照會存在不對應的鍵下，之後被一般模式或 Snapshot Mode 重用（H-4 的重用風險）。建議 G-RREQ 的 derivation 決定由哪一層核對 | Design Authority（G-RREQ 的 derivation） | 知悉 |
| C-16-4（知悉） | D-16-8 的三處比字面嚴格（`Freeway` 不分大小寫、`motorway` 以出現判定、leg summary 的旗標也算），以及 D-16-11（道路屬性回應的警告不算第 7 項的警告）、D-16-17（凍結清單必須與 `snapshot_mode=True` 一起給）。都不放寬任何條件 | Design Authority | 知悉 |
| NV-1 | 真實 Valhalla 伺服器的行為：`via` 型態是否只回傳一個 leg、警告出現的位置、`trace_attributes` 的 `edges` 欄位、狀態回應的欄位。全部依 API 文件與 C4 的參考原始碼寫成合成回應，沒有真實請求（CL-R1-1；本 run 沒有網路授權） | acceptor（真實請求的授權）；之後的整合驗收 | **NOT VERIFIED／NOT RUN** |

## 8. Audit status

- Formal：本 Ticket 的 independent audit（R1）是必要的（治理 §4.1；Bindings 第 5 節）。尚未派工；派工由 Orchestrator 依 Bindings 第 3.3、3.7 節進行。R1 的派工內容依 `decision-20261118-issue14-qalt1.md` 第 5 節第 7 項與 `decision-20261118-issue15-c151.md` 第 5 節第 6 項，須含那兩份 record 與 `decision-20261118-issue14-c141.md`。
- 本 worklog 的 self-verification（第 6 節）不是 audit。

## 9. Remaining work

1. **C-16-1**：Design Authority 裁決真實傳輸層的範圍與位置；依裁決實作（或記錄為之後的 Ticket），再補 E-1、E-6 的 H-1 證據。
2. **C-16-2**：Design Authority 確認 `map_data_date` 的讀法；若改為一律 `null`，修改 `_engine_info` 與 `test_dd_r1_2_engine_version_and_map_data_date`。
3. 之後：Orchestrator 核對本 Executor 的 binding，派 R1。#16 的結案與 SPEC-R1 SIA 以 #14、#15 的最終 subject 為準（CL-R1-21 第 7 項、CL-R1-24）。
4. C-16-3、C-16-4 由 Design Authority 決定是否列為 tracked item。
