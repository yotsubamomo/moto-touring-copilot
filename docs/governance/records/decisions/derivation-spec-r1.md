# Derivation record — SPEC-R1：路線來源（契約 v0.3 的其餘部分與 `routing`）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `derivation-spec-r1`（v1，2026-11-17） |
| Spec | **SPEC-R1 v1**＝第 2 節列出的既有段落（commit `873e37a` 的內容）＋本 record 第 4 節的 DA 決定與 clarifications＋第 5 節的 Ticket 定義 |
| 決定者 | Design Authority（`gov-design-authority`；binding 由派工者核對） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 跨 Spec 的決定 | [`decision-20261117-oc1-first-run-derivation.md`](decision-20261117-oc1-first-run-derivation.md)（BD-1：OC-1 取代 Q-5 的 Ticket 閘門；BD-2：SB-10 的剩餘範圍） |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| Tickets | 新 Tickets R1-1、R1-2、R1-3、R1-4（第 5 節）。GitHub Issues 尚未建立；建立依 OC-1 §4.1、D-3，Issue 內文引用本 record 的 Ticket 定義。Issue 建立前不得啟動 |

## 1. 依據的 Outcome Contract 條款

- OC-1 §2.1 第 1 項：Must 模組 `routing`（DESIGN §9.1：路線引擎、路線快照、國道檢查、目標 GPX，共用一個介面）、`ingest`（只讀幾何的 GPX 讀取）、`tests`。
- OC-1 §2.1 第 2 項：`contracts` 更新到 v0.3（ID 格式的放寬、契約 2 的變更）；SPEC-001 由 Design Authority 引用。
- OC-1 §2.3：私有資料不送第三方、不進版控；測試只用合成資料；技術選擇（公開的 Valhalla 伺服器，有條件批准）。
- OC-1 §3.1：AB-1、AB-2、AB-10、AB-11、AB-13 的部分（第 7 節）。
- OC-1 §4.1：DA derive `routing` 的 Spec 與 Tickets；實作、審查、修正至完成；建立 derived Issues（D-3）。
- OC-1 §5：外部依賴「公開的 Valhalla 伺服器（`routing`，有條件批准）」；SB-1、SB-7、SB-8 已關閉。

## 2. Spec 的內容（引用）

| 來源（commit `873e37a`） | 引用的段落 |
| --- | --- |
| `docs/spec/SPEC-001-plan-schema.md` | §2 的「ID」「雜湊與正規化」「隱私」「對語言模型的隱私」四列；4.1 的 RouteRequest 中 `trip_type`、`target_gpx_ref`、`target_gpx_turnaround_km` 的定義與 PlaceRef 的 `ref_id`、`entry_ref_id`（只作為 `request_key` 的組成）；4.13 的六個 `code` 與其情形（不含 `message`、`actions` 的組裝）；4.14 RouteSnapshot 與 RouteLeg 全部；5.4 中路線快照的重用期限、偏移門檻、目標路線 GPX 的門檻、去回同路的自動辨識、`request_key` 的地標指紋、雜湊正規化的精度六列；7.11 第 1–8 項；第 9 節中第 5 節列出的測試 |
| `DESIGN.md` §4.1 | 「路線工具（CR-01）」一段 |
| `DESIGN.md` §5 | 共通規則的 ID 列；契約 1 的 `route_id`；契約 2 全部（含 v0.3 的欄位與不變條件 1–5）；契約 4 的 `route_id` 與 `breaks[].after_checkpoint_id`；「路線快照」的摘要與「路線模組的確定性規則」表中第 1–5 列與第 7 列 |
| `DESIGN.md` §9.2 | `routing` 的依賴與限制 |
| `docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` | §2.1–§2.5、§2.8（已由第 11、12 節的裁決改寫的內容） |
| `docs/cr/CR-01-appendix/lead_dispositions_resolution.md` | §8.1、§8.2、§8.4–§8.7、§9.1–§9.4、§9.9、§9.10（裁決與定案內容） |

