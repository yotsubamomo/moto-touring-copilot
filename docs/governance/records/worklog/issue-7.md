# Worklog — Issue #7（SPEC-B1 B1-1）`contracts`：契約 1、3、4 的 v0.3 欄位與不變條件

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #7（BATCH-1 B1-1），OC-1 Formal run `run-20261117-oc1-issue7` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | Cycle 0：Executor 工作完成（`DONE_WITH_CONCERNS`）。Cycle 1：R1 BLOCKING（R1-F1）→ targeted correction（`8981e9d`）→ R2。結案前的狀態見第 10 節；Ticket closure 由 Orchestrator 依 orch-default §7 判定，不由本 worklog 宣告 |
| Subject | branch `oc1-run1-contracts-v03`；BASE `ff049661f968adace4dd017cf560316e5684440d`；實作 commit **`a304ee2ac0ec3d8468e446b089216f0cb000f72b`**（`a304ee2`）。本 worklog 在其後的 record-only commit 加入（`docs/governance/records/**`，Bindings 第 7 節）。Cycle 1 修正 commit **`8981e9d32d4fb2f1c13dd4909243b88114af06a2`**（第 9 節） |
| 日期 | 2026-11-17 |

## 1. Contract reference

- **Ticket**：GitHub Issue #7 的內文與 7 項 AC（以 `gh issue view 7` 唯讀取得；BD-3 的雜湊版本）。本 work item 沒有修改 Issue #7（沒有留言、改狀態或編輯）。
- **Spec**：SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）：§4 CL-B1-1、CL-B1-2、CL-B1-7；§5 的 E-1～E-5 與 #7 列（高風險類別 H-3、H-4）。
- **CL-B1-8**：`docs/governance/records/decisions/decision-20261117-issue7-spike-tests.md`（Spike 測試的處理與 E-1 在 #7 的判定）。
- **其他引用**：`decision-20261117-high-risk-categories.md`（第 3.3、3.4、4、5 節）、`decision-20261117-oc1-first-run-derivation.md`（BD-3：修改既有測試的理由寫在 worklog）；Outcome Contract OC-1（`docs/governance/records/outcome-contract.md`，acceptor 2026-11-17 針對 `873e37a` 接受）。
- **規格來源**：`DESIGN.md` §5 契約 1、3、4（v0.3 停等寬放的欄位與不變條件 1-6、3-4/6/7、4-6/8/9）、§6.1；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §1.2、§1.4、§1.6（SB2-T3、T4、T5、T8、T9 的契約部分）。
- 契約在本 work item 執行中沒有變更。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-issue7`，root session `f05b836a-2536-4286-8eb9-01b089680433`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/f05b836a-2536-4286-8eb9-01b089680433/subagents/agent-a9f372411c0f54099.{meta.json,jsonl}`。`meta.json` 的 `agentType` 是 `gov-executor`。
- Executor 自行觀測（commit 之前，以第 3.6 節的掃描方式）：agentId `a9f372411c0f54099`，(`claude-opus-5-5`, `high`) 111（觀測時點：worklog 寫入前） 則，集合只有一個元素。**這是 Executor 的自我觀測，不是派工者的核對**；依第 3.6 節，Orchestrator 採用本 return 之前須自行核對該 agent 的全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 Bindings m3、impl-default v2 §3–§5、§9、治理 §3.5、§3.7、§3.8、`gov-executor` definition、SPEC-B1、CL-B1-8、高風險類別 record、run record、Issue #7、`DESIGN.md` §5、SPEC-RESOLUTION-001 §1.2–§1.6。在 BASE 跑 `pytest -q`：`100 passed`（v0.2 的結果，依 CL-B1-8 §7 不作為 E-1 證據）。
2. `src/moto_copilot/contracts/schemas.py`：契約 1 新增必填的 `short_stop_time_s`（number ≥ 0）；契約 3 類別紀錄新增必填的 `stop_ratio`（number ≥ 0 或 null）；契約 3 表頭新增必填的 `margin_coeff`（number ≥ 0.05）與 `margin_basis`（`loo_rule`／`default`）；契約 4 路段列新增必填的 `stop_allow_s`（number ≥ 0 或 null）；契約 4 表頭 `margin_coeff` 的下限由 0 改為 0.05。`CONTRACT_VERSION` 維持 `"0.2"`（CL-B1-2）。
3. `src/moto_copilot/contracts/validate.py`：契約 1 不變條件 6；契約 3 不變條件 4、6、7；契約 4 不變條件 6（加入 `stop_allow_s`）、8、9；ETA 的累計時間改為 Σ(`typ_seg_time_s` + `stop_allow_s`)。設計決定見第 4 節。
4. `tests/fixtures/contract_v02/mock_dataset.json`：加入 v0.3 欄位、`pace_version` 改名、ETA 時間依 v0.3 算式重算（第 6 節 E-3、E-4）。
5. `tests/test_contracts.py`：新增 37 個測試函式（94 個案例，含參數化）對應 7 項 AC；修改 2 個既有測試的預期值（E-4）。
6. `tests/test_ingest.py`、`tests/test_routes_pace_eta.py`：依 CL-B1-8 §3.1 拆分 S-1～S-5、標記 S-6（E-4）。
7. 驗證（第 6 節）與 commit `a304ee2`（SA-1，topic branch，本機）。沒有 push、沒有開 PR。

## 4. Decisions and assumptions

以下都是 HOW 層級的選擇，沒有改變 Issue #7 的 AC、DESIGN §5 的 invariant 或任何 gate；沒有需要 authority 的語義決定（concern 第 8 節 C-1 除外）。

| # | 決定 | 理由 |
| --- | --- | --- |
| D-1 | `pace_version` 的樣式在 `validate.py` 以 `re.fullmatch(r"(research\|user)-[0-9]{2,}")` 檢查，不放在 JSON Schema 的 `pattern` | Python `re` 的 `$` 接受結尾的換行、`\d` 接受全形等 Unicode 數字；`fullmatch`＋`[0-9]` 兩者都拒絕（有測試）。樣式只套用在契約 3 的表頭（主鍵）；類別紀錄的 `pace_version` 本來就必須等於表頭；契約 4 表頭的 `pace_version` 仍是 `_NAME`，提供配速表時以既有的「等於配速表」檢查，沒有新增不變條件 |
| D-2 | `margin_coeff` 的「0.05 的倍數」與 `default` 的「0.20」以 1e-9 容差比較 | 只吸收二進位浮點誤差（例如 0.35 ÷ 0.05 = 6.999…）；JSON Schema 的 `multipleOf` 對小數不可靠。0.051、0.149、0.12 仍被拒絕（有測試） |
| D-3 | 契約 4 表頭的 `margin_coeff` 只加下限 0.05，不加倍數規則；與配速表的比較用完全相等 | DESIGN §5 契約 4 只寫「不小於 0.05」與「等於配速表的值」；值由 ETA 產生者自配速表表頭照抄（CL-B1-5），所以用完全相等，較嚴格（fail closed） |
| D-4 | 不變條件 8 的實作：(a) 保留既有的絕對式檢查（`eta_typ`＝出發＋累計＋`break_time_s`；`eta_safe`＝該值＋餘裕），累計改為 Σ(`typ_seg_time_s`+`stop_allow_s`)；(b) 新增相鄰兩列 `eta_typ` 差的檢查（差＝後一列 `typ_seg_time_s`＋`stop_allow_s`＋兩列 `break_time_s` 的差）；(c) 新增 `eta_safe − eta_typ`＝`margin_coeff`×累計的檢查；(d) `stop_allow_s`＝`stop_ratio`×`typ_seg_time_s`。全部容許 1 秒 | (a) 是欄位定義（DESIGN §5 契約 4 的 `eta_typ`／`eta_safe` 說明），(b)(c)(d) 是 AC 的字面形式。各列各容許 1 秒時，(a) 不蘊含 (b)(c)，所以兩者都檢查；有測試顯示 (b) 抓得到 (a) 抓不到的情形 |
| D-5 | (d) 只在提供配速表（`pace_categories`）時檢查；沒有配速表時只檢查 (a)(b)(c) | `stop_ratio` 只存在於配速表。對應 Issue #7 AC 7 的「同時提供配速表與 ETA 輸出時」與既有 `validate_eta_output` 的選用參數設計 |
| D-6 | 狀態 `ok` 的列 `stop_allow_s` 為 null 時記為違反（沿用既有「null time although status is ok」）；配速表中路線所用類別沒有 `stop_ratio` 時記為違反（「cannot be checked」），不略過 | 不變條件 8 要求每一列 `stop_allow_s` 有值；無法核對時 fail closed（H-4） |
| D-7 | `validate.py` 不由衍生路段表重算 `stop_ratio`，也不檢查 `margin_basis` 與折數 | Issue #7 排除範圍「`validate.py` 不重算配速或餘裕係數」；DESIGN §5 契約 3 不變條件 5、6 寫明由產生者的測試檢查 |
| D-8 | 非數值的 `typ_seg_time_s`／`stop_allow_s`／`break_time_s` 在新增的算術前停止（schema 已回報），不拋例外 | 新增的程式路徑不引入新的例外；既有路徑的同類問題見第 8 節 C-3 |
| D-9 | Fixture 的 `pace_version` 取 `user-01`，不用 `research-` | mock fixture 不是研究凍結的配速表；用 `research-` 會看起來像凍結的研究 Profile（H-3 判定 3.3 第 1 項） |
| D-10 | Fixture 的 `_meta.contract_version` 維持 `"0.2"`，`note` 加一句說明它帶有 v0.3 停等寬放欄位 | CL-B1-2：v0.3 尚未完整實作，不宣稱 v0.3；`test_fixture_is_marked_as_mock` 斷言它等於 `CONTRACT_VERSION == "0.2"`，不改 |
| D-11 | 模組 docstring 由「v0.2」改為「v0.2 加上 v0.3 停等寬放欄位（Issue #7）」，並寫明 ID 規則與契約 2 尚未包含 | 正確陳述現況，不宣稱 v0.3（CL-B1-2、H-3） |

