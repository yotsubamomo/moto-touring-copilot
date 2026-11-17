# Decision record — #10 配速表與契約 3 不變條件 3 的檢查（CL-B1-12）、留一趟的預測速度（CL-B1-13）、`user-` 版本的編號（CL-B1-14）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue10-pace-contract`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 第 6 節事件 20–21）。問題來自 #10 Executor 的 return：worklog `docs/governance/records/worklog/issue-10.md` 第 8 節 C-10-1（blocking）、C-10-2、C-10-3（含第 4 節 D-10-2、D-10-3） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-B1 v1（`derivation-spec-b1.md`）。本 record 是 SPEC-B1 的三則 clarification／修訂（治理 §5.3 第 2 類），編號 **CL-B1-12**（C-10-1）、**CL-B1-13**（C-10-2）、**CL-B1-14**（C-10-3），與 CL-B1-1～CL-B1-7（`derivation-spec-b1.md` §4）、CL-B1-8（`decision-20261117-issue7-spike-tests.md`）、CL-B1-9／10（`decision-20261117-issue9-e1-and-trim.md`）、CL-B1-11（`decision-20261118-issue9-qda1.md`）並列引用。CL-B1-12 修訂 CL-B1-4 第 1、3 項的文字並擴大 #10 的檔案範圍（第 3.4 節） |
| Subject 基準 | 主 checkout branch `oc1-run2-b1-ui0-r1-routing`，HEAD `9e394482e93586703eb8dc2868275d4bd1e00c0a`（#10 實作 commit `be0074d`），工作區乾淨 |
| Issue #10 原文 | 派工所附 scratchpad 檔 `issue-10-body.md`，本 record 實測 SHA-256 `880ef1341e090b86e826cd2a14812ab4a05b634b73385c3ccebea80e43245e65`，等於 BD-3。Issue #7 原文以 `gh issue view 7 --json body` 唯讀取得；Issue #11 原文為 scratchpad 檔 `issue-11-body.md` |
| 依據的條文 | 治理 §1.2、§2.1、§2.4、§2.5（E-DA）、§3.3、§3.4、§3.6（含 A）、§3.8、§5.3；Bindings m3 第 2.4、2.6（RB-7）、3.2、5、7 節；OC-1 §2.1 第 1–3 項、§3.1 AB-3／AB-4／AB-10／AB-11／AB-13、第 121 行（引用文件的變更分類）；`derivation-spec-b1.md` §2、§4 CL-B1-4、§5 #10／#11 列與 E-1～E-5、§6 SB1-AC2／AC3、§8；CL-B1-8 §3.1–§3.4、§7；CL-B1-9 第 3、4 項；`decision-20261117-high-risk-categories.md` §3.3 第 1 項、§3.4 第 3 項、§5 |
| 讀過的證據 | Bindings m3；治理本文 §1.2、§2.1、§2.4、§2.5、§3.3–§3.6、§5.3；OC-1（第 2、3、9 節相關列）；`derivation-spec-b1.md` 全文；`derivation-spec-r1.md` R1-1 列；CL-B1-8、CL-B1-9／10、CL-B1-11（表頭）records；高風險類別 record §3.3、§3.4、§5；run record 第 5、6、8 節；worklog `issue-10.md` 全文；Issue #7、#10、#11 原文；`DESIGN.md` §5 共通規則（「路段類別」列）、契約 1 欄位表與不變條件、契約 3 全文、§6.1 配速表／餘裕係數／分級門檻／版本各段；`src/moto_copilot/contracts/validate.py`（`pace_eligible`、`validate_derived_segments`、`validate_pace_table`、`validate_dataset`）、`schemas.py`（契約 1）；`src/moto_copilot/pace/table.py` 全文；`src/moto_copilot/ingest/segments.py`（`IngestParams.category_scheme`、`_category`）；`tests/test_routes_pace_eta.py`（pace 段）、`tests/test_contracts.py`（契約 3 段與 `validate_dataset` 的使用處）、`tests/test_pace_table.py`（`seg` helper、`test_timed_rows_follow_cl_b1_4_item_1`、`test_the_derived_seg_category_and_category_scheme_are_not_used`）、`tests/fixtures/contract_v02/mock_dataset.json`；參考實作 `experiments/cr01_checks/data_sb2_stop_allowance.py` 第 60–139 行（`fit`、`predict`、留一趟迴圈、`margin`）與 `data_common.py` 的 `tercile_thresholds`（只閱讀，未執行） |

