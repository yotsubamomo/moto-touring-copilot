# Decision record — C-13-1：契約 2 v0.3 之後，v0.2 Spike 的 `build_route` 產出不符合契約（CL-R1-12）；C-13-2 ID 樣式的語義（CL-R1-13）；C-13-4 文件同步

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue13-c131`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 第 6 節事件 61）。問題來自 #13（SPEC-R1 R1-1）Executor 的 return `NEEDS_DA`：worklog `docs/governance/records/worklog/issue-13.md` 第 8 節 **C-13-1**（blocking）、**C-13-2**、**C-13-4**（non-blocking） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-R1 v1（`derivation-spec-r1.md`）的修訂／clarification **CL-R1-12**（R1-1 的範圍）與 **CL-R1-13**（ID 樣式的語義），治理 §5.3 第 2 類。與 CL-R1-1～CL-R1-11 並列引用 |
| Subject 基準 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `2e9c52f5339f331cb67ac886868086543bb0510e`；#13 的實作 commit `153adcadfdf02f3697ba47f8912ac444c1a3f8d3`，之後只有 record-only commit（`git diff --stat 153adca HEAD` 只含 worklog 與 run record）；`git status --short` 為空 |
| 依據的條文 | 治理 §1.2、§2.4、§2.5（E-DA）、§3.4、§3.6、§4.7、§5.3；Bindings m3 第 2.4、2.6（RB-7）、3.2、4、5、7 節；OC-1 §2.1 第 2、3、6 項、§3.1 AB-12、AB-13、§4.1；`derivation-spec-r1.md` §2、§5（E-1～E-6、R1-1 列）、§6、§8；`derivation-spec-b1.md` §8；`decision-20261117-oc1-first-run-derivation.md` 第 6 節 G-RTE 列、第 7 節、末段「`routes` 的 Spike 這次不動」；`decision-20261117-issue7-spike-tests.md`（CL-B1-8）；`decision-20261118-issue10-c107.md`（CL-R1-11）；`decision-20261118-spec-b1-phase-acceptance.md`；`decision-20261117-high-risk-categories.md` §3.4 |
| 讀過的證據 | Bindings m3 全文；治理本文上列各節；OC-1 全文；`derivation-spec-r1.md` 全文；`derivation-spec-b1.md` 全文；CL-B1-8 record 全文；CL-R1-11 record 表頭與章節；SPEC-B1 phase acceptance record 中涉及 `routes`、pytest 與 v0.3 的段落；first-run derivation 的 G-RTE、RV、Spike 段落；高風險 record §3.4；worklog `issue-13.md` 全文；run record 事件 61；Issue #13 原文（scratchpad `issue-13-body.md`，SHA-256 重算 `d432868613aac749018d14bf79e45ca06673508e9e3e8d9919c34bd432456584`，與派工所述相同）；`DESIGN.md` §4.1 路線工具段、§5 v0.3 前言與契約 2；`docs/spec/SPEC-001-plan-schema.md` §2 的 ID 列；`src/moto_copilot/routes/catalog.py`、`routes/__init__.py`；`src/moto_copilot/contracts/schemas.py` 的樣式；`tests/test_routes_pace_eta.py` 第 1–130 行 |

本 record 撰寫時實際執行的（不讀 GPX、不需金鑰；探測程式放在 session scratchpad，只用 `tests/` 的合成幾何 `straight()`，沒有寫入 repo；執行後 `git status --short` 仍為空）：

| 指令／探測 | 結果 |
| --- | --- |
| `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`（HEAD `2e9c52f`） | `1 failed, 874 passed`；唯一失敗 `tests/test_routes_pace_eta.py::test_build_route_conforms_to_the_catalog_contract`，與 worklog E-1 相同 |
| `grep -rn "xfail\|skip" tests/` | 0 筆 |
| `git log -- src/moto_copilot/routes/catalog.py` | 只有 `9b3af99`（v0.2 基準）；#7–#13 都沒有修改 |
| `git diff 1fd1de3 HEAD -- tests/test_routes_pace_eta.py src/moto_copilot/routes` | 空 |
| `build_route` 的呼叫者（`src/`、`tests/`、`app/`） | 只有 `routes/__init__.py` 的匯出與 `tests/test_routes_pace_eta.py` 的兩個測試；`src/` 沒有產品路徑呼叫它；`tests/test_integration_b1.py`、`tests/test_eta.py` 用手寫的路線紀錄，不用 `build_route` |
| 以記憶體中的副本驗證：`build_route("R09", …, straight(6_300), source_trip_id="T900", …)` 的路線紀錄加上三個欄位的各種組合，呼叫 `validate_route_catalog` | 原樣：三項 `required property`。`trip`／`null`／`one_way` → `[]`。`trip`／`null`／`round_trip` → 不變條件 4（沒有 `turnaround`）。`routing`、`target_gpx` → AC (3)（`R09` 不是 `RS-`／`RG-`）。**在 `build_route` 現有的輸出下，三個欄位只有一組合法值** |
| Python `re.search`：SPEC-001 的字面樣式 `^(R\d{2}\|R[SG]-[0-9a-f]{10})$` 與 `schemas.ROUTE_ID_PATTERN` | 字面樣式接受 `"R01\n"`、`"R١٢"`（阿拉伯–印度數字）、`"RS-0123456789\n"`；`ROUTE_ID_PATTERN` 三者都拒絕，`"R01"`、`"RS-0123456789"` 都接受 |
| `re.search(schemas._TRIP_ID["pattern"], "T001\n")` | 成立（C-13-2 的現象屬實） |

沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有讀或執行 `experiments/` 下任何檔案，沒有讀保留行程。

---

## 1. 問題

R1-1 把契約 2 的路線紀錄升到 v0.3：`route_source`、`snapshot_id`（可為 null）、`trip_type` 成為必填欄位，並加上不變條件 4、5 與 AC (3) 的 ID 一致性。v0.2 Spike 的路線目錄產生者 `routes/catalog.py::build_route` 產生的路線紀錄沒有這三個欄位，所以既有測試 `test_build_route_conforms_to_the_catalog_contract` 失敗。兩項要求在 #13 無法同時按字面成立：

- R1-1 AC (5)「既有測試全數通過」與共通證據 E-1（pytest「全數通過」）；
- R1-1 的排除「路線目錄的產生與檢查點的編號規則」，以及 first-run derivation 末段「`routes` 的 Spike 這次不動」（`derivation-spec-b1.md` §8 的同一句是 SPEC-B1 對自身影響的陳述）。

要裁決的是：#13 怎麼處理這個測試，使它能依 E-1 結案，或寫明另行的合法處置。

## 2. C-13-1 的裁決（CL-R1-12）

### 2.1 選項的比較

| 做法 | 判斷 |
| --- | --- |
| (b) strict xfail，留給之後的 `routes` Spec（G-RTE） | **不採用。** (1) 沒有可以恢復它的 Ticket：G-RTE 在 first-run derivation 第 6 節標為「未 ready」，尚未 derive；CL-B1-8 的 xfail 之所以可行，是恢復點（#9–#11）在同一份 Spec 之內、結案條件可以機械追蹤。這裡的 xfail 會留過 SPEC-R1 的 Spec Integration Audit 與 phase acceptance，成為沒有負責 Ticket 的標記。(2) SPEC-R1 分配到 AB-13 的「本 Spec 的 pytest」；AB-13 的完成條件是 pytest「全數通過」，CL-B1-8 §3.3 第 5 項已確立 xfail 不得陳述為通過。留下 xfail，SPEC-R1 就無法按字面滿足 AB-13 的分配部分，要嘛 SIA 記 FAIL，要嘛需要重新解釋「全數通過」——後者是 accepted 語義（OC-1 §3.1），也牽涉 Bindings 第 5 節 release gate，都不是 DA 能放寬的。(3) xfail 不分原因：同一測試的其他四個斷言（段數、尾段處理、類別、檢查點）會一起被遮住 |
| 在測試中替 `build_route` 的輸出補上欄位、刪除測試，或改寫斷言 | **不採用。** 測試會證明一件不成立的事（`build_route` 的輸出符合 v0.3），或讓 `build_route` 唯一的契約符合性檢查消失（CL-B1-8 §4 的同一理由） |
| 為 `build_route` 新增 `route_source`／`trip_type` 參數或產生 `turnaround` | **不採用。** 那是路線目錄產生方式的設計，屬 G-RTE，也正是 R1-1 排除的內容 |
| (a) 在 `build_route` 的路線紀錄補上 `route_source: "trip"`、`snapshot_id: null`、`trip_type: "one_way"`，其他一律不動 | **採用**，理由見第 2.2 節 |

不採用 (a) 的主要顧慮是 CL-B1-8 §4 拒絕過「在 #7 先讓 Spike 輸出新欄位」。那個拒絕有兩個理由，這裡都不成立：
- CL-B1-8 的值（`short_stop_time_s = 0`）是補出來的資料值，不是停等事件的計算結果；這裡的三個值不是資料，而是 `build_route` 既有結構的描述，而且由契約唯一決定：它要求 `source_trip_id`（必填的 `str`），只建立起點與終點兩個檢查點，沒有 `turnaround`；依不變條件 4、5 與 AC (3)，對 `R` 加兩位數字的路線只有 `trip`／`null`／`one_way` 合法（本 record 開頭的探測）。DESIGN §4.1 也寫明 `trip` 是「由騎過的行程裁切」的路線，`build_route` 的模組說明是「several trips ride in the same direction」的一段，即單向。
- CL-B1-8 的產生者修正在同一份 Spec 的後續 Tickets 內；這裡沒有任何 ready 的 Ticket 會修 `build_route`。

所以本問題可以由證據裁決，不構成 E-DA/D1；也沒有先前的 DA 決定被 FA ruling 或 Reviewer finding 推翻，不構成 D2。

### 2.2 裁決

**CL-R1-12（R1-1 的範圍修訂）。** R1-1 的範圍加入一項：

> (f) **契約 2 v0.3 的輸出符合性（只限既有產生者的路線紀錄）**：`src/moto_copilot/routes/catalog.py` 的 `build_route` 回傳的路線紀錄加上 `"route_source": "trip"`、`"snapshot_id": None`、`"trip_type": "one_way"`。這三個值描述 `build_route` 現有的結構（取自行程、單向、沒有折返點），不是預設值，也不是新的路線目錄規則。

R1-1 的排除「路線目錄的產生與檢查點的編號規則」**不變**，並明確為：路段的切法、類別、檢查點的種類與編號、`common_stretch`／`align_to_route`、`build_route` 的介面與參數，以及路線目錄如何由 `routing`／`target_gpx` 的路線或來回行程建立，仍全部屬 G-RTE；本修訂不收編 `routes` 的 Spike（OC-1 §2.1 第 3 項），也不建立 G-RTE 要依賴的設計基線。G-RTE 可以重寫或取代 `build_route`，本修訂的三個值不約束它。

first-run derivation 末段「`routes` 的 Spike 這次不動」與 `derivation-spec-b1.md` §8 的同一句，對 `build_route` 路線紀錄的這三個鍵與模組說明（第 5.1 節）不再適用；其餘照舊。兩份 record 本身不修改，以本 record 路徑引用。

R1-1 的 AC (1)–(5) 不變；AC (5)「既有測試全數通過」維持字面意義。

### 2.3 與 E-1、SPEC-R1 Spec Integration Audit 的關係

- #13 的 E-1 以字面判定：pytest exit 0，摘要只有 `passed`；`failed`、`error`、`xfailed`、`xpassed`、`skipped` 都不出現。**不得以 xfail 或 skip 處理本問題**，`tests/` 中不得出現任何 xfail／skip 標記。
- SPEC-R1 的 Spec Integration Audit 對 SR1-AC1 與 AB-13 的分配部分，核對同一件事：最終 subject 的 pytest 全數通過、沒有 xfail／skip 標記；並核對 `routes/catalog.py` 相對 BASE `1fd1de3` 的 diff 只含第 5.1 節允許的內容。SIA 不得把路線目錄、檢查點或 `routes` 的收編記為 SPEC-R1 已涵蓋（`derivation-spec-r1.md` §6 末段已列為不在涵蓋內）。

## 3. C-13-2 的裁決

### 3.1 D-13-1 符合 SPEC-001 §2（CL-R1-13）

**符合。** SPEC-001 §2 的 ID 列以文字定義三種 ID 的語言——「`R` 加兩位數字」「`RS-`／`RG-` 加 10 個小寫十六進位字元」「`<route_id>-CP` 加兩到三位數字，依路線順序由 01 起編」「`SN-` 加 10 個小寫十六進位字元」——並以樣式記號書寫。這些 ID 全部由系統產生：`R01`／`R02` 是 fixture，`RS-`／`RG-`／`SN-` 取自 SHA-256 的十六進位字串，檢查點由 01 起編。依這些產生規則，ID 只會是 ASCII 字元組成的完整字串；「`R01` 後面接一個換行」或「以阿拉伯–印度數字寫的 `R١٢`」都不是 SPEC-001 所定義的 ID。這是既有來源唯一合理的解讀。

Python `re` 的 `\d` 比對 Unicode 數字、`$` 比對結尾換行之前（本 record 開頭的探測），把字面樣式原封不動交給 jsonschema（以 `re.search` 執行 pattern）會接受定義之外的字串。D-13-1 改寫成 `[0-9]` 並在 `$` 後加 `(?!\n)`，使程式接受的字串集合恰好等於定義的語言；在 ECMA-262（JSON Schema pattern 的語法）下兩種寫法接受的字串相同。它是同一個樣式的忠實實作，不是語義的改變，也沒有新增 requirement。

**CL-R1-13（SPEC-R1 全部 Tickets）。** SPEC-001 §2 與 R1-1 範圍 (a) 的 ID 樣式，語義是「完整字串、ASCII 數字、小寫十六進位」：任何驗證或產生 `route_id`、`checkpoint_id`、`snapshot_id` 的程式都不得接受結尾換行、前後空白或非 ASCII 數字。程式怎麼寫是 Executor 的 HOW（例如重用 `contracts.schemas` 的三個常數）；Tickets 以測試證明拒絕這些值。

### 3.2 `trip_id`、`datetime` 的既有樣式

- **現象屬實**：`_TRIP_ID`（`^T\d{3}$`）接受 `"T001\n"`；`_DATETIME` 有同樣的 `\d`／`$` 寫法。它們屬契約 1、3、4（共通規則），不屬 R1-1 範圍（R1-1 範圍 (a) 只列 `route_id`、`checkpoint_id`；`snapshot_id` 在 (b)），#13 **不修改**。
- **Disposition：tracked item `TI-C13-2`**，owner＝Design Authority。依 CL-R1-13 的同一解讀，這兩個樣式應同樣收緊；它在 OC-1 §2.1 第 2 項（`contracts` 的 v0.3）之內，不是新的 requirement。處理方式二擇一：(1) 由 Design Authority 在下一份會修改 `contracts/` 的 derivation 中納入一張 Ticket 或一項範圍（並在那時判定高風險類別：`trip_id` 是保留行程清單的鍵，須評估 H-3）；(2) acceptor 若要提早處理，以直接指示作為 Lightweight 單點修正的 Outcome Contract（Bindings 第 4 節）。在那之前它只是 tracked item，不得作為新工作執行（治理 §1.2）。
- 對既有工作：產生 `trip_id` 與時間的都是系統程式（行程清單、`ingest`、`pace`），沒有證據顯示目前有產生帶換行或非 ASCII 數字的值；本 record 不對 SPEC-B1 的 phase acceptance 作任何變更。SPEC-R1 的 SIA 不得把 `trip_id`、`datetime` 的樣式記為已收緊。

## 4. C-13-4 的 disposition

`DESIGN.md` §5 的 v0.3 前言（「`src/moto_copilot/contracts/` 的驗證程式與契約測試仍然依 v0.2 檢查」）、契約 2 的 `kind` 列與不變條件 4、5 的「草稿，待 Ticket 實作」／「草稿」，以及 §9.1 `contracts` 列、§9.3「驗證程式仍依 v0.2 檢查」，在 #13 結案後與實作不一致；SPEC-001 §2 的樣式記號需要 CL-R1-13 的註記。

- **#13 不修改 `DESIGN.md` 或 `docs/spec/`**（不在 R1-1 範圍；Executor 的派工也禁止）。
- **Disposition：併入 first-run derivation 第 7 節的文字同步清單**，新增兩項（同樣不是任何裁決生效的條件，由之後的 Spec 修訂或 AB-12 的文件工作處理，修改 `DESIGN.md` 要在相應的 work item 內進行）：

| 代號 | 位置 | 建議 |
| --- | --- | --- |
| RV-6 | `DESIGN.md` §5 v0.3 前言、契約 2 的 `kind` 列與不變條件 4、5、§9.1 `contracts` 列、§9.3 最小資料契約段 | 依實際狀態改寫：`contracts` 的驗證已依 v0.3 檢查（R1-1 結案後）；`turnaround` 與不變條件 4、5 已在驗證程式實作，但路線目錄的產生（`routes`）仍是 v0.2 Spike，只依 CL-R1-12 補上三個欄位，`turnaround` 的產生待 G-RTE。不得寫成路線目錄已依 v0.3 產生 |
| RV-7 | SPEC-001 §2 的 ID 列 | 註明 CL-R1-13：樣式以 JSON Schema（ECMA-262）語義解讀，完整字串、ASCII 數字；Python 實作不得接受結尾換行或非 ASCII 數字 |

- **Owner 與時機**：Design Authority 負責把 RV-6、RV-7 排入文件工作（OC-1 §2.1 第 6 項、AB-12）；最早在 SPEC-R1 phase acceptance 之後執行，以免 R1-2～R1-4 尚未完成時寫出過早的狀態。文件同步之前，任何狀態報告都以程式與紀錄為準，不得引用 `DESIGN.md` §5 的「依 v0.2 檢查」作為現況，也不得宣稱文件已同步。
- 不阻擋 #13 的結案，也不阻擋 SPEC-R1 的 SIA（SR1-AC1～AC5 不含文件同步）。

## 5. 對 #13 的具體要求（同一 Ticket、cycle 1；R1 派工之前完成）

### 5.1 可以修改的檔案與內容（封閉清單）

只有 `src/moto_copilot/routes/catalog.py`，而且只限：
1. `build_route` 建立的 `route` dict 加上三個鍵：`"route_source": "trip"`、`"snapshot_id": None`、`"trip_type": "one_way"`。
2. 可以加一行註解說明這三個值的依據並引用本 record（`decision-20261118-issue13-c131`，CL-R1-12）。
3. 模組說明第一行可以把「data contract v0.2, contract 2」改為說明路線紀錄帶有契約 2 v0.3 的欄位、而路線目錄的建立仍是 Pre-Spec Spike（G-RTE）的文字；不得寫成 `routes` 已依 v0.3 或已收編。

不得：改 `build_route` 的簽名或新增參數；改路段、檢查點、`common_stretch`、`align_to_route` 或任何其他程式；新增 import；修改 `routes/__init__.py`；修改 `tests/test_routes_pace_eta.py` 或任何其他測試（`test_build_route_conforms_to_the_catalog_contract` **原文不動**，由它驗證：依第 2.1 節，`validate_route_catalog` 對這條路線只接受 `trip`／`null`／`one_way`，所以這個測試通過即證明三個值都正確）；加任何 xfail／skip；修改 `contracts/` 已完成的部分（除非 R1 finding 要求）。

### 5.2 Evidence（記在 `worklog/issue-13.md`）

| # | 證據 | 要求 |
| --- | --- | --- |
| V-1 | E-1 | `.venv/Scripts/python.exe -m pytest -q` 的完整輸出：exit 0，摘要只有 `passed`（依現況預期 875 個；數目不同時照實寫並說明） |
| V-2 | 沒有標記 | `grep -rnE "xfail\|pytest\.mark\.skip" tests/` 的輸出：0 筆 |
| V-3 | 修改範圍 | `git diff --stat 153adca <新 commit>` 只含 `src/moto_copilot/routes/catalog.py`（record-only 路徑除外）；`git diff 153adca <新 commit> -- src/moto_copilot/routes/catalog.py` 全文，只含第 5.1 節的內容；`git diff 1fd1de3 <新 commit> -- tests/test_routes_pace_eta.py` 為空 |
| V-4 | AC (5) | E-2 表的 AC (5) 改為達成，引用 V-1；contracts CLI 照常 exit 0 |
| V-5 | E-5 | 寫明 `test_build_route_conforms_to_the_catalog_contract` 沒有修改；`catalog.py` 的修改列在 Work performed 與 Artifacts，理由引用 CL-R1-12 |
| V-6 | E-6 | 高風險類別仍為「不涉及」：三個常數鍵不改變 `build_route` 讀取的資料、輸出位置或任何位置資訊（H-1、H-2）；不碰保留行程、實驗或宣稱（H-3）；不是高風險 record §3.4 判定 1–5 的程式，三個值不是缺漏時的預設值（H-4） |
| V-7 | C-13 欄 | 第 8 節 C-13-1、C-13-2、C-13-4 的狀態改為引用本 record（CL-R1-12、CL-R1-13、TI-C13-2、RV-6、RV-7） |

依 SA-1 在 topic branch 作本機 commit；commit 前確認暫存的內容不含 `.env`、GPX、FIT 或 `data/`。之後由 Orchestrator 依 Bindings 第 3.3、3.7 節派 #13 的 R1；R1 的 pack 須包含本 record，R1 的審查範圍涵蓋 `catalog.py` 的 diff 與第 5.2 節的證據。

## 6. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #13 R1-1 | 範圍加 (f)（CL-R1-12）；依第 5 節修正與記錄。Issue #13 內文不改（Issue 與 derivation record 不一致時以 derivation record 及其 clarifications 為準）。worklog E-1 的 `1 failed, 874 passed`（subject `153adca`）是修正前的結果，不作為結案證據 |
| R1-2、R1-3、R1-4 | CL-R1-13 適用：它們產生的 `snapshot_id`、`RS-`／`RG-` 的 `route_id` 與任何 ID 格式檢查，以測試證明拒絕結尾換行與非 ASCII 數字（各自 AC 中 S58 的部分）。R1-4 的共用介面回傳 `route_source`、`trip_type`，不產生路線目錄紀錄，CL-R1-12 對它沒有影響。各 Ticket 的派工 pack 須包含本 record |
| SPEC-R1 Spec Integration Audit | 依第 2.3 節：pytest 全數通過、沒有 xfail／skip；`catalog.py` 的 diff 限於第 5.1 節；不得把路線目錄、`routes` 的收編、`trip_id`／`datetime` 樣式或文件同步記為已涵蓋 |
| G-RTE（之後的 `routes` Spec） | 擁有 `build_route` 的返工或取代、`turnaround` 與來回路線的目錄建立、檢查點編號、RI-1～RI-3（SPEC-B1 phase acceptance 第 5 節的規劃決定仍適用）。CL-R1-12 的三個值不是它的基線 |
| SPEC-B1（已 phase accepted） | 沒有影響：`build_route` 不在 SPEC-B1 的任何證據中（SB1-AC2 的整合測試用手寫的路線紀錄）；`test_rule3.py` 的匯入限制不受影響（第 5.1 節禁止新增 import） |
| `experiments/` 中呼叫 `build_route` 的腳本 | **NOT VERIFIED**：本 record 的可讀範圍不含 `experiments/`，沒有檢查。這些腳本本 run 不執行；路線紀錄多出三個鍵是附加的變更。之後執行它們的 work item（E1／E2 的 Spec）自行確認 |
| 文件 | RV-6、RV-7（第 4 節）；TI-C13-2（第 3.2 節） |

`derivation-spec-r1.md`、`derivation-spec-b1.md`、first-run derivation 與先前的 CL records 沒有被修改；SPEC-R1 v1 的引用集合由本 record 補上 CL-R1-12、CL-R1-13，Orchestrator 與 Reviewer 以本 record 路徑引用。

## 7. 是否改變 accepted 語義

**否。**
- OC-1 的 scope 已包含 `contracts` 的 v0.3（§2.1 第 2 項）與 `routes` Spike 的收編或返工（§2.1 第 3 項）；在 `routes/catalog.py` 的輸出加上契約要求的三個欄位，不超出 scope，也沒有新增 Must、Should、AC 或 invariant。
- AB-13「pytest 全數通過」按字面保留；本 record 選擇的做法正是為了不需要重新解釋它。Bindings 第 5 節的 release gate 沒有被解釋或放寬。
- CL-R1-12 是 derived contract（R1-1 的範圍）的修訂，CL-R1-13 是既有來源唯一合理解讀的 clarification，都屬治理 §5.3 第 2 類；TI-C13-2、RV-6、RV-7 是 tracked items，不是新工作。
- 沒有豁免任何 audit，沒有改變任何高風險類別的標示。

## 8. Boundary determination

**在 OC-1 boundary 內。** 依據：OC-1 §2.1 第 2、3 項；SPEC-R1 R1-1 已分配的 AB-2、AB-13 部分；修改只在 `src/moto_copilot/routes/catalog.py` 的三個常數鍵與說明文字，測試仍只用合成資料（OC-1 §2.3）。不涉及 RB-1～RB-7。**不需要 acceptor。**

## 9. 需要其他 authority 的事項

- **無需 acceptor。** 唯一的例外情形：acceptor 若選擇以 Lightweight 提早處理 TI-C13-2，須由 acceptor 直接指示（第 3.2 節）。
- **沒有 escalation**：不構成 E-DA/D1 或 D2（第 2.1 節末段）。
- C-13-3（Executor 的程序偏差）不在本次派工的問題之內，本 record 不作判斷；依 worklog 的建議由 Orchestrator 處理。

本 record 只執行了開頭表列的唯讀指令與 scratchpad 內的記憶體探測；沒有修改程式、測試、Spec、`DESIGN.md`、Issue、worklog 或其他 record，沒有派工任何 subagent，沒有 commit。
