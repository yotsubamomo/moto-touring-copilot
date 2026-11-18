# Issue #15 — cycle 1 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-R1 v1（`derivation-spec-r1.md` §2、§4，含 CL-R1-1／CL-R1-10；§5 R1-3 與 E-1～E-6）＋CL-R1-13（`decision-20261118-issue13-c131.md`）＋CL-R1-14／CL-R1-18（`decision-20261118-issue14-c141.md`）＋CL-R1-22～24（`decision-20261118-issue15-c151.md`）→ Issue #15 |
| Subject | 本專用 worktree 的 detached HEAD `48ff3502a059cf4652b4b913344886e905d57102`；BASE `201e3e364767bb03ce1d2aa2e3a443bd4a838eb6` |
| Audit kind | **Ticket R2 closure review，cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`（Codex，Bindings m3 O-6） |
| 日期 | 2026-11-18 |
| R1 與 correction | R1 subject `3d49cef97617ea7467fe0da626ade4e96e939608`；R1 record `docs/governance/records/audit/issue-15-c1-r1.md`；targeted correction `efbffe8`；worklog §10 的 commit `2e53f0a` |
| Issue 識別 | 採派工提供的原文，SHA-256 `a54f8034cdadd143e6a1ec594ee7d74e01bb47ce9bc13bd21537bbcf92fd5ad7`；run record §4 同值。本次沒有 GitHub 或其他網路呼叫 |

## Assurance

| Assurance 欄 | 滿足方式與證據界限 |
| --- | --- |
| (a) Independent context | 本次是 fresh Codex thread，沒有 Executor 或 R1 Reviewer 的對話 context。從磁碟重讀 R1 record、修正後的 reader／routing／測試及 correction diff；Executor 的 DONE、PASS、突變結果均視為待驗證主張 |
| (a) Verifiable binding | 依 Bindings §3.3，由 dispatcher 核對本次 rollout 的全部 `(model, effort, sandbox)`、thread、存取紀錄與 record SHA-256，記入 `run-20261117-oc1-run2.md` §6 的**本次 #15 R2 dispatch event**。本 HEAD 的事件目前只到 85（行 163）：84 是 R1 dispatch，85 是 Executor correction；**尚無本次 R2 event，不能引用不存在的事件號，也不能以 84 冒充 R2 binding**。本次 event 應在 85 之後由 dispatcher 補錄；見 NV-BIND |
| (a) Autonomous access | 自主讀取 worktree 內的契約、原始碼、測試、git 歷史與差異；自行執行兩組完整 pytest、AST／index 檢查及獨立內容與例外探測，不限於 worklog 摘要。沒有 subagent，沒有存取 worktree 外路徑、私有資料或憑證 |
| (a) Self-written record | 本 record 由此 Codex thread 自寫，是唯一新增檔案。Dispatcher 須依 Bindings §3.3 核對最後 status，原樣複製並比對 SHA-256；Executor 不代寫或改寫。本 record 不修改 worklog／run record |
| (b) 實際 models／model diversity | Executor：run record §6 事件 85，agentId `ae0a2f33f0da61e65`，dispatcher 觀測全部 129 則 assistant 訊息為 `claude-opus-5-5`／`high`。Primary：本 reviewer 是 **Codex**；Bindings 與 run record 宣告的 Codex mapping 是 `gpt-6.1-sol`／`high`，但當次精確 runtime binding 須由 dispatcher 依本次 rollout 建立，本快照尚未提供。**no model diversity claim**；不以先前 R1 的觀測替代本次證據 |

## Findings 與 closure 判斷

### R1-F1 — RESOLVED

- **原 severity：Medium／blocking；本次狀態：RESOLVED，無剩餘 blocking。Owner：#15 Executor。**
- 契約依據：CL-R1-23 第 1、5 項、CL-R1-10 第 7 項、R1-3 範圍 (a)–(b)、SPEC-001 4.13／5.5、H-2／H-4。無法解碼或解析的檔案內容須回固定錯誤；caller type error 保留原語義。
- **R1 required fix**：在 XML 解析邊界把未知 encoding 等不可解析內容轉為固定 `GpxGeometryError(UNREADABLE)`，不附 parser 訊息，`__context__`、`__cause__` 均為 `None`；bytes／path、兩種 trip type 回 `TargetGpxError('target_gpx_invalid', 'unreadable')`，不產生路線或路徑／檔名／log／例外鏈外流；保留 caller errors，不改 #9 reader，重跑 gates。
- **修正證據**：`src/moto_copilot/ingest/geometry.py:38` 的 `_UNPARSEABLE = (ET.ParseError, ValueError, LookupError)` 只保護行 93 的 `ET.fromstring(data)`。行 87 的 bytes／bytearray 型別檢查仍在 try 外；行 98 在 except 外建立固定錯誤。`routing/target_gpx.py:116`、`:127` 的兩個入口仍只轉換 `GpxGeometryError`，沒有擴張捕捉範圍。
- **回歸證據**：`tests/test_target_gpx.py:865` 直接證明 bare parser 對未知 encoding 拋 `LookupError`；行 872、885、897 分別核對固定 reader error、bytes 入口、path 入口與兩種 trip type，包含無 route、無 chain／parser text／path／log。行 914 保留 caller errors；行 927 證明有效 encoding 照常讀取。全部包含在本次兩組完整測試。
- **獨立重現與反證**：20 種合成輸入、60 次 reader error、240 次 route error 均符合 required fix；記憶體中暫時移除捕捉 tuple 的 `LookupError` 即重新得到 R1 的 `LookupError`，finally 恢復。修正與測試能區分原缺陷；詳見下節。
- **catch 不是 catch-all**：獨立注入 7 類程式／資源例外，reader 與 bytes routing 共 14 次均以原例外物件向上傳遞；沒有被轉為成功、route error 或固定內容錯誤。`LookupError` 包含其子類別，但捕捉位置限於已確認為 bytes 的單一標準庫解析呼叫，沒有包住選點、路線採用或 caller validation。
- **Required fix 的 closure**：上述要求已全部解決，無剩餘修正要求。沒有發現 correction 直接產生或暴露的新 blocking defect。

本次沒有新增 blocking 或 non-blocking finding；沒有需要新增 disposition／owner 的 non-blocking 項目。既有限制與其他 authority 的事項另列，不重開 R1 全面審查。

## 範圍、材料與實際檢查

本次依治理 §4.4 只審 R1-F1 closure、correction regression 與 correction 直接產生／暴露的 blocking defect。沒有重做 Ticket 全範圍 R1、Spec Integration Audit 或 phase acceptance。

以 `Get-Content -Encoding utf8 -LiteralPath <明確檔案>`（部分搭配 `Select-Object`）與 `rg -n <pattern> <明確檔案／目錄>` 自行讀取／定位：

- `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3，尤其 §3.3 與 records／assurance 要求。
- 生效 package 的治理本文 §2.3、§3.8、§4.1～4.7；Implementation Profile §6～7；orch-default v2.2 §6～7。
- OC-1 的授權與 AB-2／AB-10／AB-13；SPEC-R1 §2、§4 CL-R1-1／CL-R1-10、§5 R1-3 與 E-1～E-6；first-run derivation 的適用性與 boundary。
- 指定的三份 2026-11-18 DA decision records 中 CL-R1-13／14／18／22～24、C-15 §2.4／§4，以及 high-risk decision §5。
- DESIGN §5 相關段落；SPEC-001 §2、4.12／4.13、5.5、7.11 第 2 項及 S10／S27／S43／S58～S64／S78～S80。
- R1 record（含 required fix、evidence、NOT VERIFIED）；run record 的指示、事件 81～85；worklog correction §10 與相關 evidence。
- 修正前後的 `geometry.py`、未變的 `target_gpx.py`、exports；合成測試產生器、privacy／caller／network／wording 測試與新增 regression cases。

