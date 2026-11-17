# 1. Introduction 緒論

> 草稿，2026-10-31。本節回答「Why is this project worth doing?」，依老師要求分為 A Attention Getter、B Background、C Problem、D Existing Limitations、E Innovation、F Contributions。文中只引用下表狀態為「已查證」或「部分」的證據，以 [I1]、[I2]… 標示；Proposal 階段沒有實驗結果，F 段只寫預期成果。

## 證據查證表

查證日期：2026-10-31。每一筆都開過表中 URL；「部分」表示只讀到摘要、新聞轉述，或找不到官方原文。

| # | 主張 | 數字/內容 | 日期 | 來源類型 | URL | 狀態 |
| --- | --- | --- | --- | --- | --- | --- |
| I1 | 台灣 2025 年道路交通事故 30 日死亡人數 | 2025 年 2,858 人；2024 年 2,950 人；減少 92 人（−3.1%）；2023 年 3,023 人。站上註明 112–114 年為初估值 | 資料更新 2026-10-27（115/10/27） | 官方（交通部道安資訊查詢網 roadsafety.tw） | https://roadsafety.tw/AccOrder?Order=Ieok26&type=%E4%BA%8B%E6%95%85%E4%BD%8D%E7%BD%AE （查詢介面 `/api/AccOrderAjax/GetResult?Topic=事故位置&Cyear=114`） | 已查證 |
| I2 | 機車騎士占道路死亡的比例 | 2025 年機車騎士死亡 1,740 人，占 2,858 人的 60.9%；2024 年 1,857 / 2,950（62.9%）；2023 年 1,886 / 3,023（62.4%）。其中大型重型機車騎士死亡：2025 年 33 人、2024 年 57 人、2023 年 62 人（初估值） | 資料更新 2026-10-27 | 官方（roadsafety.tw） | https://roadsafety.tw/AccOrder?Order=Age&type=%E6%A9%9F%E8%BB%8A （查詢介面 `Topic=機車&MotorType=3`（全部）／`2`（大型重型）） | 已查證 |
| I3 | 交通部指機車與高齡者死亡偏多、自摔自撞事故比例較嚴重 | 交通部檢討 2025 年成果時的說法；沒有比例數字。另指無照駕駛情況惡化 | 2026-03-12（聯合報）；2026-04-14（TVBS） | 新聞 | https://udn.com/news/story/7266/9377125 ；https://cars.tvbs.com.tw/life/315916 | 部分（找不到交通部新聞稿原文；「自摔自撞惡化」在新聞中寫作「比例較為嚴重」，本文採後者） |
| I4 | 大型重型機車登記數與趨勢 | 2025 年底 279,703 輛，比 2024 年底（269,390 輛）增加 3.8%；2020 年底 178,832 輛（五年 +56.4%）；2015 年底 89,042 輛（十年約 3.1 倍）。數字為「550cc 以上」與「未滿 550cc」兩欄相加 | 2026（114 年統計年報） | 官方（交通部公路局統計年報，表 26） | https://ws.thb.gov.tw/001/Upload/436/relfile/13775/5693/fd88dd50-c215-4973-8db5-33f0c3e9510e.pdf | 已查證 |
| I5 | 大型重型機車新車領牌數 | 2023 年 27,200 輛 → 2024 年 19,925 輛 → 2025 年 15,506 輛（兩年 −43.0%）；2020–2023 年平均 25,817 輛。粉專「重車日誌－教士」稱 2026 年 1–7 月 7,456 輛，非官方 | 官方 2026；粉專轉述 2026-09-10 | 官方（公路局年報，表 27）；粉專經風傳媒轉述 | 官方同 I4；粉專：https://www.storm.mg/article/11163645 | 官方部分已查證；2026 年粉專數字未查證，不引用 |
| I6 | 南橫（台 20 線）2025-07 預防性封閉 | 2025-07-19 11 時起，台 20 線 0K–44K（梅山口至向陽）預警性封閉；原因是薇帕颱風帶來豪雨，坍方落石風險升高；公路局甲仙工務段 | 2025-07-19 | 新聞（中央社，引述公路局） | https://www.cna.com.tw/news/aloc/202507190089.aspx | 已查證（新聞層級） |
| I7 | 南橫（台 20 線）2025-09 預防性封閉 | 2025-09-22 晚間起，台 20 線 149K+110–199K（向陽至初來）預警性封閉；原因是樺加沙颱風外圍環流，台東山區豪雨特報；公路局關山工務段 | 2025-09-23 | 新聞（中央社，引述公路局） | https://www.cna.com.tw/news/ahel/202509230076.aspx | 已查證（新聞層級）。兩次原因都是颱風豪雨；原說法「地震和颱風」中的地震未查證，不引用 |
| I8 | 台灣暖季午後雷陣雨氣候特徵 | 2005–2008 年 5–10 月、綜觀天氣弱時：平均逐時雨量在 15–16 時（地方太陽時）最高；降雨頻率最高處是平行山脈走向、位於山坡下段的狹長帶 | 2011-02 | 論文（Weather and Forecasting 26(1):44–60, DOI 10.1175/2010WAF2222386.1） | https://ckanprod.data-commons.k8s.ucar.edu/dataset/warm-season-afternoon-thunderstorm-characteristics-under-weak-synoptic-scale-forcing-over-taiwa ；https://doi.org/10.1175/2010WAF2222386.1 | 已查證（摘要層級，經 Crossref 書目確認）；非 2025–2026 文獻 |
| I9 | TravelPlanner：LLM Agent 旅遊規劃能力 | 1,225 個規劃需求；兩階段模式（自己用工具蒐集資料再規劃）下 GPT-4-Turbo + ReAct 的 final pass rate 0.6%，其他模型為 0 | 2024（ICML 2024 Spotlight；arXiv v4 2024-10-23） | 論文 | https://arxiv.org/abs/2402.01622 | 已查證（全文） |
| I10 | LLM-Modulo：加上外部 critics 驗證 | TravelPlanner 驗證集 180 題、sole-planning 模式：GPT-4-Turbo final pass rate 由 4.4% 提升到 20.6%（4.6 倍）；GPT-3.5-Turbo 由 0% 到 5% | 2024-05-31 | 論文（arXiv，作者自稱 workshop paper） | https://arxiv.org/abs/2405.20625 | 已查證（全文） |
| I11 | LLM + SMT 求解器 | 把規劃問題轉成可滿足性問題交給求解器，TravelPlanner 成功率 93.9%；對照 o1-preview 約 10% | 2025-04（NAACL 2025；arXiv v3 2025-01-29） | 論文 | https://arxiv.org/abs/2404.11891v3 ；https://aclanthology.org/2025.naacl-long.176 | 已查證（摘要與書目） |
| I12 | MapEval：基礎模型的地圖與地理空間推理 | 700 題、180 個城市；30 個模型沒有一個超過 67% 正確率，都比人類低 20 個百分點以上；距離、方向、路線規劃是弱項 | 2025（ICML 2025 Spotlight；arXiv v2 2025-06-06） | 論文 | https://arxiv.org/abs/2501.00316 | 已查證（摘要）；新增證據 |
| I13 | Google 地圖機車模式在台灣上線 | 2018-07-18 上線；機車專屬捷徑、地標提示路線；以機器學習模型把機車行駛速度納入考量，提供預估行程時間。文中沒有提到依個別騎士紀錄調整，也沒有提供時間範圍 | 2018-07-18 | 官方（Google 台灣官方部落格） | https://taiwan.googleblog.com/2018/07/google.html | 已查證。原給的 ocacnews 連結打不開內容，改用官方部落格 |
| I14 | Google Routes API 二輪車路線支援台灣 | 「支援二輪車輛的國家和地區」清單列有台灣（TW） | 頁面更新 2026-10-30 | 官方（Google Maps Platform 文件） | https://developers.google.com/maps/documentation/routes/coverage-two-wheeled | 已查證；新增證據 |
| I15 | Google Maps 的 ETA 模型以整體車流訓練 | 以 GNN 預測 ETA 並已上線，部分城市（如雪梨）負面 ETA 結果減少 40% 以上 | 2021（CIKM 2021） | 論文 | https://arxiv.org/abs/2108.11482 | 已查證（摘要） |
| I16 | 既有重機 App 的功能 | Calimoto：彎道路線演算法、環線、傾角與爬升統計、行程日誌；Kurviger：網頁規劃路線傳到手機、離線地圖（付費方案）；REVER：路線紀錄、即時位置分享、天氣警示（PRO）。文中沒有提到個人化的抵達時間預測或封路風險 | 2025-01-13 | 新聞（SlashGear 評測） | https://www.slashgear.com/1755865/motorcycle-apps-find-routes-track-rides | 已查證（評測層級） |
| I17 | REVER PRO 官方功能清單 | 列有 Twisty Routing、ADV Planner、離線地圖、即時位置分享、Weather Alerts；沒有列出抵達時間預測或封路提示 | 2026-10-31 開啟 | 官方（產品頁） | https://www.rever.co/pro | 已查證 |
| I18 | 氣象署開放資料 API 可用的資料集 | F-D0047 鄉鎮天氣預報（未來 3 天逐 3 小時、1 週）、O-A0001-001 全測站逐時觀測、A-B0062-001 全臺逐日日出日沒時刻、W-C0033-001 縣市天氣警特報；需會員授權碼 | 2026-10-31 開啟 | 官方（中央氣象署 API 文件） | https://opendata.cwa.gov.tw/apidoc/v1 | 已查證 |
| I19 | TDX 省道即時路況 | 「省道發布路段即時路況資料」，每 1 分鐘更新，需在 TDX 註冊取得 API 金鑰，免費 | 2026-10-31 開啟 | 官方（政府資料開放平臺） | https://data.gov.tw/dataset/161171 | 已查證 |
| I20 | 2025 年死亡降幅未達每年 7% 目標 | 2,858 人、較 2024 年少 92 人、降幅 3.1%；2030 年減半需每年減 7%，2025 年只達約四成 | 2026-03-12 | 新聞（聯合報） | https://udn.com/news/story/7266/9375833 | 已查證（2026-11-11） |
| I21 | RETAIL 基準中最強既有模型的通過率 | 最強既有模型 1.0%；作者提出的 TGMA 多 Agent 框架 2.72% | 2025-11（EMNLP 2025） | 論文（ACL Anthology 摘要） | https://aclanthology.org/2025.emnlp-main.752/ | 已查證（2026-11-11） |

