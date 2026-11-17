# Worklog — Issue #9（SPEC-B1 B1-2）`ingest`：停等事件與三種分類

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #9（BATCH-1 B1-2），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | Cycle 2：rework `49f1d80`（第 11 節）→ cycle 2 R1 BLOCKING（C2-R1-F1）→ targeted correction `5f9a35e`（第 12 節），待 cycle 2 R2。FA ruling `ruling-20261117-issue9-c1` 授權 cycle 2；DA 以 CL-B1-11 補上要求。Cycle 1：R1 BLOCKING（R1-F1）→ correction `6f97561`（第 10 節）→ R2 BLOCKING（R2-F1）→ Alternate UNRESOLVED → FA。Cycle 0：Executor 工作完成，回報 `DONE_WITH_CONCERNS`（第 8 節）。C-9-1、C-9-2 經 Design Authority 裁決（CL-B1-9、CL-B1-10），同一 worklog identity 續派完成 CL-B1-10 的測試與 CL-B1-9 的 E-1（第 9 節）。Ticket closure 由 Orchestrator 依 orch-default §7 判定，不由本 worklog 宣告 |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `0c109aa`（本 work item 開始時的 HEAD）；實作 commit **`a281cb0c07b522f6dad8ed078d085a37b2e59e7e`**（`a281cb0`）；CL-B1-10 的測試 commit **`b4d1f84eca1b4f80bd0265c81369384d62b055e0`**（`b4d1f84`，父 commit 是 DA record 的 `e165907`）。**R1 受審的程式與測試 subject 是 `b4d1f84`（R1 worktree HEAD `f0b5be9`）**；cycle 1 修正 commit **`6f975619a2e4b6303064955237c254de19f81da5`**（`6f97561`，第 10 節），是 cycle 1 R2 的程式與測試 subject；cycle 2 rework commit **`49f1d80ed1c67c09488353faf1d2b1ac479ea3cd`**（`49f1d80`，第 11 節），是 cycle 2 R1 的程式與測試 subject；cycle 2 correction commit **`5f9a35e9d743fb68e0f59c04dba3f780c2ae1151`**（`5f9a35e`，第 12 節），是 cycle 2 R2 的程式與測試 subject；本 worklog 在其後的 record-only commit 更新（`docs/governance/records/**`，Bindings 第 7 節） |
| 日期 | 2026-11-17 |

## 1. Contract reference

