# Decision record — #7 改契約後，以 Spike 產出驗契約的既有測試在 #9–#11 完成前的處理

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261117-issue7-spike-tests`（v1） |
| 日期 | 2026-11-17 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-issue7`（run record 第 5 節事件 1）。acceptor 指示原文：「#7 改契約後，test_ingest.py 與 test_routes_pace_eta.py 中以舊 Spike 產出驗契約的測試，在 #9–#11 完成前如何處理。」 |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-B1 v1（`derivation-spec-b1.md`）。本 record 是 SPEC-B1 的 clarification（治理 §5.3 第 2 類），編號 **CL-B1-8**，與 `derivation-spec-b1.md` 第 4 節的 CL-B1-1～CL-B1-7 並列引用 |
| Subject 基準 | branch `oc1-run1-contracts-v03`，BASE `ff049661f968adace4dd017cf560316e5684440d`。在 BASE 執行 `.venv/Scripts/python.exe -m pytest -q`：`100 passed`（本 record 撰寫時實際執行） |
| 依據的條文 | 治理 §1.2、§2.4、§3.6-A、§5.3；orch-default v2.2 §5、§7（P3）、§12；Bindings m3 第 2.4、5、7 節；`derivation-spec-b1.md` §4 CL-B1-1、CL-B1-2，§5 E-1～E-5，§6 SB1-AC3，§8；`decision-20261117-oc1-first-run-derivation.md` BD-3；`decision-20261117-high-risk-categories.md` §3.3、§3.4、§5 |
| 讀過的證據 | 上列各檔；Issue #7 內文（`gh issue view 7`，唯讀）；`docs/ticket/BATCH-1-scoped-tickets.md`；`DESIGN.md` §5 契約 1、3、4；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` 中提及既有測試與 fixture 的段落；`src/moto_copilot/contracts/schemas.py`、`validate.py`，`ingest/segments.py`（輸出欄位），`pace/table.py`；`tests/test_ingest.py`、`tests/test_routes_pace_eta.py`、`tests/conftest.py`、`tests/test_contracts.py`（測試清單）、`tests/fixtures/contract_v02/mock_dataset.json`；`pyproject.toml`。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下任何腳本 |

## 1. 問題

#7 只改 `contracts`（`schemas.py`、`validate.py`）與測試 fixture：契約 1 新增必填的 `short_stop_time_s`；契約 3 新增 `stop_ratio`、`margin_coeff`、`margin_basis` 與 `pace_version` 的樣式；契約 4 新增 `stop_allow_s` 與不變條件 8、9。產生這些資料的 Spike 程式（`ingest/segments.py` 的 `build_rows`、`pace/table.py` 的 `build_pace_table` 與 `compute_eta`）要到 #9、#10、#11 才改。所以 #7 完成後，以 Spike 的實際輸出呼叫契約驗證、或與更新後 fixture 逐欄比對的既有測試會失敗。這不是 #7 的缺陷，是 Ticket 的依賴順序造成的。

同時有兩項要求互相衝突：
- Issue #7 共通規則：「既有的測試在完成後都要通過；因為契約改版而必須修改的測試，在 PR 中列出修改的理由」（BD-3：理由改列在 worklog）；SPEC-B1 E-1：pytest「全數通過」。
- Issue #7 的範圍只有 `schemas.py`、`validate.py` 與 fixture，排除範圍寫明 `validate.py` 不重算配速。修改 Spike 產生者屬 #9–#11 的範圍。

要裁決的是：這些測試在 #7 怎麼處理、什麼時候恢復，以及 E-1「全數通過」在 #7 怎麼判定。

## 2. 預期受影響的測試（依程式靜態判讀，Executor 以實際執行核對）

判讀依據：`build_rows` 的輸出沒有 `short_stop_time_s`；`build_pace_table` 的表頭沒有 `margin_coeff`、`margin_basis`，類別紀錄沒有 `stop_ratio`；`compute_eta` 的路段列沒有 `stop_allow_s`。契約 2（`validate_route_catalog`）在 #7 不變。

