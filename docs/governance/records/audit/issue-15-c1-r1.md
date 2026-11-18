# Issue #15 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-R1 v1（`derivation-spec-r1.md` §2、§4 CL-R1-1／CL-R1-10、§5 R1-3 與 E-1～E-6）＋CL-R1-13、CL-R1-14、CL-R1-18、CL-R1-22～CL-R1-24 → Issue #15 |
| Subject | 本專用 worktree 的 detached HEAD `3d49cef97617ea7467fe0da626ade4e96e939608`；BASE `201e3e364767bb03ce1d2aa2e3a443bd4a838eb6`。Implementation commits：`b771d9f`、`e78cc9f`；其他增量只有 `docs/governance/records/**` |
| Audit kind | **Ticket independent audit，R1，cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`（Codex，Bindings m3 O-6） |
| 日期 | 2026-11-18 |
| 派工／執行邊界 | 本次使用者的 fresh independent review pack；只在本 worktree 自行讀取、測試與寫本 record，沒有 subagent、網路、GitHub、git 寫入操作或實作修改 |
| Issue 識別 | Pack 提供的原文 SHA-256 `a54f8034cdadd143e6a1ec594ee7d74e01bb47ce9bc13bd21537bbcf92fd5ad7` 與 run record §4 的 #15 相符；未連線重取 Issue |

## Assurance

| Assurance 欄 | 滿足方式與證據界限 |
| --- | --- |
| (a) Context independence 四項 properties | **Independent context**：這是 fresh Codex thread，沒有繼承 Executor 的對話；自行由檔案形成判斷，worklog 的 PASS、DONE 與突變結果均視為待驗證主張。**Verifiable binding**：採 Bindings §3.3 的 Codex 機制，由 dispatcher 核對本次 rollout 的全部 `(model, effort, sandbox)`、thread、存取紀錄及 record hash，再記入 `run-20261117-oc1-run2.md` §6 的本次 #15 R1 dispatch event。**本 HEAD 尚無該 event**：搜尋 `^\| 8[1-9] |#15 R1|cx15r1` 只得到事件 81～83（行 159～161，分別是 Executor、DA、Executor correction），不能拿它們冒充本次 Reviewer binding；見 NV-BIND。**Autonomous access**：自主閱讀契約、完整新模組與測試、差異與歷史，執行兩個完整 pytest 指令、獨立失敗探測及記憶體突變，不受 worklog 摘要限制。**Self-written record**：本 record 由此 Codex thread 自寫；dispatcher 應依 Bindings §3.3 原樣複製並核對 SHA-256，不得代寫或改寫。最後的 status 核對只允許這一個新增檔案。 |
| (b) 實際 models／model diversity | Executor：run record §6 事件 81、83 記錄 `ae0a2f33f0da61e65`，實際觀測 `claude-opus-5-5`／`high`，最新為 111 則。Primary：本 reviewer 是 **Codex**；run record §1 第 4 項宣告的 mapping 是 `gpt-6.1-sol`／`high`，但這不是本次 runtime 的觀測證據。本次精確 model／effort／sandbox 的外部 rollout 核對由 dispatcher 負責，未在此快照提供；不讀 worktree 外檔案以自行補證。**no model diversity claim**。Formal binding 的最終有效性須由 dispatcher 完成 NV-BIND 的核對。 |

## Findings

### R1-F1 — 未知 XML encoding 使解析失敗逸出，沒有回傳 `target_gpx_invalid`

- **Severity：Medium；blocking。Owner：#15 Executor。**
- 契約依據：CL-R1-23 第 1 項（檔案／內容讀不到點屬 `target_gpx_invalid`）、R1-3 範圍 (a)–(b)、SPEC-001 4.13 與 5.5，以及 H-4 §5（失敗須是契約所定明確錯誤）。這是位元組內容造成的讀取失敗，不是 CL-R1-23 第 5 項允許向上傳遞的呼叫參數型別錯誤。
- 證據：`src/moto_copilot/ingest/geometry.py:84` 呼叫 `ET.fromstring(data)`，行 85 只捕捉 `ET.ParseError`、`ValueError`。未知 encoding 會拋 **`LookupError`**。`routing/target_gpx.py:122`、`:133` 只將 `GpxGeometryError` 轉為 `TargetGpxError`，所以 bytes 與檔案入口均逸出原始解析器例外。
- 以下 stdin probe 在 HEAD 上實際執行（`sys.path` 只增加本 worktree 的 `src`；不建立檔案、不用網路）：

