# 3. Deep Research 深度研究

> 範圍：台灣重機旅遊規劃（山路、天氣、日光、補給、配速、風險）。對應系統：Moto Touring Copilot（規劃 Agent、配速分析 Agent、天氣 Agent、路況與補給 Agent、驗證 Agent）。
> 查證日期：2026-10-31。文中數字只取自實際開啟的頁面；二手來源另外標註。

## 查證紀錄

| Ref | URL opened | verified | note |
| --- | --- | --- | --- |
| D1 | txdot.gov Roadway Design Manual 20.4.2 | yes | 曲率半徑與事故風險倍數 |
| D2 | gov.uk Highway Code rules 103–158 | yes | Rule 125、126、154 |
| D3 | MSF 原始論文 Risk_Factors_From_MSF_100_Study_Paper-1.pdf | yes | 2026-10-31 依文獻審查改引原始論文：「right curve doubles the risk of a crash or near-crash」、「67% of all single-vehicle crashes and near-crashes involved curve negotiation」（含近事故） |
| D4 | UCAR DASH 資料頁（Lin et al.） | yes | 只讀到摘要層級 |
| D5 | cwa.gov.tw 產品說明 8-1-1.pdf | yes | 民用暮光終定義與欄位 |
| D6 | visordown.com 2019 報導 | partial | DfT 疲勞報告的新聞轉述，原報告未找到 |
| D7 | nsw.gov.au 騎士疲勞頁 | yes | 無數字，只有成因與建議 |
| D8 | data.gov.tw/dataset/6065 | yes | 欄位含「營業中」「營業時間」 |
| D9 | cna.com.tw 2025-09-23 | yes | 未提到台14甲與地震 |
| D10 | udn.com 2026-06-10 | yes | 預警性封閉與解封 |
| D11 | insidestategovernment.com.au 2025-10-14 | partial | 轉載 Victoria Police 新聞稿；police.vic.gov.au 原頁 404 |
| D12–D16 | arxiv.org 各篇 abs 頁 | yes | 只讀摘要 |
| D17 | rosap.ntl.bts.gov/view/dot/36257 | yes | 摘要層級 |
| D18–D19 | iihs.org 兩篇新聞 | yes | |
| D20 | HLDI Bulletin 42.13 PDF | yes | 讀第 1 頁摘要 |
| D21 | www.bennetts.co.uk BikeSocial 2019 | partial | 評論文章，引用的計程車研究為汽車且未見原文 |

---

## Q1. 五個核心思維模式

### M1. 以最難的路段規劃，不以平均速度規劃

**意義：** 一趟山路行程的風險和時間誤差集中在少數彎道密集的路段。整趟平均速度會掩蓋這些路段，資深騎士看的是「最難那一段要花多久、能不能安全通過」。

**證據：** TxDOT 設計手冊整理的研究指出，單車事故在半徑 1,500 ft 以下的彎道約為直線路段的近 5 倍風險，半徑 1,500–3,000 ft 約 2 倍 [D1]。英國 Highway Code 要求以「能在可見且淨空的距離內停下」的速度行駛，並提醒鄉間彎道可能比看起來更急 [D2]。MSF 100 自然騎乘研究（100 位騎士、約 36.6 萬英里）指出，右彎的事故與近事故風險約為直線的 2 倍，單車事故與近事故有 67% 涉及過彎；這些數字包含近事故，不等於致命事故風險 [D3]。Victoria Police 也指出團騎死亡最常見的型態之一是彎道失控 [D11]。

**如何影響系統設計：** 配速分析 Agent 以路段為單位預測，特徵包含曲率、坡度與彎道密度，輸出 P50/P90 而不是單一平均值；地圖依路段上色，讓最難的路段一眼可見；baseline 比較刻意納入「整趟平均速度」，用來證明路段化的必要。

### M2. 山區天氣看時間窗，不只看「會不會下雨」

**意義：** 台灣暖季在綜觀天氣弱時，午後對流有明確的日變化。騎士關心的不是當天降雨機率，而是「我抵達山區那一段時是幾點」。

