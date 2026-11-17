# Issue #9 — cycle 1 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）→ Issue #9「B1-2 ingest」 |
| 適用 clarification | CL-B1-1、CL-B1-3、CL-B1-7；`decision-20261117-issue7-spike-tests.md` 的 CL-B1-8；`decision-20261117-issue9-e1-and-trim.md` 的 CL-B1-9、CL-B1-10 |
| Subject | 本專用 worktree，detached HEAD `09d150f0f7db34b3f46790a54e167b7f617a2fac`；BASE `0c109aaba8c8460cebea5336840cc1d556d88a71` |
| R1／correction | R1 subject `f0b5be902c9cf1775c04b8f42c88a9c6572227e3`；correction `6f975619a2e4b6303064955237c254de19f81da5`，只改 `src/moto_copilot/ingest/__main__.py`、`tests/test_ingest_cli.py`；R1 之後其餘 commits 僅改 `docs/governance/records/**` |
| Audit kind | **Ticket independent audit，R2 closure review，cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`，Codex |
| 日期／治理 | 2026-11-17；Minimal Operational Governance v2.2、Bindings m3、impl-default v2、orch-default v2.2 |
| Issue 版本 | 本次 pack 附的原文；其 SHA-256 識別 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895` 與 first-run derivation BD-3 的 #9 列相符。沒有呼叫 GitHub 或網路查核遠端版本 |

## Independence 與 model assurance

| Assurance | 滿足方式與證據邊界 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread，沒有繼承 Executor 或 R1 對話。從磁碟重讀 `issue-9-c1-r1.md`、修正後程式、測試及 worklog §10；自行形成結論，不把 Executor 的 closure 主張當成證據 |
| Verifiable binding | 本次 dispatch 是 `docs/governance/records/run/run-20261117-oc1-run2.md` §6 **事件 10**（檔案第 92 行），宣告 Codex `gpt-6.1-sol`／`high`。Bindings §3.3、§8.2 記載 O-6 qualification 已通過。事件 10 在受審 HEAD 仍為「進行中」；dispatcher 須在採用本 return 前將本次全部 turn_context 的 model／effort／sandbox、session 識別、存取核對及 record SHA-256 補入此事件。本 reviewer 不讀取 worktree 外 rollout，也不以宣告 mapping 冒充已完成的實際 binding 核對 |
| Autonomous access | 自行取得 worktree 內契約、原始碼、diff、歷史與測試，另執行 R1 最小重現及修正直接涉及的 Windows 檔名等價檢查。沒有讀取、列出或搜尋私有資料，沒有存取憑證、其他 checkout 或 worktree 外專案路徑，沒有執行 experiments、網路服務或 subagent |
| Self-written record | 本 reviewer 直接撰寫此 record；沒有修改 implementation、tests、contracts、gates 或其他治理紀錄，沒有 stage／commit。只有此新增 audit record 及允許的、已忽略 pytest cache。dispatcher 仍須核對並原樣採用，不能代寫結論 |
| Actual models／diversity | Executor：run record §6 事件 9 記 agentId `a6f915a1860417bc9`，143 則 assistant 訊息觀測為 `claude-opus-5-5`／`high`；事件 2、7 分別有 99、118 則的相同觀測。本 Primary 是 **Codex**，本次精確 model 的實際 rollout 證據由 dispatcher 補入事件 10；不挪用事件 8 的 R1 binding 作為本輪證據。**no model diversity claim**，Bindings §5 也沒有宣告 diversity 關係 |

四項 independence 依上述機制執行；正式採用仍須完成 dispatcher 所負責的 binding／存取／hash 核對，不由 reviewer 自述取代。

## R1 findings 的 closure 狀態

| Finding | 原 severity | 狀態 | 本輪結論／disposition |
| --- | --- | --- | --- |
| R1-F1 | High／blocking | **NOT RESOLVED** | 原始三個重現及大小寫情境已拒絕，新增測試也通過；但同一來源的角色隔離仍可由 Windows 預設資料串流名稱繞過，見 R2-F1。不是對 R1 的全然未修正，也不是完整 closure |
| R1-F2 | Low／non-blocking | **RESOLVED** | worklog 第 98、305、362、471 行已說明缺少 `stop_allow_s` **及隨它改變的 `eta_typ`／`eta_safe`**，保留原測試輸出。本輪重新逐列核對成立。Required fix 已完成；owner＝#9 Executor，Orchestrator 可據此更新追蹤，不延長 cycle |

## Finding R2-F1 — High／blocking：R1-F1 的來源角色隔離仍可由預設資料串流名稱繞過

