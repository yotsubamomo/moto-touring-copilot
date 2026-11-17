# Decision record — Issue #12（SPEC-UI0）Executor concerns C-1、C-2、C-3

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue12-ui0`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | OC-1 第二個 Formal run 的 Orchestrator：`docs/governance/records/run/run-20261117-oc1-run2.md` §6 事件 42–43（Executor return 指明 C-1～C-3 的 authority 是 Design Authority；治理 §2.4「已指明 authority，且與本節規則一致」） |
| Outcome Contract | OC-1（`docs/governance/records/outcome-contract.md`），acceptor 2026-11-17 針對 `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| Spec | SPEC-UI0 v1（`derivation-spec-ui0.md`，commit `8c3c588`），含 CL-UI0-1～CL-UI0-5 |
| Ticket | #12（UI-0）。Issue 原文：派工所附 `issue-12-body.md`，本次實測 SHA-256 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be`，等於 BD-3 |
| 受審 subject | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `41fd10c`（本次以 `git rev-parse HEAD` 核對，工作目錄乾淨）；實作 commit `6a278b4` |
| 依據的條文 | 治理 §1.2、§1.5、§2.1、§2.4、§2.5、§3.3、§3.4、§3.6、§5.3；Bindings m3 第 2.4、2.6（RB-7）、5 節；高風險類別 record §3.2、§3.4、§4、§5 |
| 讀過的證據 | Bindings m3；治理 §1.2–§1.5、§2.1–§2.5、§3.3–§3.6、§5.3；OC-1 全文；`derivation-spec-ui0.md`；`decision-20261117-high-risk-categories.md`；run record 檔首、第 1 節與事件 28–44；worklog `issue-12.md` 全文；Issue #12 原文；`docs/spec/SPEC-001-plan-schema.md` 4.1（BreakRequest 與規則 1–10）、4.2、5.5 的休息與方向列、7.10 第 2 步、第 9 節 S46、S65–S67、S85；`docs/ui/UI_CR01_DELTA.md` 第 5、7.1 節與 CR-B4、CR-C7 列（只讀）；`docs/cr/CR-01-appendix/lead_dispositions_resolution.md` 第 8.3、9.8 節；`DESIGN.md` §5 資料來源表（GPX 的「不送到第三方」「不離開本機」）；`app/ui0_mock_app.py`（上傳與追問回覆的段落）、`app/ui0_scenarios.py`（情境 5 的題目）、`.streamlit/config.toml`；`.venv` 內 Streamlit 1.67.0 的 `streamlit/web/server/starlette/starlette_routes.py`（上傳路由）、`streamlit/runtime/memory_uploaded_file_manager.py`、`streamlit/elements/widgets/file_uploader.py` 的參數、前端 `FileUploader.*.js`；Starlette 1.10.0 的 `starlette/formparsers.py`。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/`，沒有啟動 Streamlit |
| **結論摘要** | C-1：確認是 SPEC-001 4.1 規則第 3 項的缺口（範圍比 Executor 所述更廣）；**對 #12 無要求**；整合時的語義在第 2.4 節裁定。C-2：**符合 CL-UI0-2，無要求**。C-3：**符合 CL-UI0-2，無要求**；整合 Spec 的條件見第 4.4 節。三項都不改變 accepted 語義，都在 OC-1 boundary 內，不需要 acceptor |

## 1. 問題

Executor 在 #12 的 return（worklog 第 9.2 節）把三項 concern 指明交給 Design Authority：

- **C-1**：情境 5 的組合——行程型態與休息地點在同一輪追問，騎士回覆「來回」並為休息選了一個途經點——那段休息的方向沒有被問到。Skeleton 顯示「未決定（模擬；規格沒有定義這個組合）」，沒有自行選擇。
- **C-2**：CL-UI0-2「不顯示檔名以外的任何內容」。App 只顯示檔案數，但 Streamlit 的 `st.file_uploader` 元件本身會列出每個檔案的大小。
- **C-3**：CL-UI0-2「不寫入磁碟」。App 不寫入，但 Streamlit 1.67.0 的上傳經 Starlette 解析，超過 1 MB 的部分會暫時寫入暫存檔。

本 record 對每項回答：是否符合 SPEC-UI0；對 #12 是否有要求；對之後的整合 Spec 的影響；是否改變 accepted 語義、是否在 boundary 內、是否需要 acceptor。

## 2. C-1：同一輪追問中由回覆才成為途經點的休息，其方向

### 2.1 事實（獨立核對）

