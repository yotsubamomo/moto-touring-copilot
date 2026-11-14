# SPEC-001 Plan Schema、規則輸出與來源證據

> 狀態：**Draft v0.1（2026-11-15），審查暫停。** 專題負責人在 2026-11-15 表示預計重新調整專題目標；除了 OQ-1 之外，第 10、11 節的項目等目標確定後再審查。尚未凍結；尚未建立 Tickets；尚未實作。
> 輸入：凍結的 [DESIGN.md](../../DESIGN.md)（§4、§5 資料契約 v0.2、§6.1、§8、§9.1、§9.2）、[G1 決議](../grill/g1-grill-input.md)（Q1–Q32 與第 8 節）、G3 凍結的 UI 文件（[UI_DESIGN](../ui/UI_DESIGN.md)、[UI_FLOW](../ui/UI_FLOW.md)、[UI_ACCEPTANCE](../ui/UI_ACCEPTANCE.md)、[G3 Audit Report](../ui/G3_AUDIT_REPORT.md) 第 7 節）。
> 這份 Spec 把 G1 第 8 節的「邏輯欄位清單」定成欄位名稱與型別，並固定規則的指引文字與來源證據的型別。它沒有新增 Must 功能。

## 1. 目的與範圍

**涵蓋。**

- 規劃請求與規劃結果的結構（Plan Schema）：欄位名稱、型別、可否為空、由誰填寫。
- 規則 1–5 的輸出：結果、原因分類、原因代碼、固定的人工確認指引。
- 來源證據的型別與時間欄位，包含本地衍生資料與本地設定檔（G3 裁決 N6）。
- 由這些欄位推導的確定性規則：計畫狀態、排序、搜尋狀態、代表候選、時間餘裕、規則 5 的關卡。
- 驗收與測試規格。

**不涵蓋。**

- 衍生路段表、路線目錄、配速表、ETA 輸出：已由資料契約 v0.2 定義並凍結，這份 Spec 只引用。
- 各資料工具的內部做法（怎麼查預報、怎麼讀加油站快照）、知識庫的內容、提示詞。
- E2 的題庫、Oracle 與 Runner：另有規格（DESIGN §6.3）。這份 Spec 只規定 E2 三組共用同一個結果結構。
- Streamlit 的版面：以 G3 凍結的 UI 文件為準。第 8 節只列出畫面讀哪些欄位。
- Should 與 Won't 的項目（地圖、下載、TDX、氣象署警特報、騎士記憶）沒有欄位。

第 10 節列出這份 Spec 自己做的決定，第 11 節是需要審查者回答的問題。

## 2. 共通規則

沿用資料契約 v0.2 的規則，另外補上 Plan Schema 需要的型別。

| 項目 | 規則 |
| --- | --- |
| 型別 | 契約已有的 `string`、`int`、`float`、`datetime`、`enum`、`list`；新增 `bool`、`date`（`YYYY-MM-DD`）與巢狀的 `object` |
| 命名 | 小寫加底線。單位寫在字尾：`_s` 秒、`_m` 公尺、`_pct` 百分比（0–100）、`_l` 公升 |
| 時間 | `datetime` 是帶 `+08:00` 的 ISO 8601 字串（Asia/Taipei）。沒有時區位移的時間無效 |
| 缺值 | `null` 表示不知道或無法計算，不得用 0、−1 或空字串代替。遇到 `null` 要往下傳遞為 UNKNOWN，不得補值（NFR4） |
| 狀態用語 | 固定用語一律大寫：`PASS`／`FAIL`／`UNKNOWN`、`FEASIBLE`／`CONDITIONAL`／`INFEASIBLE`、`COMPLETE`／`INCOMPLETE`。其他 `enum` 用小寫 |
| ID | `route_id`、`checkpoint_id`、`plan_id` 沿用契約。`plan_id` 在同一份結果中唯一。`evidence_id` 的格式是 `EV-` 加大寫英數字與連字號 |
| 隱私 | 結果中不得出現座標、原始 GPX 的時間或行程代號以外的行程資訊（NFR2）。位置只以 `route_id`、`checkpoint_id` 與 `seg_index` 表示 |
| 版本 | 每份結果帶 `plan_schema_version`，這一版是 `"0.1"` |

