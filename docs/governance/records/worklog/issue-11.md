# Worklog — Issue #11（SPEC-B1 B1-4）`pace`：ETA 的停等寬放與安全餘裕

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #11（BATCH-1 B1-4），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **實作與 self-verification 完成，待 R1。** 本 worklog 不宣告 Ticket closure；closure 由 Orchestrator 依 orch-default §7 判定 |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `eb1852d262e6b3434364e3e08b6602aa7d24d733`（`eb1852d`，派工時的 HEAD）；實作 commit **`41c848bc03c963599cf936c2e578e50045e4a68f`**（`41c848b`）。本 worklog 在其後的 record-only commit |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：GitHub Issue #11 的內文與 4 項 AC。派工所附 scratchpad 原文檔 `issue-11-body.md` 實測 SHA-256 `3f4b1caecfcc81bb152ea217ec376857c0e6f6dab9c207148412d96da026f8e4`；另以 `gh issue view 11 --json body,updatedAt,state,title`（唯讀）取得的 body，UTF-8 SHA-256 相同，等於 BD-3；`updatedAt` `2026-11-15T11:11:01Z`，`state` OPEN。沒有修改 Issue。
- **Spec**：SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）：§2 引用段落；§4 CL-B1-1、**CL-B1-5**、CL-B1-7；§5 #11 列（4 項 AC＋另加：呼叫者提供的 `margin_coeff` 與配速表表頭不同時回報錯誤；高風險類別 H-3 判定 3.3 第 4 項、H-4 判定 3.4 第 3 項）；共通證據要求 E-1～E-5。
- **CL-B1-8**：`decision-20261117-issue7-spike-tests.md` §3.2（#11 結案時移除 S-4、S-5、S-6 的 strict xfail 並恢復檢查）。
- **CL-B1-9**：`decision-20261117-issue9-e1-and-trim.md` 第 2 節第 3 項（**#11 的 E-1：`tests/` 沒有 CL-B1-8 的任何標記，pytest 沒有 `xfailed`，即字面的「全數通過」**）。
- **CL-B1-12～14**：`decision-20261118-issue10-pace-contract.md`（#10 的配速表；第 9 節 #11 列「不變」，#11 以 #10 產生的配速表為輸入）。
- **高風險類別**：`decision-20261117-high-risk-categories.md` §3.3 第 4 項、§3.4 第 3 項、§5。
- **規格來源**：`DESIGN.md` §5 契約 4（欄位表、不變條件 1–9）、§6.1（時間的定義、算式、不重複計算的四條規則、用語限制）；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §1.1、§1.2、SB2-T5、T6、T8、T9。
- **Outcome Contract**：OC-1（`docs/governance/records/outcome-contract.md`）。
- 本 work item 執行中契約沒有變更。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-ad6a4bc20b0a498ea.{meta.json,jsonl}`；`meta.json` 的 `agentType` 是 `gov-executor`。
- Executor 自行觀測（實作 commit `41c848b` 之後、本 worklog 寫入前，以第 3.6 節的掃描方式）：agentId `ad6a4bc20b0a498ea`，(`claude-opus-5-5`, `high`) 77 則，集合只有一個元素。**這是自我觀測，不是派工者的核對**；Orchestrator 採用本 return 前須自行核對該 agent 的全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 `gov-executor` definition、Bindings m3、impl-default v2 §3–§5、§9、治理 §3.5、§3.7、§3.8；SPEC-B1、CL-B1-8、CL-B1-9／10、CL-B1-12～14 records；高風險類別 record §3.3、§3.4、§5；Issue #11（核對雜湊）；`DESIGN.md` §5 契約 4 與 §6.1 的相關段落；SPEC-RESOLUTION-001 §1.1、§1.2 與 SB2-T 清單；`pace/table.py`、`contracts/schemas.py`、`contracts/validate.py`、`tests/test_routes_pace_eta.py`、`tests/test_pace_table.py`（helpers）、`tests/conftest.py`、mock fixture 的配速表與 ETA 部分。
2. BASE `eb1852d` 上的 pytest：`426 passed, 3 xfailed`（3 個 XFAIL 是 S-4～S-6，`restored by #11`）。
3. `src/moto_copilot/pace/table.py` 的 `compute_eta`（Issue 的範圍）：
   - 每個路段：`typ_seg_time_s = round(length ÷ speed(c), 3)`（不變）；新增 `stop_allow_s = round(stop_ratio(c) × typ_seg_time_s, 3)`。
   - `RIDE` 是 Σ(`typ_seg_time_s` + `stop_allow_s`)；`eta_typ` = 出發時間 + `RIDE` + `break_time_s`；`eta_safe` = `eta_typ` + `margin_coeff` × `RIDE`。休息不進寬放、不乘餘裕係數。
   - `margin_coeff` 一律取自配速表表頭並寫進 ETA 表頭（CL-B1-5）。`margin_coeff` 參數改為選用（預設 `None`）：呼叫者提供而且與表頭不同時（以 `==` 比對；非數值、NaN、`True` 都算不同）`ValueError`，不採用。
   - 計算前以 `validate_pace_table(pace_header, pace_categories)` 核對契約 3；不符就 `ValueError`，不輸出 ETA。這使缺少或非有限的 `margin_coeff`、`speed_kmh` 有值而 `stop_ratio` 為 `null`、缺少 `stop_ratio`、缺少類別紀錄都成為明確錯誤，不以預設值代替（H-4）。
   - 新增 `_route_segments_of`：路線的路段必須恰好是 `seg_index` 0..n−1（n 為路線的 `n_segments`），每段的類別必須是 C1～C3；否則 `ValueError`（原 Spike 以 `zip` 會默默輸出較短的 ETA）。
   - `status` 為 `unknown` 時每列的 `typ_seg_time_s`、`stop_allow_s`、`eta_typ`、`eta_safe` 都是 `null`，`break_time_s` 照填（不變，加上 `stop_allow_s`）。
   - 模組與函式說明改寫：寫明算式、`margin_coeff` 的來源、不以預設值代替，以及「路線目錄的 `category_scheme` 與配速表是否相同」**不在此檢查**（RI-1～RI-3，CL-B1-5）。
