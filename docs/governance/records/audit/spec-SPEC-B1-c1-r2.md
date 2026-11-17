# SPEC-B1 — Spec Integration Audit，cycle 1 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`；acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md` §2、§4–§7，含適用 CL-B1-8～15 與 #9 FA ruling）→ Issues #7、#8、#9、#10、#11 |
| Subject BASE | `ff049661f968adace4dd017cf560316e5684440d` |
| Subject HEAD | `a74e683bdcc513a41ab6c7e27411a4633b4c2db9`；本 dedicated worktree 的 detached HEAD |
| R1 subject／修正 | R1：`a6f78f8f112c9a2af310452c21903c1683371b97`；修正：`98e5a1a78aa489f76632b62cadb47439c6a3b732` |
| Audit kind | **Spec Integration Audit of SPEC-B1, R2 closure review, cycle 1 (not a Ticket audit)** |
| Role／作者 | `primary_reviewer`，Codex；本 record 由 Reviewer 自行撰寫 |
| Dispatch | `docs/governance/records/run/run-20261117-oc1-run2.md:119`，§6 **事件 40**；修正派工與 Executor binding 見事件 39 |
| 日期 | 2026-11-18 |
| 結論 | **SIA-R1-F1：RESOLVED**；沒有未解 blocking finding，沒有新增 finding；SB1-AC1～SB1-AC6 均 PASS，限本 Spec 已分配範圍 |

## Assurance：independence 與 models

| (a) 四項 independence properties | (b) 實際 models 與 binding evidence |
| --- | --- |
| **Independent context**：本次為 fresh Codex thread，沒有繼承 Executor、R1 Reviewer 或 Ticket Reviewer 的對話與推理。從磁碟重新閱讀 SIA R1 record、修正後測試、契約與 diff，獨立判定 closure；worklog 的完成與 mutation 敘述均視為待核對主張。沒有派 subagent。 | 本次 correction Executor：run2 §6 **事件 39** 記載續派 #11 同一 `gov-executor`（agentId `ad6a4bc20b0a498ea`），全部 assistant 訊息觀測為 (`claude-opus-5-5`, `high`)，128 則、符合。這是 dispatcher evidence，不以 worklog §10.5 的自我觀測取代。 |
| **Verifiable binding**：依 Bindings m3 O-6／§3.3 的資格與派工機制；qualification 通過紀錄見 Bindings §8.2 #7。當次 binding 的持久承載位置是 run2 §6 **事件 40**。HEAD 上該欄仍為「進行中」；dispatcher 在採用本 record 前須核對全程 rollout 的 model／effort／sandbox、存取、作者事件與原樣回傳 hash，並回填。 | Primary：本作者為 **Codex**；事件 40 指定 mapping 為 `gpt-6.1-sol`／`high`，sandbox 應為 `workspace-write`。本 worktree 尚無當次全程 runtime 核對結果，精確實際 model／effort 須由 dispatcher 依 rollout 確認；不將指定 mapping 冒充已觀測的 binding。 |
| **Autonomous access**：自主讀取本 worktree 的原始契約、程式、測試、git 歷史與正式 records，使用 PATH Python 自行執行檢查；pack 作為入口。pytest 的 basetemp 限於 worktree 內 `.pytest_cache/`，沒有讀取外部 repo、rollout、私有資料或憑證，沒有網路呼叫。 | 既有 implementation models 沿用 R1 record 的 assurance 引用：#7 見前一 run §5 事件 2、8；#9、#10、#11、#8 見 run2 §6 事件 18、28、32、36，均記錄 `claude-opus-5-5`／`high`。本 R2 沒有重新派工或重查外部 transcripts。 |
| **Self-written record**：唯一新增交付檔為本檔。未修改 implementation、tests、fixture、契約、gates、既有 records；未 stage／commit。dispatcher 依 Bindings §3.3 原樣接收並核對 SHA-256，不代寫或改寫 verdict。 | **no model diversity claim**。Bindings §5 的 D1～D4 未宣告；不以模型名稱或預定 mapping 推定 diversity。Binding eligibility 與 implementation verdict 分別核對。 |

## 範圍、subject 與取證

依 `CLAUDE.md`、Bindings m3 §1／§3.3／§5／§7、`.claude/agents/gov-primary-reviewer.md`，以及生效 package 的治理 §2.3、§3.8、§4.1–§4.7、impl-default v2 §6–§7、orch-default v2.2 §6–§7 執行。最後一行採本次 dispatch 明定的 `Verdict: ...` 格式。

