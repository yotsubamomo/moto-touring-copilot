# Decision record — C-14-1：正規化的取位方式（CL-R1-14）；C-14-2～C-14-5 的 disposition；相關的取整規則（CL-R1-15～CL-R1-19）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue14-c141`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 第 6 節事件 69）。問題來自 #14（SPEC-R1 R1-2）Executor 的 return `NEEDS_DA`：worklog `docs/governance/records/worklog/issue-14.md` 第 7 節 **C-14-1**（blocking）、C-14-2、C-14-5（non-blocking）、C-14-3、C-14-4（DA 知悉）。**C-14-6 保留給 acceptor，不在本 record 的裁決範圍** |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-R1 v1（`derivation-spec-r1.md`）的 clarifications **CL-R1-14～CL-R1-19**，治理 §5.3 第 2 類。與 CL-R1-1～CL-R1-13 並列引用 |
| Subject 基準 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `91f2be1f94dc3b14e67a9cc1b6bc2ee4d8ba686b`；#14 的 implementation subject `366866c`（之後只有 record-only commit）；`git status --short` 為空 |
| 依據的條文 | 治理 §1.2、§2.4、§2.5（E-DA）、§3.4、§3.6-A、§3.8、§5.3；Bindings m3 第 2.4、2.6（RB-7）、3.2、5、7 節；`derivation-spec-r1.md` 第 2、4、5、6、8 節（CL-R1-2～CL-R1-4、CL-R1-10、DD-R1-2、R1-2～R1-4 列、SR1-AC1～AC5）；`decision-20261118-issue13-c131.md`（CL-R1-13、RV-6、RV-7）；`decision-20261117-high-risk-categories.md` §3.2–§3.4、§5 |
| 讀過的證據 | Bindings m3 第 0–7 節；治理本文 §1.2、§2.1、§2.4、§2.5、§3.3–§3.6、§5.3；`derivation-spec-r1.md` 全文；CL-R1-13 record 第 1–5 節；高風險 record 全文；worklog `issue-14.md` 全文；run record 第 4、5 節與事件 65–69；Issue #14 原文（scratchpad `issue-14-body.md`，SHA-256 重算 `f7a83732c3b65001e170e8a337ada636f8a984f908b41743d033519a95ca7b75`，與派工所述相同）與 `issue-15-body.md`、`issue-16-body.md` 中的相關列；`docs/spec/SPEC-001-plan-schema.md` §2、4.1 的 `target_gpx_turnaround_km`、4.14、5.4、7.11 第 1–8 項、第 9 節 S35、S36、S53～S56、S58～S64、S71～S80、S86；`docs/cr/CR-01-appendix/lead_dispositions_resolution.md` 第 8.1、8.5 節（Q-3 第 1、5 項的裁決原文與 Q3-T4、Q3-T19）；`DESIGN.md` §4.1 路線工具段、§5 共通規則的 ID 列與契約 2；`src/moto_copilot/routing/` 全部模組（`canonical.py`、`request_key.py` 與 `snapshot.py` 的相關段、`store.py`）；`tests/test_routing_snapshot.py` 第 30–116 行、`tests/test_routing_store.py` 第 300–340 行；`src/`、`tests/` 內全部 `round(`、`Decimal`、`quantize` 的出現處（`routes/catalog.py`、`ingest/segments.py`、`pace/table.py`、`contracts/validate.py`） |

本 record 撰寫時實際執行的（不讀 GPX、不需金鑰；探測以 stdin 執行、只用合成數值，沒有寫入 repo；執行後 `git status --short` 仍為空）：