- **Ticket**：GitHub Issue #9 的內文與 4 項 AC。以 `gh issue view 9 --json body,updatedAt` 唯讀取得：`updatedAt` `2026-11-15T11:10:58Z`，`body` 的 UTF-8 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895`，與 BD-3（`decision-20261117-oc1-first-run-derivation.md` §3）相同；Orchestrator 提供的 scratchpad 原文檔的 SHA-256 也相同。本 work item 沒有修改 Issue #9。
- **Spec**：SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）：§2 引用的段落；§4 CL-B1-1、**CL-B1-3**、CL-B1-7；§5 #9 列（Issue 的 4 項 AC＋CL-B1-3 第 4、5 項的三項測試；高風險類別 H-2、H-3、H-4）與 E-1～E-5。
- **CL-B1-8**：`docs/governance/records/decisions/decision-20261117-issue7-spike-tests.md`（第 3.2 節：#9 結案時 S-1、S-2 的 strict xfail 移除、原斷言不帶標記通過）。
- **CL-B1-9、CL-B1-10**：`docs/governance/records/decisions/decision-20261117-issue9-e1-and-trim.md`（DA 對 C-9-1、C-9-2 的裁決；E-1 在 #9 的判定方式，以及停等事件跨修剪邊界的處理與另加的驗證條件）。在本 work item 執行中加入 SPEC-B1 的引用集合。
- **Cycle 2**：FA ruling `docs/governance/records/decisions/ruling-20261117-issue9-c1.md`（第 3.2 節的 rework 要求與 closure 證據、第 3.3 節的 cycle 2 授權）；DA decision `docs/governance/records/decisions/decision-20261118-issue9-qda1.md`（**CL-B1-11**：「不開啟」的範圍、pace 那一邊的連結別名、L-1～L-6）。
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
- **檔名等價**（`source_key`）：只取最後一個路徑成分（`/` 與 `\` 都視為分隔符），並忽略大小寫（`casefold`）、Unicode 正規化形式（NFC）與結尾的句點與空白（Windows 不區分這些）。比較只用清單中的字串，不讀取、不 stat、不雜湊任何非 `pace` 的檔案。鍵相同就視為同一檔，寧可多拒絕。**（Cycle 2 更正：這個等價關係比作業系統開檔時接受的拼法窄——`::$DATA` 等串流寫法與 8.3 短檔名不在其中，而 `6f97561` 以 `--gpx-dir / source_file` 直接開檔，所以這兩種拼法繞過了比對（R2-F1，FA ruling 第 2.3 節重現）。當時 `source_key` docstring 的「names that can open the same file in the GPX folder are equal」不成立。修正見第 11 節。）**
- **沒有改變的事**：兩個非 `pace` 項目共用一個檔、兩個 `pace` 項目各自的檔，不構成衝突（有測試）。沒有新增清單欄位，沒有實作內容去重複（Issue #9 排除範圍）。
- **契約語義**：這是 CL-B1-3 第 4 項「非 `pace` 的項目不開啟」在清單內部矛盾時的 fail-closed 執行方式，只增加拒絕，不改變任何欄位、角色或分類的定義；我判斷不需要 Design Authority 補定。若 R2 認為「整份清單拒絕」超出 CL-B1-3（例如應只略過衝突的項目），屬 Design Authority。
- ~~已知的殘餘：以名稱比較無法辨識指向同一檔案的不同名稱，例如符號連結、硬連結或 Windows 8.3 短檔名；也無法辨識內容相同、檔名不同的兩個檔。偵測這些需要 stat 或讀取非 `pace` 的檔案。~~ **（Cycle 2 更正：這個殘餘清單不正確也不完整。它漏了串流寫法；8.3 短檔名與 pace 那一邊的 hard link、符號連結都可以只用 pace 項目自身的資訊或名稱處理，不需要碰非 `pace` 的檔案（Alternate record、FA ruling 第 2.3 節、CL-B1-11 第 3 項）。殘餘以 CL-B1-11 第 4 項為準，見第 11.5 節。）**

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
- H-3：凍結前開啟保留行程的程式路徑：自動選擇、明確指定、清單內部角色矛盾三種情形都以測試證明不開啟非 `pace` 指定的檔案（在第 10.1 節所述的名稱等價範圍內；殘餘情形已記錄）。結果陳述照實寫數目。**（Cycle 2 更正：在 `6f97561`，「名稱等價範圍內」的限定掩蓋了仍然存在的路徑——串流寫法與 8.3 短檔名會讓非 `pace` 指定的目錄項目被開啟（R2-F1）。這項 H-3 主張在 `6f97561` 不成立；cycle 2 的 H-3 self-verification 見第 11.4 節。）**
- H-4：清單矛盾是明確的拒絕（exit 2，沒有輸出），不是靜默略過或部分重建。
- 本次 correction 沒有讀取 `data/` 或 `.env`，沒有讀取或執行 `experiments/` 下的檔案，沒有派工任何 subagent。

### 10.5 Concerns 與剩餘工作

| # | 項目 | 所需 authority／負責者 |
| --- | --- | --- |
| C-9-5b | ~~第 10.1 節的殘餘~~ **由 CL-B1-11（`decision-20261118-issue9-qda1.md`）取代**，見第 11.5 節 | Design Authority：已裁決 |
| C-9-6 | 對清單內部矛盾採「整份清單拒絕」而不是只略過衝突項目（第 10.1 節「契約語義」） | 無（記錄）；R2 有疑義時 Design Authority |
| C-9-3、C-9-4 | 不變（第 8 節） | acceptor（RB-7）；AB-12 |
| R-9-1 | R2 closure review（subject `6f97561`） | Orchestrator |
| R-9-2 | S-3～S-6 由 #10、#11 恢復 | #10、#11 |

## 11. Rework — cycle 2（FA ruling 第 3.2 節、CL-B1-11）

| 欄位 | 內容 |
| --- | --- |
| 依據 | FA ruling `ruling-20261117-issue9-c1.md`（R2-F1 與 R1-F1 殘餘為同一 root cause；targeted rework；授權 cycle 2）；DA decision `decision-20261118-issue9-qda1.md`（CL-B1-11）。兩份 record 與 R2、Alternate records 在 HEAD `77d7fdb` 時已 commit。Finding 與裁決的原文以各 record 為準 |
| 派工 | Orchestrator 以同一 worklog identity 續派同一 Executor（agentId `a6f915a1860417bc9`） |
| Rework commit | **`49f1d80ed1c67c09488353faf1d2b1ac479ea3cd`**（`49f1d80`），父 commit `77d7fdb`。只改 `src/moto_copilot/ingest/__main__.py` 與 `tests/test_ingest_cli.py`；`segments.py`、`tests/test_ingest.py` 對 `b4d1f84` 沒有差異 |
| Cycle 2 R1 的 subject | `49f1d80`（程式與測試）；之後只有本 worklog 的 record-only commit |

### 11.1 Root cause 與修正

**Root cause**（FA ruling 第 3.2 節、Alternate record）：`a281cb0` 把 BASE 的「清單名稱逐字等於資料夾列表中的名稱」改為直接以 `--gpx-dir / source_file` 開檔，從此作業系統接受的任何拼法都能開檔；`6f97561` 的角色比對（`source_key`）只涵蓋其中一部分拼法。也就是：重建流程會開啟它沒有納入角色衝突比對的拼法。

**修正**（`ingest/__main__.py`，在 `select_pace_trips` 之後、開啟任何 GPX 之前呼叫 `check_pace_entries`）：

1. **pace 項目只以列表中的名稱開啟。** 以 `os.listdir(--gpx-dir)` 取得名稱（只用名稱）；每一個被選中的 `pace` 項目的 `source_file` 必須**逐字等於**列表中的一個名稱，否則整次重建拒絕。列表只回傳長檔名的主資料串流名稱，所以串流寫法（`::$DATA`、`:x:$DATA`，不分大小寫）、8.3 短檔名、大小寫或結尾字元不同的拼法、含路徑的名稱，在 `pace` 那一邊都不會被開啟。這不依賴磁碟區是否產生短檔名。
2. **非 `pace` 那一邊的拼法以文字比對。** `source_key` 現在另外去掉 NTFS 串流後綴（最後路徑成分中第一個 `:` 之後的部分），所以 `pace_a.gpx::$DATA`、`PACE_A.GPX::$data`、`pace_a.gpx. ::$DATA` 等與 `pace_a.gpx` 同鍵，在 `load_manifest` 的角色衝突檢查中被拒絕（只用清單字串）。
3. **非 `pace` 那一邊的 8.3 短檔名以 pace 項目自身的短檔名比對。** 對每一個被選中的 `pace` 項目，以 `GetShortPathNameW` 取得**它自己的**短檔名（CL-B1-11 第 1.3 項允許），若與任何非 `pace` 項目的 `source_key` 相同就拒絕。查詢失敗時拒絕（不猜）。
4. **pace 那一邊的連結別名（CL-B1-11 第 3 項）。** 對每一個被選中的 `pace` 項目 `os.lstat`：符號連結（`S_ISLNK`）或任何 reparse point（`st_file_attributes & 0x400`）→ 拒絕；不是一般檔案 → 拒絕；`st_nlink != 1` → 拒絕。
5. 所有被選中的 `pace` 項目都通過之後才開啟第一個 GPX；任何一項不符時 exit 2、不寫出衍生路段表與報告。錯誤訊息只列行程代號與原因（例如 `T901 has more than one hard link`），不列檔名（H-2）。自動選擇與 `--trips` 都適用。 **（C2-R1-F1 更正：在 `49f1d80`，第 1、3 項只套用在被選中的 `pace` 項目，所以 `--trips` 只選另一個正常 `pace` 行程時，未被選中的 `pace` 項目與非 `pace` 項目之間的 8.3 拼法矛盾不會被發現，整次重建照常進行。`5f9a35e` 起第 1、3 項套用在清單中**全部** `pace` 項目，第 4 項仍只套用在被選中的項目。見第 12 節。）**

**行為變更（E-4 相關）**：`6f97561` 對「不是單純檔名」與「找不到檔案」的 `pace` 項目在報告中註記、照常結束（exit 0）；現在這兩種情形都屬第 1 項，整次重建拒絕（exit 2）。理由：在不碰檔案系統的前提下無法區分「不存在」與「某個目錄項目的另一種拼法」，所以 fail closed（H-4）。這是更嚴格的拒絕，不改變任何欄位、角色或分類的定義。若 Reviewer 或 DA 認為缺檔應改回註記，可以只對「列表中沒有、且 `source_key` 與列表中任何名稱都不同、且不含 `:` 與 `~`」的名稱恢復註記；我沒有這樣做，因為那會引入啟發式。見第 11.6 節 C-9-7。

**沒有改變的事**：不實作內容去重複、不新增清單欄位、不實作上傳（FA ruling 第 3.2 節第 3 項）。C-9-6（矛盾清單整份拒絕）不變。

### 11.2 L-4：重建流程在開啟 GPX 之前與之時的檔案系統操作

| # | 操作 | 作用對象 | 位置 |
| --- | --- | --- | --- |
| 1 | `Path.is_file()`、`read_text`（讀清單） | 行程清單檔（`--manifest` 或 `<out>/trip_manifest.json`） | `load_manifest` |
| 2 | `source_key` 等字串處理 | 清單字串（含非 `pace` 項目的 `source_file`），不碰檔案系統 | `load_manifest` → `_refuse_conflicting_roles`、`check_pace_entries` |
| 3 | `os.listdir(--gpx-dir)` | GPX 資料夾的列舉，**只用名稱** | `check_pace_entries` |
| 4 | `os.lstat`、`GetShortPathNameW` | **只有被選中的 `pace` 項目**（`--gpx-dir / source_file`，而且 `source_file` 已確認逐字在列表中） | `pace_entry_problem`（**C2-R1-F1 更正**：`5f9a35e` 起，`GetShortPathNameW` 用在清單中全部 `pace` 項目中逐字在列表內者，`os.lstat` 仍只用在被選中的 `pace` 項目；仍然都只作用在 `pace` 項目，見第 12.2 節） |
| 5 | `read_gpx`（`ET.parse` 開檔讀取） | 只有通過第 4 項檢查的 `pace` 項目 | `main` 的迴圈 |
| 6 | `mkdir`、`write_text` | `--out` 資料夾與兩個輸出檔（只在沒有拒絕時） | `main` |

非 `pace` 項目所指的目錄項目沒有任何操作作用其上（CL-B1-11 第 1 項）：它們只在第 2 項以字串出現；第 3 項的列舉只產生名稱。Python 的 `open` audit 事件不涵蓋 stat 類呼叫，所以另有 `test_no_metadata_is_asked_of_a_non_pace_item`：把 `os.lstat` 與 `short_name` 換成會記錄引數的包裝，在一份含 holdout 與 excluded 項目的清單上執行完整 CLI，斷言兩者只被用在兩個 `pace` 檔、沒有用在非 `pace` 項目，且 audit hook 只看到兩個 `pace` 檔被開啟。這只涵蓋本程式的呼叫路徑；Reviewer 仍以閱讀程式核對（L-4）。

### 11.3 Regression tests（`tests/test_ingest_cli.py`，合成資料，在 `49f1d80` 全部 PASS）

| 測試 | 內容 | 對應 |
| --- | --- | --- |
| `test_an_ntfs_stream_spelling_on_either_side_is_refused_before_any_gpx_is_opened`（24 例） | 串流寫法 6 種（`pace` 那一邊 3 種：`::$DATA`、`::$data`、`:other:$DATA`；非 `pace` 那一邊 3 種：`::$DATA`、大寫檔名＋`::$data`、`. ::$DATA`）× `holdout`／`excluded` × 自動／`--trips T901` | FA closure 1；R2 的四個重現與 Alternate 的兩個補充情形 |
| `test_a_stream_spelling_alone_on_a_pace_entry_is_refused`（2 例） | 沒有衝突項目、只有串流寫法的 `pace` 項目也不開啟 | Alternate 重現第 7 列 |
| `test_an_8_3_short_name_on_the_pace_entry_is_refused`（4 例） | `pace` 項目寫成 `PACE_L~1.GPX`，非 `pace` 項目寫長檔名；測試先斷言這個拼法不在列表中。不論磁碟區是否產生短檔名都成立 | FA closure 1、2 |
| `test_an_8_3_short_name_on_the_non_pace_item_is_refused`（4 例） | 非 `pace` 項目寫成 `PACE_L~1.GPX`；`short_name` 以 monkeypatch 回傳該值，使測試不依賴磁碟區；並斷言短檔名只被問了 `pace` 項目 | FA closure 1、2 |
| `test_the_real_short_name_lookup_is_only_used_on_pace_entries_and_matches_the_os` | 實際呼叫 `short_name`：Windows 上回傳含 `~` 的短檔名或長檔名本身 | 真實查詢的健全性 |
| `test_a_pace_entry_that_is_a_hard_link_to_a_holdout_file_is_refused`（2 例） | 以 `os.link` 建立真實 hard link：`pace` 項目是 `holdout` 檔的另一個名稱；自動與 `--trips T901`；斷言訊息含 `T901` 與原因、不含兩個檔名 | L-1 (1)(2) |
| `test_a_pace_file_with_a_hard_link_named_by_an_excluded_item_is_refused` | 方向相反：`pace` 項目是原檔，`excluded` 項目是另一個 hard link 名稱 | L-1 (3) |
| `test_a_pace_entry_that_is_a_symbolic_link_is_refused`（4 例） | 以 monkeypatch 替換 `os.lstat` 對該 `pace` 項目的回答（符號連結的 mode，或帶 reparse point 屬性的一般檔），其他路徑取得真實回答；自動與 `--trips`；訊息不含檔名 | L-2（不依賴建立符號連結的特權） |
| `test_no_metadata_is_asked_of_a_non_pace_item` | 第 11.2 節 | L-4 的輔助證據 |
| `test_a_missing_pace_file_refuses_the_run` | 找不到的 `pace` 檔 → exit 2、沒有開啟、沒有輸出 | 第 11.1 節的行為變更 |

每一例拒絕的斷言都是：exit 2、audit hook 在 GPX 資料夾內沒有看到任何 `open`、沒有寫出衍生路段表與報告。沒有新增 `skip`／`xfail`（K-1 見第 11.4 節）。

**8.3 短檔名的證據如何不依賴環境**：`pace` 那一邊只靠「名稱必須逐字在列表中」，列表不回傳短檔名，所以在任何磁碟區都成立；非 `pace` 那一邊以替換 `short_name` 的回答表現比對邏輯。**實際觀測**（本機，scratchpad 內的合成檔，沒有 mock，腳本 `<scratchpad>/c2obs/obs.py`，執行後刪除工作目錄）：此磁碟區對 `pace_long_named_trip_a.gpx` 產生短檔名 `PACE_L~1.GPX`；以它寫在非 `pace` 項目（`holdout`／`excluded` × 自動／`--trips T901`）時四例都是 exit 2、沒有開啟任何 GPX、只剩清單檔，訊息 `T901 has a short name that a non-pace item names`；寫在 `pace` 項目時 exit 2，訊息 `T901 is not exactly the name of an entry in the GPX folder`。

**符號連結的實際觀測**：`os.symlink` 失敗（`OSError`，`winerror 1314`，缺少建立符號連結的特權）→ **NOT RUN**。L-2 的證據是上表以替換 `os.lstat` 回答的測試。

**L-3**：`test_only_pace_entries_are_opened_and_the_result_passes_the_contract`、`test_requested_pace_trips_are_the_only_ones_opened`、`test_non_pace_entries_sharing_a_file_and_distinct_pace_files_are_not_a_conflict` 沒有修改斷言，在 `49f1d80` 通過。R1-F1 的 regression tests（第 10.1 節三個）沒有修改，通過。

**E-4（修改的既有測試）**：`test_a_source_file_outside_the_gpx_folder_is_not_opened` 由「exit 0、報告註記 `source_file is not a plain file name`」改為「exit 2、沒有報告」，`outside.gpx` 沒有被開啟的斷言不變。理由：第 11.1 節的行為變更（含路徑的名稱不在列表中，整次重建拒絕）。

**Mutation check（self-verification，修改後已還原，未 commit）**，`tests/test_ingest_cli.py` 的結果：拿掉列表逐字比對 → 5 個失敗；`source_key` 不去串流後綴 → 12 個失敗；拿掉短檔名比對 → 4 個失敗；拿掉 hard link 檢查 → 3 個失敗；拿掉符號連結／reparse point 檢查 → 4 個失敗；整個不呼叫 `check_pace_entries` → 20 個失敗。（拿掉列表比對時只有 5 個失敗，是因為 `pace` 那一邊的串流寫法在有衝突項目時也會被第 2 項的文字比對攔住——兩道防線重疊。）

### 11.4 E-1：依 CL-B1-9 第 2 項，在 `49f1d80` 執行（主 checkout）

**(i) `.venv/Scripts/python.exe -m pytest -q`**（exit code 0）：

```text
........................................................................ [ 23%]
........................................................................ [ 46%]
........................................................................ [ 69%]
........................................................................ [ 92%]
...............x....x.xx.                                                [100%]
309 passed, 4 xfailed in 1.44s
```

**(iii) `.venv/Scripts/python.exe -m pytest -q -rxX`**（exit code 0）：

```text
........................................................................ [ 23%]
........................................................................ [ 46%]
........................................................................ [ 69%]
........................................................................ [ 92%]
...............x....x.xx.                                                [100%]
=========================== short test summary info ===========================
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
309 passed, 4 xfailed in 1.36s
```

K-1：`grep -rn "xfail\|skip" tests/` 只有 `tests/test_routes_pace_eta.py` 第 117（`restored by #10`）、159、173、182 行（`restored by #11`）的 4 個 CL-B1-8 標記；沒有 `restored by #9`，沒有其他 `xfail`／`skip`。

