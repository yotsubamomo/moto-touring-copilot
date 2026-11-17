# Worklog — Issue #12（SPEC-UI0）UI-0 Streamlit Mock-data Skeleton

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #12（UI-0），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator）。依 run record，SPEC-UI0 不採 fast path：#12 的 R1 是一般 Ticket audit，SIA 另派 |
| 狀態 | **cycle 1 R1 `BLOCKING`（R1-F1、R1-F2）後的 targeted correction 完成，待 R2（第 10 節）。** R1-F1 已修正並有 regression 測試。依 Design Authority 的 `decision-20261118-issue12-ui07.md`：K9 不是 UI0-7 的 FAIL（日期可只用鍵盤以年／月／日欄修改），K3-B（作業系統的檔案對話框）不在 #12 的 UI0-7 範圍內、記為範圍外的 NOT VERIFIED；依該 record 第 4.3 節，UI0-7 在 #12 範圍內沒有 BLOCKED 或 FAIL 的部分。UI0-7 是否 PASS、R1-F2 是否 RESOLVED 由 R2 判定。本 worklog 不宣告 Ticket closure。（已取代的敘述：「R1-F2 補做了只用鍵盤的操作，**仍有 BLOCKED 與 FAIL 項目**（第 10.3 節），required authority = acceptor」——由上述 DA record 取代。）以下第 1–9 節是 R1 前的紀錄，第 7 節 UI0-1、UI0-2、UI0-4、UI0-7、UI0-10 列與第 9.1 節已依第 10 節更新 |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `3906e077ab850c027d7833b30d3eebfa16f67761`（`3906e07`）；實作 commit `6a278b40dc79dcbede9486902e52dc8504a8d30e`（`6a278b4`）；**correction commit `619268ad2732b4cdd04593ff20ebe35374a7710c`（`619268a`，只修改 `app/ui0_mock_app.py`、`tests/test_ui0_skeleton.py`）**；R1 受審 HEAD `e836c99`，R1 record 在 `e94d182`；本節的更新在 `619268a` 之後的 record-only commit |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：GitHub Issue #12 全文與 UI0-1～UI0-10。派工所附 scratchpad 原文檔 `issue-12-body.md` 實測 SHA-256 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be`；另以 `gh issue view 12 --json body,updatedAt`（唯讀）取得的 body，UTF-8 SHA-256 相同，等於 BD-3；`updatedAt` `2026-11-15T15:52:44Z`。沒有修改 Issue。
- **Spec**：SPEC-UI0 v1（`docs/governance/records/decisions/derivation-spec-ui0.md`）：第 2 節引用段落（`DESIGN.md` §9.6；`docs/ui/UI_CR01_DELTA.md` 第 11、12 節；`docs/cr/CR-01-appendix/ui0_decision_table.md` U-1～U-22；G3 凍結的 UI 文件），第 4 節 CL-UI0-1～CL-UI0-5，第 5 節 #12 列（H-2、H-3）與充分證據要求 E-1～E-6。
- **高風險類別**：`decision-20261117-high-risk-categories.md` §3.2、§3.3、§5。
- **Outcome Contract**：OC-1（`docs/governance/records/outcome-contract.md`）。
- **acceptor 對本 run 的指示**（經 Orchestrator 派工轉達）：UI0-6、UI0-7 以內建瀏覽器實際檢查，只用合成資料。
- 本 work item 執行中契約沒有變更。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-acf4b1c528124a22e.{meta.json,jsonl}`；`meta.json` 的 `agentType` 是 `gov-executor`。
- Executor 自行觀測（實作 commit `6a278b4` 之後、本 worklog 寫入前，以第 3.6 節的掃描方式）：agentId `acf4b1c528124a22e`，(`claude-opus-5-5`, `high`) 241 則（worklog commit 前的最後一次掃描），集合只有一個元素。**這是自我觀測，不是派工者的核對**；Orchestrator 採用本 return 前須自行核對該 agent 的全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 `gov-executor` definition、Bindings m3、impl-default v2 §3–§5、§9、治理 §3.5、§3.7、§3.8；SPEC-UI0 derivation record；高風險類別 record §3.2–§5；Issue #12（核對雜湊）；`DESIGN.md` §9.6；`UI_CR01_DELTA.md` 第 5、11、12 節；`ui0_decision_table.md`；`UI_DESIGN.md`（G3 凍結，只讀）；`prototype/index.html` 的結果與規則呈現部分（只讀）；`SPEC-001` 第 4.1、4.2、5.1–5.3 節的追問與 UNKNOWN 部分（只讀）。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/`。
2. BASE `3906e07` 的 pytest：`556 passed`（run record CP-1 的數字；本次在實作前沒有另跑，實作後的完整結果見第 6 節）。
3. 安裝 `streamlit==1.67.0` 到 `.venv`（PyPI，`pip install "streamlit==1.67.0"`）；`pyproject.toml` 新增 optional dependency `ui = ["streamlit==1.67.0"]`。
4. 新增 `app/`（CL-UI0-1，只依賴 Streamlit 與標準函式庫，不匯入 `src/moto_copilot/`）：
   - `ui0_texts.py`：Issue #12 的固定文字逐字複製（72 個字串，含路線錯誤的訊息與做法、UNKNOWN 的原因分類與指引）；Issue 沒有寫定的文字另放一節並標明供 UI Delta Review 檢視；`fill()` 依 Issue 的佔位寫法（`{名稱}`、`〈類別〉`、`目前 N 段`）代入合成值，缺值時保留佔位。
   - `ui0_scenarios.py`：合成的情境資料。道路、地標、時間、預報、檢查點都是「示範…」的虛構名稱，沒有座標。規則結果、計畫狀態、候選標籤與 Profile「夠不夠」都是寫定的字面值（CL-UI0-5）。情境選單 23 項：Issue 的 14 個情境（4、6 各分 a／b，11 分 a～g 對應七則路線錯誤），另加 15「無可行解」（G3 沒有變更的呈現，供檢視）。
   - `ui0_guard.py`：簡化的輸入保護示範比對（Issue 第 2 節）：街道用語（路、街、巷、弄、段）接數字加「號」；數字加「號」接樓層；成對的小數經緯度。
   - `ui0_mock_app.py`：Streamlit 畫面。由上到下：頁首與資料模式標籤；「Skeleton 控制（不屬於產品畫面）」的情境選單；Profile 區（`st.expander`，內含隱私說明、多檔上傳、「更新 Profile」、處理結果、涵蓋度摘要）與緊接其下的 `st.status`；Trip Planner 欄位與「規劃」；規劃進度；追問（`st.chat_message`，一輪）；路線確認區塊；結果過期提示；路線錯誤／評估失敗共用版面，或 Trip Result 與 Validation & Replanning 兩個分頁。
5. 新增 `.streamlit/config.toml`（repo root，`streamlit run` 從 root 啟動時讀取）：`browser.gatherUsageStats = false`（不送使用統計）、`server.address = "localhost"`、`server.headless = true`、`client.toolbarMode = "viewer"`（隱藏開發者的 Deploy 按鈕）。
6. 新增 `tests/test_ui0_skeleton.py`（47 個測試，合成資料）：靜態檢查（依賴、上傳內容不被讀取、無綠色成功提示與聊天輸入、不建立或寫入狀態值、用語、合成資料、情境涵蓋）、輸入保護案例、`fill()`，以及以 `streamlit.testing.v1.AppTest` 對畫面的檢查（第 6 節 E-1）。
7. 以內建瀏覽器（`mcp__Claude_Browser__*`）實際操作 375 像素寬度與鍵盤（第 6 節 E-2、第 7 節 UI0-6、UI0-7）。
8. 依瀏覽器檢查結果做兩項小修正（都在實作 commit 內）：「採用的條件」的期限列改為顯示表單的值；結果區加一句「模擬：結果是這個情境寫定的資料，不依表單的內容計算。」。另把輸入保護測試中的經緯度樣本改為 0°N 0°E 附近的值（原樣本雖是合成值，但落在台灣中部，H-2 判定 3.2 第 4 項的保守處理）。
9. 實作 commit `6a278b4`（SA-1，本機；沒有 push、沒有開 PR）。Streamlit 程序已停止（第 6 節 E-2）。

## 4. Decisions and assumptions

