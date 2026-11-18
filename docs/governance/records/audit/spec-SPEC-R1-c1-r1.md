# SPEC-R1 — Spec Integration Audit，cycle 1 R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受版本 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-R1 v1（`decisions/derivation-spec-r1.md` §2、§4、§5 E-1～E-6／R1-1～R1-4、§6 SR1-AC1～AC5 與排除清單、§7）＋CL-R1-11～29 → Issues #13、#14、#15、#16 |
| Subject BASE | `1fd1de3585ea23f80842ac3276fe9305369b51e3` |
| Subject HEAD | `804362dc7b559867228eccbb289e22a055526bd2`，本專用 worktree 的 detached HEAD |
| Audit kind | **Spec Integration Audit of SPEC-R1，R1（full independent audit），cycle 1；不是 Ticket audit；SPEC-R1 是 OC-1 最後一份未結 Spec** |
| Role | `primary_reviewer`（Codex） |
| 日期／位置 | 2026-11-18，Asia/Taipei；`C:/Users/yotsu/AppData/Local/Temp/cxsiar1` |
| 結果 | **BLOCKING：SIA-R1-F1**。SR1-AC2 缺少要求的跨 Ticket 契約整合測試。另有具 owner 的 non-blocking 紀錄缺漏，以及逐項列出的 OC-1 分配缺口；後者交 DA，不由 Reviewer 補定設計或接受。 |

本 record 依 `.claude/agents/gov-primary-reviewer.md` 的「紀錄」要求自寫；最後一行採本次派工明定的 `Verdict:` 格式。Issue bodies 使用派工附錄的原文，沒有呼叫 GitHub 或其他網路服務。

## Assurance

### (a) 四項 independence properties

| Property | 滿足方式與證據界線 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread，沒有 Executor 或先前 Reviewer 的對話。自行從原始碼、測試、契約與 git 歷史形成判斷；worklogs 與正式 records 的結論作為待核對主張。沒有委派 subagent。 |
| Verifiable binding | 依 Bindings m3 §3.3 O-6，由 dispatcher 核對本次 rollout 全部 turn 的 model／effort／sandbox、讀寫存取及作者事件，記入 `run/run-20261117-oc1-run2.md` §6 的**本次「SPEC-R1 SIA cycle 1 R1／cxsiar1／HEAD 804362d」dispatch event**。受審版本最後一個編號事件是 **109**（`:187`，#16 completion）；`:78` 的 SPEC-R1 SIA 列仍空白，尚無本次 dispatch event／binding。事件 106 是 #16 R2，不能代用，也不虛構下一事件號。見 NV-BIND：採用本 record 前由 dispatcher 補核；目前不能宣稱四項 properties 已全部獲 binding 實證。 |
| Autonomous access | 自行取得本 worktree 內原始材料、查 git metadata、執行 PATH 上的 Python 與測試；不限於 Executor 摘要。未讀、列出或搜尋私有資料／憑證，未讀取其他 checkout、外部 rollout 或 worktree 外路徑，未執行 experiments。 |
| Self-written record | 本 Reviewer 自行建立本檔，是唯一新增的非 ignored 檔案；沒有改實作、測試、契約、worklog、其他 record 或 gate，沒有 stage／commit。dispatcher 依 O-6 核對唯一增量及原樣收錄的 SHA-256；不由 Executor 代寫、改寫或裁剪。 |

### (b) Actual models 與 diversity

Executor 的 dispatcher 證據在 run §6：#13 事件 65（`claude-opus-5-5`／`high`，agent `a95eaf00e5bb8b468`）；#14 事件 77（同 model／effort，agent `a731e697ea497fcf3`）；#15 事件 85／87 的同一 Executor；#16 事件 103、105、108（同 model／effort，agent `a1e2cfa52290d496f`，事件 108 記全部 330 則符合）。本次 Primary 是 **Codex**。Bindings 的 qualified mapping `gpt-6.1-sol`／`high` 是預期 mapping，受審 run 尚無本次實際 model／effort／sandbox 的 dispatcher 核對，不能拿舊派工代替。因此 **no model diversity claim**。#16 cycle 2 R1 的 `diversity_lost` 保留為該次歷史事實，不外推為本次狀態。

## 材料、方法與實際檢查

適用依據：治理 v2.2 §2.3、§2.4、§3.8、§4.2～4.7；impl-default v2 §6、§7；orch-default v2.2 §7 P1～P10；Bindings m3 §3.3、§5、§7；high-risk decision §5。另讀 root `CLAUDE.md`、Reviewer definition、OC-1、三份 derivation 與 B1／UI0 phase acceptance、first-run derivation、DESIGN §5／§9、SPEC-001 §2／4.12～4.14／5.5／7.11／相關 S 編號，以及下列契約決定：

- `decision-20261118-issue10-c107.md`（CL-R1-11）。
- `decision-20261118-issue13-c131.md`（CL-R1-12、13）。
- `decision-20261118-issue14-c141.md`（CL-R1-14～19）與 `decision-20261118-issue14-qalt1.md`（CL-R1-20、21）。
- `decision-20261118-issue15-c151.md`（CL-R1-22～24）。
- `decision-20261118-issue16-c161.md`（CL-R1-25～27）、`decision-20261118-issue16-c2r1f3.md`（CL-R1-28）、`decision-20261118-issue16-c165.md`（CL-R1-29）。
- `ruling-20261118-issue16-c1.md` 與 Addendum A、四票的 audit history／最終 closure records、worklogs 的 AC evidence 與結案／tracked-item 段落、run §6 事件 61～109 與 §8.1。

