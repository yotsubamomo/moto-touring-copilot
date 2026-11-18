# Worklog — Issue #16（SPEC-R1 R1-4）`routing`：路線引擎的請求與採用、共用的路線介面

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #16（SPEC-R1 R1-4），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **Cycle 2 的 rework 已完成（`022f629`，第 12 節），待 cycle 2 R1。** Cycle 1 以 Final Adjudication 結束（`ruling-20261118-issue16-c1.md`：R2-F1 targeted rework，授權 cycle 2）。pytest `2148 passed`。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure。以下為先前狀態：**R1（`audit/issue-16-c1-r1.md`）BLOCKING 的 targeted correction 已完成（`65aa00c`，第 11 節），待 R2**：R1-F1 已修正，pytest `2015 passed`。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure。以下為先前狀態：**Executor 工作完成，待 R1。** C-16-1～C-16-4 已由 `decision-20261118-issue16-c161.md` 裁決（CL-R1-25～CL-R1-27、TI-C16-3）；CL-R1-25（真實 HTTPS 傳輸層）與 CL-R1-27（道路屬性回應的警告）的修改在 `f6810d2`（第 10 節），pytest `1918 passed`。真實請求仍是 NOT RUN（NV-1）。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure。以下為先前狀態：**Executor 回報 `NEEDS_DA`。** 範圍 (a)～(f) 中不需要真實網路傳輸的部分全部完成，pytest `1843 passed`（第 6 節 E-1）。**C-16-1（blocking，範圍 (a) 的一部分）**：真實的 HTTP 傳輸層（實際把請求送到公開 Valhalla 伺服器的程式）沒有實作，因為 #14 的既有測試禁止 `routing/` 的任何模組 import 網路模組，而契約沒有寫它應該放在哪裡、或是否屬於本 Ticket；client 目前要求呼叫者傳入傳輸層。**C-16-2**：`map_data_date` 取自狀態回應的 `tileset_last_modified`，請 DA 確認這個讀法。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `bc7024b`（含已結案的 #13、#14、#15）；實作 commit **`7cb4b0cabcccb6541f395f999fe5b43e1b905e91`**（`7cb4b0c`）。CL-R1-25、CL-R1-27 的修改 commit **`f6810d2607e2f78f19020cc0ef32307dda2b23dd`**（`f6810d2`，父 commit 是 DA record 的 `2c0f662`），是 #16 的 implementation subject（取代 `7cb4b0c`）。R1-F1 的 correction commit **`65aa00c01d5ddab9a2cbbb2618ff55d3b029667c`**（`65aa00c`，父 commit 是 R1 record 的 `90efe65`），是 #16 cycle 1 的最後 implementation subject。Cycle 2 的 rework commit **`022f629f7d60996b7360687490a019c68ae86dcd`**（`022f629`，父 commit 是 FA ruling 的 `d9061c5`），是 **#16 cycle 2 的 implementation subject（cycle 2 R1 的受審 subject）**。worklog 在另外的 record-only commits |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：Issue #16 的內文。Orchestrator 提供的 scratchpad 原文檔（`issue-16-body.md`）以 `sha256sum` 重算為 `105fdc981b1087b60b419690168d205064853a1a41ccde4a6cb092b6ffa8ede1`，等於派工內容所述 run record 第 4 節的值。沒有呼叫 GitHub，沒有修改 Issue。
- **Spec**：SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md`）：第 2 節引用段落；第 4 節 DD-R1-2、CL-R1-1、**CL-R1-5～CL-R1-9**；第 5 節 R1-4 列（範圍 (a)～(f)、AC、排除、依賴、高風險類別 H-1、H-2、H-4）與 E-1～E-6。
- **DA clarifications**（全文閱讀）：
  - `decision-20261118-issue13-c131.md`：CL-R1-13（ID 樣式是 ASCII 的完整字串）。
  - `decision-20261118-issue14-c141.md`：CL-R1-14（正規化取位）、CL-R1-16、**CL-R1-17**、**CL-R1-19**（第 7.2 節：採用的檢查以原值判定；`request` 的經緯度是浮點數；`fetched_at` 不晚於實際收到回應）。
  - `decision-20261118-issue14-qalt1.md`：CL-R1-20、**CL-R1-21**（不依成因分辨或攔下 `SnapshotIntegrityError`；只經三個選取函式取得快照；`put` 與建構的錯誤向上傳遞）。
  - `decision-20261118-issue15-c151.md`：**CL-R1-24**（目標 GPX 原樣帶出、不重算、不套用引擎路線的處理、錯誤原樣傳出）。
  - `decision-20261118-issue16-c161.md`（2026-11-18，HEAD `2c0f662` 時已 commit）：**CL-R1-25**（真實 HTTPS 傳輸層在 `routing/http_transport.py`，只用 `http.client` 與 `ssl`；第 2.3～2.6 節的要求、可修改檔案的封閉清單、測試 T-1～T-10 與 evidence）、**CL-R1-26**（確認 `map_data_date` 的讀法）、**CL-R1-27**（道路屬性回應的警告使國道檢查無法驗證）、第 4.1～4.4 節（接受 D-16-8、D-16-17 的做法）、TI-C16-2、TI-C16-3。這是 DA 依治理 §5.3 第 2 類的 clarification，不是 Executor 的決定。
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
| D-16-1 | 傳輸層由呼叫者傳入：`transport(url, body_bytes, headers) -> HttpResponse`，沒有回應時拋 `TransportError`。client 負責 URL（端點＋`/route`、`/trace_attributes`、`/status`）、JSON 內容與 header（`Content-Type`、`User-Agent`），三種請求都是 POST。**（`f6810d2` 起，依 CL-R1-25）真實的 HTTPS 傳輸層是 `routing/http_transport.py` 的 `https_transport`，`valhalla_client()` 建立使用它的 client；`routing/` 的其他模組（含 `__init__.py`）不 import 它。** 先前（`7cb4b0c`）沒有提供真實傳輸層（C-16-1） | 範圍 (a)「傳輸層可替換，測試不連網」；CL-R1-9；CL-R1-25 |
| D-16-2 | 端點：模組常數 `https://valhalla1.openstreetmap.de`（與 `routing_client.py` 相同）。可以由呼叫者以 `endpoint=` 明確傳入，但只接受 `https://` 加主機（可帶埠），不可帶路徑、查詢、帳號或結尾換行。程式中沒有讀取任何環境變數的程式碼 | CL-R1-9「常數或明確傳入的設定值」；H-1 |
| D-16-3 | User-Agent 是 `route-client/1.0`。`routing_client.py` 的 `route-snapshot-check/0.1 (course project; low volume)` 帶有「course project」的描述，這裡不用 | CL-R1-9「通用的名稱，不含姓名、email 或專案名稱」 |
| D-16-4 | 路線請求只送 `locations`（每個位置只有 `lat`、`lon`、`type`）與 `routing_params()`；代號、角色與地名不送出。起點與終點的 `type` 是 `break`，中間位置是 `via`（不分段、允許迴轉），所以一個方向的回應應只有一個 leg、一條 shape；不是剛好一個 leg 時不採用（`response_malformed`）。**這是依 Valhalla API 文件的位置型態所作的選擇，真實伺服器的行為 NOT VERIFIED**（沒有真實請求，CL-R1-1） | CL-R1-5；4.14 的 `shape`（一個方向一條折線） |
| D-16-5 | `routing_params` ＝ `{"costing": "motorcycle", "costing_options": {"motorcycle": {"use_highways": 0}}, "units": "kilometers"}`，它就是快照的 `routing_params` 與 `request_key` 的 `routing_params`（R1-4 自己計算 `request_key`，呼叫者不能給不同的參數）。沒有 `exclude_*`、沒有高度 | CL-R1-5；P-1；Q-3 第 7 項；4.14「快照記錄實際送出的值」 |
| D-16-6 | RouteLeg 的 `request` ＝ `{"locations": [{ref_id, role, lat, lon, type}...], "routing_params": ...}`，依這個方向的順序；經緯度是 `float` | 4.14 `request`；CL-R1-5；CL-R1-19 第 2 項 |
| D-16-7 | 道路屬性查詢只送 `encoded_polyline`（引擎自己回傳的 shape）、`costing`、`shape_match: walk_or_snap`、`filters`（`edge.names`、`edge.length`、`edge.road_class`）。與 C4 的做法相同 | 7.11 第 5 項「只送出引擎自己回傳的折線」 |
| D-16-8 | 國道訊號（任一個就是 `fail`）：trip 或 leg summary 的 `has_highway` 為 true（或是非布林的真值）；任何轉向的 `highway` 不是 `None`／`False`；道路屬性任何一段的 `road_class` 是 `motorway`（只要出現，不論長度）；轉向的 `begin_street_names`／`street_names` 或道路屬性的 `names` 中有名稱符合 `國道\|高速公路\|freeway`（不分大小寫）。比字面略嚴：`Freeway` 不分大小寫、motorway 以出現判定（S39「含 `motorway` 路段」）、leg summary 的旗標也算。都是 fail closed 方向。**DA 接受：`decision-20261118-issue16-c161.md` 第 4.1～4.3 節** | 7.11 第 5 項；修正 B（訊號矛盾時 fail closed）；H-4 |
| D-16-9 | 無法驗證（沒有訊號時不產生 `freeway_check`）：trip summary 沒有布林值的 `has_highway`；道路屬性查詢 HTTP 不是 200、沒有回應、`edges` 不是非空清單、任何一段的 `length` 不是非負有限數、`road_class` 不是字串、`names` 不是字串清單；長度不符；路線回應中檢查需要的欄位讀不到（`response_malformed`） | 7.11 第 5 項；4.14 `has_highway`、`freeway_check` |
| D-16-10 | 2% 的判定：`|Σ edge.length − trip.summary.length| ≤ trip.summary.length × 0.02`，全部以 `Decimal(repr(x))` 精確計算，不用浮點數、不用存入快照的整數公尺（CL-R1-19 第 1 項） | 7.11 第 5 項第 (1) 款；CL-R1-19 |
| D-16-11 | 警告：回應最上層或 `trip` 中的 `warnings` 有任何項目（形式正確與否），或不是清單，就不採用。**（`f6810d2` 起，依 CL-R1-27）道路屬性查詢回應最上層的 `warnings` 存在而且不是空清單（含不是清單的任何值）時，國道檢查無法驗證（原因 `trace_warnings`），沒有國道訊號時是 `routing_unavailable`；同一回應中的國道訊號照樣收集，有訊號時是 `highway_in_route`；`null`、不存在、空清單沒有影響；它不寫入 RouteLeg 的 `warnings`；狀態回應的警告不影響採用。`FREEWAY_CHECK_METHOD` 改為 `valhalla-trace_attributes-v2`，文字加上「a road attribute reply without warnings」。** 先前（`7cb4b0c`）：道路屬性回應的警告不算（DA 不接受） | 7.11 第 5、7 項；CL-R1-27 |
| D-16-12 | 偏移（CL-R1-7）：起點、終點用 haversine（`ingest.segments.haversine_m`，地球半徑 6,371,000 m）到折線的第一點、最後一點；中間位置是到每個線段的最近點，在以該位置為中心的局部平面上計算（點到線段），最近點相同時取第一個線段；沿線里程＝之前各段的 haversine 長度加上最近線段的比例。判定 `≤ 200 m`（以計算出的原值），沿線里程**嚴格**遞增 | CL-R1-7；CL-R1-19 第 1 項；7.11 第 8 項 |
| D-16-13 | `distance_m` ＝ `trip.summary.length`（km）×1000、`engine_time_s` ＝ `trip.summary.time`，都以最短十進位表示 `ROUND_HALF_UP` 取整數；`road_names` 依 CL-R1-6（每個轉向的 `begin_street_names` 再 `street_names`，第一次出現的順序、去重複；空字串略過，不是字串時 `response_malformed`） | 4.14；CL-R1-6；CL-R1-18 的取整原則（同一種「四捨五入」） |
| D-16-14 | `fetched_at` ＝ client 在傳輸層回傳之後立刻讀取的時鐘，轉成 +08:00、捨去到秒（`replace(microsecond=0)`），是路線回應（不是道路屬性查詢）的收到時間 | CL-R1-19 第 3 項；4.14 `fetched_at` |
| D-16-15 | 請求次數與順序（CL-R1-5、CL-R1-8）：每個方向送一次路線請求；回應有可解碼的 shape 時，**即使其他檢查已不通過**也送一次道路屬性查詢，以取得全部國道訊號。來回行程的兩個方向都送出並檢查；只有在某個請求完全沒有回應（`TransportError`）時停止後續的請求，其餘方向記為 `not_sent`。不重試。兩個方向都通過之後才送一次狀態請求，然後組成快照並存檔 | CL-R1-5；CL-R1-8 |
| D-16-16 | 引擎資訊（DD-R1-2）：`engine_name` ＝ `Valhalla`；`engine_version` ＝ 狀態回應的 `version`（非空字串），沒有回報、HTTP 錯誤、不是 JSON 或沒有回應時 ＝ `unreported`；`map_data_date` ＝ 狀態回應的 `tileset_last_modified`（Unix 秒，整數）在 +08:00 的日期，沒有回報或格式不對時 ＝ `null`，不以取得日期代替。這個日期是引擎回報的「圖磚最後修改日期」，不是 OpenStreetMap 資料的擷取日期。**DA 確認：CL-R1-26**，程式不需要修改 | DD-R1-2；4.14 `map_data_date`；C4 記錄的欄位；CL-R1-26 |
| D-16-17 | 取得順序（範圍 (e)）：Snapshot Mode（`snapshot_mode=True`）只呼叫 `select_snapshot_mode`，或在給了凍結清單時只呼叫 `select_strict`，不使用 client；一般模式先 `find_reusable`，沒有時才呼叫引擎；引擎失敗或任何方向不通過時回傳 `RouteFailure`，不改用任何快照。凍結清單只能與 `snapshot_mode=True` 一起給，否則 `ValueError`（不在一般模式下默默忽略清單）。**DA 接受：`decision-20261118-issue16-c161.md` 第 4.4 節** | 7.11 第 3 項；CL-R1-4；lead 寫定「指定了凍結清單就是嚴格模式」 |
| D-16-18 | 存放的例外都不攔下（CL-R1-17、CL-R1-21）：`find_reusable`、`select_snapshot_mode`、`select_strict`、`SnapshotStore.put` 的例外原樣向上傳遞；只有 `put` 成功後才回傳路線，回傳的是 `put` 回來的快照（內容相同時是既有檔案，保留它自己的 `fetched_at`）。從已驗證的快照解碼 shape 失敗時拋 `SnapshotIntegrityError`（訊息只含 `snapshot_id`），不是路線錯誤代碼 | CL-R1-17；CL-R1-21；7.11 第 1、3 項 |
| D-16-19 | 共用介面（範圍 (f)）：`AdoptedRoute(route_id, route_source, trip_type, snapshot_id, target_gpx_ref, turnaround_m, turnaround_source, legs)`，`AdoptedLeg(direction, points, distance_m, road_names)`；`RouteFailure(code, case, reasons)`，`reasons` 只是 `方向:代碼` 的字串。`routing`：幾何是各方向自己的 shape 解碼後的點（不反轉）、里程是快照的整數公尺。`target_gpx`：原樣帶出 R1-3 的結果（點是同一組物件、長度是 `length_m` 原值、道路名稱是空的 tuple、`snapshot_id` 是 `None`），錯誤的 `code`、`case` 原樣，`TripTypeRequiredError`、`ValueError`、`TypeError` 照原樣傳出 | 範圍 (f)；CL-R1-24 |
| D-16-20 | 一般模式在開始時就檢查請求位置：方向的集合必須剛好是行程型態的方向，每個方向至少兩個位置，每個位置的代號、角色是非空字串，經緯度是有限的數字且在 ±90／±180 內。錯誤訊息不含座標。位置與 `request_key` 的地點（`origin`、`destination`、`via`）是否對應不檢查（C-16-3；DA 維持，列為 TI-C16-3） | CL-R1-5；CL-R1-9 |
| D-16-21 | 新模組不 log、不 `print`；原始碼不含 `environ`／`getenv`。只有 `http_transport.py` import `http.client` 與 `ssl`（`f6810d2` 起），其他模組不 import 任何網路模組（修改後的 #14 靜態測試以遞迴掃描證明） | CL-R1-9；H-1、H-2；CL-R1-25 |
| D-16-22 | （`f6810d2`）傳輸層的逾時 `TIMEOUT_S = 30.0` 秒（模組常數，傳給 `HTTPSConnection`，同時用於連線與每次讀取）。理由：公開伺服器的路線請求在 C4 的參考原始碼中以 90 秒為上限；本專案每次規劃最多五個請求，30 秒足以涵蓋正常回應而不讓介面長時間等待；不從環境或設定檔讀取 | CL-R1-25 第 2 項 (e) |
| D-16-23 | （`f6810d2`）傳輸層的 URL 檢查：`https://` 加主機（規則同 `valhalla.py` 的 `_ENDPOINT`）、可選的埠（1～65535）加 `/route`、`/trace_attributes` 或 `/status`，以 `re.fullmatch` 判定；不符合時在建立連線之前 `ValueError`。header 必須是 `Content-Type`、`User-Agent` 的子集，值是字串；本文必須是 `bytes`。所有失敗在 `except` 區塊之外以 `from None` 拋出，`__cause__`、`__context__` 都是 `None` | CL-R1-25 第 2 項 (c)、第 3、4 項 |

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
- （`7cb4b0c` 時的限制，已由 `f6810d2` 解決）先前真實傳輸層不存在（C-16-1），「不跟隨 HTTP 轉址」「不使用環境變數中的代理」當時 NOT VERIFIED。`f6810d2` 起由 T-1～T-4、T-7 證明，見第 10.6 節。

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
| **C-16-1**（blocking，範圍 (a) 的一部分） | **真實的 HTTP 傳輸層沒有實作。** 範圍 (a) 是「公開 Valhalla 伺服器的 client（…；傳輸層可替換，測試不連網）」。#14 的既有測試 `test_the_routing_package_imports_no_network_or_environment_modules`（`tests/test_routing_store.py`，派工禁止修改）對 `routing/` 的每一個頂層 `.py` 禁止 import `socket`、`http`、`urllib`、`requests`、`httpx`、`ssl`、`subprocess`；任何真實的 HTTP 傳輸都需要其中之一。契約沒有寫真實傳輸層是否屬於本 Ticket，也沒有寫它的位置。可行的做法：(i) 放在 `routing/` 的子套件（例如 `routing/transport/http.py`）：該測試的 `glob("*.py")` 不遞迴，所以不會掃到；但這等於繞過那個測試的字面，Executor 不自行採用；(ii) 修改 #14 的測試，明定只有一個指名的傳輸模組可以 import 網路模組（需要修改 #14 測試的授權）；(iii) 放在 `routing/` 以外的套件（超出派工可修改的範圍）；(iv) 判定真實傳輸層屬之後的整合 Ticket（與 R1-3 的「CLI 的接線」同類），R1-4 只交付可替換傳輸層的 client。無論哪一種，真實傳輸層都要：不跟隨 HTTP 轉址、不使用環境變數中的代理（H-1「不可被轉向」）、設定逾時、把連線失敗轉成 `TransportError`、錯誤訊息不含請求內容 | Design Authority（契約的範圍與位置；若選 (ii)，DA 判定是否需要其他授權） | **已裁決：CL-R1-25**（做法 (ii)，`decision-20261118-issue16-c161.md` 第 2 節）；`f6810d2` 實作（第 10 節） |
| **C-16-2**（需要確認） | `map_data_date` 取自 Valhalla 狀態回應的 `tileset_last_modified`（圖磚建置的時間，Unix 秒）在 +08:00 的日期（D-16-16）。另一種合理讀法是 Valhalla 沒有回報「圖資日期」本身，所以一律 `null`。這個值在快照的雜湊範圍內，決定 `snapshot_id`；目前沒有任何已存的快照，改變不影響既有資料 | Design Authority | **已確認：CL-R1-26**（第 3 節）；程式與測試不需修改，只改 docstring |
| C-16-3（tracked item 建議） | R1-4 不檢查各方向的請求位置與 `request_key` 的地點（`origin`、`destination`、`via` 的代號）是否對應：組成規則屬 G-RREQ（7.11 第 2 項的去程／回程組成、公路的進入端與另一端）。呼叫者若給了不一致的兩者，快照會存在不對應的鍵下，之後被一般模式或 Snapshot Mode 重用（H-4 的重用風險）。建議 G-RREQ 的 derivation 決定由哪一層核對 | Design Authority（G-RREQ 的 derivation） | **TI-C16-3**（第 5 節）；不要求 #16 修改 |
| C-16-4（知悉） | D-16-8 的三處比字面嚴格（`Freeway` 不分大小寫、`motorway` 以出現判定、leg summary 的旗標也算），以及 D-16-11（道路屬性回應的警告不算第 7 項的警告）、D-16-17（凍結清單必須與 `snapshot_mode=True` 一起給）。都不放寬任何條件 | Design Authority | 第 4.1～4.4 節接受；D-16-11 不接受，改為 **CL-R1-27**（第 4.5 節），`f6810d2` 實作 |
| NV-1 | 真實 Valhalla 伺服器的行為：`via` 型態是否只回傳一個 leg、警告出現的位置、`trace_attributes` 的 `edges` 欄位、狀態回應的欄位。全部依 API 文件與 C4 的參考原始碼寫成合成回應，沒有真實請求（CL-R1-1；本 run 沒有網路授權） | acceptor（真實請求的授權）；之後的整合驗收（`decision-20261118-issue16-c161.md` 第 2.7 節：不在 R1-4，也不在 SPEC-R1） | **NOT VERIFIED／NOT RUN**（`f6810d2` 後維持） |

