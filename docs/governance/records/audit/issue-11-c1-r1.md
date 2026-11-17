# Issue #11 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37a`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`，含 §5 #11 補充條件、CL-B1-1、5、7 及後續適用 clarifications）→ Issue #11「B1-4 pace ETA」 |
| Issue 版本 | 使用本次 dispatch pack 所附完整原文；其宣告的 UTF-8 SHA-256 `3f4b1caecfcc81bb152ea217ec376857c0e6f6dab9c207148412d96da026f8e4` 與 first-run derivation record §3 BD-3 第 #11 列相同。沒有連線取得 Issue |
| Subject | 本專用 worktree 的 detached HEAD `bf8a8e3d9dd51179253d5f24044bcfce39498a53`；BASE `eb1852d262e6b3434364e3e08b6602aa7d24d733` |
| Implementation | `41c848bc03c963599cf936c2e578e50045e4a68f`；之後 `23decdd`、`bf8a8e3` 都只改 `docs/governance/records/**` |
| Audit kind | **Ticket independent audit，R1，cycle 1；不是 Spec Integration Audit** |
| Role／作者 | `primary_reviewer`，Codex；本 record 由 Reviewer 自行撰寫 |
| 日期 | 2026-11-18 |
| Governing bindings | Project Bindings m3（O-6 qualification 已完成，§8.2 #7）；Minimal Operational Governance v2.2；impl-default v2；orch-default v2.2 |

## Assurance

| 面向 | 滿足方式與證據 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread，未繼承 Executor 的對話或推理。只把正式 worklog、run record 的完成與測試敘述視為待驗證主張；實作、測試與公式皆自行閱讀及核對 |
| Verifiable binding | 本次 dispatch 的持久引用是 `docs/governance/records/run/run-20261117-oc1-run2.md:111`，§6 **事件 31**（#11 R1，Codex `gpt-6.1-sol`／`high`，不兼作 SIA）。依 Bindings §3.3，由 dispatcher 在該事件補記本 thread 的 rollout、全部 `turn_context` 的 `(model, effort, sandbox)` 核對、存取紀錄及 record hash。受審 HEAD 的該欄仍為「進行中」；本 Reviewer 不讀取 worktree 外的 rollout，也不虛稱已完成 dispatcher 的事後核對。採用本 record 前須由 dispatcher 完成此項機制 |
| Autonomous access | 在本 worktree 內自主讀取 accepted contract、原始程式、測試、git diff／歷史並執行檢查；pack 是入口，未以 Executor 的摘要限制 coverage。沒有查詢 GitHub、網路服務、私有資料或執行 `experiments/` |
| Self-written record | 唯一新增的交付檔是本 audit record；沒有修改 implementation、tests、contract、gate，沒有 stage／commit。本次寫入事件及完成後的 `git status` 可供 dispatcher 核對作者與唯一檔案，依 Bindings §3.3 原樣接收 |
| 實際模型證據與 model diversity | Executor：run record `:110`，§6 **事件 30**，agent `ad6a4bc20b0a498ea`，dispatcher 觀測全部 87 則為 (`claude-opus-5-5`, `high`)。Primary：本作者是 **Codex**；本次記錄的派工 mapping 是 `gpt-6.1-sol`／`high`（事件 31），實際 runtime 的全程核對由 dispatcher 補記。Bindings §5 不宣告 D1–D4；**no model diversity claim**，不以模型名稱的不同證明 independence |

## 範圍與原始材料

已閱讀 root `CLAUDE.md`、Project Bindings 與 `.claude/agents/gov-primary-reviewer.md`，並依其指示核對治理本文 §2.3、§3.8、§4.1–4.7、impl-default §6–7、orch-default §6–7。最後一行的 verdict 字面格式依本次 dispatch 的明確要求。

契約閱讀涵蓋 OC-1 的 scope、constraints、AB-4／10／13 與授權；SPEC-B1 的來源、CL-B1-1／5／7、§5 #11 及 E-1–E-5；`decision-20261117-oc1-first-run-derivation.md` 的 BD-3／5；`decision-20261117-issue7-spike-tests.md` 的 S-4–S-6 與 §3.2；`decision-20261117-issue9-e1-and-trim.md` 的 CL-B1-9 第 3 項；`decision-20261118-issue10-pace-contract.md` 的 CL-B1-12–14 與對 #11 的影響；高風險類別 record §3.3、§3.4、§5。