以原始碼全文、差異、測試的實際斷言與執行結果交叉核對，不將舊 audit 的 PASS 當作本次整合的充分證據。所有命令限本 worktree。Python 一律以 `python` 啟動；沒有以環境目錄路徑呼叫 Python，也沒有覆寫 `PYTEST_DEBUG_TEMPROOT`。

| 命令／檢查 | 結果 |
| --- | --- |
| `git rev-parse HEAD`；`git status --short` | HEAD 如表頭；起始 status 空白。 |
| `python -c "import sys; print(sys.executable)"`；stdin Python 讀版本與既有 pytest temp-root 設定 | Python 3.11.2；直譯器位於本 worktree；temp root 是 `C:/Users/yotsu/AppData/Local/Temp/cxsiar1/.venv/tmp`。沒有變更該設定。 |
| **`python -m pytest -q`** | **exit 0；2238 passed in 44.37s**。 |
| **`python -m pytest -q -rxX`** | **exit 0；2238 passed in 43.13s**。兩次均無 failed／error／xfailed／xpassed／skipped 摘要。 |
| **`rg -n 'xfail\|skip' tests/`**；stdin Python AST 掃描 `tests/**/*.py` 的 Name／Attribute（xfail、skip、skipif、importorskip） | 文字只有 `test_contracts.py:1157` 的 docstring `skipped` 與 `test_routing_store.py:330` 的函式名稱 `being_skipped`；AST marker／call 結果 `[]`。沒有 pytest bypass。 |
| **`$env:PYTHONPATH='src'; python -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`** | **exit 0**；`data contracts v0.3`；derived_segments、route_catalog、pace_table、eta_output 全部 **OK**。 |
| `git diff --stat 1fd1de3..804362d -- src tests`；`git log --oneline 1fd1de3..804362d -- src tests`；指定檔案 diff／讀取 | 26 個 source／test／fixture 檔，7880 insertions、25 deletions。18 個 implementation commits 與 pack 一致；其餘 67 commits 只改 `docs/governance/records/**`（逐 commit 以 `git diff-tree --no-commit-id --name-only -r` 核對）。 |
| `git diff 1fd1de3..804362d -- src/moto_copilot/contracts src/moto_copilot/routes/catalog.py tests/test_eta.py tests/test_integration_b1.py tests/fixtures/contract_v02/mock_dataset.json` | 契約改版、fixture 三鍵與版本相符；既有 B1／ETA tests 只補來源欄位。catalog 的 diff 只限 CL-R1-12 允許的模組說明、註解與三鍵。 |
| `git diff --exit-code 1fd1de3..804362d -- tests/test_routes_pace_eta.py` | exit 0、空輸出；producer 契約測試原文保留。 |
| `git diff 665a86f..804362d -- tests/test_routing_store.py`；stdin AST 比對所有頂層函式 | added `[]`、removed `[]`；唯一 changed 函式是 `test_the_routing_package_imports_no_network_or_environment_modules`，符合 CL-R1-25。 |
| stdin AST 核對共用介面測試模組的呼叫與 `checkpoint_id` 文字；人工重讀相關 imports／assertions | `test_routing_engine.py` 只見 get_route／plan，`test_routing_transport.py` 見 get_route，兩者沒有 validate_route_catalog／validate_dataset 呼叫，也沒有 checkpoint_id；UI0 的 plan 是其 mock 流程。全 tests 搜尋及原始碼核對未找到 SR1-AC2 所需的契約整合測試。詳 F1。 |
| stdin `git ls-files -z`，只比對 index 路徑字串並輸出計數 | `data/` 前綴 **0**、`.gpx` **0**、`.fit` **0**、檔名 `.env` **0**、`.key` **0**。另以 `git ls-files -- 'data/*' '*.gpx' '.env' '**/.env' '*.fit'` 得空輸出。沒有存取這些路徑的內容。 |
| stdin 比對 src／tests 新增行的長 `sk-ant-` 與 private-key header 樣式，只輸出計數 | 兩項均 **0**。原始碼核對未見憑證處理；不把有限樣式掃描說成所有秘密形式的證明。 |
| `git diff --name-only 1fd1de3..804362d -- DESIGN.md README.md docs/spec .claude CLAUDE.md pyproject.toml app` | 空輸出；沒有暗改契約、依賴、凍結介面或 B1／UI0 產品程式。 |
| `git diff --check 1fd1de3..804362d` | 有 records 既有空白警告：issue-13 worklog 的兩處 trailing whitespace，issue-14 worklog 檔尾空白；沒有 source／test 警告。不將其誤記為 clean，也不據此新增產品要求。 |
| `Get-Content -Encoding UTF8`、指定檔案的 `rg -n` 與 stdin AST／git probes | 用於核對條款、行號、函式與差異。初次 Get-Content 的中文編碼錯誤以 UTF-8 重讀；Windows 不展開 `tests/test_routing*` 的一次 rg 失敗，改用明確檔案／tests 目錄；一次讀不存在的 orch `default-v2.md`，以指定 references 目錄查得並讀生效的 `default-v2.2.md`。沒有將失敗命令當成驗證。 |