| ID | 決定 | 依據 |
| --- | --- | --- |
| D-12-1 | Streamlit 以 `pyproject.toml` 的 optional dependency `ui` 宣告，版本釘在 1.67.0；`.venv` 以 pip 安裝 | CL-UI0-1（加入方式由 Executor 決定，不新增其他 framework）。`tests/test_ui0_skeleton.py` 需要它；沒有以 `importorskip` 跳過，缺少時測試會失敗而不是靜默略過（Profile §5 品質下限） |
| D-12-2 | 新增 root `.streamlit/config.toml`：關閉使用統計、只聽 localhost、隱藏 Deploy | Streamlit 預設會從瀏覽器送出使用統計到外部；Skeleton 不呼叫任何 API（Issue 排除範圍），隱私說明也承諾不外送 GPX。這是 `streamlit run` 的設定，不是新的 framework。**Reviewer 可判斷是否屬 CL-UI0-1 的範圍** |
| D-12-3 | 表單欄位的 widget key 每個情境換一組（`f_<欄位>_<nonce>`），以 `value=` 給情境的初值，不寫入 widget 的 Session State | 以 Session State 預填的 `st.number_input` 無法清空成「沒有值」，「出發油量必填」就無法示範；這個做法也避免 Streamlit 對「value 與 Session State 同時設定」的警告。情境 9 的出發油量預設為空，用來示範必填檢查 |
| D-12-4 | 「規劃」按下後只顯示情境寫定的結果；表單檢查（行程描述與目標 GPX 都空、出發油量空、輸入保護命中）會擋下 | CL-UI0-5：沒有計算規則結果或計畫狀態的程式。表單檢查與輸入保護是 Issue 第 2 節要求的介面行為，不是 Validator |
| D-12-5 | 追問回覆後，依回覆的行程型態選用「來回」或「單向」的模擬結果；休息列顯示回覆的內容；模擬的抵達時間不隨回覆改變 | 這是「選哪一份模擬資料」與「顯示回覆」，不是休息的排入或 ETA 計算。情境說明與結果區的 caption 寫明模擬值不隨表單改變 |
| D-12-6 | 行程型態沒有選時，期限欄位用固定標籤「期限」，下方 caption 列出兩個名稱 | Issue 只定義「來回」「單向」兩種名稱與固定標籤的退路，沒有定義未選時的名稱。沿用退路的做法；供 UI Delta Review 檢視（第 9.2 節） |
| D-12-7 | 「可以怎麼做」每則以一個清單項目逐字顯示，不依「；」拆成多項 | UI0-3 逐字相同；拆項會改變標點 |
| D-12-8 | 情境 7 直接呈現「一輪追問已回覆、休息仍然對應不到」的狀態 | Issue 情境 7 的重點是行程描述欄下方的訊息與沒有計畫；若先顯示追問，騎士選了途經點就應該對得到，與情境的狀態矛盾 |
| D-12-9 | 「配速資料中的路線涵蓋比例」的句子放在 Trip Result 分頁的「路線摘要」 | `UI_CR01_DELTA.md` CR-C1（Trip Result 有路線摘要與這個句子）。路線確認區塊（兩個分頁都看得到）顯示行程型態、里程、道路名稱、來源與路權提醒 |
| D-12-10 | 高降雨機率提醒以 `st.badge`（yellow，琥珀色）加文字列在天氣表下方；表格的「分類」欄寫「高降雨機率提醒」文字 | `st.table` 的儲存格不能上色；G3 的琥珀色對應 CONDITIONAL 的顏色 |
| D-12-11 | 另加情境 15「無可行解」 | Issue「情境選單至少包含下列各項」；用來檢視 G3 沒有變更的無可行解呈現（代表性失敗候選、「這不是有效的建議」） |

需要其他 authority 的假設：沒有用於實作的假設。發現的規格缺口與疑義列在第 9.2 節，各自指明 authority。

## 5. Artifacts

| 檔案 | 變更 | SHA-256（實作 commit 時） |
| --- | --- | --- |
| `app/ui0_mock_app.py` | 新增 | `daf446e15b6ab21351ca330ba4027460dbb76a6114019ac459e460f0097e5546` |
| `app/ui0_texts.py` | 新增 | `e6b5dd35c5cfa974098647e3db613a87b30e1a7f698a75e507a73ed64fe09227` |
| `app/ui0_scenarios.py` | 新增 | `85f33fc9f562bf94e14d3ae39a383f67575487cd6cb7e04ececb3db8a9e2d623` |
| `app/ui0_guard.py` | 新增 | `0f5770006907596dfc149112ff932695c69ea5f46f8f3e04af96c0a3a62519ee` |
| `tests/test_ui0_skeleton.py` | 新增（47 個測試） | `981950a5dfea9e10f2df7a1251a9878e1736cfd8716382f071a430a3a94548c2` |
| `.streamlit/config.toml` | 新增 | `2dd6dcaacd2c502175276f1fb6c5107e5c3125aa25d4cd5d9d258eedcc206d6e` |
| `pyproject.toml` | 修改（`ui` optional dependency） | `b6d8567a367962e3aa9743731f677b77676824c797fa59979ff7ac564cec545c` |

（雜湊是工作目錄 LF 內容；git 會提示 CRLF 轉換，以 `git show 6a278b4:<path>` 為準。）

沒有修改 `docs/ui/`、`prototype/`、`docs/requirement/`、治理檔案、`src/`。`git diff --stat 3906e07 6a278b4` 只含上表七個檔案。

## 6. Verification

### E-1 pytest

`.venv/Scripts/python.exe -m pytest -q` 的完整輸出（實作 commit `6a278b4` 的工作目錄）：

```text
........................................................................ [ 11%]
........................................................................ [ 23%]
........................................................................ [ 35%]
........................................................................ [ 47%]
........................................................................ [ 59%]
........................................................................ [ 71%]
........................................................................ [ 83%]
........................................................................ [ 95%]
...........................                                              [100%]
603 passed in 19.80s
```

556（BASE）＋47（本 Ticket 新增）＝603，沒有 skip、xfail。本 Ticket 新增的測試：`tests/test_ui0_skeleton.py`，單獨執行 `47 passed`。主要內容：

- 靜態：`app/` 只匯入 Streamlit、標準函式庫與 `app/` 內的模組，不匯入 `moto_copilot`、`os`、`pathlib`、`io`、`tempfile`、`logging`、`urllib`、`http`、`socket`、`requests`、`anthropic` 等；沒有 `open()`、`print()`、`.read()`、`.getvalue()`、`.getbuffer()`、`.seek()` 等呼叫（CL-UI0-2）；沒有 `st.success`、`st.chat_input`；`app/` 中 `ui0_scenarios.py` 以外的模組不建立含 `status`／`result` 鍵的紀錄、不對它們賦值、不回傳狀態字（CL-UI0-5）；字串常數不含 P90、百分位、分位數、這台電腦、只留在、本機、Google Maps，「警特報」只出現在「不是氣象署的警特報」（H-3）；情境資料沒有座標樣式的數字，地標都以「示範」開頭，目標 GPX 路徑都是 `synthetic/…`（UI0-9）。
- 輸入保護：「中正路 123 號」「中正路一段 123 號」「123 號 5 樓」與兩種成對小數被擋下；「國道 3 號」「台 9 線」「不要走國道 3 號，改走台 9 線」不被擋下。
- AppTest：23 個情境都沒有例外且顯示模擬標示與隱私說明；Profile 三種說明；多檔上傳（一個空檔、一個只有 GPX 標頭的合成檔）後按「更新 Profile」顯示處理結果、`st.status`、舊結果過期而不重新規劃；沒選檔時不處理；輸入保護擋下後改寫即可規劃；欄位錯誤；追問一輪（三題同一區塊、沒有「折返點」選項、未答完不送出、回覆後沒有第二輪）；6b 的方向題文字、來回必答、單向不使用；6a 的三題；情境 7 的訊息且沒有計畫；情境 8 的固定句子；期限名稱切換時值保留；目標 GPX 的路權提醒與涵蓋比例無法算出；七則路線錯誤不顯示計畫狀態、出發時間、里程與道路名稱；評估失敗；UNKNOWN 的四項與指引；預設餘裕係數與休息策略；欄位變更標示過期而不重新規劃；全部候選的表格沒有列的選取。

### E-2 Streamlit 的啟動與 14 個情境的操作紀錄

- 啟動（repo root，Git Bash，背景執行）：`.venv/Scripts/python.exe -m streamlit run app/ui0_mock_app.py --server.port 8501`。log 第一行 `Uvicorn server started on localhost:8501`；`curl http://localhost:8501/` 回 200。改設定與小修正後重啟一次再檢查。兩次啟動的程序（PID 16152、48024）都已由我停止，`8501` 不再有 listener。
- 內建瀏覽器：`mcp__Claude_Browser__navigate` 開 `http://localhost:8501`（browser pane 可以連到本機的 server），`resize_window` preset `mobile`（375×812，含行動裝置模擬），檢查完以 preset `desktop` 還原。
- **截圖：沒有。** `computer` 的 screenshot 在 pane 隱藏時逾時（「the page did not finish rendering in time」），所以證據是下面的逐步操作紀錄（CL-UI0-4 允許的另一種形式）。鍵盤輸入在 `tabs_select` 之後可以送達。
- 量測方式：每個狀態以 JavaScript（只讀取）取得 `document.documentElement.scrollWidth`、主內容 `[data-testid=stMain]` 的 `scrollWidth/clientWidth`，以及「右緣超出 375 而且沒有被任何祖先的 overflow 容器裁切」的元素數；同時記錄提示框文字的開頭、分頁、追問區塊與路線確認區塊是否存在。

