# 審查證據：原始 Proposal 與課程要求

## 0. 頁碼慣例與讀取限制

- **頁碼一律用 PDF 實體頁碼**（第 1 頁＝檔案第一頁）。`proposal.pdf` 共 43 頁，頁面上沒有印頁碼；目錄（p.2–3）所列頁碼與實體頁碼一致（Abstract=4、Introduction=5、附錄 A=43）。`Part_3._課程專題說明.pdf` 共 8 頁、`L4-1_期末計劃Proposal_寫作方法_.pdf` 共 17 頁，頁尾印的頁碼都等於實體頁碼。
- `requirements_proposal.txt` 沒有頁，改標**行號**（L 開頭）。
- 讀取方式：Read 工具的 PDF 轉圖功能不可用（缺 pdftoppm），改用 PyMuPDF 逐頁抽文字，並把圖頁另外轉成圖檔檢視（proposal p.1、p.25 架構圖、p.31 流程圖；Part 3 p.2；L4-1 p.2、p.4）。其餘頁只讀抽出的文字，表格以線性化文字判讀。
- 無法讀取：L4-1 p.1、p.3 列出的附件（`A2Z outline example.docx/pdf`、`.wmv`、`.mov`、YouTube 連結、L4-2／L5／L6 講義）只有檔名，內容不在來源資料夾內。p.28–30 的數學式抽出後排版零散，但符號與式子可辨識。
- 簡稱：**P**＝proposal.pdf；**R**＝requirements_proposal.txt；**P3**＝Part_3 PDF；**L41**＝L4-1 PDF；**圖**＝`期未計劃-架構圖建議.png`（與 P3 p.2 為同一張圖）。

---

## A. 原始 Proposal

### A1. 題目、組別、問題與目的

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| 題目 | 重機旅遊規劃顧問（Moto Touring Copilot）；副題「結合個人配速模型與外部驗證的多 Agent 重機旅遊規劃系統」 | P p.1 |
| 課程／組別／日期 | 物聯網應用與資料分析（AIoT-DA）期末專題提案；第 12 組；2026 年 11 月。組員姓名：未載明 | P p.1 |
| 問題 | 騎士出發前想知道「照我的騎法，幾點出發才能在天黑前回家、哪裡加油、哪一段有風險」；一般導航只給群體平均預估時間，重機 App 著重路線，LLM 單獨規劃在 TravelPlanner 最終通過率 0.6%；預報、日落、路況、加油站資料分散，要騎士自己換算時間 | P p.4、p.6–7 |
| 問題定義 | 給定起訖點、途經路線、日期與騎士歷史 GPX，產生「可驗證的行程計畫」：建議出發時間（附範圍）、加油點、各路段風險說明，並附每個數字的資料出處 | P p.6 |
| 目的／定位 | 「個人化的出發前決策輔助，不做事故預測」；不宣稱能降低事故率 | P p.5、p.7 |

### A2. 研究問題與假設（Proposal 沒有 RQ／H 編號，以下依原文編號）

| 原文編號 | 內容（原文短引） | 來源 |
| --- | --- | --- |
| 1.3-1 | 個人化的時間預測：預測每段要騎多久，「並給出範圍，而不是單一數字」 | P p.6 |
| 1.3-2 | 時間對齊的風險查詢：依「預計抵達該路段的時間」查預報、日落、路況 | P p.6 |
| 1.3-3 | 跨條件的一致性檢查：時間加總、回程是否在日落前、加油距離是否超過續航 | P p.6 |
| 4.1-1 | 「這趟路以我自己的騎法要騎多久？最晚幾點會回到家？」 | P p.24 |
| 4.1-2 | 「依各路段的預計抵達時間，天氣、日照和路況是否允許？」 | P p.24 |
| 4.1-3 | 「依續航和加油站營業時間，哪裡加油才不會沒油？」 | P p.24 |
| E1 | 「個人配速模型比一般導航的時間估計準嗎？」 | P p.34 |
| E2 | 「外部驗證能不能提高計畫的可行率？」 | P p.34 |
| E3 | 「風險規則是否抓得到歷史封路日？」 | P p.34 |
| E4 | 「對騎士有沒有實際價值？」 | P p.34 |
| 假設 a（預期成果） | 個人配速模型在彎道多的山區路段，整趟時間誤差低於一般導航的估計 | P p.34 |
| 假設 b | 完整 Agent 的計畫對獨立 oracle 的違規率低於只用 LLM 的版本 | P p.34 |
| 假設 c | 拿掉個人配速或天氣、路況資料後，違規率或時間誤差上升 | P p.34–35 |
| 聲明 | 「這些是待驗證的假設」；摘要：「以上成效均為待驗證的假設，本提案不含實驗結果」 | P p.35、p.4 |

