# Worklog — Issue #15（SPEC-R1 R1-3）`routing`：目標路線 GPX 的路線來源

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #15（SPEC-R1 R1-3），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **Executor 工作完成；C-15-1～C-15-3 已由 `decision-20261118-issue15-c151.md` 裁決（CL-R1-22～CL-R1-24），CL-R1-22 的修改在 `e78cc9f`（第 9 節），待 R1。** pytest `1625 passed`。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure。以下為先前狀態：**Executor 回報 `NEEDS_DA`。** 範圍 (a)、(b) 除一處之外完成，pytest `1607 passed`（第 6 節 E-1）。**C-15-1（blocking）**：騎士指定的合法折返位置落在兩個軌跡點之間時，幾何要怎麼切開，契約有兩種以上合理的讀法（CL-R1-10 第 4 項「沿軌跡 m 公尺處」與 S64「沒有補造的軌跡點」）；這部分停止，程式以專用例外 fail closed，等 Design Authority 裁決。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `201e3e3`（派工時的 HEAD，含已結案的 #9、#13、#14）；實作 commit **`b771d9feabe2984caf8f636b930e0e86798a0bd4`**（`b771d9f`）。CL-R1-22 的修改 commit **`e78cc9f99f7c2f4b4f15f29103a282ee56fd3270`**（`e78cc9f`，父 commit 是 DA record 的 `0e4a93f`），是 **#15 新的 implementation subject**（取代 `b771d9f`）。worklog 在另外的 record-only commits |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：Issue #15 的內文。Orchestrator 提供的 scratchpad 原文檔（`issue-15-body.md`）以 `sha256sum` 重算為 `a54f8034cdadd143e6a1ec594ee7d74e01bb47ce9bc13bd21537bbcf92fd5ad7`，等於派工內容所述 run record 第 4 節的值。沒有呼叫 GitHub，沒有修改 Issue。
- **Spec**：SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md`）：第 2 節引用段落；第 4 節 CL-R1-1（資料與網路）、**CL-R1-10**（目標 GPX 的讀取與自動辨識，第 1–7 項）；第 5 節 R1-3 列（範圍 (a)、(b)、AC、排除、高風險類別 H-2、H-3、H-4）與 E-1～E-6。
- **CL-R1-13**：`decision-20261118-issue13-c131.md` §3.1、第 6 節 R1-3 列：產生或驗證 `route_id` 的程式不接受結尾換行、前後空白或非 ASCII 數字，以測試證明。
- **CL-R1-14、CL-R1-18**：`decision-20261118-issue14-c141.md` 第 2.2 節與第 7.1 節。CL-R1-18：折返位置的整數公尺一律 `ROUND_HALF_UP`；騎士指定以 `Decimal(repr(km))` 乘以 1000 再取整，不先以浮點數相乘；自動判定以累計距離的最短十進位表示取整；合法性以取整後的整數判定；CL-R1-14 的捨去不適用於 `RG-`。
- **規格來源**：`docs/spec/SPEC-001-plan-schema.md` §2 的「ID」「隱私」列；4.1 `target_gpx_ref`、`target_gpx_turnaround_km`；4.13 `target_gpx_invalid`、`target_gpx_not_round_trip`；5.4「目標路線 GPX 的門檻」「去回同路的自動辨識」兩列；5.5 兩個代碼的固定文字（只作為 D-15-6 的依據，不組裝文字）；7.11 第 2 項；第 9 節 S10、S27、S43、S58、S59–S64、S78–S80。`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §2.8；`docs/cr/CR-01-appendix/lead_dispositions_resolution.md` §8.2、§9.1–§9.4、§9.12（含「明確去回同路的軌跡上，騎士指定了不合法的折返位置時回傳 `target_gpx_not_round_trip`，不退回自動判定」）。`DESIGN.md` §5（參考）。
- **高風險類別**：`decision-20261117-high-risk-categories.md` §3.2–§3.4、§5；R1-3 標為 H-2、H-3、H-4（第 6 節 E-6）。
- **CL-R1-22～CL-R1-24、TI-C15-1、RV-11**：`decision-20261118-issue15-c151.md`（v1，2026-11-18，HEAD `0e4a93f` 時已 commit）。CL-R1-22：騎士指定的合法 m 以累計距離最接近 m 的可用軌跡點實現（`Decimal` 精確比較，同距離取索引小者；可用＝`0 < cum_i < total` 且 `0 < c_i < total`；沒有可用的點 → `turnaround_unconfirmed`），`turnaround_m` 與 `RG-` 用該點的 `c_k`，兩段共用分界點，不內插；自動判定不變。CL-R1-23：接受 C-15-2。CL-R1-24：屬 #16。第 4 節是修改的封閉清單與證據要求。這是 DA 依治理 §5.3 第 2 類的 clarification，不是 Executor 的決定。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-ae0a2f33f0da61e65.{meta.json,jsonl}`；`meta.json` 的 `agentType` 是 `gov-executor`，`description` 是「Executor: implement Issue #15 R1-3」。
- Executor 自行觀測（`b771d9f` 之後、寫本 worklog 之前，以第 3.6 節的掃描方式）：agentId `ae0a2f33f0da61e65`，(`claude-opus-5-5`, `high`) 73 則，集合只有一個元素。**這是自我觀測，不是派工者的核對**；之後的訊息不在這個數字內，Orchestrator 採用本 return 前須自行核對全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 Bindings m3（檔首、第 2.5、3.6、7 節）、derivation-spec-r1（全文）、CL-R1-12／CL-R1-13 record（相關節）、CL-R1-14～CL-R1-19 record（第 1、2、7 節）、高風險類別 record §3–§5、Issue #15 原文（核對雜湊）、SPEC-001 §2、4.1、4.13、5.4、7.11 第 1–8 項、第 9 節的相關 S 編號、SPEC-RESOLUTION-001 §2.8、lead 處置 §8.2、§9.1–§9.4、§9.12、`DESIGN.md` 中目標 GPX 的段落、`ingest/gpx.py`、`ingest/segments.py` 的開頭與 `haversine_m`、`ingest/__init__.py`、`routing/` 各檔的介面、`contracts/schemas.py` 的 ID 樣式、`routes/catalog.py` 的切段方式（只作參考）、`tests/conftest.py`、`tests/test_ingest.py` 開頭、`tests/routing_synthetic.py` 開頭、`tests/test_routing_store.py` 的沒有網路測試、worklog `issue-14.md`（格式參考）、`docs/conventions/git-commit-rules.md`、`.gitignore`。沒有讀 `experiments/` 的任何檔案。
2. 基準：`201e3e3` 上 `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider` 為 `1456 passed`。
3. 新建 `src/moto_copilot/ingest/geometry.py`（範圍 (a)，CL-R1-10 第 1 項）：`read_gpx_geometry(path)`、`parse_gpx_geometry(data)`、`GeoPoint`（只有 `lat`、`lon`）、`GpxGeometry`（點、檔案位元組的 SHA-256、來源是 `trkpt` 或 `rtept`；沒有路徑欄位）、`GpxGeometryError`（固定的 reason 代碼）。依序取所有 `trk`／`trkseg` 的 `trkpt`；沒有任何 `trkpt` 時取 `rte` 的 `rtept`；不讀時間與高度。#9 的 `ingest/gpx.py`、`segments.py`、`__init__.py` 沒有修改。
4. 新建 `src/moto_copilot/routing/target_gpx.py`（範圍 (b)）：`target_gpx_route(path, trip_type, turnaround_km=None)` 與 `target_gpx_route_from_bytes(...)` 回傳 `TargetGpxRoute`（`route_id`、`trip_type`、`target_gpx_ref`、`total_length_m`、`turnaround_m`、`turnaround_source`、`legs`、`route_source = "target_gpx"`）或 `TargetGpxError(code, case)`；`target_gpx_route_id`、`turnaround_m_from_km`、`metres_half_up`、`cumulative_m`、`detect_out_and_back`。判定順序見 D-15-1。
5. `src/moto_copilot/routing/__init__.py`：加上 `target_gpx` 的匯出與模組說明；#14 既有的匯出與行為不變（`git diff 201e3e3 b771d9f -- src/moto_copilot/routing/__init__.py` 只有新增的 import、`__all__` 的新名稱與說明文字）。
6. 新建 `tests/test_target_gpx.py`（58 個測試函式，151 個案例）。GPX 全部在測試中以字串產生；寫檔只在 pytest 的 `tmp_path`。`.gitignore` 忽略 `*.gpx`，所以沒有在 `tests/` 下放 `.gpx` fixture，也沒有修改 `.gitignore`。
7. 自我驗證：全套 pytest、#9 的測試、23＋2 個突變檢查（第 6 節 E-6）、格網篩選與完整搜尋的對照、2 萬點軌跡的執行時間。突變檢查以 session scratchpad 的腳本在記憶體中替換原始碼字串、跑 `tests/test_target_gpx.py`、在 `finally` 中寫回原文；結束後 `git status --short` 只有本 Ticket 的新檔（尚未 commit 時）。
8. 依 SA-1 在 topic branch 作本機 commit `b771d9f`；commit 前以 `git diff --cached --name-only` 確認暫存的只有上列 4 個檔案，不含 `.env`、GPX、FIT 或 `data/`。`git ls-files` 沒有 `data/`、`.gpx`、`.fit`、`.env`。
9. 沒有 push、沒有開 PR、沒有碰 GitHub；沒有讀取、列出或搜尋 `data/`；沒有使用 `git status --ignored`；沒有讀 `.env`；沒有讀或執行 `experiments/` 下的任何檔案；沒有發出網路請求。