已重讀 `audit/spec-SPEC-B1-c1-r1.md` 全文，尤其 SIA-R1-F1 的 required fix（`:25` 起）。R1 Git blob SHA-256 為 `963ab59adaee0d94dce042396291e19a473ba1b435beea1cf7f461494b881a49`，存在於 run2 事件 38，與原樣接收紀錄一致。契約重讀包括 SPEC-B1 §2／§4–§7、OC-1 的 scope／AB／authority／assurance、DESIGN 契約 3／4 的相關條文、SPEC-RESOLUTION-001 §1.1–§1.2、CL-B1-8 §3.2 item 5、CL-B1-12 的計數邊界與 high-risk decision §5。其他既有裁決、Ticket closure、排除範圍依 R1 原 record 引用，沒有展開第二次全面 audit。

`git log` 與 delta 證實：R1 後只有四個 commits；`98e5a1a` 只新增 `tests/test_integration_b1.py`，其餘 `3cb4593`、`241e979`、`a74e683` 只影響 `docs/governance/records/**`。修正沒有改產品程式、舊測試、fixture、conftest 或 pytest config。已閱讀新增測試全部 198 行與修正 worklog §10、run2 事件 38～40 的完整 delta；向下追查 `test_ingest.at`、pace 建立／讀回／ETA 與契約驗證函式。Issue bodies 使用 dispatch 提供的原文版本，沒有呼叫 GitHub。

### 自行執行的 commands 與結果

全部 cwd 均為本 worktree，使用 PATH 的 **Python 3.11.2**，未使用 `.venv`。`python -B -` 表示 PowerShell here-string 經 stdin 執行有界檢查，沒有另存腳本。初次文字讀取的終端編碼問題以 UTF-8 重讀解決；沒有以亂碼內容作契約判斷。

| Command／check | 實際結果 |
| --- | --- |
| `git rev-parse HEAD`；`git status --short` | 開始乾淨；HEAD 為上列完整 SHA。交付前檢查只新增本 record |
| `git log --oneline ff04966..a74e683`；`git log --oneline a6f78f8..a74e683`；`git show --format=fuller --stat 98e5a1a` | 歷史與指定修正一致；correction 為單一測試檔、198 insertions |
| `git diff --stat ff04966..a74e683`；`git diff ff04966..a74e683`；`git diff ff04966..a74e683 -- src tests` | 完整 diff 由 Python subprocess 取得，分別 10757／4229 行；全範圍 43 files、9920 insertions、152 deletions。檢視其 path inventory／歷史，以 R1→HEAD delta 確定本 R2 審查範圍，沒有把取得全 diff 宣稱為重做全面審查 |
| `git diff --name-status a6f78f8..a74e683`；`git diff a6f78f8..a74e683 -- tests/test_integration_b1.py`；同區間的 run2／issue-11 worklog diff | 只有新增 R1 record、新增 integration test，以及 run2／issue-11 worklog 更新；修正測試與兩份 records 的 delta 已逐段閱讀 |
| `git diff a6f78f8..a74e683 -- src`；`python -B -` 對既有 tests、fixtures、conftest、pyproject、DESIGN、docs/spec、decisions、OC-1 的同區間 diff | 全部空字串；既有 implementation／verification／contract 不變 |
| **首次** `$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/sia-r2-q'; python -m pytest -q` | **exit 1：458 passed, 98 errors in 4.44s**。`.pytest_cache` 父目錄當時不存在；tmp_path setup 建立其子目錄時發生 `FileNotFoundError [WinError 3]`。包含新測試在內的 98 項 setup error，沒有測試 assertion failure；保留此失敗，不作 PASS evidence |
| `New-Item -ItemType Directory -Path .pytest_cache -Force` 後，**`$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/sia-r2-q'; python -m pytest -q`** | **exit 0：556 passed in 2.08s**。恢復只建立 worktree 內可忽略 cache 目錄，未改程式、測試或 gates |
| **`$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/sia-r2-rx'; python -m pytest -q -rxX`** | **exit 0：556 passed in 2.04s**；沒有 xfailed／xpassed／skipped／errors |
| **`rg -n 'xfail\|skip\|CL-B1-8\|decision-20261117-issue7-spike-tests' tests/`**（表內的 `\|` 為顯示 table 分隔符；實際 regex 使用未跳脫的 alternation，見下） | **exit 1、無 matches**。符合 CL-B1-8 的 Spec 層要求 |
| **`$env:PYTHONPATH='src'; python -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`** | **exit 0**：derived_segments、route_catalog、pace_table、eta_output 全部 **OK**；CLI 標題仍為 `data contracts v0.2`，符合 CL-B1-2，沒有宣稱完整 v0.3 完成 |
| `$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/sia-r2-target'; python -m pytest -q tests/test_integration_b1.py -vv` | **exit 0：collected 1 item；`test_sb1_ac2_tracks_to_ingest_to_user_pace_table_to_eta PASSED`；1 passed in 0.29s**。新案例可以單獨收集與執行 |
| `git diff --check a6f78f8..a74e683` | exit 0，無輸出 |
| `python -B -`：R1 blob SHA-256 與 run2 比對；新測試的有界用語／標記／憑證 literal scan | R1 hash 如上且出現在 run2；新測試的 P90、percentile、quantile、百分位、分位、警特報、xfail、skip、`sk-ant-`、private-key header 字串計數皆 0。不宣稱此 scan 能辨識所有憑證形式 |
| `git diff --cached --name-only`；交付前 `git status --short`／record 格式檢查 | 無 staged delta；唯一新增檔是本 record，最後一行為指定 verdict |