**契約依據。** CL-B1-3 item 4、SPEC-B1 §5 的 #9 列、`DESIGN.md:377` 的凍結前隔離要求，以及高風險 decision §5 的 H-2／H-3。這是 correction 的來源比較防線直接暴露的同一 root cause，屬治理 §4.4 的 R2 範圍。

**程式證據。** `src/moto_copilot/ingest/__main__.py:62` 的 `source_key` 只做最後成分、NFC、結尾句點／空白及 casefold；第 80 行用該鍵比對角色。`pace_a.gpx` 與 `pace_a.gpx::$DATA` 因而得到不同鍵。第 131 行的 `Path(name).name != name` 沒有拒絕後者；第 135–138 行會通過 `is_file` 並實際呼叫 GPX parser。

**本機獨立核對。** 僅使用這次 pytest 在 `.pytest_cache/r2-tmp/test_only_pace_entries_are_ope0/gpx/` 產生的合成檔，沒有建立額外 stream、連結或另一份 GPX：

```text
SYNTHETIC_DEFAULT_STREAM is_file True samefile True same_bytes True
PARSER_POINTS 601 601
STREAM_KEYS pace_a.gpx pace_a.gpx::$data
```

上述 `Path.samefile`、位元組比較與 parser 點數只針對允許的合成測試檔。在本工作環境，兩個名稱確實開啟同一檔案的同一資料，並非兩份內容偶然相同的檔案。

以真實 `load_manifest`、selection、GPX parser、`build_rows` 與 validators 執行，只 mock manifest 讀回的 JSON 及最終輸出寫入，用 audit hook 觀察實際 GPX open：

```text
DEFAULT_STREAM holdout explicit=False exit=0 actual_open=['pace_a.gpx::$DATA'] rows=8 writes=2
DEFAULT_STREAM holdout explicit=True  exit=0 actual_open=['pace_a.gpx::$DATA'] rows=8 writes=2
DEFAULT_STREAM excluded explicit=False exit=0 actual_open=['pace_a.gpx::$DATA'] rows=8 writes=2
DEFAULT_STREAM excluded explicit=True  exit=0 actual_open=['pace_a.gpx::$DATA'] rows=8 writes=2
ingest ingest-b1-1 | curv-spike0-80-250 | pace trips: 1 | non-pace entries not opened: 1 | rows: 8
```

`writes=2` 是被攔截的輸出呼叫數，不是實際寫入私有資料的宣稱。清單將 T901（pace）指向 `pace_a.gpx::$DATA`、T902（holdout 或 excluded）指向 `pace_a.gpx`；自動選擇及 `--trips T901` 都產生 pace 列，仍把同一來源宣稱為 non-pace not opened。

**最小重現命令。** 先執行本 record 的完整範圍 pytest，使下列合成 fixture 存在；PowerShell 設 `PYTHONPATH=src` 後以 here-string 傳入 `python -`：

```python
import contextlib, io, json, os, sys
from pathlib import Path
from unittest.mock import patch
from moto_copilot.ingest import __main__ as cli
w = Path('.pytest_cache/r2-tmp/test_only_pace_entries_are_ope0')
folder = (w / 'gpx').absolute()
opened = []
def audit(event, args):
    if event == 'open' and isinstance(args[0], (str, bytes, os.PathLike)):
        p = Path(os.fsdecode(args[0])).absolute()
        if p.parent == folder:
            opened.append(p.name)
sys.addaudithook(audit)
for role in ['holdout', 'excluded']:
    for requested in [[], ['--trips', 'T901']]:
        trips = [
            {'trip_id': 'T901', 'source_file': 'pace_a.gpx::$DATA', 'trip_role': 'pace'},
            {'trip_id': 'T902', 'source_file': 'pace_a.gpx', 'trip_role': role},
        ]
        opened.clear()
        with patch.object(Path, 'read_text', return_value=json.dumps({'trips': trips})), \
             patch.object(Path, 'write_text', return_value=0) as writes, \
             patch.object(Path, 'mkdir'), contextlib.redirect_stdout(io.StringIO()):
            code = cli.main(['--gpx-dir', str(folder), '--out', str(w / 'out'), *requested])
        rows = json.loads(writes.call_args_list[0].args[0])['derived_segments'] if writes.call_count else []
        print(role, requested, code, opened, len(rows), writes.call_count)
```

