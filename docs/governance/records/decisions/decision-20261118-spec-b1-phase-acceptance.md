# Decision record — SPEC-B1 v1 的 Design Authority phase acceptance

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-spec-b1-phase-acceptance`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | OC-1 第二個 Formal run 的 Orchestrator：`docs/governance/records/run/run-20261117-oc1-run2.md` §6 事件 41（orch-default v2.2 §5「phase acceptance」、§6） |
| Outcome Contract | OC-1（`docs/governance/records/outcome-contract.md`），acceptor 2026-11-17 針對 `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受。之後該檔只有狀態欄與第 10 節接受紀錄的轉錄（`01f3ea4`），條文未變（本次以 `git diff 873e37a..HEAD` 核對） |
| Spec | **SPEC-B1 v1**：`derivation-spec-b1.md`（commit `8c3c588`，至 HEAD 未修改）＋其 clarifications CL-B1-8（`decision-20261117-issue7-spike-tests.md`）、`decision-20261117-issue7-h2.md`、CL-B1-9／10（`decision-20261117-issue9-e1-and-trim.md`）、CL-B1-11（`decision-20261118-issue9-qda1.md`）、CL-B1-12～14（`decision-20261118-issue10-pace-contract.md`）、CL-B1-15（`decision-20261118-issue10-c107.md`）、FA `ruling-20261117-issue9-c1.md`；跨 Spec 決定 `decision-20261117-oc1-first-run-derivation.md`；高風險類別 `decision-20261117-high-risk-categories.md` |
| Tickets | #7（B1-1）、#9（B1-2）、#10（B1-3）、#11（B1-4）、#8（B1-5） |
| 依據的條文 | 治理 §1.2、§2.1、§2.4、§3.8、§4.7、§5.1、§5.3；orch-default v2.2 §5、§6、§7（P1–P10）；Bindings m3 第 2.6、5、7 節 |
| **結論** | **接受（ACCEPT）SPEC-B1 v1 的 phase acceptance**，限第 6 節所列分配範圍與第 8、9 節的限制。不改變 accepted 語義；不是 release authorization，不是 run completion，不是 OC-1 completion，不變更 Issues #7–#11 |

## 1. 問題

依治理 §3.8 與 orch-default §7 P10：SPEC-B1 的五張 Ticket 都已結案、Spec Integration Audit 已 closure 後，SPEC-B1 能否作 phase acceptance——跨 Ticket invariants、整合行為、累積 evidence 與未結 follow-ups 是否足以接受；接受的範圍與限制為何。

## 2. 裁決

**接受。** 理由：

1. **SIA 已 closure（P10 的前半）。** 最後有效的 SIA record `spec-SPEC-B1-c1-r2.md` 為 Reviewer closure（`Verdict: PASS`），唯一 blocking finding SIA-R1-F1 RESOLVED，沒有未解 blocking，沒有新增 finding（第 3 節）。本 record 引用之，不豁免、不取代它。
2. **五張 Ticket 都依 orch-default §7 P1–P8 結案**，P9 留在 phase 層並由 SIA 與 SB1-AC2 的整合測試滿足（第 4 節）。
3. **跨 Ticket invariants 與整合行為**在 SIA 的審查與本 DA 的獨立核對中都成立，限於合成資料與本 Spec 已寫定的範圍（第 5 節）。
4. **SB1-AC1～SB1-AC6 都有 evidence 且判為 PASS**；它們合起來涵蓋 `derivation-spec-b1.md` §7 分配到的 AB 部分（第 6 節）。本 DA 在 HEAD `f38cc50` 重跑的 gates 與 SIA R2 的結果一致。
5. **未結 follow-ups 都有 owner 與 authority，沒有任何一項是 SPEC-B1 Spec AC 的未完成部分**：它們或屬已明列的排除範圍、或屬之後的 Spec／AB-12、或需 acceptor 的 RB-7 授權（第 7、8 節）。沒有影響本 Spec 完成的未決 design ambiguity。
6. 不需要 escalation：phase acceptance 的後果可由現有 evidence 裁決（E-DA/D1 不成立）；本 DA 先前就 SPEC-B1 所作的決定沒有被 FA ruling 或 Reviewer finding 推翻或實質爭議（FA `ruling-20261117-issue9-c1.md` 處理的是 #9 實作的 blocking 爭議，並把 Q-DA-1 route 給 DA，不是推翻 DA 決定；E-DA/D2 不成立）。