**(iv) `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py`**（exit code 1；`--collect-only` 為 115 個測試；以 `PYTHONIOENCODING=utf-8` 執行）：

```text
........................................................................ [ 62%]
.................................F....F.FF.                              [100%]
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
4 failed, 111 passed in 1.11s
```

失敗的恰好是 (iii) 的 4 個 xfail 測試；訊息只涉及配速表表頭與類別紀錄缺少的 v0.3 欄位（`margin_coeff` 等）、ETA 路段列缺少 `stop_allow_s`，以及 S-4 列比對中缺少 `stop_allow_s` 及隨它改變的時間值，都在 CL-B1-8 §3.3 第 4 項列舉的 v0.3 項目之內。與第 10.3 節在 `6f97561` 的輸出比較，除了進度列與計數（`67 passed` → `111 passed`）之外完全相同。

**(v)** `git diff 0c109aa 49f1d80 --stat -- tests/test_routes_pace_eta.py tests/conftest.py tests/test_contracts.py pyproject.toml` 沒有輸出（S-3～S-6 沒有修改）；`git diff b4d1f84 49f1d80 --stat -- src/moto_copilot/ingest/segments.py tests/test_ingest.py` 沒有輸出（停等與修剪行為沒有改變，FA closure 3）；`git diff --check 0c109aa 49f1d80 -- src tests` 沒有輸出。