Spec 原文核對涵蓋 `DESIGN.md` §5 共通規則、契約 3／4 與 §6.1，`SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §1.1–1.2、SB2-T5／6／8／9，以及 `SPEC-001-plan-schema.md` §5.4 的安全餘裕係數與停等寬放兩列、`BATCH-1-scoped-tickets.md` 的共通規則、依賴與 B1-4。未把未 Freeze 的 SPEC-001 全文視為本票契約。

實作與證據閱讀包括 `src/moto_copilot/pace/table.py`、`contracts/schemas.py`、`contracts/validate.py` 的相關路徑、`tests/test_eta.py` 全文、`tests/test_routes_pace_eta.py`、`test_pace_table.py` 的合成產生器、相關 `test_contracts.py` 測試名稱、`tests/conftest.py`、`pyproject.toml`、mock fixture、#11 worklog 與本 run record。透過 `Get-Content -Encoding UTF8`、有明確檔案範圍的 `rg -n`、Python `Path.read_text`／行號擷取及下列 git 指令閱讀；初次 PowerShell 解碼不正確的文件已以 UTF-8 重讀。

## 實際執行的檢查

以下全部針對本 worktree 的指定 HEAD；沒有使用 `.venv`。Python 使用 PATH 上的 `python`。pytest 的合成暫存資料固定在本 worktree 的 `.pytest_cache/`，沒有改動 `pyproject.toml` 或 `conftest.py`。

| 指令／檢查 | 實際結果 |
| --- | --- |
| `git rev-parse HEAD`；`git rev-parse eb1852d` | 分別等於上列完整 HEAD、BASE SHA |
| `git log --oneline eb1852d..bf8a8e3`；`git log --format='%h %s' --name-only eb1852d..bf8a8e3` | 只有 `41c848b` 修改產品與測試；另兩個 commit 只改 run record／worklog |
| `git diff --stat eb1852d..bf8a8e3`；`git diff --numstat eb1852d..bf8a8e3` | 共 5 檔，521 additions、22 deletions。產品 1 檔、新增測試 1 檔、既有測試 1 檔、records 2 檔 |
| `git diff eb1852d..bf8a8e3 -- src/moto_copilot/pace/table.py tests/test_eta.py tests/test_routes_pace_eta.py`；兩個 records 的 diff／全文 | 完整核對實作 delta、33 個新增測試、S-4–S-6 六行 decorator 刪除，以及 worklog／dispatch 陳述；沒有其他實作變更 |
| `git diff --check eb1852d..bf8a8e3` | 無輸出，exit 0 |
| Python／`subprocess.check_output(['git','diff','--name-only','41c848b..bf8a8e3'])` | 斷言所有路徑皆以 `docs/governance/records/` 起頭成功，共 2 路徑；implementation 與 HEAD 的產品／測試內容相同 |
| `rg -n -i 'xfail\|skip' tests/` | 無命中，exit 1；沒有 xfail／skip 標記或相關字樣（表格中的反斜線僅為 Markdown 的 pipe escape，實際正規式使用 alternation） |
| `rg -n -i 'xfail\|skip\|data[/\\]\|\.env\|https?://\|subprocess\|socket' tests/` | 只命中合成 GPX XML 的標準 namespace 字串；不是網路呼叫。測試設定只收集 `tests/`；pipe 同上使用 Markdown escape |
| `New-Item -ItemType Directory -Path .pytest_cache -Force` | 建立 worktree 內 pytest cache，供 basetemp 使用 |
| `$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/r1-tmp-q'; python -m pytest -q` | **462 passed in 1.85s**，exit 0；完整輸出如下 |
| `$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/r1-tmp-rx'; python -m pytest -q -rxX` | **462 passed in 1.82s**，exit 0；沒有 XFAIL／XPASS／skip，完整輸出如下 |
| Python AST 比較（`git show eb1852d:tests/test_routes_pace_eta.py` 對磁碟檔） | 對 S-4、S-5、S-6，只移除 BASE AST 的 decorator 後，三個 function AST 各自完全相同；HEAD 沒有 decorator。原準備步驟與斷言完整保留 |
| `$env:PYTHONPATH='src;tests'; @'…'@ \| python -X utf8 -`：獨立 Decimal／公式核對，詳見下段 | **32 cases、128 segment rows PASS**；各 C1／C2／C3 單獨缺配速 **3 cases PASS**；mock `validate_dataset` 四項違反清單均為空；exit 0 |
| `git status --short --untracked-files=no`（開始）；`git status --short --untracked-files=all`（寫 record 前） | 均無輸出；寫入後另核對只有本 record 新增 |
| 寫入後 `git status --short --untracked-files=all`；`git diff --exit-code`；Python 檢查 record 最後一行並計算 SHA-256 | status 只有 `?? docs/governance/records/audit/issue-11-c1-r1.md`；tracked diff 為空，exit 0；最後一行檢查成功。hash 由工具輸出供 dispatcher 核對，不把 self-hash 寫入本檔 |