### A3. 功能承諾（Proposal 沒有 FR／NFR 編號；M1–M5 在文中是「思維模式」，不是模組）

| 名稱 | 承諾內容 | 來源 |
| --- | --- | --- |
| 輸入 | 起點、路線（或途經點）、出發日期、騎士限制（最晚回程時間、最長騎乘時數）、騎士歷史行程 | P p.24 |
| 輸出 | 可行的行程計畫：建議出發時間、各段預計抵達時間範圍（P50／P90）、加油點、風險說明；無可行計畫時說明哪個條件無法滿足 | P p.24 |
| ① 使用者與情境 | 在台灣騎重機旅遊的騎士；行程規劃、出發前檢查天氣與路況、油量與加油點；L3 延伸為騎乘中提醒 | P p.26 |
| ② 問題輸入 | Web 對話介面；用地名描述行程，或在地圖上選點；匯入 GPX 建立與更新個人配速 | P p.26 |
| ③ Planner & Reasoning | 五個 Agent 分工；驗證不通過就重新規劃；記住騎士偏好與過去計畫 | P p.26 |
| ④ 資料取得 | 自己的 GPX、氣象署、TDX、內政部地形（DTM）、OpenStreetMap、中油加油站、Google Maps Routes API | P p.26 |
| ⑤ Analytics Engine | 個人配速模型（P50／P90）、天氣與路況風險規則、續航與加油站檢查、日照檢查；「全部是確定性的 Python 工具」 | P p.26 |
| ⑥ Domain Knowledge | 知識庫檢索（氣象署警特報說明、公路局行車資訊、騎乘安全資料、BMW 車系規格、相關研究）；回答附出處 | P p.26 |
| ⑦ 決策與建議 | 建議出發時間、各段抵達時間範圍、加油點、風險排序與理由；不可行時說明原因與替代方案 | P p.26 |
| ⑧ 輸出與互動 | 對話回答；Google Maps 行程儀表板（路段依時間與風險上色、加油站、日落時間）；可下載的行程計畫 | P p.26 |
| 規劃 Agent | 輸入：使用者問題、騎士記憶；輸出：任務分派、彙整後的計畫草案；工具：知識庫檢索 | P p.26 |
| 配速分析 Agent | 輸入：路線、出發時間、騎士 ID；輸出：各段 P50／P90 時間、各點 P50 與 P90 預計抵達時刻；工具：路線切段、地形特徵、配速模型、Google 預估時間 | P p.26 |
| 天氣 Agent | 輸入：各段位置與 P50／P90 抵達時刻；輸出：各段降雨機率、溫度、警特報、民用暮光終；工具：氣象署預報、觀測、日出日沒資料 | P p.26 |
| 路況與補給 Agent | 輸入：路線、各點 P90 抵達時刻、車型；輸出：路況事件、可用加油站（含營業時間）、續航檢查；工具：TDX、中油加油站、車系規格 | P p.26–27 |
| 驗證 Agent | 輸入：完整計畫草案；輸出：通過，或違反的規則清單；以程式規則檢查，不讓 LLM 判斷可行性 | P p.27、p.20 |
| 驗證規則 1 日照 | d + T(0.9) ≤ min(T_dusk, T_user)（整趟 P90 回程不晚於民用暮光終或騎士設定時間） | P p.29、p.19 |
| 驗證規則 2 續航 | 相鄰補給點（含起點）距離 ≤ R×(1−m)；且抵達加油站的 P90 時刻落在營業時間內 | P p.29 |
| 驗證規則 3 天氣 | 抵達時段 [ETA(0.5), ETA(0.9)] 與大雨以上警特報重疊→高風險；高風險段不得位於日照限制最緊的最後一段 | P p.29 |
| 驗證規則 4 路況 | 路段有 TDX 封閉或管制事件時，計畫不可行 | P p.29 |
| 驗證規則 5 可追溯 | 回答中每個時間、距離、機率都必須出現在工具輸出中 | P p.30 |
| 決策 | 候選出發時間（例如每 30 分鐘一個）中，選回程餘裕最大且高風險路段最少者；無可行解時回報違反規則並提替代方案（縮短路線、提前出發、改日） | P p.30 |
| 重新規劃 | 驗證不通過即重新規劃，「設次數上限」（MAX_ATTEMPTS，數值未載明） | P p.7、p.32 |
| 例外處理 | 外部 API 失敗時回報「資料不可用」，相關規則視為未通過並說明，「不以猜測補值」 | P p.31 |
| 記憶與休息 | 跨對話記憶保存最長連續騎乘時數，自動插入休息點並計入時程；SAVE_MEMORY | P p.19、p.32 |
| 封路處理 | 不自行發明封路門檻；封閉資訊無法機器取得時標示「出發前需人工確認」並附公路局來源；每條山區路線預先產生折返點與替代路線 | P p.20 |
| 配速模型更新 | Algorithm 2：TRIM_ENDS、CLEAN_SPEED、SPLIT_MOVING、分段特徵、GROUP_KFOLD、分位數 GBM、c_0.9 | P p.32 |
| 使用流程（流程圖） | 騎士提問或匯入 GPX →（匯入：清理車速跳點→切路段→算特徵→更新配速模型）／（提問：規劃 Agent 理解需求→資訊不足則追問→配速 Agent→天氣與路況補給 Agent→組成草案→驗證規則 1–5→通過則產生建議；未通過且次數未滿則調整出發時間、加油點、路線；次數已滿則說明不可行原因與替代方案）→輸出（對話＋Google Maps 儀表板＋行程計畫）→騎士要修改則回到理解需求，否則寫入騎士記憶 | P p.31（圖 2） |
| 範例旅程 | 新竹出發走南橫當天來回、晚上七點前回家的六步驟示意（數值為示意） | P p.32–33 |
| 非功能需求 | 回應時間、可用性、成本上限、測試覆蓋等：未載明 | — |

