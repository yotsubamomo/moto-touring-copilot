# Decision record — SPEC-R1 v1 的 Design Authority phase acceptance，與 SIA-R1-G01～G13 的 DA determination

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-spec-r1-phase-acceptance`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | OC-1 第二個 Formal run 的 Orchestrator：`docs/governance/records/run/run-20261117-oc1-run2.md`（事件 113 之後；orch-default v2.2 §5「phase acceptance」、§6、§7 P10） |
| Outcome Contract | OC-1（`docs/governance/records/outcome-contract.md`），acceptor 2026-11-17 針對 `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受。之後該檔只有狀態欄與第 10 節接受紀錄的轉錄，條文未變（`git diff 873e37a..HEAD` 只有該檔的轉錄 delta；`DESIGN.md`、`README.md`、`docs/spec`、`docs/ui`、`docs/requirement`、`prototype` 自 `873e37a` 起沒有變更，`git diff --quiet` exit 0） |
| Spec | **SPEC-R1 v1**：`derivation-spec-r1.md`（commit `8c3c588`，至 HEAD 未修改）＝第 2 節引用的段落＋DD-R1-1、DD-R1-2、CL-R1-1～CL-R1-10＋第 5 節 R1-1～R1-4 與 E-1～E-6＋第 6 節 SR1-AC1～SR1-AC5；其 clarifications CL-R1-11（`decision-20261118-issue10-c107.md`）、CL-R1-12／13（`decision-20261118-issue13-c131.md`）、CL-R1-14～19（`decision-20261118-issue14-c141.md`）、CL-R1-20／21（`decision-20261118-issue14-qalt1.md`）、CL-R1-22～24（`decision-20261118-issue15-c151.md`）、CL-R1-25～27（`decision-20261118-issue16-c161.md`）、CL-R1-28（`decision-20261118-issue16-c2r1f3.md`）、CL-R1-29（`decision-20261118-issue16-c165.md`）；FA `ruling-20261118-issue16-c1.md`（含 Addendum A）；跨 Spec 決定 `decision-20261117-oc1-first-run-derivation.md`；高風險類別 `decision-20261117-high-risk-categories.md` |
| Tickets | #13（R1-1）、#14（R1-2）、#15（R1-3）、#16（R1-4）。Issue 原文：派工所附 `issue-13-body.md`～`issue-16-body.md`，本次實測 SHA-256 依序 `d4328686…6584`、`f7a83732…7b75`、`a54f8034…5ad7`、`105fdc98…ede1`，都等於 run record 第 4 節的建立雜湊。沒有呼叫 GitHub |
| 受審狀態 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `da336c086aca161e24752362f321f5d0021f447c`（`git rev-parse HEAD` 核對；`git status` 乾淨） |
| 依據的條文 | 治理 §1.2、§2.1、§2.4、§2.5、§3.8、§4.7、§5.1、§5.3；orch-default v2.2 §5、§6、§7（P1–P10）；Bindings m3 第 2.4、2.6、4、5、7 節；OC-1 §2.1、§2.3、§3.1、§3.2、§4.2、§5、§9.1 |
| **結論** | **工作一：接受（ACCEPT）SPEC-R1 v1 的 phase acceptance**，限第 6 節所列的分配範圍與第 7～9 節的限制。**工作二：SIA-R1-G01～G13 全部屬實，逐項 determination 見第 10 節；OC-1 的最終 closure 在這些缺口處理前不成立。** 不改變 accepted 語義；在 OC-1 boundary 內；phase acceptance 本身不需要 acceptor 的接受或授權（第 10 節列出之後各 derivation 需要的 acceptor 動作）；沒有 escalation。本 record 不 derive 新的 Spec 或 Ticket；不是 release authorization、不是 run completion、不是 OC-1 completion；不變更 Issues #13～#16 |

## 1. 問題

1. 依治理 §3.8 與 orch-default §7 P10：SPEC-R1 的四張 Ticket 都已結案、另外派工的 Spec Integration Audit 已 closure 之後，SPEC-R1 能否作 phase acceptance——跨 Ticket invariants、整合行為、累積 evidence 與未結 follow-ups 是否足以接受；接受的範圍與限制為何。
2. SPEC-R1 是目前 derived contract set 中最後一份未結的 Spec。SIA R1 依治理 §4.7 第五個範圍核對了全部 derived Specs 的分配，記錄 SIA-R1-G01～G13（AB-1～AB-13 的分配缺口，Medium／non-blocking，共同 owner DA）。每一項缺口是否屬實、由哪個之後的 derivation 承接、現在能否 derive、需要哪個 authority。

## 2. 裁決（工作一）

**接受。** 理由：

1. **SIA 已 closure（P10 的前半）。** 本 run 依 acceptor 指示第 4 項另外派工 SIA。最後有效 record `spec-SPEC-R1-c1-r2.md` 為 Reviewer closure（`Verdict: PASS`）：唯一 blocking 的 SIA-R1-F1 RESOLVED；SIA-R1-N1 的紀錄缺漏 RESOLVED（平台驗證本身仍 NOT RUN）；沒有修正直接產生或暴露的新 blocking defect；SIA-R1-G01～G13 依原 disposition 保留 OPEN、交 DA（第 3 節）。本 record 引用之，不豁免、不取代它；**不**引用任何 Ticket audit record 作為 SIA closure。
2. **四張 Ticket 都依 orch-default §7 P1–P8 結案**（run record §8.1），P9 留在 phase 層，由 SIA 與 SR1-AC2 的整合測試滿足（第 4 節）。
3. **跨 Ticket invariants 與整合行為**在 SIA R1／R2 的審查與本 DA 的獨立核對中都成立，限於合成資料、離線與本 Spec 已寫定的範圍（第 5 節）。
4. **SR1-AC1～SR1-AC5 都有 evidence 且判為 PASS**（各依其限定範圍），合起來涵蓋 `derivation-spec-r1.md` §7 分配給本 Spec 的 AB 部分（第 6 節）。本 DA 在 HEAD `da336c0` 重跑的 gates 與 SIA R2 的結果一致。
5. **未結 follow-ups 都有 owner 與 required authority，沒有任何一項是 SPEC-R1 Spec AC 的未完成部分**：它們或屬 §6 明列的不涵蓋範圍、或屬之後的 derivation（G-RREQ、G-RTE、G-CON、G-APP、G-E2、G-DOC）、或需要 acceptor 的授權（RB-7、真實請求、RB-6）（第 7、8 節）。沒有影響本 Spec 完成的未決 design ambiguity。
6. **SIA-R1-G01～G13 不阻擋 SPEC-R1 的 phase acceptance。** 它們是 OC-1 整體 acceptance boundary 的分配缺口，不是 SPEC-R1 分配部分的缺口；治理 §4.7 要求全部 derived Specs 合起來涵蓋整個 boundary 的時點是「Outcome Contract 或適用 phase 最終 closure 前」，SPEC-R1 的 phase acceptance 不是 OC-1 的最終 closure。Reviewer 也判為 non-blocking。這些缺口的 determination 在第 10 節，且 OC-1 的最終 closure 在它們處理前不成立。
7. **不需要 escalation。** Phase acceptance 的後果可由現有 evidence 裁決（E-DA/D1 不成立）。本 DA 先前就 SPEC-R1 所作的決定沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或實質爭議：FA `ruling-20261118-issue16-c1.md` 處理 #16 的 R2-F1（實作違反 R1-4 範圍 (f)、CL-R1-8），判為 targeted rework、明記「不是 design issue」「沒有語義問題交 DA」；SIA-R1-F1 是 SR1-AC2 的 evidence 缺口，指向 Executor 的交付，DA 寫定的 SR1-AC2 原樣被要求滿足；C2R1-F3 指出 CL-R1-25 的遺漏，已由 CL-R1-28 補上（該 record 已判定不是 D2）。E-DA/D2 不成立。