## 4. Decisions and assumptions

| # | 決定 | 依據 |
| --- | --- | --- |
| D-15-1 | 判定順序：(1) 行程型態（沒有給 → `TripTypeRequiredError`；不是 `one_way`／`round_trip` 的完整字串 → `ValueError`；在讀檔之前）；(2) 讀檔；讀不到 → `target_gpx_invalid`；(3) 點數少於 2 → 相鄰兩點（含跨 `trkseg`）超過 1 km → 總長不到 1 km，都是 `target_gpx_invalid`；(4) 單向：幾何原樣，不使用折返位置；(5) 來回：終點與起點相距超過 200 m → `target_gpx_not_round_trip`／`end_not_at_start`（即使給了折返位置）；(6) 給了折返位置：取整後 `0 < m < 總長` 才合法，否則 `turnaround_unconfirmed`，不退回自動辨識；(7) 沒有給：自動辨識，不成立 → `turnaround_unconfirmed` | CL-R1-10 第 2–4 項；lead 處置 §9.12 最後一段 |
| D-15-2 | 距離：相鄰點的 haversine（`ingest.segments.haversine_m`，地球半徑 6,371,000 m）。軌跡是一條連續的折線，跨 `trkseg` 的相鄰點照常相連並計入總長。直線距離（最遠點、終點到起點、取樣點到前段的點）也用 haversine | CL-R1-10 第 2 項「含跨 `trkseg` 的相鄰點」；與 #9 共用同一個距離函式 |
| D-15-3 | 門檻的邊界：總長 `< 1000 m` 無效；相鄰 `> 1000 m` 無效；終點與起點 `> 200 m` 不是來回；接近是 `≤ 50 m`；成立是「接近數 × 10 ≥ 9 × 取樣數」（整數比較，沒有浮點誤差） | 4.13「不到 1 km」「超過 1 km」「超過 200 m」；5.4「50 m 內」「90% 以上」 |
| D-15-4 | 自動辨識：分界是離起點直線距離最遠的點（嚴格大於才更新，所以相同時取第一個）；後段的取樣點在分界之後沿軌跡 `100 × i` 公尺（`i = 1, 2, …`，直到不超過後段長度），位置在所在線段上依距離比例內插，只用於比對，不成為輸出的點；前段是起點到分界（兩端都含）的軌跡點，比對是點對點的距離；後段沒有取樣點時不成立 | CL-R1-10 第 5 項的字面。取樣點的內插是「沿軌跡每 100 m 取一點」的必然做法；它不進入任何輸出，所以不是 S64 所說的補造 |
| D-15-5 | 為了長軌跡的效能，前段的點以單位球面上的 3D 格網分桶，只作篩選：格邊是 50 m 弦長的 1.25 倍，搜尋相鄰 27 格，每個候選再以 haversine 判定。在赤道、換日線旁、北緯 89.5°、南緯 89.9° 的合成點上，與完整搜尋的結果逐點相同（測試）。2 萬點的去回軌跡 0.1 秒內完成 | HOW。篩選不改變判定：格邊大於門檻的弦長，所以不會漏掉 50 m 內的點 |
| D-15-6 | 讀不到檔案（不存在、是目錄、無法開啟）、不是 XML、根元素不是 GPX 1.1／1.0 的 `gpx`、點的 `lat`／`lon` 缺少、不是數字、不是有限值或超出 ±90／±180：都是 `target_gpx_invalid`（case 分別是 `unreadable`、`malformed_point`），不略過壞點、不報其他例外 | 4.13「讀不到軌跡點」；5.5 `target_gpx_invalid` 的固定文字（「確認檔案路徑與內容」）顯示路徑與內容的問題屬這個代碼。略過壞點會改變幾何（H-4），所以整個檔案不採用（fail closed）。也接受 GPX 1.0 的命名空間（結構相同）；其他或沒有命名空間的檔案不讀（fail closed）。列為 C-15-2 供 DA 知悉。**DA 已接受：CL-R1-23（`decision-20261118-issue15-c151.md` 第 3 節）** |
| D-15-7 | 切開：在折返點的索引 `k` 切成去程 `points[0..k]` 與回程 `points[k..]`，折返點同時是去程的最後一點與回程的第一點（兩段的分界）。各段的點就是檔案中的點（同一組物件、原順序），不反轉、不新增、不移動、不刪除。去程長度是到 `k` 的累計距離，回程長度是總長減去它 | CL-R1-10 範圍 (b)「折返點是兩段的分界」；S64；折返點兩段共用，否則它與下一點之間的那一段距離會從兩段中消失。**DA 確認：CL-R1-22 第 7 項** |
| D-15-8 | **（`e78cc9f` 起，依 CL-R1-22）** 騎士指定的合法位置 m 由 `rider_turnaround_index(cum, m)` 選點：可用的點（`_usable`：`0 < cum_i < total` 且 `0 < c_i < total`）中 `|Decimal(repr(cum_i)) − m|` 最小者，同距離取索引小者（逐點掃描，嚴格小於才更新）；沒有可用的點 → `turnaround_unconfirmed`。`turnaround_m` 與 `RG-` 用選到的點的 `c_k`（`_round_trip` 一律以 `metres_half_up(cum[k])` 計算，自動判定與騎士指定同一處）。自動判定的分界也套用 `_usable`。先前（`b771d9f`）：只在 m 剛好是某點的累計距離時切開，其他情形 `TurnaroundSplitUndecidedError`（已刪除） | CL-R1-22 第 2～7 項（`decision-20261118-issue15-c151.md` 第 2.2 節）；先前的做法依 Executor 角色定義「遇到問題」停止並回報 C-15-1 |
| D-15-9 | `RG-`：`"RG-" + sha256(f"{檔案 SHA-256}:{trip_type}"[+ f":{m}"]).hexdigest()[:10]`，文字以 ASCII 編碼。輸入檢查：參照必須是 64 個小寫 ASCII 十六進位字元（拒絕換行、空白、大寫、非 ASCII 數字）；單向不得帶折返位置；來回的 m 必須是正整數（拒絕 `bool`、`float`、字串）。產生的代號以 `contracts.schemas.ROUTE_ID_PATTERN` 確認 | CL-R1-10 第 6 項；CL-R1-13；SPEC-001 §2 ID 列 |
| D-15-10 | 整數公尺：`turnaround_m_from_km(km)` ＝ `Decimal(repr(km)) × 1000` 依 `ROUND_HALF_UP` 取整；`metres_half_up(x)` ＝ `Decimal(repr(x))` 依 `ROUND_HALF_UP` 取整。`km` 是 `bool` 或不是數字 → `TypeError`；不是有限值 → 不合法（`turnaround_unconfirmed`） | CL-R1-18 第 1–4 項；NaN、無限大不是合法的里程（4.13「指定的里程不合法」） |
| D-15-11 | 結果與錯誤只帶代碼、情形、雜湊與幾何，不帶路徑或檔名；錯誤訊息是固定文字，不含路徑、座標、折返位置或 XML 解析器的訊息；讀檔失敗的錯誤在 `except` 區塊之外建立，所以沒有帶檔名的 `OSError` 被串接（`__context__`、`__cause__` 都是 `None`）；兩個新模組不 import `logging`、不 `print` | CL-R1-10 第 7 項；S10；SPEC-001 §2 隱私列 |
| D-15-12 | 沒有給行程型態時以 `TripTypeRequiredError`（`ValueError` 的子類別）表示「明確的錯誤」，不是第七個路線錯誤代碼 | CL-R1-10 第 3 項；4.13 的代碼只有六個；追問由之後的流程處理 |
| D-15-13 | `TargetGpxRoute` 含軌跡點（座標）。它是交給 `routes`／R1-4 共用介面的內部幾何，不是 PlanResult；結果中不得出現座標與折線（S10 的其餘部分）由之後組裝 PlanResult 的 Ticket 負責 | SPEC-001 §2 隱私列；R1-4 範圍 (f) |

