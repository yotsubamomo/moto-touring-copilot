# Issue #9 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）→ Issue #9「B1-2 ingest」 |
| 適用 clarification | CL-B1-1、CL-B1-3、CL-B1-7；`decision-20261117-issue7-spike-tests.md` 的 CL-B1-8；`decision-20261117-issue9-e1-and-trim.md` 的 CL-B1-9、CL-B1-10 |
| Subject | 專用 worktree 的 detached HEAD `f0b5be902c9cf1775c04b8f42c88a9c6572227e3`；BASE `0c109aaba8c8460cebea5336840cc1d556d88a71` |
| Implementation commits | `a281cb0c07b522f6dad8ed078d085a37b2e59e7e`、`b4d1f84eca1b4f80bd0265c81369384d62b055e0`；其餘 BASE 之後的 commits 僅修改 Bindings §7 的 record-only paths |
| Audit kind | **Ticket independent audit，R1，cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`，Codex |
| 日期 | 2026-11-17 |
| 治理 | Minimal Operational Governance v2.2、Bindings m3、impl-default v2、orch-default v2.2；依本次派工使用 PATH 上的 `python` |
| Issue 版本 | 本次 bounded pack 所附原文；SHA-256 識別 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895` 與 BD-3 的 #9 列相符。沒有連線取得 Issue 或查核遠端現況 |

## Independence 與 model assurance

| Property | 滿足方式／證據邊界 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread，由 bounded pack 開始；沒有繼承 Executor 對話或推理。自行閱讀原始契約、實作、測試、git 歷史；worklog 與 DA 的實作閱讀結論均視為待驗證主張 |
| Verifiable binding | 派工引用 `docs/governance/records/run/run-20261117-oc1-run2.md` §6 **事件 8**，有效 mapping 為 Codex `gpt-6.1-sol`／`high`（O-6）。依 Bindings §3.3，**派工者**須在採用 return 前核對本次 rollout 全部 turn_context 的 model、effort、sandbox、存取範圍及 record SHA-256，將觀測補入事件 8。受審 HEAD 的該事件目前記「進行中」；本 reviewer 不存取 worktree 外 rollout，也不把指定 mapping 冒充已完成的實際 binding 核對 |
| Autonomous access | 在本 worktree 自行讀檔、執行 git 唯讀命令、pytest、合成資料 CLI 與額外重現；不限於 Executor 所列測試。未讀取、列出或搜尋私有資料，未接觸憑證、其他 checkout 或 worktree 外的專案路徑；未執行 `experiments/`，未使用網路 |
| Self-written record | 本 record 由本 reviewer 直接寫入指定路徑；沒有修改實作、測試、契約或其他 record，沒有 stage／commit。派工者依 Bindings §3.3 原樣核對、採用，不代寫結論 |

Executor 的實際 model 證據：run record §6 事件 2、7 記錄 agentId `a6f915a1860417bc9`，分別觀測到 99、118 則 assistant 訊息，均為 `claude-opus-5-5`／`high`。本 reviewer 是 **Codex**；精確 model id 的實際觀測由派工者依事件 8 補記，本 context 沒有可獨立核對的 rollout。因此目前 **no model diversity claim**。四項 independence 的派工與執行方式如上；return 的正式採用仍須有 dispatcher 的 binding 核對，不能以本 record 的自述取代。

## Findings

### R1-F1 — High / blocking：同一來源檔案的矛盾角色可繞過保留行程隔離