## 8. Audit status

- Formal：本 Ticket 的 independent audit（R1）是必要的（治理 §4.1；Bindings 第 5 節）。尚未派工；派工由 Orchestrator 依 Bindings 第 3.3、3.7 節進行。R1 的派工內容依 `decision-20261118-issue14-qalt1.md` 第 5 節第 7 項與 `decision-20261118-issue15-c151.md` 第 5 節第 6 項，須含那兩份 record 與 `decision-20261118-issue14-c141.md`。
- 本 worklog 的 self-verification（第 6 節）不是 audit。

## 9. Remaining work

1. （`f6810d2` 後）Orchestrator 核對本 Executor 的 binding，派 R1；R1 的派工內容依 `decision-20261118-issue16-c161.md` 第 7 節末段須含該 record 與 `decision-20261118-issue14-c141.md`、`decision-20261118-issue14-qalt1.md`、`decision-20261118-issue15-c151.md`。
2. #16 的結案與 SPEC-R1 SIA 以 #14、#15 的最終 subject 為準（CL-R1-21 第 7 項、CL-R1-24）；SIA 以 #16 的最終 subject 核對 R1-2 的「不需要網路」，因為 #14 的那個靜態測試在 #16 中被修改（`decision-20261118-issue16-c161.md` 第 8 節）。
3. 不在本 Ticket：TI-C16-2、TI-C16-3（Design Authority）；NV-1 與第一次真實請求（之後的整合驗收，需要 acceptor 的授權）；RV-12～RV-14（文件同步）。
4. 先前的 C-16-1、C-16-2 已由 CL-R1-25、CL-R1-26 處理（第 7 節），C-16-3、C-16-4 已有 disposition。