## 3. 所引用的 Spec Integration Audit closure record

| 項目 | 內容 |
| --- | --- |
| **Closure record** | `docs/governance/records/audit/spec-SPEC-R1-c1-r2.md` — Spec Integration Audit of SPEC-R1，cycle 1，R2 closure review；`primary_reviewer` Codex 自寫；最後一行 `Verdict: PASS` |
| Closure record 的 SHA-256 | `38d205a091853c65ac7b8f0f4ae9993b362a75d2c7d2303e60856b78656051b7`（本 DA 以 `git show HEAD:<path> \| sha256sum` 與工作目錄檔案核對，兩者相同，且等於 run record 事件 113 記載的值；commit `da336c0`） |
| **Subject** | BASE `1fd1de3585ea23f80842ac3276fe9305369b51e3`，HEAD **`ca50bc9e2f2ec1aa635e6a59d21253b08f274d08`** |
| 同一 audit instance 的 R1 | `docs/governance/records/audit/spec-SPEC-R1-c1-r1.md`，subject `804362dc7b559867228eccbb289e22a055526bd2`，`Verdict: BLOCKING`（SIA-R1-F1 Medium／blocking：SR1-AC2 缺少把 `get_route` 各模式的實際輸出送進 R1-1 契約檢查的整合測試；SIA-R1-N1 Low／non-blocking；SIA-R1-G01～G13 Medium／non-blocking）；SHA-256 `47193632ee493b3d86e5ecf3c07f88774f2231d49be03f928a676770b0ffafdf`（本 DA 核對，等於事件 110） |
| 修正 | `4cbc71b`：只新增 `tests/test_integration_r1.py`（174 行，3 個測試函式、6 個案例；沒有修改 `src/` 或既有測試）；SPEC-R1 整合 rework 的 Executor（#16 的同一 `gov-executor`），worklog `worklog/spec-r1-integration.md`（`df3e47e`；事件 112）。SIA-R1-N1：run record 事件 111 的補登 |
| Flow | R1 BLOCKING → targeted correction → R2 PASS。沒有 Alternate Review、沒有 FA；獨立 audit instance，不是任何 Ticket audit 的 R3 |
| Binding 與存取的派工者核對 | R1：事件 110；R2：事件 113。兩者的 rollout `turn_context` 集合都只有 (`gpt-6.1-sol`, `high`, `workspace-write`)，worktree 只多出各自的 record，原樣複製後 hash 相同。R2 record 的 NV-BIND-R2（「本 HEAD 沒有本次 R2 dispatch／binding event，正式採用前必要」）由事件 113 填入。本 DA 只核對這些紀錄存在且一致，不重查外部 rollout |
| Subject 與目前 HEAD 的關係 | `git diff --name-status ca50bc9..da336c0` 只有 `docs/governance/records/audit/spec-SPEC-R1-c1-r2.md`（新增）與 `docs/governance/records/run/run-20261117-oc1-run2.md`（修改），都是 Bindings 第 7 節的 record-only paths（orch-default §7 P7 fast path）。`804362d..da336c0` 唯一的非 record 檔是 `tests/test_integration_r1.py`。`1fd1de3..da336c0` 的非 record delta 只有 `src/moto_copilot/contracts/`、`ingest/geometry.py`、`routes/catalog.py`、`routing/` 與 11 個 `tests/` 檔；`app/`、`pyproject.toml`、`DESIGN.md`、`README.md`、`docs/spec`、`docs/ui`、`prototype`、`.claude`、`CLAUDE.md`、`AGENTS.md` 都沒有變更 |

## 4. Ticket closure（SR1-AC1）

| Ticket | 最後有效 Ticket audit record | 受審 subject | 最後實作 commit | Completion predicates |
| --- | --- | --- | --- | --- |
| #13 R1-1 | `audit/issue-13-c1-r2.md`（PASS；事件 66） | `be76a97` | `3c065f8` | run record §8.1 #13：P1–P8 成立，P9 留 phase 層 |
| #14 R1-2 | cycle 1 Alternate `audit/issue-14-c1-alt.md`（`VERDICT: CLOSURE`，事件 75）＋cycle 2 `audit/issue-14-c2-r1.md`（PASS；事件 78） | `6f08a5a` | `665a86f` | 同上 #14 |
| #15 R1-3 | `audit/issue-15-c1-r2.md`（PASS；事件 86） | `48ff350` | `efbffe8` | 同上 #15 |
| #16 R1-4 | cycle 2 `audit/issue-16-c2-r2.md`（PASS；事件 106；cycle 2 經 FA ruling 授權） | `18a5c5c` | `9cc566a` | 同上 #16（事件 109） |

- 上列 subject 與實作 commit 都是 HEAD 的祖先（本 DA 以 `git merge-base --is-ancestor` 核對）。上列 audit records 的最後一行 verdict 本 DA 已讀過，與 run record 一致。
- 結案後唯一的非 record delta 是 SIA correction `4cbc71b`（只新增測試檔），由 SIA R2 審查；四張 Ticket 的 finding 沒有被重開。#14 的 `tests/test_routing_store.py` 一個測試函式在 #16 中被修改，已由 `decision-20261118-issue16-c161.md` 第 10 節判定不影響 #14 的結論，SIA R1 在最終 subject 上以 AST 比對核對（範圍一 CL-R1-25 列）。
- 已 route 的設計問題都有 record（P6）：C-13-1／2／4 → c131；C-14-1～5 → c141；Q-ALT-1 → qalt1；C-15-1～3 → c151；C-16-1～4 → c161；R2-F1 → FA ruling；C2R1-F3 → c2r1f3；C-16-5 → c165。C-14-6 保留給 acceptor（第 8 節）。

## 5. 跨 Ticket invariants 與整合行為

