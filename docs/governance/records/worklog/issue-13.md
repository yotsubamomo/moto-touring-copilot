# Worklog — Issue #13（SPEC-R1 R1-1）`contracts`：ID 樣式的放寬與契約 2 的 v0.3

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #13（SPEC-R1 R1-1），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **R1 BLOCKING（R1-F1）的 targeted correction 已完成（`3c065f8`），待 R2（第 9 節）。** 以下為先前狀態：**Executor 工作完成，待 R1。** C-13-1 已由 Design Authority 裁決（`decision-20261118-issue13-c131.md`，CL-R1-12、CL-R1-13），依該 record 第 5 節修正 `build_route`（`6ec1903`），pytest `875 passed`（第 6 節 V-1）。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure。歷程：`153adca` 時為 NEEDS_DA（`1 failed, 874 passed`）→ DA 裁決 → `6ec1903` |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `1fd1de3585ea23f80842ac3276fe9305369b51e3`（`1fd1de3`，派工時的 HEAD，含 #10 的最終 commit 與 `_whole_count`）；實作 commit **`153adcadfdf02f3697ba47f8912ac444c1a3f8d3`**（`153adca`）；CL-R1-12 的實作 commit **`6ec1903632a1fbff90405de2627eb9dee5d51950`**（`6ec1903`，父 commit 是 DA record 的 `5c2e0e8`），R1 的受審 subject。R1-F1 的 correction commit **`3c065f8d9d433aa00253078b209dd025d154df2b`**（`3c065f8`，父 commit 是 R1 record 的 `e5dfe5e`），是**最終 implementation subject**。worklog 在另外的 record-only commits |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：Issue #13 的內文。Orchestrator 提供的 scratchpad 原文檔（`issue-13-body.md`）UTF-8 SHA-256 `d432868613aac749018d14bf79e45ca06673508e9e3e8d9919c34bd432456584`，Executor 以 `sha256sum` 重算相同，等於派工內容所述 run record 第 4 節的值。沒有呼叫 GitHub，沒有修改 Issue。
- **Spec**：SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md`）：第 2 節引用段落；第 4 節 DD-R1-1（不新增目標 GPX 的雜湊欄位）、CL-R1-1（資料與網路）；第 5 節 R1-1 列（範圍 (a)–(e)、AC (1)–(5)、排除、高風險類別「不涉及」）與 E-1～E-6。
- **CL-R1-11**：`decision-20261118-issue10-c107.md` §3.2：契約 2 不變條件 2 以 `_whole_count` 取得 `after_seg_count` 與 `n_segments`；AC (4) 的不變條件 2 另加整數值 float（含 JSON round trip）的超出範圍值。
- **CL-R1-12、CL-R1-13**：`decision-20261118-issue13-c131.md`（v1，2026-11-18，HEAD `5c2e0e8` 時已 commit）。CL-R1-12 把 R1-1 的範圍加上 (f)：`build_route` 的路線紀錄加上 `"route_source": "trip"`、`"snapshot_id": None`、`"trip_type": "one_way"`，只能改 `routes/catalog.py`（第 5.1 節的封閉清單），證據 V-1～V-7（第 5.2 節）。CL-R1-13 接受 D-13-1。這是執行中的契約變更（DA 依治理 §5.3 第 2 類修訂 derived contract），不是 Executor 的決定。
- **CL-B1-2**（`derivation-spec-b1.md`）：`CONTRACT_VERSION` 在本 Ticket 改為 `"0.3"`。
- **規格來源**：`DESIGN.md` §5 共通規則的 ID 列、契約 1 的 `route_id`、契約 2 全部（欄位表與不變條件 1–5）、契約 4 的 `route_id` 與 `breaks[].after_checkpoint_id`；`docs/spec/SPEC-001-plan-schema.md` §2 的「ID」列（三個樣式）、第 9 節 S37、S58。
- **高風險類別**：`decision-20261117-high-risk-categories.md`；R1-1 標為「不涉及」（§3.1–§3.4 的判定項目都不符合，見第 6 節 E-6）。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-a95eaf00e5bb8b468.{meta.json,jsonl}`；`meta.json` 的 `agentType` 是 `gov-executor`。
- Executor 自行觀測（實作 commit 之後、寫本 worklog 之前，以第 3.6 節的掃描方式）：agentId `a95eaf00e5bb8b468`，(`claude-opus-5-5`, `high`) 89 則，集合只有一個元素。CL-R1-12 的修正（同一個 agent，以 SendMessage 續派）在 `6ec1903` 之後再觀測一次：(`claude-opus-5-5`, `high`) 108 則，集合仍只有一個元素。**這是自我觀測，不是派工者的核對**；之後的訊息不在這個數字內，Orchestrator 採用本 return 前須自行核對全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 Bindings m3、impl-default v2 §3–§5、§9、治理 §3.5、§3.7、derivation-spec-r1（全文）、CL-R1-11 record（全文）、高風險類別 record §3.4、Issue #13 原文（核對雜湊）、`DESIGN.md` §5（契約 1–4、共通規則）、SPEC-001 §2 的 ID 與雜湊列、S37、S58、`contracts/` 全部、`tests/test_contracts.py`、`tests/conftest.py`、mock fixture、`routes/catalog.py`、`tests/test_routes_pace_eta.py`、`tests/test_eta.py`、`tests/test_integration_b1.py` 的相關段落。
2. 基準：`1fd1de3` 上 `.venv/Scripts/python.exe -m pytest -q` 為 `614 passed`。
3. `src/moto_copilot/contracts/schemas.py`：
   - `CONTRACT_VERSION = "0.3"`（CL-B1-2）；模組說明改為 v0.3。
   - 新增 `ROUTE_ID_PATTERN`、`CHECKPOINT_ID_PATTERN`、`SNAPSHOT_ID_PATTERN`（SPEC-001 §2 的三個樣式，寫法見 D-13-1），由 `_ROUTE_ID`、`_CHECKPOINT_ID`、`_SNAPSHOT_ID` 使用。因為契約 1 的 `route_id`、契約 2 的三種紀錄、契約 4 的 `route_id` 與 `_BREAK.after_checkpoint_id` 原本就引用 `_ROUTE_ID`／`_CHECKPOINT_ID`，範圍 (a) 的四處都以同一個定義生效。
   - `ROUTE`：`source_trip_id` 可為 null；新增 `route_source`（`trip`／`routing`／`target_gpx`）、`snapshot_id`（null 或 `SN-` 樣式）、`trip_type`（`one_way`／`round_trip`）。`CHECKPOINT.kind` 新增 `turnaround`。新增常數 `ROUTE_SOURCES`、`TRIP_TYPES`。
   - 不新增目標 GPX 的雜湊欄位（DD-R1-1）。
