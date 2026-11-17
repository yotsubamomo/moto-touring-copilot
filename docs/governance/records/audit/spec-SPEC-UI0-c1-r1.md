# SPEC-UI0 — Spec Integration Audit，cycle 1 R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受版本 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-UI0 v1（`docs/governance/records/decisions/derivation-spec-ui0.md` §2、§4、§5、**§6、§7**）→ Issue #12 |
| Subject | 本 dedicated worktree 的 detached HEAD；BASE **`3906e077ab850c027d7833b30d3eebfa16f67761`**，HEAD **`ca07b7c1a680fe309e9aa82321c3a9af269f1a3e`**；最後 implementation commit `619268ad2732b4cdd04593ff20ebe35374a7710c` |
| Audit kind | **Spec Integration Audit of SPEC-UI0，R1，cycle 1（full independent audit；not a Ticket audit）** |
| Role／作者 | **`primary_reviewer`／Codex**；本 record 由本 reviewer 自行寫入 |
| 日期 | 2026-11-18 |
| Run record | `docs/governance/records/run/run-20261117-oc1-run2.md`（以下簡稱 run record） |
| 契約補充 | `decision-20261117-oc1-first-run-derivation.md`（BD-2、BD-3）、`decision-20261117-high-risk-categories.md`、`decision-20261118-issue12-ui0.md`、`decision-20261118-issue12-ui07.md`、`decision-20261118-issue12-q1.md`，均位於 `docs/governance/records/decisions/` |

本次依 run record §1 第 4 項與其後「SPEC-UI0 的 fast path」說明，另做治理 §4.7 的 SIA。#12 Ticket R1、R2 不是 SIA；本 record 不將它們重新標示。判斷對象是最終整合 subject 與完整 Spec 引用範圍，不限於 Ticket R1 的兩項 findings。SPEC-UI0 不是 OC-1 最後一份未結 Spec，不核對全部 derived Specs 的總分配涵蓋。

## Assurance 與 independence

| Property | 本次滿足方式、證據與界線 |
| --- | --- |
| Independent context | 這是本次派工的 fresh Codex thread，沒有繼承 Executor 或 Ticket reviewers 的對話／推理。自行閱讀 accepted contract、最終程式、測試、git 歷史與正式 records；worklog 與既有 PASS 都作為待核對主張。沒有派工 subagent |
| Verifiable binding | 適用 Bindings m3 §3.3 O-6 與 §8.2 #7 的 qualification／dispatch 機制。當次全部 rollout `turn_context`、實際 model／effort／sandbox、存取與寫入核對，應由 **dispatcher 記在 run record §6 本次「SPEC-UI0 SIA R1，cycle 1」dispatch event 的 binding 欄位**。受審 HEAD 的 event 清單至 #54，尚無本次 SIA event，因此目前沒有可誠實引用的本次 event 編號；不拿 #46（Ticket R1）、#51（Ticket R2）或 #42（Executor）代替。見 NV-SIA-3；正式採用前必須由 dispatcher 補齊，不能以本 verdict 豁免 |
| Autonomous access | 在本 worktree 自行取得完整 diff、歷史、原始檔及規範，執行兩個指定 pytest 命令、marker 搜尋、靜態核對與獨立 AppTest；pack 不是閱讀上限。第一次 pytest 的外部暫存列舉嘗試被拒，已於下節完整揭露；沒有取得該目錄內容 |
| Self-written record | 本 reviewer 直接建立本檔，沒有修改 implementation、tests、contracts、gates 或他人 records。Dispatcher 依 Bindings §3.3 核對唯一新增檔、寫入事件與 SHA-256，原樣採用；不由 Executor 轉述或改寫 |

四項 properties 由上述機制落實；binding 與原樣採用的外部核對仍須 dispatcher 完成後，本 record 才能作為有效 formal audit 使用。本 reviewer 不讀取 worktree 外的 rollout 來代行該核對。

**Models（與 context independence 分開）：** run record:122 的 event #42 記 Executor `acf4b1c528124a22e` 為 `claude-opus-5-5`／`high`（244 則）；:125 的 #47（348 則）與 :131 的 #53（371 則）核對同一 Executor 的修正及 record 更新，mapping 符合。本 Primary 是 **Codex**；run record §1 指定目標 `gpt-6.1-sol`／`high`，但指定值、qualification 或先前 reviewer 的觀測不等於本次實際 binding。當次精確 model 證據尚未記入受審 run record，故 **no model diversity claim**。

## Findings

### SIA-R1-F1 — Spec 明列的「Planner 補充說明未通過」合成呈現缺漏