**Required fix／owner。** #9 Executor 應使 manifest 可接受的來源名稱與開檔語義一致，在任何 GPX 開啟前拒絕這類角色矛盾或不支援的 Windows stream 語法；可採名稱驗證而不讀取／stat／雜湊非 pace 檔案。以合成資料補自動與明確選擇、holdout 與 excluded 的 regression evidence：exit 2、無 GPX open、無輸出列，並更新 H-2／H-3 evidence。這不要求內容去重複、私有資料存取或實作 Profile 上傳。

**Disposition。** 未解，不 defer。worklog §10.1、C-9-5b 所列連結／8.3／不同檔名內容去重複的殘餘，沒有處置本次已重現的同一檔案 stream 語法；單純記錄限制不會改變 accepted 隔離要求。本 finding 沒有主張任何真實資料已被讀取或外洩。R2 仍 blocking，下一步由 **Orchestrator** 依治理 §4.4 派 **exactly one Alternate Independent Review**；本 reviewer 不執行修正、不開 R3。

## 執行範圍、命令與結果

本輪重讀 root `CLAUDE.md`、Bindings m3（含 O-6／§3.3、§5、§7、qualification）、`.claude/agents/gov-primary-reviewer.md`；治理本文 §2.3、§3.8、§4.1–§4.7，impl-default §6–§7，orch-default §6–§7；OC-1、SPEC-B1、first-run derivation 的 BD-3／G-ING／G-REG／AB 分配、高風險 decision §5、CL-B1-8／9／10；run record §6 事件 8–10、R1 record、#9 correction worklog 及 #7 的 C-2。另核對 `DESIGN.md` §5、§6.1、SPEC-RESOLUTION-001 停等及隔離段落、SPEC-001 §2、BATCH-1 共通規則與 B1-2。這些是 closure 與 regression 的上下文，不是另做一次完整 R1 或 SIA。

| 命令／檢查 | 結果 |
| --- | --- |
| 明確路徑的 `Get-Content -Encoding UTF8 -LiteralPath ...`、`rg -n ...`，必要時 `Select-Object` 擷取章節 | 讀取上述材料、完整修正後 CLI 與 CLI tests、pytest 設定與 fixture 定義。初次 PowerShell 預設編碼輸出不清，後續已以 UTF-8 重讀；未從 repo root 作文字搜尋 |
| `git rev-parse HEAD`、`git rev-parse 0c109aa` | 與檔首 subject 相符 |
| `git log --oneline 0c109aa..09d150f`、`git log --format='%h %s' --name-only f0b5be9..09d150f`；Python 呼叫 `git rev-list`／`git diff-tree` | BASE 後 10 個 commits；R1 後 4 個 commits，只有 `6f97561` 修改兩個產品／測試檔，其餘 record-only |
| `git diff f0b5be9..09d150f -- src tests`；`git diff 0c109aa..09d150f`（亦由 Python 取得完整 diff 核對路徑）；各相關檔案的限定 diff；`git diff --stat`／`--numstat 0c109aa..09d150f` | BASE 後 8 個變更路徑、1453 additions／68 deletions。逐項閱讀 correction、既有產品／測試差異及相關 evidence；沒有 correction 以外的產品擴張 |
| `git diff f0b5be9..09d150f -- src/moto_copilot/ingest/segments.py tests/test_ingest.py` | 空；停止分類、修剪與原有 ingest 測試在 correction 中未改 |
| `git diff 0c109aa..09d150f -- tests/test_routes_pace_eta.py tests/test_contracts.py tests/conftest.py pyproject.toml` | 空；S-3～S-6 與 gates 沒有被改動 |
| `git diff --check 0c109aa..09d150f -- src tests` | 無輸出，exit 0 |
| `rg -n 'xfail\|skip' tests` | 恰好 4 個 strict xfail，位於 `test_routes_pace_eta.py:117`、`:159`、`:173`、`:182`；reason 分別為 restored by #10、#11、#11、#11；沒有 skip 或 restored by #9 |
| `rg -n 'data/\|data\\\|dotenv\|requests\|httpx\|urllib\|subprocess\|socket' tests` | 無命中；另讀 `tests/conftest.py`、CLI fixture 生成方式，確認只用 mock／合成資料 |
| `python -`：`git ls-files -z` 只在記憶體計數禁止 pattern，不輸出檔名 | `.env`、`*.key`、`*.gpx`、`*.fit`、`data/` 的 tracked path 數皆為 0；沒有開啟這些路徑 |
| `python -`：AST 比對 BASE 的 S-1／S-2 與現行原測試 | 分別 4、3 個原斷言全部保留，無 decorator；一般與強制測試均通過。沒有只移除 xfail 卻遺失檢查 |
| `python -`：R1 最小重現，僅將 fixture 暫存根改為本次 r2-tmp | holdout 自動、holdout 明確 T901、excluded 自動，均 exit 2、actual_open=[]、rows=0、writes=0；另補自動／明確的大小寫等價情境也相同 |
| 同一 `python -`：針對修正 `source_key` 的 Windows stream 等價檢查；另以 `Path.is_file`／`samefile`／`read_bytes` 及真實 parser 核對合成檔 | 實際繞過與同一檔案證據見 R2-F1；沒有 mock GPX parser、build_rows 或 validators |
| `python -`：以現行 `test_routes_pace_eta.eta_for` 與 mock fixture 逐列比較 S-4 | 差異鍵只限 stop_allow_s／eta_typ／eta_safe；典型時間差為 0、9、27、27 秒，保守時間差為 0、11、32、32 秒，與累計 allowance 及其 1.2 倍（容許 1 秒）一致。Header 與 fixture 相同，R1-F2 的修正文句正確 |