4. `src/moto_copilot/contracts/validate.py`（`validate_route_catalog` 與三個新的 helper）：
   - 不變條件 2：`after_seg_count` 與 `n_segments` 以 `_whole_count` 計數；兩者都可計數才比較；訊息樣板不變（印出原始值）；不可計數時不另加訊息（schema 已回報）（CL-R1-11）。
   - 不變條件 4：`round_trip` 的路線恰有一個 `turnaround`，其 `after_seg_count`（以 `_whole_count` 計數）滿足 0 < c < n；`one_way` 的路線沒有 `turnaround`。`trip_type` 不是這兩個值時不檢查（schema 已回報）。
   - 不變條件 5（`_route_source_errors`）：`trip` → `source_trip_id` 有值、`snapshot_id` 為 null；`routing` → 相反；`target_gpx` → 兩者都是 null。`route_source` 不是三個值之一時不檢查（schema 已回報）。
   - AC (3)：`route_id` 符合樣式時，其格式（`R`＋兩位數字／`RS-`／`RG-`）必須對應 `route_source`；`routing` 且 `snapshot_id` 符合樣式時，`RS-` 的 10 碼必須等於 `snapshot_id` 的 10 碼。
   - AC (2)：`checkpoint_id` 與 `route_id` 都符合樣式時，`checkpoint_id` 去掉 `-CP<數字>` 的前綴必須等於它的 `route_id`。
   - 模組說明改為 v0.3。其他函式與檢查（契約 1、3、4，`_whole_count` 本身、#10 的修改）沒有變更。
5. `src/moto_copilot/contracts/__init__.py`、`__main__.py`：說明字串的「v0.2」改為「v0.3」。CLI 的行為不變，輸出第一行因 `CONTRACT_VERSION` 改為 `data contracts v0.3`。
6. `tests/fixtures/contract_v02/mock_dataset.json`：`_meta.contract_version` 改為 `"0.3"`、`note` 改寫；R01、R02 加上 `"route_source": "trip"`、`"snapshot_id": null`、`"trip_type": "one_way"`。其他內容（含所有數值與座標）不變。目錄名稱 `contract_v02` 不改（D-13-5）。
7. `tests/test_contracts.py`：一個既有測試改版本斷言（第 6 節 E-5）；新增 261 個測試案例（第 6 節 E-2）。`tests/test_eta.py`、`tests/test_integration_b1.py`：手寫的路線紀錄加上三個 v0.3 欄位（E-5）。
8. 自我驗證：全套 pytest、contracts CLI、9 個突變檢查（第 6 節）。
9. 依 SA-1 在 topic branch 作本機 commit `153adca`；commit 前確認暫存的只有上列 8 個檔案，不含 `.env`、GPX、FIT 或 `data/`。沒有 push、沒有開 PR、沒有碰 GitHub。
10. `153adca` 時**沒有修改** `routes/catalog.py` 與 `tests/test_routes_pace_eta.py`，以 NEEDS_DA 回報 C-13-1。
11. 讀取 DA record `decision-20261118-issue13-c131.md` 全文後，依其第 5.1 節修改 `src/moto_copilot/routes/catalog.py`（CL-R1-12）：`build_route` 的 `route` dict 加上 `"route_source": "trip"`、`"snapshot_id": None`、`"trip_type": "one_way"`，前面加一行註解引用該 record；模組說明第一行改為「Route Catalog records with the contract 2 v0.3 route fields; building the catalog is still the Pre-Spec Spike (G-RTE).」。簽名、參數、import、路段、檢查點、`common_stretch`、`align_to_route`、`routes/__init__.py` 都沒有改；沒有修改任何測試；沒有加 xfail／skip。本機 commit `6ec1903`，暫存的只有這一個檔案。

## 4. Decisions and assumptions