本 record 撰寫時實際執行的（不讀 GPX、不需金鑰；探測程式在 stdin 執行，沒有寫入 repo）：

| 指令 | 結果 |
| --- | --- |
| `git rev-parse HEAD`、`git status --short` | `9e39448…`；乾淨 |
| `sha256sum` Issue #10 原文 | 如上，等於 BD-3 |
| `.venv/Scripts/python.exe -m pytest -q -rxX` | `375 passed, 4 xfailed`；XFAIL 為 S-3（`restored by #10`）與 S-4～S-6（`restored by #11`） |
| 探測：以 mock fixture 的衍生列呼叫 `build_pace_table(..., ["T001","T002"], pace_version="user-01", min_segments=2)`；計算 `pace_eligible` 且屬 `trip_ids` 的列數；`validate_dataset(fixture)` | 表頭 `curv-tercile-20-150`、`margin_coeff` 0.2／`default`；類別路段數 C1 1、C2 2、C3 2，合計 5；合格列 5；fixture 自己的配速表合計 5；`validate_dataset` 四項皆為 `[]` |

沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下任何腳本，沒有讀保留行程。

---

## C-10-1 → CL-B1-12：契約 3 不變條件 3 在「每次建表重算門檻」下的意思與檢查方式

### 1. 問題

`validate_pace_table(header, categories, derived_rows)` 以衍生路段表的 `seg_category` 分組，要求每個類別的 `n_segments` 等於該類別的合格列數（標為 invariant 3）。CL-B1-4 第 3 項規定配速表依重算的門檻重新分類、不用衍生表的 `seg_category`。兩者只在衍生表的分類恰好等於重算分類時一致；`ingest` 以固定門檻分類（`curv-spike0-80-250`），配速表是 `curv-tercile-<c1>-<c2>`，所以一般情形下依 CL-B1-4 正確產生的配速表會被判為違反。直接後果：S-3 無法依 CL-B1-8 §3.2 恢復、#10 的 E-1（CL-B1-9 第 3 項）不滿足；SB1-AC2 的契約 3 步驟同樣會失敗。要裁決的是：不變條件 3 在 CL-B1-4 下的意思、驗證程式該怎麼檢查、修改 `contracts/` 歸誰、S-3 如何恢復。

### 2. 判斷

1. **衝突的來源是 Spike 時代的檢查寫法，不是 DESIGN 的不變條件。** DESIGN §5 契約 3 不變條件 3 的原文是「只使用符合契約 1 不變條件 4 的列」（`quality = ok`、`seg_category` 不是 `null`、`trip_role = pace`），沒有規定逐類別計數。逐類別計數是 v0.2 Spike（`9b3af99` 起即存在，#7 未改動）在配速表直接沿用衍生表類別時的寫法。DESIGN §6.1 與契約 3 的 `category_scheme` 欄（Q-4，2026-11-15）已規定門檻在每次建表時重算，所以配速表的類別是它自己的分類，衍生表的 `seg_category` 只在兩者是同一個分級版本時才與之對應。
2. **DESIGN 明定分級門檻不在契約內。** DESIGN §5 共通規則「路段類別」列：「分級門檻不在契約內，由 `category_scheme` 標示所用的分級版本」。契約 3 不變條件 5、6 也採同一原則：需要產生者的規則才能判定的事，由產生者的測試檢查，不由契約驗證程式檢查。
3. **派生紀錄的疏漏。** `derivation-spec-b1.md` 寫 CL-B1-4 第 3 項與 §8「受影響的工作」時，沒有列出 `validate_pace_table` 依衍生類別計數的檢查會因此失效。本 record 補正；這不是 FA ruling 或 Reviewer finding 推翻的先前決定，是 Executor 依治理 §2.4 回報的契約問題，所以不構成 E-DA/D2。