**不屬於本 Spec：** 路線請求的解析（PlaceRef → 位置；詞彙表；出發錨點；目的地是公路時的進入端與另一端，decision record G-RREQ）；路線目錄的建立、切段、檢查點與 `ridden_share_pct`（G-RTE）；RouteSummary、RouteError 的 `message`／`actions` 與 PlanResult 的組裝；Evidence；凍結清單的檔案格式（E2／Demo 的 Spec）；`route_source = trip` 的示範路線（R01、R02 fixture 維持現狀）。

## 3. Boundary determination

**在 OC-1 boundary 內。** 依據：
- 範圍：OC-1 §2.1 第 1、2 項明列 `routing` 與契約 v0.3；OC-1 §4.1 明文授權 derive `routing` 的 Tickets；依 decision record BD-1，SPEC-001 未凍結不擋這次 derivation。
- 語義的來源：本 Spec 的規則都屬已關閉的 SB-1（ID 格式）、SB-7（目標 GPX）、SB-8（7.11 的待定項目），內容是 acceptor 2026-11-15 的裁決（SPEC-RESOLUTION-001 第 8 節、Q-3 七項與後續九項）。
- 與 SB-10 的關係（decision record BD-2）：本 Spec 碰到的 SPEC-001 第 10 節項目逐項對照如下，沒有一項的剩餘內容落在 SB-10 之內。

| 第 10 節 | 本 Spec 使用的內容 | 定案的依據 |
| --- | --- | --- |
| SD-14 RouteRequest、PlaceRef | 只用 `trip_type` 的兩個值與 `ref_id`／`entry_ref_id` 在 `request_key` 中的角色；不實作 RouteRequest 物件與 Planner 的填寫規則 | `trip_type` 的值：DESIGN §5 契約 2 v0.3；`request_key` 的組成：Q-3 第 5 項（處置 §8.5） |
| SD-15、SD-26 RouteSummary | 不產生 RouteSummary；只產生 RouteLeg 的 `freeway_check` 與 `has_highway` | 修正 B、F（SPEC-RESOLUTION-001 第 8 節）；SB-8 |
| SD-16 RouteError | 只回傳 `code`（與目標 GPX 的兩種情形），不組裝文字 | 路線錯誤代碼維持六個：Q-1 的裁決第 8 項（處置 §7.1）；`target_gpx_not_round_trip`：SD-39，已批准 |
| SD-25 RouteSnapshot、RouteLeg | 全部欄位 | 修正 A、B、C；Q-3 第 1、4、7 項（處置 §8.1、§8.4、§8.7）；SB-1、SB-8 |
| SD-27、SD-30、SD-33、SD-34、SD-35、SD-38、SD-39 | 重用、`request_key`、ID、目標 GPX、不可變、`via_offset_m`、高度、第六個代碼 | 各列狀態欄所引的裁決；SB-1、SB-7、SB-8 |
| SD-18 來源型別 | 不使用（Evidence 不在本 Spec） | — |

- 限制：對路線服務只送呼叫者提供的公開地標位置；不送私有 GPX、住家位置或個人識別資訊；測試不發出網路請求；不讀 `data/`。

## 4. DA 決定與 clarifications（SPEC-R1 的一部分）

**DD-R1-1 契約 2 不新增目標 GPX 的雜湊欄位。** DESIGN §5 契約 2 寫「路線目錄本身要不要另記這個雜湊尚未定，由修改契約 2 的 Ticket 提出」。決定：不新增。理由：`RG-` 的 `route_id` 由檔案內容的 SHA-256、`trip_type` 與實際採用的折返位置算出（SPEC-001 §2），給定檔案即可重算核對；規劃結果另以 `target_gpx_ref` 追溯（SPEC-001 4.12）；不新增欄位符合「契約的最小變更」。不改變 accepted 語義。