---

## A. Attention Getter：一個沒有跟上目標的數字

依交通部道安資訊查詢網的初估值，台灣 2025 年道路交通事故 30 日死亡 2,858 人，比 2024 年只少 92 人，降幅 3.1% [I1]；政府為 2030 年死亡人數減半，訂下每年減少 7% 的目標，2025 年只達成約四成 [I20]。其中機車騎士 1,740 人，占 60.9%；2023、2024 年也都在六成以上 [I2]。交通部檢討時指出，機車與高齡者死亡偏多，事故型態中自摔、自撞的比例較為嚴重 [I3]。

騎重機旅遊的人也愈來愈多。大型重型機車登記數在 2025 年底為 279,703 輛，五年內增加 56.4%，十年內約成長為 3.1 倍 [I4]；不過新車領牌數從 2023 年的 27,200 輛降到 2025 年的 15,506 輛 [I5]，表示總量仍在成長，但增速正在放緩。本專題不宣稱能降低事故率，而是從出發前的規劃切入：騎乘時間估錯、天黑前趕路、遇到午後雷雨或封路，都是規劃階段就能先看見的風險。

## B. Background：台灣的重機旅遊

重機旅遊常是一天來回或兩天一夜的山區路線，例如台 20 線南橫、台 8 線中橫、台 14 甲線。這類路線有三個特性。第一，天氣隨時間變化：台灣暖季在綜觀天氣弱時，午後雷雨在 15 至 16 時最強，降雨頻率最高的地方是沿山坡下段的狹長帶 [I8]，騎士在山上的時段直接決定會不會遇雨。第二，道路可能預防性封閉：2025 年 7 月 19 日與 9 月 22 日，公路局都因颱風豪雨對南橫部分路段實施預警性封閉 [I6][I7]。第三，補給點少，山區加油站間距長、營業時間有限。