「填寫者」一欄的意思：**表單**是使用者在 Trip Planner 輸入的值；**Planner** 是 LLM 產生的結構化資料；**主程式**是確定性的程式，數值都從工具輸出複製；**Validator** 是確定性的規則判定，不含 LLM。

## 3. 物件總覽

```text
PlanResponse = ClarificationRequest | PlanResult

PlanResult
├── adopted_conditions : PlanRequest
│     ├── breaks[]        : BreakArrangement
│     ├── refuel_stops[]  : RefuelStop
│     └── conflicts[]     : ConflictNotice
├── search               : SearchStatus
├── candidates[]         : Candidate
│     ├── rule_results[] : RuleResult        (rules 1–4)
│     ├── fuel_plan      : FuelPlan → checkpoints[] : FuelCheckpoint
│     └── weather[]      : WeatherSegment
├── replan_rounds[]      : ReplanRound → changes[] : ArrangementChange
├── explanation          : Explanation → citations[] : Citation
├── rule5_log[]          : Rule5Attempt       (internal, never displayed)
├── infeasibility_report : InfeasibilityReport
└── evidence[]           : Evidence
```

## 4. 欄位定義

### 4.1 PlanRequest（規劃請求；結果中以 `adopted_conditions` 回顯）

| 欄位 | 型別 | 可為空 | 填寫者 | 說明 |
| --- | --- | --- | --- | --- |
| `request_id` | string | 否 | 主程式 | 一次按下「規劃」的代號 |
| `route_id` | string | 否 | 表單 | 路線目錄中的單向路線（Q1） |
| `plan_date` | date | 否 | 表單 | 可以超出預報期間（Q7） |
| `earliest_departure` | datetime | 否 | 表單 | 候選的起點（Q11） |
| `latest_arrival` | datetime | 否 | 表單 | 最晚抵達終點時間（Q1）。必須晚於 `earliest_departure` |
| `start_fuel_pct` | float | 否 | 表單 | 0–100，必填；缺少時不進入規劃（Q6） |
| `free_text` | string | 是 | 表單 | 自然語言需求的原文（Q4） |
| `breaks` | list | 否（可為空清單） | Planner | 結構化的休息安排（Q4、Q20） |
| `refuel_stops` | list | 否（可為空清單） | Planner | 補給策略：在哪些檢查點加滿（Q13、Q16） |
| `conflicts` | list | 否（可為空清單） | Planner | 自然語言與表單衝突的紀錄（Q4） |
| `data_mode` | enum | 否 | 表單 | `live` 或 `snapshot`（Q23） |
| `requested_at` | datetime | 否 | 主程式 | 按下「規劃」的時間 |

`adopted_conditions` 是最後一輪實際採用的條件：重新規劃改過的休息與加油安排會反映在這裡。介面以它和目前的表單比對，判斷結果是否過期。

**BreakArrangement**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `after_checkpoint_id` | string | 否 | 和 ETA 輸出的 `breaks` 相同（契約 4） |
| `duration_s` | int | 否 | 大於 0 |
| `purpose` | enum | 否 | `rest` 或 `refuel` |
| `origin` | enum | 否 | `free_text`、`rider_profile`、`clarification`、`replan` |

**RefuelStop**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `checkpoint_id` | string | 否 | 必須是路線目錄中 `kind = fuel_station` 的檢查點（Q19） |
| `origin` | enum | 否 | `planner` 或 `replan` |

加油一律是加滿。加油停留的時間以一筆 `purpose = refuel` 的 `breaks` 表示，這樣 ETA 才會算進去（見第 11 節 OQ-3）。

**ConflictNotice**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `field` | enum | 否 | `route_id`、`plan_date`、`earliest_departure`、`latest_arrival`、`start_fuel_pct` |
| `free_text_value` | string | 否 | 自然語言中提到的值，原文 |
| `adopted` | enum | 否 | 固定為 `form`（Q4） |
| `message` | string | 否 | 顯示給使用者的提示 |

### 4.2 ClarificationRequest（追問）

需求有歧義時回傳這個物件，不產生 PlanResult（Algorithm 1 第 02 行）。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `request_id` | string | 否 | |
| `questions` | list | 否 | 至少一題 |
| `questions[].topic` | enum | 否 | `break_duration`、`break_location`、`other` |
| `questions[].text` | string | 否 | 追問的文字 |
| `questions[].options` | list of string | 是 | 有固定選項時提供 |

