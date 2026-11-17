# Issue #12 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，接受版本 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-UI0 v1（`derivation-spec-ui0.md` §2、§4 CL-UI0-1～5、§5 #12 與 E-1～6）→ Issue #12 UI-0 |
| 契約補充 | `decision-20261118-issue12-ui0.md`；`decision-20261117-high-risk-categories.md`；`decision-20261117-oc1-first-run-derivation.md` |
| Subject | 本 dedicated worktree 的 detached HEAD；BASE `3906e077ab850c027d7833b30d3eebfa16f67761`，HEAD `e836c99ddcc770e0d09e3e9c7dd2a3efdc86ba7d`；實作 commit `6a278b40dc79dcbede9486902e52dc8504a8d30e` |
| Audit kind | **Ticket independent audit，R1，cycle 1；不是 Spec Integration Audit**。依派工與 run record §1 第 4 項，不使用單 Ticket fast path |
| Role／作者 | `primary_reviewer`／Codex，本 record 由本 reviewer 自行寫入 |
| 日期 | 2026-11-18 |
| Run record | `docs/governance/records/run/run-20261117-oc1-run2.md`，以下簡稱 run record |

## Assurance 與 independence

| Property | 本次的滿足方式與證據界線 |
| --- | --- |
| Independent context | 本次是派工指定的 fresh Codex thread；沒有 Executor 對話或推理歷史。從 accepted contract、原始碼、git 歷史、測試及正式紀錄形成判斷；worklog 的 PASS 只作待驗證主張。沒有派工 subagent |
| Verifiable binding | Bindings m3 §3.3、§8.2 #7 宣告 Codex qualification 與核對機制；本次 binding 應由 dispatcher 核對 rollout 的全部 `turn_context` 並記入 **run record §6 本次「#12 R1」dispatch event**。受審 HEAD 的該節目前只有 #42（Executor）、#43（DA）、#45（audit 環境）、#44（acceptor follow-up），**尚無本次 R1 的 dispatch／binding event**。因此本 record 不虛構 event 編號或觀測值；採用前由 dispatcher 補記，見 NV-3 |
| Autonomous access | 自行核對 detached HEAD、BASE、完整 diff 的範圍、各 commit 與原始檔，執行兩個指定 pytest 指令、文字比對與獨立 AppTest 重現；沒有把 pack 當作閱讀上限。首次 pytest 的暫存目錄錯誤及後續限制措施見檢查紀錄，未隱藏此事件 |
| Self-written record | 本 reviewer 直接新增本檔，未修改 implementation、tests、contract、worklog 或 gate。Dispatcher 應依 Bindings §3.3 核對寫入事件、唯一新增檔及 SHA-256，原樣採用 |

**實際 model 的證據：** Executor 是 `claude-opus-5-5`／`high`：run record §6 event **42** 記載 agent `acf4b1c528124a22e`，244 則觀測且 mapping 符合。Primary 是本次 **Codex**；run record §1 第 4 項指定的目標 mapping 是 `gpt-6.1-sol`／`high`，但目標不等於本次實際 binding 證據。本 reviewer 未取得可在此 worktree 核對的本次 rollout，故 **no model diversity claim**；不把歷次 audit 或 qualification probe 的 model 當成本次實測。四項 properties 中 binding 的完成核對須由 dispatcher 補齊後才能採用為有效 formal audit；本 record 不自行豁免該要求。

## Findings

### R1-F1 — 單向回覆忽略明確的休息取消選項

