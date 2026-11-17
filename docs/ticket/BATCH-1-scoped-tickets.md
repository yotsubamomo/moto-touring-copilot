# 第一批 Scoped Tickets（索引）

> 日期：2026-11-15。狀態：**五張 Ticket 已在 GitHub 建立（2026-11-15），都是 OPEN，還沒有開始實作。** Ticket 的內容以 GitHub 上的為準；這份文件是索引與當時的草稿。
>
> | 編號 | Issue | 標題 | 依賴 | 狀態 |
> | --- | --- | --- | --- | --- |
> | B1-1 | [#7](https://github.com/yotsubamomo/moto-touring-copilot/issues/7) | contracts：契約 1、3、4 的 v0.3 欄位與不變條件 | 無 | OPEN |
> | B1-2 | [#9](https://github.com/yotsubamomo/moto-touring-copilot/issues/9) | ingest：停等事件與三種分類 | #7 | OPEN |
> | B1-3 | [#10](https://github.com/yotsubamomo/moto-touring-copilot/issues/10) | pace：配速表的停等比例、分級門檻、餘裕係數與版本 | #7、#9 | OPEN |
> | B1-4 | [#11](https://github.com/yotsubamomo/moto-touring-copilot/issues/11) | pace：ETA 的停等寬放與安全餘裕 | #7、#10 | OPEN |
> | B1-5 | [#8](https://github.com/yotsubamomo/moto-touring-copilot/issues/8) | 規則 3 的範圍判定（確定性測試） | 無 | OPEN |
>
> 依據：專題負責人 2026-11-15 的裁決 Q-5（[lead_dispositions_resolution.md](../cr/CR-01-appendix/lead_dispositions_resolution.md) 第 7.4 節）：在完整的 Spec Freeze 之前可以先建立 Scoped Tickets，第一批只限已定案的 `ingest`、契約 1／3／4、`pace` 與規則 3 的確定性測試。
> 每張 Ticket 都有規格依據、驗收條件與排除範圍。排除範圍內的事不在 Ticket 裡決定；遇到規格沒有寫的事，停下來回報，不自行補上。
> SPEC-001 還沒有凍結；C3 是 BLOCKED／NOT RUN。這一批不碰路線（`routing`、`routes`）、E2、Planner、資料工具與 Streamlit。

文件代號：DESIGN ＝ `DESIGN.md`；RES ＝ `docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md`；SPEC ＝ `docs/spec/SPEC-001-plan-schema.md`；處置 ＝ `docs/cr/CR-01-appendix/lead_dispositions_resolution.md`。測試代號 SB2-T*、SB9-T* 定義在 RES 1.6 與 3.5。

## 1. 共通規則

- 測試只用合成資料與既有的測試 fixture。不讀取、不列出、不搜尋 `data/`；不以真實的 GPX 執行。
- 不讀取保留行程。任何流程遇到保留行程或被排除行程的代號都要拒絕。
- 不改動這一批以外的契約與欄位：契約 2、ID 的樣式（`route_id`、`checkpoint_id`、`snapshot_id`）、路線快照、Plan Schema 都不動。
- 既有的 100 個測試在每張 Ticket 完成後都要通過；因為契約改版而必須修改的測試，在 Ticket 中列出修改的理由。
- 不執行 E1 或 E2，也不把任何測試或檢查的數字稱為 E1／E2 的結果。
- `ETA_safe` 不稱為 P90 或分位數。

## 2. 依賴關係

```text
B1-1 contracts ──► B1-2 ingest ──► B1-3 pace 配速表 ──► B1-4 pace ETA
B1-5 規則 3 的範圍判定（不依賴其他 Ticket）
```

## 3. Tickets

### B1-1 `contracts`：契約 1、3、4 的 v0.3 欄位與不變條件

| 項目 | 內容 |
| --- | --- |
| 規格依據 | DESIGN §5（契約 1、契約 3、契約 4 的欄位表與不變條件）；RES 1.4；處置 5.3、7.3 |
| 範圍 | `src/moto_copilot/contracts/schemas.py` 與 `validate.py`：契約 1 新增 `short_stop_time_s`；契約 3 的類別紀錄新增 `stop_ratio`，表頭新增 `margin_coeff`、`margin_basis`，`pace_version` 的樣式改為 `research-` 或 `user-` 加兩位以上的數字；契約 4 的路段列新增 `stop_allow_s`，表頭的 `margin_coeff` 下限改為 0.05。對應的不變條件寫進 `validate.py`。更新測試 fixture 中不符合新樣式的 `pace_version` |
| 驗收條件 | (1) `short_stop_time_s ≤ stopped_time_s`，違反時被拒絕（SB2-T3 的契約部分）。(2) `speed_kmh` 為 null 時 `stop_ratio` 必為 null，否則必有值（SB2-T4 的契約部分）。(3) `margin_basis` 只接受 `loo_rule` 與 `default`；`default` 時 `margin_coeff` 必為 0.20；`loo_rule` 時是 0.05 的倍數且不小於 0.05；`pace_version` 不符合樣式時被拒絕（SB2-T9 的契約部分）。(4) ETA 輸出的不變條件：`stop_allow_s = stop_ratio × typ_seg_time_s`、`eta_typ` 與 `eta_safe` 的算式、狀態為 `unknown` 時三者為 null（SB2-T5、T8，容許 1 秒）。(5) 同時提供配速表與 ETA 輸出時，ETA 表頭的 `margin_coeff` 必須等於配速表表頭的值 |
| 排除範圍 | ID 樣式的放寬（契約 1、2、4 都有；屬於待裁決的 Q-3 第 1 項）；契約 2 的任何欄位（`trip_type`、`turnaround`、`waypoint`）；路線快照；Plan Schema。`validate.py` 不重算配速或餘裕係數：「表頭的值等於依規則重算的值」由 B1-3 的測試檢查 |
| 依賴 | 無 |

### B1-2 `ingest`：停等事件與三種分類

| 項目 | 內容 |
| --- | --- |
| 規格依據 | RES 1.1（各種時間的定義）；DESIGN §6.1、§5 契約 1；處置 6.1 的 F-4（只處理配速行程的防線） |
| 範圍 | `src/moto_copilot/ingest/segments.py`：把連續的停止步合成停等事件；不到 3 秒的事件（疑似 GPS 假停留）計入移動時間，不加里程；3 秒以上、不到 180 秒的計入 `short_stop_time_s`；`stopped_time_s` 是 3 秒以上事件的總和。兩個門檻是 `ingest` 的參數。換新的 `ingest_version`。凍結之前的重建流程只處理配速行程：遇到保留行程或被排除行程的代號時拒絕，不開啟檔案 |
| 驗收條件 | SB2-T1（1 秒的重複位置不算停留）；SB2-T2（2、3、179、180 秒的邊界）；SB2-T3（每個路段 `short_stop_time_s ≤ stopped_time_s`；移動時間加停留時間等於修剪後的總歷時）；SB2-T11（遇到保留行程的代號時拒絕）。都以合成軌跡測試 |
| 排除範圍 | 曲率與分級的算法；目標 GPX 的讀取（沒有時間的路線點）；歷史 GPX 的多檔上傳與去重複；以真實的 GPX 重建衍生路段表（需要專題負責人另外同意）；保留行程的處理（凍結之後由隔離的評估腳本做） |
| 依賴 | B1-1 |

### B1-3 `pace`：配速表的停等比例、分級門檻、餘裕係數與版本

| 項目 | 內容 |
| --- | --- |
| 規格依據 | RES 1.2（算式與餘裕係數的規則）、1.4；DESIGN §6.1（分級門檻的規則、留一趟的程序、兩種版本）；處置 5.3、6.1 的 F-8、G-12 至 G-14、7.3 |
| 範圍 | `src/moto_copilot/pace/table.py`：(a) 各類別的 `stop_ratio` ＝ 可計時路段的 Σ 短停留 ÷ Σ 移動時間。(b) 分級門檻的規則：ok 路段的 `curvature_deg_per_km` 排序後取三分之一與三分之二位置的值，各四捨五入到 5 度／km；每次建立配速表時重算，結果寫在 `category_scheme`。(c) 餘裕係數：留一趟、每一折重算門檻、算不出配速的折不計入、0.05 的倍數中最小而且最多兩趟例外、計入的折數少於 8 時用 0.20 並把 `margin_basis` 設為 `default`。(d) `pace_version`：每次建立都是新的版本與新的檔案，不覆寫既有的；編號在 `research-` 與 `user-` 各自遞增。(e) 產品選用的版本：`built_at` 最晚的 `user-` 版本 |
| 驗收條件 | SB2-T4；SB2-T7；SB2-T9（表頭的值等於同一批行程依規則算出的值）；SB2-T10 中屬於 `pace` 的部分（不覆寫、編號、選用最新的 `user-` 版本）；SB2-T13（建立已經存在的 `research-` 版本時報錯）。門檻規則另加一項：固定的曲率清單得到固定的門檻 |
| 排除範圍 | 凍結清單的格式與雜湊核對（SB2-T12；屬於實驗腳本）；E1／E2 的腳本拒絕 `user-` 版本；介面更新 Profile；**路線目錄的路段類別怎麼跟著重算後的門檻更新**（規格沒有寫，見第 4 節）；以真實的配速行程執行留一趟或回歸檢查；保留行程 |
| 依賴 | B1-1、B1-2 |

### B1-4 `pace`：ETA 的停等寬放與安全餘裕

| 項目 | 內容 |
| --- | --- |
| 規格依據 | RES 1.2；DESIGN §6.1、§5 契約 4 |
| 範圍 | `compute_eta`：每個路段的 `stop_allow_s = stop_ratio × typ_seg_time_s`；`eta_typ` ＝ 出發時間加上累計的（典型移動時間加停等寬放）再加已排入的休息；`eta_safe` ＝ `eta_typ` 加上 `margin_coeff` 乘以累計的（典型移動時間加停等寬放）。`margin_coeff` 取自配速表的表頭，並寫進 ETA 的表頭 |
| 驗收條件 | SB2-T5；SB2-T6（加入一筆休息後，寬放與餘裕的秒數不變，兩個抵達時間只多出休息的長度）；SB2-T8；SB2-T9 中「ETA 表頭的 `margin_coeff` 等於所用配速表的值」 |
| 排除範圍 | 休息怎麼排入（預設休息、騎士指定的休息、對應檢查點）；介面的固定句子；規則 1 的判定；路線目錄 |
| 依賴 | B1-1、B1-3 |

### B1-5 規則 3 的範圍判定（確定性測試）

| 項目 | 內容 |
| --- | --- |
| 規格依據 | RES 3.1、3.5（方案 A）；DESIGN §4.2；SPEC 4.8（`in_rule3_range`）、5.2（規則 3 的條件） |
| 範圍 | 純函式：輸入是依序的路段（累計距離）、行程型態、去程的段數，以及每個路段的降雨機率分類（可以是「沒有」）；輸出是每個路段是否在規則 3 的範圍內，以及結果 PASS／FAIL／UNKNOWN。單向行程：路線最後 20% 的累計距離，跨入的路段也算。來回行程：折返點之後的全部路段。範圍內有高降雨機率提醒時 FAIL；沒有提醒但有路段缺降雨機率時 UNKNOWN；其餘 PASS |
| 驗收條件 | SB9-T1、T2、T4、T5。SB9-T3 只驗到結果是 UNKNOWN，不驗原因代碼。都用合成的路段與分類 |
| 排除範圍 | 原因代碼與它們的優先順序（依賴 SPEC 7.13 的草案，等 SB-3、SB-4 與 C3）；WeatherSegment 與 RuleResult 的 schema；鄉鎮對應與預報的讀取；Validator 的其他規則與整體結構；E2 的 Oracle（Oracle 必須獨立實作，不得引用這個函式）；方案 A／B 的敏感度分析；介面 |
| 依賴 | 無 |

## 4. 這一批沒有決定、需要另外裁決的事

- **路線目錄的路段類別怎麼跟著分級門檻更新。** 使用者更新 Profile 後門檻會重算，配速表的 `category_scheme` 跟著改變；已經建立的路線目錄是用舊的門檻分類的。規格沒有寫這時要重新分類、報錯，還是沿用。B1-3 不處理這件事。
- **以真實的配速行程執行回歸檢查**（RES 1.6：記錄範圍內騎乘時間誤差的留一趟平均帶符號誤差在 ±10% 之內）。它需要讀取配速行程，不在這一批；要執行時另外取得專題負責人的同意。
- 待裁決的 Q-3 七項（[q3_derived_details.md](../cr/CR-01-appendix/q3_derived_details.md)）都和路線、ID 有關，這一批完全不碰。

## 5. 後續的 Tickets 與 UI Gate（不在這一批）

專題負責人在 2026-11-15 裁決了 CR-01 的介面策略。它不改變這一批的範圍；這一批五張都是後端工作，不受影響。

| 順序 | 項目 | 內容 | 前提 |
| --- | --- | --- | --- |
| 1 | UI-0：Mock-data Skeleton（第一張 Streamlit 的 Ticket） | 以模擬資料做出 CR-01 的 UI Delta Prototype。至少包含：歷史 GPX 多檔上傳與 Profile 涵蓋度摘要；自然語言行程描述與必要的追問；來回／單向與期限的切換；路線確認、里程、道路名稱、來源；路線錯誤、評估失敗與 UNKNOWN；去程／回程分列的天氣與休息資訊。不連接 GPX、路線引擎、語言模型或真實 API | 影響介面的必要規格定案 |
| 2 | UI Delta Review（Gate） | 專題負責人實際檢視 Skeleton，進行一次審查：Streamlit 元件是否可行、操作流程、375 像素的手機寬度、鍵盤操作、CR-01 的介面驗收條件（UI_CR01_DELTA 第 11 節）。G3 沒有變更的部分不重新審查 | UI-0 完成 |
| 3 | 正式的介面與後端整合 | 之後的 Streamlit Tickets | UI Delta Review 通過 |

- `prototype/index.html` 不修改，保留為 G3 Frozen Baseline；不另外製作第二份 HTML。
- UI-0 還沒有建立 Ticket，也還沒有開始。它要等的規格（lead 的整理，待確認）：目標 GPX 的來回條件與休息對應不到時的呈現（Q-3 第 2、3 項）、行程描述輸入保護的訊息（SB-6）、SPEC-001 5.5 的固定文字（SB-10）。預報時段在天氣表的排法（SB-4）可以先用模擬的時段做版面。
- lead 建議的日期（待專題負責人確認）：Skeleton 11/24–11/27，檢視 11/28，正式整合 11/29–12/4。上面的規格在 11/22 前後還沒有定案時，Skeleton 會壓縮到整合的時間；12/5 的功能凍結不變。