出發油量缺少時由表單的檢查擋下，不走追問。

### 4.3 PlanResult（規劃結果）

| 欄位 | 型別 | 可為空 | 填寫者 | 說明 |
| --- | --- | --- | --- | --- |
| `plan_schema_version` | string | 否 | 主程式 | `"0.1"` |
| `result_kind` | enum | 否 | 主程式 | `plan`、`infeasible`、`output_validation_error` |
| `adopted_conditions` | PlanRequest | 否 | 主程式 | 見 4.1 |
| `search` | SearchStatus | 否 | 主程式 | 見 4.4 |
| `candidates` | list | 否 | 主程式、Validator | 全部評估過的候選，含每一輪的（Q14） |
| `recommended_plan_id` | string | 是 | 主程式 | 沒有可用的候選時為 `null`（Q2） |
| `replan_rounds` | list | 否 | 主程式 | 1 到 3 筆：初次加上最多 2 次重新規劃（Q28、Q29） |
| `explanation` | Explanation | 是 | Planner 或固定模板 | 只有通過規則 5 的文字會放在這裡（Q30） |
| `rule5_log` | list | 否 | Validator | 內部紀錄，不顯示（Q30） |
| `infeasibility_report` | InfeasibilityReport | 是 | 主程式 | `result_kind = infeasible` 時必填（Q27） |
| `evidence` | list | 否 | 主程式 | 見 4.11 |
| `status_origin` | enum | 否 | 主程式 | `validator` 或 `llm_declared`（Q12；後者只用在 E2 的 A1、A2） |
| `created_at` | datetime | 否 | 主程式 | |

`result_kind` 和其他欄位的關係：

| `result_kind` | `recommended_plan_id` | `explanation` | `infeasibility_report` | 計畫狀態能否顯示 |
| --- | --- | --- | --- | --- |
| `plan` | 有 | 有 | `null` | 可以，取推薦候選的 `plan_status` |
| `infeasible` | `null` | `null` | 有 | 顯示 INFEASIBLE |
| `output_validation_error` | 有（內部保留） | `null` | `null` | **不可以**（Q30） |

### 4.4 SearchStatus

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `status` | enum | 否 | `COMPLETE` 或 `INCOMPLETE`（Q31） |
| `reason` | string | 是 | `INCOMPLETE` 時必填 |
| `candidates_total` | int | 否 | 最後一輪應評估的候選數 |
| `candidates_evaluated` | int | 否 | 最後一輪實際評估的數量 |
| `step_min` | int | 否 | 候選的間隔，目前是 15（Q11） |
| `batch_size` | int | 否 | 每批的上限，目前是 40（Q11） |

任何一輪有候選沒有評估到時，`status` 必須是 `INCOMPLETE`（Algorithm 1 第 16 行）；所以 `candidates_evaluated < candidates_total` 時一定是 `INCOMPLETE`。

### 4.5 Candidate

| 欄位 | 型別 | 可為空 | 填寫者 | 說明 |
| --- | --- | --- | --- | --- |
| `plan_id` | string | 否 | 主程式 | 對應 ETA 輸出（契約 4） |
| `round_index` | int | 否 | 主程式 | 0 是初次評估，1、2 是重新規劃 |
| `departure_time` | datetime | 否 | 主程式 | |
| `eta_typ_end` | datetime | 是 | 主程式 | 終點的典型估計，取自 ETA 輸出最後一段的 `eta_typ` |
| `eta_safe_end` | datetime | 是 | 主程式 | 終點的保守估計，取自 `eta_safe`。不是 P90 |
| `time_limit` | datetime | 否 | 主程式 | 規則 1 使用的期限 |
| `time_limit_basis` | enum | 否 | 主程式 | `civil_dusk`、`latest_arrival`、`latest_arrival_dusk_unknown` |
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
| `reason_code` | enum | 否 | 這一次判定的原因代碼，見 5.2 |
| `reason` | string | 否 | 具體原因的文字。由固定模板加上數值組成，不由 LLM 產生 |
| `evidence_ids` | list of string | 否（可為空清單） | 指向 `evidence`。沒有可用的來源時是空清單 |
| `manual_check_guidance` | string | 是 | `result = UNKNOWN` 時必填，內容是 5.3 的固定文字 |
| `overrun_s` | int | 是 | 只有規則 1 為 `FAIL` 時有值：`eta_safe_end` 超過 `time_limit` 的秒數 |