- **Severity：Medium；blocking。Owner：#12 Executor。**
- **契約：** Issue #12「六個畫面區塊」§2 明訂：「回覆是單向時，『去程』『回程』的答案不使用。選『不安排這段休息』一律取消那一筆休息。」這是 Skeleton 必須示範的操作行為，適用 UI0-1、UI0-4；不要求實作後端排程或重算 ETA。
- **原始碼證據：** `app/ui0_mock_app.py:350` 開始的方向題回覆分支，在第 352～353 行遇到單向時直接新增「示範觀景台／20 分鐘／騎士指定（行程描述）」；只有後續 `elif` 才檢查 `OPTION_NO_REST`。`app/ui0_mock_app.py:332` 又把單向的整題回覆改成「未使用（行程型態是單向）」，連取消選項也一起隱去。
- **獨立重現：** AppTest 選 `s06b` →「規劃」→ `clarify_trip` 選「單向」→ `clarify_direction` 選「不安排這段休息」→「回覆並繼續規劃」。無 exception，休息表仍含 `{'地點': '示範觀景台', '方向': '—', '長度': '20 分鐘', '來源': '騎士指定（行程描述）'}`。同一操作選「來回」時，騎士指定的休息列為空，確認缺陷限於單向分支。另有 Profile 預設休息不屬於本 finding 的取消標的。
- **既有驗證的缺口：** `tests/test_ui0_skeleton.py:330` 只驗證單向時方向不必答、回覆顯示未使用，沒有驗證「單向＋取消」。603 個測試通過沒有覆蓋此組合。
- **Required fix：** 在顯示回覆與組成模擬休息列時保留明確取消的效果；單向只忽略去程／回程方向選擇。補上此操作組合的 regression evidence，並保留未選方向即可回覆單向及來回方向必答的行為。無須引入 Validator、排程或 ETA 計算。
- **Authority：** Executor targeted correction；如對「一律取消」有語義爭議，required authority = Design Authority。`decision-20261118-issue12-ui0.md` §2.2 的「#12 無要求」針對 C-1 的未定休息地點／方向組合，沒有免除本 Issue 已明寫的取消要求；本 finding 不要求提前實作該 decision §2.4 的整合設計。

### R1-F2 — UI0-7 所需的完整鍵盤操作證據尚未具備

- **Severity：Medium；blocking。Owner：#12 Executor（補驗與 worklog）；required authority = acceptor（目前工具無法完成的 OS 選檔及實際鍵盤檢視）。**
- **契約：** UI0-7 要求「所有操作都可以只用鍵盤完成」；CL-UI0-4 要有實際瀏覽器操作紀錄；E-3 要逐條記結果，治理 §3.8 要必要 evidence 滿足後才能結案。標準元件的名稱或可取得焦點不能證明已完成操作。
- **證據：** `docs/governance/records/worklog/issue-12.md:182` 明載 OS 檔案對話框無法操作，改用 DataTransfer 放入檔案；行程描述與 GPX 路徑的打字、日曆彈窗、Snapshot Mode 切換也沒有逐一以按鍵操作。該列標示「大部分 PASS；一項 NOT VERIFIED」，實際列有多項未完成檢查。E-2 的 `focus()` 加 Enter 是 375 px 量測操作，不能補足未走完的 keyboard-only 流程。
- **判斷：** 已有真實 browser 證據足以支持記錄中那些已操作的部分；不足以關閉整條 UI0-7。這不是宣稱元件不能用鍵盤操作，也不是因本 reviewer 沒有瀏覽器就拒絕 Executor 的證據。缺口由 Executor 自己的紀錄直接證實。CL-UI0-4 保留後續 UI Delta Review，不等於免除 Ticket 的鍵盤證據要求；run record event 44 的 routing 也不是驗收條款變更。
- **Required fix：** 補具只用鍵盤選取多個合成／空 GPX、更新 Profile，以及上述未操作欄位與控制的逐步實際紀錄；列明操作、按鍵、結果與 subject。可由 acceptor 或具備所需能力者執行，再由 Executor 如實更新 UI0-7／UI0-10。無法執行者保持 BLOCKED／NOT VERIFIED，不能用「標準元件」推定 PASS。若要把缺少的 evidence 排除於 Ticket closure，須由相應 authority 作明確 clarification／contract change，Reviewer 不代為豁免。

沒有另列 non-blocking finding。下方已知限制有 disposition 與 owner；它們不構成新增的 acceptance requirement。

## Scope、實際指令與結果

所有 shell 指令的 cwd 均為本 worktree；沒有呼叫 GitHub、網路服務或執行 `experiments/`。沒有啟動獨立 Streamlit server 或瀏覽器，故沒有待停止的 server。AppTest 在程序內執行畫面程式。