```powershell
@'
import sys
sys.path.insert(0, 'src')
from moto_copilot.routing.target_gpx import target_gpx_route_from_bytes
data = b'<?xml version="1.0" encoding="UnknownEncodingAuditProbe"?><gpx xmlns="http://www.topografix.com/GPX/1/1"/>'
for trip in ('one_way', 'round_trip'):
    try:
        print(trip, target_gpx_route_from_bytes(data, trip))
    except Exception as exc:
        print(trip, type(exc).__name__, str(exc))
'@ | python -
```

實際輸出：

```text
one_way LookupError unknown encoding: UnknownEncodingAuditProbe
round_trip LookupError unknown encoding: UnknownEncodingAuditProbe
```

另以 `unittest.mock.patch('builtins.open', return_value=io.BytesIO(data))` 呼叫 `target_gpx_route(Path('synthetic-audit-unknown-encoding.gpx'), 'one_way')`，得到相同 `LookupError`。這個路徑只交給記憶體替身，沒有讀取該檔或其他路徑。直接呼叫 `parse_gpx_geometry(data)` 也同樣逸出。對照 probe 的 UTF-32、UTF-7 宣告已能得到固定 `GpxGeometryError`／`target_gpx_invalid`，漏接集中於未知 codec 的 `LookupError`。

- 影響：使用者提供一份宣告了未知 encoding 的檔案，無法得到既定的 `target_gpx_invalid`，而是使呼叫流程以未預期的例外中止；完整 pytest 的通過沒有涵蓋此內容失敗。沒有路線被錯誤採用，亦**未主張已實際外洩私有資料**。
- **Required fix**：在 geometry reader 的 XML 解析邊界，將這類無法解碼／解析的輸入轉為固定、不含原始 parser 訊息的 `GpxGeometryError(UNREADABLE)`，維持 `__context__ is None`、`__cause__ is None`。新增未知 encoding 的 bytes 與 path 入口回歸案例，確認兩種 trip type 回傳 `TargetGpxError('target_gpx_invalid', 'unreadable')`、不產生路線且沒有路徑／檔名／log 或例外鏈外流。保留呼叫端型別錯誤的既有語義；修正後重跑 required gates。這是原範圍 (a) 內的 targeted correction，不要求改動 #9 的歷史 reader。

本次沒有其他 non-blocking finding。下列 NOT VERIFIED 與既有 tracked items 不冒充新的 implementation finding。

## 範圍、原始材料與 subject 核對

以 `Get-Content -Encoding UTF8 -LiteralPath <path>`（或對明確檔案的 `Get-Content ... | Select-Object`）與 `rg -n <pattern> <明確路徑>` 讀取／定位：