- **契約依據**：Issue #9 範圍及共通規則、CL-B1-3 item 4、SPEC-B1 §5 #9 的非 `pace` 檔案不得開啟、`DESIGN.md` §5 契約 1 後的凍結前隔離要求；高風險 record §5 的 H-2、H-3。
- **實作證據**：`src/moto_copilot/ingest/__main__.py:47` 起只檢查 `trip_id` 不重複，沒有檢查不同 ID 的 `source_file` 角色衝突；`:64` 起按 ID／單筆角色選出 pace 項目；`:105`、`:109` 直接開啟該來源。若 T901（pace）與 T902（holdout）都指向 `pace_a.gpx`，T902 雖被跳過，同一個 holdout 檔案仍以 T901 開啟並產生 pace 列。
- **獨立重現**：使用 pytest 已建立的合成 `pace_a.gpx`；只 mock manifest 的 `Path.read_text` 回傳值及輸出寫入，**保留真實 `load_manifest`、selection、GPX parser、build_rows 與契約檢查**。以 Python audit hook 觀察實際 `open`，結果如下。此清單通過現有 loader，並非必須先破壞 loader 才能到達的輸入。

```text
CONFLICT holdout explicit_pace False exit 0 actual_open_events ['pace_a.gpx']
CONFLICT holdout explicit_pace True exit 0 actual_open_events ['pace_a.gpx']
CONFLICT excluded explicit_pace False exit 0 actual_open_events ['pace_a.gpx']
```

第一次重現另觀察到：`pace trips: 1 | non-pace entries not opened: 1 | rows: 8`，private／public／pair 三項均顯示 `OK`。明確指定 `--trips T901` 也能繞過同一份清單中的 holdout 指定。

- **風險與判定**：清單角色矛盾時仍開啟已被清單指定為 holdout／excluded 的來源，破壞凍結前隔離，且輸出被標成 pace，後續契約驗證不會攔住。這是檔案開啟前的角色防線缺陷；不需要私有資料即可證實。未主張任何真實資料已被讀取或外洩。
- **Required fix／owner**：#9 Executor 在開啟任何 GPX 前驗證清單的來源與角色一致性；至少拒絕不同 ID 對同一來源檔名作 pace／非 pace 的矛盾指定，涵蓋本環境通常的檔名大小寫等價情形。對自動選擇與明確選擇 pace ID 都補合成 regression tests，以 open 事件證明拒絕時沒有任何 GPX 被開啟、沒有輸出 pace 列。更新 worklog 的 H-2／H-3 主張與 evidence。這不要求讀取或雜湊非 pace 的 GPX，也不要求實作排除範圍中的上傳／內容去重複。
- **Disposition**：未解；targeted correction 後交 R2。屬 accepted contract 違反，不作 deferral。

### R1-F2 — Low / non-blocking：worklog 對 S-4 差異的摘要不完整

- **證據**：`docs/governance/records/worklog/issue-9.md:305` 寫「S-4 的列比對只差 `stop_allow_s`」。實際獨立逐列比對還有 `eta_typ`／`eta_safe` 差異：

| seg_index | fixture 的 stop_allow_s | fixture − producer 的 eta_typ 秒數 | fixture − producer 的 eta_safe 秒數 |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 1 | 9 | 9 | 11 |
| 2 | 18 | 27 | 32 |
| 3 | 0 | 27 | 32 |

- **判定**：差異恰好是缺少停等寬放造成的累計時間，仍在 CL-B1-8 §3.3 item 4 明文允許的範圍；不影響 CL-B1-9 的 E-1 判定。pytest 的摘要只顯示第一列差異，不能據此概括所有列。屬 H-3 evidence 敘述精度問題，沒有證據支持虛構測試結果的指控。
- **Required fix**：將摘要改為「缺少 `stop_allow_s` 及隨它改變的時間值」，保留實際測試輸出。
- **Disposition／owner**：由 #9 Executor 在後續 worklog 更新時修正文句，Orchestrator 追蹤；此 non-blocking item 不延長 audit cycle。

## 範圍、原始材料與命令