## 5. Artifacts

| 檔案 | 變更（`201e3e3` → `b771d9f`） |
| --- | --- |
| `src/moto_copilot/ingest/geometry.py` | 新檔：只讀幾何的 GPX 讀取（範圍 (a)） |
| `src/moto_copilot/routing/target_gpx.py` | 新檔：目標 GPX 的路線來源（範圍 (b)） |
| `src/moto_copilot/routing/__init__.py` | 加上 `target_gpx` 的匯出與說明文字 |
| `tests/test_target_gpx.py` | 新檔：本 Ticket 的測試（合成 GPX，在測試中產生） |

`git diff --stat 201e3e3 b771d9f`：4 files changed, 1266 insertions(+), 2 deletions(-)。`git diff 201e3e3 b771d9f` 對 `ingest/gpx.py`、`ingest/segments.py`、`ingest/__init__.py`、`contracts/`、`routing/` 的 `canonical.py`、`snapshot.py`、`store.py`、`request_key.py`、`tests/test_ingest.py`、`tests/test_ingest_cli.py` 為空。

## 6. Verification

### E-1 pytest（subject `b771d9f`）

`.venv/Scripts/python.exe -m pytest -q`，exit 0，完整輸出：

```text
........................................................................ [  4%]
........................................................................ [  8%]
........................................................................ [ 13%]
........................................................................ [ 17%]
........................................................................ [ 22%]
........................................................................ [ 26%]
........................................................................ [ 31%]
........................................................................ [ 35%]
........................................................................ [ 40%]
........................................................................ [ 44%]
........................................................................ [ 49%]
........................................................................ [ 53%]
........................................................................ [ 58%]
........................................................................ [ 62%]
........................................................................ [ 67%]
........................................................................ [ 71%]
........................................................................ [ 76%]
........................................................................ [ 80%]
........................................................................ [ 85%]
........................................................................ [ 89%]
........................................................................ [ 94%]
........................................................................ [ 98%]
.......................                                                  [100%]
1607 passed in 43.59s
```