- Root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`；Bindings m3 的角色、O-6 qualification、independence、lane、records 與 release gate。
- 生效 package 的 `Minimal_Operational_Governance_v2.2_Candidate.md` §2.3、§3.8、§4.1～§4.7；`references/implementation-profiles/default-v2.md` §6～§7；`references/orchestrator-contracts/default-v2.2.md` §6～§7。
- OC-1 的範圍、AB-2／AB-10／AB-13、授權與接受紀錄；`derivation-spec-r1.md` 的引用、CL-R1-1／CL-R1-10、R1-3 與 E-1～E-6；`decision-20261117-oc1-first-run-derivation.md` 的 BD、分配與 audit 規則。
- `decision-20261118-issue13-c131.md` 的 CL-R1-13；`decision-20261118-issue14-c141.md` 的 CL-R1-14、CL-R1-18；`decision-20261118-issue15-c151.md` 的 CL-R1-22～24、§2.4 限制與 §4 T-1～T-7／突變要求；`decision-20261117-high-risk-categories.md` §5。
- `DESIGN.md` §4.1、§5 的目標 GPX、契約 2、切開與確定性規則；SPEC-001 §2、4.12、4.13、5.4、5.5、7.11 第 2 項及本票分配的 S 編號；SPEC-RESOLUTION-001 §2.2、2.3、2.8；lead dispositions resolution 的 §8.2、9.1～9.4、9.12 相關段落。
- Run record §1～§6（尤其事件 81～83）、#15 worklog 全文；兩個新模組、`routing/__init__.py` 的差異、`tests/test_target_gpx.py` 全文；#9 `ingest/gpx.py` 與 `segments.py` 的相關既有行為、既有 trim 測試。

| 指令／檢查 | 實際結果 |
| --- | --- |
| `git rev-parse HEAD`；`git rev-parse 201e3e3`；`git status --short` | HEAD／BASE 如表頭；初始 status 空白 |
| `git log --oneline 201e3e3..3d49cef`；`git log --format='%h %s' --name-only 201e3e3..3d49cef` | 七個 commits；只有 `b771d9f`、`e78cc9f` 含實作／測試，其餘為 record-only |
| `git diff --stat 201e3e3..3d49cef`；`git diff 201e3e3..3d49cef --numstat` | 七檔，1882 insertions、3 deletions；新 geometry 127 行、target_gpx 363 行、tests 891 行；exports 29 additions／2 deletions；三份 records |
| `git diff 201e3e3..3d49cef -- src/moto_copilot/routing/__init__.py` | 既有 exports 保留，只加目標 GPX exports 與模組說明 |
| `git diff b771d9f..e78cc9f -- src/moto_copilot/routing/target_gpx.py`；`git diff e78cc9f..3d49cef --name-only` | CL-R1-22 delta 為 nearest usable point、`c_k`、移除未決例外；最後 implementation commit 之後只有 run record／worklog |
| `git diff 201e3e3..3d49cef -- docs/governance/records/run/run-20261117-oc1-run2.md` | 只更新 #15 狀態與事件 81～83，無本次 R1 binding event |
| `git diff --exit-code 201e3e3..3d49cef -- src/moto_copilot/ingest/gpx.py src/moto_copilot/ingest/segments.py src/moto_copilot/ingest/__init__.py src/moto_copilot/contracts src/moto_copilot/routing/canonical.py src/moto_copilot/routing/request_key.py src/moto_copilot/routing/snapshot.py src/moto_copilot/routing/store.py tests/test_ingest.py tests/test_ingest_cli.py tests/test_routing_snapshot.py tests/test_routing_store.py` | exit 0、無輸出；#9 與 #14 既有程式、測試未變 |
| `git diff --check 201e3e3..3d49cef` | exit 0，無 whitespace error |
| `rg -n 'xfail|skip' tests/` | 只有兩處普通文字（`being_skipped` 測試名稱、contracts docstring 的 `skipped`），不是標記 |
| `rg -n 'xfail|pytest\.(mark\.(skip|skipif)|skip|importorskip)' tests/` | 無輸出；另以 `python -` 對 `tests/**/*.py` 作 AST Attribute 檢查，`xfail/skip/skipif/importorskip` 為 `[]` |
| `python -`：`subprocess.check_output(['git','ls-files','-z'])`，只輸出禁止樣式的命中數 | `.gpx=0`、`.fit=0`、`.env=0`、`data/raw/`／`data/private/`／`data/bmw/` 合計 `0`、`.key=0`。只查 git index metadata，不列出／開啟私有目錄或檔案 |
| `python -`：未知 encoding／UTF-32／UTF-7 的純記憶體 XML probe | 未知 encoding 漏出 `LookupError`，見 R1-F1；另兩者已被轉為固定錯誤 |
| `python -`：patch `builtins.open` 為 `BytesIO`／`PermissionError` | path 入口重現 R1-F1；PermissionError 正確回 `target_gpx_invalid/unreadable`，reader 錯誤文字固定，`context=None`、`cause=None` |
| `python -`：合成 antipodal 距離探測（`lat=i/100`，`i=1..8999`，第二點 `(-lat,180)`） | `haversine_m` 沒有拋數值 domain error；沒有據此提出 finding，也不將此探測外推為完整數值驗證 |

所有 Python probe 以 PowerShell here-string 傳入 `python -`；無暫存 probe script、無 GPX 落盤。沒有直接執行或檢視 `.venv`；兩次 pytest 均用 PATH 上的 `python`，未覆寫 `PYTEST_DEBUG_TEMPROOT`。套件 import／pytest 自動產生的 ignored caches 不構成 subject 變更。

## 自行執行的 required tests

Subject 均為表頭 HEAD；兩個命令都在本 worktree 執行，exit 0，完成後且寫本 record 之前 `git status --short`／`git status --porcelain` 均無輸出。

`python -m pytest -q` 完整輸出：

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
1625 passed in 24.12s
```