| 指令／檢查 | 本次實際結果 |
| --- | --- |
| `git rev-parse HEAD`；`git rev-parse 201e3e3`；`git status --short` | HEAD／BASE 如表頭；起始 status 為空 |
| `git log --oneline 201e3e3..48ff350`；`git log --format='%h %s' 3d49cef..48ff350` | overall implementation commits 是 `b771d9f`、`e78cc9f`、`efbffe8`；R1 後四個 commits 中只有 `efbffe8` 改實作／測試，其餘只改 records |
| `git diff --stat 201e3e3..48ff350`；`git diff --numstat 201e3e3..48ff350` | 8 檔，2311 insertions、3 deletions；實作／測試為 geometry、target_gpx、routing exports、test_target_gpx；其他只在 records |
| `git diff 3d49cef..48ff350 -- src tests`；`git diff --name-status 3d49cef..48ff350`；`git diff --numstat 3d49cef..48ff350` | correction 只改 geometry 的解析 catch（11 additions／1 deletion）與 test_target_gpx 新增 97 行；另有 R1 record、run record、worklog 的 records delta |
| `git diff 201e3e3..48ff350 -- src/moto_copilot/routing/__init__.py` | 既有 exports 保留；增加 target GPX exports，correction 沒有再改 |
| `git diff --exit-code efbffe8..48ff350 -- src tests` | exit 0、無輸出；gates 覆蓋的 HEAD 與 correction 的程式／測試相同 |
| `git diff --exit-code 201e3e3..48ff350 -- src/moto_copilot/ingest/gpx.py src/moto_copilot/ingest/segments.py src/moto_copilot/ingest/__init__.py tests/test_ingest.py tests/test_ingest_cli.py` | exit 0、無輸出；#9 reader、幾何基礎與既有 ingest tests 未改 |
| `git diff --exit-code 3d49cef..48ff350 -- src/moto_copilot/routing` | exit 0、無輸出；correction 沒有改 routing／選點／採用條件 |
| `git diff --check 201e3e3..48ff350` | exit 0，無 whitespace error |
| `rg -n 'xfail\|skip' tests/` | 只有 `tests/test_contracts.py:1157` 的普通 docstring `skipped` 與 `tests/test_routing_store.py:330` 的測試名稱 `being_skipped`；不是標記 |
| `@' ... '@ \| python -`：對 `tests/**/*.py` 作 AST Attribute 檢查 `xfail/skip/skipif/importorskip` | `test skip/xfail AST markers: []`；結合文字搜尋與完整 pytest 結果，確認沒有 xfail／skip markers |
| 同一 stdin 檢查：以 `git show 3d49cef:tests/test_target_gpx.py` 與 HEAD 的 AST 比較既有 test functions | 既有 64 個 test functions，removed `[]`、changed `[]`；新增 6 個 test functions。Diff 另新增 `_declared` helper，共 7 個函式，parametrization 增加 53 個 cases |
| 同一 stdin 檢查：`subprocess.check_output(['git','ls-files','-z'])`，只輸出禁止樣式命中數 | `*.gpx`、`*.fit`、`.env`、`.env.*`、`*.key`、`data/raw/*`、`data/private/*`、`data/bmw/*` 全部 0；只查 index metadata，沒有列出或讀取私有目錄 |
| `python -m pytest -q`；`python -m pytest -q -rxX` | 各 exit 0，均 1678 passed；完整輸出如下 |
| `git status --porcelain`（兩組測試後、獨立 probe 後、寫本 record 前） | 無輸出，工作目錄乾淨；ignored caches 不屬 subject delta |