### Subject 與檔案檢查

- `Get-Location`、`Get-Command python | Select-Object -ExpandProperty Source`、`python -c "...sys.executable...is_relative_to(Path.cwd())..."`：PATH 的 `python` 是本 worktree 的 `.venv/Scripts/python.exe`，`inside worktree: True`。全程使用指令名稱 `python`，沒有改用其他 checkout 或系統 interpreter 執行測試。
- `git rev-parse HEAD`、`git rev-parse 3906e07`、`git symbolic-ref -q --short HEAD`：與檔首完整 SHA 相符，symbolic-ref exit 1，確認 detached HEAD。
- `git log --oneline 3906e07..e836c99`、`git log --format='%h %s' --name-only 3906e07..e836c99`、`git diff --stat 3906e07..e836c99`、`git diff --name-status 3906e07..e836c99`、`git diff 3906e07..e836c99`：共 4 個 commit、10 個變更路徑，完整 diff 2595 行。只有 `6a278b4` 修改四個 `app/*.py`、`tests/test_ui0_skeleton.py`、`.streamlit/config.toml`、`pyproject.toml`；其後 `d5962aa`、`41fd10c`、`e836c99` 只改 `docs/governance/records/**`。
- `git diff --name-only 6a278b4..e836c99`：僅 DA decision、run record、#12 worklog 三個 record 路徑。
- `git diff 3906e07..e836c99 -- docs/ui/ prototype/ src/`：無輸出；沒有改 frozen baseline 或後端。`git diff --quiet 873e37a..e836c99 -- DESIGN.md docs/ui/UI_CR01_DELTA.md docs/ui/UI_DESIGN.md docs/ui/UI_FLOW.md docs/ui/UI_ACCEPTANCE.md docs/cr/CR-01-appendix/ui0_decision_table.md` exit 0，引用的 spec sources 與 accepted 版本一致。
- `git diff --check 3906e07..e836c99`：無輸出。寫 record 前 `git status --short` 為空、`git diff --quiet` exit 0。
- 透過指定路徑的 `Get-Content -Encoding UTF8`、`rg -n` 閱讀 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3、OC-1、SPEC-UI0 derivation、三份列明的 decision records、run record、#12 worklog、四個 app 原始檔、UI 測試、pyproject 與 Streamlit 設定；閱讀 `DESIGN.md` §9.6、DELTA §11／12 及相關路線條目、U-1～U-22 與裁決、三份 G3 frozen UI 文件的適用基線。治理閱讀包含 §2.3、§3.8、§4.1～4.7；impl-default v2 §6／7；orch-default v2.2 §6／7。這些資料用於契約與 Ticket 審查，未重新執行 G3 Review。

### pytest 與環境錯誤的完整揭露

1. 最初直接執行 `python -m pytest -q`：`505 passed, 98 errors in 37.26s`。錯誤是 pytest 的 `tmp_path` 預設嘗試 `os.scandir` worktree 外的 `pytest-of-yotsu` 暫存目錄，被 sandbox 以 `PermissionError: [WinError 5]` 拒絕；沒有取得該目錄內容。接續的首次 `python -m pytest -q -rxX` 已開始，發現同一錯誤後中止，exit 1，**不是完成的成功執行**。這是未預先限制 pytest 暫存路徑造成的存取嘗試，不能描述成本次所有工具從未嘗試 worktree 外路徑。未探查該外部目錄；dispatcher 採用前亦須核對此存取事件。
2. 將暫存與 pytest test artifacts 限制在已存在的、git-ignored `.pytest_cache` 後，重新執行兩個指定指令。PowerShell 設定與結果如下；沒有改追蹤中的設定或測試：

   ```powershell
   $env:TEMP = Join-Path (Get-Location) '.pytest_cache'
   $env:TMP = $env:TEMP
   $env:PYTEST_ADDOPTS = '--basetemp=.pytest_cache/r1-temp-a'
   python -m pytest -q
   # 603 passed in 21.47s; exit 0
   $env:PYTEST_ADDOPTS = '--basetemp=.pytest_cache/r1-temp-b'
   python -m pytest -q -rxX
   # 603 passed in 20.76s; exit 0
   ```

