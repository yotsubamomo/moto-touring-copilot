# Worklog — Issue #9（SPEC-B1 B1-2）`ingest`：停等事件與三種分類

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #9（BATCH-1 B1-2），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | Cycle 1：R1 BLOCKING（R1-F1）→ targeted correction `6f97561`（第 10 節），待 R2。Cycle 0：Executor 工作完成，回報 `DONE_WITH_CONCERNS`（第 8 節）。C-9-1、C-9-2 經 Design Authority 裁決（CL-B1-9、CL-B1-10），同一 worklog identity 續派完成 CL-B1-10 的測試與 CL-B1-9 的 E-1（第 9 節）。Ticket closure 由 Orchestrator 依 orch-default §7 判定，不由本 worklog 宣告 |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `0c109aa`（本 work item 開始時的 HEAD）；實作 commit **`a281cb0c07b522f6dad8ed078d085a37b2e59e7e`**（`a281cb0`）；CL-B1-10 的測試 commit **`b4d1f84eca1b4f80bd0265c81369384d62b055e0`**（`b4d1f84`，父 commit 是 DA record 的 `e165907`）。**R1 受審的程式與測試 subject 是 `b4d1f84`（R1 worktree HEAD `f0b5be9`）**；cycle 1 修正 commit **`6f975619a2e4b6303064955237c254de19f81da5`**（`6f97561`，第 10 節），是 R2 的程式與測試 subject；本 worklog 在其後的 record-only commit 更新（`docs/governance/records/**`，Bindings 第 7 節） |
| 日期 | 2026-11-17 |

## 1. Contract reference

- **Ticket**：GitHub Issue #9 的內文與 4 項 AC。以 `gh issue view 9 --json body,updatedAt` 唯讀取得：`updatedAt` `2026-11-15T11:10:58Z`，`body` 的 UTF-8 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895`，與 BD-3（`decision-20261117-oc1-first-run-derivation.md` §3）相同；Orchestrator 提供的 scratchpad 原文檔的 SHA-256 也相同。本 work item 沒有修改 Issue #9。
- **Spec**：SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）：§2 引用的段落；§4 CL-B1-1、**CL-B1-3**、CL-B1-7；§5 #9 列（Issue 的 4 項 AC＋CL-B1-3 第 4、5 項的三項測試；高風險類別 H-2、H-3、H-4）與 E-1～E-5。
- **CL-B1-8**：`docs/governance/records/decisions/decision-20261117-issue7-spike-tests.md`（第 3.2 節：#9 結案時 S-1、S-2 的 strict xfail 移除、原斷言不帶標記通過）。
- **CL-B1-9、CL-B1-10**：`docs/governance/records/decisions/decision-20261117-issue9-e1-and-trim.md`（DA 對 C-9-1、C-9-2 的裁決；E-1 在 #9 的判定方式，以及停等事件跨修剪邊界的處理與另加的驗證條件）。在本 work item 執行中加入 SPEC-B1 的引用集合。
- **其他引用**：`decision-20261117-high-risk-categories.md` 第 5 節（H-2、H-3、H-4 的核對範圍）；`docs/governance/records/worklog/issue-7.md` 第 8 節 C-2（acceptor 指定在 #9 處理）；Outcome Contract OC-1（`docs/governance/records/outcome-contract.md`，acceptor 2026-11-17 針對 `873e37a` 接受）。
- **規格來源**：`DESIGN.md` §5（資料處理流程、契約 1 的欄位與不變條件、「凍結之前不產生保留行程的列」）；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §1.1、§1.4、§1.6（SB2-T1、T2、T3、T11）。
- 契約在本 work item 執行中的變更：DA 以 CL-B1-9、CL-B1-10 補上 SPEC-B1 的 clarification（不改變 accepted 語義；CL-B1-10 第 6 項第 3 款為 #9 另加一項驗證條件）。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-a6f915a1860417bc9.{meta.json,jsonl}`。`meta.json` 的 `agentType` 是 `gov-executor`。
- Executor 自行觀測（實作 commit 之後、worklog 寫入前，以第 3.6 節的掃描方式）：agentId `a6f915a1860417bc9`，(`claude-opus-5-5`, `high`) 84 則，集合只有一個元素。**這是 Executor 的自我觀測，不是派工者的核對**；依第 3.6 節，Orchestrator 採用本 return 之前須自行核對該 agent 的全部 assistant 訊息。
- 續派後再觀測（CL-B1-10 測試 commit 之後、worklog 更新前）：同一 agentId，(`claude-opus-5-5`, `high`) 111 則，集合仍只有一個元素。同樣是自我觀測。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 `gov-executor` definition、Bindings m3、impl-default v2 §3–§5、§9、治理 §3.5、§3.7、§3.8、SPEC-B1、CL-B1-8、高風險類別 record 第 5 節、Issue #9（核對雜湊）、issue-7 worklog 第 8 節、`DESIGN.md` §5、SPEC-RESOLUTION-001 §1.1–§1.6。另依派工允許，唯讀閱讀 `experiments/cr01_checks/data_common.py` 的 `segment_stops` 與 `data_sb2_stop_allowance.py`（沒有執行）。在 BASE 跑 `pytest -q`：`229 passed, 6 xfailed`。
2. `src/moto_copilot/ingest/segments.py`：
   - `IngestParams` 新增 `false_stop_max_s = 3.0`、`long_stop_min_s = 180.0`；`ingest_version` 由 `ingest-spike-0.2` 改為 `ingest-b1-1`（CL-B1-3 第 6 項）。
   - 新增 `stop_kind`（整個事件的分類）與 `allocate_stop_events`（連續的停止步合成一個事件，依整個事件的長度分類，每一步的秒數計入該步所在的路段；CL-B1-3 第 2 項）。
   - `build_rows`：停止步的判定不變（CL-B1-3 第 1 項）。先切段並記錄每一步（路段、是否停止、秒數），短尾併入前一段時同時把其步對應到前一段，再分配停等事件：疑似 GPS 假停留的秒數加進 `moving_time_s`，不加 `length_m`（第 3 項）；`stopped_time_s` ＝ 短停留＋長停留；新增 `short_stop_time_s`。
   - `TripReport` 新增三種事件的次數（只有次數）。