| # | 決定 | 依據 |
| --- | --- | --- |
| D-13-1 | 三個樣式在程式中寫成 `^(R[0-9]{2}\|R[SG]-[0-9a-f]{10})$(?!\n)` 等形式：以 `[0-9]` 代替 `\d`，並在 `$` 之後加 `(?!\n)`。SPEC-001 的文字照原樣寫在 `schemas.py` 的註解中 | jsonschema 以 Python `re.search` 執行 pattern。Python 的 `\d` 也比對非 ASCII 數字、`$` 也比對結尾換行之前，實測 `re.search(r"^R\d{2}$", "R01\n")` 與 `"R١٢"` 都成立。SPEC-001 的樣式是 JSON Schema（ECMA-262）語法，在那個語義下 `\d` 只是 ASCII 數字、`$` 只在字串結尾；兩種寫法在 ECMA-262 下接受的字串相同。這是同一個樣式的忠實實作，不是語義的改變；以測試（`R01\n`、全形與阿拉伯–印度數字）與突變檢查 M3、M4 驗證。`trip_id` 與 `datetime` 的既有樣式有同樣的問題，不在 R1-1 範圍，沒有修改（C-13-2） |
| D-13-2 | AC (2)、AC (3) 的交叉檢查只在相關欄位都通過樣式時執行；欄位不合樣式或 `route_source` 不合列舉值時只由 schema 回報 | 避免對已被 schema 拒絕的值重複或誤導的訊息；結果仍不是空的（fail closed） |
| D-13-3 | `snapshot_id`、`source_trip_id` 是「欄位必須存在、值可為 null」 | `_record` 既有的慣例（模組說明「nullable ones may hold null」），與契約 2 檢查點的 `name`、`station_ref` 相同；DESIGN「必填：否」在既有程式中都是這樣實作 |
| D-13-4 | AC (4) 的不變條件 3（「同一個位置可以有多個檢查點，以 `checkpoint_id` 區分」）的違反案例是「同一個位置的兩個檢查點有相同的 `checkpoint_id`」，由既有的主鍵重複檢查拒絕（訊息 `checkpoints: duplicate primary key R01-CP01`，沒有 `(invariant 3)` 字樣） | 不變條件 3 是允許性的規則，唯一可以違反的內容是「以 `checkpoint_id` 區分」。沒有改既有訊息 |
| D-13-5 | Fixture 目錄名稱 `contract_v02` 保留 | `CLAUDE.md` 與派工內容的 AC (5) 指令使用這個路徑；改名會改動範圍外的文件與指令 |
| D-13-6 | R01、R02 定為 `route_source: trip`、`trip_type: one_way` | 兩條都有 `source_trip_id`（T002），起訖點座標不同（模擬值），沒有 `turnaround`；`trip` 是 R01／R02 的唯一合法來源（SPEC-001 §2：`R` 加兩位數字是示範路線） |
| D-13-7 | `RS-`／`RG-`、來回行程的案例在測試內由 fixture 的副本建立，不加進共用 fixture | 共用 fixture 被其他測試使用（例如 ETA 與配速）；AC (5) 只要求更新後的模擬資料集沒有違反、R01／R02 保持有效 |
| D-13-8 | 不變條件 4 的 `after_seg_count` 也以 `_whole_count` 計數 | CL-R1-11 的同一原則（契約檢查對 schema 接受的每一種整數表示都執行）；否則 `4.0` 的折返點會略過範圍檢查。以測試涵蓋 `0.0`、`4.0`、`2.0` 與 JSON round trip |
| D-13-9 | 契約 2 的路線紀錄與 `source_trip_id` 指向的行程是否存在，不檢查 | `validate_route_catalog` 不接收衍生路段表；不在 R1-1 的 AC；沒有新增 |

## 5. Artifacts

| 檔案 | 變更（`1fd1de3` → `153adca`） |
| --- | --- |
| `src/moto_copilot/contracts/schemas.py` | v0.3 ID 樣式、契約 2 欄位、`turnaround`、`CONTRACT_VERSION = "0.3"` |
| `src/moto_copilot/contracts/validate.py` | 不變條件 2（`_whole_count`）、4、5，`checkpoint_id` 前綴，`route_id`／`route_source`／`snapshot_id` 一致性 |
| `src/moto_copilot/contracts/__init__.py`、`__main__.py` | 說明字串 v0.3 |
| `tests/fixtures/contract_v02/mock_dataset.json` | v0.3 欄位與 `_meta` |
| `tests/test_contracts.py` | 1 個既有測試修改、新增 261 個測試案例 |
| `tests/test_eta.py`、`tests/test_integration_b1.py` | 手寫路線紀錄加上 v0.3 欄位 |
| `src/moto_copilot/routes/catalog.py`（`153adca` → `6ec1903`） | `build_route` 的路線紀錄加上三個 v0.3 欄位、一行引用註解、模組說明第一行（CL-R1-12） |

`git diff --stat 1fd1de3 153adca`：8 files changed, 433 insertions(+), 24 deletions(-)。`153adca` → `6ec1903` 的程式變更只有 `catalog.py`（V-3）。

## 6. Verification

### E-1／V-1 pytest（最終 subject `6ec1903`，`git status --short` 為空）

`PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m pytest -q`，exit code **0**，完整 stdout：

```text
........................................................................ [  8%]
........................................................................ [ 16%]
........................................................................ [ 24%]
........................................................................ [ 32%]
........................................................................ [ 41%]
........................................................................ [ 49%]
........................................................................ [ 57%]
........................................................................ [ 65%]
........................................................................ [ 74%]
........................................................................ [ 82%]
........................................................................ [ 90%]
........................................................................ [ 98%]
...........                                                              [100%]
875 passed in 27.42s
```

摘要只有 `passed`，沒有 `failed`、`error`、`xfailed`、`xpassed`、`skipped`。數目 875 與 DA record 的預期相同。**E-1 達成。**

### V-2 沒有 xfail／skip 標記

`grep -rnE "xfail|pytest\.mark\.skip" tests/`：沒有輸出（exit 1，0 筆）。

### V-3 修改範圍

- `git diff --stat 153adca 6ec1903`：