**結果照實寫：`309 passed, 4 xfailed`（依 CL-B1-8、CL-B1-9）。** 這不是「全數通過」；E-1 是否滿足由 cycle 2 的 Reviewer 依 CL-B1-9 核對。測試數：`--collect-only` 全部 313 個 ＝ 309＋4；`tests/test_ingest_cli.py` 由 26 個增為 70 個（＋44），`6f97561` 的 269 個＋44 ＝ 313。

### 11.5 E-2、E-5 與殘餘（L-5、L-6）

- **E-2**：CL-B1-3 第 4 項與 CL-B1-11 第 3 項的對應測試是第 11.3 節的表（L-6）；第 6、9、10 節其他各列在 `49f1d80` 仍全部 PASS（同一次 (i)）。
- **H-2**：拒絕都在開啟任何 GPX 之前；錯誤訊息只列行程代號與原因，不列檔名（hard link 與符號連結的測試斷言訊息不含檔名）。非 `pace` 項目所指的目錄項目沒有任何檔案系統操作（第 11.2 節）。新測試只用合成檔、合成清單與在 pytest 暫存目錄建立的 hard link。commit 前確認暫存的只有兩個檔案；`git ls-files` 中 `.env`、`*.key`、`*.gpx`、`*.fit`、`data/` 的數目是 0。以真實清單或真實資料核對：NOT VERIFIED（C-9-3）。
- **H-3**：凍結前開啟非 `pace` 指定檔案的程式路徑：同名、大小寫、結尾字元、路徑前綴、串流寫法（兩邊）、8.3 短檔名（兩邊）、`pace` 項目是 hard link 或符號連結／reparse point、缺檔，都以測試證明拒絕且不開啟任何 GPX。**仍不涵蓋**的只有 CL-B1-11 第 4 項的殘餘（下一點），以及 CL-B1-11 第 5 項明示不在要求內的 TOCTOU。結果陳述照實寫數目。 **（C2-R1-F1 更正：「整次重建拒絕」的主張在 `49f1d80` 不完整——未被選中的 `pace` 項目的 8.3 拼法矛盾不會使 `--trips` 選另一個行程的重建拒絕。這個情形沒有開啟非 `pace` 指定的檔案（開啟的是另一個正常 `pace` 檔），但不符合 FA ruling 第 3.2 節「不論選取哪些行程，整份清單拒絕」的要求。修正與重驗見第 12 節。）**
- **H-4**：所有不確定的情形（不在列表、無法 lstat、無法取得短檔名、不是一般檔、連結數不是 1）都是明確的拒絕，不是略過或部分重建。
- **殘餘（CL-B1-11 第 4 項，取代 C-9-5b）**：(i) 內容相同、名稱不同的兩個檔案；(ii) 非 `pace` 項目本身是指向 `pace` 檔的符號連結；(iii) 其他不同目錄項目承載同一趟行程、而 `pace` 項目自身看不出來的情形。這些依 CL-B1-11 歸 G-ING，辨識它們需要非 `pace` 項目的 metadata 或內容，#9 依 CL-B1-11 第 1 項不得處理。模組說明已寫明這兩類不在此偵測。
- 本次 rework 沒有讀取 `data/` 或 `.env`，沒有讀取或執行 `experiments/` 下的檔案，沒有派工任何 subagent。