## 10. CL-R1-25、CL-R1-27 的實作（`decision-20261118-issue16-c161.md`；subject `f6810d2`）

### 10.1 Contract reference、角色與 binding

- 依據：`decision-20261118-issue16-c161.md`（v1，HEAD `2c0f662`）第 2.3～2.6 節（CL-R1-25）、第 3 節（CL-R1-26）、第 4.5 節（CL-R1-27）、第 7 節（對 #16 的要求）。Orchestrator 於同一 Executor 派工中以訊息轉達，要求全文閱讀，特別是第 2.4～2.6 節與第 8 節；已全文閱讀。
- 角色與 binding：同第 2 節（agentId `a1e2cfa52290d496f`，`gov-executor`）。Executor 自行觀測（`f6810d2` 之後、寫本節之前）：(`claude-opus-5-5`, `high`) 168 則，集合只有一個元素。**這是自我觀測，不是派工者的核對。** 沒有使用 bounded assignments，沒有派工任何 subagent。

### 10.2 Work performed

1. 新建 `src/moto_copilot/routing/http_transport.py`（CL-R1-25 第 1～5 項）：`https_transport(url, body, headers)`、`valhalla_client(*, endpoint=VALHALLA_ENDPOINT, clock=None)`、`TIMEOUT_S`、`PATHS`、`ALLOWED_HEADERS`。只 import `http.client`、`re`、`ssl`、`collections.abc`、`datetime` 與 `.valhalla`。
2. `adoption.py`（CL-R1-27）：`_trace_facts` 加上道路屬性回應 `warnings` 的檢查（新原因 `trace_warnings`，列入無法驗證的原因）；`FREEWAY_CHECK_METHOD` 改為 v2 並加上條件；模組說明中第 (1) 款與 7.11 第 7 項的描述。
3. `valhalla.py`、`source.py`：只改 docstring（第 2.4 節第 5、6 列）。
4. `tests/test_routing_store.py`：只改 `test_the_routing_package_imports_no_network_or_environment_modules` 一個函式（第 10.5 節）。
5. `tests/test_routing_engine.py`：`NEW_MODULES` 加入 `http_transport`，靜態測試對它只放寬 `http`、`ssl`；`FREEWAY_CHECK_METHOD` 的文字檢查加上新條件；新增 CL-R1-27 的 5 個測試函式（12 個案例）。
6. 新建 `tests/test_routing_transport.py`（19 個測試函式，63 個案例；T-1～T-9）。
7. 自我驗證：全套 pytest、33 個突變檢查（第 10.7 節）、相對 `7cb4b0c` 的 diff 範圍。
8. 依 SA-1 本機 commit `f6810d2`；暫存的只有上列 7 個檔案。沒有 push、沒有碰 GitHub；沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有執行 `experiments/`；沒有發出任何網路請求。