相關資料已經公開：氣象署提供鄉鎮逐 3 小時預報、逐時觀測、日出日沒時刻與警特報 [I18]，交通部 TDX 提供每分鐘更新的省道路況 [I19]。騎士自己也常有車載 App 記錄的 GPX 軌跡，每一段路的實際騎乘時間都在裡面。技術上，LLM Agent 已能理解自然語言並呼叫外部工具，讓「用對話規劃行程」變得可行。

## C. Problem：要回答的問題

使用者的問題通常是：「週六想騎南橫來回，幾點出發才能在天黑前回到家？中途哪裡加油？哪一段可能下雨或封路？」把它拆開，系統要同時處理三件事：

1. **個人化的時間預測：** 依這位騎士過去的騎法，預測每一段路要騎多久，並給出範圍，而不是單一數字。
2. **時間對齊的風險查詢：** 依「預計抵達該路段的時間」去查那個時段的鄉鎮預報、日落時間和路況，而不是只看出發地的天氣。
3. **跨條件的一致性檢查：** 各段時間加總、回程是否在日落前、加油距離是否超過續航，彼此要互相吻合。

本專題要解決的問題定義為：給定起訖點、途經路線、日期與騎士的歷史 GPX，產生一份可驗證的行程計畫，包括建議出發時間（附範圍）、加油點與各路段的風險說明，並附上每個數字的資料出處。