4. `tests/test_routes_pace_eta.py`：移除 S-4、S-5、S-6 的三個 strict xfail 標記，測試內文不改（E-4）。
5. 新增 `tests/test_eta.py`（33 個測試，合成資料）：4 項 AC、另加的驗收條件、H-4 的缺漏路徑，以及以 #10 的 `build_pace_table` 產生的配速表計算 ETA 並通過契約 4（E-2）。
6. Mutation 檢查（self-verification，第 6 節）：8 個有效變異中 7 個被測試抓到，1 個是等價變異。
7. 實作 commit `41c848b`；在乾淨的工作區重跑 E-1（第 6 節）。

## 4. Decisions and assumptions

| ID | 決定 | 依據 |
| --- | --- | --- |
| D-11-1 | `margin_coeff` 參數保留為選用的關鍵字參數，只作核對；比對用嚴格的 `==`（另要求是數值） | CL-B1-5「呼叫者另外提供的值與表頭不同時回報錯誤，不採用」。契約 4 不變條件 9 的驗證程式也用嚴格相等（`validate_eta_output`）；寫入的值一律是表頭的值，所以 ETA 一定滿足不變條件 9。保留參數使既有的呼叫方式（S-4～S-6 的 `eta_for` 傳 `0.2`，等於 fixture 表頭）不必修改 |
| D-11-2 | `compute_eta` 在計算前以 `validate_pace_table`（不帶衍生路段表）核對配速表 | H-4 判定 3.4 第 3 項：缺漏不以預設值代替。契約 3 已規定 `margin_coeff` 必填且有限、`stop_ratio` 與 `speed_kmh` 同時為 `null`、三個類別各一筆。後果：缺少類別紀錄的配速表，原 Spike 會得到 `unknown`，現在是明確錯誤（兩者都 fail closed；契約 3 不符的表不是「某類別沒有配速」）。不帶衍生路段表，因為 ETA 不讀契約 1 |
| D-11-3 | 路線的路段數或 `seg_index` 不符、或類別不是 C1～C3 時報錯 | 契約 4 不變條件 1（每個 `plan_id` 恰有 n 列）；原 Spike 的 `zip` 在路段缺漏時會輸出 `status = ok` 的較短 ETA（fail open）。這是同一函式內的 fail-closed 處理，不改變任何 AC 語義。**Reviewer 可判斷是否屬 Issue 範圍** |
| D-11-4 | `stop_allow_s` 取到小數三位（與 `typ_seg_time_s` 相同），`RIDE` 以兩個輸出欄位的值累加 | AC 1 的關係以輸出欄位表示（`stop_allow_s = stop_ratio × typ_seg_time_s`，容許 1 秒）；以輸出欄位累加使 `eta_typ` 的逐段差在秒的捨入前恰好等於 `typ_seg_time_s + stop_allow_s` + 新排入的休息。捨入誤差 ≤ 0.0005 秒 |
| D-11-5 | 路線目錄與配速表的 `category_scheme` 不同時不檢查、不拒絕 | CL-B1-5：RI-1～RI-3 不在 #11，SPEC-B1 的結案不得宣稱已處理。函式說明寫明此點 |
| D-11-6 | S-4～S-6 的 `__v03_contract` 測試保留為獨立測試，不併回原測試 | CL-B1-8 §3.2 第 3 項（兩種都可以，須寫明）。只刪標記，diff 最小，K-2 可逐字核對 |

