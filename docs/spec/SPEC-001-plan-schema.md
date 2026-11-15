# SPEC-001 Plan Schema、規則輸出與來源證據

> 狀態：**Draft v0.2（CR-01，2026-11-15）。** 依 [CR-01](../cr/CR-01-proposal-alignment.md) 第 11–16 節修訂。仍是草稿：**專題負責人在 2026-11-15 的審查處置中沒有批准凍結**；尚未建立 Tickets；尚未實作。v0.1 是 CR-01 之前的版本，保存在 Git 基準點 `9b3af99`。
> 輸入：[DESIGN.md](../../DESIGN.md)（CR-01 修訂中：§4、§5 資料契約 v0.3（Draft，CR-01）、§6.1、§8、§9.1、§9.2）、[G1 決議](../grill/g1-grill-input.md)（Q1–Q32、第 8 節與第 11 節的 CR-01 重開紀錄）、G3 凍結的 UI 文件（[UI_DESIGN](../ui/UI_DESIGN.md)、[UI_FLOW](../ui/UI_FLOW.md)、[UI_ACCEPTANCE](../ui/UI_ACCEPTANCE.md)、[G3 Audit Report](../ui/G3_AUDIT_REPORT.md) 第 7 節）與 [UI_CR01_DELTA](../ui/UI_CR01_DELTA.md)、[CR-01](../cr/CR-01-proposal-alignment.md) 第 11–16 節與它的附錄。
> 這份 Spec 把 G1 第 8 節的「邏輯欄位清單」定成欄位名稱與型別，並固定規則的指引文字與來源證據的型別。v0.2 只修改 CR-01 影響的部分，新增的欄位都對應 CR-01 第 12 節的 Must；其他內容和 v0.1 相同。
> 2026-11-15 依兩份事後審查（[review_1_post](../cr/CR-01-appendix/review_1_post.md)、[review_2_post](../cr/CR-01-appendix/review_2_post.md)）與 [lead 的處置](../cr/CR-01-appendix/lead_dispositions.md)修正；版本仍是 v0.2 草稿。
> 2026-11-15 審查處置：專題負責人已對 P-1 至 P-11 作出裁決，另提出五項修正；這份 Spec 已同步，版本仍是 v0.2 草稿。裁決與尚未解決的 Spec Blockers 在第 11.1 節。CR-01 的技術檢查：C1 是 PASS，C2 是 FAIL，C3 是 BLOCKED／NOT RUN，C4 是 FAIL，追加的 C4b 是 PASS。標為「草案」或「提案」的內容是這份 Spec 為了回應裁決而起草的，還沒有經專題負責人確認。
> 依 P-9 的裁決：G1 沒有重開的決議（Q14、Q25、Q29、Q30）所需要的欄位與原因代碼 `reason_code` 都維持必填；`time_limit_basis` 與 `overrun_s` 延後，這一版的結果不含這兩個欄位。

## 1. 目的與範圍

**涵蓋。**

- 規劃請求與規劃結果的結構（Plan Schema）：欄位名稱、型別、可否為空、由誰填寫。
- 規則 1–5 的輸出：結果、原因分類、原因代碼、固定的人工確認指引。
- 來源證據的型別與時間欄位，包含本地衍生資料與本地設定檔（G3 裁決 N6）。
- 由這些欄位推導的確定性規則：計畫狀態、排序、候選評估、代表性失敗候選、時間餘裕、規則 5 的關卡。
- 路線請求、路線摘要與路線錯誤的結構（CR-01）。
- 路線快照的欄位（4.14）與路線模組的確定性規則（7.11）。路線快照與路線摘要的欄位定義由這份 Spec 負責，DESIGN.md §5 只寫摘要。
- 驗收與測試規格。

**不涵蓋。**

- 衍生路段表、路線目錄、配速表、ETA 輸出：由資料契約定義，這份 Spec 只引用。CR-01 把契約改為 v0.3（Draft，CR-01）：契約 2（路線目錄）的欄位有變更；`route_id` 與 `checkpoint_id` 的格式放寬，會連帶影響契約 1 與契約 4 中引用這兩個 ID 的格式檢查；契約 1、3、4 的欄位與不變條件不變。
- 路線快照的實體檔案格式（由 Tickets 決定，不得改變 4.14 的欄位名稱、型別與語意）、路線引擎的呼叫方式、公路與地標詞彙表的內容、歷史 GPX 的匯入與 Profile 的涵蓋度摘要：由 DESIGN.md 與各自的規格定義。這份 Spec 只規定它們在規劃結果中留下哪些欄位。
- 各資料工具的內部做法（怎麼查預報、怎麼讀加油站快照）、知識庫的內容、提示詞。
- E2 的題庫、Oracle 與 Runner：另有規格（DESIGN §6.3）。這份 Spec 只規定 E2 三組共用同一個結果結構。
- Streamlit 的版面：見 G3 凍結的 UI 文件與 [UI_CR01_DELTA](../ui/UI_CR01_DELTA.md)（提案，待專題負責人確認）。第 8 節只列出畫面讀哪些欄位。
- Should 與 Won't 的項目（地圖、下載、TDX、氣象署警特報、騎士記憶）沒有欄位。目標路線 GPX 的介面上傳是 Should；這份 Spec 只定義以檔案路徑提供時的欄位。

第 10 節列出這份 Spec 自己做的決定。第 11.1 節是專題負責人的裁決與尚未解決的 Spec Blockers，第 11.2 節是需要審查者回答的問題。

## 2. 共通規則

沿用資料契約的規則，另外補上 Plan Schema 需要的型別。

| 項目 | 規則 |
| --- | --- |
| 型別 | 契約已有的 `string`、`int`、`float`、`datetime`、`enum`、`list`；新增 `bool`、`date`（`YYYY-MM-DD`）與巢狀的 `object` |
| 命名 | 小寫加底線。單位寫在字尾：`_s` 秒、`_m` 公尺、`_pct` 百分比（0–100）、`_l` 公升 |
| 時間 | `datetime` 是帶 `+08:00` 的 ISO 8601 字串（Asia/Taipei）。沒有時區位移的時間無效 |
| 缺值 | `null` 表示不知道或無法計算，不得用 0、−1 或空字串代替。遇到 `null` 要往下傳遞為 UNKNOWN，不得補值（NFR4） |
| 狀態用語 | 固定用語一律大寫：`PASS`／`FAIL`／`UNKNOWN`、`FEASIBLE`／`CONDITIONAL`／`INFEASIBLE`。其他 `enum` 用小寫。CR-01：`COMPLETE`／`INCOMPLETE` 不再使用（見 4.4） |
| ID | `route_id`、`checkpoint_id`、`plan_id` 沿用契約；`route_id` 與 `checkpoint_id` 的格式依契約 v0.3 放寬。P-3 的裁決：確切格式在 Spec 凍結前定義，不留給 Tickets；`trip_id`（`T` 加三位數字）與示範路線的 `R01`、`R02` 不變。**以下是提案，待專題負責人確認（SB-1）。** `route_id` 有三種：`R` 加兩位數字（示範路線 fixture）；`RS-` 加 10 個小寫十六進位字元（路線引擎的路線，十六進位的部分和它的 `snapshot_id` 相同）；`RG-` 加 10 個小寫十六進位字元（目標路線 GPX，取自內容雜湊的前 10 碼）。樣式 `^(R\d{2}\|R[SG]-[0-9a-f]{10})$`。`checkpoint_id` 是 `<route_id>-CP` 加兩到三位數字，依路線順序由 01 起編，樣式 `^(R\d{2}\|R[SG]-[0-9a-f]{10})-CP\d{2,3}$`。`snapshot_id` 是 `SN-` 加 10 個小寫十六進位字元（4.14；7.11 第 1 項）。`plan_id` 在同一份結果中唯一。`evidence_id` 的格式是 `EV-` 加大寫英數字與連字號 |
| `trip_id` | 行程清單是 `trip_id` 的唯一來源。新上傳的歷史 GPX 以內容去重複後接續編號；已指定的 `trip_id` 不變動。實驗腳本一律讀清單，不自行編號。保留行程是以 `trip_id` 的清單凍結的，編號一變清單就會指向別的行程 |
| 隱私 | 結果中不得出現座標、路線的折線、原始 GPX 的時間或行程代號以外的行程資訊（NFR2）。位置以 `route_id`、`checkpoint_id` 與 `seg_index` 表示。CR-01：結果可以出現道路名稱，以及公路與地標詞彙表中公開地標的名稱與代號；不得出現住家位置。目標路線 GPX 在結果中只記錄內容雜湊，不記錄完整路徑與檔名（路徑可能含使用者名稱，檔名可能含日期）。從出發錨點出發的結果能不能進版控，依 DESIGN.md 的隱私規則 |
| 對語言模型的隱私 | 語言模型的 API 也是第三方。送給語言模型的只有：通過本機輸入保護（7.12）的行程文字、結構化的條件，以及不含座標與軌跡點的工具輸出（含計畫路線的道路名稱）。不送原始 GPX、逐趟的騎乘資料與住家位置。路線快照的折線（4.14）也不送。E2 的三組適用同一條規則。本機輸入保護只比對樣式；這份 Spec 不宣稱行程文字一定不含私人地址 |
| 版本 | 每份結果帶 `plan_schema_version`，這一版是 `"0.2"` |

「填寫者」一欄的意思：**表單**是使用者在 Trip Planner 輸入的值；**Planner** 是 LLM 產生的結構化資料；**主程式**是確定性的程式，數值都從工具輸出複製；**Validator** 是確定性的規則判定，不含 LLM。

## 3. 物件總覽

```text
PlanResponse = ClarificationRequest | PlanResult

PlanResult
├── adopted_conditions : PlanRequest
│     ├── route_request   : RouteRequest → origin, destination, via[] : PlaceRef   (CR-01)
│     ├── breaks[]        : BreakArrangement
│     ├── refuel_stops[]  : RefuelStop
│     └── conflicts[]     : ConflictNotice
├── route                : RouteSummary       (CR-01)
├── route_error          : RouteError         (CR-01)
├── evaluation           : Evaluation         (CR-01, replaces SearchStatus)
├── candidates[]         : Candidate          (every evaluated candidate, all rounds)
│     ├── rule_results[] : RuleResult        (rules 1–4)
│     ├── fuel_plan      : FuelPlan → checkpoints[] : FuelCheckpoint
│     └── weather[]      : WeatherSegment
├── replan_rounds[]      : ReplanRound → changes[] : ArrangementChange
├── explanation          : Explanation → citations[] : Citation
├── rule5_log[]          : Rule5Attempt       (internal, never displayed)
├── infeasibility_report : InfeasibilityReport
└── evidence[]           : Evidence

RouteSnapshot                                 (CR-01; separate file, not part of PlanResult)
└── legs[]               : RouteLeg           (direction: outbound | return)
```

PlanResult 只以 `route.snapshot_id` 指向路線快照，不含快照的內容。

## 4. 欄位定義

### 4.1 PlanRequest（規劃請求；結果中以 `adopted_conditions` 回顯）

| 欄位 | 型別 | 可為空 | 填寫者 | 說明 |
| --- | --- | --- | --- | --- |
| `request_id` | string | 否 | 主程式 | 一次按下「規劃」的代號 |
| `route_id` | string | 是 | 主程式 | CR-01：由路線解析產生（7.10），不再由表單選取。路線解析失敗時為 `null` |
| `route_request` | RouteRequest | 否 | 表單、Planner、追問 | CR-01：結構化的路線請求，見下表 |
| `plan_date` | date | 否 | 表單 | 可以超出預報期間（Q7） |
| `earliest_departure` | datetime | 否 | 表單 | 候選的起點（Q11） |
| `latest_arrival` | datetime | 否 | 表單 | 期限：路線終點的保守估計不得晚於它（Q1）。必須晚於 `earliest_departure`。CR-01：語意不變。來回行程的終點就是出發點，介面顯示為「最晚回到出發點時間」；單向行程顯示為「最晚抵達終點時間」 |
| `start_fuel_pct` | float | 否 | 表單 | 0–100，必填；缺少時不進入規劃（Q6） |
| `free_text` | string | 是 | 表單 | CR-01：行程描述的原文。可以寫起點、目的地或公路、途經點、來回或單向，也可以補充休息與偏好（Q4）。沒有提供目標路線 GPX 時必填。送出前先通過本機輸入保護（7.12） |
| `breaks` | list | 否（可為空清單） | Planner | 結構化的休息安排（Q4、Q20） |
| `refuel_stops` | list | 否（可為空清單） | Planner | 補給策略：在哪些檢查點加滿（Q13、Q16） |
| `conflicts` | list | 否（可為空清單） | Planner | 自然語言與表單衝突的紀錄（Q4） |
| `data_mode` | enum | 否 | 表單 | `live` 或 `snapshot`（Q23） |
| `requested_at` | datetime | 否 | 主程式 | 按下「規劃」的時間 |

`adopted_conditions` 是最後一輪實際採用的條件：重新規劃改過的休息與加油安排會反映在這裡。介面以它和目前的表單比對，判斷結果是否過期。CR-01：`route_request` 與 `route_id` 記錄這次實際採用的路線請求與解析結果。

**RouteRequest**（CR-01）