`python -m pytest -q -rxX` 完整輸出：

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
1625 passed in 19.02s
```

## Acceptance 與 clarifications 逐項核對

以下測試名稱都在 `tests/test_target_gpx.py`，均包含於兩次完整測試；行號為 HEAD 的證據定位。表中 PASS 限本票範圍，R1-F1 另明列 FAIL，不能用 suite 通過蓋掉它。

| 契約／AC | 原始實作與測試證據 | 結論 |
| --- | --- | --- |
| 範圍 (a)、CL-R1-10.1；不依賴時間、trkpt／rtept | geometry.py:93～100 依序取 track points，無 track 才取 route points；`test_track_points_are_read_in_file_order_across_trk_and_trkseg`、`test_reading_does_not_need_time_and_ignores_time_and_elevation`、`test_some_points_with_time_and_some_without_are_all_used`、`test_a_file_with_only_route_points_and_no_time_can_be_used`、`test_route_points_are_not_used_when_the_file_has_track_points` | 正常幾何讀取 PASS；內容失敗完整性見 R1-F1 |
| CL-R1-10.2；跨 trkseg gap | target_gpx.py:233 起檢查點數、所有相鄰點與總長；`test_no_points_or_one_point_is_invalid`、`test_total_length_under_1_km_is_invalid`、`test_adjacent_points_more_than_1_km_apart_is_invalid`、`test_a_gap_of_more_than_1_km_across_trkseg_is_invalid` | PASS |
| S27；CL-R1-10.3～5 | `test_missing_trip_type_is_an_explicit_error_and_is_not_inferred`、`test_round_trip_whose_end_is_not_at_the_start_is_not_round_trip_even_with_a_turnaround`、`test_out_and_back_without_a_turnaround_uses_the_point_farthest_from_the_start`、`test_ambiguous_shapes_are_not_detected_and_give_turnaround_unconfirmed`、T-2 | PASS；兩個 not-round-trip cases 有區分 |
| S43 的分配部分 | 行 255～324 的 invalid、rte-only、單向、trip type、200 m 案例；缺型態用 `TripTypeRequiredError`，不是新增路線錯誤代碼 | 原列幾何案例 PASS；未知 encoding 的 unreadable 延伸 FAIL（R1-F1）。追問流程不在本票 |
| S59 | `test_out_and_back_without_a_turnaround_uses_the_point_farthest_from_the_start`、`test_when_several_points_are_equally_farthest_the_first_is_the_turnaround`；target_gpx.py:203 起只有嚴格較遠才更新 | PASS；最遠點 ties 取第一個 |
| S60 | `test_ambiguous_shapes_are_not_detected_and_give_turnaround_unconfirmed` 的 loop；`test_the_four_shapes_of_s79` | PASS；無路線，case 為 `turnaround_unconfirmed` |
| S61、CL-R1-22 T-1 | `test_t1_s61_a_loop_is_cut_at_the_nearest_track_point_to_the_riders_position`（行 513），m 在兩點間、前後各較近一例；`test_t5_every_legal_whole_metre_gives_the_route_the_definition_selects` | PASS；完整流程無替換 cum，`c_k != m` 亦有案例 |
| S62、T-7 | `test_illegal_turnaround_positions_are_not_round_trip`、`test_a_turnaround_at_or_beyond_the_total_length_is_not_round_trip`、`test_an_illegal_turnaround_on_a_clear_out_and_back_does_not_fall_back_to_detection`；0、負、取整為 0、過大、NaN、±inf | PASS；不退回自動判定。非數字參數為明確 TypeError |
| S63、T-7 | `test_round_trip_whose_end_is_not_at_the_start_is_not_round_trip_even_with_a_turnaround`；target_gpx.py:249 先檢查端點 | PASS；給了折返位置也不能略過端點條件 |
| S64、範圍 (b)、T-6 | `_round_trip` 行 296～306 為 `points[:at+1]`、`points[at:]`；`assert_slices_of_the_file` 行 138 起與 `test_detected_round_trips_are_slices_of_the_file`、T-1～T-3／T-5 | PASS；兩段含同一分界、去掉一次分界後等於原檔全點；各長度等於 `cum_k`、`total-cum_k`，不反轉、不補造 |
| S78、CL-R1-10.6、T-3 | `test_t3_s78_full_flow_rider_and_detected_with_equal_metres_give_the_same_route`（行 548，非整數 cum、無替換）；另有直接 ID／不同檔案案例 | PASS；相同實際整數公尺相同 ID、選同一點的不同 m 相同 ID、不同採用點案例不同、單向與來回不同。小於 1 m 的碰撞限制另列，未宣稱消除 |
| S79、CL-R1-10.5 | `test_the_four_shapes_of_s79`、`test_exactly_90_percent_near_is_detected_and_less_is_not`、`test_detection_counts_samples_on_the_back_part_only`、`test_no_sample_on_the_back_part_means_not_detected`、`test_a_sample_is_near_within_50_m_of_a_front_point_and_not_beyond` | PASS；四形狀、≥90%、100 m 後開始、無樣本拒絕、50 m 門檻；格網與全搜尋比對也通過 |
| S80、T-2 | `test_t2_s80_on_a_clear_out_and_back_the_riders_position_wins_between_points`（行 532），m=1234，選 index 25、`c_k=1250`，不是最遠點 | PASS；rider 優先、無 cum 替換 |
| S58 的 RG-、CL-R1-13 | `test_every_produced_route_id_matches_the_contract_pattern`、`test_route_id_rejects_a_reference_that_is_not_64_lowercase_ascii_hex`、`test_route_id_rejects_inconsistent_trip_type_and_turnaround`；target_gpx.py:138～154、315 | PASS；完整字串、小寫 ASCII hex、拒絕換行／空白／非 ASCII；未修改 #13 契約 |
| S10 的路徑／檔名、CL-R1-10.7 | 行 800～868 的結果、錯誤、parser chaining、rider route 與 AST 無 logging／print 測試；新增 PermissionError 記憶體 probe | 已列路徑 PASS；正常回傳與已轉換錯誤不含路徑／檔名／log，cause/context 空。未知 encoding 尚漏出原 parser 例外（R1-F1），不宣稱所有失敗已涵蓋 |
| CL-R1-18.1～6、CL-R1-14 不適用 RG- | 行 157～175、311 的 Decimal／ROUND_HALF_UP；`test_turnaround_km_to_metres_rounds_half_up_from_the_decimal_form`、`test_float_multiplication_would_round_wrongly_and_is_not_used`、`test_detected_metres_round_half_up_not_half_even`、`test_target_gpx_module_does_not_call_round`、T-3 | PASS；0.0005→1、1.0005→1001、0.5005→501；km 先 Decimal 再乘1000；不呼叫 Python round、不經 JSON truncation |
| CL-R1-22.1～8、T-4／T-5 | `rider_turnaround_index` 行 270、`_usable` 行 288；`test_t4_the_selection_follows_the_definition`、`test_t4_no_usable_point_through_the_route_is_turnaround_unconfirmed`、`test_a_detected_boundary_that_is_not_usable_is_turnaround_unconfirmed`、T-5 四形狀每37 m掃描 | PASS；合法性以整數 m 與原 total 比較；可用條件兩項俱全；Decimal 精確距離、ties 較小索引、重複點第一個；沒有可用點明確錯誤；`turnaround_m` 與 RG- 一律用 `c_k` |
| CL-R1-23 | 行 238 的 malformed／unreadable 案例；GPX1.0／1.1、無 namespace 拒絕；壞點不略過；trip type／data／path 型別有明確 caller error | **FAIL（R1-F1）**：未知 encoding 沒有被歸入 unreadable，其餘列明案例 PASS |
| CL-R1-24 | TargetGpxRoute 保留 ref／trip type／原序幾何／長度／實際折返位置；本模組無引擎、快照或道路名稱補造路徑 | 本票 producer 部分符合；#16 共用介面、snapshot_id=null 等轉換與整合證據不在本票，NOT RUN，不作 SIA 判定 |
| 排除項與 #9／#14 回歸 | 無 UI upload／折返欄位、CLI 接線、routes 切段分類檢查點、RouteError 文字的實作增量；既有 ingest／snapshot 模組 diff 為空，完整 suite 通過 | PASS；沒有擴張 Must。新 reader 不改歷史 reader 無時間點略過等行為 |

## Evidence E-1～E-6 與高風險最低核對

| 要求 | 獨立核對結果 |
| --- | --- |
| E-1 | worklog §9.2 保留 `e78cc9f` 的完整 `1625 passed in 32.05s`；本 HEAD 之後只有 records delta；本 reviewer 的兩次完整結果如上，沒有 xfail／skip。Gate 通過不代表 R1-F1 已通過 |
| E-2 | worklog §6 的逐項 S 對照與 §9.2 的 CL-R1-22 更新合讀；S61／S78／S80 有不替換 cum 的完整流程，S64 增 T-6。§6 的原 BLOCKED／舊測試名稱是歷程，§9.2～9.3 有後續處置；本 record 另以現 HEAD 作上表核對 |
| E-3 | 新 tests 的 `at/line/path/circle/figure_eight/out_and_back/gpx` 由數學形狀生成 GPX；原點、換日線與極區均為聲明的合成 placeholder，日期與檔名亦是合成。新 records 的數值為測試／累計距離或 commit metadata；無真實騎乘 fixture／座標來源或公開地標座標。未讀取私有資料 |
| E-4、CL-R1-1 | `test_no_network_is_used` 替換 socket／create_connection／getaddrinfo；AST 測試禁止新模組網路、logging、環境讀取。原始碼的呼叫鏈只有本地開檔、解析、hash、幾何運算；未呼叫任何外部服務 |
| E-5 | BASE 的既有 tests 未變；worklog §9.3 逐項記錄本票早期測試的刪除／改寫（未決 split 例外、隱私案例、slice helper），依 CL-R1-22，沒有削弱 S64 或以替換 cum 取代必要完整流程 |
| E-6 | worklog §6／§9.2 有 H-2／H-3／H-4 self-verification；本 reviewer 自行執行 required tests、隱私／失敗 probe 與下列九個記憶體突變，並獨立指出未覆蓋失敗 R1-F1 |

獨立突變的實際命令是 `@' ... '@ | python -`：讀取 target_gpx 原文，逐個 `exec(compile(mutated_source, tg.__file__, 'exec'), tg.__dict__)` **只替換目前 Python process 的 module dictionary**，再 `runpy.run_path('tests/test_target_gpx.py')` 取得對應測試；每次以 `finally` 恢復原始 module dictionary。未將 mutant 寫入原始碼或任何檔案。這不是聲稱重跑 Executor 的 scratchpad 腳本或其全部 23 項突變。

| 獨立 mutant | 執行的既有測試／實際結果 |
| --- | --- |
| tie 時 `<` 改 `<=`，取較大索引 | T-4；CAUGHT AssertionError |
| 取 `D_i >= m` 第一點 | T-1；CAUGHT AssertionError |
| 取 `D_i <= m` 最後一點 | T-1；CAUGHT AssertionError |
| 回傳的 turnaround_m／route_id 改記 m | T-1；CAUGHT AssertionError |
| 拿掉選點可用條件、允許端點 | T-4；CAUGHT AssertionError |
| 只保留原始 cum 條件、拿掉取整 c 條件 | T-4；CAUGHT AssertionError |
| 在輸出加入線段中間的內插分界點 | T-1／slice assertion；CAUGHT AssertionError |
| 改以 float 差比較 | T-4 `1023.9/1024.1`；CAUGHT AssertionError |
| 自動判定不檢查分界可用性 | `test_a_detected_boundary_that_is_not_usable_is_turnaround_unconfirmed(...,'start')`；CAUGHT ValueError，未能回傳測試要求的明確錯誤 |

| 類別 | §5 最低核對結論 |
| --- | --- |
| **H-2** | Git index 禁止樣式 0 筆；diff／fixture／records 的資料可追溯至合成產生器與測試值；新模組不外送、不持久化 GPX、不回傳檔名／路徑或 log。已處理 I/O／parse error 的 cause/context 為空。`test_trim_removes_the_requested_distance_from_both_ends` 等歷史隱私裁切測試包含於完整 suite，#9 reader 未變；本票 target route 按契約原樣使用幾何，不套用歷史裁切。出發錨點代換、最終 PlanResult／LLM 對外輸出不屬本票 producer，沒有以本票測試冒充其整合證據；真實資料見 NV-PRIV。R1-F1 要求補齊解析錯誤封裝，不主張有已實際外洩 |
| **H-3** | 模組 docstring、detector docstring、constants 註解及 worklog 均保留 heuristic／NOT validated with real data；對應測試通過。合成測試、數值探測與突變沒有被寫成 E1 Lite、E2 或真實資料的驗證；本票沒有開啟 holdout 的程式路徑。未執行的真實資料及整合不標 PASS |
| **H-4** | trip type 缺漏明確報錯、不推定；單向不使用折返位置；無回到起點、非法 rider m、無 samples、ambiguous shape、無可用點均拒絕且有測試；兩個 not-round-trip cases 分開；不 fallback、不反轉、不補造。CL-R1-22 九項突變被抓到。但未知 encoding 失敗沒有回契約錯誤，**整體未通過（R1-F1）**。Planner／計畫狀態／規則5不在本票變更或權限內 |

## NOT VERIFIED／未執行及後續 authority

| ID | 狀態與理由 | Required authority／owner |
| --- | --- | --- |
| NV-BIND | 本次 R1 的 runtime binding、fresh 呼叫證據、rollout 存取稽核、record 原樣複製 hash，須由 dispatcher 事後核對。本 HEAD 的 run record §6 沒有本次 dispatch event；不能提供不存在的事件號，也不能由先前 #14 或 Executor 事件替代。Record 是自寫，但在 dispatcher 完成此核對前不宣稱 formal binding 已驗證 | **Orchestrator／dispatcher**，依 Bindings §3.3 在本次 #15 R1 dispatch event 補錄 thread、全部 turn_context 集合、存取檢查與 SHA-256，並作有效性判斷；本 reviewer 不越界讀取外部 rollout |
| NV-PRIV | 真實目標 GPX、真實騎乘與 heuristic 在真實資料上的表現 **NOT VERIFIED**；沒有明確路徑授權，亦未讀取 holdout。不以合成通過外推 | **acceptor**，RB-7；需要使用私有資料時另行明確授權 |
| NV-INTEGRATION | #16 共用介面、之後 routes／PlanResult／LLM 隱私、CLI／UI 及 Spec Integration Audit **NOT RUN**；屬排除項或後續分配，不因本票 suite 通過而宣稱完成 | **Design Authority** 負責後續 Spec／Ticket 分配；Orchestrator 依依賴派工；SIA 另派 |
| LIMIT-C15 | DA record §2.4 的稀疏點偏移可達數百公尺、整數公尺解析度可使不同 sub-metre 分界共用 RG-，均為已記錄限制；未當成已消除、也不新增 blocking finding。TI-C15-1 的顯示方式、RV-11 文字同步仍未完成 | **Design Authority**，沿用既有 tracked items；不擴張 #15 或本次 audit |

本次沒有修改、stage 或 commit 實作、測試、契約、worklog 或 run record。兩次完整測試後的 status 乾淨；交付時唯一預期增量為本 record。R1-F1 未解，需 targeted correction 後依既有流程作 R2；本結論不代替 Ticket completion、Spec Integration Audit、phase acceptance 或 release authorization。

Verdict: BLOCKING