標記搜尋實際命令：

```powershell
rg -n 'xfail|skip|CL-B1-8|decision-20261117-issue7-spike-tests' tests/
```

## SIA-R1-F1 closure：RESOLVED

- **原 severity：Medium／blocking。** 依據 SPEC-B1 §6 SB1-AC2、治理 §3.8／§4.7；缺的是 subject 內可持續執行的單一完整整合測試。Owner 為 #11 Executor。原 finding 及其 blocking 判定保留在 R1 record，本次不改寫。
- **Required fix 核對：**`tests/test_integration_b1.py:113` 是實際 pytest 測試，沒有標記或跳過。`:39` 的 T901 含同一軌跡中的 1 秒重複位置、30 秒短停留及 200 秒長停留；`:49` 的生成器逐秒產生直線／圓弧與同位置等待點，經 `:83` 的真實 `build_rows`。`:117` 起逐段比對無停留對照軌跡，斷言里程不變、假停留加 moving、short／stopped 秒數及各趟事件數，`:131` 起 private／public／pair 與合併 public rows 皆通過契約 1。
- **多趟與契約 3：**三趟實際 ingest 的共 18 列送入 `:140` 的 `create_pace_table`，在 tmp_path 產生 `user-01.json`，選用與讀回吻合。`:144` 固定重算門檻為 `curv-tercile-110-360`；`:146` 帶同一批衍生列驗契約 3；`:148` 起依軌跡設計獨立分組，每類各 6 列、speed 非 null、ratio 為 short／moving，三類 ratio 均大於 0。CL-B1-12 的界線正確：scheme 不同時 validator 只驗合計，逐類別斷言來自測試，沒有宣稱 validator 已重算分類。
- **matching-route 的 ok ETA 與 invariants 8／9：**`:159` 以 pace header 的同一 scheme 建立合成路線，`:160` 驗契約 2；`:161` 讀回同一 user table。`:164` 分別計算無休息／600 秒休息 ETA，`:166` 強制 status 為 ok，`:167` 核對同 header margin；`:170` 起逐列斷言速度換算、正值 allowance、累積 typ 與 safe margin，`:180` 帶同一份 header／categories 驗契約 4，實際執行 `validate.py:345` 的 invariant 9 及 `:398` 起的 invariant 8。沒有以 unknown 全 null 路徑讓公式落空。
- **時間傳遞與整份資料集：**`:186` 起檢查休息不改 allowance 或 safe−typ，只平移累計休息；`:190` 固定休息累計為 `[0,0,600,600]`。`:195` 將衍生列、路線、同一配速表與兩份 ETA 交給 `validate_dataset`，四組 violations 均為空。
- **Closure evidence：**本 Reviewer 的兩次完整成功回歸及單獨測試均通過；closure 不是採用 Executor 的「已修正」或歷史 mutation 敘述。原 required fix 已完整滿足，無剩餘 required fix。**SIA-R1-F1 = RESOLVED。**

修正只增加測試，沒有全域設定／猴子補丁或產品覆寫；原 helper `at` 只將生成的 x／y／秒轉為合成 TrackPoint（`tests/test_ingest.py:17`、`:21`），沒有外部資料讀取。既有 555 項測試仍通過，新測試增加為 556；沒有修正直接產生或暴露的新 blocking defect。