- **Severity：Medium／blocking。Owner：#12 Executor（同一 worklog identity）。**
- **契約與 Spec 層影響：** `derivation-spec-ui0.md:26` 引用 `UI_CR01_DELTA.md` 第 11 節；該文件 **:364（§11.3）明列以「Planner 的補充說明沒通過規則 5」取代舊「說明改用固定模板」情境**，:329（CR-C3）要求補充說明通過才顯示。Issue 的 14 個情境是最低清單，不排除這個已被 Spec 明文引用的介面情境。這是可用寫定資料示範的顯示行為，屬 UI0-8 的合成介面驗收與 derivation §6 的 evidence coverage，並影響 §7 分配的 AB-8 Skeleton 交付完整性。
- **實作證據：** `app/ui0_mock_app.py:525` 顯示模板後，:528 無條件 `st.write(plan["planner_note"])`，:529 無條件宣稱這段模擬補充說明通過規則 5。`app/ui0_scenarios.py:156` 的 `RULE5_PASS` 被五份 FEASIBLE／CONDITIONAL plan 使用（:207、:267、:329、:383、:439），它們都有非空的 `planner_note`；唯一沒有補充說明的是 INFEASIBLE（沒有可用計畫），不代表「模板保留、補充說明不顯示」。完整 23 項情境均無該路徑。
- **獨立核對輸出：** 以 `python -` 逐項列印最終 `S.PLANS` 的 status、rule5、補充說明是否非空：五份有計畫資料均為 `rule5=PASS, has_nonempty_planner_note=True`；`plans_with_template_but_no_supplement=[]`。另閱讀全部 scenario menu、render 分支與 `tests/test_ui0_skeleton.py`，沒有對應的情境或 omission assertion。這是最終 Spec 的 coverage evidence；不是重開 Ticket R1-F1／R1-F2。
- **現有證據不足之處：** `worklog/issue-12.md:221` 將 CR-C3 的「規則 5 通過才顯示」全部放在整合後驗收，只檢查模板與來源文字。真正判定規則 5 當然留給後端，但 §11.3 已明列的「不顯示補充說明」畫面仍能以 literal 合成資料呈現。`611 passed` 與現有 browser 操作紀錄沒有覆蓋它。UI0-8 的完整 PASS 因而不成立。
- **Required fix：** 在本 Skeleton 的合成情境中補齊上述狀態，保留固定模板，省略未通過的 Planner 補充說明及其「通過」caption；不恢復已取消的「已改用固定模板」提示。由情境資料明寫模擬結果，renderer 依資料顯示即可，**不得新增 Validator 判定、LLM 呼叫、規則結果計算或真實後端整合**。提供能驗證這項顯示差異的 regression／操作 evidence，並更新同一 #12 worklog 的 UI0-8、UI0-10／CR-C3 對照。修正後依實際 delta 提供相應 verification，由 SIA R2 核對 closure 與回歸。
- **Authority：** 契約內 targeted correction 交 Executor；若對 Spec §11.3 的適用性有實質爭議，route **Design Authority**，不得由 Executor 或 Orchestrator 自行排除該引用。既有 Q-1／Q-1b 裁決只處理來源標籤，UI0-7 裁決只處理鍵盤 scope，均未豁免此項。

### SIA-R1-N1 — 新增 DA record 殘留本 run 不採用的 fast-path 描述

- **Severity：Low／non-blocking。Owner：`decision-20261118-issue12-q1.md` 的 Design Authority；dispatcher／Orchestrator 追蹤。**
- **Evidence：** `docs/governance/records/decisions/decision-20261118-issue12-q1.md:77` 將「SPEC-UI0 的 SIA」描述為「fast path，由 #12 R1 兼任」，與 run record §1 第 4 項、其明示的不採 fast path 說明、#12 兩份 Ticket audit 的種類不一致。這份 decision 是本 run 新增的 record，並非只保留原始 derivation 的歷史文字。
- **影響與 disposition：** 可能誤導後續 phase acceptance 引用，但本 run 的明確指示與本次獨立 SIA 已可消除實際 routing 歧義，不構成 blocking。**保留為記錄一致性 follow-up，不延長本 cycle；不因此重標 Ticket audits。**
- **Required fix：** 由 record authority 在後續獲授權的 record 維護中澄清本 run 採獨立 SIA，保留原裁決內容與歷史；phase acceptance 應引用實際有效的 SIA closure record。Reviewer 不修改該 record，也不要求修改 Frozen Baseline 或追溯改寫 derivation。

## Scope、閱讀與實際執行的 checks