### 3. 裁決

#### 3.1 不變條件 3 的意思（寫定）

一份配速表可以使用、而且 `n_segments` 所計的列，是表頭 `trip_ids` 的行程中符合契約 1 不變條件 4 的列（下稱「合格列」）。配速表把合格列分到哪個類別，依它自己的 `category_scheme`；衍生表的 `seg_category` 只在衍生表的 `category_scheme` 與配速表的相同時，才代表配速表的分類。

#### 3.2 驗證程式的檢查方式（修改 `validate_pace_table` 的不變條件 3 一段）

帶入衍生路段表時：

1. **合計（一律檢查）**：三個類別的 `n_segments` 合計等於合格列數。不等時回報違反（invariant 3）。
2. **逐類別（同一分級版本時才檢查）**：被計入的合格列，其 `category_scheme` 全部等於配速表表頭的 `category_scheme` 時，另外依衍生表的 `seg_category` 逐類別核對 `n_segments`（現行的檢查與訊息不變）。其他情形不做逐類別核對：驗證程式不解析 `category_scheme`、不還原門檻、不重新分類。
3. 不變條件 2（`trip_ids` 必須都是 `pace`）、`ingest_version` 一致、不變條件 1、4、6、7 的檢查不變。`pace_eligible` 不變。
4. 合計檢查不辨識「一個不合格的列被計入、同時一個合格列被漏掉」這種計數相同的情形；逐類別核對也只是計數。契約沒有逐列的來源欄位，這是驗證程式本來的限制。分類與取列的正確性由產生者的測試涵蓋（#10 AC 3、CL-B1-4 第 1、3 項的測試、`test_suspect_and_invalid_rows_do_not_change_the_pace`），SPEC-B1 的 SIA 與任何結案陳述**不得**宣稱驗證程式核對了重算後的逐類別路段數（H-3 第 3 項）。

#### 3.3 產生者一側的對齊（修訂 CL-B1-4 第 1、3 項）

為使產生者取用的列恰好等於上面的合格列，CL-B1-4 第 1 項改為：

> **可計時的路段**：表頭 `trip_ids` 的行程中，符合契約 1 不變條件 4 的列（`trip_role = pace`、`quality = ok`、`seg_category` 不是 `null`）。這些列的 `curvature_deg_per_km` 是 `null`，或配速表用到的數值欄位（`length_m`、`moving_time_s`、`short_stop_time_s`、`curvature_deg_per_km`）缺漏、不是有限數或超出契約 1 的範圍（`length_m`、`moving_time_s` 須大於 0）時，回報明確的錯誤，不建立配速表、不寫檔；不略過、不補值。

CL-B1-4 第 3 項補一句：「不使用 `seg_category` 與 `category_scheme`」指**分類**；取列時 `seg_category` 不是 `null` 是契約 1 不變條件 4 的條件，照常適用。

理由：DESIGN 不變條件 3 要求只使用合格列；原第 1 項以「曲率不是 `null`」取列，會在 `seg_category` 為 `null`、曲率有值的列上使用不合格的列，也會在 `seg_category` 有值、曲率為 `null` 的列上默默少算一列，使合計檢查失敗。`ingest` 的 `_category` 只在曲率為 `null` 時回傳 `null`，所以真實的衍生表兩者一致，本修訂只改變不一致（不符契約 1 語意）的輸入的處理：改為明確的錯誤（H-4，不以略過掩蓋）。契約 1 的 schema 已要求 `moving_time_s` 有值時大於 0，D-10-8 的「等於 0 時略過」因此改為錯誤。

#### 3.4 歸屬：併入 #10（擴大 #10 的檔案範圍）