3. `src/moto_copilot/ingest/__main__.py`（重建流程，CL-B1-3 第 4、5 項；C-2）：
   - 移除 `_load_or_create_manifest`：沒有行程清單時拒絕（exit code 2），不開啟任何 GPX，不建立清單。
   - 只開啟清單中 `trip_role == "pace"` 的項目；其他角色不開啟、不產生列。
   - 新增 `--trips`：指定的代號中有非 `pace` 或不在清單中的，在開啟任何檔案之前拒絕整個請求。
   - 新增 `--manifest`（預設 `<out>/trip_manifest.json`，與原行為的位置相同）；清單格式不合（非 JSON、沒有 `trips` 清單、項目缺 `trip_id`／`source_file`／`trip_role`、`trip_id` 重複）時拒絕。
   - 不再列舉 `--gpx-dir`；只開啟 `--gpx-dir / source_file`，`source_file` 不是單純檔名（含路徑）時不開啟並記入報告。
   - `main(argv=None)` 以便測試呼叫。
4. `tests/test_ingest.py`：依 CL-B1-8 §3.2 恢復 S-1、S-2（第 6 節 E-4）；新增 9 個停等事件的測試。
5. `tests/test_ingest_cli.py`（新檔）：重建流程的 10 個測試函式（14 個案例，含參數化），以 audit hook 觀測開啟的檔案。
6. C-2 的處置（第 4 節 D-9-6、第 6 節）。
7. 驗證（第 6 節）與 commit `a281cb0`（SA-1，topic branch，本機）。沒有 push、沒有開 PR。

## 4. Decisions and assumptions

以下都是 HOW 層級的選擇，沒有改變 Issue #9 的 AC、DESIGN §5 的 invariant 或任何 gate。

| # | 決定 | 理由 |
| --- | --- | --- |
| D-9-1 | 停等事件由修剪後軌跡的步組成；事件若跨過修剪邊界，只有修剪範圍內的步屬於該事件，分類依這部分的長度 | **由 CL-B1-10 取代為契約內容**（`decision-20261117-issue9-e1-and-trim.md` 第 6 項）：DA 寫定這是 measurement 語義，不是 Executor 的 HOW，並裁決為與本實作相同的讀法。實作沒有因此修改；依第 6 項第 3 款另加的測試見第 9 節。（原先的理由——流程順序、AC 3、唯讀閱讀的參考程式——保留作背景；DA 的裁決不依賴參考程式） |
| D-9-2 | 分類邊界：`duration < 3` 是假停留，`3 ≤ duration < 180` 是短停留，`≥ 180` 是長停留；兩個門檻是 `IngestParams` 的欄位 | Issue #9「長度小於 3 秒」「3 秒以上、不到 180 秒」「180 秒以上」；CL-B1-3 第 6 項 |
| D-9-3 | `stopped_time_s` 以「短停留＋長停留」計算，`short_stop_time_s` 是其中的短停留；兩者都在四捨五入到 0.1 之前由同一組數值算出 | 浮點加總順序不同可能讓 `short > stopped`；以加法構成保證 `short ≤ stopped`（不變條件 6），四捨五入是單調的 |
| D-9-4 | `ingest_version` 取 `ingest-b1-1` | CL-B1-3 第 6 項只要求不同於 `ingest-spike-0.2`；不用 `0.3` 字樣，避免看起來像宣稱契約 v0.3（CL-B1-2 的精神、H-3） |
| D-9-5 | 重建流程：指定代號不在清單中也拒絕；清單格式不合、`trip_id` 重複也拒絕；`source_file` 必須是單純檔名 | CL-B1-3 第 4 項只寫「非 `pace` 的角色」；不在清單中的代號無法確認角色，依 fail closed 拒絕（與 CL-B1-4 第 10 項對 `pace` 的處理一致）。`source_file` 的限制讓流程只開啟 `--gpx-dir` 內的檔案。這些只是更嚴格的拒絕，不放寬任何要求 |
| D-9-6 | C-2：重建流程現在輸出 `short_stop_time_s`，以合成資料執行時契約檢查全部 OK、exit code 0。只以合成資料驗證；以真實行程執行屬 Issue #9 排除範圍（「以真實的 GPX 重建衍生路段表（需要專題負責人另外同意）」），沒有執行 | 第 6 節；第 8 節 C-9-3 |
| D-9-7 | 跨路段的事件由 `allocate_stop_events` 的單元測試直接驗證 | 依距離切段時，路段只在移動步之後結束，所以 `build_rows` 實際上不會產生跨路段的事件（參考程式的說明也這麼寫）。CL-B1-3 第 2 項的規則仍以一般形式實作並測試，切段方式改變時仍成立 |
| D-9-8 | 停止步的判定、清理、修剪、切段、曲率與分級都沒有改；`moving_path`（`routes` 使用）沒有改 | Issue #9 排除曲率與分級；`moving_path` 只輸出幾何，假停留不改變幾何 |
| D-9-9 | S-1、S-2 恢復時併回原測試，內容回到 #7 之前（`9b3af99`）的原文 | CL-B1-8 §3.2 第 3 項允許併回；`git diff a304ee2~1 a281cb0 -- tests/test_ingest.py` 只有新增的測試（原測試逐字相同） |

## 5. Artifacts