| 指令／探測 | 結果 |
| --- | --- |
| `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`（HEAD `91f2be1`） | `1112 passed in 28.50s`，exit 0 |
| 兩種取位對 S56 的兩組反例（以最短十進位表示為準） | `0.1234561`／`0.1234569`（只有第七位不同）：四捨五入（half-even、half-up 皆同）得 `0.123456`／`0.123457`，**不同**；捨去得 `0.123456`／`0.123456`。`0.1234559`／`0.1234561`（第六位不同）：四捨五入得 `0.123456`／`0.123456`，**相同**；捨去得 `0.123455`／`0.123456`。四捨五入在進位邊界兩側各違反 S56 的一半，捨去兩半都成立 |
| 以二進位精確值捨去（`Decimal(x)`）與以最短十進位表示捨去（`Decimal(repr(x))`）的比較 | 精確值：`0.3`→`0.299999`、`0.6`（`0.7-0.1`）→`0.599999`、`2.675`→`2.674999`；最短表示：`0.300000`、`0.600000`、`2.675000`。只有以最短表示為準，S56 所說的「第幾位小數」才是使用者看到的十進位數字 |
| 以記憶體中替換 `_format_float` 為精確值捨去，跑兩個新測試檔（不改 repo 檔案） | `173 failed, 60 passed`：現有測試會抓到「改用二進位精確值」的突變 |
| `canonical_json({"lat": 23})`、`{"lat": 23.0}`、`{"lat": 23.0000001}` | `{"lat":23}`、`{"lat":23.000000}`、`{"lat":23.000000}`：數值相等的 int 與 float 得到不同的雜湊（第 7.3 節 TI-C14-1） |
| 20 萬個合成值 `x ∈ [-180, 180]`：`round(x, 6)` 之後再依 `canonical.py` 捨去 | 0 筆改變：已取到六位的值經捨去不變（第 2.3 節） |
| 整數公尺的取整（第 7.1 節） | `round(1000.5) == 1000`（Python 的 half-even）；`0.5005 * 1000 == 500.49999999999994`；`Decimal(repr(0.5005)) * 1000` 依 `ROUND_HALF_UP` 得 501，`Decimal(repr(1.0005)) * 1000` 得 1001，`Decimal(repr(0.0005)) * 1000` 得 1 |
| `grep` `src/`、`tests/`：`round(`、`Decimal`、`quantize`、`, 6)` | 六位的取整只在 `routes/catalog.py:177`（`end_lat`／`end_lon`，`round(..., 6)`）；`ingest/` 只有 `segments.py` 的一位小數（長度與時間），`ingest/gpx.py` 沒有取整；`contracts/` 沒有任何數值正規化或雜湊 |

沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有讀或執行 `experiments/` 下任何檔案，沒有讀保留行程，沒有呼叫 GitHub，沒有派工任何 subagent，沒有 commit。

---

## 1. 問題

SPEC-001 §2「雜湊與正規化」列寫「經緯度取小數六位；以公尺計的長度與偏移取小數一位；其他浮點數取小數六位」，沒有寫取位方式。`snapshot_id`、`RS-` 的 `route_id`、`request_key` 與地點指紋（CL-R1-2）都經過這條規則，所以捨去與四捨五入會產生不同的代號值，也決定 S56 與 S71 能否成立。#14 目前採捨去（`canonical.py` 的 `_ROUNDING = ROUND_DOWN`，以 `repr` 為準）。另有四項 non-blocking／知悉事項（C-14-2～C-14-5）。

## 2. C-14-1 的裁決（CL-R1-14）

### 2.1 依據

1. **驗證契約只容許捨去。** S56（＝Q3-T4）：「經緯度第六位小數不同的兩份內容得到不同的雜湊；只有第七位以後不同的得到相同的雜湊。」S71（＝Q3-T19）：「被引用地標的座標在第六位小數以內改變時 `request_key` 改變。」兩句都以十進位的「第幾位小數」陳述，沒有限定數值範圍。把兩個值的十進位表示逐位比較：前六位都相同 ⇔ 捨去到六位後相同。這個等價只在捨去（向零）時成立；四捨五入在進位邊界兩側都有反例（本 record 開頭的探測）。Q3-T4 與 Q3-T19 屬 Q-3 第 1、5 項裁決的定案內容（處置第 8.1、8.5 節），已寫入 SPEC-001 第 9 節，SPEC-R1 第 5 節的 R1-2 AC 直接引用。Tickets 不得以挑選不跨進位邊界的數值來「通過」一條對其他數值不成立的 AC（治理 §3.4：Executor 不得藉選擇測試方法改變驗證契約）。
2. **SPEC-001 需要四捨五入時會明寫。** 同一份 Spec 的 4.1 寫「換算成公尺時四捨五入到整數」；DESIGN §6.1 與 SPEC-RESOLUTION-001 的分級門檻寫「四捨五入到 5 度／km」。§2 只寫「取小數六位」，沒有寫四捨五入。
3. **Acceptor 的裁決原文**（處置第 8.1 節）：「經緯度至少保留小數六位，不得把全部浮點數統一取小數一位。」捨去保留恰好六位，符合「至少六位」；裁決沒有指定取位方式。
4. **以最短十進位表示為準。** S56 所說的「位數」是十進位數字。浮點數的二進位精確值往往略小於它的十進位寫法（`0.3` 的精確值是 `0.29999…`），直接捨去精確值會使 `0.3` 變成 `0.299999`，等於寫進去的值與雜湊所用的值不同；以 round-trip 的最短十進位表示（Python `repr`）為準才使 S56 對使用者寫下的數值成立。
5. **向零，不是向下。** 向下取整（floor）對負數會使 `-0.1234560` 與 `-0.1234561` 得到不同的值，違反 S56 的後半；向零（`ROUND_DOWN`）對正負數都成立。