```text
 .../decisions/decision-20261118-issue13-c131.md    | 163 +++++++++++++++++
 .../records/run/run-20261117-oc1-run2.md           |   4 +-
 docs/governance/records/worklog/issue-13.md        | 201 +++++++++++++++++++++
 src/moto_copilot/routes/catalog.py                 |   4 +-
 4 files changed, 370 insertions(+), 2 deletions(-)
```

  record-only 路徑（`docs/governance/records/**`）之外只有 `src/moto_copilot/routes/catalog.py`。
- `git diff 153adca 6ec1903 -- src/moto_copilot/routes/catalog.py` 全文：

```diff
@@ -1,4 +1,4 @@
-"""Route Catalog (data contract v0.2, contract 2) from private trimmed tracks.
+"""Route Catalog records with the contract 2 v0.3 route fields; building the catalog is still the Pre-Spec Spike (G-RTE).
 
 Pre-Spec Technical Spike (M1-B). A demo route is the longest stretch that several trips ride in
 the same direction; its geometry comes from one of them (the source trip).
@@ -177,6 +177,8 @@ def build_route(route_id: str, name: str, path: list[TrackPoint], *, source_trip
                          "end_lat": round(seg_path[-1].lat, 6), "end_lon": round(seg_path[-1].lon, 6)})
     route = {"route_id": route_id, "name": name, "n_segments": len(segments),
              "total_length_m": segments[-1]["cum_length_m"], "source_trip_id": source_trip_id,
+             # From a trip, one way, no turnaround: CL-R1-12 (decision-20261118-issue13-c131)
+             "route_source": "trip", "snapshot_id": None, "trip_type": "one_way",
              "category_scheme": params.category_scheme, "catalog_version": catalog_version}
     checkpoints = [
         {"checkpoint_id": f"{route_id}-CP01", "route_id": route_id, "kind": "start", "after_seg_count": 0,
```

  內容只有第 5.1 節第 1–3 項（三個鍵、一行註解、模組說明第一行）。模組說明第一行原本的「from private trimmed tracks」沒有保留；第三行起的說明不變。
- `git diff 1fd1de3 6ec1903 -- tests/test_routes_pace_eta.py`：空（0 bytes）。

### 修正前的 E-1（subject `153adca`，歷程，不作為結案證據）

`PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`，exit code **1**，完整 stdout：

```text
........................................................................ [  8%]
........................................................................ [ 16%]
........................................................................ [ 24%]
........................................................................ [ 32%]
........................................................................ [ 41%]
........................................................................ [ 49%]
........................................................................ [ 57%]
........................................................................ [ 65%]
........................................................................ [ 74%]
...............................................................F........ [ 82%]
........................................................................ [ 90%]
........................................................................ [ 98%]
...........                                                              [100%]
================================== FAILURES ===================================
______________ test_build_route_conforms_to_the_catalog_contract ______________

    def test_build_route_conforms_to_the_catalog_contract():
        route, segments, checkpoints = build_route("R09", "合成直線（測試）", straight(6_300), source_trip_id="T900",
                                                   catalog_version="catalog-test")
>       assert validate_route_catalog([route], segments, checkpoints) == []
E       assert ['routes[0] s...red property'] == []
E         
E         Left contains 3 more items, first extra item: "routes[0] schema: (record): 'route_source' is a required property"
E         Use -v to get more diff

tests\test_routes_pace_eta.py:94: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_routes_pace_eta.py::test_build_route_conforms_to_the_catalog_contract
1 failed, 874 passed in 26.77s
```

`153adca` 時 E-1 沒有達成：`874 passed, 1 failed`。失敗的是 `build_route` 的既有測試；三項違反是 `'route_source'`、`'snapshot_id'`、`'trip_type' is a required property`（另以 `PYTHONPATH="src;tests"` 直接呼叫 `build_route` 與 `validate_route_catalog` 確認只有這三項）。它不是契約驗證程式的缺陷，而是當時範圍外的產生者沒有跟上 v0.3（C-13-1，已由 CL-R1-12 處理）。`tests/test_contracts.py` 單獨執行：`503 passed`。

### AC (5) 的 contracts CLI

`PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`，在 `153adca` 與 `6ec1903` 都是 exit code 0，輸出相同：

```text
data contracts v0.3: tests\fixtures\contract_v02\mock_dataset.json
  derived_segments: OK
  route_catalog: OK
  pace_table: OK
  eta_output: OK
```

### E-2 AC 對應的測試（全部在 `tests/test_contracts.py`，結果都是 PASS）