- SPEC-001 4.1 規則第 3 項把方向題的條件寫成「來回行程、**地點是指定的途經點**而 `direction` 是 `null`」；同一輪的版本是「行程型態還不知道、休息的地點是指定的途經點而且沒有方向」（4.1 規則第 3 項、4.1 末段第 4 點、5.5 第 688 列、7.10 第 2 步）。兩者都以「地點在追問之前已知是途經點」為前提。
- 休息對應不到地點的那一題，選項包含「各個指定途經點的名稱」（4.1 規則第 3 項；Issue #12 的固定文字）。騎士在這一題選了途經點，地點才在**回覆時**成為途經點；這時方向題沒有被列出。
- 規則第 5 項：「方向來自行程描述或追問的回覆，主程式不預設方向」；Issue #12 與 9.8 節：追問只有一輪、不增加第二輪。所以在這個組合下，現行條文沒有任何合法的方式取得方向。
- **範圍比 Executor 所述更廣**：不只是「行程型態也在這一輪問」的情形。行程型態**已知是來回**、休息對應不到地點、騎士在地點題選了途經點時，同樣沒有方向題（規則第 3 項的地點題與方向題各自以「地點已知」為條件）。
- Skeleton（`app/ui0_mock_app.py` 第 340–358 行 `rests_after_clarify`）在這個組合把方向顯示為「未決定（模擬；規格沒有定義這個組合）」，抵達時間不隨回覆改變（D-12-5）；情境 5 的地點題沒有「折返點」選項（`app/ui0_scenarios.py` 第 520–527 行，符合規則第 2 項「行程型態還不知道時，折返點不算可以對應」）。

### 2.2 對 #12 的裁決：無要求

- Issue #12 情境 5 只要求「缺起點與行程型態，加上一筆對應不到地點的休息（同一輪多題）」；UI0-4 要求一輪、行程型態與方向同一輪、方向只在來回需要回答。回覆之後這個組合怎麼呈現，Issue 沒有定義。Skeleton 沒有自行決定方向、沒有把它顯示為已排入的休息，並以「模擬；規格沒有定義這個組合」標明，符合 CL-UI0-5（不以模擬邏輯冒充判定）與 H-3（不超出證據的陳述）。
- 不要求 #12 改成第 2.4 節的做法：那是整合的語義，不在 Issue #12 的範圍內；把它加進 Skeleton 是擴大 Ticket 範圍。
- 「未決定（模擬；規格沒有定義這個組合）」是 Issue 沒有寫定的畫面文字，與 worklog C-5 的其他文字一樣交 UI Delta Review 檢視；它**不是**預定的產品行為（預定的行為見第 2.4 節）。

### 2.3 可選的設計與可否由現有證據裁決

| 選項 | 內容 | 與既有裁決的關係 |
| --- | --- | --- |
| A | 在同一輪追問中一併列出方向題，條件是「回覆後（或已知）是來回行程、而且地點題選了途經點」；不符合條件時不使用它的回答 | 延伸 9.8 節的既有做法（「選擇來回時才需要回答」的條件式方向題）；不增加第二輪、不預設方向 |
| B | 不問；這個組合在追問之後一律視為「仍然無法安排」，回到表單、不產生計畫 | 符合 fail-closed，但騎士在追問中已經照指示選了途經點，仍被要求改寫行程描述 |
| C | 第二輪追問 | 違反 Issue #12、9.8 節「不增加第二輪」 |
| D | 預設去程（或回程） | 違反規則第 5 項「主程式不預設方向」與 Q-3 第 3 項的裁決（「一律排在去程」作廢） |

C、D 被既有裁決排除。A 與 B 的後果不同，但**現有證據可以裁決**，所以不構成 E-DA/D1：

- Q-3 第 3 項的裁決原文（`lead_dispositions_resolution.md` 第 8.3 節第 375 行）：「接受既有的一次追問，追問之後仍然無法安排時不產生有效的計畫。……去程與回程都有那個地點而方向不明時，用既有的追問確認。」——方向不明時的既定做法是**在既有的那一次追問中確認**，不是讓它在追問之後才失敗。
- 9.8 節（第 509 行）已接受「條件尚未確定時照樣列出方向題、標明條件、由主程式依回覆決定用不用」的模式。選項 A 是同一模式套用到「地點也在這一輪決定」的情形。
- 同一裁決的前半句「追問之後仍然無法安排時不產生有效的計畫」與 O-2 第 (iii) 點、規則第 9 項，界定了任何做法都必須滿足的下限（第 2.4 節第 1 點）。