| 檔案 | 變更 |
| --- | --- |
| `src/moto_copilot/ingest/segments.py` | 第 3 節第 2 項 |
| `src/moto_copilot/ingest/__main__.py` | 第 3 節第 3 項 |
| `tests/test_ingest.py` | S-1、S-2 恢復；新增 9 個測試（`a281cb0`），另加 CL-B1-10 的 1 個測試（`b4d1f84`，第 9.1 節） |
| `tests/test_ingest_cli.py` | 新增 |
| `docs/governance/records/worklog/issue-9.md` | 本檔（record-only commit） |

沒有修改 `contracts/`、`pace/`、`routes/`、`tests/test_contracts.py`、`tests/test_routes_pace_eta.py`、`tests/conftest.py`、fixture、`DESIGN.md`、`README.md` 或任何治理檔案（`git diff 0c109aa --stat` 對這些路徑沒有輸出）。

## 6. Verification

### E-1（中間結果，在 `a281cb0`；不是最終 E-1 證據，最終 E-1 見第 9 節）：`.venv/Scripts/python.exe -m pytest -q`

```text
........................................................................ [ 28%]
........................................................................ [ 56%]
........................................................................ [ 84%]
..............................x....x.xx.                                 [100%]
252 passed, 4 xfailed in 0.76s
```

Exit code 0。**結果是 `252 passed, 4 xfailed`，不是全數通過。** 4 個 xfailed 都是 CL-B1-8 的 strict xfail，`reason` 指向 #10（S-3）與 #11（S-4～S-6），不屬 #9 的恢復範圍；沒有 `xpassed`、`failed`、`error`、`skipped`。`-rxX` 的列表：

```text
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
```

`--runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py`：`4 failed, 53 passed`（**更正：這個計數是在加入 `test_a_stop_in_a_short_tail_goes_with_the_tail_into_the_previous_segment` 之前執行的結果，與 `a281cb0` 不對應；在 `a281cb0` 應為 `4 failed, 54 passed`，與 DA 在 `bb47d7b` 的觀測相同。本節是中間結果，最終 E-1 見第 9 節**）；失敗的恰好是上面 4 個，訊息只涉及配速表表頭與類別紀錄缺少的 v0.3 欄位（`margin_coeff` 等）、缺少 `stop_allow_s`，以及 S-4 列比對中缺少 `stop_allow_s` 及隨它改變的時間值（`eta_typ`／`eta_safe`；R1-F2 更正，第 10 節），與 #7 記錄的缺口相同，本 work item 沒有改變它們。

BASE（`0c109aa`）是 `229 passed, 6 xfailed`；差異：S-1、S-2 由 xfail 改為通過並併回原測試（235 → 233 個測試），新增 23 個案例（9＋14），233＋23 ＝ 256 ＝ 252＋4。E-1 在 #9 如何判定見第 8 節 C-9-1。

### E-2：AC 與測試的對應（全部 PASS，於 `a281cb0`）

| AC | 測試 |
| --- | --- |
| Issue AC 1／SB2-T1：兩步都快於 20 km/h、中間夾 1 秒的重複位置 → 沒有停留，1 秒在 `moving_time_s` | `test_ingest.py::test_sb2_t1_one_second_repeated_position_between_fast_steps_is_moving_time`（另斷言 `length_m` 不變、事件記為假停留、契約 1 無違反） |
| Issue AC 2／SB2-T2：2、3、179、180 秒的停留 | `test_ingest.py::test_sb2_t2_stops_of_2_3_179_and_180_seconds_are_classified_by_length`（2 秒只增加某一段的 `moving_time_s` 2 秒、長度不變；(stopped, short) 為 (3,3)、(179,179)、(180,0)） |
| Issue AC 3／SB2-T3：每段 `short_stop_time_s ≤ stopped_time_s`；移動＋停留＝修剪後總歷時 | `test_ingest.py::test_sb2_t3_short_stops_never_exceed_stops_and_times_add_up_to_the_trimmed_duration`（含假停留、短與長停留、站立時的記錄中斷、行進中的記錄中斷、GPS 跳點）；另見 `test_a_recording_gap_that_moved_50_m_or_more_is_moving_time_not_a_stop`、`test_a_stop_in_a_short_tail_goes_with_the_tail_into_the_previous_segment` 的總和斷言 |
| Issue AC 4／SB2-T11：重建流程遇到保留行程的代號時拒絕，不開啟檔案 | `test_ingest_cli.py::test_a_requested_holdout_trip_is_refused_before_any_file_is_opened`（exit 2；`--gpx-dir` 內沒有任何檔案被開啟；沒有寫出輸出） |
| SPEC-B1 另加（CL-B1-3 第 4 項）：清單中非 `pace` 的項目不開啟 | `test_ingest_cli.py::test_only_pace_entries_are_opened_and_the_result_passes_the_contract`（holdout 與 `excluded` 的檔案沒有被開啟、沒有列；被開啟的恰好是兩個 pace 檔）、`test_requested_pace_trips_are_the_only_ones_opened` |
| SPEC-B1 另加（CL-B1-3 第 4 項）：指定代號含非 `pace` 時拒絕 | `test_a_requested_holdout_trip_is_refused_before_any_file_is_opened`、`test_a_requested_excluded_trip_is_refused_before_any_file_is_opened`；不在清單的代號：`test_a_requested_trip_missing_from_the_manifest_is_refused` |
| SPEC-B1 另加（CL-B1-3 第 5 項）：沒有清單時拒絕 | `test_ingest_cli.py::test_without_a_manifest_the_rebuild_is_refused_and_none_is_created`（exit 2；沒有 GPX 被開啟；沒有建立清單；輸出資料夾仍是空的） |
| CL-B1-3 第 1 項：記錄中斷 >10 s 且位移 ≥50 m 仍是移動 | `test_a_recording_gap_that_moved_50_m_or_more_is_moving_time_not_a_stop`；站立時的中斷與相鄰停止步合成一個事件：`test_a_standing_recording_gap_joins_the_neighbouring_stopped_steps_into_one_event` |
| CL-B1-3 第 2 項：事件跨路段依整個事件分類、秒數分給各段 | `test_an_event_across_a_segment_boundary_is_classified_once_and_split_by_time`（D-9-7）；短尾併入：`test_a_stop_in_a_short_tail_goes_with_the_tail_into_the_previous_segment` |
| CL-B1-3 第 3 項：假停留計入該段 `moving_time_s`，不加 `length_m` | AC 1、AC 2 的測試 |
| CL-B1-3 第 6 項：新 `ingest_version`；3 秒、180 秒是參數 | `test_the_ingest_version_is_new`、`test_stop_thresholds_are_ingest_parameters` |
| 其他失敗路徑 | `test_a_malformed_manifest_is_refused_before_any_gpx_is_opened`（5 種）、`test_a_source_file_outside_the_gpx_folder_is_not_opened`、`test_an_explicit_manifest_path_is_used`、`test_select_pace_trips_and_load_manifest_directly` |