## 5. Artifacts

| 檔案 | 變更 |
| --- | --- |
| `src/moto_copilot/contracts/schemas.py` | 第 3 節第 2 項 |
| `src/moto_copilot/contracts/validate.py` | 第 3 節第 3 項 |
| `tests/fixtures/contract_v02/mock_dataset.json` | E-3、E-4 |
| `tests/test_contracts.py` | 新增 37 個測試函式；修改 docstring 與 2 個測試的預期值（E-4） |
| `tests/test_ingest.py` | S-1、S-2 拆分（E-4） |
| `tests/test_routes_pace_eta.py` | S-3、S-4、S-5 拆分，S-6 標記（E-4） |
| `docs/governance/records/worklog/issue-7.md` | 本檔（record-only commit） |

實作 commit：`a304ee2ac0ec3d8468e446b089216f0cb000f72b`。`git diff --stat ff04966 a304ee2` 只含上表的程式與測試，以及 run 啟動時已存在的兩份 records（`f644757`）；不含 `ingest/`、`pace/`、`routes/`（K-5）。

## 6. Verification

所有指令都在 repo 根目錄、Git Bash 下執行，不需要金鑰、不讀 GPX、不讀 `data/`。下列輸出是在 commit 前、工作目錄內容與 `a304ee2` 相同時擷取的；commit 之後在 HEAD `a304ee2`（工作目錄乾淨）重跑輸出 1–4，除了執行秒數之外逐行相同（以 `diff` 核對）。

### E-1：pytest（CL-B1-8 §3.3 的六項判定）

**結果陳述：`193 passed, 6 xfailed`（依 `decision-20261117-issue7-spike-tests`）。** 不是「全數通過」：6 個 xfail 是 Spike 產生者尚未輸出 v0.3 欄位的已知缺口，依 CL-B1-8 §3.2 最遲在 #9、#10、#11 恢復；SPEC-B1 的 SB1-AC3 在那之前不成立。

| CL-B1-8 §3.3 | 判定 | 依據 |
| --- | --- | --- |
| 1. exit code 0 | 成立 | 下方輸出 1 的 `exit=0` |
| 2. 摘要只有 `passed` 與 `xfailed` | 成立 | `193 passed, 6 xfailed`；沒有 failed、error、xpassed、skipped |
| 3. `xfailed` 數＝帶標記的測試數，各對應 S-1～S-6 | 成立 | 6 個，見輸出 2 與下表 |
| 4. `--runxfail` 下失敗的恰好是那些測試，且只涉及 v0.3 新增項目 | 成立 | 輸出 3：失敗的恰好是 6 個；輸出 4 列出每一個的全部違反：只有 `short_stop_time_s`、`margin_coeff`、`margin_basis`、`stop_ratio`、`stop_allow_s` 的 required，S-4 只差 `stop_allow_s` 與隨它改變的 `eta_typ`／`eta_safe`。S-6 的「`seg 0 has a null time although status is ok`」是產生者沒有寫 `stop_allow_s`（讀為 null）所致，屬同一缺口（D-6） |
| 5. 完整輸出記在 worklog | 成立 | 下方輸出 1–4 |
| 6. E-4 逐項列出 | 成立 | E-4 |

| xfail 測試 | CL-B1-8 編號 | 恢復於 |
| --- | --- | --- |
| `tests/test_ingest.py::test_rows_conform_to_the_contract_in_both_versions__v03_contract` | S-1 | #9 |
| `tests/test_ingest.py::test_points_with_a_repeated_time_are_dropped__v03_contract` | S-2 | #9 |
| `tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract` | S-3 | #10 |
| `tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract` | S-4 | #11 |
| `tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract` | S-5 | #11 |
| `tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks` | S-6 | #11 |

**輸出 1：`.venv/Scripts/python.exe -m pytest -q`**

```text
........................................................................ [ 36%]
........................................................................ [ 72%]
......................x........x.............x....x.xx.                  [100%]
193 passed, 6 xfailed in 0.40s
exit=0
```

**輸出 2：`.venv/Scripts/python.exe -m pytest -q -rxX`**

```text
........................................................................ [ 36%]
........................................................................ [ 72%]
......................x........x.............x....x.xx.                  [100%]
=========================== short test summary info ===========================
XFAIL tests/test_ingest.py::test_rows_conform_to_the_contract_in_both_versions__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; build_rows does not write short_stop_time_s yet
XFAIL tests/test_ingest.py::test_points_with_a_repeated_time_are_dropped__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; build_rows does not write short_stop_time_s yet
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
193 passed, 6 xfailed in 0.40s
exit=0
```

**輸出 3：`PYTHONUTF8=1 .venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py`**（`PYTHONUTF8=1` 只為了讓 fixture 中的中文模擬路線名稱在重導向的輸出中不亂碼；不影響測試）

```text
....F........F.............F....F.FF.                                    [100%]
================================== FAILURES ===================================
______ test_rows_conform_to_the_contract_in_both_versions__v03_contract _______

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; "
                                           "build_rows does not write short_stop_time_s yet")
    def test_rows_conform_to_the_contract_in_both_versions__v03_contract():
        private, _ = rows_of(straight(12_000))
        public = to_public(private)
>       assert validate_derived_segments(private, "private") == []
E       assert ['derived_seg...roperty', ...] == []
E         
E         Left contains 8 more items, first extra item: "derived_segments(private)[0] schema: (record): 'short_stop_time_s' is a required property"
E         Use -v to get more diff

tests\test_ingest.py:74: AssertionError
_________ test_points_with_a_repeated_time_are_dropped__v03_contract __________

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; "
                                           "build_rows does not write short_stop_time_s yet")
    def test_points_with_a_repeated_time_are_dropped__v03_contract():
        pts = straight(12_000)
        pts[200:200] = [TrackPoint(pts[200].lat, pts[200].lon, pts[199].time)] * 3
        rows, _ = rows_of(pts)
>       assert validate_derived_segments(rows, "private") == []
E       assert ['derived_seg...roperty', ...] == []
E         
E         Left contains 8 more items, first extra item: "derived_segments(private)[0] schema: (record): 'short_stop_time_s' is a required property"
E         Use -v to get more diff

tests\test_ingest.py:168: AssertionError
___________ test_pace_table_matches_the_mock_fixture__v03_contract ____________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; "
                                           "build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet")
    def test_pace_table_matches_the_mock_fixture__v03_contract(data):
        header, categories = build_pace_table(data["derived_segments"], ["T001", "T002"], pace_version="user-01",
                                              min_segments=2, built_at=NOW)
>       assert validate_pace_table(header, categories, data["derived_segments"]) == []
E       assert ['pace_header...red property'] == []
E         
E         Left contains 5 more items, first extra item: "pace_header[0] schema: (record): 'margin_coeff' is a required property"
E         Use -v to get more diff

tests\test_routes_pace_eta.py:122: AssertionError
_____________ test_eta_reproduces_the_mock_fixture__v03_contract ______________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_reproduces_the_mock_fixture__v03_contract(data):
        header, rows = eta_for(data, "R01", "P-MOCK-1", [{"after_checkpoint_id": "R01-CP03", "duration_s": 600.0}])
>       assert rows == [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-1"]
E       AssertionError: assert [{'plan_id': ...: 600.0, ...}] == [{'plan_id': ...s': 0.0, ...}]
E         
E         At index 0 diff: {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'} != {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'stop_allow_s': 0.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'}
E         Use -v to get more diff

tests\test_routes_pace_eta.py:163: AssertionError
________ test_eta_is_unknown_when_a_category_has_no_pace__v03_contract ________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

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

tests\test_routes_pace_eta.py:178: AssertionError
_________ test_eta_output_passes_the_contract_with_and_without_breaks _________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

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

tests\test_routes_pace_eta.py:187: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_ingest.py::test_rows_conform_to_the_contract_in_both_versions__v03_contract
FAILED tests/test_ingest.py::test_points_with_a_repeated_time_are_dropped__v03_contract
FAILED tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
6 failed, 31 passed in 0.24s
exit=1
```

