# Issue #12 — cycle 1 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，接受版本 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-UI0 v1（`derivation-spec-ui0.md` §2、§4 CL-UI0-1～5、§5 #12 與 E-1～6）→ Issue #12 UI-0（本次派工所附全文；提供的 UTF-8 SHA-256 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be` 與 BD-3 對應，未連線取得 Issue） |
| 契約補充 | `decision-20261118-issue12-ui0.md`、`decision-20261118-issue12-ui07.md`、`decision-20261117-high-risk-categories.md`、`decision-20261117-oc1-first-run-derivation.md` |
| Subject | 本 dedicated worktree 的 detached HEAD；BASE `3906e077ab850c027d7833b30d3eebfa16f67761`，HEAD `ca91406187a8c5877ae8d23b6f8fd09749d1e40f`；R1 subject `e836c99ddcc770e0d09e3e9c7dd2a3efdc86ba7d`；correction commit `619268ad2732b4cdd04593ff20ebe35374a7710c` |
| Audit kind | **Ticket independent audit，R2 closure review，cycle 1；not a Spec Integration Audit**。不使用單 Ticket fast path |
| Role／作者 | `primary_reviewer`／Codex；本 reviewer 自行寫入本 record |
| 日期 | 2026-11-18 |
| Run record | `docs/governance/records/run/run-20261117-oc1-run2.md`，以下簡稱 run record；本次派工沿革為 §6 **event 50 的 R2 重派（attempt 2）** |

## Assurance

| Context independence property | 滿足方式、證據及界線 |
| --- | --- |
| Independent context | 本次為 fresh Codex thread，不繼承 Executor 或 R1 reviewer 的對話與推理。從磁碟重讀 R1 record、修正後的程式、測試、worklog 與 DA 裁決；Executor 的結果標籤只作待驗證主張。未派 subagent |
| Verifiable binding | 依 Bindings m3 §3.3，由 dispatcher 核對本次 rollout 全部 `turn_context`、存取事件與 record 寫入事件，記入 run record §6 event 50 的 attempt 2。**受審 HEAD 的 event 50（run record:128）目前只記 attempt 1 的 usage-limit failure 與重派安排，沒有本次 attempt 2 完成後的 binding 證據。** 不把 attempt 1 的 model、thread 或 13 次工具呼叫當成本次證據。正式採用前仍須 dispatcher 完成核對，見 NV-R2-3 |
| Autonomous access | 在本 worktree 自行核對 git subject、歷史、BASE diff 的路徑與 hunks、R1 後全部實作修正，閱讀原始材料，執行兩個指定 pytest 指令與獨立 AppTest 操作矩陣。未受限於 Executor 的摘要；沒有探查其他 checkout、私有資料或憑證 |
| Self-written record | 本 reviewer 直接新增本檔；不修改 implementation、tests、contract、worklog、gate 或 R1 record。Dispatcher 依 Bindings §3.3 核對唯一新增檔與 SHA-256，原樣採用；本檔寫入事件為作者證據 |

四項 properties 依上述機制落實；其中本次 binding 的外部核對由 dispatcher 完成後才可採用為有效 formal audit，本 record 不自行豁免該要求。

| Model diversity evidence | 實際可確認內容 |
| --- | --- |
| Executor | run record:122 的 event 42 為 `claude-opus-5-5`／`high`（244 則）；修正 event 47（:125，348 則）與 record 更新 event 49（:127，350 則以上）也是同一 agent `acf4b1c528124a22e`，dispatcher 記載 mapping 符合 |
| Primary | 本次為 **Codex**。run record §1 第 4 項及 event 50 指定 `gpt-6.1-sol`／`high`，但指定值不等於本次實際 binding。受審檔案尚未記本次 rollout 的完整觀測，本 reviewer 不讀取 worktree 外的 rollout |
| Claim | **no model diversity claim**。不以 qualification、R1 或失敗的 attempt 1 代替本次精確 model／effort 證據 |

## 範圍與檢查紀錄