「沒有開啟」的觀測：`tests/test_ingest_cli.py` 以 `sys.addaudithook` 記錄 `open` 事件的路徑，不論由哪個函式開啟都會被記錄。正向測試斷言被開啟的恰好是兩個 pace 檔，證明觀測本身有效；另外 holdout 與 excluded 的檔案內容不是 GPX，若被讀取也會失敗。

**Mutation check（self-verification，修改後已還原，未 commit）**：把清單篩選改為全部開啟 → CLI 測試 3 個失敗；拿掉非 `pace` 指定代號的拒絕 → 3 個失敗；假停留不加進移動時間 → 3 個失敗；改為依單步而不是整個事件分類 → 5 個失敗；180 秒改算短停留 → 2 個失敗；拿掉短尾併入時的對應 → 1 個失敗。

### C-2：以合成資料執行 `python -m moto_copilot.ingest`

在 scratchpad 暫存目錄（版控外）建立兩個合成 GPX（虛構原點的直線，1 秒一點）、一個內容不是 GPX 的 holdout 檔與一份合成清單（T901、T904 為 `pace`，T902 為 `holdout`），執行 `PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.ingest --gpx-dir <tmp>/gpx --out <tmp>/out`：

```text
ingest ingest-b1-1 | curv-spike0-80-250 | pace trips: 2 | non-pace entries not opened: 1 | rows: 13
...（兩趟合成行程各一行計數）
contract check (private): OK
contract check (public): OK
contract check (pair): OK
exit=0
```

同一資料加 `--trips T901 T902`：`refused: requested trip(s) are not pace trips ...: T902`，exit 2。沒有清單的輸出資料夾：`refused: no trip manifest at ...`，exit 2，資料夾仍是空的。以真實行程執行：**NOT RUN**（第 8 節 C-9-3）。

### E-3：測試資料

全部合成：`tests/test_ingest.py` 沿用既有的虛構原點（緯度 10、經度 20）與 2026-01-01 UTC 的虛構時間產生直線、圓與停留；`tests/test_ingest_cli.py` 以同一原點產生 GPX 文字，寫在 pytest 的暫存目錄；行程代號用 T901～T905，檔名是虛構的。diff 中沒有真實座標、軌跡、騎乘時間或行程清單（`git diff 0c109aa` 與新檔中沒有台灣範圍的經緯度字面值；檢查方式：以 `\b(2[1-6]|1(19|2[0-2]))\.[0-9]{3,}` 搜尋，沒有結果）。本 work item 沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下任何腳本。

### E-4：修改的既有測試

| 測試 | 修改 | 理由 |
| --- | --- | --- |
| `test_rows_conform_to_the_contract_in_both_versions`（S-1） | 把 #7 時搬到 `test_rows_conform_to_the_contract_in_both_versions__v03_contract`（strict xfail，`restored by #9`）的兩個契約斷言併回原測試，刪除該 xfail 測試；斷言原文不變 | CL-B1-8 §3.2 第 1、3 項：產生者已輸出 `short_stop_time_s`，原斷言不帶標記通過 |
| `test_points_with_a_repeated_time_are_dropped`（S-2） | 同上，併回 `validate_derived_segments(rows, "private") == []`，刪除 `__v03_contract` 測試 | 同上 |

恢復後兩個測試與 #7 之前（`a304ee2~1`）的原文逐字相同（`git diff a304ee2~1 a281cb0 -- tests/test_ingest.py` 只有檔尾新增的測試）。原斷言的檢查沒有消失，也沒有改寫。其他既有測試沒有修改：`test_a_stop_counts_as_stopped_time_not_moving_time`（120 秒，短停留）與 `test_a_recording_gap_while_standing_is_a_stop`（300 秒，長停留）在新定義下照原斷言通過。S-3～S-6 沒有動，也沒有被本 work item 轉為 xpass。

### E-5：高風險類別的 self-verification（`decision-20261117-high-risk-categories.md` 第 5 節）