| # | 情境 | 操作 | 觀察（375 像素） |
| --- | --- | --- | --- |
| 1 | 1 Profile 沒有 GPX | 選情境 → 規劃 | 說明「還沒有歷史 GPX…」；「這個情境只示範 Profile 區」；沒有分頁。doc 375、main 375/375、未裁切溢出 0 |
| 2 | 2 類別不夠 | 同上 | 「高曲率（連續彎道）的路段還不夠（目前 12 段，需要 30 段）…」。溢出 0 |
| 3 | 3 多檔更新 Profile | 以鍵盤選情境；以 DataTransfer 放入兩個合成檔（0 B 空檔、48 B 只有 `<gpx>` 標頭；共觸發兩次，元件列出 4 個）；Tab 到「更新 Profile」按 Enter | 處理結果「（模擬，與選取的 4 個檔案的內容無關）：新增 3 個；略過 1 個內容重複的；1 個無法讀取（原因：檔案中沒有軌跡點）。」；`st.status`「Profile 更新完成（模擬）」；「結果已過期。Profile 已更新。…」；分頁仍是 2 個（沒有自動規劃）；可用的行程數 12。溢出 0 |
| 4 | 4a 輸入保護 | 選情境 → 規劃 | 欄位下方「行程描述中有看起來像門牌地址或座標的內容…」；沒有分頁。溢出 0 |
| 5 | 4b 國道 3 號 | 選情境 → 規劃 → 切到 Validation 分頁 | 沒有被擋；兩個分頁、路線確認區塊；兩個分頁都溢出 0 |
| 6 | 5 追問三題 | 選情境 → 規劃 | 一個追問區塊。溢出 0 |
| 7 | 6a 追問（來回、方向） | 選情境 → 規劃 | 一個追問區塊。溢出 0 |
| 8 | 6b 行程型態與方向同一輪 | 選情境 → 規劃；**只用鍵盤**：Shift+Tab 到行程型態題、Space 選、↓ 改為「單向」、Tab 兩次到「回覆並繼續規劃」、Enter | 回覆後沒有任何追問 radio（沒有第二輪）；回覆表顯示方向題「未使用（行程型態是單向）」；出現單向的模擬結果與路線確認區塊。溢出 0 |
| 9 | 7 追問之後仍然對應不到 | 選情境 → 規劃 | 欄位下方「行程描述中的這段休息仍然沒有辦法排入：「在山上的咖啡店休息 30 分鐘」…」；沒有分頁、沒有追問。溢出 0 |
| 10 | 8 來回可行計畫 | 以鍵盤選情境、Tab 17 次到「規劃」、Enter；切到 Validation 分頁、開「全部候選」 | 兩個分頁；有「去程與回程分別計算，里程相差約 5.1%…」、「去程有路段是高降雨機率提醒…」、「出發點不是住家…」；全部候選的表格在自己的容器內橫向捲動（內層 638/307），頁面溢出 0 |
| 11 | 9 單向、期限名稱 | 選情境 → 規劃（油量空）→ 欄位錯誤「出發油量是必填的（0–100%）。」；以鍵盤：行程型態 Space 選「來回」→ 期限標籤變成「最晚回到出發點時間」，值 17:00 保留；小時 ↓、Tab、輸入 45 → 16:45；→ 改回「單向」→ 標籤「最晚抵達終點時間」，值 16:45 保留；油量輸入 80 → 規劃 → 兩個分頁 | 涵蓋比例 0% 的句子；兩個分頁都溢出 0 |
| 12 | 10 目標 GPX | 選情境 → 規劃 → Validation 分頁 | 「出發前要確認的事項（1 項）」；「系統無法算出配速資料中的路線涵蓋比例。」；兩個分頁溢出 0 |
| 13 | 11a～11g 七則路線錯誤 | 每則：選情境 → 規劃 | 各自的錯誤訊息與「可以怎麼做」；沒有分頁、沒有路線確認區塊。七則都溢出 0 |
| 14 | 12 評估失敗 | 選情境 → 規劃 | 「候選的評估沒有完成…」；沒有分頁。溢出 0 |
| 15 | 13 UNKNOWN 計畫 | 選情境 → 規劃 → Validation 分頁 | 「出發前要確認的事項（4 項）」；兩個分頁溢出 0 |
| 16 | 14 預設餘裕係數 | 選情境 → 規劃 → Validation 分頁 | 兩個分頁溢出 0 |
| 17 | 15 無可行解（補充） | 選情境 → 規劃 → Validation 分頁 | 「沒有可用的計畫」、原因摘要、替代方案；兩個分頁溢出 0 |
| 18 | 可用的公路與地標 | 以鍵盤 Enter 打開該 expander（Profile 區同時展開） | 溢出 0 |
| 19 | 重啟後（設定與小修正之後） | 情境 8 → 規劃 | Deploy 按鈕不再出現；結果區有「模擬：結果是這個情境寫定的資料…」；「最晚回到出發點時間 18:00」；溢出 0 |

第 4～17 列在選情境與按「規劃」時，以 JavaScript 的 `focus()` 移動焦點、再以實際按鍵（Enter）啟動；這幾列的目的是 375 像素的量測。鍵盤的可達性另以 Tab 逐一走過（第 7 節 UI0-7）。

### E-3 UI0-1～UI0-10

見第 7 節。

### E-4 固定文字的逐字比對

- 方法：scratchpad 腳本 `e4_verbatim_check.py`（非權威，未 commit）讀 `gh issue view 12 --json body` 的 body（UTF-8 SHA-256 `79614ef7…`，等於 BD-3），雙向比對：(1) `ui0_texts.py`「Issue #12 fixed texts」一節的每個字串（含 tuple 與 dict 內的值）都是 Issue body 的子字串；(2) Issue body 中每個表格列（略過表頭）的文字儲存格都是 `ui0_texts` 的某個常數。
- 結果：(1) 檢查 72 個字串，缺 0 個。(2) 檢查 46 個儲存格，5 個不是單一常數：兩個是選項清單（「這次路線請求中各個指定途經點的名稱；「折返點」…」「「去程」；「回程」；「不安排這段休息」」，實作為各自的選項常數與途經點名稱），三個是元件對應表的說明（「文字、`st.info`」等），不是畫面文字。
- 畫面上的呈現與常數相同：AppTest 以完全相等比對（例如 `T.GUARD_MESSAGE in values(at.error)`、路線錯誤 `values(at.error) == [...]`、方向題的 `radio.label ==`）。帶佔位的文字以合成值代入後比對（`fill()`）。

### E-5 沒有真實資料

- 畫面與程式中的道路、地標、加油站都是「示範…」的虛構名稱；Issue 指定的測試字串「國道 3 號」「台 9 線」「中正路 123 號」是 Issue 本身的範例。日期是合成的 2026-12-06；時間是寫定的模擬值；沒有座標（輸入保護的測試樣本是 0°N 0°E 附近的合成值）。
- 上傳只用合成內容（瀏覽器中以 JavaScript 建立的 `File` 物件；AppTest 中的位元組字串），沒有使用騎士的檔案，沒有寫入任何 `.gpx` 到磁碟。
- `git ls-files` 不含 `.env`、`*.gpx`、`*.fit`、`*.key`、`data/raw/`、`data/private/`、`data/bmw/`；`app/`、`tests/test_ui0_skeleton.py` 中沒有兩位數以上整數部分、四位以上小數的數字（`grep -E '[0-9]{2,3}\.[0-9]{4,}'` 沒有結果）。沒有截圖檔。

### E-6 H-2、H-3 的 self-verification（高風險類別 record §5 的清單）

**H-2**（判定 3.2 第 5 項：Streamlit 的 GPX 上傳；第 4 項：畫面與紀錄）：

- 上傳檔案的保存位置與期間：app 只取 `len(files)`，不呼叫任何讀取方法（靜態測試）。Streamlit 1.67.0 的伺服器以 `MemoryUploadedFileManager` 在記憶體保存上傳檔，隨 session 存在（`streamlit/web/server/starlette/starlette_app.py`、`starlette_routes.py`）。**框架限制**：上傳的 multipart 由 Starlette `request.form()` 解析，超過 1 MB 的部分會暫時 spool 到暫存檔（`starlette_routes.py` 的註解），之後讀進記憶體並關閉。本次的合成檔是 0 B 與 48 B，不會 spool；app 本身不寫入磁碟。見第 9.2 節 C-3。
- 顯示方式：app 只顯示選取的檔案數與合成的處理結果；沒有地圖、沒有路線摘要中的起點位置。Streamlit 元件本身列出檔名與大小。見第 9.2 節 C-2。
- 紀錄：app 沒有 log、`print`；Streamlit 的 log 只有啟動訊息（scratchpad `streamlit-ui0.log`、`streamlit-ui0-2.log`，沒有上傳內容）。
- 送往第三方：沒有任何 API 呼叫（靜態測試排除網路模組）；Streamlit 的使用統計以 `.streamlit/config.toml` 關閉。輸入保護的示範比對不送出任何東西；判定 3.2 第 3 項（行程描述的送出前檢查）指產品中送往語言模型前的檢查，本 Ticket 不涉及，正式的檢查在之後的實作 Ticket（SPEC-001 7.12）。
- `git ls-files` 與 diff 的私有資料檢查：E-5。
- 結論：沒有發現已外洩的情形；未提交前把測試中的經緯度樣本改為 0°N 0°E 附近（第 3 節第 8 項）。