依治理 §4.4 與角色 definition，本次限於 R1-F1、R1-F2 是否解決、修正回歸，以及修正直接產生或暴露的 blocking defect；沒有重做無限制 full audit，沒有執行 SIA、phase acceptance 或 UI Delta Review。

所有指令的 cwd 都是本 worktree。未呼叫網路或 GitHub，未執行 `experiments/`，未啟動獨立 Streamlit server 或瀏覽器，沒有需停止的 server。AppTest 僅在測試程序內執行 app。唯一新交付檔為本 record；測試 artifacts 限於 git-ignored pytest cache。

### 閱讀與 subject 核對

- 以 `Get-Content -Encoding UTF8 -LiteralPath ...`、分段行號輸出與指定路徑的 `rg -n` 重讀 `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3（特別是 §3.3、§5、§7）、OC-1 的範圍／接受紀錄、SPEC-UI0 derivation、R1 record 全部內容、兩份 #12 DA records 的適用裁決、run record 的指示與 events 42～50、worklog 的原始證據及 §10 修正紀錄。閱讀治理 §2.3、§3.8、§4.1～4.7，impl-default v2 §6／7、orch-default v2.2 §6／7、高風險判定 §5。對照 DESIGN §9.6、DELTA §11／12 的引用範圍、UI0 decision table 與 G3 文件中適用的凍結／操作條款；未重開 G3 Review。
- `git rev-parse HEAD`、`git rev-parse 3906e07`：完整 SHA 與檔首一致。`git symbolic-ref -q --short HEAD` 無輸出（detached HEAD）。寫 record 前 `git status --short` 為空，`Test-Path .../issue-12-c1-r2.md` 為 False。
- `git log --oneline 3906e07..ca91406`：12 個 commits。`git log --format='%h %s' --name-only e836c99..ca91406`：R1 後只有 `619268a` 修改 implementation／tests，其餘只改 `docs/governance/records/**`。
- `git diff 3906e07..ca91406` 在記憶體取得完整 diff，3106 行；輸出並核對全部檔案與 hunk 索引，配合 `git diff --stat 3906e07..ca91406`（12 檔，3024 insertions）及原始檔閱讀界定 R2 範圍。沒有把原始新增的全部功能重新作第二次 full audit。
- `git diff e836c99..ca91406 -- app tests`：完整閱讀兩處程式修正及新增測試；`--numstat` 為 app 11 additions／3 deletions、tests 81 additions／0 deletions。`git diff --name-only 619268a..ca91406` 只有 UI0-7 decision、run record、worklog 三個 record 路徑。
- `git diff --quiet e836c99..ca91406 -- .streamlit/config.toml pyproject.toml app/ui0_guard.py app/ui0_scenarios.py app/ui0_texts.py`：exit 0。runtime 設定、合成資料與固定字串未因 correction 改變。
- `git diff --quiet 3906e07..ca91406 -- DESIGN.md docs/ui/ prototype/ src/`：exit 0。`git diff --quiet 873e37a..ca91406 -- DESIGN.md docs/ui/UI_CR01_DELTA.md docs/ui/UI_DESIGN.md docs/ui/UI_FLOW.md docs/ui/UI_ACCEPTANCE.md docs/cr/CR-01-appendix/ui0_decision_table.md`：exit 0。引用的 spec sources 與 accepted 版本相同，後端與 frozen baseline 未改。
- `git diff --check 3906e07..ca91406`：exit 0，無輸出。
- `git show e836c99:docs/governance/records/worklog/issue-12.md` 分段重讀原 UI0-7 列，並閱讀 `git diff e836c99..ca91406 -- docs/governance/records/worklog/issue-12.md` 的更新段落：區分原有 Tab／分頁證據、原缺項與 K1～K12 補驗；不把 JavaScript `focus()` 的 375 px 量測當成 keyboard-only evidence。

### 自行執行的 pytest

`Get-Command python | Select-Object CommandType,Source` 與 `python -c "...sys.executable...Path(sys.executable).is_relative_to(Path.cwd())..."` 確認 PATH 的 python 位於本 worktree，`inside worktree: True`；metadata 顯示 pytest `9.2.0`、jsonschema `4.26.0`、Streamlit `1.67.0`。測試一律呼叫名稱 `python`，沒有以明列的虛擬環境路徑啟動、遍查其目錄或選用外部 interpreter。

先限制 TEMP、TMP、pytest basetemp 於本 worktree；沒有讓 pytest 探查外部預設暫存目錄：

```powershell
$env:TEMP = Join-Path (Get-Location) '.pytest_cache'
$env:TMP = $env:TEMP
$env:PYTEST_ADDOPTS = '--basetemp=.pytest_cache/r2-temp-a'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -m pytest -q
# 513 passed, 98 errors in 28.96s; exit 1
```

這次 98 個 errors 是 fixture setup：本 worktree 尚無 `.pytest_cache` 父目錄，pytest 建立其 basetemp 子目錄時得到 `FileNotFoundError [WinError 3]`。這是 reviewer 的測試環境準備錯誤，不是 app 的 failure；保留失敗，不宣稱第一次即全通過。建立允許的 cache 目錄後重跑：

```powershell
New-Item -ItemType Directory -Path .pytest_cache -Force | Out-Null
# TEMP、TMP、PYTHONDONTWRITEBYTECODE 同上
$env:PYTEST_ADDOPTS = '--basetemp=.pytest_cache/r2-temp-b'
python -m pytest -q
# 611 passed in 23.30s; exit 0
$env:PYTEST_ADDOPTS = '--basetemp=.pytest_cache/r2-temp-c'
python -m pytest -q -rxX
# 611 passed in 25.18s; exit 0
```

另執行 `rg -n 'xfail|skip' tests/`，exit 1、無匹配（兩次檢查一致）；成功的兩個 full suite 沒有 skip、xfail、xpass。611＝R1 的 603＋8 個 regression cases。沒有修改測試或降低 gates。

### 獨立 AppTest 操作

以 PowerShell here-string 傳入 `python -`，只在記憶體執行，沒有新增 script 檔。使用 `AppTest.from_file('app/ui0_mock_app.py', default_timeout=60).run()` → scenario `s06b` → `plan` → `clarify_trip`／`clarify_direction` → `clarify_reply`；直接用 Issue 的文字建立 expected，從渲染表格取得回覆與休息列，不呼叫 implementation 的休息 helper 當 oracle。

第一次 here-string 因 PowerShell 管線編碼把中文字變為 `??`，AppTest 在套用 radio 值時回報 `ValueError: '??' is not in list`，exit 1，沒有取得有效操作結果。設定 `$OutputEncoding = [System.Text.UTF8Encoding]::new($false)` 後重跑，以下 8 組 assertions 全通過，exit 0，末行 `independent matrix: 8/8 OK`（中文 stdout 的顯示仍有編碼問題，判斷依成功執行的 assertions）。AppTest 的 bare-mode `missing ScriptRunContext` warnings 不屬 app exception。

| 行程型態 | 方向回覆 | 實際結果 |
| --- | --- | --- |
| 單向 | 不安排這段休息 | 回覆保留取消文字；騎士指定休息 0 筆；Profile 預設休息保留 |
| 單向 | 去程／回程／未答（3 組） | 回覆顯示未使用；騎士指定休息 1 筆、方向「—」；Profile 預設休息保留；沒有第二輪 |
| 來回 | 不安排這段休息 | 回覆保留取消文字；騎士指定休息 0 筆；Profile 預設休息保留 |
| 來回 | 去程／回程（2 組） | 回覆及騎士指定休息方向符合選項；Profile 預設休息保留；沒有第二輪 |
| 來回 | 未答 | 拒絕回覆，有欄位提示，保留兩題追問，沒有 plan tabs |

## R1 blocking findings 的逐項結論

### R1-F1 — RESOLVED

- **原 severity：Medium／blocking；本次沒有 residual blocking。Owner：#12 Executor。**
- 契約依據：Issue §2 的「不安排這段休息」一律取消，單向只忽略去程／回程；UI0-1、UI0-4。
- `app/ui0_mock_app.py:332` 的單向回覆顯示新增 `answer != T.OPTION_NO_REST` 條件，明確取消不再被改為未使用。`:355` 的模擬休息列先檢查取消，再處理單向／來回；`:366` 仍保留獨立的 Profile 預設休息。
- `tests/test_ui0_skeleton.py:494` 驗證單向取消及回覆文字，`:503` 涵蓋單向去程／回程／未答，`:509`、`:516` 涵蓋來回取消與兩方向，`:522` 涵蓋已知來回 s06a；既有 `:330` 的來回必答／單向免答未改。兩個 full suites 與上述獨立 8 組矩陣均通過。
- worklog:296 的 **K12** 另有修正 subject 上的 keyboard-only browser 操作及最終休息表；其證據與 app／AppTest 一致。worklog:179、:275 的 K9 交叉引用誤植另列 R2-N1，不能用錯誤的引用編號冒充檢查。
- **Required fix：原要求已滿足，無額外程式修正。** 修正限於回覆顯示與合成資料列，沒有加入 Validator、真實休息排程或 ETA 計算。

### R1-F2 — RESOLVED；UI0-7：PASS（限 #12 的頁面操作範圍）

- **原 severity：Medium／blocking；本次沒有 residual blocking。Owner：#12 Executor。**
- 契約依據：UI0-7、CL-UI0-4、E-3，並套用 `decision-20261118-issue12-ui07.md` §3.1～3.2、§4.2～4.3。DA 界定 scope；各操作 evidence 是否充分由本次 reviewer 判斷。
- worklog:279～281 指明 browser 環境、correction subject `619268a`、工具及按鍵限制、只讀觀測與兩個非鍵盤例外。`619268a..HEAD` 為 record-only，沒有使這批瀏覽器操作的實作 subject 失效。

| 瀏覽器 evidence | 本次判斷 |
| --- | --- |
| K1、K2（worklog:285～286） | 從載入以 Tab 到情境選單、輸入篩選與 Enter 選取；Enter 開 Profile、未選檔時按更新取得提示。記錄含可達路徑與可觀察結果，可支持這些操作 |
| K3（:287） | Shift+Tab 到 Upload，Enter／Space 各觸發一次多選且接受 `.gpx` 的 file-input 請求。capture listener 只記錄並取消對話框請求，不代移焦點或點擊；充分支持頁面啟動控制項。**沒有證明 OS 對話框內的選檔** |
| K4、K5、K6（:288～290） | K4 明標 DataTransfer 注入不是鍵盤，只作邊界後的測試準備；K5 記錄 Tab／Shift+Tab 與 Enter 移除合成檔，K6 以鍵盤更新後取得處理結果、status、舊結果過期且未自動規劃。符合 DA §4.2 的頁面範圍；沒有把 K4 算作鍵盤成功 |
| K7、K8（:291～292） | 以按鍵輸入行程描述，驗證 guard；改寫公路描述、輸入目標 GPX 路徑、Space 切 Snapshot Mode、Enter 規劃，記錄欄位值、提示與快照標籤的變化。補足 R1 指出的三個實際操作缺口 |
| K9、K10（:293～294） | 彈窗方向鍵無作用的觀察保留；Tab 可離開，Escape 可關閉並還焦點，未記日期被意外改變。K10 在同一 date_input 的正常 Tab 路徑改日／月，日期與過期提示確實變更。依 DA 的操作單位及兩個條件，支持「設定日期」；不將彈窗本身記為 keyboard PASS |
| K11（:295）、既有 E-2 第 11 列（:121） | 時間與油量以按鍵變更；舊記錄另以鍵盤切行程型態、把期限由 17:00 改為 16:45，再切型態而保留值。涵蓋表單 radio、兩個時間欄與油量 |
| K12（:296）、E-2 第 8 列（:118） | Tab、Space、方向鍵及 Enter 完成同輪追問與回覆；K12 是單向明確取消，舊記錄是單向未答方向。兩者結果均無第二輪，與程式／獨立測試一致 |
| 公路與地標、分頁、全部候選 | E-2 第 18 列（:128）記 Enter 展開公路與地標；R1 subject 的 worklog §7 原 UI0-7 列明載 Tab 走訪、分頁方向鍵＋Enter、全部候選 expander；R1 已接受其已操作部分。與目前 worklog:182、:298、:304 的保留引用合看，沒有以 E-2 的 `focus()` 量測取代可達性證據 |

這些是 CL-UI0-4 明允的逐步實際操作紀錄，包含操作、按鍵、結果與 subject，不只是元件名稱或 PASS 標籤。修正後沒有仍需用「標準元件應可操作」推定的 R1 缺項。**UI0-7 在 DA 已界定的 #12 範圍內有充分 evidence，R1-F2 RESOLVED。**

K3-B 維持「範圍外、NOT VERIFIED」；K9 維持元件限制、原因未確定，已記入 worklog:199 的 UI0-2 與 UI0-10（:185）。不把後續 UI Delta Review 當成補齊本 Ticket gate 的 disposition。若有範圍內 AC 仍 BLOCKED，依 DA §4.1 就不能結案；本次不是以該方式豁免。**Required fix：原要求依 clarification 已滿足，無額外程式或 browser 修正要求。** 本 reviewer 無 browser 的親自重跑界線見 NV-R2-1。

## 回歸、evidence 與高風險核對

- 修正的分支順序同時保留「單向免答方向」「單向不採去回方向」「來回方向必答」「取消只影響該筆騎士指定需求」「Profile 預設休息保留」，沒有新增第二輪；兩處 app hunks之外無實作變更。未發現 correction 直接產生或暴露的新 blocking defect。
- **E-1：** 本次自行完成兩個 full pytest，611 passed，無 skip／xfail。**E-2：** R1 的 Streamlit／情境 browser evidence 與本次 K 紀錄相互對應；不宣稱親自重看原始 browser transcript。**E-3：** worklog:176～185、:199、§10 已記修正、限制與待 R2 結果，本 record 給出 UI0-7 的判斷；交叉引用小誤植見 R2-N1。**E-4：** 固定文字模組、情境與相關 sources 未變，沒有重做 R1 的全量逐字比對；新取消回覆直接使用既有常數並由 AppTest 驗證。**E-5：** correction 及新增 evidence 只含明示的合成情境、檔名／路徑與資料，無新私有資料來源。**E-6：** 以下為 R2 對 H-2／H-3 的 delta 核對，原 R1 的完整核對不因此重開。
- **H-2：** app correction 沒有新增 import、讀檔、GPX 內容解析、保存、log 或外部呼叫；上傳 callback 仍只取檔案數（app:83）。K4 明載合成／空檔與記憶體注入，不含真實軌跡。原合成 fixtures、scenario literals、runtime 設定未改；沒有觸及私有資料路徑。R1 的 release-path 核對記為 0，本次沒有重新搜尋禁止路徑；不把這一點寫成新的完整 release gate。真實隱私裁切／錨點代換不屬本 correction，NV-R2-4。
- **H-3：** 修正沒有新增受限制宣稱、保守 ETA 或降雨門檻判定，沒有新增 holdout 路徑；未執行 E1 Lite／E2，未把 mock 檢查稱為正式實驗。worklog 保留 K3／K4 非鍵盤例外、K3-B 未驗證及 K9 元件限制，沒有虛報它們通過。reviewer 的環境錯誤與重跑結果也如實記載。
- **H-1／H-4：** delta 未新增憑證、付費、規則結果計算、候選排序或真實排程。R1-F1 修正在模擬回覆／列的呈現範圍內，沒有藉 correction 擴張 operating scope。
- UI0-6 沿用 R1 已接受的 E-2 375×812、doc／main 375、未裁切溢出 0 的逐步量測。correction 沒有改版面、widget、CSS 或表格 schema，只改回覆字串選擇與休息列內容；未發現會推翻其既有 coverage 的 layout 變更。本 reviewer 未親自重新量測，不把 AppTest 當 viewport evidence。

## 新 non-blocking finding

### R2-N1 — 取消休息的 browser evidence 有兩處錯誤編號

- **Severity：Low／non-blocking。Owner：#12 Executor。**
- **Evidence：** `docs/governance/records/worklog/issue-12.md:179`（UI0-4）、`:275`（R1-F1 browser 說明）都指向 K9；實際 K9（:293）是日曆彈窗，取消休息操作在 K12（:296）。
- **依據與影響：** UI0-10／E-3 要求結果可追溯。正確 K12 及完整操作結果已存在、subject 清楚，§10.2 的表也可直接定位；不使 R1-F1 的實際證據消失，不影響本次 closure 判斷。
- **Required fix：** 將上述兩處 K9 改為 K12，保留原操作紀錄。
- **Disposition：** tracked，由 Executor 下次維護 worklog 時更正；不延長本 cycle，不要求 reviewer 修改 worklog。這不是新增 acceptance gate。

## NOT VERIFIED 與既有 routing

| ID | 未驗證內容／原因 | Required authority／處理 |
| --- | --- | --- |
| NV-R2-1 | 本 reviewer 無 browser，未親自重跑 UI0-6 的 viewport 量測或 UI0-7 的實體鍵盤流程；已獨立評估允許的逐步 browser evidence，兩者不能混稱 | **acceptor**：依 CL-UI0-4 在後續 UI Delta Review 實際檢視。此 Review 在本 run 外，未由本 record 代行；不因 reviewer 無 browser 而否定已充分的記錄 |
| NV-R2-2 | K3-B 的 OS 原生選檔對話框內只用鍵盤多選，未由 Executor 或本 reviewer 驗證；K9 彈窗焦點問題是元件或工具造成的原因也未確定。worktree 沒有原始 browser transcript、screenshot 或外部 scratchpad scripts，未到外部取得 | **acceptor**：UI Delta Review 可實際檢視 OS／日曆觀察；若需補原始 evidence，owner **#12 Executor**。K3-B 依 DA §4.2 範圍外；日曆本身不能聲稱已通過。日後逐元件要求由 **Design Authority** 依 DELTA 11.2 處理 |
| NV-R2-3 | 受審 HEAD 尚無本次 event 50 attempt 2 的 rollout／binding 完成核對。event 46 只證明 R1；event 50 的 attempt 1 明確沒有 audit record／verdict，不能沿用 | **dispatcher／Orchestrator**：正式採用前補本次 thread、全部 turn_context 的 model／effort／sandbox 集合、存取／寫入核對、唯一新增檔與 record hash；不符 Bindings 時依法處理。不是 #12 implementation finding，也不是可被本 PASS 免除的要求 |
| NV-R2-4 | 真實騎乘資料、真實 GPX 保存／隱私裁切、框架 spool 生命週期與正式 API／後端行為：未執行，本票／本次 correction 排除且沒有私有資料授權 | **acceptor**：RB-7 的資料授權與後續實際驗證；保存／整合語義由 **Design Authority**。不以 mock 或本次 PASS 宣稱這些功能完成 |

R1 的 **Q-1（資料快照標籤適用性）仍交 Design Authority**；本次 UI0-7 裁決明示未處理 Q-1。本次沒有新語義或實作變更足以撤銷該 routing，沒有將其升格為 R2 新 blocking，也沒有代 DA 裁決。Orchestrator 在完成核對及後續 SIA／phase acceptance 時仍須依原 routing 處理，不能將本 R2 PASS 當作 P6 已全數滿足。

寫入本 record 後執行 `git status --short`，只有 `?? docs/governance/records/audit/issue-12-c1-r2.md`；`git diff --exit-code`、`git diff --check` 均 exit 0、無輸出。以 `Get-Content -Encoding UTF8 ... | Select-Object -Last 5` 核對末行，並以 `Get-FileHash -Algorithm SHA256` 計算 record hash，供 dispatcher 原樣採用時核對。沒有 stage 或 commit。

R1-F1、R1-F2 均 **RESOLVED**；沒有未解 blocking finding。這是指定 subject 的 Ticket R2 audit closure 判斷，仍須 dispatcher 完成本次 binding／record 核對；不宣告 Ticket 的全部 completion predicates、SPEC-UI0 SIA／phase acceptance、acceptor UI Delta Review 或 release authorization 已完成。

Verdict: PASS