`1456`（基準）＋ `151`（新測試）＝ `1607`。`grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。#9 的 `tests/test_ingest.py`、`tests/test_ingest_cli.py`：`105 passed`。測試後 `git status --short` 為空（commit 之後）。

### E-2 AC 對 S 編號

測試檔：`tests/test_target_gpx.py`（以下省略檔名）。E-1 中全部 PASS；「結果」欄寫的是 AC 的狀態。

| AC | 測試 | 結果 |
| --- | --- | --- |
| S27（不推定為來回；終點沒有回到起點 → `target_gpx_not_round_trip`；只在明確去回同路時自動決定；有歧義時同一代碼；騎士指定優先） | `test_missing_trip_type_is_an_explicit_error_and_is_not_inferred`、`test_round_trip_whose_end_is_not_at_the_start_is_not_round_trip_even_with_a_turnaround`、`test_out_and_back_without_a_turnaround_uses_the_point_farthest_from_the_start`、`test_ambiguous_shapes_are_not_detected_and_give_turnaround_unconfirmed`、`test_the_riders_legal_position_wins_over_the_detected_one` | PASS，其中「騎士指定優先」的切開部分見 S61／S80 |
| S43（`target_gpx_invalid` 三種情形；只有路線點、沒有時間可用；去回同路時取最遠點；終點沒有回到起點；單向原樣；**沒有行程型態時不由幾何推定、回報明確的錯誤**，追問不在本 Ticket） | `test_no_points_or_one_point_is_invalid`、`test_total_length_under_1_km_is_invalid`、`test_adjacent_points_more_than_1_km_apart_is_invalid`、`test_a_file_with_only_route_points_and_no_time_can_be_used`、`test_out_and_back_without_a_turnaround_uses_the_point_farthest_from_the_start`、`test_round_trip_whose_end_is_not_at_the_start_is_not_round_trip_even_with_a_turnaround`、`test_end_within_200_m_of_the_start_counts_as_returned_and_beyond_does_not`、`test_one_way_uses_the_geometry_as_it_is_even_when_start_and_end_meet`、`test_missing_trip_type_is_an_explicit_error_and_is_not_inferred`、`test_unknown_trip_type_values_are_rejected` | PASS |
| S59 | `test_out_and_back_without_a_turnaround_uses_the_point_farthest_from_the_start`、`test_when_several_points_are_equally_farthest_the_first_is_the_turnaround` | PASS |
| S60 | `test_ambiguous_shapes_are_not_detected_and_give_turnaround_unconfirmed[loop]`、`test_the_four_shapes_of_s79` | PASS |
| S61（環狀、指定折返位置後以那個位置切開） | `test_a_loop_is_cut_at_the_riders_position_when_a_point_is_there`（以替換累計距離讓一個點剛好在 m 上，只測切開）；`test_a_legal_turnaround_between_track_points_is_held_for_the_design_authority`（m 在兩點之間時不回傳路線） | **BLOCKED（C-15-1）**：剛好在軌跡點上的情形 PASS；一般情形（m 在兩點之間）等 DA 裁決，目前 fail closed |
| S62（0、負數、超過總長 → 回報，沒有路線） | `test_illegal_turnaround_positions_are_not_round_trip`（`0`、`0.0`、`-0.0`、`-1.0`、`-0.0005`、`0.0004`（取整為 0）、`1e9`、NaN、±inf）、`test_a_turnaround_at_or_beyond_the_total_length_is_not_round_trip`（等於與超過總長）、`test_an_illegal_turnaround_on_a_clear_out_and_back_does_not_fall_back_to_detection`、`test_turnaround_must_be_a_number` | PASS |
| S63 | `test_round_trip_whose_end_is_not_at_the_start_is_not_round_trip_even_with_a_turnaround`（沒有給與給了 1.5、0、−2、99 km） | PASS |
| S64（任何情形都沒有反轉或補造的軌跡點） | `assert_slices_of_the_file`（各段是檔案中連續、同向的一段；去程＋回程去掉重複的分界＝檔案的全部點）用在所有回傳路線的測試；`test_detected_round_trips_are_slices_of_the_file`、`test_a_one_way_track_is_not_reversed_or_completed_into_a_round_trip`；突變「回程反轉」被抓到（E-6） | PASS（已回傳的路線）。m 在兩點之間的情形目前不回傳路線，所以沒有補造；裁決後要再驗證 |
| S78（自動與指定相等時 `route_id` 相同；不同時不同；單向與來回不同） | `test_s78_same_file_same_turnaround_metres_same_route_id_different_metres_different`、`test_s78_through_the_route_rider_and_detected_with_equal_metres_give_the_same_route_id`（以替換累計距離讓分界剛好在整數公尺上）、`test_route_id_is_rg_plus_the_first_10_hex_of_the_defined_text`、`test_a_different_file_gives_a_different_route_id` | PASS（`route_id` 的計算）。**經由完整流程的騎士指定 `route_id`，在一般情形（分界的累計距離不是剛好的整數）受 C-15-1 影響**：例如自動判定 3000.0000x m 取整為 3000，騎士指定 3.0 km 也是 3000，但 3000 m 處不剛好是軌跡點，目前不回傳路線 |
| S79（四種合成形狀） | `test_the_four_shapes_of_s79`、`test_ambiguous_shapes_are_not_detected_and_give_turnaround_unconfirmed[loop/figure_eight/partly_same_road]`、`test_the_90_percent_threshold_on_both_sides`、`test_exactly_90_percent_near_is_detected_and_less_is_not`、`test_detection_counts_samples_on_the_back_part_only`、`test_no_sample_on_the_back_part_means_not_detected`、`test_a_sample_is_near_within_50_m_of_a_front_point_and_not_beyond` | PASS |
| S80（明確去回同路的軌跡上，騎士指定的另一個合法位置為準） | `test_the_riders_legal_position_wins_over_the_detected_one`（剛好在點上）；`test_a_legal_turnaround_between_track_points_is_held_for_the_design_authority[out_and_back]`（在兩點之間時不退回自動判定，也不回傳路線） | **BLOCKED（C-15-1）**：優先順序成立（不退回自動判定）；一般情形的切開等 DA 裁決 |
| S58 中 `RG-` 的部分（CL-R1-13） | `test_every_produced_route_id_matches_the_contract_pattern`、`test_route_id_rejects_a_reference_that_is_not_64_lowercase_ascii_hex`（結尾換行、前後空白、大寫、長度不對、阿拉伯–印度數字、全形數字）、`test_route_id_rejects_inconsistent_trip_type_and_turnaround`（`"3000\n"`、`"round_trip\n"`、`True`、`3000.0` 等） | PASS |
| S10 中「不含目標 GPX 的路徑與檔名」（輸出、錯誤與 log） | `test_results_and_errors_carry_no_path_or_file_name`（7 種情形；目錄名與檔名是可辨認的合成字串；檢查 `repr`、欄位、stdout／stderr、log 紀錄）、`test_missing_or_unopenable_files_are_invalid_without_naming_the_file`、`test_parse_errors_do_not_carry_the_parser_message_or_a_chained_exception`、`test_the_held_split_error_carries_no_path`、`test_route_and_error_have_no_field_for_a_path`、`test_the_new_modules_do_not_log_print_use_the_network_or_read_the_environment` | PASS |
| 另加：讀取不依賴時間欄位 | `test_reading_does_not_need_time_and_ignores_time_and_elevation`、`test_some_points_with_time_and_some_without_are_all_used` | PASS |
| 另加：`trkpt` 與只有 `rtept` 的檔案都能讀 | `test_track_points_are_read_in_file_order_across_trk_and_trkseg`、`test_a_file_with_only_route_points_and_no_time_can_be_used`、`test_route_points_are_not_used_when_the_file_has_track_points`、`test_gpx_1_0_namespace_is_read` | PASS |
| 另加：跨 `trkseg` 的相鄰點超過 1 km 時是 `target_gpx_invalid` | `test_a_gap_of_more_than_1_km_across_trkseg_is_invalid` | PASS |
| CL-R1-18 第 6 項（`.5` 進位；騎士與自動同一規則） | `test_turnaround_km_to_metres_rounds_half_up_from_the_decimal_form`（`0.0005`→1、`1.0005`→1001、`0.5005`→501 等 11 組）、`test_float_multiplication_would_round_wrongly_and_is_not_used`、`test_detected_metres_round_half_up_not_half_even`、`test_target_gpx_module_does_not_call_round`、S78 的兩個測試 | PASS |

### E-3 合成資料的來源

- 所有 GPX 由 `tests/test_target_gpx.py` 的 `gpx()` 在測試中產生成字串；形狀（直線、去回、圓、8 字形、矩形繞行、鋸齒）由程式以「離原點向東、向北幾公尺」計算，原點是 0°N、0°E（開放海域）。換日線與極區的測試把同樣的形狀移到 0°N、179.99°E 附近（太平洋）與 89.5°N（北冰洋）、89.9°S，都是明顯的 placeholder。沒有真實的軌跡、地名、住家附近的座標或私有路線；沒有公開地標的座標。
- 測試中的檔名與目錄名（`SyntheticUserNameDir`、`2026-01-02-synthetic-home-ride.gpx`）是為了檢查不外流而虛構的字串，只寫在 `tmp_path` 下。
- `tests/` 下沒有新增 `.gpx` fixture；repo 中沒有任何 GPX 檔。

### E-4 沒有網路請求

- `test_no_network_is_used`：把 `socket.socket`、`socket.create_connection`、`socket.getaddrinfo` 換成會報錯的替身，執行讀檔、單向、來回與錯誤的情形，全部照常完成。
- `test_the_new_modules_do_not_log_print_use_the_network_or_read_the_environment`：兩個新模組沒有 import `socket`、`http`、`urllib`、`requests`、`httpx`、`ssl`、`subprocess`、`logging`，沒有 `print`，原始碼沒有 `environ`／`getenv`。#14 既有的 `test_the_routing_package_imports_no_network_or_environment_modules` 也涵蓋新的 `routing/target_gpx.py`，照常通過。

### E-5 修改的既有測試

沒有修改任何既有測試。

### E-6 高風險類別的 self-verification（高風險 record §5 的清單）

這是 Executor 的 self-verification，不是 independent audit。

**H-2（私有騎乘資料與位置；判定 3.2 第 1、4 項）**
- `git ls-files | grep -E '(^data/|\.gpx$|\.env$|\.fit$)'`：沒有輸出（exit 1）。
- 新的程式只開啟呼叫者給的路徑，讀進位元組後不保留路徑；沒有寫出任何檔案（決定衍生輸出位置的程式不涉及）。
- 路徑與檔名不出現在結果、錯誤、例外串接與 log（E-2 的 S10 列）。突變「把路徑接進錯誤訊息」被抓到（下表）。
- diff 中的座標全部是合成的（E-3）。
- 需要私有資料才能核對的項目：**真實目標 GPX（例如 E2 的真實行程題）在本程式下的結果 NOT VERIFIED**，required authority = acceptor（RB-7；本 run 沒有私有資料授權）。

**H-3（實驗與宣稱的誠信；判定 3.3 第 4 項）**
- 模組說明與 `detect_out_and_back` 的 docstring 寫明 50 m／100 m／90% 是保守的啟發式門檻，「NOT validated with real data」；`test_the_detection_is_described_as_not_validated` 檢查這句存在，且原始碼沒有「has been validated」「is validated」「proven」等宣稱。
- 本 worklog 沒有任何實驗結果；沒有把合成測試寫成以真實資料驗證。

**H-4（決策關卡的 fail-closed；判定 3.4 第 4 項：路線的採用條件）**
- 不推定：沒有行程型態時報錯，不看幾何；單向即使起終點重合也不切；不合法的騎士位置不退回自動辨識。
- 不反轉、不補造：S64 的檢查用在每一條回傳的路線；**唯一無法由契約決定的情形（C-15-1）以例外停止，不回傳路線，也不回退到自動判定**。
- 每條缺漏或失敗路徑都是明確的錯誤：讀不到、壞點、點太少、太疏、太短、終點沒回來、位置不合法（含 NaN、無限大、取整為 0）、自動辨識不成立、後段沒有取樣點。
- 突變檢查（在記憶體中替換原始碼，跑 `tests/test_target_gpx.py`，結束後寫回原文）：

| 突變 | 結果 |
| --- | --- |
| 90% 改為 80% | 抓到 |
| 50 m 改為 70 m | 抓到 |
| 取樣間隔 100 m 改為 50 m | 抓到 |
| 200 m 改為 250 m | 抓到 |
| 1 km 總長改為 900 m | 抓到 |
| 1 km 相鄰改為 2 km | 抓到 |
| `ROUND_HALF_UP` 改為 half-even | 抓到 |
| 先以浮點數乘 1000 再取整 | 抓到 |
| 不合法的騎士位置退回自動辨識 | 抓到 |
| 回程反轉 | 抓到 |
| 分界本身也當取樣點 | 抓到 |
| 相同最遠距離時取最後一個 | 抓到 |
| 沒有行程型態時不報錯 | 抓到 |
| 前段改為整條軌跡 | 抓到 |
| `≥ 90%` 改為 `> 90%` | 第一次沒有抓到；新增 `test_exactly_90_percent_near_is_detected_and_less_is_not` 後抓到 |
| 給了折返位置時略過終點檢查 | 抓到 |
| 格網的格邊小於門檻的弦長 | 抓到 |
| 允許 m 等於或超過總長 | 抓到 |
| 只讀 `rtept` | 抓到 |
| 沒有 `trkpt` 時不改讀 `rtept` | 抓到 |
| 錯誤訊息接上路徑 | 抓到 |
| 接受 NaN／無限大的座標 | 抓到 |
| `target_gpx_ref` 不是檔案位元組的 SHA-256 | 抓到 |

## 7. Concerns

| # | 內容 | 建議的 owner／authority | 是否阻擋 |
| --- | --- | --- | --- |
| **C-15-1** | **狀態：已裁決——CL-R1-22（`decision-20261118-issue15-c151.md` 第 2 節，採 (b) 加可用條件與同距離規則，`RG-` 用 `c_k`），已在 `e78cc9f` 修改（第 9 節）。** 原內容：**騎士指定的折返位置落在兩個軌跡點之間時，怎麼切開。** CL-R1-10 第 4 項「以沿軌跡 m 公尺處為折返點」、範圍 (b)「在折返點把幾何切成去程與回程（折返點是兩段的分界）」，與 S64「任何情形下都沒有反轉或補造的軌跡點」在這個情形下讀不出唯一的做法。實際上 m 幾乎一定落在兩點之間（累計距離是浮點數，m 是整數）；連騎士指定的整數公尺等於自動判定的整數公尺時（S78），分界的累計距離也通常不是剛好的整數。合理的讀法至少有：(a) 在 m 處內插一個點，作為去程的終點與回程的起點（位置在既有線段上，但它是檔案中沒有的點，與 S64 的字面衝突）；(b) 以累計距離最接近 m 的軌跡點為分界（相同時取前一個）；(c) 以累計距離大於或等於 m 的第一個軌跡點為分界；(d) 以小於或等於 m 的最後一個軌跡點為分界。(b)–(d) 不新增點，但實際的分界不在 m，需要同時決定 `RG-` 的「實際採用的折返位置」記 m 還是那個點取整後的公尺（S78 與 CL-R1-18 第 2 項目前以 m 計算），以及 `turnaround_m` 欄位的值。目前的實作：m 剛好在某個點上時切在那一點；其他情形 `TurnaroundSplitUndecidedError`，不回傳路線（fail closed）。裁決後的修改集中在 `target_gpx.py` 的 `_point_at_exactly` 與其呼叫處，以及 S61、S78、S80 的完整流程測試 | Design Authority | 已解決（原為「是」） |
| C-15-2 | **狀態：已裁決——CL-R1-23 接受，程式不改（同 record 第 3 節）。** **無法讀取的檔案與壞點歸為 `target_gpx_invalid`（D-15-6）。** 4.13 只列「讀不到軌跡點或只有一點」等三種情形；檔案不存在、不是 GPX、座標壞掉歸為同一代碼，是依 5.5 的固定文字（「確認檔案路徑與內容」）與 fail closed 的判斷。另外接受 GPX 1.0 的命名空間；其他命名空間或沒有命名空間的檔案不讀。若 DA 認為檔案不存在應改為其他錯誤（例如呼叫端的例外），是一處的修改 | Design Authority（知悉） | 否 |
| C-15-3 | **狀態：已裁決——CL-R1-24（同 record 第 5 節）是 #16 的要求；本 Ticket 沒有動作。** `TargetGpxRoute` 的欄位名稱與形狀（`legs`、`turnaround_m`、`turnaround_source`）是本 Ticket 的 HOW；R1-4 的共用介面（範圍 (f)）要回傳「目標 GPX 的折返位置」與各方向的幾何、里程，屆時可直接使用或轉換。目標 GPX 沒有道路名稱，本 Ticket 不產生 | R1-4（#16）的 Executor／Design Authority（知悉） | 否 |

## 8. 剩餘工作

- ~~C-15-1 的 DA 裁決與依裁決的修改~~：已完成（CL-R1-22；`e78cc9f`；第 9 節）。
- 由 Orchestrator 依 Bindings 第 3.3、3.7 節派 R1；R1 的 pack 須含 `decision-20261118-issue15-c151.md`、`decision-20261118-issue14-c141.md`（CL-R1-18）與 `decision-20261118-issue13-c131.md`（CL-R1-13）（DA record 第 4.4 節）。受審 subject 是 `e78cc9f`。
- 真實目標 GPX 的行為 NOT VERIFIED（H-2；required authority = acceptor）。
- Tracked items（不是本 Ticket 的工作）：TI-C15-1（騎士指定與採用的折返位置不同時的顯示）、RV-11（SPEC-001 的文字同步）；owner＝Design Authority。

## 9. CL-R1-22 的修改（`decision-20261118-issue15-c151.md` 第 4 節）

### 9.1 修改（`0e4a93f` → `e78cc9f`；只改 DA record 第 4.1 節的三個檔案）

1. `src/moto_copilot/routing/target_gpx.py`：以 `rider_turnaround_index(cum, metres)` 與 `_usable(cum, index)` 取代 `_point_at_exactly`（CL-R1-22 第 2～4 項；D-15-8）；沒有可用的點時回傳 `target_gpx_not_round_trip`／`turnaround_unconfirmed`；`_round_trip` 改為由分界點的累計距離計算 `turnaround_m = c_k` 與 `RG-`（第 5 項），騎士指定與自動判定共用；自動判定的分界套用 `_usable`（第 6 項；偵測本身不變）；刪除 `TurnaroundSplitUndecidedError`；模組說明、`_round_trip` 與新函式的 docstring 改寫成 CL-R1-22 的定義並引用該 record，刪除「pending a Design Authority decision」等文字。說明 50 m／100 m／90% 是保守的啟發式、NOT validated with real data 的文字保留。
2. `src/moto_copilot/routing/__init__.py`：只移除 `TurnaroundSplitUndecidedError` 的 import 與 `__all__` 項目。
3. `tests/test_target_gpx.py`：見第 9.3 節（E-5）與第 9.2 節的 E-2。
4. `src/moto_copilot/ingest/` 沒有修改（`git diff b771d9f e78cc9f -- src/moto_copilot/ingest` 為空）。`git diff --stat b771d9f e78cc9f` 的程式與測試部分：`routing/__init__.py` 2 行刪除、`routing/target_gpx.py` 與 `tests/test_target_gpx.py`；其餘是 record-only 路徑（DA record、run record、本 worklog）。
5. 依 SA-1 本機 commit `e78cc9f`，message 註明 CL-R1-22；暫存的只有上列三個檔案（`git diff --cached --name-only` 確認），不含 `.env`、GPX、FIT 或 `data/`。沒有 push、沒有碰 GitHub；沒有讀取、列出或搜尋 `data/`；沒有讀或執行 `experiments/`；沒有讀 `.env`。

### 9.2 Verification（subject `e78cc9f`）

**E-1。** `.venv/Scripts/python.exe -m pytest -q`，exit 0，完整輸出：

```text
........................................................................ [  4%]
........................................................................ [  8%]
........................................................................ [ 13%]
........................................................................ [ 17%]
........................................................................ [ 22%]
........................................................................ [ 26%]
........................................................................ [ 31%]
........................................................................ [ 35%]
........................................................................ [ 39%]
........................................................................ [ 44%]
........................................................................ [ 48%]
........................................................................ [ 53%]
........................................................................ [ 57%]
........................................................................ [ 62%]
........................................................................ [ 66%]
........................................................................ [ 70%]
........................................................................ [ 75%]
........................................................................ [ 79%]
........................................................................ [ 84%]
........................................................................ [ 88%]
........................................................................ [ 93%]
........................................................................ [ 97%]
.........................................                                [100%]
1625 passed in 32.05s
```

`1607` − `2`（刪除／改寫的測試，第 9.3 節）＋ `20`（新增的案例）＝ `1625`；`tests/test_target_gpx.py` 是 169 個案例。`grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。測試後 `git status --short` 為空；`git ls-files` 沒有 `data/`、`.gpx`、`.fit`、`.env`。