G1 Q15 列出的 `source`、`fetched_at`／`snapshot_at` 與 `simulated` 放在 Evidence，由 `evidence_ids` 取得，不在這裡重複。

### 4.7 FuelPlan 與 FuelCheckpoint

**FuelPlan**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `reserve_pct` | float | 是 | 安全保留油量，來自 Rider Profile（暫定 20） |
| `reserve_l` | float | 是 | 換算成公升 |
| `tank_capacity_l` | float | 是 | 來自 Rider Profile |
| `consumption_l_per_100km` | float | 是 | 平均油耗，來自 Rider Profile（單位見 OQ-2） |
| `profile_evidence_id` | string | 否 | 指向 Rider Profile 的來源證據 |
| `checkpoints` | list | 否 | 起點、每個計畫加油站、終點，依路線順序 |

**FuelCheckpoint**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `checkpoint_id` | string | 否 | |
| `kind` | enum | 否 | 沿用路線目錄：`start`、`fuel_station`、`waypoint`、`end` |
| `arrival_typ` | datetime | 是 | 起點為 `null` |
| `arrival_safe` | datetime | 是 | 起點為 `null` |
| `fuel_on_arrival_pct` | float | 是 | 抵達時的剩餘油量 |
| `fuel_on_arrival_l` | float | 是 | |
| `refuel_planned` | bool | 否 | 是否安排在這裡加滿 |
| `station_status` | enum | 否 | `OPEN`、`CLOSED`、`UNKNOWN`、`NOT_APPLICABLE` |
| `station_evidence_id` | string | 是 | 加油站營業時間的來源 |

`station_status` 是 `UNKNOWN` 的加油站之後，各檢查點的剩餘油量必須是 `null`：能不能補油不確定，不報告為確定的數值（DESIGN §4.2）。

### 4.8 WeatherSegment

每個路段一筆。介面把它彙總成前段、中段與最後 20% 三列顯示。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `seg_index` | int | 否 | 路線目錄的路段 |
| `arrival_typ` | datetime | 是 | 抵達這個路段的典型時間 |
| `arrival_safe` | datetime | 是 | 保守時間 |
| `pop_pct` | int | 是 | 抵達時段內最高的降雨機率 |
| `pop_class` | enum | 是 | `LOW`（0–39）、`MEDIUM`（40–69）、`HIGH_ALERT`（70–100） |
| `in_last_20pct` | bool | 否 | 路段是否落在或跨入路線最後 20% 的累計距離（Q18） |
| `evidence_id` | string | 是 | 預報的來源 |

`HIGH_ALERT` 在介面上稱為「高降雨機率提醒」。它是本專題自訂的分類，不是氣象署的警特報，也不表示降雨強度。

### 4.9 ReplanRound 與 ArrangementChange

**ReplanRound**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `round_index` | int | 否 | 0–2 |
| `changes` | list | 否 | 第 0 輪是空清單 |
| `candidates_evaluated` | int | 否 | |
| `best_status` | enum | 否 | `FEASIBLE`、`CONDITIONAL`、`INFEASIBLE`、`NO_CANDIDATES` |
| `stop_reason` | enum | 是 | 只有最後一輪有值：`found`、`max_replans`、`no_valid_change`、`not_materially_different` |

**ArrangementChange**

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
| `text` | string | 否 | 通過規則 5 的說明文字 |
| `origin` | enum | 否 | `planner` 或 `template` |
| `rule5` | RuleResult | 否 | `rule_id = 5`、`result = PASS` |
| `citations` | list | 否（可為空清單） | 知識庫的出處（FR7） |

**Citation**：`doc_id`（string）、`title`（string）、`locator`（string，可為空）。

**Rule5Attempt**（內部紀錄）

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `attempt` | int | 否 | 1–3 |
| `text_origin` | enum | 否 | `planner`、`planner_regenerated`、`template` |
| `result` | enum | 否 | `PASS` 或 `FAIL` |
| `untraceable_values` | list of string | 否 | 找不到來源的數值 |
| `checked_at` | datetime | 否 | |