3. `rg -n 'xfail|skip' tests/`：exit 1，0 個匹配；兩次成功執行沒有 xfail、xpass 或 skip。556 個既有測試加 47 個 UI-0 測試，共 603。
4. `python -c "import importlib.metadata as m; ..."`：pytest `9.2.0`、jsonschema `4.26.0`、Streamlit `1.67.0`，符合派工環境。

首次暫存錯誤不是本 Ticket 的 implementation finding；成功重跑支持 E-1，但不掩蓋初次執行的錯誤與路徑限制事件。

### 獨立內容與操作檢查

- `rg -n` 於明確指定的 `app/`、`tests/test_ui0_skeleton.py`、`.streamlit/config.toml` 搜尋 imports、檔案讀取、logging、網路與受限用語；另以 `python -` 的 AST 掃描列出四個 app 模組 imports：只有 `__future__`、`datetime`、`re`、`streamlit` 與三個 app 本地模組。逐函式閱讀確認沒有匯入 `moto_copilot`、動態後端載入、API 呼叫、GPX 解析或內容寫檔／log。上傳 callback `app/ui0_mock_app.py:83` 只取檔案數，目標 GPX 路徑只作文字輸入。
- `git ls-files -- '.env' '*.gpx' '*.fit' '*.key' 'data/raw/*' 'data/private/*' 'data/bmw/*'` 的結果在程序內計數：**0**；沒有輸出或讀取私有檔案。檢查變更、synthetic fixture 與 worklog：地點是 app 明寫的「示範…」，日期是合成 `2026-12-06`；guard 座標樣本是 Issue 示範用途的合成近零值；上傳測試是空 bytes 與不含軌跡的 GPX 標頭。沒有將真實 GPX 當測試資料。
- **UI0-3：** 以 `python -` 在記憶體建立 expected 值，直接從本次派工附的 Issue #12 原文逐項抄錄，與 `ui0_texts` 用 `==` 比較，沒有空白或標點正規化；不是拿 implementation 自己當 expected。結果：`39 named strings + 14 error strings + 5 reason labels + 11 guidance mappings; mismatches=0`。AST 再列舉固定文字區所有 assignment 名稱：`UNCHECKED_FIXED_NAMES: set()`；`CATEGORIES` 由三個已比對的名稱組成。人工核對選項列表、UNKNOWN 指引對應、Issue 佔位及 `fill()` 渲染呼叫，沒有文字差異。Issue 全文 hash 以派工提供值 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be` 對照 BD-3 #12 列一致；未連線取得或宣稱重新雜湊完整 Issue body。
- **獨立 AppTest：** 用 `python -` 執行 `AppTest.from_file('app/ui0_mock_app.py', default_timeout=60).run()`，操作 `scenario=s06b`、`plan`、`clarify_trip`、`clarify_direction`、`clarify_reply`，比較單向／來回的休息表。輸出與 R1-F1 相符，兩者 exception 都是 0。沒有新增測試檔或修改實作。另查看 s08 的畫面；嘗試用 `at.get('badge')` 取得 badge 回傳空集合，故**沒有**用此 API 的空集合推論畫面沒有標籤，標籤檢查依原始碼與既有 render tests。

## 六個區塊、情境與 UI0-1～10