**DD-R1-2 引擎版本取不到時。** RouteSnapshot 的 `engine_version` 不可為空。決定：取自路線引擎的狀態回應；引擎沒有回報時記為固定字串 `unreported`，不推測、不以其他資訊代替。`map_data_date` 依 SPEC-001 4.14：沒有回報時為 `null`，不以取得日期代替。

**CL-R1-1（全部）資料與網路。** Executor 不讀取、不列出、不搜尋 `data/`，不執行 `experiments/` 下任何腳本（可以閱讀 `experiments/cr01_checks/routing_client.py`、`routing_c4_snapshots.py` 的原始碼作參考）。測試只用合成的幾何、合成的引擎回應與合成的 GPX；測試不發出網路請求。本 Spec 的 AC 不需要任何真實的路線請求。

**CL-R1-2（R1-2）`request_key` 的地點指紋。** 呼叫者為每個被引用的代號（`origin`、`destination`、每個 `via` 的 `ref_id`，以及有值的 `entry_ref_id`）提供該代號的座標定義（物件，經緯度依 SPEC-001 §2 正規化為小數六位）。指紋＝該物件依 SPEC-001 §2 正規化後的 JSON 的 SHA-256 前 16 碼。座標定義物件的確切內容由之後的詞彙表 Spec 定義；`request_key` 只對呼叫者給的物件計算，鍵中不含座標本身。

**CL-R1-3（R1-2）存放。** 快照檔寫到呼叫者提供的目錄，一個 `snapshot_id` 一個檔案；沒有寫在受版控路徑內的預設位置（從住家或出發錨點出發的快照不得進版控，DESIGN §5）。檔案一經寫入就不修改、不刪除；檔案位元組決定凍結清單所記的 SHA-256。取得時間＝各方向 `fetched_at` 中最晚的一個；30 天以「現在」減取得時間不超過 30 × 24 小時判定，「現在」可由呼叫者注入以便測試。

**CL-R1-4（R1-2）嚴格模式與凍結清單。** 嚴格模式的輸入是凍結清單的項目（每項含 `request_key`、`snapshot_id`、檔案的 SHA-256），以資料傳入；凍結清單的檔案格式不在本 Spec。SPEC-001 7.11 第 3 項所說的「停止執行」以一個專用的例外表示，不回傳 `route_error`，不回退到任何其他快照。

**CL-R1-5（R1-4）請求的輸入。** 每個方向的請求位置（起點、依序的中間位置、終點；每個位置帶代號、角色與經緯度）由呼叫者提供；來回行程的去程與回程各給一組，本 Spec 不由去程推導回程（回程的組成屬 G-RREQ）。路線參數固定為機車設定加 `use_highways: 0`，不送硬性排除，不要求高度。每次規劃每個方向最多送一次路線請求與一次道路屬性查詢，不自動重試。

**CL-R1-6（R1-4）`road_names`。** 每個方向依行經順序，取轉向指示中的道路名稱（每個轉向的起始道路名稱與道路名稱），依第一次出現的順序列出、去掉重複的名稱，不另設長度門檻。這是 SPEC-001 4.14 「主要道路名稱，依行經順序」在本 Spec 中的定義（與 C4 檢查的做法一致）。

**CL-R1-7（R1-4）偏移與順序。** 起點偏移＝起點位置到折線第一點的距離；終點偏移＝終點位置到折線最後一點的距離；中間位置的偏移＝到折線上最近點的距離（點到線段）。中間位置在折線上最近點的沿線里程必須**嚴格**遞增；相等也算不符合順序（fail closed）。

