# Decision record — 本專案的高風險類別

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261117-high-risk-categories` |
| 日期 | 2026-11-17 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | 無角色主 session（Bindings 第 3.5 節），只作派工介面。acceptor 2026-11-17 指示原文：「下一步確認」，指 Bindings 第 8.2 節 #4 |
| 依據的條文 | 治理 §5.1（「Design Authority MUST 決定專案適用的高風險分類及 assurance 要求」；Assurance policy 須含高風險類別）、§4.5（高風險類別的 blocking finding 不得由 Final Adjudicator 單獨 defer）、§4.1（無法確認適用性時不得靜默選擇不審查）、§2.5（選型原則：決策後果與可捕捉性）；Bindings m2 第 5 節（Lightweight audit 觸發條件與 H-1～H-3 候選）、第 2.6 節 RB-3、RB-4、RB-5、RB-6、RB-7、第 7 節、第 8.2 節 #4 |
| 讀過的證據 | `docs/governance/project-bindings.md`（m2）；治理本文 §1.2、§1.5、§2.1–§2.7、§3.1–§3.8、§4.1–§4.7、§5.1–§5.4；root `CLAUDE.md`；`DESIGN.md` §1–§4.2、§5、§6.2、§10–§12；`docs/requirement/requirements_proposal.txt`；`docs/ticket/BATCH-1-scoped-tickets.md` 標題；`experiments/llm_smoke_test/smoke_test.py`、`experiments/cr01_checks/routing_client.py`、`experiments/cr01_checks/data_common.py`、`src/moto_copilot/pace/table.py` 中與憑證、外部請求、私有路徑、保留行程有關的行（只讀原始碼，沒有執行）。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env` |

## 1. 問題

Bindings 第 5 節列出初始候選 H-1（憑證與機密）、H-2（私有騎乘資料）、H-3（實驗與宣稱的誠信），要求在第一次正式 audit 或 Formal activation 前由 Design Authority 確認或修改。本 record 決定：

1. 本專案的高風險類別：確認、修改、刪除或新增。
2. 每個類別的範圍與判定方式（怎樣的變更算「涉及」）。
3. 每個類別對 assurance 的影響。

不在本次範圍：以高風險類別作 capability escalation trigger（Bindings 第 3.2、5 節明定不採用，本 record 不改變這一點）。

## 2. 判斷依據

選類別的標準是治理 §2.5 的「決策後果與可捕捉性」：錯誤的後果大、不可逆或難以由後續步驟（測試、release gate、Formal 的每票 audit）發現者，才列為高風險。本專案的特殊條件：

- **Repository 是公開的。** 憑證或私有位置一旦進入 git 歷史，移除要改寫歷史（RB-6）、輪替憑證（RB-3），都是保留給 acceptor 的動作；push 之後（RB-1）無法收回。這類錯誤不可逆，且單看測試結果看不出來。
- **評分與口頭提問依據的是可追溯的證據。** 上位契約要求「不得虛構實驗結果」並由教師就實驗結果口頭提問（`requirements_proposal.txt` 第二、五節）。保留行程一旦被用來調整設定，污染無法撤銷（DESIGN §6.2）。
- **產品的核心主張是 Validator 的 fail-closed 判定。** 資料不足時回報 UNKNOWN、不補值（NFR4、§3 設計原則 3）；規則 4 不得預設 PASS、規則 2 不預設滿油（§4.2）；E2 量的就是這個機制（§6.3）。此處的 fail-open 缺陷在輸出上看起來正常（計畫照樣是 `FEASIBLE`），不會因執行失敗而暴露，而輸出是騎士出發前的決策依據（天黑前能否回到出發點、油量是否足夠）。

候選 H-1～H-3 都符合上述標準，予以確認；範圍依證據修訂（第 3 節）。另新增 H-4（決策關卡的 fail-closed 語義），理由見第 3.4 節。

考慮過但不列為類別的項目：

| 項目 | 不列入的理由 |
| --- | --- |
| 修改上位契約、治理檔案、凍結基線 | 已是 RB-5 保留動作；Agent 不得執行，不需要以 audit 補強 |
| Push、PR、合併、對外發布 | 已是 RB-1、RB-2 保留動作 |
| 破壞性 git 操作 | 已是 RB-6 保留動作 |
| 老師的講義 PDF 與架構圖進入版控 | 由 `.gitignore`（`docs/requirement/*.pdf`、`*.png`）與 RB-5（`docs/requirement/` 唯讀）涵蓋；Agent 沒有合法理由新增或改動這些檔案。若 acceptor 希望 release gate 也檢查這兩個 pattern，那是 Bindings 第 5 節的變更（見第 7 節建議 R-2） |
| 一般程式正確性（配速計算、路線切段等） | Formal 下每張 Ticket 已有 independent audit 與 Spec Integration Audit；錯誤可由測試與 E1 Lite 捕捉。其中會讓判定 fail-open 的部分由 H-4 涵蓋 |