本次涵蓋 SPEC-UI0 的引用、CL-UI0-1～5、E-1～6、Spec-level AC、分配的 AB-8／10／13，以及 H-2／H-3。範圍外是 acceptor 的 UI Delta Review、正式 `src/` 整合、真實資料、真實 API 與實驗結果。沒有 GitHub／網路呼叫，沒有執行 `experiments/`，沒有讀取 `data/`、`.env` 或憑證；沒有啟動獨立 Streamlit server 或瀏覽器。

### 原始材料與版本

以明確路徑的 `Get-Content -Encoding utf8`、分段行號輸出、`rg -n` 閱讀：

- `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3（生效 package、O-6、qualification、audit／record-only 規則）。
- 生效 package 內 `Minimal_Operational_Governance_v2.2_Candidate.md` §2.2～2.3、§3.8、§4.1～4.7；`references/implementation-profiles/default-v2.md` §6～7；`references/orchestrator-contracts/default-v2.2.md` §6～7 與 completion predicates。
- OC-1、SPEC-UI0 derivation 全文、BD-2／BD-3 與 AB 分配；高風險 record §3.2～3.4、§4～5；三份 #12 DA records；run record §1、§6（特別是 events 42～54）、§8.1；#12 worklog 與兩份 Ticket audit records。
- `DESIGN.md` §9.1、§9.2、§9.6；DELTA §6、§9、§11、§12；U-1～22 與修正裁決；G3 `UI_DESIGN.md`、`UI_FLOW.md`、`UI_ACCEPTANCE.md` 的適用基線；`SPEC-001-plan-schema.md` §5.1～5.5。沒有重新執行 G3 Review，沒有把 §5.5 的提案文字當成已接受的正式產品文字。
- 四個 `app/*.py`、全部 `tests/test_ui0_skeleton.py`、`tests/conftest.py`、`pyproject.toml`、`.streamlit/config.toml`。對照 supplied Issue #12 的固定文字、選項、佔位與情境；未連線取得 Issue。

| Check／實際命令 | 結果 |
| --- | --- |
| `Get-Location`、`git rev-parse HEAD`、`git rev-parse 3906e07`、`git symbolic-ref -q --short HEAD` | cwd 為本 worktree，完整 SHA 與檔首一致；symbolic-ref 無輸出、exit 1，確認 detached HEAD。初始 `git status --short` 為空 |
| `python -c "...sys.executable...Path(sys.executable).is_relative_to(Path.cwd())..."` | PATH 的 python 位於本 worktree，`python_in_worktree=True`；Streamlit 1.67.0、pytest 9.2.0。所有 Python 執行均使用名稱 `python`，沒有切換 interpreter 或到外部 checkout |
| `git diff 3906e07..ca07b7c` | 在記憶體取得完整 3503 行 diff，列出並核對全部 file／hunk 索引，再對照最終原始檔與 records；`--stat` 為 14 檔、3396 insertions、1 deletion |
| `git log --oneline 3906e07..ca07b7c` | 17 個 commits：初始實作 `6a278b4`、correction `619268a` 及治理 records；核對 scope 與兩輪 Ticket subject |
| `git diff e836c99..619268a -- app tests` | 逐 hunk 核對取消休息的兩處分支修正與新增 8 個 regression cases；沒有夾帶其他功能 |
| `git log --format='%h %s' --name-only 619268a..ca07b7c`、`git diff --name-only ca91406..ca07b7c` | 最後 implementation 之後，以及 Ticket R2 subject 之後，全部 delta 僅 `docs/governance/records/**`；符合 Bindings §7 record-only 宣告 |
| `git diff 3906e07..ca07b7c -- docs/ui prototype`；另以 `git diff --quiet 3906e07..ca07b7c -- docs/ui prototype src` 核對 | 無輸出；quiet exit 0。沒有修改 G3 Frozen Baseline、任何 `docs/ui/` 或後端 |
| `git diff --quiet 873e37a..ca07b7c -- DESIGN.md docs/ui/UI_CR01_DELTA.md docs/ui/UI_DESIGN.md docs/ui/UI_FLOW.md docs/ui/UI_ACCEPTANCE.md docs/cr/CR-01-appendix/ui0_decision_table.md` | exit 0；引用 sources 與契約指定版本一致 |
| `git diff --check 3906e07..ca07b7c` | 無輸出、exit 0 |
| `git ls-files` 的結果僅在記憶體按禁止樣式計數 | `data/`、`.env`／其變體、`.gpx`、`.fit`、`.key` 合計 **0**；未嘗試到這些路徑取得檔案 |
| 對完整 diff 的 added lines 作 credential-pattern 計數（`sk-ant-…`、長值 `api[_-]?key=…`） | **0**；沒有輸出疑似憑證值。搭配實際 source／record 閱讀，不把有限樣式掃描稱為完整憑證證明 |
| `rg -n -i 'xfail|skip' tests/` | 無匹配、exit 1；不是跳過測試。成功的兩個 full suites 均無 xfail／xpass／skip 摘要 |
| `python -` AST 列舉四個 app modules 的 imports | 只有 `__future__`、`datetime`、`re`、`streamlit` 與 app 本地模組；沒有 `moto_copilot`、動態後端載入或網路 client |
| `rg -n 'P90|百分位|分位數|Google Maps|警特報|只留在|本機|驗證|隱私' app/`，搭配逐函式／字串閱讀 | 受限宣稱符合用語規則；「警特報」僅在否定官方警特報的說明；未以「驗證」字樣誤稱折返啟發式已驗證 |
| `python -` scenario inventory／status inspection | **23** 項情境全部標示模擬；所有規則／plan status 是寫定資料。補充說明負面情境缺漏的輸出見 SIA-R1-F1 |

Issue 的 UTF-8 SHA-256 以派工提供的 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be` 對照 BD-3 #12 列相同。本次沒有重新取得或宣稱重新 hash 完整 GitHub body。

### pytest：初次錯誤與成功重跑分開記錄

1. 首次依派工直接執行 `python -m pytest -q`，結果 **`513 passed, 98 errors`，exit 1**。98 個 errors 出自 fixture setup：pytest 預設嘗試 `os.scandir` worktree 外的 `pytest-of-yotsu` 暫存目錄，被 sandbox 以 `PermissionError: [WinError 5]` 拒絕。沒有取得目錄內容；沒有後續探查或要求提高權限。這是本 reviewer 未先限制 pytest 暫存位置造成的存取嘗試，不能聲稱整次 session 完全沒有嘗試外部路徑；dispatcher 採用前須一併核對，見 NV-SIA-3。工具 host 等待輸出曾 timeout；後續取得同一 session 的最終失敗結果，未將 timeout 當作 PASS。
2. 將暫存與 synthetic test artifacts 限制到本 worktree 已存在、git-ignored 的 pytest cache，再完成兩個指定命令。沒有修改 tests 或追蹤中的 pytest 設定：

```powershell
$auditCache = Join-Path (Get-Location).Path '.pytest_cache'
$env:PYTEST_DEBUG_TEMPROOT = $auditCache
$env:TEMP = $auditCache
$env:TMP = $auditCache
python -m pytest -q
# 611 passed in 18.40s；exit 0
python -m pytest -q -rxX
# 611 passed in 17.52s；exit 0
```

611＝BASE 的 556＋初始 UI-0 的 47＋correction 的 8。第一次暫存錯誤不是 Skeleton assertion failure；成功重跑支持 E-1，不掩蓋原錯誤。測試通過也沒有補足 SIA-R1-F1 未被測試的 Spec 情境。

### 獨立 AppTest 與固定文字核對

以 PowerShell UTF-8 here-string 傳入 `python -`，只在記憶體執行 `streamlit.testing.v1.AppTest`，不建立 script 檔；TEMP／TMP 同樣限制在本 cache。操作結果全部 assertions 通過、exit 0：

- s08 規劃後切 Snapshot Mode：舊 `plan_inputs`／outcome 保留、顯示過期；再次規劃才採用新 mode 並消除過期。沒有把目前 checkbox 狀態冒充舊結果的資料模式。
- s06b 同輪回覆單向＋「不安排這段休息」：騎士指定休息不再出現、Profile 預設休息保留、沒有第二輪。與 `619268a`、新增 regression cases 及 K12 記錄一致。
- 從完成計畫切到七則路線錯誤及評估失敗，逐一按規劃：沒有 result tabs、只有 Profile 的三個 metrics、有錯誤訊息、沒有 app exception；未殘留先前的出發時間／路線計畫。

三組輸出分別以 `snapshot: ... OK`、`clarify one-way explicit cancellation ... OK`、`transition ... all 7 route errors and evaluation failure: OK` 確認。AppTest 的 bare-mode `missing ScriptRunContext` warning 已觀察到，沒有 app exception。這些是程序內畫面測試，不是 browser／375 px／實體鍵盤證據。

**UI0-3／E-4：** 本次逐項人工對照 supplied Issue 的固定文字與 `ui0_texts.py`：Profile 三種說明與 U-7、描述與 guard、三種休息追問題與選項、追問後無法對應、期限／錨點、兩種路權、去回差、三種涵蓋比例、六碼七則路線錯誤與對應做法、評估失敗、人工確認附句、天氣／抵達／預設餘裕與休息策略，未見逐字差異。保留 Issue 佔位，`fill()` 只代入合成值。UNKNOWN 的原因分類與人工指引另對照 SPEC-001 §5.1／§5.3，對應一致。已有 AppTest 的 equality assertions 驗證渲染端使用這些值。Executor E-4 記載 72 個固定字串的雙向比對方法與例外；原 scratchpad 不在本 worktree，本次未重跑該腳本，也不把以 implementation 常數作 expected 的測試當成獨立逐字 oracle。

## 治理 §4.7：五個範圍的明確結論

### 1. 跨 Ticket invariants

**PASS（適用部分）。** 本 Spec 只有 #12，沒有另一張 implementation Ticket 的跨票資料鏈；不因此省略 invariant 核對，也不要求與 BATCH-1 接線。四個 app 模組共享固定文字與 literal scenarios，依賴方向未進入 `src/`；上傳不讀內容、情境不計算 Validator 狀態、頁首／來源／結果標示模擬。Profile 更新及欄位修改不自動規劃、舊結果過期；Snapshot 顯示以產生結果時的 inputs 為準。Full tests 與獨立 AppTest 支持上述相互作用。負面補充說明情境的 Spec coverage 問題另為 SIA-R1-F1，不能由單票結案推定不存在。

### 2. Spec-level AC coverage，含分配的 AB

| derivation §6 的 Spec-level AC | 判斷與 evidence |
| --- | --- |
| #12 依 orch-default §7 結案 | **PASS（既有 Ticket closure 可追溯）**。run record:215 起 §8.1 的 P1～P9；無 dependencies，OC→Spec→Ticket 引用有效；events #46／#51 有兩輪 Ticket binding 與自寫 records；R1-F1／F2 由 R2 RESOLVED；R2-N1 在 worklog:373 更正；C-1～3、UI0-7、Q-1／Q-1b 均有 DA disposition；worklog §11 反映 closure／follow-ups；審後 delta 全為 record-only。本次新發現的 Spec coverage 缺陷交同票 rework，不改寫既有 Ticket verdict |
| UI0-1～UI0-10 有充分對應 evidence | **FAIL（未完整涵蓋）**。逐項如下；UI0-8 有 SIA-R1-F1，其餘已列 evidence 不能代替缺漏情境 |
| §7 的 AB 分配有對應 evidence | **未全部滿足**。AB-8 Skeleton 部分受 SIA-R1-F1 影響；AB-10 有證據；AB-13 的 pytest 通過、SIA 本次 BLOCKING、phase acceptance 尚待 SIA closure，詳下表 |
| 沒有修改 G3 Frozen Baseline 與 docs/ui | **PASS**。指定 diff 為空，另對 accepted sources 的 quiet diff exit 0 |

| Ticket AC | 本次 Spec-level 核對 |
| --- | --- |
| UI0-1 | 六區與 Issue 最低 14 類情境都有程式及操作 evidence：1→s01、2→s02、3→s03、4→s04a/b、5→s05、6→s06a/b、7→s07、8→s08、9→s09、10→s10、11→s11a～g、12→s12、13→s13、14→s14，另 s15；共 23 個選項。最低清單部分 PASS；Spec 額外明列情境的完整性仍受 F1 影響 |
| UI0-2 | **PASS（有已記錄限制）**。1.67.0 元件實際 render；worklog §7 列原生 dataframe CSV、表格上色替代、期限 key、tabs、上傳 metadata／spool 與日曆限制。沒有加入 framework |
| UI0-3 | **PASS**。上述逐字對照、worklog E-4 方法與渲染 evidence；提案文字仍留給 UI Delta Review，不因本次結果變成正式產品接受 |
| UI0-4 | **PASS**。一輪、同輪型態／方向、單向免答方向、取消只取消該筆需求，源碼、55 個 UI 測試中的相關 cases、獨立 AppTest 與 K12 相符。C-1 的未定地點／方向組合依 DA 對 #12 無新增要求；不提前實作正式整合語義 |
| UI0-5 | **PASS**。穩定 key 的 time_input 標籤隨型態切換；test:376 與 E-2 第 11 列記錄 16:45 保留。未選型態用「期限」已記錄供 review |
| UI0-6 | **PASS（評估既有 browser evidence）**。worklog E-2 的 375×812、doc/main 375、未裁切溢出 0，涵蓋情境、兩分頁與 expander 展開；CL-UI0-4 容許逐步紀錄，未要求必有截圖。本次沒有重新量測 |
| UI0-7 | **PASS（限 DA 界定的頁面操作範圍，評估既有 evidence）**。K1～K12 與原 Tab／分頁記錄相互支持；不將 K4 注入當鍵盤、不把 K3-B 或 K9 彈窗記為已驗證。詳下節 |
| UI0-8 | **FAIL／SIA-R1-F1**。worklog §7 列了 CR-P/B/R/C/D 與整合後驗收，但 CR-C3 對「補充說明不顯示」的合成呈現無 evidence，且 §11.3 明列的該情境未交付。後端真假判定仍屬整合後驗收 |
| UI0-9 | **PASS（合成資料範圍）**。MOCK_DATE、示範名稱、synthetic 路徑、空檔／無軌跡 GPX 標頭與模擬來源可追溯；tracked 私有路徑 0。沒有用真實行程反查，因此不宣稱真實資料正確性已驗證 |
| UI0-10 | **紀錄存在，完整性待 F1 修正**。worklog §6～7、§9.2、§10～11 有結果、替代、限制、修正與 owner；F1 的缺漏須反映到該紀錄，不能沿用完整 PASS |

| 分配的 AB 部分 | 結論與邊界 |
| --- | --- |
| AB-8：Skeleton 與供 UI Delta Review 的紀錄 | **FAIL／F1**：六區、最低情境與紀錄已具備，但 Spec 指定的負面補充說明呈現不全。acceptor 的 UI Delta Review 及正式整合本來就是另一部分，不以它們尚未完成作本次 blocking |
| AB-10：NFR5 模擬標示、U-7 隱私文字 | **PASS**。23 個 labels、頁首、Profile／route／result 標示與來源列均可追溯；U-7 與 supplied Issue 一致；不宣稱檔案只留在使用者電腦 |
| AB-13：本 Spec 的 pytest、SIA closure、DA phase acceptance | **pytest PASS；SIA BLOCKING；phase acceptance 尚未完成**。本 record 不建立 P10。DA phase acceptance 必須在有效 SIA closure 後引用該 closure record；這個正常先後次序不是另一個 implementation finding。私有資料 gate 本次已核對 0，但不宣告整個 OC-1／release 的 AB-13 PASS |

**E-1～E-6 sufficiency：** E-1 本次兩個 full suites 成功；E-2 實際啟動／停止與 browser 操作有逐步紀錄，但 F1 沒有對應操作；E-3 有逐條表及元件限制，完整性受 F1 影響；E-4 如上；E-5 合成來源／diff／fixture／evidence 無私有資料跡象、沒有截圖可另查；E-6 的 H-2／H-3 self-verification 存在，本 reviewer 另作下節獨立核對。不能因所有 E 欄位存在便推定內容完整。

### 3. 整合行為

**既有已覆蓋路徑 PASS；完整 Spec 行為因 F1 未完成。** Profile→過期提示、表單→規劃／錯誤、同輪追問→選取合成 plan、路線確認→共用分頁、UNKNOWN→固定指引、無可行解→代表性失敗候選，均可由源碼、AppTest 及記錄互相支持。沒有真實資料或後端整合。錯誤分支不殘留先前 plan，Snapshot 舊結果模式未隨 checkbox 搶先改寫；取消休息的修正保留預設休息。模板後的補充說明只有成功顯示路徑，缺少 §11.3 要求的省略路徑，不能視為完整整合覆蓋。

### 4. 最終 subject 的 verification／audit coverage

**既有 verification 與 subject identity 可對應；整體 SIA closure 尚不成立。** Ticket R1 subject `e836c99`、R2 `ca91406`，最後 implementation `619268a`；至本次 HEAD 全為 record-only。Browser E-2 初始記錄搭配 correction subject 的 K1～K12；修正只更動回覆顯示與合成休息列，沒有更改版面／元件。Full pytest 在本次 HEAD 完成，原始 scenario／renderer／tests 也由本次 R1 閱讀，不僅沿用 Ticket R2。F1 是這次對完整 Spec 的新 coverage finding，沒有推翻或重開兩個已閉合的 Ticket findings。後續修正仍須識別 delta 並由 SIA R2 驗證。

### 5. Traceability 與 boundary 符合性

**引用鏈與 boundary PASS；分配部分的交付完整性受 F1 影響。** OC-1 §2.1(4)→derivation §1～3／§7→#12、BD-3 hash、worklog、Ticket audits、DA decisions 與 run closure 可追溯。沒有修改 frozen files、Should 擴張、付費呼叫、真實資料或正式後端整合；C-4 root Streamlit 設定是 runtime HOW，C-8 補充無可行解是已存在的 Must 呈現。Q-1／Q-1b 已由 DA 處置，不要求所有 engine 一律有 snapshot badge，也不新增示範路線選單。§5.5 中提案文字與正式產品接受分開。N1 的 fast-path 誤述需澄清，但本次 scope 沒有因此失去識別。沒有跨全部 derived Specs 重新分配或要求 OC-1 全面 closure。

## CL、browser evidence 與高風險核對

| Clarification | 本次結論 |
| --- | --- |
| CL-UI0-1 | **PASS**。程式在 app，匯入僅 Streamlit／標準函式庫／本地 UI 模組；`ui` extra 釘 1.67.0；不匯入 src |
| CL-UI0-2 | **PASS（依 DA clarification 的 app 範圍）**。`app/ui0_mock_app.py:83` callback 只取 `len(files)` 並顯示 literal 處理結果，不讀／解析／保存／log 內容；目標 GPX 只取文字。C-2 metadata、C-3 framework spool 依 DA §3.2／§4.2，不重開為 app 違規；動態 framework 生命週期 NOT VERIFIED |
| CL-UI0-3 | **PASS**。紀錄在指定 #12 worklog；docs/ui、prototype diff 為空 |
| CL-UI0-4 | 有可評估的實際 browser 逐步記錄；UI0-6／7 判斷如上。**本 reviewer 沒有瀏覽器，沒有親自重跑 375 px 或 keyboard-only**，不把 AppTest 當成替代 |
| CL-UI0-5 | **PASS**。literal plan／rule／candidate 狀態，`_pass/_fail/_unknown` 只包裝寫定資料；沒有由數值計算 status 或排序。表單 guard、必要回答與模擬回覆顯示不是 Validator。F1 的修正也應維持此限制 |

**UI0-7 的獨立 evidence sufficiency 判斷：** K1／K2 記 Tab 到情境、Enter 展 Profile 與無檔更新；K3 記鍵盤啟動 multi/gpx file-input 請求，listener 僅取消 OS 對話框；K4 明標程式注入；K5／K6 以鍵盤移除／更新並顯示結果、status、過期而不自動規劃；K7／K8 補足描述／路徑打字、guard、Snapshot 切換與規劃；K9 保留彈窗無法進入的觀察，Tab／Escape 可離開，K10 在相同 date_input 的一般 Tab 順序修改日期；K11 與 E-2 第 11 列支持時間／油量／型態與期限切換；K12 支持同輪追問與取消。原 E-2 第 18 列及保留的 Tab／分頁紀錄涵蓋公路 expander、分頁與全部候選。依 `decision-20261118-issue12-ui07.md` §3.1／§4.2，以操作為單位的範圍有充分證據；沒有靠「標準元件應該可以」推定未做的操作。K3-B 是範圍外 NOT VERIFIED，K9 是原因未定的元件／工具限制，均未被寫成 PASS；後續 UI Delta Review 不是用來豁免範圍內 gate 的 disposition。

**H-2（依高風險 record §5）：** tracked 禁止路徑 0；diff、fixture、worklog／K 紀錄的檔名、日期、時間及位置說明都能追溯到 literal mock、Issue 示範或空／標頭 bytes，未見真實軌跡／座標／私有路線。app 沒有第三方 request／prompt 或內容 log；Streamlit 設定關閉 telemetry、listen localhost。隱私裁切與錨點代換的真實資料驗證不屬 Skeleton，未標 PASS；需要私有資料者為 NOT VERIFIED、required authority=acceptor。

**H-3（同 §5）：** ETA_safe 未稱 P90／百分位；70% 以上稱自訂「高降雨機率提醒」並否定官方警特報與強度；不宣稱比 Google Maps 準確、啟發式折返已驗證或檔案只留在使用者電腦。路權／涵蓋比例保留限制，來源列標示模擬。沒有 app holdout 讀取路徑，沒有執行 E1 Lite／E2 或把 preview 寫成其結果。結果／gate 陳述依本次實際輸出與既有允許的 browser 紀錄逐項判斷；F1 正是不能由既有完整 PASS 陳述代替 evidence 的缺口。

**H-1／H-4 的最終分類：** 沒有憑證／付費，未新增 H-1；沒有規則結果、候選排序、真實路線採用或休息排程，未新增 H-4。模擬回覆列與 omission renderer 不應擴成真正的判定機制；若修法引入該類行為，必須 route DA 重新分類。

## 既有 tracked items、NOT VERIFIED 與後續 authority

| 項目 | 核對結果、disposition 與 owner／required authority |
| --- | --- |
| Ticket R1-F1／R1-F2、R2-N1 | 前兩者的 R2 closure 有 source／regression／browser record 支持；R2-N1 兩處 K9→K12 已更正（worklog:179、:275、:373）。不重開。Owner #12 Executor 維護修正證據 |
| C-1 | DA 對 #12 無新增要求；之後 app 整合須遵守 `decision-20261118-issue12-ui0.md` §2.4 的同輪方向／未能安排時處理。Owner／required authority=後續整合 Spec 的 DA |
| C-2／C-3 | DA 釐清 app 與框架邊界；§3.3 的合成上傳 evidence／真實檔名限制、§4.4 的保存期間、位置、刪除與 spool 說明留後續整合。Owner／required authority=整合 Spec DA；私有資料或改變部署 boundary 時 required authority=acceptor |
| C-4／C-8 | 有效 HOW／範圍內，無待辦；worklog:414、:416 指 #12 Executor 維護紀錄。不是新的工作授權 |
| C-5～C-7 | 非固定文字、模擬結果不隨全部表單重算、原生 dataframe CSV，worklog:415 有 owner=acceptor 的 UI Delta Review；tracked，不代表產品接受 |
| Q-1／Q-1b | `decision-20261118-issue12-q1.md` 已處置；Q-1 不需 correction。Q-1b 的示範路線來源三值與正式介面如何呈現歸後續 app Spec DA；若恢復騎士選示範路線，required authority=acceptor（CR-B1 contract change）。沒有新增 #12 要求 |
| NV-SIA-1：browser 親自重跑／UI Delta Review | **NOT VERIFIED**：本 reviewer 無瀏覽器，沒有親自重跑 UI0-6／7；本次只評估記錄。原 NV-1／NV-R2-1 已帶 owner，required authority=**acceptor**，依 CL-UI0-4 進行 UI Delta Review，亦為 AB-8 的另一部分，不能用本 SIA 取代 |
| NV-SIA-2：原始 browser／framework evidence | **NOT VERIFIED**：本 worktree 沒有原始 transcript、截圖、scratchpad 或原始啟動 log；沒有到外部取得。CL-UI0-4 允許的逐步記錄仍可評估。需補原始 evidence 時 owner=**#12 Executor**；framework spool／刪除生命週期未動態驗證，保存契約 required authority=**DA**；涉及真實 GPX 的驗證 required authority=**acceptor** |
| K3-B／K9 | **NOT VERIFIED／資訊**：OS 原生選檔的 keyboard multi-select 沒有驗證；日曆彈窗問題原因未確定。worklog:411、:417～418 與 run record:229 有 owner=acceptor UI Delta Review；正式逐元件要求交整合 Spec DA。依有效裁決不擋既有 UI0-7，不宣稱已驗證 |
| NV-SIA-3：本次 assignment binding／存取／原樣 record | **NOT VERIFIED（由 dispatcher 完成）**：本次 SIA 的 event／實際 model／全程 effort 等證據尚未記入受審 run record。required authority=**dispatcher／Orchestrator**：採用前補本次 dispatch event、thread、全部 turn_context 集合、存取核對（含首次 pytest 被拒的外部暫存嘗試）、唯一新增檔、寫入作者與 SHA-256。不是可被 verdict 免除的 formal-assurance 要求，不由本 reviewer 虛構或替補事件編號 |
| 既有 NV-3／NV-R2-3 | 兩次 Ticket assignment 的 dispatcher 後續核對已見 run record events #46／#51，record 更新引用 worklog:374、:412；不能挪用作本次 SIA binding |
| NV-SIA-4：真實資料、正式 API／保存／後端 | **NOT VERIFIED／NOT RUN**：本票排除，無私有資料授權。承接原 NV-4／NV-R2-4（worklog:413）。required authority=**acceptor**（RB-7 資料授權與實際驗證）；保存／整合語義 owner=**DA**。沒有讀取 holdout 或以 mock 冒稱真實實驗完成 |
| AB-13／P10 下一步 | SIA-R1-F1 → #12 Executor targeted correction → SIA R2；有效 closure 後才由 **DA** 作 phase acceptance 並引用 closure record。SIA-R1-N1 留有 owner，不延長 cycle。不是 release、正式整合或 OC-1 全部完成的授權 |

本次只有 SIA-R1-F1 為 blocking；這是最終 Spec subject 的新 coverage finding。#12 的既有 Ticket R2 PASS、兩個已閉合 findings 與 UI0-7 DA 裁決維持原紀錄；本次不代行 acceptor 或 DA 的保留動作。唯一新交付檔為本 record；未 stage、commit 或修改其他追蹤檔。

寫入後核對：git status --short 僅有本 audit record 新增；git diff --exit-code 與 git diff --check 都為 exit 0。以 Get-Content 確認末行 verdict，並計算 Get-FileHash -Algorithm SHA256 供 dispatcher 核對。

Verdict: BLOCKING