測試環境的前置失敗也保留於此，不算成功證據：最初未指定 basetemp 的 `python -m pytest -q` 在 tmp_path setup 階段輸出 `E` 後工具提前返回，本次未保留其 completion／exit code；隨後指定 `.pytest_cache/r1-tmp` 的 `python -m pytest -q -rxX`，因父目錄尚未存在而得到 `FileNotFoundError [WinError 3]`、`365 passed, 97 errors in 3.04s`，exit 1。建立允許的 cache 父目錄後，以上兩個必要命令均完整通過；沒有以放寬、跳過或修改測試處理錯誤。

`python -m pytest -q` 的完整成功輸出：

```text
........................................................................ [ 15%]
........................................................................ [ 31%]
........................................................................ [ 46%]
........................................................................ [ 62%]
........................................................................ [ 77%]
........................................................................ [ 93%]
..............................                                           [100%]
462 passed in 1.85s
```

`python -m pytest -q -rxX` 的完整成功輸出：

```text
........................................................................ [ 15%]
........................................................................ [ 31%]
........................................................................ [ 46%]
........................................................................ [ 62%]
........................................................................ [ 77%]
........................................................................ [ 93%]
..............................                                           [100%]
462 passed in 1.82s
```

獨立公式檢查沒有寫入測試檔：在記憶體內使用既有合成 `catalog()`／`pace_table()`，速度改成 27.3／45.7／62.1 km/h，停等比例取全零或 0.1333333333／0.7／1.3，係數取 0.05／0.15／0.20／0.75，交叉四種 `BREAK_SETS`，共 32 組；將輸入路段反序，另確認排序。以 Decimal 計算 `length * 3.6 / speed` 與回傳典型移動秒數比對（誤差 ≤0.000501 秒），逐列獨立累加回傳移動時間與寬放；檢查 stop_ratio 乘積誤差 ≤0.000501 秒、累計 ETA／逐段差／margin 誤差 ≤1 秒，並呼叫 `validate_eta_output`。另外逐一把 C1、C2、C3 設為合法的配速不足類別（speed／ratio 均 null、n_segments=1），確認整份 ETA unknown 且四個時間欄位全部 null。最後對既有 mock fixture 執行 `validate_dataset`，結果為：

```text
independent Decimal/formula checks: 32 cases, 128 segment rows PASS
each route category without pace: 3 cases PASS
mock validate_dataset: {'derived_segments': [], 'route_catalog': [], 'pace_table': [], 'eta_output': []}
```

## Acceptance 與 invariants 逐項判定

以下程式行號對應受審 HEAD；測試均包含在本 Reviewer 的 462 passed 內。

