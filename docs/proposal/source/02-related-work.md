# 2. Related Work 相關研究

> 草稿，2026-10-31。本節依老師要求約一半 AI 技術、一半領域知識；先依分類（taxonomy）整理技術演進與方法比較，再列 Article Summary Table，最後歸納 Existing Research → Limitations → Research Gap → Our Project。

## 查證紀錄

每一筆文獻都開過下列頁面；表中「partial」表示只讀到摘要或書目，沒有讀到全文，因此文中只引用摘要層級的內容。

| Ref | URL opened | verified | note |
| --- | --- | --- | --- |
| [1] | https://mlanthology.org/aaai/2018/wang2018aaai-you/ ；https://github.com/Dawn90/DeepTTE | partial | AAAI 原頁 ojs.aaai.org 被擋（bot 防護），改由 ML Anthology 書目頁與作者程式庫查證；摘要只寫「兩個大規模資料集」，程式庫範例資料為成都，另一個資料集名稱未查證；摘要沒有具體數字 |
| [2] | https://arxiv.org/abs/2108.11482 ；https://ar5iv.labs.arxiv.org/html/2108.11482 | yes | CIKM 2021 Applied Research Track；讀到 supersegment 定義、輸入特徵、限制與離線實驗城市 |
| [3] | https://arxiv.org/abs/2407.05895 ；https://arxiv.org/html/2407.05895v2 | yes | arXiv 頁的 journal reference 為 IEEE T-ITS（2025）；資料集、指標、限制取自 HTML 全文 |
| [4] | https://arxiv.org/abs/2402.01622 ；https://arxiv.org/html/2402.01622 | yes | ICML 2024 Spotlight；GPT-4-Turbo 在兩階段（自己用工具蒐集資料再規劃）設定下 final pass rate 0.6% |
| [5] | https://arxiv.org/abs/2404.11891v3 ；https://aclanthology.org/2025.naacl-long.176（經搜尋結果確認書目） | yes | arXiv 頁未列 venue，NAACL 2025 書目（pp. 3434–3483）由 ACL Anthology 條目確認 |
| [6] | https://arxiv.org/abs/2501.00316 | partial | 只讀摘要頁；ICML 2025 Spotlight 取自 arXiv comments |
| [7] | https://wseas.com/journals/articles.php?id=165 | partial | 提供的 ir.lib.uth.gr 連結 SSL 錯誤打不開，改由期刊官方頁查證；摘要沒有模型係數與結果數字 |
| [8] | https://rosap.ntl.bts.gov/view/dot/36257 | partial | 年份為 2017（不是候選清單寫的 2018）；頁面未說明使用的是 SHRP 2 NDS 或其他子資料集，也未提到機車 |
| [9] | https://www.cutr.usf.edu/2019/02/development-of-crash-modification-factors-of-horizontal-curve-design-features-for-single-motorcycle-crashes-on-rural-two-lane-highways-a-matched-case-control-study/ | partial | 由作者單位（USF CUTR）頁面查證書目與摘要；CMF 數值未列出 |
| [10] | https://arxiv.org/abs/2303.16065 ；https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0295848 | yes | 正式發表於 PLOS ONE（2023-12-18）；比較對象為 Naismith、Tobler、Campbell et al. |
| [11] | https://ckanprod.data-commons.k8s.ucar.edu/dataset/warm-season-afternoon-thunderstorm-characteristics-under-weak-synoptic-scale-forcing-over-taiwa ；https://scholars.lib.ntu.edu.tw/handle/123456789/463591 | yes | 找到期刊本文：Weather and Forecasting 26(1):44–60。UCAR 資料頁另列 Rita Roberts 為 creator，NTU 書目只有 4 位作者，本文採期刊書目 |
| [12] | https://ir.lib.ncu.edu.tw/ir/handle/987654321/103259 | partial | ASCE 原頁 403，改由中央大學機構典藏書目頁查證；摘要沒有效能數字 |
| [13] | https://arxiv.org/abs/2405.20625 | partial | 只讀摘要頁；摘要自稱 workshop paper，但頁面未寫是哪個 workshop |
| [14] | https://aclanthology.org/2025.emnlp-main.626 | yes | EMNLP 2025 main，pp. 12392–12418 |
| [15] | https://calimoto.com/en | yes | 產品官網 |
| [16] | https://kurviger.com/en | yes | 產品官網 |
| [17] | https://www.rever.co/ | yes | 產品官網 |
| [18] | https://taiwan.googleblog.com/2018/07/google.html | yes | Google 官方公告：2018-07-18 機車模式在台上線（原引用的數位時代報導談的是腳踏車模式，2026-10-31 依文獻審查改引官方公告） |
| [19] | https://apps.apple.com/app/id1250173746 | yes | App Store 產品頁 |
| [20] | https://aclanthology.org/2025.emnlp-main.752/ | yes | EMNLP 2025；摘要：最強既有模型 1.0%、TGMA 2.72%；2026-11-11 查證 |
| [21] | https://arxiv.org/abs/2505.10922 | partial | arXiv 摘要：完整系統 8.5、無策略 7.2、無外部 API 6.8；評分方式未讀全文 |
| [22] | https://arxiv.org/abs/2611.09407 | partial | arXiv v1（2026-11-06）摘要：時空檢索注入天氣、道路距離、營業時間；ReAct 式重新規劃針對使用者修改 |