## 3. 所引用的 Spec Integration Audit closure record

| 項目 | 內容 |
| --- | --- |
| **Closure record** | `docs/governance/records/audit/spec-SPEC-B1-c1-r2.md` — Spec Integration Audit of SPEC-B1，cycle 1，R2 closure review；`primary_reviewer` Codex 自寫；最後一行 `Verdict: PASS` |
| Closure record 的 SHA-256 | `64ae4911cf5444ce917a1ca4d4eb0116926bcf4f9fafc0c21f98cab94eac6525`（本 DA 以 `git show HEAD:<path> \| sha256sum` 與工作目錄檔案核對，兩者相同，且等於 run2 事件 40 記載的值） |
| **Subject** | BASE `ff049661f968adace4dd017cf560316e5684440d`，HEAD **`a74e683bdcc513a41ab6c7e27411a4633b4c2db9`** |
| 同一 audit instance 的 R1 | `docs/governance/records/audit/spec-SPEC-B1-c1-r1.md`，subject `a6f78f8f112c9a2af310452c21903c1683371b97`，`Verdict: BLOCKING`（SIA-R1-F1 Medium／blocking：缺少 SB1-AC2 的單一整合測試）；SHA-256 `963ab59adaee0d94dce042396291e19a473ba1b435beea1cf7f461494b881a49`（等於 run2 事件 38） |
| 修正 | `98e5a1a`：只新增 `tests/test_integration_b1.py`（#11 Executor，同一 worklog identity，run2 事件 39；`worklog/issue-11.md` §10） |
| Flow | R1 BLOCKING → targeted correction → R2 PASS。沒有 Alternate Review、沒有 FA；獨立 audit instance，不是任何 Ticket audit 的 R3 |
| Binding 與存取的派工者核對 | R1：run2 事件 38；R2：run2 事件 40。兩者的 rollout `turn_context` 集合都只有 (`gpt-6.1-sol`, `high`, `workspace-write`)，worktree 只多出各自的 record，原樣複製後 hash 相同。R2 record 的 NV-3（「binding 由 dispatcher 核對」）在 HEAD `f38cc50` 的事件 40 已填入核對結果。本 DA 只核對這些紀錄存在且一致，不重查外部 rollout |
| Subject 與目前 HEAD 的關係 | 目前 HEAD `f38cc50`；`git diff --name-status a74e683..f38cc50` 只有 `docs/governance/records/audit/spec-SPEC-B1-c1-r2.md`（新增）與 `docs/governance/records/run/run-20261117-oc1-run2.md`（修改），都是 Bindings 第 7 節的 record-only paths（orch-default §7 P7 fast path）。`a6f78f8..f38cc50` 的非 record delta 只有 `tests/test_integration_b1.py` |

## 4. Ticket closure（SB1-AC1）

| Ticket | 最後有效 audit record | 受審 subject | 最後實作 commit | Completion predicates |
| --- | --- | --- | --- | --- |
| #7 | `audit/issue-7-c1-r2.md`（PASS） | `96b15cd` | `8981e9d` | `run-20261117-oc1-issue7.md` §7.1 P1–P8 成立，P9 留 phase 層 |
| #9 | `audit/issue-9-c2-r2.md`（PASS；cycle 2，FA ruling 授權） | `7f2fee6` | `5f9a35e` | run2 §8.1 #9 |
| #10 | `audit/issue-10-c1-r2.md`（PASS） | `8177015` | `e4fc93b` | run2 §8.1 #10 |
| #11 | `audit/issue-11-c1-r1.md`（PASS） | `bf8a8e3` | `41c848b`（SIA 修正 `98e5a1a` 另由 SIA R2 審查） | run2 §8.1 #11 |
| #8 | `audit/issue-8-c1-r1.md`（PASS） | `22f7e2a` | `47f1cdb` | run2 §8.1 #8 |

