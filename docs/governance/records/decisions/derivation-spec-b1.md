# Derivation record — SPEC-B1：停等寬放與規則 3 的範圍判定

| 欄位 | 內容 |
| --- | --- |
| Record ID | `derivation-spec-b1`（v1，2026-11-17） |
| Spec | **SPEC-B1 v1**＝第 2 節列出的既有段落（commit `873e37a` 的內容）＋本 record 第 4 節的 DA clarifications 與第 5 節的 Ticket 定義 |
| 決定者 | Design Authority（`gov-design-authority`；binding 由派工者核對） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 跨 Spec 的決定 | [`decision-20261117-oc1-first-run-derivation.md`](decision-20261117-oc1-first-run-derivation.md)（BD-1～BD-5、AB 分配總表、run 的順序） |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| Tickets | #7（B1-1）、#9（B1-2）、#10（B1-3）、#11（B1-4）、#8（B1-5），原樣引用（雜湊見 decision record BD-3） |

## 1. 依據的 Outcome Contract 條款

- OC-1 §2.1 第 1 項：Must 模組 `ingest`、`pace`、`validator`（規則 3 的範圍判定）、`tests`。
- OC-1 §2.1 第 2 項：`contracts` 更新到 v0.3（停等寬放的部分）；既有的 Spec 與 Issues #7–#11 由 Design Authority 引用。
- OC-1 §2.1 第 3 項：`ingest`、`pace` 與 `contracts` 的 Spike 依 Spec 收編或返工。
- OC-1 §2.3：私有資料、測試只用合成資料、保留行程隔離（RB-7）。
- OC-1 §3.1：AB-3、AB-4、AB-7、AB-10、AB-11、AB-13 的部分（第 7 節）。
- OC-1 §4.1：實作、self-verification、targeted correction、審查、修正至完成。
- OC-1 §5：SB-2、SB-9 已關閉；本 Spec 不碰 SB-3、4、5、6、10 的範圍。

## 2. Spec 的內容（引用）

| 來源（commit `873e37a`） | 引用的段落 |
| --- | --- |
| `DESIGN.md` §5 | 共通規則（ID 列除外，ID 的放寬屬 SPEC-R1）；契約 1、契約 3、契約 4 的欄位表與不變條件中標示「v0.3（停等寬放）」的部分，以及這三份契約既有的不變條件；「凍結之前不產生保留行程的列」一段 |
| `DESIGN.md` §6.1 | 時間的定義、算式、不重複計算的四條規則、餘裕係數的規則與留一趟的程序、分級門檻的規則、餘裕係數隨配速表一起重建、研究用與使用者的 Profile 分開；用語限制 |
| `docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` | §1.1–§1.4、§1.6（SB2-T1～SB2-T13，其中屬於本 Spec 的見第 5 節）；§3.1 判定規則；§3.5 測試 SB9-T1～SB9-T5 |
| `docs/spec/SPEC-001-plan-schema.md` | 4.8 的 `in_rule3_range` 定義；5.2 規則 3 各列的「結果」與「條件」欄（不含原因代碼的命名與優先順序）；5.4 的「規則 3 的範圍」「安全餘裕係數」「停等寬放」三列 |
| `docs/grill/g1-grill-input.md` | Q18（單向行程的最後 20%） |
| GitHub Issues | #7、#8、#9、#10、#11 的內文（BD-3 的雜湊版本） |
| `docs/ticket/BATCH-1-scoped-tickets.md` | 第 1 節共通規則、第 2 節依賴關係 |

**不屬於本 Spec**（各 Issue 的排除範圍之外，另外明列）：ID 樣式的放寬與契約 2（SPEC-R1）；規則 3 的原因代碼、RuleResult 與 WeatherSegment 的 schema（SB-3、SB-4、SB-10）；凍結清單的格式與 E1／E2 腳本對版本的檢查（SB2-T10 的實驗部分、SB2-T12）；路線目錄的類別隨門檻重算（RI-1～RI-3，屬 `routes`）；以真實行程執行的回歸檢查（decision record G-REG）。

## 3. Boundary determination