| 欄位 | 型別 | 可為空 | 填寫者 | 說明 |
| --- | --- | --- | --- | --- |
| `trip_type` | enum | 是 | 表單、Planner 或追問 | `one_way`（單向）或 `round_trip`（來回：同一組起訖與途經點的去程與回程，終點回到起點）。表單有選時以表單為準；沒選時由 Planner 從行程描述取得；都沒有時追問。不由目標路線 GPX 的幾何推定（7.11 第 2 項）。只有 `result_kind = route_error` 時可以是 `null` |
| `origin` | PlaceRef | 是 | Planner 或追問 | 起點：出發錨點，或詞彙表中的公開地標。提供目標路線 GPX 時為 `null` |
| `destination` | PlaceRef | 是 | Planner 或追問 | 目的地：詞彙表中的地標或公路。提供目標路線 GPX 時為 `null` |
| `via` | list of PlaceRef | 否（可為空清單） | Planner | 途經點，依行經順序 |
| `target_gpx_ref` | string | 是 | 表單 | 目標路線 GPX 的參照：檔案的內容雜湊。只讀幾何，不讀時間。沒有提供時為 `null` |

**PlaceRef**（CR-01）

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `kind` | enum | 否 | `start_anchor`（出發錨點）、`landmark`（公開地標）、`road`（公路） |
| `ref_id` | string | 否 | 公路與地標詞彙表或 Rider Profile 中的代號。不是座標 |
| `name` | string | 否 | 顯示用的名稱 |
| `entry_ref_id` | string | 是 | 只有 `kind = road` 時有值：從公路的哪一端進入，指向詞彙表中的入口 |

Planner 只能填入詞彙表與 Rider Profile 中存在的代號，不得自行編造地點或座標。缺少的項目走追問（4.2）；對不到詞彙表的名稱回傳 `route_error`（4.13）。提供目標路線 GPX 時路線以 GPX 為準，行程描述中關於路線的部分不使用，並以 ConflictNotice 提示。來回行程的回程怎麼產生，見 7.11 第 2 項：回程另送一次請求，不反轉去程的折線。

**BreakArrangement**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `after_checkpoint_id` | string | 否 | 和 ETA 輸出的 `breaks` 相同（契約 4） |
| `duration_s` | int | 否 | 大於 0 |
| `purpose` | enum | 否 | `rest` 或 `refuel` |
| `origin` | enum | 否 | `free_text`、`rider_profile`、`clarification`、`replan` |

CR-01：行程描述沒有提到休息時，主程式依 Rider Profile 的預設休息排入休息，`origin = rider_profile`。排入的規則是確定性的，由這份 Spec 定義（7.11 第 9 項）；DESIGN.md 只寫摘要。

**RefuelStop**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `checkpoint_id` | string | 否 | 必須是路線目錄中 `kind = fuel_station` 的檢查點（Q19） |
| `origin` | enum | 否 | `planner` 或 `replan` |

加油一律是加滿。加油停留的時間以一筆 `purpose = refuel` 的 `breaks` 表示，這樣 ETA 才會算進去（見第 11.2 節 OQ-3）。

**ConflictNotice**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `field` | enum | 否 | `trip_type`、`target_gpx_ref`、`plan_date`、`earliest_departure`、`latest_arrival`、`start_fuel_pct`。CR-01：路線不再由表單選取，`route_id` 改為 `trip_type`；`target_gpx_ref` 用在行程描述另外寫了路線、同時又提供目標路線 GPX 的情形 |
| `free_text_value` | string | 否 | 自然語言中提到的值，原文 |
| `adopted` | enum | 否 | 固定為 `form`（Q4） |
| `message` | string | 否 | 顯示給使用者的提示 |

### 4.2 ClarificationRequest（追問）

需求有歧義或缺少必要條件時回傳這個物件，不產生 PlanResult（Algorithm 1 第 02 行）。CR-01：一次回傳所有缺少的項目，使用者一次回覆；不做多輪聊天。回覆後仍無法解析路線時回傳 `route_error`（4.13），不再追問。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `request_id` | string | 否 | |
| `questions` | list | 否 | 至少一題 |
| `questions[].topic` | enum | 否 | CR-01：`start_point`（缺起點）、`entry_side`（不知道從公路的哪一端進）、`trip_type`（沒說來回或單向）、`break_duration`（休息多久）、`other`。v0.1 的 `break_location` 併入 `other` |
| `questions[].text` | string | 否 | 追問的文字 |
| `questions[].options` | list of string | 是 | 有固定選項時提供。CR-01：`start_point` 與 `entry_side` 的選項只來自詞彙表與 Rider Profile |

出發油量缺少時由表單的檢查擋下，不走追問。CR-01：行程描述與目標路線 GPX 都沒有提供時，也由表單的檢查擋下。

### 4.3 PlanResult（規劃結果）

| 欄位 | 型別 | 可為空 | 填寫者 | 說明 |
| --- | --- | --- | --- | --- |
| `plan_schema_version` | string | 否 | 主程式 | `"0.2"` |
| `result_kind` | enum | 否 | 主程式 | `plan`、`infeasible`、`output_validation_error`；CR-01 新增 `route_error`、`evaluation_failed` |
| `adopted_conditions` | PlanRequest | 否 | 主程式 | 見 4.1 |
| `route` | RouteSummary | 是 | 主程式 | CR-01：見 4.12。`result_kind = route_error` 時為 `null` |
| `route_error` | RouteError | 是 | 主程式 | CR-01：見 4.13。只有 `result_kind = route_error` 時有值 |
| `evaluation` | Evaluation | 是 | 主程式 | CR-01：取代 v0.1 的 `search`，見 4.4。`result_kind = route_error` 時為 `null` |
| `candidates` | list | 否（可為空清單） | 主程式、Validator | 全部評估過的候選，含每一輪的（Q14）。Q14 不在 CR-01 的重開範圍內，維持必填，不延後 |
| `recommended_plan_id` | string | 是 | 主程式 | 沒有可用的候選時為 `null`（Q2） |
| `replan_rounds` | list | 否 | 主程式 | 1 到 3 筆：初次加上最多 2 次重新規劃（Q28、Q29）。CR-01：`result_kind = route_error` 時是空清單 |
| `explanation` | Explanation | 是 | 固定模板、Planner | 只有通過規則 5 的文字會放在這裡（Q30） |
| `rule5_log` | list | 否 | Validator | 內部紀錄，不顯示（Q30）。CR-01 沒有重開 Q30 的這一部分，維持必填，不延後 |
| `infeasibility_report` | InfeasibilityReport | 是 | 主程式 | `result_kind = infeasible` 時必填（Q27） |
| `evidence` | list | 否 | 主程式 | 見 4.11 |
| `status_origin` | enum | 否 | 主程式 | `validator` 或 `llm_declared`（Q12；後者只用在 E2 的 A1、A2） |
| `created_at` | datetime | 否 | 主程式 | |

`result_kind` 和其他欄位的關係：

| `result_kind` | `route` | `evaluation.completed` | `recommended_plan_id` | `explanation` | `infeasibility_report` | 計畫狀態能否顯示 |
| --- | --- | --- | --- | --- | --- | --- |
| `plan` | 有 | `true` | 有 | 有 | `null` | 可以，取推薦候選的 `plan_status` |
| `infeasible` | 有 | `true` | `null` | `null` | 有 | 顯示 INFEASIBLE |
| `route_error`（CR-01） | `null` | 沒有 `evaluation` | `null` | `null` | `null` | **不可以**。顯示 `route_error` 的訊息 |
| `evaluation_failed`（CR-01） | 有 | `false` | `null` | `null` | `null` | **不可以**。不輸出建議的出發時間 |
| `output_validation_error` | 有 | `true` | 有（內部保留） | `null` | `null` | **不可以**（Q30） |

`plan` 與 `infeasible` 都要求 `evaluation.completed = true`：候選沒有全部評估完，就不能說某個候選是最晚的可行出發時間，也不能說全部候選都不可行。

### 4.4 Evaluation（CR-01：取代 SearchStatus）

CR-01 取消每批 40 個候選與搜尋 COMPLETE／INCOMPLETE 的狀態，條件是保證完整評估，而且評估失敗或中止時不輸出最晚出發時間的宣稱（CR-01 第 11 節「附條件接受」）。v0.1 的 `status`、`reason` 與 `batch_size` 不再使用。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `candidates_total` | int | 否 | 最後一輪應評估的候選數 |
| `candidates_evaluated` | int | 否 | 最後一輪實際評估的數量 |
| `completed` | bool | 否 | 每一輪的每一個候選都評估完才是 `true` |
| `failure` | string | 是 | `completed = false` 時必填：評估在哪一步失敗或中止。由固定模板組成，不由 LLM 產生 |
| `step_min` | int | 否 | 候選的間隔，目前是 15（Q11） |

規則：

- `completed = true` 時，`candidates_evaluated` 必須等於 `candidates_total`。
- `completed = false` 時，`result_kind` 必須是 `evaluation_failed`：`recommended_plan_id` 是 `null`；不輸出建議的出發時間，不宣稱最晚的可行出發時間，也不宣稱無可行解。
- 工具回傳 UNKNOWN 不算評估失敗：候選照常評估，對應的規則是 UNKNOWN。評估失敗指的是程式錯誤或中止，使得有候選沒有得到規則結果。

### 4.5 Candidate

| 欄位 | 型別 | 可為空 | 填寫者 | 說明 |
| --- | --- | --- | --- | --- |
| `plan_id` | string | 否 | 主程式 | 對應 ETA 輸出（契約 4） |
| `round_index` | int | 否 | 主程式 | 0 是初次評估，1、2 是重新規劃。保留每一輪的候選需要它（Q14），不延後 |
| `departure_time` | datetime | 否 | 主程式 | |
| `eta_typ_end` | datetime | 是 | 主程式 | 終點的典型估計，取自 ETA 輸出最後一段的 `eta_typ`。CR-01：來回行程的終點就是出發點 |
| `eta_safe_end` | datetime | 是 | 主程式 | 終點的保守估計，取自 `eta_safe`。不是 P90 |
| `time_limit` | datetime | 否 | 主程式 | 規則 1 使用的期限 |
| `time_limit_basis` | enum | — | 主程式 | **延後（P-9 裁決，2026-11-15）：這一版的結果不含這個欄位。** 原定義保留備查：`civil_dusk`、`latest_arrival`、`latest_arrival_dusk_unknown`（SD-7） |
| `time_margin_s` | int | 是 | 主程式 | `time_limit` 減 `eta_safe_end`。只用來顯示，不是排序依據 |
| `plan_status` | enum | 否 | Validator | 由規則 1–4 決定（Q30） |
| `rule_results` | list | 否 | Validator | 規則 1–4 各一筆 |
| `fuel_plan` | FuelPlan | 否 | 主程式 | 見 4.7 |
| `weather` | list | 否（可為空清單） | 主程式 | 見 4.8。沒有預報時是空清單 |

### 4.6 RuleResult

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `rule_id` | int | 否 | 1–5 |
| `result` | enum | 否 | `PASS`、`FAIL`、`UNKNOWN`；規則 5 只有 `PASS` 或 `FAIL` |
| `reason_class` | enum | 是 | `result = UNKNOWN` 時必填，其他情形為 `null`。五個值見 5.1 |
| `reason_code` | enum | 否 | 這一次判定的原因代碼，見 5.2。**維持必填（P-9 裁決）**：代碼是穩定的識別碼，定案後不改名、不改意義；新增代碼要經過有紀錄的修訂 |
| `reason` | string | 否 | 具體原因的文字。由固定模板加上數值組成，不由 LLM 產生。CR-01：ETA 因為配速資料不足而無法估計時，寫明缺的是哪個類別、還差多少路段 |
| `evidence_ids` | list of string | 否（可為空清單） | 指向 `evidence`。沒有可用的來源時是空清單 |
| `manual_check_guidance` | string | 是 | `result = UNKNOWN` 時必填，內容是 5.3 的固定文字。CR-01：依 `rule_id` 與 `reason_class` 查表 |
| `overrun_s` | int | — | **延後（P-9 裁決，2026-11-15）：這一版的結果不含這個欄位。** 原定義保留備查：只有規則 1 為 `FAIL` 時有值，是 `eta_safe_end` 超過 `time_limit` 的秒數（SD-9） |

G1 Q15 列出的 `source`、`fetched_at`／`snapshot_at` 與 `simulated` 放在 Evidence，由 `evidence_ids` 取得，不在這裡重複。

**UNKNOWN 的四項（Q25）維持必填，不延後。** CR-01 沒有重開 Q25。四項在這份 Spec 的對應（呈現方式見 UI_FLOW 第 7 節）：

| Q25 的項目 | 欄位 |
| --- | --- |
| 缺失的項目 | `rule_id` 與 `reason` |
| 原因代碼與具體原因 | `reason_class`（五個共用分類之一）、`reason_code` 與 `reason` |
| 來源與時間 | `evidence_ids` 指向的 Evidence；沒有可用的來源時是空清單 |
| 固定的人工確認指引 | `manual_check_guidance` |

`reason_code` 是在五個共用分類之下再細分的代碼，凍結的介面沒有顯示它。P-9 的裁決要求保留穩定的原因代碼，所以它維持必填；介面是否顯示不變。

### 4.7 FuelPlan 與 FuelCheckpoint

**FuelPlan**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `reserve_pct` | float | 是 | 安全保留油量，來自 Rider Profile（暫定 20） |
| `reserve_l` | float | 是 | 換算成公升 |
| `tank_capacity_l` | float | 是 | 來自 Rider Profile |
| `consumption_l_per_100km` | float | 是 | 平均油耗，來自 Rider Profile（單位見 OQ-2） |
| `profile_evidence_id` | string | 否 | 指向 Rider Profile 的來源證據 |
| `checkpoints` | list | 否 | 起點、每個計畫加油站、終點，依路線順序。CR-01：檢查點由加油站快照沿路線產生。來回行程的去程與回程各自產生檢查點：回程也經過同一個加油站時，它在回程另有一個檢查點，`checkpoint_id` 不同。回程是另外算的路線，不保證經過去程的每一個加油站。折返點的 `kind` 是 `turnaround`，會列在清單中 |