以上 subjects 都是 HEAD 的祖先（本 DA 以 `git merge-base --is-ancestor` 核對）；`5402776..c909e01`（#7 結案到 run2 BASE）只改 `run-20261117-oc1-issue7.md`。#7 之後對 `contracts/` 的變更由 #10 的 R1／R2（含 CL-B1-15 delta）審查，#10 之後對 `pace/` 的變更由 #11 R1 審查（SIA R1 scope 4 已逐組核對各最後閉合 subject 之後對應檔案無差異）。

## 5. 跨 Ticket invariants 與整合行為

| # | Invariant（跨哪些 Ticket） | Evidence | 判定與限制 |
| --- | --- | --- | --- |
| I-1 | 停等事件分類的輸出符合契約 1：疑似假停留計入 `moving_time_s`、不增 `length_m`；短停留進 `short_stop_time_s`；`short ≤ stopped`；public／private 分欄（#9 → #7） | SIA R1 scope 1 第 1 列；`tests/test_integration_b1.py:117–137` 對三趟合成軌跡逐段斷言並通過契約 1 private／public／pair | 成立 |
| I-2 | 配速表只用 CL-B1-12 定義的可計時路段、每次建表重算門檻、`category_scheme` 依 CL-B1-4 第 4 項、`stop_ratio`＝Σshort÷Σmoving、資料不足時 `speed`／`stop_ratio` 同為 `null`（#9 → #10 → #7 契約 3） | SIA R1 scope 1 第 2、4 列；整合測試 `:140–156`（`curv-tercile-110-360`、每類 6 列、ratio 獨立重算） | 成立。**限制（CL-B1-12）**：衍生表與配速表的 `category_scheme` 不同時，`validate_pace_table` 只核對總數，逐類別正確性由 #10 測試與整合測試的斷言承擔，不得歸功於驗證程式 |
| I-3 | ETA 的 `margin_coeff` 取自所用配速表表頭、`stop_ratio` 取自同一表、休息不乘餘裕、使用到缺配速類別則整份 `unknown` 不補值（#10 → #11 → #7 契約 4，NFR4） | SIA R1 scope 1 第 3、4 列；整合測試 `:159–190`（`ok` 路徑，契約 4 含不變條件 8、9）；`unknown` 路徑由 `tests/test_eta.py` 承擔 | 成立 |
| I-4 | 保留行程與非 `pace` 行程不進重建：清單以外不開檔、沒有自動建立暫定清單、`trip_ids` 含非 `pace` 時配速表拒絕（#9 CLI、#10） | SB1-AC5（SIA R1 依 CL-B1-11 §3 item 6 的讀法判 PASS）；本 DA 核對 `ingest/__main__.py` 只有 `load_manifest`（唯讀），沒有 `_load_or_create_manifest` | 成立，**限 CL-B1-11 明定的範圍**：非 `pace` 端的別名、內容相同的不同檔名與 TOCTOU 不在此 PASS 內（G-ING） |
| I-5 | `research-`／`user-` 版本分離、不覆寫、`user-` 版本的選用（#7 樣式 → #10） | SIA R1 scope 2 AB-11 列；整合測試 `:142–143`（`user-01.json` 建立、選用、讀回） | 成立 |
| I-6 | 規則 3 的範圍判定是純函式、與 `pace` 等模組無匯入關係（#8 對其他票） | SB1-AC4；本 DA 核對 `validator/rule3.py` 只匯入 `__future__`、`math`、`fractions`、`typing` | 成立 |

**整合行為。** SB1-AC2 的長鏈（合成軌跡 → `ingest` → 多趟 `user-` 配速表 → matching `category_scheme` 的合成路線 → `ok` ETA → `validate_dataset` 四組皆無違反）由 subject 中可收集的單一 pytest 測試表現；本 DA 已閱讀該測試全文，確認它實際呼叫 `build_rows`、`create_pace_table`、`compute_eta` 與各契約驗證函式，斷言有實質輸入（`ok` 狀態、三類配速非 `null`、allowance 大於 0），不是以 `unknown` 全 `null` 路徑讓算式落空。

