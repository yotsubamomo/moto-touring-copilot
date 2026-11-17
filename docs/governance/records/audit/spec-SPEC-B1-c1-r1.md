# SPEC-B1 — Spec Integration Audit，cycle 1 R1

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`；acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md` §2、§4–§7，加上適用 CL-B1-8～15 與 #9 FA ruling）→ Issues #7、#9、#10、#11、#8 |
| Subject BASE | `ff049661f968adace4dd017cf560316e5684440d`（#7 開始前） |
| Subject HEAD | `a6f78f8f112c9a2af310452c21903c1683371b97`；本 dedicated worktree 的 detached HEAD |
| Audit kind | **Spec Integration Audit of SPEC-B1, R1, cycle 1 (not a Ticket audit)**；獨立 audit instance，不是任何 Ticket 的 R3 |
| Role／作者 | `primary_reviewer`，Codex；本 record 由 Reviewer 自行撰寫 |
| Dispatch | `docs/governance/records/run/run-20261117-oc1-run2.md:117`，§6 **事件 38** |
| 日期 | 2026-11-18 |
| 結論 | 一項 **Medium／blocking**：SIA-R1-F1，SB1-AC2 所要求的單一完整整合測試不存在於 subject；其他五項 SB1-AC 判為 PASS |

## Assurance：independence 與 models

| (a) 四項 independence properties | (b) 實際 models 與 binding evidence |
| --- | --- |
| **Independent context**：本次為 fresh Codex thread，沒有繼承 Executor 或各 Ticket Reviewer 的對話、推理。自行從契約、原始碼、測試、git diff／log 形成判斷；正式 worklogs 與既有 audits 可讀，但其完成敘述均為待核對主張。沒有派 subagent。 | Executor #7：前一 run `run-20261117-oc1-issue7.md` §5 事件 2、8 記載 `claude-opus-5-5`／`high`，初次 120 則、correction 後共 158 則。 |
| **Verifiable binding**：Bindings m3 O-6／§3.3，qualification 見 §8.2 #7。本次 binding 的持久承載位置為 run2 §6 **事件 38**。受審 HEAD 的事件仍為「進行中」；dispatcher 須在採用本 record 前核對全部 rollout `turn_context` 的 model／effort／sandbox、存取紀錄、作者事件與原樣回傳 hash，回填該事件。本 record 不把派工 mapping 當作已完成的 runtime 觀測。 | Executor #9、#10、#11、#8：run2 §6 事件 18、28、32、36 分別記載同一 Ticket 最後的 Executor binding，觀測 205、191、98、98 則，均為 (`claude-opus-5-5`, `high`)。初次 implementation binding 另見事件 2、20、30、34；#10 修正見事件 24、26。這些是本 worktree 內的 dispatcher evidence，未存取外部 transcript。 |
| **Autonomous access**：自主讀取本 worktree 內的治理、原始契約、最終產物、歷史、測試與合成 fixture，自行執行 PATH 的 Python 及必要探測。pack 是入口，沒有作為 coverage 上限。首次 pytest 的預設暫存目錄探查被 sandbox 拒絕，詳見命令紀錄；其後 pytest 暫存明確限定於 worktree。 | Primary：本作者是 **Codex**。事件 38 指定 `gpt-6.1-sol`／`high`，Bindings 要求 `workspace-write`；本次實際 runtime 的完整 binding 核對仍由 dispatcher 完成。沒有讀取 worktree 外 rollout 或任何 credential。 |
| **Self-written record**：唯一新增的交付檔案是本檔；未修改 implementation、tests、contracts、gates、worklogs、既有 audits 或 run record，未 stage／commit。dispatcher 依 Bindings §3.3 原樣接收並核對 SHA-256，不代寫或改寫結論。 | **no model diversity claim**。Bindings §5 沒有宣告 D1–D4；不以模型產品名稱或預定 mapping 推定 diversity。當次 binding eligibility 不由 implementation verdict 取代。 |

## Finding

### SIA-R1-F1 — 缺少 SB1-AC2 要求的 ingest → user pace table → ETA 單一整合測試