由此，既有來源在 S56／S71 的約束下只有一種合理解讀而尚未寫下（治理 §3.6-A）。**不構成 E-DA/D1**：兩種讀法的後果雖然不同，但證據（S56、S71 與其裁決來源）可以裁決。**不構成 D2**：沒有先前的 DA 決定被 FA ruling 或 Reviewer finding 推翻或爭議。

### 2.2 裁決

**CL-R1-14（SPEC-001 §2 正規化的取位方式；SPEC-R1 全部 Tickets）。** 正規化 JSON 中的每一個浮點數（JSON 的非整數數值；Python 的 `float`），依下列方式寫出：

1. 取該值的最短 round-trip 十進位表示（Python `repr` 所得的數字）；
2. 保留小數 N 位，**捨去**多出的位數（向零，`ROUND_DOWN`），不四捨五入、不向下取整；
3. 以定點寫法寫出恰好 N 位小數（不用指數寫法）；結果為零時不帶負號；
4. N＝1：以公尺計的長度與偏移；N＝6：經緯度與其他浮點數。
5. 整數、布林值、字串、`null` 不受影響；NaN 與無限大不可正規化，報錯。

這條規則是 `snapshot_id`（雜湊範圍依 §2 ID 列）、`RS-` 的 `route_id`、`request_key` 與 CL-R1-2 地點指紋共用的唯一規則。它只決定雜湊與快照檔的內容，**不用來決定路線是否採用**（第 7.2 節 CL-R1-19 第 1 項）。

**#14 的現行實作符合本裁決**：`canonical.py` 的 `_format_float` 以 `Decimal(repr(value))` 依 `ROUND_DOWN` 取 N 位、零值去掉負號、拒絕非有限值；`request_key.py` 的指紋與 `request_key` 都經 `sha256_hex`，與 `snapshot_id` 共用同一函式。D-14-2（以公尺計的值以 `_m` 結尾的鍵辨認，含外層的鍵）符合 SPEC-001 §2 的命名規則，本 record 不另作裁決。**不需要為 C-14-1 修改任何程式或測試。** 選項 (b)（改為四捨五入並改 S56 的測試）不採用。

**基線的穩定性。** 這條規則一旦有快照被存下、或被列入凍結清單（E2、凍結的 Demo），改變它就會使既有的 `snapshot_id`、`request_key` 對不上，成為其他工作依賴的設計基線的變更；之後任何修改都要經 Design Authority 的 derivation 並評估既有快照與凍結清單（治理 §5.3）。目前沒有任何已存的快照或凍結清單（worklog C-14-1 欄），本裁決不影響既有資料。

### 2.3 一致性檢查