**H-3**（判定 3.3 第 4 項：介面宣稱；第 3 項：本紀錄中的結果陳述）：

- 保守估計：畫面稱「保守估計」，說明「保守估計是典型估計加上安全餘裕的估計」；沒有 P90、百分位或分位數（靜態測試）。
- 降雨：「高降雨機率提醒」並附「它是本專題自訂的分類，不是氣象署的警特報，也不表示降雨強度。」；沒有稱為警特報。
- 隱私說明：只有 U-7 裁決後的文字；沒有「只在這台電腦」之類的宣稱（靜態測試）。
- 國道檢查：只有 Issue 的固定句子（「這不是道路主管機關的驗證」）；目標 GPX 的路線另一則（「系統沒有檢查國道」）。
- 模擬標示：頁首「模擬資料：本頁不連接任何 API 或語言模型」；情境標籤都含「模擬」；路線確認、涵蓋度摘要、結果區各有「模擬」標籤；來源證據每一列的類型是「模擬」；結果區另有「結果是這個情境寫定的資料，不依表單的內容計算」。
- 沒有與 Google Maps 或一般導航比較；折返判斷沒有描述為已驗證（Skeleton 沒有這類文字）。
- 本 worklog 的結果陳述：每項 PASS 都對應第 6 節的實際執行；沒有執行的項目標為 NOT VERIFIED。這不是 E1 Lite 或 E2 的結果。

**H-1、H-4（最終 diff 重新判定）**：H-1 不涉及（沒有憑證、設定值或付費呼叫；`.streamlit/config.toml` 不含憑證）。H-4 不涉及：app 沒有計算規則 1–5、計畫狀態、候選排序的程式（CL-UI0-5，靜態測試），狀態都在情境資料中；追問回覆後的「選用哪一份模擬結果」與「顯示回覆的休息」不是休息的排入或重新規劃（D-12-5）。**請 Reviewer 核對這兩項判定**；有疑義時依高風險 record §4 第 4 項由 Design Authority 判定。

## 7. UI0-1～UI0-10 逐條結果（UI0-10 的紀錄，CL-UI0-3）

| AC | 結果 | 依據 |
| --- | --- | --- |
| UI0-1 六個區塊可在瀏覽器操作，每個狀態有合成情境 | **PASS（R1-F1 修正後）** | E-2 第 1～19 列；AppTest 23 個情境。追問的六種題目都有情境（缺起點、行程型態、休息對應不到：情境 5；進入端、休息長度、方向：6a；行程型態＋方向同一輪：6b）。R1-F1（單向＋「不安排這段休息」沒有取消休息）在 `619268a` 修正，第 10.1 節 |
| UI0-2 元件在 1.67.0 可用；做不到的列出替代 | **PASS（有替代與限制，見下表）** | 實際安裝 `streamlit==1.67.0`，Issue 對照表的元件全部使用並實際渲染 |
| UI0-3 固定文字逐字相同 | **PASS** | E-4 |
| UI0-4 追問一輪；行程型態與方向同一輪；方向只在來回需要回答 | **PASS（R1-F1 修正後）** | AppTest（5、6a、6b）；E-2 第 8 列（鍵盤）；第 10.1 節的 regression 測試與第 10.2 節 K12（瀏覽器、只用鍵盤；R2-N1 更正，原誤寫為 K9） |
| UI0-5 期限名稱隨行程型態切換；值是否保留照實記錄 | **PASS：值會保留**，採用隨行程型態改變的標籤，不需要退路 | AppTest（16:45 在切換前後保留）；E-2 第 11 列（瀏覽器中 17:00 與 16:45 都在切換後保留）。條件：widget 有固定的 key（D-12-3）。行程型態未選時用固定標籤「期限」（D-12-6） |
| UI0-6 375 像素沒有整頁的水平溢出 | **PASS** | E-2：23 個情境（含追問回覆後、欄位錯誤後的狀態）、兩個分頁、Profile／公路與地標／全部候選展開時，`scrollWidth` 都是 375，沒有未裁切的溢出；寬表格在自己的容器內捲動 |
| UI0-7 所有操作都可以只用鍵盤完成 | **待 R2 判定。依 `decision-20261118-issue12-ui07.md`，#12 範圍內沒有 BLOCKED 或 FAIL 的部分**（該 record 第 3、4.3 節）。已取代的判定：(1) R1 前「大部分 PASS；一項 NOT VERIFIED」；(2) correction 時「未通過驗證：BLOCKED 一項、FAIL 一項，其餘 PASS」 | 以操作為單位（DA record 第 3.1 節）。只用鍵盤完成的操作紀錄：情境選單、Profile expander、「更新 Profile」（含沒有選檔）、「Upload」按鈕送出多選且限 `.gpx` 的選檔請求（K3）、移除檔案（K5）、選檔之後按「更新 Profile」（K6）、行程描述的輸入、公路與地標 expander、行程型態、日期（K10，年／月／日欄）、時間、出發油量、目標 GPX 路徑、Snapshot Mode、「規劃」、追問的 radio 與回覆、分頁、全部候選 expander（第 10.2 節、第 6 節 E-2）。**K9**（日曆彈窗內鍵盤焦點進不去）：不是 UI0-7 的 FAIL，記為元件的限制（UI0-2 限制 7），日期這項操作由 K10 完成（DA record 第 3.2 節）。**K3-B**（在作業系統的原生檔案對話框中只用鍵盤多選 GPX）：不在 #12 的 UI0-7 範圍內，**範圍外，NOT VERIFIED**；#12 範圍內的上傳操作由 K3、K5、K6 涵蓋（DA record 第 4.2 節）。沒有任何人驗證過作業系統對話框中可只用鍵盤多選，本 worklog 不作此宣稱 |
| UI0-8 可用合成資料檢查的介面條件；需要後端的列為整合後驗收 | **PASS（清單如下）** | 下方「UI0-8 清單」 |
| UI0-9 沒有真實資料；全部標示為模擬 | **PASS** | E-5；E-6 H-3 的模擬標示 |
| UI0-10 簡短紀錄 | **本節＋第 9.2 節＋第 10 節** | 第 10 節補上 R1-F1 的修正、R1-F2 的鍵盤操作紀錄與 UI0-7 的現況；依 `decision-20261118-issue12-ui07.md` 更新 UI0-7 列、UI0-2 限制 7 與第 10.2、10.3 節的 K3-B、K9 判定（原判定標明已取代）。UI0-7 的最終判定屬 R2 |

**元件的對應、替代與限制（UI0-2）**

| 元件 | 結果 |
| --- | --- |
| `st.expander`（Profile 區、公路與地標、全部候選）、`st.file_uploader`（`type=["gpx"]`、`accept_multiple_files=True`）、`st.button`、`st.status`（在 Profile 的 expander 之外、緊接其下）、`st.metric`、`st.table`、`st.info`／`st.warning`、`st.text_area`＋`st.caption`、`st.radio`（橫排、`index=None`）、`st.time_input`（標籤由 session state 決定）、`st.text_input`、`st.chat_message` 內 `st.radio`＋`st.button`、`st.container(border=True)` 內 `st.badge`／`st.metric`／文字／`st.caption`、`st.error` 加清單、`st.dataframe`（`on_select="ignore"`）、`st.tabs` | 照 Issue 的對照表使用，可以運作 |
| 另外使用的標準元件 | `st.container(horizontal=True)` 排列標籤；`st.date_input`、`st.number_input`、`st.toggle`（G3 沒有變更的欄位） |
| 限制 1：`st.file_uploader` 本身列出每個檔案的檔名與大小 | app 不顯示其他內容（C-2） |
| 限制 2：`st.dataframe` 的工具列有「Show/hide columns」與「Download as CSV」 | 元件內建，無法以參數關閉；表格本身是唯讀、沒有列的選取。UI_DESIGN 第 7 節排除的是表單內的下載按鈕，Issue 排除「計畫檔下載」；這個內建工具列由 UI Delta Review 判斷是否可接受 |
| 限制 3：`st.table` 的儲存格不能上色 | 高降雨機率提醒改以表格下方的琥珀色 `st.badge` 加文字列出（D-12-10） |
| 限制 4：`st.number_input` 若有非空的初值，AppTest 無法清空；瀏覽器中是否能清空沒有實測 | 情境 9 的出發油量預設為空，示範必填檢查（D-12-3） |
| 限制 5：`st.tabs` 不能以程式切換 | 與 G3 已知差異相同；Trip Result 是第一個分頁 |
| 限制 6：上傳的 multipart 解析由框架處理，超過 1 MB 的部分會暫時 spool 到暫存檔 | C-3 |
| 限制 7（R1 後新增，依 `decision-20261118-issue12-ui07.md` 第 6 節第 3 項）：`st.date_input` 的日曆彈窗 | 本環境中鍵盤焦點進不了彈窗（K9），沒有困住焦點；日期可以在同一元件的年／月／日欄只用鍵盤修改（K10）。元件前端有 `role=dialog` 與鍵盤操作說明，本環境的現象是元件還是工具造成的未確定 |