沒有重跑外部 scratchpad 的 mutation scripts，也沒有自行修改 source 作突變。worklog 的突變結果保留為 Executor evidence，本次獨立執行的是上述檢查與最終 suite。沒有真實網路、GitHub、API、Streamlit server 或 experiments 執行。

## 範圍一：跨 Ticket invariants

| Invariant | 原始碼／測試 evidence 與結論 |
| --- | --- |
| 契約 v0.3 ↔ routing IDs | schemas 的三個 ASCII 完整字串 pattern、validate.py 的來源／references／hex 一致性與 checkpoint 前綴檢查相符；CL-R1-11 的 `_whole_count` 保留。snapshot.py 的 `route_id_for` 與 target_gpx.py 的 `target_gpx_route_id` 使用同一格式。引擎產生的 RS／SN hex 一致有 `test_routing_engine.py:1699`；但全部模式及 GPX 輸出的 checkpoint 契約整合未有證據，**未完整成立，F1**。 |
| 正規化與 identity | canonical.py 的 `Decimal(repr(value))`、向零捨去、固定小數位與負零處理，同時被 request_key／指紋／snapshot hash 使用；snapshot hash 排除自身 ID 與 fetched_at。CL-R1-14、15、16、18、19 的角色沒有混用：GPX 整數公尺採 half-up；引擎採用先比較原值，再正規化存檔。snapshot／store tests 與 engine `:1387` 的略大於 200 m 拒收案例隨 suite 通過。 |
| R1-2 存放 ↔ R1-4 採用（CL-R1-17／20／21） | source.py 只經三個選取函式，沒有重新列舉或先用 predicate 排除候選；選取、put、strict 例外向上傳遞，沒有轉 route error、重試、改用過期快照或其他目錄。store.py 候選按名稱，明確 stat 且在 read 前拒絕非 regular file。engine tests `:1491`、`:1503`、`:1511`、`:1521`、`:1535` 在整合入口核對上述停止、不呼叫引擎與無路線；**成立於合成測試範圍**。 |
| R1-3 ↔ R1-4 的 target GPX passthrough（CL-R1-24） | source.py `_target_gpx` 原樣傳出 ID、ref、trip type、各方向原序 points／length、c_k 與 error code／case；road_names 空、snapshot_id null。target 分支在 store／engine 分支之前。engine `:1618` 參數化 one_way、detected round_trip、騎士指定落兩點間的 round_trip、單向忽略 km；以 Untouchable store／拒絕傳輸證明不使用兩者。`:1653` 核對 invalid 與兩種 not_round_trip，`:1659` 保留 caller errors。**成立**。 |
| #14 無網路計算 ↔ #16 真實傳輸（CL-R1-25） | 最終靜態測試 `test_routing_store.py:532` 遞迴掃描全部 .py；只精確豁免 http_transport.py 的 http／ssl，仍禁止其他網路模組、環境讀取及其他檔案引用該模組。`:518` 封鎖 socket 下執行 hash／store／selection；最終 suite 通過。相對 #14 最終 subject 僅此測試函式被改，沒有放寬 #14 AC；**成立**。 |

## 範圍二：Spec-level AC 與所分配 AB

### SR1-AC1～SR1-AC5

| AC | 判定 | Evidence 與限制 |
| --- | --- | --- |
| SR1-AC1（derivation `:144`） | **PASS** | 四票 P1～P8 及 closure 如下表；worklog 有 E-1～E-6 mapping，合成來源／離線方法與 test 改版理由可追溯。CL-R1-12 的無 xfail／skip、catalog 封閉 delta 與原測試保留均在本 HEAD 自行核對。P9 留在 phase 層不冒充 Ticket 尚未結案。 |
| SR1-AC2（`:145`） | **FAIL** | get_route 的一般首次存放／重用、Snapshot Mode、strict 及 GPX 單向／來回各有行為測試，T-9 有真實傳輸加替身連線；但沒有把這些輸出的 route_id／snapshot_id／checkpoint_id 一起交 R1-1 契約驗證。`:1699` 只檢查一次引擎路徑的 RS／SN regex 與 hex；沒有 checkpoint_id。**SIA-R1-F1**。 |
| SR1-AC3（`:146`） | **PASS（本 Spec 的合成路線層範圍）** | engine `:524`、`:562`、`:691`、`:771` 及 non-200、overflow、surrogate、warnings／offset／order 測試從 get_route 斷言失敗沒有路線／里程／名稱與新快照，國道訊號優先；CL-R1-21 put failure 沒有回傳未存檔路線。CL-R1-27 trace warnings、3xx／傳輸錯誤也拒收；GPX errors 原樣傳出。不是對所有可想像輸入或資源耗盡的窮舉宣稱。 |
| SR1-AC4（`:147`） | **PASS（依已分配層級）** | FakeEngine、HTTPSConnection／wire doubles 與 socket／DNS guards；transport T-5（`:278`、`:293`）檢查固定例外／traceback 不含合成請求座標；GPX path 測試（engine `:1639`、test_target_gpx 隱私／解析失敗測試）核對結果／錯誤／log 不含路徑與檔名。內部 AdoptedRoute／snapshot 本來承載幾何，這不是對 PlanResult／LLM 隱私已完成的宣稱；該部分未分配。 |
| SR1-AC5（`:148`） | **PASS** | 新增 adoption.py 說明明寫國道檢查與路線共用引擎／開放圖資，並非道路主管機關資料的獨立驗證；target_gpx.py 明寫 conservative heuristic、NOT validated with real data；`test_target_gpx.py:983` 通過。變更沒有宣稱 ETA_safe 是 P90、降雨規則是官方警特報、配速比 Google Maps 準確，或檔案只留在使用者電腦。 |