**跨 Spec 的整合條件（不屬本 Spec，見第 9 節）。** `compute_eta` 不檢查路線目錄與配速表的 `category_scheme` 是否相同（`pace/table.py:370` docstring 明列）；`routes` 的 Spike 目錄仍用 Spike 的 scheme。本 DA 核對 `src/` 目前沒有任何產品路徑把 `routes` 目錄與新的配速表組合起來計算 ETA（`compute_eta` 只在測試中呼叫；`planner`、`app/` 尚不存在）。**規劃決定**：之後任何會在產品路徑上組合 `routes` 目錄與配速表的 Spec（`routes` Spec，G-RTE；或 Planner／主程式），MUST 在其 derivation 中納入 RI-1～RI-3 的處理，作為該路徑的前提；在那之前，SPEC-B1 的接受不得被引用為「ETA 對任意路線目錄正確」。

## 6. 分配到的 AB 部分與累積 evidence（`derivation-spec-b1.md` §7）

本節陳述的是 **SPEC-B1 分配部分**的 evidence 狀態；依 OC-1 §3.2，任何一項 AB 的 PASS 須所有分配到它的 derived Spec AC 都結案，SPEC-B1 單獨不能使任何 AB 整體 PASS。

| AB | SPEC-B1 分配部分 | 對應的 Spec AC | 累積 evidence | 分配部分的狀態 |
| --- | --- | --- | --- | --- |
| AB-3 | 由歷史 GPX 重建配速表的計算核心：停等分類、`user-` 版本的建立與選用 | SB1-AC1（#9、#10）、SB1-AC2 | #9、#10 的 audit closure；整合測試；合成 GPX 測試 | 已具 evidence（合成資料）。上傳、合併、去重複、涵蓋度摘要、介面不在內（G-ING、G-APP） |
| AB-4 | 典型與保守估計的計算（停等寬放、餘裕係數），程式文字不稱 P90 | SB1-AC1（#7、#10、#11）、SB1-AC2、SB1-AC6 | #10、#11 的 audit closure；整合測試；`src/`、`tests/` 用語只有否定句（`pace/table.py:7`「not a P90」） | 已具 evidence。介面與文件用語屬之後的 Spec 與 AB-12 |
| AB-7 | 規則 3 的範圍判定與三值結果 | SB1-AC1（#8）、SB1-AC4 | #8 audit closure；`tests/test_rule3.py`；匯入檢查 | 已具 evidence。原因代碼、RuleResult、其他規則不在內（G-VAL） |
| AB-10 | NFR4（ETA `unknown` 不輸出時間、不補值）；NFR2（測試只用合成資料）；保留行程不進重建 | SB1-AC1、SB1-AC3、SB1-AC5 | 各 Ticket E-3；SIA R1 H-2 核對；`git ls-files` 禁止路徑 0 | 已具 evidence（合成資料）。**真實資料上的隔離與公開衍生列的揭露程度 NOT VERIFIED**（第 8 節） |
| AB-11 | 產品端凍結機制：`research-` 不覆寫、保留行程拒絕 | SB1-AC1（#9、#10）、SB1-AC5 | #10 版本測試；#9／#10 角色拒絕測試；整合測試 | 已具 evidence。凍結清單格式、E1／E2 腳本的版本檢查不在內（G-E1、G-E2） |
| AB-13 | 本 Spec 的 pytest 全數通過、SIA closure、DA phase acceptance | SB1-AC3 | pytest（下表）；SIA closure（第 3 節）；本 record | **分配部分自本 record 起完成**。Bindings 第 5 節的 release gate 與其他 Spec 的同類條件不在本分配內 |

**本 DA 在 HEAD `f38cc50`（主 checkout，`git status` 乾淨）親自執行的 gates：**