| # | Invariant | Evidence | 判定與限制 |
| --- | --- | --- | --- |
| I-1 | 契約 v0.3 ↔ routing 的 identity：`get_route` 各模式（一般模式首次存放、重用、Snapshot Mode、嚴格模式；目標 GPX 單向、來回自動辨識、來回騎士指定落在兩點之間）回傳的 `route_id`、`route_source`、`trip_type`、`snapshot_id` 承載到契約 2 後通過 R1-1 的 `validate_route_catalog`；`RS-` 的 hex 等於 `snapshot_id` 的 hex；`checkpoint_id` 前綴等於 `route_id` | SIA R2 的 F1 closure（11 次零違反的實際 validator 呼叫、3 次被拒的負向 guard）；本 DA 閱讀 `tests/test_integration_r1.py` 全文：五個路線參數列都經 `assert_contract_identity`，其中 `validate_route_catalog(...) == []`；`test_the_catalog_check_rejects_a_broken_identity` 證明驗證不是空的；本 DA 重跑該檔 6 passed | 成立。測試中的路線目錄、路段與 `CP01…` 只是承載 ID 的合成測試資料，不是 G-RTE 的產生或編號規則（測試檔 docstring 與 worklog D-SIA-1 都如此限定） |
| I-2 | 正規化與 identity（CL-R1-14～16、18、19）：同一條正規化規則用於 `request_key`、指紋與 snapshot hash；採用檢查以原值判定 | SIA R1 範圍一第 2 列 | 成立（合成範圍） |
| I-3 | R1-2 存放 ↔ R1-4 採用（CL-R1-17、20、21）：選取、存放與嚴格模式的錯誤向上傳遞，不轉成 route error、不重試、不改用過期快照 | SIA R1 範圍一第 3 列；integration 測試的嚴格模式列 | 成立（合成範圍） |
| I-4 | R1-3 ↔ R1-4 的目標 GPX passthrough（CL-R1-24）：原樣傳出 ID、ref、行程型態、各方向原序點與錯誤 | SIA R1 範圍一第 4 列；integration 測試以直接呼叫 R1-3 的結果比對 | 成立 |
| I-5 | #14 的無網路計算 ↔ #16 的真實傳輸層（CL-R1-25）：只有 `http_transport.py` 豁免 `http`／`ssl` | SIA R1 範圍一第 5 列 | 成立 |
| I-6 | 任何不採用的情形都不存快照、不產生里程與道路名稱；國道訊號優先（SR1-AC3） | SIA R1 SR1-AC3 列；最終 suite 回歸 | 成立於本 Spec 的合成路線層；不是對所有可能輸入的窮舉證明 |
| I-7 | 用語：國道檢查不稱為道路主管機關的驗證；去回同路的自動辨識不稱為已驗證（SR1-AC5） | SIA R1 SR1-AC5 列；本 DA 以限定在 `src/moto_copilot/routing`、`src/moto_copilot/ingest/geometry.py`、`tests/test_integration_r1.py` 的搜尋核對：命中都是否定或限定句（`adoption.py:35`「not an independent check against road authority data」；`target_gpx.py:27`、`:75`、`:195`「NOT validated with real data」；`source.py:273` 的 `validated` 指快照的結構檢查） | 成立 |

**整合行為。** 一般模式 `get_route` → R1-2 `find_reusable` → R1-4 各方向採用 → 建快照 → 存放 → 由快照組成採用的路線；第二次規劃不發引擎請求；Snapshot Mode 與嚴格模式只選取；目標 GPX 經另一個來源分支原樣帶出，不套用引擎的採用檢查；T-9 以真實 HTTPS 傳輸層接替身連線走同一個 `get_route`（SIA R1 範圍三）。SIA-R1-F1 修正後，這些整合路徑的輸出也與契約 2 的 identity 約束一起被驗證（SIA R2 範圍三）。高風險類別 H-1、H-2、H-3、H-4 的最低核對範圍由 SIA R1 範圍三逐項記錄，SIA R2 確認修正只新增合成測試、沒有新的產品 I/O、採用規則或宣稱；限制（真實 TLS／伺服器、真實資料、PlanResult／LLM 的裁切）見第 8 節。

## 6. 分配到的 AB 部分與累積 evidence（`derivation-spec-r1.md` §6、§7）

本節陳述的是 **SPEC-R1 分配部分**的 evidence 狀態；依 OC-1 §3.2，任何一項 AB 的 PASS 須所有分配到它的 derived Spec AC 都結案、證據都存在（AB-1、AB-5、AB-9、AB-12 另須實際執行），SPEC-R1 單獨不能使任何 AB 整體 PASS。

**Spec 層級 AC（derivation §6）：**

| Spec AC | 狀態 | Evidence 與限制 |
| --- | --- | --- |
| SR1-AC1 | **PASS** | 第 4 節；SIA R1 `:80`、`:86`～`:95`，SIA R2 承接 |
| SR1-AC2 | **PASS** | SIA R2 的 SIA-R1-F1 closure；第 5 節 I-1 |
| SR1-AC3 | **PASS（本 Spec 的合成路線層）** | SIA R1 `:82`，SIA R2 回歸；第 5 節 I-6 |
| SR1-AC4 | **PASS（依已分配層級）** | SIA R1 `:83`、SIA R2：測試封鎖 socket／連線／DNS，傳輸層用替身；GPX 的路徑與檔名不出現在輸出、錯誤與 log；傳輸層例外不含請求座標。內部的採用路線與快照本來就承載幾何，**不是** PlanResult／LLM 輸出隱私已完成的宣稱（未分配，第 10 節 G10） |
| SR1-AC5 | **PASS** | 第 5 節 I-7 |

**分配的 AB 部分（derivation §7）：**

| AB | SPEC-R1 分配部分 | 累積 evidence | 分配部分的狀態 |
| --- | --- | --- | --- |
| AB-1 | 「路線快照上的實際道路路線」的產生、檢查與保存**能力**（含真實傳輸層，CL-R1-25） | R1-2、R1-4 的 AC；SR1-AC2、SR1-AC3；T-9 | **能力具備（合成與替身連線範圍）。** 實際取得道路路線的證據 **NOT RUN**（NV-1），端到端執行不在本分配（c161 §2.7）。**AB-1 整體不是 PASS** |
| AB-2 | FR1 中路線引擎產生實際道路路線、支援來回與單向、改用只讀幾何的目標 GPX、路線失敗時明確報錯 | SR1-AC2、SR1-AC3；R1-3、R1-4 的 AC | 已具 evidence（合成）。行程描述、追問、期限語意、詞彙表不在本分配（G02） |
| AB-10 | NFR2：路線層對第三方只送呼叫者提供的位置與通用 User-Agent；目標 GPX 不外流。NFR4：路線取不到或不能採用時回傳明確的錯誤，不補造路線 | SR1-AC3、SR1-AC4；T-5、T-6 | 已具 evidence（本層）。**送出的位置是否為公開地標由上游保證，屬 G-RREQ（TI-C16-3），不在本分配**；隱私裁切與錨點代換不在本分配 |
| AB-11 | 路線快照嚴格模式的機制（凍結清單指定的快照、檔案 SHA-256 核對、不回退） | R1-2 store tests；R1-4 engine 的嚴格模式列；SR1-AC2 的嚴格模式列 | 已具 evidence（機制）。凍結清單的檔案格式、E2 Runner 不在本分配（TI-C14-5，G11） |
| AB-13 | 本 Spec 的 pytest、Spec Integration Audit closure、Design Authority phase acceptance | 下表；第 3 節；本 record | **分配部分自本 record 起完成。** Release gate 與其他 Spec 的同類條件不在本分配（G13） |

**本 DA 在 HEAD `da336c0`（主 checkout，`git status` 乾淨）親自執行的 gates：**