所有命令在本 worktree 執行；Python 一律用 PATH 的 `python`，沒有直接引用或檢視環境目錄，沒有覆寫 `PYTEST_DEBUG_TEMPROOT`。沒有建立 probe script 或 GPX；path probes 以記憶體替身供應內容。Pytest 自己的合成檔案使用其既定 `tmp_path`。

## 獨立 closure／regression probe

實際命令是 PowerShell here-string `@' ... '@ | python -`，`sys.path.insert(0, 'src')`；以 `runpy.run_path('tests/test_target_gpx.py')` 取得合成產生器與 10 種 `UNPARSEABLE` 輸入，再加：`utf-7`、`utf-32`、`undefined`、`bz2_codec`、`quopri_codec`、`uu_codec`、`aliases` 宣告，以及非法 UTF-8、截斷 XML、未定義 entity，共 20 種。沒有執行任何 experiments 腳本。

1. 對每個內容，以直接 parse、`read_gpx_geometry(Path)`、`read_gpx_geometry(str)` 檢查固定錯誤、reason、訊息、args／欄位及空的 cause/context。`builtins.open` 用 `io.BytesIO` 替換，合成檔名不會交給檔案系統。
2. 每種內容 × 兩種 trip type × `km=None/1.234` × bytes／Path／str，結果必須完全是 `TargetGpxError` 的兩個固定欄位。收集 root logger、redirect stdout／stderr，並令 socket／create_connection／getaddrinfo 遇呼叫即失敗。
3. 在 `ET.fromstring` 注入 `ET.ParseError`、`ValueError`、`UnicodeError`、`LookupError`，確認四個 family 均被清理；再注入 `TypeError`、`AttributeError`、`MemoryError`、`RecursionError`、`RuntimeError`、`AssertionError`、`OSError`，分別經 reader 與 bytes routing，確認原例外物件向上傳遞。
4. 檢查 5 種非 bytes 參數、4 種非 path 參數、缺漏／不合法 trip type 經兩入口，以及字串 turnaround，共 16 次 caller errors；trip type 必須在開檔前報錯。有效 bytearray 仍成功。
5. 只在目前 Python process 暫把 `_UNPARSEABLE` 改回原 tuple，對 unknown encoding 重現 `LookupError`；finally 恢復，沒有寫回原始碼。