## D. Existing Limitations：現有方法的不足

**一般導航的預估時間不是個人化的。** Google 地圖 2018 年在台灣推出機車模式，官方說明是以機器學習把機車行駛速度納入考量 [I13]；Google Maps 的 ETA 模型則以整體車流資料訓練，目標是讓多數用路人的預估更準 [I15]。官方說明沒有提到依個別騎士的紀錄調整，也沒有提供時間範圍，而山區彎道路段的騎乘時間因人差異很大。

**重機 App 著重路線與紀錄，不處理時間與風險的整合。** Calimoto、Kurviger、REVER 提供彎道路線規劃、環線、騎乘紀錄與位置分享，REVER 付費方案有天氣警示 [I16][I17]；評測與官方功能清單都沒有提到個人化的抵達時間預測或封路提示。

**單靠 LLM 做不好時間與空間的計算。** 在 TravelPlanner 基準中，GPT-4-Turbo 自己用工具蒐集資料再規劃，同時滿足所有硬性與常識限制的最終通過率只有 0.6% [I9]；更貼近真實旅遊情境的 RETAIL 基準中，最強的既有模型通過率也只有 1.0% [I21]；MapEval 測試 30 個基礎模型，沒有一個在地圖推理上超過 67%，距離與路線規劃是主要弱項 [I12]。加上外部驗證後結果明顯改善：LLM-Modulo 用 critics 檢查計畫，把 GPT-4-Turbo 的通過率從 4.4% 提升到 20.6% [I10]；把問題交給 SMT 求解器的方法達到 93.9% [I11]。這些研究處理的是機票、住宿型的行程，沒有涵蓋騎乘配速、逐時天氣與日落時間這類連續時間的限制。