| 區塊 | 已核對的實作及 evidence；例外另列 |
| --- | --- |
| Profile | expander、多檔 gpx uploader、明確更新按鈕、摘要三個 metric 與三類 table；status 在 expander 外緊接其下、不顯示百分比。callback 只取檔案數並換成合成結果，舊結果過期、不自動規劃；s01～s03 與 upload AppTest 涵蓋 |
| 自然語言與追問 | text_area 及固定 caption、guard 的三種門牌與成對小數、國道 3 號／台 9 線不擋、兩種路線輸入皆空及油量必填；六種題目分配於 s05、s06a、s06b，一輪回覆，s07 在描述欄下報錯且無計畫。取消例外為 R1-F1 |
| 行程型態與期限 | radio 可未選；期限以 widget key 保留時間值，s09 與測試驗證 16:45 切換來回／單向保留；worklog E-2 第 11 列另有 browser 操作。出發錨點 caption、日期、出發時間、油量、路徑文字欄與 Snapshot Mode 存在。模擬結果不依所有表單值重算的限制已寫明 |
| 路線確認 | container 在追問之下、過期提示之上、兩分頁之外；行程型態、里程、道路順序、來源、路權固定句子、去回差提示存在，沒有地圖或強制確認按鈕；s08、s09、s10、s14。來源快照標籤的契約對照疑義另記 Q-1 |
| 路線錯誤／評估失敗／UNKNOWN | s11a～g 對應六碼七則文字；s12 沒有計畫狀態／出發時間／路線確認；評估失敗的重試方法在 Issue 固定錯誤訊息內。s13 四條 UNKNOWN 呈現缺失、原因分類與原因、來源與時間資訊、固定指引及不會改成 PASS 的附句 |
| 天氣、加油與休息 | s08 去回分表、回程規則 3 範圍、去程 75% 的高降雨機率提醒；單向三列、每列預報時段與時長；s10／s13 無來源列 UNKNOWN。加油同站去回兩列；休息列有地點／長度／來源；s14 預設餘裕係數及整趟不套用預設休息，另指定休息保留 |

情境 inventory：Issue 1→s01、2→s02、3→s03、4→s04a／b、5→s05、6→s06a／b、7→s07、8→s08、9→s09、10→s10、11→s11a～g、12→s12、13→s13、14→s14，另有 s15。合計 **23 個選項**，每項 label 都有「模擬」；成功重跑的 UI tests 逐項 render，Executor E-2 操作表對應全部情境及兩分頁。情境存在不代表所有選項組合正確，R1-F1 即其反例。

| AC | R1 判斷 |
| --- | --- |
| UI0-1 | 六區與必要情境已具備，AppTest 可渲染；操作行為有 R1-F1，不能整條關閉 |
| UI0-2 | 在 1.67.0 使用標準元件；47 個 UI tests 通過。worklog §7 逐項記錄 dataframe CSV 工具列、table 儲存格上色替代、tabs 切換等限制；沒有新增 framework |
| UI0-3 | 獨立逐字比較無差異，含七則路線錯誤與人工指引 |
| UI0-4 | 一輪與單向免答方向已驗證；取消選項違反 Issue，見 R1-F1 |
| UI0-5 | label 切換與原值保留有 AppTest 及記錄的 browser evidence；未選型態的「期限」文字有記錄 |
| UI0-6 | 接受 worklog E-2 的逐步 browser 量測作為 CL-UI0-4 允許的證據：375×812、doc／main 寬度、未裁切溢出、展開與兩分頁都有記載。沒有截圖不單獨構成缺陷。本 reviewer 未親自 browser 重跑，記 NV-1 |
| UI0-7 | 已記錄操作的部分有證據，完整 AC 尚未驗證，見 R1-F2、NV-1 |
| UI0-8 | worklog §7 有 CR-P1～6、B1～7、R1～4、C1～8、D1～2、F3／4 對照，合成顯示與整合後驗收有分開；後端判定未以 mock 冒充完成 |
| UI0-9 | synthetic 來源與模擬標示可追溯到 literal 資料；沒有讀取私有資料或真實歷史行程作比對 |
| UI0-10 | worklog §7／§9.2 記錄結果、限制、差異；取消問題及 keyboard evidence 補齊後須更新，不能沿用現有 closure 主張 |

## CL 與 E-1～E-6