### A4. 架構

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| Agent 數 | 五個：規劃（Orchestrator）、配速分析、天氣、路況與補給、驗證；另有「騎士記憶：偏好、歷史計畫」資料庫 | P p.4、p.7、p.25（圖 1）、p.26–27 |
| LLM 分工 | LLM 只負責理解需求、分派工作與解釋結果，「數字一律來自工具計算」 | P p.7 |
| LLM／框架 | 「支援工具呼叫的 LLM API（供應商待定）、自行撰寫的多 Agent 迴圈」 | P p.33 |
| 天氣、日出日沒 | 氣象署開放資料 API（預報、警特報、民用暮光終）；CODiS 歷史觀測供訓練 | P p.33、p.28 |
| 路況 | 交通部 TDX 省道即時路況；「道路阻斷沒有找到機器可讀來源」 | P p.33 |
| 加油站 | 中油加油站資料（位置、營業時間，最後更新 2024-05）。p.16–17 另寫「中油與台糖加油站」，p.33 資料表只列中油（文內不一致） | P p.33、p.16–17 |
| 地形與路網 | 內政部 20 m DTM、OpenStreetMap；公路局 GIS（急彎、陡坡、速限） | P p.33 |
| Google Maps 用途 | Maps JavaScript 顯示地圖；Routes API 兩輪車預估時間作為 baseline 與配速 Agent 的工具；「費用待確認」 | P p.33、p.26 |
| 配速模型 | 目標為路段移動時間的對數；Baseline：平均速度、速限換算、Google Maps 兩輪車預估時間；模型一：多元迴歸；模型二：LightGBM 分位數損失（q=0.5、0.9） | P p.28–29 |
| 整趟 P90 | 各段 P50 相加＋休息時間 B＋conformal 校正量 c_0.9（依行程分組的保留資料殘差第 90 百分位）；各點 P90 抵達時刻依已騎里程比例分攤 c_0.9；各段 P90 只用於地圖上色，不加總 | P p.29 |
| 知識庫 | RAG 檢索；狀態「待蒐集」 | P p.33 |
| 介面 | Streamlit + Google Maps（Web 對話與儀表板）；地圖依路段時間與風險上色、時間軸、行程計畫 | P p.33、p.27 |
| IoT／裝置 | SENSE：騎士 GPX（約 1 秒一點）與政府開放資料；L3 延伸：手機定位 App→MQTT（家中 RPi 5）→即時更新抵達時間與語音提醒；「不在車上加裝任何東西」 | P p.27、p.28、p.33–34 |
| 分析工具 | pandas、scikit-learn、statsmodels、LightGBM、OSMnx、地圖比對工具 | P p.33 |
| 課程框架對應 | ③-1 至 ③-6 Workflow、六大能力、Level 對應表 | P p.27–28 |