**證據：** Lin et al. 分析 2005–2008 年 5–10 月弱綜觀強迫下的台灣午後雷雨，平均時雨量在地方太陽時 15–16 時達高峰，降雨最頻繁的區域是沿山脈走向的低坡帶 [D4]。

**如何影響系統設計：** 天氣 Agent 不查整天預報，而是用配速 Agent 給出的各段預計抵達時間（含 P90）查該時段該地點的預報；若山區路段的 P90 抵達時間落入午後對流時段，風險規則加權並建議提早出發。具體門檻用歷史行程與觀測回測決定，不預設。

### M3. 日光與騎乘時數是硬限制，不是偏好

**意義：** 天黑後山路的視距與路面辨識度下降，疲勞又會削弱判斷力。資深騎士把「天黑前離開山區」和「定時休息」當成不可談判的條件。

**證據：** 氣象署定義民用暮光終為太陽中心低於地平線 6 度，之後一般戶外活動通常需要人工照明；資料以縣市、逐日提供，含日沒與民用暮光終欄位 [D5]。NSW 政府列出騎士疲勞的成因包括冷熱天氣、噪音、強風與脫水，並建議即使不覺得累也要休息 [D7]。英國 DfT 的騎士疲勞報告據報導指出 14–16 時的午後低谷是高風險時段之一，結論是要更規律休息 [D6]（partial）。

**如何影響系統設計：** 驗證 Agent 的硬規則：整趟 P90 回程時間不得晚於民用暮光終或騎士設定的更早時間，違反就退回規劃 Agent；跨對話記憶保存騎士的最長連續騎乘時數，規劃時自動插入休息點，休息時間計入總時程。

### M4. 補給以「到達時有沒有開」規劃，不只看距離

**意義：** 山區加油站間距長，部分站點營業時間有限。只檢查「續航 > 站距」會漏掉清晨出發或傍晚回程時加油站已關的情況。

**證據：** 中油加油站服務資訊開放資料的欄位包含「營業中」與「營業時間」，另有經緯度與油品別 [D8]。

**如何影響系統設計：** 路況與補給 Agent 先由配速 Agent 取得抵達各站的時間，再用營業時間過濾可用站點；驗證 Agent 檢查任兩個「抵達時有營業」的站點之間距離不超過扣除安全餘量的續航。車系油箱與油耗放在知識庫並附出處。

### M5. 山區道路狀態是動態的，官方會預防性封閉

**意義：** 南橫等山區省道會在豪雨前後預警性封閉，解封取決於現場狀況。昨天能走的路，今天不一定能走；行程要有折返點與替代方案。

**證據：** 2025 年 9 月樺加沙颱風外圍環流使台東山區達超大豪雨警戒（24 小時累積雨量 500 mm 以上），台20線向陽至初來路段（149K+110–199K+000）預警封閉 [D9]。2026 年 6 月台20線寶來二橋至桃源區公所路段因雨預警封閉，雨勢趨緩、排除零星路況後才解除 [D10]。兩篇報導都沒有提到固定的雨量封路門檻。

**如何影響系統設計：** 系統不自行發明封路門檻；路況與補給 Agent 讀 TDX 即時路況，封閉資訊無法以機器取得時，計畫標示「出發前需人工確認」並附公路局來源。規劃 Agent 對每條山區路線預先產生折返點與替代路線。

---

## Q2. 三個最重要的專業爭論

### C1. LLM Agent 能否自我修正規劃，或必須依賴外部驗證器