### 10.3 Artifacts（`7cb4b0c` → `f6810d2`）

| 檔案 | 變更 | 封閉清單（第 2.4 節） |
| --- | --- | --- |
| `src/moto_copilot/routing/http_transport.py` | 新檔 | 第 1 列 |
| `tests/test_routing_store.py` | 一個函式（一個 diff hunk） | 第 2 列 |
| `tests/test_routing_engine.py`、`tests/test_routing_transport.py`（新檔） | 測試 | 第 3 列 |
| `src/moto_copilot/routing/adoption.py` | CL-R1-27 | 第 4 列 |
| `src/moto_copilot/routing/source.py` | 只有 docstring（`_engine_info` 引用 CL-R1-26 與「圖磚最後修改日期」；`get_route` 引用第 4.4 節） | 第 5 列 |
| `src/moto_copilot/routing/valhalla.py` | 只有模組說明的「Transport」段 | 第 6 列 |

沒有修改 `canonical.py`、`request_key.py`、`snapshot.py`、`store.py`、`target_gpx.py`、`__init__.py`、`contracts/`、`ingest/`、`tests/routing_synthetic.py`、`tests/test_routing_snapshot.py`、`tests/test_target_gpx.py`、`pyproject.toml`。

### 10.4 E-1 pytest（subject `f6810d2`）

`.venv/Scripts/python.exe -m pytest -q`，在 commit 之後、工作目錄乾淨時執行，exit 0，完整輸出：

```text
........................................................................ [  3%]
........................................................................ [  7%]
........................................................................ [ 11%]
........................................................................ [ 15%]
........................................................................ [ 18%]
........................................................................ [ 22%]
........................................................................ [ 26%]
........................................................................ [ 30%]
........................................................................ [ 33%]
........................................................................ [ 37%]
........................................................................ [ 41%]
........................................................................ [ 45%]
........................................................................ [ 48%]
........................................................................ [ 52%]
........................................................................ [ 56%]
........................................................................ [ 60%]
........................................................................ [ 63%]
........................................................................ [ 67%]
........................................................................ [ 71%]
........................................................................ [ 75%]
........................................................................ [ 78%]
........................................................................ [ 82%]
........................................................................ [ 86%]
........................................................................ [ 90%]
........................................................................ [ 93%]
........................................................................ [ 97%]
..............................................                           [100%]
1918 passed in 42.16s
```

