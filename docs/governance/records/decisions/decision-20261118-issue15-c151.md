# Decision record — C-15-1：騎士指定的折返位置落在兩個軌跡點之間時的切開（CL-R1-22）；C-15-2 的 disposition（CL-R1-23）；R1-4 使用目標 GPX 結果的要求（CL-R1-24）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue15-c151`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（派工內容引用 run record 事件 81）。問題來自 #15（SPEC-R1 R1-3）Executor 的 return `NEEDS_DA`：worklog `docs/governance/records/worklog/issue-15.md` 第 7 節 **C-15-1**（blocking）、C-15-2、C-15-3（non-blocking） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-R1 v1（`derivation-spec-r1.md`）的 clarifications **CL-R1-22～CL-R1-24**，治理 §5.3 第 2 類。與 CL-R1-1～CL-R1-21 並列引用；CL-R1-22 是 CL-R1-10 第 4、6 項與 CL-R1-18（`decision-20261118-issue14-c141.md` 第 7.1 節）的 clarification，不取代它們 |
| Subject 基準 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `6df0cc8`；#15 的 implementation subject `b771d9feabe2984caf8f636b930e0e86798a0bd4`（之後只有 record-only commit）；`git status --short` 為空。本 DA 在 HEAD 上執行 `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`：`1607 passed`（只是本裁決的背景觀測，不是 #15 的 E-1） |
| 讀過的依據 | 治理 §1.2、§2.1、§2.4、§2.5、§3.3–§3.6、§5.3；Bindings m3 第 2.4、2.6（RB-7）、3.2、5、7 節；`derivation-spec-r1.md` 第 2、4（CL-R1-5、CL-R1-7、CL-R1-10）、5（R1-3、R1-4 列）、6 節；`decision-20261118-issue14-c141.md`（CL-R1-14、CL-R1-18、CL-R1-19）；`decision-20261118-issue14-qalt1.md`（CL-R1-21）；`decision-20261117-high-risk-categories.md` §3.4、§5；SPEC-001 §2 ID 列、4.1 `target_gpx_turnaround_km`、4.12、4.13、5.4、5.5、7.11 第 2、3、5 項、第 9 節 S10、S14、S27、S43、S58～S64、S78～S80；SPEC-RESOLUTION-001 §2.2、§2.8；lead 處置 §8.2、§9.1～§9.4、§9.12；`DESIGN.md` §5（含路線目錄建立的第 2 步：目標 GPX 的切開）；Issue #15 原文（scratchpad，`sha256sum` 重算為 `a54f8034cdadd143e6a1ec594ee7d74e01bb47ce9bc13bd21537bbcf92fd5ad7`，與派工內容相同）與 Issue #16 原文；`src/moto_copilot/routing/target_gpx.py`、`src/moto_copilot/ingest/geometry.py`、`src/moto_copilot/routing/__init__.py`、`tests/test_target_gpx.py`（相關段落） |
| 資料 | 沒有讀取、列出或搜尋 `data/`；沒有讀或執行 `experiments/`；沒有讀 `.env`。探測只用合成的點，以 stdin 執行，沒有寫入 repo |

## 1. 問題

來回行程、終點回到起點、騎士給了 `target_gpx_turnaround_km` 時，CL-R1-18 第 2 項把它換成整數公尺 m，第 4 項以 `0 < m < 軌跡總長` 判定合法。CL-R1-10 第 4 項寫「以沿軌跡 m 公尺處為折返點」，R1-3 範圍 (b) 要求在折返點把幾何切成去程與回程。軌跡的累計距離是浮點數，m 是整數，所以 m 幾乎總是落在兩個軌跡點之間；但 S64（lead 處置 §8.2 的 Q3-T12，acceptor 裁決時列出的測試）寫「**任何情形下**都沒有反轉或補造的軌跡點」，7.11 第 2 項寫「系統不推定、不反轉，也不補造回程」。

現行實作（`b771d9f`）只在 m 剛好等於某點的累計距離時切開，其他情形拋 `TurnaroundSplitUndecidedError`。S61、S80 的一般情形，以及 S78 經由完整流程的騎士指定部分，都被擋住。要裁決的是：切在哪裡；去程與回程是否都含分界點；`turnaround_m` 與 `RG-` 記哪一個公尺數。