---

## 2.1 分類架構

本專題同時涉及「預測一段路要騎多久」與「讓 LLM 排出可行的行程」兩件事，再加上重機騎乘與台灣山區環境的領域知識。相關研究依下列分類整理：

| 類別 | 子題 | 文獻 |
| --- | --- | --- |
| A. AI 技術 | A1 旅行時間預估（Travel Time Estimation, TTE） | [1] [2] [3] |
| | A2 LLM Agent 行程規劃與驗證 | [4] [5] [6] [13] [14] |
| B. 領域知識 | B1 機車在彎道的速度行為 | [7] [8] |
| | B2 以地形預測移動速度（個人配速的類比） | [10] |
| | B3 騎乘風險：彎道、天氣、封路 | [9] [11] [12] |
| C. 既有產品 | 重機導航與路線規劃 App | [15]–[19] |

## 2.2 AI 技術

### A1 旅行時間預估：由加總路段到端對端，再到機率分布

**加總路段時間。** 最直觀的做法是把路徑切成路段，分別估時間後相加；本專題的平均速度與速限換算 baseline 屬於這一類。DeepTTE [1] 指出這種做法忽略路口與號誌，局部誤差會累積。

**端對端深度學習（2018）。** DeepTTE [1] 直接預測整條路徑的時間：以 geo-convolution 把地理資訊放進卷積，疊上 recurrent 單元捕捉時間相依，並以 multi-task learning 同時預測整段與各局部子路徑的時間。作者在兩個大規模軌跡資料集上報告優於當時方法；作者程式庫附的範例資料來自成都，並註明要接近論文結果需要五百萬條以上軌跡。

**圖神經網路與產品部署（2021）。** Google Maps 的 GNN ETA [2] 把常見路線上相連的路段組成 supersegment（路段平均約 50–100 m，一個 supersegment 約 20 段），輸入即時速度、過去 17 週的歷史速度、路段長度與道路等級，已在 Google Maps 上線，摘要報告在 Sydney 等城市把負面 ETA 結果降低 40% 以上。論文也承認只涵蓋約一百萬個預先定義的 supersegment，較冷門的地面道路改用較簡單的逐段模型。

**機率式預估（2024–2025）。** ProbETA [3] 認為天氣與駕駛行為會讓不同行程的時間彼此相關，因此以 low-rank 多變量高斯分布同時建模行程之間與行程內部的相關，在成都與哈爾濱兩個網約車資料集上 MAPE 比既有方法降低 12.60% 以上，並以 CRPS 評估分布品質。它的限制是假設旅行時間服從高斯分布，且訓練資料只有各 6 天。

**這一條演進線的共同點：** 資料都是城市汽車或計程車軌跡、目標是群體平均，模型需要大量軌跡；三篇在我們讀到的範圍內都沒有處理機車、山區彎道或單一使用者的個人化。

### A2 LLM Agent 行程規劃：由「直接生成」到「外部驗證」