`1843`（`7cb4b0c`）＋ `12`（CL-R1-27）＋ `63`（傳輸層）＝ `1918`。`grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。測試後 `git status --short` 為空。

### 10.5 E-2、E-4、E-5

**E-2 新增的列**（測試檔：`tests/test_routing_transport.py`，除非另寫）

| AC／條文 | 測試 | 結果 |
| --- | --- | --- |
| 範圍 (a) 真實傳輸層；T-1 轉址 | `test_t1_a_redirect_is_returned_as_it_is_and_not_followed[301/302/303/307/308]`（真實 `http.client` 寫入記憶體中的 socket；一個連線、一個請求、主機不變）、`test_t1_a_redirected_route_request_is_routing_unavailable_with_no_snapshot` | PASS |
| T-2 代理與環境變數 | `test_t2_proxies_and_endpoint_variables_do_not_change_the_connection`（新的直譯器；8 個代理變數（大小寫）與 5 個端點類變數；主機是 `valhalla1.openstreetmap.de`、埠是預設、沒有 `set_tunnel`） | PASS |
| T-3 TLS | `test_t3_tls_verification_is_on`、`test_t3_the_transport_has_no_switch_for_tls_or_proxies` | PASS |
| T-4 逾時 | `test_t4_the_timeout_is_the_fixed_constant`、`test_t4_a_timeout_is_a_transport_error` | PASS |
| T-5 失敗的轉換 | `test_t5_every_failure_is_a_transport_error_without_content`（建構、`request`、`getresponse`、`read` × `OSError`、`ConnectionRefusedError`、`ssl.SSLError`、`RemoteDisconnected`、`IncompleteRead` ＝ 20 個案例；錯誤訊息本身含合成座標字串，traceback 中沒有它；`__cause__`、`__context__` 都是 `None`；一個連線、已關閉）、`test_t5_a_failure_through_the_client_keeps_positions_out_of_the_message` | PASS |
| T-6 內容與 header | `test_t6_the_wire_request_is_a_post_with_the_given_body_and_only_the_listed_headers[/route,/trace_attributes,/status]`（線上的位元組：`POST <path> HTTP/1.1`；header 只有 `Host`、`Accept-Encoding`、`Content-Length`、`Content-Type`、`User-Agent`；本文相同）、`test_t6_the_client_requests_reach_the_wire_unchanged`、`test_t6_headers_outside_the_closed_list_are_refused_before_connecting`、`test_t6_the_body_must_be_bytes` | PASS |
| T-7 URL 的拒絕 | `test_t7_urls_other_than_the_three_actions_are_refused_before_connecting`（13 種）、`test_t7_an_explicit_port_is_used` | PASS |
| T-8 HTTP 錯誤狀態 | `test_t8_http_error_statuses_are_replies_not_exceptions`（400、404、429、500、503） | PASS |
| T-9 建立方式 | `test_t9_valhalla_client_uses_the_real_transport_and_the_default_endpoint`、`test_t9_a_round_trip_through_the_real_transport_equals_the_fake_engine`（結果與兩個存放目錄的檔案位元組都與 `FakeEngine` 相同）、`test_importing_the_routing_package_does_not_load_the_transport` | PASS |
| T-10 靜態 | `tests/test_routing_store.py::test_the_routing_package_imports_no_network_or_environment_modules`、`tests/test_routing_engine.py::test_the_new_modules_do_not_read_env_log_print_or_import_network_modules` | PASS |
| 「另加：端點不受環境變數影響」 | 第 6 節 E-2 原列，加上 T-1～T-4、T-7 | PASS |
| 「另加：請求的 User-Agent 與內容不含個人識別資訊」 | 第 6 節 E-2 原列，加上 T-5、T-6 | PASS |
| CL-R1-27（`tests/test_routing_engine.py`） | `test_cl_r1_27_a_road_attribute_reply_with_warnings_is_unverifiable`（一筆、多筆、形式不正確、字串、物件、空物件；`routing_unavailable`、不產生 `freeway_check`、沒有快照、請求次數不變）、`test_cl_r1_27_warnings_with_a_freeway_signal_are_still_highway_in_route`（`motorway`、國道名稱）、`test_cl_r1_27_empty_or_null_warnings_in_the_road_attribute_reply_change_nothing`、`test_cl_r1_27_warnings_only_in_the_return_road_attribute_reply_store_nothing`、`test_cl_r1_27_status_reply_warnings_do_not_affect_adoption` | PASS |
| DD-R1-2 | 第 6 節 E-2 原列，改為引用 CL-R1-26（讀法確認，程式與測試不變） | PASS |

**E-4。** 傳輸層的測試以替身取代 `http.client.HTTPSConnection`：`Scripted`（記錄建構參數、`request`、`set_tunnel`、`close`，依腳本回答或在指定階段拋出）與 `Wire`（真實的 `HTTPSConnection`，只替換 `connect`，讓 `http.client` 自己把請求寫進記憶體中的 socket 並解析預先寫好的回應）。本檔 autouse fixture 照 E-4 封鎖 `socket.socket`、`socket.create_connection`、`socket.getaddrinfo`。T-2 與套件載入測試的子行程以替身連線執行。沒有任何網路請求。

**E-5（`tests/test_routing_store.py` 的修改，`decision-20261118-issue16-c161.md` 第 2.2、2.4 節）。** 只改 `test_the_routing_package_imports_no_network_or_environment_modules` 一個函式（名稱保留）：
1. `glob("*.py")` 改為 `rglob("*.py")`：子套件不能繞過（理由：第 2.2 節不採用做法 (i)）。
2. 只有路徑恰為 `routing/http_transport.py` 的檔案可以 import `http` 與 `ssl`；它仍不得 import `socket`、`urllib`、`requests`、`httpx`、`subprocess`；其他檔案照舊全部禁止（理由：CL-R1-25 第 1 項）。
3. 斷言 `http_transport.py` 存在，並且在掃描的清單中（豁免不能指向不存在的檔案）。
4. 斷言其他檔案沒有 import `http_transport`：`import ...http_transport`、`from .http_transport import …`、`from . import http_transport`、絕對路徑，以及字串參數含 `http_transport` 的 `__import__`／`import_module` 呼叫。
5. `environ`／`getenv` 的禁止照舊適用於全部檔案，含 `http_transport.py`。
該檔的其他測試沒有改（`git diff 7cb4b0c f6810d2 -- tests/test_routing_store.py` 只有一個 hunk）。R1-2 AC「快照與 `request_key` 的計算不需要網路」仍由這個測試（更嚴的形式）與 `test_hashing_storage_and_selection_need_no_network`（執行期封鎖 socket）證明；另有 `test_importing_the_routing_package_does_not_load_the_transport` 證明 `import moto_copilot.routing` 不載入傳輸層。

### 10.6 E-6

**H-1（第 2.3 節第 2 項）**

| 項目 | 實作 | 測試 |
| --- | --- | --- |
| (a) 不跟隨轉址 | 每次呼叫一個 `HTTPSConnection`、一個 `request`；3xx 原樣回傳；client 不採用非 200 | T-1（含經 `get_route` 的 `routing_unavailable`） |
| (b) 不使用代理 | 不呼叫 `set_tunnel`；沒有讀環境變數的程式；不用 `urllib.request` | T-2、T-3（`tunnel is None`）、T-10 |
| (c) 只連到 URL 指定的主機 | `_target` 以 `re.fullmatch` 再檢查 URL，主機與埠只來自它；不符合時在建立連線之前 `ValueError` | T-7、T-2、T-1 |
| (d) TLS 驗證不得關閉 | `ssl.create_default_context()`；沒有任何關閉驗證或換憑證的參數 | T-3 |
| (e) 逾時 | `TIMEOUT_S = 30.0`，傳給 `HTTPSConnection`；不重試 | T-4、T-5（一個連線） |

`git ls-files` 不含 `.env`、`*.key`、`data/`、`.gpx`、`.fit`（0 筆）；diff 中沒有金鑰字串。

**H-2**：T-5（錯誤訊息與 traceback 不含合成座標字串與請求本文）、T-6（本文原樣、header 只有封閉清單加 `http.client` 自動的三項）。diff 中的座標全部是第 6 節 E-3 的合成值；新測試用的主機名稱是 `.invalid` 保留網域或 `engine.example`。

**H-4**：3xx（T-1）、傳輸失敗（T-5）與 CL-R1-27 的道路屬性警告都不被採用；國道訊號在 CL-R1-27 的情形下仍優先（`test_cl_r1_27_warnings_with_a_freeway_signal_are_still_highway_in_route`）。

### 10.7 突變檢查（第 2.6 節第 8 項）

腳本 `mutate16b.py`（session scratchpad）在記憶體中替換原始碼字串後執行 `tests/test_routing_engine.py`、`tests/test_routing_transport.py`、`tests/test_routing_store.py`，在 `finally` 中**以原本的位元組**寫回（不以 git 還原）；N8 移動檔案到子套件後再移回並刪除子套件。結束時 `routing/` 下全部 `.py` 的 SHA-256 與開始時相同（`sources restored: True`），之後 `git status --short` 只有本次尚未 commit 的修改。33 個突變全部被抓到：

| # | 突變 | 失敗 |
| --- | --- | --- |
| N1 | 改用 `urllib.request.urlopen` | 39 |
| N2a | `check_hostname = False` | 2 |
| N2b | `check_hostname = False` 加 `CERT_NONE` | 2 |
| N3 | 3xx 時再送一次請求到另一主機 | 6 |
| N4 | 失敗後重試一次 | 22 |
| N5 | 例外不加 `from None`，訊息含本文 | 20 |
| N6 | `source.py` import `http_transport` | 2 |
| N7 | `__init__.py` import `http_transport` | 2 |
| N8 | `http_transport.py` 移到子套件 `routing/transport/` | 2 個 collection error（其他測試檔 import 它）；另以只執行該靜態測試確認：`assert transport.is_file()` 失敗 |
| N9 | 忽略道路屬性回應的警告（CL-R1-27） | 9 |
| M1～M23 | 第 6 節 E-6 的 23 個突變，在新程式上重跑 | 全部被抓到（每個 1～10） |

### 10.8 Diff 與未執行的項目

- 相對 `7cb4b0c` 的 diff 只含第 10.3 節的 7 個檔案，內容符合封閉清單（`valhalla.py`、`source.py` 只有 docstring；`test_routing_store.py` 只有一個函式）。
- **真實請求：NOT RUN。** NV-1 維持 NOT VERIFIED／NOT RUN（`decision-20261118-issue16-c161.md` 第 2.7 節：不在 R1-4，也不在 SPEC-R1）。真實伺服器上 TLS、轉址與回應形狀的實際行為沒有觀測。
- Python 3.13 以後的直譯器：NOT RUN（本機只有 3.11.2／3.12）。

### 10.9 Audit status

同第 8 節：R1 必要，尚未派工；本節的 self-verification 不是 audit。

## 11. R1-F1 的 targeted correction（audit `issue-16-c1-r1.md`；subject `65aa00c`）

### 11.1 Finding 與契約

- **R1-F1（Medium，blocking，owner #16 Executor）**：`f6810d2` 的 `adoption.py` 遇到 HTTP 狀態不是 200 的路線回應時，在呼叫 `_route_facts` 之前就回傳沒有訊號的 `engine_error`；遇到不是 200 的道路屬性回應時只加 `trace_failed`，沒有執行 `_trace_facts`。本文中可讀的國道訊號（`has_highway: true`、`motorway`、國道名稱）因此遺失，結果是 `routing_unavailable` 而不是 `highway_in_route`，違反 CL-R1-8「先檢查所有可取得的國道訊號，再決定代碼」。
- 修正的要求（audit record 第 2 節 Required fix；Orchestrator 派工）：回應是否成功與訊號的收集分開；非 200 仍記 `engine_error`／`trace_failed`、永不採用；決定代碼前收集本文所有可讀的國道訊號；不跟隨轉址、不重試、不採用錯誤回應、不存快照；加入三類回歸案例，確認沒有訊號的非 200 仍是 `routing_unavailable`、200 的既有行為不變；讀不到或不是 JSON 的非 200 本文仍是 `routing_unavailable` 而且不拋例外。
- 角色與 binding：同第 2 節（agentId `a1e2cfa52290d496f`，`gov-executor`）。Executor 自行觀測（`65aa00c` 之後、寫本節之前）：(`claude-opus-5-5`, `high`) 197 則，集合只有一個元素。**這是自我觀測，不是派工者的核對。** 沒有使用 bounded assignments，沒有派工任何 subagent。

### 11.2 修改（`90efe65` → `65aa00c`；只有 `adoption.py` 與 `tests/test_routing_engine.py`）

| # | 決定 | 依據 |
| --- | --- | --- |
| D-16-24 | 路線回應：狀態不是 200 或本文沒有 `trip` 物件時，結果一律是 `engine_error`、`leg = None`（永不採用）。本文是物件而且有 `trip` 物件時（不論狀態），先以 `_route_facts` 收集其中的國道訊號（`has_highway`、轉向的 highway 旗標、轉向的國道名稱），有訊號時 `freeway_check = "fail"`。這個回應不作為任何後續請求的依據：**不以錯誤回應的 shape 送道路屬性查詢**（CL-R1-5 的一次查詢是對可採用的路線回應；錯誤回應的 shape 不是可採用的路線） | CL-R1-8；R1-F1 |
| D-16-25 | 道路屬性回應：狀態不是 200 時仍記 `trace_failed`（無法驗證）；本文是物件時以 `_trace_facts` 收集其中的國道訊號（`motorway`、國道名稱），它的其他原因（長度、警告）不另外列入，因為查詢已經是失敗 | CL-R1-8；R1-F1；CL-R1-27 不受影響 |
| D-16-26 | **〔已被第 12 節取代：本列對 `65aa00c` 不成立。〕** 原文：「讀不到的本文（不是 JSON、不是物件、`trip` 或 `edges` 的形狀不對、欄位型別錯誤）只得到 `engine_error`／`trace_failed` 與能讀到的訊號，不拋例外；結果是 `routing_unavailable`（除非讀到國道訊號）」。更正：在 `65aa00c`，`trip.summary.length`、`trip.summary.time` 或 `edges[n].length` 是絕對值超出浮點範圍的整數（例如 `10**400`）時，`_real` 的 `math.isfinite` 拋 `OverflowError`，HTTP 200 與非 200 都是未捕捉的例外（R2-F1，`audit/issue-16-c1-r2.md`；`ruling-20261118-issue16-c1.md`）。本列的陳述自 cycle 2 的 subject `022f629` 起才成立（D-16-27） | R1-F1 Required fix；H-4；R2-F1 |

模組說明補上「非 200 的回應永不採用，但本文中可讀的國道訊號照樣收集」。`source.py`、`valhalla.py`、`http_transport.py` 與其他檔案沒有修改（`git diff --stat 90efe65 65aa00c`：2 files changed, 128 insertions(+), 3 deletions(-)）。

### 11.3 E-1 pytest（subject `65aa00c`）

`.venv/Scripts/python.exe -m pytest -q`，在 commit 之後、工作目錄乾淨時執行，exit 0，完整輸出：

```text
........................................................................ [  3%]
........................................................................ [  7%]
........................................................................ [ 10%]
........................................................................ [ 14%]
........................................................................ [ 17%]
........................................................................ [ 21%]
........................................................................ [ 25%]
........................................................................ [ 28%]
........................................................................ [ 32%]
........................................................................ [ 35%]
........................................................................ [ 39%]
........................................................................ [ 42%]
........................................................................ [ 46%]
........................................................................ [ 50%]
........................................................................ [ 53%]
........................................................................ [ 57%]
........................................................................ [ 60%]
........................................................................ [ 64%]
........................................................................ [ 67%]
........................................................................ [ 71%]
........................................................................ [ 75%]
........................................................................ [ 78%]
........................................................................ [ 82%]
........................................................................ [ 85%]
........................................................................ [ 89%]
........................................................................ [ 92%]
........................................................................ [ 96%]
.......................................................................  [100%]
2015 passed in 38.98s
```

`.venv/Scripts/python.exe -m pytest -q -rxX`，exit 0，摘要：

```text
.......................................................................  [100%]
2015 passed in 39.18s
```

`1918`（`f6810d2`）＋ `97`（R1-F1 的回歸案例）＝ `2015`。`grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。測試後 `git status --short` 為空。`git ls-files` 不含 `data/`、`.gpx`、`.fit`、`.env`、`*.key`（0 筆）。