## 2. C-15-1 的裁決（CL-R1-22）

### 2.1 選項的判斷

| 選項 | 判斷 |
| --- | --- |
| (a) 在 m 處內插一個點 | **不採用。** 內插的點是檔案中沒有的點，放進去程的最後一點與回程的第一點，就是輸出中的「補造的軌跡點」。S64 的「任何情形下」不留例外；它是 acceptor 裁決時列出的測試，Ticket 與 Executor 不得改變它的 PASS／FAIL 語義（治理 §3.4）。採用 (a) 等於改變 accepted 的測試語義，是 contract change（治理 §5.3 第 1 類），不在 Design Authority 的權限內。另外，(a) 在 S78 的典型情形下，同一個 `route_id` 會對應兩種幾何：自動判定切在最遠點，騎士指定的同一個整數公尺切在相距不到 0.5 m 的內插點。Executor 的 D-15-4 在取樣時內插，取樣點不進入輸出，這與 (a) 不同，不受本裁決影響 |
| (b) 最接近 m 的軌跡點 | **採用**，加上第 2.2 節的可用條件與同距離時的規則。它不新增點，S64 字面成立；它是不補造點的前提下離騎士指定位置最近的實現，最符合 7.11 第 2 項 (i)「以那個位置為折返點」與 S61「以那個位置切開」；自動判定也一律切在檔案中的點（最遠點），兩種來源有同一個不變條件：每一段都是檔案中連續、同向的一段 |
| (c) m 之後（含 m）的第一點；(d) m 之前（含 m）的最後一點 | **不採用。** 兩者都不補造點，但會把折返點系統性地往後或往前移，最大可達一整段（≤ 1 km）；沒有任何來源支持這種方向上的偏差。(b) 的偏移不超過 (c)、(d) 中較小的一個 |

「實際採用的折返位置」記哪一個公尺數：SPEC-001 §2 ID 列與 lead 處置 §9.1 都寫 `RG-` 含「**實際採用**的折返位置（距起點的累計公尺，取整數；不論它是自動判定還是騎士指定的）」，並要求「相同的有效折返點得到相同的 `route_id`；不同的折返點得到不同的 `route_id`」。切在某個軌跡點時，實際採用的折返點就是那個點；記 m 會讓兩個不同的 m 切在同一點時得到兩個 `route_id`，違反「相同的有效折返點得到相同的 `route_id`」。所以記那個點的整數公尺，取整依 CL-R1-18 第 3 項（與自動判定同一條規則）。

### 2.2 規則（CL-R1-22；R1-3）

適用：`trip_type = round_trip`，終點與起點相距不超過 200 m，而且騎士給了 `target_gpx_turnaround_km`。

記號：軌跡點 `p_0 … p_{n-1}`（檔案順序）；`cum_i` 是 `p_0` 到 `p_i` 沿軌跡的累計距離（相鄰點 haversine 的和，D-15-2）；`total = cum_{n-1}`；`D_i = Decimal(repr(cum_i))`；`c_i = D_i` 依 `ROUND_HALF_UP` 取整（CL-R1-18 第 1、3 項）。