**輸出 4：被遮住的失敗的完整違反清單。** pytest 的斷言訊息會截斷清單，所以另以 Executor 的暫存腳本（不在 repo 內，只重跑與 6 個 xfail 測試相同的產生者呼叫並印出每一則違反）取得：

```text
== S-1 private: 8 violation(s)
    derived_segments(private)[0] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[1] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[2] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[3] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[4] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[5] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[6] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[7] schema: (record): 'short_stop_time_s' is a required property
== S-1 public: 8 violation(s)
    derived_segments(public)[0] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(public)[1] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(public)[2] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(public)[3] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(public)[4] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(public)[5] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(public)[6] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(public)[7] schema: (record): 'short_stop_time_s' is a required property
== S-2: 8 violation(s)
    derived_segments(private)[0] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[1] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[2] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[3] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[4] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[5] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[6] schema: (record): 'short_stop_time_s' is a required property
    derived_segments(private)[7] schema: (record): 'short_stop_time_s' is a required property
== S-3: 5 violation(s)
    pace_header[0] schema: (record): 'margin_coeff' is a required property
    pace_header[0] schema: (record): 'margin_basis' is a required property
    pace_categories[0] schema: (record): 'stop_ratio' is a required property
    pace_categories[1] schema: (record): 'stop_ratio' is a required property
    pace_categories[2] schema: (record): 'stop_ratio' is a required property
== S-4 header equal: True
   seg 0 differs in: {'stop_allow_s': ('<absent>', 0.0)}
   seg 1 differs in: {'eta_safe': ('2026-11-21T07:06:00+08:00', '2026-11-21T07:06:11+08:00'), 'eta_typ': ('2026-11-21T07:05:00+08:00', '2026-11-21T07:05:09+08:00'), 'stop_allow_s': ('<absent>', 9.0)}
   seg 2 differs in: {'eta_safe': ('2026-11-21T07:20:48+08:00', '2026-11-21T07:21:20+08:00'), 'eta_typ': ('2026-11-21T07:19:00+08:00', '2026-11-21T07:19:27+08:00'), 'stop_allow_s': ('<absent>', 18.0)}
   seg 3 differs in: {'eta_safe': ('2026-11-21T07:28:00+08:00', '2026-11-21T07:28:32+08:00'), 'eta_typ': ('2026-11-21T07:25:00+08:00', '2026-11-21T07:25:27+08:00'), 'stop_allow_s': ('<absent>', 0.0)}
== S-5: 2 violation(s)
    eta_segments[0] schema: (record): 'stop_allow_s' is a required property
    eta_segments[1] schema: (record): 'stop_allow_s' is a required property
== S-6 P-A: 5 violation(s)
    eta_segments[0] schema: (record): 'stop_allow_s' is a required property
    eta_segments[1] schema: (record): 'stop_allow_s' is a required property
    eta_segments[2] schema: (record): 'stop_allow_s' is a required property
    eta_segments[3] schema: (record): 'stop_allow_s' is a required property
    eta_segments: P-A seg 0 has a null time although status is ok
== S-6 P-B: 5 violation(s)
    eta_segments[0] schema: (record): 'stop_allow_s' is a required property
    eta_segments[1] schema: (record): 'stop_allow_s' is a required property
    eta_segments[2] schema: (record): 'stop_allow_s' is a required property
    eta_segments[3] schema: (record): 'stop_allow_s' is a required property
    eta_segments: P-B seg 0 has a null time although status is ok
```

**契約 CLI（root `CLAUDE.md` 的 Commands）：`PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`**

```text
data contracts v0.2: tests\fixtures\contract_v02\mock_dataset.json
  derived_segments: OK
  route_catalog: OK
  pace_table: OK
  eta_output: OK
exit=0
```

### CL-B1-8 §3.4 的機械核對

| # | 結果 |
| --- | --- |
| K-1 | `grep -rn "xfail\|skip" tests/`：6 處，全部是 `@pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #<n>; ...")`，`test_ingest.py` 2 處（#9、#9）、`test_routes_pace_eta.py` 4 處（#10、#11、#11、#11），與 CL-B1-8 第 2 節一致；沒有 `skip` |
| K-2 | `git diff ff04966 -- tests/test_ingest.py tests/test_routes_pace_eta.py`：原測試只少了被搬走的斷言（S-1 兩行、S-2 一行、S-3 一行、S-4 一行、S-5 一行）；新測試中的斷言與 BASE 原文逐字相同，唯一的字面修改是 S-3 新測試中傳給 `build_pace_table` 的 `pace_version`：`"pace-mock-1"` → `"user-01"`（CL-B1-8 §3.1 第 5 項） |
| K-3 | 第 2 節列的其他 26 個測試在 diff 中沒有變更 |
| K-4 | 本節 E-1 |
| K-5 | `git diff --stat ff04966 a304ee2` 不含 `src/moto_copilot/ingest/`、`pace/`、`routes/` |
| K-6 | `tests/test_contracts.py` 沒有任何 xfail／skip |

### E-2：AC 與另加條件對應的測試

全部結果取自 `pytest -v tests/test_contracts.py`（162 個案例全部 PASSED）；括號內是參數化案例數。