| 指令／檢查 | 結果 |
| --- | --- |
| `.venv/Scripts/python.exe -m pytest -q -rxX` | **2244 passed in 43.87s**；沒有 xfailed／xpassed／skipped（直譯器 Python 3.11.2） |
| `.venv/Scripts/python.exe -m pytest -q tests/test_integration_r1.py` | 6 passed |
| `PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json` | exit 0；`data contracts v0.3`；derived_segments、route_catalog、pace_table、eta_output 都 OK |
| `grep -rnE "pytest\.mark\.(xfail\|skip)\|importorskip\|xfail\(" tests/` | 0 筆 |
| `git ls-files` 中 `.env`（含變體）、`*.gpx`、`*.fit`、`*.key`、`data/` 開頭的路徑計數（只比對路徑字串） | 0 |
| `git diff 1fd1de3..HEAD -- src tests` 新增行中長 `sk-ant-` 值、private-key header、長 `api_key=` 值樣式的計數 | 0（不宣稱此樣式能辨識所有秘密形式） |
| `git diff --quiet 1fd1de3..HEAD` 對 `DESIGN.md`、`README.md`、`docs/spec`、`docs/ui`、`docs/requirement`、`prototype`、`app`、`pyproject.toml`、`.claude`、`CLAUDE.md`、`AGENTS.md` | exit 0 |
| Issues #13～#16 原文的 SHA-256 | 等於 run record 第 4 節 |

2244＝#16 結案時的 2238＋`tests/test_integration_r1.py` 的 6，與 SIA R2（worktree `.venv`，2244 passed）及事件 112 的 Orchestrator 重跑一致。

## 7. 仍 open 的 follow-ups／tracked items

下列都**不是已完成的項目**，也不是 SPEC-R1 Spec AC 的未完成部分。依治理 §1.2，follow-up 與 non-blocking finding 產生的後續事項在 acceptor 接受並授權前只是 tracked items，不得作為新工作執行；屬 OC-1 boundary 內、由 DA 之後 derive 進某份 derived contract 的，以該 derivation record 的 boundary determination 為據。

| ID | 內容 | 來源 | Owner／required authority |
| --- | --- | --- | --- |
| TI-C13-2、C-13-7 | `trip_id`／`datetime` 的既有樣式未收緊；不可 hash 的 ID 在舊 validator 集合檢查的 `TypeError` | c131；run §8.1 #13 | **DA**，之後的 contracts derivation（G-CON）。不宣稱已修復 |
| RV-6～RV-14 | `DESIGN.md`、SPEC-001 對 v0.3 實作狀態、ID 文字、快照與傳輸層文字的同步（c131 §4、c141、qalt1、c151、c161 第 7 節） | 各 DA record | **DA**，G-DOC（AB-12）。c131 §4 寫定的時機條件「最早在 SPEC-R1 phase acceptance 之後」自本 record 起成立；文件同步之前，狀態報告以程式與紀錄為準 |
| RV-1～RV-5 | first-run derivation 第 7 節的文字同步建議 | first-run §7 | **DA**，之後的 Spec 修訂或 G-DOC |
| TI-C14-1 | 詞彙表座標定義物件的 float 型別與整數轉換 | c141 | **DA**，G-RREQ／詞彙表（G-KB） |
| TI-C14-5、RV-8～RV-10 | `FrozenEntry` 與凍結清單檔案格式的對應；取位、取整與 store 錯誤的文字 | c141、qalt1 | **DA**，G-E2／凍結 Demo（AB-11）與 G-DOC |
| TI-C15-1、RV-11 | 騎士指定與實際採用的折返位置不同時的顯示；GPX 分界的文字 | c151 | **DA**，之後的整合 Spec（G-APP）與 G-DOC |
| CL-R1-22 §2.4 的兩項限制 | 稀疏檔案上採用的折返點可離指定位置數百公尺；相距不到 1 m 的分界點取整後 `RG-` 相同 | c151 §2.4 | **DA** 知悉；顯示問題併 TI-C15-1。**未消除，不記為已涵蓋或已驗證無風險** |
| TI-C16-2、RV-12～RV-14 | 「圖磚最後修改日期」在來源證據與介面上的用語（不稱為 OSM 擷取日期或已確認最新）；文字同步 | c161 | **DA**，整合 Spec（G-APP）與 G-DOC |
| TI-C16-3、TI-C165-1 | `request_key` 地點與每方向請求位置的一致性、`ref_id`／role 的合法值、送出前拒絕非法 Unicode 的上游核對；位置是否為公開地標 | c161、c165 | **DA**，G-RREQ。目前呼叫端的 `ValueError`／`SnapshotValidationError` fail closed 依 DA disposition 接受，不說成產品的輸入保護已完成 |
| TI-C2R1F3-1 | 預設信任來源可受 `SSL_CERT_FILE`／`SSL_CERT_DIR` 影響；`OPENSSL_CONF` 的影響 NOT VERIFIED | c2r1f3 | **DA**：本 record 確認它已由 SIA R1／R2 列為已知限制；承接到 G-DOC（`DESIGN.md` Limitations 或安全說明不得宣稱傳輸層完全不受環境變數影響）。不另改安全策略 |
| NV-PY313／NV-PY；NV-SYMLINK | Python 3.13 以後與其他平台、真實失效或循環連結 **NOT RUN**；只實跑 Python 3.11.2（Windows） | #14、#16 worklogs；SIA-R1-N1；事件 111 | Owner＝**Orchestrator**（routing 與紀錄），required authority＝**DA**。**本 DA 的範圍判定**：SPEC-R1 的 evidence 只涵蓋 Python 3.11.2；`pyproject.toml` 的 `requires-python = ">=3.11"` 不得被解讀為 3.13 以後已驗證。是否另作 3.13 以後的驗證、或在文件中明寫已驗證的版本，在 G-DOC（或另一個平台驗證 work item）derive 時決定；需要變更環境權限時才交 acceptor。不是本 phase acceptance 的條件 |
| C-13-3／NV-ACCESS | #13 Executor 自行揭露的 `experiments/` 搜尋；外部 transcript 未重查 | 事件 61；SIA R1 `:179` | **Orchestrator**（已記錄）；不據此宣稱私有資料外洩 |
| C-13-6／NV-EXP | `experiments/` 中呼叫 `build_route` 的腳本在契約 v0.3 下的實際行為 NOT VERIFIED／NOT RUN | c131 §6 | 之後執行該腳本的 work item；需要私有資料時 **acceptor（RB-7）** |
| WL-R1（記錄一致性） | `worklog/spec-r1-integration.md` 最後更新於 `df3e47e`（SIA R2 之前），檔首「狀態」列仍寫「待 SIA cycle 1 R2」、第 8 節仍寫「補登不在本次」，沒有記載 SIA R2 的結果與事件 111 的補登。權威的 closure 紀錄是 SIA R2 record 與 run record 事件 111、113，所以不影響本接受 | 本 DA 核對（`git log -1 -- <worklog>` 為 `df3e47e`） | **Orchestrator** 追蹤；是否派 Executor 作 record-only 更新由 Orchestrator 決定。不是 phase acceptance 的條件，也不是新工作的授權 |
| `diversity_lost`（#16 cycle 2 R1） | Codex usage limit 時依 Profile §6 改派 Claude path 的歷史事實 | 事件 99 | 資訊；不外推為其他 audit 的狀態 |

## 8. NOT VERIFIED、NOT RUN 與需要 acceptor 的事項