**CL-R1-8（R1-4）錯誤代碼的決定。** 引擎有回應時，先檢查所有可取得的國道訊號，再決定代碼。來回行程兩個方向都送出並檢查（引擎完全無法連線時除外），代碼依兩個方向合計決定：任一方向有任何國道訊號 → `highway_in_route`；否則任何不採用的原因（引擎錯誤、警告、道路屬性查詢失敗或長度不符、沒有回報 `has_highway`、偏移或順序不符）→ `routing_unavailable`。任何一個方向沒有通過，整條路線都不存快照。

**CL-R1-9（R1-4）端點與識別。** 路線引擎的端點是程式中的常數或明確傳入的設定值，不從環境變數自動取得。請求的 User-Agent 是通用的名稱，不含姓名、email 或專案名稱（與 `routing_client.py` 相同的原則）。log 與例外訊息不輸出請求中的座標。

**CL-R1-10（R1-3）目標 GPX 的讀取與自動辨識。**
1. 讀取：依序取所有 `trk`／`trkseg` 的 `trkpt`；沒有任何 `trkpt` 時取 `rte` 的 `rtept`。只讀經緯度，不讀時間與高度；沒有時間的點照常使用。
2. 檢查：點數少於 2、總長度不到 1 km、相鄰兩點（含跨 `trkseg` 的相鄰點）相距超過 1 km 時是 `target_gpx_invalid`。
3. 行程型態只由呼叫者給定，不由幾何推定；沒有給時回報明確的錯誤（追問由之後的流程處理）。單向：幾何原樣使用，不使用折返位置。
4. 來回：終點與起點相距超過 200 m → `target_gpx_not_round_trip`（情形「終點沒有回到起點」），即使給了折返位置。否則：給了 `target_gpx_turnaround_km` → 換算成公尺四捨五入到整數 m；0 < m < 軌跡總長時以沿軌跡 m 公尺處為折返點，否則 → `target_gpx_not_round_trip`（情形「無法確認折返點」）。沒有給 → 自動辨識；不成立 → `target_gpx_not_round_trip`（情形「無法確認折返點」）。
5. 自動辨識：以離起點直線距離最遠的軌跡點（有多個時取第一個）為分界；後段自分界沿軌跡每 100 m 取一點（100 m、200 m…，不含分界本身）；取樣點 50 m 內有前段（起點到分界）的任何軌跡點即為接近；後段沒有任何取樣點時不成立；接近的取樣點占全部取樣點 ≥ 90% 時成立，折返點是那個最遠點。這是保守的啟發式門檻，沒有以真實資料驗證過，程式說明與紀錄不得宣稱它經過驗證。
6. `route_id`：`RG-`＋SHA-256（檔案內容 SHA-256 的十六進位字串＋`:`＋`trip_type`，來回行程再接 `:`＋折返位置的整數公尺）的前 10 碼。`target_gpx_ref`＝檔案內容的 SHA-256。
7. 輸出與錯誤都不含檔案的路徑與檔名，也不寫入 log。

## 5. Tickets

共通的充分證據要求（每張 Ticket 都適用）：
- E-1：`.venv/Scripts/python.exe -m pytest -q` 的完整輸出記在 worklog，全數通過。
- E-2：worklog 逐條列出每一項 AC 對應的測試名稱與結果（SPEC-001 第 9 節的 S 編號照引）。
- E-3：測試的幾何、引擎回應與 GPX 全部是合成的，worklog 寫明來源；diff 中沒有真實的軌跡、住家附近的座標或私有路線；公開地標的座標若出現，寫明出處。
- E-4：測試沒有網路請求（以 worklog 記錄的方式說明，例如以替身取代傳輸層）。
- E-5：因契約改版而修改的既有測試，在 worklog 逐項列出理由。
- E-6：對標示的高風險類別，Executor 依 `decision-20261117-high-risk-categories.md` 第 5 節作 self-verification 並記錄；independent audit 依同一節的最低核對範圍。

### R1-1 `contracts`：ID 樣式的放寬與契約 2 的 v0.3