| AC | SPEC-001 第 9 節 | 測試 |
| --- | --- | --- |
| (1) 樣式；`R01`／`R02` 仍有效；不符合的值被拒絕 | S37、S58（屬於契約的部分） | `test_r01_and_r02_stay_valid_trip_routes`；`test_s37_s58_every_route_id_format_passes_in_contracts_1_2_and_4`（5 例：R01→`RS-`、`RG-`、`R99`，R02→`RS-`、`RG-`；R01 的改名同時涵蓋契約 1 的 `route_id`、契約 4 的 `route_id` 與 `breaks[].after_checkpoint_id`）；`test_routes_of_all_three_sources_in_one_catalog`；`test_checkpoint_id_has_two_or_three_digits`（12 例）；`test_a_break_may_use_a_three_digit_checkpoint`；`test_s37_s58_a_route_id_of_another_format_is_rejected`（23 個值 × 5 個位置＝115 例：契約 2 的路線、路線路段、檢查點，契約 1，契約 4）；`test_s37_s58_a_checkpoint_id_of_another_format_is_rejected`（15 例）；`test_s37_s58_a_break_at_a_checkpoint_id_of_another_format_is_rejected`（15 例）；`test_s58_a_snapshot_id_of_another_format_is_rejected`（12 例）。被拒絕的值包含位數不對、大寫十六進位、錯誤前綴、前後空白、結尾換行、全形與阿拉伯–印度數字 |
| (2) `checkpoint_id` 的前綴等於 `route_id` | — | `test_checkpoint_id_starts_with_its_route_id`（4 例）；`test_checkpoint_id_of_an_rs_route_starts_with_that_route_id`（3 例，含同格式不同十六進位） |
| (3) `route_source` 與 ID 一致；`RS-` 的十六進位等於 `snapshot_id` | — | `test_route_id_format_must_agree_with_route_source`（6 例：三種來源各兩種錯誤格式；同時斷言沒有不變條件 5 或 schema 的違反，只因 ID 不一致而被拒絕）；`test_rs_route_id_has_the_hex_digits_of_its_snapshot_id`（不一致被拒絕、一致時沒有違反） |
| (4) 不變條件 1–5 各有一例被拒絕（4、5 為 v0.3） | — | `test_each_contract_2_invariant_has_a_rejected_violation`（5 例，每例先確認原資料沒有違反）。另：不變條件 2 的 CL-R1-11 `test_invariant_2_counts_whole_number_floats`（8 組 × 原物件／JSON round trip＝16 例：`9.0`、`5.0` 與 `n_segments` `4.0` 的超出範圍值被拒絕，`3.0`、`4.0`、`0.0` 的範圍內值沒有違反；round trip 後確認值仍是 float）、`test_an_after_seg_count_that_cannot_be_counted_is_still_a_violation`（7 例，含 1.5、`True`、`None`、`"3"`、NaN、Infinity、−1.0）；不變條件 4 的 `test_round_trip_with_one_turnaround_inside_the_route_passes`（4 例）、`test_a_break_may_be_at_the_turnaround`、`test_invariant_4_round_trip_needs_one_turnaround_strictly_inside`（6 × 2＝12 例：折返點在 0、n、`0.0`、`4.0`，兩個折返點，沒有折返點）、`test_invariant_4_one_way_route_has_no_turnaround`；不變條件 5 的 `test_invariant_5_route_source_decides_which_reference_is_set`（6 例，三種來源各兩個欄位） |
| (5) 模擬資料集沒有違反；既有測試全數通過 | — | **達成（V-4）。** `test_mock_fixture_conforms_to_every_contract`（既有）、`test_r01_and_r02_stay_valid_trip_routes`、`test_contracts_cli_reports_no_violation_for_the_mock_fixture`（以 subprocess 執行 CLI，exit 0）；contracts CLI 照常 exit 0；既有測試全數通過：V-1（`875 passed`，含原文未改的 `test_build_route_conforms_to_the_catalog_contract`） |
| 範圍 (b) 的 schema 欄位 | — | `test_a_v02_route_record_without_the_v03_fields_is_rejected`（4 例）、`test_route_source_and_trip_type_have_fixed_values`（10 例）、`test_checkpoint_kind_turnaround_is_spelled_exactly`（3 例） |
| 範圍 (d) `CONTRACT_VERSION` | — | `test_fixture_is_marked_as_mock`（既有，修改，E-5） |

### 突變檢查（self-verification，不是 audit）

以 scratchpad 的腳本逐一暫時修改程式、執行 `tests/test_contracts.py`、在 `finally` 還原原始位元組；全部完成後 `git diff --stat` 與修改前相同，`tests/test_contracts.py` 再跑一次 `503 passed`。

| # | 突變 | 結果 |
| --- | --- | --- |
| M1 | 不變條件 2 換回 `isinstance(..., int)` 的條件 | 9 failed |
| M2 | 拿掉 `checkpoint_id` 前綴檢查 | 7 failed |
| M3 | 樣式中拿掉 `(?!\n)` | 13 failed（全部是結尾換行的案例） |
| M4 | `ROUTE_ID_BODY` 的 `[0-9]` 換回 `\d` | 10 failed |
| M5 | 拿掉 `RS-`／`SN-` 十六進位相等檢查 | 1 failed |
| M6 | 拿掉不變條件 4 | 13 failed |
| M7 | 拿掉不變條件 5 | 7 failed |
| M8 | 拿掉 `route_id` 格式與 `route_source` 的一致性檢查 | 6 failed |
| M9 | 折返點範圍改成 0 ≤ c ≤ n | 8 failed |

### E-3 合成資料

新增測試的資料都是 mock fixture 的副本在測試內修改，或手寫的常數：十六進位 `a1b2c3d4e5`、`0f9e8d7c6b` 是隨意選的，不是任何快照或 GPX 的雜湊。沒有新增座標；fixture 的座標（10.01, 20.01 等）原本就是模擬值，沒有改動。diff 中沒有真實軌跡、住家附近的座標或私有路線，也沒有公開地標的座標。

### E-4 沒有網路請求

R1-1 的程式只做 JSON Schema 與字串、整數的比較；schema 沒有 `$ref`，jsonschema 不會取得遠端資源。新增的 CLI 測試以 `subprocess` 在本機執行 `python -m moto_copilot.contracts` 讀 fixture 檔。沒有任何測試使用 socket、HTTP client 或路線引擎。

### E-5 因契約改版而修改的既有測試