| 指令／檢查 | 結果 |
| --- | --- |
| `.venv/Scripts/python.exe -m pytest -q -rxX` | **556 passed in 2.02s**；沒有 xfailed／xpassed／skipped |
| `.venv/Scripts/python.exe -m pytest -q tests/test_integration_b1.py` | 1 passed |
| `grep -rnE "xfail\|pytest\.mark\.skip\|CL-B1-8" tests/` | 0 筆（CL-B1-8 §3.2 第 5 項的 Spec 層級條件成立） |
| `PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json` | exit 0；四組 OK；標題 `data contracts v0.2`（CL-B1-2：`CONTRACT_VERSION` 在 R1-1 前不改，SPEC-B1 不宣稱完整 v0.3） |
| `git ls-files` 中 `.env`、`*.gpx`、`*.fit`、`data/` 開頭的路徑計數（只比對路徑字串） | 0 |
| `git diff ff04966..HEAD` 中長 `sk-ant-` 值與 private-key header 樣式的計數 | 0（不宣稱此樣式能辨識所有秘密形式） |
| `src/`、`tests/` 的 P90／percentile／百分位／分位數／警特報／official warning | 只有兩個否定句：`pace/table.py:7`、`validator/rule3.py:6` |

SIA R2 以 PATH 上的 Python 3.11.2 在專用 worktree 執行同一 suite（556 passed）；本 DA 以 `.venv` 在主 checkout 重跑，結果一致。

## 7. 仍 open 的 follow-ups／tracked items

下列都**不是已完成的項目**，也不是 SPEC-B1 Spec AC 的未完成部分。依治理 §1.2，follow-up 與 non-blocking finding 產生的後續事項在 acceptor 接受並授權前只是 tracked items，不得作為新工作執行；屬 OC-1 boundary 內、由 DA 之後 derive 進某份 derived contract 的，以該 derivation record 的 boundary determination 為據（先例：`decision-20261118-issue10-c107.md` §2）。

| ID | 內容 | 來源 | Owner／required authority |
| --- | --- | --- | --- |
| R2-F1（#7） | 契約 helper 對超大整數拋 `OverflowError`（Low，non-blocking） | `audit/issue-7-c1-r2.md`；`worklog/issue-7.md` §10.3 | #7 Executor，Orchestrator 追蹤；要執行須 acceptor 接受並授權，或由之後的 derived contract 納入 |
| C-6（#7） | 未改的既有欄位對非有限值仍依 v0.2 的行為 | `worklog/issue-7.md` §10.3 | Design Authority 或 acceptor 決定是否處理；目前 tracked |
| C2-R2-N1（#9） | `source_key` docstring 引用已改名的函式（文字，行為正確） | `audit/issue-9-c2-r2.md`；`worklog/issue-9.md` §13.2 | #9 Executor，需後續授權的變更 |
| C-10-4（#10） | `compare_methods` 仍以衍生表的 `seg_category` 分組 | `decision-20261118-issue10-pace-contract.md` §10 | Design Authority；若用於 E1 方法選擇，由涵蓋凍結清單與實驗的 Spec 處理 |
| 整數處理路徑盤點（#10） | 只盤點了 `isinstance(..., int)` 的寫法，其他以整數為前提的路徑未盤點；不宣稱已無同類問題 | `decision-20261118-issue10-c107.md` §8；`worklog/issue-10.md` §12.2 | Design Authority |
| CL-R1-11 | 契約 2 `after_seg_count` 範圍檢查對整數值 float fail open | `decision-20261118-issue10-c107.md` §3.2 | SPEC-R1 的 R1-1（#13）；Orchestrator 派工時 pack 含該 record |
| C-11-2／RI-1～RI-3 | 路線目錄與配速表 `category_scheme` 不同時的重建／拒絕 | `derivation-spec-b1.md` CL-B1-5；`worklog/issue-11.md` §9.2 | 之後的 `routes` Spec（G-RTE），Design Authority；第 5 節的規劃決定 |
| C-8-1 | 規則 3 的 k 由折返點產生、`in_range` 寫入 WeatherSegment | `worklog/issue-8.md` §9.2 | 之後的 `routes`／`validator` Spec（G-VAL），Design Authority |
| C-8-3 | 上游以累加 float 表示「剛好 0.8 × T」時的捨入 | `worklog/issue-8.md` §9.2 | 後續 producer／整合工作；有 material ambiguity 時 Design Authority |
| CL-B1-11 第 4 項殘餘 | 非 `pace` 端的連結別名、內容相同的不同檔名 | `decision-20261118-issue9-qda1.md`；run2 事件 13 | G-ING（之後的 Profile 管理 Spec），Design Authority；其中需取得保留行程 metadata 或內容者 fail-closed 至 acceptor（A-1） |
| AB-12 文件 | `DESIGN.md`／`README.md` 的實作狀態陳述過時（C-4、C-9-4、C-10-6、C-11-4、C-8-2、C-8-4）；RV-4（把 CL-B1-4 的 `category_scheme` 格式寫入 DESIGN §5、§6.1） | 各 worklog；first-run derivation §7 | AB-12 的文件工作（G-DOC），之後 derive |
| C-10-5、C-11-3、C-9-6～C-9-9 | 資訊或已由 Reviewer 判定的記錄項 | 各 worklog | 無需動作；有疑義時 Design Authority |