| 項目 | 內容 |
| --- | --- |
| 範圍 | `src/moto_copilot/contracts/schemas.py`、`validate.py` 與既有 fixture：(a) `route_id` 改為 `^(R\d{2}\|R[SG]-[0-9a-f]{10})$`，`checkpoint_id` 改為 `^(R\d{2}\|R[SG]-[0-9a-f]{10})-CP\d{2,3}$`，套用在契約 1 的 `route_id`、契約 2 全部、契約 4 的 `route_id` 與 `breaks[].after_checkpoint_id`；(b) 契約 2 的路線紀錄：`source_trip_id` 可空、新增 `route_source`（`trip`／`routing`／`target_gpx`）、`snapshot_id`（可空，`^SN-[0-9a-f]{10}$`）、`trip_type`（`one_way`／`round_trip`）；檢查點的 `kind` 新增 `turnaround`；(c) 契約 2 不變條件 4、5；(d) `CONTRACT_VERSION` 改為 `"0.3"`（`derivation-spec-b1.md` CL-B1-2）；(e) 更新模擬 fixture 使其符合 v0.3（R01、R02 保持有效） |
| AC | (1) S37 與 S58 中屬於契約的部分：`route_id`、`checkpoint_id`、`snapshot_id` 符合 SPEC-001 §2 的樣式，`R01`／`R02` 仍然有效，不符合的值被拒絕。(2) 檢查點的 `checkpoint_id` 前綴等於它的 `route_id`。(3) `route_source` 與 ID 一致：`routing` 的 `route_id` 是 `RS-` 而且十六進位部分等於 `snapshot_id` 的十六進位部分；`target_gpx` 的是 `RG-`；`trip` 的是 `R` 加兩位數字；不一致時被拒絕（SPEC-001 §2 的 ID 定義）。(4) 契約 2 不變條件 1–5 各有一個違反的案例被拒絕，其中 4、5 為 v0.3 新增。(5) `validate_dataset` 對更新後的模擬資料集沒有違反；既有測試全數通過 |
| 排除 | RouteSnapshot 的 schema（R1-2）；Plan Schema；`request_key`；路線目錄的產生與檢查點的編號規則；目標 GPX 的雜湊欄位（DD-R1-1：不新增） |
| 依賴 | #7（同一組檔案，v0.3 的第一部分） |
| AB | AB-2、AB-13 的部分 |
| 高風險類別 | **不涉及**。依據：只改 ID 樣式與契約欄位的驗證；不讀寫私有資料或憑證、不決定輸出位置（H-1、H-2）；不碰保留行程、實驗或宣稱（H-3）；不計算規則結果、狀態或路線的採用（H-4）。若實作中碰到上述任何路徑，Executor route 至 Design Authority |

### R1-2 `routing`：路線快照的模型、正規化雜湊、不可變的存放與選取