**UI0-8 清單**（`UI_CR01_DELTA.md` 第 11.1 節的條件）

| 條件 | Skeleton 以合成資料檢查的部分（結果） | 整合後驗收 |
| --- | --- | --- |
| CR-P1 | 多檔選取、按「更新 Profile」才處理（PASS） | 一個檔案也能更新的實際處理 |
| CR-P2 | 處理結果的三個數字與原因的顯示（PASS） | 重複上傳不增加行程數；`trip_id` 在更新前後相同 |
| CR-P3 | 三個數值與各類別的列（PASS） | 數值與實際資料一致 |
| CR-P4 | 沒有 GPX、某類別不足、都足夠三種說明（PASS） | 判定類別是否足夠 |
| CR-P5 | 固定的隱私說明；摘要沒有座標、日期時間、路線名稱（PASS） | 歷史 GPX 與逐趟資料確實不送給語言模型（U-7「後續的實作要驗證這個承諾」） |
| CR-P6 | 更新後舊結果過期；不觸發規劃（PASS） | — |
| CR-B1、CR-B2、CR-B3、CR-B5 | 欄位、期限名稱（含採用的條件）、欄位錯誤、行程描述的說明（PASS） | — |
| CR-B4 | 一輪、同一區塊、固定選項、沒有對話輸入框（PASS） | 由行程描述判斷缺少的項目 |
| CR-B6 | 命中時不送出、修改後可再規劃；Issue 的示範案例（PASS，簡化比對） | 確切的樣式（SPEC-001 7.12） |
| CR-B7 | 兩則目標 GPX 的路線錯誤的顯示（PASS） | 終點是否回到起點、折返點的判定 |
| CR-R1 | 路線確認區塊的內容、路權提醒（PASS） | 國道檢查本身 |
| CR-R2 | 七則路線錯誤的版面（PASS） | 各錯誤的觸發條件 |
| CR-R3 | Snapshot Mode 時的「資料快照」標籤（PASS，情境 14） | 快照的重用與嚴格模式 |
| CR-R4 | 里程差的句子與去回里程（PASS） | 百分比由結構化欄位算出且一致 |
| CR-C1 | 三種涵蓋比例句子（PASS） | 百分比與結構化欄位一致 |
| CR-C2 | 評估失敗不顯示計畫狀態與出發時間（PASS） | 評估未完成的判定 |
| CR-C3 | 模板文字與 Planner 補充說明的來源標示（PASS） | 規則 5 通過才顯示 |
| CR-C4、CR-C5、CR-C6 | 加油的去程／回程、去回兩次；預報時段與時段長度、UNKNOWN 的列；去回分表與固定句子（PASS） | 預報時段的實際格式與鄉鎮對應（等 C3） |
| CR-C7 | 騎士指定的休息顯示、追問的三種休息題（PASS） | 排入並計入 ETA；追問後仍對應不到的判定 |
| CR-C8 | 抵達時間的固定句子、預設餘裕係數的句子（PASS） | 是否使用預設值的判定 |
| CR-D1 | 唯讀、沒有列的選取、推薦／代表性失敗候選的標籤（PASS；限制 2） | — |
| CR-D2 | 代表性失敗候選與「這不是有效的建議」的呈現（PASS，情境 15） | 選法的實作 |
| F3、F4 | UI0-6、UI0-7 | — |

## 8. Audit status

- Formal：本 Ticket 的 independent audit 必要（Bindings 第 5 節；治理 §4.1）。依 run record，SPEC-UI0 不採 fast path，R1 是一般 Ticket audit，SIA 另派。
- 進度：R1 已完成（Codex，`docs/governance/records/audit/issue-12-c1-r1.md`，`Verdict: BLOCKING`；R1-F1、R1-F2 都是 Medium／blocking）。targeted correction 見第 10 節；R2 待 Orchestrator 派工。（R1 前本列寫「R1 尚未派工」。）
- 所涉高風險類別：H-2、H-3（DA 標示）；最終 diff 重新判定 H-1、H-4 不涉及（第 6 節 E-6），請 Reviewer 核對。
- 本 worklog 的 self-verification 不是 audit。

## 9. Remaining work

### 9.1 剩餘工作

- R1（Orchestrator 派工）；之後的 SPEC-UI0 SIA 與 DA phase acceptance。
- UI0-7 的 NOT VERIFIED 項目（依 `decision-20261118-issue12-ui07.md`：K3-B 為 #12 範圍外的 NOT VERIFIED；K9 為元件限制的觀察）與 UI0-6、UI0-7 的實際檢視，由 acceptor 在 UI Delta Review 進行（CL-UI0-4 末句）；UI Delta Review 不在本 run，也不是 #12 的 evidence（DA record 第 4.1 節）。
- 本 Ticket 不修改 `docs/ui/`（含 `UI_CR01_DELTA.md`）；下表與 Issue／DELTA 不一致之處由 UI Delta Review 之後的工作處理（CL-UI0-3）。

### 9.2 和 Issue 不一致或規格沒有定義之處、concerns

| ID | 內容 | 所需 authority |
| --- | --- | --- |
| C-1 | 規格缺口：情境 5 的組合——行程型態與休息地點都在同一輪追問、騎士回覆「來回」並選了途經點時，那段休息的方向沒有被問到（SPEC-001 4.1 規則第 3 項只在地點已知是途經點時才列方向題）。Skeleton 在這個組合顯示「未決定（模擬；規格沒有定義這個組合）」，不自行決定 | Design Authority（正式整合前裁決；不擋 Skeleton） |
| C-2 | CL-UI0-2「不顯示檔名以外的任何內容」：app 只顯示檔案數；Streamlit 的上傳元件本身會列出每個檔案的大小。是否符合 CL-UI0-2 的意思 | Design Authority |
| C-3 | CL-UI0-2「不寫入磁碟」與 H-2 判定 3.2 第 5 項：app 不寫入；Streamlit 1.67.0 的上傳經 Starlette 解析，超過 1 MB 的部分會暫時 spool 到系統暫存檔，之後只存在記憶體。本次合成檔不超過 48 B。正式整合處理真實 GPX 時需要決定是否接受（例如以 `server.maxUploadSize` 或其他方式處理） | Design Authority（正式整合的 Spec） |
| C-4 | 新增 root `.streamlit/config.toml`（D-12-2）；CL-UI0-1 規定程式放在 `app/`。這是 `streamlit run` 的設定檔，不是程式 | Reviewer 判斷；有疑義時 Design Authority |
| C-5 | Issue 沒有寫定的畫面文字（追問的起點、進入端、行程型態、休息長度的題目；欄位錯誤；過期提示；處理結果；模擬說明）與 D-12-6 的未選行程型態時的期限標籤 | acceptor 的 UI Delta Review（不需要在本 run 處理） |
| C-6 | 模擬結果不隨表單改變（D-12-5）：例如情境 9 改成「來回」後按規劃，結果仍是單向的模擬資料；「採用的條件」的日期、時間、油量、期限取自表單，其他是情境的值 | acceptor 的 UI Delta Review（Skeleton 的已知限制） |
| C-7 | `st.dataframe` 內建工具列的「Download as CSV」（UI0-2 限制 2） | acceptor 的 UI Delta Review |
| C-8 | 另加情境 15（無可行解），不是 Issue 的 14 個情境之一（D-12-11） | Reviewer 判斷是否在範圍內 |

C-1～C-3 不影響本 Ticket 的 AC 結果（Skeleton 沒有自行決定語義，也沒有處理真實檔案）；依治理 §2.4 由 Orchestrator route。

## 10. Cycle 1 R1 之後的 targeted correction（治理 §4.4）

- 依據：R1 record `docs/governance/records/audit/issue-12-c1-r1.md`（Codex `primary_reviewer`，受審 HEAD `e836c99`，`Verdict: BLOCKING`）的 R1-F1、R1-F2；Orchestrator 的 routing（同一 worklog identity）。DA record `decision-20261118-issue12-ui0.md`：C-1～C-3 對 #12 無要求，本節沒有為它們修改任何東西。
- 執行者與 binding：同第 2 節（agentId `acf4b1c528124a22e`，以 SendMessage 續派），第 10.5 節。
- 範圍：只修 R1-F1 並補 regression 測試；R1-F2 補做瀏覽器的鍵盤操作並如實更新 UI0-7、UI0-10。沒有修改驗收條件、`docs/ui/`、`prototype/`、R1 record 或 DA record。