| 條款 | 判定與證據 |
| --- | --- |
| Issue AC 1／SB2-T5 | **PASS**。`table.py:399–404` 以同類別 speed 算典型移動時間、ratio 算寬放、ride 累加兩者；到達時間加累計休息，margin 只乘 ride。`test_eta.py:102` 人工算出的四段時間、`:120` 四組 invariant 測試，以及本次獨立 32 組公式核對均通過。三位小數的欄位捨入與整秒 ISO 輸出在允許的 1 秒內 |
| Issue AC 2／SB2-T6 | **PASS**。`test_eta.py:143` 比較無休息與三組休息：移動／寬放相同，margin 秒數相同，典型與保守時間只增加累計休息；涵蓋 fuel_station 與 waypoint。`table.py:400–404` 不將 breaks 納入寬放或 margin |
| Issue AC 3／SB2-T8 | **PASS**。`table.py:385` 收集路線所用缺配速類別；`:395–397` 先將四欄全部設 null，unknown 不進計算。`test_eta.py:158` 含有無休息、`:170` 含未用到的缺配速類別；S-5 與本次 C1／C2／C3 缺配速三例通過。保留完整 n 列與 break_time_s，沒有部分時間或補值 |
| Issue AC 4／SB2-T9 ETA 部分 | **PASS**。`table.py:377`、`:391` 取並記錄同一配速表 header 的係數；`:404` 計算也用該值。`test_eta.py:181` 涵蓋 loo_rule／default／unknown；`:271` 使用 #10 `build_pace_table` 的九趟合成輸出，係數與版本可追溯、契約 4 通過 |
| SPEC-B1 §5 #11 追加條件 | **PASS**。`table.py:378–380` 不同 caller margin 明確 ValueError，不採用。`test_eta.py:191` 六種值（含微小不同、字串、NaN、bool）、`:196` 不得強行改回預設 0.20 均通過；相同值的允許路徑亦有測試 |
| CL-B1-5 同表 stop_ratio／margin | **PASS**。`:383–384` 的 speed、ratio 和 `:377` 的係數來自同一份已驗證配速表；無預設 ratio／margin 後門。不同 category_scheme 的 RI-1–RI-3 沒有被宣稱已處理，`:370–371` 明列排除 |
| 契約 4 不變條件 1、5–9 | **PASS（本票適用行為）**。`:338–348` 拒絕缺段／重段／不合法類別；正常與 unknown 都逐段輸出。輸入皆為正長度、合法配速時，ride 非遞減、safe 不早於 typ。S-4–S-6、四組契約驗證與獨立公式檢查覆蓋完整列數、unknown、時間關係與係數來源 |
| 契約 4 既有休息關聯（2–4） | **本次無回歸**。仍使用既有 `expected_break_times`，沒有更動排入或檢查點對應方法。新增測試在合法內部檢查點排休息，進入該檢查點之前的列不受影響，之後逐列累加；既有契約測試亦通過。不據此宣稱本票完成休息排入功能 |
| CL-B1-8 §3.2 S-4／S-5／S-6 恢復 | **PASS**。`test_routes_pace_eta.py:163`、`:175`、`:182` 不帶標記通過；對 BASE 的 diff 僅刪除三個兩行 decorator，AST 核對內文未改。worklog §4 D-11-6、§6 E-4 明寫保留為獨立測試，未讓檢查消失 |
| CL-B1-9 第 3 項，#11 字面全數通過 | **PASS**。兩次完整成功結果均只有 462 passed，沒有 failed／error／xfailed／xpassed／skipped；`tests/` 無任何 xfail／skip 字樣 |
| CL-B1-1、Issue 共通限制 | **本次可查證範圍符合**。變更僅一個 pace 實作與合成測試；沒有修改契約、凍結基線、Issue、私有資料、experiment 程式。測試修改理由已列 worklog。Executor 的歷史存取行為需 dispatcher 的原始 transcript 核對，本 Reviewer 不將其自述等同存取證據 |
| CL-B1-7 用語 | **PASS**。新增說明是 conservative estimate、無 coverage guarantee；沒有將 ETA 稱為百分位數，也沒有將高降雨機率稱為官方警特報。`table.py:7` 的既有「not a P90」否定陳述未被本票修改；不是新增宣稱 |

## E-1–E-5 與高風險核對

| 要求 | 判定 |
| --- | --- |
| E-1 | **滿足**。worklog §6 保存 `41c848b` 上 `.venv/Scripts/python.exe -m pytest -q`／`-rxX` 的完整 462 passed 輸出；implementation 到 HEAD 只有 records delta。本 Reviewer 依派工改用 PATH Python 獨立重跑，兩次均 462 passed；沒有把未執行的 `.venv` 命令寫成 Reviewer 實測 |
| E-2 | **滿足**。worklog §6 表逐條列出四項 AC、caller margin 追加條件、同表 ratio 與 H-4，測試名稱可在原始測試找到且均實際通過。對照內容與測試斷言一致 |
| E-3 | **滿足本票檔案檢查**。`test_eta.py:1–6`、`:24–66` 使用手寫速度、長度、停等比例與 (0, 0) 附近佔位座標；`:271` 依 `test_pace_table.py:37–47` 的虛構 T101–T109 產生器建表。fixture 的來源由 `conftest.py:1` 明列 mock。本票 diff 沒有真實軌跡、真實騎乘時間或行程清單，也沒有憑證或外送請求 |
| E-4 | **滿足**。既有測試只刪 S-4–S-6 標記，worklog §6 E-4 逐一寫明恢復方式與依據；原斷言 AST 不變，沒有 fixture、全域設定或其他既有測試變更 |
| E-5 | **滿足**。worklog §6 E-5 分別記錄 H-3／H-4 的 self-verification，與 independent audit 分開；本 Reviewer 的最低範圍核對見下 |