| 項目 | R1 判斷 |
| --- | --- |
| CL-UI0-1 | 程式在 app；只依賴標準函式庫、Streamlit 1.67.0 與 app 本地模組，無 src imports |
| CL-UI0-2 | app 不讀、解析、保存或記錄 upload 內容；元件本身顯示檔名與大小、框架暫存依 DA decision §3.2／4.2 的有效 clarification 評估，不重開 C-2／C-3；框架生命週期未在本次動態實測，NV-2 |
| CL-UI0-3 | UI0-10 位於指定 worklog；沒有改 docs/ui 或 prototype |
| CL-UI0-4 | UI0-6 有可評估的逐步記錄；UI0-7 evidence 不完整，R1-F2 |
| CL-UI0-5 | 規則結果、計畫狀態及候選排序都是情境字面值；app 只選擇顯示與表單檢查，沒有 Validator-like computation。_pass／_fail／_unknown helpers 包裝寫定狀態，不從量測值判定狀態；整合後驗收只列出 |
| E-1 | 兩次完成的獨立 full pytest 603 passed，無 skip／xfail |
| E-2 | worklog E-2 記載實際 Streamlit 啟動指令、localhost log／200、逐情境 browser 操作及停止；與 AppTest／原始碼互相支持。原始 browser transcript、啟動 log 不在本 worktree，NV-2，不假裝重看；keyboard 缺口不能由此補足 |
| E-3 | 逐條紀錄與元件替代存在，UI0-7 尚缺完整驗證；R1-F2 |
| E-4 | 原 worklog 的 script 不在本 worktree，故本次另以 supplied Issue 值獨立比較，不依賴其自述結果 |
| E-5 | diff、app literals、合成 fixture、紀錄與模擬標示已核對；沒有 screenshot artifact 可另查，沒有宣稱檢查過不存在的截圖 |
| E-6 | worklog §6 E-6 確實逐項記 H-2／H-3；本 reviewer 的最低核對如下。UI0-7 evidence 仍不足，不能用 self-verification 段落使其 PASS |

## H-2、H-3 最低核對與風險分類

**H-2：** release-gate 禁止路徑的 tracked count 是 0；變更中資料的合成來源可在 scenario literals、測試 bytes 與明示的 MOCK_DATE 追溯。沒有 app 的第三方請求或對外 prompt，`.streamlit/config.toml:6` 關閉 usage statistics，server address 是 localhost。上傳 app 只取 len、不寫 log、不讀內容；框架行為依有效 DA clarification，未把「app 不保存」擴大宣稱為框架永不使用磁碟。隱私裁切、錨點代換與真實 GPX 保存程式不屬本 Ticket，沒有要求或宣稱已完成其測試。需要私有資料的實際重建或隱私驗證記 NV-4，required authority = acceptor；沒有取得該資料。

**H-3：** UI 字串無 P90／百分位宣稱；「高降雨機率提醒」附非氣象署警特報、非強度的說明；隱私採 U-7 修正文；路權說明保留「不是道路主管機關的驗證」與 GPX 未檢查限制；涵蓋比例未聲稱一定騎過同一道路；沒有與 Google Maps 準確度比較或已驗證折返啟發式的宣稱。狀態標籤遵循 G3 的文字及顏色，頁首、情境、結果及來源列標示模擬。沒有開啟保留行程的 app 程式路徑，沒有執行 E1／E2，worklog 沒有把本 UI preview 寫成 E1 Lite／E2 結果。獨立 pytest 證據已取得；Executor browser 證據的可支持範圍與缺口分開判斷，特別是 R1-F2。

**H-1／H-4：** 本 delta 沒有憑證或付費呼叫，不新增 H-1；沒有規則計算、候選排序或真實休息排入／路線採用邏輯，不新增 H-4。R1-F1 是模擬回覆與畫面資料不一致，修正須維持 CL-UI0-5，不藉修正加入後端排程；若 Executor 採用會新增該類判定的修法，須 route Design Authority 重新分類。

## Concerns、routing 與 NOT VERIFIED