1. **m 與合法性照舊。** m 依 CL-R1-18 第 2 項取得；`0 < m < total` 才合法（CL-R1-18 第 4 項），否則 `target_gpx_not_round_trip`（`turnaround_unconfirmed`），不退回自動判定（lead 處置 §9.12 末段）。m 只用於合法性與第 3 項的選點，不進入 `RG-` 的雜湊。
2. **可用的軌跡點。** 同時符合 `0 < cum_i < total` 與 `0 < c_i < total` 的點。（這使分界點不是起點或終點，兩段都至少有兩點、長度都大於 0，而且 `RG-` 的整數公尺是正整數，滿足 `target_gpx_route_id` 的輸入檢查。）
3. **選點。** 折返點是可用的點中 `|D_i − m|` 最小的 `p_k`；有多個時取**索引最小**的一個。比較以 `Decimal` 精確進行，不以浮點數的差比較。m 剛好等於某點的 `D_i` 時就是那一點（距離 0），涵蓋現行 `_point_at_exactly` 的情形；重複的點（相同累計距離）取第一個，與自動判定「多個最遠點時取第一個」一致。具體寫法（例如在 `cum` 上 `bisect` 再比較兩側的可用點）是 Executor 的 HOW，但結果必須等於本項的定義。
4. **沒有可用的點時** 回傳 `target_gpx_not_round_trip`（`turnaround_unconfirmed`），不回傳路線、不拋其他例外。依第 3.1 節的 haversine 三角不等式，通過點數、相鄰距離、總長與終點檢查的來回軌跡一定有可用的點（若沒有，所有點的累計距離都在 0.5 m 以內或總長附近，中間只有一步大跨越，而那一步的兩端分別接近起點與終點，相距不超過約 201 m，與總長至少 1 km 矛盾）；本項只是防禦，Executor MAY 以替換 `cum` 的方式測試它。
5. **實際採用的折返位置＝`c_k`。** `turnaround_m = c_k`，`route_id = RG-`（檔案 SHA-256 `:round_trip:` `c_k`，CL-R1-10 第 6 項）。`turnaround_source = "rider"`。`c_k` 可以不等於 m；兩個不同的 m 選到同一點時 `route_id` 相同，選到不同點時不同。
6. **自動判定不變。** 折返點是最遠點 `p_F`，`turnaround_m = c_F`（CL-R1-18 第 3 項）。自動判定的分界套用同一個可用條件（現行的 `0 < c_F < total` 檢查，加上偵測成立時後段至少 100 m 所保證的 `cum_F < total`），不可用時 `turnaround_unconfirmed`。
7. **切開與分界點。** 去程 `= (p_0 … p_k)`，回程 `= (p_k … p_{n-1})`：**兩段都含分界點 `p_k`**，它是去程的最後一點、回程的第一點。各段的點是檔案中的同一組點、原順序；不反轉、不新增、不移動、不刪除，也不去掉兩段共用的那一點。去程長度 `= cum_k`，回程長度 `= total − cum_k`。理由：7.11 第 2 項與 `DESIGN.md` §5（路線目錄建立的第 2 步）要求「折返點是路段邊界」、去程與回程分開切段；分界點若只放在一段，`p_{k-1}–p_k` 或 `p_k–p_{k+1}` 那一段的距離會從兩段之中消失，去程加回程不再等於總長（4.12 `distance_m`「來回行程是去程加回程」）。共用的分界點不是補造的點：去程與回程依序相接、去掉一次分界點，正好是檔案的全部點（S64 的機械檢查）。這與 D-15-7 一致。
8. **單向** 照 CL-R1-10 第 3 項：幾何原樣使用，不使用折返位置，不套用本規則。

### 2.3 與各條文的一致性

| 條文 | 一致性 |
| --- | --- |
| S64、7.11 第 2 項「不推定、不反轉、不補造」 | 輸出的點全部是檔案中的點，依原順序；沒有內插點。成立 |
| S61「環狀的 GPX 指定折返位置後以那個位置切開」；7.11 第 2 項 (i) | 切在最接近那個位置的可用軌跡點；位置合法時一定回傳路線，不再停止。軌跡點之間沒有被記錄的位置，所以軌跡點就是「那個位置」在這份檔案上的實現。偏移的上限見第 2.4 節 |
| S80、7.11 第 2 項 (i)「騎士指定優先」 | 合法的 m 一律依第 3 項選點，不退回自動判定；選到的點可能剛好是最遠點（稀疏的軌跡上），這時仍是 `turnaround_source = "rider"` |
| S78「自動判定與騎士指定換算成公尺後相等時 `route_id` 相同」 | 騎士給 `m = c_F` 時，`|D_F − m| ≤ 0.5`，而且 `D_F = m − 0.5` 是唯一可以等於 0.5 的情形（half-up）。選到的 `p_k` 滿足 `|D_k − m| ≤ |D_F − m|`：若 `< 0.5`，`c_k = m`；若兩者都是 0.5，只可能是 `D_F = m − 0.5`、`D_k = m + 0.5`，同距離取索引小的，也就是 `p_F`。所以 `c_k = c_F`，`route_id` 相同。本 DA 以合成的去回軌跡（相鄰間距 0.2～300 m 的隨機組合）探測 957 個偵測成立的案例，`c_k ≠ c_F` 的案例為 0。`D_i` 隨索引不減（`repr` 的單調性），比較以 `Decimal` 精確進行，所以這個推論在實作上成立 |
| CL-R1-10 第 4 項「以沿軌跡 m 公尺處為折返點」 | 依本規則讀成「以累計距離最接近 m 的可用軌跡點為折返點」。這是本 DA 先前文字的 clarification |
| CL-R1-10 第 5 項 | 不變 |
| CL-R1-10 第 6 項、SPEC-001 §2、lead 處置 §9.1 | 「折返位置的整數公尺」＝實際採用的點的 `c_k`。相同的有效折返點得到相同的 `route_id` |
| CL-R1-18 第 1～5 項 | 第 1、2、4、5 項不變；第 3 項（累計距離以最短十進位表示 half-up）延伸到騎士指定時選到的點。第 6 項的證據要求不變，另加第 4 節的完整流程測試 |
| CL-R1-14 | 不適用：選點、合法性與 `RG-` 都不經 §2 的 JSON 正規化 |