### 2.4 對之後的整合 Spec 的裁決

1. **下限（不變式，現在即有效）。** 來回行程中，指定給途經點的休息需求在追問之後 `direction` 仍是 `null` 時：不得產生把它當作已排入的計畫；不得預設方向；不得默默省略；不得增加第二輪追問。這只是把 Q-1、Q-3 第 3 項、9.8 節與規則第 4、5、9 項合起來寫明，不是新的語義。屬 H-4（判定 3.4 第 5 項）。
2. **採用選項 A。** 整合時，SPEC-001 4.1 規則第 3 項的方向題條件由「地點已知是途經點」擴大為「地點已知是途經點，**或**這一輪的地點題選項中有途經點」；條件在回覆時才確定的部分（行程型態、地點題的回答），依 9.8 節的模式標明「……時才需要回答」，由主程式依回覆決定是否必答與是否使用。涵蓋兩種情形：(a) 行程型態與地點都在這一輪問；(b) 行程型態已知是來回、地點在這一輪問。地點題選「折返點」或「不安排這段休息」、或回覆是單向時，方向題的回答不使用；方向題選「不安排這段休息」時取消那一筆休息需求（4.2 既有規則）。
3. **殘餘情形依選項 B 的下限處理。** 若仍有任何路徑讓上述休息在回覆後 `direction` 是 `null`（例如程式缺陷或資料不一致），依規則第 4 項回到表單、不產生計畫；整合 Spec 決定這時沿用 5.5 的「追問之後仍然對應不到」訊息或另寫一則（現有訊息要求騎士「把休息的地點改成這次行程指定的途經點」，對這個情形不貼切）。
4. **整合 Spec 必須包含**：SPEC-001 4.1 規則第 3 項、4.2 `questions[]`、5.5 的對應修訂；方向題在 (a)、(b) 兩種情形的固定模板（標為提案，與 5.5 其他文字一樣交 acceptor 確認）；仿 S85（Q3-T33）的測試，至少涵蓋：(a)、(b) 兩種情形都在同一次追問中出現方向題、沒有第二次追問；回覆來回＋途經點＋去程／回程時對到該方向的 `waypoint` 檢查點並計入 ETA；回覆單向或選折返點時不使用方向的回答；第 1 點的下限。實作這一部分的 Ticket 標示 H-4。
5. 本裁決只決定語義與必須包含的內容；方向題是一開始就列出（標明條件）還是在騎士選了途經點後才顯示，屬於整合時的介面做法，由整合 Spec 決定，前提是仍在同一個追問區塊、同一次回覆內完成。

### 2.5 是否改變 accepted 語義、boundary

- **不改變 accepted 語義。** OC-1 的 accepted 語義在 AB-2（FR1：行程描述、追問、來回與單向）層級；本裁決沒有新增 requirement、AC 或 scope，也沒有違反任何 acceptor 裁決（Q-1、Q-3 第 3 項、9.8 節），而是依 Q-3 第 3 項的原文「方向不明時，用既有的追問確認」補上條文沒有涵蓋的組合。屬治理 §5.3 第 2 類（derived contract 的設計與 clarification）。SPEC-001 的修訂在 OC-1 §2.1 第 2 項的範圍內（「Spec 修訂……由 Design Authority 引用或修訂」）。
- **Boundary：在 OC-1 boundary 內。** 依據同上；不涉及 reserved boundary。
- **不需要 acceptor。** 新的方向題模板是提案文字，與 5.5 其他提案一樣由 acceptor 在 UI 文字的確認中決定是否採用；acceptor 在 UI Delta Review 或之後另作決定時，以 acceptor 的決定為準。

## 3. C-2：上傳元件列出檔案大小

### 3.1 事實

- App 只取 `len(files)`（`app/ui0_mock_app.py` 第 83–94 行），處理結果只顯示選取的檔案數與合成的數字。
- `st.file_uploader` 是 Issue #12 元件對照表指定的元件。Streamlit 1.67.0 前端 `FileUploader.*.js` 對每個已上傳的檔案保留 `name` 與 `size` 並在元件內的清單呈現；`file_uploader()` 沒有隱藏這份清單的參數（本次讀過其參數）。清單中「大小」的呈現是 Executor 在瀏覽器中的觀察；本次沒有啟動瀏覽器重看，只核對了前端保留 `size` 的程式碼。

### 3.2 裁決：符合 CL-UI0-2，對 #12 無要求