| 位置 | 用到的取位 | 判斷 | 處置 |
| --- | --- | --- | --- |
| SPEC-001 5.4「雜湊正規化的精度」「`request_key` 的地標指紋」、7.11 第 1、4 項 | 都引用 §2 的規則 | 一致：同一條規則 | 文字同步 RV-8（第 7.4 節） |
| CL-R1-2 地點指紋（R1-2） | 「經緯度依 SPEC-001 §2 正規化為小數六位」 | 一致：程式以同一個 `sha256_hex` 計算 | 無 |
| R1-1 的契約（`contracts/`） | 沒有數值正規化或雜湊；只匯入 `SNAPSHOT_ID_PATTERN` 等樣式 | 不涉及 | 無 |
| `routes/catalog.py:177`（契約 2 路線目錄的 `end_lat`／`end_lon`，`round(..., 6)`；同檔的長度 `round(..., 1)`） | Python `round`（half-even） | **不是 §2 的規則**：§2 的正規化只適用於 `request_key` 與 `snapshot_id` 的雜湊；路線目錄的欄位是契約 2 的資料值，契約 2 沒有規定取位，也不進入任何雜湊。探測顯示 `round(x, 6)` 的結果經捨去不變，即使這類值之後進入雜湊也不會漂移 | 無。路線目錄的產生屬 G-RTE（CL-R1-12），本 record 不約束它 |
| `ingest/segments.py`（#9，契約 1 的長度與時間 `round(..., 1)`）；`ingest/gpx.py` | 一位小數；GPX 讀取沒有取整 | 不是 §2 的規則（契約 1 的資料值，不雜湊）。派工內容所說「#9 的 ingest 的 `round(..., 6)`」在 HEAD 不存在；六位的取整只在上一列的 `routes/catalog.py` | 無 |
| `pace/table.py`、`contracts/validate.py` 的 `round` | 配速表的設定值與容差 | 不涉及 | 無 |
| R1-3 的 `RG-`（SPEC-001 §2 ID 列；CL-R1-10 第 4、6 項） | 不經 §2 的正規化：輸入是檔案 SHA-256 的十六進位字串、`trip_type` 與**整數公尺**；4.1 明寫「四捨五入到整數」 | 與 §2 是不同的量、不同的規則，不衝突；但整數公尺的取整方式與自動判定時的取整需要寫明 | **CL-R1-18**（第 7.1 節） |
| R1-4 的偏移、長度與門檻（7.11 第 5、8 項） | 偏移存入快照時依 §2 取一位（捨去） | 捨去使存入的值不大於原值；門檻若以存入的值判定，`200.04 m` 會被當成 `200.0 m` 通過 | **CL-R1-19 第 1 項**（第 7.2 節） |

## 3. C-14-2 的裁決（CL-R1-15）

**確認 D-14-11。** 7.11 第 3 項的「取其中最新的一個」（一般模式）與「取得時間最晚的一個」（一般的 Snapshot Mode）有多個快照的取得時間同時最晚時，取 `snapshot_id` 字典順序最小者。

- 理由：同時最晚的候選都是相容的快照（`request_key` 相同、每個方向的 `freeway_check_method` 與現行相同、存放時已通過 4.14 的值檢查），選哪一個都是合法的路線；規則要求的是結果確定、不受目錄順序影響（H-4：選取有確定的結果）。停止執行（fail closed）會讓一個無害的情形擋住規劃，沒有對應的風險可防。
- 不適用於嚴格模式：嚴格模式只看凍結清單，不比取得時間（CL-R1-4）。
- 這是補上的最小內容（lead 寫定的同類細節），不改變 7.11 第 3 項的語義。現有測試 `test_equal_acquisition_times_resolve_to_the_smallest_snapshot_id` 即其證據；`store.py` 的 `_latest` docstring 可以把「reported for Design Authority confirmation」改為引用本 record（第 8.1 節第 3 項）。

## 4. C-14-3 的裁決（CL-R1-16）：要求修改

**一般模式的「30 天內」是 `0 ≤ 現在 − 取得時間 ≤ 30 × 24 小時`。** 取得時間晚於「現在」的快照不是「30 天內」的快照，一般模式不重用。

- 理由：5.4 與 7.11 第 3 項的「取得時間在 30 天內」指取得發生在過去 30 天之內；CL-R1-3 的「『現在』減取得時間不超過 30 × 24 小時」是本 Design Authority 為了界定邊界（30 × 24 小時而不是日曆日）寫的，不是為了接受負的經過時間。取得時間在未來表示時鐘或紀錄不一致，快照的新鮮度無法確立；依 H-4（過期快取的處理），無法確立時不重用。
- 後果：時鐘倒退期間，一般模式對該請求會呼叫路線引擎；內容相同時依 7.11 第 1 項沿用既有的檔案，取得時間不更新。這與 5.4「同一條路超過 30 天之後……每次規劃都會重新向路線引擎取得」是同一類已知限制，不另設快取機制。
- 不改變：一般的 Snapshot Mode 不看期限（7.11 第 3 項 (b)），取得時間只用於排序，照舊；嚴格模式不看取得時間，照舊。CL-R1-3 的其他內容（取得時間＝各方向 `fetched_at` 中最晚者、「現在」可注入）不變。
- 這是 CL-R1-3 的 clarification（治理 §5.3 第 2 類），不改變 accepted 語義。對 #14 的修改見第 8.1 節。

## 5. C-14-4 的 disposition（CL-R1-17）：接受