### 11.6 Concerns 與剩餘工作

| # | 項目 | 所需 authority／負責者 |
| --- | --- | --- |
| C-9-7 | 第 11.1 節的行為變更：找不到或不在列表中的 `pace` 項目由「註記、exit 0」改為「整次重建拒絕、exit 2」。我判斷這是 fail-closed 的 HOW（無法不碰檔案系統就區分缺檔與別名），不改變契約語義 | 無（記錄）；Reviewer 有疑義時 Design Authority |
| C-9-8 | 對 `pace` 項目以 `GetShortPathNameW` 取得短檔名：CL-B1-11 第 1.3 項明列「它的短檔名」為允許的查詢。只在 Windows 上呼叫；其他系統沒有短檔名，回傳 None | 無（記錄） |
| C-9-3 | 以真實資料重建：NOT VERIFIED。另見 CL-B1-11 第 7 節 A-2（真實資料夾是否有跨角色連結或複本）與 FA ruling NV-2（真實磁碟區的短檔名） | acceptor（RB-7） |
| C-9-4 | 文件寫明重建需要清單；另依 CL-B1-11 第 8 節，`DESIGN.md` §12 應如實寫出 CL-B1-11 第 4 項的殘餘 | AB-12 的文件工作 |
| C-9-6 | 不變 | 無（記錄） |
| R-9-1 | Cycle 2 R1（完整 audit，subject `49f1d80`；pack 引用 FA ruling 與 CL-B1-11） | Orchestrator |
| R-9-2 | S-3～S-6 由 #10、#11 恢復 | #10、#11 |