### 2.4 已知的限制（不是本裁決引入的，SIA 不得記為已涵蓋）

- **偏移。** 採用的折返點與騎士指定的 m 之間的距離不超過所在線段的一半；在起點或終點附近、最近的點不可用時，最多可達一整段。accepted 的門檻允許相鄰點相距到 1 km（5.4），所以稀疏的檔案（例如只有路線點）上偏移可達數百公尺。結果的 `turnaround_m` 如實記錄採用的位置；騎士原本的請求保留在規劃請求的 `target_gpx_turnaround_km`（4.1，結果中以 `adopted_conditions` 回顯）。兩者不同時要不要、如何向騎士顯示，是之後整合 Spec 的事（TI-C15-1）。
- **整數公尺的解析度。** 兩個不同的分界點，累計距離取整後相同時（相距不到 1 m），`RG-` 相同而幾何相差不到 1 m。這來自 acceptor 裁決的「累計公尺，取整數」（§9.1），任何一種切法都有；本規則已使騎士指定時的分界只取決於 m，自動判定與騎士指定在 S78 的情形下也得到同一個 `c`。

### 2.5 與 R1-4 的偏移與順序檢查（CL-R1-7、CL-R1-19）的關係

- CL-R1-7（起點、終點、中間位置的偏移與沿線順序）與 7.11 第 5～8 項的採用檢查只適用於路線引擎的路線。目標 GPX 的路線不呼叫引擎（7.11 第 3 項 (a)），沒有請求位置，也不做國道檢查（7.11 第 5 項末句；4.12 跨欄位規則：`freeway_check` 是 `null`）。R1-4 不得對目標 GPX 的各段套用這些檢查（CL-R1-24 第 3 項）。
- 引擎的來回路線是兩次獨立的請求，去程的最後一點與回程的第一點各自接近目的地；目標 GPX 的兩段共用同一個分界點。兩者在共用介面上的形狀相同（各方向一條有序的折線），只是後者的分界點完全相同。
- CL-R1-19 的原則（判定以原值進行，不以正規化後的值）在 R1-3 的對應是：合法性以整數 m 與浮點的 `total` 比較，選點以 `D_i` 與 m 精確比較，都不使用 CL-R1-14 正規化後的值。

### 2.6 E-DA 的判斷

- **不構成 E-DA/D1。** (a) 由 S64 的字面與治理 §3.4（Ticket 不得改變 AC 的 PASS／FAIL 語義）排除；(b)～(d) 之間，「以那個位置」與 7.11 第 2 項 (i) 支持偏移最小的 (b)，(c)、(d) 的方向偏差沒有任何來源；`turnaround_m` 記哪一個由 §2 的「實際採用」與 §9.1 的「相同的有效折返點得到相同的 `route_id`」決定。現有證據足以裁決。
- **不構成 E-DA/D2。** CL-R1-10 第 4 項與 CL-R1-18 沒有被 FA ruling 推翻，也沒有被經 route 的 Reviewer finding 以證據爭議；C-15-1 是 Executor 提出的契約充分性問題。