- **Severity：Medium；blocking。** 明確的 Spec verification contract 未滿足，不是要求擴張功能。依據為 `derivation-spec-b1.md:109`（SB1-AC2）、治理 §3.8 的跨 Ticket 整合驗證及 §4.7 的 Spec-level AC coverage。555 個測試通過不能取代缺少的驗收案例。
- **證據：**`tests/test_eta.py:271` 的 `test_eta_from_a_pace_table_built_from_derived_segments` 從 `trips_three_categories` 取得手工衍生列；其產生器 `tests/test_pace_table.py:37` 呼叫 `seg`（`:27`）直接建 dict，`ingest_version` 為 `ingest-test`，沒有 TrackPoint 軌跡或 `build_rows`。它有 matching `category_scheme`、`user-02`、配速表 → ETA 及契約 4 檢查，但沒有 ingest，也沒有 1 秒假停留、短停留、長停留經 ingest 後連到同一份配速表的證據。
- **其他候選仍不充分：**`tests/test_routes_pace_eta.py:122` 以 mock fixture 建表、`:151` 的 `eta_for` 直接使用 fixture 自帶配速表；兩者沒有串接 ingest 的輸出。`tests/test_ingest.py:193`、`:211`、`:234` 驗證停等與契約 1，但未將結果送進配速表及 ETA。全 `tests/` 的 producer／validator 呼叫搜尋、AST 檢查與 helper 來源閱讀，沒有找到其他完整鏈路；`tests/conftest.py` 也只有 mock fixture，沒有補足該鏈。
- **不是重開 Ticket finding：**各 Ticket 已關閉，#11 的 R1 明確不是 SIA；本 finding 對象為整合後 subject 的 Spec AC。`worklog/issue-11.md:161`、`:206` 也把完整鏈路留給 Spec 層；此敘述只是佐證，缺漏判斷來自測試原始碼。
- **Required fix／owner：**由 **#11 Executor** 在同一 worklog identity 下作 SPEC-B1 integration targeted correction（Orchestrator 依 orch-default §6 派工）：新增一個可由 pytest 收集、留在 subject 中的合成整合測試。一條軌跡須含 1 秒重複位置、短停留、長停留，實際經 ingest 產生契約 1 合格列；以多趟合成行程建立 `user-` 配速表並帶衍生列通過契約 3；在明確 matching `category_scheme` 的合成路線上計算 **ok ETA**，帶入同一份 pace header／categories 通過契約 4，實際涵蓋 invariants 8、9。保留停等分類與時間傳遞的實質斷言，避免 unknown 全 null 的案例讓算式檢查落空；重跑完整 suite、`-rxX` 及標記搜尋，更新 worklog 的整合 evidence，識別修正後 subject 供本 SIA 的 R2 closure review。
- 本次 reviewer-only 記憶體探測通過（下文），但沒有把測試加進 subject，**不能關閉本 finding**。不需新增設計語義或 acceptor approval；不要求實作 RI-1～RI-3 或使用真實 GPX。

新增 non-blocking findings：**無**，所以沒有新增 disposition／owner。既有 #7 R2-F1、#9 C2-R2-N1 等 tracked items 維持其原 record 的 disposition；本 audit 沒有新 integration-level evidence 推翻其 closure，不重複列為新 finding。

## 範圍與取證方式

依 root `CLAUDE.md`、Bindings m3（含 §1 生效 package、O-6、§5／§7）、`.claude/agents/gov-primary-reviewer.md`，及有效 package 的治理 §2.3、§3.8、§4.1–§4.7、impl-default v2 §6–§7、orch-default v2.2 §6–§7 執行。最後一行採本次明確 dispatch 指定的 `Verdict: ...` 格式。

契約閱讀包括 OC-1 §2／§3.1／§4／§6／接受紀錄、first-run derivation 的 BD 與 G-* 分工、SPEC-B1 §2／§4–§7、DESIGN §5／§6.1／§9 的相關段落、SPEC-RESOLUTION-001 的停等／ETA／規則 3 定義、SPEC-001 4.8／5.2／5.4 的引用部分、G1 Q18、BATCH-1 共通規則／依賴圖。另讀 CL-B1-8 的 Spike tests 裁決、#7 H-2 補標、CL-B1-9／10、#9 FA ruling、CL-B1-11、CL-B1-12～14、CL-B1-15／CL-R1-11 的邊界。各 Ticket worklog 的 AC mapping、E-3／E-4／E-5、修正與結案 follow-ups，與原始 audits／run records 交叉核對。

Issue bodies 採本次 pack 的原文版本，所附 SHA-256 與 first-run derivation BD-3 一致；沒有向 GitHub 重新取得。`git diff 873e37a..HEAD -- DESIGN.md docs/spec/SPEC-001-plan-schema.md docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md docs/grill/g1-grill-input.md docs/ticket/BATCH-1-scoped-tickets.md` 無差異，引用來源沒有被本次工作改寫。