**LLM 直接規劃的能力不足（2024–2025）。** TravelPlanner [4] 提供 1,225 個旅遊需求、六種搜尋工具與近四百萬筆資料，要求 Agent 同時滿足常識限制與使用者的硬限制（預算、房型等）。GPT-4-Turbo 以 ReAct 自己用工具蒐集資料再規劃時，final pass rate 只有 0.6%；直接提供資料、只做規劃時也只有 4.4%。主要失敗原因包括工具參數錯誤、重複無效動作、幻覺，以及無法同時追蹤多個全域限制。MapEval [6] 以 180 個城市、54 個國家的 700 題地理問題測試 30 個 foundation model，沒有一個超過 67%，且都落後人類 20% 以上；摘要指出模型在距離、方向、路線規劃上特別弱。

**加入外部批評器（2024）。** LLM-Modulo [13] 讓 LLM 負責產生與改寫計畫，再由一組 critic 檢查並回饋。在 TravelPlanner 上，GPT-3.5-Turbo 由 0% 提升到 5%，GPT-4-Turbo 約為原本的 4.6 倍。

**交給形式化求解器（2025）。** Hao 等人 [5] 把多限制規劃問題轉成 constraint satisfiability 問題，交給 SMT 類求解器求解，在 TravelPlanner 上成功率 93.9%（摘要提到 o1-preview 在資訊齊全時約 10%）。無解時，系統取出 unsatisfiable core 說明失敗原因並建議修改。

**檢索增強與時空約束（2025）。** TP-RAG [14] 建立 2,348 個真實旅遊需求、85,575 個標註 POI 與 18,784 條參考行程的 benchmark，發現加入參考行程能改善路線效率，但參考資料互相衝突或有雜訊時會降低穩健性；作者提出的 EvoRAG 結合檢索行程與 LLM 推理，減少常識違規。

**多 Agent 與即時環境（2025–2026）。** RETAIL [20] 把旅遊規劃推向真實情境，最強的既有模型通過率只有 1.0%，作者以主題導向的多 Agent 框架 TGMA 提升到 2.72%，並加入環境感知以確保計畫可行。Vaiage [21] 以多個 Agent 搭配外部 API 與地圖回饋做個人化行程，完整系統平均 8.5 分（滿分 10），拿掉策略或外部 API 分別降到 7.2 與 6.8 分（作者自評，僅讀到摘要）。ROAM [22] 以時空檢索層把天氣預報、實際道路距離與 POI 營業時間放進提示，再以 ReAct 式 Agent 處理使用者的修改要求並重新檢查可行性；它的重新規劃針對使用者編輯，沒有處理封路。三者都把外部環境帶進規劃，但都以城市景點行程為對象，也都沒有依個人速度推算各點的抵達時間。

**這一條演進線的共同點：** 結論一致指向「LLM 負責理解與組織，數字與限制交給外部工具計算和驗證」。但這些 benchmark 的限制多是預算、POI、交通班次與城市間移動，都沒有「每段路要騎多久」「天黑前回得來嗎」「油夠不夠到下一個加油站」這類依賴個人配速與即時環境的限制。

## 2.3 領域知識

### B1 機車在彎道的速度行為

道路設計領域長期用 operating speed model（以道路幾何預測自由車流第 85 百分位速度）描述彎道車速。Lemonakis 等人 [7] 指出既有模型多以小客車、貨車為對象，很少考慮機車，但機車騎士在事故中比例偏高，尤其是平曲線；他們以裝有儀器的機車，由有經驗的騎士在自然騎乘條件與不同照明下，於希臘雙車道鄉道量測，篩選影響運行速度的幾何參數，建立簡化的機車速度模型。

Geedipally 等人 [8] 用 SHRP 2 車速資料檢驗彎道速度模型能否跨州移轉：Texas 的速度差模型乘上一個調整係數後可以用在 Indiana；熟悉路線的駕駛在彎道中點的第 85 百分位速度高於不熟悉的駕駛，而模型對不熟悉路線者的預測較準。這說明「同一條彎道，不同人、不同熟悉度會騎出不同速度」，群體模型對個人會有系統性偏差，是本專題改用騎士自己 GPX 的直接依據。

### B2 以地形預測移動速度：個人配速模型的類比