- **觀點 A：** LLM 透過反思與自我批評就能改善結果。
- **觀點 B：** LLM 的自我檢查不可靠，可行的計畫要靠外部、可靠（sound）的驗證器。
- **雙方最有力的證據：** A 方：Reflexion 以語言化的自我反思回饋，在 HumanEval 達 91% pass@1，高於 GPT-4 原報告的 80% [D15]。B 方：TravelPlanner 中 GPT-4 的成功率只有 0.6% [D12]；以 GPT-4 同時生成與驗證計畫時，自我批評反而降低表現，且 LLM 驗證器產生大量偽陽性 [D14]；LLM-Modulo 加上外部批評器後，GPT-4 Turbo 表現約提升 4.6 倍 [D13]；把旅遊規劃轉成可滿足性問題交給求解器，成功率達 93.9%，同文指出 o1-preview 約 10% [D16]。
- **目前共識：** 對有硬限制（時間、預算、距離）的規劃，外部可靠驗證器是目前最有效的做法；自我反思在有客觀回饋（例如測試結果）的任務中較有效。
- **尚未解決的問題：** 風險、舒適度這類軟性限制很難寫成可靠驗證器；驗證器沒涵蓋到的錯誤仍會通過。
- **對本專題的意義：** 驗證 Agent 用程式規則檢查時間、續航、日落與數字來源，不讓 LLM 自己判斷「計畫是否可行」；消融實驗（只用 LLM vs 完整 Agent）直接檢驗這個爭論。

### C2. 配速模型應個人化，還是用可轉移的通用模型

- **觀點 A：** 速度選擇因人而異，需要用個人資料訓練。
- **觀點 B：** 通用的彎道速度模型經校準就能跨地區使用，個人資料太少反而不穩。
- **雙方最有力的證據：** SHRP2 資料的研究同時支持兩邊：德州建立的速度差模型乘上調整係數後可用在印第安納州（B）；但熟悉路線的駕駛在彎道中點的 85 百分位速度較高，且模型對不熟悉路線的駕駛預測較準（A）[D17]。TxDOT 也指出機車過彎行為與汽車不同：入彎減速、車道內橫移、出彎加速 [D1]，代表汽車模型不能直接套用在機車。
- **目前共識：** 群體模型經校準可以轉移；個人熟悉度是主要的變異來源，通用模型對熟悉路線的騎士誤差較大。
- **尚未解決的問題：** 需要多少趟個人資料才夠；騎士配速隨時間漂移；個人模型在沒騎過的路線（冷啟動）表現如何。
- **對本專題的意義：** 以個人 GPX 訓練，baseline 包含通用估計（Google Maps、速限換算）；驗證採依行程分組與時間外推，並把「熟悉／不熟悉路線」分開報告誤差。

### C3. ABS 等電子輔助的安全效益，會不會被風險補償抵銷

- **觀點 A：** ABS 實質降低事故，效益不是自我選擇造成的。
- **觀點 B：** 騎士會把安全裕度換成更快的速度，總體效益被稀釋。
- **雙方最有力的證據：** A 方：IIHS 2021 年研究顯示有 ABS 的機車致命事故率低 22%，旅行車型約低 25% [D18]；HLDI 2014 年發現高風險騎士選 ABS 的比例不低於低風險騎士且同樣受益，自我選擇無法解釋效果 [D19]；HLDI 2025 年更新顯示 ABS 使碰撞理賠頻率下降 25% [D20]。B 方：風險補償理論代表人物 John Adams 認為 ABS 的效益會被騎士當成性能消耗掉；評論文章引用英國 2013–2017 年大型機車死亡數大致持平，即使 ABS 已強制 [D21]（partial，屬總體統計，干擾因素多）。
- **目前共識：** ABS 的事故降低效果有大量資料支持；機車騎士的風險補償缺少直接量測，目前多為理論與總體數字推論。
- **尚未解決的問題：** 沒有研究直接比較 ABS 與非 ABS 騎士的實際路上速度；彎道 ABS、循跡控制等新輔助的行為影響未知。
- **對本專題的意義：** Copilot 本身也是一種安全輔助，可能讓騎士更晚出發、更貼近極限。系統因此以 P90 而不是 P50 判斷是否趕得上日落，不因車輛有 ABS 而放寬風險規則，並在回答中清楚說明不確定性。

---

## Q3. 十個深度理解問題