**H-3（高風險 record §5）。** 新增程式、測試與兩個 records 的結果／狀態陳述已對照實際產物和本次測試：原 worklog 的 462 passed 數目可重現；S-4–S-6 已真正恢復；沒有把測試寫成 E1 Lite／E2 結果。`compute_eta` 是記憶體內計算，沒有新增任何 GPX／保留行程的開啟路徑。diff 新增的 ETA 說明符合用語限制。Executor 額外 mutation 的原始 scratchpad 不在本 worktree，其數字未作為本 Reviewer 的通過依據（見 NOT VERIFIED）。

**H-4（高風險 record §5）。** `table.py:374–376` 先驗契約 3，不以預設值補缺。`test_eta.py:240` 八種損壞表涵蓋缺／null／NaN margin、有 speed 而 null ratio、缺／負／無限 ratio、缺類別；全部明確錯誤。`:191` 的 caller 衝突、`:248` 的缺段／重段／錯誤類別、`:263` 無時區出發時間均為錯誤。合法「配速不足」則整份 unknown，四欄 null，連帶未使用類別的區別也有測試。非有限或缺漏未被靜默變成 0、0.20 或 ok。函式沒有新增外部 API／逾時／快取路徑；Planner 改寫、計畫狀態、規則 5 與路線採用不是本票變更，這些最低項目在本票不適用，沒有宣稱通過它們。

**C-11-1 的範圍判斷。** 配速表驗證與路段完整性檢查皆在同一 ETA 函式的輸入防線內，分別維持缺值不補值及契約 4 不變條件 1。沒有更動資料契約、排休息的設計或路線分類語義；屬本票實作 HOW，未發現需要另作設計裁決的範圍爭議。

## Findings

沒有 blocking finding；沒有 non-blocking finding。因而沒有待修 finding ID、severity、required fix 或需指定 disposition／owner 的 finding。上列測試環境前置失敗已排除且完整重跑成功，不是 implementation finding。

## NOT VERIFIED 與明確排除

| 項目 | 原因與 required authority／owner |
| --- | --- |
| 真實騎乘資料建立的配速表／ETA、真實資料回歸、保留行程隔離的實際資料驗證 | **NOT VERIFIED／NOT RUN**；沒有私有資料授權，未嘗試取得。required authority = **acceptor**（RB-7）。這些不是 Issue #11 的合成資料 AC |
| Executor mutation 原始輸出與完整歷史存取紀錄 | **NOT VERIFIED**；其原始材料在本 worktree 外，禁止存取。required authority／核對 owner = **Orchestrator dispatcher**；如需私有資料才另 route acceptor。未將 mutation 數字或 Executor 的存取自述當成通過證據 |
| 本次 Primary 的全程 runtime binding／存取紀錄與 record hash | 受審 run record 事件 31 尚待完成後補記；required authority／核對 owner = **dispatcher**（Bindings §3.3）。本 Reviewer 沒有讀取外部 rollout。此為採用原始 record 前的派工機制核對，不是要求修改產品 |
| 路線與配速表 category_scheme 不同的 RI-1–RI-3 | **排除範圍，未驗證其處理**；CL-B1-5 明列交之後 `routes` Spec，owner = Design Authority。不能由本票 PASS 推論已整合 |
| SB1-AC2 完整 ingest → pace → ETA 與其他 Spec 層級 AC | **本次不是 SIA**。本票只驗證 pace table → ETA 的合成連接；完整整合由另派 SPEC-B1 SIA 檢查，owner = Orchestrator／SIA Reviewer |
| DESIGN／README 的實作狀態文字同步 | 屬既有 C-11-4／AB-12 文件工作，本票沒有更改；不因文字仍稱未實作而否定本次已直接檢查的實作，也不宣告 AB-12 完成 |

本 verdict 僅表示指定 subject 上 Issue #11 的 R1 沒有 blocking finding；不代替 dispatcher 的 binding 核對、Ticket completion check、SPEC-B1 SIA、DA phase acceptance 或 release authorization。

Verdict: PASS