登山健行領域有和本專題結構最接近的研究。Wood 等人 [10] 從約兩萬條公開 GPS 軌跡篩出英格蘭與威爾斯 7,636 條（約 88,000 km），以 GLM 用坡度、地表類型與障礙程度預測步行速度，並與 Naismith rule、Tobler hiking function、Campbell et al. 比較。以 50 m 為單位時 GLM 的 RMSE 較低；但換成整條路線時，各模型的平均百分比誤差都在 13.5%–15.5%，沒有一個明顯較好。作者也說明模型只代表平均條件下的平均個人，沒有納入體能、年齡、天氣等個人因素。這兩點都對應本專題：以地形特徵逐段預測可行，但要做整趟預測，還需要個人化資料與區間估計。

### B3 騎乘風險：彎道、午後雷雨與預警性封路

**彎道與事故風險。** Xin 等人 [9] 以 Florida 2005–2015 年鄉間雙車道公路的 1,601 個事故路段與 16,010 個對照路段做 matched case-control 分析，發現半徑 1,500 ft 以下的非反向急彎對單一機車事故風險最高，其次為急反向彎與中等反向彎；作者也指出騎士在急彎、窄路肩與鋪面不佳處可能有風險補償行為。

**台灣午後雷雨。** Lin 等人 [11] 分析 2005–2008 年暖季（5–10 月）綜觀尺度弱時的台灣午後雷雨，結合雷達、閃電、探空與地面觀測，發現平均逐時雨量在當地時間 15–16 時達到高峰，降雨最常出現在山脈較低坡面上一條與山脈平行的狹長帶。也就是說，同一條山路的降雨風險會隨抵達時段與所在高度改變，這是天氣 Agent 需要依「預計抵達各段的時間」查預報，而不是只查出發地天氣的原因。

**山區道路預警性封閉。** Yang 等人 [12] 以 2004 年敏督利颱風引發的崩塌訓練 logistic regression，在南投國姓鄉繪製崩塌機率圖，標出颱風期間建議封閉的高風險路段，並以之後颱風造成的實際封路驗證。這類研究提供「降雨與封路有關」的依據，但結果是特定地區的崩塌潛勢，不是全台可即時查詢的封路資料。

## 2.4 方法比較

| Method | Core Idea | Strength | Weakness | Application | Limitation |
| --- | --- | --- | --- | --- | --- |
| 平均速度／速限換算 | 路段距離除以平均速度或速限，再加總 | 簡單、不需訓練資料 | 忽略彎道、坡度、路口；誤差會累積 [1] | 本專題 baseline | 無法反映個人與地形差異 |
| 運行速度迴歸 [7][8] | 以道路幾何預測第 85 百分位速度 | 可解釋，與道路設計規範接軌 | 只描述群體，對熟悉路線者偏差較大 [8] | 彎道設計、速度管理 | 單點速度，不是整趟時間；機車樣本少 |
| 地形 GLM [10] | 以坡度與地表類型逐段預測速度 | 特徵少、可解釋，逐段誤差低於經驗公式 | 整趟誤差 13.5%–15.5%，未納入個人因素 | 健行時間估算 | 平均個人、平均條件 |
| 端對端深度 TTE [1] | 整條路徑直接預測，multi-task 同時學子路徑 | 減少加總誤差 | 需要大量軌跡（數百萬條） | 城市計程車 ETA | 城市汽車資料，不提供區間 |
| GNN ETA [2] | supersegment 圖結構加即時與歷史速度 | 已大規模部署，降低負面 ETA | 依賴大量即時車流；冷門道路改用簡單模型 | Google Maps | 群體平均，未提到個人化與機車 |
| 機率式 TTE [3] | 低秩多變量高斯，建模行程間相關 | 輸出分布，可評估不確定性 | 假設高斯分布 | 網約車 ETA | 城市資料、各 6 天 |
| LLM Agent（ReAct 等）[4] | LLM 自己選工具、蒐集資料、產生計畫 | 彈性高，能處理自然語言需求 | 工具誤用、幻覺、無法追蹤多個限制 | 旅遊規劃 benchmark | GPT-4-Turbo pass rate 0.6% |
| LLM + critics [13] | LLM 產生，外部 critic 檢查並回饋 | 不需完整形式化，可逐步修正 | 提升幅度有限（GPT-3.5 由 0% 到 5%） | 旅遊規劃 | critic 的涵蓋範圍決定上限 |
| LLM + 形式化求解器 [5] | 轉成 SMT 問題交給求解器 | 成功率 93.9%，能說明無解原因 | 需要能形式化的限制 | 多限制規劃 | 限制以預算、班次為主，沒有時間預測不確定性 |
| 檢索增強規劃 [14] | 檢索參考行程再由 LLM 調整 | 改善路線效率與 POI 合理性 | 參考資料衝突或有雜訊時不穩 | 城市旅遊行程 | 以 POI 為中心，不含騎乘時間與天候 |
| **本專題** | 個人 GPX 配速模型（MLR → LightGBM 分位數）+ 多 Agent + 驗證 Agent 重新規劃 | 預測對個人化、有 P50／P90 區間；數字由工具產生並驗證 | 只有一位騎士、279 趟資料；風險規則沒有正確答案可驗證 | 台灣重機旅遊 | 不宣稱預測事故；封路資料覆蓋有限 |