## 12. Correction — cycle 2（C2-R1-F1）

| 欄位 | 內容 |
| --- | --- |
| 依據 | Cycle 2 R1 audit record `docs/governance/records/audit/issue-9-c2-r1.md`（Codex，`primary_reviewer`，verdict BLOCKING；HEAD `05f5a6b` 時已 commit）的 **C2-R1-F1**（Medium／blocking）與其 required fix。Finding 原文以該 record 為準。限制仍依 FA ruling 第 3.2 節與 CL-B1-11 |
| 派工 | Orchestrator 以同一 worklog identity 續派同一 Executor（agentId `a6f915a1860417bc9`），治理 §4.4 targeted correction |
| Correction commit | **`5f9a35e9d743fb68e0f59c04dba3f780c2ae1151`**（`5f9a35e`），父 commit `05f5a6b`。只改 `src/moto_copilot/ingest/__main__.py` 與 `tests/test_ingest_cli.py`；既有測試沒有被刪改（`git diff 49f1d80 5f9a35e -- tests/test_ingest_cli.py` 沒有刪除行） |
| Cycle 2 R2 的 subject | `5f9a35e`（程式與測試）；之後只有本 worklog 的 record-only commit |

### 12.1 修正

原因：`49f1d80` 的 `check_pace_entries` 只對 `chosen`（套用 `--trips` 之後）做名稱檢查，而 8.3 短檔名的比對只在那裡；全清單的 `_refuse_conflicting_roles` 只比對文字鍵。