| 測試 | 修改 | 理由 |
| --- | --- | --- |
| `tests/test_contracts.py::test_fixture_is_marked_as_mock` | 斷言 `"0.2"` 改為 `"0.3"` | CL-B1-2：`CONTRACT_VERSION` 在本 Ticket 改為 `"0.3"`；fixture 的 `_meta.contract_version` 同步改。斷言的強度不變（仍要求三者相等） |
| `tests/test_eta.py` 的 `catalog()`（被 `test_synthetic_inputs_conform_to_contracts_2_and_3` 等使用） | 手寫的 R05–R07 路線紀錄加上 `"route_source": "trip"`、`"snapshot_id": None`、`"trip_type": "one_way"` | 契約 2 v0.3 新增的必填欄位；這些路線有 `source_trip_id` 而且沒有折返點，依不變條件 5、4 只有這組值合法。斷言沒有改 |
| `tests/test_integration_b1.py` 的 `catalog()`（`test_sb1_ac2_tracks_to_ingest_to_user_pace_table_to_eta`） | 手寫的 R08 路線紀錄加上同樣三個欄位 | 同上。斷言沒有改 |
| `tests/test_contracts.py` 模組說明 | 文字改為 v0.3 | 說明與內容一致；不影響任何斷言 |

沒有刪除、跳過或標記 xfail 任何測試，沒有放寬任何既有斷言（V-2）。

**V-5**：`tests/test_routes_pace_eta.py::test_build_route_conforms_to_the_catalog_contract` **沒有修改**（V-3：`git diff 1fd1de3 6ec1903 -- tests/test_routes_pace_eta.py` 為空），在 `6ec1903` 通過。讓它通過的是產品程式 `src/moto_copilot/routes/catalog.py` 的修改（第 3 節第 11 項、第 5 節），理由是 CL-R1-12：`build_route` 只建立取自行程、單向、沒有折返點的路線，依契約 2 不變條件 4、5 與 AC (3)，對 `R` 加兩位數字的路線只有 `trip`／`null`／`one_way` 合法；這三個值描述它現有的結構，不是預設值。由於 `validate_route_catalog` 對這條路線只接受這一組值，這個原文未改的測試通過即證明三個值正確。

### E-6／V-6 高風險類別

R1-1 標為「不涉及」，CL-R1-12 沒有改變這個標示。`catalog.py` 的修改：三個常數鍵不改變 `build_route` 讀取的資料（它仍只讀呼叫者傳入的幾何）、不決定輸出位置、不產生或輸出任何位置資訊（H-1、H-2）；不碰保留行程、實驗或宣稱（H-3）；`build_route` 不是高風險 record §3.4 判定 1–5 的程式，三個值是對既有結構的描述，不是資料缺漏時的預設值（H-4）。其餘 self-verification：變更只在 `contracts/` 的 schema 與驗證程式、mock fixture 與測試；不讀寫私有資料或憑證、不決定輸出位置（H-1、H-2）；不碰保留行程、實驗或宣稱（H-3）；不是高風險 record §3.4 判定 1–5 列出的任何程式（規則結果、計畫狀態、工具的缺漏處理、路線採用的檢查、快照選取、休息），所以不涉及 H-4。實作中沒有碰到需要 route 的高風險路徑。

### 私有資料與追蹤檔

- 沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有執行 `experiments/` 下任何腳本；沒有讀保留行程。
- `git ls-files | grep -iE '(^data/|\.gpx$|\.fit$|(^|/)\.env)'`：沒有輸出（exit 1）。
- 一次程序偏差見 C-13-3。

## 7. Audit status

Formal：本 Ticket 的 independent audit **required**（Bindings 第 5 節）。**R1 已完成：BLOCKING**（`docs/governance/records/audit/issue-13-c1-r1.md`，受審 subject `6ec1903`，finding R1-F1 Medium／blocking），correction 見第 9 節，待 Orchestrator 派 R2。以下為 R1 前的狀態：R1 尚未派工；派工由 Orchestrator 依 Bindings 第 3.3、3.7 節進行，R1 的 pack 須包含 `decision-20261118-issue13-c131.md`，審查範圍涵蓋 `catalog.py` 的 diff 與 V-1～V-7（該 record 第 5.2 節）。最終 implementation subject 是 `6ec1903`。本 worklog 的自我驗證（含突變檢查）不是 audit。

## 8. Remaining work and concerns