技術演進可以歸納為兩條線：時間預估由「加總平均」走向「端對端」、「圖結構」再到「機率分布」，但始終以城市汽車與群體平均為對象；LLM 規劃由「直接生成」走向「外部 critic」、「形式化求解器」與「檢索增強」，但限制條件始終沒有涵蓋依賴個人速度與即時環境的時間可行性。

## 2.5 Article Summary Table

| Ref | Year | Problem | AI Method | Domain Knowledge | Dataset | Findings | Limitation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [1] | 2018 | 城市中任意路徑的旅行時間 | DeepTTE：geo-convolution + recurrent + multi-task | 路口、號誌使路段時間無法直接相加 | 兩個城市的大規模計程車軌跡資料集（公開範例資料為成都） | 優於當時方法（摘要無具體數字） | 需要大量軌跡；城市汽車；無區間 |
| [2] | 2021 | Google Maps 的 ETA 預測 | GNN on supersegments，MetaGradients 訓練 | 道路等級、歷史與即時車速 | Google Maps 生產資料；離線實驗 NYC、LAX、TYO、SGP | Sydney 等城市負面 ETA 降低 40% 以上 | 只涵蓋約一百萬個 supersegment；未提到個人化、機車、天氣 |
| [3] | 2025（arXiv 2024） | 機率式旅行時間，考慮行程間相關 | ProbETA：低秩多變量高斯 + link representation（empirical Bayes） | 天氣與駕駛行為造成行程間相關 | 成都、哈爾濱網約車 GPS（各 6 天） | MAPE 降低 12.60% 以上，以 CRPS 評估分布 | 高斯假設；城市資料；無個人化 |
| [4] | 2024 | LLM Agent 能否完成真實旅遊規劃 | ReAct 等 Agent 框架 + 工具 | 旅遊常識限制與使用者硬限制 | 1,225 個需求、約四百萬筆沙盒資料 | GPT-4-Turbo 兩階段 final pass rate 0.6% | 限制以預算、班次、住宿為主；美國國內旅遊 |
| [5] | 2025 | 讓 LLM 嚴謹地解多限制規劃 | LLM 轉譯 + SMT／satisfiability 求解器 | 旅遊限制的形式化 | TravelPlanner、國際旅遊與無解問題資料集 | TravelPlanner 成功率 93.9%；無解問題修改後可解 81.6%／91.7% | 需要限制可形式化；不處理預測的不確定性 |
| [6] | 2025 | foundation model 的地圖空間推理 | 30 個 foundation model 評測（文字、API、視覺） | 距離、方向、路線、地點知識 | 700 題，180 個城市、54 國 | 最佳不超過 67%，落後人類 20% 以上 | 選擇題形式；只評測不提出改善方法 |
| [7] | 2021 | 機車騎士在雙車道鄉道的運行速度 | 迴歸型運行速度模型（統計，非 ML） | 平曲線幾何、照明條件、機車事故比例高 | 儀器化機車，有經驗騎士自然騎乘（希臘） | 以少數幾何參數建立實用的機車速度模型 | 摘要未列騎士人數與誤差；群體模型 |
| [8] | 2017 | 彎道速度模型能否跨州移轉 | 速度預測與速度差模型（統計） | 曲線嚴重度、側向摩擦差、路線熟悉度 | SHRP 2 車速資料（Texas → Indiana） | 加調整係數可移轉；熟悉者彎道速度較高，模型對其較不準 | 摘要未提機車；單點速度 |
| [9] | 2019 | 平曲線設計對單一機車事故風險的影響 | matched case-control + conditional logistic | 曲線半徑、反向曲線、路肩、鋪面 | Florida 鄉間雙車道 2005–2015：1,601 案例、16,010 對照 | 半徑 ≤ 1,500 ft 非反向急彎風險最高 | 美國資料；CMF 不能直接換算成個人行程風險 |
| [10] | 2023 | 以 GPS 軌跡改善健行速度預測 | GLM（坡度、地表、障礙） | Naismith、Tobler、Campbell 等經驗公式 | 英格蘭與威爾斯 7,636 條軌跡、約 88,000 km | 50 m 路段 RMSE 低於經驗公式；整趟各模型誤差 13.5%–15.5% | 代表平均個人；未納入體能、天氣 |
| [11] | 2011 | 台灣暖季午後雷雨的時空特性 | 觀測資料統計分析（非 ML） | 海風、山區地形、綜觀尺度弱 | 2005–2008 暖季雷達、閃電、探空、地面觀測 | 雨量高峰在 15–16 時，集中在山脈較低坡面 | 只描述氣候特性，不是逐日預報 |
| [12] | 2012 | 預測颱風崩塌造成的山區道路封閉 | logistic regression 崩塌機率模型 | 崩塌致因與觸發因子 | 南投國姓鄉，敏督利颱風（2004）崩塌 | 標出建議封閉路段，與之後颱風的封路相符 | 單一地區；摘要未報告效能數字；非即時資料 |