### 自行執行的 checks 與結果

所有 shell commands 的 cwd 均為本 worktree。使用 PATH 的 Python **3.11.2**，沒有使用 `.venv`、網路、GitHub 或 `experiments/` 腳本。`python -B -` 表示 PowerShell here-string 經 stdin 執行，不新增探測腳本。Git 的禁止路徑 gate 只處理 index path 字串並輸出計數，不列出／讀取 `data/` 內容。

| 指令／檢查 | 實際結果 |
| --- | --- |
| `git status --short`；`git rev-parse HEAD`；`git log --oneline ff04966..a6f78f8` | 開始乾淨；HEAD 等於指定完整 SHA；歷史吻合 pack 的 implementation commits 及 record-only commits。交付前再核對唯一新增檔為本 record |
| `git diff --stat ff04966..a6f78f8`；`git diff --name-only ff04966..a6f78f8 -- src tests` | 41 files，9471 insertions／152 deletions；16 個 src／test／fixture paths。其餘全部為 `docs/governance/records/**` |
| `git diff ff04966..a6f78f8 -- src tests`；`git diff ff04966..a6f78f8`（亦以 Python `subprocess.check_output` 取得完整內容） | src/tests diff 4025 行；全 diff 10296 行。分檔閱讀實作、測試／fixture delta、records 的裁決、evidence、closure 與 follow-ups；沒有把過長工具輸出當成完整可見證據 |
| **`python -m pytest -q`，首次預設環境** | **exit 1：458 passed, 97 errors in 31.21s**。97 項為 `tmp_path` setup 的 `PermissionError`：pytest 嘗試探查 worktree 外預設暫存目錄，被 sandbox 拒絕。命令已自行結束；後續送出的 Ctrl-C 沒有改變該結果。這不是測試斷言失敗，仍保留失敗紀錄；dispatcher 應連同本次存取紀錄核對，不宣稱該次沒有外部暫存探查 |
| **`$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/sia-q'; python -m pytest -q`** | **exit 0：555 passed in 2.20s**；暫存位於 worktree 的 git-ignored cache |
| **`$env:PYTEST_ADDOPTS='--basetemp=.pytest_cache/sia-rx'; python -m pytest -q -rxX`** | **exit 0：555 passed in 2.56s**；沒有 xfailed／xpassed／skipped／errors |
| **`rg` 標記搜尋**（實際 regex alternation 命令見下方） | **exit 1，無 matches**；兩個 pattern 的結果相同。CL-B1-8 Spec-level 恢復要求已滿足 |
| **`$env:PYTHONPATH='src'; python -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`** | **exit 0**；`derived_segments: OK`、`route_catalog: OK`、`pace_table: OK`、`eta_output: OK`。標題 `data contracts v0.2` 符合 CL-B1-2：這不是宣稱完整 v0.3 已完成 |
| `rg` 對 `tests/` 的 ingest／build／ETA／validate 呼叫搜尋；`python -B -` AST producer 呼叫及 validator imports；閱讀 helpers／conftest | 只有 `test_eta.py`、`test_routes_pace_eta.py` 呼叫 compute_eta，均未將 ingest output 接入；F1 的缺漏證據。validator imports 僅 `__future__`、math、fractions、typing 與自身 `.rule3`，沒有 pace、planner、LLM 或其他第三方模組 |
| `python -B -` reviewer-only 完整合成鏈路（下節詳述） | exit 0；3 trips／27 rows；契約 1／3／4 空 violations，ok ETA，invariants 8／9 及休息只平移時間的 assertions 通過。不是 tracked pytest integration test |
| `python -B -` 讀五份最後 closure records、計算 `git show HEAD:<audit record>` 的 SHA-256，與兩份 run records 內文比對 | 五份最後一行均為 `Verdict: PASS`；五個 Git-blob hashes 都存在於對應 run record，包含 #9 cycle 2 R2，沒有誤採 cycle 1 的 blocking record |
| `git diff --name-only <最後 implementation>..HEAD -- <對應 src/tests paths>`（由 Python 逐組執行） | contracts／test_contracts 自 e4fc93b、ingest／test_ingest／CLI tests 自 5f9a35e、test_pace_table 自 e4fc93b、pace／ETA／routes_pace_eta tests 自 41c848b、validator／rule3 tests 自 47f1cdb，全部無差異 |
| `python -B -` fixture BASE／HEAD 比較與獨立 stop_ratio 重算 | routes、route_segments、checkpoints、private_start_times 全部未變；沒有新增真實座標／時間。fixture C1／C2／C3 ratios 分別為 0、12/(64+96)=0.075、null；與 fixture 相同。ETA 重算另由 fixture reproduction tests 及 contract CLI 核對 |
| `python -B -`：`git ls-files -z` 禁止 pattern 計數；完整 diff 新增行的有界 credential pattern 檢查 | `.env`、GPX、FIT、任何 `data/`、`*.key` 計數各 **0**；長 `sk-ant-` 值與 private-key header patterns 各 **0**。不宣稱這兩個 patterns 能辨識所有秘密形式 |
| 完整 diff 新增行用語掃描，另以 `python -B -` 搜尋 source/tests 的 P90／percentile／百分位／分位數／官方警特報／official warning | source/tests 僅兩個否定句：`pace/table.py:7` 的「not a P90」、`validator/rule3.py:6` 的「not an official weather warning」。records 是規則、排除、歷史引用及 NOT RUN／NOT VERIFIED 的陳述；未發現新增正面能力宣稱。第一次 inline script 在中文 regex 因 PowerShell stdin encoding 變成問號而報 `re.error`，後半 AST／claim checks 沒有執行；設定 UTF-8 `$OutputEncoding` 後完整重跑成功，不採用失敗腳本未執行部分為證據 |