## 3. C-15-2 的 disposition（CL-R1-23）：接受

**CL-R1-23（R1-3；CL-R1-10 第 1、2 項的 clarification）。**

1. **檔案讀不到**（不存在、是目錄、無法開啟）、**不是 XML**、**根元素不是 GPX 的 `gpx`**、**任何一點的 `lat`／`lon` 缺少、不是數字、不是有限值或超出 ±90／±180**：都是 `target_gpx_invalid`。依據：4.13 的情形「讀不到軌跡點」包含整份檔案讀不到點；5.5 這個代碼的 `actions`「確認檔案路徑與內容」明示路徑與內容的問題屬於它；路線錯誤代碼維持六個（4.13），不新增。
2. **壞點使整份檔案不採用，不略過。** 略過壞點會改變幾何（相鄰距離、總長、折返點），與「不補造、不推定」（7.11 第 2 項）及 H-4 的 fail closed 一致的做法是整份不採用。
3. **GPX 1.0 與 1.1 的命名空間都接受。** CL-R1-10 第 1 項沒有限制版本；兩版的 `trk`／`trkseg`／`trkpt`、`rte`／`rtept` 與 `lat`／`lon` 屬性結構相同。其他命名空間或沒有命名空間的檔案不讀（`target_gpx_invalid`），這是保守的 fail closed，接受。
4. `case` 字串（`unreadable`、`malformed_point` 等）是 R1-3 的內部情形，不是新的路線錯誤代碼；它不得被呈現為第七個代碼，也不得被當作 `target_gpx_not_round_trip` 的兩種情形之一。
5. `TypeError`（路徑或位元組的型別錯誤）與 `TripTypeRequiredError`、`ValueError`（行程型態）是呼叫端的錯誤，不是路線錯誤代碼（D-15-12）；照現狀。

`src/moto_copilot/ingest/geometry.py` 不需要修改。觀測（不是要求）：解析使用 `xml.etree.ElementTree`，不解析外部實體；本環境的 expat 是 2.5.0（Python 3.11.2），含實體展開的防護；檔案是騎士在本機提供的，不另列 tracked item。

## 4. 對 #15 的具體要求

### 4.1 可以修改的檔案

| 檔案 | 修改 |
| --- | --- |
| `src/moto_copilot/routing/target_gpx.py` | (1) 以 CL-R1-22 第 2～5 項取代 `_point_at_exactly` 與其呼叫處；`turnaround_m` 與 `RG-` 用 `c_k`。(2) 刪除 `TurnaroundSplitUndecidedError`（不再有未決的情形）。(3) 自動判定的分界套用同一個可用條件（第 6 項；行為不變）。(4) 模組說明、`_round_trip` 與新函式的 docstring 改寫成 CL-R1-22 的定義並引用本 record，刪除「pending a Design Authority decision」等文字。說明 50 m／100 m／90% 是保守的啟發式、沒有以真實資料驗證的文字保留（H-3） |
| `src/moto_copilot/routing/__init__.py` | 只移除 `TurnaroundSplitUndecidedError` 的 import 與 `__all__` 項目；需要時調整說明文字 |
| `tests/test_target_gpx.py` | 刪除或改寫 `test_a_legal_turnaround_between_track_points_is_held_for_the_design_authority` 與其他使用 `TurnaroundSplitUndecidedError` 的測試；新增第 4.2 節的測試。既有以 `_with_exact_cumulative` 替換累計距離的測試可以保留，但 S61、S78、S80 必須另有**不替換累計距離**的完整流程測試 |
| `docs/governance/records/worklog/issue-15.md` | record-only：見第 4.3 節 |

`src/moto_copilot/ingest/` 下的檔案與其他模組不修改。

### 4.2 測試（全部合成資料，在測試中產生）