**接受 D-14-8**：存放目錄中名稱符合 `SN-[0-9a-f]{10}.json`、但讀不到、不是合法快照、內容的 `snapshot_id` 與檔名不同或與內容雜湊不符的檔案，使一般模式與一般的 Snapshot Mode 都以 `SnapshotIntegrityError` 停止，不略過。

- 理由：快照是寫入一次、不修改的檔案（7.11 第 1 項），壞檔表示損毀或被改動。略過它可能讓選取結果變成另一個（較舊的）快照而不被發現，與「Snapshot Mode 只讀已保存、驗證過的快照」（DESIGN §4.1）及 H-3／H-4 的 fail closed 不一致。
- 後果：一個壞檔會擋住該目錄的所有規劃，直到騎士處理。這是 fail closed 的已知代價，接受。
- **對 R1-4 的要求**（CL-R1-17，併入 #16 的派工）：R1-4 不得攔下 `SnapshotIntegrityError` 後改用其他快照、改呼叫路線引擎繼續規劃，或把它轉成一般的路線錯誤代碼而隱藏原因；它讓這個例外向上傳遞（停止），例外訊息與 log 不含存放目錄的路徑或檔案內容。向騎士顯示的文字屬之後的整合 Spec（RouteError 的文字不在 SPEC-R1，`derivation-spec-r1.md` 第 2 節），在那之前不得把它呈現為 `snapshot_missing` 或 `routing_unavailable`。

## 6. C-14-5 的 disposition（TI-C14-5）

- 凍結清單項目在 R1-2 的介面是 `FrozenEntry(request_key, snapshot_id, sha256)`（D-14-12；CL-R1-4 只要求三項內容以資料傳入）。欄位名稱是 R1-2 的內部介面，不是檔案格式。
- **歸屬：tracked item `TI-C14-5`，owner＝Design Authority，在 derive E2／凍結 Demo 的 Spec 時處理**：該 Spec 定義凍結清單的檔案格式（`derivation-spec-r1.md` 第 2 節「不屬於本 Spec」），並寫明它的欄位如何對應到這三項（例如 E2 的題目以 `route_id` 指定快照：`RS-` 的十六進位部分等於 `snapshot_id` 的十六進位部分，SPEC-001 §2；清單仍須提供 `request_key` 與檔案的 SHA-256）。該 Spec 可以用不同的欄位名稱再轉換，但不得改變嚴格模式的語義（只用清單指定的快照、核對位元組的 SHA-256、任何不符即停止、不回退）。
- 在那之前它只是 tracked item（治理 §1.2），不阻擋 #14。

## 7. 對 R1-3、R1-4 與之後 Specs 的影響

### 7.1 R1-3（#15）：CL-R1-18 折返位置的整數公尺

SPEC-001 §2 的 `RG-` 雜湊含「實際採用的折返位置（距起點的累計公尺，取整數；不論它是自動判定還是騎士指定的）」，4.1 寫「換算成公尺時四捨五入到整數」，S78 要求兩種來源「換算成公尺後相等時 `route_id` 相同」。這是同一個量，所以兩種來源用同一條取整規則：

1. **四捨五入＝`ROUND_HALF_UP`**（`.5` 進位）。不得使用 Python 內建的 `round()`：它是 half-even（`round(1000.5) == 1000`），與「四捨五入」不同。
2. **騎士指定**：`target_gpx_turnaround_km` 以其最短十進位表示（`Decimal(repr(km))`）乘以 1000，再依第 1 項取整數。不得先以浮點數相乘（`0.5005 * 1000 == 500.49999999999994`，取整後是 500 而不是 501）。
3. **自動判定**：最遠點沿軌跡的累計距離（公尺，浮點數）以其最短十進位表示依第 1 項取整數。
4. CL-R1-10 第 4 項的合法性判斷（0 < m < 軌跡總長）以取整後的整數 m 判定，照舊。
5. `RG-` 的雜湊不經 §2 的 JSON 正規化，CL-R1-14 的捨去**不適用**於這裡。
6. 證據：#15 以測試證明 `.5` 進位（例如 `0.0005` km → 1 m、`1.0005` km → 1001 m、`0.5005` km → 501 m），以及自動判定與騎士指定的整數公尺相等時 `route_id` 相同（S78）。

這是 SPEC-001 已明寫的「四捨五入」與 §2「不論來源」的唯一合理解讀（治理 §3.6-A），不改變 accepted 語義。#15 尚未派工；Orchestrator 派 #15 時把本 record 列入派工內容。