已讀 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3（含 O-6、§3.3、§3.7、§5、§7）、治理本文 §2.3、§3.8、§4.1–§4.7、impl-default §6–§7、orch-default §6–§7；OC-1；SPEC-B1 derivation、first-run derivation（含 BD-3、G-ING、G-REG、AB 分配）、高風險 decision、CL-B1-8／9／10 decisions；#9 worklog 與 #7 worklog 的 C-2、追蹤表；`DESIGN.md` §5、§6.1；SPEC-RESOLUTION-001 §1.1–§1.6；SPEC-001 §2；BATCH-1 共通規則、依賴與 B1-2。來源檔與測試詳見下表。讀檔使用 worktree 內明確路徑的 `Get-Content -Encoding UTF8`／`rg -n`；第一次 PowerShell 預設編碼的輸出不清楚，已用 UTF-8 重讀。

| 命令／檢查 | 實際結果 |
| --- | --- |
| `git status --short`、`git rev-parse HEAD`、`git rev-parse 0c109aa` | 開始與寫 record 前皆無 tracked／untracked delta；HEAD、BASE 如檔首 |
| `git log --oneline 0c109aa..f0b5be9`、`git log --format='%h %s' --name-only 0c109aa..f0b5be9`、`git diff --stat 0c109aa..f0b5be9` | 6 個 commits；7 個變更路徑。兩個 implementation commits 以外均為 `docs/governance/records/**` |
| `git diff 0c109aa..f0b5be9 -- src/moto_copilot/ingest/segments.py src/moto_copilot/ingest/__main__.py tests/test_ingest.py tests/test_ingest_cli.py`；閱讀完整現行檔案 | 完整檢查產品與測試差異，發現 R1-F1；另讀 `ingest/gpx.py`、`ingest/__init__.py`、contract validator 相關路徑 |
| `git diff 0c109aa..f0b5be9 -- tests/test_routes_pace_eta.py tests/test_contracts.py tests/conftest.py pyproject.toml` | 空；S-3～S-6 與 gates 未改 |
| `rg -n 'xfail\|skip' tests` | 恰好 4 個 strict xfail，位於 `test_routes_pace_eta.py:117`、`:159`、`:173`、`:182`；沒有 skip 或 `restored by #9` |
| `rg` 檢查 `tests/` 的私有路徑、網路與 subprocess 引用；閱讀 `pyproject.toml`、`tests/conftest.py` | 無相關命中；pytest 路徑設定為 `src`／`tests`，資料 fixture 明載 mock |
| `rg` 檢查 `src/moto_copilot/ingest`、`src/moto_copilot/routes` 的讀檔／網路呼叫 | ingest 的 GPX 開啟點為 `__main__.py:109` → `gpx.py:20`；本票沒有新增第三方請求 |
| `python -`：以 `subprocess.check_output` 取得 `git ls-files -z` 並只輸出違禁 pattern 的數量 | `.env`、`*.key`、`*.gpx`、`*.fit`、`data/` 的 tracked path 數量為 **0**；沒有開啟這些路徑或輸出任何私有檔案清單 |
| 同一 `python -`：以 `git rev-list`／`git diff-tree` 核對各 commit；以 `ast` 比對 S-1／S-2 的原斷言 | record-only 範圍符合；S-1 的 4 個斷言、S-2 的 3 個斷言均完整保留且不帶標記；GPX parser 未改 |
| 同一 `python -`：擷取完整 `git diff 0c109aa..f0b5be9` 的新增行，掃描用語／credential patterns | 僅命中紀錄中描述禁用詞或掃描 pattern 的文字；沒有受限制的正面宣稱、憑證值或真實軌跡。人工核對合成來源，沒有以「不在台灣範圍」當作唯一證據 |
| `git diff --check 0c109aa..f0b5be9` | worklog 的 pytest 原始輸出有 4 行尾空白（243、258、275、292）；無產品缺陷。限定四個程式／測試檔的同一檢查無輸出、exit 0 |

### pytest 與 CLI 的實際執行

所有執行都在本 worktree。為避免 `tmp_path` 使用 worktree 外的預設暫存路徑，各次 pytest 設定：

```powershell
$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/r1-tmp'
$env:PYTHONIOENCODING='utf-8'
```