| 編號 | 內容 |
| --- | --- |
| T-1（S61） | 環狀軌跡，m 嚴格落在兩點之間：較接近後一點時切在後一點，較接近前一點時切在前一點；回傳路線，`turnaround_m = c_k`（並且至少一個案例中 `c_k ≠ m`），`route_id == target_gpx_route_id(ref, "round_trip", c_k)` |
| T-2（S80） | 明確去回同路的軌跡，騎士的合法 m 不等於 `c_F` 而且落在兩點之間：切在 CL-R1-22 選到的點，不是最遠點；`turnaround_source == "rider"` |
| T-3（S78，完整流程） | 不替換累計距離、最遠點的累計距離不是整數的合成去回軌跡：自動判定的結果，與騎士給 `c_F / 1000` km 的結果，`turnaround_m` 與 `route_id` 相同；兩個不同的 m 選到同一點時 `route_id` 相同；選到不同點時不同；同一檔案的單向與來回不同 |
| T-4（選點的定義） | 以替換 `cum` 或直接測試選點的函式：同距離時取索引小的（例如 `cum` 中有 `m − 0.5` 與 `m + 0.5`）；重複的點取第一個；最近的點是起點（m 在第一段內）時取第一個可用點；最近的點是終點時取最後一個可用點；`0 < cum_i` 但 `c_i = 0` 的點不可用；沒有可用的點時是 `turnaround_unconfirmed` |
| T-5（性質測試） | 在環狀與去回兩種軌跡上，以固定間隔掃過 `1 … ⌈total⌉ − 1` 的整數 m（例如每 37 m）：每一個合法的 m 都回傳路線，不拋例外；選到的 `k` 等於測試中依 CL-R1-22 第 2、3 項逐點計算的結果（以 `Decimal` 為 oracle）；每條路線都通過 T-6 |
| T-6（S64，所有回傳路線） | 每段都是檔案中連續、同向的一段；去程的最後一點與回程的第一點是同一點；去程＋回程去掉一次分界點等於檔案的全部點；去程長度 `== cum_k`、回程長度 `== total − cum_k`；沒有任何不在檔案中的點 |
| T-7（既有行為的回歸） | 不合法的 m（0、負數、取整為 0、等於或超過總長、NaN、無限大）仍是 `turnaround_unconfirmed`，不退回自動判定；終點沒有回到起點時即使給了 m 也是 `end_not_at_start`；單向不使用 m |

突變檢查（記在 E-6，H-4）至少包括：同距離時取索引大的；改成 (c)「≥ m 的第一點」；改成 (d)「≤ m 的最後一點」；`route_id`／`turnaround_m` 改用 m 而不是 `c_k`；拿掉可用條件（允許起點或終點作分界）；在 m 處內插一點；以浮點數的差比較距離（若現有測試無法區分，寫明理由）。每一項都要被測試抓到，抓不到時補測試。

### 4.3 Evidence 與 commit

1. **Commit。** 一個與 `b771d9f` 分開的 implementation commit，只含第 4.1 節的三個程式與測試檔，message 註明 CL-R1-22。它成為 #15 新的 implementation subject。worklog 另以 record-only commit。
2. **E-1。** 在新 subject 上 `.venv/Scripts/python.exe -m pytest -q` 的完整輸出，全數通過；`grep -rnE "xfail|pytest\.mark\.skip" tests/` 為 0 筆。
3. **E-2。** S61、S78、S80 改為 PASS 並列出 T-1～T-3、T-5 的測試名稱；S64 列加上 T-6 涵蓋新的切法；S27、S43、S59、S60、S62、S63、S79、S58、S10 照舊並在新 subject 上重新確認；CL-R1-18 第 6 項的列加上 T-3。各列註明 CL-R1-22。
4. **E-5。** 刪除或改寫的既有測試逐項列出理由（本 record）。
5. **E-6。** H-4：第 4.2 節的突變檢查結果；H-2：結果與錯誤仍不含路徑與檔名（既有測試在新 subject 上通過）；H-3：說明文字仍寫明啟發式門檻沒有以真實資料驗證。真實目標 GPX 的行為仍是 NOT VERIFIED（required authority = acceptor，RB-7）。
6. **Worklog。** D-15-7（切開）維持並引用 CL-R1-22 第 7 項；D-15-8 改寫為 CL-R1-22；D-15-6 引用 CL-R1-23；C-15-1～C-15-3 的狀態改為引用本 record；第 8 節剩餘工作更新。