### 11.4 E-2：R1-F1 的 coverage（`tests/test_routing_engine.py`）

| 情形 | 測試 | 結果 |
| --- | --- | --- |
| 非 200 的路線回應帶 `has_highway: true`、國道名稱、highway 旗標（狀態 302、400、429、500、503） | `test_r1_f1_a_non_200_route_reply_with_a_freeway_signal_is_highway_in_route`（15 個案例；經 `get_route` 的來回行程：`highway_in_route`，reasons 含訊號與 `engine_error`，沒有路線、沒有快照；請求是 `route`、`route`、`trace_attributes`：錯誤回應不送道路屬性查詢、另一方向照送、沒有狀態請求） | PASS |
| 非 200 的道路屬性回應帶 `motorway`、`Freeway` 名稱、`國道` 名稱（同上 5 種狀態） | `test_r1_f1_a_non_200_road_attribute_reply_with_a_freeway_signal_is_highway_in_route`（15 個案例；reasons 含訊號與 `trace_failed`；沒有重試、沒有狀態請求、沒有快照） | PASS |
| 兩方向各一種：去程道路屬性 503 帶 `motorway`、回程路線 500 | `test_r1_f1_a_non_200_trace_with_a_signal_in_one_direction_and_an_error_route_in_the_other` | PASS |
| 非 200、沒有訊號 → 仍是 `routing_unavailable` | `test_r1_f1_a_non_200_route_reply_without_a_signal_is_routing_unavailable`、`test_r1_f1_a_non_200_route_reply_is_never_adopted`（完整的合成路線本文、狀態 302～503：`leg = None`、`freeway_check = None`、只送一個請求）、`test_r1_f1_a_non_200_road_attribute_reply_without_a_signal_is_routing_unavailable`；既有的 `test_no_request_is_retried_after_an_error_reply`、`test_s35_s38_one_direction_failing_stores_nothing_and_has_no_route`、`test_s39_a_failed_road_attribute_query_is_routing_unavailable_with_no_snapshot` 照常通過 | PASS |
| 讀不到或不是 JSON 的本文不拋例外 | `test_r1_f1_unreadable_route_bodies_are_routing_unavailable_and_do_not_raise`（11 種本文 × 狀態 200、302、500）、`test_r1_f1_unreadable_non_200_trace_bodies_are_routing_unavailable_and_do_not_raise`（9 種本文 × 狀態 302、500） | PASS |
| 200 的既有採用與拒收行為不變 | `tests/test_routing_engine.py` 的既有 177 個案例與 `tests/test_routing_transport.py` 的 63 個案例全部照常通過（沒有修改任何既有測試） | PASS |