| AC／條件 | 測試（`tests/test_contracts.py`） | 結果 |
| --- | --- | --- |
| AC1 `short_stop_time_s ≤ stopped_time_s`，違反時被拒絕 | `test_short_stops_cannot_exceed_all_stops`、`test_short_stops_above_zero_stops_are_rejected`、`test_short_stops_may_equal_all_stops`（邊界相等可接受）、`test_short_stop_time_is_a_non_negative_number`（3：−1、null、字串）、`test_short_stop_time_is_required_in_both_versions`（2：公開、私有版）、`test_mock_fixture_conforms_to_every_contract`（正向） | PASSED |
| AC2 `speed_kmh` null ⇔ `stop_ratio` null；有值時可以是 0 | `test_stop_ratio_must_be_null_when_speed_is_null`、`test_stop_ratio_must_have_a_value_when_speed_has_one`、`test_stop_ratio_may_be_zero`、`test_stop_ratio_is_a_non_negative_number`（2）、`test_stop_ratio_is_required` | PASSED |
| AC3 `margin_basis` 只接受兩值；`default` ⇒ 0.20；`loo_rule` ⇒ 0.05 的倍數且 ≥ 0.05 | `test_margin_basis_has_two_values_only`（5）、`test_margin_fields_are_required`（2）、`test_default_margin_must_be_0_20`（4）、`test_loo_rule_margin_accepts_multiples_of_0_05`（12）、`test_loo_rule_margin_rejects_other_values`（6）、`test_margin_coeff_is_a_number`（3）；正向的 `default`／0.2 由 `test_mock_fixture_conforms_to_every_contract` | PASSED |
| AC4 `pace_version` 不符合樣式時被拒絕 | `test_pace_version_pattern_accepts_research_and_user`（5）、`test_pace_version_pattern_rejects_other_strings`（16，含舊的 `pace-mock-1`、`user-1`、大小寫、前後空白、結尾換行、全形數字） | PASSED |
| AC5 ETA `ok` 的不變條件（容許 1 秒） | `stop_allow_s`＝`stop_ratio`×`typ_seg_time_s`：`test_stop_allow_is_stop_ratio_times_typical_time`、`test_stop_allow_tolerates_one_second`（4）、`test_eta_without_stop_allowance_is_rejected`、`test_stop_allow_needs_the_category_stop_ratio`。逐段差：`test_eta_typ_steps_follow_typical_time_allowance_and_new_breaks`、`test_eta_typ_step_counts_a_new_break_once`。`eta_safe − eta_typ`：`test_eta_safe_margin_covers_the_allowance`、`test_eta_safe_margin_tolerates_one_second`、`test_eta_margin_of_0_05_is_allowed`。其他：`test_ok_plan_needs_a_stop_allowance`、`test_stop_allow_is_a_non_negative_number`（2）、`test_stop_allow_is_required`、`test_eta_without_a_pace_table_checks_the_times_only`；既有的 `test_eta_must_follow_the_formula`、`test_checkpoint_arrival_uses_row_c_minus_one`（5）、`test_mock_fixture_conforms_to_every_contract` | PASSED |
| AC6 `unknown` 時 `stop_allow_s`、`eta_typ`、`eta_safe` 都是 null | `test_unknown_plan_must_not_carry_a_stop_allowance`（2：0.0 與 9.0；0 也不被接受）、`test_unknown_plan_with_every_time_null_passes`；既有的 `test_unknown_plan_must_not_carry_any_time`（3） | PASSED |
| AC7 同時提供時 ETA 表頭 `margin_coeff` 等於配速表表頭 | `test_eta_margin_must_equal_the_pace_table_margin`（2：`ok` 與 `unknown` 的計畫）、`test_eta_margin_is_checked_against_the_pace_table_in_the_dataset`（經 `validate_dataset`）、`test_eta_margin_against_a_pace_table_without_margin_is_rejected` | PASSED |
| 範圍：契約 4 表頭 `margin_coeff` 下限 0.05 | `test_eta_margin_is_at_least_0_05`（3）、`test_eta_margin_of_0_05_is_allowed` | PASSED |
| 範圍：fixture 中不符合新樣式的 `pace_version` 改名 | fixture 中已沒有 `pace-mock-1`；`test_mock_fixture_conforms_to_every_contract` 與契約 CLI 都通過 | PASSED |
| CL-B1-2：`CONTRACT_VERSION` 不改為 0.3 | `test_fixture_is_marked_as_mock`（斷言 `CONTRACT_VERSION == "0.2"`）；CLI 印出 `data contracts v0.2` | PASSED |
| CL-B1-1：只用合成資料，不讀 `data/`、不執行 `experiments/` | E-3；本 work item 的指令紀錄沒有任何 `data/`、`.env`、`experiments/` 的存取 | 符合 |
| CL-B1-7：不稱 P90／百分位數、不稱官方警特報 | `git diff ff04966 -- src tests` 的新增行對 `p90\|percentile\|百分位\|分位\|警特報\|official warning`（不分大小寫）沒有任何符合 | 符合 |
| CL-B1-8 | 本節 E-1 與 K-1～K-6 | 符合 |

**檢查本身會不會漏抓（mutation，self-verification）。** 以暫存腳本逐一停用 `validate.py` 中新增的 13 項檢查（每次改一處、只跑 `tests/test_contracts.py`、結束後還原，並以 `cmp` 確認與原檔逐位元相同），每一項都至少有一個測試失敗：

```text
M1 short>stopped off: 2 failed, 160 passed in 0.32s
M2 fullmatch->match: 4 failed, 158 passed in 0.33s
M3 default 0.20 off: 4 failed, 158 passed in 0.33s
M4 multiple-of off: 3 failed, 159 passed in 0.32s
M5 inv4 off: 2 failed, 160 passed in 0.32s
M6 inv9 off: 4 failed, 158 passed in 0.33s
M7 unknown stop_allow off: 2 failed, 160 passed in 0.31s
M8 stop_allow ratio off: 4 failed, 158 passed in 0.32s
M9 step check off: 2 failed, 160 passed in 0.32s
M10 safe-typ diff off: 2 failed, 160 passed in 0.32s
M11 cumulative w/o allowance: 6 failed, 156 passed in 0.34s
M12 ok null stop_allow off: 1 failed, 161 passed in 0.30s
M13 missing-ratio fail-open: 1 failed, 161 passed in 0.32s
```

### E-3：合成資料

- 測試資料只有兩種來源，都是合成的：(1) `tests/fixtures/contract_v02/mock_dataset.json`（`_meta.mock = true`，數值、時間與座標都是虛構的；座標是既有的 10.0x／20.0x 模擬值，本次沒有新增或修改任何座標）；(2) `tests/test_ingest.py` 既有的合成幾何（`straight` 等，原點 10.0／20.0 的虛構直線）。本次沒有新增任何座標、軌跡或真實時間。
- Fixture 新增的值與其推導：`short_stop_time_s` 在 `stopped_time_s` 為 12 與 30 的兩列等於 `stopped_time_s`（沒有 180 秒以上的停留），其他列為 0；`stop_ratio` 依 DESIGN §5 的定義以 fixture 自己的可計時路段算出：C1 ＝ 0 ÷ 150 ＝ 0.0、C2 ＝ 12 ÷ 160 ＝ 0.075、C3 為 null（`speed_kmh` 為 null）；表頭 `margin_coeff = 0.2`、`margin_basis = default`（2 趟，計入的折數必然少於 8）；ETA 的 `stop_allow_s` 與 `eta_typ`／`eta_safe` 依 DESIGN §5 契約 4 的算式算出並取到整秒：`stop_allow_s` = 0、9、18、0；`eta_typ` = 07:03:00、07:05:09、07:19:27、07:25:27；`eta_safe` = 07:03:36、07:06:11、07:21:20、07:28:32（出發 07:00:00，R01-CP03 之後休息 600 秒）。
- Diff 中沒有真實座標、軌跡、騎乘時間或行程清單（`git diff ff04966 a304ee2` 人工檢視）。

### E-4：修改既有測試與 fixture 的逐項理由

| # | 位置 | 修改 | 理由 |
| --- | --- | --- | --- |
| 1 | `tests/test_ingest.py::test_rows_conform_to_the_contract_in_both_versions`（S-1） | 兩行 `validate_derived_segments(...) == []` 搬到新測試 `..._v03_contract`（strict xfail，restored by #9）；原測試保留其餘兩個斷言 | CL-B1-8 §3.1 第 1、3、4 項：`build_rows` 尚未輸出 `short_stop_time_s` |
| 2 | `tests/test_ingest.py::test_points_with_a_repeated_time_are_dropped`（S-2） | 最後一行搬到新測試（strict xfail，#9），連同它需要的準備步驟複製過去；原測試保留去除重複時間點的斷言與原有的準備步驟（`rows, _ = rows_of(pts)` 仍在，只是後面沒有斷言） | 同上。保留原測試的準備步驟，使原測試相對 BASE「只少了被搬走的斷言」（K-2） |
| 3 | `tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture`（S-3） | `validate_pace_table(...) == []` 搬到新測試（strict xfail，#10），新測試傳給 `build_pace_table` 的 `pace_version` 由 `"pace-mock-1"` 改為 `"user-01"`；原測試保留 `"pace-mock-1"` 與其餘兩個斷言 | CL-B1-8 §3.1 第 5 項：只改新測試中會被契約驗證的字面值，使剩下的失敗原因只有產生者的缺口 |
| 4 | `tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture`（S-4） | 列比對的斷言搬到新測試（strict xfail，#11）；原測試保留表頭比對 | `compute_eta` 尚未輸出 `stop_allow_s`，fixture 的列有它 |
| 5 | `tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace`（S-5） | 最後的 `validate_eta_output(...) == []` 搬到新測試（strict xfail，#11）；原測試保留三個斷言（含「`unknown` 時不輸出任何時間」，H-4）與原有的準備步驟 | 同上 |
| 6 | `tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks`（S-6） | 整個測試加 strict xfail（#11），不拆分 | CL-B1-8 §3.1 第 3 項：沒有其他斷言 |
| 7 | `tests/test_contracts.py::test_checkpoint_arrival_uses_row_c_minus_one` | R01-CP03／CP04／CP05 的預期時間改為 07:05:09／07:06:11、07:19:27／07:21:20、07:25:27／07:28:32；CP01、CP02 不變 | 預期值取自 fixture 的 ETA 列，fixture 依契約 4 v0.3 的算式加入了 `stop_allow_s`。被測行為（取 c − 1 那一列、不含該檢查點本身的休息）不變 |
| 8 | `tests/test_contracts.py::test_eta_must_follow_the_formula` | 第一個竄改值 `07:09:00` 改為 `07:09:27` | 註解寫「as if the break were not counted」；新 fixture 中不計休息的值是 07:19:27 − 600 秒 ＝ 07:09:27。新舊兩個值都違反，斷言與訊息不變；改值只是讓註解仍然精確 |
| 9 | `tests/test_contracts.py` 模組 docstring | 「v0.2」改為「v0.2 with the v0.3 stop-allowance fields of contracts 1, 3, 4」 | 正確描述被測的契約內容 |
| 10 | `tests/fixtures/contract_v02/mock_dataset.json` | 加入 `short_stop_time_s`、`stop_ratio`、`margin_coeff`、`margin_basis`、`stop_allow_s`；`pace_version` `pace-mock-1` → `user-01`（表頭、三筆類別、兩筆 ETA 表頭）；P-MOCK-1 的 `eta_typ`／`eta_safe` 重算；`_meta.note` 加一句 | Issue #7 範圍（新欄位必填；更新不符合新樣式的 `pace_version`）；值見 E-3；`user-` 的理由見 D-9；`_meta.contract_version` 不改，見 D-10 |