**FuelCheckpoint**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `checkpoint_id` | string | 否 | |
| `kind` | enum | 否 | 沿用路線目錄：`start`、`fuel_station`、`waypoint`、`end`；契約 2 v0.3 新增 `turnaround`（來回行程的折返點；草稿，待 Ticket 實作） |
| `arrival_typ` | datetime | 是 | 起點為 `null` |
| `arrival_safe` | datetime | 是 | 起點為 `null` |
| `fuel_on_arrival_pct` | float | 是 | 抵達時的剩餘油量 |
| `fuel_on_arrival_l` | float | 是 | |
| `refuel_planned` | bool | 否 | 是否安排在這裡加滿 |
| `station_status` | enum | 否 | `OPEN`、`CLOSED`、`UNKNOWN`、`NOT_APPLICABLE` |
| `station_evidence_id` | string | 是 | 加油站營業時間的來源 |

`station_status` 是 `UNKNOWN` 的加油站之後，各檢查點的剩餘油量必須是 `null`：能不能補油不確定，不報告為確定的數值（DESIGN §4.2）。

### 4.8 WeatherSegment

每個路段一筆。介面把它彙總成前段、中段與最後 20% 三列顯示。CR-01：這是單向行程的做法；來回行程怎麼彙總與顯示，等 D3 定案（第 11.1 節 P-8）。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `seg_index` | int | 否 | 路線目錄的路段 |
| `arrival_typ` | datetime | 是 | 抵達這個路段的典型時間 |
| `arrival_safe` | datetime | 是 | 保守時間 |
| `pop_pct` | int | 是 | 和抵達時段 [`arrival_typ`, `arrival_safe`] 重疊的各個預報時段、以及路段對應的各個鄉鎮中，最高的降雨機率（7.13）。它是預報時段的數值，不是抵達那一刻的預報 |
| `pop_class` | enum | 是 | `LOW`（0–39）、`MEDIUM`（40–69）、`HIGH_ALERT`（70–100） |
| `forecast_period_start` | datetime | 是 | 採用的預報時段中最早的起始時間（審查處置的修正 4；草案）。沒有可用的預報時為 `null` |
| `forecast_period_end` | datetime | 是 | 採用的預報時段中最晚的結束時間。沒有可用的預報時為 `null` |
| `forecast_resolution_h` | int | 是 | 單筆預報時段的長度，以小時計，取自實際的預報資料（例如 3 或 12）。沒有可用的預報時為 `null` |
| `in_last_20pct` | bool | 否 | 路段是否落在或跨入路線最後 20% 的累計距離（Q18）。CR-01：只對單向行程有定義；來回行程的規則 3 範圍待 D3 裁決，定案後可能改用另一個欄位 |
| `evidence_id` | string | 是 | 預報的來源 |

`HIGH_ALERT` 在介面上稱為「高降雨機率提醒」。它是本專題自訂的分類，不是氣象署的警特報，也不表示降雨強度。

降雨機率的時間解析度與預報的涵蓋區間必須保留（審查處置的修正 4）：顯示與說明只能寫成某個預報時段的降雨機率，不得把 12 小時一筆的資料寫成精確時刻的預報。規則見 7.13。

### 4.9 ReplanRound 與 ArrangementChange

**ReplanRound**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `round_index` | int | 否 | 0–2 |
| `changes` | list | 否 | 這一輪相對前一輪的結構化變更（Q29）。第 0 輪是空清單。Q29 不在 CR-01 的重開範圍內，維持必填，不延後 |
| `change_summary` | string | 是 | CR-01：`changes` 的顯示文字。由主程式依 `changes` 以固定模板組成，不是 LLM 的文字；第 0 輪為 `null`。它不取代 `changes` |
| `candidates_evaluated` | int | 否 | |
| `best_status` | enum | 否 | `FEASIBLE`、`CONDITIONAL`、`INFEASIBLE`、`NO_CANDIDATES` |
| `stop_reason` | enum | 是 | 只有最後一輪有值：`found`、`max_replans`、`no_valid_change`、`not_materially_different` |

**ArrangementChange**（Q29 的結構化變更摘要；不延後）

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `kind` | enum | 否 | `add_refuel`、`remove_refuel`、`add_break`、`remove_break`、`change_break_duration` |
| `checkpoint_id` | string | 否 | |
| `from_duration_s` | int | 是 | |
| `to_duration_s` | int | 是 | |

重新規劃只能改 `breaks` 與 `refuel_stops`。路線、日期、`earliest_departure`、`latest_arrival` 與 `start_fuel_pct` 不得改動（Q19）。不保存也不顯示 LLM 的原始推理（Q29）。

### 4.10 Explanation、Citation、Rule5Attempt、InfeasibilityReport

**Explanation**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `text` | string | 否 | 通過規則 5 的說明文字。CR-01：由固定模板組成 |
| `planner_text` | string | 是 | CR-01：Planner 的說明。通過規則 5 才有值，顯示在 `text` 之後；沒通過或沒有產生時為 `null` |
| `planner_text_status` | enum | 否 | CR-01：`attached`（通過並附加）、`rejected`（沒通過規則 5，不顯示）、`not_generated`（沒有產生） |
| `origin` | enum | 否 | `planner` 或 `template`。**CR-01：取代**，改由 `planner_text_status` 表示，不輸出這個欄位 |
| `rule5` | RuleResult | 否 | `rule_id = 5`、`result = PASS`。CR-01：檢查的是最後顯示的全部文字（`text` 加上附加的 `planner_text`） |
| `citations` | list | 否（可為空清單） | 知識庫的出處（FR7） |

**Citation**：`doc_id`（string）、`title`（string）、`locator`（string，可為空）。

**Rule5Attempt**（內部紀錄；Q30 的「內部保留規則 5 的失敗紀錄與最後通過的結果」，不延後）

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `attempt` | int | 否 | 1–3 |
| `text_origin` | enum | 否 | `template`（固定模板）、`planner`（Planner 的說明）、`final_output`（最後顯示的全部文字）。CR-01 取消了重新產生，v0.1 的 `planner_regenerated` 不再使用 |
| `result` | enum | 否 | `PASS` 或 `FAIL` |
| `untraceable_values` | list of string | 否 | 找不到來源的數值 |
| `checked_at` | datetime | 否 | |

每一次規則 5 的檢查各留一筆（7.7）。沒通過的文字只留在內部紀錄，不放進 `explanation`，也不顯示。

**InfeasibilityReport**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `summary` | string | 否 | 原因摘要，由固定模板組成 |
| `fail_counts` | object | 否 | `rule_1` 到 `rule_4` 各一個 `int`，統計最後一輪的候選 |
| `representative` | object | 是 | 沒有任何候選時為 `null` |
| `representative.plan_id` | string | 否 | |
| `representative.label` | enum | 否 | `closest_to_time_limit` 或 `representative_failure`。**CR-01：取代**，一律稱「代表性失敗候選」，不輸出這個欄位 |
| `representative.basis` | enum | 否 | 見 7.5。**CR-01：取代**，選法只有一種，不輸出這個欄位 |
| `alternatives` | list | 否 | 每筆有 `text`（string）、`verified`（固定 `false`）、`auto_executed`（固定 `false`） |

### 4.11 Evidence（來源證據）

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `evidence_id` | string | 否 | |
| `source` | string | 否 | 資料來源的名稱 |
| `source_type` | enum | 否 | 五個值，見第 6 節 |
| `fetched_at` | datetime | 是 | 只有 `live_api` 有值 |
| `snapshot_at` | datetime | 是 | 只有 `snapshot` 有值 |
| `built_at` | datetime | 是 | 只有 `local_derived` 有值 |
| `version` | string | 是 | 例如 `pace_version`、`catalog_version` 或設定檔的版本 |
| `coverage` | string | 否 | 時間或地點的涵蓋範圍 |
| `simulated` | bool | 否 | `source_type = simulated` 時為 `true`，其他為 `false` |

### 4.12 RouteSummary（路線摘要，CR-01）

路線解析成功後由主程式填寫。數值取自路線快照（4.14）或路線目錄，Planner 不填寫。路線摘要與路線快照的欄位都由這份 Spec 定義；DESIGN.md §5 只寫摘要。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `route_id` | string | 否 | 和 `adopted_conditions.route_id` 相同 |
| `route_source` | enum | 否 | `trip`（由騎過的行程建立的示範路線，也就是 R01／R02 fixture）、`routing`（路線引擎）、`target_gpx`（目標路線 GPX） |
| `snapshot_id` | string | 是 | 路線快照的代號。一條路線對應一個路線快照（4.14）；來回行程的去程與回程在同一個快照裡。可否為空見下方的跨欄位規則 |
| `trip_type` | enum | 否 | `one_way` 或 `round_trip`。和路線目錄的路線紀錄相同（契約 2 v0.3 新增的路線層級欄位，草稿） |
| `distance_m` | int | 否 | 整條路線的里程；來回行程是去程加回程 |
| `engine_time_s` | int | 是 | 路線引擎回報的行駛時間；來回行程是兩個方向的總和。它不是個人估計，不用在規則判定，介面也不顯示 |
| `road_names` | list of string | 否（可為空清單） | 主要道路名稱，依行經順序；來回行程先去程、後回程。取不到名稱時是空清單 |
| `freeway_check` | enum | 是 | 獨立的國道檢查結果：`pass` 或 `fail`。每個方向都通過才是 `pass`；逐方向的結果在路線快照。結果中不得出現 `fail`：沒通過的路線不會成為結果 |
| `leg_length_diff_pct` | float | 是 | 去程與回程的里程差，以百分比表示：兩者相減的絕對值，除以兩者的平均，再乘以 100（7.11 第 11 項） |
| `leg_length_diff_flag` | bool | 是 | `leg_length_diff_pct` 大於 2 時為 `true`：回程走的道路和去程有明顯的不同，介面在路線摘要標示（5.5） |
| `turnaround_checkpoint_id` | string | 是 | 來回行程的折返點，指向 `kind = turnaround` 的檢查點；單向行程為 `null` |
| `ridden_share_pct` | float | 是 | 這條路線的里程中，和配速行程的軌跡重合的比例（0–100），不分方向。只比對配速行程；介面稱為「配速資料中的路線涵蓋比例」，不得宣稱它代表騎士騎過的所有道路（審查處置的修正 1）。無法比對時為 `null`。算法見 7.11 第 10 項 |
| `route_evidence_id` | string | 否 | 指向路線的來源證據（第 6 節） |

路線引擎自己回報的國道旗標 `has_highway` 逐方向記錄在路線快照（4.14），不放在路線摘要，也不是採用路線的依據。這份 Spec 的初稿曾經用 `has_highway` 表示產品自己的檢查結果；為了不和引擎的欄位同名不同義，改為 `freeway_check`。

**`route_source` 的跨欄位規則**

| `route_source` | `snapshot_id` | `freeway_check` | `engine_time_s` | `leg_length_diff_pct`、`leg_length_diff_flag` | `route_request.target_gpx_ref` | 路線目錄的 `source_trip_id`（契約 2） |
| --- | --- | --- | --- | --- | --- | --- |
| `trip` | `null` | `null`（沒有檢查） | `null` | `null` | `null` | 必填 |
| `routing` | 必填 | 必須是 `pass` | 必填 | 來回行程必填；單向行程為 `null` | `null` | `null` |
| `target_gpx` | `null` | `null`（沒有檢查） | `null` | `null` | 必填（檔案的內容雜湊） | `null` |

目標路線 GPX 的路線沒有路線快照。它在結果中可追溯的代號是 `target_gpx_ref` 的內容雜湊。

規則：

- **採用條件。** 路線引擎回傳的路線，每個方向都通過獨立的國道檢查（`freeway_check = pass`）才採用。這一條沒有例外，和用哪一種路線參數無關。沒通過時回傳 `route_error`（`highway_in_route`）。
- **回應的警告。** 路線參數已裁決為 `use_highways: 0`（P-1）：請求不送出硬性排除，回應出現任何警告就不採用。規則寫在 7.11 第 7 項。
- `road_names` 是給騎士檢視路權用的。結果不含座標與折線。
- `ridden_share_pct` 只用來告知，不改變任何規則結果，也不分級。

### 4.13 RouteError（路線錯誤，CR-01）

路線無法取得或不能採用時回傳，`result_kind = route_error`。這時不評估候選，也不由語言模型產生或補上路線（CR-01 D2）。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `code` | enum | 否 | 見下表 |
| `message` | string | 否 | 5.5 的固定文字，不由 LLM 產生 |
| `actions` | list of string | 否 | 騎士可以怎麼做；5.5 的固定文字 |
| `unresolved` | list of string | 否（可為空清單） | `code = not_in_gazetteer` 時，列出行程描述中對不到詞彙表的名稱 |

| `code` | 情形 |
| --- | --- |
| `not_in_gazetteer` | 行程描述中的公路或地標不在詞彙表內，追問也補不齊 |
| `routing_unavailable` | 路線引擎沒有回應、回傳錯誤，或找不到可用的路線。一般模式下不自動改用舊的路線快照（7.11 第 3 項）。回應因為警告而不採用時歸在這裡（P-1 已裁決）；因為端點偏移而不採用時暫定也歸在這裡，隨 7.11 第 8 項定案 |
| `highway_in_route` | 任一方向沒有通過獨立的國道檢查（`freeway_check = fail`） |
| `snapshot_missing` | Snapshot Mode 下，這個路線請求沒有已保存的路線快照。Snapshot Mode 不呼叫路線引擎 |
| `target_gpx_invalid` | 目標路線 GPX 讀不到軌跡點，或點距太疏、無法當成路線的幾何。騎士指定來回、但 GPX 不符合 7.11 第 2 項的來回條件時，暫定也歸在這裡（SB-7） |