標記搜尋的原樣命令（沒有將 regex 的 alternation 符號跳脫）：

```powershell
rg -n 'xfail|skip|CL-B1-8' tests/
rg -n 'xfail|skip|CL-B1-8|decision-20261117-issue7-spike-tests' tests/
```

### Reviewer-only 整合行為探測

以 `runpy.run_path('tests/test_ingest.py')` 取得 `ride_with_stops`，建立 T901～T903 三趟純合成軌跡，每趟 waits 為 `[1, 30, 180]` 秒。實際呼叫 `build_rows`／`to_public`，不是手工填衍生欄位。各趟 report 為 false／short／long = 1／1／1；short 總秒數 30、stopped 總秒數 210；與 `[0,0,0]` 對照軌跡相比 moving 多 1 秒、各段 length 不變，所有列 quality 為 ok。

將共 27 列送入 `build_pace_table(... pace_version='user-01', min_segments=2)`，得到 `curv-tercile-0-0`、0.20／default、C1／C2／C3 counts = 0／0／27。獨立核對 stop_ratio 等於 short／moving 總和。由 `tests/test_eta.py` 的合成 catalog 取 R05 的幾何佔位／檢查點，明確將路段類別設 C3、路線 scheme 設成同一 `curv-tercile-0-0`；沒有呼叫 `routes` 重分類。

分別無休息／在 waypoint 後加 900 秒休息呼叫 compute_eta。每次 validate_dataset 的四組 violations 皆為空；ETA status 為 ok、header margin 等於 pace header，逐列獨立斷言 allowance 比例、typ cumulative、safe margin（容許 1 秒），兩次輸出的 allowance 不變，typ／safe 各只平移累計休息長度。實際輸出：

```text
reviewer-only in-memory synthetic chain: PASS; trips=3; rows=27; per-trip stops false/short/long=1/1/1; contracts 1/3/4 empty violations
scheme=curv-tercile-0-0; margin=0.2/default; counts=[0, 0, 27]
matching synthetic route: ok ETA with/without 900s break; invariant 8/9 and break-only shift assertions PASS
This probe is not a tracked integration test in the subject and does not satisfy the SB1-AC2 test-artifact requirement.
```

這是目前組合可運作的一個有界 synthetic observation，沒有證明真實騎乘表現、其他曲率分布或 RI-1～RI-3。SB1-AC2 明文要求「以一個整合測試表現」；Reviewer 不得修改 tests，故此探測沒有修復 subject 的驗收產物缺漏。

## §4.7 scope 1：跨 Ticket invariants