## 8. NOT VERIFIED 與需要 acceptor 的事項

| ID | 事項 | 狀態 | Required authority |
| --- | --- | --- | --- |
| NV-A | 以真實行程清單與真實 GPX 重建的契約符合性；真實保留行程／被排除行程的實際隔離；真實配速、留一趟與 ETA 的表現；公開衍生列的實際揭露程度（C-9-3、H2-R6、SIA R2 NV-1） | NOT VERIFIED | **acceptor**（RB-7） |
| NV-B | 真實資料夾中的 hard link、符號連結、內容相同的檔案、8.3 短檔名別名（CL-B1-11 A-2、FA NV-2、SIA R2 NV-2） | NOT VERIFIED | **acceptor**（RB-7） |
| NV-C | 在凍結前取得保留行程或被排除行程檔案的 metadata 或內容的任何設計（CL-B1-11 A-1、G-ING (2)） | 未決；該路徑 fail-closed | **acceptor**（RB-7） |
| NR-A | 停等寬放的回歸檢查（G-REG，以真實配速行程留一趟） | NOT RUN | **acceptor**（RB-7） |
| NR-B | E1 Lite、E2 的正式執行；保留行程的解封。本 Spec 的任何數字都不是 E1／E2 的結果 | NOT RUN | **acceptor**（OC-1 §4.2） |
| NV-D | 各 Ticket Executor 的 mutation 原始腳本與輸出的歷史執行（SIA R1／R2 NV-4） | NOT VERIFIED as historical execution；SIA closure 不依賴它 | Executor／dispatcher（若需要） |
| A-ACC-1 | Issues #7–#11 在 GitHub 上的狀態（仍 OPEN）與內容 | 本 record 不變更 | **acceptor**（OC-1 D-3、§4.2） |
| A-ACC-2 | Push、PR、合併；release gate 的最終判定 | 未執行 | **acceptor**（RB-1；Bindings 第 5 節） |

## 9. 不屬本 Spec、不得記為已涵蓋的範圍

- RI-1～RI-3（路線目錄與配速表的 `category_scheme` 不同時的處理），以及任何 `routes` 目錄與配速表的產品端組合。
- 停等寬放的回歸檢查（G-REG）與任何真實資料的執行。
- 凍結清單的格式、E1 Lite／E2 腳本對版本的檢查（SB2-T10 的實驗部分、SB2-T12）、Oracle、題庫。
- 規則 3 的原因代碼與優先順序、RuleResult 與 WeatherSegment 的 schema（SB-3、SB-4、SB-10）；規則 1、2、4、5 與計畫狀態。
- ID 樣式的放寬與契約 2 的 v0.3（SPEC-R1）；CL-R1-11（#13）。`CONTRACT_VERSION` 仍為 `"0.2"`，SPEC-B1 不宣稱契約 v0.3 已完整實作。
- 多檔上傳、合併、以內容去重複、涵蓋度摘要、Profile 管理（G-ING），含 CL-B1-11 第 4 項的殘餘與 TOCTOU。
- 介面、`README.md`、`DESIGN.md` 的用語與實作狀態（AB-12）。
- 契約 3 在不同 `category_scheme` 下的逐類別計數核對（CL-B1-12：驗證程式只核對總數）。
- OC-1 整體的 acceptance boundary 分配核對：SPEC-UI0、SPEC-R1 仍未結，且 first-run derivation §4 的 G-* 尚未分配；SPEC-B1 不是 OC-1 最後一份未結 Spec，本 record 不作全部 derived Specs 的合計核對。