| ID | 事項 | 狀態 | Required authority |
| --- | --- | --- | --- |
| NV-1／RV-5 | 對公開 Valhalla 伺服器的真實請求：TLS、轉址、真實回應形狀（via 是否單一 leg、warnings 位置、trace／status 欄位）、異常值、五條參考路線的 10 段是否 `pass`、詞彙表地標的偏移 | **NOT RUN／NOT VERIFIED**（本 Spec 的 AC 不需要真實請求，CL-R1-1；本 run 不連網） | **acceptor**（第一次真實請求的指示；OC-1 §5 的有條件批准）；執行由之後的整合或詞彙表 work item 承擔（c161 §2.7；G01、G02） |
| NV-PRIV | 真實 GPX、保留行程、住家附近的位置、部署時的快照存放路徑、折返啟發式在真實資料上的表現、裁切與錨點代換後才外送 | **NOT VERIFIED**（本 run 沒有 RB-7 授權，沒有取得資料） | **acceptor（RB-7）**。不得由合成資料外推 |
| C-14-6／R1-N1 | `aa42392` 的歷史與 `worklog/issue-14.md` 引用手寫範例座標（成對時落在台灣境內；Executor 表明不是騎乘資料）；公開前的 records／歷史處置 | 未決；沒有改寫歷史 | **acceptor**（RB-1 公開前的決定；改寫歷史屬 RB-6）。不假定是私有騎乘資料，也不宣稱已清理 |
| `efbffe8` commit message | 第一行前綴格式偏離 `git-commit-rules.md`（事件 85 已揭露） | 未改寫 | **acceptor**（RB-6） |
| A-ACC-1 | Issues #13～#16 在 GitHub 上的狀態 | 本 record 不變更。OC-1 §4.1、D-3 允許 Agents 管理新建 derived Issues 的狀態；是否、何時關閉由 Orchestrator 依其授權與 run 規則處理 | Orchestrator（D-3）；本 DA 不作 |
| A-ACC-2 | Push、PR、合併；release gate 的最終判定 | 未執行 | **acceptor**（RB-1；Bindings 第 5 節） |

## 9. 不屬本 Spec、不得記為已涵蓋的範圍

`derivation-spec-r1.md` §6 的 known-not-covered 逐項保留，**不在本接受內**：

- 真實路線請求的結果（五條參考路線）；詞彙表；路線請求的解析（PlaceRef → 位置、出發錨點、目的地是公路時的進入端與另一端、回程組成）；路線目錄、切段、檢查點的產生與編號、`ridden_share_pct`；RouteSummary 與 RouteError 的 `message`／`actions`。
- 另外保留：CL-R1-22 §2.4 的兩項限制；TI-C15-1；CLI、介面、PlanResult、LLM 的整合；凍結清單的檔案格式與 E2 Runner；`route_source = trip` 的示範路線（R01、R02 維持現狀）；`routes/catalog.py` 的 CL-R1-12 三個鍵不是 `routes` 的收編，也不是 G-RTE 的基線（c131）。
- `tests/test_integration_r1.py` 中的合成路線目錄與 `CP01…` 只是 identity 的承載，不是上述任何項目的實作 evidence。
- 真實資料、真實 API、付費呼叫；E1 Lite、E2 的任何結果（本 Spec 沒有任何實驗數字）。
- `README.md`、`DESIGN.md` 對 `routing` 實作狀態與契約 v0.3 的陳述（AB-12；`DESIGN.md` 第 3 行仍寫「尚未實作」）。

## 10. SIA-R1-G01～G13 的 DA determination（工作二）

### 10.1 共同判定

1. **全部屬實。** 本 DA 以 OC-1 §3.1 的 AB-1～AB-13、三份 derivation record 的 §7、first-run derivation §4 的「尚未分配的部分」欄與 §6 的 G-* 表、SPEC-B1 與 SPEC-UI0 phase acceptance 的第 6、9 節，以及本 record 第 6 節核對：SPEC-B1、SPEC-UI0、SPEC-R1 合起來**沒有**涵蓋 AB-1～AB-13。十三項 AB 中，AB-5、AB-6、AB-9、AB-12 沒有任何分配；其餘九項只有部分分配。G01～G13 的每一列都對應一個真實的分配缺口；沒有一列是三份 Spec 的 implementation defect，也沒有發現造成歧義的重疊（AB-10、AB-11、AB-13 的重疊各有具體子範圍，與 SIA R1 範圍五的判斷一致）。
2. **Severity 與處置。** 同意 Reviewer 的 Medium／non-blocking：它們不擋 SPEC-B1、SPEC-UI0、SPEC-R1 的 phase acceptance（第 2 節第 6 點），也不延長任何 SIA cycle。它們的處置是「由之後的 derivation 承接」，不是 dismiss，也不是 defer 成 OC-1 不需要的範圍。本 record 沒有縮小、放掉或改判任何 AB；放掉 Must 的路徑只有 OC-1 §3.2 與 `DESIGN.md` §9.3 的捨棄順序，屬 acceptor。
3. **OC-1 的最終 closure 在這些缺口處理前不成立。** 依治理 §4.7 與 OC-1 §3.1，OC-1 closure 前全部 derived Specs 必須合起來涵蓋 AB-1～AB-13。SPEC-R1 是**目前** derived contract set 中最後一份未結的 Spec；之後 derive 的 Specs 加入後，屆時同一 OC-1 最後一份未結 Spec 的 SIA **MUST 重新**作全部 derived Specs 的分配涵蓋核對。本 record 的 determination 不取代那次核對。
4. **本次不 derive。** 依派工範圍（本 run 只到三份 Spec 的 SIA closure 與 phase acceptance），本 record 只記錄 determination 與 routing，**不 derive 新的 Spec 或 Ticket**，也不建立 Issues。「可以開始 derive」只表示前提中屬 DA 自己的部分已成立，不代表已排程、已派工或已授權執行；它在之後由 DA 在新的派工中以各自的 derivation record 作 boundary determination。
5. **「現況」相對 first-run derivation §6 的變化**（本 DA 核對 HEAD 的紀錄；`DESIGN.md`、`docs/spec` 自 `873e37a` 起沒有變更）：
   - SPEC-R1 自本 record 起 phase-accepted：**G-RTE** 對 SPEC-R1 共用介面的依賴、**G-DOC** 中 RV-6～RV-14 的時機條件，自本 record 起成立。
   - SPEC-B1 自 `decision-20261118-spec-b1-phase-acceptance.md` 起 phase-accepted：G-RTE 對 #10 `category_scheme` 格式（CL-B1-4）的依賴已成立。
   - 其他前提**沒有變化**：SPEC-001 §11.1 的 SB-3、SB-4、SB-6、SB-10 仍未解決，SB-5（C3）仍 BLOCKED／NOT RUN；UI Delta Review 未進行；OC-1 §9.1 C-1 的額度沒有新授權；氣象署授權碼依 `HANDOFF-2026-11-17.md` 第 3.4 節尚待 acceptor 申請（本 DA 不讀 `.env`，憑證是否到位 NOT VERIFIED）；詞彙表的公路與地標尚待 acceptor 選擇（first-run A-7）。

### 10.2 逐項 determination