| # | 測試 | 會失敗的斷言 | 其他斷言 | 恢復於 |
| --- | --- | --- | --- | --- |
| S-1 | `tests/test_ingest.py::test_rows_conform_to_the_contract_in_both_versions` | `validate_derived_segments(private, "private") == []`、`validate_derived_segments(public, "public") == []` | `validate_public_private_pair(...) == []`、公開版沒有 `start_time`：不受影響 | #9 |
| S-2 | `tests/test_ingest.py::test_points_with_a_repeated_time_are_dropped` | 最後一行 `validate_derived_segments(rows, "private") == []` | 去除重複時間點的斷言：不受影響 | #9 |
| S-3 | `tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture` | `validate_pace_table(header, categories, ...) == []` | 各類別的配速與路段數、`method`、`n_trips`：不受影響 | #10 |
| S-4 | `tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture` | `rows == [...]`（fixture 的路段列會有 `stop_allow_s`） | `header == data["eta_headers"][0]`：預期不受影響 | #11 |
| S-5 | `tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace` | 最後的 `validate_eta_output(...) == []` | `status == "unknown"`、原因含 C3、所有時間為 `None`：不受影響 | #11 |
| S-6 | `tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks` | 整個測試都是契約檢查 | 無 | #11 |

這兩個檔案中其他 26 個測試預期不受 #7 影響（路線的 10 個、`ingest` 的其他 12 個、`test_holdout_trip_is_refused`、`test_suspect_and_invalid_rows_do_not_change_the_pace`、`test_method_comparison_reports_both_medians`、`test_eta_needs_an_aware_departure_time`），**一律不得加標記**。

## 3. 裁決（CL-B1-8）

### 3.1 處理方式：只隔離「Spike 產出 v0.3 欄位缺口」的斷言，標為 strict xfail

1. **可以標記的條件（全部成立才可以）。** (a) 測試在第 2 節的 S-1～S-6 之內；(b) 該斷言失敗的**唯一**原因是 Spike 產生者的輸出缺少 v0.3 新增的欄位，或與 v0.3 fixture 的新增欄位比對不符；(c) #7 的範圍內無法讓它通過而不修改 Spike 產生者。
2. **不可以的做法。** 刪除測試；`pytest.mark.skip`／`skipif`；改寫斷言使它通過（例如在測試裡替 Spike 輸出補上欄位、放寬比對、改回 v0.2 的 schema）；讓 v0.3 的新欄位在 schema 中變成可省略；在 #7 修改 `ingest/`、`pace/`、`routes/` 的程式；修改 `pyproject.toml` 或 `conftest.py` 的全域設定來達成。
3. **拆分。** 原測試中不受影響的斷言（第 2 節「其他斷言」欄）留在原測試、原名、原文，必須照常通過。會失敗的斷言連同它需要的準備步驟，原文搬到一個新的測試函式，名稱是原名加 `__v03_contract`（例如 `test_rows_conform_to_the_contract_in_both_versions__v03_contract`），放在原測試之後。S-6 沒有其他斷言，不拆分，直接標記原測試。
   - 理由：S-2、S-3、S-5 的其他斷言分別守著去除重複點、保留行程以外的配速計算，以及 ETA 為 `unknown` 時不輸出任何時間（H-4，#7 本身也標示 H-4）。整個測試標成 xfail 會連這些斷言的回歸一起遮住，因為 xfail 不分失敗的原因。
4. **標記的寫法。** 每個新測試（與 S-6）只加一個 `@pytest.mark.xfail(strict=True, reason=...)`，`reason` 以 `"v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #<n>"` 開頭，`<n>` 是第 2 節「恢復於」欄的 Issue 編號。`strict=True` 必須寫在標記上：Spike 改好之後測試意外通過時會轉為失敗，強制移除標記。
5. **唯一允許的斷言內文字修改。** 搬到新測試中、傳給產生者並且其輸出會被契約驗證的 `pace_version` 字面值（S-3 的 `"pace-mock-1"`），改成符合 v0.3 樣式的值（與 fixture 改名後的值相同），使新測試剩下的失敗原因只有產生者的缺口。其他字面值、斷言與準備步驟逐字不變。留在原測試或不受影響測試中的 `pace_version` 字面值（例如 `"p"`）不改；若 Executor 仍改了，須在 E-4 列出理由。
6. **清單是封閉的。** 實際執行時：
   - S-1～S-6 中某個斷言實際沒有失敗 → 不標記、不拆分。
   - S-1～S-6 以外的任何測試失敗，或 S-1～S-6 中有斷言因第 1 項 (b) 以外的原因失敗（例如 #7 改了 `pace_eligible`、`expected_break_times`、`CATEGORIES` 等 Spike 會匯入的共用函式）→ **不得**依本 record 標記。屬 #7 範圍內者由 #7 修正；認為仍屬產生者缺口而本清單未列者，route 至 Design Authority（治理 §2.4），不自行擴大清單。
   - `tests/test_contracts.py` 是 #7 本身的範圍，不得有任何 xfail／skip 標記。