第一次 `python -m pytest -q` 因 `.pytest_cache` 父目錄尚不存在，14 個 CLI 測試出現 `FileNotFoundError` setup errors：`239 passed, 4 xfailed, 14 errors in 1.35s`，exit 1。這是 reviewer 的暫存位置設定問題；以 `New-Item -ItemType Directory -Path .pytest_cache -Force` 建立允許的 cache 目錄後重跑。沒有修改測試或產品來排除此問題。

| 指令 | 結果／exit code |
| --- | --- |
| `python -m pytest -q`（上述設定修正後） | `253 passed, 4 xfailed in 1.07s`；0 |
| `python -m pytest -q -rxX` | `253 passed, 4 xfailed in 1.07s`；0 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py` | `4 failed, 41 passed in 0.55s`；1，失敗恰好 S-3～S-6 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py`（CL-B1-9 的完整範圍） | `4 failed, 55 passed in 0.72s`；1，失敗恰好 S-3～S-6 |

完整一般測試輸出：

```text
........................................................................ [ 28%]
........................................................................ [ 56%]
........................................................................ [ 84%]
...............................x....x.xx.                                [100%]
253 passed, 4 xfailed in 1.07s
```

`-rxX` 的四個 reason 均為 `v0.3 producer gap (decision-20261117-issue7-spike-tests)`：

- `test_pace_table_matches_the_mock_fixture__v03_contract`：restored by #10，缺 `stop_ratio`、`margin_coeff`、`margin_basis`。
- `test_eta_reproduces_the_mock_fixture__v03_contract`：restored by #11，缺 `stop_allow_s`。
- `test_eta_is_unknown_when_a_category_has_no_pace__v03_contract`：restored by #11，缺 `stop_allow_s`。
- `test_eta_output_passes_the_contract_with_and_without_breaks`：restored by #11，缺 `stop_allow_s`。

另以 `python -`、`runpy.run_path('tests/test_routes_pace_eta.py')` 呼叫同一 mock fixture 與 validators，檢視未被 pytest 摘要完整列出的違反：S-3 恰好表頭缺兩欄、三個類別各缺 `stop_ratio`；S-5 恰好兩列缺 `stop_allow_s`；S-6 的四列缺該欄，並因該缺值回報 `has a null time although status is ok`。S-4 逐列的全部差異見 R1-F2；另外斷言其典型時間差等於累計 allowance，保守時間差與累計 allowance × 1.2 的差不超過 1 秒，通過。故未發現 #9 的新失敗被 xfail 遮住，E-1 依 CL-B1-9 成立；這不表示四個 xfail 已通過。

上述補查第一次只設定 `PYTHONPATH=src`，在成功完成尾端修剪／空軌跡檢查之後，匯入測試 helper 時報 `ModuleNotFoundError: test_ingest`；補上 worktree 內的 `tests` 後重跑。兩次「僅少 `stop_allow_s`」的過嚴格診斷斷言失敗，揭露 R1-F2；改以 CL-B1-8 真正允許的時間差範圍核對後通過。這些是 reviewer 的診斷程式修正，沒有修改受審檔案。

**C-2 的實際 module CLI**：設定 `PYTHONPATH=src` 後執行：

```text
python -m moto_copilot.ingest --gpx-dir .pytest_cache/r1-tmp/test_only_pace_entries_are_ope0/gpx --out .pytest_cache/r1-tmp/test_only_pace_entries_are_ope0/out
```

使用這次 pytest 生成的合成檔案與清單，exit 0：

```text
ingest ingest-b1-1 | curv-spike0-80-250 | pace trips: 2 | non-pace entries not opened: 2 | rows: 13
trip   points jumps jitter badtime      km  segs    ok  susp  inv  C1/C2/C3/null  stops false/short/long  note
T901      601     0      0       0     8.0     8     8     0    0  8/0/0/0  0/0/0
T904      451     0      0       0     5.0     5     5     0    0  5/0/0/0  0/0/0
contract check (private): OK
contract check (public): OK
contract check (pair): OK
```