**E-2（更新的列；各列依 CL-R1-22）。** 其他各列（S27、S43、S59、S60、S62、S63、S79、S58、S10、「另加」三列）的測試名稱不變，在 `e78cc9f` 上重新執行全部 PASS（E-1）。

| AC | 測試 | 結果 |
| --- | --- | --- |
| S61（環狀、指定折返位置後以那個位置切開） | T-1 `test_t1_s61_a_loop_is_cut_at_the_nearest_track_point_to_the_riders_position`（完整流程，不替換累計距離：m 嚴格落在兩點之間，較接近後一點時切在後一點、較接近前一點時切在前一點；`turnaround_m = c_k ≠ m`；`route_id == target_gpx_route_id(ref, "round_trip", c_k)`）；T-5 `test_t5_every_legal_whole_metre_gives_the_route_the_definition_selects[loop/out_and_back/figure_eight/sparse_loop]`；保留的 `test_a_loop_is_cut_at_the_riders_position_when_a_point_is_there`（替換累計距離，只測剛好在點上的切開） | **PASS**（原為 BLOCKED） |
| S80（明確去回同路的軌跡上，騎士指定的另一個合法位置為準） | T-2 `test_t2_s80_on_a_clear_out_and_back_the_riders_position_wins_between_points`（完整流程：m = 1234 落在兩點之間，切在 CL-R1-22 選到的點（索引 25，`c_k = 1250`），不是最遠點，`turnaround_source == "rider"`）；`test_an_illegal_turnaround_on_a_clear_out_and_back_does_not_fall_back_to_detection`；保留的 `test_the_riders_legal_position_wins_over_the_detected_one` | **PASS**（原為 BLOCKED） |
| S78 | T-3 `test_t3_s78_full_flow_rider_and_detected_with_equal_metres_give_the_same_route`（完整流程，不替換累計距離；最遠點的累計距離不是整數：自動判定與騎士給 `c_F / 1000` km 的 `turnaround_m`、`route_id` 與兩段的點都相同；`c_F + 3` m 選到同一點，`route_id` 相同；`c_F − 200` m 選到另一點，`route_id` 不同；單向與來回不同）；先前的 `test_s78_same_file_same_turnaround_metres_same_route_id_different_metres_different`、`test_s78_through_the_route_rider_and_detected_with_equal_metres_give_the_same_route_id`、`test_route_id_is_rg_plus_the_first_10_hex_of_the_defined_text`、`test_a_different_file_gives_a_different_route_id` | **PASS**（完整流程的騎士指定部分原受 C-15-1 影響） |
| S64（T-6） | `assert_slices_of_the_file` 加上：各段的點都在檔案中；去程長度 `== cum_k`、回程長度 `== total − cum_k`、總長 `== cum_{n-1}`、`turnaround_m == c_k`、`route_id` 依 `c_k`（完全相等，不是近似）。用在 T-1、T-2、T-3、T-5（每一個被掃過的 m）與所有既有的回傳路線測試；替換累計距離的兩個測試以 `lengths=False` 只檢查點 | PASS，新的切法也涵蓋 |
| 選點的定義（T-4） | `test_t4_the_selection_follows_the_definition`（9 組：0.5 同距離取索引小；`1023.9`／`1024.1` 在 `Decimal` 下同距離、在浮點數的差下不同距離；重複的點取第一個；最近的是起點時取第一個可用點；最近的是終點時取最後一個可用點；`0 < cum` 但 `c = 0` 不可用；`c = total` 不可用；沒有可用的點；精確比較取較近者），每一組也與測試自己的 `Decimal` oracle 相同；`test_t4_no_usable_point_through_the_route_is_turnaround_unconfirmed`（替換累計距離，經由完整流程回傳 `turnaround_unconfirmed`）；`test_a_detected_boundary_that_is_not_usable_is_turnaround_unconfirmed[start/end]`（第 6 項的防禦，替換偵測函式） | PASS |
| 既有行為的回歸（T-7） | `test_illegal_turnaround_positions_are_not_round_trip`（0、負數、取整為 0、超大、NaN、±inf）、`test_a_turnaround_at_or_beyond_the_total_length_is_not_round_trip`、`test_an_illegal_turnaround_on_a_clear_out_and_back_does_not_fall_back_to_detection`、`test_round_trip_whose_end_is_not_at_the_start_is_not_round_trip_even_with_a_turnaround`、`test_one_way_uses_the_geometry_as_it_is_even_when_start_and_end_meet` | PASS |
| CL-R1-18 第 6 項 | 先前各測試，加上 T-3（騎士指定與自動判定的整數公尺相等時 `route_id` 相同，經由完整流程） | PASS |