### Ticket closure 與最終 subject

| Ticket | 有效 closure evidence | 最終範圍核對 |
| --- | --- | --- |
| #13 R1-1 | `audit/issue-13-c1-r2.md`，subject `be76a97`，PASS；run 事件 66 binding、§8.1 completion；worklog §10 | 原 R1-F1 已由型別守衛修正。be76a97 至本 HEAD 的 contracts、test_contracts、catalog delta 空。 |
| #14 R1-2 | cycle 1 Alternate CLOSURE＋DA CL-R1-20 後 cycle 2 `audit/issue-14-c2-r1.md`，`6f08a5a`，PASS；run 事件 78、§8.1；worklog §12 | canonical／request_key／snapshot／store／test_routing_snapshot delta 空；test_routing_store 只有上述 DA 授權的一函式 delta，已重新核對。Low C2-R1-N1 的 pytest 輸出補登在 worklog §12.1。 |
| #15 R1-3 | `audit/issue-15-c1-r2.md`，`48ff350`，PASS；run 事件 86、§8.1；worklog §11 | geometry／target_gpx／test_target_gpx delta 空。XML encoding regression retained。 |
| #16 R1-4 | cycle 2 `audit/issue-16-c2-r2.md`，`18a5c5c`，PASS；run 事件 106 binding、109 completion；worklog §15 | `git diff 18a5c5c..804362d -- src tests` 空。R1-F1、R2-F1、C2R1-F1～F4 closure、FA Addendum A 與 CL-R1-28／29 實作相符。 |

這些是既有 Ticket 結案 evidence 的核對；本 record 不重開已閉合 finding。F1 是對整合 subject 的新 evidence-sufficiency finding。

### SPEC-R1 §7 的分配部分

| AB | Spec AC coverage 與實際狀態 |
| --- | --- |
| AB-1（derivation `:156`） | route client、採用、snapshot 保存的**能力**由 R1-2／R1-4、SR1-AC3、T-9 涵蓋；真實傳輸層存在。首次實際取得道路與端到端操作仍 NOT RUN，不能把能力測試寫成 AB-1 整體 PASS。 |
| AB-2（`:157`） | routing／GPX 單向、來回及明確錯誤由 AC2／AC3 涵蓋其路線層分配；**AC2 整合契約 evidence 未完成**。行程描述、追問、期限、gazetteer 不在分配內。 |
| AB-10（`:158`） | NFR2 的送出內容／通用 User-Agent 與 GPX 不外送、NFR4 的 route failure 由 AC3／AC4／AC5 有證據。位置本身是不是公開地標、隱私裁切／錨點代換仍屬 G-RREQ／TI-C16-3，不宣稱已驗證。 |
| AB-11（`:159`） | strict selection 的 FrozenEntry／file SHA-256／method／stop without fallback 由 store tests 與 engine `:1452`／`:1459` 有證據；清單檔案格式、E2 Runner／Oracle 不在分配內。 |
| AB-13（`:160`） | pytest 與 index gate 成立；本次 **SIA closure 未成立（F1）**，DA phase acceptance 尚未執行。故分配部分尚未完成；不將正常的後續 phase acceptance 順序另算 implementation defect。 |

Spec AC 的條文可追溯至這五項分配，但目前 evidence 未全數滿足，不能宣告 SPEC-R1 phase acceptance。

## 範圍三：整合行為與高風險核對

一般模式經 get_route → R1-2 find_reusable → R1-4 各方向採用 → build_snapshot → put → _from_snapshot；第一次存一份、第二次不發引擎請求（engine `:423`、`:493`）。31 天後內容相同保留舊檔／時間，內容不同新 ID／新檔，取得失敗不改用過期快照（`:500`、`:513`、`:524`）。Snapshot Mode（`:1438`）與 strict（`:1452`）只選取；strict stop、壞檔與寫入錯誤保持專用例外。target GPX 經另一個來源分支原樣帶出，沒有挪用引擎採用檢查。T-9（transport `:395`）將真實 HTTPS transport 接替身連線，再走同一 get_route。這些整合**行為**有證據；欠缺的契約串接不因它們通過而消失。