沒通過的文字只留在內部紀錄，不放進 `explanation`，也不顯示。

**InfeasibilityReport**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `summary` | string | 否 | 原因摘要，由固定模板組成 |
| `fail_counts` | object | 否 | `rule_1` 到 `rule_4` 各一個 `int`，統計最後一輪的候選 |
| `representative` | object | 是 | 沒有任何候選時為 `null` |
| `representative.plan_id` | string | 否 | |
| `representative.label` | enum | 否 | `closest_to_time_limit` 或 `representative_failure` |
| `representative.basis` | enum | 否 | 見 7.5 |
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
| 3 | `R3_ETA_UNKNOWN` | UNKNOWN | `UPSTREAM_UNKNOWN` | ETA 輸出的狀態是 `unknown` |
| 4 | `R4_NO_EVENT` | PASS | — | 事件來源中沒有這條路線的封閉或管制事件 |
| 4 | `R4_ROAD_EVENT` | FAIL | — | 路線上有封閉或管制事件 |
| 4 | `R4_NO_SOURCE` | UNKNOWN | `NO_SOURCE` | 沒有可用的事件來源。不得預設為 PASS |
| 5 | `R5_TRACEABLE` | PASS | — | 文字中的每個數值都能在結構化欄位中找到 |
| 5 | `R5_UNTRACEABLE` | FAIL | — | 至少一個數值找不到來源 |

同一條規則同時符合 FAIL 與 UNKNOWN 的條件時，結果是 FAIL。

### 5.3 固定的人工確認指引（Q25）

指引是固定文字，依原因代碼查表，不由 LLM 產生。

| 規則 | `reason_code` | 指引文字 |
| --- | --- | --- |
| 1 | `R1_DUSK_UNAVAILABLE` | 查詢當日的民用暮光終時間，確認保守抵達時間在天黑之前。 |
| 2 | `R2_STATION_HOURS_UNKNOWN` | 出發前確認這個加油站當天的營業時間，或先在起點加滿。 |
| 2 | `R2_PROFILE_INCOMPLETE` | 在 Rider Profile 補上油箱容量與平均油耗後重新規劃。 |
| 3 | `R3_OUT_OF_COVERAGE`、`R3_FORECAST_UNAVAILABLE` | 出發前查看氣象署的最新預報，確認抵達時段的降雨機率。 |
| 4 | `R4_NO_SOURCE` | 出發前到公路主管機關的路況資訊，確認沿線有沒有封閉或管制。 |
| 1、2、3 | `R1_ETA_UNKNOWN`、`R2_ETA_UNKNOWN`、`R3_ETA_UNKNOWN` | 系統無法估計抵達時間，這條規則無法判定。請自行估計騎乘時間後再決定是否出發。 |

每一則指引之後，介面固定附上一句：「自行確認不會把這條規則改為 PASS。」（Q8、Q25）

### 5.4 設定值

這些都是本專題自訂的暫行設定，不是官方標準。

| 設定 | 值 | 依據 |
| --- | --- | --- |
| 高降雨機率提醒的門檻 | 降雨機率 ≥ 70% | PD-4 |
| 規則 3 的範圍 | 路線最後 20% 的累計距離 | Q18 |
| 安全保留油量 | 油箱容量的 20%，可在 Rider Profile 調整 | M0 決策 |
| 候選間隔、每批上限 | 15 分鐘、40 個 | Q11 |
| 重新規劃的上限 | 2 次 | Q28 |
| 安全餘裕係數 | 暫定 0.2，E1 Lite 之後定案 | DESIGN §6.1 |

## 6. 來源證據的型別

G1 定了三種：真實 API、資料快照、模擬。G3 裁決 N6 要求本地衍生資料與本地設定檔另有型別，不得標成 API。這份 Spec 定為五種。

| `source_type` | 顯示文字 | 時間欄位 | 標籤顏色 | 用在哪裡 |
| --- | --- | --- | --- | --- |
| `live_api` | 真實 API | `fetched_at` 必填 | 灰（G3 裁決 N5） | 一般模式下的氣象署預報與日出日沒 |
| `snapshot` | 資料快照 | `snapshot_at` 必填 | 藍 | Snapshot Mode 的預報與日出日沒；加油站快照 |
| `simulated` | 模擬 | 都可以是 `null` | 紫 | 路況事件情境檔；Prototype 的模擬檢查點 |
| `local_derived` | 本地衍生資料 | `built_at` 必填 | 灰 | 個人配速表與路線目錄（ETA 的依據） |
| `local_config` | 本地設定檔 | 都是 `null`；`version` 必填 | 灰 | Rider Profile |