AI 技術 6 篇（[1]–[6]），領域知識 6 篇（[7]–[12]）；[13]、[14] 在 2.2 與 2.4 補充演進脈絡。

## 2.6 既有產品

重機導航 App 已經處理了「找好騎的路」：calimoto 有四種路線設定（含 Winding、Twisty）與衡量彎道程度的 Calimeter，Premium 版提供 TomTom 即時封路資料 [15]；Kurviger 可調整路線彎曲程度、避開目前的封路與未鋪面道路、產生最長 600 km 的環線並匯入 GPX [16]；REVER 提供路線規劃與離線騎乘紀錄 [17]；Google Maps 2018 年 7 月在台灣推出機車導航 [18]；BMW Motorrad Connected 有彎道路線選項、騎乘紀錄（含傾角）、GPX 匯出、剩餘續航與目前位置天氣 [19]。我們開啟的產品頁面都沒有提到以騎士自己的歷史紀錄預測每段騎乘時間、依各段抵達時間檢查沿途天氣與日落，或在出發前驗證整份計畫是否可行。

## 2.7 Existing Research → Limitations → Research Gap → Our Project

| 階段 | 內容 |
| --- | --- |
| **Existing Research** | 旅行時間預估已由加總平均發展到端對端、圖神經網路與機率分布 [1][2][3]；LLM 規劃研究證實 LLM 單獨規劃失敗率高，需要外部 critic、求解器或檢索 [4][5][6][13][14]，近期多 Agent 系統開始把天氣、道路距離與營業時間帶進規劃 [20][21][22]；道路與安全研究建立了機車彎道速度、彎道事故風險、台灣午後雷雨與颱風封路的知識 [7][8][9][11][12]；健行研究顯示以地形逐段預測速度可行 [10]。 |
| **Limitations** | (1) TTE 模型以城市汽車、群體平均為主，需要大量軌跡，沒有處理機車與山區彎道，也沒有個人化 [1][2][3]。(2) 機車速度研究預測的是群體第 85 百分位的單點速度，且對熟悉路線者偏差較大 [7][8]；地形模型在整趟層級仍有 13.5%–15.5% 誤差 [10]。(3) LLM 規劃 benchmark 的限制是預算、班次與 POI，不含依賴個人速度與即時天候的時間可行性 [4][5][14]；多 Agent 系統雖加入環境資料，但對象是城市景點行程，沒有依個人速度推算各點抵達時間 [20][21][22]，而 LLM 本身在距離與路線推理上弱 [6]。(4) 天氣與封路研究是各自獨立的區域分析，沒有接到行程規劃 [11][12]。(5) 既有 App 能找彎路與封路，但頁面上沒有個人化騎乘時間與行前可行性驗證 [15]–[19]。 |
| **Research Gap** | 目前沒有看到一個系統同時做到：以單一騎士的歷史軌跡學出含地形與時段特徵的個人配速並給出區間；把配速區間和沿途天氣、日落、封路、加油距離放在同一份計畫裡；再由驗證者檢查計畫中的時間與距離是否一致可行，不行就重新規劃。 |
| **Our Project** | 本專題以騎士自己的 279 趟 GPX 建立路段騎乘時間模型（特徵：彎曲度、坡度、道路等級、時段、天氣），以多元迴歸為 baseline、LightGBM 分位數損失輸出 P50／P90，並和平均速度、Google Maps 預估時間比較，用 MAE、MAPE 與區間覆蓋率評估。Agent 端採多 Agent 分工：規劃、配速、天氣（氣象署預報，依各段抵達時間查詢）、路況與補給（TDX 路況、中油與台糖加油站、車輛續航）、驗證；驗證 Agent 檢查日落前回程、時間加總、續航距離與數字出處，不通過就退回重新規劃，對應 [4][5][13] 的「外部驗證」結論。風險部分採氣象署警特報門檻的透明規則，不宣稱預測事故。 |