**資料分散。** 預報、日落、路況與加油站分屬不同平台，目前要靠騎士自己逐一查詢、自己換算時間。

## E. Innovation：本專題的不同之處

1. **用自己的 GPX 學配速，並輸出範圍。** 以騎士歷史行程的實際騎乘時間為正確答案，依曲率、坡度、道路等級等特徵預測每段時間，給出 P50 與 P90，再和 Google Maps 二輪車路線的預估時間比較 [I14]。
2. **依預計抵達時間查風險。** 先算出每段的預計抵達時段，再用該時段的鄉鎮預報、日落時間與路況評估風險，讓午後雷雨這類隨時間變化的因素能落到具體路段上。
3. **把驗證放進規劃迴圈。** 參考 LLM-Modulo 的作法 [I10]，由驗證 Agent 用明確規則檢查計畫，不通過就退回重新規劃，LLM 只負責理解需求、分派工作與解釋結果，數字一律來自工具計算。
4. **回答附出處。** 用知識庫保存氣象署警特報說明、公路局行車資訊與騎乘安全資料，回答時附上來源。

本專題的定位是個人化的出發前決策輔助，不做事故預測。

## F. Contributions：預期貢獻

以下為預期貢獻，實際成效待期末實驗驗證。

1. **個人配速模型與預測區間。** 從 279 趟 GPX 建立路段資料表，以多元迴歸與梯度提升樹（分位數損失）預測路段與整趟時間，輸出 P50／P90。Baseline 為平均速度、速限換算與 Google Maps 二輪車預估時間 [I14]；指標為 MAE、MAPE 與 P90 區間覆蓋率，採依行程分組的交叉驗證，並以最新行程做時間外推測試。預期可量化個人模型在山區路段與導航預估時間的差距。
2. **具驗證與重新規劃的多 Agent 規劃器。** 規劃、配速分析、天氣、路況與補給、驗證五個 Agent 分工；驗證規則包括回程是否早於日落、各段時間加總是否一致、加油距離是否在續航內、回答中的數字是否都能追溯到工具輸出，不通過則重新規劃並設次數上限。預期產出可檢查、可追溯的行程計畫。
3. **台灣開放資料與知識庫的整合。** 串接氣象署鄉鎮預報、觀測、日出日沒與警特報 [I18]、TDX 省道路況 [I19]、內政部地形、加油站資料與 OpenStreetMap 路網，並建立附出處的領域知識庫。預期提供一套可重複使用的資料取得與前處理流程。
4. **含消融實驗的評估設計。** 準備 20 至 30 題規劃問題，比較「只用 LLM」「LLM + 知識庫」「完整 Agent（工具 + 驗證迴圈）」三種做法對獨立 oracle（事先算好的暮光終、營業時間、管制事件與實際行程時間）的違規率、時間誤差與一致率，並報告拒答率；另以歷史行程回測，並做 2 至 3 個完整案例。預期能說明工具計算與驗證迴圈各自帶來多少改善。

本專題只有一位騎士的資料（n = 1），結論限於個人化情境；方法上任何匯入自己 GPX 的騎士都能各自訓練。騎乘中即時回傳與語音提醒列為 L3 延伸，不在 Proposal 承諾範圍內。

---

## References