`result_kind = route_error` 時，結果只有：`plan_schema_version`、`result_kind`、`adopted_conditions`（其中 `route_id` 為 `null`）、`route_error`、`evidence`（可為空清單）、`status_origin` 與 `created_at`。`route`、`evaluation`、`recommended_plan_id`、`explanation` 與 `infeasibility_report` 是 `null`；`candidates`、`replan_rounds` 與 `rule5_log` 是空清單。

### 4.14 RouteSnapshot（路線快照，CR-01）

路線快照是 `routing` 模組產生的檔案，不是 PlanResult 的一部分。**一條路線對應一個路線快照**，以 `snapshot_id` 識別。來回行程的去程與回程在同一個快照裡，各是 `legs[]` 的一筆。欄位由這份 Spec 定義；實體檔案格式由 Tickets 決定。尚未實作。

快照含折線，所以不放進規劃結果，也不送給語言模型（第 2 節）。從住家或出發錨點出發的快照不進版控（DESIGN.md 的隱私規則）。

**RouteSnapshot**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `snapshot_id` | string | 否 | 快照的代號 |
| `request_key` | string | 否 | 路線請求的比對鍵（7.11 第 4 項）。Snapshot Mode 以它找已保存的快照 |
| `trip_type` | enum | 否 | `one_way` 或 `round_trip` |
| `routing_params` | object | 否 | 送給引擎的設定：機車設定與國道的參數。國道的參數是 `use_highways: 0`（P-1 裁決），不送出硬性排除；快照記錄實際送出的值 |
| `engine_name` | string | 否 | 路線引擎的名稱 |
| `engine_version` | string | 否 | 路線引擎的版本 |
| `map_data_date` | date | 是 | 引擎使用的圖資日期。引擎沒有回報時為 `null`，不得以取得日期代替 |
| `legs` | list of RouteLeg | 否 | `one_way` 一筆（`outbound`）；`round_trip` 兩筆，依序是 `outbound`、`return` |

**RouteLeg**（快照中一個方向的路線）

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `direction` | enum | 否 | `outbound`（去程）或 `return`（回程） |
| `request` | object | 否 | 這個方向送出的請求：起點、途經點、終點（詞彙表或 Rider Profile 中的代號，依這個方向的行經順序）與 `routing_params`。每個方向各送一次請求 |
| `shape` | string | 否 | 引擎為這個方向回傳的折線（編碼後）。`return` 的折線來自它自己的請求，不得由 `outbound` 的折線反轉產生 |
| `distance_m` | int | 否 | 這個方向的里程 |
| `engine_time_s` | int | 否 | 引擎回報的行駛時間 |
| `road_names` | list of string | 否（可為空清單） | 主要道路名稱，依行經順序 |
| `warnings` | list of object | 否（可為空清單） | 回應中的警告，原樣記錄：每筆有 `code`（int）與 `text`（string）。沒有警告時是空清單 |
| `has_highway` | bool | 是 | 路線引擎回報的國道旗標。引擎沒有回報時為 `null`。只作紀錄，不是採用路線的依據 |
| `freeway_check` | enum | 否 | 獨立的國道檢查結果：`pass` 或 `fail`。判定條件見 7.11 第 5 項。存成快照的路線，每個方向都是 `pass` |
| `freeway_check_method` | string | 否 | 這次檢查用的方法與資料來源（7.11 第 5 項） |
| `endpoint_offset_m` | object | 否 | `start` 與 `end` 兩個 `float`：要求的地標到折線起點、終點的距離 |
| `elevation_m` | list of float | 是 | 選填：沿折線的高度值。沒有取得時為 `null`。規則 3 在來回行程上的範圍（P-8）若採用高度的定義才會用到 |
| `fetched_at` | datetime | 否 | 取得這個方向回應的時間 |

## 5. 規則的固定內容

### 5.1 UNKNOWN 的原因分類（Q15）

| `reason_class` | 顯示文字 |
| --- | --- |
| `NO_SOURCE` | 沒有資料來源 |
| `OUT_OF_COVERAGE` | 超出涵蓋期間 |
| `SOURCE_ERROR` | 外部服務失敗 |
| `MISSING_INPUT` | 缺少必要輸入 |
| `UPSTREAM_UNKNOWN` | 上游結果為 UNKNOWN |

### 5.2 原因代碼

每條規則每一種結果對應固定的代碼。`reason` 的文字由代碼的模板加上數值組成。

**`reason_code` 維持必填（P-9 裁決）。** 這張表同時定義每條規則在各種條件下的結果與原因分類，判定一律依這張表。代碼是穩定的識別碼：定案後不改名、不改意義。

| 規則 | `reason_code` | 結果 | `reason_class` | 條件（DESIGN §4.2） |
| --- | --- | --- | --- | --- |
| 1 | `R1_WITHIN_LIMIT` | PASS | — | `eta_safe_end` ≤ min（民用暮光終, `latest_arrival`） |
| 1 | `R1_OVER_LATEST_ARRIVAL` | FAIL | — | `eta_safe_end` 晚於 `latest_arrival`。暮光終是 UNKNOWN 時也是 FAIL（Q17） |
| 1 | `R1_OVER_CIVIL_DUSK` | FAIL | — | 沒有超過 `latest_arrival`，但晚於民用暮光終 |
| 1 | `R1_DUSK_UNAVAILABLE` | UNKNOWN | `SOURCE_ERROR` 或 `NO_SOURCE` | 取不到暮光終，而且沒有超過 `latest_arrival` |
| 1 | `R1_ETA_UNKNOWN` | UNKNOWN | `UPSTREAM_UNKNOWN` | ETA 輸出的狀態是 `unknown` |
| 2 | `R2_FUEL_OK` | PASS | — | 每個檢查點的剩餘油量 ≥ 安全保留油量，計畫加油站的抵達時段都在營業時間內 |
| 2 | `R2_BELOW_RESERVE` | FAIL | — | 任一檢查點低於安全保留油量 |
| 2 | `R2_STATION_CLOSED` | FAIL | — | 抵達時段有任何部分在營業時間外 |
| 2 | `R2_STATION_HOURS_UNKNOWN` | UNKNOWN | `NO_SOURCE` | 計畫加油站沒有營業時間資料 |
| 2 | `R2_PROFILE_INCOMPLETE` | UNKNOWN | `MISSING_INPUT` | 缺油箱容量或平均油耗 |
| 2 | `R2_ETA_UNKNOWN` | UNKNOWN | `UPSTREAM_UNKNOWN` | ETA 輸出的狀態是 `unknown` |
| 3 | `R3_NO_ALERT_IN_LAST_20PCT` | PASS | — | 最後 20% 範圍內沒有 `HIGH_ALERT` 的路段 |
| 3 | `R3_ALERT_IN_LAST_20PCT` | FAIL | — | 最後 20% 範圍內有 `HIGH_ALERT` 的路段 |
| 3 | `R3_OUT_OF_COVERAGE` | UNKNOWN | `OUT_OF_COVERAGE` | 日期超出預報涵蓋期間 |
| 3 | `R3_FORECAST_UNAVAILABLE` | UNKNOWN | `SOURCE_ERROR` | 取不到預報 |
| 3 | `R3_AREA_UNMAPPED`（草案） | UNKNOWN | `NO_SOURCE` | 路段對不到鄉鎮，或鄉鎮在預報中找不到對應的地點（7.13 第 3 項） |
| 3 | `R3_ETA_UNKNOWN` | UNKNOWN | `UPSTREAM_UNKNOWN` | ETA 輸出的狀態是 `unknown` |
| 4 | `R4_NO_EVENT` | PASS | — | 事件來源中沒有這條路線的封閉或管制事件 |
| 4 | `R4_ROAD_EVENT` | FAIL | — | 路線上有封閉或管制事件 |
| 4 | `R4_NO_SOURCE` | UNKNOWN | `NO_SOURCE` | 沒有可用的事件來源。不得預設為 PASS |
| 5 | `R5_TRACEABLE` | PASS | — | 文字中的每個數值都能在結構化欄位中找到 |
| 5 | `R5_UNTRACEABLE` | FAIL | — | 至少一個數值找不到來源 |

同一條規則同時符合 FAIL 與 UNKNOWN 的條件時，結果是 FAIL。

CR-01 的補充：

- 規則 1 的 `latest_arrival` 語意不變；來回行程指回到出發點的時間。
- 規則 3 的 `R3_NO_ALERT_IN_LAST_20PCT` 與 `R3_ALERT_IN_LAST_20PCT` 是單向行程的條件。來回行程的範圍待 D3 裁決（第 11.1 節 P-8），定案後補上對應的條件。
- 路段對不到鄉鎮，或對應的鄉鎮在預報中找不到地點時（7.13 第 3 項），規則 3 是 UNKNOWN，原因分類是 `NO_SOURCE`，代碼是 `R3_AREA_UNMAPPED`（草案，隨 7.13 確認）。鄉鎮界線採用國土測繪中心的資料（P-4 裁決）。

### 5.3 固定的人工確認指引（Q25）

指引是固定文字，不由 LLM 產生。v0.1 依原因代碼查表。CR-01：改依規則編號與 `reason_class` 查表；每條規則的每個原因分類只對應一則指引，指引文字和 v0.1 相同。這個查法不依賴 `reason_code`；`reason_code` 依 P-9 的裁決維持必填。

| 規則 | `reason_class` | `reason_code` | 指引文字 |
| --- | --- | --- | --- |
| 1 | `SOURCE_ERROR`、`NO_SOURCE` | `R1_DUSK_UNAVAILABLE` | 查詢當日的民用暮光終時間，確認保守抵達時間在天黑之前。 |
| 2 | `NO_SOURCE` | `R2_STATION_HOURS_UNKNOWN` | 出發前確認這個加油站當天的營業時間，或先在起點加滿。 |
| 2 | `MISSING_INPUT` | `R2_PROFILE_INCOMPLETE` | 在 Rider Profile 補上油箱容量與平均油耗後重新規劃。 |
| 3 | `OUT_OF_COVERAGE`、`SOURCE_ERROR`、`NO_SOURCE` | `R3_OUT_OF_COVERAGE`、`R3_FORECAST_UNAVAILABLE`、`R3_AREA_UNMAPPED`（草案） | 出發前查看氣象署的最新預報，確認抵達時段的降雨機率。 |
| 4 | `NO_SOURCE` | `R4_NO_SOURCE` | 出發前到公路主管機關的路況資訊，確認沿線有沒有封閉或管制。 |
| 1、2、3 | `UPSTREAM_UNKNOWN` | `R1_ETA_UNKNOWN`、`R2_ETA_UNKNOWN`、`R3_ETA_UNKNOWN` | 系統無法估計抵達時間，這條規則無法判定。請自行估計騎乘時間後再決定是否出發。 |

每一則指引之後，介面固定附上一句：「自行確認不會把這條規則改為 PASS。」（Q8、Q25）

### 5.4 設定值

這些都是本專題自訂的暫行設定，不是官方標準。

| 設定 | 值 | 依據 |
| --- | --- | --- |
| 高降雨機率提醒的門檻 | 降雨機率 ≥ 70% | PD-4 |
| 規則 3 的範圍 | 單向行程：路線最後 20% 的累計距離。來回行程：**待裁決**（D3，第 11.1 節 P-8：lead 在 11/27 前提出最小方案，最晚 2026-12-03 定案） | Q18；CR-01 D3 |
| 安全保留油量 | 油箱容量的 20%，可在 Rider Profile 調整 | M0 決策 |
| 候選間隔 | 15 分鐘。CR-01：每批 40 個的上限取消 | Q11；CR-01 第 11 節 |
| 重新規劃的上限 | 2 次 | Q28 |
| 安全餘裕係數 | 暫定 0.2。加入停等寬放之後，以配速行程的留一趟殘差重新決定，並在讀取保留行程之前凍結（P-2、P-5） | DESIGN §6.1 |
| 去回里程差的標示門檻 | 2%（`leg_length_diff_pct` 大於 2） | CR-01 審查後的處置 L-3；和檢查 C4 記錄去回里程差時用的門檻相同 |
| 停等寬放 | **尚未定義。** P-2 裁決升為 Must：先處理 `ingest` 的假停留；算式與數值只由配速行程決定；和安全餘裕係數不重複計算（DESIGN §6.1；SB-2） | CR-01 審查處置 P-2 |
| 道路寫法的固定樣式（規則 5，7.7） | 「國道 N 號」「台 N 線」「縣道 N」「鄉道」。草稿：清單由 Tickets 補齊 | CR-01；7.7 |

### 5.5 CR-01 的固定文字

以下文字由主程式依條件選用，不由 LLM 產生。**文字是提案，等專題負責人確認**；確認前不凍結。`{…}` 是由結構化欄位填入的值。

**路權提醒、配速資料的涵蓋比例與其他固定說明**