### 10.1 R1-F1：單向回覆忽略了明確的取消

- **原因**：`rests_after_clarify` 在單向時不看方向題的回答，一律排入休息；`render_clarify_answers` 在單向時把整題回答改成「未使用（行程型態是單向）」，取消也被隱藏。Issue #12 §2：「回覆是單向時，『去程』『回程』的答案不使用。選『不安排這段休息』一律取消那一筆休息。」
- **修正**（`619268a`，`app/ui0_mock_app.py`）：方向題回答「不安排這段休息」時，單向與來回都不排入那一筆休息；單向只忽略「去程」「回程」（或沒有回答），休息照行程描述排入、不分方向；回覆表在取消時顯示「不安排這段休息」，只有「去程」「回程」或沒有回答時才顯示「未使用（行程型態是單向）」。Profile 的預設休息不是這一筆休息需求，不受影響（R1 record 亦同）。沒有加入 Validator、排程或 ETA 計算，CL-UI0-5 不變；H-4 的判定不變（顯示回覆，不是休息的排入）。
- **Regression 測試**（`tests/test_ui0_skeleton.py`，新增 8 個）：
  - `test_one_way_reply_with_no_rest_cancels_the_rest`：6b、單向＋取消 → 騎士指定的休息為空，回覆表顯示「不安排這段休息」，只剩 Profile 預設休息。
  - `test_one_way_reply_ignores_only_the_outbound_or_return_choice`（去程、回程、沒有回答三個參數）：休息照行程描述排入、方向「—」，回覆表顯示「未使用」。
  - `test_round_trip_reply_with_no_rest_cancels_the_rest`；`test_round_trip_reply_uses_the_chosen_direction`（去程、回程）；`test_known_round_trip_direction_no_rest_cancels_the_rest`（6a）。
  - 既有的「單向不必回答方向」「來回時方向必答」測試保留不變。
- **測試確實能抓到缺陷**：只把 `app/ui0_mock_app.py` 還原成 `6a278b4` 的版本（`git stash push app/ui0_mock_app.py`）時，`tests/test_ui0_skeleton.py` 的結果是 `1 failed, 54 passed`，失敗的是 `test_one_way_reply_with_no_rest_cancels_the_rest`；修正後 `55 passed`。
- **瀏覽器**：第 10.2 節 K12 以只用鍵盤的方式重做 6b 的單向＋取消，結果與測試相同（R2-N1 更正，原誤寫為 K9）。

### 10.2 R1-F2：只用鍵盤的瀏覽器操作紀錄

- Subject：工作目錄等於 `619268a`（修正已套用；`git status` 只有這兩個檔案被修改，之後 commit 為 `619268a`）。Streamlit 啟動：repo root，`.venv/Scripts/python.exe -m streamlit run app/ui0_mock_app.py --server.port 8501`（背景）；內建瀏覽器 `mcp__Claude_Browser__*` 開 `http://localhost:8501`；檢查結束後停止程序（PID 37600），`8501` 沒有 listener。視窗是 pane 的預設尺寸（375 像素的檢查見第 6 節 E-2，本節沒有改版面）。
- **規則**：本節所有操作都只用 `computer` 的 `key`／`type`（Tab、Shift+Tab、Enter、Space、方向鍵、Escape、Ctrl+A、輸入文字）。JavaScript 只用來**讀取**狀態（`document.activeElement`、`focusin` 事件的紀錄、元件的文字與值），沒有用 `focus()` 移動焦點，也沒有以程式點擊。兩個例外如實標明：K3 的攔截器、K4 的以程式放入檔案。
- 只用合成資料：檔名 `synthetic-empty-a.gpx`、`synthetic-empty-b.gpx`（0 B）、`synthetic-header-only.gpx`（48 B，只有 `<gpx version="1.1"></gpx>`），在瀏覽器記憶體中以 `File` 物件建立，沒有寫到磁碟；文字與路徑都是「示範…」或 `synthetic/…`。

| # | 操作 | 按鍵 | 結果（讀取的狀態） | 判定 |
| --- | --- | --- | --- | --- |
| K1 | 從頁面載入開始到情境選單，選情境 3 | Tab ×6（Skip to main content → Main menu → main → 兩個標題連結 → 模擬情境）；Ctrl+A；輸入 `3.`；Enter | 焦點 `INPUT 模擬情境`；畫面出現情境 3 的說明「畫面上已經有上次規劃的結果…」 | PASS |
| K2 | 打開 Profile，沒有選檔就按「更新 Profile」 | Tab（Profile summary）、Enter；Tab ×2（Upload → 更新 Profile）；Enter | Profile 展開；提示「還沒有選取任何 .gpx 檔。」；沒有處理結果 | PASS |
| K3 | 以鍵盤按「Upload」 | Shift+Tab（Upload）；Enter；Space | 為了不在使用者的桌面留下開著的 OS 對話框，事先在頁面掛一個 capture listener，記錄並取消 file input 的 `click`（只有這個作用）。Enter 與 Space 各送出一次選檔請求：`{multiple: true, accept: "application/streamlit,.gpx"}` ×2 | 按鈕可以用鍵盤啟動：PASS。對話框內選取多個檔案：**#12 範圍外，NOT VERIFIED**（K3-B；`decision-20261118-issue12-ui07.md` 第 4.2 節）。已取代的判定：「BLOCKED」 |
| K4 | 放入三個合成檔（**以程式放入，不是鍵盤**） | —（`input.files = DataTransfer` 加 `change` 事件） | 元件列出 `synthet...mpty-a.gpx 0.0B`、`synthet...mpty-b.gpx 0.0B`、`synthet...r-only.gpx 48.0B` | 不算鍵盤操作，只是讓 K5、K6 能進行 |
| K5 | 以鍵盤移除第二個檔 | Tab 走到 `Remove synthetic-empty-b.gpx`（focusin 紀錄：Remove a → Remove b → Remove header-only → Add files → 更新 Profile）；Shift+Tab 回到它；Enter | 清單只剩 `synthetic-empty-a.gpx`、`synthetic-header-only.gpx`。觀察：移除後焦點離開被移除的按鈕（`activeElement` 一度是 BODY），再按 Tab 從下一個控制項繼續 | PASS（焦點的移動記為觀察） |
| K6 | 以鍵盤按「更新 Profile」 | Tab／Shift+Tab 到 `更新 Profile`；Enter | 「處理結果（模擬，與選取的 2 個檔案的內容無關）：新增 3 個；略過 1 個內容重複的；1 個無法讀取…」；`st.status`「Profile 更新完成（模擬）」；「結果已過期。Profile 已更新。…」；分頁仍是 2 個（沒有自動規劃）；可用的行程數 12 | PASS |
| K7 | 行程描述的輸入（輸入保護命中） | Tab 到 `TEXTAREA 行程描述`；Ctrl+A；輸入「從中正路一段 123 號出發，走示範縣道丙到示範老街。」；Tab ×14 到「規劃」；Enter | textarea 的值是輸入的文字；欄位下方「行程描述中有看起來像門牌地址或座標的內容，系統沒有送出這段文字…」；上次的結果保留並標示「上次規劃後變更了：行程描述」。（第一次少按一個 Tab，焦點在標題連結上，沒有輸入任何字；退回後重做，如實記錄） | PASS |
| K8 | 行程描述改為公路寫法、目標 GPX 路徑、Snapshot Mode、規劃 | Shift+Tab ×14 回 textarea；Ctrl+A；輸入「從示範車站出發，不要走國道 3 號，改走台 9 線到示範老街。」；Tab ×12 到 `INPUT 目標路線 GPX 的檔案路徑`；輸入 `synthetic/keyboard-demo.gpx`；Tab 到 `Snapshot Mode`；Space；Tab 到「規劃」；Enter | checkbox 由 false 變 true；規劃後沒有輸入保護訊息、沒有過期提示；頁首「Snapshot Mode：目前顯示的結果使用固定的資料快照」；採用的條件「Snapshot Mode（固定的資料快照）」；路線確認有「資料快照」標籤；textarea 與路徑欄的值是輸入的文字 | PASS |
| K9 | 日曆彈窗 | Shift+Tab ×8 到 `Choose date`；Enter → 彈窗開啟（`role=dialog`，文字「Use arrow keys to navigate dates. Enter to select. Escape to close.」），焦點仍在按鈕；→、↓：日期不變、焦點不動；Tab：焦點跳到「最早可出發時間」的小時欄，彈窗關閉；Space 再開；Shift+Tab：焦點到日欄；Escape：彈窗關閉、焦點回按鈕 | 彈窗內有可聚焦的「Previous month」「Next month」等按鈕與日期格子，但在這個環境中**鍵盤焦點進不去**，沒有辦法用鍵盤在彈窗中選日期 | **觀察／元件限制，不是 UI0-7 的 FAIL**（`decision-20261118-issue12-ui07.md` 第 3 節；日期由 K10 完成）。已取代的判定：「FAIL（本環境觀察）」（K9-F） |
| K10 | 日期改用年／月／日欄 | Shift+Tab 到日欄；↑；Shift+Tab 到月欄；輸入 `11`；Tab ×2 | 日期 2026/12/06 → 2026/12/07 → 2026/11/07；過期提示列出「日期」 | PASS（選日期這件事可以只用鍵盤完成） |
| K11 | 最早可出發時間與出發油量 | 在小時欄按 ↑；Tab ×4 到出發油量；Ctrl+A；輸入 `55`；Tab | 最早可出發時間 12:00 → 13:00；油量 55；過期提示「上次規劃後變更了：日期、最早可出發時間、出發油量」 | PASS |
| K12 | R1-F1 的路徑（6b，單向＋取消） | Shift+Tab ×20 回情境選單；Ctrl+A；輸入 `6b.`；Enter；Tab ×19 到「規劃」；Enter；Tab ×2 到行程型態題；Space、↓（單向）；Tab 到方向題；Space、↓×2（不安排這段休息）；Tab 到「回覆並繼續規劃」；Enter | 回覆後沒有任何追問 radio；回覆表：行程型態「單向」、方向題「不安排這段休息」；休息表只有「示範觀景台／—／15 分鐘／依 Profile 排入的預設休息」，沒有騎士指定的那一筆 | PASS |