| # | 內容 | 建議的 owner／authority | 狀態 |
| --- | --- | --- | --- |
| **C-13-1** | `src/moto_copilot/routes/catalog.py` 的 `build_route`（v0.2 Spike 的路線目錄產生者）產生的路線紀錄沒有 `route_source`、`snapshot_id`、`trip_type`，不符合契約 2 v0.3，使既有測試 `tests/test_routes_pace_eta.py::test_build_route_conforms_to_the_catalog_contract` 失敗（E-1）。R1-1 的範圍只列 `schemas.py`、`validate.py` 與既有 fixture，排除明列「路線目錄的產生」；`derivation-spec-b1.md` 也寫明 `routes/` 的 Spike 不動。Executor 不自行決定以下任何一種處理：(a) 授權 R1-1 在 `build_route` 的輸出加上 `route_source: "trip"`、`snapshot_id: null`、`trip_type: "one_way"`（它只建立取自行程的單向路線，只有起點與終點檢查點），並以既有測試驗證；(b) 由之後的 `routes`（G-RTE）Spec 處理，在那之前以有理由的方式標示該測試（例如 strict xfail 並引用裁決）；(c) 其他。(b) 會讓 R1-1 結案時 E-1「全數通過」以裁決為依據；(a) 會擴大 R1-1 的範圍到排除項目。**只有這個測試受影響**，其他 874 個測試通過 | Design Authority（boundary determination／scope） | **已裁決並實作。** `decision-20261118-issue13-c131.md` §2.2 **CL-R1-12** 採用 (a)：R1-1 範圍加 (f)，只限 `build_route` 路線紀錄的三個鍵；(b) 與改測試都不採用。`6ec1903` 依 §5.1 實作，V-1～V-7 見第 6 節 |
| C-13-2 | `_TRIP_ID`（`^T\d{3}$`）與 `_DATETIME` 的既有樣式在 Python `re` 下有 D-13-1 所述的同一個寬鬆（`"T001\n"`、非 ASCII 數字會被接受）。不在 R1-1 範圍，沒有修改，沒有測試 | Design Authority（是否另作 clarification 或 tracked item） | **已裁決。** 同 record §3.1 **CL-R1-13**：D-13-1 符合 SPEC-001 §2（ID 是完整字串、ASCII 數字、小寫十六進位）。`trip_id`、`datetime` 的樣式：§3.2 tracked item **TI-C13-2**（owner Design Authority），#13 不修改 |
| C-13-3 | 程序偏差：一次 `Grep` 搜尋的 glob 是 `{src,tests,app,experiments}/**/*.py`，回傳了 `experiments/m1b_spike/run_m1b.py`、`experiments/cr01_checks/routing_c1_curvature.py`、`routing_d3_windows.py` 中含 `build_route`／`validate_dataset` 的幾行原始碼。`experiments/` 不在派工內容列出的可讀路徑內（CL-R1-1 允許閱讀的只有 `routing_client.py`、`routing_c4_snapshots.py`）。這只是追蹤中原始碼的文字比對，沒有讀取 `data/`、沒有執行任何腳本、沒有讀到私有資料；結果只用來確認 `build_route` 的呼叫者，沒有用於實作。之後的搜尋都限於允許的路徑 | Orchestrator（記錄；是否需要其他處理） | Orchestrator 已知悉，要求之後的搜尋只列允許的路徑。DA record §9：不在該次派工的問題內，由 Orchestrator 處理。CL-R1-12 的修正沒有任何搜尋或讀取超出允許路徑 |
| C-13-4 | `DESIGN.md` §5 仍寫「`src/moto_copilot/contracts/` 的驗證程式與契約測試仍然依 v0.2 檢查」，`turnaround` 與不變條件 4、5 仍標「草稿，待 Ticket 實作」；SPEC-001 的樣式以 `\d` 書寫（D-13-1）。Executor 不得修改 `DESIGN.md` 與 `docs/spec/`，沒有修改 | Design Authority／文件的 owner（同步時機） | **已處置。** 同 record §4：併入文字同步清單 **RV-6**（`DESIGN.md` §5、§9.1、§9.3）與 **RV-7**（SPEC-001 §2 註記 CL-R1-13），owner Design Authority，最早在 SPEC-R1 phase acceptance 之後；不阻擋 #13 |
| C-13-5 | `README.md`、`DESIGN.md` §10 的指令沒有改；CLI 的輸出第一行改為 `data contracts v0.3` | 無需處理（記錄） | 記錄 |
| C-13-6 | `experiments/` 中呼叫 `build_route` 的腳本，路線紀錄多出三個鍵後的行為 | 之後執行它們的 work item | **NOT VERIFIED**（DA record §6；本 run 不執行 `experiments/`） |

**剩餘工作**（R1 前的狀態，已由第 9 節取代）：Executor 端沒有。下一步由 Orchestrator 對最終 subject `6ec1903` 派 R1；R1 的 findings 由 Executor 以 targeted correction 處理。TI-C13-2、RV-6、RV-7 是 Design Authority 的 tracked items，不在 #13。

## 9. R1-F1 的 targeted correction（cycle 1）

### 9.1 依據與範圍

- Finding：`docs/governance/records/audit/issue-13-c1-r1.md` **R1-F1**（Medium／blocking，owner Issue #13 Executor）。受審 subject `6ec1903`；派工時 HEAD `e5dfe5e`（R1 record 的 commit）。
- 缺陷：`_route_source_errors` 以 `source not in _REFERENCES_SET` 對任意 JSON 值做 dict membership；`[]`、`{}`、`["trip"]` 不可 hash，拋出 `TypeError`，使 `validate_route_catalog` 與 `validate_dataset` 中止、不回傳 report。修正前以同樣的探測重現（`[]` → `TypeError: unhashable type: 'list'`，`{}` → `'dict'`）。
- 範圍：只修 R1-F1 的 required fix，不夾帶其他變更（治理 §4.4）。

### 9.2 修正（`3c065f8`）

- `src/moto_copilot/contracts/validate.py` `_route_source_errors`：條件改為 `if not isinstance(source, str) or source not in _REFERENCES_SET: return []`，加一行註解引用 R1-F1。不是字串或不是三個合法值之一的 `route_source` 只由 schema 的 enum 回報（`routes[i] schema: route_source: ... is not one of ['trip', 'routing', 'target_gpx']`），來源的交叉檢查（不變條件 5、ID 格式一致性、`RS-`／`SN-` 十六進位）跳過。沒有放寬 enum，沒有吞掉任何例外。合法來源、不變條件 1–5、AC (2)、(3) 的檢查與 CL-R1-12 的三鍵修正都不變。
- `tests/test_contracts.py`：新增 `test_a_route_source_of_another_json_type_is_reported_not_raised`（4 例：`[]`、`{}`、`["trip"]`、`{"trip": "trip"}`），每例先作 JSON round trip，斷言 (i) `validate_route_catalog` 回傳 `routes[0] schema: route_source` 且沒有該路線的交叉檢查訊息；(ii) `validate_dataset` 回傳四份契約的 report，`route_catalog` 含同一 schema 違反，其他三份為空。沒有修改任何既有測試。
- `git diff --stat e5dfe5e 3c065f8`：`validate.py` 3 行（+2／−1）、`tests/test_contracts.py` +15；沒有其他檔案。