規則：

- 時間欄位只填和型別對應的那一個，其他是 `null`。不得虛構取得時間（Q15）。
- `simulated = true` 的證據一律以「模擬」標示，在介面、實驗紀錄與結果中都和真實資料分開（NFR5）。
- Snapshot Mode 下不得出現 `live_api`。
- 綠色不用在來源類型上。

建議的證據代號與各規則的對應：

| `evidence_id` | 來源 | 型別 | 使用的規則 |
| --- | --- | --- | --- |
| `EV-ETA` | 個人配速表與路線目錄 | `local_derived` | 1、2、3 |
| `EV-PROFILE` | Rider Profile | `local_config` | 2 |
| `EV-DUSK` | 中央氣象署日出日沒 | `live_api` 或 `snapshot` | 1 |
| `EV-FORECAST` | 中央氣象署預報 | `live_api` 或 `snapshot` | 3 |
| `EV-STATION` | 加油站快照 | `snapshot` | 2 |
| `EV-ROAD` | 路況事件情境檔 | `simulated` | 4 |

MVP 沒有即時路況來源：真實日期的規則 4 沒有證據，`evidence_ids` 是空清單，結果是 `UNKNOWN`。

## 7. 判定與填值規則

### 7.1 誰可以寫什麼

- 計畫中的數值（時間、油量、機率、距離）一律由主程式從工具輸出複製。Planner 不填寫數值（Q3）。
- Planner 只產生：`breaks`、`refuel_stops`、`conflicts`、追問、重新規劃的提案，以及說明文字。
- `rule_results`、`plan_status` 與規則 5 的結果由 Validator 產生。Planner 不能改寫。`validator` 模組不得匯入 `planner` 或任何 LLM 客戶端（DESIGN §9.2）。

### 7.2 計畫狀態

依候選的規則 1–4：全部 `PASS` 是 `FEASIBLE`；沒有 `FAIL` 而且至少一條 `UNKNOWN` 是 `CONDITIONAL`；至少一條 `FAIL` 是 `INFEASIBLE`。

### 7.3 推薦的候選

在最後一輪的候選中，先比狀態（`FEASIBLE` 高於 `CONDITIONAL`），狀態相同取 `departure_time` 最晚的。`INFEASIBLE` 的候選不參與。結果和評估的順序無關。

### 7.4 搜尋狀態

候選從 `earliest_departure` 開始每 15 分鐘一個，到仍可能在 `latest_arrival` 前抵達的最後一個為止。每批最多 40 個，逐批評估整個範圍，不得靜默截斷。任何一輪有候選沒評估到時 `status = INCOMPLETE`，此時不得宣稱推薦的是最晚的可行出發時間。

### 7.5 代表候選（Q27 與 G3 裁決 N7）

`result_kind = infeasible` 而且最後一輪有候選時：

1. 取 `FAIL` 規則數最少的候選，稱為候選組。
2. 候選組都只違反規則 1 時，取 `overrun_s` 最小的。
3. 其他情形取 `departure_time` 最晚的。

| 情形 | `label` | `basis` |
| --- | --- | --- |
| **全部**候選都只違反規則 1 | `closest_to_time_limit`（最接近時間限制的候選） | `all_only_rule1_least_overrun` |
| 候選組都只違反規則 1，但其他候選還違反別的規則 | `representative_failure`（代表性失敗候選） | `fewest_fail_only_rule1_least_overrun` |
| 其他 | `representative_failure` | `fewest_fail_latest_departure` |

任何 `INFEASIBLE` 的候選都不是有效的建議；替代方案不自動執行，也不標示為已驗證。

### 7.6 時間餘裕

`time_limit` 是 min（民用暮光終, `latest_arrival`）。暮光終是 UNKNOWN 時用 `latest_arrival`，並把 `time_limit_basis` 設為 `latest_arrival_dusk_unknown`。`time_margin_s` 只用來顯示。

### 7.7 規則 5 的關卡（Q30）