| 類別 | 最低核對範圍、結果與未涵蓋部分 |
| --- | --- |
| H-1 | valhalla.py 常數端點／明確設定，http_transport 再檢查 HTTPS URL／封閉 paths，沒有 redirect／proxy／retry／環境端點讀取；TLS CERT_REQUIRED＋hostname check＋default cert loading，固定正逾時。T-1～T-10 隨 suite 通過，T-11／12（`:438`／`:450`）驗證 CL-R1-28 與無 keylog 檔。index .env／key 0，沒有付費 client。**合成傳輸範圍成立**；實際 TLS／server NOT RUN。SSL_CERT_FILE／DIR 可影響信任根，OPENSSL_CONF NOT VERIFIED，見既有限制，沒有宣稱完全不受環境影響。 |
| H-2 | geometry reader 沒有 path／filename 結果欄位，解析錯誤不附 parser text／chain；target 分支不接傳輸或 store。引擎只送 positions 與固定參數，trace 只送引擎自己的 shape，status 為空本文，headers 封閉、User-Agent 通用；codes／roles 不送出。合成幾何與 GPX 都由 tests 產生，fixture 有 mock 註記；index gate 為 0。**本層範圍成立**。真實資料、錨點轉換、PlanResult／LLM 裁切 NOT VERIFIED；C-14-6 歷史樣例的公開前處置仍交 acceptor，不宣稱實際外洩或已清理。 |
| H-3 | 沒有讀 holdout，沒有正式 E1 Lite／E2 執行；DD-R1-2／CL-R1-26／29 的 unreported／null 誠實區別 metadata 缺報。strict 只提供凍結機制。折返偵測保留未以真實資料驗證的聲明；沒有將 synthetic／Spike 的結果冒充研究結果。 |
| H-4 | 國道任一訊號優先，HTTP 非 200 也收集可讀訊號；warnings／trace failure／缺 has_highway／長度差／offset／via order 失敗不採用，整條路線才存檔。每方向各有 request／shape／time，不反轉去程；store 與 strict 錯誤向上停止。GPX 不猜 trip type、不以非法 rider m 回退自動、不反轉補點。已測失敗路徑與 suite 成立；沒有以此宣稱 Planner／規則 5／計畫狀態已整合。 |

## 範圍四：最終 subject verification／audit coverage

逐 commit 的 implementation 清單與 pack 一致：#13 `153adca`、`6ec1903`、`3c065f8`；#14 `aa42392`、`366866c`、`5eee704`、`359b948`、`665a86f`；#15 `b771d9f`、`e78cc9f`、`efbffe8`；#16 `7cb4b0c`、`f6810d2`、`65aa00c`、`022f629`、`a4f0cd9`、`ecddc57`、`9cc566a`。其餘只在 Bindings 宣告的 record-only paths，未藉此掩蓋產品改動。

四票最終 source 與其 audit subject 的對應如前表；唯一跨已結案票的 test delta 是 CL-R1-25 明許的靜態測試，已在最終 HEAD 重讀、作 AST 比較並執行。兩次完整 pytest 與 CLI 都在 **804362d** 執行，沒有拿舊版本測試當作本 HEAD 的結果。最終單票 coverage 成立；**必要的 Spec 整合驗證仍有 F1 缺口**，故不能由單票 closure 推導 SIA closure。

## 範圍五：traceability、boundary 與全部 derived Specs 的合計核對

Issue #13～#16 以 SPEC-R1 §5 為權威定義，run §4 的建立雜湊、CP-2 的歷史核對與本次 pack 原文對應；CL-R1-11～29 各以 DA decision record 加入引用集合。SPEC-R1 沒有恢復 Scope Reduction，沒有擴張 Must、改 Plan Schema、實作 G-RTE 或暗改上位契約。CL-R1-12 對 Spike 的三鍵改動並不代表 routes 已收編。

本次另依治理 §4.7 第五範圍／OC-1 §3.1 核對全部 derived Specs：**SPEC-B1＋SPEC-UI0＋SPEC-R1 合計仍未涵蓋整個 AB-1～AB-13**。B1、UI0 的 phase acceptance records 只接受各自分配部分，明文保留整體未完成；不能將它們的 ACCEPT 解讀為剩餘 boundary 被接受省略。分配表的重疊（AB-10、AB-11、AB-13）各有具體子範圍，沒有發現必須另判的新歧義重疊；公開位置的 upstream 保證由 TI-C16-3 承接，不算已涵蓋。

### 分配缺口 findings：SIA-R1-G01～G13

以下每一列都是獨立 finding，**Severity＝Medium／non-blocking（設計 routing signal）**；依治理 §4.2／§2.4，不將已記錄的未 derivation 範圍改判成 #13～#16 implementation defect。**Disposition＝保留 open、交 DA determination／後續 derivation；共同 owner＝Design Authority，Orchestrator 負責依規則派工；實際 routing requests＝NOT RUN（本次禁止網路／外部派工）**。這些 findings 不延長本 SIA 的 implementation correction cycle，也不允許 OC-1 最終 closure。每列 required fix 是補齊既有 accepted boundary 的分配／驗收證據安排；如需改變 OC-1 或保留權限，DA 必須交 acceptor，Reviewer 不替代其決定。

共同證據：OC-1 §3.1／§3.2；`decision-20261117-oc1-first-run-derivation.md`（下稱 first-run）§4 `:96`～`:108` 與 §6 `:145`～`:157`；三份 derivation §7；B1 phase acceptance §6／§8；UI0 phase acceptance §6／§8。下表逐列補足定位與所需 authority。