### 3.2 何時恢復

1. 第 2 節「恢復於」欄的 Ticket 是**最遲**的恢復點。該 Ticket 結案時，`reason` 指向它的標記必須全部移除：新測試不帶標記通過；或該 Ticket 依自己的 AC 改寫或取代它（例如 #10 改了 `build_pace_table` 的介面），並在該 Ticket worklog 的 E-4 逐項寫明原斷言的檢查改由哪個測試涵蓋。只移除標記而讓檢查消失不算恢復。
2. 較早的 Ticket 使某個新測試意外通過（strict xfail 轉為失敗）時，由那張 Ticket 移除該標記並在其 worklog 記錄。
3. 恢復時，`__v03_contract` 測試可以併回原測試，也可以保留為獨立測試；兩種都要在 worklog 寫明。
4. 本 record 對 #9、#10、#11 的上述結案條件，是 SPEC-B1 E-1（「全數通過」）在這三張 Ticket 的字面要求，不是新增的 AC。
5. **SPEC-B1 的 Spec 層級驗收**：SB1-AC3「全部測試通過」與 AB-13 的「pytest 全數通過」按字面判定——`tests/` 中不得留有任何 `reason` 含 `decision-20261117-issue7-spike-tests` 的標記，pytest 結果沒有 `xfailed`。這是 SPEC-B1 Spec Integration Audit 的核對項之一。

### 3.3 E-1「全數通過」在 #7 的判定

E-1 在 #7 依下列全部條件判定為滿足；任一不成立即不滿足：

1. `.venv/Scripts/python.exe -m pytest -q` 的 exit code 是 0。
2. 摘要行只出現 `passed` 與 `xfailed`；`failed`、`error`、`xpassed`、`skipped` 都是 0 或不出現。
3. `xfailed` 的數目等於帶本 record 標記的測試數，每一個都對應第 2 節的 S-1～S-6 之一（最多 6 個）。以 `.venv/Scripts/python.exe -m pytest -q -rxX` 的輸出列出每個 xfail 測試與其 `reason`。
4. 以 `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py` 證明被遮住的失敗就是缺口：失敗的測試恰好是那些 xfail 測試，且每一個的失敗訊息只涉及 v0.3 新增的項目（`short_stop_time_s`、`stop_ratio`、`margin_coeff`、`margin_basis`、`pace_version` 的樣式、`stop_allow_s`、契約 4 不變條件 8／9），或 S-4 的列比對中只差 `stop_allow_s` 與隨它改變的時間值。
5. 第 1、3、4 項的完整輸出記在 #7 worklog（E-1）。worklog 的結果陳述照實寫出數目，例如「`N passed, M xfailed`（依 `decision-20261117-issue7-spike-tests`）」，不得只寫「全數通過」或「100 passed」。這是 H-3 判定第 3 項的「通過」陳述，xfail 不得陳述為通過。
6. E-4：worklog 逐項列出被拆分或標記的測試、搬動的斷言、`pace_version` 字面值的修改（若有），理由引用本 record 與第 2 節的編號。

### 3.4 Executor 與 Reviewer 可以機械核對的項目

| # | 核對 | 方法 |
| --- | --- | --- |
| K-1 | 標記只出現在允許的位置 | `grep -n "xfail\|skip" tests/`：只出現在 `test_ingest.py`、`test_routes_pace_eta.py`，數目不超過 6，每一個都是 `xfail(strict=True, reason="v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #<n>"...)`，`<n>` 與第 2 節相符；沒有 `skip` |
| K-2 | 原測試的其他斷言未被刪改 | 對 BASE 的 `git diff -- tests/test_ingest.py tests/test_routes_pace_eta.py`：原測試只少了被搬走的斷言；新測試中的斷言與 BASE 的原文逐字相同（第 3.1 節第 5 項的 `pace_version` 字面值除外） |
| K-3 | 不受影響的測試未被動 | 第 2 節列的其他 26 個測試在 diff 中沒有變更（若有，E-4 有理由且不是標記） |
| K-4 | E-1 判定 | 第 3.3 節第 1–4 項的輸出 |
| K-5 | 產生者未在 #7 修改 | `git diff --stat <BASE>` 不含 `src/moto_copilot/ingest/`、`pace/`、`routes/` |
| K-6 | `test_contracts.py` 無標記 | K-1 的 grep 結果 |

## 4. 為什麼選這個做法