## 3. 裁決：高風險類別

本 record 是本專案高風險類別的權威定義（Bindings 第 5 節：「以 decision record 承載」）。Bindings 第 5 節 H-1～H-3 的候選文字只是初始候選；兩者不一致時以本 record 為準。

### 3.1 H-1 憑證、機密與付費呼叫（確認，範圍擴及付費呼叫）

**範圍。** Anthropic API key、中央氣象署授權碼、TDX 等現在與未來的憑證；`.env` 與任何可能存放憑證的檔案；載入憑證、以憑證建立請求、決定請求端點的程式；含有憑證的模組所產生的 log、例外訊息、evidence 與介面輸出；會產生費用的 API 呼叫及其額度控制。

付費呼叫併入 H-1 的理由：付費呼叫與憑證使用是同一條程式路徑；額度控制失效的後果（超出 RB-4 授權的費用）不可逆，且測試只用 scripted model 時看不出來。`experiments/llm_smoke_test/smoke_test.py` 已有端點固定與 budget guard，這正是本類別要保護的控制。

**判定：變更符合下列任一項即「涉及 H-1」。**

1. 新增或修改讀取環境變數、`.env`、secrets 檔或 Streamlit secrets 的程式；或把憑證傳給 client、header、URL 的程式。
2. 新增或修改請求的端點或 base URL 的決定方式（含 SDK 的 base URL、環境變數覆寫）。
3. 在持有或傳遞憑證的模組中，新增或修改 log、例外處理、request／response 的序列化、evidence 或結果檔的寫出。
4. 新增付費 API 的呼叫點，或修改既有付費呼叫的 model id、`max_tokens`、重試或迴圈上限、budget guard、價格表、累計費用的記錄。
5. Streamlit 介面新增或修改會顯示設定值、環境資訊或憑證 client 錯誤訊息的區塊。
6. 修改 `.gitignore` 中與機密有關的項目（`.env`、`*.key`），或修改 Bindings 第 5 節 release gate 的機密檢查所依賴的設定。
7. 工作會把憑證化執行（例如 C3 真實 API smoke test）的輸出寫入 git、worklog、evidence 或文件。

**不涉及**：文件只寫出變數名稱與設定步驟、不含任何值；與憑證和付費呼叫無關的程式。

H-1 不授權任何動作：填寫、輪替憑證仍是 RB-3，任何付費呼叫仍須在 RB-4 的授權額度內。

### 3.2 H-2 私有騎乘資料與位置（確認，範圍明確化）

**範圍。** `data/` 的內容（含 `data/private/`、`data/bmw/`、`data/raw/`）；GPX、FIT；由它們導出的軌跡、位置、時間序列、行程清單與保留行程指定；住家與工作地點附近的座標；從住家或出發錨點出發的路線與路線快照（NFR2）；目標 GPX 的幾何；送往第三方（路線服務、地名查詢、語言模型與其他外部 API）的內容；對外請求中的個人識別資訊（姓名、email 等，例如 User-Agent）。

**判定：變更符合下列任一項即「涉及 H-2」。**

1. 新增或修改會開啟 GPX、FIT 或 `data/` 下檔案的程式，或決定衍生輸出寫到哪裡的程式（`ingest`、Profile 管理、目標 GPX 的路線來源、路線快照的儲存）。
2. 新增或修改起點與終點附近的裁切（隱私裁切），或公開版衍生路段表的產生與欄位。
3. 新增或修改送往第三方的內容：路線與地名請求的組成（只用公開地標、以出發錨點代替住家）、送給語言模型的 prompt 與工具輸出（不含座標與軌跡點）、行程描述的送出前檢查（SPEC-001 7.12）、對外請求的 header 與 User-Agent。
4. 新增或修改測試 fixture、圖表、文件、log、evidence 或治理紀錄，其中含有座標、軌跡、逐點時間、行程時間或路線幾何，而內容不是可證明的合成資料或公開地標。
5. Streamlit 的 GPX 上傳：上傳檔案的保存位置、保存期間、顯示方式（含地圖或路線摘要中可能出現的起點位置）。
6. 修改 `.gitignore` 中與私有資料有關的項目（`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/`），或 release gate 的私有資料檢查所依賴的設定。