**在 OC-1 boundary 內。** 依據：
- 範圍：全部屬於 OC-1 §2.1 第 1–3 項明列的模組與契約更新；沒有新增 Must 或 Should。
- 語義的來源：停等寬放（SB-2，acceptor 2026-11-15 批准 M2，O-3、Q-4 核准推導細節）與規則 3 的範圍（SB-9，方案 A）都是已關閉的 Blockers，內容是 acceptor 的裁決。
- 本 Spec 引用的 SPEC-001 段落（4.8 的 `in_rule3_range`、5.2 規則 3 的結果條件、5.4 三列）的內容由 SB-9 與 SB-2 的裁決定案（SD-37 的狀態欄亦同），不屬於 SB-10 的剩餘範圍（decision record BD-2）。#8 的排除範圍已把原因代碼與 schema 排除。
- 限制：只用合成資料；不讀保留行程；不讀 `data/`。
- Ticket 的建立依據：BATCH-1 是 acceptor 2026-11-15 的 Q-5 裁決核准的 Scoped Tickets；在 OC-1 下以引用方式成為 derived contracts（Bindings 第 8.1 節）。

## 4. DA clarifications（SPEC-B1 的一部分）

這些是既有來源只有一種合理解讀而尚未寫下、或需要固定以免 Tickets 之間不一致的設計細節（治理 §5.3 第 2 類），不改變任何 Issue 的 AC。

**CL-B1-1（全部 Tickets）共通規則的解讀。** 依 decision record BD-3：修改既有測試的理由寫在 worklog；規格沒有寫的事依治理 §2.4 route。Executor 不讀取、不列出、不搜尋 `data/`，不執行 `experiments/` 下任何腳本；CL-B1-4 引用的 `experiments/` 原始碼只能閱讀，不得執行。測試只用合成資料。

**CL-B1-2（#7）契約版本字串。** `CONTRACT_VERSION` 在 #7 不改為 `"0.3"`：v0.3 的 ID 放寬與契約 2 在 SPEC-R1 的 R1-1，那張 Ticket 完成時才改。避免在 v0.3 尚未完整實作時宣稱 v0.3（H-3）。契約 4 表頭 `margin_coeff` 的下限改為 0.05 屬 #7。

**CL-B1-3（#9）停等事件的細節。**
1. 停止步的判定不變：低於 3 km/h，或記錄中斷超過 10 秒而且位移不到 50 m。記錄中斷超過 10 秒而且位移 50 m 以上的步仍算移動（現行做法），不屬於停等事件。
2. 停等事件依**整個事件**的長度分類；事件的秒數分配給各步所在的路段。事件跨過路段邊界時，兩個路段各自計入自己那部分的秒數，分類依整個事件的長度。
3. 疑似 GPS 假停留（事件不到 3 秒）的秒數計入該步所在路段的 `moving_time_s`，不增加 `length_m`。
4. 「重建流程」指 `python -m moto_copilot.ingest` 這類依行程清單批次產生衍生路段表的流程。它只開啟清單中 `trip_role` 是 `pace` 的檔案；清單中其他角色（`holdout`、被排除的行程或任何其他值）的項目不開啟、不產生列。呼叫者明確指定的行程代號中有非 `pace` 的角色時，在開啟任何檔案之前拒絕（明確的錯誤）。
5. 找不到行程清單時，重建流程拒絕執行，不開啟任何 GPX，**不再自動建立「全部暫定為 `pace`」的清單**（現行 `_load_or_create_manifest` 的行為要移除）。理由：行程清單是 `trip_id` 與角色的唯一來源（SPEC-001 §2），沒有清單就無法得知哪些是保留行程，自動建立會在凍結前開啟保留行程的檔案（DESIGN §5 契約 1 之後的說明；SB2-T11）。
6. `ingest_version` 換成新的值（任何不同於 `ingest-spike-0.2` 的字串）；3 秒、180 秒是 `IngestParams` 的參數。