- `validate_pace_table` 的修改歸 **#10**，不重開 #7、不另建 Ticket。理由：(a) S-3 的恢復是 #10 的結案條件（CL-B1-8 §3.2），必須在同一個受審 subject 內成立；(b) #7 已在前一個 run 結案，它的 7 項 AC 都不涉及不變條件 3，#7 的 evidence 不受影響；(c) 範圍在 OC-1 §2.1 第 2 項（`contracts` 更新到 v0.3）與第 3 項（Spike 的收編或返工）之內；(d) Issue #7 的排除「`validate.py` 不重算配速或餘裕係數」仍然成立——本裁決的檢查只計數，不重算配速、不重新分類。
- 這是 SPEC-B1 對 #10 的範圍修訂（derived contract，治理 §5.3 第 2 類）。Issue #10 的內文與 8 項 AC 不改（acceptor 對本 run 的指示：不修改 Issues #7–#12）；本 record 與 `derivation-spec-b1.md` §5 #10 列並列引用。

#### 3.5 S-3 的恢復

S-3（`tests/test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract`）在 3.2 的修改後應**不改內文**就通過：fixture 衍生表是 `curv-mock`、#10 的輸出是 `curv-tercile-20-150`，不同分級版本，只做合計檢查；探測結果合計 5、合格列 5。#10 移除它的 strict xfail 標記（`reason` 已不正確）即符合 CL-B1-8 §3.2 第 1 項「新測試不帶標記通過」。可以保留為獨立測試或併回原測試，依 CL-B1-8 §3.2 第 3 項在 worklog 寫明。

不採用的做法：

| 做法 | 不採用的理由 |
| --- | --- |
| (a) 驗證程式依 `category_scheme` 還原門檻、重新分類 | 把分級門檻與 CL-B1-4 第 4 項的格式變成契約 3 的不變條件，與 DESIGN「分級門檻不在契約內」相反，也等於新增其他工作（`routes` 的 RI-2）會依賴的契約基線；驗證程式要複製產生者的分類規則。fixture 的 `curv-mock` 無法解析，只能改寫 fixture 的配速表（連帶改動 #11 的 S-4～S-6 所用的 ETA 期望值）或在無法解析時放行（fail-open） |
| (b) 只核對合計，拿掉逐類別 | 同一分級版本時逐類別核對仍然正確而且較強，沒有理由拿掉；保留它也使既有的 `test_segment_count_counts_only_eligible_rows` 不必改 |
| (c) S-3 改用兩種分類剛好一致的資料 | 遮住衝突，SB1-AC2 與 `validate_dataset` 的真實路徑仍會失敗 |
| (d) S-3 不帶衍生路段表驗證 | 不變條件 2、3 的檢查從 S-3 消失；CL-B1-8 §3.2 第 1 項「只移除標記而讓檢查消失不算恢復」 |

本裁決採用的是 (b) 加上 (a) 不需要的那一部分（同一分級版本時沿用衍生類別），以既有證據（DESIGN §5 的明文、不變條件 5、6 的同一原則、CL-B1-8 §3.2）即可裁決，不構成 E-DA/D1。

### 4. 是否改變 accepted 語義

**否。** DESIGN 契約 3 不變條件 3 的文字與意思不變；本裁決改的是 Spike 時代的檢查程式，使它符合該不變條件與 DESIGN §6.1、Q-4 已核准的「每次建表重算門檻」。CL-B1-4 第 1 項的修訂使 DA 自己的 clarification 回到 DESIGN 不變條件 3 的字面。沒有新增或移除 OC-1 的 Must、AB 或 gate；AB-13「pytest 全數通過」與 SB1-AC3 仍按 CL-B1-8 §3.2 第 5 項字面判定。

### 5. Boundary determination

在 OC-1 boundary 內：OC-1 §2.1 第 1 項（`pace`、`tests`）、第 2 項（`contracts` 的 v0.3）、第 3 項（Spike 的收編或返工）；SPEC-B1 已分配的 AB-3、AB-10、AB-11、AB-13 部分。只用合成資料與既有 fixture（OC-1 §2.3）。不需要 acceptor。

---

## C-10-2 → CL-B1-13：留一趟每一折的預測所用的速度