既有測試中行為受影響但沒有修改的：`test_too_few_segments_means_null_speed` 與 `test_enough_segments_means_a_speed` 改了 `speed_kmh` 之後，現在也會多出不變條件 4 的違反（`stop_ratio` 沒有跟著改）；兩者斷言的是特定訊息存在，仍然通過，不需修改。

### E-5：高風險類別的 self-verification

本節是 Executor 的 self-verification，**不是 audit**（治理 §2.3；高風險類別 record 第 5 節末段）。

**開始時與最終 diff 的判定。**

| 類別 | SPEC-B1 對 #7 的標示 | Executor 以最終 diff 重新判定 |
| --- | --- | --- |
| H-1 | 不涉及 | 不涉及：沒有碰憑證、環境變數、端點或付費呼叫（判定 3.1 第 1–7 項都不符合）。仍核對：diff 沒有金鑰字樣（`sk-ant\|api_key\|secret\|token` 無符合）、`git ls-files` 不含 `.env`、`*.key` |
| H-2 | 不涉及 | **無法確定，route 至 Design Authority（第 8 節 C-1）**：判定 3.2 第 2 項是「新增或修改……公開版衍生路段表的產生與欄位」，#7 在契約 1 的公開版 schema 新增了欄位 `short_stop_time_s`（欄位本身是 acceptor 核准的 v0.3 欄位，DESIGN §5 標示「公開版：有」）。依判定程序第 2、3 項，Executor 不記為「不涉及」 |
| H-3 | 涉及（判定 3.3 第 1 項） | 涉及（同） |
| H-4 | 涉及（判定程序第 2 項） | 涉及（契約 4 的 `unknown` 與不變條件 8 是 ETA 缺漏不補值的防線） |

**H-3（最低核對範圍，第 5 節）。**
- `research-`／`user-` 分離的機制：`pace_version` 只接受兩種開頭加兩位以上的 ASCII 數字，其他一律拒絕（AC4 的 21 個案例；mutation M2 會被抓到）。Fixture 用 `user-01`，不用 `research-`（D-9）。
- 凍結前沒有開啟保留行程的程式路徑：本次只改 `contracts`（純驗證，不開檔），沒有新增任何開啟檔案的程式；`ingest/`、`pace/` 沒有修改（K-5）。沒有讀 `data/`。
- 狀態陳述能對應到實際執行的 evidence：本 worklog 的每一項「通過」都附輸出；結果寫成 `193 passed, 6 xfailed`，沒有寫成「全數通過」；沒有任何數字被稱為 E1 Lite 或 E2 的結果；SPEC-B1 的 SB1-AC3 在 #9–#11 完成前不成立（E-1）。
- 版本宣稱：`CONTRACT_VERSION` 仍是 `"0.2"`，docstring 寫明只加入 v0.3 停等寬放、ID 規則與契約 2 未包含（CL-B1-2、D-10、D-11）。
- 用語：新增文字沒有 P90、百分位數、官方警特報（E-2 的 CL-B1-7 列）。

**H-4（最低核對範圍，第 5 節）。**
- `unknown` 時 `stop_allow_s` 必須是 null，0 也不接受（不以 0 補值）：`test_unknown_plan_must_not_carry_a_stop_allowance`（0.0、9.0）；M7 會被抓到。
- `ok` 時 `stop_allow_s` 缺漏（null）被拒絕：`test_ok_plan_needs_a_stop_allowance`；M12 會被抓到。
- 無法核對時不放行：配速表中路線所用類別沒有 `stop_ratio` 時回報違反（`test_stop_allow_needs_the_category_stop_ratio`；M13）；配速表表頭沒有 `margin_coeff` 時 ETA 的不變條件 9 回報違反（`test_eta_margin_against_a_pace_table_without_margin_is_rejected`）。
- 新欄位都是必填：缺 `short_stop_time_s`、`stop_ratio`、`margin_coeff`、`margin_basis`、`stop_allow_s` 都被拒絕（各自的 `..._required` 測試）；v0.3 欄位沒有做成可省略（CL-B1-8 §3.1 第 2 項）。
- 不以預設值掩蓋：`validate.py` 沒有為任何缺漏欄位補值；`h.get("margin_coeff", 0)` 是既有程式，只在 schema 已回報違反的情形下才會取到 0。
- 既有的不變條件 7（缺一個類別的配速時 ETA 必為 `unknown`）沒有修改，相關測試照常通過。
- 限制：沒有提供配速表時，不變條件 8 的 `stop_allow_s`＝`stop_ratio`×`typ_seg_time_s` 與不變條件 9 不檢查（D-5；AC7 的條件是「同時提供時」）。

**H-2 的 self-verification（未標示，但依 C-1 先做最低核對）。** `git ls-files` 不含 `.env`、`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/`；diff 與 fixture 的座標與時間都是合成的（E-3）；公開版新增的 `short_stop_time_s` 是秒數（路段內短停留的總長），不是日期或時刻，`test_public_rows_hold_no_date_time_or_coordinates` 仍然通過；公開版與私有版的欄位仍一致（`test_short_stop_time_is_required_in_both_versions`、`test_mock_fixture_conforms_to_every_contract`）。這一節不構成 H-2 的判定。

## 7. Audit status

- **Required**：Formal lane，每張 Ticket 都需要 independent audit（治理 §4.1；Bindings 第 5 節）；#7 涉及 H-3、H-4，audit record 須逐項寫明對所涉類別的核對（高風險類別 record 第 5 節）。依 run record 第 1 節第 4、5 項，R1 由 Codex（`gpt-6.1-sol`／`high`）執行，不兼作 Spec Integration Audit。
- **進度**：R1 與 R2 都已完成，record 與最後一行 verdict 見第 10 節。Executor 不派正式 audit，也不判定 closure。
- **高風險類別**：依 Design Authority 的判定為 H-2、H-3、H-4（`docs/governance/records/decisions/decision-20261117-issue7-h2.md`）。
- 第 6 節的 mutation 檢查與 self-verification 不是 audit。

## 8. Remaining work 與 concerns

| # | 項目 | 所需 authority／負責者 |
| --- | --- | --- |
| C-1 | **H-2 是否涉及。** #7 在契約 1 公開版的 schema 新增欄位 `short_stop_time_s`，符合 H-2 判定 3.2 第 2 項的字面（「公開版衍生路段表的……欄位」），但 SPEC-B1 對 #7 只標示 H-3、H-4。依高風險類別 record 第 4 節第 2、3 項，由 Design Authority 判定是否要補標 H-2；若補標，R1 須依第 5 節加做 H-2 的最低核對 | **已判定**：`decision-20261117-issue7-h2` 判定 #7 涉及 H-2（類別改為 H-2、H-3、H-4） |
| C-2 | Spike 的 `python -m moto_copilot.ingest` 在 #9 完成前會回報契約違反（`build_rows` 沒有 `short_stop_time_s`），exit code 1。這是 CL-B1-8 所述的產生者缺口，屬 #9；本 work item 沒有執行該指令（它會讀私有資料）：NOT RUN | #9 的 Executor |
| C-3 | 既有（v0.2）的 `validate_eta_output` 在某些 schema 不合法的輸入下會拋例外而不是回報違反，例如字串的 `typ_seg_time_s`、缺 `break_time_s` 的列、沒有時區的時間字串。本次新增的程式路徑已避開（D-8），既有路徑沒有修改（超出 #7 的 AC）。記為觀察，是否處理由之後的工作決定 | 無（記錄） |
| C-4 | `DESIGN.md` §5 寫「`src/moto_copilot/contracts/` 的驗證程式與契約測試仍然依 v0.2 檢查」，本 commit 之後對停等寬放的部分已不正確；依 SPEC-B1 §8，`DESIGN.md` 的實作狀態陳述由 AB-12 的文件工作處理，本 work item 沒有修改 `DESIGN.md` | AB-12 的文件工作 |
| C-5 | Fixture 目錄名稱 `contract_v02` 沒有改（不在 Issue #7 範圍；改名會動到 `conftest.py` 與 root `CLAUDE.md` 的指令）。 | 無（記錄） |
| R-1 | R1、correction、R2 都已完成（第 10 節）。剩下的是 Orchestrator 依 orch-default §7 判定 Ticket closure，以及第 10 節的 tracked follow-ups | Orchestrator |
| R-2 | 6 個 strict xfail 依 CL-B1-8 §3.2 在 #9（S-1、S-2）、#10（S-3）、#11（S-4～S-6）結案前移除並恢復檢查 | #9、#10、#11 |