**不涉及**：只使用合成資料且不碰上述程式路徑的變更；只描述規則、不含任何私有資料或其導出值的文件。

H-2 不授權任何讀取或公開：讀取 `data/` 與公開任何私有資料或其導出資訊的範圍仍由 acceptor 依 RB-7 決定。DESIGN NFR2 所說「公開資料只放裁掉頭尾後的衍生路段表」，其實際公開範圍是否已經 acceptor 依 RB-7(3) 授權，本 record 沒有判定；真的要把該表放進 git 時，由該 work item 依 RB-7 向 acceptor 確認。

### 3.3 H-3 實驗與宣稱的誠信（確認，範圍明確化）

**範圍。** 保留行程（holdout）的隔離；E1 Lite 與 E2 的程式、設定、提示、Oracle、凍結清單與分析計畫；實驗結果、技術檢查狀態（PASS、FAIL、NOT RUN、BLOCKED）與 gate 狀態的陳述；產品介面與文件中受 root `CLAUDE.md` 用語規則約束的宣稱，以及 DESIGN 已寫定的同類限制（國道檢查不是道路主管機關資料的獨立驗證；`ridden_share_pct` 不保證騎過同一條路；模擬與真實資料分開標示，NFR5）。

**判定：變更符合下列任一項即「涉及 H-3」。**

1. 新增或修改保留行程的隔離機制：保留行程的指定與清單雜湊、凍結清單與 SHA-256 核對、`research-` 與 `user-` 配速表的分離、拒絕保留行程與被排除行程的檢查（例如 `pace/table.py` 現有的拒絕）、上傳時與保留行程內容相同的檔案的去重複規則，或任何可能在凍結前開啟保留行程的程式路徑。
2. 新增或修改 E1 Lite、E2 的程式、設定、提示、Oracle、題目、凍結的路線快照清單，或在凍結之後修改分析計畫。
3. 寫入或改變任何「已執行」「通過」「未執行」的陳述：實驗結果（DESIGN §11、README、簡報素材、紀錄）、技術檢查狀態、gate 或驗收狀態。
4. 在介面文字或文件中新增或改變下列主題的宣稱（能力、準確度、驗證狀態、資料來源）：`ETA_safe`／保守估計與百分位數；降雨機率門檻與官方警特報；與 Google Maps 或一般導航的比較；折返判斷與其他啟發式門檻的驗證狀態；隱私說明（檔案存放與外送範圍）；國道檢查的性質；模擬與真實資料的標示。

**不涉及**：不改變上述宣稱內容的編修（錯字、連結、排版、段落搬移而文字不變）；不碰上述機制與陳述的程式。

### 3.4 H-4 決策關卡的 fail-closed 語義（新增）

**新增理由。** 第 2 節第三點：Validator 的判定是產品對騎士的主要輸出，也是 E2 的研究對象；fail-open 缺陷不會在執行時暴露。Formal 的每票 audit 已涵蓋多數情況，H-4 的實際作用有兩項：(a) 結案之後對這些程式的 Lightweight 單點修正須經 independent audit；(b) 這類 blocking finding 不得由 Final Adjudicator 單獨 defer（治理 §4.5）。兩項都只影響數量有限的工作，不違背 Bindings 的 Lightweight 優先。

**範圍。** 規則 1–5 的 PASS／FAIL／UNKNOWN 判定；計畫狀態（`FEASIBLE`／`CONDITIONAL`／`INFEASIBLE`）的決定與 Planner 不能改寫它的保證；候選評估與排序（`INFEASIBLE` 不參與排序、評估失敗或中止時不宣稱最晚可行出發時間）；規則 5 的輸出關卡與固定模板；工具在資料缺漏、外部 API 失敗、超出涵蓋範圍時回報 UNKNOWN 而不補值（NFR4；含不預設滿油、規則 4 不預設 PASS）；路線的採用條件（國道檢查的 fail closed、偏移門檻、回應警告即不採用、Snapshot Mode 的嚴格模式不回退）；騎士指定的休息不得被默默省略、移除、搬移或縮短（DESIGN §4.1，O-2、Q-1 的裁決）。

**判定：變更符合下列任一項即「涉及 H-4」。**

1. 新增或修改計算規則 1–5 結果、計畫狀態或候選排序的程式。
2. 新增或修改規則 5 的檢查、固定模板的組裝，或 Planner 輸出與 Validator 結果的合併方式。
3. 新增或修改下列工具中處理缺漏、失敗、逾時、過期快取或預設值的程式：天氣、日照、加油站與油量、路況事件、配速與 ETA，以及鄉鎮對應。
4. 新增或修改路線採用的檢查（`freeway_check`、偏移、警告、途經點順序）、快照的重用與 Snapshot Mode 的選取。
5. 新增或修改休息需求的對應、排入與重新規劃時的保留。