| 用途 | 條件 | 文字 |
| --- | --- | --- |
| 路權提醒 | `route_source = routing` | 這條路線由路線引擎依開放圖資產生，已檢查不含國道。其他道路的機車通行限制（例如部分快速公路與高架道路）系統無法保證，請出發前自行確認路權。 |
| 路權提醒 | `route_source` 是 `target_gpx` 或 `trip` | 這條路線取自你提供的 GPX 或騎過的行程。系統沒有檢查國道與機車通行限制，請出發前自行確認路權。 |
| 去回里程差 | `leg_length_diff_flag = true` | 回程是另外算的路線，和去程的里程相差約 {`leg_length_diff_pct`}%，走的道路不完全相同。請查看道路名稱。 |
| 涵蓋比例 | `ridden_share_pct` 大於 0 | 配速資料中的路線涵蓋比例：這條路線約有 {`ridden_share_pct`}% 的里程和你的配速資料重合（不分方向）。這個比例只比對用來建立個人配速表的行程，不代表你騎過的所有道路。抵達時間依你的個人配速表估計；配速資料沒有涵蓋的路段，估計的可信度較低。 |
| 涵蓋比例 | `ridden_share_pct` 等於 0 | 配速資料中的路線涵蓋比例：0%。配速資料中沒有和這條路線重合的行程；這不表示你沒有騎過這條路。抵達時間依你在同類彎道上的個人配速估計，可信度較低。 |
| 涵蓋比例 | `ridden_share_pct` 是 `null` | 系統無法算出配速資料中的路線涵蓋比例。 |
| 評估失敗 | `result_kind = evaluation_failed` | 候選的評估沒有完成，這次不提供建議的出發時間。請再按一次「規劃」；仍然失敗時，改用 Snapshot Mode 或稍後再試。 |
| 行程描述的輸入保護（7.12；草案） | 行程描述出現門牌或座標的寫法 | 行程描述中有看起來像門牌地址或座標的內容，系統沒有送出這段文字。請改用公路或地標的名稱描述；起點在住家附近時，請用出發錨點。 |
| 預報時段的說明（7.13；草案） | 天氣表有降雨機率時 | 降雨機率是所列預報時段的數值，不是抵達那一刻的預報；各列採用的預報時段與時段長度見表中的欄位。 |

**路線錯誤**

| `code` | `message` | `actions` |
| --- | --- | --- |
| `not_in_gazetteer` | 行程描述中的「{`unresolved`}」不在目前支援的公路與地標清單內，系統沒有產生路線。 | 改用清單內的公路或地標重新描述；或提供目標路線 GPX。 |
| `routing_unavailable` | 路線服務沒有回傳可用的路線，系統沒有產生路線。 | 稍後再按一次「規劃」；改用 Snapshot Mode 規劃已有快照的行程；或提供目標路線 GPX。 |
| `highway_in_route` | 路線服務回傳的路線沒有通過國道檢查，系統不採用這條路線。 | 增加途經點讓路線避開國道；或提供目標路線 GPX。 |
| `snapshot_missing` | Snapshot Mode 只使用已保存的路線快照，這個行程沒有對應的快照。 | 關閉 Snapshot Mode 後重新規劃；或改成有快照的行程。 |
| `target_gpx_invalid` | 目標路線 GPX 無法當成路線使用：讀不到軌跡點，或點與點之間的距離太遠。 | 確認檔案路徑與內容；改用記錄較密的 GPX；或改用行程描述。 |

## 6. 來源證據的型別

G1 定了三種：真實 API、資料快照、模擬。G3 裁決 N6 要求本地衍生資料與本地設定檔另有型別，不得標成 API。這份 Spec 定為五種。

| `source_type` | 顯示文字 | 時間欄位 | 標籤顏色 | 用在哪裡 |
| --- | --- | --- | --- | --- |
| `live_api` | 真實 API | `fetched_at` 必填 | 灰（G3 裁決 N5） | 一般模式下的氣象署預報與日出日沒 |
| `snapshot` | 資料快照 | `snapshot_at` 必填 | 藍 | Snapshot Mode 的預報與日出日沒；加油站快照；路線快照（CR-01）；鄉鎮界線檔（7.13，草案） |
| `simulated` | 模擬 | 都可以是 `null` | 紫 | 路況事件情境檔；Prototype 的模擬檢查點 |
| `local_derived` | 本地衍生資料 | `built_at` 必填 | 灰 | 個人配速表與路線目錄（ETA 的依據）；由目標路線 GPX 建立的路線（CR-01） |
| `local_config` | 本地設定檔 | 都是 `null`；`version` 必填 | 灰 | Rider Profile |

規則：

- 時間欄位只填和型別對應的那一個，其他是 `null`。不得虛構取得時間（Q15）。
- `simulated = true` 的證據一律以「模擬」標示，在介面、實驗紀錄與結果中都和真實資料分開（NFR5）。
- Snapshot Mode 下不得出現 `live_api`。CR-01：Snapshot Mode 也不呼叫路線引擎。
- 綠色不用在來源類型上。

**CR-01：路線快照與上傳的歷史 GPX 不需要第六種型別。**

- 路線快照是 `snapshot`：`snapshot_at` 是快照各方向的 `fetched_at` 中最晚的一個（4.14），`version` 記錄引擎的版本與圖資日期，`source` 寫路線引擎與圖資的名稱，`coverage` 寫路線的起訖名稱與行程型態。一般模式下新取得的路線也先存成快照再使用，所以型別同樣是 `snapshot`，不是 `live_api`。
- 由目標路線 GPX 或示範路線建立的路線是 `local_derived`：`built_at` 是建立路線的時間。
- 由上傳的歷史 GPX 重建的個人配速表仍是 `local_derived`：`built_at` 是重建的時間，`version` 是 `pace_version`，`coverage` 寫可用的行程數與路段數。Rider Profile 設定檔仍是 `local_config`。
- 五種型別已經涵蓋這些來源，所以不新增型別。

建議的證據代號與各規則的對應：

| `evidence_id` | 來源 | 型別 | 使用的規則 |
| --- | --- | --- | --- |
| `EV-ETA` | 個人配速表與路線目錄 | `local_derived` | 1、2、3 |
| `EV-ROUTE`（CR-01） | 路線快照；或由目標路線 GPX、示範路線建立的路線 | `snapshot` 或 `local_derived` | 路線摘要（`route.route_evidence_id`） |
| `EV-PROFILE` | Rider Profile | `local_config` | 2 |
| `EV-DUSK` | 中央氣象署日出日沒 | `live_api` 或 `snapshot` | 1 |
| `EV-FORECAST` | 中央氣象署預報 | `live_api` 或 `snapshot` | 3 |
| `EV-AREA`（草案） | 內政部國土測繪中心的鄉鎮市區界線（本機檔案，不標成 API） | `snapshot` | 3（路段對應鄉鎮，7.13） |
| `EV-STATION` | 加油站快照 | `snapshot` | 2 |
| `EV-ROAD` | 路況事件情境檔 | `simulated` | 4 |

MVP 沒有即時路況來源：真實日期的規則 4 沒有證據，`evidence_ids` 是空清單，結果是 `UNKNOWN`。

## 7. 判定與填值規則

### 7.1 誰可以寫什麼

- 計畫中的數值（時間、油量、機率、距離）一律由主程式從工具輸出複製。Planner 不填寫數值（Q3）。
- Planner 只產生：`route_request`（CR-01；只能引用詞彙表與 Rider Profile 中的代號）、`breaks`、`refuel_stops`、`conflicts`、追問、重新規劃的提案，以及說明文字。
- CR-01：路線的幾何、里程與道路名稱只來自路線快照、目標路線 GPX 或路線目錄。Planner 不產生路線；路線服務失敗時，也不得以語言模型的輸出代替（D2）。
- `rule_results`、`plan_status` 與規則 5 的結果由 Validator 產生。Planner 不能改寫。`validator` 模組不得匯入 `planner` 或任何 LLM 客戶端（DESIGN §9.2）。

### 7.2 計畫狀態

依候選的規則 1–4：全部 `PASS` 是 `FEASIBLE`；沒有 `FAIL` 而且至少一條 `UNKNOWN` 是 `CONDITIONAL`；至少一條 `FAIL` 是 `INFEASIBLE`。

### 7.3 推薦的候選

在最後一輪的候選中，先比狀態（`FEASIBLE` 高於 `CONDITIONAL`），狀態相同取 `departure_time` 最晚的。`INFEASIBLE` 的候選不參與。結果和評估的順序無關。

### 7.4 候選評估（CR-01：取代搜尋狀態）

候選從 `earliest_departure` 開始每 15 分鐘一個，到仍可能在 `latest_arrival` 前抵達的最後一個為止。每一個候選都要評估，不分批，不截斷。

評估沒有完成時（4.4），`result_kind = evaluation_failed`：不輸出建議的出發時間，不宣稱最晚的可行出發時間，也不宣稱無可行解。只有 `evaluation.completed = true` 的 `plan` 結果，才能把推薦的候選稱為最晚的可行出發時間。

### 7.5 代表性失敗候選（Q27；CR-01 簡化）

`result_kind = infeasible` 而且最後一輪有候選時：

1. 取 `FAIL` 規則數最少的候選。
2. 平手時取 `departure_time` 最晚的。

選出的候選一律稱為「代表性失敗候選」，並標明不是有效的建議。結果和評估的順序無關。

CR-01 取消了 v0.1 的三項內容（CR-01 第 11 節「接受：簡化代表候選」）：候選都只違反規則 1 時取 `overrun_s` 最小的那一步；「最接近時間限制的候選」的名稱；`label` 與 `basis` 的對照表。G3 裁決 N7 的命名規則隨之不再適用。

任何 `INFEASIBLE` 的候選都不是有效的建議；替代方案不自動執行，也不標示為已驗證。

### 7.6 時間餘裕

`time_limit` 是 min（民用暮光終, `latest_arrival`）。暮光終是 UNKNOWN 時用 `latest_arrival`；這個情形由規則 1 的 UNKNOWN（`R1_DUSK_UNAVAILABLE`）說明。`time_limit_basis` 依 P-9 的裁決延後。`time_margin_s` 只用來顯示。

### 7.7 規則 5 的關卡（Q30；CR-01：固定模板優先）

1. 主程式先由推薦候選與路線摘要的結構化欄位組成固定模板的說明，並以規則 5 檢查。
2. Planner 的說明另外以規則 5 檢查。通過才附加在模板之後（`planner_text_status = attached`）；沒通過就不顯示，也不重新產生（`rejected`）。
3. 最終檢查保留：顯示給使用者的全部文字都必須通過規則 5。固定模板沒通過時 `result_kind = output_validation_error`：不顯示計畫狀態，不重新評估候選。
4. 每一次檢查都寫入 `rule5_log`（4.10）：固定模板、Planner 的說明、最後顯示的全部文字各一筆。這是 Q30 的內部紀錄，CR-01 沒有重開，不延後。

v0.1 的順序是 Planner 的說明優先、沒通過時重新產生一次、再改用固定模板。CR-01 改為固定模板優先，並取消重新產生（CR-01 第 11 節「接受：規則 5 以固定模板優先」「保留：規則 5 的最終檢查」）。

可追溯的檢查方式：從文字中取出數值（時間、百分比、分鐘、公里、公升），和推薦候選與路線摘要（CR-01）的結構化欄位依同一套顯示格式比對。規則編號與 5.4 的設定值不算在內。顯示格式見 OQ-6。

CR-01 對道路名稱的檢查，分兩步：

1. 先把 `route.road_names` 與詞彙表名稱在文字中逐字出現的地方遮蔽，再取數值。這樣道路名稱裡的數字（例如公路的編號）不會被當成數值。
2. 再以 5.4 的固定樣式找出文字中的道路寫法。找到不在 `route.road_names` 裡的道路寫法時，這段文字不通過。

### 7.8 重新規劃（Q19、Q28）

初次評估之後最多 2 次。提案不合法（改了不能改的欄位、加油的檢查點不是有資料的加油站），或和前一輪沒有實質差異時，提前停止並記錄 `stop_reason`。

### 7.9 E2

E2 的三組都輸出 PlanResult。A3 的 `status_origin` 是 `validator`；A1、A2 是 `llm_declared`。其他差異由 E2 的規格定義。

CR-01：E2 的每一題是一個路線代號加上條件，路線代號對應凍結的路線快照；有工具的組別讀同一份路線。A1 沒有工具，只收到文字描述的行程與條件。任何一組都不會收到座標或私有的幾何（第 2 節「對語言模型的隱私」）。題目的格式由 E2 的規格定義（DESIGN §6.3）。

修改 A2／A3 時，整體流程的差異必須明確記錄（CR-01 第 11 節「保留」）。CR-01 本身已經改了 A3 的整體流程，這三項要和之後的修改一樣記錄在 E2 的規格裡：

- 規劃之前先做路線解析（7.10）。
- 候選全數評估，不分批（7.4）。
- 說明以固定模板優先（7.7）。

A2 與 A3 仍共用相同的路線快照、候選集合、工具與資料快照（Q12）。

審查處置的修正 5：E2 的報告必須把 A2 與 A3 的整體流程差異明確列出，和各項指標一起呈現。自由文字的路線解析（7.10）不在 E2 的範圍內，另由端到端的 Demo 驗收，不納入 E2 已驗證的主張。真實行程題的 Oracle 答案，在分析方法與模型設定凍結之後，由隔離的評估腳本使用保留行程產生（P-5）。

### 7.10 路線解析（CR-01）

1. 表單的檢查通過後，Planner 把行程描述轉成 `route_request`。提供目標路線 GPX 時不解析地點，只取 `trip_type`。
2. 缺起點、進入端或行程型態時回傳 ClarificationRequest（4.2）。
3. 主程式依 `route_request` 取得路線，順序見 7.11 第 3 項。Snapshot Mode 只讀已保存的路線快照，不呼叫路線引擎。
4. 路線引擎的結果，每個方向都通過獨立的國道檢查才採用（7.11 第 5、6 項）。採用後建立路段與檢查點，填寫 `route_id` 與 `route`。
5. 任何一步失敗時回傳 `route_error`（4.13），不評估候選。

對路線服務與地名查詢的請求只送出公開地標；私有 GPX 與住家位置不送往第三方（CR-01 D2）。送給語言模型的內容依第 2 節「對語言模型的隱私」。

### 7.11 路線模組的確定性規則（CR-01）

這張表是路線模組各項規則的唯一定義處。DESIGN.md 只寫摘要並指向這裡；兩份文件不互相把定義推給對方。「待定」的項目附上期限，定案後寫回這張表。都尚未實作。