E-3：新案例的回應全部由既有的合成產生器（`route_body`、`trace_body`）或手寫的位元組組成，沒有新的座標來源。E-4：同一檔的 autouse socket 封鎖與 `FakeEngine` 替身；沒有網路請求。E-5：沒有修改既有測試。

### 11.5 E-6 與突變檢查

- H-4 **〔已被第 12 節取代：下一句的第一個子句對 `65aa00c` 不成立。〕** 原文：「每一種非 200 的情形都是明確的路線錯誤代碼，永不採用、不存快照；國道訊號在非 200 時也優先（CL-R1-8）。」更正：在 `65aa00c`，數值欄位是超出浮點範圍的整數時（非 200 與 200 都是），結果是未捕捉的 `OverflowError`，不是路線錯誤代碼；沒有採用、沒有存快照（R2-F1）。自 `022f629` 起成立的 H-4 陳述見第 12.6 節。H-1、H-2 不受影響（傳輸層與請求內容沒有修改；錯誤回應不觸發任何新的請求）。
- 突變（`mutate16b.py`，原文以原本的位元組寫回；結束時 `routing/` 下全部 `.py` 的 SHA-256 與開始時相同，`sources restored: True`）：第 10.7 節的 33 個突變加上 4 個新突變，**37 個全部被抓到**。新突變：

| # | 突變 | 失敗 |
| --- | --- | --- |
| F1a | 非 200 路線回應的訊號不收集（還原 R1-F1 的缺陷） | 15 |
| F1b | 非 200 道路屬性回應的訊號不收集（還原 R1-F1 的缺陷） | 16 |
| F1c | 有 `trip` 的非 200 路線回應被當成成功的回應處理 | 26 |
| F1d | 對非 200 路線回應送道路屬性查詢 | 34 |

### 11.6 Remaining work

1. Orchestrator 核對本 Executor 的 binding，派 R2（受審 subject `65aa00c`）；R2 重讀 R1 record 與本節的證據。
2. 第 9 節第 2～3 項不變（#14、#15 的最終 subject；TI-C16-2、TI-C16-3；NV-1 與真實請求 NOT RUN；RV-12～RV-14）。

## 12. Cycle 2：R2-F1 的 rework（`ruling-20261118-issue16-c1.md`；subject `022f629`）

### 12.1 Cycle 1 的結果與本 cycle 的契約

- Cycle 1：R1（`audit/issue-16-c1-r1.md`）R1-F1 BLOCKING → correction `65aa00c` → R2（`audit/issue-16-c1-r2.md`）**R2-F1** BLOCKING → Alternate（`audit/issue-16-c1-alt.md`）`VERDICT: UNRESOLVED (R2-F1)` → Final Adjudication（`decisions/ruling-20261118-issue16-c1.md`，HEAD `d9061c5`）：**targeted rework，授權 cycle 2（自 R1 起）**；不 dismiss、不 defer、不交 DA。三份 audit record 與 ruling 已全文閱讀。
- R2-F1 的 root cause（ruling 第 3.2 節）：`adoption.py` 的 `_real` 以 `math.isfinite` 檢查數值；`math.isfinite` 先把 `int` 轉成 `float`，對絕對值超出浮點範圍的整數（例如 `2**1024`、`10**400`、`-(10**400)`）拋 `OverflowError`。`_real` 自 `7cb4b0c` 起逐字未變；它的呼叫處 `trip.summary.length`、`trip.summary.time`、`edges[n].length` 在 HTTP 200 與非 200 兩條路徑都會經過，所以兩條路徑都以未捕捉的例外中止，回程不送出、不決定代碼。
- 要達成的結果（ruling 第 3.2 節第 1～4 項）：不拋未捕捉例外；這類值無法作為有限數值時保守拒收（沒有訊號 → `routing_unavailable`，有訊號 → `highway_in_route`，非 200 保留 `engine_error`／`trace_failed`）；訊號收集與兩方向檢查不中斷；其他行為不變（含 `2**1023` 與其他無效值的結果、R1-F1 的修正）。封閉清單：`adoption.py`、`tests/test_routing_engine.py`、本 worklog。
- 角色與 binding：同第 2 節（agentId `a1e2cfa52290d496f`，`gov-executor`；E-EX 不適用，O-1）。Executor 自行觀測（`022f629` 之後、寫本節之前）：(`claude-opus-5-5`, `high`) 231 則，集合只有一個元素。**這是自我觀測，不是派工者的核對。** 沒有使用 bounded assignments，沒有派工任何 subagent。

### 12.2 修改（`d9061c5` → `022f629`；只有 `adoption.py` 與 `tests/test_routing_engine.py`）

| # | 決定 | 依據 |
| --- | --- | --- |
| D-16-27 | `_real(value)`：不是 `int`／`float` 或是 `bool` → `False`；否則回傳 `math.isfinite(value)`，它拋 `OverflowError` 時 → `False`。效果：rework 前被接受的值全部照舊被接受（`math.isfinite` 沒有拋出時結果相同，例如 `2**1023`）；rework 前會拋例外的值（絕對值超出浮點範圍的整數）改為「不可用」，與字串、`null`、清單、物件、`1e400` 同一處理：該欄位記為讀不到（路線回應 `response_malformed`、道路屬性回應 `trace_failed`），國道訊號照樣收集，兩個方向照樣送出並檢查。修正只在 `_real` 一處，三個欄位與兩條路徑都經過它（呼叫處沒有改）。**沒有新增任何長度或時間的上限**：可用與否的界線就是 rework 前 `math.isfinite` 能不能判定的界線，所以不需要 Design Authority 決定新的語義（ruling 第 3.2 節第 4 項） | R2-F1；ruling 第 3.2 節；CL-R1-8；SPEC-001 7.11 第 5 項 |
| — | 模組說明補上「長度或時間不是可用的有限數值（含超出浮點範圍的整數）時記為讀不到，200 與其他狀態皆然，不中斷訊號收集」；`_real` 加上 docstring | ruling closure 證據第 6 項 |

`git diff --stat d9061c5 022f629`：`adoption.py` 15 additions／2 deletions，`tests/test_routing_engine.py` 118 additions／0 deletions；沒有刪改既有測試函式（E-5：無）。`source.py`、`valhalla.py`、`http_transport.py` 與其他檔案沒有修改。

### 12.3 E-1 pytest（subject `022f629`）

`.venv/Scripts/python.exe -m pytest -q`，在 commit 之後、工作目錄乾淨時執行，exit 0，完整輸出：