- **H-2**：`git ls-files` 不含 `.env`、`*.gpx`、`*.fit`、`data/`（檢查結果沒有輸出）；commit 前確認暫存的只有四個程式與測試檔。fixture 與測試的座標、時間都是合成的（E-3）。重建流程寫出的私有輸出位置沒有改變（仍是呼叫者指定的 `--out`）；印出與報告只含次數與行程代號，不含座標或時間戳。新的流程只開啟 `--gpx-dir` 內、清單中 `pace` 項目的檔案（`source_file` 必須是單純檔名）。**（R1-F1 推翻了這項主張在 `a281cb0`／`b4d1f84` 的完整性：同一來源檔同時被列為 `pace` 與非 `pace` 時，該檔仍會以 `pace` 項目開啟。修正與重驗見第 10 節。）**沒有送往第三方的內容。以真實資料核對的項目：NOT VERIFIED（C-9-3）。
- **H-3**：凍結前開啟保留行程的程式路徑：`ingest/__main__.py` 只開啟 `pace` 項目；指定非 `pace` 代號、沒有清單、清單不合格時都在開啟任何檔案之前拒絕（**R1-F1：在 `a281cb0`／`b4d1f84`，同一來源檔的角色矛盾沒有被拒絕，「凍結前不開啟保留行程」的主張不完整；修正與重驗見第 10 節**）；自動建立「全部暫定為 `pace`」的清單的路徑已移除（有測試）。`build_rows` 本身不讀檔，它的 `trip_role` 參數由呼叫者提供，重建流程一律傳 `pace`。沒有任何結果寫成 E1 Lite 或 E2；新增文字沒有 P90、百分位數或官方警特報的字樣（以 `P90|percentile|百分位|分位|警特報` 搜尋 diff 與新檔，沒有結果）。pytest 的結果照實寫成 `252 passed, 4 xfailed`。
- **H-4**：移動時間與 `quality` 的計算路徑：`moving_time_s` 只在 `quality` 為 `invalid` 時是 `null`（沿用既有規則，不補 0）；契約 1 的不變條件 3、6 由 `validate_derived_segments` 在每個新測試與 CLI 測試中檢查，沒有違反；每一步只計入移動或停留其中之一，總和等於修剪後的總歷時（AC 3 的測試）。重建流程的缺漏路徑（沒有清單、清單格式不合、代號不明、檔案不存在、`source_file` 不合格）都是明確的拒絕或報告中的註記，不是預設值或靜默略過。

### 未執行的檢查

- 以真實 GPX 或真實行程清單執行重建流程：NOT RUN（Issue #9 排除範圍；RB-7）。
- 回歸檢查（G-REG）：不在本 Spec（SPEC-B1 §2）。

## 7. Audit status

Formal：本 Ticket 的 independent audit **required**（治理 §4.1；Bindings 第 5 節），尚未開始。依 Bindings 第 3.7 節由 Orchestrator 派工；R1 須依高風險類別 record 第 5 節核對 H-2、H-3、H-4。本 worklog 的 self-verification 不是 audit。

## 8. Remaining work 與 concerns

| # | 項目 | 所需 authority／負責者 |
| --- | --- | --- |
| C-9-1 | **已裁決（CL-B1-9），處置見第 9 節。** 原提問：**E-1 在 #9 的判定。** SPEC-B1 E-1 要求 pytest「全數通過」；本 work item 結束時是 `252 passed, 4 xfailed`。剩下的 4 個是 CL-B1-8 指向 #10、#11 的 strict xfail，依 CL-B1-8 §3.2 第 1 項，它們最遲在 #10、#11 恢復，#9 的範圍內無法讓它們通過（需要修改 `pace/`）。但 CL-B1-8 第 7 節 #9 列寫「其 E-1 不得有本 record 的 xfail」，字面上涵蓋全部 6 個，與第 3.2 節第 1、4 項（各 Ticket 只負責指向自己的標記）不一致；CL-B1-8 §3.3 的判定方式只寫了 #7。我依第 3.2 節的讀法處理（只移除 S-1、S-2），沒有自行解釋 E-1 在 #9 是否滿足 | Design Authority：已裁決 |
| C-9-2 | **已裁決（CL-B1-10），處置見第 9 節。** 原提問：停等事件跨過修剪邊界時的分類（D-9-1）。我依既有流程（先修剪、後分離）只以修剪範圍內的步組成事件。若 Reviewer 或 DA 認為應以修剪前的完整事件分類，需要另行裁決；那會改變修剪邊界附近事件的分類，但不影響 AC 1～4 的測試 | Design Authority：已裁決 |
| C-9-3 | **C-2 的處置。** issue-7 worklog C-2 所述的契約違反（`build_rows` 沒有 `short_stop_time_s`）在 `a281cb0` 已由產生者輸出該欄位解決，以合成資料執行 `python -m moto_copilot.ingest` 時契約檢查全部 OK、exit 0（第 6 節）。以真實行程執行時是否也沒有違反：**NOT VERIFIED**（需要讀取私有資料；Issue #9 排除範圍） | acceptor（是否授權以真實資料執行，RB-7） |
| C-9-4 | 介面變更：`python -m moto_copilot.ingest` 不再自動建立清單；沒有清單的使用者會被拒絕。現有的私有輸出資料夾若已有清單，行為只差在非 `pace` 項目不再開啟。`DESIGN.md` §10 與 `README.md` 沒有這個指令的說明，所以沒有文件要改；之後的文件工作（AB-12）若加入這個指令，需寫明要先有清單 | AB-12 的文件工作 |
| C-9-5 | 契約 1 的 `trip_role` enum 只有 `pace`、`holdout`；重建流程跳過的「被排除」行程在清單中的實際寫法不在 repo 內（版控外的清單），本 work item 沒有讀取。實作對任何非 `pace` 的值都不開啟，所以不依賴它的寫法 | 無（記錄） |
| R-9-1 | Independent audit（R1）與之後的 closure 判定 | Orchestrator |
| R-9-2 | S-3（#10）、S-4～S-6（#11）的恢復 | #10、#11 |

Executor 工作的完成不等於 #9 的 closure（orch-default §7）、SPEC-B1 的 Spec Integration Audit 或 phase acceptance。

## 9. 續派：CL-B1-9、CL-B1-10 的處置（同一 work item，cycle 0）

| 欄位 | 內容 |
| --- | --- |
| 依據 | Orchestrator 的續派訊息（同一 worklog identity）；`decision-20261117-issue9-e1-and-trim.md`（HEAD `e165907` 時已 commit）第 11 節 #9 列的 (a)(b)(c) |
| 新 commit | `b4d1f84eca1b4f80bd0265c81369384d62b055e0`：只改 `tests/test_ingest.py`（新增一個測試）。程式沒有修改 |
| 最終 subject | `b4d1f84`（程式與測試）；之後只有本 worklog 的 record-only commit |