### 4.4 #15 的 R1

Orchestrator 派 #15 的 R1 時，派工內容須含本 record、`decision-20261118-issue14-c141.md`（CL-R1-18）與 `decision-20261118-issue13-c131.md`（CL-R1-13）。R1 對 C-15-1 核對實作符合 CL-R1-22（最接近、可用條件、同距離取索引小、以 `Decimal` 精確比較、`c_k`、兩段共用分界點），不得把 (a)、(c)、(d) 或「記 m」記為另一個可接受的實作。

## 5. 對 R1-4（#16）的要求（CL-R1-24；回應 C-15-3）

**CL-R1-24（R1-4；R1-4 範圍 (f) 共用介面對 `target_gpx` 來源的要求，併入 #16 的派工）。** `TargetGpxRoute` 的欄位名稱與形狀是 R1-3 的 HOW；#16 MAY 直接使用或轉換成共用介面的型別，但：

1. **原樣帶出** R1-3 的結果：`route_id`、`route_source = "target_gpx"`、`trip_type`、`target_gpx_ref`、`snapshot_id = null`、各方向的幾何（點與順序原樣，含兩段共用的分界點）與長度、目標 GPX 的折返位置（＝`turnaround_m`，即 CL-R1-22 實際採用的 `c_k` 或自動判定的 `c_F`；單向為 `null`）。單向只有 `outbound`，來回依序 `outbound`、`return`（與 4.14 的 `legs` 順序一致）。目標 GPX 沒有道路名稱：道路名稱是空清單（4.12「取不到名稱時是空清單」），不得以其他資訊補上。`turnaround_source` MAY 帶出，只作說明，不參與任何識別。
2. **不得重新計算**：不重新選折返點、不以騎士的 km 重算 `turnaround_m` 或 `route_id`、不反轉、不重排、不正規化、不去除重複、不刪除共用的分界點、不內插。
3. **不得套用引擎路線的處理**：目標 GPX 不呼叫路線引擎或道路屬性查詢，不經 R1-2 的選取或存放（不產生、不讀取快照），不做國道檢查、警告、偏移與順序的檢查（7.11 第 3 項 (a)、第 5 項末句；4.12 跨欄位規則；第 2.5 節）。
4. **錯誤原樣傳出**：`TargetGpxError` 的 `code` 就是路線錯誤代碼，`case` 必須保留到之後組裝文字的 Spec（S14：`target_gpx_not_round_trip` 的兩種情形各用 5.5 的一則文字）；不得轉成 `routing_unavailable` 或其他代碼，也不得改用自動判定或其他路線來源。`TripTypeRequiredError`、`ValueError`、`TypeError` 照原樣向上傳遞，不轉成路線錯誤代碼（追問由之後的流程處理）。
5. 結果、錯誤與 log 不含目標 GPX 的路徑與檔名（CL-R1-10 第 7 項，不變）。
6. **#16 的證據**：以合成 GPX 經共用介面走單向與來回（含騎士指定、落在兩點之間的折返位置）：欄位等於直接呼叫 R1-3 的結果；傳輸層與存放的替身沒有被呼叫；`target_gpx_invalid` 與 `target_gpx_not_round_trip` 的兩種情形經共用介面原樣傳出。#16 的派工內容須含本 record。

## 6. 對 SPEC-R1 Spec Integration Audit 的影響

- SR1-AC2：以合成 GPX 走目標 GPX 的單向與來回時，經 R1-4 共用介面的結果符合 CL-R1-22（騎士指定落在兩點之間時切在最接近的可用點、兩段共用分界點、`RG-` 用 `c_k`）與 CL-R1-24 第 1～4 項；`RG-` 通過 R1-1 的樣式檢查。
- SR1-AC3：目標 GPX 的錯誤沒有產生路線、沒有快照、沒有被轉成其他代碼。
- SR1-AC4：路徑與檔名不出現在整合路徑的輸出、錯誤與 log。
- SR1-AC5：新增的文字沒有把去回同路的自動辨識稱為已驗證。
- SIA 不得把下列項目記為已涵蓋：真實目標 GPX 的結果（NOT VERIFIED，RB-7）；第 2.4 節的兩項限制；TI-C15-1；之後 `routes` 的切段與檢查點（G-RTE）；RV-11。