### 指定 pytest 與 regression evidence

全部使用 PATH 上的 `python`，工作目錄始終是本 worktree；沒有使用 `.venv`。為使合成 GPX 與 `tmp_path` 不落到 worktree 外，先建立 `.pytest_cache`，設定：

```powershell
$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/r2-tmp'
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
```

| 指令 | 實際結果 |
| --- | --- |
| `python -m pytest -q` | `265 passed, 4 xfailed in 1.25s` |
| `python -m pytest -q -rxX` | `265 passed, 4 xfailed in 1.20s` |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py` | `4 failed, 41 passed in 0.51s` |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py`（CL-B1-9 完整範圍） | `4 failed, 67 passed in 0.90s`；該批 shell 最終 exit 1 |

一般測試完整輸出：

```text
........................................................................ [ 26%]
........................................................................ [ 53%]
........................................................................ [ 80%]
...........................................x....x.xx.                    [100%]
265 passed, 4 xfailed in 1.25s
```

兩次 `--runxfail` 失敗都恰好是以下四個，與 `-rxX` 的清單相同：

| 測試（`tests/test_routes_pace_eta.py`） | reason／失敗內容 |
| --- | --- |
| `test_pace_table_matches_the_mock_fixture__v03_contract` | restored by #10；缺 margin_coeff、margin_basis、stop_ratio，第一個錯誤是 margin_coeff required |
| `test_eta_reproduces_the_mock_fixture__v03_contract` | restored by #11；缺 stop_allow_s 及隨它改變的時間值；全部列差異另已核對 |
| `test_eta_is_unknown_when_a_category_has_no_pace__v03_contract` | restored by #11；兩列缺 stop_allow_s |
| `test_eta_output_passes_the_contract_with_and_without_breaks` | restored by #11；缺 stop_allow_s，並有契約 4 的 null time although status is ok 訊息 |

四個 reason 都以 `v0.3 producer gap (decision-20261117-issue7-spike-tests)` 開頭；不是通過。與 R1 evidence、未改動的 producer／測試及本輪逐列核對一致，沒有發現 correction 被 xfail 遮住的新回歸。CL-B1-9 的 E-1 條件成立；它不能證明新增 manifest 防線完備，也不覆蓋 R2-F1。

本次全部 26 個 CLI 測試（原 14＋新增 12）及停止分類、時間守恆、CL-B1-10 修剪邊界測試均包含在上述執行，沒有其他失敗。新增參數化測試 `tests/test_ingest_cli.py:188` 起的 10 例涵蓋相同名稱、大小寫、結尾句點／空白、兩種分隔符；第 222、232 行起另驗 loader 拒絕及正常清單。它們沒有涵蓋本輪重現的 stream 語法。沒有重新執行 Executor 所稱的 source mutation 測試，該歷史執行主張 **NOT VERIFIED**；本輪 closure 判斷採自行重現與 regression evidence。

### C-2：實際 module CLI（合成資料）

設定 `PYTHONPATH=src`，執行：

```text
python -m moto_copilot.ingest --gpx-dir .pytest_cache/r2-tmp/test_only_pace_entries_are_ope0/gpx --out .pytest_cache/r2-tmp/test_only_pace_entries_are_ope0/out
```

exit 0；重建 2 個 pace 行程、13 列；non-pace entries not opened 為 2，private／public／pair 三項 contract check 均為 OK。`test_only_pace_entries_are_opened_and_the_result_passes_the_contract` 另斷言列有 `short_stop_time_s`、角色只有 pace、violations 皆空。故 #7 worklog §8／§10 的 **C-2 producer 欄位缺口在合成範圍已處理**；這與來源隔離仍有 R2-F1 是兩項不同結論，不能互相取代。

