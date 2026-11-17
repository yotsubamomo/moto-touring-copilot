# Worklog — Issue #10（SPEC-B1 B1-3）`pace`：配速表的停等比例、分級門檻、餘裕係數與版本

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #10（BATCH-1 B1-3），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **實作與 self-verification 完成（第 9 節，`e0f6c78`），待 R1。** 第一次 return 時因 C-10-1 BLOCKED（第 1–8 節，保留原文作為歷程）；Design Authority 以 `decision-20261118-issue10-pace-contract.md`（CL-B1-12～14）裁決後完成 rework，S-3 已恢復，#10 的 E-1 依 CL-B1-9 第 3 項滿足（第 9.3 節）。本 worklog 不宣告 closure。 |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `20939aa`（派工時的 HEAD）；實作 commit **`be0074d51805b2f912c3d35350f3c9d52f76e8c8`**（`be0074d`）；rework commit **`e0f6c7833620acb959a3e6bff8278b0506997eeb`**（`e0f6c78`，父 commit 是 DA record 的 `e0626a3`）。**受審的程式與測試 subject 是 `e0f6c78`**；本 worklog 的更新在其後的 record-only commit |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：GitHub Issue #10 的內文與 8 項 AC。Orchestrator 提供的 scratchpad 原文檔 SHA-256 `880ef1341e090b86e826cd2a14812ab4a05b634b73385c3ccebea80e43245e65`；另以 `gh issue view 10 --json body`（唯讀）取得的 body，UTF-8 SHA-256 相同，與 BD-3 相同；`updatedAt` `2026-11-15T11:10:59Z`，`state` OPEN。沒有修改 Issue。
- **Spec**：SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）：§2 引用段落；§4 CL-B1-1、**CL-B1-4**（第 1–10 項）、CL-B1-7；§5 #10 列（8 項 AC＋另加 3 項：`category_scheme` 格式、7 折／8 折、沒有可計時路段時不建立不寫檔；高風險類別 H-2、H-3、H-4）；E-1～E-5。
- **CL-B1-8**：`decision-20261117-issue7-spike-tests.md` §3.2（#10 結案時移除 S-3 的 strict xfail 並恢復檢查）。
- **CL-B1-9**：`decision-20261117-issue9-e1-and-trim.md` 第 3 項（#10 的 E-1 只允許 S-4～S-6 的 xfail，`--runxfail` 範圍加上 #10 新增或修改的測試檔）。
- **高風險類別**：`decision-20261117-high-risk-categories.md` §3.2 第 1 項、§3.3 第 1 項、§3.4 第 3 項、§5。
- **規格來源**：`DESIGN.md` §5 契約 3（欄位與不變條件 1–7）、§6.1（配速表、餘裕係數的規則與留一趟程序、分級門檻、版本）；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §1.4、SB2-T4、T7、T9、T10、T13。
- **參考實作（只閱讀，未執行）**：`experiments/cr01_checks/data_common.py` 的 `tercile_thresholds`；`experiments/cr01_checks/data_sb2_stop_allowance.py` 的 `fit`、`predict`、`margin`；`src/moto_copilot/ingest/segments.py` 的 `_category`。
- 本 work item 執行中契約沒有變更。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-a54ac9cf0e452782b.{meta.json,jsonl}`，`meta.json` 的 `agentType` 是 `gov-executor`。
- Executor 自行觀測（實作 commit 之後、worklog 寫入前，以第 3.6 節的掃描方式）：agentId `a54ac9cf0e452782b`，(`claude-opus-5-5`, `high`) 80 則，集合只有一個元素。**這是自我觀測，不是派工者的核對**；Orchestrator 採用本 return 前須自行核對該 agent 的全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 `gov-executor` definition、Bindings m3、impl-default v2 §3–§5、§9、治理 §3.5、§3.7、§3.8、SPEC-B1、CL-B1-8、CL-B1-9／10 record、高風險類別 record §3.2–§3.4 與 §5、Issue #10（核對雜湊）、`DESIGN.md` §5 契約 3 與 §6.1、SPEC-RESOLUTION-001 §1.4 與 SB2-T 清單、現有 `pace/table.py`、`contracts/schemas.py`、`contracts/validate.py`、`tests/test_routes_pace_eta.py`、`tests/conftest.py`、mock fixture；唯讀閱讀兩個參考實作的上列函式（未執行）。
2. `src/moto_copilot/pace/table.py`（Issue 的範圍）：
   - `timed_rows`：CL-B1-4 第 1 項的可計時路段；使用到的欄位不是有限的非負數時報錯（不補值）。
   - `tercile_thresholds`、`classify`、`category_scheme`：第 2–4 項。門檻 `round(v[n//3]/5)*5`、`round(v[2n//3]/5)*5`（Python `round`）；分類邊界與 `ingest` 的 `_category` 相同；`curv-tercile-<c1>-<c2>`（整數）。沒有可計時路段時報錯。
   - `_category_pace`：每個類別的 `speed_kmh`（不加權中位數，沿用到小數兩位）、`stop_ratio`（Σ`short_stop_time_s` ÷ Σ`moving_time_s`，不捨入）、`n_segments`；路段數少於 `min_segments` 時兩者都是 `null`（第 5 項）。
   - `loo_folds`：第 6 項的留一趟。每一折以其餘行程重算門檻與配速；被拿掉的那一趟沒有可計時路段、或它的任何類別在該折沒有配速時，這一折不計入；計入的折回傳 `r = 實際 ÷ 預測 − 1`。
   - `margin_from_residuals`：第 7 項。計入少於 8 折 → (0.20, `default`)；否則第三大的 `r₃`，`round(max(0.05, ceil(max(r₃,0)/0.05 − 1e-9) × 0.05), 2)`，`loo_rule`（與參考實作的 `margin` 相同的浮點處理）。
   - `build_pace_table`：在計算前先拒絕（第 10 項：`trip_ids` 中有不是 `pace`、不在表中、角色不一致或重複的行程）；不使用衍生路段表的 `seg_category` 與 `category_scheme`（第 3 項）；表頭新增 `margin_coeff`、`margin_basis`，類別紀錄新增 `stop_ratio`；`built_at` 必須帶時區。
   - `create_pace_table`：第 8 項。寫到呼叫者提供且已存在的目錄（沒有預設位置）；檔名 `<pace_version>.json`；自動編號＝該開頭現有最大編號＋1、至少兩位；`research-` 可由呼叫者指定編號；同一版本（含同編號的不同位數寫法）已存在時 `FileExistsError`；以 `open(..., "x")` 寫入，不覆寫、不修改、不刪除既有檔案；寫入前以 `validate_pace_table` 核對契約 3，不符就不寫。
   - `latest_user_pace_table`：第 9 項。`built_at` 最晚的 `user-` 版本，相同時取編號較大者；沒有 `user-` 版本時回傳 `None`（回到凍結清單的 `research-` 版本不在 #10）。檔內 `pace_version` 與檔名不符、或 `built_at` 沒有時區時報錯。
   - `load_pace_table`：讀回 `(header, categories)`。
   - `compare_methods`、`compute_eta`：行為不變（`compare_methods` 改用同一個拒絕函式，只對不合法的輸入更嚴格；`compute_eta` 屬 #11）。
3. `src/moto_copilot/pace/__init__.py`：匯出新函式。
4. `tests/test_pace_table.py`（新增，55 個測試，全部合成資料）：AC 與另加驗收條件的對應見第 6 節 E-2。
5. `tests/test_routes_pace_eta.py`：因契約改版修改兩個既有測試（第 6 節 E-4）。S-3 的 xfail 測試**沒有修改**（第 8 節 C-10-1）。
6. 依 SA-1 在 topic branch 作本機 commit `be0074d`；commit 前確認暫存的只有上列 4 個檔案，不含 `.env`、GPX、FIT 或 `data/`。沒有 push、沒有開 PR。

## 4. Decisions and assumptions

| # | 決定 | 依據 |
| --- | --- | --- |
| D-10-1 | 分成純計算的 `build_pace_table`（不寫檔）與寫檔的 `create_pace_table`。`build_pace_table` 不檢查 `pace_version` 的樣式；只有 `create_pace_table` 產生版本字串，並在寫檔前以契約 3 驗證 | 既有測試以 `"p"` 呼叫 `build_pace_table`（CL-B1-8 §3.1 第 5 項：這些字面值不改）；版本的產生與不覆寫都集中在寫檔路徑 |
| D-10-2 | 留一趟每一折的預測使用與配速表相同的程序得到的配速（`speed_kmh` 到小數兩位），參考實作的 `fit` 用未捨入的速度 | CL-B1-4 第 6 項「以同一個 `min_segments` 建立該折的配速」；DESIGN §6.1 比較的是「預測的 RIDE」，而 ETA 用的是配速表的 `speed_kmh`。差異是相對 0.01 km/h 量級，只在 `r₃` 恰好距 0.05 的倍數極近時才可能改變結果。**非顯然的選擇，列為 C-10-2 請 DA 確認** |
| D-10-3 | `user-` 版本不接受呼叫者指定的編號（`ValueError`）；`research-` 的編號必須是非負整數。同一個開頭的同一個數值以任何位數寫法存在，都視為該版本已存在 | CL-B1-4 第 8 項只允許 `research-` 指定編號；`user-` 依建立順序遞增。以數值判定已存在是 fail closed。列為 C-10-3 |
| D-10-4 | `latest_user_pace_table` 沒有 `user-` 版本時回傳 `None`，不自行讀任何 `research-` 版本 | CL-B1-4 第 9 項：`research-` 的退回屬凍結清單，不在 #10。`None` 不是預設值，呼叫者必須另行處理 |
| D-10-5 | `trip_ids` 中同一行程重複、或某行程在衍生路段表中有一個以上的 `trip_role`，也在計算前拒絕 | 第 10 項的「無法確認角色」；契約 3 表頭 `trip_ids` 為 `uniqueItems` |
| D-10-6 | `build_pace_table` 不再要求衍生路段表只有一個 `category_scheme`；仍要求只有一個 `ingest_version` | CL-B1-4 第 3 項：`pace` 不依賴 `seg_category` 與 `category_scheme`；`ingest_version` 寫入表頭 |
| D-10-7 | `stop_ratio` 不捨入 | DESIGN 契約 3 與 AC 1 的定義是「等於」Σ÷Σ；契約 4 不變條件 8 由 ETA 以同一個值計算 |
| D-10-8 | 可計時路段中 `moving_time_s` 等於 0 的列不計入（CL-B1-4 第 1 項「大於 0」）；非有限值則報錯 | 第 1 項的字面定義；H-4：不以預設值掩蓋缺漏 |

## 5. Artifacts

| 檔案 | 變更 | 版本 |
| --- | --- | --- |
| `src/moto_copilot/pace/table.py` | 修改（第 3 節第 2 項） | `be0074d` |
| `src/moto_copilot/pace/__init__.py` | 修改（匯出） | `be0074d` |
| `tests/test_pace_table.py` | 新增 | `be0074d` |
| `tests/test_routes_pace_eta.py` | 修改兩個既有測試（E-4） | `be0074d` |
| `docs/governance/records/worklog/issue-10.md` | 本檔 | record-only commit |

沒有修改 `contracts/`、`ingest/`、`routes/`、fixture、`conftest.py`、`pyproject.toml`；`git diff --stat 20939aa be0074d` 只有上表前 4 個檔案。

## 6. Verification

### E-1：在 `be0074d` 執行（主 checkout，`git status` 乾淨）——**依 CL-B1-9 第 3 項判定為不滿足**

**(i) `.venv/Scripts/python.exe -m pytest -q`**

```text
........................................................................ [ 18%]
........................................................................ [ 37%]
........................................................................ [ 56%]
........................................................................ [ 75%]
........................................................................ [ 94%]
.........x....x.xx.                                                      [100%]
375 passed, 4 xfailed in 1.59s
exit=0
```

**(iii) `.venv/Scripts/python.exe -m pytest -q -rxX`**

```text
........................................................................ [ 18%]
........................................................................ [ 37%]
........................................................................ [ 56%]
........................................................................ [ 75%]
........................................................................ [ 94%]
.........x....x.xx.                                                      [100%]
=========================== short test summary info ===========================
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
375 passed, 4 xfailed in 1.52s
exit=0
```

**(iv) `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py tests/test_pace_table.py`**（`--collect-only`：181 個測試）

```text
........................................................................ [ 39%]
............................................F....F.FF................... [ 79%]
.....................................                                    [100%]
================================== FAILURES ===================================
___________ test_pace_table_matches_the_mock_fixture__v03_contract ____________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '<mock 名稱，主控台編碼亂碼>', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; "
                                           "build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet")
    def test_pace_table_matches_the_mock_fixture__v03_contract(data):
        header, categories = build_pace_table(data["derived_segments"], ["T001", "T002"], pace_version="user-01",
                                              min_segments=2, built_at=NOW)
>       assert validate_pace_table(header, categories, data["derived_segments"]) == []
E       AssertionError: assert ['pace_catego...invariant 3)'] == []
E         
E         Left contains 2 more items, first extra item: 'pace_categories: C1 n_segments is 1, but 2 rows are eligible (invariant 3)'
E         Use -v to get more diff

tests\test_routes_pace_eta.py:125: AssertionError
_____________ test_eta_reproduces_the_mock_fixture__v03_contract ______________

data = {...同上...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_reproduces_the_mock_fixture__v03_contract(data):
        header, rows = eta_for(data, "R01", "P-MOCK-1", [{"after_checkpoint_id": "R01-CP03", "duration_s": 600.0}])
>       assert rows == [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-1"]
E       AssertionError: assert [{'plan_id': ...: 600.0, ...}] == [{'plan_id': ...s': 0.0, ...}]
E         
E         At index 0 diff: {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'} != {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'stop_allow_s': 0.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'}
E         Use -v to get more diff

tests\test_routes_pace_eta.py:169: AssertionError
________ test_eta_is_unknown_when_a_category_has_no_pace__v03_contract ________

data = {...同上...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_is_unknown_when_a_category_has_no_pace__v03_contract(data):
        header, rows = eta_for(data, "R02", "P-MOCK-2", [])
        data["eta_headers"], data["eta_segments"] = [header], rows
>       assert validate_eta_output([header], rows, data["routes"], data["route_segments"], data["checkpoints"],
                                   data["pace_header"], data["pace_categories"]) == []
E       assert ['eta_segment...red property'] == []
E         
E         Left contains 2 more items, first extra item: "eta_segments[0] schema: (record): 'stop_allow_s' is a required property"
E         Use -v to get more diff

tests\test_routes_pace_eta.py:184: AssertionError
_________ test_eta_output_passes_the_contract_with_and_without_breaks _________

data = {...同上...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_output_passes_the_contract_with_and_without_breaks(data):
        for plan_id, breaks in (("P-A", []), ("P-B", [{"after_checkpoint_id": "R01-CP04", "duration_s": 900.0}])):
            header, rows = eta_for(data, "R01", plan_id, breaks)
>           assert validate_eta_output([header], rows, data["routes"], data["route_segments"], data["checkpoints"],
                                       data["pace_header"], data["pace_categories"]) == []
E           assert ['eta_segment...status is ok'] == []
E             
E             Left contains 5 more items, first extra item: "eta_segments[0] schema: (record): 'stop_allow_s' is a required property"
E             Use -v to get more diff

tests\test_routes_pace_eta.py:193: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
4 failed, 177 passed in 1.39s
exit=1
```

輸出逐字轉錄，只有兩處改寫：mock fixture 中一個中文路線名稱在主控台輸出為亂碼，以「`<mock 名稱，主控台編碼亂碼>`」表示；後三個 `data = {...}` 行與第一個相同，以「`{...同上...}`」縮寫。原始輸出在 Executor 的 scratchpad（`s10/e1-*.txt`），不是受版控的 evidence。

S-3 的兩個違反（另以同一個 `build_pace_table` 與 `validate_pace_table` 直接呼叫取得完整清單）：

```text
['pace_categories: C1 n_segments is 1, but 2 rows are eligible (invariant 3)', 'pace_categories: C3 n_segments is 2, but 1 rows are eligible (invariant 3)']
```

同一份輸出不帶衍生路段表（`validate_pace_table(header, categories)`）時是 `[]`：v0.3 的 `stop_ratio`、`margin_coeff`、`margin_basis` 與 `pace_version` 的樣式都已符合。

**依 CL-B1-9 第 3 項（以第 2 項代入）逐條判定：**

| 條件 | 結果 |
| --- | --- |
| i. exit code 0 | 成立 |
| ii. 摘要只有 `passed`、`xfailed` | 成立（`375 passed, 4 xfailed`） |
| iii. 每個 xfail 都是 `restored by #11`（S-4～S-6）、數目不超過 3、沒有 `restored by #9` 或 `#10` 的標記 | **不成立**：`restored by #10` 的 S-3 標記仍在（`tests/test_routes_pace_eta.py` 第 120 行），xfail 是 4 個 |
| iv. `--runxfail` 失敗的恰好是那些 xfail，訊息只涉及 v0.3 項目 | S-4～S-6：成立（只涉及 `stop_allow_s`）。**S-3：不成立**——失敗原因已不是 v0.3 產生者缺口，而是契約 3 不變條件 3 的計數（第 8 節 C-10-1）；它的 `reason` 文字「does not write stop_ratio, margin_coeff or margin_basis yet」已不正確 |
| v. S-4～S-6 的測試與標記在 #10 沒有修改 | 成立（`git diff 20939aa be0074d -- tests/test_routes_pace_eta.py` 只改 `test_pace_table_matches_the_mock_fixture` 與 `test_suspect_and_invalid_rows_do_not_change_the_pace`） |

**結果陳述**：`375 passed, 4 xfailed`。其中 4 個 xfail 不是通過；S-3 的 xfail 已經遮住一個非缺口的失敗。**#10 的 E-1 不滿足**，這是 C-10-1 的直接結果。

標記核對（CL-B1-8 §3.4 K-1 的 grep，`grep -rn "xfail\|skip" tests/`）：只有 `tests/test_routes_pace_eta.py` 第 120（`restored by #10`）、165、179、188 行（`restored by #11`）；沒有 `skip`；`test_pace_table.py` 與 `test_contracts.py` 沒有標記。

### E-2：AC 與測試的對應（全部 PASS，於 `be0074d`；58 個測試 `-rA` 全部 PASSED）

| AC／條件 | 測試（`tests/test_pace_table.py`，另註明者除外） | 結果 |
| --- | --- | --- |
| AC 1 `stop_ratio`＝可計時路段 Σ 短停留 ÷ Σ 移動；`speed_kmh` 為 null 時為 null | `test_stop_ratio_is_short_stops_over_moving_time_of_the_timed_segments`（長停留、suspect、invalid 不進加總）；`test_stop_ratio_is_null_when_speed_is_null_and_zero_when_there_are_no_short_stops` | PASS |
| AC 2 以保留行程的代號建立會被拒絕 | `test_a_trip_that_is_not_a_confirmed_pace_trip_is_refused[trip_ids0..2]`（保留行程、只有保留行程、不在表中的代號；`build_pace_table`、`loo_folds`、`create_pace_table` 都拒絕且目錄沒有檔案）；`test_a_trip_with_mixed_roles_or_listed_twice_is_refused`；`test_the_refusal_comes_before_any_computation`；`test_routes_pace_eta.py::test_holdout_trip_is_refused` | PASS |
| AC 3 固定的曲率清單得到固定的門檻 | `test_a_fixed_curvature_list_gives_fixed_thresholds`（含 Python `round` 的 .5 情形與 n = 1、2） | PASS |
| AC 4 餘裕係數的規則：固定殘差清單→固定值；每一折重算門檻；算不出配速的折不計入；少於 8 折是 0.20／`default` | `test_margin_rule_on_a_fixed_residual_list`；`test_margin_rule_rounding_and_floor[7 組]`；`test_margin_rule_rejects_a_non_finite_residual`；`test_each_fold_recomputes_the_thresholds_and_a_fold_without_pace_is_not_counted`（每折門檻＝其餘行程的三分位，與全體門檻 (70, 130) 不同；用全體門檻則沒有任何一折計入）；`test_a_left_out_trip_without_timed_segments_is_not_counted`；`test_header_margin_is_the_default_with_7_counted_folds`；`test_the_default_depends_on_counted_folds_not_on_trips` | PASS |
| AC 5 表頭的 `margin_coeff` 等於同一批行程依規則算出的值 | `test_header_margin_equals_the_rule_on_the_same_trips_with_8_counted_folds`（每折的 r 等於依 DESIGN §6.1 手算的值；第三大 r＝13/120，係數 0.15，`loo_rule`） | PASS |
| AC 6 每次建立都是新版本與新檔案；既有 `research-`、`user-` 檔案不變；編號各自遞增 | `test_each_build_is_a_new_version_and_file_numbered_per_prefix`（逐位元比對既有檔案）；`test_numbering_continues_after_the_largest_existing_number` | PASS |
| AC 7 建立已存在的 `research-` 版本時報錯，不覆寫 | `test_an_existing_research_version_is_an_error_and_is_not_overwritten`（含同編號三位數寫法） | PASS |
| AC 8 有多個 `user-` 版本時選 `built_at` 最晚者 | `test_the_latest_user_version_by_built_at_is_chosen`（最晚者不是編號最大者；相同時取編號較大者；`research-` 不被選；沒有 `user-` 時 `None`）；`test_a_user_file_with_a_wrong_version_or_time_is_an_error` | PASS |
| 另加 1：`category_scheme` 符合 CL-B1-4 第 4 項 | `test_category_scheme_has_the_fixed_format`；`test_stop_ratio_is_short_stops_over_moving_time_of_the_timed_segments`（`curv-tercile-20-300`） | PASS |
| 另加 2：固定殘差清單計入 7 折與 8 折時分別得到 0.20／`default` 與依第 7 項算出的值 | `test_margin_rule_on_a_fixed_residual_list`（同一清單的前 7 個與全部 8 個）；以建表驗證：`test_header_margin_is_the_default_with_7_counted_folds` 與 `..._with_8_counted_folds` | PASS |
| 另加 3：沒有可計時路段時不建立、不寫檔 | `test_no_timed_segment_means_no_thresholds_and_no_table` | PASS |
| CL-B1-4 第 1 項 | `test_timed_rows_follow_cl_b1_4_item_1`；`test_only_the_rows_of_the_listed_trips_are_used` | PASS |
| CL-B1-4 第 3 項（分類邊界與 `ingest` 相同；不用衍生表的類別） | `test_classification_uses_the_same_boundary_as_ingest[8 組]`；`test_the_derived_seg_category_and_category_scheme_are_not_used` | PASS |
| CL-B1-4 第 8 項（目錄由呼叫者提供；`user-` 不可指定編號） | `test_the_directory_must_be_given_and_exist`；`test_a_user_version_cannot_be_given_a_number` | PASS |
| 失敗路徑（H-4） | `test_a_timed_row_with_a_bad_number_is_an_error_not_a_value[6 組]`；`test_min_segments_must_be_a_positive_integer[5 組]`；`test_built_at_must_be_timezone_aware_and_one_ingest_version` | PASS |
| 寫出的檔案符合契約 3 | `test_each_build_is_a_new_version_and_file_numbered_per_prefix`（`validate_pace_table(header, categories, rows) == []`，讀回內容相同）；`test_header_margin_equals_the_rule_on_the_same_trips_with_8_counted_folds` | PASS |
| 合成資料本身符合契約 1 | `test_synthetic_rows_conform_to_contract_1` | PASS |
| SB2-T13 的 `pace` 部分（不覆寫） | 同 AC 7 | PASS |

注意：上表兩個以 `validate_pace_table(..., rows)` 核對的測試，合成資料的衍生 `seg_category`（`ingest` 預設門檻 80／250）與重算後的分類剛好相同，所以不變條件 3 的計數一致。這不是對 C-10-1 的處理，也不代表一般情形會通過。

**突變檢查（self-verification，不是 audit）**：在 `be0074d` 上逐一做下列修改、執行 `tests/test_pace_table.py tests/test_routes_pace_eta.py`、再以 `git checkout` 還原（最後 `git status` 乾淨）。每一個都被測試抓到：

| 突變 | 結果 |
| --- | --- |
| M1 每一折改用全體行程的門檻 | 1 failed |
| M2 `stop_ratio` 改用 `stopped_time_s`（含長停留） | 1 failed |
| M3 餘裕係數改取第二大的 r | 9 failed |
| M4 寫檔改為覆寫（`"w"`，並略過已存在的檢查） | 1 failed |
| M5 拿掉角色的拒絕 | 6 failed |

### E-3：測試資料

- `tests/test_pace_table.py`：全部是手寫的整數值（長度 1000 m 等、移動 60 秒等、曲率 10／100／300 等），沒有座標、軌跡、逐點時間或行程清單；代號 `T101`～`T999` 是編造的。`built_at` 是固定的常數。檔案只寫到 pytest 的 `tmp_path`。
- `tests/test_routes_pace_eta.py`：沿用既有的 mock fixture（`tests/fixtures/contract_v02/mock_dataset.json`，`_meta.mock = true`，未修改）。
- diff 中沒有真實座標、軌跡、騎乘時間或行程清單。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下任何腳本，沒有讀保留行程。

### E-4：修改的既有測試（`tests/test_routes_pace_eta.py`）

| 測試 | 修改 | 理由 | 原檢查的涵蓋 |
| --- | --- | --- | --- |
| `test_pace_table_matches_the_mock_fixture` | 期望值由 `[("C1", 60.0, 2), ("C2", 45.0, 2), ("C3", None, 1)]` 改為 `[("C1", None, 1), ("C2", 52.5, 2), ("C3", 40.5, 2)]`；加 docstring。`pace_version="pace-mock-1"`、`method`、`n_trips` 的斷言不變 | CL-B1-4 第 3 項：配速表以重算的門檻分類，不用 fixture 衍生列的 `seg_category`。fixture 的可計時曲率 15、20、140、150、420 → `curv-tercile-20-150`；C1＝{15}（1 段，少於 2 → null），C2＝{20, 140}（60、45 km/h → 52.5），C3＝{150, 420}（45、36 km/h → 40.5）。手算見 docstring | 同一測試仍以 fixture 驗證三個類別的配速與路段數 |
| `test_suspect_and_invalid_rows_do_not_change_the_pace` | `categories[0]["speed_kmh"] == 60.0` 改為：整份配速表（表頭與類別）等於只用 `quality == ok` 的列建立的配速表，另加 `categories[1]["speed_kmh"] == 52.5`。`pace_version="p"` 不變 | 重新分類後 C1 只剩 1 段，`speed_kmh` 為 null，原斷言不再成立。新斷言比原斷言更嚴：suspect／invalid 列若進入計算，會改變門檻、`category_scheme`、配速或餘裕係數 | 同一測試 |

**S-3（`test_pace_table_matches_the_mock_fixture__v03_contract`）沒有恢復**，標記與內文未修改：見第 8 節 C-10-1。CL-B1-8 §3.2 第 1 項要求的恢復在 #10 的範圍內無法完成。

### E-5：高風險類別的 self-verification（`decision-20261117-high-risk-categories.md` 第 5 節）

| 類別 | 核對 | 結果 |
| --- | --- | --- |
| H-2（決定衍生輸出寫到哪裡） | `create_pace_table` 只寫到呼叫者提供且已存在的目錄，沒有預設位置，不建立目錄（`test_the_directory_must_be_given_and_exist`）；測試只寫 `tmp_path`。diff 與新測試不含座標、軌跡、時間序列或行程清單（E-3）。`git ls-files` 不含 `.env`、`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/`（於 `be0074d` 執行 `git ls-files \| grep -iE "\.env\|\.gpx\|\.fit\|^data/(raw\|private\|bmw)/"`：無輸出）。工作目錄在測試後沒有新增檔案（`git status` 乾淨） | 符合。真實行程上的行為 NOT VERIFIED（沒有授權，RB-7） |
| H-3（保留行程拒絕、`research-`／`user-` 分離、不覆寫） | 拒絕在任何計算之前（`test_the_refusal_comes_before_any_computation`），涵蓋保留行程、不在表中、角色不一致、重複；`research-` 與 `user-` 編號分開，建立任一種都不改寫另一種的檔案（逐位元比對）；以 `"x"` 模式寫入，已存在即報錯。結果陳述：E-1 照實寫 `375 passed, 4 xfailed` 並判定不滿足，xfail 沒有陳述為通過。用語：新增文字沒有把 `eta_safe` 稱為 P90 或百分位數，沒有官方警特報的宣稱（`grep -niE "p90\|percentile\|百分位\|分位數\|警特報"`：只有模組說明原有的否定句 "it is not a P90"） | 符合 |
| H-4（配速為 null 的處理與預設值） | 路段數不足時 `speed_kmh` 與 `stop_ratio` 都是 null，不以其他類別代替；沒有可計時路段時報錯、不建表、不寫檔；使用到的欄位缺漏或非有限值時報錯（6 組）；`min_segments`、`built_at` 不合法時報錯；0.20 只在計入少於 8 折時出現（契約定義的 `default`，並以 `margin_basis` 標示），不是缺漏時的補值；被拿掉的那一趟算不出配速時該折不計入，不以 0 或其他值代替；沒有 `user-` 版本時回傳 `None` 而不是讀任何預設版本 | 符合 |

### 未執行的檢查

- 以真實的配速行程建立配速表、留一趟或回歸檢查：NOT RUN（Issue 排除範圍；需要 acceptor 另外同意，RB-7）。
- E1 Lite／E2：NOT RUN（不在範圍）。本工作的任何數字都不是 E1／E2 的結果。
- SB1-AC2 的整合測試：NOT RUN（屬 SPEC-B1 Spec Integration Audit 的範圍，需要 #11）。依 C-10-1，它在目前的驗證程式下預期會在契約 3 不變條件 3 失敗。

## 7. Audit status

Formal：每張 Ticket 的 independent audit 為必要（Bindings 第 5 節）。尚未派工；R1 由 Orchestrator 依 Bindings 第 3.3、3.7 節派工。本 worklog 的突變檢查與自我核對是 self-verification，不是 audit。依 C-10-1，在 Design Authority 裁決之前，#10 的 E-1 不滿足。

## 8. Remaining work 與 concerns

| ID | 內容 | 狀態／required authority |
| --- | --- | --- |
| **C-10-1**（**已裁決**：CL-B1-12，第 9 節） | **S-3 無法依 CL-B1-8 §3.2 恢復；#10 的 E-1 不滿足。** `contracts/validate.py` 的 `validate_pace_table(header, categories, derived_rows)` 以衍生路段表的 `seg_category` 計算每個類別的合格列數，要求等於 `n_segments`（第 253–258 行，標為 invariant 3）。CL-B1-4 第 3 項要求配速表以重算的門檻重新分類、不使用衍生表的 `seg_category`。兩者只在衍生表的分類剛好與重算的三分位分類相同時一致；mock fixture 不是（`curv-mock` 與 `curv-tercile-20-150`），所以符合 CL-B1-4 的輸出得到 2 個違反（E-1 第 iv 項）。`ingest` 以固定門檻（預設 80／250）分類，所以 SB1-AC2 的整合（ingest → `user-` 配速表 → 通過契約 3 v0.3）與 `validate_dataset` 在一般情形下也會遇到同樣的違反。DESIGN 契約 3 不變條件 3 的原文是「只使用符合契約 1 不變條件 4 的列」，沒有寫逐類別計數；逐類別計數是 v0.2 Spike 由衍生表取類別時的實作。可能的處理（Executor 不作選擇）：(a) 驗證程式依表頭 `category_scheme` 還原門檻後重新分類再計數；(b) 改為只核對合格列的總數；(c) S-3 改用衍生分類剛好一致的資料（會遮住這個衝突，Executor 認為不妥，沒有採用）；(d) S-3 不帶衍生路段表驗證，另以其他測試涵蓋不變條件 2／3。(a)、(b) 需要修改 `contracts/validate.py`，在 Issue #10 的範圍（`pace/table.py`）之外；(c)、(d) 涉及「只移除標記而讓檢查消失不算恢復」的判斷。S-3 的標記與內文保持原樣 | **BLOCKED**，required authority = **Design Authority**（契約語義與 boundary：修改 `contracts/` 是否在 #10 內、不變條件 3 在 CL-B1-4 下的意思、S-3 的恢復方式）。裁決後的剩餘工作：依裁決修改並移除 S-3 的標記，重新執行並記錄 E-1 |
| C-10-2（**已裁決**：CL-B1-13 確認，不需修改） | D-10-2：留一趟每一折的配速用到小數兩位的 `speed_kmh`（與配速表、ETA 相同），參考實作用未捨入的速度 | 請 Design Authority 確認；不阻擋 |
| C-10-3（**已裁決**：CL-B1-14 確認；第 3 項的要求已實作，第 9 節） | D-10-3：`user-` 不接受指定編號；同一數值的不同位數寫法視為已存在 | 請 Design Authority 確認；不阻擋 |
| C-10-4（DA record 第 10 節：tracked item，#10 不修改） | `compare_methods`（DC-10 的方法比較）仍以衍生表的 `seg_category` 分組，與配速表的分類來源不同。不在 Issue #10 的範圍，未修改 | 資訊；是否需要調整由 Design Authority 決定 |
| C-10-5 | mock fixture 的配速表（`curv-mock`，C1 60.0／C2 45.0／C3 null）不再是以 fixture 衍生列建立的結果；#11 的 ETA 測試以 fixture 的配速表為輸入，不受影響 | 資訊 |
| C-10-6 | `DESIGN.md` 的實作狀態陳述（§6.1「都尚未實作」等）在本工作後部分過時 | 依 derivation §8，由 AB-12 的文件工作處理；不在 #10 |
| — | 以真實行程的檢查 | NOT VERIFIED，required authority = acceptor（RB-7）；不是 #10 的 AC |

## 9. Rework：CL-B1-12、CL-B1-13、CL-B1-14 的處置（同一 work item、同一 cycle 的實作階段）

派工：Orchestrator 以 SendMessage 續派同一 Executor（agentId `a54ac9cf0e452782b`），依 `docs/governance/records/decisions/decision-20261118-issue10-pace-contract.md`（DA，HEAD `e0626a3`）第 8 節「#10 必須變更」的清單完成契約內工作。Contract reference 增列：**CL-B1-12**（不變條件 3 的意思與檢查方式；修訂 CL-B1-4 第 1、3 項；#10 的檔案範圍擴及 `contracts/validate.py` 的不變條件 3 一段與 `tests/test_contracts.py`）、**CL-B1-13**（確認 D-10-2）、**CL-B1-14**（確認 D-10-3，並要求選用路徑對同數值兩個檔案報錯）。CL-B1-4 第 1、3 項以該 record 第 3.3 節為準。

### 9.1 Work performed（`e0f6c78`）

1. `src/moto_copilot/contracts/validate.py`：只改 `validate_pace_table` 中帶入衍生路段表時的不變條件 3 一段（CL-B1-12 §3.2），另在模組說明補一句。合格列＝`pace_eligible` 且屬表頭 `trip_ids`。(1) 三個類別的 `n_segments` 合計不等於合格列數時回報 `n_segments add up to <n>, but <m> rows are eligible (invariant 3)`（`n_segments` 不是整數時已由 schema 回報，不做合計）。(2) 合格列的 `category_scheme` 全部等於表頭時，另做原有的逐類別核對（訊息不變）。不解析 `category_scheme`、不重新分類。不變條件 1、2、4、6、7 與 `ingest_version` 的檢查、`pace_eligible` 都不變。
2. `src/moto_copilot/pace/table.py`：
   - `timed_rows`：依修訂後的 CL-B1-4 第 1 項，改為取合格列（`trip_role = pace`、`quality = ok`、`seg_category` 不是 `null`）；`seg_category` 只用來取列，不用來分類。合格列曲率為 `null`、數值欄位缺漏、不是有限數或為負，或 `length_m`／`moving_time_s` 不大於 0 時報錯，不略過、不補值（取代 D-10-8）。
   - `create_pace_table`：寫入前以 `validate_pace_table(header, categories, rows)`（帶衍生路段表）核對，不符就不寫。
   - `latest_user_pace_table`：同一數值有一個以上的 `user-` 檔案時報錯（CL-B1-14 第 3 項）。
   - `loo_folds` 不變（CL-B1-13）；`compare_methods` 不變（DA record 第 10 節）。
3. 測試：見第 9.2 節的 E-2 增列與第 9.4 節的 E-4。`tests/test_routes_pace_eta.py` 只移除 S-3 的 strict xfail 標記（兩行），內文不改；S-4～S-6 不動。
4. 沒有修改 fixture、`conftest.py`、`pyproject.toml`、`ingest/`、`routes/`、`DESIGN.md`、任何 Issue 或 record（本 worklog 除外）。`git diff --stat e0626a3 e0f6c78`：`contracts/validate.py`、`pace/table.py`、`tests/test_contracts.py`、`tests/test_pace_table.py`、`tests/test_routes_pace_eta.py`。Commit 前確認暫存的檔案不含 `.env`、GPX、FIT 或 `data/`。沒有 push、沒有開 PR。

**Decision D-10-9**：CL-B1-12 §3.3 的合格列括號寫「`trip_role = pace`、`quality = ok`、`seg_category` 不是 `null`」，契約 1 不變條件 4（`pace_eligible`）另含 `moving_time_s` 不是 `null`。`timed_rows` 依括號的三項取列，`moving_time_s` 為 `null` 的列因此是「數值欄位缺漏」而報錯，不是被略過。兩種讀法在符合契約 1 的資料上相同（契約 1 不變條件 3：`moving_time_s` 為 `null` 恰好是 `invalid`）；只在不符契約 1 的輸入上不同，此時報錯是 fail closed，與該節「不略過、不補值」一致。驗證程式一側仍用 `pace_eligible`，所以兩側在任何能建表的輸入上取到同一組列。不視為需要 DA 的語義問題，記錄於此供 R1 核對。

### 9.2 E-2 的增列與變動（於 `e0f6c78`，全部 PASS）

| 條件（CL-B1-12 §8／§3、CL-B1-14） | 測試 | 結果 |
| --- | --- | --- |
| §3.2 (i) 不同分級版本、合計等於合格列、逐類別與衍生類別不同 → 沒有違反 | `test_contracts.py::test_another_scheme_checks_the_total_not_the_derived_categories` | PASS |
| §3.2 (ii) 不同分級版本、多計一列或少計一列 → 違反 | `test_contracts.py::test_another_scheme_still_needs_the_total_of_eligible_rows[C3-3-6]`、`[C2-1-4]` | PASS |
| §3.2 (iii) 同一分級版本、合計相同但逐類別不符 → 違反（且沒有合計違反） | `test_contracts.py::test_the_same_scheme_still_checks_each_category`；既有 `test_segment_count_counts_only_eligible_rows`（未修改）仍 PASS | PASS |
| §3.2 (iv) `trip_ids` 以外的行程與保留行程的列不計入 | `test_contracts.py::test_rows_of_other_trips_and_holdout_rows_are_not_eligible`（計入保留行程 T003 的兩列或另一個 pace 行程的一列都是違反） | PASS |
| §3.3 合格列曲率為 `null` → `build_pace_table`／`create_pace_table` 報錯、目錄沒有檔案 | `test_pace_table.py::test_an_eligible_row_without_curvature_is_an_error_and_nothing_is_written`；`test_timed_rows_follow_cl_b1_4_item_1`（修改，E-4） | PASS |
| §3.3 `moving_time_s` 等於 0 → 報錯、不寫檔（取代 D-10-8） | `test_pace_table.py::test_an_eligible_row_with_zero_moving_time_is_an_error_and_nothing_is_written` | PASS |
| §3.3 曲率有值而 `seg_category` 為 `null` 的列不被使用 | `test_pace_table.py::test_a_row_with_curvature_but_no_seg_category_is_not_used` | PASS |
| §8 衍生分類與重算分類不同的合成案例，寫出的表通過 `validate_pace_table(header, categories, rows)` | `test_pace_table.py::test_a_table_whose_categories_differ_from_the_derived_ones_passes_contract_3`（衍生 C1、C1、C2；重算 `curv-tercile-60-120` 為 C1、C2、C3） | PASS |
| §8 `create_pace_table` 寫入前帶衍生路段表核對 | `test_pace_table.py::test_the_writer_checks_contract_3_with_the_derived_rows`（以 monkeypatch 讓產生者多計一段，`create_pace_table` 報錯且沒有檔案） | PASS |
| CL-B1-14 第 3 項：同數值兩個 `user-` 檔案 → `latest_user_pace_table` 報錯 | `test_pace_table.py::test_one_user_version_in_two_files_is_an_error` | PASS |
| S-3 恢復（CL-B1-8 §3.2 第 1 項） | `test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract`：不帶標記 PASS，內文未改，保留為獨立測試（CL-B1-8 §3.2 第 3 項） | PASS |

第 6 節 E-2 的其他列在 `e0f6c78` 仍全部 PASS（`test_no_timed_segment_means_no_thresholds_and_no_table` 經修改，見 E-4）。第 6 節 E-2 末段所述「兩個以 `validate_pace_table(..., rows)` 核對的測試分類剛好一致」仍成立；新增的 `test_a_table_whose_categories_differ_...` 涵蓋不一致的情形。依 CL-B1-12 §3.2 第 4 項：在分級版本不同時，驗證程式只核對合計；重算後的逐類別路段數由產生者的測試（AC 3、CL-B1-4 第 1、3 項的測試、`test_suspect_and_invalid_rows_do_not_change_the_pace`）證明，**不是**由驗證程式核對。

**突變檢查（self-verification，不是 audit）**：在工作區對上述修改逐一做下列突變，執行 `tests/test_contracts.py tests/test_pace_table.py tests/test_routes_pace_eta.py` 後還原。

| 突變 | 結果 |
| --- | --- |
| M6 拿掉合計檢查 | 3 failed |
| M7 不論分級版本一律逐類別核對（回到舊行為） | 4 failed |
| M8 永不逐類別核對 | 2 failed |
| M9 合格列不限 `trip_ids` | 1 failed |
| M10 合格列曲率為 `null` 時略過而不報錯 | 2 failed |
| M11 拿掉同數值兩個檔案的檢查 | 1 failed |
| M12 `create_pace_table` 核對時不帶衍生路段表 | 第一次 0 failed（沒有被抓到）→ 新增 `test_the_writer_checks_contract_3_with_the_derived_rows` 後 1 failed |

### 9.3 E-1：依 CL-B1-9 第 3 項，在 `e0f6c78` 執行（主 checkout，`git status` 乾淨）

**(i) `.venv/Scripts/python.exe -m pytest -q`**

```text
........................................................................ [ 18%]
........................................................................ [ 36%]
........................................................................ [ 55%]
........................................................................ [ 73%]
........................................................................ [ 92%]
.........................x.xx.                                           [100%]
387 passed, 3 xfailed in 1.58s
exit=0
```

**(iii) `.venv/Scripts/python.exe -m pytest -q -rxX`**

```text
........................................................................ [ 18%]
........................................................................ [ 36%]
........................................................................ [ 55%]
........................................................................ [ 73%]
........................................................................ [ 92%]
.........................x.xx.                                           [100%]
=========================== short test summary info ===========================
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
387 passed, 3 xfailed in 1.59s
exit=0
```

**(iv) `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py tests/test_pace_table.py tests/test_contracts.py`**（`--collect-only`：390 個測試）

```text
........................................................................ [ 18%]
.................................................F.FF................... [ 36%]
........................................................................ [ 55%]
........................................................................ [ 73%]
........................................................................ [ 92%]
..............................                                           [100%]
================================== FAILURES ===================================
_____________ test_eta_reproduces_the_mock_fixture__v03_contract ______________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '<mock 名稱，主控台編碼亂碼>', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_reproduces_the_mock_fixture__v03_contract(data):
        header, rows = eta_for(data, "R01", "P-MOCK-1", [{"after_checkpoint_id": "R01-CP03", "duration_s": 600.0}])
>       assert rows == [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-1"]
E       AssertionError: assert [{'plan_id': ...: 600.0, ...}] == [{'plan_id': ...s': 0.0, ...}]
E         
E         At index 0 diff: {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'} != {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'stop_allow_s': 0.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'}
E         Use -v to get more diff

tests\test_routes_pace_eta.py:167: AssertionError
________ test_eta_is_unknown_when_a_category_has_no_pace__v03_contract ________

data = {...同上...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_is_unknown_when_a_category_has_no_pace__v03_contract(data):
        header, rows = eta_for(data, "R02", "P-MOCK-2", [])
        data["eta_headers"], data["eta_segments"] = [header], rows
>       assert validate_eta_output([header], rows, data["routes"], data["route_segments"], data["checkpoints"],
                                   data["pace_header"], data["pace_categories"]) == []
E       assert ['eta_segment...red property'] == []
E         
E         Left contains 2 more items, first extra item: "eta_segments[0] schema: (record): 'stop_allow_s' is a required property"
E         Use -v to get more diff

tests\test_routes_pace_eta.py:182: AssertionError
_________ test_eta_output_passes_the_contract_with_and_without_breaks _________

data = {...同上...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_output_passes_the_contract_with_and_without_breaks(data):
        for plan_id, breaks in (("P-A", []), ("P-B", [{"after_checkpoint_id": "R01-CP04", "duration_s": 900.0}])):
            header, rows = eta_for(data, "R01", plan_id, breaks)
>           assert validate_eta_output([header], rows, data["routes"], data["route_segments"], data["checkpoints"],
                                       data["pace_header"], data["pace_categories"]) == []
E           assert ['eta_segment...status is ok'] == []
E             
E             Left contains 5 more items, first extra item: "eta_segments[0] schema: (record): 'stop_allow_s' is a required property"
E             Use -v to get more diff

tests\test_routes_pace_eta.py:191: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
3 failed, 387 passed in 1.71s
exit=1
```

輸出逐字轉錄，改寫同第 6 節（亂碼的 mock 路線名稱、後兩個 `data = {...}` 以「同上」縮寫）。原始輸出在 Executor 的 scratchpad（`s10/f-*.txt`），不是受版控的 evidence。

**依 CL-B1-9 第 3 項逐條判定：**

| 條件 | 結果 |
| --- | --- |
| i. exit code 0 | 成立 |
| ii. 摘要只有 `passed`、`xfailed` | 成立（`387 passed, 3 xfailed`） |
| iii. 每個 xfail 都是 `restored by #11`，對應 S-4～S-6，數目不超過 3；沒有 `restored by #9` 或 `#10` 的標記；沒有其他 `xfail`／`skip` | 成立。`grep -rn "xfail\|skip" tests/`：只有 `tests/test_routes_pace_eta.py` 第 163、177、186 行，三個都是 `restored by #11`；`test_contracts.py`、`test_pace_table.py` 沒有標記 |
| iv. `--runxfail` 失敗的恰好是那些 xfail，訊息只涉及 v0.3 項目 | 成立：3 個失敗恰好是 S-4～S-6，訊息只涉及 `stop_allow_s`（必填）與 S-4 的列比對只差 `stop_allow_s`。S-3 在 `--runxfail` 與一般執行都 PASS |
| v. S-4～S-6 的測試與標記在 #10 沒有修改 | 成立：`git diff 20939aa e0f6c78 -- tests/test_routes_pace_eta.py` 只有第 6 節 E-4 的兩個測試與 S-3 標記的移除 |

**結果陳述**：`387 passed, 3 xfailed`（依 CL-B1-8、CL-B1-9）。3 個 xfail 是 #11 的 S-4～S-6，不是通過。**#10 的 E-1 依 CL-B1-9 第 3 項滿足。** SPEC-B1 層級的 SB1-AC3（沒有任何 `xfailed`）仍待 #11。

### 9.4 E-4：本次修改的既有測試

| 測試 | 修改 | 理由 |
| --- | --- | --- |
| `tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract`（S-3） | 移除 strict xfail 標記（兩行）；內文未改，保留為獨立測試 | CL-B1-8 §3.2 第 1、3 項；CL-B1-12 §3.5：驗證程式修改後，fixture（`curv-mock`）與輸出（`curv-tercile-20-150`）分級版本不同，只做合計檢查（合計 5、合格列 5），原斷言 `validate_pace_table(header, categories, data["derived_segments"]) == []` 不帶標記通過。原檢查（不變條件 2、3 等帶衍生路段表的核對）仍在同一斷言中 |
| `tests/test_pace_table.py::test_timed_rows_follow_cl_b1_4_item_1`（`be0074d` 新增） | 原本「`quality = ok`、`seg_category` 有值、曲率 `null`」的列被預期略過；改為：該列有曲率時被取用（預期清單加上 `("T102", 0)`），曲率改為 `null` 後預期 `ValueError`（`no curvature`）；加 docstring | CL-B1-12 §3.3 修訂 CL-B1-4 第 1 項：取列依契約 1 不變條件 4，合格列曲率為 `null` 是錯誤；DA record 第 8 節明列此修改 |
| `tests/test_pace_table.py::test_no_timed_segment_means_no_thresholds_and_no_table`（`be0074d` 新增） | 第三列由「`moving_time_s` = 0（略過）」改為 `quality = suspect`；`moving_time_s` = 0 移到新測試 `test_an_eligible_row_with_zero_moving_time_is_an_error_and_nothing_is_written`，預期錯誤 | CL-B1-12 §3.3：`moving_time_s` 等於 0 改為錯誤（取代 D-10-8）。原測試的目的（沒有可計時路段時不建表、不寫檔）不變 |

`tests/test_contracts.py` 的既有測試沒有修改（只新增 4 個測試函式與一個 helper）。

### 9.5 E-3、E-5 的增補

- E-3：新增測試全部是手寫的整數值或 mock fixture 的副本（在測試內修改副本，fixture 檔案未改）；代號 `T004`、`T121`～`T123` 是編造的；沒有座標、軌跡或時間序列；檔案只寫到 `tmp_path`。
- E-5 H-3：驗證程式的合格列計數排除保留行程、suspect、invalid 與 `trip_ids` 以外的列，並有違反的測試（第 9.2 節 (ii)、(iv)）。H-4：合格列的缺漏（曲率 `null`、`moving_time_s` 為 0）是明確錯誤且不寫檔；同一版本兩個檔案時不自行挑選。H-2：沒有新的寫入位置；`git ls-files | grep -iE "\.env|\.gpx|\.fit|^data/(raw|private|bmw)/"` 於 `e0f6c78` 無輸出。用語：新增的程式說明與錯誤訊息沒有 P90、百分位數或官方警特報的字樣。
- `validate.py` 的 diff 只涉及 `validate_pace_table` 的不變條件 3 一段與模組說明的一句（DA record 第 8 節 R1 最低核對範圍）。

### 9.6 Binding、audit status 與剩餘工作

- Binding（自我觀測，不是派工者的核對）：agentId `a54ac9cf0e452782b`，rework commit 之後、本節寫入前，(`claude-opus-5-5`, `high`) 132 則，集合只有一個元素。沒有使用 bounded assignments，沒有派工任何 subagent。
- Audit status：Formal，R1 必要，尚未派工；R1 的 bounded pack 須包含 DA record `decision-20261118-issue10-pace-contract.md`（該 record 第 9 節）。本節的突變檢查是 self-verification，不是 audit。
- 剩餘工作與 concerns：C-10-1～C-10-3 已裁決並處置；C-10-4 是 DA 的 tracked item；C-10-5、C-10-6 維持第 8 節的處理。新增 concern：無。真實行程上的行為仍是 NOT VERIFIED（RB-7，required authority = acceptor），不是 #10 的 AC。