### 9.3 同類模式的盤點

R1-F1 要求檢查本 Ticket 新增的其他 helper：

| Helper／檢查（本 Ticket 新增） | 對任意 JSON 值的處理 | 結果 |
| --- | --- | --- |
| `_route_source_errors` 的 `source not in _REFERENCES_SET` | dict membership | **R1-F1，已修** |
| `_REFERENCES_SET[source]`、`_ID_FORMAT[source]` | 只在上面的守衛之後（`source` 已是合法字串） | 安全 |
| `_matches` | 先 `isinstance(value, str)` | 安全 |
| `_source_of_route_id` | 只在 `_matches(ROUTE_ID_PATTERN, rid)` 之後呼叫 | 安全 |
| `checkpoint_id` 前綴（`cid.rpartition`） | 只在 `cid`、`rid` 都通過 `_matches` 之後 | 安全 |
| 不變條件 4 的 `trip_type == "round_trip"`、`kind == "turnaround"` | 相等比較，不需 hash | 安全 |
| 不變條件 2、4 的 `_whole_count` | `isinstance` 判斷 | 安全 |

以合成 fixture 的副本逐一把新增或相關欄位設為 `[]`、`{}`、`["trip"]`（經 JSON round trip）呼叫 `validate_dataset`：修正前只有 `route_source` 屬本 Ticket 的 helper 拋錯；`snapshot_id`、`trip_type`、`source_trip_id`、`n_segments`、`kind`、`after_seg_count` 都正常回傳 report。

**範圍外的既有缺陷（C-13-7，不在本 correction）**：同一探測中，`route_id`（路線、檢查點、衍生路段、ETA 表頭）與 `checkpoint_id` 為 `[]`／`{}` 時也拋 `TypeError`。在 BASE `1fd1de3` 的 `src/` 以 `git archive` 匯出到 scratchpad 後重跑同樣的探測，結果相同，所以它來自 v0.2 既有的主鍵重複檢查（`_duplicates` 的 set）與 `route_ids` 的 set／dict，不是本 Ticket 新增的 helper。依治理 §4.4 與 R1-F1「不要求全面重寫舊 validator」，沒有修改；列為 C-13-7。

### 9.4 驗證（最終 subject `3c065f8`，`git status --short` 為空）

`PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m pytest -q`，exit code **0**：

```text
........................................................................ [  8%]
........................................................................ [ 16%]
........................................................................ [ 24%]
........................................................................ [ 32%]
........................................................................ [ 40%]
........................................................................ [ 49%]
........................................................................ [ 57%]
........................................................................ [ 65%]
........................................................................ [ 73%]
........................................................................ [ 81%]
........................................................................ [ 90%]
........................................................................ [ 98%]
...............                                                          [100%]
879 passed in 28.21s
```

`PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe -m pytest -q -rxX`，exit code **0**：

```text
........................................................................ [  8%]
........................................................................ [ 16%]
........................................................................ [ 24%]
........................................................................ [ 32%]
........................................................................ [ 40%]
........................................................................ [ 49%]
........................................................................ [ 57%]
........................................................................ [ 65%]
........................................................................ [ 73%]
........................................................................ [ 81%]
........................................................................ [ 90%]
........................................................................ [ 98%]
...............                                                          [100%]
879 passed in 27.64s
```

875 → 879：新增的 4 個 R1-F1 案例。摘要只有 `passed`，沒有 xfail／xpass 的列。

`PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`，exit code 0：

```text
data contracts v0.3: tests\fixtures\contract_v02\mock_dataset.json
  derived_segments: OK
  route_catalog: OK
  pace_table: OK
  eta_output: OK
```

- `grep -rnE "xfail|pytest\.mark\.skip" tests/`：0 筆。
- 突變檢查 M10：把守衛換回 `if source not in _REFERENCES_SET:` → 新增的 4 例全部失敗（`4 failed`）；還原後通過。
- `git ls-files | grep -iE '(^data/|\.gpx$|\.fit$|(^|/)\.env)'`：沒有輸出。
- E-3、E-4、E-6 不變：新增案例是 fixture 副本，沒有座標或私有資料；沒有網路；高風險類別仍「不涉及」（修正只讓錯誤型別回報為違反，不涉及 H-1～H-4 的路徑）。
- 沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/`；搜尋只在允許的路徑。

### 9.5 Binding

同一個 agent（`a95eaf00e5bb8b468`，`gov-executor`）以 SendMessage 續派。Executor 自行觀測（`3c065f8` 之後、寫本節之前）：(`claude-opus-5-5`, `high`) 125 則，集合只有一個元素。這是自我觀測，不是派工者的核對。

### 9.6 Concerns 與剩餘工作

| # | 內容 | 建議的 owner／authority | 狀態 |
| --- | --- | --- | --- |
| R1-F1 | 見 9.1–9.4 | Reviewer（R2 核對 closure） | Executor 已修正；closure 由 R2 判定，本 worklog 不宣告已解決 |
| C-13-7 | v0.2 既有的 `route_id`、`checkpoint_id` 主鍵與集合檢查，對不可 hash 的值拋 `TypeError`（BASE `1fd1de3` 已存在）。不在 R1-1 新增的 helper，沒有修改 | Design Authority（是否列為 tracked item 或納入之後的 `contracts` 工作） | open |

**剩餘工作**：Executor 端沒有。下一步由 Orchestrator 對 `3c065f8` 派 R2（治理 §4.4：R1-F1 是否解決、有沒有回歸、修正直接產生或暴露的 blocking defect）。