| Finding | AB | 缺口（屬實） | 承接的 derivation | 現在能否 derive | Required authority |
| --- | --- | --- | --- | --- | --- |
| **SIA-R1-G01** | AB-1 端到端流程 | SPEC-R1 只有路線能力；端到端整合（`routes`、`sources`、`validator`、`planner`、`app/`）與依 `README.md` 重現的實際執行紀錄都沒有分配 | G-RTE、G-SRC、G-VAL、G-PLN、G-APP（端到端的執行與紀錄由最後的整合 Spec 承擔，在 G-APP derive 時判定歸屬）；另依賴 G-RREQ、G-KB | **未 ready**：G-SRC、G-PLN BLOCKED（C3、憑證、額度），G-APP 待 UI Delta Review。AB-1 須有實際執行證據（OC-1 §3.2），在 C-1 授權前只能記 BLOCKED | DA（derivation）；**acceptor**：OC-1 §9.1 C-1 的 Planner LLM 額度（RB-4、D-5）、RB-3 憑證、UI Delta Review（AB-8）、第一次真實路線請求的指示（NV-1） |
| **SIA-R1-G02** | AB-2 FR1 | 行程描述的解析、追問、期限語意、詞彙表解析、行程描述的輸入保護 | G-RREQ（請求解析，含 TI-C14-1、TI-C16-3、TI-C165-1）、G-KB（詞彙表）、G-PLN（解析與追問）、G-CON（SB-10 的 RouteRequest 等） | **未 ready**：G-RREQ 需要詞彙表的 Spec 與內容；SB-6、SB-10 未關閉；G-PLN 的 LLM 部分 BLOCKED。屬 DA 自己的部分可以開始：詞彙表的欄位與座標定義物件、回程請求的組成、Rider Profile 的出發錨點欄位、SB-6／SB-10 的逐項審查（Bindings 第 2.6 節不保留 Spec review） | DA；**acceptor**：詞彙表選哪些公路與地標（A-7）、C3 的執行與憑證（RB-3、RB-4）、Planner 額度（C-1） |
| **SIA-R1-G03** | AB-3 FR2 | 多檔上傳、合併、以內容去重複、行程清單接續、涵蓋度摘要、上傳檔的保存 | G-ING（併入 SPEC-UI0 phase acceptance 第 7 節 C-2、C-3 的保存契約條件與 CL-B1-11 第 4 項殘餘） | **可以開始 derivation 的部分**：去重複的鍵與上傳檔的保存位置與期間（first-run G-ING (1)(3)）由 DA 決定。**未 ready 的部分**：「與保留行程或被排除行程相同的檔案略過」所需的內容雜湊從哪裡來（(2)）；行程清單是否已記錄雜湊 NOT VERIFIED（需要讀私有資料） | DA；(2) 若需要開啟或雜湊保留行程的檔案 → **acceptor（RB-7）**；部署到騎士電腦以外的主機時 fail-closed 至 acceptor |
| **SIA-R1-G04** | AB-4 FR3 | SPEC-B1 有主要部分；介面與文件中「不稱為 P90 或百分位數」的用語與顯示沒有分配 | G-APP（介面的顯示與用語）、G-DOC（`README.md`、`DESIGN.md`；`README.md` 第 20 行仍寫 P50／P90 與 Google Maps 比較，屬 Scope Reduction 之前的描述，G-DOC 必須處理） | **未 ready**：G-APP 待 UI Delta Review；G-DOC 在功能接近完成時 derive | DA；**acceptor**：UI Delta Review；`README.md` 的 push 時機（RB-1） |
| **SIA-R1-G05** | AB-5 FR4 | 沒有任何分配：氣象署預報、民用暮光終、路段對應鄉鎮與預報時段、規則 3 的原因代碼 | G-SRC（預報、暮光終）、G-CON（WeatherSegment 的預報時段欄位、`R3_AREA_UNMAPPED`）、G-VAL（規則 3 的原因代碼）、G-RTE 的鄉鎮對應部分 | **未 ready／BLOCKED**：SB-3、SB-4 要等 C3；SB-5（C3）BLOCKED／NOT RUN；AB-5 須有至少一次以真實授權碼取得的預報回應紀錄，沒有授權碼時不得記為完成 | **acceptor**：氣象署授權碼（RB-3）、C3 的執行指示（US$3 已授權，RB-4）；之後 DA 依 C3 結果關閉 SB-3／SB-4 並 derive |
| **SIA-R1-G06** | AB-6 FR5 | 沒有任何分配：沿線加油站與檢查點的自動產生、依出發油量逐段檢查、封路情境的來源標示 | G-RTE（路線目錄、切段、檢查點、加油站投影、`ridden_share_pct`、RI-1～RI-3、`build_route` 的返工或取代）、G-SRC（加油站資料集、油量、路況情境檔）、G-VAL（油量規則） | **G-RTE：可以開始 derivation**（對 SPEC-R1 介面與 CL-B1-4 的依賴已成立；加油站投影規則由 DA 自己定義）；但整份不是 implementation-ready：鄉鎮對應屬 SB-3（等 C3），依 OC-1 §5 在 Blocker 關閉前不得納入 Tickets，DA 在 G-RTE 的 derivation record 中決定切分。**G-SRC 的加油站與路況部分未 ready**：政府資料開放平臺資料集的欄位與營業時間格式 NOT VERIFIED；OQ-2 油耗單位、OQ-3 加油時間屬 SB-10；情境檔格式未定義 | DA（投影規則、`routes` 的 Spec、情境檔格式、OQ-2／OQ-3 的審查）；實際取得公開資料集若需要網路或第三方帳號，依該 work item 的授權（第三方帳號屬 **acceptor**，RB-3） |
| **SIA-R1-G07** | AB-7 FR6 | SPEC-B1 只有規則 3 的範圍判定；規則 1、2、4、5、RuleResult 與原因代碼、計畫狀態、排序、候選評估、重新規劃、無可行解的說明、`validator` 的匯入限制測試沒有分配 | G-VAL（含 C-8-1）、G-CON（Plan Schema、RuleResult）、G-PLN（重新規劃的合法性） | **未 ready**：SB-10 的剩餘範圍（SD-2、SD-3、SD-4、SD-10、SD-11、SD-19；OQ-6）與規則 5 的道路寫法清單屬 DA，可以開始逐項審查；規則 3 的原因代碼與優先順序要等 C3（SB-3、SB-4） | DA；C3 的部分 → **acceptor**（RB-3、C3 的執行指示） |
| **SIA-R1-G08** | AB-8 FR7 | SPEC-UI0 只有 Skeleton；UI Delta Review 與正式的介面整合沒有分配 | G-APP | **未 ready**：derive 前須先有 acceptor 的 UI Delta Review 紀錄（`DESIGN.md` §9.6；SPEC-UI0 phase acceptance 第 12 節）；並依賴後端各模組 | **acceptor**（UI Delta Review，OC-1 §4.2）；之後 DA derive，納入 SPEC-UI0 phase acceptance 第 7 節的整合條件（C-1、C-2、C-3、Q-1、Q-1b、K9、Skeleton 不進產品路徑） |
| **SIA-R1-G09** | AB-9 知識庫 | 沒有任何分配：最小知識庫（關鍵字檢索、附出處）、公路與地標詞彙表、Planner 使用檢索結果的合成 Demo 情境與其執行紀錄 | G-KB（Demo 的實際整合併 G-PLN） | **Spec 的結構可以開始 derivation**（DA）；詞彙表的內容未 ready（acceptor 選擇）；AB-9 的實際執行 BLOCKED（C-1）。只有詞彙表或靜態知識庫不算 PASS；不擴張為進階 RAG | DA（Spec）；**acceptor**：公路與地標的選擇（A-7）、向老師確認知識庫深度（OC-1 §5，不擋開始）、C-1 的額度 |
| **SIA-R1-G10** | AB-10 NFR1～NFR5 | 三份 Spec 各有一部分；其餘模組的 NFR（每個時間、距離、機率可追溯到工具輸出；PlanResult／LLM 的隱私裁切與錨點代換；資料缺漏時 UNKNOWN；模擬資料的來源標記）與上游的公開地標保證沒有分配 | 不另立 derivation：**每一份之後的 derivation（G-RREQ、G-ING、G-RTE、G-SRC、G-VAL、G-PLN、G-KB、G-APP）MUST 在其 §7 明列自己的 NFR 部分**；PlanResult／LLM 的裁切屬 G-PLN／G-CON；公開地標保證屬 G-RREQ（TI-C16-3） | 隨各承接 derivation 的 readiness | DA；以真實資料核對裁切與錨點代換 → **acceptor（RB-7）**。`git ls-files` 檢查為 0 不等於這些產品路徑已驗證 |
| **SIA-R1-G11** | AB-11 實驗的程式與凍結 | SPEC-B1 的 `research-` 版本與保留行程拒絕、SPEC-R1 的嚴格模式機制之外：E1 Lite 的程式與分析計畫、E2 的題庫、Oracle、Runner、三組設定、凍結清單的檔案格式（含 TI-C14-5）與 12/5 凍結日的 commit 沒有分配 | G-E1、G-E2 | **G-E1 的 Spec 可以開始 derivation**（`DESIGN.md` §6.2 未寫定的分界、`suspect` 路段處理、路線引擎時間的選取規則、凍結清單格式、隔離的評估腳本，都屬 DA）；以真實行程執行未 ready。**G-E2 未 ready**：依賴 G-PLN（C3）與 G-SRC（SB-3、SB-4）；時間相依 Oracle 的取捨屬 DA。正式執行的結果不是 AB-11 的完成條件，本 record 不把它增列 | DA（Spec、Oracle 取捨）；**acceptor**：真實行程（RB-7）、保留行程的解封、E1 Lite／E2 的正式執行（OC-1 §4.2）、Pilot 與 E2 的支出（RB-4、D-5） |
| （G11 附帶）G-REG | — | 停等寬放以真實配速行程作留一趟的回歸檢查（SPEC-RESOLUTION-001 §1.6）。first-run §6 單列，沒有指定 AB；它屬哪一項 AB 的證據，在 derive 時由 DA 判定；不是 AB-11 的完成條件 | G-REG | **未 ready**：需要讀取配速行程 | **acceptor（RB-7）** |
| **SIA-R1-G12** | AB-12 文件 | 沒有任何分配：`README.md`、`DESIGN.md` 依實際狀態更新；Installation、How to Run 實際跑過；Architecture、Flowchart、行號 Pseudocode 與實作一致；Results 只寫真實執行所得 | G-DOC（承接 RV-1～RV-14、TI-C2R1F3-1、TI-C16-2、C-9-4、C-10-6、C-11-4、C-8-2、C-8-4、`DESIGN.md` 第 3 行的「尚未實作」、`README.md` 第 20 行） | **部分可以開始**：RV-6～RV-14 的同步時機條件自本 record 起成立，DA 可以把它們排入 G-DOC；Installation、How to Run 的實跑與 Results、Pseudocode 對照要等功能接近完成。Lane 在 derive 時依 Bindings 第 4 節判定 | DA；**acceptor**：push 與 `README.md` 公開的時機（RB-1）；對外繳交（RB-2） |
| **SIA-R1-G13** | AB-13 整合條件 | 三份 Spec 各自的 pytest、SIA、phase acceptance 之外：之後各 Spec 的同類條件與最後的 release gate 沒有分配 | 不另立 derivation：**每一份之後的 derivation MUST 在 §7 分配自己的 AB-13 部分**（pytest、SIA closure、DA phase acceptance）；最後一份未結 Spec 的 SIA 重新作全部分配核對（第 10.1 節第 3 點）；release gate 依 Bindings 第 5 節在合併前判定 | 隨各承接 derivation。SPEC-R1 的 AB-13 部分自本 record 起完成 | DA（分配與 traceability）；**acceptor**：release（合併進 `main`）、push、PR（RB-1） |