| 項目 | 內容 |
| --- | --- |
| 範圍 | 新建 `src/moto_copilot/routing/`：(a) SPEC-001 §2 的正規化 JSON；(b) `snapshot_id`（雜湊範圍不含 `snapshot_id` 與各方向的 `fetched_at`）與對應的 `RS-` `route_id`；(c) RouteSnapshot／RouteLeg 的結構檢查（SPEC-001 4.14 的欄位、型別、可否為空；`one_way` 一筆 `outbound`，`round_trip` 依序 `outbound`、`return`；沒有高度欄位）；(d) `request_key`（7.11 第 4 項，CL-R1-2）；(e) 寫入一次的存放：內容相同沿用既有檔案而不寫入，以既有代號寫入不同內容時報錯，不修改、不刪除（7.11 第 1 項，CL-R1-3）；(f) 選取：一般模式的重用（`request_key` 相同、`freeway_check_method` 與現行相同、30 天內，取最新）、一般的 Snapshot Mode（相容的快照中取得時間最晚者，沒有時回傳 `snapshot_missing`）、嚴格模式（CL-R1-4） |
| AC | S36；S37 中 `request_key` 的部分（途經點順序對調得到不同的鍵）；S53；S54；S55；S56；S58 中 `snapshot_id` 的部分；S71；S72；S73；S74；S75；S76；S77；S86；S35 中屬於存放與選取的部分（31 天前的快照不被一般模式重用；重新取得而內容相同時沿用舊檔、不產生新檔，內容不同時存成新檔；兩種情形舊檔的內容都不變；Snapshot Mode 仍然可以使用舊檔）；S23 中屬於結構的部分（欄位齊全、`legs` 的筆數與順序、沒有高度欄位）；S17 中「沒有對應快照時回傳 `snapshot_missing`」。另加：快照與 `request_key` 的計算不需要網路；存放位置由呼叫者提供，測試使用暫存目錄 |
| 排除 | 呼叫路線引擎、國道檢查、偏移（R1-4）；凍結清單的檔案格式；詞彙表與座標定義的內容；路線目錄 |
| 依賴 | R1-1 |
| AB | AB-1、AB-2、AB-11、AB-13 的部分 |
| 高風險類別 | **H-2**（快照含折線，決定衍生輸出寫到哪裡，判定 3.2 第 1 項）、**H-3**（嚴格模式是 E2 與凍結 Demo 使用的凍結快照機制，判定 3.3 第 2 項）、**H-4**（快照的重用與 Snapshot Mode 的選取，判定 3.4 第 4 項） |

### R1-3 `routing`：目標路線 GPX 的路線來源

| 項目 | 內容 |
| --- | --- |
| 範圍 | (a) `src/moto_copilot/ingest/` 內只讀幾何的 GPX 讀取（CL-R1-10 第 1 項）；(b) `src/moto_copilot/routing/` 內的目標 GPX 路線來源：檢查、行程型態、來回條件、折返點（騎士指定優先，其次自動辨識）、`RG-` 的 `route_id` 與 `target_gpx_ref`、在折返點把幾何切成去程與回程（折返點是兩段的分界），或回傳 `target_gpx_invalid`／`target_gpx_not_round_trip`（並標明兩種情形中的哪一種）（7.11 第 2 項，CL-R1-10） |
| AC | S27；S43（其中「沒有指定行程型態時系統追問」屬追問流程，不在本 Ticket；本 Ticket 驗證沒有給行程型態時不由幾何推定，回報明確的錯誤）；S59；S60；S61；S62；S63；S64；S78；S79（四種合成形狀）；S80；S58 中 `RG-` 的部分；S10 中「不含目標 GPX 的路徑與檔名」的部分（輸出、錯誤與 log）。另加：讀取不依賴時間欄位；`trkpt` 與只有 `rtept` 的檔案都能讀；跨 `trkseg` 的相鄰點超過 1 km 時是 `target_gpx_invalid` |
| 排除 | 介面上的折返欄位與檔案上傳（Should）；CLI 的接線（之後的整合 Ticket；本 Ticket 以函式參數接受 `target_gpx_turnaround_km`）；切段、分類與檢查點（`routes`）；RouteError 的文字 |
| 依賴 | R1-1（`RG-` 的樣式）；#9（同一個 `ingest` 套件，避免同時修改） |
| AB | AB-2、AB-10、AB-13 的部分 |
| 高風險類別 | **H-2**（開啟 GPX 的程式；路徑與檔名不得外流，判定 3.2 第 1、4 項）、**H-3**（折返判斷的啟發式門檻不得描述為已驗證，判定 3.3 第 4 項）、**H-4**（目標 GPX 的來回條件與折返點是路線的採用條件：不推定、不反轉、不補造，判定 3.4 第 4 項） |

### R1-4 `routing`：路線引擎的請求與採用、共用的路線介面