| 編號 | 項目 | 規則 | 狀態 |
| --- | --- | --- | --- |
| 1 | `snapshot_id` 的樣式 | 一條路線對應一個路線快照，一個代號。提案：`SN-` 加 10 個小寫十六進位字元，取自 `request_key` 與各方向折線合併後的 SHA-256 的前 10 碼，樣式 `^SN-[0-9a-f]{10}$`。同一個請求得到相同的折線時代號相同；圖資更新使折線改變時是新的代號。路線引擎路線的 `route_id` 用同一組十六進位字元（第 2 節）。不同的內容得到相同的代號時報錯，不覆寫 | **提案，待專題負責人確認**（P-3 裁決：Spec 凍結前定義，不留給 Tickets；SB-1） |
| 2 | 回程的產生 | 來回行程是一個路線快照、兩個方向。去程與回程各送一次請求：回程的請求把起點與終點對調，途經點依相反的順序。回程不由去程的折線反轉產生。同一組起訖與途經點的去程與回程，不保證走相同的道路。**目標路線 GPX（審查處置的修正 3）：** 系統不由幾何推定行程型態；行程型態只來自表單、行程描述或追問。騎士指定來回時，還要符合下列之一才當成 `round_trip`：(a) 騎士明確指定折返點（詞彙表中的地標）；(b) GPX 本身是來回的幾何，起點與終點的距離在端點門檻內（第 8 項）。兩者都不符合時不規劃，回傳 `route_error`；系統不自行補上回程 | 回程的產生已定（CR-01 審查後的處置 L-3）。目標路線 GPX 的來回條件已定（修正 3）；`target_gpx` 的來回路線沒有 `legs`。(b) 沒有指定折返點時折返點取在哪裡、不符合條件時的 `code` 與文字，待定（SB-7） |
| 3 | 取得路線的順序 | (a) 有目標路線 GPX：用它的幾何，不呼叫路線引擎。(b) Snapshot Mode：只讀 `request_key` 相同的已保存快照；沒有時回 `snapshot_missing`。(c) 一般模式：呼叫路線引擎，通過檢查後先存成快照再使用。引擎失敗或結果不採用時回 `route_error`，不自動改用舊的快照 | (a)(b)(c) 已定。一般模式下，同一個請求已經有快照時要不要直接使用、不再呼叫引擎，待定（SB-8；公開伺服器只能低頻使用）。同一個 `request_key` 有多個快照時 Snapshot Mode 用哪一個，一起定 |
| 4 | Snapshot Mode 的比對 | `request_key` 由 `trip_type`、`origin`、`destination`、`via` 的代號（含 `entry_ref_id`，依順序）與 `routing_params` 組成的正規化字串取雜湊。完全相同才算同一個請求。不含座標 | 已定；正規化的寫法由 Tickets 寫定 |
| 5 | 獨立的國道檢查 | 逐方向判定，結果記在 `freeway_check`。`pass` 的條件：這個方向上道路等級是國道的里程為 0，而且道路名稱不含國道。它和引擎回報的 `has_highway` 分開判定，分開記錄。道路等級與名稱怎麼取得，記在 `freeway_check_method`。檢查 C4b 用的做法是對同一個伺服器再送一次道路屬性查詢，只送出引擎自己回傳的折線；這個做法的道路屬性仍來自同一個引擎與圖資 | 判定條件已定。產品用哪一種做法取得道路屬性，待定（SB-8） |
| 6 | 採用條件 | 每個方向都是 `freeway_check = pass` 才採用，才存成快照。這一條沒有例外，和路線參數無關 | 已定（CR-01 第 16 節；處置 L-5） |
| 7 | 回應的警告 | 路線參數是 `use_highways: 0`（P-1 裁決），請求不送出硬性排除（`exclude_highways`）。回應出現任何警告就不採用，回傳 `route_error`（`routing_unavailable`）。`use_highways: 0` 是偏好，不是保證：採用與否仍由第 5、6 項的獨立國道檢查決定。已知限制：這個設定可能連快速公路也避開，平面轉場較慢（檢查 C4b） | 已定（P-1 裁決，2026-11-15） |
| 8 | 端點偏移 | 每個方向量出要求的地標到折線起點、終點的距離，記在 `endpoint_offset_m`。路線服務在目的地附近沒有道路時仍會回傳路線，而且沒有警告，所以產品要自己量 | 量測與記錄已定。偏移多大時不採用這條路線，門檻待定（SB-8） |
| 9 | 預設休息的排入 | 由這份 Spec 定義。已定的部分：行程描述與追問都沒有給休息安排時才排入；由主程式排，不經過語言模型；同樣的路線與 Rider Profile 得到同樣的結果；休息只能排在檢查點之後（契約 4 的 `after_checkpoint_id`）；排入的每一筆 `origin = rider_profile`；重新規劃可以調整它們（7.8） | Rider Profile 的預設休息用哪些設定值表示、排在哪些檢查點，待定（SB-8，定案後寫進這一列） |
| 10 | `ridden_share_pct` 的算法 | 由這份 Spec 定義。分母是路線的總里程（`distance_m`）。分子是路線中「騎過」的路段的里程總和。一個路段算騎過：它的幾何和至少一趟配速行程裁切後的軌跡重合，不分方向。來回行程的去程與回程分開比對，再加總。只用幾何，不讀時間。保留行程與被排除的行程不參與比對，所以這個比例不代表騎士騎過的所有道路；介面稱為「配速資料中的路線涵蓋比例」（審查處置的修正 1）。沒有配速行程可以比對時為 `null` | 只比對配速行程已由審查處置確認（修正 1）。「重合」的距離門檻與最短長度待定（SB-8） |
| 11 | 去回里程差 | `leg_length_diff_pct` 是去程與回程里程相減的絕對值，除以兩者的平均，再乘以 100。大於 2 時 `leg_length_diff_flag = true`，介面在路線摘要標示。它只是告知，不影響路線是否採用 | 已定（處置 L-3） |

### 7.12 行程描述的本機輸入保護（CR-01 審查處置的修正 2；草案）

行程描述（`free_text`）會送給語言模型，語言模型的 API 是第三方（第 2 節）。只在介面上提醒不要寫住家地址並不足夠，所以送出前先在本機檢查。尚未實作；擋下的樣式是草案，凍結前確認（SB-6）。

| 編號 | 項目 | 規則 |
| --- | --- | --- |
| 1 | 時機 | 屬於表單檢查：在建立規劃請求、呼叫語言模型之前執行。檢查本身不經過語言模型，也不呼叫任何外部服務 |
| 2 | 擋下的樣式 | (a) 門牌的寫法：數字後面接「號」，或數字搭配「巷」「弄」「樓」「之」等門牌用語。(b) 座標的寫法：成對的小數經緯度。確切的樣式清單在凍結前補齊 |
| 3 | 命中時 | 不送出，不進入規劃，回到表單，在欄位下方顯示 5.5 的固定訊息。沒有「仍然送出」的選項（CR-01 D2：住家位置不送給第三方） |
| 4 | 誤擋 | 公開地標的門牌地址也會被擋下；騎士改用公路或地標的名稱 |
| 5 | 明確的限制 | 這是樣式比對，只能擋下常見的寫法。以地名、店名或敘述透露的住家位置（例如「我家巷口的超商」）擋不住。這份 Spec 與產品都不宣稱行程描述一定不含私人地址；介面的說明與期末報告的限制要寫明這一點 |
| 6 | 紀錄 | 被擋下的文字不寫入結果、紀錄檔或實驗紀錄 |
| 7 | E2 | 題目的文字由題庫提供，同樣先通過這個檢查 |

### 7.13 路段對應鄉鎮與預報時段（CR-01 審查處置 P-4 與修正 4；草案）

鄉鎮界線採用內政部國土測繪中心的鄉鎮市區界線（P-4 裁決），存成本機檔案。路段在本機對應到鄉鎮，再查氣象署的鄉鎮預報；座標不送到任何外部服務。尚未實作。界線資料的版本與授權條款還沒有查證；鄉鎮和氣象署預報地點的對照、預報產品的時段長度與涵蓋區間，都要等 C3 的真實 API 驗證（SB-3、SB-4、SB-5）。這份 Spec 不假設預報的時間解析度。

| 編號 | 項目 | 規則 |
| --- | --- | --- |
| 1 | 對應 | 路線目錄的每個路段，以它的折線點落在哪些鄉鎮市區的界線內，決定它經過的鄉鎮 |
| 2 | 跨鄉鎮 | 一個路段經過多個鄉鎮時全部採用；`pop_pct` 取這些鄉鎮中最高的值。不做里程加權，不取平均 |
| 3 | 對應失敗 | 折線點不在任何界線內時取最近的鄉鎮；距離超過門檻就算對應失敗（門檻的數值待定）。鄉鎮在預報中找不到對應的地點也算對應失敗。路段有任何一部分對應失敗、其餘部分又沒有 `HIGH_ALERT` 時，`pop_pct` 與 `pop_class` 是 `null`，不得當成 `LOW`；這個路段在規則 3 的範圍內時，規則 3 是 UNKNOWN（`NO_SOURCE`，`R3_AREA_UNMAPPED`）。其餘部分已有 `HIGH_ALERT` 時照常判定（FAIL 優先，SD-11） |
| 4 | 預報時段 | 預報中的每一筆降雨機率對應一個時段（起、訖）。路段的抵達時段是 [`arrival_typ`, `arrival_safe`]；所有和它重疊的預報時段都採用，`pop_pct` 取其中最高的值。採用的範圍記在 `forecast_period_start` 與 `forecast_period_end`，單筆時段的長度記在 `forecast_resolution_h` |
| 5 | 超出涵蓋區間 | 抵達時段有任何部分不在預報的涵蓋區間內、已涵蓋的部分又沒有 `HIGH_ALERT` 時，`pop_pct` 是 `null`；路段在規則 3 的範圍內時，規則 3 是 UNKNOWN（`OUT_OF_COVERAGE`） |
| 6 | 時間解析度的說法 | 降雨機率是整個預報時段的數值。介面與說明只能寫成「某個預報時段的降雨機率」，並保留時段的起訖與長度；不得把 12 小時一筆的資料寫成抵達那一刻的降雨機率。天氣的文字由固定模板產生（5.5、7.7） |
| 7 | 來源證據 | `EV-FORECAST` 的 `coverage` 記錄預報的涵蓋區間與時段長度。界線檔另有 `EV-AREA`（`snapshot`：`snapshot_at` 是下載日期，`version` 是資料版本）；它是本機的資料檔，不標成 API（G3 裁決 N6） |
| 8 | 對應結果的存放 | 路段對應到哪些鄉鎮，記在路線目錄的衍生資料還是規劃結果，還沒有定；前者要改契約 2（SB-3） |

## 8. 介面讀取的欄位

版面見 G3 凍結的 UI 文件與 [UI_CR01_DELTA](../ui/UI_CR01_DELTA.md)（提案，待專題負責人確認）。這裡只列出各區塊的資料來源。Profile 區的涵蓋度摘要不來自 PlanResult，不在這張表內。

| 畫面區塊 | 欄位 |
| --- | --- |
| 計畫狀態標籤 | `result_kind`、推薦候選的 `plan_status` |
| 評估失敗的訊息（CR-01：取代搜尋狀態標籤與提示） | `result_kind`、`evaluation` |
| 追問區塊（CR-01） | ClarificationRequest 的 `questions` |
| 路線確認區塊、路線摘要、去回里程差的標示、配速資料涵蓋比例的句子（CR-01） | `route`，加上 5.5 的固定文字 |
| 路線錯誤（CR-01） | `route_error` |
| 期限的顯示名稱（CR-01） | `adopted_conditions.route_request.trip_type` |
| 待確認事項 | 推薦候選中 `result = UNKNOWN` 的 `rule_results[].manual_check_guidance` |
| 四張數值卡片 | 推薦候選的 `departure_time`、`eta_typ_end`、`eta_safe_end`、`time_margin_s` |
| 說明 | `explanation.text`；CR-01：`explanation.planner_text` 與 `explanation.planner_text_status` |
| 採用的條件、衝突提示 | `adopted_conditions` |
| 加油安排 | 推薦候選的 `fuel_plan` |
| 天氣 | 推薦候選的 `weather` |
| 來源證據 | `evidence` |
| 頂端的 Snapshot Mode 標籤 | `adopted_conditions.data_mode`（描述畫面上的結果） |
| 結果過期 | 表單和 `adopted_conditions` 的比對。CR-01：Profile 更新後，另以 `EV-ETA` 的 `version` 和目前的 `pace_version` 比對 |
| 逐條規則結果 | `rule_results` |
| 最終輸出的驗證 | `explanation.rule5`，或 `result_kind` |
| 全部候選 | `candidates` 中最後一輪的候選（`round_index` 最大的）。CR-01：唯讀，不選取。先前各輪的候選保留在結果裡，介面不顯示 |
| 重新規劃紀錄 | `replan_rounds` |
| 無可行解 | `infeasibility_report` |

## 9. 驗收與測試規格

實作時必須有的測試。目前都**尚未實作**。