**E-6（新 subject 上的 self-verification；不是 independent audit）。**
- **H-4**：DA record 第 4.2 節要求的突變（session scratchpad 的腳本在記憶體中替換原始碼字串，跑 `tests/test_target_gpx.py`，在 `finally` 中寫回原文；結束後 `git status --short` 只有尚未 commit 的三個檔案）：

| 突變 | 結果 |
| --- | --- |
| 同距離時取索引大的（`<` 改為 `<=`） | 抓到（4 個失敗） |
| 改成 (c)「`D_i ≥ m` 的第一個可用點」 | 抓到（11） |
| 改成 (d)「`D_i ≤ m` 的最後一個可用點」 | 抓到（10） |
| `turnaround_m`／`RG-` 改用 m 而不是 `c_k` | 抓到（7） |
| 拿掉可用條件（起點或終點可作分界） | 抓到（10） |
| 只保留第一個可用條件（拿掉 `0 < c_i < total`） | 抓到（3） |
| 在 m 處內插一點作為分界 | 抓到（10） |
| 以浮點數的差比較距離 | 抓到（1：T-4 的 `1023.9`／`1024.1` 一組） |
| 自動判定的分界不檢查可用條件 | 第一次沒有抓到；新增 `test_a_detected_boundary_that_is_not_usable_is_turnaround_unconfirmed` 後抓到（2） |

  第 6 節 E-6 的 23 項突變在 `e78cc9f` 的原始碼上重跑，全部抓到。