## H-2／H-3／H-4 與 correction 的影響

| 類別 | 本輪核對結論 |
| --- | --- |
| H-2 | 新增測試及本輪重現來源可追溯為測試函式生成的合成 GPX；tracked 禁止 path 計數為 0，correction 沒有新增第三方呼叫或修改裁切／公開版轉換。一般隱私與契約 regression 通過；**來源角色隔離仍 FAIL（R2-F1）**。真實資料 NOT VERIFIED |
| H-3 | Executor 已註明 R1 推翻舊版隔離主張，R1-F2 的描述已修正；一般／xfail 計數與 evidence 相符，沒有將測試寫成 E1／E2。自動及明確選擇的原重現已拒絕，但 **凍結前不開啟非 pace 的防線仍 FAIL（R2-F1）**；worklog §10.4 的名稱範圍限定不等於 accepted contract 的例外 |
| H-4 | 普通矛盾清單在 loader 階段 exit 2，沒有部分 GPX 重建；正常清單及既有缺漏／拒絕測試通過。停止分類、缺值及 quality 路徑沒有 correction delta，相關測試均通過。stream 矛盾仍得到 exit 0／pace 列，屬本次同一 fail-closed 缺口。沒有將 Planner、外部 API 或其他本票未涉及路徑說成已驗證 |

C-9-6 的「整份矛盾清單拒絕」是修復隔離的 fail-closed 行為，沒有觀察到需另補語義才能作本輪判定的問題；不將這項 concern 變成新 AC。C-9-5b 中其他連結／短檔名情境本輪未做擴充全面審查，也未宣告已解決。

## 執行完整性、NOT VERIFIED 與後續 authority

- 所有測試與診斷都在本 worktree 內；診斷程式由 stdin 執行，未建立額外腳本。唯一新增治理檔是本 record。沒有修改、stage 或 commit 任何 tracked 檔案。
- `git status --short` 曾顯示測試產生的 `.pytest_cache/` 未被忽略。以已核對絕對路徑的 PowerShell `Remove-Item -Recurse -Force` 清理 cache 的命令被執行政策拒絕，**NOT RUN**；沒有改用其他刪除工具。改在 cache 內寫入標準用途的 `.gitignore`（`*`）保留允許的測試暫存，`git status --short --ignored -- .pytest_cache` 顯示 `!! .pytest_cache/`，一般 status 恢復為空。這不修改 repo 的 `.gitignore`。
- **NV-1／C-9-3**：真實清單、真實 GPX 重建／回歸、真實 holdout 隔離均 **NOT VERIFIED**；本票排除真實重建且沒有 RB-7 授權。required authority＝**acceptor**。沒有嘗試取得私有資料；不把合成繞過證據寫成真實外洩。
- **NV-2／binding adoption**：本輪完整 rollout 的精確 model／effort／sandbox、存取紀錄、session 識別與 record hash 核對由 **dispatcher／Orchestrator** 補入 run record §6 事件 10。受審版本尚無此核對結果，不能以 R1 的完成欄位代替。
- **NV-3**：Executor 在 worklog §10.1 所稱暫時移除呼叫／弱化 source_key 的歷史 mutation 執行未自行重做，屬 **NOT VERIFIED** 的歷史 self-verification 主張；本輪不依賴它，不需私有資料授權。
- **AB-12／C-9-4** 文件工作維持原 owner；S-3 由 #10、S-4～S-6 由 #11 恢復，SPEC-B1 的無 xfail 要求維持。沒有宣告 Spec closure、phase acceptance、OC-1 完成或 release authorization。
- **本輪後續**：R1-F2 已解；R1-F1 尚未完全解決，以 R2-F1 識別殘餘 blocking evidence。required authority＝**Orchestrator**，派 exactly one Alternate Review；若對 finding 的設計語義有爭議，依治理 §4.3／§4.5 先 route **Design Authority**，不由 reviewer 改契約。
- 寫入後核對：`git status --short` 只有 `?? docs/governance/records/audit/issue-9-c1-r2.md`；`git diff --exit-code`、`git diff --cached --exit-code` 均 exit 0，cache 顯示 ignored。另用 `Get-FileHash -Algorithm SHA256` 產生交付 hash、`Get-Content ... | Select-Object -Last 1` 核對最後一行，並以限定路徑 `rg -n` 核對 source／test 行號；最終 hash 由 dispatcher 對交付檔計算並記入事件 10。

Verdict: BLOCKING