- CL-UI0-2 的這一句是 Design Authority 為 Issue #12「歷史 GPX 的上傳只驗證元件的操作……不解析、不保存實際的 GPX 內容」所寫的 clarification。它的意思是：**app 不顯示讀取檔案內容後得到的任何資訊**（軌跡、座標、時間、路線、點數等）。標準上傳元件本身顯示的檔案中繼資料（檔名、大小）不是 app 的輸出，也不是檔案內容；Issue 指定使用這個元件，就接受它的標準呈現。
- 依此，CL-UI0-2 的這一句釐清為：「app 不顯示檔案內容或由內容導出的資訊；`st.file_uploader` 自身列出的檔名與大小不在此限」。這是對 Design Authority 自己的 clarification 的釐清，不改變 Issue #12 或 OC-1 的語義。
- H-2：檔案大小不含座標、時間或路線；Skeleton 只用合成或空檔（CL-UI0-2 第二句）。不涉及外洩。

### 3.3 對之後的整合 Spec 的影響

- 整合時上傳的是騎士的真實 GPX。元件清單的檔名與大小只出現在騎士自己的畫面，可以接受；但**真實檔名可能含騎乘日期或地名**。整合 Spec 必須寫明：截圖、Demo 影片、README、evidence 與治理紀錄中的上傳畫面只用合成檔（或不含元件清單），不得出現真實檔名（H-2 判定 3.2 第 4 項；RB-7(3)）。
- Profile 的涵蓋度摘要仍依 Issue #12／CR-P5：不顯示座標、騎乘日期時間、路線名稱，不逐趟列出行程。元件清單不是摘要，不受此句約束，但 app 不得另外列出檔名清單。

## 4. C-3：框架在解析上傳時的暫存檔

### 4.1 事實（獨立核對 `.venv` 內的套件原始碼）

- Streamlit 1.67.0 的伺服器是 Starlette（`streamlit/config.py` 的伺服器模式只有 `starlette-*` 三種）。上傳路由 `_upload_put`（`starlette_routes.py` 第 870–990 行附近）以 `request.form()` 解析 multipart，接著 `await upload.read()` 把內容讀進記憶體，在 `finally` 中 `upload.file.close()`，再交給 `MemoryUploadedFileManager`（記憶體，隨 session 存在）。
- Starlette 1.10.0 `formparsers.py`：每個檔案部分寫入 `SpooledTemporaryFile(max_size=1024*1024)`；超過 1 MiB 時轉存到作業系統的暫存目錄。本環境是 Windows、Python 3.11.2，`tempfile.TemporaryFile is tempfile.NamedTemporaryFile` 為 `True`，即以 delete-on-close 開啟的暫存檔，關閉時刪除（依標準函式庫的文件行為；本次沒有實測檔案的生命週期）。
- 串流途中超過上限而中止時，路由的註解說明暫存檔交由 GC 關閉。
- 本次測試檔是 0 B 與 48 B，不會轉存。App 本身沒有任何寫檔的程式（worklog E-1 的靜態測試）。

### 4.2 裁決：符合 CL-UI0-2，對 #12 無要求

- CL-UI0-2「不寫入磁碟」約束的是 **app**：app 不把上傳內容寫成檔案、不保存。框架為了解析 HTTP 請求、在請求處理期間使用、關閉即刪除的暫存檔，不是 app 的寫入，也不是 Issue #12「不保存實際的 GPX 內容」所說的保存。
- Skeleton 依 CL-UI0-2 第二句只接收合成或空檔，所以框架的暫存行為不涉及私有資料。worklog UI0-2 的限制 6 已如實記錄這項框架行為，不需要另外修改。
- 不要求以 `server.maxUploadSize` 或 `file_uploader(max_upload_size=…)` 限制：上限加上 1 MB 的框架餘裕之內，超過 1 MiB 的檔案仍會先被轉存才被拒絕，限制不能消除這項行為，只會改變元件的操作。

### 4.3 對 #12 之外的提醒（資訊，不是要求）

UI Delta Review 由 acceptor 進行。CL-UI0-2 規定檢視只用合成或空的 `.gpx` 檔；若 acceptor 自行選擇上傳真實檔案，內容會隨 session 存在伺服器記憶體中，超過 1 MiB 時會先經過作業系統暫存目錄。是否這樣做是 acceptor 依 RB-7 的決定。

### 4.4 對之後的整合 Spec 的影響