沒有需要其他 authority 的假設。

## 5. Artifacts

| 檔案 | 變更 | commit |
| --- | --- | --- |
| `src/moto_copilot/pace/table.py` | `compute_eta` 依 Issue #11 的算式與 CL-B1-5；新增 `_route_segments_of`；模組說明 | `41c848b` |
| `tests/test_eta.py` | 新增（33 個測試） | `41c848b` |
| `tests/test_routes_pace_eta.py` | 刪除 S-4～S-6 的 strict xfail 標記（6 行） | `41c848b` |
| `docs/governance/records/worklog/issue-11.md` | 本 worklog | 其後的 record-only commit |

`git diff --stat eb1852d 41c848b`：3 個檔案，342 行新增、22 行刪除。沒有修改 `contracts/`、`ingest/`、`routes/`、fixture、`conftest.py`、`pyproject.toml`、`DESIGN.md`、任何 Issue 或其他 record。

## 6. Verification

### E-1：在 `41c848b` 執行（主 checkout，`git status --short` 為空）——依 CL-B1-9 第 3 項判定為**滿足**

`git rev-parse HEAD` → `41c848bc03c963599cf936c2e578e50045e4a68f`。

`.venv/Scripts/python.exe -m pytest -q`，exit code 0，完整輸出：

```text
........................................................................ [ 15%]
........................................................................ [ 31%]
........................................................................ [ 46%]
........................................................................ [ 62%]
........................................................................ [ 77%]
........................................................................ [ 93%]
..............................                                           [100%]
462 passed in 1.68s
```

`.venv/Scripts/python.exe -m pytest -q -rxX`，exit code 0，完整輸出（沒有 XFAIL／XPASS 列）：

```text
........................................................................ [ 15%]
........................................................................ [ 31%]
........................................................................ [ 46%]
........................................................................ [ 62%]
........................................................................ [ 77%]
........................................................................ [ 93%]
..............................                                           [100%]
462 passed in 1.60s
```

CL-B1-9 第 3 項的判定：摘要只有 `passed`；沒有 `xfailed`、`xpassed`、`failed`、`error`、`skipped`。`grep -rn "xfail\|skip" tests/` 沒有任何輸出（exit 1）：`tests/` 中沒有 CL-B1-8 或任何其他 xfail／skip 標記。`--runxfail` 不適用（沒有 xfail）。結果陳述：**`462 passed`，沒有 xfail**。相對 BASE 的 `426 passed, 3 xfailed`：+33（`tests/test_eta.py`）+3（S-4～S-6 由 xfail 轉為 passed）。