C-2 所指 producer 缺少 `short_stop_time_s` 的缺口已在合成資料範圍解決；不將此結論擴張為真實 GPX 驗證。

### R1-F1 的最小重現方式

在上列完整範圍 pytest 執行後，以 `PYTHONPATH=src`、`python -` 執行以下程式。沒有新增測試檔，也沒有修改合成清單或寫出新輸出；只讀本次 pytest 的合成 GPX。

```python
import contextlib, io, json, sys
from pathlib import Path
from unittest.mock import patch
from moto_copilot.ingest import __main__ as cli
w = Path('.pytest_cache/r1-tmp/test_only_pace_entries_are_ope0')
target = (w / 'gpx' / 'pace_a.gpx').resolve()
opened = []
def audit(event, args):
    if event == 'open' and isinstance(args[0], str) and Path(args[0]).absolute() == target:
        opened.append(target.name)
sys.addaudithook(audit)
for role, requested in [('holdout', []), ('holdout', ['--trips', 'T901']), ('excluded', [])]:
    trips = [
        {'trip_id': 'T901', 'source_file': 'pace_a.gpx', 'trip_role': 'pace'},
        {'trip_id': 'T902', 'source_file': 'pace_a.gpx', 'trip_role': role},
    ]
    opened.clear()
    with patch.object(Path, 'read_text', return_value=json.dumps({'trips': trips})), \
         patch.object(Path, 'write_text', return_value=0), patch.object(Path, 'mkdir'), \
         contextlib.redirect_stdout(io.StringIO()):
        code = cli.main(['--gpx-dir', str(w / 'gpx'), '--out', str(w / 'out'), *requested])
    print(role, requested, code, opened)
```

另以 `python -` 做三類補查：

- 未知的非 pace 角色 `unrecognized`：自動選擇為空且 not-opened 計數為 1；明確指定其 ID 拋 `ManifestError`，通過。
- 將 CL-B1-10 合成軌跡的幾何與時間順序反轉，保持時間遞增，核對**尾端**修剪：完整事件 200 秒、範圍內 80 秒，分類為短停留；時間守恆與契約 1 均通過。原測試已核對前端。
- 空軌跡、單點、修剪後過短軌跡：均無衍生列且有明確 `report.note`。缺少來源檔的合成 manifest：不呼叫 GPX parser，印出 `source file not found`；現有行為是 exit 0 並在報告註記。沒有把這種局部缺漏註記當成來源成功重建的證據。

## Acceptance 與 evidence 逐項核對

下列 test names 未加路徑者均位於 `tests/test_ingest.py`；CLI 測試位於 `tests/test_ingest_cli.py`。PASS 僅指該列條件，整體 verdict 受 R1-F1 阻擋。