整合時 app 本來就要讀取並保存 GPX 與由它導出的資料（FR2：合併、去重複、重建配速表），所以 CL-UI0-2 的「不寫入磁碟」**不延續到整合**；整合 Spec 必須自己定義上傳資料的保存契約（H-2 判定 3.2 第 1、5 項）。本 record 先確定下列幾點：

1. **框架的暫存行為本身不是缺陷**，條件是部署只在騎士自己的電腦上（DESIGN §5 資料來源表：私有 GPX「不送到第三方」「不離開本機」；目前 `.streamlit/config.toml` 的 `server.address = "localhost"`）。暫存檔與 app 自己保存的資料在同一台電腦，且關閉即刪除。
2. 整合 Spec 必須寫明：上傳內容在記憶體中的保存期間；app 保存原始 GPX 與衍生資料的位置（必須是 `.gitignore` 涵蓋、不進版控的路徑）、保存期間與刪除方式；框架在超過 1 MiB 時使用作業系統暫存目錄的行為（記入 DESIGN 的 Limitations 或隱私說明的依據）。
3. 產品文字與文件不得宣稱上傳的檔案「不寫入磁碟」或「只留在記憶體」；隱私說明依 U-7 裁決後的文字，本來就沒有這類宣稱（root `CLAUDE.md` 的用語規則；H-3 判定 3.3 第 4 項）。
4. 若之後要部署到騎士電腦以外的主機（例如雲端託管），上傳的 GPX 會離開本機，這超出 DESIGN §5 與 NFR2 的現行條件，本 record 的第 1 點不適用；那是 boundary 問題，須依治理 §1.2 route 至 acceptor（RB-7）。
5. 實作上傳與保存的整合 Ticket 標示 H-2（判定 3.2 第 1、5 項）。

## 5. 是否改變 accepted 語義、boundary determination、是否需要 acceptor

| 項目 | 改變 accepted 語義 | Boundary | 需要 acceptor |
| --- | --- | --- | --- |
| C-1 | 否（治理 §5.3 第 2 類；依 Q-3 第 3 項的原文補上條文未涵蓋的組合） | 在 OC-1 boundary 內（§2.1 第 2、4 項） | 否。新的方向題模板是提案文字，由 acceptor 在 UI 文字的確認中決定 |
| C-2 | 否（釐清 Design Authority 自己的 CL-UI0-2） | 在 OC-1 boundary 內 | 否 |
| C-3 | 否（同上；整合的保存契約留給整合 Spec，本 record 只定下限） | 在 OC-1 boundary 內；第 4.4 節第 4 點的雲端部署除外（屆時 route 至 acceptor） | 否 |

沒有 capability escalation：C-1 的 A、B 兩案可由現有裁決原文裁決（第 2.3 節），不構成 E-DA/D1；本 record 沒有被 FA ruling 或 Reviewer finding 推翻的先前決定，不構成 E-DA/D2。CL-UI0-2 的兩處釐清是 Design Authority 對自己 clarification 的說明，不是被推翻後的修改。

## 6. 受影響的 work items 與 evidence

- **#12**：**沒有要求**；不需要修改 `app/`、`tests/`、`.streamlit/`、`pyproject.toml` 或 worklog。C-1～C-3 不影響 UI0-1～UI0-10 的結果。R1（Orchestrator 派工）可引用本 record 評估 C-1～C-3；本 record 不是 audit，也不替 Reviewer 判定 C-4、C-8 或其他 finding。
- **SPEC-UI0**：CL-UI0-2 依第 3.2、4.2 節釐清，SPEC-UI0 的版本與其他內容不變；SIA 可引用本 record。
- **之後的整合 Spec（`app/` 的正式整合、Planner 的追問與休息需求的對應）**：第 2.4、3.3、4.4 節是 derivation 時必須納入的內容；SPEC-001 4.1、4.2、5.5 與第 9 節的修訂在該 derivation 中進行。
- **Completion report（交 acceptor 的資訊，不是 required authority）**：(1) Skeleton 情境 5 的「未決定」不是預定的產品行為，預定的行為見第 2.4 節；(2) UI Delta Review 依 CL-UI0-2 只用合成或空檔（第 4.3 節）。
- **Evidence**：本 record 只讀原始碼與紀錄，沒有執行測試、沒有啟動 Streamlit 或瀏覽器；C-2 中「元件顯示大小」的呈現沿用 Executor 的瀏覽器觀察，C-3 中暫存檔的刪除時點依 Python 標準函式庫的文件行為，兩者都沒有在本次實測。

本 record 沒有讀取 `data/` 或 `.env`，沒有派工任何 subagent，沒有修改其他檔案，沒有 commit。