新增 blocking findings：**無**。新增 non-blocking findings：**無**，因此沒有新增 disposition／owner。R1 所引 #7 R2-F1、#9 C2-R2-N1 等既有 tracked items 維持原 disposition／owner，本次沒有新 evidence 推翻其 closure，不延長 cycle。

## §4.7 五個 scopes 在 closure 後的狀態

| Scope | R2 結論與 evidence |
| --- | --- |
| **1. 跨 Ticket invariants** | **PASS（本 Spec 分配範圍）。** R1 record `:90` 起的接口／缺漏傳遞／rule 3 隔離結論保留；src 與舊測試無 delta。新增測試把 #9→#10→#11 及 #7 的契約 1／3／4 真正串成同一條鏈，停等時間、ratio、header margin、ETA 算式均有實質斷言，補足 R1 唯一缺口 |
| **2. Spec-level AC coverage／allocated boundary** | **SB1-AC1～AC6 均 PASS**，逐條如下。R1 `:102` 起對 AC 集合涵蓋 allocated AB 部分的分析保留；補上 AC2 後沒有新 allocation gap。AB-13 的 SIA closure 可由本 record 支持，但 DA phase acceptance 仍需另外作成 |
| **3. 整合行為** | **PASS（有界合成行為）。** R1 `:136` 起第一類已驗證行為保留；其第二類「subject 沒有完整測試」已由新案例解除。三趟 ingest→user table 寫入／選用／讀回→matching-route ok ETA，以及休息只平移時間均通過。R1 第三類排除保留，沒有宣稱處理 RI-1～RI-3 或完整 Planner workflow |
| **4. 最終 subject verification／audit coverage** | **PASS。** R1 `:144` 起的既有 Ticket coverage 保留，原 implementation／tests／fixture／contracts 未改；本 R2 審查唯一非 record delta 並在指定 HEAD 重跑成功。新案例已在 subject 內，補足原本 Spec coverage 缺口。當次 runtime binding 的採用核對由 dispatcher 在事件 40 完成 |
| **5. Traceability／Outcome Contract boundary conformance** | **符合。** R1 `:150` 起的引用鏈／boundary 判斷不受修正影響。修正明確對應 SB1-AC2／SIA-R1-F1，經 run2 事件 39 在 #11 同一 worklog identity 執行，worklog §10 可追溯；沒有改需求、設計語義、Must、凍結基線或保留操作，沒有新 boundary ambiguity |

### SB1-AC1～SB1-AC6

| AC | Closure 後狀態與理由 |
| --- | --- |
| **SB1-AC1：PASS** | 沿用 R1 `:106`、`:113` 起的逐票 closure 核對（#7 c1-r2、#9 c2-r2、#10 c1-r2、#11 c1-r1、#8 c1-r1；run2 §8.1／前一 run §7.1）。correction 沒有變更這些 artifacts 或 Ticket 契約。#11 的 integration rework 本次依 SIA cycle 閉合，不重開 Ticket audit |
| **SB1-AC2：PASS** | 新增 `tests/test_integration_b1.py:113`，符合全部 required fix，見上節。單獨執行 1 passed；完整 suite 556 passed |
| **SB1-AC3：PASS** | 本次 contract CLI 四組 OK，完整 suite 與 -rxX 各 556 passed；tests 無 xfail／skip／CL-B1-8 標記，符合 CL-B1-8 §3.2 item 5 |
| **SB1-AC4：PASS** | 沿用 R1 `:109` 對規則 3 判定表與匯入隔離的結論；validator／rule3 tests 未改，完整回歸通過。新增測試未引入 rule3→pace 的依賴 |
| **SB1-AC5：PASS** | 沿用 R1 `:110` 在 CL-B1-11 §3 item 6 明定邊界內的結論；ingest CLI 與相關 tests 未改且回歸通過。非 pace 端 alias／metadata 殘餘與 TOCTOU 仍依 R1 的限制，沒有擴大 PASS |
| **SB1-AC6：PASS** | R1 `:111` 的舊內容核對保留；新增測試與 records delta 未新增受禁宣稱，清楚寫明 synthetic／CL-B1-12 限制／RI 排除，沒有把測試當 E1 Lite／E2 結果 |

### 分配到的 acceptance boundary