## References

[1] D. Wang, J. Zhang, W. Cao, J. Li, Y. Zheng, "When Will You Arrive? Estimating Travel Time Based on Deep Neural Networks," *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-18)*, vol. 32, no. 1, pp. 2500–2507, 2018. https://ojs.aaai.org/index.php/AAAI/article/view/11877

[2] A. Derrow-Pinion, J. She, D. Wong, O. Lange, T. Hester, L. Perez, M. Nunkesser, S. Lee, X. Guo, B. Wiltshire, P. W. Battaglia, V. Gupta, A. Li, Z. Xu, A. Sanchez-Gonzalez, Y. Li, P. Veličković, "ETA Prediction with Graph Neural Networks in Google Maps," *Proceedings of the 30th ACM International Conference on Information and Knowledge Management (CIKM 2021), Applied Research Track*, 2021. https://arxiv.org/abs/2108.11482

[3] C. Xu, Q. Wang, L. Sun, "Link Representation Learning for Probabilistic Travel Time Estimation," *IEEE Transactions on Intelligent Transportation Systems*, 2025 (arXiv:2407.05895, 2024). https://arxiv.org/abs/2407.05895

[4] J. Xie, K. Zhang, J. Chen, T. Zhu, R. Lou, Y. Tian, Y. Xiao, Y. Su, "TravelPlanner: A Benchmark for Real-World Planning with Language Agents," *Proceedings of the 41st International Conference on Machine Learning (ICML 2024)*, 2024. https://arxiv.org/abs/2402.01622

[5] Y. Hao, Y. Chen, Y. Zhang, C. Fan, "Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools," *Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the ACL (NAACL 2025), Volume 1: Long Papers*, pp. 3434–3483, 2025. https://aclanthology.org/2025.naacl-long.176

[6] M. L. Dihan, M. T. Hassan, M. T. Parvez, M. H. Hasan, M. A. Alam, M. A. Cheema, M. E. Ali, M. R. Parvez, "MapEval: A Map-Based Evaluation of Geo-Spatial Reasoning in Foundation Models," *Proceedings of the 42nd International Conference on Machine Learning (ICML 2025)*, 2025. https://arxiv.org/abs/2501.00316

[7] P. Lemonakis, G. Botzoris, A. Galanis, N. Eliou, "Speed Models for Motorcycle Riders for Two-lane Rural Roads," *WSEAS Transactions on Environment and Development*, vol. 17, pp. 595–603, 2021. doi:10.37394/232015.2021.17.57. https://wseas.com/journals/articles.php?id=165