| 跨 Ticket 關係 | 最終 subject 的核對與結論 |
| --- | --- |
| #9 ingest → #7 契約 1 | `segments.py:209` 的事件分類／分配、`:303` 之後的假停留加 moving／short 分欄、`:330` 輸出欄位，與契約 1 short ≤ stopped 一致。`test_ingest.py:193`、`:211`、`:234`、`:312` 覆蓋假停留、3／180 秒邊界、時間守恆、trim boundary；private／public／pair checks 保留並通過 |
| #9 → #10 → #7 契約 3 | `pace/table.py:71` 的 timed_rows 依 CL-B1-12 取合格列，`:126` 依新門檻分組、用 short／moving 比例；`:144` 每折重算門檻／配速，`:194` 同批 trip_ids 產生 margin 與版本追溯欄位。`validate.py:268` 之後依 CL-B1-12 核對總合；scheme 不同時**不逐類別核對**。逐類別正確性由 #10 tests（如 `test_pace_table.py:58`、`:128`、`:163`、`:350`）覆蓋，不能歸功於 validator |
| #10 → #11 → #7 契約 4 | `pace/table.py:374` 先檢查契約 3，`:377` 取 header margin，`:383` 取同表速度／ratio，`:399` 之後按 moving＋allowance 累積；`validate.py:345`、`:398`、`:408` 之後檢查 invariant 9／8。`test_eta.py:102`、`:120`、`:143`、`:181`、`:271` 的公式、break、header 與兩階段連接測試通過 |
| 缺值／資料不足傳遞 | 類別不足時 speed 與 stop_ratio 同為 null；ETA 使用到任何缺配速類別則全份 unknown，不留部分時間（`pace/table.py:385`、`:395`）。`test_eta.py:158` 及 malformed pace table tests、contract tests 皆通過；沒有將缺 ratio 補 0 或缺 margin 補 0.20 |
| #8 規則 3 與 pace 隔離 | `validator/rule3.py:69` 起依範圍分類與 FAIL→UNKNOWN→PASS 優先序，只有標準函式庫；沒有讀取配速表或將 rule 3 PASS 當作整趟無雨。範圍與資料缺漏測試及 import tests 通過 |

上述接口與局部 invariant 證據一致，未發現新的 integration runtime defect；**subject 缺少把第一、二、三列串成同一測試的長鏈回歸保障，見 SIA-R1-F1**。

## §4.7 scope 2：Spec-level AC coverage 與 allocated acceptance boundary

| Spec AC | 證據與判定 |
| --- | --- |
| **SB1-AC1 — PASS** | 五張 Ticket 的最後有效原始 audits 均為 closure；下表列版本。前一 run §7.1、run2 §8.1 各列 P1–P8 已成立，P9 明確留在 phase／SIA 層；不是以 Ticket PASS 冒充整合 PASS。dispatcher 已在 run 事件記錄五份 audits 的 binding／存取／原樣 hash；本次另核對 Git-blob hashes 均存在於 run record。Issue 在線上是否 OPEN 不影響本機治理結案，且本次不查 GitHub |
| **SB1-AC2 — FAIL** | 沒有符合 `derivation-spec-b1.md:109` 的單一整合測試，見 SIA-R1-F1。`test_eta.py:271` 僅為手工衍生列 → 配速表 → ETA；reviewer-only probe 不能充當 subject 中的 pytest 測試 |
| **SB1-AC3 — PASS** | mock dataset contract CLI 四組 OK；兩次限定 worktree 暫存的完整 pytest 為 555 passed；`-rxX` 沒有 xfailed／xpassed，tests 搜尋無 xfail／skip／CL-B1-8 標記。CL-B1-8 §3.2 item 5 的字面要求滿足。CONTRACT_VERSION 保留 0.2 是 CL-B1-2 的明定，不是完整 v0.3 的 PASS |
| **SB1-AC4 — PASS** | `rule3.py:71`、`:78`、`:122`、`:127` 符合單向 strict >80%、來回 index ≥k、FAIL 優先於 UNKNOWN；`test_rule3.py:33`、`:45`、`:69`、`:93`、`:130`、`:154`、`:185`、`:230` 覆蓋判定表與邊界，`:375`、`:382` 的 static／runtime imports tests 通過；自行 AST 核對僅 stdlib／自身 imports，與 pace 無匯入關係 |
| **SB1-AC5 — PASS** | 依 CL-B1-11 §3 item 6 的明確讀法。`ingest/__main__.py:58` 只讀既有 manifest，`:95` 比較角色矛盾，`:162` 起全 pace 名稱檢查＋selected pace link 檢查在任何 GPX read 前執行，`:187` 只選 pace，`:230` 才逐一 read_gpx。沒有自動建立暫定 manifest 的路徑。`test_ingest_cli.py:89`、`:125`、`:201` 及 stream／8.3／hard-link／模擬 symlink／metadata spy／未選 pace 的 tests 保留並全通過；非 pace 端 filesystem 操作沒有新增。CL-B1-11 item 4 的殘餘、TOCTOU 明確不在此 PASS 內 |
| **SB1-AC6 — PASS** | src/tests 新增行僅有兩個禁止用語的否定句，worklogs／records 中是誠信規則、排除與 evidence 限制；未新增把 ETA_safe 當分位數、把本專題提醒當官方警特報的宣稱。沒有把本次合成檢查寫成 E1 Lite／E2 結果 |

