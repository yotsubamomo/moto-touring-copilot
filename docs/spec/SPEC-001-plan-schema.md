# SPEC-001 Plan Schema、規則輸出與來源證據

> 狀態：**Draft v0.2（CR-01，2026-11-15）。** 依 [CR-01](../cr/CR-01-proposal-alignment.md) 第 11–16 節修訂。仍是草稿：**專題負責人在 2026-11-15 的審查處置中沒有批准凍結**；尚未建立 Tickets；尚未實作。v0.1 是 CR-01 之前的版本，保存在 Git 基準點 `9b3af99`。
> 輸入：[DESIGN.md](../../DESIGN.md)（CR-01 修訂中：§4、§5 資料契約 v0.3（Draft，CR-01）、§6.1、§8、§9.1、§9.2）、[G1 決議](../grill/g1-grill-input.md)（Q1–Q32、第 8 節與第 11 節的 CR-01 重開紀錄）、G3 凍結的 UI 文件（[UI_DESIGN](../ui/UI_DESIGN.md)、[UI_FLOW](../ui/UI_FLOW.md)、[UI_ACCEPTANCE](../ui/UI_ACCEPTANCE.md)、[G3 Audit Report](../ui/G3_AUDIT_REPORT.md) 第 7 節）與 [UI_CR01_DELTA](../ui/UI_CR01_DELTA.md)、[CR-01](../cr/CR-01-proposal-alignment.md) 第 11–16 節與它的附錄。
> 這份 Spec 把 G1 第 8 節的「邏輯欄位清單」定成欄位名稱與型別，並固定規則的指引文字與來源證據的型別。v0.2 只修改 CR-01 影響的部分，新增的欄位都對應 CR-01 第 12 節的 Must；其他內容和 v0.1 相同。
> 2026-11-15 依兩份事後審查（[review_1_post](../cr/CR-01-appendix/review_1_post.md)、[review_2_post](../cr/CR-01-appendix/review_2_post.md)）與 [lead 的處置](../cr/CR-01-appendix/lead_dispositions.md)修正；版本仍是 v0.2 草稿。
> 2026-11-15 審查處置：專題負責人已對 P-1 至 P-11 作出裁決，另提出五項修正；這份 Spec 已同步，版本仍是 v0.2 草稿。裁決與尚未解決的 Spec Blockers 在第 11.1 節。CR-01 的技術檢查：C1 是 PASS，C2 是 FAIL，C3 是 BLOCKED／NOT RUN，C4 是 FAIL，追加的 C4b 是 PASS。標為「草案」或「提案」的內容是這份 Spec 為了回應裁決而起草的，還沒有經專題負責人確認。
> 依 P-9 的裁決：G1 沒有重開的決議（Q14、Q25、Q29、Q30）所需要的欄位與原因代碼 `reason_code` 都維持必填；`time_limit_basis` 與 `overrun_s` 延後，這一版的結果不含這兩個欄位。
> 2026-11-15 [SPEC-RESOLUTION-001](SPEC-RESOLUTION-001-sb2-sb8-sb9.md) 已由專題負責人裁決（SB-2 採模型 M2；SB-8 有條件批准，附修正 A–G；SB-9 採方案 A；E2 最多 3 題模擬預報），這份 Spec 已同步。版本仍是 Draft v0.2，**凍結尚未批准**。由裁決推導、還要請專題負責人確認的細節，標在 7.11 的狀態欄與第 10 節。
> 2026-11-15 聚焦審查（[review_1](../cr/CR-01-appendix/review_1_resolution.md)、[review_2](../cr/CR-01-appendix/review_2_resolution.md)）之後，依 [lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 1 節（F-1 至 F-27）修正。處置第 3 節的 O-1 至 O-6 當時留給專題負責人裁決，這一輪沒有採用 lead 的建議。版本仍是 Draft v0.2，**凍結尚未批准**。
> 2026-11-15 專題負責人裁決了 O-1 至 O-6（[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 5 節），這份 Spec 已同步：O-1 至 O-5 定案；O-6 的四項推導細節沒有批准，維持待確認（處置第 5.6 節）。依 O-2 的裁決由 lead 定的做法（錯誤代碼 `break_not_placeable`、兩項確定性檢查、關鍵詞清單、撤回 `unplaced_breaks`）同樣待專題負責人確認。版本仍是 Draft v0.2，**凍結尚未批准**；O-6 的細節交付並確認之前，不宣告完整的 Spec Freeze。Spec Blockers 的現況在第 11.1 節：SB-2 與 SB-9 是 CLOSED，其餘各項都還沒有關閉。都尚未實作。
> 2026-11-15 第二輪聚焦審查（[review_1](../cr/CR-01-appendix/review_1_resolution_r2.md)、[review_2](../cr/CR-01-appendix/review_2_resolution_r2.md)）之後，依 [lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 6 節（G-1 至 G-22）修正。上一段所列、lead 依 O-2 定的做法（錯誤代碼 `break_not_placeable`、兩項確定性檢查、關鍵詞清單）已撤回，不再寫在規範性的章節裡；這份 Spec 當時只保留 O-2 裁決的三點，做法的修正案在處置第 6.2 節，等專題負責人裁決（Q-1；已裁決，見下一段）。路線錯誤代碼是六個。O-6 的清單改列在處置第 6.3 節，取代第 5.6 節的表。版本仍是 Draft v0.2，**凍結尚未批准**；O-6 的細節確認之前，不宣告完整的 Spec Freeze。都尚未實作。
> 2026-11-15 專題負責人裁決了 Q-1 至 Q-5（[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 7 節），這份 Spec 已同步：Q-1 有條件批准，騎士明確要求的休息已定案（4.1）；Q-2 批准，E2 三組的任務說明共用五條規則的自然語言定義（7.9）；Q-4 批准，Profile 的版本做法不再待確認；Q-5 批准，凍結之前可以先建立第一批 Scoped Tickets（11.1）；Q-3 沒有批准，七項推導細節的完整原文在 [q3_derived_details.md](../cr/CR-01-appendix/q3_derived_details.md)，供專題負責人逐項裁決。沒有進行第三輪審查。Spec Blockers 的現況在第 11.1 節：只有 SB-2 與 SB-9 是 CLOSED。版本仍是 Draft v0.2，**凍結尚未批准**，完整的 Spec Freeze 沒有宣告；C3 維持 BLOCKED／NOT RUN。都尚未實作。
> 2026-11-15 專題負責人逐項裁決了 Q-3 的七項（[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 8 節），這份 Spec 已同步：第 1 項快照與 ID 有條件批准（第 2 節、4.14、7.11 第 1 項）；第 2 項目標路線 GPX 的折返點修改（4.1、4.13、7.11 第 2 項）；第 3 項指定的休息部分批准，休息需求多一個方向（4.1、4.2）；第 4 項 `via_offset_m` 批准，並增加順序的檢查（7.11 第 8 項）；第 5 項 `request_key` 有條件批准（7.11 第 4 項）；第 6 項 Snapshot Mode 修改，分成一般模式與嚴格模式（7.11 第 3 項）；第 7 項批准移除高度欄位（4.14）。處置第 8 節取代上面各段中和它不同的地方。標示「lead 寫定」的是裁決沒有寫、為了讓規則可以實作而補上的最小內容。測試是第 9 節的 S53–S77（Q3-T1 至 T25）。沒有重跑審查。Spec Blockers 的現況在第 11.1 節：SB-1、SB-2 與 SB-9 是 CLOSED，SB-7 與 SB-8 是 PENDING。版本仍是 Draft v0.2，**凍結尚未批准**，完整的 Spec Freeze 沒有宣告；C3 維持 BLOCKED／NOT RUN。都尚未實作。
> 2026-11-15 專題負責人裁決了 Q-3 後續的九項（A、B1–B3、C1–C5）與兩件附帶的事（[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 9 節），這份 Spec 已同步：目標路線 GPX 的 `RG-` 代號含實際採用的折返位置（第 2 節）；去回同路的自動辨識是保守的啟發式門檻，沒有以真實資料驗證過（5.4、7.11 第 2 項）；折返位置先由 CLI 指定，騎士指定的合法位置優先於自動判定（4.1、7.11 第 2 項）；`waypoint` 檢查點的編號與加油安排（4.7、7.11 第 9 項）；規劃請求多一個 `rest_policy`（4.1）；重新規劃保留騎士指定的加油停留（4.1、4.9、7.8）；行程型態與休息方向放在同一輪追問（4.1、4.2）；嚴格模式在凍結清單沒有對應項目時停止（7.11 第 3 項）。處置第 9 節取代上面各段與處置第 8 節中和它不同的地方；上一段的「SB-7 與 SB-8 是 PENDING」是當時的紀錄。測試是第 9 節的 S78–S86（Q3-T26 至 T34），另有 `routes` 整合的驗收條件 RI-1 至 RI-3。沒有重跑審查。Spec Blockers 的現況在第 11.1 節：SB-1、SB-2、SB-7、SB-8 與 SB-9 是 CLOSED；SB-3、SB-4、SB-5、SB-6、SB-10 還沒有關閉。版本仍是 Draft v0.2，**凍結尚未批准**，完整的 Spec Freeze 沒有宣告；C3 維持 BLOCKED／NOT RUN。都尚未實作。

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

- 衍生路段表、路線目錄、配速表、ETA 輸出：由資料契約定義，這份 Spec 只引用。CR-01 把契約改為 v0.3（Draft，CR-01）：契約 2（路線目錄）的欄位有變更；`route_id` 與 `checkpoint_id` 的格式放寬，會連帶影響契約 1 與契約 4 中引用這兩個 ID 的格式檢查。CR-01 本身沒有改契約 1、3、4 的欄位；停等寬放（SPEC-RESOLUTION-001 第 1.4 節，2026-11-15 裁決）在契約 1、3、4 各新增一個已核准的欄位（`short_stop_time_s`、`stop_ratio`、`stop_allow_s`）；配速表表頭的 `margin_coeff`、`margin_basis` 與 `pace_version` 的格式是由裁決推導的，已核准（2026-11-15，O-3）；`pace_version` 是契約 3 既有的主鍵，沒有新增欄位。定義在 DESIGN.md §5 與 §6.1，這份 Spec 只引用。
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
| 命名 | 小寫加底線。單位寫在字尾：`_s` 秒、`_m` 公尺、`_km` 公里、`_pct` 百分比（0–100）、`_l` 公升 |
| 時間 | `datetime` 是帶 `+08:00` 的 ISO 8601 字串（Asia/Taipei）。沒有時區位移的時間無效 |
| 缺值 | `null` 表示不知道或無法計算，不得用 0、−1 或空字串代替。遇到 `null` 要往下傳遞為 UNKNOWN，不得補值（NFR4） |
| 狀態用語 | 固定用語一律大寫：`PASS`／`FAIL`／`UNKNOWN`、`FEASIBLE`／`CONDITIONAL`／`INFEASIBLE`。其他 `enum` 用小寫。CR-01：`COMPLETE`／`INCOMPLETE` 不再使用（見 4.4） |
| ID | `route_id`、`checkpoint_id`、`plan_id` 沿用契約；`route_id` 與 `checkpoint_id` 的格式依契約 v0.3 放寬。P-3 的裁決：確切格式在 Spec 凍結前定義，不留給 Tickets；`trip_id`（`T` 加三位數字）與示範路線的 `R01`、`R02` 不變。**格式已寫定（SPEC-RESOLUTION-001 第 2.2 節），並由 Q-3 第 1 項的裁決接受（2026-11-15，有條件批准；處置第 8.1 節）。** `snapshot_id` 是 `SN-` 加 10 個小寫十六進位字元，樣式 `^SN-[0-9a-f]{10}$`：取自正規化後的快照內容的 SHA-256 前 10 碼。雜湊的範圍不含 `snapshot_id` 本身與各方向的取得時間（`legs[].fetched_at`）；這一句是 lead 寫定，已由 2026-11-15 的裁決保留（處置第 9.10 節）：取得時間每次都不同，含在內就永遠不會「內容完全相同」。重新取得後內容完全相同時代號相同，沿用既有的檔案；內容不同時是新的代號、新的檔案（4.14；7.11 第 1 項）。`route_id` 有三種：`R` 加兩位數字（示範路線 fixture）；`RS-` 加 10 個小寫十六進位字元（路線引擎的路線，十六進位的部分和它的 `snapshot_id` 相同；和快照一對一，新的快照有新的 `route_id`）；`RG-` 加 10 個小寫十六進位字元（目標路線 GPX：把檔案內容 SHA-256 的十六進位字串、一個冒號與 `trip_type` 的值依序相接；來回行程再接一個冒號與實際採用的折返位置（距起點的累計公尺，取整數；不論它是自動判定還是騎士指定的），單向行程沒有這一段；相接後取 SHA-256，用前 10 碼。相同的幾何、相同的有效折返點得到相同的 `route_id`，不同的折返點得到不同的 `route_id`；同一個檔案的單向與來回是兩條路線；沒有快照。折返位置的部分依 2026-11-15 的裁決，處置第 9.1 節）。樣式 `^(R\d{2}\|R[SG]-[0-9a-f]{10})$`。`checkpoint_id` 是 `<route_id>-CP` 加兩到三位數字，依路線順序由 01 起編，樣式 `^(R\d{2}\|R[SG]-[0-9a-f]{10})-CP\d{2,3}$`。以既有的代號寫入不同的內容時報錯，不覆寫。已保存的結果繼續記錄並顯示它當時使用的 `route_id` 與 `snapshot_id`，不會被改指到新的快照（7.11 第 1 項）。`plan_id` 在同一份結果中唯一。`evidence_id` 的格式是 `EV-` 加大寫英數字與連字號 |
| 雜湊與正規化 | 雜湊一律用 SHA-256。`request_key`（7.11 第 4 項）與 `snapshot_id` 共用同一條正規化規則：內容寫成 UTF-8 的 JSON，鍵依字典順序，沒有多餘的空白；經緯度取小數六位；以公尺計的長度與偏移取小數一位；其他浮點數取小數六位；時間用上面「時間」一列的格式。`snapshot_id` 的雜湊範圍不含 `snapshot_id` 本身與各方向的 `fetched_at`（上面「ID」一列）。這條規則由這份 Spec 定義，不留給 Tickets（P-3）。Q-3 第 1 項的裁決（2026-11-15；處置第 8.1 節）：經緯度至少保留小數六位，不得把全部浮點數統一取同一個較粗的位數；公尺值與其他浮點數的位數是 lead 寫定 |
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

BreakRequest                                  (Q-1; Planner → main program, before route resolution; not part of PlanResult)
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
| `breaks` | list | 否（可為空清單） | 主程式、Planner | 結構化的休息安排（Q4、Q20）。騎士明確要求的休息由主程式依休息需求對應後寫入，Planner 不直接寫這些筆；見下方「騎士明確要求的休息」 |
| `rest_policy` | enum | 否 | Planner | 整趟的休息策略：`default`（沒有特別指定，預設休息的規則照常適用）或 `none`（騎士明確選擇整趟不安排休息，不套用 Rider Profile 的預設休息）。由 Planner 從行程描述轉成結構化資料；不用關鍵詞猜測，也沒有為它另設追問。追問中的「不安排這段休息」只取消那一筆休息需求，不改變它。`none` 只表示不套用預設休息：騎士另外明確指定的休息照常排入，重新規劃的規則也不因它改變。結果的「採用的條件」會顯示它。套用的規則見 7.11 第 9 項。2026-11-15 的裁決（處置第 9.6 節）；欄位名稱是 lead 定的 |
| `refuel_stops` | list | 否（可為空清單） | Planner | 補給策略：在哪些檢查點加滿（Q13、Q16）。每一筆的 `origin` 區分系統安排的與騎士指定的（下方 RefuelStop） |
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
| `target_gpx_ref` | string | 是 | 表單 | 目標路線 GPX 的參照：檔案內容的 SHA-256。只讀幾何，不讀時間。沒有提供時為 `null` |
| `target_gpx_turnaround_km` | float | 是 | 騎士（先由 CLI；介面欄位是 Should） | 目標路線 GPX 的折返位置：距離起點的軌跡里程，以公里表示，換算成公尺後使用。選填，只在提供目標路線 GPX 而且行程型態是來回時使用；必須大於 0、小於軌跡總長。騎士指定的合法折返位置優先於自動判定；沒有指定時，軌跡明確去回同路才自動決定折返點（7.11 第 2 項）。沒有指定時為 `null`。換算成公尺時四捨五入到整數。先由 CLI 支援；介面上選填的折返欄位是 Should，不是第一張 Streamlit Ticket（UI-0）的 Must，不得擋住 UI Gate。允許指定軌跡上的折返位置是 Q-3 第 2 項的裁決（2026-11-15；處置第 8.2 節）；以公里輸入、先由 CLI 支援與優先順序是 2026-11-15 的裁決（處置第 9.3、9.4 節）。欄位名稱是 lead 定的 |

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
| `origin` | enum | 否 | `free_text`、`rider_profile`、`clarification`、`replan`。`free_text` 與 `clarification` 是使用者的約束；`rider_profile` 是系統依設定排入的預設休息；`replan` 是重新規劃排入的（下方規則第 6 項） |

CR-01：行程描述沒有提到休息時，主程式依 Rider Profile 的預設休息排入休息，`origin = rider_profile`；`rest_policy = none` 時不排（2026-11-15 的裁決，處置第 9.6 節）。排入的規則是確定性的，由這份 Spec 定義（7.11 第 9 項）；DESIGN.md 只寫摘要。

**騎士明確要求的休息**（SPEC-RESOLUTION-001 修正 D；2026-11-15，O-2、Q-1 與 Q-3 第 3 項的裁決）

O-2 的裁決有三點：(i) 路線上已確認的指定途經點建立為 `waypoint` 檢查點；(ii) 騎士明確要求的休息無法安排時，必須由確定性的程式回報，不能依賴語言模型自己發現；(iii) 沒有把指定的休息納入 ETA 的計畫，不得作為已滿足條件的有效計畫。第 (i) 點寫在 7.11 第 2、9 項。第 (ii)、(iii) 點的做法已由 Q-1 的裁決定案（2026-11-15，有條件批准；[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 7.1 節）。來回行程途經點的休息排在去程或回程，依 Q-3 第 3 項的裁決（2026-11-15，部分批准；處置第 8.3 節）。行程型態與休息方向在同一輪追問、兩種「不休息」的意圖，依 2026-11-15 的裁決（處置第 9.6、9.8 節）。**這一段是這些規則的定義處**；4.2、4.9、5.5、7.1、7.8、7.10 與 7.11 第 9 項只寫各自相關的部分並指向這裡。都尚未實作。

**BreakRequest（休息需求）**

Planner 在路線解析之前，把騎士要求的每一段休息轉成一筆休息需求，交給主程式。這時還沒有檢查點，所以沒有 `after_checkpoint_id`。休息需求是對應之前的中間資料，不是 PlanResult 的欄位；對應之後的結果在 `breaks`。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `place` | string | 是 | 休息的地點：詞彙表中的地標代號，或固定值 `turnaround`（折返點）。行程描述沒有寫地點時為 `null` |
| `direction` | enum | 是 | 休息排在哪一個方向：`outbound`（去程）或 `return`（回程）。行程描述寫明去程或回程時由 Planner 填入；沒有寫時為 `null`。只用在來回行程、地點是指定的途經點的休息；地點是折返點或行程是單向時不需要方向（規則第 3、5 項）。行程型態還不知道時，方向和行程型態在同一輪追問確認（規則第 3 項）。欄位名稱是 lead 定的（2026-11-15，Q-3 第 3 項的裁決，處置第 8.3 節；同一輪追問依處置第 9.8 節） |
| `duration_s` | int | 是 | 休息的長度（秒），大於 0。行程描述沒有寫長度時為 `null` |
| `source_text` | string | 否 | 行程描述中要求這段休息的原文。追問的文字與表單的固定訊息引用它（5.5） |
| `origin` | enum | 否 | `free_text`（來自行程描述）或 `clarification`（來自追問的回覆），意義和 BreakArrangement 的 `origin` 相同 |

**規則**

「依據」欄標明每一項是專題負責人對 Q-1 的裁決，還是 lead 依 Q-1 的裁決寫定的做法（不是裁決的原文）。和方向有關的部分依 Q-3 第 3 項的裁決（2026-11-15；處置第 8.3 節）。

| 編號 | 項目 | 規則 | 依據 |
| --- | --- | --- | --- |
| 1 | 休息需求 | Planner 在路線解析之前，把騎士要求的每一段休息轉成一筆 BreakRequest：地點、方向、長度（秒）、原文、來源。行程描述寫明去程或回程時，Planner 填入 `direction`。不寫 `after_checkpoint_id` | Q-1 的裁決；方向依 Q-3 第 3 項的裁決（欄位名稱是 lead 定的） |
| 2 | 可以對應的地點 | 這次路線請求中指定的途經點（`route_request.via`）；來回行程的折返點（`place` 是 `turnaround`，或就是目的地）。行程型態還不知道時，折返點不算可以對應 | Q-1 的裁決 |
| 3 | 對應不到時的回報 | 由主程式判定，不由語言模型判定；在路線解析之前依 `route_request` 檢查（7.10 第 2 步）。地點沒有寫、或不在第 2 項之內時，和其他缺少的項目一起放進既有的那一次追問（4.2，主題 `other`），每一筆休息需求一題：文字由主程式依 5.5 的固定模板產生，列出原文；選項是各個指定途經點的名稱、「折返點」（只有已知是來回行程時）與「不安排這段休息」。長度沒有寫時用既有的主題 `break_duration`。騎士選「不安排這段休息」是他自己的決定，這段休息就不再是條件；它只取消那一筆休息需求，不改變 `rest_policy`（處置第 9.6 節）。**方向：** 來回行程、地點是指定的途經點而 `direction` 是 `null` 時，去程與回程都有那個地點，主程式不自行決定方向：放進同一次追問（主題 `other`），每一筆休息需求一題，文字依 5.5 的固定模板，選項是「去程」「回程」「不安排這段休息」。地點是折返點，或行程是單向時，不需要方向。**行程型態與方向同一輪：** 行程型態和休息方向放在同一輪追問，不增加第二輪。方向的問題只用在來回行程、而且那個途經點在去程與回程各經過一次的情形。行程型態本身也在這一輪問的時候（還不知道是來回或單向），方向的那一題照樣列出，並標明「選擇來回時才需要回答」；主程式依回覆的行程型態決定用不用它：回覆來回時依方向對應，回覆單向時方向的答案不使用 | lead 依 Q-1 的裁決寫定的做法，已由 Q-3 第 3 項的裁決接受（2026-11-15；處置第 8.3 節）。方向的追問是 Q-3 第 3 項的裁決；行程型態與方向同一輪追問是 2026-11-15 的裁決（處置第 9.8 節） |
| 4 | 追問之後仍然對應不到 | 不產生計畫。和缺出發油量一樣由表單的檢查擋下：回到表單，在行程描述欄下方顯示 5.5 的固定訊息，不再追問。這不是 `route_error`，也沒有 PlanResult | lead 依 Q-1 的裁決寫定的做法，已由 Q-3 第 3 項的裁決接受（2026-11-15；處置第 8.3 節） |
| 5 | 對應與計入 ETA | 路線採用之後，主程式把每一筆休息需求對到檢查點：途經點對到它的 `waypoint` 檢查點，折返點對到 `turnaround` 檢查點。來回行程的途經點在去程與回程各有一個 `waypoint` 檢查點：依 `direction` 對到那個方向的檢查點；方向來自行程描述或追問的回覆，主程式不預設方向。單向行程不需要方向。對應後成為 `breaks` 的一筆：`after_checkpoint_id` 是那個檢查點，`purpose = rest`，`duration_s` 與 `origin` 不變；長度計入 `ETA_typ`（DESIGN §6.1 的 BREAK） | Q-1 的裁決。來回行程依方向對應是 Q-3 第 3 項的裁決（2026-11-15；處置第 8.3 節）；先前「一律排在去程」的做法作廢 |
| 6 | 預設休息與使用者約束的區分 | 以 `breaks[].origin` 區分：`free_text`、`clarification` 是使用者的約束；`rider_profile` 是系統依設定排入的預設休息；`replan` 是重新規劃排入的 | Q-1 的裁決 |
| 7 | 重新規劃 | 不得移除、搬移或縮短 `origin` 是 `free_text` 或 `clarification` 的休息。可以調整的只有 `origin` 是 `rider_profile` 或 `replan` 的休息，以及系統安排的加油停留（`refuel_stops[].origin` 是 `planner` 或 `replan`，包含第一次規劃排的）；騎士指定的加油停留（`free_text`、`clarification`）不得移除或搬移（RefuelStop；處置第 9.7 節）。帶著使用者的休息找不到可行的計畫時，回報無可行解（4.9、7.8） | Q-1 的裁決；加油停留依 2026-11-15 的裁決（處置第 9.7 節） |
| 8 | 關鍵詞 | 不做關鍵詞猜測。先前的關鍵詞檢查與 `break_not_placeable` 不採用；路線錯誤代碼維持六個（4.13） | Q-1 的裁決 |
| 9 | 不保證的部分 | 把行程描述轉成休息需求是語言模型的工作，系統不保證它的正確率。程式保證的是：已經轉成休息需求的休息，不是排入並計入 ETA，就是經過追問由騎士決定，不會被默默省略。騎士可以從結果的「採用的條件」看到排入了哪些休息 | Q-1 的裁決 |
| 10 | 沒有途經點的路線 | 目標路線 GPX 與示範路線沒有指定的途經點：來回行程只能在折返點休息；單向行程的休息需求一律走第 3 項 | Q-1 的裁決 |

- 可以排休息的檢查點是 `kind` 為 `waypoint`、`fuel_station`、`turnaround` 的檢查點，而且要符合契約 4 的位置條件：不在路線的起點與終點（7.11 第 9 項）。騎士明確要求的休息只對應到 `waypoint` 與 `turnaround` 檢查點（規則第 2、5 項）。位置條件這一句是 lead 寫的細節（處置 G-22）；Q-1 的十項規則沒有列出這一句。
- `unplaced_breaks` 與 UnplacedBreak 不採用。這個欄位、它的 `reason` 與對應的固定訊息都已刪除：對應不到的休息以追問回報，結果中不另外列出。lead 先前依 O-2 定的做法（兩項確定性檢查、休息的關鍵詞清單、排不進去時回傳錯誤代碼 `break_not_placeable`）也不採用（規則第 8 項）。
- 依 Rider Profile 排入的預設休息排不進去時就不排，不報錯（7.11 第 9 項）；它不是騎士當次指定的。
- 行程型態還不知道、休息的地點是指定的途經點而且沒有方向時，方向的那一題和行程型態的那一題在同一輪追問一併列出，標明「選擇來回時才需要回答」；不增加第二輪（規則第 3 項；2026-11-15 的裁決，處置第 9.8 節）。
- 兩種「不休息」的意圖分開，以結構化的條件區分，不用關鍵詞猜測（2026-11-15 的裁決，處置第 9.6 節）。騎士明確選擇整趟不安排休息：`rest_policy = none`，不套用 Rider Profile 的預設休息。在追問中取消某一筆或全部的個別休息需求：`rest_policy` 不變，不自動解讀成整趟禁止預設休息；取消之後沒有任何休息安排而 `rest_policy = default` 時，預設休息照常套用（7.11 第 9 項）。

**RefuelStop**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `checkpoint_id` | string | 否 | 必須是路線目錄中 `kind = fuel_station` 的檢查點（Q19） |
| `origin` | enum | 否 | `planner`（第一次規劃時系統安排的）、`replan`（重新規劃排入的）、`free_text`（騎士在行程描述中指定的）、`clarification`（來自追問的回覆）。前兩種是系統安排的，後兩種是騎士指定的（2026-11-15 的裁決，處置第 9.7 節） |

加油一律是加滿。加油停留的時間以一筆 `purpose = refuel` 的 `breaks` 表示，這樣 ETA 才會算進去（見第 11.2 節 OQ-3）。重新規劃可以調整系統安排的加油停留（`origin` 是 `planner` 或 `replan`），包含第一次規劃排的與之後各輪排的。騎士明確指定的加油地點或其他加油約束必須保留，不得取消或違反：`origin` 是 `free_text` 或 `clarification` 的加油停留不得移除或搬移（4.9、7.8）。

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
| `questions[].topic` | enum | 否 | CR-01：`start_point`（缺起點）、`entry_side`（不知道從公路的哪一端進）、`trip_type`（沒說來回或單向）、`break_duration`（休息多久）、`other`。v0.1 的 `break_location` 併入 `other`。騎士明確要求的休息對應不到地點時用 `other`，長度沒有寫時用 `break_duration`；來回行程途經點的休息沒有方向時也用 `other`；行程型態也未知時，它和 `trip_type` 的那一題在同一次追問（4.1 規則第 3 項） |
| `questions[].text` | string | 否 | 追問的文字。休息對應不到地點的那一題，文字由主程式依 5.5 的固定模板產生，列出原文，不由 LLM 產生。休息方向的那一題同樣由主程式依 5.5 的固定模板產生；行程型態也在這一輪問的時候，文字標明「選擇來回時才需要回答」 |
| `questions[].options` | list of string | 是 | 有固定選項時提供。CR-01：`start_point` 與 `entry_side` 的選項只來自詞彙表與 Rider Profile。休息對應不到地點的那一題，選項固定：這次路線請求中各個指定途經點的名稱、「折返點」（只有已知是來回行程時）、「不安排這段休息」。休息方向的那一題，選項固定：「去程」「回程」「不安排這段休息」。不論行程型態的回覆是什麼，選「不安排這段休息」都會取消那一筆休息需求；回覆是單向時，只有「去程」「回程」的答案不使用 |

出發油量缺少時由表單的檢查擋下，不走追問。CR-01：行程描述與目標路線 GPX 都沒有提供時，也由表單的檢查擋下。

騎士明確要求的休息（2026-11-15，Q-1 的裁決；規則的定義處是 4.1）：休息需求的地點沒有寫、或不在可以對應的地點之內時，由主程式判定，和其他缺少的項目一起放進這一次追問，每一筆休息需求一題。騎士選「不安排這段休息」時，這段休息不再是條件。追問回覆之後仍然對應不到時，不產生計畫，由表單的檢查擋下：回到表單，在行程描述欄下方顯示 5.5 的固定訊息，不再追問。來回行程、休息的地點是指定的途經點而沒有寫方向時，同樣放進這一次追問，選項是「去程」「回程」「不安排這段休息」（2026-11-15，Q-3 第 3 項的裁決；4.1 規則第 3 項）。行程型態和休息方向在同一輪追問確認，不增加第二輪：方向的問題只用在來回行程、而且那個途經點在去程與回程各經過一次的情形；行程型態本身也在這一輪問的時候，方向的那一題標明「選擇來回時才需要回答」，主程式依回覆的行程型態決定用不用它（2026-11-15 的裁決；處置第 9.8 節）。「不安排這段休息」只取消那一筆休息需求，不改變 `rest_policy`（處置第 9.6 節）。

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
| `checkpoints` | list | 否 | 起點、每個計畫加油站、終點，依路線順序。CR-01：檢查點由加油站快照沿路線產生。來回行程的去程與回程各自產生檢查點：回程也經過同一個加油站時，它在回程另有一個檢查點，`checkpoint_id` 不同。回程是另外算的路線，不保證經過去程的每一個加油站。折返點的 `kind` 是 `turnaround`，會列在清單中。`waypoint` 不當作 `fuel_station`，也不列入這份清單（2026-11-15 的裁決，處置第 9.5 節） |

**FuelCheckpoint**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `checkpoint_id` | string | 否 | |
| `kind` | enum | 否 | 沿用路線目錄：`start`、`fuel_station`、`waypoint`、`end`；契約 2 v0.3 新增 `turnaround`（來回行程的折返點；草稿，待 Ticket 實作）。`waypoint` 是指定的途經點建立的檢查點（7.11 第 9 項；2026-11-15，O-2 的裁決） |
| `arrival_typ` | datetime | 是 | 起點為 `null` |
| `arrival_safe` | datetime | 是 | 起點為 `null` |
| `fuel_on_arrival_pct` | float | 是 | 抵達時的剩餘油量 |
| `fuel_on_arrival_l` | float | 是 | |
| `refuel_planned` | bool | 否 | 是否安排在這裡加滿 |
| `station_status` | enum | 否 | `OPEN`、`CLOSED`、`UNKNOWN`、`NOT_APPLICABLE` |
| `station_evidence_id` | string | 是 | 加油站營業時間的來源 |

`station_status` 是 `UNKNOWN` 的加油站之後，各檢查點的剩餘油量必須是 `null`：能不能補油不確定，不報告為確定的數值（DESIGN §4.2）。

### 4.8 WeatherSegment

每個路段一筆。介面把它彙總成前段、中段與最後 20% 三列顯示。CR-01：這是單向行程的做法。來回行程分成去程與回程顯示，回程標示為規則 3 的範圍（SPEC-RESOLUTION-001 方案 A，2026-11-15 裁決）；各分成幾列在 Streamlit 實作時決定（UI_CR01_DELTA 第 10 節）。

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
| `in_rule3_range` | bool | 否 | 路段是否在規則 3 的範圍內。單向行程：落在或跨入路線最後 20% 的累計距離（Q18）。來回行程：折返點之後的每一個路段，也就是整段回程（SPEC-RESOLUTION-001 方案 A）。目標路線 GPX 的來回路線以 7.11 第 2 項的折返點分去程與回程；路線在折返點切開，折返點是路段邊界。範圍以外的路段只顯示，不影響規則 3 的結果；去程的高降雨機率提醒照常顯示（5.5） |
| `evidence_id` | string | 是 | 預報的來源 |

`HIGH_ALERT` 在介面上稱為「高降雨機率提醒」。它是本專題自訂的分類，不是氣象署的警特報，不表示降雨強度，也不代表官方認定的危險道路。

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

使用者的休息（2026-11-15，Q-1 的裁決；4.1 規則第 6、7 項）：重新規劃不得移除、搬移或縮短 `origin` 是 `free_text` 或 `clarification` 的休息。可以調整的只有 `origin` 是 `rider_profile` 或 `replan` 的休息，以及系統安排的加油停留（`refuel_stops[].origin` 是 `planner` 或 `replan`，包含第一次規劃排的）；騎士指定的加油停留（`free_text`、`clarification`）不得移除或搬移（RefuelStop；處置第 9.7 節）。`remove_break` 與 `change_break_duration` 因此不得指向使用者的休息：每一輪之後，這些休息都還在，檢查點與長度不變。帶著使用者的休息找不到可行的計畫時，回報無可行解（`result_kind = infeasible`）。騎士指定的加油停留同理（2026-11-15 的裁決；處置第 9.7 節）：`remove_refuel` 不得指向 `origin` 是 `free_text` 或 `clarification` 的加油停留；每一輪之後，這些加油停留都還在，檢查點不變。系統安排的加油停留可以被移除或更換。

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
| `freeway_check` | enum | 是 | 國道檢查的結果：`pass` 或 `fail`。一個方向要所有訊號一致、都沒有國道才是 `pass`（7.11 第 5 項）；每個方向都通過，這裡才是 `pass`。逐方向的結果在路線快照。結果中不得出現 `fail`：沒通過的路線不會成為結果 |
| `leg_length_diff_pct` | float | 是 | 去程與回程的里程差，以百分比表示：兩者相減的絕對值，除以兩者的平均，再乘以 100（7.11 第 11 項） |
| `leg_length_diff_flag` | bool | 是 | `leg_length_diff_pct` 大於 2 時為 `true`：回程走的道路和去程有明顯的不同，介面在路線摘要標示（5.5） |
| `turnaround_checkpoint_id` | string | 是 | 來回行程的折返點，指向 `kind = turnaround` 的檢查點；單向行程為 `null` |
| `ridden_share_pct` | float | 是 | 這條路線中，幾何和配速行程的軌跡接近的比例（0–100，取整數），不分方向：取樣點 50 m 內有配速行程的軌跡點算接近，連續接近的取樣點少於 3 個的片段不算。只比對配速行程。它不保證實際走過同一條道路，也不代表騎士騎過的所有道路（審查處置的修正 1；SPEC-RESOLUTION-001 修正 G）；介面稱為「配速資料中的路線涵蓋比例」。無法比對時為 `null`。算法見 7.11 第 10 項 |
| `route_evidence_id` | string | 否 | 指向路線的來源證據（第 6 節） |

路線引擎自己回報的國道旗標 `has_highway` 逐方向記錄在路線快照（4.14），不放在路線摘要。它是國道檢查的訊號之一：是 `true` 時這條路線不採用（SPEC-RESOLUTION-001 修正 B）。這份 Spec 的初稿曾經用 `has_highway` 表示產品自己的檢查結果；為了不和引擎的欄位同名不同義，改為 `freeway_check`。

**`route_source` 的跨欄位規則**

| `route_source` | `snapshot_id` | `freeway_check` | `engine_time_s` | `leg_length_diff_pct`、`leg_length_diff_flag` | `route_request.target_gpx_ref` | 路線目錄的 `source_trip_id`（契約 2） |
| --- | --- | --- | --- | --- | --- | --- |
| `trip` | `null` | `null`（沒有檢查） | `null` | `null` | `null` | 必填 |
| `routing` | 必填 | 必須是 `pass` | 必填 | 來回行程必填；單向行程為 `null` | `null` | `null` |
| `target_gpx` | `null` | `null`（沒有檢查） | `null` | `null` | 必填（檔案內容的 SHA-256） | `null` |

目標路線 GPX 的路線沒有路線快照。它在結果中可追溯的代號是 `target_gpx_ref`（檔案內容的 SHA-256）。

規則：

- **採用條件。** 路線引擎回傳的路線，每個方向都通過國道檢查（`freeway_check = pass`）才採用。這一條沒有例外，和用哪一種路線參數無關。任一方向有任何一項訊號顯示有國道時回傳 `route_error`（`highway_in_route`），優先於其他原因；沒有國道的訊號但無法驗證時回傳 `routing_unavailable`（7.11 第 5 項）。
- **國道檢查的用語。** 這項檢查和路線用的是同一個引擎與同一份開放圖資。它不是道路主管機關資料的獨立驗證，文件、介面與報告都不得這樣宣稱（SPEC-RESOLUTION-001 修正 F）。
- **偏移。** 起點、終點與送給引擎的每一個中間位置（指定的途經點與公路的進入端），偏移都不超過 200 m，而且中間位置在折線上依請求的順序出現，才採用（7.11 第 8 項）。
- **回應的警告。** 路線參數已裁決為 `use_highways: 0`（P-1）：請求不送出硬性排除，回應出現任何警告就不採用。規則寫在 7.11 第 7 項。
- `road_names` 是給騎士檢視路權用的。結果不含座標與折線。
- `ridden_share_pct` 只用來告知，不改變任何規則結果，也不分級。它只表示幾何接近的比例。

### 4.13 RouteError（路線錯誤，CR-01）

路線無法取得或不能採用時回傳，`result_kind = route_error`。這時不評估候選，也不由語言模型產生或補上路線（CR-01 D2）。騎士明確要求的休息對應不到地點時不走路線錯誤：以追問回報，追問之後仍然對應不到時由表單的檢查擋下（4.1、4.2）。

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `code` | enum | 否 | 見下表 |
| `message` | string | 否 | 5.5 的固定文字，不由 LLM 產生 |
| `actions` | list of string | 否 | 騎士可以怎麼做；5.5 的固定文字 |
| `unresolved` | list of string | 否（可為空清單） | `code = not_in_gazetteer` 時，列出行程描述中對不到詞彙表的名稱 |

| `code` | 情形 |
| --- | --- |
| `not_in_gazetteer` | 行程描述中的公路或地標不在詞彙表內，追問也補不齊 |
| `routing_unavailable` | 路線引擎沒有回應、回傳錯誤，或找不到可用的路線。也包含三種不採用的情形：回應出現任何警告（P-1；7.11 第 7 項）；起點、終點或任何一個中間位置（途經點、公路的進入端）的偏移超過 200 m，或中間位置在折線上的順序和請求不同（7.11 第 8 項）；國道檢查無法驗證（道路屬性查詢失敗、長度不符，或引擎沒有回報 `has_highway`；7.11 第 5 項）。這三種情形同時有任何國道的訊號時，回傳的是 `highway_in_route`。一般模式下不改用已失效的路線快照（7.11 第 3 項） |
| `highway_in_route` | 任一方向的國道檢查有任何一項訊號顯示有國道（`freeway_check = fail`；7.11 第 5 項）。優先於 `routing_unavailable` 的各種原因 |
| `snapshot_missing` | 一般的 Snapshot Mode 下，這個路線請求沒有可用的已保存快照：沒有 `request_key` 相同的快照，或只有 `freeway_check_method` 和現行檢查方法不同的快照（7.11 第 3 項）。Snapshot Mode 不呼叫路線引擎。嚴格模式（執行時指定了凍結清單）下，凍結清單沒有對應的項目、清單指定的檔案不存在、雜湊不符或檢查方法不同時是停止執行，不回退到其他快照（7.11 第 3 項） |
| `target_gpx_invalid` | 目標路線 GPX 讀不到軌跡點或只有一點、總長度不到 1 km，或相鄰兩點相距超過 1 km（幾何太疏，無法當成路線的幾何） |
| `target_gpx_not_round_trip` | 騎士指定來回，但目標路線 GPX 不能當成來回的路線。兩種情形：(1) GPX 的終點沒有回到起點（相距超過 200 m），即使指定了折返位置也一樣；(2) 終點回到起點，但無法確認折返點：軌跡不是明確的去回同路，而騎士沒有指定折返位置，或指定的里程不合法。系統不推定、不反轉，也不補造回程（7.11 第 2 項；SPEC-RESOLUTION-001 修正 E；Q-3 第 2 項的裁決，處置第 8.2 節） |

路線錯誤代碼共六個。lead 先前依 O-2 定的 `break_not_placeable` 不採用（2026-11-15，Q-1 的裁決；4.1 規則第 8 項）。Q-3 第 2、3 項的裁決（2026-11-15）也沒有新增代碼。

`result_kind = route_error` 時，結果只有：`plan_schema_version`、`result_kind`、`adopted_conditions`（其中 `route_id` 為 `null`）、`route_error`、`evidence`（可為空清單）、`status_origin` 與 `created_at`。`route`、`evaluation`、`recommended_plan_id`、`explanation` 與 `infeasibility_report` 是 `null`；`candidates`、`replan_rounds` 與 `rule5_log` 是空清單。

### 4.14 RouteSnapshot（路線快照，CR-01）

路線快照是 `routing` 模組產生的檔案，不是 PlanResult 的一部分。**一條路線對應一個路線快照**，以 `snapshot_id` 識別。來回行程的去程與回程在同一個快照裡，各是 `legs[]` 的一筆。欄位由這份 Spec 定義；實體檔案格式由 Tickets 決定。尚未實作。

**快照不可變（SPEC-RESOLUTION-001 修正 A，2026-11-15 裁決；Q-3 第 1 項的裁決，處置第 8.1 節）。** 快照檔寫入一次之後不再修改，程式也不刪除。快照由正規化後的內容產生代號：重新取得後內容完全相同時代號相同，沿用既有的檔案，不寫入、不修改；內容不同時是新的代號、新的檔案，舊檔不動。以既有的代號寫入不同的內容時報錯，不覆寫。E2 與 Demo 凍結的快照因此不會被覆寫。不另建索引檔或版本號。雜湊的範圍不含 `snapshot_id` 本身與各方向的 `fetched_at`（lead 寫定；已由 2026-11-15 的裁決保留，處置第 9.10 節）。沿用既有的檔案時，它的取得時間不更新，也不得偽造或覆寫（7.11 第 3 項）。新的快照有新的 `route_id`；已保存的結果繼續指向它當時使用的快照（7.11 第 1 項）。

快照含折線，所以不放進規劃結果，也不送給語言模型（第 2 節）。從住家或出發錨點出發的快照不進版控（DESIGN.md 的隱私規則）。

**RouteSnapshot**

| 欄位 | 型別 | 可為空 | 說明 |
| --- | --- | --- | --- |
| `snapshot_id` | string | 否 | 快照的代號：`SN-` 加正規化後的快照內容的 SHA-256 前 10 碼（第 2 節；7.11 第 1 項）。雜湊的範圍不含這個欄位本身與各方向的 `fetched_at`（lead 寫定）。依 Q-3 第 1 項的裁決（2026-11-15，有條件批准） |
| `request_key` | string | 否 | 路線請求的比對鍵（7.11 第 4 項）。一般模式的重用與 Snapshot Mode 都以它找已保存的快照 |
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
| `has_highway` | bool | 否 | 路線引擎回報的國道旗標，是國道檢查的訊號之一（7.11 第 5 項）。是 `true` 時這條路線不採用（fail closed）；引擎沒有回報時算無法驗證，也不採用。所以存成快照的方向一定是 `false` |
| `freeway_check` | enum | 否 | 國道檢查的結果：`pass` 或 `fail`。判定條件見 7.11 第 5 項。存成快照的路線，每個方向都是 `pass`；無法驗證時不產生這個值，也不存快照 |
| `freeway_check_method` | string | 否 | 這次檢查用的方法、資料來源與門檻（7.11 第 5 項）。檢查的方法或門檻改過時，這個字串跟著改；一般模式重用快照與 Snapshot Mode 讀快照時，都和現行的檢查方法比對，不同就不使用（7.11 第 3 項） |
| `endpoint_offset_m` | object | 否 | `start` 與 `end` 兩個 `float`：要求的地標到折線起點、終點的距離。存成快照的方向，兩個值都不超過 200 m（7.11 第 8 項） |
| `via_offset_m` | list of float | 否（可為空清單） | 送給引擎的每一個中間位置到折線最近點的距離，依這個方向送出的順序。中間位置包含指定的途經點與公路的進入端（`entry_ref_id`）。沒有中間位置時是空清單。存成快照的方向，每個值都不超過 200 m（7.11 第 8 項；SPEC-RESOLUTION-001 修正 C）。各個中間位置在折線上最近點的沿線里程，要依請求的順序遞增（7.11 第 8 項）。這個欄位、以及把公路的進入端納入檢查，已由 Q-3 第 4 項的裁決批准（2026-11-15；處置第 8.4 節） |
| `fetched_at` | datetime | 否 | 取得這個方向回應的時間。不在 `snapshot_id` 的雜湊範圍內（第 2 節） |

快照不記錄高度：規則 3 在來回行程上的範圍（方案 A）不需要高度，MVP 也不向路線引擎要求高度資料，RouteLeg 沒有高度欄位。移除高度欄位已由 Q-3 第 7 項的裁決批准（2026-11-15；處置第 8.7 節）。

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
| 3 | `R3_NO_ALERT_IN_RANGE` | PASS | — | 規則 3 的範圍內（`in_rule3_range = true`）每個路段都有降雨機率，而且沒有 `HIGH_ALERT` 的路段 |
| 3 | `R3_ALERT_IN_RANGE` | FAIL | — | 規則 3 的範圍內有 `HIGH_ALERT` 的路段。範圍內另有路段缺預報時仍是 FAIL |
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

規則 3 的範圍內同時有不同原因的缺預報時，`reason_code` 取下列固定順序中最前面的一個：`R3_ETA_UNKNOWN`、`R3_FORECAST_UNAVAILABLE`、`R3_OUT_OF_COVERAGE`、`R3_AREA_UNMAPPED`；`reason_class` 隨代碼決定。

CR-01 的補充：

- 規則 1 的 `latest_arrival` 語意不變；來回行程指回到出發點的時間。
- 規則 3 的範圍已定（SPEC-RESOLUTION-001 方案 A，2026-11-15 裁決）：單向行程是路線最後 20% 的累計距離；來回行程是折返點之後的整段回程。`R3_NO_ALERT_IN_RANGE` 與 `R3_ALERT_IN_RANGE` 單向與來回共用，判定只看 `in_rule3_range = true` 的路段。範圍以外的路段只顯示：去程有高降雨機率提醒或缺預報，都不影響規則 3 的結果。
- 規則 3 的 PASS 不代表去程不會下雨。去程的高降雨機率提醒照常顯示，介面另有一句固定說明（5.5）。
- 這兩個代碼由原本只表示最後 20% 的名稱改名。代碼還沒有凍結，現在改名不違反 P-9。
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

這些都是本專題自訂的設定，不是官方標準。其中快照的 30 天與預設休息的 90／15 分鐘是裁決接受的數值；目標路線 GPX 的 1 km、道路屬性長度的 2% 與詞彙表的 100 m 是隨 SB-8 的有條件批准一起通過的提案值，不是裁決逐項接受的數值；目標路線 GPX 去回同路的 50 m／100 m／90% 是有條件批准的保守啟發式門檻，沒有以真實資料驗證過。這些數值都沒有資料依據（SPEC-RESOLUTION-001 第 7 節）。

| 設定 | 值 | 依據 |
| --- | --- | --- |
| 高降雨機率提醒的門檻 | 降雨機率 ≥ 70% | PD-4 |
| 規則 3 的範圍 | 單向行程：路線最後 20% 的累計距離，跨入的路段也算。來回行程：折返點之後的全部回程。範圍以外的路段只顯示，不影響結果 | Q18；CR-01 D3；SPEC-RESOLUTION-001 第 3 節（方案 A，2026-11-15 裁決） |
| 安全保留油量 | 油箱容量的 20%，可在 Rider Profile 調整 | M0 決策 |
| 候選間隔 | 15 分鐘。CR-01：每批 40 個的上限取消 | Q11；CR-01 第 11 節 |
| 重新規劃的上限 | 2 次 | Q28 |
| 安全餘裕係數 | 由固定規則決定，不再是暫定值：每次建立配速表時，以同一批配速行程的留一趟結果算出 `margin_coeff`，寫在配速表的表頭；規則見 DESIGN §6.1。留一趟中計入的折數少於 8 時用預設的 0.20，介面要說明這是預設值（5.5）。它是描述性的設定值，不是 P90，沒有覆蓋率的保證。研究用的配速表在讀取保留行程之前凍結（P-2、P-5） | DESIGN §6.1；SPEC-RESOLUTION-001 第 1.2 節（2026-11-15 裁決）。表頭的 `margin_coeff`（0.05 的倍數，不小於 0.05）、`margin_basis`（`loo_rule` 或 `default`）與 `pace_version` 的格式是由裁決推導的（第 8 節第 1 點），已核准（2026-11-15，O-3）；`pace_version` 是契約 3 既有的主鍵，沒有新增欄位。契約 4 的表頭保留實際採用的 `margin_coeff`，必須等於所用配速表表頭的值 |
| 去回里程差的標示門檻 | 2%（`leg_length_diff_pct` 大於 2） | CR-01 審查後的處置 L-3；和檢查 C4 記錄去回里程差時用的門檻相同 |
| 停等寬放 | 停等事件依長度分三種，門檻是 3 秒與 180 秒：不到 3 秒是疑似 GPS 假停留，算進移動時間；3 秒以上、不到 180 秒是短停留，是寬放的依據；180 秒以上是長停留，不進配速表與寬放。每個路段類別一個 `stop_ratio`（短停留 ÷ 移動時間），存在配速表；路段的寬放是 `stop_ratio` 乘以它的典型移動時間，計入典型估計。算式與不重複計算的規則見 DESIGN §6.1，這裡不重複。Plan Schema 沒有新增欄位；介面不顯示寬放的秒數，只在抵達時間旁顯示 5.5 的固定句子 | CR-01 審查處置 P-2；SPEC-RESOLUTION-001 第 1 節（模型 M2，2026-11-15 裁決） |
| 路線快照的重用期限 | 30 天。一般模式下，請求相同、檢查方法相同、取得時間在 30 天內的快照直接重用；Snapshot Mode 不看這個期限。沿用既有檔案的快照，取得時間不更新：同一條路超過 30 天之後，一般模式每次規劃都會重新向路線引擎取得（7.11 第 3 項）。這是 MVP 的已知限制；不偽造或覆寫取得時間，也不為此新增複雜的快取架構 | SPEC-RESOLUTION-001 第 2.1 節（2026-11-15 裁決）；Q-3 第 1 項的裁決（處置第 8.1 節）；已知限制依 2026-11-15 的裁決（處置第 9.10 節） |
| 起點、終點與途經點的偏移門檻 | 200 m。起點、終點與送給引擎的每一個中間位置（途經點、公路的進入端）任何一個超過就不採用這條路線；中間位置在折線上的順序和請求不同時也不採用（7.11 第 8 項） | SPEC-RESOLUTION-001 第 2.5 節（2026-11-15 裁決；修正 C）。把公路的進入端也納入、偏移記在 `via_offset_m`，已由 Q-3 第 4 項的裁決批准（2026-11-15；處置第 8.4 節）；順序的判定方式是 lead 依裁決的測試要求寫定 |
| 預設休息 | 連續騎乘 90 分鐘休息一次，每次 15 分鐘。兩個值是 Rider Profile 的設定（`default_break_interval_min`、`default_break_duration_min`），可以修改（7.11 第 9 項） | SPEC-RESOLUTION-001 第 2.6 節（2026-11-15 裁決） |
| 涵蓋比例的接近判定 | 取樣點 50 m 內有配速行程的軌跡點算接近；連續接近的取樣點少於 3 個的片段不算（取樣間隔 100 m；7.11 第 10 項） | SPEC-RESOLUTION-001 第 2.7 節（2026-11-15 裁決） |
| 目標路線 GPX 的門檻 | 總長度至少 1 km；相鄰兩點相距不超過 1 km；騎士指定來回時，終點要回到起點（相距 200 m 以內）（4.13；7.11 第 2 項） | SPEC-RESOLUTION-001 第 2.8 節（2026-11-15 裁決）。1 km 是隨 SB-8 的有條件批准通過的提案值 |
| 目標路線 GPX 去回同路的自動辨識（保守的啟發式門檻） | 以離起點直線距離最遠的軌跡點把軌跡分成前後兩段；後段每 100 m 取一點，取樣點 50 m 內有前段的軌跡點算接近。接近的取樣點達 **90%** 以上算明確去回同路，折返點自動取那個最遠點（7.11 第 2 項）。50 m 與 100 m 沿用涵蓋比例的接近判定。50 m／100 m／90% 是 MVP 自動辨識的保守啟發式門檻，**沒有以真實資料驗證過**，文件與報告都不得宣稱它經過驗證。辨識不明確時交給騎士指定，不默默猜測；騎士指定的合法折返位置優先於自動辨識 | Q-3 第 2 項的裁決（2026-11-15；處置第 8.2 節）；2026-11-15 的裁決（有條件批准；處置第 9.2、9.4 節）。只以合成資料測試（第 9 節 S79） |
| `request_key` 的地標指紋 | 地標座標定義的 SHA-256 前 16 碼；座標先正規化為小數六位（7.11 第 4 項） | Q-3 第 5 項的裁決（2026-11-15，有條件批准；處置第 8.5 節） |
| 雜湊正規化的精度 | 經緯度取小數六位；以公尺計的長度與偏移取小數一位；其他浮點數取小數六位（第 2 節） | Q-3 第 1 項的裁決（2026-11-15；處置第 8.1 節）：經緯度至少小數六位。公尺值與其他浮點數的位數是 lead 寫定 |
| 道路寫法的固定樣式（規則 5，7.7） | 「國道 N 號」「台 N 線」「縣道 N」「鄉道」。草稿：清單由 Tickets 補齊 | CR-01；7.7 |

### 5.5 CR-01 的固定文字

以下文字由主程式依條件選用，不由 LLM 產生。UI-0 決策對照表的 22 項已在 2026-11-15 由專題負責人確認（[ui0_decision_table.md](../cr/CR-01-appendix/ui0_decision_table.md)）：其中去回里程差、`routing_unavailable` 與休息策略的文字依裁決修正，其餘照原文。不在對照表內、仍標為「提案」的文字還沒有確認。這不代表 SB-6、SB-10 或這份 Spec 已經關閉。`{…}` 是由結構化欄位填入的值。標明「依裁決修正」或「依裁決新增」的句子是為了符合 SPEC-RESOLUTION-001（2026-11-15 裁決）而寫的；其中抵達時間的說明與 `target_gpx_not_round_trip` 第一則的文字取自那份文件（第 1.4、2.8 節）。

**路權提醒、配速資料的涵蓋比例與其他固定說明**

| 用途 | 條件 | 文字 |
| --- | --- | --- |
| 路權提醒（依裁決修正：修正 F） | `route_source = routing` | 這條路線由路線引擎依開放圖資產生。系統用同一份開放圖資再檢查一次，沒有發現國道路段；這不是道路主管機關的驗證。其他道路的機車通行限制（例如部分快速公路與高架道路）系統無法保證，請出發前自行確認路權。 |
| 路權提醒 | `route_source` 是 `target_gpx` 或 `trip` | 這條路線取自你提供的 GPX 或騎過的行程。系統沒有檢查國道與機車通行限制，請出發前自行確認路權。 |
| 去回里程差（2026-11-15 依裁決修正，U-14） | `leg_length_diff_flag = true` | 去程與回程分別計算，里程相差約 {`leg_length_diff_pct`}%。實際經過的道路可能不同，請核對道路名稱。 |
| 涵蓋比例（依裁決修正：修正 G） | `ridden_share_pct` 大於 0 | 配速資料中的路線涵蓋比例：這條路線約有 {`ridden_share_pct`}% 的里程，幾何和你的配速資料接近（不分方向）。這個比例只比對用來建立個人配速表的行程；它不保證你實際走過同一條道路，也不代表你騎過的所有道路。抵達時間依你的個人配速表估計；配速資料沒有涵蓋的路段，估計的可信度較低。 |
| 涵蓋比例（依裁決修正：修正 G） | `ridden_share_pct` 等於 0 | 配速資料中的路線涵蓋比例：0%。配速資料中沒有幾何和這條路線接近的行程；這不表示你沒有騎過這條路，這個比例也不代表你騎過的所有道路。抵達時間依你在同類彎道上的個人配速估計，可信度較低。 |
| 涵蓋比例 | `ridden_share_pct` 是 `null` | 系統無法算出配速資料中的路線涵蓋比例。 |
| 抵達時間的說明（依裁決修正） | 顯示典型抵達或保守抵達時間時 | 抵達時間已包含路上短暫停等（紅燈、車流）的估計，以及排入的休息與加油；不包含沒有安排的長時間停留。 |
| 預設的餘裕係數（依裁決新增） | 規劃所用的配速表，表頭的 `margin_basis` 是 `default`：留一趟中計入的折數少於 8，`margin_coeff` 是預設的 0.20（`margin_basis` 已核准，2026-11-15，O-3） | 保守估計用的是預設的餘裕係數 0.20：可以用來估計餘裕的行程不到 8 趟，這個值不是由你的騎乘資料得出的。 |
| 去程的高降雨機率提醒（依裁決新增） | 來回行程，而且去程（規則 3 的範圍以外）有 `HIGH_ALERT` 的路段 | 去程有路段是高降雨機率提醒。規則 3 在來回行程只檢查回程，所以規則 3 的 PASS 不代表去程不會下雨。 |
| 評估失敗 | `result_kind = evaluation_failed` | 候選的評估沒有完成，這次不提供建議的出發時間。請再按一次「規劃」；仍然失敗時，改用 Snapshot Mode 或稍後再試。 |
| 休息策略的顯示（2026-11-15 裁決，U-22） | 「採用的條件」中的 `rest_policy`：`default` | 未特別限制，依 Profile 安排預設休息。 |
| 休息策略的顯示（2026-11-15 裁決，U-22） | 「採用的條件」中的 `rest_policy`：`none` | 不套用預設休息；另外指定的休息仍會安排。 |
| 行程描述的輸入保護（7.12；草案） | 行程描述出現門牌或座標的寫法 | 行程描述中有看起來像門牌地址或座標的內容，系統沒有送出這段文字。請改用公路或地標的名稱描述；起點在住家附近時，請用出發錨點。 |
| 預報時段的說明（7.13；草案） | 天氣表有降雨機率時 | 降雨機率是所列預報時段的數值，不是抵達那一刻的預報；各列採用的預報時段與時段長度見表中的欄位。 |

**路線錯誤**

| `code` | `message` | `actions` |
| --- | --- | --- |
| `not_in_gazetteer` | 行程描述中的「{`unresolved`}」不在目前支援的公路與地標清單內，系統沒有產生路線。 | 改用清單內的公路或地標重新描述；或提供目標路線 GPX。 |
| `routing_unavailable`（2026-11-15 依裁決修正，U-16；一則訊息涵蓋各種原因） | 系統無法產生可採用的路線。 | 請檢查起訖點與途經點，或改用已有的路線快照／目標 GPX。如果是路線服務暫時無法使用，請稍後再試。 |
| `highway_in_route` | 路線服務回傳的路線沒有通過國道檢查，系統不採用這條路線。 | 增加途經點讓路線避開國道；或提供目標路線 GPX。 |
| `snapshot_missing` | Snapshot Mode 只使用已保存的路線快照，這個行程沒有對應的快照。 | 關閉 Snapshot Mode 後重新規劃；或改成有快照的行程。 |
| `target_gpx_invalid` | 目標路線 GPX 無法當成路線使用：讀不到軌跡點、路線太短，或點與點之間的距離太遠。 | 確認檔案路徑與內容；改用記錄較密的 GPX；或改用行程描述。 |
| `target_gpx_not_round_trip`（代碼已批准）：終點沒有回到起點 | 這個 GPX 不是來回的路線：終點沒有回到起點。 | 請改選單向，或提供含回程的 GPX。 |
| `target_gpx_not_round_trip`：終點回到起點，但無法確認折返點（提案；依 Q-3 第 2 項的裁決新增） | 系統無法確認這個 GPX 的折返點：軌跡不是明確的去回同路，而且沒有指定折返位置，或指定的位置不在軌跡的範圍內。 | 指定折返位置（距起點的公里數，大於 0、小於軌跡總長）；或改選單向。 |

`target_gpx_not_round_trip` 是一個代碼、兩則固定文字，依情形選用（4.13）。第一則的 `message` 與 `actions` 連起來，就是 SPEC-RESOLUTION-001 第 2.8 節批准的那一句固定文字。第二則依 Q-3 第 2 項的裁決新增（處置第 8.2 節第 4 項：訊息說明無法確認折返點，請指定折返位置或改選單向），文字是提案。折返位置先由 CLI 指定；介面上選填的折返欄位是 Should，不是第一張 Streamlit Ticket（UI-0）的 Must。介面沒有這個欄位時，有歧義的 GPX 在介面上只會得到這一則訊息（2026-11-15 的裁決，處置第 9.3 節）；所以第二則的 `actions` 不指向特定的介面欄位（提案）。

**騎士明確要求的休息**（2026-11-15，Q-1 的裁決之後新增；方向的兩列依 Q-3 第 3 項的裁決新增；行程型態也在同一輪追問時的一列依 2026-11-15 的裁決新增，處置第 9.8 節；文字是提案）

| 用途 | 條件 | 文字 |
| --- | --- | --- |
| 追問的固定模板（提案） | 休息需求的地點沒有寫，或不在可以對應的地點之內（4.1 規則第 3 項）。每一筆休息需求一題，主題是 `other` | 行程描述中的這段休息，系統沒有辦法對到這次行程的地點：「{`source_text`}」。請從下列選項選擇休息的地點，或選擇不安排這段休息。 |
| 追問的固定選項 | 同上 | 這次路線請求中各個指定途經點的名稱；「折返點」（只有已知是來回行程時）；「不安排這段休息」 |
| 方向追問的固定模板（提案） | 已知是來回行程、休息需求的地點是指定的途經點，而 `direction` 是 `null`（4.1 規則第 3 項）。每一筆休息需求一題，主題是 `other` | 行程描述中的這段休息，地點在去程與回程都會經過：「{`source_text`}」。請選擇要排在去程或回程，或選擇不安排這段休息。 |
| 方向追問的固定選項（提案） | 同上 | 「去程」；「回程」；「不安排這段休息」 |
| 方向追問的固定模板：行程型態也在同一輪追問時（提案） | 行程型態還不知道、休息需求的地點是指定的途經點，而 `direction` 是 `null`（4.1 規則第 3 項）。和行程型態的那一題放在同一次追問，每一筆休息需求一題，主題是 `other`；選項和上一列相同 | （選擇來回時才需要回答）行程描述中的這段休息，如果是來回行程，地點在去程與回程都會經過：「{`source_text`}」。請選擇要排在去程或回程，或選擇不安排這段休息。 |
| 表單層級的固定訊息（提案） | 追問回覆之後仍然對應不到（4.1 規則第 4 項）。顯示在行程描述欄下方，不產生計畫 | 行程描述中的這段休息仍然沒有辦法排入：「{`source_text`}」。系統沒有產生計畫。請把休息的地點改成這次行程指定的途經點（來回行程也可以是折返點），或刪除這段休息後重新規劃。 |

`source_text` 是休息需求的原文（4.1 的 BreakRequest）。「不安排這段休息」只取消那一筆休息需求，不改變 `rest_policy`（4.1）。`adopted_conditions.unplaced_breaks` 的固定訊息與 `reason` 的兩句固定文字（SPEC-RESOLUTION-001 修正 D 之後新增的）已隨欄位刪除；lead 依 O-2 寫的 `break_not_placeable` 錯誤文字不採用（4.1）。

## 6. 來源證據的型別

G1 定了三種：真實 API、資料快照、模擬。G3 裁決 N6 要求本地衍生資料與本地設定檔另有型別，不得標成 API。這份 Spec 定為五種。

| `source_type` | 顯示文字 | 時間欄位 | 標籤顏色 | 用在哪裡 |
| --- | --- | --- | --- | --- |
| `live_api` | 真實 API | `fetched_at` 必填 | 灰（G3 裁決 N5） | 一般模式下的氣象署預報與日出日沒 |
| `snapshot` | 資料快照 | `snapshot_at` 必填 | 藍 | Snapshot Mode 的預報與日出日沒；加油站快照；路線快照（CR-01）；鄉鎮界線檔（7.13，草案） |
| `simulated` | 模擬 | 都可以是 `null` | 紫 | 路況事件情境檔；Prototype 的模擬檢查點；E2 中標示為 Simulated Weather Scenario 的題目所用的模擬預報（7.9） |
| `local_derived` | 本地衍生資料 | `built_at` 必填 | 灰 | 個人配速表與路線目錄（ETA 的依據）；由目標路線 GPX 建立的路線（CR-01） |
| `local_config` | 本地設定檔 | 都是 `null`；`version` 必填 | 灰 | Rider Profile |

規則：

- 時間欄位只填和型別對應的那一個，其他是 `null`。不得虛構取得時間（Q15）。
- `simulated = true` 的證據一律以「模擬」標示，在介面、實驗紀錄與結果中都和真實資料分開（NFR5）。
- Snapshot Mode 下不得出現 `live_api`。CR-01：Snapshot Mode 也不呼叫路線引擎。
- E2 中標示為 Simulated Weather Scenario 的題目（最多 3 題；7.9），預報的來源證據是 `simulated`，`simulated = true`。這是既有的型別，不新增型別；它和真實預報的題目分開報告。
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
| `EV-FORECAST` | 中央氣象署預報；E2 的 Simulated Weather Scenario 題目是模擬預報 | `live_api` 或 `snapshot`；模擬預報是 `simulated` | 3 |
| `EV-AREA`（草案） | 內政部國土測繪中心的鄉鎮市區界線（本機檔案，不標成 API） | `snapshot` | 3（路段對應鄉鎮，7.13） |
| `EV-STATION` | 加油站快照 | `snapshot` | 2 |
| `EV-ROAD` | 路況事件情境檔 | `simulated` | 4 |

MVP 沒有即時路況來源：真實日期的規則 4 沒有證據，`evidence_ids` 是空清單，結果是 `UNKNOWN`。

## 7. 判定與填值規則

### 7.1 誰可以寫什麼

- 計畫中的數值（時間、油量、機率、距離）一律由主程式從工具輸出複製。Planner 不填寫數值（Q3）。
- Planner 只產生：`route_request`（CR-01；只能引用詞彙表與 Rider Profile 中的代號）、休息需求（BreakRequest，4.1）、`rest_policy`（4.1）、`breaks`（騎士明確要求的休息除外：那些由主程式依休息需求對應後寫入）、`refuel_stops`、`conflicts`、追問、重新規劃的提案，以及說明文字。休息對應不到地點的那一題追問，文字由主程式依固定模板產生（4.2、5.5）。
- 騎士明確要求的休息無法安排時，必須由確定性的程式回報，不由 Planner 判定，也不依賴 Planner 自己回報（2026-11-15，O-2 的裁決）。做法已依 Q-1 的裁決定案（4.1）：主程式在路線解析之前檢查每一筆休息需求的地點，對應不到時以追問回報；路線採用之後由主程式對到檢查點、寫入 `breaks` 並計入 ETA。把行程描述轉成休息需求是 Planner 的工作，系統不保證它的正確率（4.1 規則第 9 項）。不做關鍵詞猜測；`unplaced_breaks` 與 `break_not_placeable` 不採用。
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

初次評估之後最多 2 次。提案不合法（改了不能改的欄位、加油的檢查點不是有資料的加油站、移除、搬移或縮短使用者的休息、移除或搬移騎士指定的加油停留），或和前一輪沒有實質差異時，提前停止並記錄 `stop_reason`。使用者的休息指 `origin` 是 `free_text` 或 `clarification` 的休息（2026-11-15，Q-1 的裁決；4.1 規則第 7 項、4.9）。騎士指定的加油停留指 `refuel_stops[].origin` 是 `free_text` 或 `clarification` 的加油停留；重新規劃可以調整系統安排的加油停留（`planner`、`replan`），包含第一次規劃排的（2026-11-15 的裁決，處置第 9.7 節；4.1 的 RefuelStop）。

### 7.9 E2

E2 的三組都輸出 PlanResult。A3 的 `status_origin` 是 `validator`；A1、A2 是 `llm_declared`。其他差異由 E2 的規格定義。

CR-01：E2 的每一題是一個路線代號加上條件，路線代號對應凍結的路線快照；有工具的組別讀同一份路線。A1 沒有工具，只收到文字描述的行程與條件。任何一組都不會收到座標或私有的幾何（第 2 節「對語言模型的隱私」）。題目的格式由 E2 的規格定義（DESIGN §6.3）。

修改 A2／A3 時，整體流程的差異必須明確記錄（CR-01 第 11 節「保留」）。CR-01 本身已經改了 A3 的整體流程，這三項要和之後的修改一樣記錄在 E2 的規格裡：

- 規劃之前先做路線解析（7.10）。
- 候選全數評估，不分批（7.4）。
- 說明以固定模板優先（7.7）。

A2 與 A3 仍共用相同的路線快照、候選集合、工具與資料快照（Q12）。

審查處置的修正 5：E2 的報告必須把 A2 與 A3 的整體流程差異明確列出，和各項指標一起呈現。自由文字的路線解析（7.10）不在 E2 的範圍內，另由端到端的 Demo 驗收，不納入 E2 已驗證的主張。真實行程題的 Oracle 答案，在分析方法與模型設定凍結之後，由隔離的評估腳本使用保留行程產生（P-5）；同一次讀取產生的封存衍生資料也供 E1 的最後報告使用，之後不再讀原始檔。

SPEC-RESOLUTION-001（2026-11-15 裁決）對 E2 的要求：

- **模擬預報。** 凍結的真實預報裡可能沒有任何高降雨機率提醒的時段。題庫最多可以有 3 題使用模擬預報，題目明確標示為 Simulated Weather Scenario，結果和真實預報的題目分開報告。這些題目的預報來源證據是 `simulated`（第 6 節）。凡是天氣輸入和凍結的真實預報不同的題目（改值或刪除）都算 Simulated Weather Scenario，計入 3 題的上限；人工移除預報來製造 UNKNOWN 的題目也算。真實來源本身缺漏（例如日期超出預報涵蓋區間）不算人工模擬，不計入。
- **題數的算法（2026-11-15，O-4 的裁決）。** 模擬預報的題目計入正式的 12–15 題，最多 3 題。題庫凍結時預先定義三個數：`N_total`（全部正式題目，12–15）、`N_weather_real`（預報沒有經過人工修改的題目）、`N_weather_sim`（預報經過人工修改或移除的題目，不超過 3）；`N_total = N_weather_real + N_weather_sim`。H2 只以主要結果表判讀：`N_weather_real` 的題目，不分題型的合計；全部題目與模擬預報題的兩張表另外報告，不得用來改變 H2 的結論。主要結果表的 N、N_F、N_I 與每個指標的分母都以 `N_weather_real` 的題目重新計數。任何指標的分母少於 5 題時標記「證據有限」（5 是 lead 提案的數值）；H2 所用的任一指標標記「證據有限」時，H2 的結論寫成「證據有限，不下結論」。「沒有明顯升高」沒有事前定的門檻，只列題數，不做判定。題目的執行順序在題庫凍結時固定；因預算停止時，三個 N 都只算三組都跑完的題目，並寫明原訂的題數。
- **相同的資料與凍結。** A1、A2、A3 使用相同的資料：三組的題目文字相同，有工具的組別讀同一份凍結資料；A1 沒有工具，題目文字不另外附上預報值。題庫與 Oracle 在正式 E2 之前凍結。規則不因題目的結果回頭調整。
- **規則 3 題目的預期狀態（2026-11-15，O-1 的裁決；第二輪聚焦審查後修正）。** 規則 3 是專題自訂的策略，不是物理事實；高降雨機率路段取決於抵達時段，抵達時段取決於出發時間、配速表、餘裕係數與鄉鎮對應。Oracle 不匯入 Planner、Validator 或任何工具的程式（DESIGN §6.3）：它不執行 Validator 的程式，也不拿 Validator 的輸出當答案；規則 3 的題目由獨立的程式套用同一個策略的定義（範圍與門檻），檢查的是計畫有沒有遵守策略，不是策略本身對不對。題目分成兩類。**時間不變題**：在題目的候選抵達時間範圍（最早可出發時間到期限）內，規則 3 範圍內每個路段所對應的鄉鎮，各預報時段的降雨機率分類都相同（或都缺）。前提：這一題的 ETA 可以估計；對不到鄉鎮的路段記錄在題庫紀錄；「到期限為止」只對通過規則 1 的候選成立。Oracle 只用凍結的預報、凍結的路線目錄（路段與折返點）、題庫紀錄中的路段對應鄉鎮與定案的範圍判定；結果和出發時間、配速表、餘裕係數無關。路段對應鄉鎮由一支獨立的腳本在題庫凍結時產生並人工核對：輸入是凍結的路線目錄（路段）與鄉鎮界線檔，不匯入 `sources`、`routes`、`pace`、Validator、Planner；路線目錄加入凍結清單（檔案的 SHA-256）；路段的長度與類別來自 production 的 `routes`，是共用的輸入，要揭露。**跨時段題**：不符合上述條件的題目，只有在實作了時間相依的 Oracle 時才正式計分。題目沒有出發時間（只有最早可出發時間與期限），所以時間相依的 Oracle 做兩件事：(a) 對各組計畫自己寫的出發時間判定規則 3；(b) 對題目的候選出發時間（最早可出發時間起、每 15 分鐘一個，到期限為止）逐一判定，得出這一題的預期狀態。輸入全部來自凍結清單：研究用配速表的 `speed_kmh`、`stop_ratio`、`margin_coeff`，路線目錄的路段長度與類別，計畫或題目的休息與加油停留，凍結的預報，路段對應鄉鎮的紀錄。這些輸入和 production 共用，Oracle 獨立的只有程式碼，不寫成「完全獨立」。ETA 算式依 DESIGN §6.1 重寫，抵達時段怎麼對到預報時段依 4.8 與 7.13（草案）；不匯入 `pace`、Validator、Planner 或任何 production 的程式。兩種 Oracle 都以合成案例確認：PASS、FAIL、UNKNOWN 每種結果至少一個案例，預期值由人工驗算並寫入題庫紀錄；時間相依的 Oracle 至少一個案例的抵達時段跨過預報時段的邊界，人工驗算的數值在執行 Oracle 之前寫入題庫紀錄。實作之後可以宣稱的範圍：Oracle 與 A3 在這些題目上對同一份凍結輸入的判定是否一致；不宣稱預報時段的對齊在真實行程上是正確的。沒有實作時間相依的 Oracle 時，跨時段題不出題，或出題但不計分並標明；出題但不計分的跨時段題不是正式題目，不計入 `N_total`、`N_weather_real`、`N_weather_sim`，不占 3 題的上限，也不能用來補足 12–15 題；E2 的報告不得宣稱已驗證跨預報時段的正確對齊。題庫必備的題型是兩種時間不變題：範圍內有提醒（預期 FAIL）與範圍內缺預報（預期 UNKNOWN）；「只有去程有提醒（預期 PASS）」只有在實作了時間相依的 Oracle 時才出題（DESIGN §6.3）。三組收到相同的任務說明（2026-11-15，Q-2 的裁決；處置第 7.2 節）：A1、A2、A3 的任務說明共用五條規則的自然語言定義，三組相同；任務說明不提供個別題目的 Oracle 答案，也不提供不屬於該組的工具數值（A1 沒有工具，不會收到任何工具的輸出）。任務說明在題庫凍結前寫進 E2 的規格。兩類題目的定義是 lead 依裁決寫定的，待確認。完整的規則在 DESIGN §6.3；裁決的原文在 [lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 5.1 節，第二輪聚焦審查後的修正在第 6.1 節。
- **Over-refusal Rate。** E2 必須報告 Over-refusal Rate，不得只報告規則符合率。來回行程的規則 3 檢查整段回程，比原本的範圍嚴格，可行的計畫會變少。規則 3 題目的預期狀態本身就依方案 A 判定，所以 Over-refusal Rate 只能量出各組偏離規則的程度，量不到方案 A 比「最後 20%」嚴格多少；方案 A 的代價另以文字與 SPEC-RESOLUTION-001 第 3.2 節的路線資料說明，報告要照實寫。Over-refusal Rate 與它的定義不變。
- **方案 A 與方案 B 的敏感度分析（2026-11-15，O-5 的裁決）。** 對來回行程的題目，以完全相同的凍結資料，分別用方案 A（整段回程）與方案 B（路線最後 20%）判定規則 3。分開報告兩個數：(1)「額外的規則 3 FAIL」：方案 A 是 FAIL、方案 B 不是 FAIL 的題數；(2)「因規則 3 的差異而使整體計畫由可行轉為不可行」的題數：預期狀態在方案 B 之下是 `FEASIBLE` 或 `CONDITIONAL`、在方案 A 之下是 `INFEASIBLE`。這是敏感度分析，不稱為 Over-refusal Rate，也不推論額外的拒絕是否不合理。兩個數由 Oracle 在題庫凍結時算出（這一句是 lead 依裁決寫定的，待確認）；跨時段題只有在實作了時間相依的 Oracle 時才納入，否則註明未納入。兩個數都附分母（納入分析的來回題數），並分成真實預報與模擬預報兩列。要揭露：模擬預報的題目是刻意設計成方案 A 與方案 B 結果不同的，所以模擬預報那一列的「額外的規則 3 FAIL」必然至少是 1，不代表方案 A 在實際預報下多拒絕多少；有參考價值的是真實預報那一列，題數可能是 0。方案 B 的判定和方案 A 一樣要有合成案例與人工驗算。
- **凍結的路線快照。** 題目以 `route_id` 指定快照。凍結清單列出每個快照的 `snapshot_id` 與檔案的 SHA-256；Runner 以嚴格模式執行：只採用清單指定的快照，執行前核對雜湊，凍結清單沒有對應的項目、檔案不存在或雜湊不符就停止，不回退到其他快照（7.11 第 3 項；2026-11-15，Q-3 第 6 項的裁決與處置第 9.9 節）。凍結清單中的快照在凍結時以現行的國道檢查方法檢查過；檢查方法在 E2 凍結之後不得更改。

### 7.10 路線解析（CR-01）

1. 表單的檢查通過後，Planner 把行程描述轉成 `route_request`，並把騎士要求的每一段休息轉成一筆休息需求（4.1 規則第 1 項）；騎士明確選擇整趟不安排休息時填入 `rest_policy = none`，否則是 `default`（4.1）。提供目標路線 GPX 時不解析路線的地點，只取 `trip_type`；休息需求照常產生。
2. 缺起點、進入端或行程型態時回傳 ClarificationRequest（4.2）。主程式在這一步、路線解析之前，依 `route_request` 檢查每一筆休息需求：地點沒有寫或不在可以對應的地點之內、長度沒有寫，或來回行程途經點的休息沒有方向時，把問題放進同一次追問（4.1 規則第 2、3 項）。行程型態和休息方向在同一輪追問，不增加第二輪：行程型態也在這一輪問的時候，方向的那一題標明「選擇來回時才需要回答」（處置第 9.8 節）。追問回覆之後仍然對應不到時，不產生計畫，由表單的檢查擋下（4.1 規則第 4 項）；這不是 `route_error`。
3. 主程式依 `route_request` 取得路線，順序見 7.11 第 3 項。Snapshot Mode 只讀已保存的路線快照，不呼叫路線引擎；指定了凍結清單時是嚴格模式。
4. 路線引擎的結果，每個方向都通過國道檢查、沒有警告、偏移在門檻內而且中間位置的順序相符才採用（7.11 第 5–8 項）。採用後建立路段與檢查點，填寫 `route_id` 與 `route`。
5. 任何一步失敗時回傳 `route_error`（4.13），不評估候選。
6. 路線採用之後、評估候選之前，主程式把每一筆休息需求對到檢查點，寫成 `breaks` 的一筆，長度計入 ETA（4.1 規則第 5 項）。沒有把騎士指定的休息納入 ETA 的計畫，不得作為已滿足條件的有效計畫（2026-11-15，O-2 的裁決；做法依 Q-1 的裁決，4.1）。

對路線服務與地名查詢的請求只送出公開地標；私有 GPX 與住家位置不送往第三方（CR-01 D2）。送給語言模型的內容依第 2 節「對語言模型的隱私」。

### 7.11 路線模組的確定性規則（CR-01）

這張表是路線模組各項規則的唯一定義處。DESIGN.md 只寫摘要並指向這裡；兩份文件不互相把定義推給對方。第 1–10 項已依 [SPEC-RESOLUTION-001](SPEC-RESOLUTION-001-sb2-sb8-sb9.md)（2026-11-15 裁決）定案並寫回這張表；數值是設定常數，定案後不依測試結果調整。聚焦審查後的修正（[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)的 F-15 至 F-22）也已寫入。先前標為「由裁決推導」的七項細節已由專題負責人逐項裁決（2026-11-15，Q-3；[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 8 節），第 1、2、3、4、8、9 項已依裁決改寫。狀態欄標明「lead 寫定」的部分不是裁決的原文，是裁決沒有寫、為了讓規則可以實作而補上的最小內容。處置第 5.6、6.3 節與 [q3_derived_details.md](../cr/CR-01-appendix/q3_derived_details.md) 是裁決之前的清單。第 9 項中，騎士明確要求的休息已依 Q-1 的裁決定案（2026-11-15；處置第 7.1 節）：規則的定義處是 4.1，這張表只寫摘要；lead 先前依 O-2 定的做法不採用；來回行程途經點的休息依方向安排（Q-3 第 3 項的裁決）。Q-3 後續的九項（A、B1–B3、C1–C5）與兩件附帶的事已由專題負責人裁決（2026-11-15；處置第 9 節），第 2、3、9 項已依裁決改寫；處置第 9 節取代第 8 節中和它不同的地方。都尚未實作。

| 編號 | 項目 | 規則 | 狀態 |
| --- | --- | --- | --- |
| 1 | `snapshot_id` 的樣式；快照的重用與不覆寫 | 一條路線對應一個路線快照，一個代號。`SN-` 加 10 個小寫十六進位字元，樣式 `^SN-[0-9a-f]{10}$`：取自正規化後的快照內容（依第 2 節的規則）的 SHA-256 前 10 碼。雜湊的範圍不含 `snapshot_id` 本身與各方向的取得時間（`fetched_at`）。重新取得後內容完全相同：代號相同，沿用既有的檔案，不寫入、不修改。內容不同（折線或任何其他內容）：新的代號、新的檔案，舊檔不動。以既有的代號寫入不同的內容時報錯，不覆寫。路線引擎路線的 `route_id` 用同一組十六進位字元（第 2 節），和快照一對一；新的快照有新的 `route_id`。已保存的結果繼續記錄並顯示它當時使用的 `route_id` 與 `snapshot_id`，不會被改指到新的快照；要用新的快照就重新規劃，得到新的結果。快照不可變：檔案寫入一次之後不再修改，程式也不刪除。不另建索引檔或版本號 | 已定（SPEC-RESOLUTION-001 第 2.1、2.2 節，2026-11-15 裁決；修正 A）。代號的格式、內容相同就重用、內容不同不覆寫、已保存結果的指向依 Q-3 第 1 項的裁決（2026-11-15，有條件批准；處置第 8.1 節）。雜湊的範圍不含取得時間是 lead 寫定，已由 2026-11-15 的裁決保留（處置第 9.10 節）；目標路線 GPX 的 `RG-` 代號含實際採用的折返位置（第 2 節；處置第 9.1 節）；第 2 節正規化規則中公尺值與其他浮點數的位數也是 lead 寫定 |
| 2 | 去程、回程與折返點 | 來回行程是一個路線快照、兩個方向。去程的請求是起點、途經點、目的地；回程是目的地、倒序的途經點、起點。各送一次，回程不由去程的折線反轉產生；兩個方向不保證走相同的道路。折返點是目的地；目的地是公路時，折返點是公路上進入端的另一端（由詞彙表定義）。去程與回程分開切段，折返點一定是路段邊界；路段編號連續，編號小於去程段數的是去程。折返點是 `kind = turnaround` 的檢查點；加油站在兩個方向各自投影，各有一個檢查點；每個指定的途經點在兩個方向各建立一個 `kind = waypoint` 的檢查點（第 9 項）。任何一個方向失敗，整條路線失敗。**目標路線 GPX（修正 E；2026-11-15，Q-3 第 2 項的裁決）：** 系統不由幾何推定行程型態；行程型態只來自表單、行程描述或追問。來回的條件不變：騎士明確指定來回，而且 GPX 的終點回到起點（相距 200 m 以內），才當成 `round_trip`；只指定折返點不足以證明有回程，終點沒有回到起點時回傳 `route_error`（`target_gpx_not_round_trip`），即使指定了折返位置也一樣。折返點的決定依下列順序（2026-11-15 的裁決；處置第 9.2–9.4 節）。(i) 騎士指定了折返位置 `target_gpx_turnaround_km`（距離起點的軌跡里程，以公里表示，換算成公尺後使用；4.1）而且合法（大於 0、小於軌跡總長）時，以那個位置為折返點。騎士明確指定的合法折返位置優先於自動判定，軌跡明確去回同路時也一樣。(ii) 騎士沒有指定時做去回同路的自動辨識：先以離起點直線距離最遠的軌跡點（有多個時取第一個）把軌跡分成前後兩段；後段每 100 m 取一點，取樣點 50 m 內有前段的軌跡點算接近。接近的取樣點達 90% 以上時算明確去回同路，自動以那個最遠點為折返點。50 m／100 m／90% 是 MVP 自動辨識的保守啟發式門檻，沒有以真實資料驗證過，文件與報告都不得宣稱它經過驗證。(iii) 沒有達到 (ii) 的條件時（環狀、8 字形、重合比例不足或其他有歧義的幾何），不自動推定折返點，也不默默猜測，交給騎士指定。有歧義而騎士沒有指定折返位置，或指定的里程不合法時，不規劃，回傳 `target_gpx_not_round_trip`，訊息說明無法確認折返點（5.5）；不新增錯誤代碼。折返位置先由 CLI 指定；介面上選填的折返欄位是 Should，不是第一張 Streamlit Ticket（UI-0）的 Must，不得擋住 UI Gate；介面沒有這個欄位時，有歧義的 GPX 在介面上只會得到 `target_gpx_not_round_trip` 的訊息。`RG-` 的 `route_id` 含實際採用的折返位置（第 2 節）。目標路線 GPX 的來回路線在折返點切開，去程與回程分開切段，折返點是路段邊界。系統不推定、不反轉，也不補造回程。騎士指定單向時幾何原樣使用，即使起點與終點重合，也不使用折返位置。`target_gpx` 的來回路線沒有 `legs` | 已定（處置 L-3；SPEC-RESOLUTION-001 第 2.3、2.8 節，2026-11-15 裁決；修正 E）。目標路線 GPX 的折返點依 Q-3 第 2 項的裁決（2026-11-15，修改；處置第 8.2 節）；先前「不接受折返位置、一律取最遠點」的寫法作廢。去回同路自動辨識的門檻（保守的啟發式，沒有以真實資料驗證）、折返位置以「距起點的公里數」輸入並先由 CLI 支援、騎士指定的合法位置優先於自動判定、`RG-` 代號含實際採用的折返位置，已由專題負責人裁決（2026-11-15；處置第 9.1–9.4 節）；欄位名稱 `target_gpx_turnaround_km` 是 lead 定的。途經點的 `waypoint` 檢查點依 O-2 的裁決（2026-11-15） |
| 3 | 取得路線的順序；快照的產生、重用與失效 | (a) 有目標路線 GPX：用它的幾何，不呼叫路線引擎。(b) Snapshot Mode：只讀已保存的快照，不呼叫路線引擎，不看 30 天的期限。分兩種。**一般的 Snapshot Mode**（沒有指定凍結清單）：用 `request_key` 相同、`freeway_check_method` 和現行方法相同的已保存快照中，取得時間最晚的一個；沒有時回 `snapshot_missing`。**嚴格模式**（執行時指定了凍結清單：E2 的 Runner 與凍結的 Demo）：只採用清單指定的 `snapshot_id`，並核對檔案的 SHA-256；凍結清單沒有對應的 `request_key` 或 `snapshot_id`、檔案不存在或雜湊不符時停止執行，不回退到任何其他快照，即使有取得時間更晚的快照。兩種模式下，`freeway_check_method` 和現行方法不同的快照都不採用；嚴格模式下遇到這種情形同樣停止。(c) 一般模式：先算 `request_key`。有 `request_key` 相同、`freeway_check_method` 和現行的檢查方法相同、取得時間在 30 天內的快照時，用其中最新的一個，不呼叫引擎。沒有時呼叫路線引擎（來回行程兩次），再做道路屬性查詢（第 5 項）。每個方向都通過三項檢查才採用並存檔：回應沒有警告（第 7 項）、國道檢查通過（第 5 項）、起點、終點與中間位置的偏移與順序都符合（第 8 項）。存檔依第 1 項：內容和既有的快照完全相同時沿用既有的檔案，不寫入、不修改；內容不同時存成新的快照。任何一個方向沒通過就整條不存檔，回 `route_error`。**失效：** `request_key` 不同、超過 30 天，或 `freeway_check_method` 不同。失效只表示一般模式不再重用；檔案原樣保留，舊檔不動。沿用既有的檔案時，它的取得時間不更新：同一條路超過 30 天之後，一般模式每次規劃都會重新向路線引擎取得；內容沒有變時不產生新檔。這是 MVP 的已知限制：不得偽造或覆寫取得時間，也不為此新增複雜的快取架構。引擎失敗時回 `routing_unavailable`，一般模式不改用已失效的快照；騎士可以切到 Snapshot Mode。快照的取得時間是各方向 `fetched_at` 中最晚的一個。**E2 與 Demo 的凍結：** 凍結清單列出每個快照的 `snapshot_id` 與檔案的 SHA-256；E2 的題目以 `route_id` 指定快照；兩者都以嚴格模式執行，不經過一般的選擇。凍結清單中的快照在凍結時以現行方法檢查過；檢查方法在 E2 凍結之後不得更改 | 已定（SPEC-RESOLUTION-001 第 2.1 節，2026-11-15 裁決；修正 A）。內容相同就沿用既有的檔案依 Q-3 第 1 項的裁決（處置第 8.1 節）。Snapshot Mode 的兩種模式、凍結清單記錄檔案的雜湊、檢查方法不相容時不採用，依 Q-3 第 6 項的裁決（2026-11-15，修改；處置第 8.6 節）。「指定了凍結清單就是嚴格模式」是 lead 寫定的觸發方式。凍結清單的每一筆記錄 `request_key`、`snapshot_id` 與檔案的 SHA-256，嚴格模式以 `request_key` 查到這一筆。嚴格模式在凍結清單沒有對應的項目時停止、超過 30 天後重複查詢是 MVP 的已知限制，依 2026-11-15 的裁決（處置第 9.9、9.10 節） |
| 4 | `request_key` 與快照的比對 | `request_key` 是正規化 JSON 的 SHA-256（正規化規則見第 2 節），內容是 `trip_type`、`origin`、`destination`、`via`（含 `entry_ref_id`，依順序）與 `routing_params`。每個地點以「代號加指紋」表示：指紋是該地標座標定義的 SHA-256 前 16 碼，座標先正規化為小數六位（第 2 節）。只有被引用的地標改過，才算不同的請求；沒有被引用的地標改變時 `request_key` 不變。完全相同才算同一個請求。鍵裡沒有座標本身，不顯示。不用整份詞彙表的版本：版本一改，所有已保存快照的鍵都對不上，Snapshot Mode 會找不到任何快照。一個 `request_key` 可以對應多個不同時間的快照；一個快照只對應一個 `route_id` | 已定（SPEC-RESOLUTION-001 第 2.2 節，2026-11-15 裁決）。正規化規則寫在第 2 節，不留給 Tickets。地標代號加座標定義的指紋、不用整份詞彙表的版本，依 Q-3 第 5 項的裁決（2026-11-15，有條件批准；處置第 8.5 節）：指紋取前 16 碼，座標正規化為小數六位 |
| 5 | 國道檢查 | 逐方向判定，結果記在 `freeway_check`。資料來源：對同一個路線引擎再送一次道路屬性查詢（`trace_attributes`），只送出引擎自己回傳的折線，取每個路段的道路等級、道路名稱與長度；做法記在 `freeway_check_method`。結果有三種。四項都成立才是 `pass`：(1) 道路屬性查詢成功，回傳的總長度和路線里程相差不超過 2%；(2) 道路等級為 `motorway` 的里程是 0；(3) 道路屬性的名稱與轉向指示的道路名稱都不符合 `國道\|高速公路\|Freeway`，轉向指示也沒有標為 highway 的；(4) 引擎回報的 `has_highway` 是 `false`。**有任何國道的訊號（第 2–4 項的任何一項，任一方向）就是 `fail`（修正 B：訊號互相矛盾時 fail closed）**，回 `highway_in_route`，優先於其他原因（警告、偏移、無法驗證）；例如 `has_highway` 是 `true` 而道路屬性查不到國道，仍然不採用。沒有國道的訊號但無法驗證（查詢失敗、長度不符，或引擎沒有回報 `has_highway`）時也不採用，回 `routing_unavailable`；這時不產生 `freeway_check` 的值，也不存快照。**用語（修正 F）：** 這項檢查和路線用的是同一個引擎與同一份開放圖資，圖資標錯時兩者會一起錯。先前的文件與 P-1 的裁決稱它「獨立的國道檢查」，意思只是它不依賴路線參數與引擎的單一旗標；它不是道路主管機關資料的獨立驗證，文件、介面與報告都不得這樣宣稱。這項檢查只管國道；快速公路與其他禁行機車的路段不在範圍內。目標路線 GPX 的路線不做這項檢查 | 已定（SPEC-RESOLUTION-001 第 2.4 節，2026-11-15 裁決；修正 B、F） |
| 6 | 採用條件 | 每個方向都是 `freeway_check = pass`、回應沒有警告（第 7 項）、起點、終點與中間位置的偏移都在門檻內（第 8 項），才採用，才存成快照。這一條沒有例外，和路線參數無關 | 已定（CR-01 第 16 節；處置 L-5；SPEC-RESOLUTION-001 第 2.1 節，2026-11-15 裁決） |
| 7 | 回應的警告 | 路線參數是 `use_highways: 0`（P-1 裁決），請求不送出硬性排除（`exclude_highways`）。回應出現任何警告就不採用，回傳 `route_error`（`routing_unavailable`；同時有國道的訊號時是 `highway_in_route`，第 5 項）。`use_highways: 0` 是偏好，不是保證：採用與否仍由第 5、6 項的國道檢查決定。已知限制：這個設定可能連快速公路也避開，平面轉場較慢（檢查 C4b） | 已定（P-1 裁決，2026-11-15） |
| 8 | 起點、終點與途經點的偏移；途經點的順序 | 每個方向檢查三種位置：起點（地標到折線起點的距離）、終點（地標到折線終點的距離）、送給引擎的每一個中間位置（地標到折線最近點的距離）。中間位置包含指定的途經點與公路的進入端（`entry_ref_id`）。起點與終點記在 `endpoint_offset_m`，中間位置依送出的順序記在 `via_offset_m`。任何一個超過 **200 m** 就不採用，回 `routing_unavailable`。**順序：** 每個中間位置在折線上最近點的沿線里程，必須依請求的順序遞增；不符合時不採用，回 `routing_unavailable`。這是為了擋下靠近但沒有依序經過的路線。路線服務在目的地附近沒有道路時仍會回傳路線，而且沒有警告，所以產品要自己量。詞彙表建立時，偏移超過 100 m 的地標先調整位置 | 已定（SPEC-RESOLUTION-001 第 2.5 節，2026-11-15 裁決；修正 C）。`via_offset_m`、把公路的進入端納入檢查與 200 m 的門檻已由 Q-3 第 4 項的裁決批准（2026-11-15；處置第 8.4 節）。裁決另要求依路線行進順序驗證途經點；順序的判定方式是 lead 依裁決的測試要求寫定 |
| 9 | 預設休息的排入；途經點的檢查點與騎士指定的休息 | 由這份 Spec 定義。Rider Profile 的設定：`default_break_interval_min`（連續騎乘多久休息一次，預設 90）與 `default_break_duration_min`（每次多久，預設 15），可以在設定檔修改。`rest_policy = default`（4.1），而且行程描述與追問之後沒有任何騎士指定的休息安排時才套用；由主程式排，不經過語言模型。`rest_policy = none`（騎士明確選擇整趟不安排休息）時不套用預設休息，折返點的那一次也不排。在追問中取消了某一筆或全部的個別休息需求，不等於整趟不休息：取消之後沒有任何休息安排而 `rest_policy = default` 時，預設休息照常套用（2026-11-15 的裁決；處置第 9.6 節）。排入規則：一個檢查點最多一筆休息（契約 4）。排入的順序固定：先排騎士指定的休息與加油停留，再排來回行程折返點的那一次，最後排預設休息。預設休息依路線順序走過檢查點，累計典型騎乘時間（含停等寬放）；累計到間隔時，在下一個不是起點、終點的檢查點之後排一次休息，累計歸零；那個檢查點已經有休息時不再排預設休息，累計歸零。加油停留與折返點的休息也讓累計歸零。套用預設休息時，來回行程的折返點固定排一次休息，長度相同；折返點已經有休息時不再加。騎士已經給了休息安排時，預設休息整組不套用，折返點的這一次也不排。到終點之前沒有檢查點時不排，不報錯。兩個設定值任一缺少時不排預設休息，走既有的追問（休息長度）。每一筆 `origin = rider_profile`，只能排在檢查點之後（契約 4 的 `after_checkpoint_id`）；同樣的路線與設定得到同樣的結果；重新規劃可以調整它們（7.8）。**途經點的檢查點（2026-11-15，O-2 的裁決）：** 每個指定的途經點，偏移檢查通過（不超過 200 m，第 8 項）後，在離它最近的路段邊界建立一個 `kind = waypoint` 的檢查點（契約 2 既有的種類），名稱是地標的名稱；來回行程的去程與回程各建立一個。可以排休息的檢查點是 `waypoint`、`fuel_station`、`turnaround`，而且要符合契約 4 的位置條件：不在路線的起點與終點。檢查點依行經的順序編號；同一個位置有多個檢查點時加油站在前。`waypoint` 不當作 `fuel_station`，也不列入 FuelPlan 的檢查點（4.7）。編號與加油安排這兩點依 2026-11-15 的裁決（處置第 9.5 節）；位置條件是 lead 寫的細節（處置 G-22）。**騎士明確要求的休息（修正 D；O-2 與 Q-1 的裁決）：** 規則的定義處是 4.1，這裡是摘要。無法安排時，必須由確定性的程式回報，不能依賴語言模型自己發現；沒有把指定的休息納入 ETA 的計畫，不得作為已滿足條件的有效計畫。Planner 先產生休息需求（地點、長度、原文、來源）。可以對應的地點是這次路線請求中指定的途經點，以及來回行程的折返點。對應不到時由主程式以追問回報，追問之後仍然對應不到時不產生計畫。路線採用之後，主程式把途經點對到它的 `waypoint` 檢查點（來回行程依休息需求的方向對到去程或回程的那一個；方向不明時先以追問確認，行程型態也未知時兩題在同一輪），把折返點對到 `turnaround` 檢查點，成為 `breaks` 的一筆並計入 `ETA_typ`。重新規劃不得移除、搬移或縮短這些休息；騎士指定的加油停留也不得移除或搬移，系統安排的可以調整（4.1 的 RefuelStop；處置第 9.7 節）。不做關鍵詞猜測；`adopted_conditions.unplaced_breaks` 與 `break_not_placeable` 不採用 | 預設休息的排入已定（SPEC-RESOLUTION-001 第 2.6 節，2026-11-15 裁決；修正 D；排入的順序是聚焦審查後補上的）。途經點的檢查點已依 O-2 的裁決定案（2026-11-15）。騎士明確要求的休息已依 Q-1 的裁決定案（2026-11-15，有條件批准；處置第 7.1 節），並依 Q-3 第 3 項的裁決修改（2026-11-15，部分批准；處置第 8.3 節）：「對應不到時以追問回報、追問之後由表單的檢查擋下」是 lead 依 Q-1 的裁決寫定的做法，已由 Q-3 第 3 項的裁決接受；來回行程途經點的休息依方向安排，方向不明時追問，先前「一律排在去程」的做法作廢；`direction` 的欄位名稱是 lead 定的；其餘是 Q-1 的裁決。`waypoint` 檢查點的編號與加油安排、`rest_policy` 與兩種「不休息」的意圖、重新規劃保留騎士指定的加油停留、行程型態與方向同一輪追問，已由專題負責人裁決（2026-11-15；處置第 9.5–9.8 節）；`rest_policy` 的欄位名稱是 lead 定的。SB-8 是 CLOSED（11.1） |
| 10 | `ridden_share_pct` 的算法 | 由這份 Spec 定義。路線每個方向每 100 m 取一點（沿用路線目錄既有的取樣）。取樣點 **50 m** 內有任何一趟配速行程修剪後的軌跡點，算接近，不分方向。連續接近的取樣點**少於 3 個**的片段不算，避免把橫越的道路算進去。數值是接近的取樣點數除以全部取樣點數，乘以 100，取整數；去程與回程分開比對再合計。只用幾何，不讀時間，在本機比對。保留行程與被排除的行程不參與比對。沒有配速行程時為 `null`。**用語（修正 G）：** 這個數值只表示路線的幾何和配速行程的軌跡接近的比例。它不保證實際走過同一條道路（並行的道路、高架與平面道路都可能在 50 m 內），也不代表騎士騎過的所有道路。介面稱為「配速資料中的路線涵蓋比例」（審查處置的修正 1） | 已定（審查處置的修正 1；SPEC-RESOLUTION-001 第 2.7 節，2026-11-15 裁決；修正 G） |
| 11 | 去回里程差 | `leg_length_diff_pct` 是去程與回程里程相減的絕對值，除以兩者的平均，再乘以 100。大於 2 時 `leg_length_diff_flag = true`，介面在路線摘要標示。它只是告知，不影響路線是否採用 | 已定（處置 L-3） |

### 7.12 行程描述的本機輸入保護（CR-01 審查處置的修正 2；草案）

行程描述（`free_text`）會送給語言模型，語言模型的 API 是第三方（第 2 節）。只在介面上提醒不要寫住家地址並不足夠，所以送出前先在本機檢查。尚未實作；擋下的樣式是草案，凍結前確認（SB-6）。

| 編號 | 項目 | 規則 |
| --- | --- | --- |
| 1 | 時機 | 屬於表單檢查：在建立規劃請求、呼叫語言模型之前執行。檢查本身不經過語言模型，也不呼叫任何外部服務 |
| 2 | 擋下的樣式（2026-11-15 裁決，U-1：收窄） | (a) 門牌的寫法：前面有街道用語（路、街、巷、弄、段）而後面是數字加「號」；或有明確門牌語境的「數字加號」接「數字加樓」。只有數字加「號」不算門牌，公路的寫法不得被擋下。(b) 座標的寫法：成對的小數經緯度。驗收案例見下表；確切的正規表示式由實作的 Ticket 寫定 |
| 3 | 命中時 | 不送出，不進入規劃，回到表單，在欄位下方顯示 5.5 的固定訊息。沒有「仍然送出」的選項（CR-01 D2：住家位置不送給第三方） |
| 4 | 誤擋 | 公開地標的門牌地址也會被擋下；騎士改用公路或地標的名稱 |
| 5 | 明確的限制 | 這是樣式比對，只能擋下常見的寫法。以地名、店名或敘述透露的住家位置（例如「我家巷口的超商」）擋不住。這份 Spec 與產品都不宣稱行程描述一定不含私人地址；介面的說明與期末報告的限制要寫明這一點 |
| 6 | 紀錄 | 被擋下的文字不寫入結果、紀錄檔或實驗紀錄 |
| 7 | E2 | 題目的文字由題庫提供，同樣先通過這個檢查 |

**驗收案例（2026-11-15 裁決，U-1）。** 確切的正規表示式留給實作的 Ticket，但必須通過下列案例。

| 輸入中含有 | 結果 |
| --- | --- |
| 「中正路 123 號」 | 擋下 |
| 「中正路一段 123 號」 | 擋下 |
| 「123 號 5 樓」（明確的門牌語境） | 擋下 |
| 成對的小數經緯度 | 擋下 |
| 「國道 3 號」 | 不擋下 |
| 「台 9 線」 | 不擋下 |

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
| 待確認事項 | 推薦候選中 `result = UNKNOWN` 的 `rule_results[].manual_check_guidance`。`unplaced_breaks` 不採用，這裡沒有「排不進去的休息」的訊息；騎士明確要求的休息對應不到地點時以追問回報，追問之後仍然對應不到時由表單的檢查擋下，沒有結果（4.1、4.2） |
| 四張數值卡片 | 推薦候選的 `departure_time`、`eta_typ_end`、`eta_safe_end`、`time_margin_s`；抵達時間旁有 5.5 的固定句子（抵達時間的說明；餘裕係數是預設值時另加一句） |
| 說明 | `explanation.text`；CR-01：`explanation.planner_text` 與 `explanation.planner_text_status` |
| 採用的條件、衝突提示 | `adopted_conditions` |
| 加油安排 | 推薦候選的 `fuel_plan` |
| 天氣 | 推薦候選的 `weather`；`in_rule3_range` 決定哪些列標示為規則 3 的範圍。來回行程的去程有高降雨機率提醒時，另顯示 5.5 的固定句子 |
| 來源證據 | `evidence` |
| 頂端的 Snapshot Mode 標籤 | `adopted_conditions.data_mode`（描述畫面上的結果） |
| 結果過期 | 表單和 `adopted_conditions` 的比對。CR-01：Profile 更新後，另以 `EV-ETA` 的 `version` 和目前的 `pace_version` 比對 |
| 逐條規則結果 | `rule_results` |
| 最終輸出的驗證 | `explanation.rule5`，或 `result_kind` |
| 全部候選 | `candidates` 中最後一輪的候選（`round_index` 最大的）。CR-01：唯讀，不選取。先前各輪的候選保留在結果裡，介面不顯示 |
| 重新規劃紀錄 | `replan_rounds` |
| 無可行解 | `infeasibility_report` |

## 9. 驗收與測試規格

實作時必須有的測試。目前都**尚未實作**。S31–S45 對應 SPEC-RESOLUTION-001 的測試編號（SB2-T、SB8-T、SB9-T）；其中 S31–S34 測的是資料契約 1、3、4 與配速模組，列在這裡是為了追溯。S46–S52 對應 Q-1 的驗收測試（Q1-T1 至 T7；[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 7.1 節）。S53–S77 對應 Q-3 七項裁決的測試（Q3-T1 至 T25；處置第 8 節），依序一對一。S78–S86 對應 Q-3 後續九項裁決的測試（Q3-T26 至 T34；處置第 9 節），依序一對一。RI-1 至 RI-3 是 `routes` 整合的驗收條件，列在表後；它們不屬於第一批 Scoped Tickets（BATCH-1）。

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
| S14 | CR-01：`route_error` 的六種 `code` 各有一個案例（第六種 `target_gpx_not_round_trip` 依 SPEC-RESOLUTION-001 新增）。結果符合 4.13：沒有 `route`，`candidates` 是空清單，`message` 與 `actions` 和 5.5 完全相同。`target_gpx_not_round_trip` 的兩種情形（終點沒有回到起點；無法確認折返點）各一個案例，各用 5.5 對應的那一則文字 |
| S15 | CR-01：路線引擎失敗，或回傳的路線沒有通過國道檢查時，結果中沒有任何路線的里程與道路名稱；Planner 的輸出不會被當成路線。一般模式下不會改用已失效的路線快照（7.11 第 3 項） |
| S16 | CR-01：`route.freeway_check` 不為 `fail`。三種 `route_source` 各有一個案例，欄位的必填與 `null` 符合 4.12 的跨欄位規則 |
| S17 | CR-01：Snapshot Mode 下不呼叫路線引擎；沒有對應的路線快照時回傳 `snapshot_missing` |
| S18 | CR-01：ClarificationRequest 的 `topic` 只有五個值；`start_point` 與 `entry_side` 的選項都存在於詞彙表或 Rider Profile |
| S19 | CR-01：`route_request` 的每個 `ref_id` 都存在於詞彙表或 Rider Profile。行程型態在表單與行程描述不一致時以表單為準，並有 ConflictNotice |
| S20 | CR-01：顯示的文字中，道路寫法都在 `route.road_names` 裡（7.7 的兩步檢查）；涵蓋比例句子的數值等於 `route.ridden_share_pct`，去回里程差句子的數值等於 `route.leg_length_diff_pct` |
| S21 | CR-01：來回行程中，去程與回程都經過的加油站在 `fuel_plan.checkpoints` 出現兩次，`checkpoint_id` 不同；`turnaround_checkpoint_id` 指向 `kind = turnaround` 的檢查點 |
| S22 | CR-01：送給語言模型的內容（提示與工具輸出）沒有座標樣式的數值，沒有折線、軌跡點、GPX 的路徑與檔名，也沒有逐趟的騎乘資料（第 2 節） |
| S23 | CR-01：路線快照符合 4.14。來回行程的快照有 `outbound` 與 `return` 兩筆 `legs`，各有自己的 `request`、`shape` 與 `fetched_at`；`return` 的折線不是 `outbound` 的反轉。每一筆都有 `warnings`、`has_highway`（一定是 `false`）、`freeway_check`、`freeway_check_method`、兩端的 `endpoint_offset_m` 與 `via_offset_m`；快照沒有高度欄位 |
| S24 | CR-01：任何一個方向的 `freeway_check` 是 `fail` 時，整條路線不存成快照，結果是 `highway_in_route`。去回里程差大於 2% 時 `leg_length_diff_flag = true` |
| S25 | CR-01：Rider Profile 的預設休息排入後，每一筆的 `origin = rider_profile`，都排在檢查點之後；同樣的輸入得到同樣的安排（7.11 第 9 項） |
| S26 | 審查處置：行程描述含門牌或座標的樣式時，不建立規劃請求，也不呼叫語言模型；顯示 5.5 的固定訊息。案例依 7.12 的驗收案例表（2026-11-15 裁決）：「中正路 123 號」「中正路一段 123 號」「123 號 5 樓」與成對的經緯度都被擋下；「國道 3 號」「台 9 線」不被擋下 |
| S27 | 審查處置：目標路線 GPX 不會被系統推定為來回。行程型態不由幾何決定；騎士指定來回、但 GPX 的終點沒有回到起點時回傳 `route_error`（`target_gpx_not_round_trip`）。折返點只在明確去回同路時自動決定；有歧義時由騎士指定折返位置，無法確認時回傳同一個代碼；騎士指定的合法折返位置優先於自動判定（7.11 第 2 項；Q-3 第 2 項的裁決；S59–S64、S79、S80） |
| S28 | 審查處置：`pop_pct` 有值的 WeatherSegment 一定有 `forecast_period_start`、`forecast_period_end` 與 `forecast_resolution_h`；顯示的文字沒有把降雨機率寫成某一時刻的預報 |
| S29 | 審查處置：路段對不到鄉鎮時 `pop_pct` 是 `null`，不是 `LOW`；路段經過多個鄉鎮時 `pop_pct` 是其中最高的值（7.13） |
| S30 | 審查處置：送給路線引擎的請求帶 `use_highways: 0`，不帶硬性排除；回應有警告時結果是 `route_error`（`routing_unavailable`） |
| S31 | 停等的分類（SB2-T1、SB2-T2、SB2-T3；契約 1）：兩步都快於 20 km/h、中間夾 1 秒重複位置的合成軌跡沒有停留，這 1 秒在 `moving_time_s` 裡。2 秒的停留進移動時間；3 秒與 179 秒進 `short_stop_time_s`；180 秒只進 `stopped_time_s`。每個路段 `short_stop_time_s` 不大於 `stopped_time_s`；整趟的移動時間加停留時間等於修剪後的總歷時（容許捨入） |
| S32 | 配速表的停等比例與餘裕係數（SB2-T4、SB2-T7、SB2-T9；契約 3）：`stop_ratio` 等於該類別可計時路段的短停留總和除以移動時間總和，`speed_kmh` 是 `null` 時也是 `null`；以保留行程的代號建立配速表會被拒絕。餘裕係數的規則對固定的殘差清單給出固定的值；每一折重算分級門檻，被拿掉的那一趟算不出配速的折不計入，計入的折數少於 8 時是 0.20。配速表表頭的 `margin_coeff` 和同一批行程依規則算出的值相同；ETA 表頭的值等於所用配速表的值。`margin_basis` 只有 `loo_rule` 與 `default` 兩個值：`default` 時 `margin_coeff` 必為 0.20；`loo_rule` 時是 0.05 的倍數且不小於 0.05。`pace_version` 符合樣式（`research-` 或 `user-` 加兩位以上的數字） |
| S33 | ETA 的不變條件（SB2-T5、SB2-T6、SB2-T8；契約 4）：`stop_allow_s` 等於 `stop_ratio` 乘以 `typ_seg_time_s`；`eta_typ` 的逐段差等於 `typ_seg_time_s` 加 `stop_allow_s`，再加新排入的休息；`eta_safe` 減 `eta_typ` 等於 `margin_coeff` 乘以兩者的累計（容許 1 秒）。加入一筆休息後，`stop_allow_s` 與餘裕的秒數不變，兩個估計都只多出休息的長度。ETA 的狀態是 `unknown` 時，`stop_allow_s`、`eta_typ`、`eta_safe` 都是 `null` |
| S34 | 研究用與使用者的 Profile 分開（SB2-T10）：介面更新 Profile 只會產生 `user-` 版本的配速表，不改寫任何 `research-` 版本的檔案，也不改寫既有的 `user-` 版本：每次更新都是新的版本、新的檔案（`user-` 也不改寫已核准，2026-11-15，Q-4）。E1 與 E2 的腳本拒絕 `user-` 版本。產品選用的版本是 `built_at` 最晚的 `user-` 版本，沒有時用凍結清單指定的 `research-` 版本 |
| S35 | 快照的重用與失效（SB8-T1、SB8-T2、SB8-T3、SB8-T4）：同一個請求第二次規劃不呼叫引擎。以 31 天前取得的快照測試，一般模式重新取得：內容不同時存成新檔，內容相同時沿用舊檔、不產生新檔（S53）；兩種情形舊檔的內容都不變，Snapshot Mode 仍然可以使用舊檔。引擎失敗且只有過期快照時，一般模式回傳 `routing_unavailable`。回程的檢查沒通過時，去程也不存檔 |
| S36 | 快照不可變（SB8-T4a、SB8-T4b、SB8-T6）：以既有的代號寫入不同的內容會報錯，檔案不變。凍結清單的雜湊和檔案不符時 Runner 停止。同一份快照內容算出同一個 `snapshot_id`；雜湊範圍內的任何內容不同則不同（範圍不含 `snapshot_id` 與各方向的 `fetched_at`；S53、S54） |
| S37 | 代號與 `request_key`（SB8-T5、SB8-T7）：途經點順序對調得到不同的 `request_key`。所有代號符合第 2 節的樣式，`R01`／`R02` 仍然有效 |
| S38 | 去程、回程與折返點（SB8-T8、SB8-T9、SB8-T10）：來回路線的 `turnaround` 檢查點位於去程最後一段之後。回程的折線不是去程的反轉（以一條去回不同路的快照驗證）。回程的請求失敗時結果是路線錯誤，沒有里程與道路名稱 |
| S39 | 國道檢查（SB8-T10a、SB8-T11、SB8-T12、SB8-T13）：`has_highway` 是 `true`、道路屬性沒有國道的 fixture 判為 `fail`。道路屬性含 `motorway` 路段或國道名稱的 fixture 判為 `fail`。五條參考路線的 10 段都是 `pass`。道路屬性查詢失敗時結果是 `routing_unavailable`，沒有快照 |
| S40 | 偏移（SB8-T14、SB8-T15、SB8-T16、SB8-T16a）：終點偏移 6.8 km 的探測快照被拒收。五條參考路線都通過。詞彙表每個地標的偏移不超過 100 m。途經點離折線超過 200 m 的 fixture 被拒收，結果是 `routing_unavailable` |
| S41 | 預設休息與途經點的檢查點（SB8-T17、SB8-T18、SB8-T19、SB8-T20、SB8-T20c）：固定的路線與設定得到固定的休息清單。來回行程的折返點有一筆休息。行程描述寫了休息時不排預設休息。缺設定值時回傳追問。每個指定的途經點有一個 `kind = waypoint` 的檢查點，來回行程的去程與回程各一個；要求在途經點休息時，這筆休息在 `breaks` 裡，抵達時間含它。結果中沒有 `unplaced_breaks` 欄位。騎士明確要求的休息排不進去時的測試（原 SB8-T20a、SB8-T20b）已隨做法撤回，由 S46–S52 取代 |
| S42 | `ridden_share_pct`（SB8-T21、SB8-T22、SB8-T23、SB8-T24、SB8-T25）：和配速行程同一條路的路線不低於 95%。完全不相交的路線是 0。只在一個路口相交的路線是 0。反方向的路線得到相同的數值。只有保留行程騎過的路線是 0 |
| S43 | 目標路線 GPX（SB8-T26、SB8-T27）：SPEC-RESOLUTION-001 第 2.8 節的每一種情形各一個案例：讀不到軌跡點或只有一點、總長度不到 1 km、相鄰兩點相距超過 1 km（都是 `target_gpx_invalid`）；只有路線點、沒有時間的檔案可以使用；指定來回、終點回到起點而且明確去回同路時正常，騎士沒有指定折返位置時，折返點是離起點最遠的軌跡點（其他幾何與指定折返位置的情形見 S59–S64、S79、S80）；指定來回而終點沒有回到起點時是 `target_gpx_not_round_trip`；指定單向時幾何原樣使用。沒有指定行程型態時系統追問，不由幾何決定 |
| S44 | 規則 3 的範圍（SB9-T1、SB9-T2、SB9-T3、SB9-T4、SB9-T5）：來回行程中只有去程有高降雨機率提醒時是 PASS，並顯示 5.5 的去程提醒句子。範圍內有提醒時是 FAIL，即使範圍內另有路段缺預報。範圍內沒有提醒、有路段缺預報時是 UNKNOWN，原因代碼依 5.2 的固定順序。單向行程的結果和原本的最後 20% 定義相同。範圍以外的路段缺預報不影響結果 |
| S45 | 凍結之前的保留行程隔離與研究用配速表的完整性（SB2-T11、SB2-T12、SB2-T13）：凍結之前的重建流程（`ingest` 與配速表）遇到保留行程的代號會拒絕，不開啟檔案。E1、E2 的腳本執行前核對凍結清單記錄的研究用配速表檔案與衍生路段表的 SHA-256，不符就停止。凍結用的腳本遇到既有的 `research-` 版本時報錯，不覆寫 |
| S46 | 休息對到途經點（Q1-T1；依 Q-3 第 3 項的裁決改為單向行程或已指明方向的情形）：休息需求的地點是指定的途經點，行程是單向，或來回行程而且已指明方向時，結果的 `breaks` 有這一筆，`after_checkpoint_id` 是那個 `waypoint` 檢查點，`eta_typ` 含它的長度 |
| S47 | 休息對到折返點（Q1-T2）：來回行程、地點是折返點時，對到 `turnaround` 檢查點 |
| S48 | 對應不到（Q1-T3）：地點不是途經點也不是折返點時，回傳追問，選項依 4.1 規則第 3 項，沒有計畫 |
| S49 | 不安排這段休息（Q1-T4）：追問回覆「不安排這段休息」時，計畫中沒有這一筆，其他休息不受影響 |
| S50 | 行程型態未知（Q1-T5）：行程型態未知時要求在目的地休息，追問的選項沒有「折返點」 |
| S51 | 重新規劃不動使用者的休息（Q1-T6）：重新規劃的每一輪之後，`origin` 是 `free_text` 或 `clarification` 的休息都還在，檢查點與長度不變 |
| S52 | 沒有關鍵詞檢查（Q1-T7）：行程描述寫「不休息」「晚餐前回到家」而 Planner 沒有產生休息需求時，不追問，照常規劃 |
| S53 | 快照的重用（Q3-T1）：同一份內容、不同的取得時間得到同一個 `snapshot_id`，既有的檔案沒有被改寫 |
| S54 | 內容不同（Q3-T2）：折線或任何其他內容不同時是新的代號，舊檔的內容不變 |
| S55 | 不覆寫（Q3-T3）：以既有的代號寫入不同的內容會報錯 |
| S56 | 正規化的精度（Q3-T4）：經緯度第六位小數不同的兩份內容得到不同的雜湊；只有第七位以後不同的得到相同的雜湊 |
| S57 | 已保存結果的指向（Q3-T5）：重新取得並產生新快照之後，已保存結果的 `route_id` 與 `snapshot_id` 不變 |
| S58 | 代號的樣式（Q3-T6）：所有代號符合第 2 節的樣式 |
| S59 | 去回同路（Q3-T7）：去回同路的目標路線 GPX，騎士沒有指定折返位置時，自動取離起點最遠的軌跡點為折返點 |
| S60 | 環狀、沒有折返位置（Q3-T8）：環狀的目標路線 GPX 沒有指定折返位置時回傳 `target_gpx_not_round_trip`，沒有計畫 |
| S61 | 環狀、指定折返位置（Q3-T9）：環狀的目標路線 GPX 指定折返位置後，以那個位置切開 |
| S62 | 不合法的里程（Q3-T10）：指定的里程是 0、負數或超過總長時回報，沒有計畫 |
| S63 | 終點沒有回到起點（Q3-T11）：即使指定了折返位置也回傳 `target_gpx_not_round_trip` |
| S64 | 不反轉、不補造（Q3-T12）：任何情形下都沒有反轉或補造的軌跡點 |
| S65 | 寫明方向的休息（Q3-T13）：行程描述寫明「回程在某途經點休息」時，對到回程的 `waypoint` 檢查點 |
| S66 | 方向不明（Q3-T14）：來回行程、途經點的休息沒有方向時回傳追問，選項是去程、回程、不安排，沒有計畫 |
| S67 | 回覆方向（Q3-T15）：追問回覆「回程」後，對到回程的檢查點並計入 ETA |
| S68 | 途經點的偏移（Q3-T16）：途經點離折線超過 200 m 時拒收 |
| S69 | 途經點的順序（Q3-T17）：兩個途經點都在 200 m 內、但折線經過它們的順序和請求相反時拒收 |
| S70 | 公路的進入端（Q3-T18）：公路的進入端也有偏移紀錄（`via_offset_m`） |
| S71 | 被引用的地標改變（Q3-T19）：被引用地標的座標在第六位小數以內改變時 `request_key` 改變 |
| S72 | 未引用的地標改變（Q3-T20）：沒有被引用的地標改變時 `request_key` 不變 |
| S73 | 途經點對調（Q3-T21）：途經點的順序對調時 `request_key` 改變 |
| S74 | 凍結清單優先（Q3-T22）：有凍結清單時採用清單指定的快照，即使有取得時間更晚的快照 |
| S75 | 雜湊失敗（Q3-T23）：清單指定的檔案不存在或 SHA-256 不符時停止，沒有回退 |
| S76 | 檢查方法不相容（Q3-T24）：檢查方法不同的快照在兩種模式下都不採用 |
| S77 | 一般的 Snapshot Mode（Q3-T25）：取相容的快照中取得時間最晚的一個 |
| S78 | 目標路線 GPX 的 `route_id`（Q3-T26）：同一個檔案，自動判定的折返位置和騎士指定的折返位置相同（換算成公尺後相等）時 `route_id` 相同；折返位置不同時 `route_id` 不同；同一個檔案的單向與來回 `route_id` 不同 |
| S79 | 去回同路的自動辨識（Q3-T27；合成資料）：四種形狀各一個案例：去回同路（自動取最遠點）、環狀、8 字形、重合比例不足（例如去程與回程只有一部分同路）。後三種都不自動推定，沒有指定折返位置時回傳 `target_gpx_not_round_trip` |
| S80 | 指定優先於自動（Q3-T28）：明確去回同路的軌跡上，騎士指定了另一個合法的折返位置時，以騎士指定的為準 |
| S81 | `waypoint` 檢查點（Q3-T29）：同一個路段邊界同時有加油站與途經點時，加油站的編號在前；FuelPlan 的檢查點清單沒有 `waypoint` |
| S82 | 整趟不休息（Q3-T30）：`rest_policy = none` 時，結果沒有任何 `origin = rider_profile` 的休息 |
| S83 | 取消個別的休息（Q3-T31）：追問中取消了全部的個別休息需求、`rest_policy = default` 時，預設休息照常排入 |
| S84 | 重新規劃與加油停留（Q3-T32）：重新規劃之後，騎士指定的加油停留（`origin` 是 `free_text` 或 `clarification`）都還在，檢查點不變；系統安排的（`planner`、`replan`）可以被移除或更換 |
| S85 | 行程型態與方向同一輪（Q3-T33）：行程型態未知、又有途經點的休息時，同一次追問同時有行程型態與方向兩題；回覆單向時方向的答案不使用，回覆來回時依方向對應檢查點；沒有第二次追問 |
| S86 | 嚴格模式沒有對應的項目（Q3-T34）：凍結清單沒有這個請求的項目時停止，沒有採用任何其他快照 |
| D1–D16 | DESIGN §8 列出的排序與候選搜尋測試（目前 16 項）。CR-01：以 DESIGN.md 修訂後的清單為準；分批與 INCOMPLETE 的測試改為完整評估與評估失敗的測試 |

**`routes` 整合的驗收條件（RI-1 至 RI-3；2026-11-15 的裁決，處置第 9.10 節）。** Profile 更新後，既有的路線必須依新的門檻重新分類；無法重建時，不可混用舊的類別與新的配速。這三條是 `routes` 整合的驗收條件，不屬於第一批 Scoped Tickets（BATCH-1），也不擴張其中的 #10。尚未實作。

| 編號 | `routes` 整合的驗收條件 |
| --- | --- |
| RI-1 | 路線目錄的 `category_scheme` 和所用配速表的 `category_scheme` 不同時，不計算 ETA |
| RI-2 | 這時由路線的幾何（路線快照或目標路線 GPX）依新的門檻重新分類路段，重建路線目錄的紀錄後再計算 |
| RI-3 | 幾何取不到、無法重建時回報錯誤，不產生計畫；不得以舊的類別搭配新的配速 |

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
| SD-12 | 休息安排的 `origin` 沒有 `form` | G1 第 8 節寫「來自表單或自然語言」，但凍結的表單沒有休息欄位。休息來自自然語言、追問的回覆、Rider Profile 或重新規劃 | 維持，待審查。CR-01：行程描述沒寫休息時依 Rider Profile 排入。Q-1 的裁決（2026-11-15）：`origin` 用來區分使用者的約束（`free_text`、`clarification`）與系統排入的休息（`rider_profile`、`replan`）；重新規劃不得移除、搬移或縮短前者（4.1、4.9）。2026-11-15 的裁決（處置第 9.6、9.7 節）：規劃請求新增 `rest_policy`（SD-42）；RefuelStop 的 `origin` 以同樣的方式區分系統安排的與騎士指定的加油停留（SD-43） |
| SD-13 | `free_text` 沿用原名，意義擴大為行程描述 | CR-01 只要一個文字欄；不改名可以少動其他欄位 | CR-01 新增，待審查 |
| SD-14 | 新增 RouteRequest 與 PlaceRef；地點只以詞彙表或 Rider Profile 的代號表示 | CR-01 第 12 節的 Must（行程描述、詞彙表、追問）；D2 不得編造路線 | CR-01 新增，待審查 |
| SD-15 | 新增 RouteSummary。國道檢查的結果是 `freeway_check`，在非路線引擎的來源是 `null`；另有 `turnaround_checkpoint_id`，指向 `kind = turnaround` 的檢查點 | 結果要顯示里程、道路名稱與配速資料的涵蓋比例；加油安排要分得出去程與回程 | CR-01 新增，待審查。審查後把初稿的 `has_highway` 改名為 `freeway_check`（SD-26） |
| SD-16 | 新增 `route_error`、RouteError 與 `code`（CR-01 時五種，現在六種） | D2：路線服務失敗時必須有明確的錯誤處理 | CR-01 新增，待審查。第六種依 SPEC-RESOLUTION-001（2026-11-15 裁決）新增（SD-39）。lead 依 O-2 加的另一種（`break_not_placeable`）不採用（Q-1 的裁決；SD-40） |
| SD-17 | Evaluation 取代 SearchStatus；新增 `evaluation_failed` | CR-01 第 11 節「附條件接受」的兩個條件 | CR-01 新增，待審查 |
| SD-18 | 路線快照的來源型別是 `snapshot`，一般模式也一樣；Snapshot Mode 不呼叫路線引擎 | D2：Demo 與 E2 使用凍結的快照 | CR-01 新增，待審查 |
| SD-19 | 人工確認指引依規則編號與 `reason_class` 查表 | 不論 `reason_code` 是否延後，都查得到固定的指引 | CR-01 新增，待審查 |
| SD-20 | ReplanRound 新增 `change_summary`，是 `changes` 的顯示文字 | 介面的重新規劃紀錄要一段固定模板的文字。`changes`（Q29 的結構化變更摘要）維持必填，不由它取代 | CR-01 新增，待審查。初稿曾以它取代 `changes`，已改回 |
| SD-21 | Explanation 以 `planner_text` 與 `planner_text_status` 取代 `origin`；Rule5Attempt 的 `text_origin` 改為 `template`、`planner`、`final_output` | 固定模板優先之後，模板一定存在，Planner 的說明是附加的；重新產生已取消。`rule5_log` 維持必填（Q30） | CR-01 新增，待審查 |
| SD-22 | 追問主題的 `break_location` 併入 `other` | CR-01 的追問主題是起點、進入端、行程型態與休息長度 | CR-01 新增，待審查。Q-1 的裁決（2026-11-15）：騎士明確要求的休息對應不到地點時用 `other`，文字由主程式依固定模板產生，選項固定（4.2；SD-41）。Q-3 第 3 項的裁決（2026-11-15）：來回行程途經點的休息沒有方向時同樣用 `other` 追問，選項是去程、回程、不安排（4.1、4.2）。2026-11-15 的裁決（處置第 9.8 節）：行程型態和休息方向在同一輪追問；行程型態也在這一輪問的時候，方向的那一題標明「選擇來回時才需要回答」 |
| SD-23 | 提供目標路線 GPX 時路線以 GPX 為準 | 兩個路線來源同時出現時要有確定的結果 | CR-01 新增，待審查 |
| SD-24 | 5.5 的固定文字，以及「道路寫法必須出現在 `road_names`」的兩步檢查（7.7） | 路權提醒、配速資料的涵蓋比例與錯誤訊息都不由 LLM 產生 | CR-01 新增；文字是提案，待確認。SPEC-RESOLUTION-001（2026-11-15 裁決）之後修正了路權提醒與涵蓋比例的句子，並新增抵達時間的說明、預設的餘裕係數、去程的高降雨機率提醒與第六種路線錯誤的文字。O-2 的裁決（2026-11-15）之後：排不進去的休息的固定訊息隨 `unplaced_breaks` 撤回；lead 依 O-2 寫的錯誤文字經第二輪聚焦審查後也撤回。Q-1 的裁決（2026-11-15）之後新增追問的固定模板、固定選項與表單層級的固定訊息（5.5；提案，SD-41）。預設餘裕係數的句子改為和條件一致的說法。Q-3 的裁決（2026-11-15）之後：`target_gpx_not_round_trip` 增加「無法確認折返點」的一則文字，並新增休息方向追問的模板與選項（5.5；提案）。2026-11-15 的裁決（處置第 9.3、9.8 節）之後：無法確認折返點那一則的 `actions` 不指向特定的介面欄位；新增行程型態也在同一輪追問時的方向追問模板（5.5；提案） |
| SD-25 | 新增 RouteSnapshot 與 RouteLeg（4.14）：一條路線一個快照，`legs[]` 逐方向記錄請求、折線、警告、`has_highway`、`freeway_check` 與方法、`endpoint_offset_m`、`via_offset_m`、取得時間 | CR-01 審查後的處置 L-3、L-4：路線快照的欄位由這份 Spec 定義；回程另送請求，不反轉折線 | 審查後新增，待審查。SPEC-RESOLUTION-001（2026-11-15 裁決）：快照不可變（SD-34）、新增 `via_offset_m`（SD-35）、移除高度欄位（SD-38）；三項已由 Q-3 第 1、4、7 項的裁決處理（2026-11-15） |
| SD-26 | RouteSummary 以 `freeway_check` 表示國道檢查的結果；引擎回報的 `has_highway` 記在路線快照。新增 `leg_length_diff_pct` 與 `leg_length_diff_flag` | 不讓同一個名稱有兩種意義；去回里程差超過 2% 時要在路線摘要標示（L-3） | 審查後新增，待審查。SPEC-RESOLUTION-001（2026-11-15 裁決；修正 B、F）：`has_highway` 是國道檢查的訊號之一，是 `true` 時不採用；這項檢查不稱為道路主管機關資料的獨立驗證 |
| SD-27 | `request_key` 與快照的比對；一般模式重用 30 天內的快照，不改用已失效的快照；回應因為警告、偏移或國道檢查無法驗證而不採用時，歸在 `routing_unavailable` | Snapshot Mode 要能確定地找到快照；路線服務失敗時要有明確的錯誤（D2）；公開伺服器只能低頻使用 | 審查後新增。警告的處理已由 P-1 裁決（7.11 第 7 項）。`request_key` 的組成、30 天的重用與歸類已定（SPEC-RESOLUTION-001 第 2.1、2.2、2.4、2.5 節，2026-11-15 裁決）。聚焦審查後的兩項修正已由 Q-3 的裁決處理（2026-11-15；處置第 8.5、8.6 節）：`request_key` 不用詞彙表的版本，每個地點帶上地標座標定義的指紋，取前 16 碼（第 5 項，有條件批准；7.11 第 4 項）；Snapshot Mode 分成一般模式與嚴格模式，兩種都比對檢查方法，嚴格模式只用凍結清單指定的快照、不回退（第 6 項，修改；7.11 第 3 項）。有國道的訊號時優先回 `highway_in_route`（7.11 第 5 項）。2026-11-15 的裁決（處置第 9.9、9.10 節）：嚴格模式下凍結清單沒有對應的 `request_key` 或 `snapshot_id` 時也停止；超過 30 天後可能重複向路線引擎查詢是 MVP 的已知限制 |
| SD-28 | `ridden_share_pct` 的算法（7.11 第 10 項）：只和配速行程的幾何比對，不分方向，來回行程分方向比對再合計；取樣點 50 m 內算接近，連續接近的取樣點少於 3 個的片段不算 | DESIGN 與 Spec 原本互相把算法推給對方；保留行程不進配速表，所以不參與比對 | 已定（審查處置的修正 1；SPEC-RESOLUTION-001 第 2.7 節，2026-11-15 裁決；修正 G）：只比對配速行程；門檻是 50 m 與 3 個取樣點（裁決寫的 300 m，聚焦審查後改以點數定義）；數值只表示幾何接近，不保證走過同一條道路。介面名稱是「配速資料中的路線涵蓋比例」 |
| SD-29 | 預設休息的排入規則由這份 Spec 定義（7.11 第 9 項） | 同上；休息安排是 Plan Schema 的欄位 | 已定（SPEC-RESOLUTION-001 第 2.6 節，2026-11-15 裁決）：預設 90／15 分鐘，可在 Rider Profile 修改；排入的位置與順序見 7.11 第 9 項。騎士明確要求的休息已依 Q-1 的裁決定案（2026-11-15），見 SD-40 與 SD-41 |
| SD-30 | ID 的確切格式（第 2 節；7.11 第 1 項）：`route_id` 的三種樣式、`checkpoint_id` 與 `snapshot_id` | P-3 裁決：Spec 凍結前定義，不留給 Tickets；`trip_id` 與 `R01`／`R02` 不變 | 已定（SPEC-RESOLUTION-001 第 2.2 節，2026-11-15 裁決）。`snapshot_id` 取自正規化後的快照內容（SD-34）。聚焦審查後補上：雜湊一律用 SHA-256，`RG-` 的雜湊加入 `trip_type`，正規化規則寫在第 2 節。Q-3 第 1 項的裁決（2026-11-15，有條件批准；處置第 8.1 節）：格式接受；雜湊的範圍不含 `snapshot_id` 與各方向的 `fetched_at`（lead 寫定）；經緯度正規化為小數六位。2026-11-15 的裁決（處置第 9.1 節）：`RG-` 的雜湊含實際採用的折返位置（距起點的累計公尺，取整數），不論它是自動判定還是騎士指定的。SB-1 是 CLOSED（11.1） |
| SD-31 | 行程描述的本機輸入保護（7.12）與它的固定訊息（5.5） | 審查處置的修正 2：不得只靠提示語 | 審查處置後新增；草案，待確認（SB-6） |
| SD-32 | 路段對應鄉鎮與預報時段的規則（7.13）；WeatherSegment 新增三個預報時段的欄位；新增 `R3_AREA_UNMAPPED` 與 `EV-AREA` | P-4 裁決與審查處置的修正 4 | 審查處置後新增；草案，待確認（SB-3、SB-4） |
| SD-33 | 目標路線 GPX 的來回條件（7.11 第 2 項） | 審查處置的修正 3；SPEC-RESOLUTION-001 修正 E | 已定（SPEC-RESOLUTION-001 第 2.8 節，2026-11-15 裁決）：GPX 的終點回到起點才能當成來回；錯誤代碼是 `target_gpx_not_round_trip`（SD-39）。Q-3 第 2 項的裁決（2026-11-15，修改；處置第 8.2 節）：只有明確去回同路時自動取離起點最遠的軌跡點為折返點；有歧義時騎士可以指定折返位置（RouteRequest 新增 `target_gpx_turnaround_km`，4.1），無法確認時回傳 `target_gpx_not_round_trip`。先前「不接受折返位置、一律取最遠點」的寫法作廢。2026-11-15 的裁決（處置第 9.2–9.4 節）：50 m／100 m／90% 是自動辨識的保守啟發式門檻，沒有以真實資料驗證過；折返位置以距起點的公里數輸入，先由 CLI 支援，介面上選填的欄位是 Should；騎士指定的合法折返位置優先於自動判定。欄位名稱是 lead 定的。SB-7 是 CLOSED（11.1） |
| SD-34 | 路線快照不可變；`snapshot_id` 取自正規化後的快照內容（不含 `snapshot_id` 本身與各方向的 `fetched_at`）：內容完全相同就沿用既有的檔案，內容不同才是新的快照與新的 `route_id`；E2 與 Demo 的凍結清單記錄檔案的 SHA-256 | 修正 A：重新取得資料不得覆寫 E2 已凍結的快照。不另建版本管理 | SPEC-RESOLUTION-001（2026-11-15 裁決；修正 A）。Q-3 第 1 項（有條件批准）與第 6 項（修改）的裁決（2026-11-15；處置第 8.1、8.6 節）：先前「每一次取得都是新的代號」的寫法作廢；凍結清單記錄檔案的雜湊，嚴格模式核對。雜湊不含取得時間是 lead 寫定，已由 2026-11-15 的裁決保留（處置第 9.10 節） |
| SD-35 | RouteLeg 新增 `via_offset_m` | 修正 C：起點、終點與每個指定的途經點都要檢查偏移 | SPEC-RESOLUTION-001（2026-11-15 裁決；修正 C）。Q-3 第 4 項的裁決批准（2026-11-15；處置第 8.4 節）：欄位涵蓋送給引擎的每一個中間位置，包含公路的進入端；另加途經點順序的檢查（7.11 第 8 項），判定方式是 lead 寫定 |
| SD-36 | **撤回（2026-11-15，O-2 的裁決之後）。** 原本的決定：PlanRequest 新增 `unplaced_breaks` 與 UnplacedBreak（4.1），`reason` 的兩個值是這份 Spec 定的 | 修正 D：騎士明確要求的休息排不進去時必須回報，不能默默省略 | 欄位、`reason` 與固定訊息都已刪除，不採用。取代它的做法已依 Q-1 的裁決定案（2026-11-15；SD-40、SD-41）：對應不到的休息以追問回報，結果中不另外列出。推導細節 4（SPEC-RESOLUTION-001 第 8 節第 4 點）的三個版本列在處置第 6.3 節與 `q3_derived_details.md`（裁決之前的清單）；Q-3 第 3 項的裁決見 SD-40 |
| SD-37 | WeatherSegment 的範圍欄位改名為 `in_rule3_range`（原名 `in_last_20pct`），單向與來回共用；規則 3 的兩個原因代碼改名為 `R3_NO_ALERT_IN_RANGE` 與 `R3_ALERT_IN_RANGE` | 方案 A：來回行程檢查整段回程，欄位不能再只表示最後 20%。代碼還沒有凍結，改名不違反 P-9 | SPEC-RESOLUTION-001 第 3.5 節（2026-11-15 裁決） |
| SD-38 | RouteLeg 移除高度欄位 `elevation_m`；不向引擎要求高度值 | 方案 A 不需要高度 | SPEC-RESOLUTION-001 第 3.5 節。Q-3 第 7 項的裁決批准移除（2026-11-15；處置第 8.7 節） |
| SD-39 | RouteError 新增第六個 `code`：`target_gpx_not_round_trip` | 修正 E：目標路線 GPX 的來回行程必須確實包含回到起點的幾何 | 已批准（SPEC-RESOLUTION-001 第 2.8 節，2026-11-15 裁決）。Q-3 第 2 項的裁決（2026-11-15）：無法確認折返點時也用這個代碼，不新增代碼 |
| SD-40 | 指定的途經點建立 `kind = waypoint` 的檢查點（4.1、4.7、7.11 第 2、9 項）。騎士明確要求的休息：Planner 先產生休息需求；對應不到時由主程式以追問回報，追問之後仍然對應不到時不產生計畫；對應到的休息由主程式寫入 `breaks` 並計入 ETA；重新規劃不得移除、搬移或縮短（4.1 的十項規則） | O-2 的裁決只有三點：途經點建立為 `waypoint` 檢查點；無法安排時由確定性的程式回報，不依賴語言模型；沒有把指定的休息納入 ETA 的計畫不得作為有效的計畫。Q-1 的裁決定了後兩點的做法 | 2026-11-15，O-2 與 Q-1 的裁決（Q-1 有條件批准；處置第 7.1 節）。途經點的檢查點是 O-2 裁決的內容。十項規則中，第 3、4 項是 lead 依 Q-1 的裁決寫定的做法，已由 Q-3 第 3 項的裁決接受（2026-11-15；處置第 8.3 節）；第 5 項改為依方向對應，先前「一律排在去程」的做法作廢；其餘是 Q-1 的裁決。lead 先前依 O-2 定的做法（兩項確定性檢查、關鍵詞清單、歸在 `route_error`、新增 `code` `break_not_placeable` 與固定文字）不採用；路線錯誤代碼是六個。2026-11-15 的裁決（處置第 9.5 節）：檢查點依行經的順序編號，同一個位置加油站在前；`waypoint` 不當作 `fuel_station`，也不列入 FuelPlan 的檢查點 |
| SD-41 | 新增 BreakRequest（休息需求；4.1）：`place`、`direction`、`duration_s`、`source_text`、`origin`。它是 Planner 交給主程式的中間資料，不是 PlanResult 的欄位。另有追問的固定模板、固定選項與表單層級的固定訊息（4.2、5.5） | Q-1 的裁決：Planner 先產生地點與長度的結構化休息需求，路線建立後由確定性的程式對應檢查點；無法對應時回報，不得默默省略 | Q-1 的裁決之後新增（2026-11-15）。休息需求與它的四項內容是裁決要求的；欄位名稱、固定值 `turnaround` 與「不放進 PlanResult」是這份 Spec 定的，固定文字是提案，待確認。`direction` 依 Q-3 第 3 項的裁決新增（2026-11-15），欄位名稱是 lead 定的；方向追問的模板與選項是提案 |
| SD-42 | PlanRequest 新增 `rest_policy`（`default`／`none`；4.1） | 兩種「不休息」的意圖要在結構化的條件中區分，不用關鍵詞猜測：騎士明確選擇整趟不安排休息，和在追問中取消個別的休息需求 | 2026-11-15 的裁決之後新增（處置第 9.6 節）。`none` 時不套用 Rider Profile 的預設休息；追問中的「不安排這段休息」不改變它；`default` 而且沒有任何休息安排時，預設休息照常套用（7.11 第 9 項）。欄位名稱是 lead 定的 |
| SD-43 | RefuelStop 的 `origin` 由兩個值增為四個：`planner`、`replan`（系統安排的）與 `free_text`、`clarification`（騎士指定的） | 重新規劃可以調整系統安排的加油停留，包含第一次規劃排的；騎士指定的必須保留 | 2026-11-15 的裁決之後新增（處置第 9.7 節）。重新規劃不得移除或搬移後兩種（4.1、4.9、7.8） |

## 11. 裁決、Spec Blockers 與待審查的事項

### 11.1 P-1 至 P-11 的裁決與尚未解決的 Spec Blockers

專題負責人在 2026-11-15 的審查處置中對 P-1 至 P-11 作出裁決，並提出五項修正；**這份 Spec 的凍結尚未批准**。完整的紀錄在 [CR-01](../cr/CR-01-proposal-alignment.md) 第 18 節。編號沿用 [lead 的處置](../cr/CR-01-appendix/lead_dispositions.md)第 3 節；G1 第 11 節與 UI_CR01_DELTA 都指向這一節，DESIGN.md §13.5 以同樣的編號列出同一批裁決。lead 先前的建議和裁決不同的地方，以裁決為準。年份都是 2026。

| 編號 | 事項 | 裁決 | 對這份 Spec 的影響 |
| --- | --- | --- | --- |
| P-1 | 路線參數 | 採 `use_highways: 0`，每個方向另做獨立的國道檢查，通過才採用。不送出硬性排除；回應出現任何警告就不採用。要記錄的限制：這個設定可能連快速公路也避開，平面轉場較慢 | 4.12、4.13、4.14、7.11 第 7 項 |
| P-2 | 停等寬放 | 升為 Must。先處理 `ingest` 的假停留；寬放只用配速資料決定；不得和既有的安全餘裕重複計算；需要改契約時明確提出 | 5.4、5.5；Plan Schema 沒有新增欄位。SB-2 已裁決（模型 M2），契約 1、3、4 的欄位見 DESIGN §5 |
| P-3 | `route_id`、`checkpoint_id`、`snapshot_id` 的格式 | 確切格式在 Spec 凍結前定義，不延到 Tickets 才決定。既有的 `trip_id` 與 `R01`／`R02` 不變 | 第 2 節、7.11 第 1 項（已定；SB-1） |
| P-4 | 路段對應鄉鎮的資料來源 | 採用國土測繪中心的鄉鎮界線，在本機把路段對應到氣象署的鄉鎮預報。跨鄉鎮、對應失敗與 PoP 預報時間窗的處理要明確定義 | 4.8、5.2、第 6 節、7.13（草案，SB-3） |
| P-5 | 保留行程與 E2 Oracle 的先後 | 先凍結 E1／E2 的分析方法與模型設定，再由隔離的評估腳本使用保留行程。禁止依保留行程的結果調整模型或規則 | 7.9；不影響欄位 |
| P-6 | E1 的路線引擎 ETA | 只在公開地標之間、時間定義相容的路段比較；不宣稱整趟的比較 | 不影響欄位 |
| P-7 | 2026-11-14 被排除的那一趟 | 維持排除 | 不影響欄位；7.11 第 10 項的比對範圍不含這一趟 |
| P-8 | 規則 3 在來回行程上的範圍（D3） | 暫不選曲率或固定高度的定義。lead 在 11/27 前提出有固定規則、可重現、符合研究目標的最小方案，再由專題負責人定案 | 4.8、5.2、5.4（已定：方案 A，SB-9） |
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

註（2026-11-15 聚焦審查後補上）：修正 3 的「明確提供折返點」已由 SPEC-RESOLUTION-001 的修正 E 取代。修正 E 的原文是「只指定折返點不足以證明有回程」：目標路線 GPX 本身回到起點才算來回行程。Q-3 第 2 項的裁決（2026-11-15；處置第 8.2 節）：只有明確去回同路時自動決定折返點，有歧義時騎士可以指定軌跡上的折返位置；先前「不接受折返位置」的寫法作廢（7.11 第 2 項）。P-1 一列的「獨立的國道檢查」是裁決的原文，意思是這項檢查不依賴路線的偏好參數，也不依賴引擎的單一旗標；它用的是同一份圖資，不是獨立的權威驗證（7.11 第 5 項）。

**Spec Blockers 的狀態（Q-3 後續九項裁決之後，2026-11-15）。** 下表是專題負責人裁決 Q-3 後續九項（A、B1–B3、C1–C5）之後的狀態：SB-1、SB-7、SB-8 三列取自 [lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 9.11 節，其餘七列和先前的表相同；它取代同一份文件第 5.7、7.6、8.8 節的表與第 6.5 節的說明。DESIGN.md §13.5、SPEC-RESOLUTION-001 第 5 節與 [CR-01](../cr/CR-01-proposal-alignment.md) 第 24 節有同一張表；CR-01 第 23 節與更早的 Blocker 表由它取代。標準（處置第 8.8 節）：規格與測試都寫定，而且沒有需要專題負責人確認的事項，才標記 CLOSED。SB-1、SB-2、SB-7、SB-8 與 SB-9 五項是 CLOSED；SB-3、SB-4、SB-5、SB-6、SB-10 沒有變更。沒有標記 CLOSED 的項目仍然擋住這份 Spec 的凍結。凍結之前不建立 Tickets，例外只有 2026-11-15 核准的第一批 Scoped Tickets（Q-5）：只限 `ingest`、契約 1／3／4、`pace` 與規則 3 的確定性測試，清單在 [docs/ticket/BATCH-1-scoped-tickets.md](../ticket/BATCH-1-scoped-tickets.md)；除了這一批之外，凍結之前不建立其他 Tickets。**這份 Spec 的凍結尚未批准**，完整的 Spec Freeze 沒有宣告。表中的 Q3-T 是處置第 8、9 節的測試編號（第 9 節的 S53–S86）；Q-4 指處置第 7 節的裁決；RI-1 至 RI-3 是 `routes` 整合的驗收條件（第 9 節），不屬於第一批 Scoped Tickets。七項與後續九項的裁決與定案內容在處置第 8、9 節；[q3_derived_details.md](../cr/CR-01-appendix/q3_derived_details.md) 是裁決之前供逐項裁決用的原文。

| 編號 | 狀態 | 說明 |
| --- | --- | --- |
| SB-1 ID 格式 | **CLOSED** | 格式、雜湊的範圍與正規化、重用與不覆寫的規則、已保存結果的指向、目標 GPX 的 `route_id` 含實際採用的折返位置，都已裁決並寫定；測試是 Q3-T1 至 T6、T26 |
| SB-2 停等寬放 | **CLOSED** | 定義、算式、留一趟的程序（含分級門檻的規則）、契約 1／3／4 的欄位與不變條件、測試都已寫定；Profile 的版本做法已核准（Q-4） |
| SB-3 路段對應鄉鎮 | 未解決 | 界線資料的版本與授權條款；鄉鎮和氣象署預報地點的對照（C3） |
| SB-4 預報時段欄位 | 未解決 | 氣象署實際回應的時段長度與涵蓋區間（C3） |
| SB-5 C3 真實 API 驗證 | **BLOCKED／NOT RUN** | Anthropic 憑證與氣象署授權碼 |
| SB-6 行程描述的輸入保護 | 未解決 | UI-0 需要的部分已確認（2026-11-15）：門牌偵測的方向與驗收案例、命中時的訊息、欄位下方的說明。確切的正規表示式留給實作的 Ticket；SPEC-001 7.12 的其餘各項仍待審查 |
| SB-7 目標 GPX 的來回條件 | **CLOSED** | 來回的條件、自動辨識的門檻（保守的啟發式，沒有以真實資料驗證）、折返位置的輸入與優先順序、不反轉不補造，都已裁決並寫定；測試是 Q3-T7 至 T12、T27、T28 |
| SB-8 7.11 待定項目 | **CLOSED** | 快照的重用與嚴格模式、國道檢查、偏移與順序、`request_key`、預設休息與指定休息、`waypoint` 檢查點、加油停留的來源，都已裁決並寫定；測試是 Q3-T13 至 T25、T29 至 T34。Profile 更新後的路線重新分類列為 `routes` 整合的驗收條件（RI-1 至 RI-3） |
| SB-9 規則 3 的範圍 | **CLOSED** | 方案 A |
| SB-10 尚未逐項審查的內容 | 未解決 | UI-0 決策對照表的 22 項已確認（2026-11-15）。SPEC-001 第 10 節、第 11.2 節，以及 5.5 中不在對照表內的文字仍待審查 |

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
| OQ-9 | 規則 3 在來回行程上的範圍（CR-01 D3） | **已裁決（SPEC-RESOLUTION-001，2026-11-15）：方案 A。** 來回行程檢查折返點之後的全部回程；單向行程維持最後 20%。欄位是 `in_rule3_range`（4.8），判定條件在 5.2，設定在 5.4；天氣表分成去程與回程（UI_CR01_DELTA 第 10 節） |
| OQ-10 | 停等寬放（CR-01 第 15 節；C2 是 FAIL） | **已裁決（P-2 升為 Must；SPEC-RESOLUTION-001，2026-11-15：模型 M2）。** 每個路段類別一個 `stop_ratio`；契約 1、3、4 各新增欄位，算式在 DESIGN §6.1。Plan Schema 沒有新增欄位；介面只在抵達時間旁加一句固定文字（5.4、5.5） |
| OQ-11 | 2026-11-14 被排除的那一趟行程要不要納入（CR-01 第 13 節） | **已裁決：維持排除（P-7）。** |
| OQ-12 | 目標路線 GPX 是單向的幾何時，要不要自動補上回程 | **已定案：不補，也不由幾何推定來回**（審查處置的修正 3）。SPEC-RESOLUTION-001（2026-11-15 裁決；修正 E）：GPX 的終點回到起點才能當成來回，只指定折返點不足以證明有回程；否則回傳 `target_gpx_not_round_trip`（7.11 第 2 項）。Q-3 第 2 項的裁決（2026-11-15；處置第 8.2 節）：明確去回同路時自動取離起點最遠的軌跡點為折返點；有歧義時騎士可以指定折返位置（距起點的公里數），無法確認時回傳 `target_gpx_not_round_trip`；不反轉，也不補造回程。2026-11-15 的裁決（處置第 9.2–9.4 節）：自動辨識的門檻是保守的啟發式，沒有以真實資料驗證過；折返位置以距起點的公里數輸入，先由 CLI 支援；騎士指定的合法折返位置優先於自動判定 |
| OQ-13 | 行程型態在表單上是不是必選 | 暫定選填：有選時以表單為準；沒選時由行程描述判斷，再沒有就追問 |
| OQ-14 | 公路與地標詞彙表要不要列為來源證據 | 暫定不列：它是知識庫的內容，出處以 Citation 表示 |
| OQ-15 | 5.5 的固定文字是否接受 | 提案如 5.5 |
| OQ-16 | 7.11 原本沒有定案的項目 | **已定案（SPEC-RESOLUTION-001，2026-11-15 裁決）。** 第 1–10 項已寫回 7.11，沒有留給 Tickets。由裁決推導的七項細節已由專題負責人逐項裁決（2026-11-15，Q-3；處置第 8 節）並寫回 7.11；標示「lead 寫定」的部分見各項的狀態欄。第 9 項中，騎士明確要求的休息已依 Q-1 的裁決定案，並依 Q-3 第 3 項的裁決修改（2026-11-15；4.1）。Q-3 後續的九項也已裁決（2026-11-15；處置第 9 節）並寫回 4.1、4.2、4.7、4.9、7.8 與 7.11。SB-8 是 CLOSED（11.1） |

CR-01 技術檢查的現況：C1（曲率一致性）是 PASS；C2（整趟誤差）是 FAIL；C3（LLM 與氣象署）是 BLOCKED／NOT RUN；C4（路線快照）是 FAIL，因為公開伺服器忽略硬性排除；追加的 C4b（軟性偏好）是 PASS。C1、C4、C4b 已有結果，剩下 C3。路線參數（P-1）與停等寬放（P-2；模型 M2）已裁決。這些是技術檢查，不是 E1 Lite 或 E2 的結果。路線服務不可用時，騎士可以改以目標路線 GPX 提供路線；RouteSummary 已經涵蓋這個來源。

## 12. 之後的步驟

1. C3 仍是 BLOCKED／NOT RUN，要等 Anthropic 憑證與氣象署授權碼。真實 API 驗證完成之前維持這個狀態，不以模擬結果代替。
2. SPEC-RESOLUTION-001 已在 2026-11-15 裁決並同步到這份 Spec（停等寬放、7.11 第 1–10 項、目標路線 GPX 的來回條件、規則 3 在來回行程上的範圍）。聚焦審查後的修正也已同步。O-1 至 O-6 已在 2026-11-15 裁決並同步（[lead 的處置](../cr/CR-01-appendix/lead_dispositions_resolution.md)第 5 節）：O-1 至 O-5 定案，O-6 的四項推導細節沒有批准。第二輪聚焦審查後的修正（處置第 6 節的 G-1 至 G-22）也已同步；lead 依 O-2 定的做法已撤回。Q-1 至 Q-5 已在 2026-11-15 裁決並同步（處置第 7 節）：Q-1、Q-2、Q-4、Q-5 定案，Q-3 當時沒有批准。Q-3 的七項已在 2026-11-15 逐項裁決並同步（處置第 8 節）。Q-3 後續的九項與兩件附帶的事已在 2026-11-15 裁決並同步（處置第 9 節）。Spec Blockers 的現況列在第 11.1 節：SB-1、SB-2、SB-7、SB-8 與 SB-9 是 CLOSED；剩下的 Blockers 是 SB-3、SB-4、SB-5、SB-6 與 SB-10，解決之前不凍結。除了第一批 Scoped Tickets（Q-5；11.1）之外，凍結之前不建立其他 Tickets。
3. 專題負責人審查第 10 節、第 11.2 節、標為「草案」或「提案」的內容，以及標明「lead 寫定」的細節。處置第 6.4 節的 Q-1 至 Q-5 已裁決（處置第 7 節）。Q-3 的七項也已逐項裁決（處置第 8 節）。Q-3 後續的九項也已裁決（處置第 9 節）。還需要專題負責人確認的是 SB-6、SB-10 中會擋住第一張 Streamlit Ticket（UI-0）的固定文字與操作流程，整理在 `docs/cr/CR-01-appendix/ui0_decision_table.md`（由 lead 撰寫；CR-01 第 24 節）。
4. Blockers 解決後，由專題負責人決定是否凍結這份 Spec。**凍結尚未批准。** 完整的 Spec Freeze 沒有宣告；第 11.1 節沒有標記 CLOSED 的 Blockers 解決之前不宣告。
5. 凍結之後才建立 Tickets，例外只有 2026-11-15 核准的第一批 Scoped Tickets（Q-5）：只限 `ingest`、契約 1／3／4、`pace` 與規則 3 的確定性測試，清單在 [docs/ticket/BATCH-1-scoped-tickets.md](../ticket/BATCH-1-scoped-tickets.md)。每張 Ticket 要有明確的規格依據、測試條件與排除範圍，不得決定尚未裁決的路線或 E2 問題。除了這一批之外，凍結之前不建立其他 Tickets。路線模組、資料工具、Planner、Validator 與 Streamlit 的正式實作在 Tickets 之後。