| 做法 | 不採用的理由 |
| --- | --- |
| 刪除這些測試 | 它們是 #9–#11 的產生者對 v0.3 契約的符合性檢查；刪除後恢復與否無從追蹤，E-4 也無法逐項交代 |
| `skip` | 產生者修好之後不會提醒恢復；skip 的測試會一直沉默 |
| 改寫斷言、在測試中補欄位、或讓新欄位可省略 | 測試會證明一件不成立的事（Spike 輸出符合 v0.3）；違反 Issue #7 的 AC 與 DESIGN §5 的「必填」；屬 H-3／H-4 不得以預設值掩蓋缺漏的範圍 |
| 在 #7 先讓 Spike 輸出新欄位（例如 `short_stop_time_s = 0`） | 超出 Issue #7 的範圍；而且 0 是補出來的值，不是停等事件的計算結果（DESIGN §5 共通規則的缺值規則、H-4） |
| 整個測試標 xfail，不拆分 | xfail 不分失敗原因，會遮住同一測試中守著 H-4（`unknown` 不輸出時間）與資料清理的斷言 |

本問題只有一個做法同時滿足：#7 的範圍、AC 與 DESIGN §5 的必填欄位不變；既有的檢查一項都不消失；恢復的時點與責任可機械追蹤。所以不構成 E-DA/D1。

## 5. 是否改變 accepted 語義

**否。**
- OC-1 的 accepted 語義（AB-13「pytest 全數通過」作為整合條件）在 SPEC-B1 的 Spec 層級按字面保留（第 3.2 節第 5 項）；本 record 沒有放寬它。
- E-1 與 Issue #7 的共通規則是 derived contract（Bindings 第 8.1 節；`decision-20261117-oc1-first-run-derivation.md` BD-3）。本 record 解決的是同一份 derived contract 內兩項要求在 #7 無法同時按字面成立的衝突，並把 Issue 自己預期的「因契約改版而必須修改的測試」具體化。屬治理 §5.3 第 2 類；依 orch-default §7 P3，gate 在某 Ticket 的適用方式只能源於這類 DA clarification，本 record 即是。
- 沒有新增或移除任何 AC、invariant 或 Must；沒有豁免任何 audit；沒有改變高風險類別的標示。
- 本 record **不解釋** Bindings 第 5 節 release gate（合併進 `main` 前的「pytest 全數通過」）。那是 acceptor 擁有的 Bindings；而且在 SPEC-B1 的 Spec Integration Audit 與 phase acceptance 之前，SPEC-B1 的任何中間狀態本來就不符合該 gate 的 Formal 條件。

## 6. Boundary determination

在 OC-1 boundary 內：修改的只有 `tests/` 的兩個既有測試檔（OC-1 §2.1 第 1 項 `tests/`、第 3 項 Spike 的收編），不動產品程式的範圍，也不碰私有資料（測試仍只用合成資料與 mock fixture）。不需要 acceptor。

## 7. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #7 B1-1 | 依第 3.1、3.3、3.4 節處理 S-1～S-6；E-1、E-4 依第 3.3 節記錄。R1 的 reviewer 以第 3.4 節核對 |
| #9 B1-2 | 結案時移除 S-1、S-2 的標記並恢復檢查（第 3.2 節）；其 E-1 不得有本 record 的 xfail |
| #10 B1-3 | 結案時移除 S-3 的標記並恢復檢查；其 E-1 同上 |
| #11 B1-4 | 結案時移除 S-4～S-6 的標記並恢復檢查；其 E-1 同上 |
| SPEC-B1 Spec Integration Audit | SB1-AC3 依第 3.2 節第 5 項按字面核對 |
| 既有 evidence | BASE 的 `100 passed` 是 v0.2 的結果，不作為 #7 的 E-1 證據 |

`derivation-spec-b1.md` 沒有被修改；SPEC-B1 v1 的引用集合由本 record 補上 CL-B1-8，Orchestrator 與 Reviewer 以本 record 路徑引用。

## 8. 需要其他 authority 的事項

無。本 record 不需要 acceptor，也不觸發 escalation。

本 record 只執行了 BASE 上的 `.venv/Scripts/python.exe -m pytest -q` 與 `--collect-only`（不需金鑰、不讀 GPX），以及唯讀的 `gh issue view 7`；沒有讀取 `data/` 或 `.env`，沒有執行 `experiments/` 下的任何腳本，沒有修改程式、測試、Spec、Issue 或其他 record，沒有派工任何 subagent，沒有 commit。