### A5. 資料

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| 行程資料 | BMW Motorrad Connected 匯出的 GPX，279 趟；單一騎士（n = 1）；「279 趟 GPX 已在手上」 | P p.33、p.8、p.35 |
| 已確認程度 | 只「已檢查一趟」：約 1 秒一點，有經緯度、高度、時間 | P p.33、p.35 |
| 路段與特徵 | 路段約 0.5–2 km（或依道路切分）；特徵：曲率（每公里轉角、最小半徑）、坡度（DTM）、道路等級、公路局急彎與陡坡標記、時段、天氣、已騎里程 | P p.28 |
| 驗證切分 | 依行程分組的交叉驗證；以最新行程做時間外推測試；「熟悉／不熟悉路線」分開報告誤差 | P p.7、p.34、p.21 |
| 隱私 | 原始檔不進 repo；裁掉頭尾（TRIM_ENDS）；只公開衍生資料 | P p.35–36、p.32 |
| 資料品質對策 | GPX 高度雜訊→坡度改用 DTM；車速跳點→平滑 | P p.35 |

### A6. 實驗與評估

| 實驗 | 問題 | 方法／對照組 | 題數 | 指標 | 成功標準 | 來源 |
| --- | --- | --- | --- | --- | --- | --- |
| E1 配速模型 | 個人模型比一般導航準嗎 | 平均速度、速限換算、Google 兩輪車預估時間 vs 多元迴歸 vs LightGBM；依行程分組交叉驗證＋最新行程時間外推 | 不適用 | 路段與整趟 MAE、MAPE；整趟 P90 覆蓋率 | 只有方向（假設 a）；數值門檻未載明 | P p.34 |
| E2 驗證與消融 | 外部驗證能否提高可行率 | 三組：只用 LLM／LLM + 知識庫／完整 Agent（工具 + 驗證）；另以完整 Agent 為基準逐一拿掉個人配速模型（改用 Google 預估時間）、天氣資料、路況資料 | 約 20–30 題 | oracle 違規率、回程時間對 oracle 的誤差、數字與 oracle 一致率、拒答／不可行報告率、候選出發時間數 | 只有方向（假設 b、c）；數值門檻未載明 | P p.34、p.8 |
| E2 的 oracle | — | 每題事先以獨立腳本（不經 Agent 與其工具）算出：民用暮光終、沿線加油站營業時間、該日已知管制事件、以實際騎過行程為準的各段時間；不以規則 1–5 自評，避免循環驗證 | — | — | — | P p.34 |
| E3 風險規則 | 規則是否抓得到歷史封路日 | 以歷史封路紀錄回測；敏感度分析 | 未載明 | 命中率、誤報率 | 未載明；「不宣稱預測事故」 | P p.34 |
| E4 案例研究 | 對騎士有沒有實際價值 | 2–3 個完整情境；以過去實際行程回測預測回程時間與實際的差 | 2–3 案 | 質性說明與回測誤差 | 未載明 | P p.34 |

### A7. 範圍

| 類別 | 內容 | 來源 |
| --- | --- | --- |
| 承諾範圍 | L2 Knowledge Agent：知識庫檢索、多 Agent 多步推理、驗證與重新規劃——「承諾完成」；L1（對話介面、讀取 GPX 與開放資料、Python 分析、圖表）「包含在 L2 內」 | P p.28、p.35 |
| 延伸 | L3 IoT Autonomous Agent：騎乘中手機定位經 MQTT 回傳、即時更新抵達時間並語音提醒——「延伸，期末視進度」；「不在 Proposal 承諾範圍內」 | P p.28、p.8 |
| 延伸 | 道路阻斷資料（沒有機器可讀來源與歷史紀錄）列為延伸；先用 TDX 即時路況 | P p.35 |
| 不做 | 事故預測；不宣稱降低事故率（沒有因果證據）；不自行發明封路門檻；不在車上加裝任何東西 | P p.7、p.35、p.20、p.33 |
| 適用限制 | 只有一位騎士，結論限於個人化情境；風險評分沒有正確答案 | P p.8、p.35 |

### A8. 交付物與時程

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| 時程、里程碑、日期 | 未載明（全文沒有時程表或里程碑；只提到實驗在「期末」驗證） | P p.7、p.34 |
| 期末交付清單 | 未載明（Proposal 沒有列期末交付物；系統輸出為對話、Google Maps 儀表板、可下載行程計畫） | P p.26 |
| Proposal 階段產物 | 附錄 A 提到 Word、PDF、PPT、簡報影片，以及 GitHub 上的 `final_project/doc/proposal/ai-usage-log.md`、`doc/brief/architecture-scope.md`、`final_project/tools/` | P p.43 |