| 項目 | Disposition／owner |
| --- | --- |
| C-1 | 依 DA decision §2.2，對 Skeleton 無新增要求；整合語義由 §2.4 約束之後整合 Spec。Owner：之後整合的 Design Authority；不重開為本票 finding |
| C-2／C-3 | 依 DA decision §3.2／4.2，在 clarification 範圍內符合；不要求 #12 改 framework 上傳元件。Owner：之後整合的 Design Authority，納入保存期間、大小／檔名與暫存限制；本次動態驗證界線見 NV-2 |
| **C-4** | root `.streamlit/config.toml` 是必要 Streamlit runtime 設定，內容只有 telemetry、toolbar、localhost／headless；CL-UI0-1 的 app 程式位置限制沒有禁止 root runtime 設定。屬契約內 HOW，沒有 scope finding。Owner：#12 Executor 維護既有記錄 |
| **C-8** | Issue 寫「情境選單至少包含」14 項，s15 只呈現既有無可行解的合成資料，沒有新增後端或改 G3；在範圍內，沒有 scope finding。Owner：#12 Executor |
| C-5～C-7 | 未寫定文字、模擬結果不隨所有表單輸入重算、標準 dataframe CSV 工具列：既有 worklog 已說明。Owner：acceptor 的 UI Delta Review；tracked，不代表已接受產品行為或已完成該 Review。沒有把計畫下載的 Should 功能加入 app |

**Q-1（契約適用性 routing，非 blocking finding）：** Issue §4 寫「路線引擎的路線帶『資料快照』的標籤」，DELTA §11.1 CR-R3 則以 Snapshot Mode／一般模式重用快照為條件。`app/ui0_mock_app.py:371` 只在表單 snapshot 為真時顯示該 badge；s14 涵蓋 Snapshot Mode，普通 engine 模擬情境沒有該 badge。**Required authority = Design Authority**：確認 Issue 該句是否要求所有 engine 模擬情境都顯示 badge，或只要求代表快照的情境。這是引用條款的適用性疑義，依治理 §4.2 route，沒有自行補成新 requirement；clarification 如要求修正，須有相應 evidence。SIA／phase acceptance 應追蹤此問題。

| NOT VERIFIED ID | 未驗證內容、原因及 required authority |
| --- | --- |
| NV-1 | Reviewer 無 browser，未親自量測 375 px 或走 keyboard-only。已評估 worklog 的實際操作紀錄，UI0-6 可由該證據支持；UI0-7 中 OS 選檔與其他未操作部分仍不足，見 R1-F2。required authority = **acceptor**（CL-UI0-4 的實際 UI Delta Review／缺項補驗）；不將待補操作記 PASS |
| NV-2 | 本 worktree 沒有 Executor 的 scratchpad scripts、Streamlit 原始 logs、browser tool 原始 transcript；沒有 screenshot。未到 worktree 外取得，框架 spool／關閉刪除也未在本次動態實測。required authority = **#12 Executor**（提供可在允許範圍內核對的 evidence）；框架保存契約的判斷由 **Design Authority**。此限制本身沒有推翻已存在且允許的逐步操作記錄 |
| NV-3 | 本次 Primary 精確 model／effort／完整 turn_context 與存取紀錄未由本 reviewer 核對；受審 HEAD 沒有本次 R1 dispatch event，不能拿 event 42 或 45 代替。required authority = **dispatcher／Orchestrator**，依 Bindings §3.3 補記本次 event、binding、record hash 與存取核對；包含初次 pytest 被拒的外部暫存列舉嘗試。若判定不符 Bindings，依其規則處理，不能因本 record 已寫出 verdict 就省略 qualification |
| NV-4 | 真實騎乘資料的正確性、真實 upload／保存／隱私裁切、正式 API 與後端判定：本票排除且無私有資料授權，未執行。required authority = **acceptor**（RB-7；後續工作的資料授權），語義／整合設計由 Design Authority；不構成本票新增需求 |

R1-F1 需要 targeted correction；R1-F2 需要補齊驗證或由相應 authority 處理契約。兩者未解決前不能宣告 Ticket audit closure。後續 R2 僅核對這兩項的修正、回歸與修正直接暴露的 blocking defect；另行 SIA 與 acceptor 的 UI Delta Review 均未由本 record 代行。

Verdict: BLOCKING