修正：把檢查分成兩個函式。
- `pace_name_problem`：套用在**清單中全部 `pace` 項目**，不論 `--trips`。(a) 名稱必須逐字在 GPX 資料夾列表中——不在列表中的名稱可能是任何目錄項目（包括非 `pace` 項目所指者）的另一種拼法，不碰檔案系統就無法分辨，所以整次重建拒絕；(b) 對逐字在列表中的 `pace` 項目查詢**它自己的**短檔名，與非 `pace` 項目的 `source_key` 比對。
- `pace_link_problem`：只套用在**被選中的** `pace` 項目（CL-B1-11 第 3 項的範圍），且只對通過 `pace_name_problem` 的項目執行 `os.lstat`——名稱不在列表中的項目從不被 stat。
- 任何一項不符時 exit 2，不開啟任何 GPX，不寫出衍生路段表與報告。拒絕訊息的開頭改為 `the pace entries of the manifest do not pass the checks before opening:`，因為現在可能指向未被選中的項目；仍只列行程代號與原因，不列檔名。
- 模組說明改寫為與實作一致（名稱檢查涵蓋全部 `pace` 項目、「whichever trips are requested」；連結檢查涵蓋被選中的項目）。

**連帶的行為變更**（第 11.6 節 C-9-7 的延伸）：未被選中的 `pace` 項目若找不到檔案或不在列表中，`--trips` 選其他行程的重建也會被拒絕。理由同 C-9-7：無法不碰檔案系統就區分缺檔與別名。見第 12.5 節 C-9-9。

沒有對非 `pace` 項目所指的目錄項目作任何檔案系統操作（CL-B1-11 第 1 項）；沒有新增 `skip`／`xfail`；沒有擴張範圍。

### 12.2 L-4 的更新（第 11.2 節第 4 列）

| # | 操作 | 作用對象 | 位置 |
| --- | --- | --- | --- |
| 4a | `GetShortPathNameW`（`short_name`） | 清單中**全部** `pace` 項目，且只限 `source_file` 逐字在列表中者 | `pace_name_problem` |
| 4b | `os.lstat` | **被選中的** `pace` 項目，且只限已通過 4a 者 | `pace_link_problem` |

其他列不變。兩者都只作用在 `pace` 項目；非 `pace` 項目仍只以字串出現。`test_no_metadata_is_asked_of_a_non_pace_item` 在 `5f9a35e` 仍通過。

### 12.3 Regression tests（`tests/test_ingest_cli.py`，合成資料，在 `5f9a35e` 全部 PASS）

| 測試 | 內容 |
| --- | --- |
| `test_an_unselected_pace_entry_whose_short_name_a_non_pace_item_names_refuses_the_run`（4 例） | R1 record 的情形：T901（`pace`，長檔名）與 T902（`holdout`／`excluded`，其短檔名）是同一目錄項目，T904 是另一個正常 `pace` 行程；自動選擇與 `--trips T904` 都拒絕。`short_name` 以 monkeypatch 回傳短檔名，使測試不依賴磁碟區；斷言它只被問了 `pace` 項目 |
| `test_an_unselected_conflicting_pace_entry_refuses_a_run_that_requests_another_pace_trip`（6 例） | `--trips T904`，未被選中的 T901 與 `holdout`／`excluded` 項目的矛盾以三種拼法出現：8.3 短檔名寫在未被選中的 `pace` 項目、串流寫法寫在未被選中的 `pace` 項目、串流寫法寫在非 `pace` 項目 |
| `test_an_unselected_pace_entry_is_not_link_checked_and_an_ordinary_request_still_runs` | 連結檢查只用在被選中的項目：未被選中、帶第二個 hard link 而沒有名稱矛盾的 `pace` 項目，不阻擋 `--trips T904`（exit 0，只開啟 `pace_b.gpx`）；選它本身時拒絕 |

每一例拒絕的斷言：exit 2、audit hook 在 GPX 資料夾內沒有看到任何 `open`、兩個輸出檔都不存在。

**實際觀測**（本機，scratchpad 內的合成檔，沒有 mock，腳本 `<scratchpad>/c2obs/obs2.py`，執行後刪除工作目錄）：此磁碟區對 `pace_long_named_trip_a.gpx` 的真實短檔名是 `PACE_L~1.GPX`，不在 `os.listdir` 中。R1 record 的清單（T901 `ordinary.gpx` pace、T904 長檔名 pace、T902 短檔名 holdout）：自動、`--trips T901`、`--trips T904` 三者都是 exit 2、沒有開啟任何 GPX、只剩清單檔，訊息 `T904 has a short name that a non-pace item names`（R1 的重現中 `--trips T901` 是 exit 0 並開啟 `ordinary.gpx`）。短檔名寫在未被選中的 `pace` 項目、`--trips T901`：exit 2，訊息 `T904 is not exactly the name of an entry in the GPX folder`。對照組（沒有非 `pace` 項目）`--trips T901`：exit 0，只開啟 `ordinary.gpx`。

**Mutation check（修改後已還原，未 commit）**：把名稱檢查改回只套用在 `chosen` → `tests/test_ingest_cli.py` 4 個失敗（第一個測試的 2 例 `--trips T904` 與第二個測試中 8.3 寫在未被選中 `pace` 項目的 2 例；串流寫法的 4 例由 `load_manifest` 的文字比對攔住，是重疊的防線）。