**CL-B1-4（#10）配速表的操作定義。** 以下以參考實作為準，Executor 只閱讀不執行：分級門檻 `experiments/cr01_checks/data_common.py` 的 `tercile_thresholds`；分類邊界 `src/moto_copilot/ingest/segments.py` 的 `_category`；餘裕係數 `experiments/cr01_checks/data_sb2_stop_allowance.py` 的 `margin`。
1. **可計時的路段**：表頭 `trip_ids` 的行程中，`trip_role = pace`、`quality = ok`、`curvature_deg_per_km` 不是 `null`、`moving_time_s` 大於 0 的列。
2. **分級門檻**：可計時路段的 `curvature_deg_per_km` 由小到大排序，n 是個數；`c1_max = round(v[n // 3] / 5) × 5`，`c2_max = round(v[2n // 3] / 5) × 5`（Python 的 `round`，與參考實作相同）。沒有任何可計時路段時，不建立配速表：回報明確的錯誤，不寫檔。
3. **分類**：`curvature < c1_max` 是 C1；否則 `curvature < c2_max` 是 C2；其餘是 C3。配速表依這組門檻重新分類，不使用衍生路段表中的 `seg_category` 與 `category_scheme`（契約 1 的欄位不變，只是 `pace` 不依賴它們）。
4. **`category_scheme` 的格式**：`curv-tercile-<c1_max>-<c2_max>`，兩個值寫成整數（例如 `curv-tercile-80-250`）。格式固定，之後 `routes` 要由它還原門檻（RI-2）。
5. **`stop_ratio`**：每個類別 Σ`short_stop_time_s` ÷ Σ`moving_time_s`，只用可計時路段；該類別路段數少於 `min_segments`（`speed_kmh` 為 `null`）時為 `null`。`min_segments` 是呼叫者提供的參數。
6. **留一趟**：只對表頭 `trip_ids` 的行程。每一折以其餘行程依第 2、3 項重算門檻並分類，以同一個 `min_segments` 建立該折的配速；被拿掉的那一趟依該折的門檻分類它的可計時路段。被拿掉的那一趟沒有可計時路段，或它的可計時路段中有任何類別在該折的 `speed_kmh` 是 `null`，這一折不計入。計入的折：實際＝Σ(`moving_time_s` + `short_stop_time_s`)，預測＝Σ `length_m` ÷ `speed` × (1 + `stop_ratio`)，`r` ＝ 實際 ÷ 預測 − 1。
7. **`margin_coeff`**：計入的折數少於 8 時是 0.20，`margin_basis = default`。否則 `r` 由大到小排序，取第三大的 `r₃`，`margin_coeff = max(0.05, ⌈max(r₃, 0) ÷ 0.05⌉ × 0.05)`，取到小數兩位（浮點誤差的處理與參考實作相同），`margin_basis = loo_rule`。
8. **版本與檔案**：配速表寫到呼叫者提供的目錄，一個版本一個檔案，檔名含 `pace_version`；沒有寫在受版控路徑內的預設位置（測試用暫存目錄）。寫入前若同一版本的檔案已存在，回報錯誤，不覆寫；既有檔案不修改、不刪除。自動編號時，取該開頭現有的最大編號加 1，至少兩位數補零（`user-01`、`user-02`…）；`research-` 版本允許由呼叫者指定編號，已存在時回報錯誤（SB2-T13）。
9. **選用的版本**：目錄中 `built_at` 最晚的 `user-` 版本；`built_at` 相同時取編號較大者。沒有 `user-` 版本時，回到凍結清單的 `research-` 版本，屬凍結清單的範圍，不在 #10。
10. **保留行程的拒絕**：`trip_ids` 中有任何行程在衍生路段表中不是 `pace`（或不在表中而無法確認角色）時，在計算之前拒絕。

**CL-B1-5（#11）ETA。** ETA 表頭的 `margin_coeff` 一律取自所用配速表的表頭；呼叫者另外提供的值與表頭不同時回報錯誤，不採用。`stop_ratio` 取自同一份配速表。路線目錄的 `category_scheme` 與配速表不同時的處理（RI-1～RI-3）不在 #11，是 `routes` 的整合條件；SPEC-B1 的結案不得宣稱已處理這種情形。

**CL-B1-6（#8）規則 3 的範圍判定。**
1. 位置：`src/moto_copilot/validator/` 之下的一個模組（DESIGN §9.1）。純函式；只依賴標準函式庫；不匯入 `planner`、任何 LLM client、`sources`、`routing`、`routes`、`pace`。不建立其他規則的骨架。
2. 輸入：依序的路段累計距離（每個路段終點的累計距離，遞增）、`trip_type`（`one_way`／`round_trip`）、去程的段數 k、每個路段的降雨機率分類（`LOW`、`MEDIUM`、`HIGH_ALERT` 或「沒有」）。輸出：與路段同序的「是否在範圍內」清單，以及 `PASS`／`FAIL`／`UNKNOWN`。
3. 單向行程：總長 T；路段的終點累計距離大於 0.8 × T（嚴格大於）就在範圍內。終點剛好等於 0.8 × T 的路段沒有跨入。k 不使用。
4. 來回行程：`seg_index ≥ k` 的路段在範圍內；k 必須滿足 0 < k < 路段數，否則回報明確的錯誤。
5. 結果：範圍內有任何 `HIGH_ALERT` 是 FAIL；否則範圍內有任何「沒有」是 UNKNOWN；否則 PASS。範圍以外的路段不影響結果。