SB1-AC1 的逐票核對：

| Ticket | 最後有效 closure record／受審 HEAD | 完成紀錄與最終 coverage |
| --- | --- | --- |
| #7 | `audit/issue-7-c1-r2.md`，96b15cd，PASS | 前一 run §7.1 P1–P9／§7.2；run §5 事件 9 binding 已補齊。實作最後 8981e9d；後續契約 delta 由 #10 的 R1／R2（含 CL-B1-15）審查，本次全 suite 重驗 |
| #9 | `audit/issue-9-c2-r2.md`，7f2fee6，PASS | run2 §8.1 #9／事件 17–19；FA 授權 cycle 2 的實質改變與 CL-B1-11 已納入；最後實作 5f9a35e，此後對應 src/tests 無差異 |
| #10 | `audit/issue-10-c1-r2.md`，8177015，PASS | run2 §8.1 #10／事件 27–29；R1-F1／F2 resolved，CL-B1-15 delta 已獨立審查；最後相關 contracts／table tests 為 e4fc93b，後續 ETA delta 由 #11 審查 |
| #11 | `audit/issue-11-c1-r1.md`，bf8a8e3，PASS | run2 §8.1 #11／事件 31–33；最後實作 41c848b，此後 pace／ETA tests 無差異 |
| #8 | `audit/issue-8-c1-r1.md`，22f7e2a，PASS | run2 §8.1 #8／事件 35–37；最後實作 47f1cdb，此後 validator／rule3 tests 無差異 |

**AC 集合的涵蓋判斷：**SB1-AC1 引用 §5 的 Ticket AC／clarifications，SB1-AC2 補完整鏈路，AC3–6 補全域契約、隔離、語義與用語；連同 §7 明列的治理完成 gates，對 allocated boundary 的功能與 verification 要求有對應，未發現需另行 derive 的分配缺口。這是 coverage 設計的判斷，**不表示全部已實現**：AC2 已 FAIL，AB-13 的 SIA closure／DA acceptance 尚未成立。

| §7 分配 | Spec AC／驗證對應與完成界線 |
| --- | --- |
| **AB-3 計算核心** | AC1 的 #9 停等分類、#10 user 建立／選用；AC2 串接核心。現有 producer tests 與版本 tests 通過；AC2 evidence 缺口阻擋 Spec 整體 closure。沒有涵蓋上傳／合併／去重複／涵蓋度摘要／UI |
| **AB-4 ETA 計算與程式用語** | AC1 的 #7／#10／#11、AC2、AC3、AC6；公式與 margin／break 測試通過，完整 tracked 鏈路仍缺。介面／交付文件措辭屬後續 Spec |
| **AB-7 規則 3 範圍與三值** | AC1 的 #8、AC4，已具測試與 import evidence。不涵蓋原因代碼、RuleResult、其他規則 |
| **AB-10 此 Spec 的 NFR2／NFR4／隔離部分** | AC1 的 public/private allowlist、unknown、pace role gates；AC3 mock／全 suite、AC5 隔離。合成來源可追溯；真實私有資料隔離／揭露程度 NOT VERIFIED，不將 G-ING 殘餘計入 |
| **AB-11 產品端 freeze 機制部分** | AC1 的 #10 版本分離／不覆寫、#9／#10 role refusal，加 AC5。只涵蓋這些產品端機制；沒有 freeze manifest 或 E1／E2 script version checks |
| **AB-13 本 Spec 整合完成** | AC1／AC3 的 Ticket closure／pytest 已有證據；本 SIA 依治理 §4.7 判定，phase acceptance 依 orch-default §7 P10 由 DA 在 SIA closure 後作成。這兩個是明定後續 gates，不能由 AC3 PASS 推論完成；目前因 F1，SIA 未 closure、DA phase acceptance 尚不能進行 |

SPEC-UI0、SPEC-R1 仍 open；本次不是 OC-1 最後一份未結 Spec，**不執行全部 derived Specs 分配合計的最終 allocation check**，也不宣告 OC-1 或任何完整 AB 已完成。

## §4.7 scope 3：整合行為

最終 subject 的三類行為分開判定：