| 編號 | 測試 |
| --- | --- |
| S1 | PlanResult 與 ClarificationRequest 通過 JSON Schema 驗證；缺必填欄位、型別錯誤、沒有時區的時間都被拒絕 |
| S2 | `result_kind` 和 `recommended_plan_id`、`explanation`、`infeasibility_report` 的組合符合 4.3 的表。CR-01：加上 `route`、`route_error` 與 `evaluation.completed` |
| S3 | CR-01 取代：`evaluation.completed = true` 時 `candidates_evaluated` 等於 `candidates_total`。評估中途失敗時 `result_kind = evaluation_failed`、`recommended_plan_id` 是 `null`，結果的文字中沒有「最晚的可行出發時間」，也沒有無可行解的結論 |
| S4 | `result = UNKNOWN` 的規則一定有 `reason_class` 與 `manual_check_guidance`，指引文字和 5.3 完全相同。CR-01：依規則編號與 `reason_class` 查表 |
| S5 | 各條件下的 `result`、`reason_class` 與 `reason_code` 符合 5.2 的表（P-9 裁決：`reason_code` 維持必填） |
| S6 | 每個 `evidence_ids` 都指向存在的 `evidence` |
| S7 | Evidence 的時間欄位和 `source_type` 一致；`simulated` 和 `source_type` 一致 |
| S8 | Snapshot Mode 的結果沒有 `live_api`；個人配速表與 Rider Profile 不會是 `live_api` |
| S9 | `station_status = UNKNOWN` 的加油站之後，剩餘油量是 `null` |
| S10 | 結果中沒有座標欄位。CR-01：也沒有折線、目標路線 GPX 的路徑與檔名；道路名稱與公開地標的名稱可以出現 |
| S11 | CR-01 簡化：代表性失敗候選是 `FAIL` 規則數最少、其次出發時間最晚的候選；結果和評估的順序無關 |
| S12 | `adopted_conditions` 反映重新規劃後的安排；路線、日期與時間限制沒有被改動 |
| S13 | `rule5_log` 記錄每一次檢查。沒通過規則 5 的 Planner 說明不在 `explanation` 裡，`planner_text_status = rejected`；固定模板沒通過時 `result_kind = output_validation_error` |
| S14 | CR-01：`route_error` 的五種 `code` 各有一個案例。結果符合 4.13：沒有 `route`，`candidates` 是空清單，`message` 與 `actions` 和 5.5 完全相同 |
| S15 | CR-01：路線引擎失敗，或回傳的路線沒有通過獨立的國道檢查時，結果中沒有任何路線的里程與道路名稱；Planner 的輸出不會被當成路線。一般模式下不會自動改用舊的路線快照 |
| S16 | CR-01：`route.freeway_check` 不為 `fail`。三種 `route_source` 各有一個案例，欄位的必填與 `null` 符合 4.12 的跨欄位規則 |
| S17 | CR-01：Snapshot Mode 下不呼叫路線引擎；沒有對應的路線快照時回傳 `snapshot_missing` |
| S18 | CR-01：ClarificationRequest 的 `topic` 只有五個值；`start_point` 與 `entry_side` 的選項都存在於詞彙表或 Rider Profile |
| S19 | CR-01：`route_request` 的每個 `ref_id` 都存在於詞彙表或 Rider Profile。行程型態在表單與行程描述不一致時以表單為準，並有 ConflictNotice |
| S20 | CR-01：顯示的文字中，道路寫法都在 `route.road_names` 裡（7.7 的兩步檢查）；涵蓋比例句子的數值等於 `route.ridden_share_pct`，去回里程差句子的數值等於 `route.leg_length_diff_pct` |
| S21 | CR-01：來回行程中，去程與回程都經過的加油站在 `fuel_plan.checkpoints` 出現兩次，`checkpoint_id` 不同；`turnaround_checkpoint_id` 指向 `kind = turnaround` 的檢查點 |
| S22 | CR-01：送給語言模型的內容（提示與工具輸出）沒有座標樣式的數值，沒有折線、軌跡點、GPX 的路徑與檔名，也沒有逐趟的騎乘資料（第 2 節） |
| S23 | CR-01：路線快照符合 4.14。來回行程的快照有 `outbound` 與 `return` 兩筆 `legs`，各有自己的 `request`、`shape` 與 `fetched_at`；`return` 的折線不是 `outbound` 的反轉。每一筆都有 `warnings`、`has_highway`、`freeway_check`、`freeway_check_method` 與兩端的 `endpoint_offset_m` |
| S24 | CR-01：`freeway_check` 為 `fail` 的方向不會存成快照，結果是 `highway_in_route`。去回里程差大於 2% 時 `leg_length_diff_flag = true` |
| S25 | CR-01：Rider Profile 的預設休息排入後，每一筆的 `origin = rider_profile`，都排在檢查點之後；同樣的輸入得到同樣的安排（7.11 第 9 項） |
| S26 | 審查處置：行程描述含門牌或座標的樣式時（7.12 的每一類各一個案例），不建立規劃請求，也不呼叫語言模型；顯示 5.5 的固定訊息 |
| S27 | 審查處置：目標路線 GPX 不會被系統推定為來回。行程型態不由幾何決定；騎士指定來回、但不符合 7.11 第 2 項的條件時回傳 `route_error` |
| S28 | 審查處置：`pop_pct` 有值的 WeatherSegment 一定有 `forecast_period_start`、`forecast_period_end` 與 `forecast_resolution_h`；顯示的文字沒有把降雨機率寫成某一時刻的預報 |
| S29 | 審查處置：路段對不到鄉鎮時 `pop_pct` 是 `null`，不是 `LOW`；路段經過多個鄉鎮時 `pop_pct` 是其中最高的值（7.13） |
| S30 | 審查處置：送給路線引擎的請求帶 `use_highways: 0`，不帶硬性排除；回應有警告時結果是 `route_error`（`routing_unavailable`） |
| D1–D16 | DESIGN §8 列出的排序與候選搜尋測試（目前 16 項）。CR-01：以 DESIGN.md 修訂後的清單為準；分批與 INCOMPLETE 的測試改為完整評估與評估失敗的測試 |

## 10. 這份 Spec 做的決定

G1 第 8 節註明名稱與型別由 Spec 定案。除了命名之外，以下幾項是這份 Spec 新增或改動的，請逐項審查。

「CR-01 後的狀態」一欄只記錄 CR-01 造成的變化。v0.1 的審查在 CR-01 之前暫停，專題負責人還沒有逐項審查這張表：標為「維持，待審查」的項目不是已確認的決定。

「取代」來自 CR-01 第 11 節明列的裁決（簡化代表候選、規則 5 以固定模板優先、取消分批與搜尋狀態）。初稿標為「提議延後」的三個欄位已由審查處置 P-9 裁決（2026-11-15）：`reason_code` 維持必填，`time_limit_basis` 與 `overrun_s` 延後。

G1 沒有重開的決議維持有效，它們需要的欄位不得延後（CR-01 審查後的處置 L-6）：保留全部評估過的候選（Q14）、UNKNOWN 的四項（Q25）、每一輪的結構化變更摘要（Q29）、規則 5 的內部紀錄（Q30）。這份 Spec 的初稿曾把其中幾項標為延後，已經改回。

| 編號 | 決定 | 理由 | CR-01 後的狀態 |
| --- | --- | --- | --- |
| SD-1 | `source_type` 由三種增為五種，加入 `local_derived` 與 `local_config` | G3 裁決 N6 | 維持，待審查。CR-01 的新來源不需要第六種（第 6 節） |
| SD-2 | RuleResult 的 `evidence_ids` 是清單，不是單一的 `evidence_id` | 一條規則會用到多個來源，例如規則 1 用 ETA 與暮光終 | 維持，待審查 |
| SD-3 | 新增 `reason_code` | 讓「具體原因」與指引可以查表並測試。不需要時可以拿掉，只保留 `reason` | **維持必填（P-9 裁決）**：保留穩定的原因代碼。指引依規則編號與 `reason_class` 查表（SD-19） |
| SD-4 | 規則 2 有兩則指引 | DESIGN §4.2 的規則 2 有兩種 UNKNOWN：缺營業時間、缺 Rider Profile 的數值 | 維持，待審查 |
| SD-5 | 新增 `result_kind` 與 ClarificationRequest | 把有計畫、無可行解、輸出驗證錯誤、追問四種回應分清楚；都是 G1 已決定的行為 | 擴充：`result_kind` 新增 `route_error` 與 `evaluation_failed`（SD-16、SD-17） |
| SD-6 | `candidates` 保留每一輪的候選，以 `round_index` 區分；介面的表格與 FAIL 統計只用最後一輪 | Q14 要求保留全部評估過的候選；凍結的原型顯示的是最後一輪 | 維持，不延後：Q14 不在 CR-01 的重開範圍內。初稿曾標為延後，已改回 |
| SD-7 | 新增 `time_limit` 與 `time_limit_basis` | 暮光終是 UNKNOWN 時，時間餘裕的基準要說清楚 | `time_limit` 維持，待審查；`time_limit_basis` **延後（P-9 裁決）** |
| SD-8 | Evidence 新增 `built_at` 與 `version` | 本地衍生資料沒有取得時間，也沒有快照時間 | 維持，待審查 |
| SD-9 | 規則 1 新增 `overrun_s` | 代表候選要比較「超過期限最少」 | **延後（P-9 裁決）**：簡化後的選法不比較超過期限的長度 |
| SD-10 | `R*_ETA_UNKNOWN` 三個代碼與它們共用的一則指引 | ETA 輸出的狀態可以是 `unknown`（契約 4），下游規則要有對應的結果。G1 沒有討論這個情形 | 代碼隨 SD-3 維持（P-9 裁決）；結果、原因分類與指引維持，待審查 |
| SD-11 | 同一條規則同時符合 FAIL 與 UNKNOWN 的條件時，結果是 FAIL | 把 Q17（規則 1）的做法套用到規則 2、3、4。已確定違反的不因為其他資料缺漏而變成 UNKNOWN | 維持，待審查 |
| SD-12 | 休息安排的 `origin` 沒有 `form` | G1 第 8 節寫「來自表單或自然語言」，但凍結的表單沒有休息欄位。休息來自自然語言、追問的回覆、Rider Profile 或重新規劃 | 維持，待審查。CR-01：行程描述沒寫休息時依 Rider Profile 排入 |
| SD-13 | `free_text` 沿用原名，意義擴大為行程描述 | CR-01 只要一個文字欄；不改名可以少動其他欄位 | CR-01 新增，待審查 |
| SD-14 | 新增 RouteRequest 與 PlaceRef；地點只以詞彙表或 Rider Profile 的代號表示 | CR-01 第 12 節的 Must（行程描述、詞彙表、追問）；D2 不得編造路線 | CR-01 新增，待審查 |
| SD-15 | 新增 RouteSummary。獨立的國道檢查結果是 `freeway_check`，在非路線引擎的來源是 `null`；另有 `turnaround_checkpoint_id`，指向 `kind = turnaround` 的檢查點 | 結果要顯示里程、道路名稱與騎過多少；加油安排要分得出去程與回程 | CR-01 新增，待審查。審查後把初稿的 `has_highway` 改名為 `freeway_check`（SD-26） |
| SD-16 | 新增 `route_error`、RouteError 與五種 `code` | D2：路線服務失敗時必須有明確的錯誤處理 | CR-01 新增，待審查 |
| SD-17 | Evaluation 取代 SearchStatus；新增 `evaluation_failed` | CR-01 第 11 節「附條件接受」的兩個條件 | CR-01 新增，待審查 |
| SD-18 | 路線快照的來源型別是 `snapshot`，一般模式也一樣；Snapshot Mode 不呼叫路線引擎 | D2：Demo 與 E2 使用凍結的快照 | CR-01 新增，待審查 |
| SD-19 | 人工確認指引依規則編號與 `reason_class` 查表 | 不論 `reason_code` 是否延後，都查得到固定的指引 | CR-01 新增，待審查 |
| SD-20 | ReplanRound 新增 `change_summary`，是 `changes` 的顯示文字 | 介面的重新規劃紀錄要一段固定模板的文字。`changes`（Q29 的結構化變更摘要）維持必填，不由它取代 | CR-01 新增，待審查。初稿曾以它取代 `changes`，已改回 |
| SD-21 | Explanation 以 `planner_text` 與 `planner_text_status` 取代 `origin`；Rule5Attempt 的 `text_origin` 改為 `template`、`planner`、`final_output` | 固定模板優先之後，模板一定存在，Planner 的說明是附加的；重新產生已取消。`rule5_log` 維持必填（Q30） | CR-01 新增，待審查 |
| SD-22 | 追問主題的 `break_location` 併入 `other` | CR-01 的追問主題是起點、進入端、行程型態與休息長度 | CR-01 新增，待審查 |
| SD-23 | 提供目標路線 GPX 時路線以 GPX 為準 | 兩個路線來源同時出現時要有確定的結果 | CR-01 新增，待審查 |
| SD-24 | 5.5 的固定文字，以及「道路寫法必須出現在 `road_names`」的兩步檢查（7.7） | 路權提醒、配速資料的涵蓋比例與錯誤訊息都不由 LLM 產生 | CR-01 新增；文字是提案，待確認 |
| SD-25 | 新增 RouteSnapshot 與 RouteLeg（4.14）：一條路線一個快照，`legs[]` 逐方向記錄請求、折線、警告、`has_highway`、`freeway_check` 與方法、`endpoint_offset_m`、取得時間；高度選填 | CR-01 審查後的處置 L-3、L-4：路線快照的欄位由這份 Spec 定義；回程另送請求，不反轉折線 | 審查後新增，待審查 |
| SD-26 | RouteSummary 以 `freeway_check` 表示獨立的國道檢查；引擎回報的 `has_highway` 只記在路線快照。新增 `leg_length_diff_pct` 與 `leg_length_diff_flag` | 不讓同一個名稱有兩種意義；去回里程差超過 2% 時要在路線摘要標示（L-3） | 審查後新增，待審查 |
| SD-27 | `request_key` 與 Snapshot Mode 的比對；一般模式不自動改用舊的路線快照；回應因為警告或端點偏移而不採用時，暫定歸在 `routing_unavailable` | Snapshot Mode 要能確定地找到快照；路線服務失敗時要有明確的錯誤（D2） | 審查後新增，待審查。警告的處理已由 P-1 裁決（7.11 第 7 項） |
| SD-28 | `ridden_share_pct` 的算法（7.11 第 10 項）：只和配速行程的幾何比對，不分方向，來回行程分方向比對再加總 | DESIGN 與 Spec 原本互相把算法推給對方；保留行程不進配速表，所以也不算「騎過」 | 只比對配速行程已由審查處置確認（修正 1），介面名稱改為「配速資料中的路線涵蓋比例」。距離門檻待定（SB-8） |
| SD-29 | 預設休息的排入規則由這份 Spec 定義（7.11 第 9 項） | 同上；休息安排是 Plan Schema 的欄位 | 審查後新增。已定的部分待審查；設定值與排入的位置待定 |
| SD-30 | ID 的確切格式（第 2 節；7.11 第 1 項）：`route_id` 的三種樣式、`checkpoint_id` 與 `snapshot_id` | P-3 裁決：Spec 凍結前定義，不留給 Tickets；`trip_id` 與 `R01`／`R02` 不變 | 審查處置後新增；提案，待專題負責人確認（SB-1） |
| SD-31 | 行程描述的本機輸入保護（7.12）與它的固定訊息（5.5） | 審查處置的修正 2：不得只靠提示語 | 審查處置後新增；草案，待確認（SB-6） |
| SD-32 | 路段對應鄉鎮與預報時段的規則（7.13）；WeatherSegment 新增三個預報時段的欄位；新增 `R3_AREA_UNMAPPED` 與 `EV-AREA` | P-4 裁決與審查處置的修正 4 | 審查處置後新增；草案，待確認（SB-3、SB-4） |
| SD-33 | 目標路線 GPX 的來回條件（7.11 第 2 項） | 審查處置的修正 3 | 審查處置後新增；折返點的取法與錯誤的 `code` 待定（SB-7） |