### 6. 裁決

**確認 D-10-2。** CL-B1-4 第 6 項的「以同一個 `min_segments` 建立該折的配速」指：以其餘行程、依 #10 建立配速表的同一個程序（同一個函式路徑）得到的類別值，也就是該折假設建表時會寫進類別紀錄的值——`speed_kmh` 取到小數兩位（與配速表相同），`stop_ratio` 不捨入（與配速表相同，D-10-7）。預測＝Σ `length_m` ÷ `speed_kmh` × (1 + `stop_ratio`)。

理由：
- DESIGN §6.1 的餘裕係數比較「實際騎乘時間」與「預測的 `RIDE`」；`RIDE` 由 ETA 以配速表的 `speed_kmh` 與 `stop_ratio` 計算（Issue #11 的算式、契約 4 不變條件 8）。以同一組值作預測，`r` 才是 ETA 實際使用的預測量的殘差。
- DESIGN 契約 3 與 §6.1：`research-` 與 `user-` 用「同一個建立程序與同一條餘裕係數規則」。
- CL-B1-4 指定的參考實作只涵蓋門檻（`tercile_thresholds`）、分類邊界（`_category`）與餘裕係數的取值規則（`margin`），**不包括** `fit`／`predict`；參考實作的 `fit` 用未捨入的中位數（本 record 已閱讀第 67–83 行核對），這不約束第 6 項。
- 差異是相對 0.01 km/h 的量級，只在 `r₃` 恰好落在 0.05 的倍數附近時可能改變結果；另一種讀法不構成後果實質不同的合理設計，不是 E-DA/D1。

影響：#10 的實作（`loo_folds` 用 `_category_pace`）已符合，不需修改。真實資料上與 `experiments/cr01_checks/` 檢查結果的比較屬回歸檢查（G-REG），不在 SPEC-B1；若之後比較，邊界上的差異以本條為準解釋，不視為缺陷。

---

## C-10-3 → CL-B1-14：`user-` 版本的編號與「同一版本」的判定

### 7. 裁決

1. **確認：`user-` 版本不接受呼叫者指定的編號**（`ValueError`）。DESIGN 契約 3「依建立順序遞增」、§6.1「編號在兩種開頭各自遞增」，CL-B1-4 第 8 項只允許 `research-` 指定編號（SB2-T13 的凍結腳本用途）；允許 `user-` 指定編號會使編號不再反映建立順序。只有一種合理解讀。
2. **確認：同一個開頭、同一個數值，不論補零位數，是同一個版本。** 寫入時以數值判定已存在，已存在就報錯、不寫（現行實作）。理由：DESIGN 以編號表示建立順序、以「編號較大者」作 `built_at` 相同時的選擇依據（CL-B1-4 第 9 項），兩個字串同數值會使「最大編號＋1」與「編號較大者」沒有唯一答案；以數值判定是 fail closed（H-3 不覆寫、H-4）。
3. **由第 2 項帶出的要求（#10）**：`latest_user_pace_table` 在目錄中發現同一個數值有一個以上的 `user-` 檔案（例如 `user-04.json` 與 `user-004.json`，只可能由 `create_pace_table` 以外的方式產生）時，回報明確的錯誤，不自行挑選；現行實作在 `built_at` 也相同時依目錄列舉順序取第一個，結果不確定。CL-B1-4 第 8 項「一個版本一個檔案」。`create_pace_table` 遇到這種目錄時已因「已存在」拒絕對應的編號，自動編號仍取最大數值＋1，不需修改。

是否改變 accepted 語義：否（第 1、2 項是既有來源唯一合理的讀法；第 3 項是同一讀法在選用路徑的 fail-closed 後果，不新增 AC 語義）。Boundary：在 OC-1 boundary 內（AB-3、AB-11 的 `pace` 部分），不需要 acceptor。

---

## 8. 對 #10 的具體要求（targeted rework，同一 Ticket、同一 cycle 的實作階段；R1 尚未派工）