1. Planner 的說明沒通過時重新產生一次。
2. 仍沒通過時改用固定模板。模板由推薦候選的結構化欄位組成，也要通過規則 5。
3. 模板也沒通過時 `result_kind = output_validation_error`：不顯示計畫狀態，不重新搜尋。
4. 每一次檢查都寫入 `rule5_log`。

可追溯的檢查方式：從文字中取出數值（時間、百分比、分鐘、公里、公升），和推薦候選的結構化欄位依同一套顯示格式比對。規則編號與 5.4 的設定值不算在內。顯示格式見 OQ-6。

### 7.8 重新規劃（Q19、Q28）

初次評估之後最多 2 次。提案不合法（改了不能改的欄位、加油的檢查點不是有資料的加油站），或和前一輪沒有實質差異時，提前停止並記錄 `stop_reason`。

### 7.9 E2

E2 的三組都輸出 PlanResult。A3 的 `status_origin` 是 `validator`；A1、A2 是 `llm_declared`。其他差異由 E2 的規格定義。

## 8. 介面讀取的欄位

版面以 G3 凍結的 UI 文件為準。這裡只列出各區塊的資料來源。

| 畫面區塊 | 欄位 |
| --- | --- |
| 計畫狀態標籤 | `result_kind`、推薦候選的 `plan_status` |
| 搜尋狀態標籤與提示 | `search` |
| 待確認事項 | 推薦候選中 `result = UNKNOWN` 的 `rule_results[].manual_check_guidance` |
| 四張數值卡片 | 推薦候選的 `departure_time`、`eta_typ_end`、`eta_safe_end`、`time_margin_s` |
| 說明 | `explanation.text`、`explanation.origin` |
| 採用的條件、衝突提示 | `adopted_conditions` |
| 加油安排 | 推薦候選的 `fuel_plan` |
| 天氣 | 推薦候選的 `weather` |
| 來源證據 | `evidence` |
| 頂端的 Snapshot Mode 標籤 | `adopted_conditions.data_mode`（描述畫面上的結果） |
| 結果過期 | 表單和 `adopted_conditions` 的比對 |
| 逐條規則結果 | `rule_results` |
| 最終輸出的驗證 | `explanation.rule5`，或 `result_kind` |
| 全部候選 | 最後一輪的 `candidates` |
| 重新規劃紀錄 | `replan_rounds` |
| 無可行解 | `infeasibility_report` |

## 9. 驗收與測試規格

實作時必須有的測試。目前都**尚未實作**。

| 編號 | 測試 |
| --- | --- |
| S1 | PlanResult 與 ClarificationRequest 通過 JSON Schema 驗證；缺必填欄位、型別錯誤、沒有時區的時間都被拒絕 |
| S2 | `result_kind` 和 `recommended_plan_id`、`explanation`、`infeasibility_report` 的組合符合 4.3 的表 |
| S3 | 任何一輪有候選沒評估到時 `search.status` 是 `INCOMPLETE`；`candidates_evaluated < candidates_total` 時也是 |
| S4 | `result = UNKNOWN` 的規則一定有 `reason_class` 與 `manual_check_guidance`，指引文字和 5.3 完全相同 |
| S5 | `reason_code` 和 `result`、`reason_class` 的組合符合 5.2 的表 |
| S6 | 每個 `evidence_ids` 都指向存在的 `evidence` |
| S7 | Evidence 的時間欄位和 `source_type` 一致；`simulated` 和 `source_type` 一致 |
| S8 | Snapshot Mode 的結果沒有 `live_api`；個人配速表與 Rider Profile 不會是 `live_api` |
| S9 | `station_status = UNKNOWN` 的加油站之後，剩餘油量是 `null` |
| S10 | 結果中沒有座標欄位 |
| S11 | 代表候選：全部只違反規則 1；候選組只違反規則 1 而其他候選還違反別的規則；超過期限較少的候選多違反一條規則；一般情形。`label` 與 `basis` 符合 7.5 |
| S12 | `adopted_conditions` 反映重新規劃後的安排；路線、日期與時間限制沒有被改動 |
| S13 | `rule5_log` 記錄每一次檢查；沒通過的文字不在 `explanation` 裡 |
| D1–D14 | DESIGN §8 列出的 14 項排序與候選搜尋測試 |