| Finding | AB／已有分配 | 缺口、evidence 與 required fix／authority |
| --- | --- | --- |
| SIA-R1-G01 | AB-1：R1 路線能力 | first-run `:96`；缺端到端實際執行與 routes／sources／validator／planner／app 分配（G-RTE、G-SRC、G-VAL、G-PLN、G-APP）。DA derive 串接與 evidence；OC-1 §9.1 C-1 的 Planner 真實 LLM 開發／Demo 額度須 **acceptor**，目前 BLOCKED；Valhalla 實際請求 NOT RUN。 |
| SIA-R1-G02 | AB-2：R1 路線層 | first-run `:97`；行程描述解析、追問、期限／詞彙表與輸入保護尚未分配（G-RREQ、G-PLN、G-KB、G-CON，SB-6／SB-10）。DA 定義並 derive；憑證／新增支出由 **acceptor**。F1 是另列的本 Spec evidence 缺陷，不用未來 Spec 掩蓋。 |
| SIA-R1-G03 | AB-3：B1 重建核心 | first-run `:98`、`:146`；多檔上傳、合併去重複、行程清單接續與摘要／Profile 管理未分配（G-ING）。DA 決定鍵、保存語義並 derive；如需保留／排除行程內容雜湊，**acceptor RB-7**，NOT VERIFIED。 |
| SIA-R1-G04 | AB-4：B1 ETA 核心 | first-run `:99`；產品介面與文件的 FR3 用語／顯示仍需 G-APP、G-DOC 分配。DA derive 並安排對照驗收；不能用 mock UI 或核心不稱 P90 推論全部介面／文件完成。 |
| SIA-R1-G05 | AB-5：無完整分配 | first-run `:100`、`:149`；氣象預報／日照與鄉鎮／時段（G-SRC，SB-3／4／5）未 ready，沒有所需真實授權碼回應 evidence。DA 處理規格／C3 後續；憑證由 **acceptor RB-3**，目前 BLOCKED／NOT RUN，不能以 mock 代替。 |
| SIA-R1-G06 | AB-6：無分配 | first-run `:101`；沿線加油站／檢查點投影、油量逐段檢查、路況情境與來源格式（G-RTE、G-SRC）尚缺。DA 定義資料與投影語義並 derive；資料集欄位／營業格式 NOT VERIFIED，實際資料取得依後續授權。 |
| SIA-R1-G07 | AB-7：B1 規則 3 範圍 | first-run `:102`、`:150`；規則 1／2／4／5、RuleResult／原因代碼、計畫狀態／排序、重新規劃、無可行解與匯入限制未分配（G-VAL、G-CON、G-PLN）。DA derive；SB-10 殘餘與 C3 依賴不能視為已定案。 |
| SIA-R1-G08 | AB-8：UI0 Skeleton | first-run `:103`、`:153`；UI Delta Review 仍須 **acceptor** 實際決定，正式 backend integration（G-APP）尚未分配。DA 依 review／後端就緒狀態 derive；UI0 ACCEPT 不是正式整合或整個 AB-8 PASS。 |
| SIA-R1-G09 | AB-9：無分配 | first-run `:104`、`:152`；最小知識庫／詞彙表與 Planner 實際使用檢索出處的 Demo（G-KB）尚缺。DA derive；公路／地標選擇、老師對知識庫深度的確認由 **acceptor**；C-1 的真實執行額度仍 **acceptor**，目前 BLOCKED。不新增進階 RAG 要求。 |
| SIA-R1-G10 | AB-10：三 Spec 各部分 NFR | first-run `:105`；其他模組 NFR1～NFR5、PlanResult／LLM 的裁切／來源追溯與 upstream 公開地標保證尚缺分配。DA 明列於 G-RREQ／G-RTE／G-SRC／G-VAL／G-PLN／G-APP 等相應 Spec；真實資料核對須 **acceptor RB-7**。現有 index gate 0 不等於這些產品路徑已驗證。 |
| SIA-R1-G11 | AB-11：B1 產品凍結＋R1 strict | first-run `:106`、`:154`～`:156`；E1 Lite／E2 程式、分析計畫、題庫、Oracle、Runner、清單格式／凍結 evidence 未分配（G-E1、G-E2；G-REG 的真實停等回歸仍未授權）。DA derive；資料／正式執行／Pilot 支出按 **acceptor** 的 RB-7／RB-4／OC-1 §4.2；不將正式研究執行結果增列為 AB-11 的完成條件。 |
| SIA-R1-G12 | AB-12：無分配 | first-run `:107`、`:157`；G-DOC 尚未 derive，Installation／How to Run 的實跑及 Architecture／Flowchart／Pseudocode／Results 對照缺 evidence。DA 依實作 derive 並納 RV 清單；本 audit 不代改 DESIGN／README，也不將舊狀態文字當現況。 |
| SIA-R1-G13 | AB-13：三 Spec 各自 gates | first-run `:108`；其餘 derived Specs 尚不存在，其 pytest／SIA／phase acceptance 與最後 release gate 沒有完整分配。本 Spec 的 F1 與未 phase acceptance 也使累積狀態未完成。DA 補齊各 Spec／最後 gate 的承載與 traceability；release／push／PR／merge 仍 **acceptor RB-1**，沒有因本 gate 檢查獲授權。 |

G-CON、G-ING、G-RREQ、G-RTE、G-SRC、G-VAL、G-PLN、G-KB、G-APP、G-E1、G-E2、G-REG、G-DOC **全部仍 open／未 ready 或尚未 derive**；沒有哪一項因 B1／UI0 phase acceptance 或本次 synthetic suite 而被默認填滿。G-CON 的 Plan Schema 也不是本次 contracts v0.3 已驗證的四份資料契約。

## Implementation／evidence finding

### SIA-R1-F1 — 缺少 SR1-AC2 所要求的跨 Ticket 契約整合測試