Executor 工作的完成不等於 #7 的 closure（orch-default §7）、SPEC-B1 的 Spec Integration Audit 或 phase acceptance。

## 9. Correction — cycle 1（R1-F1）

| 欄位 | 內容 |
| --- | --- |
| 依據 | R1 audit record `docs/governance/records/audit/issue-7-c1-r1.md`（Codex，`primary_reviewer`，cycle 1，verdict BLOCKING；原樣 commit 於 `881fd7a`）的 blocking finding **R1-F1**「新增 numeric 欄位接受 NaN，繞過不變條件」與其 Required fix。Finding 原文不在此轉述或改寫，以該 record 為準 |
| 派工 | Orchestrator 以同一 worklog identity 續派同一 Executor（agentId `a9f372411c0f54099`）作 targeted correction |
| 修正 commit | **`8981e9d32d4fb2f1c13dd4909243b88114af06a2`**（`8981e9d`），父 commit `881fd7a`。只改 `src/moto_copilot/contracts/validate.py` 與 `tests/test_contracts.py` |
| Binding（自我觀測） | 同一 agent 至 worklog 更新前：(`claude-opus-5-5`, `high`) 153 則，集合只有一個元素；派工者仍須自行核對（第 2 節） |
| 範圍 | 只處理 R1-F1 的 Required fix：本票新增或修改的四個 numeric 欄位 `short_stop_time_s`、`stop_ratio`、`margin_coeff`（契約 3 表頭與契約 4 表頭）、`stop_allow_s`。沒有改 schema、fixture、`ingest/`、`pace/`、`routes/`、`conftest.py`、`pyproject.toml`；沒有新增或改動任何 xfail；沒有修改 R1 record |

### 9.1 對應 R1-F1 的修改

| # | 修改（`validate.py`） | 對應 Required fix 的哪一句 |
| --- | --- | --- |
| F-1 | 新增 `_non_finite_errors`：四個欄位的值是 NaN、+inf 或 −inf 時，回報 `<label>[<i>]: <field> is not a finite number (<value>)`。在 `validate_derived_segments`（`short_stop_time_s`）、`validate_pace_table`（表頭 `margin_coeff`、類別 `stop_ratio`）、`validate_eta_output`（表頭 `margin_coeff`、路段列 `stop_allow_s`）的 schema 檢查之後、不變條件之前執行 | 「在……不變條件運算前，明確將非有限值記為 violation」；涵蓋四個欄位；NaN／正負 infinity 都拒絕 |
| F-2 | 不變條件的運算只接受有限值：契約 1 不變條件 6 的 `short_stop_time_s`、契約 3 不變條件 6 的 `margin_coeff` 改用 `_is_finite_number`；ETA 迴圈遇到非有限的 `stop_allow_s` 停止算術（F-1 已回報），非有限的 ETA `margin_coeff` 不進入 `eta_safe` 的兩項算術（F-1 已回報） | 「僅讓 `_is_number` 回 False 後略過比較還不充分」：略過只發生在 F-1 已記為 violation 之後；`stop_allow_s` 不再拋 `ValueError` |
| F-3 | ETA 狀態 `ok` 時，路線所用類別在配速表中的 `stop_ratio` 不是有限值，回報 `stop_allow_s cannot be checked: category <c> has a non-finite stop_ratio (<value>) in the pace table (invariant 8)`。原本「沒有 `stop_ratio`」的訊息與測試不變 | 「無法核對停等比例的資料仍被判定為符合契約」：在只呼叫 `validate_eta_output` 的路徑也不放行 |

保留：合法的 0、nullable 欄位的 null、一秒容差、所有既有訊息與既有測試都不變。非有限值沒有被補成 0 或 null。

### 9.2 Decisions and assumptions（cycle 1）

| # | 決定 | 理由 |
| --- | --- | --- |
| D-12 | 非有限值以獨立的訊息回報，不併入 schema 錯誤 | JSON Schema 的 `minimum` 不拒絕 NaN、也不拒絕 +inf；以明確的檢查不依賴 jsonschema 的行為。−inf 會同時有 schema 的下限錯誤與本訊息，兩者都是違反，沒有衝突 |
| D-13 | 範圍只限 R1-F1 列出的四個欄位；既有欄位（`stopped_time_s`、`typ_seg_time_s`、`break_time_s`、`speed_kmh` 等）的非有限值處理不變 | R1-F1 Required fix 明寫「不要求順帶重寫其他既有畸形輸入處理」。見 9.5 C-6 |
| D-14 | ETA 的 `typ_seg_time_s` 仍以 `_is_number` 判斷，不改成「非有限即停止」 | 改成停止會把既有欄位的非有限值由「拋例外」變成「無聲放行」（fail open）。既有行為不在本次範圍，不擴大，也不讓它變差 |

沒有需要猜測語義之處：四個欄位在契約中都是 number（JSON 沒有 NaN／infinity），R1-F1 明定要拒絕的值與要保留的行為。

### 9.3 回歸測試（`tests/test_contracts.py`，新增 6 個測試函式、36 個案例，全部 PASSED）

| 測試 | 案例 | 涵蓋 |
| --- | --- | --- |
| `test_non_finite_values_in_the_v03_fields_are_rejected` | 18（6 個位置 × NaN／inf／−inf） | 經 `validate_dataset`（不拋例外）：契約 1 `short_stop_time_s`；契約 3 `stop_ratio`、表頭 `margin_coeff`；契約 4 表頭 `margin_coeff`、`ok` 列與 `unknown` 列的 `stop_allow_s`。R1 重現中的四個 false acceptance／例外都在內 |
| `test_non_finite_short_stops_are_rejected_on_their_own` | 3 | `validate_derived_segments` 單獨呼叫 |
| `test_non_finite_margin_is_rejected_by_the_pace_table_alone` | 6（`default`／`loo_rule` × 3） | R1 重現中的「pace alone」：`validate_pace_table` 單獨呼叫時 `default`／NaN 被拒絕 |
| `test_non_finite_stop_ratio_does_not_let_the_eta_pass` | 3 | 只呼叫 `validate_eta_output`（含配速表）時，非有限 `stop_ratio` 不讓 `stop_allow_s` 通過（AC5） |
| `test_non_finite_eta_values_give_violations_without_a_pace_table` | 3 | 沒有配速表時，非有限 `stop_allow_s` 與 ETA `margin_coeff` 回報違反、不拋例外 |
| `test_non_finite_literals_parsed_from_json_text_are_rejected` | 3（`NaN`、`Infinity`、`-Infinity`） | 由 JSON 文字經 `json.loads`（契約 CLI 使用的解析方式）進入時同樣被拒絕 |

逐案結果（`pytest -v tests/test_contracts.py -k non_finite`）：