| 項目 | 內容 |
| --- | --- |
| 範圍 | (a) 公開 Valhalla 伺服器的 client（端點與識別依 CL-R1-9；傳輸層可替換，測試不連網）：每個方向一次路線請求（CL-R1-5）與一次道路屬性查詢；(b) 每個方向的採用檢查：回應的警告（7.11 第 7 項）、國道檢查的四項訊號與 `freeway_check_method`（7.11 第 5 項）、起點與終點偏移、中間位置的偏移與順序（7.11 第 8 項，CL-R1-7）；(c) 錯誤代碼的決定（CL-R1-8）；(d) 由回應組成 RouteLeg（`road_names` 依 CL-R1-6；`engine_name`、`engine_version`、`map_data_date` 依 DD-R1-2），每個方向都通過才經 R1-2 存成快照；(e) 取得路線的順序（7.11 第 3 項）：Snapshot Mode 只經 R1-2 選取、不呼叫引擎；一般模式先經 R1-2 找 30 天內可重用的快照，沒有才呼叫引擎；引擎失敗時回傳 `routing_unavailable`，不改用已失效的快照；(f) 共用的路線介面：`routing` 與 `target_gpx`（R1-3）兩種來源由同一個函式回傳「採用的路線（各方向的幾何、里程、道路名稱、`route_id`、`route_source`、`trip_type`、`snapshot_id` 或 `target_gpx_ref`、目標 GPX 的折返位置）」或「路線錯誤代碼」 |
| AC | S15 中屬於路線的部分（引擎失敗或國道檢查沒通過時沒有路線、沒有里程與道路名稱；一般模式不改用已失效的快照）；S17（Snapshot Mode 不呼叫引擎）；S23 中屬於行為的部分（來回行程兩個方向各有自己的 `request`、`shape`、`fetched_at`，`return` 的折線不是 `outbound` 的反轉）；S24 的第一句（任一方向 `freeway_check` 是 `fail` 時整條不存快照，結果是 `highway_in_route`；第二句的 `leg_length_diff_flag` 屬 RouteSummary，不在本 Spec）；S30；S35 中屬於引擎的部分（同一個請求第二次規劃不呼叫引擎；31 天後重新取得；引擎失敗而只有過期快照時回傳 `routing_unavailable`；回程沒通過時去程也不存檔）；S38 中屬於路線的部分（回程的折線不是去程的反轉；回程的請求失敗時是路線錯誤，沒有里程與道路名稱）；S39 中以合成回應可以驗證的部分（`has_highway` 是 `true` 而道路屬性沒有國道時是 `fail`；道路屬性含 `motorway` 或國道名稱時是 `fail`；道路屬性查詢失敗時是 `routing_unavailable`，沒有快照）；S40 中以合成回應可以驗證的部分（終點偏移數公里的回應被拒收；途經點離折線超過 200 m 被拒收，結果是 `routing_unavailable`）；S68；S69；S70。另加：沒有回報 `has_highway`、道路屬性長度與路線里程相差超過 2% 時是 `routing_unavailable` 而且不產生 `freeway_check` 的值；國道訊號與其他不採用的原因同時出現時是 `highway_in_route`；中間位置的沿線里程相等時拒收；請求的 User-Agent 與內容不含個人識別資訊；端點不受環境變數影響 |
| 排除 | S39「五條參考路線的 10 段都是 `pass`」與 S40「五條參考路線都通過」「詞彙表每個地標的偏移不超過 100 m」：需要真實的路線請求與詞彙表，屬整合或詞彙表的驗收（decision record RV-5）；路線請求的解析（G-RREQ）；`route_source = trip`；路線目錄 |
| 依賴 | R1-2、R1-3 |
| AB | AB-1、AB-2、AB-10、AB-13 的部分 |
| 高風險類別 | **H-1**（決定請求端點的方式，判定 3.1 第 2 項；沒有憑證，核對重點是端點不可被轉向）、**H-2**（送往第三方的內容與 User-Agent，判定 3.2 第 3 項）、**H-4**（路線採用的檢查：國道檢查、偏移、警告、途經點順序，判定 3.4 第 4 項） |