其他機器檢查（同一 subject）：
- `PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`：四項都是 `OK`，exit 0。
- `git ls-files` 對 `.env`、`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/` 沒有命中。
- 暫存內容對 `sk-ant`、`api_key=` 沒有命中；暫存檔案只有第 5 節的三個。

### E-2：AC 與測試的對應（全部 PASS，於 `41c848b`）

| AC／條件 | 測試 | 結果 |
| --- | --- | --- |
| AC 1：`stop_allow_s = stop_ratio × typ_seg_time_s`；`eta_typ` 的逐段差＝`typ_seg_time_s + stop_allow_s` + 新排入的休息；`eta_safe − eta_typ = margin_coeff × Σ(typ_seg_time_s + stop_allow_s)`（容許 1 秒）（SB2-T5） | `test_eta.py::test_eta_follows_the_formula_worked_out_by_hand`（人工算出的逐列值，含休息不乘餘裕）；`test_eta.py::test_eta_meets_the_stop_allowance_and_margin_invariants[breaks0..3]`（四種休息組合，逐列核對三條關係並通過 `validate_eta_output`）；`test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract`（S-4，與 fixture 的 `stop_allow_s` 與時間逐欄相同）；`test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks`（S-6，契約 4 不變條件 8） | PASS |
| AC 2：加入一筆休息後，`stop_allow_s` 與餘裕的秒數不變，`eta_typ` 與 `eta_safe` 都只多出休息的長度（SB2-T6） | `test_eta.py::test_a_break_shifts_eta_typ_and_eta_safe_by_its_length_only[breaks0..2]`（一筆在加油站、一筆在途經點、兩筆；逐列比較有無休息：`typ_seg_time_s`、`stop_allow_s`、`eta_safe − eta_typ` 相同，`eta_typ` 與 `eta_safe` 各多出該列的 `break_time_s`，休息之前的列不變） | PASS |
| AC 3：ETA 狀態是 `unknown` 時，`stop_allow_s`、`eta_typ`、`eta_safe` 都是 null（SB2-T8） | `test_eta.py::test_unknown_eta_has_no_stop_allowance_and_no_time[breaks0..1]`（有無休息；`break_time_s` 照填；通過契約 4）；`test_eta.py::test_only_the_route_categories_decide_unknown`；`test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace`；`test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract`（S-5，契約 4 不變條件 6） | PASS |
| AC 4：ETA 表頭的 `margin_coeff` 等於所用配速表表頭的值（SB2-T9 的 ETA 部分） | `test_eta.py::test_eta_header_margin_coeff_is_the_pace_tables[pace0..2]`（`loo_rule` 0.15、`default` 0.20、含 `unknown` 的路線；不傳與傳相同值結果一樣）；`test_eta.py::test_eta_from_a_pace_table_built_from_derived_segments`（以 #10 的 `build_pace_table` 自 9 趟合成行程建表，`margin_basis = loo_rule`，ETA 表頭等於該表頭，通過契約 4）；S-4（表頭等於 fixture） | PASS |
| 另加：呼叫者提供的 `margin_coeff` 與配速表表頭不同時回報錯誤（SPEC-B1 §5 #11 列） | `test_eta.py::test_a_caller_margin_coeff_that_differs_from_the_pace_table_is_an_error[0.2, 0.1, 0.15000001, "0.15", nan, True]`；`test_eta.py::test_the_caller_cannot_bring_back_a_default_margin` | PASS |
| CL-B1-5：`stop_ratio` 取自同一份配速表 | AC 1 的各測試（寬放依該表的 `stop_ratio`）；`test_eta_from_a_pace_table_built_from_derived_segments`（以該表的 `stop_ratio` 核對，含 `stop_ratio = 0` 的類別） | PASS |
| H-4：缺漏與不合法的輸入是明確錯誤 | `test_eta.py::test_a_pace_table_that_breaks_contract_3_is_an_error[...]`（缺 `margin_coeff`、`null`、NaN；有配速而 `stop_ratio` 為 `null`；缺 `stop_ratio`；負值；無限大；缺類別紀錄）；`test_eta.py::test_route_segments_that_do_not_match_the_route_are_an_error`（缺一段、重複一段、類別不合法）；`test_eta.py::test_departure_time_must_be_timezone_aware`；`test_routes_pace_eta.py::test_eta_needs_an_aware_departure_time` | PASS |
| 合成輸入本身符合契約 2、3 | `test_eta.py::test_synthetic_inputs_conform_to_contracts_2_and_3` | PASS |