| 檔案 | 要求 |
| --- | --- |
| `src/moto_copilot/contracts/validate.py` | 只改 `validate_pace_table` 中「帶入衍生路段表」的不變條件 3 一段，依第 3.2 節：合計一律檢查；被計入的合格列 `category_scheme` 全部等於表頭時，另做現行的逐類別核對。不解析 `category_scheme`。其他函式與檢查不變；模組說明可補一句不變條件 3 的檢查方式 |
| `src/moto_copilot/pace/table.py` | (1) `timed_rows` 依修訂後的 CL-B1-4 第 1 項：取列條件改為合格列（加上 `seg_category` 不是 `null`）；合格列的曲率為 `null` 或數值欄位不合法時報錯，`moving_time_s` 等於 0 也報錯（取代 D-10-8）。(2) `create_pace_table` 寫入前的契約 3 核對**帶入衍生路段表**（`validate_pace_table(header, categories, rows)`），使寫出的檔案在不變條件 2、3 上也經過檢查。(3) `latest_user_pace_table` 依 CL-B1-14 第 3 項。`loo_folds` 不變（CL-B1-13）；`compare_methods` 不在本次範圍（第 10 節） |
| `tests/test_contracts.py` | 新增測試（合成資料或 fixture 的副本）：(i) 不同分級版本、合計等於合格列、逐類別與衍生類別不同 → 不變條件 3 沒有違反；(ii) 不同分級版本、合計多計一列（例如計入 suspect 列）或少計一列 → 違反；(iii) 同一分級版本、合計相同但逐類別不符 → 違反（逐類別核對仍在）；(iv) `trip_ids` 以外的行程與保留行程的列不被計入合格列。既有測試不改；若改，E-4 逐項寫明 |
| `tests/test_pace_table.py` | `test_timed_rows_follow_cl_b1_4_item_1` 中「`quality = ok`、`seg_category` 有值、曲率 `null`」的列改為預期錯誤（E-4 寫明理由引用本 record）；新增：合格列曲率為 `null` 時 `build_pace_table`／`create_pace_table` 報錯且目錄沒有檔案；曲率有值而 `seg_category` 為 `null` 的列不被使用；至少一個「衍生分類與重算分類不同」的合成案例，`create_pace_table` 寫出的表通過 `validate_pace_table(header, categories, rows)`；同數值兩個 `user-` 檔案時 `latest_user_pace_table` 報錯 |
| `tests/test_routes_pace_eta.py` | 移除 S-3 的 strict xfail 標記，內文不改（第 3.5 節）；S-4～S-6 不動 |
| `docs/governance/records/worklog/issue-10.md` | 引用 CL-B1-12～14；E-2 加入上列測試；E-4 列出修改的既有測試；C-10-1～3 標為已裁決 |

不改：`tests/fixtures/contract_v02/mock_dataset.json`、`tests/conftest.py`、`pyproject.toml`、`ingest/`、`routes/`、`DESIGN.md`、任何 Issue 內文。

**#10 的 E-1**：依 CL-B1-9 第 3 項——摘要只有 `passed` 與 `xfailed`，xfail 只有 S-4～S-6（`restored by #11`，不超過 3 個），`tests/` 中沒有 `restored by #10` 的標記；`--runxfail` 的範圍為 `tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py tests/test_pace_table.py tests/test_contracts.py`，失敗的恰好是 S-4～S-6 且只涉及 `stop_allow_s`。完整輸出記在 worklog。

**高風險類別**：#10 原有的 H-2、H-3、H-4 標示不變，新增的修改落在其中：驗證程式的合格列計數守著「不得使用保留行程、suspect、invalid 的列」（H-3 判定 3.3 第 1 項），取列時的缺漏處理是 H-4 判定 3.4 第 3 項。R1 的最低核對範圍除高風險類別 record §5 外，須看到：第 3.2 節第 1、2 項各有通過與違反的測試；不同分級版本時計入 suspect／invalid／保留行程／`trip_ids` 以外的列會被判為違反；合格列曲率為 `null` 時是明確錯誤而且沒有寫檔；`validate.py` 的 diff 只涉及不變條件 3 一段。