1. **已直接驗證：**契約 1 的短停留輸出／配速取列、配速表 → ETA（matching scheme）、休息不乘 margin、缺類別全份 unknown、規則 3 純函式與其他模組的隔離。全部 suite、原始碼與 reviewer-only probe 支持這些有界結論。
2. **未由 subject 中測試閉合：**完整 ingest → user pace → matching-route ETA 的單一可持續驗證案例。個別 Ticket PASS 不能相加成 SB1-AC2 PASS；F1 是本 scope 的 blocking 結論。
3. **明確排除：**RI-1～RI-3 的不同 scheme 路線重建／拒絕，仍在 `compute_eta` docstring 明列未檢查；本 probe 自行提供 matching 合成契約 2 紀錄，沒有以 `routes` 的 Spike 目錄冒充已處理更新。上游產生 rule 3 的 k／forecast classes、WeatherSegment／RuleResult、完整 Planner／Validator workflow 也沒有在本 Spec 驗收。

## §4.7 scope 4：最終 subject 的 verification／audit coverage

implementation 歷史為 #7 a304ee2／8981e9d、#9 a281cb0／b4d1f84／6f97561／49f1d80／5f9a35e、#10 be0074d／e0f6c78／93e52b8／e4fc93b、#11 41c848b、#8 47f1cdb；其餘 delta 為 record-only。各最後閉合 subject 與 HEAD 的對應檔案差異核對結果見 checks；#10 審查了 #7 後的 contracts delta，#11 審查了 #10 後的 pace delta，沒有未經 Ticket review 的額外產品變更。

因此各 Ticket 原 coverage 的 identity 可追溯，最終 HEAD 也已由本次 555 passed 重新驗證。仍不能宣告 Spec-level coverage 完整：完整鏈路測試缺少，F1 必須修正並識別新 HEAD，再依 §3.8／本 SIA R2 做 closure／regression 核對。run2 事件 38 的 runtime binding／作者核對由 dispatcher 完成後，本 record 才能作正式採用依據；本 record 不自行修改 run 或宣告 phase acceptance。

## §4.7 scope 5：traceability 與 Outcome Contract boundary conformance

OC-1 §2.1 第 1 項的 ingest／pace／validator／tests、第 2 項契約更新、第 3 項 Spike 收編，對應 SPEC-B1 §1／§2／§5 的五張 Tickets，並經 §7 分配到上表六項 AB 的限定部分。引用 Issue bodies 與 BD-3 相符；後續 CL records 均有明確範圍與 boundary determination。#10 的 `validate.py` 範圍擴充有 CL-B1-12／15 依據，沒有由 Executor 擅自擴張 #7；#9 alias／metadata 分工有 FA ruling 與 CL-B1-11 依據。

本次看見的最終變更符合這條 traceability 鏈，沒有新增 Must、恢復 Scope Reduction、改寫凍結基線、觸及保留操作或改變 accepted Outcome 語義的證據。沒有新的 boundary ambiguity 需交 DA；F1 是已寫定的 verification contract 缺漏，route Orchestrator → Executor targeted correction。若對此 finding 的證據／blocking 有實質爭議，依治理 §4.3–§4.5 路由，不由 Executor 或 Orchestrator 降級。

## 整合層高風險核對（high-risk record §5）

| 類別 | 本次最低核對範圍、證據與限制 |
| --- | --- |
| **H-2 私有資料** | #7 依 H-2 補標 record 納入。tracked 禁止路徑計數皆 0，有界秘密 pattern 皆 0；fixture 的 coordinates／private_start_times 未改，新數字可由 mock 值重算。ingest tests 的軌跡來自 `at`／`straight`／`ride_with_stops` 的明確合成生成器；CLI tests 的 GPX 亦為合成；pace／ETA tests 是手工 round numbers／佔位座標，rule3 只有距離／分類。public schema 只新增 numeric short_stop_time_s、仍拒絕 start_time／多餘欄位，public/private pair checks 保留。隱私 trim／trim-boundary tests 通過；本 Spec 沒有新增路線請求／第三方呼叫，錨點代換屬 N/A。真實公開列的揭露程度、私有磁碟／manifest 狀態 NOT VERIFIED（acceptor）。首次 pytest 的外部暫存探查及後續 worktree-only 修正已如實記錄，交 dispatcher 存取核對 |
| **H-3 誠信／隔離／版本** | 在 CL-B1-11 定義的範圍內，重建只開 selected pace，所有 pace 名稱矛盾與 selected links 在首個 GPX 前拒絕；非 pace 端只做字串比較。#10 以獨立 research／user 編號、`open('x')` 不覆寫，版本與 built_at 選用 tests 全通過。沒有自動 provisional manifest 路徑。各 Ticket 歷史 xfailed 照其 CL-B1-8／9 規則與 subject 看待，未冒充最終全通過；最終無標記。合成探測不稱實驗結果；用語符合限制；G-ING、G-REG、freeze／E1/E2 checks 不列已覆蓋。F1 防止把局部 PASS 擴張為整個 Spec PASS |
| **H-4 fail-closed** | 取列缺曲率／非法數值／無可計時列時明確 error、不寫 pace file；低於 min_segments 時 speed／ratio null；default margin 是契約的折數規則，有 default／loo_rule tests，沒有因缺欄補值。ETA 使用缺配速類別則全份 unknown；缺 ratio／margin、margin mismatch、路段缺漏／重複皆由 tests 驗 error。contracts 的新增非有限欄位及 CL-B1-15 整數值 float counts tests 通過。規則 3 範圍內缺分類為 UNKNOWN、有提醒則 FAIL，非法輸入為 error，範圍外缺漏不影響結果；import tests 防止引入 pace／Planner 依賴。外部逾時、Planner 改寫、規則 5、路線採用 gates 不屬本 Spec 實作，不能記為本 audit 已驗 |

