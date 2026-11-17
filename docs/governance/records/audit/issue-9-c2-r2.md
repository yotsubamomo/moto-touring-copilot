# Issue #9 — cycle 2 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`；接受版本 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`，#9 列、CL-B1-1／3／7）→ Issue #9「B1-2 ingest」；另適用 CL-B1-8／9／10／11 與 FA ruling `ruling-20261117-issue9-c1.md` §3.2–3.3 |
| Issue 版本 | 使用 dispatch 所附原文；所附 UTF-8 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895` 與 first-run derivation BD-3 的 #9 列一致。未連線取得 Issue，未另宣稱重新計算該原文的 hash |
| Subject | 本 dedicated worktree，detached HEAD `7f2fee643a9a58e09e3222e861d7a9058e2a8753`；BASE `0c109aaba8c8460cebea5336840cc1d556d88a71` |
| R1 與 correction | Cycle 2 R1 subject `4b69201195da887e6382a7fd84f05c7e7fd587e4`；correction `5f9a35e9d743fb68e0f59c04dba3f780c2ae1151`。`5f9a35e..7f2fee6 -- src tests` 無差異 |
| Audit kind | **Ticket independent audit，R2 closure review，cycle 2；不是 Spec Integration Audit** |
| Role | `primary_reviewer`，Codex |
| 日期 | 2026-11-18 |
| 結果 | C2-R1-F1 **RESOLVED**；沒有未解 blocking finding。新增一項 Low／non-blocking 文字引用問題，見 C2-R2-N1 |

## 1. Assurance

| (a) Independence property | 滿足方式與證據邊界 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread，未繼承 Executor 或先前 Reviewer 的對話／推理。先從磁碟重讀 cycle 2 R1 record、修正後原始碼與 diff；Executor worklog 的結論均作為待驗證主張，以程式、測試與獨立合成探測核對。沒有派 subagent |
| Verifiable binding | 依 Bindings m3 O-6／§3.3；qualification 通過記於 Bindings §8.2 #7。**本次 dispatch 的 durable reference 是 `docs/governance/records/run/run-20261117-oc1-run2.md` §6 事件 17（第 99 行）**。該事件目前為「進行中」；依 O-6，派工者須在 return 後核對全部 rollout turn_context、存取紀錄與本檔 SHA-256，原樣回填該事件。本 reviewer 沒有讀取 worktree 外的 rollout，不宣稱這項 return 後核對已完成 |
| Autonomous access | 自行讀取本 worktree 內契約、R1、實作、測試、worklog、git history 與 diff，自行執行 PATH 的 `python`、pytest、真實 8.3 名稱及 CLI 探測；pack 是入口，未限制必要 source access。未使用 `.venv`、網路或 GitHub |
| Self-written record | 本檔由 reviewer 自行寫入。未修改 implementation、tests、contract、gates 或其他 records，未 stage／commit／push；僅新增本檔及允許的測試 caches。派工者須原樣取得本檔、核對 hash，不得代改 findings／verdict |

| (b) Assignment | 實際 model 的可用證據 |
| --- | --- |
| Executor | run record §6 事件 16（第 98 行）：同一 agentId `a6f915a1860417bc9`；派工者核對全部 assistant 訊息，觀測集合只有 (`claude-opus-5-5`, `high`)，196 則。引用的是派工者紀錄，不以 Executor 自述代替 |
| Primary | 本 reviewer 是 **Codex**。run record §1 第 4 項固定 Codex `gpt-6.1-sol`／`high`，§6 事件 17 記本次 fresh R2 dispatch；實際全部 turn_context 的 model／effort／sandbox 證據依 O-6 由派工者核對後記於事件 17。本檔不自造 session id、turn 數或最終核對結果 |
| Model diversity | **no model diversity claim**。不以不同產品／模型名稱推定 diversity；independence 與 diversity 分開陳述 |

本 implementation verdict 不代替派工者完成當次 assignment qualification，也不代替 Ticket completion、Spec closure、phase acceptance 或 release authorization。

## 2. 範圍、讀取與 subject 核對

本輪只處理：(1) cycle 2 R1 唯一 blocking finding C2-R1-F1 的 required fix；(2) 修正的 regression；(3) 修正直接產生或暴露的 blocking defects。沒有重做第二次 unlimited full audit，沒有進行 Spec Integration Audit。

重新讀取 `docs/governance/records/audit/issue-9-c2-r1.md`，包括其 §4 finding、四行實際重現、§6 的 FA／CL-B1-11 核對與證據限制。治理依 root `CLAUDE.md`、本次 AGENTS 指示、Bindings m3、`.claude/agents/gov-primary-reviewer.md`；package 治理本文 §2.3、§3.8、§4.1–4.7、impl-default v2 §6–7、orch-default v2.2 §6–7。尾行格式依本次 dispatch 指定使用 `Verdict: PASS`。

契約讀取：OC-1 的 scope／constraints／AB／authorization；SPEC-B1 的 #9、CL-B1-1／3／7、E-1～E-5、SB1-AC5 及 boundary 分配；first-run derivation 的 BD-3／G-ING／分配；CL-B1-8、CL-B1-9／10、FA ruling §3.2–3.3、CL-B1-11 §3／§3.1／§7／§8、high-risk decision §5；`DESIGN.md` §5 的流程、契約 1 與 §6.1 的時間定義；SPEC-RESOLUTION-001 §1.1、SB2-T1／2／3／11；SPEC-001 §2 的缺值及行程清單唯一來源；BATCH-1 的 B1-2。#7 worklog §8／§10 的 C-2 與 run record §1 第 3 項確認其分派至 #9。

修正證據讀取：`ingest/__main__.py`、`gpx.py`，`segments.py` 的 BASE diff；`test_ingest_cli.py`、`test_ingest.py` 的 BASE diff、S-3～S-6 標記、`tests/conftest.py`、`pyproject.toml`；#9 worklog §11 的 filesystem／L-1～L-6 及 §12 全部 correction claims。讀取用 `Get-Content -Encoding UTF8 <明確檔案>` 與 `rg -n <pattern> <明確路徑>`；初次中文顯示編碼不正確後以 UTF-8 重讀。未從 repo root 泛用搜尋。

| 指令／檢查 | 結果 |
| --- | --- |
| `git status --short`；`git rev-parse HEAD`；`git rev-parse 0c109aa` | 開始時乾淨；SHA 如檔首；寫 record 前再次 status 仍為空 |
| `git log --oneline 0c109aa..7f2fee6`；`git diff --stat 0c109aa..7f2fee6` | 歷史及 aggregate scope 與 dispatch 相符；13 changed files，產品／測試只有兩個 ingest 檔與兩個 ingest test 檔，其餘為 records |
| `git diff 4b69201..7f2fee6 -- src tests`；`git log --format='%h %s' --name-only 4b69201..7f2fee6` | correction 只改 `ingest/__main__.py`、`test_ingest_cli.py`；另外三個 commits 都只改 `docs/governance/records/**`。既有 CLI tests 沒有刪改，新增 11 cases |
| `python -` 透過 subprocess 擷取 `git diff 0c109aa..7f2fee6` | 完整 diff 為 13 files／3407 lines；核對檔案邊界與有界敏感樣式。另以 focused diff 閱讀 `__main__.py`、`segments.py`、`test_ingest.py`；CLI 測試直接讀最終檔案。歷史 records 不作第二次全面 audit |
| `git diff 5f9a35e..7f2fee6 -- src tests` | 空；本次所有測試涵蓋 correction 後 HEAD 的程式與測試 |
| `git diff 4b69201..7f2fee6 -- src/moto_copilot/ingest/segments.py tests/test_ingest.py` | 空；停等分類、時間分配與 trim-boundary 實作／測試未被 correction 更改 |
| `git diff 0c109aa..7f2fee6 -- tests/test_routes_pace_eta.py tests/conftest.py tests/test_contracts.py pyproject.toml` | 空；S-3～S-6、契約 tests 與全域 pytest 設定未被本票修改 |
| `git diff --check 0c109aa..7f2fee6 -- src tests` | exit 0，無輸出 |
| `rg -n 'xfail\|skip' tests` | 只有 `test_routes_pace_eta.py:117,159,173,182` 四個 strict xfail；#10 一個、#11 三個；沒有 #9 標記、其他 xfail 或 skip |
| `python -` 擷取 `git ls-files -z` 並只印禁止 pattern 計數 | `.env=0, *.key=0, *.gpx=0, *.fit=0, data/=0`；未列出禁止路徑或讀取對應內容 |
| `python -` 對完整 diff 的有界憑證樣式計數 | `sk-ant-` 長值及 api-key assignment 長值各 0。第二個 regex 初次誤用 literal backslashes，未作有效證據；更正為 whitespace／引號樣式後另次執行仍為 0。沒有輸出可能的秘密值，不宣稱涵蓋所有秘密形式 |

## 3. 自行執行的 pytest

所有 process 均使用 PATH 的 `python`，cwd 是本 worktree。以 `$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/<名稱>'` 限制 pytest 暫存位置；TEMP／TMP 也設於 worktree，成功重跑時設為 `.pytest_cache`，並設 `PYTHONIOENCODING=utf-8`。未改測試設定。

首次 `python -m pytest -q` 已指定 worktree 內的 basetemp，但 `.pytest_cache` 父目錄尚未存在，產生 `FileNotFoundError [WinError 3]`：**239 passed, 4 xfailed, 81 errors in 3.37s，exit 1**。81 個均為 CLI tmp_path setup errors。沒有因此存取外部暫存目錄；以 `New-Item -ItemType Directory -Path .pytest_cache -Force` 建立允許的 cache 目錄後重跑。這是 reviewer 的執行準備錯誤，不是產品 defect；保留該失敗，以下為實際成功重跑及必要的 runxfail 結果。

| 命令 | basetemp | 結果 |
| --- | --- | --- |
| `python -m pytest -q` | `c2-r2-q` | **320 passed, 4 xfailed in 1.92s**；exit 0 |
| `python -m pytest -q -rxX` | `c2-r2-rx` | **320 passed, 4 xfailed in 1.75s**；exit 0 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py` | `c2-r2-xf` | **4 failed, 41 passed in 0.50s**；exit 1 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py` | `c2-r2-xfcli` | **4 failed, 122 passed in 1.50s**；exit 1 |

`-rxX` 四項恰為：

| CL-B1-8 | 測試（均在 `tests/test_routes_pace_eta.py`） | reason／runxfail 失敗內容 |
| --- | --- | --- |
| S-3 | `test_pace_table_matches_the_mock_fixture__v03_contract` | restored by #10；缺 `margin_coeff` 等 v0.3 配速表欄位 |
| S-4 | `test_eta_reproduces_the_mock_fixture__v03_contract` | restored by #11；列比對缺 `stop_allow_s` 及相關時間值 |
| S-5 | `test_eta_is_unknown_when_a_category_has_no_pace__v03_contract` | restored by #11；unknown ETA 列缺 `stop_allow_s` |
| S-6 | `test_eta_output_passes_the_contract_with_and_without_breaks` | restored by #11；缺 `stop_allow_s` 及其契約不變條件 |

兩個 runxfail 命令失敗集合完全相同，沒有 ingest／CLI 新失敗被標記遮住。S-1／S-2 的原契約斷言已併回 `test_ingest.py:62,145` 的無標記測試；BASE diff 可核對斷言保留，成功重跑亦驗證其恢復。worklog §12.4 記錄最終程式 subject `5f9a35e` 的三類完整 E-1 輸出、exit codes、標記與修改理由；本次結果可對應其數目與缺口。**E-1 依 CL-B1-9 滿足；不是字面的全部測試通過。** SPEC-B1／AB-13 的無 xfail 要求未因此成立或被豁免。

## 4. C2-R1-F1 closure

### C2-R1-F1 — RESOLVED

- **原 severity：Medium／blocking；本輪狀態：RESOLVED。** 原證據與 required fix：`issue-9-c2-r1.md:80–101`，依 FA §3.2 結果 1、CL-B1-11 第 2 項，整份清單的跨角色名稱矛盾不能因 `--trips` 未選該 pace 而漏判。
- **修正證據：**`src/moto_copilot/ingest/__main__.py:175–180` 對全部 `trip_role == pace` 呼叫 `pace_name_problem`，再只對選中的 pace 呼叫 `pace_link_problem`。第 137–143 行先拒絕不在 listing 的名稱，否則只查 pace 自身短檔名並與非 pace 的文字 key 比對。第 219–224 行完成全體檢查／拒絕後，才到第 230–231 行開啟第一個 GPX；沒有 partial GPX read。
- **不依賴磁碟區的 regression evidence：**`tests/test_ingest_cli.py:444` 的 4 cases 涵蓋 holdout／excluded × 自動／只選另一個正常 pace；替換的是 pace 短檔名回答，走完整 main。第 473 行的 6 cases 另覆蓋未選 pace 端的 8.3／stream 拼法及非 pace 端的 stream 拼法。共同 helper 第 258 行斷言 exit 2、GPX open 空集合、兩個輸出檔不存在。全部在本次 pytest 通過；未加 skip／xfail。
- **獨立實際重現：**以真實 `GetShortPathNameW`，沒有 mock 名稱查詢、GPX parser、build_rows 或 validator，重跑 R1 四行案例並擴至 excluded／相反方向，結果如下。
- **Required fix 核對：**全清單處理、非 pace 不查詢、必要 regression cases、模組說明／worklog claims 及最終 E-1 均已具備。`__main__.py:23–30` 與 worklog §12.1／12.2／12.5 正確區分全清單名稱檢查與 selected pace 連結檢查。沒有剩餘 blocking 修正要求；一處 helper 名稱引用過時另列 N1，不影響上述語義。

獨立探測用 PowerShell here-string 傳給 `python -`，沒有新增探測腳本。所有合成檔位於 `tempfile.TemporaryDirectory(dir=<worktree>/.pytest_cache)`，明確 assert 在 cwd 內，結束由 context manager 清理自己的目錄。軌跡生成器來自 `runpy.run_path('tests/test_ingest_cli.py')['_gpx']`，虛構原點／日期。Python audit hook 只在 main 執行期間記錄該 GPX 資料夾內所有 `open`；拒絕案例並檢查沒有衍生表／報告及訊息不含檔名。

R1 同型清單：T901 pace `ordinary.gpx`、T904 pace `pace_long_named_trip_a.gpx`、T902 非 pace `PACE_L~1.GPX`。本次真實 alias 是 **`PACE_L~1.GPX`**，不在 `os.listdir` 名稱清單中。

| 清單／選取 | holdout 結果 | excluded 結果 |
| --- | --- | --- |
| 非 pace 為短檔名；自動選取 | exit 2，GPX open=[]，無輸出 | 同左 |
| 同上；`--trips T901`，只選正常 pace（R1 的漏判情形） | exit 2，GPX open=[]，無輸出 | 同左 |
| 同上；`--trips T904` | exit 2，GPX open=[]，無輸出 | 同左 |
| literal 對照：非 pace 改成長檔名；`--trips T901` | exit 2，GPX open=[]，無輸出 | 同左 |
| 相反方向：未選 pace 改成短檔名、非 pace 為長檔名；`--trips T901` | exit 2，GPX open=[]，無輸出 | 同左 |

## 5. Regression、FA §3.2 與 CL-B1-11

上述同一個 inline probe 共 **16 cases，全部 assertions 通過，exit 0**；除上表 10 cases，另有：

| 探測 | 實際結果 |
| --- | --- |
| 正常 pace + 未選取正常 pace + 分開的無效合成 holdout／excluded；只選正常 pace | exit 0；只開 `ordinary.gpx`；表內均為 pace、有 `short_stop_time_s`；private／public／pair violations 全空 |
| 對上述正向案例包裝 `short_name`、`os.stat`、`os.lstat` | GPX 目錄項目的實際呼叫只有 `short_name(ordinary.gpx)`、`short_name(長檔名 pace)`、`lstat(ordinary.gpx)`；沒有作用於非 pace 的呼叫。Wrapper 不取代正常回答，並斷言不查非 pace |
| 未選 pace 的 short_name 回答拋 OSError | exit 2，零 GPX open，無輸出 |
| 未選 pace 缺檔（C-9-9） | exit 2，零 GPX open，無輸出 |
| 第二個被選 pace 有真實第二個 hard link | exit 2，連前面的正常 pace 都未開啟，無輸出 |
| 上述 hard link pace 未選取，僅選正常 pace | exit 0，只開正常 pace，三類契約違反皆空 |
| 被選 pace 的 lstat 拋 OSError | exit 2，零 GPX open，無輸出 |

正向 metadata 包裝是第一個正向 case 的附帶觀測，不另算 case。另嘗試 `os.symlink` 建立合成連結，回報 `winerror 1314`；真實 symlink CLI 觀測 **NOT RUN**，沒有要求額外系統權限。

| 契約證據 | 本輪核對結論 |
| --- | --- |
| FA closure 1–2：stream／8.3，兩邊、角色及選取 | 既有第 279、298、313 行 tests 保留，本次通過；新第 444／473 行補未選取項目；邏輯證據不依賴短檔名設定，本次另有真實 8.3 觀測。沒有 skip／xfail |
| FA closure 3：原 R1-F1 tests、停等／修剪 | 第 201／222／232 行原測試保留並通過；correction 沒有更動 `segments.py`／`test_ingest.py`。指定 pytest 重驗時間總和、假停留不加里程、short ≤ stopped、CL-B1-10 trim-boundary 測試 |
| FA closure 4：最終 E-1 | §3 已自行執行；worklog §12.4 的完整 evidence 對應相同程式／測試 identity |
| FA closure 5–6：claims 與高風險 | worklog §12 更正完整清單的拒絕範圍、列 L-4 更新及 H-2／3／4；CL-B1-11 第 4 項殘餘及 TOCTOU 沒有冒稱已解決。文字 helper 引用問題見 N1 |
| L-1 | `test_ingest_cli.py:347,363` 三例真實 `os.link`、完整 CLI、拒絕前零 GPX open、無輸出、訊息不含檔名；本次皆通過，獨立 probe 也重驗第二個被選項目才有問題的情形 |
| L-2 | 第 378 行 symlink mode／reparse 屬性 × 自動／指定四例保留並通過；替換 pace 的 lstat 回答，不依賴建立 symlink 特權。真實 link 限制照實記 NOT RUN |
| L-3 | 第 89／125／232 行三個正向測試沒有修改斷言，本次皆通過 |
| L-4 | `load_manifest` 第 60／63 行只查／讀 manifest；第 171 行 listdir 只用名稱；第 176–177 行只對全部 pace 查短檔名；第 179–180 行只對 selected、名稱通過的 pace 作 lstat；第 231 行只讀 chosen pace；第 245–248 行才建立／寫輸出。非 pace 項目只作字串處理，沒有 stat、resolve、readlink、hash 或短檔名查詢作用其上。另核對 `gpx.py:20` 的 ET.parse；既有 metadata spy 與本次 wrapper 只是輔助，結論有 source inspection 支持 |
| L-5／L-6 | worklog §11／§12 正確交代硬連結、pace symlink 及非 pace filesystem 禁令、殘餘歸 G-ING；E-2／E-5 增補可對應實際 tests。helper 舊名稱是 Low，不是行為宣稱失實 |
| C-9-9 | 未選 pace 缺檔會全次拒絕已實際確認。這是 FA 允許在開檔前拒絕未納入比對拼法的 fail-closed 做法，不產生非 pace 查詢或契約欄位／角色變更；本輪沒有需 DA 裁決的 ambiguity |

**C-2 自行核對：**另以一個 `python -` 在 cache 內建立合成 GPX／manifest，透過 subprocess 執行 `python -m moto_copilot.ingest --gpx-dir <合成 gpx> --out <合成 out>`，cwd 與 PYTHONPATH 都指向本 worktree。**exit 0**：T901 601 points、8 rows、only pace，private／public／pair 三個 contract check 全為 OK，列皆有 `short_stop_time_s`。這確認 #7 worklog §8／§10 的 producer gap 在合成資料上已處理，不是以真實 GPX 重建的結論。

| 高風險類別 | 本輪有界核對 |
| --- | --- |
| H-2 | 禁止追蹤路徑計數皆 0；diff／fixtures／新增 evidence 的軌跡與時間可追溯至 synthetic 生成器。修正拒絕訊息只列 trip id，無檔名；無外部服務呼叫。隱私 trim／錨點相關實作未被本次 correction 更動，既有 trim 及 public/private 契約測試通過。未用私有資料作查證 |
| H-3 | 原整份清單 refusal claim 的漏判已以真實 alias 重驗解決；最終結果照實記 320 passed／4 xfailed，不稱全部通過。CL-B1-11 的 isolation 範圍與 G-ING 殘餘分開；未將合成測試／Spike 稱為 E1 Lite 或 E2，未引入受禁止的能力宣稱 |
| H-4 | 名稱不在 listing、未選 pace 名稱查詢失敗、selected lstat 失敗、link 問題均在首個 GPX 前明確拒絕；正常選取仍成功。時間與 quality 路徑未變且指定回歸測試通過。Planner／規則 5／路線採用等非本次 delta，未冒稱已審查 |

未發現 correction 直接引入或暴露的新 blocking defect。

## 6. 新 non-blocking finding

### C2-R2-N1 — source_key docstring 仍引用已刪除的 helper 名稱

- **Severity：Low；non-blocking。**
- **證據：**`src/moto_copilot/ingest/__main__.py:87` 仍稱短檔名由 `pace_entry_problem` 處理；correction 已把它拆成第 128 行的 `pace_name_problem` 與第 147 行的 `pace_link_problem`，原 helper 不再存在。`git diff 4b69201..7f2fee6 -- src tests` 可核對此 rename／split 與未同步的引用。
- **影響：**讀者依 docstring 定位不到實際 helper；名稱比對的文字語義與 runtime 行為仍正確，沒有造成契約違反或必要 evidence 缺漏，不阻擋 closure。
- **Required fix：**把該引用改為實際處理短檔名的 `pace_name_problem`，或移除具體 helper 名稱。
- **Disposition／owner：**記為後續文字修正，由 **#9 Executor** 在獲授權的後續變更中處理；本輪不修改 implementation、不延長 cycle，不把此 tracked item 當成新 work item 的授權。

## 7. NOT VERIFIED／NOT RUN 與 authority

| ID | 項目與理由 | Required authority／owner |
| --- | --- | --- |
| NV-1 | 真實行程清單的角色、真實 GPX 的契約符合性、真實 holdout／excluded 隔離：需要私有騎乘資料，本票排除且本次未授權；只驗合成資料 | **acceptor**，RB-7；承接 C-9-3 |
| NV-2 | 真實資料所在磁碟區的 8.3 設定、實際是否存在跨角色 hard link／symlink／複本：本次真實 alias 觀測僅對 cache 中的合成檔有效 | **acceptor**；FA NV-2、CL-B1-11 §7 A-2 |
| NV-3 | CL-B1-11 第 4 項的複本與非 pace 端別名，及取得非 pace metadata／hash 的設計：不在 #9 scope，不作本輪 blocking 或已涵蓋宣稱 | **Orchestrator** 追蹤 G-ING；取得保留行程 metadata／內容的 required authority 為 **acceptor**（CL-B1-11 §7 A-1） |
| NV-4 | 本次 Primary 全部 rollout 的實際 model／effort／sandbox、存取紀錄與 record 原樣回傳 hash：worktree 內沒有原始 rollout，事件 17 尚為進行中；不自行讀取外部路徑或豁免核對 | **派工者／Orchestrator**，依 Bindings §3.3 回填事件 17；這是 assignment eligibility 核對，不由 implementation verdict 取代 |
| NR-1 | 真實 symlink CLI 觀測因建立時 winerror 1314 而 NOT RUN；L-2 的不依賴特權證據已實際執行通過 | 無須為 #9 另外取得權限；保留證據限制 |
| NR-2 | E1 Lite、E2、G-REG、Executor 歷史 mutation checks、本 Spec 的整合驗收本輪均 NOT RUN；沒有把 worklog 的歷史執行當成 reviewer 本次執行 | 真實實驗／私有資料為 **acceptor**；SIA 由 **Orchestrator** 另派；AB-12 的文件 follow-up（C-9-4）維持原 owner |

本輪唯一 cycle 2 R1 blocking finding 已解決；N1 有 disposition 與 owner，不延長 cycle。最終工作區只應有本 audit record 一個新增檔案，另有 git-ignored 測試 caches；派工者仍須完成 O-6 的 return 核對。

Verdict: PASS