**不涉及**：不改變上述判定行為的介面版面；只新增測試而不改產品程式的變更。

## 4. 判定程序（各類別共用）

1. **Lightweight。** Executor 在 worklog 開始時，對 H-1～H-4 逐項記錄「涉及／不涉及」與依據（引用第 3 節的判定項目編號）；結案前以最終 diff 重新判定。最終 diff 涉及開始時未記錄的類別時，independent audit 自該時起成為必要。
2. **無法確定時不得記為「不涉及」**（治理 §4.1）：記為涉及並執行 audit，或 route 至 Design Authority 判定。
3. **Formal。** Design Authority 在 derivation record 中為每張 Ticket 標示所涉及的類別；Orchestrator 依標示機械處理，不自行降級（治理 §5.1）。Executor 發現實際變更涉及未標示的類別時，route 至 Design Authority。
4. **Reviewer** 認為某類別被涉及而未被標示時，以 finding 提出；對是否涉及有爭議時由 Design Authority 判定。
5. 本程序不影響 Bindings 第 5 節的其他觸發條件（acceptor 要求、Design Authority 裁決要求）。

## 5. 裁決：對 assurance 的影響

| 影響 | H-1 | H-2 | H-3 | H-4 |
| --- | --- | --- | --- | --- |
| Lightweight：涉及即須 independent audit（Bindings 第 5 節觸發條件） | 是 | 是 | 是 | 是 |
| Formal：每票 audit 與 Spec Integration Audit 原本就必要；audit record 須逐項寫明對所涉類別的核對（見下） | 是 | 是 | 是 | 是 |
| Blocking finding 的 deferral 須另有 Design Authority 確認並記入 disposition；Final Adjudicator 不得單獨 defer（治理 §4.5） | 是 | 是 | 是 | 是 |
| 主張「已實際外洩」的 finding 不得 defer（見下） | 是 | 是 | — | — |
| 作為 capability escalation trigger | 否（Bindings 第 3.2、5 節） | 否 | 否 | 否 |

**Audit record 對所涉類別的最低核對範圍**（不新增 round 或 audit instance，只界定 R1 對該類別必須看到的內容）：

- **H-1**：diff 與新產生的檔案中沒有憑證值；log、例外與 evidence 不輸出憑證或含憑證的 header；端點不可被環境變數或設定轉向；付費呼叫有額度上限並在超出前停止；`git ls-files` 不含 `.env`、`*.key`。
- **H-2**：`git ls-files` 不含 Bindings 第 5 節 release gate 所列路徑；diff、fixture、紀錄與 evidence 中的座標、軌跡、時間來自合成資料或公開地標並可追溯其來源；送往第三方的內容符合 NFR2；隱私裁切與錨點代換有測試。Reviewer 需要私有資料才能核對的項目，依 Bindings 第 3.7 節第 3 項寫明 NOT VERIFIED 並回報 required authority = acceptor，不記為已驗證。
- **H-3**：每項結果與狀態陳述都能對應到實際執行的 evidence（未執行者標 NOT RUN 或 BLOCKED）；凍結前沒有開啟保留行程的程式路徑；技術檢查、預覽或 Spike 的結果沒有寫成 E1 Lite 或 E2 的結果；第 3.3 節第 4 項的宣稱符合 root `CLAUDE.md` 的用語規則與 DESIGN 已寫定的限制。
- **H-4**：缺漏、失敗、逾時、超出涵蓋範圍的每條路徑都有測試顯示結果是 UNKNOWN 或明確錯誤，而不是 PASS 或預設值；計畫狀態與規則結果不能被 Planner 改寫；規則 5 未通過時不顯示計畫狀態；路線採用的檢查在訊號矛盾或無法驗證時不採用。

**已實際外洩的處理（H-1、H-2）。** Finding 主張憑證或私有資料已進入 git 歷史、已寫入已提交的紀錄，或已送往第三方時，該 finding 不得 defer；受影響路徑停止，並 route 至 acceptor。理由：補救需要輪替憑證（RB-3）、改寫歷史（RB-6）或決定外洩範圍的處理（RB-7），都是保留給 acceptor 的動作（治理 §1.5 第 3 項）。Design Authority 不會為這類 finding 確認 deferral。尚未提交、只在工作目錄中的內容，以 targeted correction 處理即可。