- **Severity：Medium／blocking。Owner：SPEC-R1 整合 rework 的 Executor；Orchestrator 依治理 §4.4 派工。**
- **契約**：`derivation-spec-r1.md:145` 明列一般模式首次呼叫並存放、再次重用、Snapshot Mode、strict、target GPX 單向／來回，都經 R1-4 共用介面，而且輸出的 route_id／snapshot_id／checkpoint_id 通過 R1-1 契約檢查，RS hex 等於 SN hex。治理 §3.8／§4.7 要求適用的整合驗證，單票 PASS 不充分。
- **證據**：`tests/test_routing_engine.py:1699` 只呼叫一次 `plan(round_trip_engine(), store)`，assert RS／SN 的 regex 與 hex；沒有 checkpoint 或 R1-1 validator。一般重用 `:493`、Snapshot Mode `:1438`、strict `:1452`、target passthrough `:1618` 都各有行為斷言，沒有契約串接。`tests/test_contracts.py:850` 起的 ID tests 使用手寫 HEX_A／HEX_B，沒有取得 get_route 輸出；無法建立另一半的連線。全 tests 的 AST／文字核對與 imports／實際函式閱讀相符，並非只按測試名稱推論。
- **影響**：目前 2238 passed 仍不能證明 SR1-AC2，不能證明 R1-4 各模式的真實 IDs 與契約 2 的來源／references／checkpoint 前綴約束一起相容。這是 accepted AC 缺 evidence，不是要求提前實作 G-RTE。
- **Required fix**：加入可由 pytest 收集的整合測試，覆蓋上述各模式；使用 get_route 真正回傳的 IDs、trip type、來源與 snapshot reference，驗證首次 store／再用與 Snapshot／strict 不發引擎請求；GPX 至少含單向與來回、騎士指定兩點間折返的 passthrough。使用最小合成的契約資料承載相應 checkpoint_id，經 R1-1 的契約驗證函式（包括 checkpoint 前綴、來源 references、RS／SN hex 一致）並實質斷言無違反。若以參數化／共用 assertion 實現，所有列須實際走驗證。保持 G-RTE 的產生／編號規則為排除範圍，不藉此修改產品 catalog；若需變更契約語義交 DA。補記整合 evidence，重新執行完整 suite／CLI，交本 SIA cycle 1 R2 核對 closure 與 regression。

### SIA-R1-N1 — #16 的平台未驗證項目沒有具名 owner

- **Severity：Low／non-blocking。**
- **證據／依據**：`worklog/issue-16.md:891`，§15.4 的 NV-PY 在 Owner／required authority 欄為 `—`；run `:352` 亦只說 Python 3.13 以後 NOT RUN。#16 R2 的 NV-PY 寫「之後的平台驗證」，仍非具名 owner。治理 §3.7 的 remaining-work／handoff 應能追溯負責者與下一步；本次 pack 另明令核對所有 NOT VERIFIED 項目的 owners。
- **Disposition**：保留 NOT RUN，不要求本 cycle 安裝 Python 或擴張平台測試。**Owner＝Orchestrator（補登／routing）；required authority＝Design Authority（確認支援／verification scope），後續執行者由合法派工具名**。只有實際需要改環境權限時才交 acceptor，不臨時新增 approval gate。
- **Required fix／follow-up**：下次更新 run／worklog 時補 owner、scope 與 evidence 建立位置，併同 #14 NV-PY313 的既有安排；不得把替身的版本無關邏輯說成已實跑 3.13+。不延長目前 cycle。實際 routing NOT RUN。

## Tracked items、已知限制與 NOT VERIFIED 的承接

以下按既有 authority 承接，不因本 record 而新授權執行。除 N1 的具名缺漏外，四票的 open items 可在結案 worklog、DA record 與 run §8.1 找到 owner／authority。舊 audit 的 integration NOT VERIFIED 只在本次確有 evidence 的部分解除；F1 與之後產品整合保持 open。