| 分配 | Closure 後的限定完成狀態 |
| --- | --- |
| **AB-3 計算核心** | 原停等分類／user 版本建立選用 evidence 保留；AC2 的完整鏈路已補足。不含上傳、合併、去重複、摘要或 UI |
| **AB-4 ETA 計算與程式用語** | AC2 補足完整鏈路；同一 header／categories、allowance／margin／break checks 通過。文件／介面後續工作仍不計入 |
| **AB-7 規則 3 範圍與三值** | R1 evidence 保留，AC4 回歸通過；原因代碼、RuleResult、其他規則仍排除 |
| **AB-10 本 Spec 的 NFR2／NFR4／隔離部分** | 合成來源及完整計算傳遞新增 evidence；unknown／隔離既有測試回歸通過。真實資料狀態仍 NOT VERIFIED |
| **AB-11 產品端機制部分** | 研究版本不覆寫、角色拒絕沿用 R1；新例實際建立／選用 user 版本。不包含 freeze manifest 或 E1／E2 script checks |
| **AB-13 本 Spec 的整合條件** | pytest 與本 SIA closure 已有 evidence；**DA phase acceptance 尚未在 subject 作成，AB-13 不宣告全部完成**。release gate、OC-1 completion 不能由此 verdict 推定 |

SPEC-UI0、SPEC-R1 仍為後續未結 Spec（run2 §5；R1 record `:134`），本次不是 OC-1 最後一份未結 Spec；沿用 R1 的 allocation check 邊界，不執行全 OC-1 最終分配合計核對，不宣告完整 AB 或 OC-1 完成。

## 高風險與 NOT VERIFIED／NOT RUN

本次是 R2 targeted closure；high-risk decision §5 的既有核對沿用 R1 `:156` 起，本次只核對修正影響。**H-2**：新增軌跡來自明確生成器與既有虛構原點，路線座標／時間／代號皆為合成佔位，無 fixture 改動、外部 API 或真實 GPX 讀取。**H-3**：文字區分合成測試與實驗，明示 CL-B1-12／RI 邊界；首次失敗與恢復均如實記錄。**H-4**：新增案例強制 ok、三類配速非 null、allowance 大於 0，使公式檢查有實質輸入；既有 unknown／缺漏／拒絕路徑未改且整套回歸通過。沒有新付費或憑證路徑。

| ID | 狀態、原因與 required authority／owner |
| --- | --- |
| NV-1 | 真實 GPX、manifest 角色、holdout／excluded 隔離、真實 LOO／ETA 表現與公開衍生列揭露程度 **NOT VERIFIED**；需要私有資料，沒有明確路徑授權。required authority = **acceptor**（RB-7），沒有嘗試取得 |
| NV-2 | 真實磁碟的 alias／hard link／symlink／同內容不同檔名及 G-ING 殘餘 **NOT VERIFIED**；沿用 R1 NV-2 與 CL-B1-11 item 4。owner = Design Authority／Orchestrator；任何私有資料 metadata／內容授權 = **acceptor**。沒有額外建立真實 symlink 探測；suite 的現有合成／模擬案例不能代替真實資料核對 |
| NV-3 | 本次全程 runtime binding／存取／作者／回傳 hash **NOT VERIFIED by reviewer**；原始 rollout 位於 worktree 外，未讀取。required authority／owner = **dispatcher／Orchestrator**，在 run2 **事件 40** 核對並補記後方可正式採用。採用前須驗證實際 mapping 符合 O-6，不能用本 verdict 取代 |
| NV-4 | worklog §10.2 的 Executor 歷史 mutation 三例與完整外部操作歷程 **NOT VERIFIED as historical execution**；本次沒有讀取外部原始材料，也沒有修改產品檔案重演 mutation。本次 closure 依自己的 source review 與親跑結果成立。若需歷史原始證據，owner = **Executor／dispatcher** |
| NR-1 | RI-1～RI-3、G-REG、freeze manifest／E1／E2 version checks、rule 3 原因代碼、WeatherSegment／RuleResult 與 CL-R1-11（SPEC-R1／#13）仍排除，不記已完成；後續由 **Design Authority／Orchestrator** 派工。真實資料回歸與正式 E1 Lite／E2 **NOT RUN**，required authority = **acceptor** |
| NR-2 | **DA phase acceptance、OC-1 completion、release 未執行／不由本 record 宣告。** 後續由 **Design Authority** 引用有效本 closure record 作 phase acceptance；dispatcher 先完成事件 40 核對。沒有 stage、commit、push、PR、merge、網路或 GitHub 操作 |

本 R2 的原 blocking finding 已解除，沒有修正引入的回歸或直接產生／暴露的新 blocking defect；本 record 支持 SPEC-B1 的 SIA closure，其他完成條件仍依各自 authority 與 records 處理。

Verdict: PASS