Self-verification 不因 audit 而免除：Executor 仍須依治理 §3.5 驗證所涉類別引入的風險；上表的核對範圍可作為 Executor self-verification 的清單，但 self-verification 不得記為 audit（治理 §2.3）。

## 6. 是否改變 accepted 語義

**否。**

- 目前沒有已接受的 Outcome Contract（Bindings 第 8.2 節 #5 未完成），本 record 沒有改變任何 Outcome Contract 的 intent、scope、constraints 或 acceptance semantics。
- 決定高風險類別及其 assurance 要求是治理 §5.1 指定給 Design Authority 的權限；Bindings 第 5 節明定候選由 Design Authority「確認或修改」，並以 decision record 承載。因此確認 H-1～H-3、修訂其範圍、新增 H-4，都在 Bindings 已授予的範圍內，不是 Bindings 變更。
- 本 record 不改動 Bindings、root `CLAUDE.md`、`binding-verification.md` 或任何 RB-5 檔案；不放寬任何 reserved boundary；不改變 Bindings 第 5 節「Lightweight 預設不做 independent audit」的預設，只依其觸發條件界定「涉及」的判定。

## 7. 需要其他 authority 的事項

| # | 事項 | Authority | 理由 |
| --- | --- | --- | --- |
| A-1 | 本 record 要成為穩定引用，需要 commit。SA-1 只在有已接受的 Outcome Contract 時適用（Bindings 第 2.5 節），目前沒有，所以 commit 需要 acceptor 的明確指示 | acceptor | Bindings 第 2.5 節、root `CLAUDE.md` 的 Git workflow |
| A-2 | Bindings 第 8.2 節 #4 的狀態轉錄（例如「完成，見本 record」） | acceptor 指示，由無角色 session 轉錄 | 修改 Bindings 是 RB-5；狀態欄依第 9 節慣例是紀錄轉錄 |

**建議（不是本裁決生效的條件，是否採用由 acceptor 決定）：**

- **R-1**：Bindings 第 5 節「高風險類別」的候選文字可改為引用本 record，並列出 H-4，避免讀者只看 Bindings 而漏掉 H-4 與修訂後的範圍。這是 Bindings 的文字變更（RB-5），依治理 §5.3 記入第 9 節。
- **R-2**：release gate 的「沒有追蹤中的機密或私有資料」可加入 `docs/requirement/*.pdf`、`docs/requirement/*.png` 與 `*.key`，使它與 `.gitignore` 一致。這是 Bindings 第 5 節的變更。

## 8. 受影響的 work items 與 evidence

- **現有產出（Bindings 第 8.1 節）**：保持原樣，不因本 record 重新審查。本 record 沒有核對目前 repository 或 git 歷史中是否已有私有資料或憑證：需要列出追蹤中的 `data/` 路徑才能完整核對，本次沒有授權，記為 **NOT VERIFIED**；若要核對，required authority = acceptor（RB-7）。
- **GitHub Issues #7–#11（BATCH-1）**：初步判斷涉及 H-2（`ingest` 開啟 GPX、停等事件）、H-3（`pace` 的保留行程拒絕與 `research-` 版本）、H-4（規則 3 的範圍判定，B1-5）；`contracts`（B1-1）視其變更是否碰到上述路徑。這只是初步判斷，正式的逐票標示由 Bindings 第 8.2 節 #6 的 derivation record 作出（第 4 節第 3 項）。這些工作屬 Formal，每張 Ticket 原本就必須 audit；本 record 的作用是 audit record 的核對範圍與 deferral 限制。
- **GitHub Issue #12（UI-0，mock-data Skeleton）**：初步判斷涉及 H-3（介面文字中的受約束宣稱、模擬資料的標示）；若介面呈現 Validator 狀態的邏輯不只是 mock 顯示，另涉及 H-4。正式標示同上。
- **C3 真實 API smoke test**：涉及 H-1（憑證、付費呼叫、輸出寫入 evidence）與 H-3（結果陳述）。執行仍需 acceptor 依 RB-3、RB-4 進行或授權，上限 US$3。
- **之後的 routing、routes、Profile 管理、天氣、日照、油量、路況、Planner、Validator、Streamlit 整合、E1 Lite、E2**：依第 3 節判定，在各自的 derivation record 中標示。
- **Bindings 第 8.2 節 #4**：本 record 完成 Design Authority 的確認；狀態轉錄見 A-2。

本 record 沒有執行任何測試或腳本，沒有讀取 `data/` 或 `.env`，沒有派工任何 subagent，沒有 commit。