第一次 R1 前的操作（第 6 節 E-2 第 8、10、11 列，與第 7 節原 UI0-7 列所列的 Tab 走訪）仍然有效；那幾列中以 JavaScript `focus()` 移動焦點的部分，只作 375 像素量測的證據，不作鍵盤證據（R1 record 亦同）。

### 10.3 UI0-7 的現況

| 項目 | 判定 | 說明與所需 authority |
| --- | --- | --- |
| K1、K2、K5～K8、K10～K12，以及第 7 節列出的其他控制項（公路與地標 expander、分頁、全部候選 expander、追問的 radio） | PASS | 實際按鍵操作的紀錄在第 10.2 節與第 6 節 E-2 |
| K3「Upload」按鈕的啟動 | PASS | 選檔請求有送出；對話框以 listener 取消，沒有實際打開 |
| **K3-B 在作業系統的檔案選擇對話框中選取多個合成或空的 GPX** | **#12 範圍外，NOT VERIFIED**（`decision-20261118-issue12-ui07.md` 第 4.2 節）。已取代的判定：「BLOCKED」 | 缺少的能力：內建瀏覽器的工具（`mcp__Claude_Browser__*`）只能操作頁面，不能操作作業系統的對話框，也沒有上傳檔案的工具；為了不在使用者的桌面留下無法關閉的對話框，沒有實際打開它。檔案只能以程式放入（K4），那不是鍵盤操作。**required authority = acceptor**：在 UI Delta Review 中實際以鍵盤操作對話框，或另作決定。依上述 DA record，作業系統的原生檔案對話框不是 Skeleton 的畫面，不在 #12 的 UI0-7 範圍內；#12 範圍內的上傳操作由 K3、K5、K6 涵蓋。原記的「required authority = acceptor」已取代：acceptor 可在 UI Delta Review 檢視（CL-UI0-4 末句），不是 #12 結案的條件 |
| **K9-F 以鍵盤在日曆彈窗中選日期** | **觀察／元件限制，不是 UI0-7 的 FAIL**（`decision-20261118-issue12-ui07.md` 第 3 節）。已取代的判定：「FAIL（本環境觀察）」 | Streamlit 1.67.0 的 `st.date_input` 日曆彈窗在這個瀏覽器中，焦點無法進入彈窗（Enter／Space 開啟、Tab 離開時關閉、方向鍵沒有作用）。日期本身可以只用鍵盤在年／月／日欄改（K10），所以「選日期」的操作可以完成；但日曆彈窗這個控制項不能只用鍵盤操作。沒有修改元件或驗收條件。是否以年／月／日欄滿足 UI0-7、或要求改用其他元件，**required authority = acceptor**（UI Delta Review）；如需修改契約或元件對應，經 Design Authority。依上述 DA record 第 3.1、3.2 節，UI0-7 以操作為單位，「設定日期」已由 K10 只用鍵盤完成，彈窗沒有困住焦點；不需要修改程式。原記的 required authority 已取代；是否在正式整合要求彈窗本身可用鍵盤，屬 DELTA 11.2「驗收清單定稿時確認」的事項（DA record 第 3.3、7 節） |
| K5 的焦點移動（移除檔案後焦點離開該按鈕） | 觀察，不是失敗 | 下一個 Tab 從下一個控制項繼續；交 UI Delta Review 檢視 |

依 `decision-20261118-issue12-ui07.md` 第 4.3 節，UI0-7 在 #12 範圍內沒有 BLOCKED 或 FAIL 的部分；各操作的鍵盤證據是否足夠、UI0-7 是否 PASS、R1-F2 是否 RESOLVED，由 R2 判定，本 worklog 不宣告。本 worklog 不以「標準元件」推定任何未操作的項目。（已取代的敘述：「UI0-7 因 K3-B（BLOCKED）與 K9-F（FAIL）**不能標為 PASS**」。）

### 10.4 Gates（主 checkout，`619268a` 的工作目錄）

`.venv/Scripts/python.exe -m pytest -q`：

```text
........................................................................ [ 11%]
........................................................................ [ 23%]
........................................................................ [ 35%]
........................................................................ [ 47%]
........................................................................ [ 58%]
........................................................................ [ 70%]
........................................................................ [ 82%]
........................................................................ [ 94%]
...................................                                      [100%]
611 passed in 22.97s
```

`.venv/Scripts/python.exe -m pytest -q -rxX`：

```text
........................................................................ [ 11%]
........................................................................ [ 23%]
........................................................................ [ 35%]
........................................................................ [ 47%]
........................................................................ [ 58%]
........................................................................ [ 70%]
........................................................................ [ 82%]
........................................................................ [ 94%]
...................................                                      [100%]
611 passed in 22.50s
```

611＝603＋8 個 R1-F1 regression 測試；沒有 xfail、xpass、skip（`-rxX` 沒有任何摘要列）。correction commit 的檔案 SHA-256（工作目錄 LF 內容）：`app/ui0_mock_app.py` `1aecf7ac35711c5a35e8f3b1765f5f242a5583b58fdf4281339a5e58b81639d0`、`tests/test_ui0_skeleton.py` `77deefffd8b8e6a300fa470acd7a424117921dd61fa36fc0bf6899487f7eef61`。`git diff --name-only 6a278b4 619268a` 只含這兩個檔與 record 路徑。暫存內容沒有 `.env`、`*.gpx` 或 `data/` 的檔案。

### 10.5 Binding、高風險類別與剩餘工作

- Binding 自我觀測：見第 10.6 節（record-only commit 前掃描）。這是自我觀測，Orchestrator 採用前須自行核對。
- 高風險類別：修正只改追問回覆的顯示與模擬休息列，H-2（上傳的處理不變）、H-3（沒有新的宣稱文字；新增的只有既有常數的使用）的核對結果不變；H-1、H-4 仍不涉及。
- K3-B 與 K9 依 `decision-20261118-issue12-ui07.md` 改記為範圍外的 NOT VERIFIED 與元件限制的觀察（已取代的敘述：「R1-F2 的 BLOCKED（K3-B）與 FAIL（K9-F）由 acceptor 處理」）；交 acceptor 的資訊見該 record 第 7 節；R1 record 的 NV-1～NV-4、Q-1 不屬本次 correction 的範圍，本節沒有處理。
- 剩餘：R2（Orchestrator 派工；只核對 R1-F1、R1-F2 的修正與回歸）。

### 10.6 Binding 自我觀測（correction 之後）

agentId `acf4b1c528124a22e`（`agentType` `gov-executor`，同第 2 節的派工，correction 以 SendMessage 續派），全部 assistant 訊息 (`claude-opus-5-5`, `high`) 346 則，集合只有一個元素（record-only commit 前掃描）。沒有 escalation、替代或 bounded assignment。

### 10.7 依 Design Authority record 的更新（record-only）

- 依據：`decision-20261118-issue12-ui07.md`（Design Authority，commit `efea0dd`），第 6 節「對 #12 的要求」第 1～5 項。
- 更新的位置：檔首「狀態」列；第 7 節 UI0-7、UI0-10 列與 UI0-2 的限制 7（新增）；第 9.1 節；第 10.2 節 K3、K9 列的判定；第 10.3 節的 K3-B、K9-F 列與末段；第 10.5 節。每一處都引用該 record，原先的判定以「已取代」標明保留。
- 沒有修改 `app/`、`tests/`、`.streamlit/`、`pyproject.toml`；沒有重做瀏覽器操作；受審的實作 subject 仍是 `619268a`。
- 本節不宣告 UI0-7 PASS，也不宣告 R1-F2 RESOLVED；由 R2 判定。