## 6. Spec 層級的驗收（Spec Integration Audit 的範圍）

| 編號 | 條件 | 證據 |
| --- | --- | --- |
| SR1-AC1 | 四張 Ticket 都依 orch-default §7 結案 | audit records 與 worklogs |
| SR1-AC2 | 跨 Ticket 的整合：以合成的引擎回應走一般模式（第一次呼叫引擎並存快照、第二次重用）、Snapshot Mode、嚴格模式，以及以合成 GPX 走目標 GPX 的單向與來回，都經 R1-4 的共用介面；產生的 `route_id`、`snapshot_id`、`checkpoint_id` 樣式通過 R1-1 的契約檢查，`RS-` 的十六進位部分等於 `snapshot_id` | 整合測試與 pytest 輸出 |
| SR1-AC3 | 任何不採用的情形都不存快照、不產生路線的里程與道路名稱；國道訊號的優先順序在整合路徑上成立 | 測試 |
| SR1-AC4 | 測試全程沒有網路請求；輸出、錯誤與 log 不含目標 GPX 的路徑與檔名，也不含請求的座標 | 測試與 diff |
| SR1-AC5 | 新增的文字沒有把國道檢查稱為道路主管機關的驗證，沒有把去回同路的自動辨識稱為已驗證 | diff |

已知不在本 Spec 涵蓋內、SIA 不得記為已涵蓋：真實路線請求的結果（五條參考路線）；詞彙表；路線請求的解析；路線目錄、檢查點與 `ridden_share_pct`；RouteSummary 與 RouteError 的文字。

## 7. 分配到的 Outcome Contract acceptance boundary 部分

| AB | 本 Spec 分配到的部分 |
| --- | --- |
| AB-1 | 「路線快照上的實際道路路線」的產生、檢查與保存能力。不含端到端的執行證據 |
| AB-2 | FR1 中「由路線引擎產生實際道路路線」「支援來回與單向」「改用只讀幾何的目標 GPX」「路線失敗時明確報錯」。不含行程描述、追問、期限語意、詞彙表 |
| AB-10 | NFR2：路線層對第三方只送呼叫者提供的公開地標位置、通用的 User-Agent；目標 GPX 不外流；NFR4：路線取不到或不能採用時回傳明確的錯誤，不補造路線 |
| AB-11 | 路線快照的嚴格模式（凍結清單指定的快照、雜湊核對、不回退）的機制。不含凍結清單的格式與 E2 Runner |
| AB-13 | 本 Spec 的 pytest、Spec Integration Audit closure、Design Authority phase acceptance |

## 8. 受影響的工作

- 新建 `src/moto_copilot/routing/`；`contracts` 的 ID 樣式與契約 2 改為 v0.3；`ingest` 新增只讀幾何的讀取。
- 既有測試與模擬 fixture 會因契約 2 的 v0.3 而修改；理由記在 worklog。
- `routes`（G-RTE）的 Spec 會以 R1-4 的共用介面為輸入；路線請求的解析（G-RREQ）會以 CL-R1-2、CL-R1-5 的輸入形式為介面。
- SPEC-001 4.12、4.14 的 `road_names` 與 DESIGN §5 契約 2 的待定句，建議同步（decision record RV-2、RV-3）。

## 9. Implementation readiness

**Implementation-ready（Issue 建立後）。** 規則全部來自已關閉的 SB-1、SB-7、SB-8 與 acceptor 的裁決；原本需要 Executor 猜測的細節（指紋的輸入、存放與時間、嚴格模式的停止方式、請求的輸入與次數、道路名稱、偏移與順序的定義、錯誤代碼的決定、端點與識別、GPX 的讀取與自動辨識的取樣）已由第 4 節固定。需要真實請求或詞彙表才能驗證的測試已明確排除，不以合成結果冒充。