### A9. 預期成果的明確宣稱

| 宣稱 | 來源 |
| --- | --- |
| 「預期可量化個人模型在山區路段與導航預估時間的差距」 | P p.7 |
| 「預期產出可檢查、可追溯的行程計畫」 | P p.7 |
| 「預期提供一套可重複使用的資料取得與前處理流程」 | P p.8 |
| 「預期能說明工具計算與驗證迴圈各自帶來多少改善」 | P p.8 |
| 個人配速模型在彎道多的山區路段整趟誤差低於一般導航；完整 Agent 違規率低於只用 LLM；拿掉模組後變差 | P p.34–35 |
| 系統輸出是可解釋的建議而不是單一預估時間（例句：某段 14:20 抵達、有大雨特報、建議 13:30 前通過） | P p.35 |
| 可行性宣稱：資料來源都已確認可取得；同一套流程已在公開汽車資料集 VED 跑通（僅證明流程可行，不是本題結果） | P p.35 |
| 預期較弱處：沒騎過的路線個人模型可能退化；塞車路段 Google Maps 可能較準 | P p.22 |

---

## B. 課程要求

### B1. 專題必備要素、Level、架構期待

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| 核心要求 | 「AI Agent + Domain Knowledge + Data Analytics + Real-World Application」；不應只訓練一個 Model 或做單純 Chatbot，要設計 Domain AI Agent：理解需求、取得與分析資料、結合領域知識推理、提供有依據的結果 | R L21–25、L202–203 |
| 基本架構 ①–⑧ | User/Application Scenario → Query/Input → Planner & Reasoning Agent → Data Acquisition/Retrieval → Analytics Engine → Domain Knowledge Integration → Decision/Recommendation → Output & Interaction | R L115–122 |
| 資料來源 | 「可以包含」IoT Sensor、Database、CSV/Excel、API、Web、Open Data、PDF/Paper、Knowledge Base、Vector DB | R L124 |
| 三種技術表示 | System Architecture（模組編號並逐一說明）、Flowchart、具行號的 Pseudocode | R L126–151 |
| Agent Workflow | ③-1 Understand → ③-2 Plan → ③-3 Acquire → ③-4 Analyze → ③-5 Generate → ③-6 Interact，「所有學生作品可以共同遵循」 | P3 p.4 |
| 六大能力 | TALK × KNOW × SENSE × ANALYZE × THINK × SHOW | P3 p.4–5 |
| IoT 的定位 | ⑤-1 IoT Data「保留了本課程最重要的 IoT 核心特色」；⑤-2 同頁寫「很多實際的 AI 應用不需要感測器」 | P3 p.5 |
| 分析原則 | 「LLM 負責理解、推理與解釋；Analytics Engine 負責計算、驗證與提供證據」 | P3 p.6 |
| Level | Level 1 LLM + Data「是基礎完成線」；Level 2 Knowledge Agent（RAG、文件檢索、Web Search、API、多步推理）；Level 3 IoT Autonomous Agent（IoT Sensor、MQTT、即時資料流、進階分析、主動警示）；不要求一開始就做 Level 3 | P3 p.7 |
| 架構圖內容 | 十區資訊圖：① 使用者與應用情境；② 問題輸入與互動介面（Chat、Voice、Mobile、Web App、AR/VR）；③ Domain Data Agent 六階段；④ 六大能力；⑤ 資料來源與工具層（5-1 IoT、5-2 內部、5-3 外部、5-4 知識庫、5-5 分析工具）；⑥ 分析引擎；⑦ 輸出（Chat UI、Dashboard、Charts、Map/GIS、Report、Design/3D、Alert）；⑧ 領域範例；⑨ 三個 Level（圖上標為基礎應用／進階應用／完整應用）；⑩ 成果與評量六項勾選 | 圖；P3 p.2 |
| Deep Research | 每組須回答 Q1 五個核心思維模式、Q2 三個專業爭論、Q3 十個深度理解問題 | R L87–108；L41 p.1 |
| 寫作方法 | A–Z SOP：Abstract A–F、Introduction G–L、Related Work M–O、Proposed Scheme PA–PM、Simulation Q–V（指標、baseline、設定、參數、結果含 Ablation、RQ→證據→結論）、Conclusion W–Z | L41 p.2、p.5–17 |