### 7.2 R1-4（#16）：CL-R1-19

1. **採用的檢查以未正規化的值判定。** 起點、終點與中間位置的偏移（≤ 200 m）、中間位置沿線里程的嚴格遞增（CL-R1-7）、道路屬性長度與路線里程的 2% 差異，都以 R1-4 計算出的原值判定，不以 CL-R1-14 正規化後的值判定。正規化只用於雜湊與存檔（`build_snapshot`）。理由：捨去使存入的值不大於原值，以存入的值判定會讓 200.04 m 被當成 200.0 m 而通過（fail open）。#16 以測試證明原值略大於 200 m（例如 200.04 m）時拒收。
2. **`request` 中的經緯度以浮點數放入**（不以整數放入，例如 `121` 要寫成 `121.0`）。理由：CL-R1-14 只作用於浮點數，數值相等的 int 與 float 會得到不同的雜湊（本 record 開頭的探測）。後果只是一般模式找不到可重用的快照（多一次引擎請求），不會誤用快照，但會使 S56 對整數值不成立。
3. **`fetched_at` 不得晚於實際收到回應的時間**（格式化到秒時捨去，不進位），以免 CL-R1-16 使剛存的快照在同一秒內被當成未來的快照。
4. `SnapshotIntegrityError` 的處理依 CL-R1-17（第 5 節）。

### 7.3 之後的 Specs（tracked items，在被接受並授權前不得作為新工作執行，治理 §1.2）

| 代號 | 內容 | Owner |
| --- | --- | --- |
| TI-C14-1 | 詞彙表 Spec（座標定義物件的內容，CL-R1-2）定義座標欄位的型別為浮點數，讀取時把整數值的座標轉成浮點數，使 CL-R1-14 對所有座標成立 | Design Authority（詞彙表／G-RREQ 的 derivation） |
| TI-C14-5 | 凍結清單的檔案格式與 `FrozenEntry` 的對應（第 6 節） | Design Authority（E2／凍結 Demo 的 Spec） |
| — | 壞檔時向騎士顯示的文字（第 5 節） | Design Authority（之後的整合 Spec） |

### 7.4 文字同步（併入 first-run derivation 第 7 節的清單；不是任何裁決生效的條件）

| 代號 | 位置 | 建議 |
| --- | --- | --- |
| RV-8 | SPEC-001 §2「雜湊與正規化」列、5.4「雜湊正規化的精度」列 | 註明 CL-R1-14：以最短十進位表示為準，捨去（向零），定點寫法，零不帶負號；只用於雜湊與存檔，不用於採用的判定 |
| RV-9 | SPEC-001 §2 ID 列的 `RG-`、4.1 `target_gpx_turnaround_km` | 註明 CL-R1-18：四捨五入是 half-up，騎士指定與自動判定用同一條取整規則 |

Owner 與時機同 RV-6、RV-7（`decision-20261118-issue13-c131.md` 第 4 節）：Design Authority，最早在 SPEC-R1 phase acceptance 之後，於 AB-12 的文件工作中執行。

## 8. 對 #14 的具體要求（同一 Ticket、cycle 1；R1 派工之前完成）

### 8.1 可以修改的檔案與內容（封閉清單）

1. `src/moto_copilot/routing/store.py` 的 `find_reusable`：只重用 `timedelta(0) <= now - acquired_at(s) <= REUSE_WINDOW` 的快照（CL-R1-16）；docstring 改寫為同一定義並引用本 record。
2. `tests/test_routing_store.py`：新增測試，證明 (a) 取得時間晚於 `now`（例如晚 1 秒與晚 1 天）的快照不被一般模式重用，結果是 `None`；(b) 同一個快照仍可由一般的 Snapshot Mode 選取（沒有期限）；(c) `now` 恰等於取得時間時可重用（經過時間 0 的邊界）。既有測試不改。
3. 註解與 docstring 的引用：`canonical.py` 中 `_ROUNDING` 上方的註解與 `store.py` 中 `_latest` 的 docstring，可以把「reported for Design Authority confirmation」改為引用本 record（CL-R1-14、CL-R1-15）。只改註解文字。

不得：修改 `_ROUNDING`、`_format_float` 或 S56／S71 的任何測試；修改 Snapshot Mode、嚴格模式、`put`、`load`、壞檔處理或 `request_key`；修改 `src/`、`tests/` 的其他檔案；加任何 xfail／skip。