| # | 類型 | 問題 | 好答案的重點 |
| --- | --- | --- | --- |
| 1 | Why | 為什麼整趟平均速度不適合用來判斷能否天黑前回家？ | 風險與時間誤差集中在彎道密集的山區路段 [D1]。平均值會掩蓋最慢那一段，而天黑時人可能正好在最難的路段上；要用路段化預測加 P90。 |
| 2 | What-if | 如果配速模型的 P50 很準，但 P90 區間覆蓋率只有 60%，會發生什麼？ | 系統會低估晚歸的機率，日落硬規則形同失效。好答案會提到用覆蓋率當評估指標，並以分位數損失或校準修正。 |
| 3 | Trade-off | 預防性封路的資訊沒有機器可讀 API，系統要「保守地全部警示」還是「只警示有資料的路段」？ | 全部警示會造成警示疲乏，只警示有資料的會漏報。合理做法是區分「已知封閉」「狀態未知需人工確認」兩級，並附公路局來源 [D9][D10]。 |
| 4 | Failure Case | 驗證 Agent 全部通過，計畫還可能在哪些地方出錯？ | 驗證只檢查有寫成規則的硬限制，例如時間、續航、日落 [D13]。路面碎石、臨時施工、騎士當天身體狀況都不在規則內；所以要有折返點並標示驗證範圍。 |
| 5 | Evidence | 「右彎風險較高」這個說法的證據強度如何？能直接用在台灣嗎？ | MSF 100 原始論文 [D3] 的數字包含近事故，樣本是美國 100 位騎士。台灣同為靠右行駛，方向上可比，但道路幾何與交通組成不同，只能當假設，要用自己的 GPX 檢查。 |
| 6 | Comparison | 個人配速模型和 Google Maps 預估時間，各自在什麼情境比較準？ | 個人模型在騎過的路線、休閒騎乘情境應較準，因為熟悉度會改變速度 [D17]。Google Maps 有即時車流，塞車路段可能較準；沒騎過的路線個人模型可能退化。 |
| 7 | Design Decision | 為什麼驗證交給程式規則，不讓另一個 LLM 當驗證者？ | LLM 自我驗證有大量偽陽性，甚至降低規劃表現 [D14]；外部可靠驗證器在 TravelPlanner 類任務效果明顯 [D13][D16]。LLM 負責理解與解釋，數字一律來自工具輸出。 |
| 8 | Real-world Scenario | 週六團騎南橫，朋友騎得比你快，系統該怎麼規劃？ | 團騎中試圖跟上是可能的致命因素 [D11]。計畫應以隊伍中最慢者的配速估計，設集合點，並提醒各自以自己的速度騎。 |
| 9 | What-if | 如果出發當天早上下過雨，但預報下午轉晴，計畫要怎麼調整？ | 雨後路面與落石風險未必隨天氣轉晴消失，南橫封閉也是雨勢趨緩後才視路況解除 [D10]。應先確認封閉狀態、降低山區路段配速假設並重算日落餘裕。 |
| 10 | Trade-off | 為了避開午後對流提早出發，代價是什麼？ | 清晨氣溫低、加油站可能未營業 [D8]，疲勞也可能提早累積 [D7]。好答案要說明這是多目標權衡，系統應比較不同出發時間的方案，而不是只給單一答案。 |

---

## References