## 11. 裁決、Spec Blockers 與待審查的事項

### 11.1 P-1 至 P-11 的裁決與尚未解決的 Spec Blockers

專題負責人在 2026-11-15 的審查處置中對 P-1 至 P-11 作出裁決，並提出五項修正；**這份 Spec 的凍結尚未批准**。完整的紀錄在 [CR-01](../cr/CR-01-proposal-alignment.md) 第 18 節。編號沿用 [lead 的處置](../cr/CR-01-appendix/lead_dispositions.md)第 3 節；G1 第 11 節與 UI_CR01_DELTA 都指向這一節，DESIGN.md §13.5 以同樣的編號列出同一批裁決。lead 先前的建議和裁決不同的地方，以裁決為準。年份都是 2026。

| 編號 | 事項 | 裁決 | 對這份 Spec 的影響 |
| --- | --- | --- | --- |
| P-1 | 路線參數 | 採 `use_highways: 0`，每個方向另做獨立的國道檢查，通過才採用。不送出硬性排除；回應出現任何警告就不採用。要記錄的限制：這個設定可能連快速公路也避開，平面轉場較慢 | 4.12、4.13、4.14、7.11 第 7 項 |
| P-2 | 停等寬放 | 升為 Must。先處理 `ingest` 的假停留；寬放只用配速資料決定；不得和既有的安全餘裕重複計算；需要改契約時明確提出 | 5.4；沒有新增欄位，等 SB-2 |
| P-3 | `route_id`、`checkpoint_id`、`snapshot_id` 的格式 | 確切格式在 Spec 凍結前定義，不延到 Tickets 才決定。既有的 `trip_id` 與 `R01`／`R02` 不變 | 第 2 節、7.11 第 1 項（提案，SB-1） |
| P-4 | 路段對應鄉鎮的資料來源 | 採用國土測繪中心的鄉鎮界線，在本機把路段對應到氣象署的鄉鎮預報。跨鄉鎮、對應失敗與 PoP 預報時間窗的處理要明確定義 | 4.8、5.2、第 6 節、7.13（草案，SB-3） |
| P-5 | 保留行程與 E2 Oracle 的先後 | 先凍結 E1／E2 的分析方法與模型設定，再由隔離的評估腳本使用保留行程。禁止依保留行程的結果調整模型或規則 | 7.9；不影響欄位 |
| P-6 | E1 的路線引擎 ETA | 只在公開地標之間、時間定義相容的路段比較；不宣稱整趟的比較 | 不影響欄位 |
| P-7 | 2026-11-14 被排除的那一趟 | 維持排除 | 不影響欄位；7.11 第 10 項的比對範圍不含這一趟 |
| P-8 | 規則 3 在來回行程上的範圍（D3） | 暫不選曲率或固定高度的定義。lead 在 11/27 前提出有固定規則、可重現、符合研究目標的最小方案，再由專題負責人定案 | 4.8、5.2、5.4（未定，SB-9） |
| P-9 | Spec 提議延後的欄位 | 保留 G1 Q14／Q25／Q29／Q30 所需的欄位與穩定的原因代碼（`reason_code`）。`time_limit_basis` 與 `overrun_s` 可以延後 | 4.5、4.6、5.2、5.3、7.6、第 10 節 |
| P-10 | E2 落後時的處理 | 正式 E2 最晚 12/8 開始。題數不足 12–15 題時，必須明示未達原訂的驗收條件，不可事後降低標準 | 不影響欄位 |
| P-11 | 路線確認與手機、鍵盤的驗收 | 路線確認不增加強制的點擊。保留基本的驗收：375 像素寬度沒有整頁溢出、可以用鍵盤操作 | 不影響欄位 |

**額外修正**

| 修正 | 內容 | 這份 Spec 的位置 |
| --- | --- | --- |
| 1 | `ridden_share_pct` 只比對配速行程；介面稱為「配速資料中的路線涵蓋比例」，不得宣稱它代表使用者騎過的所有道路 | 4.12、5.5、7.11 第 10 項 |
| 2 | 不得只靠提示語宣稱 `free_text` 絕不含私人地址；補上本機的輸入保護與明確的限制 | 第 2 節、4.1、5.5、7.12（草案） |
| 3 | `target_gpx` 沒有明確提供折返點或來回的幾何時，不得自行推定為 `round_trip` | 4.1、7.11 第 2 項 |
| 4 | 天氣資料的時間解析度與預報涵蓋區間必須保留；不能把 12 小時的 PoP 解釋成精確時刻的預報 | 4.8、5.5、7.13（草案） |
| 5 | E2 的報告必須明確區分 A2／A3 的整體流程差異；自由文字的路線解析另由端到端 Demo 驗收，不納入 E2 已驗證的主張 | 7.9 |

**尚未解決的 Spec Blockers。** 下列事項解決之前不凍結這份 Spec，也不建立 Tickets。

| 編號 | 事項 | 現況 | 需要什麼 |
| --- | --- | --- | --- |
| SB-1 | ID 的確切格式（P-3） | 提案已寫入 SPEC-001 第 2 節與 7.11 第 1 項 | 專題負責人確認格式 |
| SB-2 | 停等寬放的定義與契約變更（P-2） | 原則已寫入 DESIGN §6.1。還沒有定義的：「短停留」的界定、寬放的算式、和安全餘裕係數的關係式。需要的契約變更是提案：契約 3（配速表）新增寬放的參數與依據；契約 4（ETA 輸出）新增寬放的分項 | lead 提出定義草案；專題負責人核准契約變更 |
| SB-3 | 路段對應鄉鎮的規則（P-4） | 規則草案在 SPEC-001 7.13。界線資料的版本與授權條款還沒有查證；最近鄉鎮的距離門檻未定；鄉鎮和氣象署預報地點的對照沒有驗證；對應結果存在路線目錄還是規劃結果未定（前者要改契約 2） | 專題負責人確認草案；對照要等 C3 |
| SB-4 | 預報時段的欄位（修正 4） | 欄位草案在 SPEC-001 4.8。氣象署實際回應的時段長度與涵蓋區間沒有驗證 | C3 完成後確認 |
| SB-5 | C3：真實 API 驗證 | **BLOCKED／NOT RUN**。沒有 Anthropic 憑證，沒有氣象署授權碼；沒有以模擬結果代替 | 憑證與授權碼到位後執行（費用上限 US$3） |
| SB-6 | 行程描述的本機輸入保護（修正 2） | 規則草案在 SPEC-001 7.12；擋下的樣式清單與訊息文字是草案 | 專題負責人確認 |
| SB-7 | 目標路線 GPX 的來回條件（修正 3） | 條件已寫入 SPEC-001 7.11 第 2 項。沒有指定折返點時折返點取在哪裡、不符合條件時的錯誤代碼與文字未定 | lead 提案；專題負責人確認 |
| SB-8 | SPEC-001 7.11 其餘待定的項目 | 第 3 項（已有快照時是否重用、多個快照時用哪一個）、第 5 項（國道檢查的資料來源）、第 8 項（端點偏移的門檻）、第 9 項（預設休息的設定）、第 10 項（重合的距離門檻） | lead 提案，寫回 7.11；不留給 Tickets |
| SB-9 | 規則 3 在來回行程上的範圍（P-8） | 未定。lead 在 2026-11-27 前提出最小方案 | 專題負責人定案；Spec 是否等它才凍結，由專題負責人決定 |
| SB-10 | 尚未逐項審查的內容 | SPEC-001 第 10 節的決定、第 11.2 節的問題、5.5 的固定文字 | 專題負責人審查 |

### 11.2 待審查的問題（這份 Spec 的暫定做法）

| 編號 | 問題 | 這份 Spec 的暫定做法 |
| --- | --- | --- |
| OQ-1 | 這份 Spec 的範圍夠不夠？它只涵蓋 Plan Schema、規則輸出與來源證據。資料工具（`sources`）的輸入輸出、知識庫與 E2 Runner 要併進來，還是各自另寫 | **已解決。裁決（2026-11-15）：各自另寫** |
| OQ-2 | Rider Profile 的平均油耗用什麼單位 | 公升／100 公里（`consumption_l_per_100km`）。若習慣用公里／公升，欄位改名 |
| OQ-3 | 加油要花多少時間，DESIGN 沒有規定 | 以一筆 `purpose = refuel` 的休息表示，長度是 Rider Profile 的設定值 |
| OQ-4 | `local_derived` 與 `local_config` 的顯示文字與標籤顏色 | 「本地衍生資料」「本地設定檔」，灰色 |
| OQ-5 | 加油站資料算 `snapshot` 還是另一種型別 | `snapshot`（G1 的實作備註稱它為加油站快照） |
| OQ-6 | 規則 5 比對數值時的顯示格式 | 時間 `HH:MM`；分鐘與百分比取整數；公升與公里取一位小數 |
| OQ-7 | 知識庫出處（Citation）的欄位 | `doc_id`、`title`、`locator`。知識庫的內容還沒有規格 |
| OQ-8 | Plan Schema 的 JSON Schema 放在哪個模組 | 留給 Tickets 決定；不修改凍結的 `contracts/` |
| OQ-9 | 規則 3 在來回行程上的範圍（CR-01 D3） | **待定案，見 11.1 的 P-8 與 SB-9。** 這份 Spec 只定義單向行程的範圍。定案後補上來回行程的判定條件、WeatherSegment 的欄位與天氣的彙總方式 |
| OQ-10 | 停等寬放（CR-01 第 15 節；C2 是 FAIL） | **已裁決為 Must（P-2）。** 算式、和安全餘裕的關係與需要的契約變更還沒有定義（SB-2）；這份 Spec 目前沒有停等寬放的欄位 |
| OQ-11 | 2026-11-14 被排除的那一趟行程要不要納入（CR-01 第 13 節） | **已裁決：維持排除（P-7）。** |
| OQ-12 | 目標路線 GPX 是單向的幾何時，要不要自動補上回程 | **已由審查處置的修正 3 定案：不補，也不由幾何推定來回**（7.11 第 2 項） |
| OQ-13 | 行程型態在表單上是不是必選 | 暫定選填：有選時以表單為準；沒選時由行程描述判斷，再沒有就追問 |
| OQ-14 | 公路與地標詞彙表要不要列為來源證據 | 暫定不列：它是知識庫的內容，出處以 Citation 表示 |
| OQ-15 | 5.5 的固定文字是否接受 | 提案如 5.5 |
| OQ-16 | 7.11 標為「待定」的項目 | 列為 SB-7、SB-8；Spec 凍結前定案並寫回 7.11，不留給 Tickets |

CR-01 技術檢查的現況：C1（曲率一致性）是 PASS；C2（整趟誤差）是 FAIL；C3（LLM 與氣象署）是 BLOCKED／NOT RUN；C4（路線快照）是 FAIL，因為公開伺服器忽略硬性排除；追加的 C4b（軟性偏好）是 PASS。C1、C4、C4b 已有結果，剩下 C3。路線參數（P-1）與停等寬放（P-2）已裁決。這些是技術檢查，不是 E1 Lite 或 E2 的結果。路線服務不可用時，騎士可以改以目標路線 GPX 提供路線；RouteSummary 已經涵蓋這個來源。

## 12. 之後的步驟

1. C3 仍是 BLOCKED／NOT RUN，要等 Anthropic 憑證與氣象署授權碼。真實 API 驗證完成之前維持這個狀態，不以模擬結果代替。
2. 解決第 11.1 節的 Spec Blockers（SB-1 至 SB-10）。lead 在 2026-11-27 前提出規則 3 在來回行程上的最小方案（P-8）。
3. 專題負責人審查第 10 節、第 11.2 節，以及標為「草案」或「提案」的內容。
4. Blockers 解決後，由專題負責人決定是否凍結這份 Spec。**凍結尚未批准。**
5. 凍結之後才建立 Tickets。路線模組、資料工具、Planner、Validator 與 Streamlit 的正式實作在 Tickets 之後。