## NOT VERIFIED／NOT RUN／排除與 required authority

| ID | 項目、原因與處理 |
| --- | --- |
| NV-1 | **真實 GPX／manifest 角色、真實 holdout／excluded 隔離、真實配速／ETA／LOO 表現與公開衍生列揭露程度：NOT VERIFIED。** 需要私有資料，沒有明確路徑授權，不嘗試取得。required authority = **acceptor**（RB-7）；合成 PASS 不適用於真實資料 |
| NV-2 | 真實資料磁碟區的 8.3、hard link／symlink、複本情形：**NOT VERIFIED**；CL-B1-11 item 4 殘餘屬 G-ING，包含非 pace 端別名及同內容不同檔名，沒有當成 SB1-AC5 coverage。owner = Design Authority／Orchestrator 追蹤 G-ING；任何非 pace metadata／內容取得所需 authority = **acceptor**。TOCTOU 依 CL-B1-11 威脅模型排除 |
| NV-3 | **本次 Codex 全程 runtime binding／存取／原樣回傳 hash：NOT VERIFIED by reviewer。** 原始 rollout 不在 worktree，禁止讀取。required authority／核對 owner = **dispatcher／Orchestrator**，在 run2 事件 38 補記，採用本 audit 前完成；連同首次 pytest 暫存探查核對，不以本 verdict 代替 |
| NV-4 | Executor 歷史 mutation scripts／raw stdout 擷取／完整外部操作歷程：**NOT VERIFIED as historical execution**。只讀 worktree 內的正式 records，未存取其中引用的外部路徑。本判斷以原始碼、最終測試及自行探測為據；若需歷史原始證據，由 **Executor／dispatcher** 提供可審材料 |
| NR-1 | RI-1～RI-3、G-REG、freeze manifest／E1／E2 version checks、rule 3 reason codes 與其 schema：**本次排除，未驗證其完成**；後續由 **Design Authority** derive／Orchestrator 派適用工作。G-REG／正式 E1 Lite／E2 與真實資料執行 **NOT RUN**，所需 authority = **acceptor** |
| NR-2 | `contracts/validate.py` 約第 205 行契約 2 count 範圍檢查的 CL-R1-11：屬 **SPEC-R1／#13**，沒有記為 SPEC-B1 已涵蓋。contract CLI 的 route_catalog OK 只表示該 mock 符合現有檢查，不能證明此後續修正已完成。owner = Design Authority／#13 Executor |
| NR-3 | 真實 symlink 建立與額外真實 alias 探測本次 **NOT RUN**；已執行 suite 中的三例真實 hard-link tests、OS 短檔名 lookup test及不依賴特權的模擬 symlink／reparse tests。沒有借用舊 Reviewer 的額外觀測作本次親跑結果，沒有為本 audit 要求額外權限 |
| NR-4 | **SIA closure、DA phase acceptance、OC-1 completion、release：未成立／未執行。** F1 修正後先由本 SIA 的 R2 核對；DA 才能依 closure record 作 phase acceptance。沒有 stage／commit／push／PR／merge，沒有線上 Issue 狀態查詢或變更 |

本 R1 有一項未解 blocking finding（SIA-R1-F1），不得據此將 SPEC-B1 或 allocated AB-13 的整合完成標為 PASS。

Verdict: BLOCKING