### 10.3 G-* derivation 的狀態總表（本 record 時點）

| 代號 | 狀態 | 本 record 時點的變化 | 下一個前提 | 由誰解除 |
| --- | --- | --- | --- | --- |
| G-CON | 未 ready | 無 | SB-10 剩餘範圍的逐項審查；SB-3／SB-4（C3） | DA；C3 → acceptor 的憑證與執行指示 |
| G-ING | 部分可以開始（(1)(3)） | 無（SPEC-UI0 的 C-2、C-3 條件已存在） | (2) 雜湊來源 | DA；(2) → acceptor（RB-7） |
| G-RREQ | 未 ready（DA 的部分可以開始） | SPEC-R1 的 CL-R1-2、CL-R1-5 介面已 phase-accepted | 詞彙表的 Spec 與內容 | DA；內容 → acceptor（A-7） |
| G-RTE | **可以開始 derivation**（不含 SB-3 部分） | 對 SPEC-R1 介面的依賴自本 record 起成立 | DA 定義加油站投影規則；鄉鎮對應等 C3 | DA；SB-3 → C3 |
| G-SRC | 未 ready／部分 BLOCKED | 無 | 氣象署授權碼；C3；資料集格式；情境檔格式 | acceptor（RB-3）；DA |
| G-VAL | 未 ready（DA 的部分可以開始） | 無 | SB-10 剩餘範圍；規則 5 道路寫法清單；SB-3／SB-4 | DA；C3 |
| G-PLN | BLOCKED | 無 | C3、PD-5 模型選定、C-1 額度、SB-6、「主程式」的模組對應 | acceptor（RB-3、RB-4、C-1）；DA |
| G-KB | Spec 結構可以開始；執行 BLOCKED | 無 | 公路與地標的選擇；C-1 | acceptor；DA |
| G-APP | 未 ready | 無 | UI Delta Review；後端模組 | acceptor；之後 DA |
| G-E1 | Spec 可以開始；執行未 ready | 無 | 分析計畫的未定項目、凍結清單格式（12/5 凍結） | DA；資料與執行 → acceptor |
| G-E2 | 未 ready | 無 | G-PLN、G-SRC；Oracle 規格 | DA；支出與執行 → acceptor |
| G-REG | 未 ready | 無 | RB-7 授權 | acceptor |
| G-DOC | 部分可以開始（RV 同步） | RV-6～RV-14 的時機條件自本 record 起成立 | 功能接近完成；實跑 | DA；push → acceptor |

**時程提醒（不是裁決）。** OC-1 §5 以 2026-12-20 為完成期限，`DESIGN.md` §9.3 的凍結是 12/5。上表中 G-SRC、G-PLN、G-E2、G-KB 的執行與 AB-1、AB-5、AB-9 的 PASS 都卡在 acceptor 的動作（氣象署授權碼、C3 的執行指示、C-1 的額度、詞彙表的選擇、UI Delta Review）；這些動作沒有到位時，相關 AB 依 OC-1 §3.2 記為 BLOCKED，不記為 PASS。

## 11. 是否改變 accepted 語義、boundary、authority、escalation