- **H-2**：結果與錯誤仍不含路徑與檔名：第 6 節列出的隱私測試在新 subject 上通過；`test_the_held_split_error_carries_no_path` 改為 `test_a_rider_turnaround_route_carries_no_path`（騎士指定的路線的 `repr` 與欄位不含目錄名與檔名，沒有 log）。diff 中的座標全部是合成的（第 6 節 E-3；新測試只用 `circle()`、`out_and_back()`、`figure_eight()` 與手寫的累計距離數列）。真實目標 GPX 的行為仍 **NOT VERIFIED**，required authority = acceptor（RB-7）。
- **H-3**：說明文字仍寫明 50 m／100 m／90% 是保守的啟發式門檻、NOT validated with real data；`test_the_detection_is_described_as_not_validated` 在新 subject 上通過。新增的文字沒有把選點或自動辨識稱為已驗證。

### 9.3 E-5：刪除或改寫的既有測試（`b771d9f` 中由本 Ticket 新增的測試）

| 測試 | 處置 | 理由 |
| --- | --- | --- |
| `test_a_legal_turnaround_between_track_points_is_held_for_the_design_authority` | 刪除，由 T-1、T-2 取代 | 它驗證 `TurnaroundSplitUndecidedError`，CL-R1-22 使合法的 m 一律回傳路線，該例外依 DA record 第 4.1 節刪除 |
| `test_the_held_split_error_carries_no_path` | 改寫為 `test_a_rider_turnaround_route_carries_no_path` | 同上；改為檢查同一個輸入（環狀、1.2345 km）回傳的路線不含路徑與檔名 |
| `assert_slices_of_the_file`（輔助函式） | 加上 T-6 的長度、`c_k` 與 `route_id` 檢查；新增參數 `lengths` | DA record 第 4.2 節 T-6；替換累計距離的兩個保留測試以 `lengths=False` 呼叫，因為它們的長度是替換後的值 |

保留的 `test_a_loop_is_cut_at_the_riders_position_when_a_point_is_there`、`test_the_riders_legal_position_wins_over_the_detected_one`、`test_s78_through_the_route_rider_and_detected_with_equal_metres_give_the_same_route_id`（替換累計距離）沒有修改斷言，只在前兩者加上 `lengths=False`；S61、S78、S80 另有不替換累計距離的完整流程測試（T-1～T-3）。#9、#13、#14 的測試沒有修改。

### 9.4 Binding

Executor 自行觀測（`e78cc9f` 之後、寫本節之前）：agentId `ae0a2f33f0da61e65`（同一個 agent，以 SendMessage 續派），(`claude-opus-5-5`, `high`) 104 則，集合只有一個元素。**這是自我觀測，不是派工者的核對。**