```text
test_non_finite_values_in_the_v03_fields_are_rejected[derived-short_stop_time_s-derived_segments-derived_segments(public)[0]-nan] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[derived-short_stop_time_s-derived_segments-derived_segments(public)[0]-inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[derived-short_stop_time_s-derived_segments-derived_segments(public)[0]--inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[pace_category-stop_ratio-pace_table-pace_categories[1]-nan] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[pace_category-stop_ratio-pace_table-pace_categories[1]-inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[pace_category-stop_ratio-pace_table-pace_categories[1]--inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[pace_header-margin_coeff-pace_table-pace_header[0]-nan] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[pace_header-margin_coeff-pace_table-pace_header[0]-inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[pace_header-margin_coeff-pace_table-pace_header[0]--inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_header-margin_coeff-eta_output-eta_headers[0]-nan] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_header-margin_coeff-eta_output-eta_headers[0]-inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_header-margin_coeff-eta_output-eta_headers[0]--inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_ok_row-stop_allow_s-eta_output-eta_segments[1]-nan] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_ok_row-stop_allow_s-eta_output-eta_segments[1]-inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_ok_row-stop_allow_s-eta_output-eta_segments[1]--inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_unknown_row-stop_allow_s-eta_output-eta_segments[4]-nan] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_unknown_row-stop_allow_s-eta_output-eta_segments[4]-inf] PASSED
test_non_finite_values_in_the_v03_fields_are_rejected[eta_unknown_row-stop_allow_s-eta_output-eta_segments[4]--inf] PASSED
test_non_finite_short_stops_are_rejected_on_their_own[nan] PASSED
test_non_finite_short_stops_are_rejected_on_their_own[inf] PASSED
test_non_finite_short_stops_are_rejected_on_their_own[-inf] PASSED
test_non_finite_margin_is_rejected_by_the_pace_table_alone[default-nan] PASSED
test_non_finite_margin_is_rejected_by_the_pace_table_alone[default-inf] PASSED
test_non_finite_margin_is_rejected_by_the_pace_table_alone[default--inf] PASSED
test_non_finite_margin_is_rejected_by_the_pace_table_alone[loo_rule-nan] PASSED
test_non_finite_margin_is_rejected_by_the_pace_table_alone[loo_rule-inf] PASSED
test_non_finite_margin_is_rejected_by_the_pace_table_alone[loo_rule--inf] PASSED
test_non_finite_stop_ratio_does_not_let_the_eta_pass[nan] PASSED
test_non_finite_stop_ratio_does_not_let_the_eta_pass[inf] PASSED
test_non_finite_stop_ratio_does_not_let_the_eta_pass[-inf] PASSED
test_non_finite_eta_values_give_violations_without_a_pace_table[nan] PASSED
test_non_finite_eta_values_give_violations_without_a_pace_table[inf] PASSED
test_non_finite_eta_values_give_violations_without_a_pace_table[-inf] PASSED
test_non_finite_literals_parsed_from_json_text_are_rejected[NaN] PASSED
test_non_finite_literals_parsed_from_json_text_are_rejected[Infinity] PASSED
test_non_finite_literals_parsed_from_json_text_are_rejected[-Infinity] PASSED
```

**R1 record 的重現程式（原文照跑，`.venv/Scripts/python.exe -B -`）在 `8981e9d` 的輸出：** 四個欄位都回報違反，`stop_allow_s` 不再拋例外。

```text
short_stop_time_s {'derived_segments': ['derived_segments(public)[0]: short_stop_time_s is not a finite number (nan)'], 'route_catalog': [], 'pace_table': [], 'eta_output': []}
stop_ratio {'derived_segments': [], 'route_catalog': [], 'pace_table': ['pace_categories[1]: stop_ratio is not a finite number (nan)'], 'eta_output': ['eta_segments: P-MOCK-1 seg 1 stop_allow_s cannot be checked: category C2 has a non-finite stop_ratio (nan) in the pace table (invariant 8)', 'eta_segments: P-MOCK-1 seg 2 stop_allow_s cannot be checked: category C2 has a non-finite stop_ratio (nan) in the pace table (invariant 8)']}
margin_coeff {'derived_segments': [], 'route_catalog': [], 'pace_table': ['pace_header[0]: margin_coeff is not a finite number (nan)'], 'eta_output': ["eta_headers: P-MOCK-1 margin_coeff 0.2 differs from the pace table's nan (invariant 9)", "eta_headers: P-MOCK-2 margin_coeff 0.2 differs from the pace table's nan (invariant 9)"]}
pace alone ['pace_header[0]: margin_coeff is not a finite number (nan)']
stop_allow_s {'derived_segments': [], 'route_catalog': [], 'pace_table': [], 'eta_output': ['eta_segments[0]: stop_allow_s is not a finite number (nan)']}
```

**Mutation（self-verification）。** 以暫存腳本逐一還原修正的四個部分（每次一處，只跑 `-k non_finite`，結束後以 `cmp` 確認原檔逐位元相同），每一項都有回歸測試失敗：

```text
F1 explicit non-finite check off: 33 failed, 3 passed, 162 deselected in 0.49s
F2 margin arithmetic guard off: 6 failed, 30 passed, 162 deselected in 0.32s
F3 stop_allow arithmetic guard off: 6 failed, 30 passed, 162 deselected in 0.32s
F4 non-finite stop_ratio branch off: 6 failed, 30 passed, 162 deselected in 0.30s
```

### 9.4 E-1：CL-B1-8 的檢查（在 `8981e9d` 重跑，工作目錄乾淨）

**結果陳述：`229 passed, 6 xfailed`（依 `decision-20261117-issue7-spike-tests`）。** 不是「全數通過」。比 cycle 0 多的 36 個 passed 恰為 9.3 的回歸案例；xfail 仍是同樣 6 個（S-1～S-6）。

| CL-B1-8 §3.3 | 判定 |
| --- | --- |
| 1. exit code 0 | 成立（輸出 C1-1） |
| 2. 只有 `passed` 與 `xfailed` | 成立 |
| 3. `xfailed` 數＝標記數，各對應 S-1～S-6 | 成立（輸出 C1-2；K-1：`grep -rn "xfail\|skip" tests/` 仍是同樣 6 處 strict xfail，沒有 skip，`test_contracts.py` 沒有標記） |
| 4. `--runxfail` 只失敗那 6 個，且只涉及 v0.3 缺口 | 成立（輸出 C1-3）。輸出與 cycle 0 的輸出 3 除執行秒數外逐行相同（`diff`）；第 6 節輸出 4 的暫存腳本重跑結果與 cycle 0 逐行相同 |
| 5、6 | 本節與 9.1–9.3 |

K-5：`git diff --name-only ff04966 -- src/moto_copilot/ingest src/moto_copilot/pace src/moto_copilot/routes tests/conftest.py pyproject.toml` 沒有輸出。契約 CLI 對 fixture：四份契約都是 OK，exit 0。

**輸出 C1-1：`.venv/Scripts/python.exe -m pytest -q`**

```text
........................................................................ [ 30%]
........................................................................ [ 61%]
..........................................................x........x.... [ 91%]
.........x....x.xx.                                                      [100%]
229 passed, 6 xfailed in 0.47s
exit=0
```

**輸出 C1-2：`.venv/Scripts/python.exe -m pytest -q -rxX`**

```text
........................................................................ [ 30%]
........................................................................ [ 61%]
..........................................................x........x.... [ 91%]
.........x....x.xx.                                                      [100%]
=========================== short test summary info ===========================
XFAIL tests/test_ingest.py::test_rows_conform_to_the_contract_in_both_versions__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; build_rows does not write short_stop_time_s yet
XFAIL tests/test_ingest.py::test_points_with_a_repeated_time_are_dropped__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; build_rows does not write short_stop_time_s yet
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
229 passed, 6 xfailed in 0.49s
exit=0
```

**輸出 C1-3：`PYTHONUTF8=1 .venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py`**