### 12.4 E-1：依 CL-B1-9 第 2 項，在 `5f9a35e` 執行（主 checkout）

**(i) `.venv/Scripts/python.exe -m pytest -q`**（exit code 0）：

```text
........................................................................ [ 22%]
........................................................................ [ 44%]
........................................................................ [ 66%]
........................................................................ [ 88%]
..........................x....x.xx.                                     [100%]
320 passed, 4 xfailed in 1.55s
```

**(iii) `.venv/Scripts/python.exe -m pytest -q -rxX`**（exit code 0）：

```text
........................................................................ [ 22%]
........................................................................ [ 44%]
........................................................................ [ 66%]
........................................................................ [ 88%]
..........................x....x.xx.                                     [100%]
=========================== short test summary info ===========================
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
320 passed, 4 xfailed in 1.56s
```

K-1：`grep -rn "xfail\|skip" tests/` 只有 `tests/test_routes_pace_eta.py` 第 117（`restored by #10`）、159、173、182 行（`restored by #11`）的 4 個 CL-B1-8 標記；沒有 `restored by #9`，沒有其他 `xfail`／`skip`。

**(iv) `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py`**（exit code 1；`--collect-only` 為 126 個測試；以 `PYTHONIOENCODING=utf-8` 執行）：

```text
........................................................................ [ 57%]
............................................F....F.FF.                   [100%]
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
4 failed, 122 passed in 1.22s
```

失敗的恰好是 (iii) 的 4 個 xfail 測試；訊息只涉及配速表表頭與類別紀錄缺少的 v0.3 欄位（`margin_coeff` 等）、ETA 路段列缺少 `stop_allow_s`，以及 S-4 列比對中缺少 `stop_allow_s` 及隨它改變的時間值，都在 CL-B1-8 §3.3 第 4 項列舉的 v0.3 項目之內。與第 11.4 節在 `49f1d80` 的輸出比較，除了進度列與計數（`111 passed` → `122 passed`）之外完全相同。

**(v)** `git diff 0c109aa 5f9a35e --stat -- tests/test_routes_pace_eta.py tests/conftest.py tests/test_contracts.py pyproject.toml` 沒有輸出；`git diff b4d1f84 5f9a35e --stat -- src/moto_copilot/ingest/segments.py tests/test_ingest.py` 沒有輸出；`git diff --check 0c109aa 5f9a35e -- src tests` 沒有輸出；`git ls-files` 中 `.env`、`*.key`、`*.gpx`、`*.fit`、`data/` 的數目是 0。

**結果照實寫：`320 passed, 4 xfailed`（依 CL-B1-8、CL-B1-9）。** 這不是「全數通過」；E-1 是否滿足由 cycle 2 R2 依 CL-B1-9 核對。測試數：`--collect-only` 全部 324 個 ＝ 320＋4；`tests/test_ingest_cli.py` 由 70 個增為 81 個（＋11），313＋11 ＝ 324。

### 12.5 E-5 與 concerns

- **H-2**：新的拒絕在開啟任何 GPX 之前；訊息不列檔名；新測試只用合成檔與合成清單。非 `pace` 項目所指的目錄項目仍沒有任何檔案系統操作（第 12.2 節）。以真實資料核對：NOT VERIFIED（C-9-3）。
- **H-3**：「整份清單的 `pace`／非 `pace` 拼法矛盾，不論選取哪些行程，都在開啟任何 GPX 之前拒絕」現在以自動、`--trips` 選衝突項目本身（第 11.3 節）、`--trips` 選其他行程（第 12.3 節）三種選取方式的測試表現，涵蓋大小寫、結尾字元、路徑前綴、串流寫法與 8.3 短檔名。仍不涵蓋的只有 CL-B1-11 第 4 項的殘餘與第 5 項的 TOCTOU（第 11.5 節）。結果陳述照實寫數目。
- **H-4**：不確定的情形（名稱不在列表、短檔名查詢失敗、lstat 失敗）都是明確拒絕。
- 本次 correction 沒有讀取 `data/` 或 `.env`，沒有讀取或執行 `experiments/` 下的檔案，沒有派工任何 subagent。

| # | 項目 | 所需 authority／負責者 |
| --- | --- | --- |
| C-9-9 | 第 12.1 節的連帶行為變更：未被選中的 `pace` 項目找不到檔案或不在列表中，也會使選其他行程的重建拒絕（C-9-7 的延伸）。這是更嚴格的拒絕，不改變契約語義 | 無（記錄）；Reviewer 有疑義時 Design Authority |
| C-9-7、C-9-8、C-9-6 | 不變（第 11.6 節） | 同第 11.6 節 |
| C-9-3、C-9-4 | 不變 | acceptor（RB-7）；AB-12 |
| R-9-1 | Cycle 2 R2 closure review（subject `5f9a35e`） | Orchestrator |
| R-9-2 | S-3～S-6 由 #10、#11 恢復 | #10、#11 |