實際輸出（exit 0）：

```text
independent content probe: 20 inputs; 60 fixed reader errors; 240 route errors; chains/path/log/stdout/stderr absent; network guarded
parser exception families sanitized: 4
non-catch-all probe: 14 programming/resource failures propagated as the original object
caller semantics: 16 errors retained; valid bytearray accepted
in-memory removal of LookupError reproduces R1-F1: CAUGHT LookupError
```

## Required tests 完整輸出

`python -m pytest -q`，exit 0：

```text
........................................................................ [  4%]
........................................................................ [  8%]
........................................................................ [ 12%]
........................................................................ [ 17%]
........................................................................ [ 21%]
........................................................................ [ 25%]
........................................................................ [ 30%]
........................................................................ [ 34%]
........................................................................ [ 38%]
........................................................................ [ 42%]
........................................................................ [ 47%]
........................................................................ [ 51%]
........................................................................ [ 55%]
........................................................................ [ 60%]
........................................................................ [ 64%]
........................................................................ [ 68%]
........................................................................ [ 72%]
........................................................................ [ 77%]
........................................................................ [ 81%]
........................................................................ [ 85%]
........................................................................ [ 90%]
........................................................................ [ 94%]
........................................................................ [ 98%]
......................                                                   [100%]
1678 passed in 40.61s
```

`python -m pytest -q -rxX`，exit 0：

```text
........................................................................ [  4%]
........................................................................ [  8%]
........................................................................ [ 12%]
........................................................................ [ 17%]
........................................................................ [ 21%]
........................................................................ [ 25%]
........................................................................ [ 30%]
........................................................................ [ 34%]
........................................................................ [ 38%]
........................................................................ [ 42%]
........................................................................ [ 47%]
........................................................................ [ 51%]
........................................................................ [ 55%]
........................................................................ [ 60%]
........................................................................ [ 64%]
........................................................................ [ 68%]
........................................................................ [ 72%]
........................................................................ [ 77%]
........................................................................ [ 81%]
........................................................................ [ 85%]
........................................................................ [ 90%]
........................................................................ [ 94%]
........................................................................ [ 98%]
......................                                                   [100%]
1678 passed in 33.58s
```

## E-1～E-6 與 H-2／H-3／H-4 regression