## 9. 對其他 work items 與 evidence 的影響

| Work item／evidence | 影響 |
| --- | --- |
| #7 B1-1（前一 run 已結案） | 不重開。它的 AC 與 evidence 不涉及不變條件 3，不受影響；`validate.py` 的這次修改由 #10 的 R1 與 SPEC-B1 的 SIA 審查 |
| #11 B1-4 | 不變。E-1 依 CL-B1-9 第 3 項（字面全數通過）。它的測試以 fixture 的配速表（`curv-mock`）為輸入，不受第 3.2、3.3 節影響 |
| SPEC-B1 SIA：SB1-AC2 | 解除阻擋：`ingest`（`curv-spike0-…`）→ `user-` 配速表（`curv-tercile-…`）的契約 3 檢查走合計核對，依修訂後的 CL-B1-4 可以通過。注意：(1) 這條路徑上驗證程式只核對合計，逐類別的正確性由 #10 的產生者測試證明（第 3.2 節第 4 項），SIA 不得記為驗證程式已逐類別核對；(2) SB1-AC2 的路線須是 `category_scheme` 與配速表相同的**合成契約 2 紀錄**——`routes` 產生的目錄仍是 `curv-spike0-…`，依門檻重建路線類別屬 RI-1～RI-3，不在 SPEC-B1（`derivation-spec-b1.md` §6 末段），不得宣稱已涵蓋 |
| SPEC-B1 SIA：SB1-AC3 | `validate_dataset` 對 mock fixture 走同一分級版本（`curv-mock`）的逐類別核對，結果與現在相同（探測為 `[]`）。仍依 CL-B1-8 §3.2 第 5 項字面判定 |
| R1-1（#13，SPEC-R1） | 同樣修改 `contracts/validate.py`（契約 2 與 ID 樣式），與不變條件 3 一段不重疊。並行度 1；後執行者以含前者的 HEAD 為 BASE，不得回復對方的修改 |
| 既有 evidence | `be0074d`／`9e39448` 上的 `375 passed, 4 xfailed` 與 worklog E-1 是 #10 的中間結果，不是最終 E-1 證據。E-2 中以 `validate_pace_table(..., rows)` 核對的兩個測試在修改後仍應通過（分類剛好一致，合計也一致） |
| C-10-5（fixture 配速表不再由其衍生列重建） | 資訊，維持現狀：fixture 的配速表是契約資料的樣本，`validate_dataset` 以同一分級版本核對它；它不宣稱是 #10 的輸出 |

`derivation-spec-b1.md` 與先前的 CL records 沒有被修改；SPEC-B1 v1 的引用集合由本 record 補上 CL-B1-12～14，CL-B1-4 第 1、3 項以本 record 第 3.3 節為準。Orchestrator 與 Reviewer 以本 record 路徑引用（#10 R1 的 bounded pack 須包含本 record）。

## 10. 附帶：C-10-4（`compare_methods`）

不在本次派工的三個問題內，只記處理：`compare_methods` 是 DC-10 在正式 E1 前選擇方法用的比較，仍以衍生表的 `seg_category` 分組，它的輸出不寫入配速表，不在 Issue #10 與 SPEC-B1 的 AC 內。#10 不修改它。它若之後用於 E1 的方法選擇，分組方式應與配速表相同，屬凍結清單與實驗的工作（SPEC-B1 §2「不屬於本 Spec」），由屆時的 Spec 處理；在那之前是 tracked item。

## 11. 需要其他 authority 的事項

無。三項裁決都不改變 accepted 語義，都在 OC-1 boundary 內，不需要 acceptor；不觸發 escalation（第 3.5 節末、第 6 節末、第 7 節）。真實行程上的行為仍是 NOT VERIFIED（RB-7，required authority = acceptor），不在本 record 範圍，維持 worklog 的記載。

本 record 只執行了開頭表格中的指令；沒有修改程式、測試、Spec、Issue 或其他 record，沒有派工任何 subagent，沒有 commit。