## 7. Tracked items 與文字同步

Tracked items（在被接受並授權前不得作為新工作執行，治理 §1.2）：

| 代號 | 內容 | Owner |
| --- | --- | --- |
| TI-C15-1 | 之後組裝 RouteSummary／文字的整合 Spec 決定：騎士指定的折返位置與實際採用的 `turnaround_m` 不同時，是否以及如何向騎士顯示（例如「折返點在距起點 x km 的軌跡點」）；顯示的折返位置必須是實際採用的值 | Design Authority（整合 Spec 的 derivation） |

文字同步（併入 first-run derivation 第 7 節的清單；不是任何裁決生效的條件）：

| 代號 | 位置 | 內容 |
| --- | --- | --- |
| RV-11 | SPEC-001 4.1 `target_gpx_turnaround_km`、§2 ID 列的 `RG-`、7.11 第 2 項 (i) | 註明 CL-R1-22：騎士指定的位置以累計距離最接近的可用軌跡點實現，不內插；`RG-` 用該點的整數公尺；兩段共用分界點 |

## 8. 是否改變 accepted 語義、boundary、authority 與 escalation

- **是否改變 accepted 語義：否。** CL-R1-22 是 S64（「任何情形下都沒有…補造的軌跡點」）與 7.11 第 2 項 (i)、S61（「以那個位置切開」）同時成立的唯一讀法：不補造點，就只能切在檔案中的點，而離指定位置最近的點是「那個位置」在這份檔案上最接近的實現；合法性（`0 < m < 總長`）、騎士優先、不退回自動判定、`RG-` 含「實際採用的折返位置」都不變。它是本 DA 先前的 CL-R1-10 第 4、6 項與 CL-R1-18 第 3 項的 clarification（治理 §5.3 第 2 類），不建立其他工作依賴的新設計基線：R1-4 依賴的形狀（各方向的有序折線、折返位置、`route_id`）不變。CL-R1-23 寫下 4.13、5.5 與 fail closed 的唯一合理解讀；CL-R1-24 是 7.11 第 3 項 (a)、第 5 項與 4.12 跨欄位規則對 R1-4 的直接結果。都不改變 OC-1 的 intent、scope、constraints 或 acceptance semantics，不新增 Must、requirement 或 AC。被排除的 (a) 才會改變 accepted 語義（S64）；若之後有人主張應以內插精確落在 m，那是 contract change，須經 acceptor，不在本 record 的範圍。
- **Boundary：在 OC-1 boundary 內。** 依據同上；範圍是 SPEC-R1 R1-3、R1-4 已分配的 AB-2、AB-10、AB-13 部分（`derivation-spec-r1.md` 第 7 節），沒有擴張。
- **需要 acceptor：否。** 沒有接受、授權或 reserved boundary 的缺口。真實目標 GPX 的驗證需要私有資料授權（RB-7），維持 NOT VERIFIED，不是本裁決的條件。
- **Escalation：沒有**（第 2.6 節）。

## 9. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #15（R1-3） | 依第 4 節修改；新的 implementation subject 取代 `b771d9f`。既有 evidence（E-1 的 `1607 passed`、E-3、E-4、23＋2 項突變檢查）保留為歷程，在新 subject 上依第 4.3 節重新取得 E-1、E-2、E-6。之後由 Orchestrator 派 R1（第 4.4 節） |
| #16（R1-4） | 派工內容加入本 record；CL-R1-24 的要求與證據（第 5 節）。#16 依賴 R1-3，結案與 SPEC-R1 SIA 以 #15 的最終 subject 為準 |
| SPEC-R1 的 Spec Integration Audit | 第 6 節 |
| 之後的 Specs | `routes`（G-RTE）以兩段共用的分界點作為折返的路段邊界（7.11 第 2 項，不是新的要求）；整合 Spec 處理 TI-C15-1 |