## 11. Cycle 1 R2 之後的結尾紀錄（record-only）

本節由 Executor（同一 worklog identity，agentId `acf4b1c528124a22e`，Orchestrator 以 SendMessage 續派）依 Orchestrator 的派工寫入。只修改本 worklog；`app/`、`tests/`、`.streamlit/`、`pyproject.toml`、`docs/ui/`、`prototype/` 都沒有變更。本節**不**宣告 Ticket closure、SPEC-UI0 的 SIA 或 phase acceptance、acceptor 的 UI Delta Review 或 release；Ticket closure 由 Orchestrator 依 orch-default §7 判定。

### 11.1 R2 的結果

- Record：`docs/governance/records/audit/issue-12-c1-r2.md`（Codex `primary_reviewer`，cycle 1 R2，attempt 2；commit `badebc1`；本次讀到的 SHA-256 `f81c482d7dc711889e844439f8cf95c845b5c8a9a8caee0b0ce17897899ede34`）。**`Verdict: PASS`。**
- **R1-F1：RESOLVED**（單向回覆＋「不安排這段休息」取消那一筆休息；`619268a` 的修正與 regression 測試）。
- **R1-F2：RESOLVED**（依 `decision-20261118-issue12-ui07.md` 的 clarification；K3-B 維持 #12 範圍外的 NOT VERIFIED，K9 維持元件限制、原因未確定）。
- **R2-N1**（Low／non-blocking，owner #12 Executor）：worklog 第 7 節 UI0-4 列與第 10.1 節的瀏覽器說明把取消休息的鍵盤操作誤指為 K9，實際是 K12。**已在本次更正**：兩處都改為 K12，並註明「R2-N1 更正，原誤寫為 K9」；第 10.2 節的 K9、K12 操作紀錄本身沒有改動。
- R2 attempt 1 因 Codex usage limit 失敗，沒有 record 或 verdict（`ca91406` 的 run record 紀錄）；attempt 2 的 binding 證據由 Orchestrator 記在 run record（`eac676b`）。R2 record 的 NV-R2-3（dispatcher 的 binding 核對）由 Orchestrator 處理，不是本 worklog 能完成的事。

### 11.2 Q-1、Q-1b 的 disposition

- 依據：Design Authority 的 `docs/governance/records/decisions/decision-20261118-issue12-q1.md`（commit `6b9f611`；SHA-256 `19172c4f6d9744c6d581d6b1f76b7369a59f7970b3783d3b156cddbdbcc61c7a`）。
- **Q-1（「資料快照」標籤）**：Issue #12 第 4 節只要求代表路線快照的情形顯示該標籤（Snapshot Mode，或一般模式下重用 30 天內的快照），不要求所有 engine 模擬情境都顯示。現行實作（表單的 Snapshot Mode 為真時顯示）與證據滿足 #12，**不需要 targeted correction 或補充 evidence**。
- **Q-1b（「示範路線」來源標籤）**：#12 沒有要求在 Skeleton 中呈現示範路線的來源標籤或為它建立情境（CR-01 之後的 Trip Planner 沒有能得到示範路線的輸入）。對 #12 **沒有要求**。示範路線在 Streamlit 中是否、如何出現是**規格缺口**，歸之後正式整合的 `app/` Spec（owner：該 Spec 的 Design Authority）；若要讓騎士在介面上選用示範路線，牽涉 CR-B1，需要 acceptor。

### 11.3 最終的受審 subject

- **最後的實作 commit：`619268ad2732b4cdd04593ff20ebe35374a7710c`（`619268a`）**。它之後沒有任何修改 `app/`、`tests/`、`.streamlit/`、`pyproject.toml` 的 commit。
- **R2 的受審 subject：`ca91406187a8c5877ae8d23b6f8fd09749d1e40f`（`ca91406`）**。`git diff --name-only 619268a ca91406` 只含 `docs/governance/records/**`（DA record `decision-20261118-issue12-ui07.md`、run record、本 worklog）；`ca91406..6b9f611` 也只含 record 路徑（R2 record、Q-1 DA record、run record）。依 Bindings 第 7 節與 orch-default §7 P7，這些 record-only delta 不改變受審 subject 的 identity。本節的 commit 同樣是 record-only。

### 11.4 Gate：pytest（本節的最終 HEAD）

在主 checkout 執行 `.venv/Scripts/python.exe -m pytest -q`。工作目錄是 `6b9f611` 加上本 worklog 的修改（只有本檔；`git diff -- app tests .streamlit pyproject.toml` 沒有輸出），程式與測試和本節 commit 完全相同：

```text
........................................................................ [ 11%]
........................................................................ [ 23%]
........................................................................ [ 35%]
........................................................................ [ 47%]
........................................................................ [ 58%]
........................................................................ [ 70%]
........................................................................ [ 82%]
........................................................................ [ 94%]
...................................                                      [100%]
611 passed in 23.96s
```

與第 10.4 節（`619268a`）相同：611 passed，沒有 skip、xfail。

### 11.5 仍在追蹤的事項與 owner

| ID | 內容 | Owner／required authority |
| --- | --- | --- |
| NV-R2-1 | R2 reviewer 沒有瀏覽器，沒有親自重跑 UI0-6 的 375 像素量測或 UI0-7 的實體鍵盤流程；R2 評估的是本 worklog 的逐步紀錄 | acceptor：依 CL-UI0-4 在 UI Delta Review 實際檢視（本 run 之外） |
| NV-R2-2 | K3-B 的 OS 原生檔案對話框中只用鍵盤多選沒有人驗證；K9 彈窗焦點問題的原因（元件或工具）未確定；本 worktree 沒有原始的瀏覽器 transcript、截圖或 scratchpad scripts | acceptor（UI Delta Review）；需要補原始 evidence 時 owner 是 #12 Executor；之後的逐元件要求由 Design Authority 依 DELTA 11.2 處理 |
| NV-R2-3 | R2 attempt 2 的 binding、存取與 record 寫入的完整核對 | dispatcher／Orchestrator（run record；不是 #12 的 implementation finding） |
| NV-R2-4 | 真實騎乘資料、真實 GPX 的保存與隱私裁切、框架 spool 的生命週期、正式 API 與後端行為：本票排除，沒有執行，也沒有私有資料授權 | acceptor（RB-7 的資料授權與之後的實際驗證）；保存與整合的語義由 Design Authority |
| C-4 | root `.streamlit/config.toml`（D-12-2）；R1 判定為契約內的 HOW，沒有 scope finding | #12 Executor 維護既有紀錄（無待辦） |
| C-5～C-7 | Issue 沒有寫定的畫面文字與未選行程型態時的期限標籤（C-5）；模擬結果不隨表單改變（C-6）；`st.dataframe` 內建的「Download as CSV」（C-7） | acceptor 的 UI Delta Review（tracked；不代表已接受為產品行為） |
| C-8 | 另加的情境 15（無可行解）；R1 判定在範圍內，沒有 scope finding | #12 Executor 維護既有紀錄（無待辦） |
| K3-B | 作業系統的原生檔案對話框中只用鍵盤多選 GPX：#12 範圍外，NOT VERIFIED（`decision-20261118-issue12-ui07.md` 第 4.2 節） | acceptor 可在 UI Delta Review 檢視（CL-UI0-4 末句）；不是 #12 結案的條件 |
| K9（資訊） | `st.date_input` 的日曆彈窗在本環境中鍵盤焦點進不去，沒有困住焦點；日期可只用鍵盤以年／月／日欄修改（K10）；UI0-2 限制 7 | acceptor 可在 UI Delta Review 提出；正式整合是否加入逐元件要求，屬 DELTA 11.2「驗收清單定稿時確認」的事項（Design Authority；改變 P-11 的語義時經 acceptor） |
| Q-1b 規格缺口 | 示範路線在 Streamlit 中是否、如何出現，以及路線確認區塊的「示範路線」標籤 | 之後正式整合的 `app/` Spec 的 Design Authority；要讓騎士選用示範路線時牽涉 CR-B1，需要 acceptor（`decision-20261118-issue12-q1.md` 第 7 節） |

C-1～C-3 依 `decision-20261118-issue12-ui0.md` 對 #12 沒有要求，相關的整合條件由之後的整合 Spec 處理（該 record 第 2.4、4.4 節）。

### 11.6 Binding

本節由 agentId `acf4b1c528124a22e`（`gov-executor`，有效 mapping `claude-opus-5-5`／`high`）寫入；沒有派工任何 subagent。本節 commit 前的自我掃描：全部 assistant 訊息 (`claude-opus-5-5`, `high`) 369 則，集合只有一個元素。這是自我觀測，Orchestrator 採用前須自行核對。