### 8.2 Evidence（記在 `worklog/issue-14.md`）

| # | 證據 | 要求 |
| --- | --- | --- |
| 1 | D-14-1、D-14-10、D-14-11 與 C-14-1～C-14-5 的狀態 | 改為引用本 record（CL-R1-14～CL-R1-17、TI-C14-5）；C-14-6 維持 acceptor 待決 |
| 2 | E-1 | 修改後的 subject 上完整 pytest 輸出，exit 0，摘要只有 `passed` |
| 3 | 突變 | 拿掉下界（恢復成只檢查上界）時，第 8.1 節第 2 項的新測試失敗 |
| 4 | Diff | 相對 `366866c` 的 diff 只含第 8.1 節列出的檔案與內容 |
| 5 | E-2 | S35 列（存放與選取的部分）加上新測試名稱 |

### 8.3 R1 的派工

Orchestrator 派 #14 的 R1 時，派工內容須含本 record 與 `decision-20261118-issue13-c131.md`。R1 對 H-4 的核對（高風險 record 第 5 節）包含 CL-R1-16 的下界與 CL-R1-15 的確定性；對 C-14-1 核對實作符合 CL-R1-14（以最短十進位表示、向零、定點、零不帶負號），不得把四捨五入記為另一個可接受的實作。

## 9. 是否改變 accepted 語義、boundary、authority、escalation

- **是否改變 accepted 語義：否。** CL-R1-14 寫下的是 S56／S71（Q-3 第 1、5 項裁決的定案測試）唯一能成立的讀法，符合裁決原文「經緯度至少保留小數六位」；CL-R1-15 補上 7.11 第 3 項沒有處理的同時最晚；CL-R1-16 是本 Design Authority 先前寫的 CL-R1-3 的 clarification，符合 5.4「取得時間在 30 天內」的字面；CL-R1-17 接受 Executor 的 fail closed 選擇；CL-R1-18 寫下 SPEC-001 4.1 已明寫的「四捨五入」與 §2「不論來源」的唯一合理解讀；CL-R1-19 使 7.11 第 5、8 項的門檻依原值判定（fail closed）。都不改變 OC-1 的 intent、scope、constraints 或 acceptance semantics（治理 §5.3 第 2 類）。
- **Boundary：在 OC-1 boundary 內。** 全部屬 OC-1 §2.1 第 1 項（`routing`）與 SPEC-R1 已分配的 AB-1、AB-2、AB-10、AB-11、AB-13 部分（`derivation-spec-r1.md` 第 7 節）；沒有新增 Must、requirement 或 AC，沒有恢復 Scope Reduction。
- **需要 acceptor：否**（本 record 的各項裁決）。C-14-6（`aa42392` 歷史中的手寫範例座標是否在 push 前整理，RB-6）保留給 acceptor，本 record 不處理。
- **Escalation：沒有。** 沒有 E-DA/D1 或 D2（第 2.1 節末段）；C-14-2～C-14-5 與 CL-R1-18、CL-R1-19 都可由既有來源與證據裁決。

## 10. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #14（R1-2） | 第 8 節的 targeted 修改後才派 R1。C-14-1 不需要修改；既有 evidence（E-1、E-2 的 S56／S71 列、突變 M1）仍有效。CL-R1-16 的修改使 `find_reusable` 的 evidence 需要第 8.2 節的補充 |
| #15（R1-3） | 派工內容加入本 record；CL-R1-18 是其 AC 的補充證據（第 7.1 節第 6 項） |
| #16（R1-4） | 派工內容加入本 record；CL-R1-17、CL-R1-19 的要求與測試（第 5 節、第 7.2 節） |
| SPEC-R1 的 Spec Integration Audit | SR1-AC2 的整合路徑核對 `snapshot_id`、`request_key`、指紋都經同一條 CL-R1-14 規則；SR1-AC3 核對採用的檢查以原值判定（CL-R1-19 第 1 項）；`RG-` 的整數公尺依 CL-R1-18。SIA 不得把 TI-C14-1、TI-C14-5、RV-8、RV-9 記為已涵蓋 |
| 既有程式（`routes/catalog.py`、`ingest/`、`contracts/`、`pace/`） | 不受影響（第 2.3 節） |
| 高風險類別 | R1-2 的標示（H-2、H-3、H-4）不變；R1-3、R1-4 的標示不變 |