### 9.1 CL-B1-10：修剪邊界落在停等事件中間

新增 `tests/test_ingest.py::test_a_stop_event_cut_by_the_trim_is_classified_by_its_part_inside_the_trimmed_track`（PASS）。合成軌跡（虛構原點）：以 20 m/s 行進 1940 m，接著停 200 秒，停的期間每秒向前漂移 0.5 m（1.8 km/h，仍是停止步），共漂移 100 m，使累計距離在停的期間越過 `trim_m` = 2000 m；之後再行進 10 km。測試先以 `clean_points`、`trim_ends` 確認修剪起點落在停留之中，且修剪前的完整事件（200 秒）≥ 180 秒、範圍內部分（實測 80 秒）在 3～180 秒之間，再斷言：

- 報告的事件是 1 個短停留、0 個長停留；
- 第一段的 `stopped_time_s` 與 `short_stop_time_s` 都等於範圍內部分的秒數，全趟的總和也是，修剪掉的 120 秒不出現在任何欄位；
- 移動加停留等於修剪後的總歷時；契約 1 的檢查沒有違反。

測的是前端（構造方式由 Executor 選擇，CL-B1-10 第 6 項第 3 款）。CL-B1-10 第 8 項 DA 閱讀的結論（`a281cb0` 的行為符合第 1、2 款）在測試中成立；實作沒有修改。

### 9.2 E-1：依 CL-B1-9 第 2 項，在最終 subject `b4d1f84` 執行

**(i) `.venv/Scripts/python.exe -m pytest -q`**（exit code 0）：

```text
........................................................................ [ 28%]
........................................................................ [ 56%]
........................................................................ [ 84%]
...............................x....x.xx.                                [100%]
253 passed, 4 xfailed in 0.78s
```

**(iii) `.venv/Scripts/python.exe -m pytest -q -rxX`**（exit code 0）：

```text
........................................................................ [ 28%]
........................................................................ [ 56%]
........................................................................ [ 84%]
...............................x....x.xx.                                [100%]
=========================== short test summary info ===========================
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
253 passed, 4 xfailed in 0.83s
```

K-1：`grep -rn "xfail\|skip" tests/` 只有 `tests/test_routes_pace_eta.py` 第 117（`restored by #10`）、159、173、182 行（`restored by #11`）的 4 個 CL-B1-8 標記；沒有 `restored by #9`，沒有其他 `xfail`／`skip`。

**(iv) `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py`**（exit code 1；`--collect-only` 為 59 個測試；以 `PYTHONIOENCODING=utf-8` 執行，使 mock fixture 的路線名稱正確顯示）：

```text
.................................................F....F.FF.              [100%]
================================== FAILURES ===================================
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
FAILED tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
4 failed, 55 passed in 0.49s
```

失敗的恰好是 (iii) 的 4 個 xfail 測試；訊息只涉及配速表表頭的 `margin_coeff`（必填）、ETA 路段列的 `stop_allow_s`（必填），以及 S-4 的列比對中缺少 `stop_allow_s` 及隨它改變的時間值（`eta_typ`／`eta_safe`；**R1-F2 更正**：原文「只差 `stop_allow_s`」不完整，pytest 摘要只顯示第一列，第 2 列起累計的時間值也不同），都在 CL-B1-8 §3.3 第 4 項列舉的 v0.3 項目之內。

**計數的核對與更正**：DA record 開頭觀測到 `bb47d7b`（＝`a281cb0` 的程式與測試）上是 `4 failed, 54 passed`，我在第 6 節記的是 `53 passed`。原因：我在加入短尾併入的測試之前執行並記下了那次輸出，之後又新增了該測試，沒有重跑該指令就寫進 worklog。`a281cb0` 的正確數字是 `54 passed`（58 個測試），與 DA 的觀測一致；最終 subject `b4d1f84` 多了 CL-B1-10 的測試，是 `4 failed, 55 passed`（59 個測試）。第 6 節已加註更正。

**(v) S-1、S-2 與 S-3～S-6**：S-1、S-2 依 CL-B1-8 §3.2 第 1、3 項恢復（第 6 節 E-4，原文逐字相同）。`git diff 0c109aa b4d1f84 --stat -- tests/test_routes_pace_eta.py tests/conftest.py tests/test_contracts.py pyproject.toml` 沒有輸出：S-3～S-6 的測試與標記沒有修改。

**判定所需的事實**（依 CL-B1-9 第 2 項逐款）：(i) exit code 0；(ii) 摘要行只有 `passed` 與 `xfailed`；(iii) 4 個 xfail 全部是 `restored by #10`／`#11`，對應 S-3～S-6，沒有 `restored by #9` 與其他標記；(iv) `--runxfail` 失敗的恰好是那 4 個，訊息只涉及 v0.3 項目；(v) 如上。**結果照實寫：`253 passed, 4 xfailed`（依 CL-B1-8、CL-B1-9）。** 這不是「全數通過」；E-1 是否滿足由 Reviewer 依 CL-B1-9 核對。

測試數：BASE `0c109aa` 是 235 個（`229 passed, 6 xfailed`）；S-1、S-2 併回後 233 個；新增 24 個案例（`test_ingest.py` 10 個、`test_ingest_cli.py` 14 個），233＋24 ＝ 257 ＝ 253＋4。

### 9.3 E-2 的增列