**是否改變 accepted 語義：否。**
- 工作一只依既有 evidence 判定 SPEC-R1 的 phase acceptance；沒有修改 OC-1 的 intent、scope、constraints 或 acceptance semantics，沒有修改 SPEC-R1 的 AC、invariant 或 gate。
- 第 7 節 NV-PY 的範圍判定只限定既有 evidence 的有效範圍（Python 3.11.2），不新增 Must、不改 `pyproject.toml`，屬治理 §5.3 第 2 類。
- 工作二只記錄缺口的 determination 與 routing；沒有新增、縮小或放掉任何 AB，沒有恢復 Scope Reduction，沒有引入 Should。第 10.2 節 G10、G13「每一份之後的 derivation MUST 在 §7 明列自己的 NFR 與 AB-13 部分」是 OC-1 §3.1「derivation record 必須寫明該 Spec 分配到哪幾項 AB」的直接適用，不是新要求。
- 沒有豁免任何 audit 或 gate；沒有 defer 任何 blocking finding；沒有改變高風險類別（R1-2 的 H-2／H-3／H-4、R1-3 的 H-2／H-3／H-4、R1-4 的 H-1／H-2／H-4 維持）或 assurance 要求。

**Boundary：在 OC-1 boundary 內**（`derivation-spec-r1.md` 第 3 節；OC-1 §2.1 第 1、2 項）。SIA R1／R2 範圍五都判定 traceability 與 boundary 符合；沒有 boundary finding。第 10 節列出的承接 derivation 都在 OC-1 §2.1、§4.1 明列的範圍內；它們各自的 boundary determination 在 derive 時作。

**需要 acceptor：** phase acceptance 本身不需要（治理 §2.1、§3.8 屬 DA）。之後的路徑需要的 acceptor 動作逐項列在第 8 節與第 10.2 節的 required authority 欄（C-1 額度、RB-3 憑證、C3 的執行指示、RB-7 私有資料、UI Delta Review、詞彙表的選擇、第一次真實路線請求、RB-1、RB-6）；本 record 不代行其中任何一項。

**Escalation：沒有**（第 2 節第 7 點）。第 10 節的 determination 由既有紀錄（OC-1 §3.1、first-run §4／§6、三份 derivation §7、兩份 phase acceptance）即可裁決，不構成 E-DA/D1；本 DA 先前的分配決定沒有被 FA ruling 或 Reviewer finding 推翻（SIA R1 明記 G01～G13 與 first-run §4、§6 一致），不構成 E-DA/D2。

## 12. 狀態（分開陳述，治理 §3.8）

- **SPEC-R1 phase acceptance**：**接受**（本 record）。orch-default §7 P10 的兩個條件（SIA closure、DA phase acceptance record 引用之）自本 record 起都存在。
- **SPEC-R1 的 Spec completion**：Spec 層級的 completion predicates 由 Orchestrator 依 record 核對，本 record 不代為宣告 run 的狀態更新。
- **Run completion**（`run-20261117-oc1-run2`）：本 record 不宣告。Run 的 terminus（三份 Spec 都完成 SIA closure 與 phase acceptance）由 Orchestrator 依紀錄判定。
- **OC-1 completion**：**未完成，最終 closure 不成立**。SIA-R1-G01～G13 open；AB-5、AB-6、AB-9、AB-12 沒有任何分配，其餘 AB 只有部分分配；AB-1、AB-5、AB-9 另須實際執行證據。
- **Release authorization**：沒有。合併進 `main` 由 acceptor 進行（RB-1）。
- **Issues #13～#16**：本 record 不變更。

## 13. 受影響的 work items 與 evidence

- run record §5 frontier 第 12 列（SPEC-R1 SIA → DA phase acceptance）：本 record 是其 phase acceptance。
- **SPEC-B1、SPEC-UI0**：不受影響。本 pytest 包含兩者的全部測試，仍通過；`app/` 自 SPEC-R1 BASE 起沒有變更。本 record 不因其他 Spec 的後續 delta 自動失效，也不為它們背書。
- **之後的 derivations**（第 10 節）：G-RTE 以 R1-4 的共用介面（`get_route` 與其回傳的採用路線或路線錯誤代碼）為輸入；G-RREQ 以 CL-R1-2、CL-R1-5 的輸入形式為介面，並承接 TI-C14-1、TI-C16-3、TI-C165-1；G-APP 承接 TI-C15-1、TI-C16-2；G-E2 承接 TI-C14-5；G-DOC 承接 RV-1～RV-14、TI-C2R1F3-1。之後任何修改 `src/moto_copilot/routing/`、`contracts/` 或 `ingest/geometry.py` 的 Ticket，須在其 self-verification 中保持 SPEC-R1 的測試（含 `tests/test_integration_r1.py`）全數通過；只有出現新的 integration-level evidence 顯示 SPEC-R1 的 invariants 被破壞時，才由 DA 判定是否需要重新驗證本 Spec。
- **之後同一 OC-1 最後一份未結 Spec 的 SIA**：MUST 重新作全部 derived Specs 的分配涵蓋核對（第 10.1 節第 3 點）。
- **Completion report（交 acceptor）**：第 8 節的 NV-1、NV-PRIV、C-14-6、`efbffe8`、A-ACC-2，以及第 10.2 節 required authority 含 acceptor 的各項。

## 14. 執行紀錄

本 DA 讀了 Bindings m3 第 2、4、5、7 節；治理 §1.2、§3.8、§4.7、§5.3；orch-default v2.2 的 phase acceptance 與 P9／P10 段；OC-1 全文；`derivation-spec-r1.md` 全文；first-run derivation 全文；SIA R1、R2 records 全文；run record 第 1～5 節、事件 107～113 與 §8.1 的 #13～#16；`worklog/spec-r1-integration.md` 全文；`tests/test_integration_r1.py` 全文；SPEC-B1、SPEC-UI0 phase acceptance（格式與第 6～12 節）；c131、c141、qalt1、c151、c161、c2r1f3、c165 中與 SIA、phase acceptance、tracked items 有關的段落；FA `ruling-20261118-issue16-c1.md` 中與 DA 的關係；高風險類別 record 的目錄與第 5 節相關行；SPEC-001 §11.1 的 Spec Blockers 表；`HANDOFF-2026-11-17.md` 第 3.3、3.4 節；`README.md` 第 20 行；`DESIGN.md` 第 3 行；`pyproject.toml` 的 `requires-python`。執行了第 6 節所列的 pytest、contracts CLI、`git` 核對、Issue 原文與 audit records 的 SHA-256，以及限定在 `src/moto_copilot/routing`、`src/moto_copilot/ingest/geometry.py`、`tests/test_integration_r1.py` 的文字搜尋。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env` 或任何憑證，沒有讀或執行 `experiments/` 下的任何檔案，沒有讀保留行程，沒有呼叫 GitHub，沒有網路請求；沒有修改程式、測試、worklog、Issue、`DESIGN.md`、`docs/spec/` 或其他 record；沒有派工任何 subagent；沒有 commit。

Decision: SPEC-R1 v1 phase acceptance — ACCEPT（引用 SIA closure `audit/spec-SPEC-R1-c1-r2.md`，subject `ca50bc9`）。SIA-R1-G01～G13 全部屬實，逐項承接與 required authority 見第 10 節；OC-1 的最終 closure 在這些缺口處理前不成立。不改變 accepted 語義；在 OC-1 boundary 內；沒有 escalation；不是 release authorization。
