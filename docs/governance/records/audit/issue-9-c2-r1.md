# Issue #9 — cycle 2 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，接受版本 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`derivation-spec-b1.md`，#9 列、CL-B1-1／3／7）→ Issue #9 B1-2 ingest；另適用 CL-B1-8／9／10／11、FA ruling `ruling-20261117-issue9-c1.md` §3.2–3.3 |
| Issue 版本 | 使用本次 dispatch 附上的原文；其所附 UTF-8 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895` 與 first-run derivation BD-3 相符。沒有連線重新取得 Issue |
| Subject | 本 dedicated worktree，detached HEAD `4b69201195da887e6382a7fd84f05c7e7fd587e4`；BASE `0c109aaba8c8460cebea5336840cc1d556d88a71` |
| 實作 identity | `a281cb0`、`b4d1f84`、`6f97561`、`49f1d80`；其餘 BASE 之後的 delta 為 `docs/governance/records/**`。最後實作 commit 為 `49f1d80ed1c67c09488353faf1d2b1ac479ea3cd` |
| Audit kind | **Ticket independent audit，R1，cycle 2；完整 accepted work scope；不是 Spec Integration Audit** |
| Role | `primary_reviewer`，Codex |
| 日期 | 2026-11-18 |
| 結果 | 一項 Medium／blocking finding：C2-R1-F1。既有 pytest 成功不構成該項 closure |

## 1. Assurance：context independence 與 model diversity 分開記載

| (a) Independence property | 本次滿足方式與證據邊界 |
| --- | --- |
| Independent context | 本次為 fresh Codex thread；沒有 Executor、cycle 1 Reviewer 的對話或推理 context。派工提供契約、subject、record 路徑及 Issue 原文，未提供預設結論。自行先讀實作及測試，形成判斷；worklog、FA 與 DA record 的主張均經原始碼、diff 與本次執行核對 |
| Verifiable binding | 使用 Bindings m3 O-6／§3.3 的派工機制。**當次 dispatch 的 durable reference 是 `run/run-20261117-oc1-run2.md` §6 事件 15（第 97 行）**。該事件目前記 `Codex gpt-6.1-sol / high`、進行中；依 Bindings，派工者在 return 後核對全部 rollout turn_context、存取紀錄及 record SHA-256，再原樣回填該事件。本 reviewer 沒有讀取 worktree 外的 rollout，不能自行宣稱該最終核對已完成 |
| Autonomous access | 自行讀取 worktree 內契約、原始碼、測試、git history 與 diff，自行執行 pytest、CLI 與合成探測；pack 是入口，未限制判斷。沒有委派 subagent。首次 pytest 的預設 tmpdir 存取失敗及後續限制，另於 §3 如實記載 |
| Self-written record | 本檔由本 reviewer 自行寫入；沒有修改 implementation、tests、contract、gates 或其他 record，沒有 stage、commit、push。派工者須原樣取得本檔並核對 hash；不得代改 finding 或 verdict |

| (b) Assignment | 實際 model 的可用證據 |
| --- | --- |
| Executor | run record §6 事件 14（第 96 行）：agentId `a6f915a1860417bc9`，全部 assistant 訊息觀測集合只有 (`claude-opus-5-5`, `high`)，176 則。這是派工者的核對紀錄，不採用 Executor 自我觀測代替 |
| Primary | 本 reviewer 是 Codex；事件 15 宣告 `gpt-6.1-sol / high`。完整當次 binding 證據由派工者核對並記於事件 15；本檔不自造 model id、session id、turn 數或 rollout 核對結果 |
| Model diversity | **no model diversity claim**。Bindings 未宣告 diversity 關係，且本輪 Primary 的完整 binding 核對尚待派工者回填；不以模型名稱推定 independence |

本檔對 implementation 的 verdict 不代替派工者依 O-6 完成 assignment qualification／存取核對，也不構成 Ticket completion、Spec closure 或 phase acceptance。

## 2. 範圍、契約與 subject 核對

閱讀 root `CLAUDE.md`、本次提供的 AGENTS 指示、Bindings m3（含 O-6、qualification 通過紀錄）、`.claude/agents/gov-primary-reviewer.md`；適用 package 的治理本文 §2.3、§3.8、§4.1–4.7、impl-default v2 §6–7、orch-default v2.2 §6–7。紀錄尾行依本次 dispatch 指定使用 `Verdict: BLOCKING`。

契約閱讀涵蓋 OC-1、SPEC-B1 derivation、first-run derivation（BD-3、G-ING、G-REG、AB 分配）、high-risk decision §5、CL-B1-8、CL-B1-9／10、CL-B1-11、FA ruling §3.2–3.3；另核對 `DESIGN.md` §5／§6.1、SPEC-RESOLUTION-001 的時間定義及 SB2-T1／2／3／11、SPEC-001 的行程清單唯一來源及缺值規則、BATCH-1 索引。#7 worklog §8／§10 的 C-2 與 run record §1 第 3 項確認其分派至 #9；#9 worklog 全部相關階段及最終 §11 作為待核對 claims。

程式閱讀涵蓋 `ingest/__main__.py`、`segments.py`、`gpx.py`，契約驗證的相關 invariants；測試閱讀涵蓋 `test_ingest.py`、`test_ingest_cli.py`、`test_routes_pace_eta.py` 的標記與契約檢查，以及 `conftest.py`、`pyproject.toml`。沒有執行任何 `experiments/` 腳本。

| 指令／檢查 | 結果 |
| --- | --- |
| `git rev-parse HEAD`；`git rev-parse 0c109aa`；`git status --short` | SHA 如檔首；開始時工作區乾淨 |
| `git log --oneline 0c109aa..4b69201`；`git diff --stat 0c109aa..4b69201`；`git diff --name-only 0c109aa..4b69201` | 18 commits；12 changed files。產品／測試 delta 限於兩個 ingest 檔與兩個 ingest test 檔；其他為 records |
| `git diff 0c109aa..4b69201 -- src/moto_copilot/ingest/__main__.py`；同範圍 `-- src/moto_copilot/ingest/segments.py tests/test_ingest.py` | 獨立核對完整實作與停等測試變更；角色檢查與名稱解析的問題見 F1 |
| `git log --format=%h --name-only 0c109aa..4b69201 -- src tests` | 只有檔首所列四個 implementation commits |
| `git diff 09d150f..4b69201 -- src/moto_copilot/ingest/segments.py tests/test_ingest.py tests/test_routes_pace_eta.py tests/conftest.py pyproject.toml` | 空；cycle 2 沒有改變停等、修剪、後續票的標記或全域 pytest 設定 |
| `git diff 0c109aa..4b69201 -- tests/test_routes_pace_eta.py tests/test_contracts.py tests/conftest.py pyproject.toml` | 空；S-3～S-6 未被本票修改 |
| `git diff --check 0c109aa..4b69201 -- src tests` | exit 0，無輸出 |
| `rg -n 'xfail\|skip' tests` | 只有 `test_routes_pace_eta.py:117,159,173,182` 的四個 strict xfail；一個 restored by #10、三個 restored by #11；無 #9 標記、無 skip |
| `Get-Content -Encoding utf8 <上述明確檔案>`／`rg -n <章節或測試名稱> <明確檔案>` | 檔案及行號核對；未作 repo root 全域搜尋。初次中文讀取編碼不正確後以 UTF-8 重讀 |
| `python -c "import sys; print(sys.version.split()[0])"` | PATH Python 3.11.2；沒有使用 `.venv` |

## 3. 自行執行的 pytest 與環境限制

**首次執行偏差必須保留：**直接執行 `python -m pytest -q` 時，pytest 的預設 tmp_path setup 嘗試對 worktree 外的預設 pytest 暫存位置作目錄列舉，sandbox 以 `PermissionError: [WinError 5]` 拒絕。結果為 `239 passed, 4 xfailed, 70 errors in 23.33s`，exit 1；70 個均為 CLI 測試 setup errors。沒有取得該目錄內容，沒有沿失敗路徑進一步查詢，也沒有放寬 sandbox。這是本 reviewer 未先限制 pytest tmpdir 的執行偏差，不能寫成「從未嘗試存取 worktree 外路徑」，也不是產品 defect。

之後每個 pytest process 都用 PowerShell 環境變數把 basetemp 限於 worktree 的 `.pytest_cache`：`$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/<下表名稱>'`。第一個成功重跑另含 `--tb=short`；其餘使用預設 traceback。沒有修改 pytest 設定或測試檔；合成檔與暫存位置均在 worktree。四個獨立命令分別使用不同 basetemp。

| 命令 | basetemp 名稱 | 實際結果 |
| --- | --- | --- |
| `python -m pytest -q` | `c2-r1-q` | **309 passed, 4 xfailed in 1.66s**；exit 0 |
| `python -m pytest -q -rxX` | `c2-r1-rx` | **309 passed, 4 xfailed in 1.68s**；exit 0；下列四個 XFAIL，無其他標記 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py` | `c2-r1-xf` | **4 failed, 41 passed in 0.58s**；exit 1，失敗恰為下列四個 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py` | `c2-r1-xfcli` | **4 failed, 111 passed in 1.40s**；exit 1，失敗恰為下列四個 |

`-rxX` 的完整結果列：

```text
XFAIL tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #10; build_pace_table does not write stop_ratio, margin_coeff or margin_basis yet
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks - v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet
```

`--runxfail` 的錯誤核對：S-3 為配速表缺 v0.3 必填欄位（首項 `margin_coeff`）；S-4 為缺 `stop_allow_s` 及其影響的累計時間；S-5 為 unknown ETA 列缺 `stop_allow_s`；S-6 為 ETA 必填欄位／不變條件缺口。均為 CL-B1-8／9 允許的後續產生者缺口，沒有 CLI 或 ingest 新失敗被 xfail 遮住。

本次數目與 worklog §11.4 的最終 subject 數目相同。該節已記錄三個必要命令的完整輸出、exit codes、標記清單，且 `49f1d80..HEAD` 沒有程式或測試 delta。**E-1 依 CL-B1-9 滿足；不稱為「全數通過」，也不以 E-1 滿足代替 F1 closure。**

## 4. Findings

### C2-R1-F1 — 未被選取的 pace 項目，其 8.3 跨角色矛盾不會使整份清單拒絕

- **Severity：Medium；blocking。**
- **依據：**FA ruling §3.2「要達成的結果」第 1 項：清單以作業系統解析到同一目錄項目的拼法同時給予 pace／非 pace 角色時，須在開啟任何 GPX 前拒絕，或事先拒絕這類拼法；兩邊的 8.3 短檔名都在其中。此要求沒有以 `--trips` 的選取範圍縮限。CL-B1-11 §3 第 2 項保留 FA 的要求；第 3 項對 selected pace 的連結檢查沒有撤銷整份清單角色矛盾的要求。程式模組說明 `__main__.py:17–18` 亦宣稱 whichever trips are requested。
- **程式證據：**`__main__.py:73` 的全清單 `_refuse_conflicting_roles` 只比較文字 key（第 88–102 行），沒有納入 8.3 alias。真正的短檔名比對在第 145–146 行，但第 **161 行只對 `chosen` 執行**；第 202–203 行先套用 `--trips` 再呼叫它。因此不在 `chosen` 的長檔名與非 pace 短檔名之間的矛盾不會被發現。
- **測試缺口：**`test_ingest_cli.py:313` 的兩種選取都是自動選全部或明確選中衝突 pace 本身；沒有選取另一個正常 pace、同時保留未選取衝突項目的案例。
- **獨立重現：**以下以真實 Windows `GetShortPathNameW` 回答，沒有 mock parser、build_rows、validator 或名稱查詢。合成 GPX 來自 `tests/test_ingest_cli.py::_gpx`（虛構原點、虛構日期）；檔案在 `.pytest_cache` 內 temporary directory。三筆清單為：T901 pace `ordinary.gpx`、T904 pace `pace_long_named_trip_a.gpx`、T902 holdout `PACE_L~1.GPX`。真實短檔名為 `PACE_L~1.GPX`，不在 `os.listdir` 名稱清單中。Python audit hook 觀測 GPX 資料夾的 `open` 事件。

```text
同一份長檔名／8.3 短檔名清單：
自動選取        exit=2  gpx_open=[]                outputs=[trip_manifest.json]
--trips T901    exit=0  gpx_open=[ordinary.gpx]    outputs=[derived_segments_private.json, ingest_report.json, trip_manifest.json]
--trips T904    exit=2  gpx_open=[]                outputs=[trip_manifest.json]
對照：T902 改為長檔名，--trips T901：
                exit=2  gpx_open=[]                outputs=[trip_manifest.json]
```

成功案例首行為 `ingest ingest-b1-1 | curv-spike0-80-250 | pace trips: 1 | non-pace entries not opened: 1 | rows: 8`。同一目錄項目的角色矛盾，只因改用短檔名、且沒有選到衝突 pace 本身，就由拒絕變為成功。

**影響與分類理由：**這是已寫定的整次拒絕要求未完整達成，因此 blocking。此案例開啟的是另一個正常 pace，**沒有證據顯示此案例實際開啟 holdout 內容或造成私有資料外洩**；據此評 Medium，不把它誇大為已發生污染。它仍是 FA 所要求的同一目錄項目拼法處理缺口，不屬 CL-B1-11 第 4 項分配給 G-ING 的不同目錄項目／複本殘餘。

**Required fix／owner：#9 Executor。**在開啟第一個 GPX 前，使整份清單的 pace／非 pace 角色矛盾判定涵蓋未選取 pace 項目的 8.3 拼法，或依 FA 允許的方式先拒絕此類拼法；仍僅使用清單字串、目錄名稱與 pace 自身資訊，不查詢任何非 pace 檔案。新增至少「另有正常 pace，`--trips` 僅選正常 pace，未選取 pace 與 holdout／excluded 的短檔名衝突」的 regression cases，斷言 exit 2、GPX open 空集合、兩個輸出檔皆不存在。更正模組說明與 worklog 的完整拒絕 claims，使它們與最終實作及證據一致；依 CL-B1-9 重跑 E-1。不同解讀若有爭議，交 Design Authority；本 reviewer 不改寫契約或豁免 FA 條款。

本輪沒有其他獨立 non-blocking finding；不建立沒有 owner／disposition 的建議清單。

## 5. Issue AC、clarifications 與 evidence 逐項核對

以下 PASS 僅指該列的有界核對，不是 Ticket verdict。

| 要求 | 原始碼／實際執行證據 | 結論 |
| --- | --- | --- |
| Issue AC1／SB2-T1 | `test_ingest.py:193`：前後 72 km/h、重複位置 1 秒；停留兩欄皆 0，moving 增 1 秒、里程不變、契約通過 | PASS |
| Issue AC2／SB2-T2 | `test_ingest.py:211`：2／3／179／180 秒；short 總和 182、stopped 362，2 秒只進 moving，長度不變 | PASS |
| Issue AC3／SB2-T3 | `test_ingest.py:234`：混合停等、GPS jump、記錄中斷；逐段 short ≤ stopped，時間總和等於 trimmed duration；另有短尾合併測試第 298 行 | PASS |
| Issue AC4／SB2-T11 | `test_ingest_cli.py:104`：明確指定 T901＋holdout T902，exit 2、沒有 GPX open、沒有輸出 | PASS |
| SPEC-B1 §5 #9：非 pace 不開啟／不產生列 | 第 89、125、232 行的正向測試只開啟所選 pace；holdout／excluded 沒有列；另補測任意角色值也略過 | PASS：此項本身；整份清單矛盾另見 F1 |
| 指定非 pace／未知 trip id 開檔前拒絕 | 第 104、113、119 行；混合指定也在第一個 GPX 前拒絕 | PASS |
| 無 manifest → 拒絕且不建立暫定清單 | 第 131、176 行；`load_manifest` 不再建立清單 | PASS |
| 被拒絕檔案未開啟 | CLI 測試的 audit hook 對 GPX folder 全部 open 計數；正向案例證明觀測有效，非 pace 檔故意為無效 GPX | PASS：既有覆蓋；F1 新情境不符合整次拒絕 |
| CL-B1-3(1) 原停止步定義 | `segments.py:275–282`：>10 秒且 <50 m 停止，≥50 m 移動並 suspect；其他步速度 <3 km/h 停止；第 253、263 行測試與既有 gap 測試通過 | PASS |
| CL-B1-3(2) 整事件分類、各步秒數歸所在段 | `allocate_stop_events` 只在 moving 步或結尾關閉事件；第 276 行直接測跨段 200 秒 long、4 秒 short、2 秒 false。現行距離切段只在 moving 步結束，故完整軌跡不會產生連續 stopped 步跨段的情形；以 allocator 直接驗證適當 | PASS |
| CL-B1-3(3) 假停留 moving、不加里程 | `segments.py:306–311`；AC1／2 的基線比對 | PASS |
| CL-B1-3(4) pace 選取、明確拒絕非 pace | 先 select 再統一檢查，之後才進 read_gpx loop；上列 CLI 測試 | PASS：選取規則；FA 加強要求見 F1 |
| CL-B1-3(5) manifest 唯一來源 | 沒有 glob 自動建立全部 pace 的舊路徑；load_manifest 必要，未讀實際私有清單 | PASS |
| CL-B1-3(6) 新版本、門檻為參數 | `IngestParams` 為 `ingest-b1-1`、3／180；第 227、292 行驗參數變動及輸出版本 | PASS |
| CL-B1-7 用語 | 檢查新增程式 docstrings、錯誤訊息與 worklog；限制性提及並非能力宣稱；沒有把 ETA_safe 稱為百分位數或把降雨門檻當官方警特報，也未把合成測試稱為 E1／E2 | PASS |
| CL-B1-8 S-1／S-2 恢復 | diff 顯示三個原契約斷言併回第 62、145 行的原測試，未放寬、未補值，兩個 __v03_contract xfail 移除；其他斷言保留 | PASS |
| CL-B1-9 | §3 的三類必要輸出與工作紀錄一致；S-3～S-6 的測試及標記無 delta | E-1 滿足 |
| CL-B1-10 修剪邊界 | 第 312 行合成漂移測試：完整 200 秒 long；裁切後 80 秒 short；範圍外秒數不計、總時間與契約檢查成立。兩端均由同一 kept[start:end] 路徑處理 | PASS |
| E-2 | worklog §6 的逐 AC 表、§9.3 的 trim 表、§10.4／§11.3／§11.5 的增補可對應實際測試名稱及本次結果 | 已提供；FA 完整 scope 仍有 F1 |
| E-3 | 測試生成器明示 LAT0=10、LON0=20、T0=2026-01-01；直線／圓／漂移、JSON manifest 與 link 均在測試建立。既有 mock fixture 由 conftest 讀取且標示 invented。diff 沒有加入真實騎乘資料 | PASS：synthetic provenance |
| E-4 | worklog §6 列 S-1／S-2 併回理由；§11.3 列 outside-source 測試由 exit 0 改 exit 2 的原因。原 R1-F1 regression assertions、L-3 三個正向測試不變；未修改後續票或全域測試設定 | PASS |
| E-5 | worklog §11.2／§11.5 已列 H-2／3／4 self-verification。具體機制與 claims 自行核對如下；完整拒絕範圍的 claim 受 F1 限制 | 有紀錄；不以 self-verification 宣告 closure |

## 6. FA §3.2 與 CL-B1-11 L-1～L-6

| 項目 | 核對與結論 |
| --- | --- |
| FA 要達成結果 1／closure 1–2 | 串流寫法兩邊、holdout／excluded、自動／指定的 24 cases 通過；pace 單獨串流拼法也拒絕。8.3 pace 拼法必須逐字在 listing；非 pace 拼法比對 pace 自身短檔名。兩邊各四個 regression cases 通過；非 pace 短檔名的邏輯測試以替換 short_name 的回答排除磁碟區依賴，無 skip／xfail。但整份清單／未選取衝突的範圍 **不滿足，見 F1** |
| FA closure 3 | R1-F1 十個變體、load_manifest conflict、正常不同檔的 tests 均保留並通過；cycle 2 未修改 segments.py／test_ingest.py |
| FA closure 4 | 最終程式與測試 subject 的完整 E-1 見 worklog §11.4；本次自行重跑如 §3 |
| FA closure 5–6 | source_key docstring 不再宣稱涵蓋所有拼法；worklog §10.1／§10.4 明確更正、§11 引用 DA。殘餘分類正確，H-2／3／4 有更新；然而「whichever trips are requested」及完整拒絕的覆蓋仍須隨 F1 更正 |
| CL-B1-11 L-1 | `test_ingest_cli.py:347` 的自動／指定兩例，加第 363 行相反方向 excluded 一例；實際 `os.link`，非 mock。全數通過，exit 2、零 GPX open、無輸出、訊息不含檔名 |
| L-2 | 第 378 行 symlink mode／reparse 屬性 × 自動／指定四例，以替換 pace 的 lstat 回答走 main 完整流程，不依賴建立連結權限，全部通過。worklog 如實記真實 symlink NOT RUN；本 reviewer 另在 worktree cache 嘗試也得到 winerror 1314，見 §7 |
| L-3 | 第 89、125、232 行三個正向 tests 的 assertions 無變更，本次通過 |
| L-4 | worklog §11.2 列清單 is_file/read_text、目錄 listdir（名稱）、pace lstat/GetShortPathNameW、pace ET.parse、輸出 mkdir/write_text。逐一對照 source 與 `gpx.py`：非 pace 條目僅作字串處理，沒有 stat／resolve／readlink／hash 等作用其上。第 403 行 spy test 輔助證明，只用 open hook 不足以證明 metadata；本次有完成原始碼核對 |
| L-5 | 歷史殘餘已劃除／更正，C-9-5b 由 CL-B1-11 取代。hard link 與 pace symlink 已實作，殘餘只留不同目錄項目的複本、非 pace 那邊的連結等；這些與 TOCTOU 沒有被本 reviewer 另立 finding。完整 manifest refusal claim 的缺口併 F1 |
| L-6 | E-2 增列 link tests，E-5 明列檔案系統操作及 link fail closed。相應測試實際通過；FA 全 scope 的不足仍為 F1 |

**允許／禁止操作的判斷：**lstat 與 GetShortPathNameW 的參數都從被選中的 pace、且已逐字存在於 listing 的 source_file 組成；所有這些檢查完成後才進 `read_gpx`。清單角色衝突檢查只用字串，無非 pace metadata 查詢。`os.listdir` 只使用名稱，沒有使用 DirEntry 附帶 metadata。CL-B1-11 選取後連結檢查與「非 pace 不碰檔案系統」部分成立。F1 的 required fix 仍必須遵守此限制。

## 7. 補充自行探測與高風險最低核對

所有補充程式以 PowerShell here-string 傳給 **`python -`**，沒有新增探測腳本。使用 `tempfile.TemporaryDirectory(dir=Path('.pytest_cache').resolve())`，assert 路徑在 cwd 內，結束後由 context manager 清理自己的合成目錄。匯入的是本 worktree `src`，生成器用 `runpy.run_path('tests/test_ingest_cli.py')` 取得；不讀私有資料。

| 探測命令／內容 | 實際結果 |
| --- | --- |
| `python -`：真實 8.3 查詢＋完整 main(argv) 的四個 selection／literal 對照，audit hook 記錄 GPX open | F1 的四行輸出；只有未選衝突、選其他 pace 的短檔名案例 exit 0 |
| `python -`：Unicode 大小寫候選探測（i／dotless-i／dotted-I） | 兩個 Unicode 候選在此磁碟區不存在對應檔，不構成重現；ASCII 大小寫對照被拒絕。沒有據此提出 finding |
| `python -`：listdir OSError、lstat OSError、short_name OSError、非 regular、link count 0、第二個被選項為真實 hard link | 六例全部 exit 2、GPX open 空集合、沒有兩個輸出檔。第二個項目有問題時，前面的正常 pace 也不開啟 |
| 上述 fail-closed probe 的首次執行 | 前三個 OSError 案例符合；第四例因 reviewer 製造的 os.stat_result 其 st_file_attributes 為 None 而 TypeError，腳本 exit 1。這是 probe fake 不符合 Windows lstat 的欄位型別，未作產品 finding；改用含整數 st_file_attributes 的 SimpleNamespace 後，上列六例完整重跑且成功。沒有修改產品或測試 |
| 同一 `python -`：trip_role=`unrecognized` 的項目 | exit 0，只開正常 pace `p.gpx`，沒有開非 pace；確認任意非 pace 值皆被略過 |
| 同一 `python -`：對合成檔 `os.symlink` | 失敗，winerror 1314；真實 symlink CLI 觀測 **NOT RUN**，替換 lstat 的 L-2 證據已執行 |
| `python -` 啟動 subprocess：`python -m moto_copilot.ingest --gpx-dir <cache 合成 gpx> --out <cache out>`，PYTHONPATH 指向本 worktree src | exit 0；T901 601 points、8 rows、only pace；private/public/pair 三個 contract check 全為 OK；report violations 全空。這是獨立 C-2 重驗，未使用 `.venv` |
| `python -` 擷取 `git ls-files -z`，只輸出禁止 pattern 計數；不輸出路徑清單或讀取對應檔案 | `.env=0, *.key=0, *.gpx=0, *.fit=0, data/=0`，涵蓋 Bindings 所列三個 data 子目錄 |
| 同一 `python -` 擷取完整 `git diff 0c109aa..4b69201`，對 key-like value patterns 作計數 | `sk-ant-` 長值／api key assignment 長值的命中數 0；沒有輸出可能的憑證值。這是有界樣式檢查，不宣稱證明所有可能的秘密皆不存在 |

| 高風險類別 | 最低核對結論 |
| --- | --- |
| **H-2** | 已核對追蹤路徑計數、diff 與 synthetic fixtures／evidence 的來源；輸出 private rows 仍寫到呼叫者指定 out，公開版不含 start_time、無經緯度。沒有外部服務呼叫，沒有改變錨點代換；既有 trim 測試與新增 trim-boundary 測試通過。CL-B1-11 的非 pace metadata 限制符合。真實資料需 acceptor，未宣稱驗證 |
| **H-3** | 結果數目與自行執行可對應；四個 xfail 未記成 pass，未執行真實實驗如實標示。選中的 pace 之 link／alias 保護有實際證據，沒有新證據證明 holdout 被開啟；但 FA 的整份清單拒絕與完整 claims 尚有 F1，不作整體 PASS。未把 Spike／合成測試當 E1 Lite／E2；用語符合限制 |
| **H-4** | 時間總和、假停留不加里程、short ≤ stopped、gap suspect／null 不補值均由實作及 tests 核對；manifest 缺漏／錯誤／未知代號與新增 filesystem 查詢失敗為明確錯誤。六個 reviewer failure probes 亦無 partial GPX open。全清單角色矛盾例外見 F1。Planner、規則 5、路線採用與 API timeout 不在本票變更範圍，不冒稱已涵蓋 |

C-2 的 producer gap（少 short_stop_time_s）在合成資料上已解決；這項判斷不等於以真實行程重建，也不代表整張 #9 closure。C-9-7 的缺檔／不在 listing 改為整次拒絕，符合 FA 可在開檔前拒絕拼法的 fail-closed 方向；未據此增加設計要求。C-9-4 文件工作仍歸 AB-12。

## 8. NOT VERIFIED、NOT RUN 與後續 authority

| ID | 項目與原因 | Required authority／owner |
| --- | --- | --- |
| NV-1 | 真實行程清單／GPX 重建的契約符合性、實際 excluded 角色值：需要私有資料，本票排除且未授權。只確認程式對任意非 pace 字串皆拒絕選取／不開啟 | **acceptor**（RB-7），承接 C-9-3；不自行取得資料 |
| NV-2 | 真實騎乘資料所在磁碟區的 8.3 設定及跨角色 link／複本是否存在；本次的真實短檔名觀測只對 cache 中合成檔有效 | **acceptor**；承接 FA NV-2 與 CL-B1-11 §7 A-2 |
| NV-3 | G-ING 殘餘：不同檔案內容相同、非 pace 為指向 pace 的符號連結，以及所需 metadata／hash 的來源；CL-B1-11 第 4 項不分配給 #9，未測私有資料也不藉此 blocking | Orchestrator 追蹤 G-ING；需要取得保留行程 metadata／內容的授權為 **acceptor**（CL-B1-11 §7 A-1） |
| NV-4 | 本次 Primary rollout 的全部 model／effort／sandbox 與存取紀錄核對，在 worktree 內無該原始證據；事件 15 尚記進行中。包含 §3 首次 pytest 的被拒絕 worktree 外暫存存取，須由派工者如實處理 assignment eligibility；本 reviewer 不自行豁免 | **派工者／Orchestrator**，依 Bindings §3.3 回填事件 15，保留完整存取核對，不得寫成從未嘗試外部 temp 存取 |
| NR-1 | 真實 symbolic-link CLI 測試因 winerror 1314 無法建立 link，NOT RUN；無 skip／xfail，L-2 的不依賴特權測試已通過 | 無須為 #9 額外取得系統權限；如實保留證據限制 |
| NR-2 | E1 Lite、E2、G-REG、Executor 歷史 mutation checks：本 reviewer 未執行，沒有把它們當本次結果；完整 Spec integration 亦非本 audit | 真實實驗／私有資料由 **acceptor**；SIA 由 Orchestrator 另派 |

本次 R1 的 finding 應交 #9 Executor targeted correction，再由 Primary 依 cycle 2 R2 範圍核對；不自行增加 round、不作設計裁決、不 promote。FA §3.3 對同一 root cause 在 cycle 2 R2 後的進展限制繼續適用。本檔只新增 audit record；最終 git status 應由派工者一併核對。

Verdict: BLOCKING