**CL-B1-7（全部）用語。** 新增或修改的程式說明、錯誤訊息與 worklog 不得把 `eta_safe`／保守估計稱為 P90 或任何百分位數；降雨機率 ≥ 70% 不稱為官方警特報（root `CLAUDE.md`）。

## 5. Tickets

共通的充分證據要求（每張 Ticket 都適用）：
- E-1：`.venv/Scripts/python.exe -m pytest -q` 的完整輸出記在 worklog，全數通過。
- E-2：worklog 逐條列出 Ticket 的每一項 AC（含本 record 的 clarifications 所涉者）對應的測試名稱與結果。
- E-3：測試資料全部是合成的，worklog 寫明來源；diff 中沒有真實座標、軌跡、騎乘時間或行程清單。
- E-4：因契約改版而修改的既有測試，在 worklog 逐項列出理由。
- E-5：對標示的高風險類別，Executor 依 `decision-20261117-high-risk-categories.md` 第 5 節的核對範圍作 self-verification 並記錄；independent audit 依同一節的最低核對範圍。

| Ticket | 範圍與 AC | 本 Spec 的補充 | 依賴 | AB | 高風險類別 |
| --- | --- | --- | --- | --- | --- |
| **#7 B1-1** `contracts`：契約 1、3、4 的 v0.3 欄位與不變條件 | Issue #7 的範圍與 7 項 AC（對應 SB2-T3、T4、T5、T8、T9 的契約部分） | CL-B1-1、CL-B1-2 | 無 | AB-4、AB-10、AB-13 的部分 | **H-3**（`pace_version` 的 `research-`／`user-` 樣式是兩種配速表分離的機制之一，判定 3.3 第 1 項）、**H-4**（契約 4 的 `unknown` 不變條件是 ETA 缺漏不補值的防線；無法確定時記為涉及，判定程序第 2 項） |
| **#9 B1-2** `ingest`：停等事件與三種分類 | Issue #9 的範圍與 4 項 AC（SB2-T1、T2、T3、T11）；另加 CL-B1-3 第 4、5 項的測試：清單中非 `pace` 的項目不開啟、指定代號含非 `pace` 時拒絕、沒有清單時拒絕（以合成的清單與檔案驗證，並以測試確認被拒絕的檔案沒有被開啟） | CL-B1-1、CL-B1-3 | #7 | AB-3、AB-10、AB-11、AB-13 的部分 | **H-2**（開啟 GPX 與行程清單的程式，判定 3.2 第 1 項）、**H-3**（保留行程的拒絕，判定 3.3 第 1 項）、**H-4**（移動時間與 `quality` 的計算路徑，判定 3.4 第 3 項） |
| **#10 B1-3** `pace`：配速表的停等比例、分級門檻、餘裕係數與版本 | Issue #10 的範圍與 8 項 AC（SB2-T4、T7、T9、T10 的 `pace` 部分、T13）；另加：`category_scheme` 符合 CL-B1-4 第 4 項的格式；固定的殘差清單在計入 7 折與 8 折時分別得到 0.20／`default` 與依第 7 項算出的值；沒有可計時路段時不建立、不寫檔 | CL-B1-1、CL-B1-4 | #7、#9 | AB-3、AB-4、AB-10、AB-11、AB-13 的部分 | **H-2**（決定衍生輸出寫到哪裡，判定 3.2 第 1 項）、**H-3**（保留行程拒絕、`research-`／`user-` 分離、不覆寫，判定 3.3 第 1 項）、**H-4**（配速為 `null` 的處理與預設值，判定 3.4 第 3 項） |
| **#11 B1-4** `pace`：ETA 的停等寬放與安全餘裕 | Issue #11 的範圍與 4 項 AC（SB2-T5、T6、T8、T9 的 ETA 部分）；另加：呼叫者提供的 `margin_coeff` 與配速表表頭不同時回報錯誤 | CL-B1-1、CL-B1-5、CL-B1-7 | #7、#10 | AB-4、AB-10、AB-13 的部分 | **H-3**（保守估計的用語，判定 3.3 第 4 項）、**H-4**（ETA 的 `unknown` 與缺漏處理，判定 3.4 第 3 項） |
| **#8 B1-5** 規則 3 的範圍判定（確定性測試） | Issue #8 的範圍與 5 項 AC（SB9-T1、T2、T3 只驗結果、T4、T5）；另加：單向行程終點剛好在 0.8 × T 的路段不在範圍內；來回行程 k 不合法時回報錯誤；模組不匯入 CL-B1-6 第 1 項列出的模組（以測試或靜態檢查驗證） | CL-B1-1、CL-B1-6 | 無 | AB-7、AB-13 的部分 | **H-4**（規則結果的計算，判定 3.4 第 1 項）。不涉及 H-3：函式的輸入是分類，不碰 70% 門檻的宣稱 |