| 條件 | 測試 | 結果（`b4d1f84`） |
| --- | --- | --- |
| CL-B1-10 第 6 項第 3 款：修剪邊界落在停等事件中間，完整事件與範圍內部分的分類不同；範圍內依範圍內長度分類、範圍外秒數不出現、移動＋停留＝修剪後總歷時、契約 1 通過 | `tests/test_ingest.py::test_a_stop_event_cut_by_the_trim_is_classified_by_its_part_inside_the_trimmed_track` | PASS |

第 6 節 E-2 的其他列在 `b4d1f84` 仍全部 PASS（同一次 (i) 的執行）。

### 9.4 E-3、E-5 的增補

新測試的座標、時間都是合成的（同一虛構原點、2026-01-01 UTC 起算）；diff 沒有真實座標、軌跡或騎乘時間。H-4：新測試釘住了修剪邊界附近移動時間與停留分類的計算路徑。本次續派沒有讀取 `data/`、`.env`，沒有執行或讀取 `experiments/` 下的檔案，沒有派工任何 subagent。

### 9.5 C-9-1、C-9-2 的處置與剩餘工作

- C-9-1：依 CL-B1-9 處理；#9 只移除 S-1、S-2 的標記，E-1 依第 2 項的條件記錄（第 9.2 節）。不再是 open concern。
- C-9-2：CL-B1-10 寫定與 D-9-1 相同的讀法；依第 6 項第 3 款加入測試（第 9.1 節）。不再是 open concern。
- 仍 open：C-9-3（以真實行程執行重建流程，NOT VERIFIED，acceptor／RB-7）；C-9-4（AB-12 文件工作）；R-9-1（independent audit：R1 以 `b4d1f84` 為受審 subject，並依 CL-B1-9、CL-B1-10 核對）；R-9-2（S-3～S-6 由 #10、#11 恢復）。

## 10. Correction — cycle 1（R1-F1、R1-F2）

| 欄位 | 內容 |
| --- | --- |
| 依據 | R1 audit record `docs/governance/records/audit/issue-9-c1-r1.md`（Codex，`primary_reviewer`，cycle 1，verdict BLOCKING；HEAD `3ddbe9f` 時已 commit）的 blocking finding **R1-F1** 與 non-blocking **R1-F2**。Finding 原文以該 record 為準，此處不轉述或改寫 |
| 派工 | Orchestrator 以同一 worklog identity 續派同一 Executor（agentId `a6f915a1860417bc9`）作 targeted correction（治理 §4.4） |
| 修正 commit | **`6f975619a2e4b6303064955237c254de19f81da5`**（`6f97561`），父 commit `3ddbe9f`。只改 `src/moto_copilot/ingest/__main__.py` 與 `tests/test_ingest_cli.py` |
| R2 的 subject | `6f97561`（程式與測試）；之後只有本 worklog 的 record-only commit |

### 10.1 R1-F1 的修正

- **做法**：`load_manifest` 在檢查完各項目的欄位與 `trip_id` 不重複之後，呼叫 `_refuse_conflicting_roles`：若任一來源檔同時被某個 `pace` 項目與某個非 `pace` 項目引用，整份清單拒絕（`ManifestError`，exit 2）。這發生在選擇行程與開啟任何 GPX 之前，所以自動選擇與 `--trips` 明確指定都被攔住。錯誤訊息只列出行程代號（例如 `T901 (pace) and T902`），不列檔名。
- **檔名等價**（`source_key`）：只取最後一個路徑成分（`/` 與 `\` 都視為分隔符），並忽略大小寫（`casefold`）、Unicode 正規化形式（NFC）與結尾的句點與空白（Windows 不區分這些）。比較只用清單中的字串，不讀取、不 stat、不雜湊任何非 `pace` 的檔案。鍵相同就視為同一檔，寧可多拒絕。
- **沒有改變的事**：兩個非 `pace` 項目共用一個檔、兩個 `pace` 項目各自的檔，不構成衝突（有測試）。沒有新增清單欄位，沒有實作內容去重複（Issue #9 排除範圍）。
- **契約語義**：這是 CL-B1-3 第 4 項「非 `pace` 的項目不開啟」在清單內部矛盾時的 fail-closed 執行方式，只增加拒絕，不改變任何欄位、角色或分類的定義；我判斷不需要 Design Authority 補定。若 R2 認為「整份清單拒絕」超出 CL-B1-3（例如應只略過衝突的項目），屬 Design Authority。
- **已知的殘餘（記錄，不是本 finding 的要求）**：以名稱比較無法辨識指向同一檔案的不同名稱，例如符號連結、硬連結或 Windows 8.3 短檔名；也無法辨識內容相同、檔名不同的兩個檔（內容去重複屬 Issue #9 排除範圍，DESIGN §5 第 5 步）。偵測這些需要 stat 或讀取非 `pace` 的檔案，R1-F1 的 required fix 也明示不要求。

**Regression tests**（`tests/test_ingest_cli.py`，合成資料，全部 PASS）：

| 測試 | 內容 |
| --- | --- |
| `test_a_source_file_with_a_pace_and_a_non_pace_role_is_refused_before_any_gpx_is_opened`（10 個參數化案例） | T901（`pace`，`pace_a.gpx`）與 T902（`holdout` 或 `excluded`）指向同一檔；自動選擇與 `--trips T901` 都測；名稱變體：完全相同、大小寫不同、結尾句點、結尾空白、`sub/` 與 `sub\` 路徑前綴。每一例斷言 exit 2、audit hook 觀測到 `--gpx-dir` 內沒有任何檔案被開啟、沒有寫出衍生路段表與報告。涵蓋 R1 record 的三個重現情形（holdout 自動、holdout 指定 T901、excluded 自動） |
| `test_the_conflict_is_reported_by_trip_id_and_found_by_load_manifest` | `load_manifest` 直接拒絕，訊息列出 `T901 (pace) and T902` |
| `test_non_pace_entries_sharing_a_file_and_distinct_pace_files_are_not_a_conflict` | 兩個非 `pace` 項目以不同大小寫共用一檔時仍正常重建，只開啟兩個 `pace` 檔 |

**Closure 證據（self-verification，修改後已還原，未 commit）**：拿掉 `_refuse_conflicting_roles` 的呼叫 → `tests/test_ingest_cli.py` 11 個失敗（10 個參數化案例與 `load_manifest` 的測試）；把 `source_key` 改成不忽略大小寫與結尾字元 → 5 個失敗。所以新測試在修正前會失敗、修正後通過。

### 10.2 R1-F2 的修正

第 6 節與第 9.2 節中「S-4 的列比對只差 `stop_allow_s`」改為「缺少 `stop_allow_s` 及隨它改變的時間值（`eta_typ`／`eta_safe`）」，保留原本的測試輸出。原因：pytest 的摘要只顯示第一列的差異；R1 record 的逐列比對顯示第 2 列起累計的 `eta_typ`、`eta_safe` 也不同，差異來自缺少的停等寬放，仍在 CL-B1-8 §3.3 第 4 項允許的範圍內。

### 10.3 回歸證據：E-1 依 CL-B1-9 第 2 項，在 `6f97561` 執行（主 checkout）

**(i) `.venv/Scripts/python.exe -m pytest -q`**（exit code 0）：

```text
........................................................................ [ 26%]
........................................................................ [ 53%]
........................................................................ [ 80%]
...........................................x....x.xx.                    [100%]
265 passed, 4 xfailed in 0.90s
```

**(iii) `.venv/Scripts/python.exe -m pytest -q -rxX`**（exit code 0）：

```text
........................................................................ [ 26%]
........................................................................ [ 53%]
........................................................................ [ 80%]
...........................................x....x.xx.                    [100%]
=========================== short test summary info ===========================
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
265 passed, 4 xfailed in 0.92s
```

K-1：`grep -rn "xfail\|skip" tests/` 只有 `tests/test_routes_pace_eta.py` 第 117（`restored by #10`）、159、173、182 行（`restored by #11`）的 4 個 CL-B1-8 標記；沒有 `restored by #9`，沒有其他 `xfail`／`skip`。