| 要求 | 本次 correction 範圍內的核對 |
| --- | --- |
| E-1 | worklog §10.4 記錄 correction subject `efbffe8` 的 `-q` 為 1678 passed／34.91s，並以 `-q -rxX` 保留完整進度（明寫兩者進度相同，只有時間不同），後者為 38.26s。本 reviewer 在最終 HEAD 自行重跑兩組，結果如上；沒有以 Executor 主張代替執行 |
| E-2 | §10.3／10.4 將新增證據連到 S43、S10、CL-R1-23；既有 S27／S58～64／S78～80 與 T-1～T-7 全部隨完整 suite 重跑。S61、S78、S80 的原完整流程測試位於 test_target_gpx.py:513、532、548，correction 未修改它們；不替換累計距離的測試仍成立 |
| E-3 | 新輸入來自 `gpx(out_and_back())` 的 encoding 宣告變體，另有程式產生的 entity XML；原本幾何是數學合成形狀。Diff 沒有新增實際 GPX 檔、真實軌跡或地標資料。獨立 probe 沿用合成產生器，不讀私有檔案 |
| E-4／CL-R1-1 | 新模組的呼叫鏈只有本地讀取、解析、hash 與幾何運算，沒有網路 client；`test_no_network_is_used`（行 967）與 AST 禁用網路／logging／環境讀取的測試均通過。獨立 invalid-input probe 也封鎖 socket／DNS；沒有外部服務呼叫 |
| E-5 | correction 沒有刪除或改寫既有 test functions；AST 比對與 diff 一致。沒有把原本會失敗的斷言改成放行 |
| E-6 | §10.4 有 H-2／H-3／H-4 self-verification 與四項突變主張；本 reviewer 以本節、獨立內容探測及移除 LookupError 的記憶體反證作自己的核對。沒有把未重跑的 Executor scratchpad 突變結果當成獨立執行結果 |
| **H-2** | index 禁止樣式皆 0；合成 fixture 可追溯。新失敗路徑的結果與 reader 錯誤沒有路徑／檔名／parser text／log／chain，20 種獨立內容探測均符合。#9 reader 與既有 ingest tests 未改且完整 suite 通過；沒有替目標 GPX 新增歷史隱私裁切。最終 PlanResult／LLM 的裁切與錨點代換不在此 correction，沒有據此宣稱整合隱私已驗證；真實資料見 NV-PRIV |
| **H-3** | routing 與 heuristic 說明文字未改；`test_the_detection_is_described_as_not_validated`（行 983）通過，保留 50 m／100 m／90% 是保守 heuristic、NOT validated with real data。合成測試與 probe 沒有冒充 E1 Lite／E2，沒有讀 holdout |
| **H-4** | 新增失敗一律明確 `target_gpx_invalid/unreadable`，沒有路線或 fallback；caller errors 保留。原本缺 trip type 不推定、端點條件、非法 rider m 不退回自動、四形狀、最近可用點／tie／c_k、S64 原序 slices 與共享分界均包含在完整 suite，且 routing delta 為空。Correction 沒有引入反轉、補點、引擎或快照路徑。本票不計算 Planner／規則 5／計畫狀態，沒有越界判定它們 |

## NOT VERIFIED／未執行與 required authority

| ID | 狀態、理由與後續 |
| --- | --- |
| NV-BIND | **NOT VERIFIED（由 dispatcher 完成本次 binding 核對）**：此 HEAD 尚無本次 #15 R2 dispatch event；本 reviewer 不讀 worktree 外 rollout。Required authority／owner＝**Orchestrator／dispatcher**：依 Bindings §3.3 在本次 event 記錄 thread、全部 turn_context 集合、存取核對、唯一新增 record 與原樣複製 SHA-256，再判斷本次 audit 的 formal binding 有效性。事件 84 已建立 R1 的 binding，不能代替 R2；不將未有證據的 property 宣稱為已獨立驗證 |
| NV-PRIV | 真實目標 GPX、真實騎乘、heuristic 在真實資料上的表現 **NOT VERIFIED**；沒有明確路徑授權，沒有讀取 holdout。Required authority＝**acceptor**（RB-7）；不得以合成測試外推 |
| NV-INTEGRATION | #16 共用介面、CLI／UI、routes／RouteSummary／PlanResult／LLM 的完整整合與 Spec Integration Audit **NOT RUN**；屬後續 Ticket／Spec 或排除項。Required authority／owner＝**Design Authority**（分配與語義），Orchestrator 依依賴另派工作與 SIA；本 record 不宣告這些完成 |
| LIMIT-C15 | 沿用 DA C-15 record §2.4 的稀疏軌跡偏移、sub-metre 分界共用整數公尺 RG- 的限制；TI-C15-1 顯示方式與 RV-11 文字同步沒有在 correction 中解決，也沒有記為已涵蓋。Owner＝**Design Authority**，沿既有 tracked items；不是本次新增 finding |

本次未修改、stage 或 commit 任何實作、測試、契約、worklog 或 run record。兩組完整測試與獨立 probe 後、寫本 record 前 status 均乾淨；交付允許的唯一增量是本 record。以下 verdict 表示本次 R2 範圍內沒有未解 blocking finding；formal binding 仍須 dispatcher 完成 NV-BIND，不代替 Ticket completion、Spec Integration Audit、phase acceptance 或 release authorization。

Verdict: PASS