### B2. 交付物與格式

| 階段 | 交付物與最低要求 | 來源 |
| --- | --- | --- |
| Proposal | ① Proposal Document（Abstract、Introduction、Related Work、Deep Research、Proposed Scheme、References）；② Proposal PPT；③ GitHub Repository（正式專題 repo）；④ DESIGN.md（從 Proposal 階段建立並持續維護） | R L165–171 |
| Final：GitHub | 完整 Source Code、資料／資料來源、執行與測試方式 | R L177 |
| Final：README.md | 專題介紹、Installation、How to Run、Demo | R L178 |
| Final：DESIGN.md | Architecture、Components、Data Flow、AI Model、Domain Knowledge、Algorithm、Implementation Mapping、Results、Limitations | R L179、L184–186 |
| Final：PPT／Video | Final PPT 超過 20 頁；Final Video 為 YouTube 專題簡報與 Demo，超過 10 分鐘 | R L180–181 |
| Final：Experiments／Conclusion | Dataset、Evaluation Metrics、Results、Comparison；Contributions、Limitations、Future Work | R L182–183 |
| Handover 標準 | 不只是「程式可以跑」；原開發者不在時，下一位開發者能靠 GitHub + README.md + DESIGN.md 理解、執行、驗證並繼續開發 | R L188–190 |

### B3. 評分

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| Proposal 占比 | 成績比重 10%；評分方式「直接打分數」 | R L13–16、L29–30 |
| Proposal 評分表 | Introduction 20%；Related Work 20%；Deep Research 20%；Proposed AI Agent + System Architecture 20%；Flowchart + Pseudocode + Technical Feasibility 15%；GitHub + DESIGN.md + 完整度 5% | R L192–200 |
| 期末評分權重 | 未載明。僅有方向性敘述：六大能力「非常適合直接成為未來的專題評分指標」；成功作品六項：解決真實問題、資料來源多元、分析有深度、能引用專業知識、介面有創意、對使用者有價值 | P3 p.4、p.7 |
| 口頭提問 | 教師可針對 Architecture、DESIGN.md、論文、資料、程式碼與實驗結果口頭提問；學生須能解釋 AI 做了什麼、為何這樣設計、如何驗證 | R L160–162 |

### B4. 一致性、範圍變更、個人或分組

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| 分組 | 類型為分組作業（原文簡體「分组作业」）；Deep Research 寫「每組必須」。個人單獨完成的規定：未載明 | R L1–4、L88 |
| Proposal 與期末的一致性 | 沒有明文條款。相關敘述：DESIGN.md 自 Proposal 階段持續維護；DESIGN.md 需含 Implementation Mapping；完整專題故事為 Proposed AI Agent → Architecture / Flowchart / Pseudocode → Implementation → Experiments → Final Handover | R L171、L179、L207 |
| 範圍變更 | 未載明 | — |
| 結果真實性 | Proposal 未完成實驗者寫 Expected Findings，「不得虛構實驗結果」 | R L51 |
| AI 使用 | 允許並鼓勵；須能解釋與驗證 | R L152–160 |

### B5. 日期

| 項目 | 內容 | 來源 |
| --- | --- | --- |
| Proposal 開放繳交 | 2026-10-05 00:00 | R L5–6 |
| Proposal 繳交期限 | 2026-11-11；允許遲交：是 | R L7–12 |
| 期末發表／最終繳交日 | 未載明 | — |

---

## 來源中沒有載明的事項

- Proposal：組員姓名與分工；FR／NFR 編號清單；RQ／H 正式編號；時程、里程碑與任何日期；期末交付清單；E1–E4 的數值成功門檻；E3 的封路紀錄來源與筆數；MAX_ATTEMPTS、安全餘裕 m、候選出發時間範圍的實際數值；LLM 供應商與模型；知識庫內容與規模；回應時間、成本等非功能指標；279 趟的期間、里程、路線分布。
- 課程：期末專題的評分權重與評分表；期末發表與最終繳交日期；Final PPT、影片以外的格式細節（檔名、上傳位置）；Proposal 與期末成果不一致時的處理或範圍變更程序；是否允許一人一組；Level 與成績的對應關係；IoT 感測器或實體裝置是否為必備（來源只寫資料來源「可以包含」IoT Sensor，Level 1 為「基礎完成線」）。
- 無法查閱的課程附件：L4-1 p.1、p.3 列出的範例檔、影片與其他講義。