## 10. 是否改變 accepted 語義

**否。**
- 本 record 只依既有 evidence 判定 SPEC-B1 的 phase acceptance，沒有修改 OC-1 的 intent、scope、constraints 或 acceptance semantics，沒有修改 SPEC-B1 的 AC、invariant 或 gate。
- 第 5 節的規劃決定（之後組合 `routes` 目錄與配速表的 Spec 須納入 RI-1～RI-3）是 CL-B1-5 與 first-run derivation G-RTE 已寫定的分工的重申，屬治理 §5.3 第 2 類，不新增 Must。
- 沒有豁免任何 audit 或 gate；沒有 defer 任何 blocking finding；沒有改變高風險類別或 assurance 要求。

## 11. 狀態（分開陳述，治理 §3.8）

- **SPEC-B1 phase acceptance**：**接受**（本 record）。orch-default §7 P10 的兩個條件（SIA closure、DA phase acceptance record 引用之）自本 record 起都存在。
- **SPEC-B1 的 Spec completion**：Spec 層級的 completion predicates 由 Orchestrator 依 record 核對，本 record 不代為宣告 run 的狀態更新。
- **Run completion**（`run-20261117-oc1-run2`）：未完成；SPEC-UI0、SPEC-R1 仍在 frontier。
- **OC-1 completion**：未完成；AB-1、AB-2、AB-5、AB-6、AB-8、AB-9、AB-12 等未分配或未結。
- **Release authorization**：沒有。合併進 `main` 由 acceptor 進行（RB-1）。
- **Issues #7–#11**：不變更，保留給 acceptor。

## 12. 受影響的 work items 與 evidence

- run2 §5 frontier 第 5 列（SPEC-B1 SIA → DA phase acceptance）：本 record 是其 phase acceptance。
- **SPEC-R1 的 R1-1（#13）**：會修改 `contracts/validate.py`（CL-B1-12、CL-B1-15 之後）。之後任何修改 SPEC-B1 模組（`contracts`、`ingest`、`pace`、`validator`）的 Ticket，須在其 self-verification 中保持 SPEC-B1 的測試（含 `tests/test_integration_b1.py`）全數通過；回歸由該 Ticket 的 audit 與其 Spec 的 SIA 承擔。只有出現新的 integration-level evidence 顯示 SPEC-B1 的 invariants 被破壞時，才由 Design Authority 判定是否需要重新驗證本 Spec；本 record 不因其他 Spec 的後續 delta 自動失效，也不為它們背書。
- 之後的 `routes` Spec（G-RTE）、Planner／主程式（G-PLN）：第 5 節的規劃決定。
- AB-12（G-DOC）：第 7 節的文件 tracked items 與 RV-4。
- SPEC-UI0：不受影響。

## 13. 執行紀錄

本 DA 讀了 Bindings m3、治理 §1.2、§2.1、§2.4、§2.5、§3.1–§3.8、§4.7、§5.3、orch-default v2.2 §5–§7、OC-1、`derivation-spec-b1.md`、first-run derivation、高風險類別 record 與各 clarification record 的裁決與 authority 節、SIA R1／R2 records、兩份 run records 的相關節、五份 worklog 的 follow-up 節、`tests/test_integration_b1.py` 全文、`ingest/__main__.py` 與 `validator/` 的匯入及函式清單。執行了第 6 節所列的 pytest、contracts CLI、`git` 核對與限定在 `src/`、`tests/` 的文字搜尋。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下的任何腳本，沒有讀保留行程；沒有修改程式、測試、Spec、Issue 或其他 record；沒有派工任何 subagent；沒有 commit。

Decision: SPEC-B1 v1 phase acceptance — ACCEPT（引用 SIA closure `audit/spec-SPEC-B1-c1-r2.md`，subject `a74e683`）。不改變 accepted 語義；不是 release authorization。