```text
....F........F.............F....F.FF.                                    [100%]
================================== FAILURES ===================================
______ test_rows_conform_to_the_contract_in_both_versions__v03_contract _______

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; "
                                           "build_rows does not write short_stop_time_s yet")
    def test_rows_conform_to_the_contract_in_both_versions__v03_contract():
        private, _ = rows_of(straight(12_000))
        public = to_public(private)
>       assert validate_derived_segments(private, "private") == []
E       assert ['derived_seg...roperty', ...] == []
E         
E         Left contains 8 more items, first extra item: "derived_segments(private)[0] schema: (record): 'short_stop_time_s' is a required property"
E         Use -v to get more diff

tests\test_ingest.py:74: AssertionError
_________ test_points_with_a_repeated_time_are_dropped__v03_contract __________

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #9; "
                                           "build_rows does not write short_stop_time_s yet")
    def test_points_with_a_repeated_time_are_dropped__v03_contract():
        pts = straight(12_000)
        pts[200:200] = [TrackPoint(pts[200].lat, pts[200].lon, pts[199].time)] * 3
        rows, _ = rows_of(pts)
>       assert validate_derived_segments(rows, "private") == []
E       assert ['derived_seg...roperty', ...] == []
E         
E         Left contains 8 more items, first extra item: "derived_segments(private)[0] schema: (record): 'short_stop_time_s' is a required property"
E         Use -v to get more diff

tests\test_ingest.py:168: AssertionError
___________ test_pace_table_matches_the_mock_fixture__v03_contract ____________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; "
                                           "build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet")
    def test_pace_table_matches_the_mock_fixture__v03_contract(data):
        header, categories = build_pace_table(data["derived_segments"], ["T001", "T002"], pace_version="user-01",
                                              min_segments=2, built_at=NOW)
>       assert validate_pace_table(header, categories, data["derived_segments"]) == []
E       assert ['pace_header...red property'] == []
E         
E         Left contains 5 more items, first extra item: "pace_header[0] schema: (record): 'margin_coeff' is a required property"
E         Use -v to get more diff

tests\test_routes_pace_eta.py:122: AssertionError
_____________ test_eta_reproduces_the_mock_fixture__v03_contract ______________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

    @pytest.mark.xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; "
                                           "compute_eta does not write stop_allow_s yet")
    def test_eta_reproduces_the_mock_fixture__v03_contract(data):
        header, rows = eta_for(data, "R01", "P-MOCK-1", [{"after_checkpoint_id": "R01-CP03", "duration_s": 600.0}])
>       assert rows == [s for s in data["eta_segments"] if s["plan_id"] == "P-MOCK-1"]
E       AssertionError: assert [{'plan_id': ...: 600.0, ...}] == [{'plan_id': ...s': 0.0, ...}]
E         
E         At index 0 diff: {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'} != {'plan_id': 'P-MOCK-1', 'seg_index': 0, 'typ_seg_time_s': 180.0, 'stop_allow_s': 0.0, 'break_time_s': 0.0, 'eta_typ': '2026-11-21T07:03:00+08:00', 'eta_safe': '2026-11-21T07:03:36+08:00'}
E         Use -v to get more diff

tests\test_routes_pace_eta.py:163: AssertionError
________ test_eta_is_unknown_when_a_category_has_no_pace__v03_contract ________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

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

tests\test_routes_pace_eta.py:178: AssertionError
_________ test_eta_output_passes_the_contract_with_and_without_breaks _________

data = {'_meta': {'mock': True, 'contract_version': '0.2', 'note': 'MOCK FIXTURE. Every number, time and coordinate here is i...ngth_m': 13500.0, ...}, {'route_id': 'R02', 'name': '示範路線乙（模擬）', 'n_segments': 2, 'total_length_m': 5000.0, ...}], ...}

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

tests\test_routes_pace_eta.py:187: AssertionError
=========================== short test summary info ===========================
FAILED tests/test_ingest.py::test_rows_conform_to_the_contract_in_both_versions__v03_contract
FAILED tests/test_ingest.py::test_points_with_a_repeated_time_are_dropped__v03_contract
FAILED tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
6 failed, 31 passed in 0.23s
exit=1
```

**契約 CLI：`PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`**

```text
data contracts v0.2: tests\fixtures\contract_v02\mock_dataset.json
  derived_segments: OK
  route_catalog: OK
  pace_table: OK
  eta_output: OK
exit=0
```

### 9.5 E-4、E-5 與 concerns（cycle 1）

- **E-4**：沒有修改任何既有測試；只在 `test_contracts.py` 新增 `import json` 與 9.3 的 6 個測試函式。
- **E-3**：回歸測試只用 mock fixture 與字面的 NaN／infinity，沒有新增座標、時間或行程。
- **E-5（self-verification，不是 audit）**：H-4，缺漏與無法核對的路徑不再放行，非有限值不補值，例外改為回傳違反（9.1、9.3）。H-3，結果陳述照實寫出 xfail 數，mutation 與重現都附輸出。H-2（依 `decision-20261117-issue7-h2` 已補標），本次沒有修改 schema 的欄位清單、fixture 或公開版的產生；`git ls-files` 的私有資料樣式計數仍為 0。
- **C-6（記錄，不屬 R1-F1）**：本票沒有修改的既有欄位如果是非有限值，仍依 v0.2 的行為處理：`stopped_time_s` 等可能無聲通過，`typ_seg_time_s` 可能在 ETA 算術拋例外。R1-F1 明寫不要求處理這部分（D-13、D-14）。是否另開工作由有權角色決定。

## 10. 結案前的狀態（cycle 1 R2 之後）

本節依治理 §3.7 與 orch-default §7 P8，記錄 R2 之後、Ticket closure 判定之前的狀態。本節只引用紀錄，不判定 closure，也不改寫或摘要任何 finding 的判定。

### 10.1 Audit records

| Round | Record | Commit | 最後一行（原文） |
| --- | --- | --- | --- |
| Cycle 1 R1 | `docs/governance/records/audit/issue-7-c1-r1.md` | `881fd7a` | `Verdict: BLOCKING` |
| Cycle 1 R2（scoped closure review） | `docs/governance/records/audit/issue-7-c1-r2.md` | `6316108` | `Verdict: PASS` |

兩份 record 都由 Codex（`primary_reviewer`）撰寫，派工者原樣 commit。各 finding 的內容、severity、判定與 disposition 以 record 原文為準。Binding 的核對結果記在 run record `docs/governance/records/run/run-20261117-oc1-issue7.md` 第 5 節。

### 10.2 Subject

| 項目 | 內容 |
| --- | --- |
| Branch | `oc1-run1-contracts-v03`（本機；沒有 push、沒有 PR） |
| BASE | `ff049661f968adace4dd017cf560316e5684440d` |
| 實作的最後一個 commit | **`8981e9d32d4fb2f1c13dd4909243b88114af06a2`**（R1-F1 correction）。之前的實作 commit 是 `a304ee2ac0ec3d8468e446b089216f0cb000f72b` |
| 最終 subject | 本次 worklog 更新的 commit，也就是加入本節之後的 HEAD；其父 commit 是 `6316108`（R2 record）。`8981e9d` 之後的每個 commit 都只改 `docs/governance/records/**`（Bindings 第 7 節的 record-only paths） |
| 測試狀態 | `8981e9d` 的 E-1：`229 passed, 6 xfailed`（依 `decision-20261117-issue7-spike-tests`；輸出見第 9.4 節）。6 個 xfail 是 S-1～S-6，依 CL-B1-8 §3.2 由 #9、#10、#11 恢復 |

### 10.3 Tracked follow-ups

下列項目都**尚未經 acceptor 接受或授權**。本表只記錄追蹤與交接對象，不構成新的 work item、Outcome Contract 或執行授權。

| ID | 來源 | 內容（引用來源） | Owner | 狀態 |
| --- | --- | --- | --- | --- |
| R2-F1 | `issue-7-c1-r2.md` 的 R2-F1 | 依 R2 record 原文：**Disposition／owner**：作為 non-blocking follow-up 記於本 record，owner＝#7 Executor（由 Orchestrator 追蹤；若成為新的 work item，仍須適用接受與授權）。本輪不修改實作或測試。這不是對 blocking finding 的 deferral，也不替任何尚未通過的 gate 標 PASS。 | 依 R2 record：#7 Executor，由 Orchestrator 追蹤 | Open；尚未經 acceptor 接受或授權；本 worklog 沒有對它作任何修改 |
| C-2 | 本 worklog 第 8 節 C-2 | Spike 的 `python -m moto_copilot.ingest` 在 #9 完成前會回報契約違反（`build_rows` 沒有 `short_stop_time_s`）；未執行（NOT RUN） | #9 | Open；尚未經 acceptor 接受或授權 |
| C-4 | 本 worklog 第 8 節 C-4 | `DESIGN.md` §5「`contracts` 仍依 v0.2 檢查」的陳述對停等寬放部分已過時 | AB-12 的文件工作 | Open；尚未經 acceptor 接受或授權 |
| C-6 | 本 worklog 第 9.5 節 C-6 | 本票沒有修改的既有欄位（`stopped_time_s`、`typ_seg_time_s`、`break_time_s` 等）的非有限值仍依 v0.2 的行為處理 | 交給有權限的角色決定是否處理 | Open；尚未經 acceptor 接受或授權 |
| R-2 | 本 worklog 第 8 節 R-2 | 6 個 strict xfail 在 #9（S-1、S-2）、#10（S-3）、#11（S-4～S-6）結案前移除並恢復檢查（CL-B1-8 §3.2） | #9、#10、#11 | Open（SPEC-B1 已定的後續 Ticket 範圍） |

C-1（H-2 是否涉及）已由 `decision-20261117-issue7-h2.md` 判定；C-3 是第 8 節的記錄項，沒有 owner。

### 10.4 尚未成立的事

- #7 的 Ticket closure（orch-default §7）由 Orchestrator 判定；本 worklog 不宣告已結案。
- SPEC-B1 的 Spec Integration Audit、Design Authority 的 phase acceptance、SB1-AC3（沒有 xfail 的 pytest 全數通過）與 Bindings 第 5 節的 release gate 都沒有成立。
- 沒有執行 E1 Lite、E2 或任何真實 GPX 的檢查。
