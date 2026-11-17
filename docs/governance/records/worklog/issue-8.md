# Worklog — Issue #8（SPEC-B1 B1-5）規則 3 的範圍判定（確定性測試）

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #8（BATCH-1 B1-5），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **實作與 self-verification 完成，待 R1。** 本 worklog 不宣告 Ticket closure；closure 由 Orchestrator 依 orch-default §7 判定 |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `05e0a98890f1dc5a20bb0c02c54f3f2b0c2dece0`（`05e0a98`，派工時的 HEAD）；實作 commit **`47f1cdb89214d3eba6b4a3003c89f7021c5fabe1`**（`47f1cdb`，唯一修改 `src/`、`tests/` 的 commit）。本 worklog 在其後的 record-only commit |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：GitHub Issue #8 的內文與 5 項 AC。派工所附 scratchpad 原文檔 `issue-8-body.md` 實測 SHA-256 `061ad87fb3dff17ccbcbb75a433fd2f01c7ac8ff5c226aa65bd6af157d7418e4`；另以 `gh issue view 8 --json body,updatedAt`（唯讀）取得的 body，UTF-8 SHA-256 相同、位元組與原文檔相同（3103 bytes），等於 BD-3；`updatedAt` `2026-11-15T11:10:56Z`。沒有修改 Issue。
- **Spec**：SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）：§2 引用段落（SPEC-001 4.8 的 `in_rule3_range`、5.2 規則 3 各列的結果與條件、5.4「規則 3 的範圍」列；SPEC-RESOLUTION-001 §3.1、§3.5；G1 Q18）；§4 CL-B1-1、**CL-B1-6**、CL-B1-7；§5 #8 列（5 項 AC＋另加三項：單向行程終點剛好在 0.8 × T 的路段不在範圍內；來回行程 k 不合法時回報錯誤；模組不匯入 CL-B1-6 第 1 項列出的模組；高風險類別 H-4 判定 3.4 第 1 項，不涉及 H-3）；共通證據要求 E-1～E-5。
- **高風險類別**：`decision-20261117-high-risk-categories.md` §3.4、§5（H-4）。
- **其他引用**：`DESIGN.md` §9.1（`validator` 的位置與匯入限制）；契約 2 的 `ROUTE_SEGMENT`（`src/moto_copilot/contracts/schemas.py`：`length_m`、`cum_length_m` 都必須大於 0），作為 D-8-3 的依據。
- **Outcome Contract**：OC-1（`docs/governance/records/outcome-contract.md`）。
- 本 work item 執行中契約沒有變更。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-a9c66ffc5117ca116.{meta.json,jsonl}`；`meta.json` 的 `agentType` 是 `gov-executor`。
- Executor 自行觀測（實作 commit `47f1cdb` 之後、本 worklog 寫入前，以第 3.6 節的掃描方式）：agentId `a9c66ffc5117ca116`，(`claude-opus-5-5`, `high`) 81 則，集合只有一個元素。**這是自我觀測，不是派工者的核對**；Orchestrator 採用本 return 前須自行核對該 agent 的全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 `gov-executor` definition、Bindings m3、impl-default v2 §3–§5、§9、治理 §3.5、§3.7、§3.8；SPEC-B1（全文）；高風險類別 record §3.4、§4、§5；Issue #8（核對雜湊）；SPEC-RESOLUTION-001 §3（§3.1、§3.5）；SPEC-001 4.8、5.2（規則 3 各列與補充）、5.4；G1 Q18；`DESIGN.md` §9.1 的 `validator` 列；既有程式的風格（`pace/table.py`、`tests/test_eta.py`、`tests/conftest.py`、`pyproject.toml`）與契約 2 的 schema；worklog `issue-11.md` 的格式。
2. BASE `05e0a98` 上的 pytest：`462 passed`；`grep -rn "xfail\|skip" tests/` 沒有輸出。
3. 新增 `src/moto_copilot/validator/rule3.py`（CL-B1-6 第 1 項的位置：`validator/` 之下的一個模組；Issue 的「模組位置在這張票決定」）：
   - 公開函式 `judge_rule3(cumulative_m, trip_type, pop_classes, outbound_segments=None) -> Rule3Outcome`；`Rule3Outcome` 是 `NamedTuple(in_range: tuple[bool, ...], result: str)`，`result` 是 `PASS`／`FAIL`／`UNKNOWN`。不是 RuleResult，不帶原因代碼（Issue 排除範圍）。
   - 單向（`one_way`）：T＝最後一個累計距離；路段終點嚴格大於 0.8 × T 就在範圍內（以有理數精確比較，D-8-2）；k 不使用（D-8-4）。
   - 來回（`round_trip`）：`seg_index ≥ k` 在範圍內；k 必須是整數（不接受 `bool`）而且 0 < k < 路段數，否則 `ValueError`。
   - 結果：範圍內有 `HIGH_ALERT` → FAIL；否則範圍內有 `None` → UNKNOWN；否則 PASS。範圍外的路段不參與。
   - 輸入核對（H-4，D-8-3、D-8-5）：累計距離必須是有限數值（不接受 `bool`、字串、`None`）、第一個大於 0、嚴格遞增；分類必須是 `LOW`、`MEDIUM`、`HIGH_ALERT` 或 `None`，數量等於路段數；`trip_type` 必須是 `one_way` 或 `round_trip`。不符一律 `ValueError`，不產生結果。
   - 只匯入標準函式庫（`__future__`、`math`、`fractions`、`typing`）。
4. 新增 `src/moto_copilot/validator/__init__.py`：只匯出 `judge_rule3`、`Rule3Outcome` 與三個結果常數；說明寫明其他規則、原因代碼與 RuleResult 不在這裡。沒有建立其他規則的骨架（D-8-7）。
5. 新增 `tests/test_rule3.py`（93 個測試，全部合成資料；對應見第 6 節 E-2）。
6. Mutation 檢查（self-verification，第 6 節）：14 個變異全部被測試抓到。
7. 實作 commit `47f1cdb`；在乾淨的工作區執行 E-1（第 6 節）。

## 4. Decisions and assumptions

| ID | 決定 | 依據 |
| --- | --- | --- |
| D-8-1 | 模組 `src/moto_copilot/validator/rule3.py`，函式 `judge_rule3`，輸出 `Rule3Outcome`（同序的 `in_range` 與三值結果） | CL-B1-6 第 1、2 項；Issue「模組位置在這張票決定」。名稱避開 SPEC-001 的 `RuleResult`、`Evaluation`，以免被讀成那些 schema |
| D-8-2 | 單向行程的邊界以有理數精確比較：每個 `float` 先取 `repr()`（還原成同一個 `float` 的最短十進位）轉成 `Fraction`，再比較 `end > 4/5 × T` | CL-B1-6 第 3 項「嚴格大於」「剛好等於 0.8 × T 的路段沒有跨入」。直接用 `float` 計算 `0.8 * T` 會有二進位捨入：例如 T = 10 000.8、終點 8 000.64（＝0.8 × T）時 `0.8 * 10000.8` 是 `8000.639999999999`，終點會被誤判為跨入；以 `Fraction(value)`（二進位的精確值）則 T = 1.0、終點 0.8 會被誤判為跨入。`repr` 的十進位值才是呼叫者寫下的數值。這是 HOW，不改變定義；測試以這兩類值驗證（M2、M2b 變異） |
| D-8-3 | 累計距離必須第一個大於 0、嚴格遞增；零長度的路段是錯誤 | CL-B1-6 第 2 項「遞增」；契約 2 規定路段的 `length_m` 與 `cum_length_m` 都大於 0（`ROUTE_SEGMENT`），所以合法的路線目錄只會給出嚴格遞增的累計距離，沒有第二種合理解讀。不符時報錯（fail closed），不猜測零長度路段是否「跨入」 |
| D-8-4 | 單向行程完全忽略 `outbound_segments`，傳入任何值（含不合法的值）結果都相同 | CL-B1-6 第 3 項「k 不使用」 |
| D-8-5 | 不在 `LOW`／`MEDIUM`／`HIGH_ALERT`／`None` 之內的分類（例如 `"low"`、`"NONE"`、`""`、`70`、NaN）是錯誤，不當成 `LOW` 也不當成「沒有」 | CL-B1-6 第 2 項列出四種輸入；H-4 判定 3.4 第 1 項：不合法的輸入不得得到 PASS 或預設值 |
| D-8-6 | CL-B1-6 第 1 項的匯入限制以兩個測試驗證：(a) 靜態：以 `ast` 解析 `validator/__init__.py` 與 `validator/rule3.py`（`import moto_copilot.validator.rule3` 時載入的兩個檔案），相對匯入依 `moto_copilot.validator` 解析成絕對名稱；每個匯入必須是 `sys.stdlib_module_names` 的模組或 `moto_copilot.validator` 本身，不得是 `planner`、`sources`、`routing`、`routes`、`pace`、`anthropic`、`openai`，也不得有 `__import__`／`import_module` 的動態匯入；另以一個測試確認檢查器本身會抓到這些情形。(b) 執行期：在新的直譯器中 `import moto_copilot.validator.rule3`，比較匯入前後的 `sys.modules`，新增的模組只能是標準函式庫與 `moto_copilot`、`moto_copilot.validator`、`moto_copilot.validator.rule3`，並確認載入的檔案就是受測的原始碼 | SPEC-B1 §5 #8 列「以測試或靜態檢查驗證」；worklog 要記錄方式（派工內容） |
| D-8-7 | 「不建立其他規則的骨架」以檔案清單確認（`ls src/moto_copilot/validator` 只有 `__init__.py`、`rule3.py`），不寫成測試 | 寫成測試會使之後實作其他規則的 Ticket 必須修改本票的測試；這一項只約束本票的產物 |
| D-8-8 | 測試中的「最後 20%」另以獨立的寫法表示（路段 [起點, 終點] 與 (0.8 × T, T] 的重疊長度大於 0），並在 6 條合成路線上窮舉所有分類組合比較範圍與結果 | AC 4（SB9-T4）「結果和『最後 20%，跨入的路段也算』的定義相同」。這是測試內的對照寫法，**不是 E2 的 Oracle**（Issue 排除範圍：Oracle 必須獨立實作，不得引用本函式） |

沒有需要其他 authority 的假設。

## 5. Artifacts

| 檔案 | 變更 | commit |
| --- | --- | --- |
| `src/moto_copilot/validator/__init__.py` | 新增（9 行） | `47f1cdb` |
| `src/moto_copilot/validator/rule3.py` | 新增（134 行） | `47f1cdb` |
| `tests/test_rule3.py` | 新增（404 行，93 個測試） | `47f1cdb` |
| `docs/governance/records/worklog/issue-8.md` | 本 worklog | 其後的 record-only commit |

`git diff --stat 05e0a98 47f1cdb`：3 個檔案，547 行新增，0 行刪除。沒有修改任何既有檔案（`contracts/`、`ingest/`、`pace/`、`routes/`、fixture、`conftest.py`、`pyproject.toml`、`DESIGN.md`、任何 Issue 或其他 record）。

## 6. Verification

### E-1：在 `47f1cdb` 執行（主 checkout，`git status --short` 為空）

`git rev-parse HEAD` → `47f1cdb89214d3eba6b4a3003c89f7021c5fabe1`。

`.venv/Scripts/python.exe -m pytest -q`，exit code 0，完整輸出：

```text
........................................................................ [ 12%]
........................................................................ [ 25%]
........................................................................ [ 38%]
........................................................................ [ 51%]
........................................................................ [ 64%]
........................................................................ [ 77%]
........................................................................ [ 90%]
...................................................                      [100%]
555 passed in 2.04s
```

`.venv/Scripts/python.exe -m pytest -q -rxX`，exit code 0，完整輸出（沒有 XFAIL／XPASS 列）：

```text
........................................................................ [ 12%]
........................................................................ [ 25%]
........................................................................ [ 38%]
........................................................................ [ 51%]
........................................................................ [ 64%]
........................................................................ [ 77%]
........................................................................ [ 90%]
...................................................                      [100%]
555 passed in 2.07s
```

判定：摘要只有 `passed`；沒有 `xfailed`、`xpassed`、`failed`、`error`、`skipped`。`grep -rn "xfail\|skip" tests/` 沒有任何輸出（exit 1）。結果陳述：**`555 passed`，沒有 xfail、沒有 skip**。相對 BASE 的 `462 passed`：+93（`tests/test_rule3.py`）。

其他機器檢查（同一 subject）：
- `PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`：四項都是 `OK`，exit 0。
- `git ls-files` 對 `.env`、`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/` 沒有命中。
- 暫存內容對 `sk-ant`、`api_key=` 沒有命中（0）；暫存檔案只有第 5 節的三個。
- 執行期匯入的實測（`PYTHONPATH=src`，匯入前後 `sys.modules` 的差）：`__future__`、`_decimal`、`_typing`、`collections.abc`、`contextlib`、`decimal`、`fractions`、`math`、`moto_copilot`、`moto_copilot.validator`、`moto_copilot.validator.rule3`、`numbers`、`typing`、`typing.io`、`typing.re`、`warnings`：除 `moto_copilot*` 外全部是標準函式庫。

### E-2：AC 與測試的對應（全部 PASS，於 `47f1cdb`；測試都在 `tests/test_rule3.py`）

| AC／條件 | 測試 | 結果 |
| --- | --- | --- |
| AC 1：來回行程中只有去程有提醒時 PASS（SB9-T1） | `test_round_trip_with_an_alert_only_on_the_outbound_leg_passes`（去程 3 段全是 `HIGH_ALERT`，回程 `LOW`／`MEDIUM`；範圍與結果逐項比對）；`test_segments_outside_the_range_do_not_affect_the_result[round_trip-…]` 的窮舉也涵蓋 | PASS |
| AC 2：範圍內有提醒時 FAIL，即使範圍內另有路段缺降雨機率（SB9-T2） | `test_round_trip_alert_in_range_fails_even_with_missing_rain_probability[classes0..2]`；`test_one_way_alert_in_range_fails_even_with_missing_rain_probability[classes0..1]`（提醒與缺值的前後順序都測）；`test_three_valued_result_inside_the_range[classes6, classes7]` | PASS |
| AC 3：範圍內沒有提醒、有路段缺降雨機率時 UNKNOWN（只驗結果）（SB9-T3） | `test_no_alert_but_missing_rain_probability_in_range_is_unknown[…]`（來回與單向各 2 例，其中各 1 例在範圍外有 `HIGH_ALERT`）；`test_three_valued_result_inside_the_range[classes3, classes4]` | PASS |
| AC 4：單向行程的結果和「最後 20%，跨入的路段也算」的定義相同（SB9-T4） | `test_one_way_range_is_the_last_20_percent_with_crossing_segments[…]`（12 條人工算出範圍的路線：單一路段、跨入、恰在邊界、邊界外 1 m／0.01 m、長路段、非整數 0.8 × T、浮點邊界）；`test_one_way_results_equal_the_last_20_percent_definition_for_every_class_combination[ends0..5]`（6 條路線 × 所有分類組合，與獨立寫法的定義比較，D-8-8）；`test_one_way_ignores_the_outbound_count` | PASS |
| AC 5：範圍以外的路段缺降雨機率不影響結果（SB9-T5） | `test_segments_outside_the_range_do_not_affect_the_result[…]`（單向 1 條、來回 k=2 與 k=4；每組範圍內分類下，範圍外的所有分類組合——含缺值與提醒——結果都相同且等於只看範圍內的定義）；`test_missing_rain_probability_only_outside_the_range_still_passes` | PASS |
| 另加：單向行程終點剛好在 0.8 × T 的路段不在範圍內 | `test_one_way_range_is_the_last_20_percent_with_crossing_segments[segment 1 ends exactly at 0.8 x T = 8 000]`、`[0.8 x 10 000.8 = 8 000.64 exactly]`、`[0.8 x 0.29 = 0.232 exactly …]`（後兩例是 `float` 直接計算會誤判的值，D-8-2）；窮舉測試中的 `[1_000, 3_000, 7_999, 8_000, 8_001, 10_000]` | PASS |
| 另加：來回行程 k 不合法時回報錯誤 | `test_round_trip_with_an_invalid_outbound_count_is_an_error[0, 4, 5, -1, None, True, False, 1.0, 2.0, "2"]`（4 段路線）；`test_round_trip_with_one_segment_has_no_valid_outbound_count` | PASS |
| 另加：模組不匯入 CL-B1-6 第 1 項列出的模組（以測試或靜態檢查驗證） | 靜態：`test_rule3_module_imports_only_the_standard_library[__init__.py, rule3.py]`；檢查器自測：`test_the_import_checker_catches_forbidden_and_relative_imports`；執行期：`test_importing_rule3_loads_no_forbidden_or_third_party_module`（方式見 D-8-6） | PASS |
| CL-B1-6 第 4 項：來回行程的範圍是 `seg_index ≥ k`，與距離無關 | `test_round_trip_range_is_every_segment_from_k_on[…]`（6 組 n、k，均勻與不均勻的距離）；`test_round_trip_range_does_not_use_the_last_20_percent` | PASS |
| CL-B1-6 第 5 項：三值的順序（FAIL ＞ UNKNOWN ＞ PASS；`MEDIUM` 不是提醒） | `test_three_valued_result_inside_the_range[classes0..8]` | PASS |
| H-4：不合法的輸入是明確錯誤，不產生結果 | `test_invalid_cumulative_distances_are_an_error[…]`（13 例：空、0、負值、相等、遞減、NaN、無限大、`bool`、字串、`None`、非序列）；`test_invalid_rain_probability_classes_are_an_error[…]`（10 例：數量不符、未知字串、空字串、數值、NaN、非序列）；`test_unknown_trip_type_is_an_error[…]`（5 例）；單向與來回都測 | PASS |
| 純函式 | `test_inputs_are_not_modified_and_the_answer_is_repeatable`（不修改輸入、重複呼叫相同、`list` 與 `tuple` 輸入相同） | PASS |

**Mutation 檢查**（self-verification，不是 audit）：腳本 `C:/Users/yotsu/AppData/Local/Temp/claude/4fa6cbf1f948238d/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/scratchpad/mutate8.py` 逐一修改 `rule3.py`、跑全部 `tests/`、在 `finally` 還原（之後 `git status --short` 只剩本次新增的未追蹤檔案）。在實作 commit 之前的工作區執行：

| 變異 | 結果 |
| --- | --- |
| M1 邊界改為 `>=` | 7 failed |
| M2 以 `float` 計算 `0.8 * T` | 3 failed |
| M2b 以二進位精確值 `Fraction(value)` | 3 failed |
| M3 UNKNOWN 先於 FAIL | 10 failed |
| M4 來回行程改為 `seg_index > k` | 20 failed |
| M5 拿掉 k 的範圍核對（k = n 時範圍為空、得到 PASS） | 5 failed |
| M6 拿掉分類的核對 | 6 failed |
| M7 單向行程在有 k 時改用 k | 1 failed |
| M8 拿掉遞增的核對 | 4 failed |
| M9 結果看全部路段而不只範圍內 | 18 failed |
| M10 缺值當成 PASS | 15 failed |
| M11 不合法的 `trip_type` 當成單向 | 5 failed |
| M12 k 接受 `bool` | 1 failed |
| M13 最後 25% 而不是 20% | 7 failed |

### E-3：測試資料

全部是合成的：`tests/test_rule3.py` 的路線只有累計距離（整數公尺，如 2 000、8 000、10 000，以及為了浮點邊界而選的 10 000.8、8 000.64、0.29、0.232 等），沒有座標；降雨機率分類是手寫的 `LOW`／`MEDIUM`／`HIGH_ALERT`／`None`。沒有使用 fixture。diff 中沒有真實座標、軌跡、騎乘時間、預報或行程清單。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下任何腳本，沒有讀保留行程。

### E-4：修改的既有測試

沒有。本票只新增檔案；沒有因契約改版而修改的既有測試。

### E-5：高風險類別的 self-verification（`decision-20261117-high-risk-categories.md` 第 5 節）

- **H-4（判定 3.4 第 1 項：計算規則 3 結果的程式）**，依第 5 節的最低核對範圍「缺漏、失敗、逾時、超出涵蓋範圍的每條路徑都有測試顯示結果是 UNKNOWN 或明確錯誤，而不是 PASS 或預設值」：
  - 範圍內缺降雨機率（`None`，涵蓋上游的對不到鄉鎮、超出涵蓋區間、取不到預報、ETA 無法估計等原因，函式不區分）→ UNKNOWN（AC 3 的測試、M10）；同時有提醒 → FAIL，不被缺值降成 UNKNOWN（AC 2、M3）。
  - 不合法的分類、距離、`trip_type`、k → `ValueError`，沒有預設結果（H-4 列的測試、M6、M8、M11、M12）。
  - 範圍不會是空的：單向行程最後一段的終點是 T，必大於 0.8 × T；來回行程 k < n。所以 PASS 一定是範圍內至少一段都有分類而得到的，不會因範圍為空而成立（M5 證明 k 的核對有測試守著）。
  - 範圍外的路段（含去程的提醒與缺值）不影響結果（AC 5 的窮舉、M9）。規則 3 的 PASS 不代表去程沒有降雨，模組說明寫明；去程提醒的介面句子（SPEC-001 5.5）不在本票。
  - 「計畫狀態與規則結果不能被 Planner 改寫」「規則 5」「路線採用」：本票沒有這些程式，不適用。
- **H-3**：SPEC-B1 §5 #8 列判定不涉及（輸入是分類，不碰 70% 門檻）。另依 CL-B1-7 核對用語：`grep -i "p90\|percentile\|quantile\|百分位\|分位\|警特報\|official"` 對新增的三個檔案只有一處命中——`rule3.py` 說明中的「it is not an official weather warning」，是否定的陳述（與 Issue 內文同旨）。本 worklog 沒有把降雨機率 ≥ 70% 稱為官方警特報，也沒有把任何檢查稱為 E1 Lite 或 E2 的結果。
- **H-1、H-2**：不涉及（沒有憑證、付費呼叫、GPX 或位置資料；E-3）。

### 未執行的檢查

- 以真實路線與真實預報執行規則 3：**NOT RUN／NOT VERIFIED**（不在本票；真實資料受 RB-7 限制）。
- 規則 3 的原因代碼與其優先順序、RuleResult 與 WeatherSegment 的 schema、鄉鎮對應、預報讀取：Issue 排除範圍，沒有實作也沒有檢查，不得記為已涵蓋。
- E2 的 Oracle：Issue 排除範圍；本票的測試內對照寫法（D-8-8）不是 Oracle。
- SB1-AC4（規則 3 與 §3.1 判定表一致、與 `pace` 沒有匯入關係）：本票的測試提供證據，但 Spec 層級的判定屬 SPEC-B1 的 Spec Integration Audit。

## 7. Audit status

Formal：本 Ticket 的 independent audit（R1）**required**（治理 §4.1；Bindings 第 5 節），尚未派工；由 Orchestrator 依 Bindings 第 3.3、3.7 節派工。高風險類別 H-4（SPEC-B1 §5 #8 列）的最低核對範圍見高風險類別 record §5。本 worklog 的 self-verification（含 mutation 檢查）不是 audit。

## 8. Remaining work 與 concerns

| ID | 內容 | 性質 | Authority／owner |
| --- | --- | --- | --- |
| C-8-1 | 來回行程的 k（去程段數）由誰、依什麼規則算出（SPEC-001 7.11 第 2 項的折返點、路線在折返點切開），以及 `in_range` 怎麼寫進 WeatherSegment 的 `in_rule3_range`，都不在本票；本函式只接受呼叫者給的 k 並核對 0 < k < n | 已知範圍外，tracked | 之後的 `routes`／`validator` Spec（Design Authority；run record G-VAL） |
| C-8-2 | `src/moto_copilot/__init__.py` 的說明仍寫「Only the data-contract package exists so far」，在先前的 Tickets 之後已過時；本票沒有修改（不在範圍） | 資訊，範圍外 | AB-12 的文件工作（`derivation-spec-b1.md` §8） |
| C-8-3 | D-8-2 以 `repr()` 的十進位值作精確比較；呼叫者若以計算得來的 `float`（例如累加的浮點和）表示「剛好 0.8 × T」，其最短十進位可能不是預期的值，結果依該 `float` 的實際十進位而定。契約 2 的 `cum_length_m` 由同一 producer 寫出，本票不處理上游的捨入 | 資訊（不阻擋） | R1 reviewer；有疑義時 Design Authority |
| C-8-4 | `DESIGN.md` 的實作狀態陳述（`validator` 尚未實作）在本票之後部分過時 | 範圍外 | AB-12 的文件工作 |

剩餘工作：R1（Orchestrator 派工）；之後依 audit 結果做 targeted correction（若有）。沒有阻擋本 Ticket 的事項。