```text
........................................................................ [  3%]
........................................................................ [  6%]
........................................................................ [ 10%]
........................................................................ [ 13%]
........................................................................ [ 16%]
........................................................................ [ 20%]
........................................................................ [ 23%]
........................................................................ [ 26%]
........................................................................ [ 30%]
........................................................................ [ 33%]
........................................................................ [ 36%]
........................................................................ [ 40%]
........................................................................ [ 43%]
........................................................................ [ 46%]
........................................................................ [ 50%]
........................................................................ [ 53%]
........................................................................ [ 56%]
........................................................................ [ 60%]
........................................................................ [ 63%]
........................................................................ [ 67%]
........................................................................ [ 70%]
........................................................................ [ 73%]
........................................................................ [ 77%]
........................................................................ [ 80%]
........................................................................ [ 83%]
........................................................................ [ 87%]
........................................................................ [ 90%]
........................................................................ [ 93%]
........................................................................ [ 97%]
............................................................             [100%]
2148 passed in 22.48s
```

`.venv/Scripts/python.exe -m pytest -q -rxX`，exit 0，摘要：

```text
............................................................             [100%]
2148 passed in 22.74s
```

`2015`（`65aa00c`）＋ `133`（cycle 2 的回歸案例）＝ `2148`。`grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。測試後 `git status --short` 為空。`git ls-files` 不含 `data/`、`.gpx`、`.fit`、`.env`、`*.key`（0 筆）。

### 12.4 E-2：R2-F1 的 coverage（`tests/test_routing_engine.py`）

| 情形 | 測試 | 結果 |
| --- | --- | --- |
| `trip.summary.length`、`trip.summary.time` × HTTP 200、302、400、429、500、503 × 有、無 `has_highway` × `2**1024`、`10**400`、`-(10**400)`（經 `get_route` 的來回行程；只改去程） | `test_r2_f1_a_route_summary_number_beyond_the_float_range`（72 個案例）：沒有例外；代碼依訊號；200 的 reasons 含 `outbound:response_malformed`，非 200 含 `outbound:engine_error`；`assert_no_route`；沒有快照檔；請求序列 200 是 `route, trace_attributes, route, trace_attributes`、非 200 是 `route, route, trace_attributes`（回程照樣送出、不依錯誤回應的 shape 查詢、沒有重試、沒有狀態請求）；並確認 JSON 本文中是整數字面值 | PASS |
| `edges[n].length` × 同上 6 種狀態 × 有、無 `motorway` × 同上 3 個值 | `test_r2_f1_a_road_attribute_edge_length_beyond_the_float_range`（36 個案例）：沒有例外；reasons 含 `outbound:trace_failed`，有訊號時含 `outbound:motorway_edge`；沒有路線、沒有快照；請求序列 `route, trace_attributes, route, trace_attributes` | PASS |
| 回程的三個欄位 | `test_r2_f1_a_number_beyond_the_float_range_in_the_return_direction`（9 個案例） | PASS |
| 單方向的結果 | `test_r2_f1_evaluate_direction_records_the_field_as_unreadable`（6 個案例：`leg = None`、`freeway_check = None`、reasons 含 `response_malformed`） | PASS |
| `2**1023` 的結果與 rework 前相同 | `test_r2_f1_the_largest_float_range_int_keeps_its_earlier_result`（`summary.length`、edge `length`：都是 `trace_length_mismatch`、`routing_unavailable`，沒有快照） | PASS |
| 其他無效值不變（ruling 第 2.3 節 D 列） | `test_r2_f1_other_invalid_lengths_keep_their_results`（`"abc"`、`-1`、`null`、`1e400`、`-1e400`、`[]`、`{}`、`true`；200、`has_highway: true` → `highway_in_route`，reasons 含 `has_highway`、`response_malformed`、`trace_length_mismatch`） | PASS |
| R1-F1 的回歸與既有測試 | `test_r1_f1_*` 97 個案例、其他既有測試全部保留並通過（`tests/` 只有新增行） | PASS |

E-3：新案例的回應全部由既有的合成產生器（`route_body`、`trace_body`，0°N、0°E 附近的合成點）加上數值常數組成，或在其 JSON 位元組中替換一個欄位；沒有新的座標來源。E-4：同一檔的 autouse socket 封鎖與 `FakeEngine`；沒有網路請求。E-5：無。

### 12.5 修改前後的比對（ruling closure 證據第 2 項）

Scratchpad 的 `probe_c2.py` 把 `git show 65aa00c:src/moto_copilot/routing/adoption.py` 載入成記憶體中的模組，與工作目錄的 `adoption.py`（內容等於 `022f629`）以同一組合成輸入執行 `evaluate_direction`，比較 (signals, reasons, freeway_check, 是否沒有 leg, 請求序列)。探測不寫入 repo，匯入後封鎖 socket。

| 輸入 | 結果 |
| --- | --- |
| 11 種值（`"abc"`、`-1`、`null`、`1e400`、`-1e400`、`[]`、`{}`、`true`、`2**1023`、`0`、`3.5`）× 3 個欄位 × 狀態 200、503 × 有、無訊號（132 組） | **132 組完全相同，0 組不同** |
| `2**1024`、`10**400`、`-(10**400)` × 3 個欄位 × 狀態 200、503 × 有、無訊號（36 組） | `65aa00c`：36 組全部 `OverflowError`；`022f629`：0 組例外，例如 200、無訊號：`summary.length` → (`response_malformed`, `trace_length_mismatch`)、`summary.time` → (`response_malformed`)、edge `length` → (`trace_failed`)，`freeway_check = None` |

第一次執行時探測腳本自己出錯（以 `importlib` 載入舊模組前沒有放進 `sys.modules`，`dataclasses` 找不到模組），改正後重跑得到上表；這是 harness 的錯誤，不是產品的行為。

### 12.6 E-6

- **H-4**（自 `022f629` 起）：引擎回應的 `trip.summary.length`、`trip.summary.time`、`edges[n].length` 不論是什麼可由 `_parse_json` 解析出的值，都不會使 `evaluate_direction` 或 `get_route` 拋出未捕捉的例外：無法作為有限數值時記為讀不到，沒有國道訊號時是 `routing_unavailable`、有時是 `highway_in_route`，永不採用、不存快照，兩個方向照樣送出並檢查（第 12.4、12.5 節）。這個陳述只涵蓋這三個欄位；回應的其他部分維持第 6、10、11 節既有的證據範圍（例如 `audit/issue-16-c1-alt.md` 第 2.2 節 (6) 的有界探測），不另外宣稱為窮舉。
- **H-1、H-2**：不受影響（傳輸層、client、請求內容與錯誤訊息沒有修改；新案例沒有新的請求）。
- **突變**（`mutate16b.py`，原文以原本的位元組寫回，結束時 `routing/` 下全部 `.py` 的 SHA-256 與開始時相同，`sources restored: True`；之後 `git status --short` 只有本次尚未 commit 的修改）：第 10.7、11.5 節的 37 個突變加上 2 個新突變，**39 個全部被抓到**。新突變：

| # | 突變 | 失敗 |
| --- | --- | --- |
| C2a | 恢復 cycle 1 的 `_real`（對 `int` 直接呼叫 `math.isfinite`，即先轉成 `float`） | 123 |
| C2b | 超出浮點範圍的整數被當成可用的數值 | 18 |

### 12.7 NOT VERIFIED 與 remaining work

- NV-1（真實伺服器是否會回傳這類數值、真實回應的形狀）：**NOT VERIFIED／NOT RUN**（ruling 第 6 節）。只在 Python 3.11.2 執行；`math.isfinite` 對過大 `int` 的行為在其他版本沒有實測（NV-4）。
- 範圍界定：`valhalla.py:104`、`canonical.py:45`、`target_gpx.py:166`、`:173` 的 `math.isfinite` 不在本 rework 範圍（ruling 第 3.2 節），沒有修改，也不作判斷。
- 下一步：Orchestrator 核對本 Executor 的 binding，派 cycle 2 R1（受審 subject `022f629`，完整 audit；pack 含 ruling 與 cycle 1 的三份 audit records）。第 9 節第 2～3 項不變。