| 條件 | 自行核對的證據與結論 |
| --- | --- |
| Issue AC1／SB2-T1 | `test_sb2_t1_one_second_repeated_position_between_fast_steps_is_moving_time`（`:193`）：前後均 >20 km/h；1 秒只進 moving、length 不變、契約通過。PASS |
| Issue AC2／SB2-T2 | `test_sb2_t2_stops_of_2_3_179_and_180_seconds_are_classified_by_length`（`:211`）：2 秒進 moving；(stopped, short) 為 (3,3)、(179,179)、(180,0)，總 stopped 362、short 182。PASS |
| Issue AC3／SB2-T3 | `test_sb2_t3_short_stops_never_exceed_stops_and_times_add_up_to_the_trimmed_duration`（`:234`），含 jump、gap、假停留、短／長停留；每段 short ≤ stopped、總時間等於修剪後歷時。另有短尾合併測試（`:298`）。PASS |
| Issue AC4／SB2-T11 | CLI `test_a_requested_holdout_trip_is_refused_before_any_file_is_opened`（`:103`）：混合指定 pace、holdout，exit 2、GPX open 集合空、沒有輸出。此明確 ID 情境 PASS；整體來源隔離仍 FAIL（R1-F1） |
| SPEC-B1 §5：非 pace 項目不得開啟 | CLI `test_only_pace_entries_are_opened_and_the_result_passes_the_contract`（`:88`）、指定 pace 子集合測試（`:124`）及未知角色補查通過；但相同來源的角色衝突可繞過，FAIL（R1-F1） |
| SPEC-B1 §5：明確指定非 pace 時在任何 GPX 開啟前拒絕 | CLI holdout、excluded（`:112`）、未知 ID（`:118`）測試及未知角色補查，PASS；manifest 本身須先被讀取以判定角色，「任何檔案之前」依上下文指任何 GPX |
| SPEC-B1 §5：無清單拒絕、不建立暫定清單 | CLI `test_without_a_manifest_the_rebuild_is_refused_and_none_is_created`（`:130`），exit 2、無 GPX open、無清單／輸出。程式已移除 `_load_or_create_manifest` 與 GPX glob 掃描。PASS |
| CL-B1-3 item 1 | `segments.py:276` 保留 >10 s gap 的 <50 m／≥50 m 分流及非 gap 的 <3 km/h 判斷。移動 gap（測試 `:253`）及站立 gap 與相鄰停止步合成 200 s（`:263`）通過；未改停止判定 |
| CL-B1-3 item 2 | `allocate_stop_events`（`segments.py:216`）先加總連續停止步再分類、逐步分配；`test_an_event_across_a_segment_boundary_is_classified_once_and_split_by_time`（`:276`）對 200／4／2 s 跨段事件直接驗證。距離切段只在 moving step 結束，現行 build_rows 不會在連續停止步中切段；直接測試有合理的 coverage。PASS |
| CL-B1-3 item 3 | 假停留秒數在 `segments.py:307` 加進 moving，沒有加進 length；AC1／AC2 對列與總和確認。PASS |
| CL-B1-3 items 4、5 | 選擇／拒絕順序及無清單行為如上；item 4 存在 R1-F1；item 5 PASS |
| CL-B1-3 item 6 | `IngestParams` 的 3、180 秒欄位（`segments.py:37`、`:38`）、新版本 `ingest-b1-1`（`:44`）；`test_stop_thresholds_are_ingest_parameters`、`test_the_ingest_version_is_new` 通過。PASS |
| CL-B1-1、CL-B1-7 | 只用合成資料；既有測試修改理由在 E-4；未執行 experiments；新增程式／錯誤／worklog 沒有將保守估計稱為分位數、沒有官方警特報的正面宣稱。PASS |
| CL-B1-8 §3.2：S-1／S-2 恢復 | 併回原測試（`test_ingest.py:62`、`:145`），原斷言 AST 相同，不帶 xfail 通過；沒有消失的檢查。E-4 逐項交代；S-3～S-6 的 diff 空。PASS |
| CL-B1-9 | 最終 subject exit 0、只有 passed／xfailed、4 個 reason 均指 #10／#11；強制執行僅有 S-3～S-6 失敗，完整差異均在允許項目內。worklog §9.2 有完整一般／-rxX／--runxfail 輸出及中間計數更正。E-1 PASS，附 R1-F2 的敘述修正 |
| CL-B1-10 | `test_a_stop_event_cut_by_the_trim_is_classified_by_its_part_inside_the_trimmed_track`（`:312`）驗證 200 s 的整個事件在前端修剪後剩 80 s，分類依保留部分，範圍外不進欄位，時間守恆及契約通過；另做尾端對稱補查。PASS |
| E-1 | 自行重跑與 worklog 最終 253 passed／4 xfailed 一致；依 CL-B1-9 成立，不能稱全數通過 |
| E-2 | worklog §6、§9.3 列出 Issue AC、CL-B1-3、CL-B1-10 對應測試名稱與結果；已逐項執行並讀斷言。新增發現的 R1-F1 未被既有測試涵蓋，須補 regression |
| E-3 | `test_ingest.py:17`、`:18`、`:21`、`:169` 與 CLI test `:21`、`:22`、`:46`、`:69` 明確產生虛構原點、時間、直線／圓及行程清單；既有 fixture 明載 mock。沒有真實資料 diff |
| E-4 | 只有 S-1／S-2 併回；理由、原斷言去向與保留方式記在 worklog §6。沒有其他既有測試語義修改 |
| E-5 | worklog §6、§9.4 有 H-2／H-3／H-4 self-verification。已獨立核對如下；其隔離全面成立的主張被 R1-F1 推翻，須修正後重驗 |