- [D1] Texas Department of Transportation. *Roadway Design Manual*, Section 20.4.2 Horizontal Curves (Specific). TxDOT, online edition（未載明年份）. https://www.txdot.gov/manuals/des/rdw/chapter-20-motorcyclist-design-considerations/20-4-highway-features/20-4-2-horizontal-curves--specific--.html
- [D2] Department for Transport. *The Highway Code*: General rules, techniques and advice for all drivers and riders (103 to 158). GOV.UK, online edition. https://www.gov.uk/guidance/the-highway-code/general-rules-techniques-and-advice-for-all-drivers-and-riders-103-to-158
- [D3] Williams, V., McLaughlin, S., Atwood, J., Buche, T. "Factors that Increase and Decrease Motorcyclist Crash Risk." Virginia Tech Transportation Institute / Motorcycle Safety Foundation (MSF 100 Motorcyclists Naturalistic Study), 2016. https://msf-usa.org/wp-content/uploads/2021/07/Risk_Factors_From_MSF_100_Study_Paper-1.pdf
- [D4] Lin, P., Chang, P., Jou, B. J.-D., Wilson, J. W., & Roberts, R. "Warm season afternoon thunderstorm characteristics under weak synoptic-scale forcing over Taiwan Island." American Meteorological Society; record at UCAR/NCAR DASH, 2011. https://ckanprod.data-commons.k8s.ucar.edu/dataset/warm-season-afternoon-thunderstorm-characteristics-under-weak-synoptic-scale-forcing-over-taiwa
- [D5] 中央氣象署。《日出日沒時刻：全臺各縣市年度逐日日出日沒時刻資料》產品說明文件，2023。https://www.cwa.gov.tw/Data/data_catalog/8-1-1.pdf
- [D6] Visordown. "Government runs study into rider fatigue." Visordown, 2019. https://www.visordown.com/news/general/government-runs-study-rider-fatigue
- [D7] NSW Government. "Fatigue"（Safe riding behaviour for motorcyclists）. nsw.gov.au, n.d. https://www.nsw.gov.au/driving-boating-and-transport/roads-safety-and-rules/motorcycles-and-scooters/safe-riding-behaviour-for-motorcyclists/fatigue
- [D8] 台灣中油股份有限公司。〈台灣中油公司加油站服務資訊〉，政府資料開放平臺。https://data.gov.tw/dataset/6065
- [D9] 中央社。〈樺加沙影響 南橫台東端初來至向陽持續封閉〉，2025-09-23。https://www.cna.com.tw/news/ahel/202509230076.aspx
- [D10] 聯合報（張議晨）。〈高雄山區豪雨狂炸…全台3日累積雨量包辦前2名 台20線部分路段今恢復通行〉，2026-06-10。https://udn.com/news/story/7266/9557495
- [D11] Inside State Government. "Victoria Police revs up group safety message for motorcyclists"（轉載 Victoria Police 新聞稿）, 2025-10-14. https://www.insidestategovernment.com.au/victoria-police-revs-up-group-safety-message-for-motorcyclists/
- [D12] Xie, J., et al. "TravelPlanner: A Benchmark for Real-World Planning with Language Agents." ICML, 2024. https://arxiv.org/abs/2402.01622
- [D13] Gundawar, A., et al. "Robust Planning with LLM-Modulo Framework: Case Study in Travel Planning." arXiv, 2024. https://arxiv.org/abs/2405.20625
- [D14] Valmeekam, K., Marquez, M., & Kambhampati, S. "Can Large Language Models Really Improve by Self-critiquing Their Own Plans?" arXiv, 2023. https://arxiv.org/abs/2310.08118
- [D15] Shinn, N., et al. "Reflexion: Language Agents with Verbal Reinforcement Learning." arXiv, 2023. https://arxiv.org/abs/2303.11366
- [D16] Hao, Y., Chen, Y., Zhang, Y., & Fan, C. "Large Language Models Can Solve Real-World Planning Rigorously with Formal Verification Tools." arXiv, 2024. https://arxiv.org/abs/2404.11891
- [D17] Geedipally, S. R., et al. "Evaluating Curve Speed Behavior Using SHRP 2 Data." ATLAS Center, Report ATLAS-2017-21, 2017. https://rosap.ntl.bts.gov/view/dot/36257
- [D18] IIHS. "Largest study of its kind strengthens argument for motorcycle ABS." IIHS News, 2021. https://www.iihs.org/news/detail/largest-study-of-its-kind-strengthens-argument-for-motorcycle-abs
- [D19] IIHS. "Motorcycle ABS benefits both high-risk and low-risk riders." IIHS News, 2014. https://www.iihs.org/news/detail/motorcycle-abs-benefits-both-high-risk-and-low-risk-riders
- [D20] Highway Loss Data Institute. "Evaluation of motorcycle antilock braking systems, alone and in conjunction with combined control braking systems: an update." HLDI Bulletin 42(13), 2025. https://www.iihs.org/media/66a450d6-b3c2-40cd-9716-cab3a7c37ff9/W7ERBQ/HLDI%20Research/Bulletins/hldi_bulletin_42.13.pdf
- [D21] Purvis, B. "Why isn't ABS saving our lives?" Bennetts BikeSocial, 2019. https://www.bennetts.co.uk/bikesocial/news-and-views/features/bikes/why-isnt-abs-saving-our-lives