每張 Ticket 的 AC 都引用 Issue 的原文；本表的「另加」是本 Spec 的 clarifications 帶出的驗收條件，屬 SPEC-B1 的 verification contract（治理 §3.4），Executor 不得自行改變。

## 6. Spec 層級的驗收（Spec Integration Audit 的範圍）

| 編號 | 條件 | 證據 |
| --- | --- | --- |
| SB1-AC1 | 五張 Ticket 都依 orch-default §7 結案 | audit records 與 worklogs |
| SB1-AC2 | 跨 Ticket 的整合：一條合成軌跡（含 1 秒重複位置、短停留與長停留）經 `ingest` 產生衍生路段表（通過契約 1 v0.3 的檢查）→ 以多趟合成行程建立 `user-` 配速表（通過契約 3 v0.3；`category_scheme` 依 CL-B1-4）→ 在一條 `category_scheme` 與配速表相同的合成路線上計算 ETA（通過契約 4 v0.3，含不變條件 8、9）。以一個整合測試表現 | 測試與 pytest 輸出 |
| SB1-AC3 | `contracts` 的 `validate_dataset` 對更新後的模擬資料集沒有違反；全部測試通過 | pytest 輸出 |
| SB1-AC4 | 規則 3 的範圍判定與 SPEC-RESOLUTION-001 §3.1 的判定表一致，並與 `pace` 沒有匯入關係 | 測試與匯入檢查 |
| SB1-AC5 | 沒有任何程式路徑會在重建時開啟非 `pace` 的行程檔案；沒有自動建立暫定清單的路徑 | 程式與測試 |
| SB1-AC6 | 新增的文字沒有 P90、百分位數或官方警特報的宣稱 | diff |

已知不在本 Spec 涵蓋內、SIA 不得記為已涵蓋：RI-1～RI-3；回歸檢查（G-REG）；凍結清單與 E1／E2 腳本的版本檢查；規則 3 的原因代碼。

## 7. 分配到的 Outcome Contract acceptance boundary 部分

| AB | 本 Spec 分配到的部分 |
| --- | --- |
| AB-3 | 由歷史 GPX 重建配速表的計算核心：停等事件的分類、`user-` 版本的建立與選用。不含上傳、合併、去重複、涵蓋度摘要與介面 |
| AB-4 | 典型估計與保守估計的計算（停等寬放、餘裕係數），以及程式文字不稱 P90。介面與文件的用語屬之後的 Spec |
| AB-7 | 規則 3 的範圍判定與三值結果（不含原因代碼、RuleResult、其他規則） |
| AB-10 | NFR4：ETA 為 `unknown` 時不輸出時間、不補值；NFR2：測試只用合成資料；保留行程不進重建 |
| AB-11 | 產品端的凍結機制：`research-` 版本不覆寫、保留行程拒絕。不含凍結清單與實驗程式 |
| AB-13 | 本 Spec 的 pytest 全數通過、Spec Integration Audit closure、Design Authority phase acceptance |

## 8. 受影響的工作

- `src/moto_copilot/contracts/`、`ingest/`、`pace/` 的 Spike 程式依本 Spec 返工；`ingest/__main__.py` 的暫定清單行為移除（CL-B1-3 第 5 項）。
- `tests/` 的既有測試與 `tests/fixtures/contract_v02/mock_dataset.json` 的 `pace_version` 會改；理由記在 worklog。
- `routes/` 的 Spike 不動；它建立的路線目錄仍用 Spike 的 `category_scheme`，與新配速表不相容的處理屬 RI-1～RI-3（之後的 `routes` Spec）。
- 之後的 `routes` Spec 依賴 CL-B1-4 第 4 項的 `category_scheme` 格式。
- `DESIGN.md` 的實作狀態陳述在本 Spec 結案後過時，由 AB-12 的文件工作處理。

## 9. Implementation readiness

**Implementation-ready。** 每張 Ticket 都有明確的範圍、AC（Issue 原文加第 5 節的補充）、依賴與證據要求；原本需要 Executor 猜測的細節（停等事件跨路段、暫定清單、門檻的位置與捨入、留一趟的預測集合、餘裕係數的算法、`category_scheme` 的格式、版本檔案、規則 3 的邊界）已由第 4 節固定。沒有依賴未關閉的 Spec Blocker。