[8] S. R. Geedipally, M. P. Pratt, B. Dadashova, L. Wu, M. Shirazi, "Evaluating Curve Speed Behavior Using SHRP 2 Data," Texas A&M Transportation Institute / ATLAS Center, Report ATLAS-2017-21, 2017. https://rosap.ntl.bts.gov/view/dot/36257

[9] C. Xin, Z. Wang, C. Lee, P.-S. Lin, T. Chen, R. Guo, Q. Lu, "Development of crash modification factors of horizontal curve design features for single-motorcycle crashes on rural two-lane highways: A matched case-control study," *Accident Analysis & Prevention*, vol. 123, pp. 51–59, 2019. https://www.cutr.usf.edu/2019/02/development-of-crash-modification-factors-of-horizontal-curve-design-features-for-single-motorcycle-crashes-on-rural-two-lane-highways-a-matched-case-control-study/

[10] A. Wood, W. Mackaness, T. I. Simpson, J. D. Armstrong, "Improved prediction of hiking speeds using a data driven approach," *PLOS ONE*, 2023. doi:10.1371/journal.pone.0295848. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0295848

[11] P.-F. Lin, P.-L. Chang, B. J.-D. Jou, J. W. Wilson, and R. D. Roberts, "Warm Season Afternoon Thunderstorm Characteristics under Weak Synoptic-Scale Forcing over Taiwan Island," *Weather and Forecasting*, vol. 26, no. 1, pp. 44–60, 2011. doi:10.1175/2010WAF2222386.1. https://scholars.lib.ntu.edu.tw/handle/123456789/463591

[12] S.-R. Yang, C.-W. Shen, C.-M. Huang, C.-T. Lee, C.-T. Cheng, C.-Y. Chen, "Prediction of Mountain Road Closure Due to Rainfall-Induced Landslides," *Journal of Performance of Constructed Facilities*, vol. 26, no. 2, pp. 197–202, 2012. doi:10.1061/(ASCE)CF.1943-5509.0000242. https://ir.lib.ncu.edu.tw/ir/handle/987654321/103259

[13] A. Gundawar, M. Verma, L. Guan, K. Valmeekam, S. Bhambri, S. Kambhampati, "Robust Planning with LLM-Modulo Framework: Case Study in Travel Planning," arXiv:2405.20625 (workshop paper), 2024. https://arxiv.org/abs/2405.20625

[14] H. Ni, F. Liu, X. Ma, L. Su, S. Wang, D. Yin, H. Xiong, H. Liu, "TP-RAG: Benchmarking Retrieval-Augmented Large Language Model Agents for Spatiotemporal-Aware Travel Planning," *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing (EMNLP 2025)*, pp. 12392–12418, 2025. https://aclanthology.org/2025.emnlp-main.626

[15] calimoto, product website. https://calimoto.com/en （2026-10-31 查閱）

[16] Kurviger, product website. https://kurviger.com/en （2026-10-31 查閱）

[17] REVER, product website. https://www.rever.co/ （2026-10-31 查閱）

[18] Google 台灣官方部落格，〈Google 地圖機車模式正式在台上線〉，2018-07-18。https://taiwan.googleblog.com/2018/07/google.html

[19] BMW Motorrad Connected, Apple App Store listing. https://apps.apple.com/app/id1250173746 （2026-10-31 查閱）

[20] B. Deng, Y. Feng, Z. Liu, Q. Wei, X. Zhu, S. Chen, Y. Guo, Y. Wang, "RETAIL: Towards Real-world Travel Planning for Large Language Models," *Proceedings of EMNLP 2025*, pp. 14870–14902, 2025. https://aclanthology.org/2025.emnlp-main.752/

[21] B. Liu, J. Ge, J. Wang, "Vaiage: A Multi-Agent Solution to Personalized Travel Planning," arXiv:2505.10922, 2025. https://arxiv.org/abs/2505.10922

[22] Z. Ye, X. Lin, "ROAM: Retrieval-Augmented Optimization for Feasible Multi-Day Itinerary Planning," arXiv:2611.09407, 2026. https://arxiv.org/abs/2611.09407