## 高風險最低核對

| 類別 | 核對與結論 |
| --- | --- |
| H-2 | git index 違禁 path 計數為 0；diff、fixture、worklog 與本次 evidence 的位置／時間可追溯為合成；無新第三方請求。既有起訖各 2000 m 的裁切測試、公開版移除 start_time 及兩版配對檢查通過，CL-B1-10 前／後端補查通過。未新增錨點代換或外送路徑，該部分不適用本票。檔案角色隔離 **FAIL：R1-F1**；真實騎乘資料核對 NOT VERIFIED |
| H-3 | pytest 與 CLI 證據自行執行，沒有將 xfail 記為 PASS、沒有將技術測試寫成 E1／E2。中間計數的更正在 worklog §9.2 可追溯；CL-B1-7 用語符合，R1-F2 是摘要精度 follow-up。凍結前沒有開啟 holdout 的全面主張 **FAIL：R1-F1** |
| H-4 | moving／stopped／short 的計算與總時間測試通過；`segments.py:318`、`:331` 未以 0 偽裝無有效 moving 的資料；空／單點／過短輸入補查均無列且有 note，jump／recording gap 的 suspect 舊測試通過。無 manifest、壞 manifest、未知 ID、明確非 pace ID 均有拒絕且無 GPX open 的測試。缺少 GPX 有明確缺檔 note；不得視為該來源重建成功。Planner 改寫、規則 5、路線採用、外部 API 逾時與過期快取不在本票路徑，不冒充已測。本票清單角色衝突的 fail-closed 防線仍須 R1-F1 修正 |

## NOT VERIFIED、authority 與後續

- **NV-1／C-9-3**：真實行程清單的角色、真實 GPX 重建是否符合契約、私有保留行程實際隔離與真實配速回歸均 **NOT VERIFIED**。原因是本票排除真實重建，且沒有 RB-7 授權；required authority = **acceptor**。未讀取或嘗試取得資料。C-2 的合成範圍已驗證，不以 NV-1 冒充 C-2 未處理，也不把真實結果標 PASS。
- **NV-2／binding adoption**：本次精確 Codex model／effort／sandbox 的 rollout 全程核對、session id 與 record hash，依 Bindings §3.3 由 **dispatcher／Orchestrator** 補入 run record §6 事件 8。本 reviewer 不存取 worktree 外的 rollout；在此之前沒有 model diversity claim。這是採用本 return 的必要核對，非要求讀取私有騎乘資料。
- **C-9-4／AB-12**：新流程需先有 manifest 的文件工作維持追蹤，owner 為之後 AB-12 文件 work item；不擴張 #9 為建立清單／介面上傳。
- S-3 由 #10、S-4～S-6 由 #11 恢復；SPEC-B1 的無 xfail 要求仍有效。本票沒有執行 SIA、沒有宣告 Spec closure、phase acceptance、OC-1 完成或 release authorization。
- 本輪需要 #9 Executor 對 R1-F1 作 targeted correction，再由 Primary 執行 R2。沒有因真實資料未驗證而要求解除 RB-7，也沒有未決的 measurement 語義由 reviewer 自行補定。

Verdict: BLOCKING