**Mutation 檢查**（self-verification，不是 audit）：腳本 `C:/Users/yotsu/AppData/Local/Temp/claude/4fa6cbf1f948238d/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/scratchpad/mutate11.py` 逐一修改 `table.py`、跑全部 `tests/`、在 `finally` 還原（之後 `git diff --stat` 確認只剩本次實作的變更）。在實作 commit 之前的工作區執行：

| 變異 | 結果 |
| --- | --- |
| M1 寬放恆為 0 | 9 failed |
| M2 餘裕也乘休息 | 10 failed |
| M3 餘裕不含寬放 | 8 failed |
| M4 表頭寫入呼叫者的值 | 0 failed——**等價變異**：核對通過時呼叫者的值必等於表頭；M5 拿掉核對時被抓到 |
| M5 拿掉呼叫者 `margin_coeff` 的核對 | 7 failed |
| M6 拿掉配速表的契約 3 核對 | 8 failed |
| M6b 缺 `margin_coeff` 時預設 0.2（核對仍在） | 0 failed——被契約 3 核對遮住（核對在前、先報錯），不是缺口；M6 證明核對本身有測試守著 |
| M7 `unknown` 時寬放填 0 | 4 failed |
| M8 拿掉路段的核對（回到 `zip`） | 1 failed |

### E-3：測試資料

全部是合成的：`tests/test_eta.py` 的配速表、路線目錄與檢查點是手寫的整數或簡單小數（長度 1000–6000 m、速度 30／45／60 km/h、停等比例 0.05／0.10／0.20、餘裕係數 0.15／0.20）；路段終點座標是 (0.0, 0.01×i) 的佔位值，不是地點；行程代號 `T101`–`T109`、`T900` 是虛構的；`trips_three_categories`（`tests/test_pace_table.py`，#10 已有）產生的衍生列是虛構的整數。其餘輸入是既有的 mock fixture。diff 中沒有真實座標、軌跡、騎乘時間或行程清單。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下任何腳本，沒有讀保留行程。

### E-4：修改的既有測試（依 CL-B1-8 §3.2）

| 測試 | 修改 | 恢復方式 |
| --- | --- | --- |
| S-4 `tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract` | 刪除 `@pytest.mark.xfail(strict=True, reason="... restored by #11; ...")`（2 行），內文不改 | 不帶標記通過（CL-B1-8 §3.2 第 1 項）；保留為獨立測試（第 3 項，D-11-6） |
| S-5 `tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract` | 同上 | 同上 |
| S-6 `tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks` | 同上 | 不帶標記通過；它原本就沒有拆分 |

`git diff eb1852d 41c848b -- tests/test_routes_pace_eta.py` 只有這 6 行刪除。其他既有測試沒有修改：`eta_for` 與 `test_eta_needs_an_aware_departure_time` 仍傳 `margin_coeff=0.2`（等於 fixture 表頭，D-11-1），不需要改。沒有因契約改版而改寫的斷言。

### E-5：高風險類別的 self-verification（`decision-20261117-high-risk-categories.md` 第 5 節）

