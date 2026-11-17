# Issue #10 — cycle 1 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（acceptor 接受基準 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`，#10 列及三項追加 AC）→ Issue #10「B1-3 pace」。適用 CL-B1-1、CL-B1-4（依 CL-B1-12 修訂）、CL-B1-7～9、CL-B1-12～15 |
| Subject | 此 dedicated worktree 的 detached HEAD；BASE `20939aac12b29c4feaecec133f779e636c598cb9`；HEAD `8177015fb5bd22b780e4ed4cdcecc6e49347d38a` |
| Delta 基準 | R1 subject `c47716c16b4f8c500d71e67cb2791f3fc549b06a`；targeted correction `93e52b8abb2f98a0bf2f9e7701c786c2c3b57019`；CL-B1-15／最終 implementation `e4fc93b5a95494dca946b7702023bc01ddc952e6` |
| Audit kind | **Ticket independent audit, R2 closure review, cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`（Codex；Bindings m3 O-6） |
| 日期 | 2026-11-18 |
| Dispatch | `docs/governance/records/run/run-20261117-oc1-run2.md` §6 **事件 27**（第 108 行）；correction／DA ruling／CL-B1-15 return 分別為事件 24／25／26 |
| 結果範圍 | R1-F1、R1-F2 closure；修正的 regression 與直接產生或暴露的 blocking defects；CL-B1-15 delta 的首次獨立審查。沒有作 Spec phase acceptance、run completion 或 release 判定 |

## Independence 與 model assurance

| Property | 滿足方式與證據界線 |
| --- | --- |
| Independent context | fresh Codex thread，沒有繼承 Executor 或 R1 reviewer 的對話與推理。自行重讀 R1 record、修正後原始檔、契約及 worklog；所有 Executor 完成主張均作待驗證輸入。沒有委派 subagent |
| Verifiable binding | Bindings §3.3、§8.2 #7 記載 O-6 qualification 已通過。本次派工識別是 run **事件 27**；dispatcher 須依 §3.3 核對全部 rollout `turn_context` 的 model／effort／sandbox、存取紀錄及作者證據，並將核對寫入該事件。本 HEAD 的事件 27 仍是「進行中」，沒有冒稱已完成 runtime 核對；正式採用本 record 前仍須 dispatcher 完成此 gate |
| Autonomous access | 自行取得此 worktree 的治理、契約、R1 record、git history／diff、修正後程式與測試；用 PATH 的 `python` 自行測試、建立合成反例、比對完整 stdout。沒有依 Executor 的摘要限制取證 |
| Self-written record | 本檔由 Primary 自行撰寫；沒有修改 implementation、tests、contract、gate 或其他 record，沒有 stage／commit。測試暫存產物已清除。dispatcher 後續應核對只有本檔新增，原樣保存並核對 SHA-256 |

Executor 的實際 model 證據是 run record **事件 24（第 105 行）**與**事件 26（第 107 行）**：同一 agent `a54ac9cf0e452782b`，全部 assistant 訊息分別觀測 167、187 則，集合均為 (`claude-opus-5-5`, `high`)。Primary 是本次 **Codex**；事件 27 的預定 mapping 是 `gpt-6.1-sol`／`high`，本 subject 尚無本次 rollout 的觀測結果。因此此處是 **no model diversity claim**。不以角色 frontmatter、預定 mapping 或自述代替實際 binding；不讀 worktree 外的 rollout。

## 契約與審查邊界

已讀 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3（含 O-6、qualification、assurance 與 record-only 規則），以及有效 package 的治理 §2.3、§3.8、§4.1～4.7、impl-default v2 §6～7、orch-default v2.2 §7。最後一行依本次明確派工採 `Verdict: ...` 格式。

契約取證包含 OC-1 的範圍、AB、授權與接受紀錄；SPEC-B1 的 #10 列、追加 AC、CL-B1-1／4／7、E-1～E-5；first-run derivation 的 BD-3～5；CL-B1-8 的 S-3 恢復規則；CL-B1-9 的 #10 E-1 判準；CL-B1-12～14 record（特別是 invariant 3 與 minimum checks）；CL-B1-15 record 的 §3.1、§6、§7；高風險 record §5。另核對 DESIGN §5 契約 3、§6.1、SPEC-RESOLUTION-001 §1.2／1.4、SPEC-001 §5.4、BATCH-1 共通規則與 B1-3 範圍。Issue 使用派工提供的原文；pack 標示的 SHA-256 與 BD-3 #10 列相同：`880ef1341e090b86e826cd2a14812ab4a05b634b73385c3ccebea80e43245e65`。沒有向 GitHub 或任何網路服務查詢。

本次從磁碟重讀 `issue-10-c1-r1.md` 全文與 worklog §10、§11；檢閱 `validate.py` 的 helper、契約 1 與契約 3 路徑、`schemas.py` 對應 integer 欄位、`tests/test_contracts.py` 新舊相關案例與 `tests/conftest.py`。合成探測只讀 `tests/fixtures/contract_v02/mock_dataset.json`，確認 `_meta.mock = true`。

以 BASE diff 核對整體變更邊界，再逐行審查 `c47716c..8177015 -- src tests`。R1 後只有 `93e52b8`、`e4fc93b` 修改程式／測試，且都只改 `contracts/validate.py` 與 `tests/test_contracts.py`；其餘七個 commit 只改 `docs/governance/records/**`。`e4fc93b..8177015` 只有 run record 與 worklog，最終 E-1 與本次 HEAD 的 implementation 相符。

這是 scoped R2，沒有重做 #10 第二次全面 audit。CL-B1-15 的契約 2 `after_seg_count` 修正明確屬 **CL-R1-11／#13**，沒有列為 #10 缺陷或已驗證功能。沒有執行或匯入任何 `experiments/` 腳本。

## 實際檢查與結果

命令均在此 worktree 執行，測試使用 PATH 的 `python`，沒有使用或存取 `.venv`。pytest 程序設定 `PYTHONIOENCODING=utf-8`、`PYTHONDONTWRITEBYTECODE=1`，並以 `PYTEST_ADDOPTS=--basetemp=.pytest_cache/<本次名稱>` 將合成暫存限制在 worktree；沒有修改 pytest 設定。

| 命令／檢查 | 實際結果 |
| --- | --- |
| `Get-Content -Encoding UTF8 -LiteralPath <上述明確檔案>`；`python -` 以 UTF-8 讀取明確檔案及行段 | 取得上述治理、契約、R1 與 corrected evidence。初次 PowerShell／Python 顯示碼頁不符的內容，改用 UTF-8 重讀；沒有以亂碼作判準 |
| `git rev-parse HEAD`、`git rev-parse 20939aa c47716c 93e52b8 e4fc93b`、`git status --short` | SHAs 如表頭；起始工作區乾淨 |
| `git log --oneline 20939aa..8177015`、`git diff --stat 20939aa..8177015`、`git diff 20939aa..8177015` 及按明確程式／測試路徑檢閱 diff | BASE 起 11 個變更檔。整體範圍核對後，R2 聚焦 R1 後 delta；沒有從 BASE 重開既有 R1 全面審查 |
| `git diff c47716c..8177015 -- src tests`、`git diff 93e52b8 e4fc93b -- src/moto_copilot/contracts/validate.py tests/test_contracts.py` | R1-F1 helper／合計修正與 CL-B1-15 兩處交叉檢查符合授權範圍；新測試只新增，沒有修改既有案例 |
| `git rev-list --reverse c47716c..8177015`；逐 commit `git diff-tree --no-commit-id --name-only -r <SHA>`；`git diff --name-only e4fc93b..8177015` | 9 個 R1 後 commits：2 個 implementation、7 個 record-only；最終 implementation 之後只有 record-only |
| `python -m pytest -q`（`r2-default`） | exit **0**；`426 passed, 3 xfailed in 4.78s` |
| `python -m pytest -q -rxX`（`r2-reasons`） | exit **0**；`426 passed, 3 xfailed in 1.87s`；僅下列 S-4～S-6 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py tests/test_pace_table.py tests/test_contracts.py`（`r2-runxfail`） | exit **1**（CL-B1-9 預期）；`3 failed, 426 passed in 1.88s`；失敗恰為 S-4～S-6，只涉及 `stop_allow_s` 缺口 |
| `rg -n 'xfail\|skip' tests` | 只有 `tests/test_routes_pace_eta.py:163,177,186` 的三個 `strict=True` xfail，reason 均指向 `restored by #11`；沒有其他 skip／xfail |
| `python -`：以 `subprocess.run` 重新擷取上列三個 pytest 命令，逐字比較 worklog §11.3 三個 `text` blocks | exits **0／0／1**；結果依序為 `426 passed, 3 xfailed in 1.91s`、`426 passed, 3 xfailed in 1.91s`、`3 failed, 426 passed in 1.91s`。只正規化 CRLF 與 summary 的執行秒數，其餘完整 stdout **全部相等**；沒有手動縮寫或名稱替換。此次重跑目的為 R1-F2 的 durable evidence 核對 |
| `python -`：獨立合成計數／跳號 probe | 下節列出矩陣與結果；所有 assertions 通過，exit **0** |
| `python -`：`git show <SHA>:src/moto_copilot/contracts/validate.py`，在記憶體 compile 歷史版本並呼叫合成案例 | `c47716c`：錯誤 float 總數未拒絕、路段不足帶速度未拒絕；`93e52b8`：前者拒絕、後者未拒絕；`e4fc93b`：兩者均拒絕。精確區分 correction 與 CL-B1-15 的效果，沒有改寫磁碟上的程式 |
| `python -`：以 AST 比較 R1 與 HEAD 的函式 | `validate.py` 既有函式只改 `validate_derived_segments`、`validate_pace_table`，只新增 `_whole_count`；`tests/test_contracts.py` 沒有既有函式被改或刪除。另確認相對 `93e52b8` 的 `_whole_count` 與契約 2 函式 AST 完全相同 |
| `git diff --check c47716c..8177015 -- src tests` | exit **0** |
| `rg -n '^\| (24\|25\|26\|27) \|' docs/governance/records/run/run-20261117-oc1-run2.md`；Bindings qualification 明確路徑查詢 | 核對 Executor 觀測、DA ruling、最終 return 與本次事件 27。沒有開啟其列出的外部 transcript 路徑 |
| `git ls-files -- <明確安全路徑清單>` | 151 個條目；只列明確的程式、文件、測試等路徑，未查詢私有目錄。這不是完整 release privacy gate 的宣稱 |
| 測試產物與 `git status --short` 核對 | 中途發現 `.pytest_cache/` 的自訂 basetemp 未被 Git 忽略，reviewer 的「status 應空白」assertion 因此失敗；不是產品測試失敗。清除本次產物後 status 為空；寫入本 record 後再核對只有本檔新增 |

清理只針對本 worktree 的 `.pytest_cache`：先核對絕對位置與內容，清單恰為 `r2-default`、`r2-reasons`、`r2-runxfail`、`r2-stdout-1`～`3`、`v`。PowerShell recursive cleanup 曾被工具 policy 拒絕，沒有執行；改以明確 allowlist、拒絕根目錄 symlink、檢查每個 link target 都在 cache 內的 Python 清理完成。沒有動到其他路徑、追蹤檔或 git index。

三個 XFAIL／`--runxfail` failure 的完整集合：

```text
tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
```

S-4 在第 167 行的第一列只差 `stop_allow_s: 0.0`；S-5 第 182 行缺兩個 `stop_allow_s` 必填欄位；S-6 第 191 行缺必填欄位及 status ok 時的值。S-3 不帶標記通過；S-4～S-6 的內文與標記在 R1 後完全未改，BASE diff 也只有其他 pace 斷言與 S-3 標記的既有修改。三個 xfail **不是通過**；這些數字不是 E1 Lite／E2 結果。

## Findings closure

### R1-F1 — RESOLVED

- **原 severity：Medium／blocking；owner：#10 Executor。** 契約依據為 CL-B1-12 §3.2「合計一律檢查」。
- **原 required fix**：總數檢查涵蓋 schema 接受的合法整數表示；不可計數者明確違反；加入不同 scheme 的正確／多計／少計 float、混合型別與 JSON round trip；保留同 scheme 逐類別檢查，不加入 scheme 解析或重分類。
- **實作證據**：`src/moto_copilot/contracts/validate.py:83` 的 `_whole_count` 排除 bool，有限整數值 float 轉 int；第 274～280 行對不能合計的值回報 invariant 3，否則一定比較合計；第 281～286 行保留同 scheme 逐類別核對。`tests/test_contracts.py:284`～323 新增 17 個 regression cases，全部在全套測試中通過。
- **獨立核對**：以 `[1,2,2]`、`[1,2,3]`、`[1,1,2]`，各欄位 int／float 的全部 8 種組合，再各做 raw／JSON round trip，共 **48 例 PASS**。正確總數得到 `[]`，錯誤總數分別回報 `n_segments add up to 6, but 5 rows are eligible`／`add up to 4`。同 scheme 的正確 float 表通過，同總數錯分配仍回報 `C1 n_segments is 3.0, but 2 rows are eligible`。非整數、bool、null、字串、NaN、正負 Infinity **7 例**均回報不可計數。
- **Closure／required fix 狀態**：要求已滿足，無剩餘 required fix；沒有將此 closure 擴大為驗證器能識別「一列多計、一列漏算但總數相同」或重算分類的宣稱。

### R1-F2 — RESOLVED

- **原 severity：Medium／blocking；owner：#10 Executor。** 契約依據為 SPEC-B1 E-1、CL-B1-9 第 3 項及 CL-B1-12 §8 的完整 stdout requirement。
- **原 required fix**：在最終 implementation subject 重跑三個 E-1 命令，把完整 stdout、exit code 與 subject 識別放入 worklog，不以「同上」或人工改名取代，並保留舊歷程。
- **Durable evidence**：`docs/governance/records/worklog/issue-10.md:490`～603 保留 `93e52b8` 修正與三份完整輸出；第 **647～756 行**明確以 `e4fc93b5a95494dca946b7702023bc01ddc952e6` 作新的最終 E-1，附三個命令、exit codes **0／0／1**、完整進度、三段 traceback 與 summary。舊輸出沒有被刪除或冒充最終結果。
- **獨立核對**：重新擷取三個命令的 stdout，與第 654～743 行三個 code blocks 比較；僅換行正規化與執行秒數不同，其餘逐字相同，包含三段 `data = {...}`、mock 中文名稱與 pytest 自己的省略顯示。這些 `...` 是 pytest 原生輸出，沒有 worklog 作者縮寫。最終 subject 後只有 record-only commits。
- **Closure／required fix 狀態**：完整 evidence requirement 已滿足，無剩餘 required fix；不需要存取 Executor 的外部 scratchpad。

## CL-B1-15 delta 的獨立判定

**結果：PASS；沒有 blocking finding。** 依 `decision-20261118-issue10-c107.md` §6、§7，這是同一 cycle 的 delta review，沒有新增 round。

| 要求 | 核對與結果 |
| --- | --- |
| 契約 3 兩項 min_segments 檢查對合法整數表示執行 | `validate.py:248`～255 先以 `_whole_count` 取得兩個計數；比較方式、原訊息不變。不能計數時不加新訊息，由既有 schema 拒絕。獨立 raw／JSON、int／float、帶／不帶 derived rows、兩個違反方向共 **32 例 PASS** |
| 契約 1 seg_index 不跳號 | `validate.py:128`～130 轉換全部索引後沿用 `_contiguous`；不能計數者不執行此交叉檢查。全部 8 種 int／float 組合 × raw／JSON × 跳號／不跳號，共 **32 例 PASS**；正常序列沒有任何違反，跳號均有原訊息 |
| §6 測試 (i)～(iv) | `tests/test_contracts.py:326`～350：C3 `1.0` 帶速度、min `2.0` 帶不足路段、C2 `2.0` 缺速度，各測 raw／JSON，6 例通過 |
| (v) 正確 float 表不誤報 | 第 353～362 行，全部 n 與 min 都為整數值 float，raw／JSON 均 `[]`，2 例通過 |
| (vi) 不可計數值不放行 | 第 365～375 行，n 與 min 的非整數、bool、null、字串、NaN 共 10 例通過；另以獨立 probe 不帶 derived rows 測兩欄各 7 個無效值，共 **14 例 PASS**，確認不是靠 invariant 3 補擋 |
| (vii) float 跳號／不跳號與 JSON | 第 378～388 行，4 例通過；另有上述混合表示矩陣 |
| 只改兩處；保留其他檢查 | `93e52b8..e4fc93b` 只含兩處與模組說明；`_whole_count`、R1-F1 invariant 3、`pace_eligible`、schema 與契約 2 不變。沒有修改 pace／ingest／routes／fixture／conftest／pyproject／DESIGN |
| E-2／E-4／mutation／E-5 | worklog §11.2 逐項對應 (i)～(vii)，E-4 明確只新增 22 案例；第 645 行記錄只退回契約 3 guard 為 6 failed、只退回契約 1 為 2 failed、兩者為 8 failed，以及還原後結果。§11.4 記錄 H-4 與合成來源。歷史 mutation 操作不是本 reviewer 親見，未冒稱獨立重演；本次以歷史 source 的記憶體探測與獨立正反矩陣確認缺陷與修正 |
| Commit 與最終 E-1 | `e4fc93b` 與 `93e52b8` 分開，前者只含指定兩檔且 message 註明 CL-B1-15；worklog §11.3 完整輸出與本次重跑一致，符合 CL-B1-9 |

`validate_dataset` 對既有合成 fixture 的所有違反清單仍為空。R1 後新增的 17＋22＝39 個案例與全套由 387 增至 426 的結果一致。沒有發現修正引入 regression，或直接產生／暴露而仍未處置的 blocking defect。

## 高風險範圍的核對

| 類別 | 本次 R2 delta 核對與界線 |
| --- | --- |
| H-2 | 新測試只修改既有 synthetic fixture 的副本及計數值，fixture 檔案未改。delta 沒有 GPX 讀取、新的檔案輸出入口或外送；pytest 的暫存合成檔均在 worktree，已清除。沒有重新宣稱完成整個產品的裁切／錨點代換或真實資料隱私驗證 |
| H-3 | R1-F1 false clean 已消除；R1-F2 的最終 stdout 有 durable、可比對證據。保留中間結果，明確區分 3 xfailed 與通過；沒有把此次檢查寫成 E1／E2，沒有新增禁止用語宣稱。pace 的角色拒絕、版本分離與不覆寫程式自 R1 未改，全套 regression 通過 |
| H-4 | min_segments 不足帶速度、足夠缺速度，對各 int／float 表示均拒絕；不可計數者 schema 不回傳 clean。既有 null／default／錯誤路徑的程式沒有被放寬，全套通過。沒有延伸到 Planner、規則 5、路線採用等不屬本 delta 的功能 |

新增 findings：**無**。新增 non-blocking findings：**無**，不需 disposition、deferral 或新增 owner；沒有 gate waiver。

## NOT VERIFIED／NOT RUN 與 required authority

| 項目 | 原因與 required authority |
| --- | --- |
| 真實配速行程重建、留一趟、G-REG，私有位置與 holdout 隔離的真實資料驗證 | **NOT VERIFIED／NOT RUN**。本票排除且 RB-7 未授權明確私有路徑；沒有嘗試取得資料。required authority = **acceptor** |
| E1 Lite、E2、holdout 解封 | **NOT RUN**，不在此次驗收授權。required authority = **acceptor** |
| 本次 Codex rollout 的實際 model／effort／sandbox、完整存取紀錄與 record 作者核對 | **NOT VERIFIED by reviewer**。worktree 內事件 27 尚進行中；依 O-6 由 **dispatcher／Orchestrator** 完成並記錄，採用本 audit 前須核對。沒有讀外部 rollout 或憑證 |
| Executor 當時的 raw stdout 擷取過程與 mutation 操作歷程 | **NOT VERIFIED as historical execution**，未版控原始操作紀錄不在此 worktree；責任為 **Executor**。已獨立核對 worklog 保存的最終 stdout 與本次執行相同，並以歷史 source／新案例核對行為；沒有依歷史自述單獨作 closure |
| SPEC-B1 的整合、SB1-AC2／AC3、phase acceptance；#13 的 CL-R1-11 | **NOT RUN as SIA／非本次 scope**。由 **Orchestrator** 另派適用工作與 Spec Integration Audit，再由 **Design Authority** phase acceptance；不把契約 2 或仍有 3 個 xfail 的 Spec gate 記為完成 |

R1-F1、R1-F2 均 RESOLVED；CL-B1-15 delta PASS；本次 scoped closure review 無未解 blocking。正式採用仍須 dispatcher 完成事件 27 的 binding／作者／存取 gate；本 record 不代替其他 completion predicates。

Verdict: PASS