**(iv) `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py`**（exit code 1；`--collect-only` 為 71 個測試；以 `PYTHONIOENCODING=utf-8` 執行）：

```text
.............................................................F....F.FF.  [100%]
================================== FAILURES ===================================
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
FAILED tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
FAILED tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
4 failed, 67 passed in 0.72s
```

失敗的恰好是 (iii) 的 4 個 xfail 測試；訊息只涉及配速表表頭與類別紀錄缺少的 v0.3 欄位（`margin_coeff` 等）、ETA 路段列缺少 `stop_allow_s`，以及 S-4 列比對中缺少 `stop_allow_s` 及隨它改變的時間值，都在 CL-B1-8 §3.3 第 4 項列舉的 v0.3 項目之內。與第 9.2 節在 `b4d1f84` 的輸出逐行比較，除了進度列與計數（`55 passed` → `67 passed`，多出 12 個新案例）之外完全相同。

**(v)** `git diff 0c109aa 6f97561 --stat -- tests/test_routes_pace_eta.py tests/conftest.py tests/test_contracts.py pyproject.toml` 沒有輸出：S-3～S-6 的測試與標記沒有修改。S-1、S-2 的恢復不變（第 6 節 E-4）。`git diff --check 0c109aa 6f97561 -- src tests` 沒有輸出。

**結果照實寫：`265 passed, 4 xfailed`（依 CL-B1-8、CL-B1-9）。** 這不是「全數通過」；E-1 是否滿足由 R2 依 CL-B1-9 核對。測試數：`b4d1f84` 的 257 個加上 12 個新案例 ＝ 269 ＝ 265＋4。

### 10.4 E-2、E-5 的更新

- E-2：CL-B1-3 第 4 項（清單中非 `pace` 的項目不開啟）的對應測試加上第 10.1 節的三個測試；第 6、9 節其他各列在 `6f97561` 仍全部 PASS（同一次 (i)）。
- H-2：新的拒絕在開啟任何 GPX 之前發生，錯誤訊息不含檔名；新測試只用合成檔與合成清單。commit 前確認暫存的只有兩個檔案，`git ls-files` 仍不含 `.env`、`*.gpx`、`*.fit`、`data/`。以真實清單或真實資料核對：NOT VERIFIED（C-9-3）。
- H-3：凍結前開啟保留行程的程式路徑：自動選擇、明確指定、清單內部角色矛盾三種情形都以測試證明不開啟非 `pace` 指定的檔案（在第 10.1 節所述的名稱等價範圍內；殘餘情形已記錄）。結果陳述照實寫數目。
- H-4：清單矛盾是明確的拒絕（exit 2，沒有輸出），不是靜默略過或部分重建。
- 本次 correction 沒有讀取 `data/` 或 `.env`，沒有讀取或執行 `experiments/` 下的檔案，沒有派工任何 subagent。

### 10.5 Concerns 與剩餘工作

| # | 項目 | 所需 authority／負責者 |
| --- | --- | --- |
| C-9-5b | 第 10.1 節的殘餘：名稱比較無法辨識連結、8.3 短檔名或內容相同的不同檔名 | 無（記錄）；是否需要以檔案識別（stat）或內容比較加強，屬 Design Authority／之後的上傳與去重複工作 |
| C-9-6 | 對清單內部矛盾採「整份清單拒絕」而不是只略過衝突項目（第 10.1 節「契約語義」） | 無（記錄）；R2 有疑義時 Design Authority |
| C-9-3、C-9-4 | 不變（第 8 節） | acceptor（RB-7）；AB-12 |
| R-9-1 | R2 closure review（subject `6f97561`） | Orchestrator |
| R-9-2 | S-3～S-6 由 #10、#11 恢復 | #10、#11 |