- **H-3（判定 3.3 第 4 項：`ETA_safe`／保守估計與百分位數）**：新增與修改的程式說明、錯誤訊息與測試文字以 `grep -i "p90\|percentile\|quantile\|百分位\|分位\|警特報"` 核對：`tests/test_eta.py` 沒有命中；`git diff -U0` 的新增行沒有命中（唯一的命中是 diff hunk 標頭帶出的 #10 既有文字「it is not a P90」，本次沒有修改）。新增說明的寫法是「a conservative estimate with a safety margin; it carries no coverage guarantee」。本 worklog 的 E-1 結果照實寫出 `462 passed`，沒有把任何檢查稱為 E1 Lite 或 E2 的結果；真實行程上的行為未執行（見下）。`compute_eta` 不開啟任何檔案，與保留行程的隔離無關。
- **H-4（判定 3.4 第 3 項：配速與 ETA 的缺漏處理）**：缺漏、不合法或超出範圍的每條路徑都有測試，結果是 `unknown` 或明確錯誤，而不是 `ok` 或預設值——類別沒有配速 → `unknown` 且所有時間與寬放為 `null`（AC 3 的測試）；缺 `margin_coeff`／非有限／`null` → 錯誤，不用 0.20；有配速而缺 `stop_ratio` → 錯誤，不用 0；呼叫者的 `margin_coeff` 不同 → 錯誤；路段缺漏或重複 → 錯誤，不輸出較短的 ETA；出發時間沒有時區 → 錯誤。Mutation M5–M8 證明這些守門各有測試。
- **H-1、H-2**：不涉及（沒有憑證、付費呼叫、GPX 或位置資料；E-3）。

### 未執行的檢查

- 以真實行程建立的配速表計算 ETA：**NOT RUN／NOT VERIFIED**（RB-7；required authority = acceptor）。
- 路線目錄與配速表 `category_scheme` 不同時的處理：不在 #11（RI-1～RI-3，CL-B1-5），沒有檢查，不得記為已涵蓋。
- SB1-AC2 的跨 Ticket 整合（`ingest` → 配速表 → ETA）：屬 SPEC-B1 的 Spec Integration Audit，不在本 Ticket；`test_eta_from_a_pace_table_built_from_derived_segments` 只涵蓋「配速表 → ETA」一段，不是 SB1-AC2。

## 7. Audit status

Formal：本 Ticket 的 independent audit（R1）**required**（治理 §4.1；Bindings 第 5 節），尚未派工；由 Orchestrator 依 Bindings 第 3.3、3.7 節派工。高風險類別 H-3、H-4（SPEC-B1 §5 #11 列）的最低核對範圍見高風險類別 record §5。本 worklog 的 self-verification（含 mutation 檢查）不是 audit。

## 8. Remaining work 與 concerns

| ID | 內容 | 性質 | Authority／owner |
| --- | --- | --- | --- |
| C-11-1 | D-11-2、D-11-3 讓 `compute_eta` 對契約 3 不符的配速表與不一致的路線路段報錯（原 Spike 前者可能給 `unknown`、後者給較短的 ETA）。兩者都是 fail closed，不改變 AC；是否屬 Issue 範圍由 R1 判斷 | 資訊（不阻擋） | R1 reviewer；有爭議時 Design Authority |
| C-11-2 | 路線目錄的 `category_scheme` 與配速表不同時 `compute_eta` 照常計算（RI-1～RI-3 不在 #11）。`routes` 的 Spike 目錄是 `curv-spike0-…`，#10 的配速表是 `curv-tercile-…`；兩者接起來的 ETA 在 RI-1～RI-3 處理前沒有意義 | 已知範圍外，tracked | 之後的 `routes` Spec（Design Authority） |
| C-11-3 | mock fixture 的 `P-MOCK-2` `unknown_reason` 是中文句子，`compute_eta` 寫英文的 `no pace for category C3`；S-5 不比對該欄，契約只要求非空字串。既有差異，未修改 | 資訊 | 無 |
| C-11-4 | `DESIGN.md` 的實作狀態陳述（契約 4 的 `stop_allow_s`「尚未實作」等）在本 Ticket 之後過時 | 範圍外 | AB-12 的文件工作（`derivation-spec-b1.md` §8） |
| — | 真實行程上的行為 NOT VERIFIED | 範圍外 | acceptor（RB-7） |

剩餘工作：R1（Orchestrator 派工）；之後依 audit 結果做 targeted correction（若有）。沒有阻擋本 Ticket 的事項。