| Item | 狀態／範圍 | Owner／required authority／disposition |
| --- | --- | --- |
| #13 C-13-3／NV-ACCESS | 歷史 experiments 搜尋揭露；未在本 worktree 重查外部 transcript，**NOT VERIFIED**。不據此宣稱私有資料外洩，也不說已獨立清查全部存取。 | Orchestrator／dispatcher（原 run 事件 61 與後續 binding 核對）。 |
| #13 C-13-6／NV-EXP | experiments 中 build_route 呼叫者的實際行為 **NOT VERIFIED／NOT RUN**；本次未執行。 | 之後執行該腳本的 work item；需要私有資料時 **acceptor RB-7**。 |
| TI-C13-2；C-13-7 | trip_id／datetime 舊 pattern 未收緊；不可 hash 的 ID 在舊 validator 集合檢查的 TypeError 維持既有 tracked concern，沒有新 integration evidence 顯示本次正常 IDs 觸發它。 | **DA**，後續 contracts derivation；不重開原 Ticket findings、不宣稱已修復。 |
| RV-6、RV-7 | v0.3 實作狀態與 ID 文字尚未同步。 | **DA**，AB-12；最早 phase acceptance 後的文件工作。 |
| C-14-6／R1-N1 | 歷史與 worklog 的手寫範例座標公開前處置未決；現行測試改近零合成值。只記其來源主張，不另輸出數值，也不假定是私有騎乘資料。 | **acceptor RB-6**；沿原 Low disposition。沒有改寫歷史。 |
| TI-C14-1 | 詞彙表座標定義物件的 float 型別與整數轉換未完成。 | **DA**，G-RREQ／詞彙表。 |
| TI-C14-5；RV-8～RV-10 | FrozenEntry 與凍結清單檔案格式的對應、取位／取整／store 錯誤文字尚未涵蓋。 | **DA**，E2／凍結 Demo 與 AB-12。 |
| NV-PY313／NV-PY | Python 3.13+／其他平台實跑 **NOT RUN**；只實跑本 worktree Python 3.11.2。CL-R1-20 的明確 stat 與替身證明邏輯，不等於跨版本 evidence。 | Orchestrator 安排合法派工的 Executor；契約 scope **DA**；#16 具名補登見 N1。 |
| NV-SYMLINK | 真實失效／循環連結 **NOT RUN**，既有 worklog 記權限不足，本次未探測；ENOENT／ELOOP 替身已測。 | 後續受派 Executor；Orchestrator 安排；契約 **DA**，需要權限變更時 **acceptor**。 |
| TI-C15-1；RV-11 | 騎士指定位置與實際 c_k 的顯示、GPX 分界文字尚未涵蓋。 | **DA**，之後整合 Spec／AB-12。 |
| CL-R1-22 §2.4 兩項限制 | 稀疏 GPX 的最近可用點可離指定 m 數百公尺；不同分界取同整數公尺可共用 RG ID，幾何差小於 1 m。**未消除，不能記為已涵蓋／已驗證無風險**。 | **DA** 知悉，顯示問題併 TI-C15-1；不自行加入偏移上限或改 identity。 |
| TI-C16-2；RV-12～RV-14 | source.py 已正確記「圖磚最後修改日期」；之後來源證據／UI 的顯示、SPEC／DESIGN 文字同步尚未完成。 | **DA**，整合／文件 Spec；不能稱 OSM 擷取日期或已確認最新。 |
| TI-C16-3；TI-C165-1 | request_key 地點與每方向 positions 一致性的上游核對、ref_id／role 合法值與送出前拒絕非法 Unicode 尚未涵蓋。當前 caller ValueError／SnapshotValidationError fail closed 依 DA disposition 接受；不將它說成產品輸入保護完成。 | **DA**，G-RREQ。 |
| TI-C2R1F3-1 | default trust 可受 SSL_CERT_FILE／SSL_CERT_DIR 影響；**OPENSSL_CONF 影響 NOT VERIFIED**。CL-R1-28 消除 keylog 寫檔，不消除此信任來源限制；不宣稱傳輸層完全不受環境變數影響。 | **DA**，SIA 確認列入（本列）與後續文件 Spec；本次不另改安全策略。 |
| NV-1／RV-5 | 真實 Valhalla 連線／TLS／redirect／回應形狀（via 是否單 leg、warnings 位置、trace／status 欄位）、異常值與五條參考路線、詞彙表 landmark 偏移 **NOT RUN／NOT VERIFIED**。 | **acceptor** 決定真實請求授權；之後合法整合 work item 執行。沒有因 synthetic tests 放寬 CL-R1-27。 |
| NV-PRIV／NV-PRIVATE | 真實 GPX、holdout、住家位置、部署 store 路徑、heuristic 真實表現／裁切／錨點外送 **NOT VERIFIED**；沒有授權或取得資料。 | **acceptor RB-7**。不得由合成資料外推；G-REG／G-ING 的私有雜湊需求同樣保留。 |
| #15 `efbffe8` commit message | 第一行前綴格式偏離；run 事件 85 已揭露；沒有改寫。 | **acceptor** 決定歷史處置（RB-6）；不延長本 cycle。 |
| NV-BIND（本次） | 本次 SIA dispatch／binding 事件尚未在受審 run 中。**NOT VERIFIED，採用前必要**。先前四票 dispatch 的 binding 已在事件 66／78／86／106 補登，不將其誤列為仍缺，也不代用本次。 | **dispatcher／Orchestrator**：補記本次 thread、全部 turn_context 集合、存取／唯一新檔／作者事件、原樣收錄 hash，再判斷 formal binding 有效；Reviewer 不讀 worktree 外 rollout。 |
| NV-MUT | 外部 scratchpad mutation logs 未讀／未原樣重跑；本次沒作 source mutation。 | 本 Reviewer 限定本次 evidence 的範圍；Executor claims 不冒充 independent execution，不另創工作。 |

SPEC-R1 §6 的 known-not-covered 清單逐項維持：真實參考路線、詞彙表、請求解析、路線目錄／檢查點產生／ridden_share_pct、RouteSummary 與 RouteError message／actions；另維持 CL-R1-22 的兩項限制、CLI／UI／PlanResult／LLM 整合與凍結清單／E2 Runner 尚未覆蓋。F1 只要求測試層的合成契約承載，不會把上述排除項改記為已實作。

本 record 不作 DA phase acceptance、OC-1 completion、run completion 或 release 決定。F1 的契約內 rework 可依既有治理流程推進；G01～G13 的設計 routing、N1 的補登與所有保留權限由上述 authority 處理。**真實 routing／DA 派工請求均 NOT RUN**；只在本 record 提出所需 authority，沒有虛報已派工或已接受。

交付核對：寫入後 `git status --short` 只有 `?? docs/governance/records/audit/spec-SPEC-R1-c1-r1.md`；`git diff --exit-code` 為 exit 0，追蹤中的檔案未改。stdin Python 確認五個 §4.7 範圍、五條 AC、13 列分配缺口與末行 verdict 都存在；首次以管線中文字面值比對 heading 的 False 經 Unicode escape 比對確認是命令文字編碼問題，文件五個範圍並未缺漏。

Verdict: BLOCKING