## 10. 這份 Spec 做的決定

G1 第 8 節註明名稱與型別由 Spec 定案。除了命名之外，以下幾項是這份 Spec 新增或改動的，請逐項審查。

| 編號 | 決定 | 理由 |
| --- | --- | --- |
| SD-1 | `source_type` 由三種增為五種，加入 `local_derived` 與 `local_config` | G3 裁決 N6 |
| SD-2 | RuleResult 的 `evidence_ids` 是清單，不是單一的 `evidence_id` | 一條規則會用到多個來源，例如規則 1 用 ETA 與暮光終 |
| SD-3 | 新增 `reason_code` | 讓「具體原因」與指引可以查表並測試。不需要時可以拿掉，只保留 `reason` |
| SD-4 | 規則 2 有兩則指引 | DESIGN §4.2 的規則 2 有兩種 UNKNOWN：缺營業時間、缺 Rider Profile 的數值 |
| SD-5 | 新增 `result_kind` 與 ClarificationRequest | 把有計畫、無可行解、輸出驗證錯誤、追問四種回應分清楚；都是 G1 已決定的行為 |
| SD-6 | `candidates` 保留每一輪的候選，以 `round_index` 區分；介面的表格與 FAIL 統計只用最後一輪 | Q14 要求保留全部評估過的候選；凍結的原型顯示的是最後一輪 |
| SD-7 | 新增 `time_limit` 與 `time_limit_basis` | 暮光終是 UNKNOWN 時，時間餘裕的基準要說清楚 |
| SD-8 | Evidence 新增 `built_at` 與 `version` | 本地衍生資料沒有取得時間，也沒有快照時間 |
| SD-9 | 規則 1 新增 `overrun_s` | 代表候選要比較「超過期限最少」 |
| SD-10 | `R*_ETA_UNKNOWN` 三個代碼與它們共用的一則指引 | ETA 輸出的狀態可以是 `unknown`（契約 4），下游規則要有對應的結果。G1 沒有討論這個情形 |
| SD-11 | 同一條規則同時符合 FAIL 與 UNKNOWN 的條件時，結果是 FAIL | 把 Q17（規則 1）的做法套用到規則 2、3、4。已確定違反的不因為其他資料缺漏而變成 UNKNOWN |
| SD-12 | 休息安排的 `origin` 沒有 `form` | G1 第 8 節寫「來自表單或自然語言」，但凍結的表單沒有休息欄位。休息來自自然語言、追問的回覆、Rider Profile 或重新規劃 |

## 11. 待審查的問題

| 編號 | 問題 | 這份 Spec 的暫定做法 |
| --- | --- | --- |
| OQ-1 | 這份 Spec 的範圍夠不夠？它只涵蓋 Plan Schema、規則輸出與來源證據。資料工具（`sources`）的輸入輸出、知識庫與 E2 Runner 要併進來，還是各自另寫 | **已裁決（2026-11-15）：各自另寫** |
| OQ-2 | Rider Profile 的平均油耗用什麼單位 | 公升／100 公里（`consumption_l_per_100km`）。若習慣用公里／公升，欄位改名 |
| OQ-3 | 加油要花多少時間，DESIGN 沒有規定 | 以一筆 `purpose = refuel` 的休息表示，長度是 Rider Profile 的設定值 |
| OQ-4 | `local_derived` 與 `local_config` 的顯示文字與標籤顏色 | 「本地衍生資料」「本地設定檔」，灰色 |
| OQ-5 | 加油站資料算 `snapshot` 還是另一種型別 | `snapshot`（G1 的實作備註稱它為加油站快照） |
| OQ-6 | 規則 5 比對數值時的顯示格式 | 時間 `HH:MM`；分鐘與百分比取整數；公升與公里取一位小數 |
| OQ-7 | 知識庫出處（Citation）的欄位 | `doc_id`、`title`、`locator`。知識庫的內容還沒有規格 |
| OQ-8 | Plan Schema 的 JSON Schema 放在哪個模組 | 留給 Tickets 決定；不修改凍結的 `contracts/` |

## 12. 之後的步驟

1. 審查者回覆第 10、11 節。
2. 修訂後凍結這份 Spec。
3. 凍結之後才建立 Tickets。Planner、Validator 與 Streamlit 的正式實作在 Tickets 之後。