- [I1][I2] 交通部路政及道安司，〈道安資訊查詢網：事故位置與機車死傷統計（112–114 年為初估值）〉，資料更新 2026-10-27。https://roadsafety.tw/AccOrder?Order=Ieok26&type=%E4%BA%8B%E6%95%85%E4%BD%8D%E7%BD%AE ；https://roadsafety.tw/AccOrder?Order=Age&type=%E6%A9%9F%E8%BB%8A
- [I3] 聯合新聞網，〈政策又跳票？交通事故死亡數去年共奪 2858 命 降幅僅 3.1%〉，2026-03-12。https://udn.com/news/story/7266/9377125 ；TVBS 新聞網，〈台灣 2025 年交通事故死亡人數 2858 人，降幅僅 3.1% 且 4 縣市有攀升跡象〉，2026-04-14。https://cars.tvbs.com.tw/life/315916
- [I4][I5] 交通部公路局，《中華民國 114 年交通部公路局統計年報》，表 26 機動車輛登記數、表 27 新車領牌數，2026。https://ws.thb.gov.tw/001/Upload/436/relfile/13775/5693/fd88dd50-c215-4973-8db5-33f0c3e9510e.pdf
- [I6] 中央社，〈颱風影響　南橫公路梅山口到向陽段預警性封路〉，2025-07-19。https://www.cna.com.tw/news/aloc/202507190089.aspx
- [I7] 中央社，〈樺加沙影響　南橫台東端初來至向陽持續封閉〉，2025-09-23。https://www.cna.com.tw/news/ahel/202509230076.aspx
- [I8] Lin, P.-F., Chang, P.-L., Jou, B. J.-D., Wilson, J. W., Roberts, R. D., "Warm Season Afternoon Thunderstorm Characteristics under Weak Synoptic-Scale Forcing over Taiwan Island," *Weather and Forecasting*, 26(1), 44–60, American Meteorological Society, 2011-02. https://doi.org/10.1175/2010WAF2222386.1
- [I9] Xie, J., et al., "TravelPlanner: A Benchmark for Real-World Planning with Language Agents," ICML 2024. https://arxiv.org/abs/2402.01622
- [I10] Gundawar, A., et al., "Robust Planning with LLM-Modulo Framework: Case Study in Travel Planning," arXiv, 2024-05-31. https://arxiv.org/abs/2405.20625
- [I11] Hao, Y., Chen, Y., Zhang, Y., Fan, C., "Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools," NAACL 2025, pp. 3434–3483, 2025-04. https://aclanthology.org/2025.naacl-long.176
- [I12] Dihan, M. L., et al., "MapEval: A Map-Based Evaluation of Geo-Spatial Reasoning in Foundation Models," ICML 2025. https://arxiv.org/abs/2501.00316
- [I13] Google 台灣官方部落格，〈Google 地圖機車模式正式在台上線〉，2018-07-18。https://taiwan.googleblog.com/2018/07/google.html
- [I14] Google Maps Platform，"Countries and regions supported for two-wheeled vehicles"（Routes API），頁面更新 2026-10-30。https://developers.google.com/maps/documentation/routes/coverage-two-wheeled
- [I15] Derrow-Pinion, A., et al., "ETA Prediction with Graph Neural Networks in Google Maps," CIKM 2021. https://arxiv.org/abs/2108.11482
- [I16] Henges, K., "6 Popular Motorcycle Apps For Finding Routes And Tracking Rides," SlashGear, 2025-01-13. https://www.slashgear.com/1755865/motorcycle-apps-find-routes-track-rides
- [I17] REVER, "REVER PRO," 產品頁，2026-10-31 開啟。https://www.rever.co/pro
- [I18] 中央氣象署，〈氣象資料開放平臺 Opendata API 說明文件〉，2026-10-31 開啟。https://opendata.cwa.gov.tw/apidoc/v1
- [I19] 交通部，〈省道發布路段即時路況資料〉，政府資料開放平臺，2026-10-31 開啟。https://data.gov.tw/dataset/161171
- [I20] 胡瑞玲，〈交通死亡降幅龜速 去年奪2858命僅降3.1％未達標〉，聯合報，2026-03-12。https://udn.com/news/story/7266/9375833
- [I21] B. Deng, Y. Feng, Z. Liu, Q. Wei, X. Zhu, S. Chen, Y. Guo, Y. Wang, "RETAIL: Towards Real-world Travel Planning for Large Language Models," *Proceedings of EMNLP 2025*, pp. 14870–14902, 2025. https://aclanthology.org/2025.emnlp-main.752/
