# DESIGN — Moto Touring Copilot 重機旅遊規劃顧問

> 狀態：實作前（2026-11-14 完成 Scope Reduction、Design Review Fix 與 M0 決策，範圍為 **Level 2 Lite 的 Agent-first MVP**）。**尚未實作，沒有任何實驗結果，UI Prototype 也尚未建立。** M0 進行中：資料契約 v0.2 已審查並凍結，供 M1 Spike 使用；最小專案骨架與契約測試已建立；已收到 21 趟 GPX；`ingest`、`routes`、`pace` 與 ETA 的 Spike 都已執行，輸出通過契約檢查。M1 Review 已完成：兩條示範路線與保留行程暫定接受；LLM Smoke Test 只完成本地驗證，真實 API 測試為 NOT RUN（§13.4）。
> 完整論述、文獻與證據見 [Proposal](docs/proposal/proposal.pdf)。Proposal 描述的是縮減前的完整設計；兩者不一致時，實作以本文件為準，差異與理由記錄在 [§13.1](#131-scope-reduction-紀錄2026-11-14)，設計審查的修正記錄在 [§13.2](#132-design-review-fix-紀錄2026-11-14)，M0 決策記錄在 [§13.3](#133-m0-決策紀錄2026-11-14)。
> 本文件著重「下一位開發者如何理解、執行、驗證並接手」。

## 目錄

1. [Problem](#1-problem)
2. [Requirements](#2-requirements)
3. [Architecture](#3-architecture)
4. [Components](#4-components)
5. [Data](#5-data)
6. [AI / Analytics](#6-ai--analytics)
7. [Domain Knowledge](#7-domain-knowledge)
8. [Algorithm](#8-algorithm)
9. [Implementation Mapping](#9-implementation-mapping)
10. [How to Run](#10-how-to-run)
11. [Results](#11-results)
12. [Limitations](#12-limitations)
13. [Change Log](#13-change-log)

## 1. Problem

騎士出發前最常問、也最容易判斷錯的問題是：「照我的騎法，這趟山路幾點出發才能在天黑前回家？中途哪裡加油？哪一段可能下雨或封路？」

- 一般導航的預估時間是群體平均，不知道個別騎士在彎道與坡道的騎法。
- 天氣、日落、路況、加油站分散在不同平台，騎士要自己換算「抵達該路段時」的狀況。
- 大型語言模型單獨規劃行程並不可靠（TravelPlanner 中 GPT-4-Turbo 同時滿足所有限制的最終通過率 0.6%；RETAIL 中最強的既有模型 1.0%），需要外部工具計算與驗證。
- 近期多 Agent 規劃系統（Vaiage、ROAM）已把天氣、道路距離與營業時間帶進規劃，但對象是城市景點行程，沒有依個人速度推算各點抵達時間。

定位：個人化的**出發前決策輔助**，不做事故預測，也不宣稱能降低事故率。

### 核心研究問題（MVP）

> AI Agent 結合確定性工具與獨立驗證機制，能否提高重機旅遊行程規劃的可行性？

這個問題由 E2 回答（§6.3）。個人配速在 MVP 是支撐這個問題的工具，由 E1 Lite 檢查它是否比單一平均速度合理（§6.2）。

## 2. Requirements

### 2.1 功能需求

需求編號沿用 Proposal 階段的 FR1–FR8，內容依 MVP 範圍修訂。

| ID | 需求（MVP 版本） | 範圍 | 與原版的差異 |
| --- | --- | --- | --- |
| FR1 | 以表單欄位與自然語言描述行程（示範路線、日期、最早可出發時間、最晚抵達終點時間、出發油量），需求有歧義時追問 | Must | 路線限定在路線目錄內，一次規劃是一條單向路線從頭騎到尾；目錄外的路線回覆「不在支援範圍」。會影響驗證的條件用表單欄位；自然語言只補充休息與偏好，其中會影響 ETA 的休息安排要轉成結構化資料。兩者衝突時以表單為準並提示 |
| FR2 | 以指令匯入騎士自己的 GPX，建立個人配速表 | Must | 15–30 趟代表性行程；介面上傳與自動更新模型不做 |
| FR3 | 估計各路段騎乘時間與各點抵達時間，輸出「典型估計」與「加上安全餘裕的保守估計」 | Must | 原為 P50／P90 分位數；MVP 的保守估計**不是**經過校正的 P90（§6.1） |
| FR4 | 依各路段預計抵達時間查氣象署預報與民用暮光終 | Must | 氣象署警特報為 Should；高降雨機率提醒是本專題自訂的門檻（§4.2） |
| FR5 | 查沿線加油站位置與營業時間，依騎士的出發油量逐段檢查油量；處理封路事件 | Must | 加油站為靜態快照；不預設滿油；封路以情境檔提供並標示來源；TDX 即時路況為 Should |
| FR6 | 驗證整份計畫（規則 1–5），沒有可用計畫就重新規劃；無可行解時說明原因與替代方案 | Must | 每條規則為 PASS／FAIL／UNKNOWN，計畫狀態為 FEASIBLE／CONDITIONAL／INFEASIBLE（§4.2） |
| FR7 | 以 Streamlit 的三個畫面呈現（Trip Planner、Trip Result、Validation & Replanning，§9.6）；驗證狀態與資料來源以獨立區塊呈現，回答附出處 | Must | 地圖儀表板與可下載的計畫檔為 Should；不依賴 Google Maps |
| FR8 | 騎乘中手機定位經 MQTT 回傳，即時更新抵達時間並語音提醒 | Won't | 原為延伸（L3），本次確定不做 |

### 2.2 非功能需求

| ID | 需求 |
| --- | --- |
| NFR1 | 回答中的每個時間、距離、機率都必須來自工具輸出（可追溯） |
| NFR2 | 原始 GPX 不進版控；公開資料只放裁掉頭尾後的衍生路段表 |
| NFR3 | 不在車上加裝任何設備 |
| NFR4 | 外部 API 失敗、資料缺漏或超出資料涵蓋範圍時，結果標示為 UNKNOWN 並告知騎士，不以猜測補值 |
| NFR5 | 模擬的測試資料（例如封路情境）必須帶有來源標記，在介面、實驗紀錄與結果中都和真實事件分開呈現 |

NFR5 是本次新增，來自 Scope Reduction 的設計約束。

### 2.3 Scope Matrix（Must / Should / Won't）

Must 是 MVP 承諾完成的範圍。Should 只在里程碑 M3 準時完成時才做（§9.3），不影響 MVP 驗收。Won't 是本學期確定不做，列入 Future Work（§12）。

| 領域 | Must Have | Should Have | Won't Have |
| --- | --- | --- | --- |
| Agent 架構 | 單一 Planner LLM＋確定性 Python 工具＋獨立 Validator | — | 五個獨立 LLM Agent |
| 騎士資料 | 靜態 Rider Profile | — | 跨 Session Memory |
| 路線 | 2–3 條固定示範路線（路線目錄） | — | 任意路線自動產生 |
| GPX | 15–30 趟代表性行程 | — | 279 趟全量處理 |
| 配速 | 基礎配速表、ETA、時間餘裕計算 | 多元迴歸（MLR）、LightGBM | 完整 P50／P90 分位數模型、conformal 校正 |
| 特徵 | 由軌跡本身算出的簡單路段類別 | — | 完整 DTM／OSM 特徵工程 |
| 天氣與日照 | 氣象署預報、民用暮光終 | 氣象署警特報 | 歷史天氣作為配速特徵 |
| 補給 | 靜態加油站快照、依出發油量的逐段油量檢查 | — | — |
| 路況 | 封路情境（標示來源）與資料缺失的安全處理 | TDX 即時路況 | E3 真實歷史封路回測、RPi 5 每日收集器 |
| 知識 | 最小領域知識庫（關鍵字檢索、附出處） | 進階知識檢索 | — |
| 介面 | Streamlit 的三個畫面：Trip Planner、Trip Result、Validation & Replanning | 進階地圖 | Google Routes／Google Maps 作為必要依賴 |
| 實驗 | E1 Lite、E2（三組、12–15 題、獨立 Oracle） | — | E3；E2 的逐一拿掉模組消融；E4 作為獨立實驗（併入 Demo） |
| IoT | — | — | L3：MQTT、即時定位、語音提醒 |

期末必繳項目不在刪減範圍內，見 §9.5。UI/UX Prototype 是開發流程的產物（§9.6），不是 MVP 的功能，不列入上表。

### 2.4 範圍（對應課程 Level）

| Level | 內容 | 範圍 |
| --- | --- | --- |
| L1 | 對話、讀 GPX 與開放資料、Python 分析 | 包含在 L2 Lite 內 |
| L2 Lite | 知識庫、單一 Planner 的多步工具呼叫、獨立驗證與重新規劃 | 承諾完成 |
| L3 | 騎乘中即時串流與語音提醒 | 不做 |

## 3. Architecture

MVP 架構：

```mermaid
flowchart TB
    U["① 使用者與情境：重機旅遊騎士"] --> Q["② 問題輸入：Trip Planner 畫面，欄位＋自然語言；GPX 以指令匯入"]
    Q --> PL
    subgraph P["③ Planner & Reasoning"]
        direction TB
        PL["Planner：單一 LLM，以工具呼叫取得數字"]
        VA{"Validator：確定性 Python，規則 1–5<br/>每條規則 PASS / FAIL / UNKNOWN<br/>計畫狀態與候選排序"}
        PL -- 計畫草案 --> VA
        VA -- 候選全部 INFEASIBLE：重新規劃 --> PL
    end
    subgraph T["⑤ Analytics Engine：確定性工具"]
        direction LR
        T1["配速與 ETA<br/>典型估計＋安全餘裕"]
        T2["天氣與日照"]
        T3["加油站與油量"]
        T4["路況事件<br/>情境檔，標示來源"]
    end
    D["④ 資料：15–30 趟 GPX、路線目錄、氣象署預報與日出日沒、靜態加油站、路況情境檔"]
    K["⑥ Domain Knowledge：最小知識庫"]
    PL <--> T
    PL <--> K
    T <--> D
    VA -- FEASIBLE 或 CONDITIONAL --> R["⑦ 決策與建議：計畫狀態、出發時間、抵達時間範圍、加油安排、風險、UNKNOWN 項目"]
    R --> OUT["⑧ 輸出：Trip Result 與 Validation & Replanning 畫面"]
    VA -- 重試用盡：不可行報告 --> OUT
```

Proposal 的原始架構圖（五個 Agent）保留在 [docs/figures/architecture.png](docs/figures/architecture.png) 供對照，**不代表 MVP**。

依作業規範的 ①–⑧ 模組：

| 編號 | 模組 | MVP 內容 |
| --- | --- | --- |
| ① | 使用者與情境 | 在台灣騎重機旅遊的騎士 |
| ② | 問題輸入 | Trip Planner 畫面：固定路線、日期、最早可出發時間、最晚抵達終點時間、出發油量的欄位，加上自然語言需求；GPX 以指令匯入 |
| ③ | Planner & Reasoning | 單一 Planner LLM 理解需求、呼叫工具、組成計畫；獨立的 Validator 檢查每條規則、決定計畫狀態並排序候選計畫；沒有可用計畫時重新規劃 |
| ④ | 資料取得 | 自己的 GPX、路線目錄、氣象署、靜態加油站、路況情境檔（§5） |
| ⑤ | Analytics Engine | 配速與 ETA、天氣與日照、續航、路況事件：全部是確定性的 Python 工具 |
| ⑥ | Domain Knowledge | 最小知識庫，關鍵字檢索，回答附出處 |
| ⑦ | 決策與建議 | 計畫狀態、出發時間、典型與保守抵達時間、加油安排、風險說明、UNKNOWN 項目 |
| ⑧ | 輸出與互動 | Trip Result 與 Validation & Replanning 畫面；逐條規則的狀態與資料來源以獨立區塊呈現 |

設計原則：

1. LLM 負責理解、規劃與解釋；所有數字由確定性工具計算。
2. Validator 與 Planner 分離：Validator 是不含 LLM 的 Python 程式，由主程式在 Planner 之外執行，Planner 不能略過或改寫它的結果。
3. 資料不足時回報 UNKNOWN，不補值（NFR4）。
4. 模擬資料與真實資料分開標示（NFR5）。
5. Validator 的三值狀態與來源證據是介面的核心資訊，以獨立區塊呈現，不藏在對話文字裡（§9.6）。

## 4. Components

### 4.1 Planner、工具與 Validator

Proposal 的五個 Agent 在 MVP 收斂為一個 LLM 與一組確定性元件。原本由「配速、天氣、路況與補給」三個 Agent 負責的工作改成工具，原本的驗證 Agent 改成 Validator。

| 元件 | 類型 | 輸入 | 輸出 |
| --- | --- | --- | --- |
| Planner | LLM（唯一的 LLM） | 使用者問題、騎士設定檔、工具輸出、Validator 結果 | 追問、工具呼叫、結構化的休息與加油安排、說明文字。計畫中的數值由主程式從工具輸出填入，不由 Planner 填寫 |
| 配速與 ETA 工具 | 確定性 | 路線、出發時間、配速表、休息時間 | 各段典型時間、各點典型與保守抵達時間 |
| 天氣工具 | 確定性 | 各段位置與抵達時段 | 該時段的氣象署預報，或 UNKNOWN |
| 日照工具 | 確定性 | 路線所在地、日期 | 民用暮光終，或 UNKNOWN |
| 加油站與油量工具 | 確定性 | 路線、典型與保守抵達時間、Rider Profile、騎士當次的出發油量 | 沿線加油站與營業時間、各路段油耗、抵達各站前的剩餘油量、補油後的續航；資料缺漏處為 UNKNOWN |
| 路況事件工具 | 確定性 | 路線、日期 | 事件清單（每筆帶來源標記），沒有事件來源時為 UNKNOWN |
| 知識庫檢索 | 確定性 | 查詢字串 | 段落與出處 |
| Validator | 確定性，不含 LLM | 結構化計畫、工具輸出 | 規則 1–5 各自的 PASS／FAIL／UNKNOWN 與理由、計畫狀態 |

騎士設定檔（Rider Profile）是靜態檔案：車型、油箱容量、平均油耗、安全保留油量（暫定為油箱容量的 20%，可在設定檔調整）、休息習慣、預設的最晚抵達終點時間。出發油量不放在設定檔，騎士每次規劃時必須明確提供，以油箱的百分比（0–100%）輸入，由工具依油箱容量換算成公升。所有油量與續航的計算都由工具執行，Planner 不自行估算。MVP 不做 Proposal 的跨 Session「騎士記憶」（PD-3 定案）。

### 4.2 驗證規則

符號：`ETA_typ` 是典型抵達時間，`ETA_safe` 是加上安全餘裕後的保守抵達時間（定義見 §6.1）。`ETA_safe` 取代 Proposal 的 P90 抵達時刻，它是保守估計，不是分位數。

| 規則 | PASS 條件 | UNKNOWN 條件 |
| --- | --- | --- |
| 1 日照 | 終點的 `ETA_safe` ≤ min（民用暮光終, 最晚抵達終點時間） | 取不到暮光終資料，而且保守估計沒有超過最晚抵達終點時間。保守估計已經超過最晚抵達終點時間時是 FAIL，不是 UNKNOWN |
| 2 油量 | 從出發油量逐段扣除油耗後，每個檢查點的剩餘油量都不低於安全保留油量；抵達計畫加油站的時段 [`ETA_typ`, `ETA_safe`] 在營業時間內；補油後足以抵達下一個補給點或終點（細節見下） | 缺油箱容量、平均油耗或該站的營業時間（出發油量是必填，缺少時不進入規劃） |
| 3 天氣（專題自訂策略） | 高降雨機率路段（抵達時段 [`ETA_typ`, `ETA_safe`] 內任一預報時段的 PoP ≥ 70%，定義見下）不位於路線最後 20% 的距離範圍內 | 取不到預報，或日期超出預報涵蓋期間 |
| 4 路況 | 路線上沒有封閉或管制事件 | 沒有可用的事件來源；**不得預設為 PASS** |
| 5 可追溯 | 計畫的數值欄位由主程式從工具輸出填入；Planner 說明文字中的每個數字也都出現在工具輸出中 | 不適用（只有 PASS／FAIL） |

**計畫狀態（PD-1 定案）。** 由 Validator 依規則結果決定，Planner 不能改寫。

| 計畫狀態 | 條件 | 能否作為建議 |
| --- | --- | --- |
| `FEASIBLE` | 所有規則 PASS | 可以 |
| `CONDITIONAL` | 沒有 FAIL，至少一條 UNKNOWN | 可以，但必須逐條列出 UNKNOWN 的規則與騎士要自行確認的事項 |
| `INFEASIBLE` | 至少一條 FAIL | 不可以，只用來說明原因與替代方案 |

候選計畫的排序：先比狀態，`FEASIBLE` 優先於 `CONDITIONAL`；狀態相同時選出發時間最晚的候選（§8）。候選只要不是 `INFEASIBLE`，它的保守估計就已經在期限內。計畫狀態由規則 1–4 逐候選判定。規則 5 是最終輸出的強制關卡：說明文字（或它的固定模板）通過之後，計畫才維持規則 1–4 決定的狀態；都沒通過時回報輸出驗證錯誤，不顯示計畫狀態（§8）。候選搜尋另外有 COMPLETE／INCOMPLETE 狀態，不和計畫狀態混在一起。`INFEASIBLE` 的候選不參與排序。沒有 `FEASIBLE` 但有 `CONDITIONAL` 時，提供條件式計畫；全部 `INFEASIBLE` 時回報原因與替代方案。

MVP 沒有即時路況來源，所以真實日期的規劃在規則 4 上是 UNKNOWN，計畫狀態最多是 `CONDITIONAL`。這是刻意的設計結果，不是缺陷：系統不知道有沒有封路時不能說可行。騎士自行確認路況不會把 UNKNOWN 改為 PASS；介面把它列為出發前要確認的事項。

**規則 2 的油量檢查。** 不預設滿油。

1. 出發油量是必填，由騎士當次以油箱的百分比（0–100%）明確提供，由工具依 Rider Profile 的油箱容量換算成公升；沒有提供時 Planner 追問，不進入規劃，也不以滿油代替。油箱容量、平均油耗與安全保留油量來自 Rider Profile；安全保留油量暫定為油箱容量的 20%，可在設定檔調整。
2. 各路段油耗 = 路段距離 × 平均油耗。從出發油量逐段扣除，得到抵達每個計畫加油站前與抵達終點時的剩餘油量；這些位置稱為檢查點。
3. 只有在計畫明確安排在該站加滿，且該站可用（有營業時間資料，抵達時段在營業時間內）時，補油後的油量才以滿油計算，再繼續逐段扣除到下一個補給點或終點。其他情況油量不重置。
4. PASS：每個檢查點的剩餘油量 ≥ 安全保留油量，且抵達各計畫加油站的時段都在營業時間內。
5. FAIL：任一檢查點的剩餘油量低於安全保留油量，或抵達時段有任何部分落在營業時間外。
6. UNKNOWN：缺油箱容量、平均油耗，或計畫加油站沒有營業時間資料。不以預設值代替；該站之後的剩餘油量取決於能否補油，不報告為確定的數值。
7. 以上計算全部由油量工具執行，Planner 不自行估算油量或續航。E2 的 A1 是沒有工具的對照組，不適用這一條。

**規則 3 的高降雨機率提醒（PD-4 定案，專題自訂策略）。** MVP 只使用氣象署預報的降雨機率（PoP）。

| PoP | 自訂顯示分類 | 對規則 3 的作用 |
| --- | --- | --- |
| 0–39% | 低降雨機率 | 無 |
| 40–69% | 中降雨機率 | 無，只顯示 |
| 70–100% | 高降雨機率提醒 | 該路段標為高降雨機率路段 |

- 門檻（PoP ≥ 70%）與三段分類都是**本專題自訂的暫行設定**，沒有經過驗證，不是氣象署的分類。
- PoP 是降雨的機率，**不代表降雨強度**，也**不等於氣象署的大雨或豪雨特報**。介面、報告與簡報一律稱為「高降雨機率提醒」，不得寫成警特報或大雨預報。
- 規則 3 沿用原先的保守做法：高降雨機率路段若位於路線最後 20% 的範圍，結果為 FAIL。這個範圍以路線的累計距離計算，不依路段數；跨入這個範圍的路段也算在內。這是專題自訂的保守策略，不是官方的天氣安全標準。
- 取不到預報或日期超出預報涵蓋期間時，結果為 UNKNOWN。
- 氣象署警特報屬 Should：實作時以官方名稱另外呈現，不和高降雨機率提醒合併成同一個訊號。

### 4.3 對應課程框架

| 課程 Workflow | 本專題（MVP） |
| --- | --- |
| Understand | Planner 取出行程條件，缺資訊就追問 |
| Plan | Planner 決定工具呼叫順序與候選出發時間 |
| Acquire | 工具取得預報、暮光終、加油站與路況事件 |
| Analyze | 配速表、ETA 與餘裕、續航計算、風險規則 |
| Generate | Validator 檢查後產生建議；不可行時提出替代方案 |
| Interact | Streamlit 的三個畫面（§9.6） |

六大能力（TALK、KNOW、SENSE、ANALYZE、THINK、SHOW）的原始對應見 Proposal §4.4.2。MVP 的差異：SENSE 不含騎乘中的定位串流；ANALYZE 以配速表為主，迴歸與梯度提升樹為 Should；THINK 是單一 Planner 加獨立驗證，不是多 Agent；SHOW 不含語音，地圖為 Should。

## 5. Data

| 來源 | 用途 | 取得方式 | MVP 範圍 | 備註 |
| --- | --- | --- | --- | --- |
| BMW Motorrad Connected GPX | 配速表、E1 Lite、E2 Oracle 的實際行程時間 | App 內逐趟匯出 | Must：15–30 趟代表性行程。279 趟全量為 Won't | 約 1 秒一點，只有經緯度、高度、時間；**不進版控** |
| 路線目錄 | 2–3 條固定示範路線的幾何與切段 | 由自己騎過該路線的 GPX 裁切後建立 | Must | 公開的是裁掉頭尾後的衍生路段表 |
| 中央氣象署預報 | 抵達時段的天氣 | opendata.cwa.gov.tw API（需授權碼） | Must | 超出預報涵蓋期間回報 UNKNOWN |
| 中央氣象署日出日沒 | 民用暮光終 | 氣象署開放資料 | Must | |
| 中油加油站資料 | 位置、營業時間 | 政府資料開放平臺 data.gov.tw/dataset/6065，存成靜態快照 | Must | 記錄快照日期；台塑沒有開放資料，MVP 不涵蓋（§12） |
| 中央氣象署警特報 | 以官方名稱呈現的警特報 | 氣象署開放資料 | Should | 不和自訂的高降雨機率門檻混用（§4.2） |
| 車輛規格 | 油箱容量、平均油耗 | BMW 車系規格，寫入 Rider Profile 與知識庫 | Must | 油耗以單一平均值計算（§12） |
| 路況事件情境檔 | 規則 4、E2 的封路題 | 人工編寫 | Must | 每筆帶 `source`：`simulated`（模擬）或 `real`（真實公告，附出處） |
| 交通部 TDX | 省道即時路況 | TDX API（需授權碼） | Should | |
| Google Maps Platform | 地圖顯示、預估時間對照 | Maps JavaScript API、Routes API | 非必要依賴 | E1 Lite 只在 Should 中以人工查詢的紀錄作參考 |
| 內政部 20 m DTM、公路局 GIS、OpenStreetMap | 坡度、急彎、道路等級特徵 | 政府資料開放平臺、OSMnx | Won't | 完整特徵工程不做 |
| CODiS 歷史天氣 | 配速模型的天氣特徵 | CODiS | Won't | MVP 的配速不使用天氣特徵 |

### 資料處理流程（GPX）

1. 裁掉每趟起點與終點附近的路段（住家與工作地點隱私）
2. 清理車速跳點並平滑
3. 分離移動時間與停留時間
4. 切成路段，由軌跡幾何算出路段類別（暫定依曲率分級，細節於實作時定）

行程挑選原則：每條示範路線至少要有可以保留不進配速表的實際行程，作為 E2 Oracle 的實際行程時間；其餘行程涵蓋不同路段類別。目前 279 趟尚未盤點，能否滿足這個條件是 M0 要確認的事（§9.3、§13.1 風險 R1）。

### 最小資料契約 v0.2

狀態：**v0.2，Reviewed / Frozen for M1 Spike**（2026-11-14）。v0.1 的審查發現 DC-1 至 DC-10 與裁決見 §13.4。凍結之後的修改要先記入 Change Log。DC-10（配速的計算方法）保留為方法選擇事項，不阻擋 Spike。

契約只涵蓋 Spike 需要的四份資料，不是完整的 GIS Schema：不含路網拓樸、行政區、地形與完整軌跡點。

**共通規則。**

| 項目 | 規則 |
| --- | --- |
| 型別 | `string`、`int`、`float`、`datetime`、`enum`、`list` |
| 單位 | 寫在欄位名稱的字尾：`_m` 公尺、`_s` 秒、`_kmh` 公里／小時、`_deg_per_km` 每公里的度數。座標為 WGS84 十進位度 |
| 時間與時區 | `datetime` 一律是帶時區位移的 ISO 8601 字串，時區為 Asia/Taipei（`+08:00`）。GPX 的原始時間是 UTC，在 `ingest` 轉換。沒有時區位移的時間視為無效 |
| 缺值 | 以 `null` 表示「不知道或無法計算」，不得用 0、−1 或空字串代替。必填欄位不得為 `null`。使用端遇到 `null` 要往下傳遞為 UNKNOWN，不得補值（NFR4） |
| ID | `trip_id`：`T` 加三位數字，是去識別化的行程代號，不含日期資訊。`route_id`：`R` 加兩位數字，代表一條**有方向**的路線；反向騎視為另一條路線。`checkpoint_id`：`<route_id>-CP<兩位數字>`。`plan_id`：一次 ETA 計算的代號，由產生者指定，在同一批輸出中唯一 |
| 路段類別 | `seg_category` 是 `enum`：`C1`（低曲率）、`C2`（中曲率）、`C3`（高曲率）。分級門檻不在契約內，由 `category_scheme` 標示所用的分級版本 |
| 來源追溯 | 每份資料都帶自己的版本字串與上游的版本或代號，能從 ETA 追回配速表、路線目錄與行程 |
| 實體格式 | 只規範邏輯欄位。檔案格式（CSV、Parquet 或 JSON）在 Spike 決定，不得改變欄位名稱、型別與語意 |

**版控外的私有資料。** 以下資料含住家位置或完整的騎乘時間，一律不進版控，也不屬於這四份契約：

| 資料 | 內容 | 使用者 |
| --- | --- | --- |
| 原始 GPX | App 匯出的檔案 | `ingest` |
| 裁切後的軌跡 | `ingest` 裁掉頭尾後的軌跡點，格式由 `ingest` 內部決定 | `routes`（建立路線目錄的幾何） |
| 行程對照表 | 每趟的 `trip_id`、原始檔名、`trip_role`、`route_id`，由人工指定 | `ingest` |
| 私有版衍生路段表 | 契約 1 加上 `start_time` | 內部分析、E2 Oracle |

**契約 1：Derived Segment Table（衍生路段表）。** 產生者 `ingest`；使用者 `pace`、E1 Lite、E2 Oracle。一列是一趟行程中的一個路段；主鍵（`trip_id`, `seg_index`）。不含經緯度（NFR2）。

這份表有兩個版本，列完全相同，只差 `start_time` 一欄：

- **公開版**進版控，不含任何日期與時間。E1 Lite 只使用公開版的欄位，所以結果可以由公開資料重現。
- **私有版**不進版控，多一欄 `start_time`，供內部分析與 E2 Oracle 取得實際的騎乘時間。

| 欄位 | 型別 | 必填 | 公開版 | 說明 |
| --- | --- | --- | --- | --- |
| `trip_id` | string | 是 | 有 | 行程代號 |
| `seg_index` | int | 是 | 有 | 路段在該行程中的順序，從 0 起算（裁掉頭尾之後），連續不跳號 |
| `trip_role` | enum | 是 | 有 | `pace`（用於配速表）或 `holdout`（保留給 E2 Oracle，不進配速表） |
| `route_id` | string | 否 | 有 | 這趟行程對應的示範路線，由行程對照表指定；`null` 表示不在路線目錄內 |
| `start_time` | datetime | 是 | **沒有** | 進入該路段的時間。只存在於私有版 |
| `length_m` | float | 是 | 有 | 路段長度，大於 0 |
| `moving_time_s` | float | 否 | 有 | 移動時間，不含停留；有值時必須大於 0。無法取得有效的移動時間時為 `null`，不得以 0 或其他數值代替 |
| `stopped_time_s` | float | 是 | 有 | 路段內的停留時間；沒有停留時為 0 |
| `curvature_deg_per_km` | float | 否 | 有 | 每公里的累計轉向角；`null` 表示點數不足，無法計算 |
| `seg_category` | enum | 否 | 有 | 路段類別；`null` 表示無法分類 |
| `quality` | enum | 是 | 有 | `ok`、`suspect`（有移動時間但仍有疑慮，例如 GPS 中斷）或 `invalid`（沒有有效的移動時間） |
| `category_scheme` | string | 是 | 有 | 分級版本 |
| `ingest_version` | string | 是 | 有 | 產生這一列的 `ingest` 版本 |

不變條件：

1. 同一個 `trip_id` 的所有列，`trip_role` 與 `route_id` 相同。
2. 一份衍生路段表只有一個 `ingest_version` 與一個 `category_scheme`。
3. `quality` 為 `invalid` 時 `moving_time_s` 必為 `null`，反之亦然；`quality` 為 `ok` 或 `suspect` 時 `moving_time_s` 大於 0。
4. 只有 `quality` 為 `ok`、`seg_category` 不是 `null`、`trip_role` 為 `pace` 的列可以進配速表。
5. 公開版與私有版的列一一對應，共同欄位的值相同。

**契約 2：Route Catalog（路線目錄）。** 產生者 `routes`；使用者 `pace`、`sources`、Planner。包含三種紀錄。幾何取自版控外的裁切後軌跡；目錄本身只保留路段終點的座標，起訖已裁掉住家附近的路段。

路線（主鍵 `route_id`）：

| 欄位 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `route_id` | string | 是 | 路線代號 |
| `name` | string | 是 | 顯示名稱 |
| `n_segments` | int | 是 | 路段數，大於 0 |
| `total_length_m` | float | 是 | 路線總長，和最後一個路段的 `cum_length_m` 是同一個計算結果 |
| `source_trip_id` | string | 是 | 路線幾何取自哪一趟行程 |
| `category_scheme` | string | 是 | 分級版本 |
| `catalog_version` | string | 是 | 路線目錄的版本 |

路線路段（主鍵（`route_id`, `seg_index`））：

| 欄位 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `route_id` | string | 是 | 所屬路線 |
| `seg_index` | int | 是 | 路段順序，從 0 到 `n_segments` − 1，連續不跳號 |
| `length_m` | float | 是 | 路段長度，大於 0 |
| `cum_length_m` | float | 是 | 從路線起點到這個路段終點的累計距離，隨 `seg_index` 遞增 |
| `seg_category` | enum | 是 | 路段類別；路線目錄不允許 `null` |
| `end_lat`、`end_lon` | float | 是 | 路段終點的座標 |

檢查點（主鍵 `checkpoint_id`）：

| 欄位 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `checkpoint_id` | string | 是 | 檢查點代號 |
| `route_id` | string | 是 | 所屬路線 |
| `kind` | enum | 是 | `start`、`fuel_station`、`waypoint`、`end` |
| `after_seg_count` | int | 是 | 抵達這個檢查點之前已經完成的路段數。起點為 0，終點為 `n_segments`；值為 c 的檢查點位在路段 c − 1 的終點 |
| `name` | string | 否 | 顯示名稱 |
| `station_ref` | string | 視 `kind` | 加油站快照中的站代號。`kind` 為 `fuel_station` 時必填，其他情況必為 `null`。加油站資料本身不在本契約內 |

不變條件：

1. 每條路線恰有一個 `start`（`after_seg_count` 為 0）與一個 `end`（`after_seg_count` 等於 `n_segments`）。
2. 所有檢查點的 `after_seg_count` 介於 0 與 `n_segments` 之間。檢查點以整數定位，不以距離的相等比對定位。
3. 同一個位置可以有多個檢查點（例如起點同時是加油站），以 `checkpoint_id` 區分。

**契約 3：Pace Table（配速表）。** 產生者 `pace`；使用者 ETA 計算、E1 Lite。一份配速表是一筆表頭加上每個路段類別一筆紀錄。

表頭（主鍵 `pace_version`）：

| 欄位 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `pace_version` | string | 是 | 配速表的版本 |
| `method` | string | 是 | 配速的計算方法。v0.2 固定為 `median_unweighted`：路段移動速度（`length_m` ÷ `moving_time_s`，換算為 km/h）的中位數，不加權。改用其他方法要先記入 Change Log（DC-10） |
| `category_scheme` | string | 是 | 分級版本 |
| `ingest_version` | string | 是 | 上游衍生路段表的版本 |
| `min_segments` | int | 是 | 產生配速所需的最少路段數 |
| `n_trips` | int | 是 | 用到的行程數 |
| `trip_ids` | list of string | 是 | 建表用到的行程 |
| `built_at` | datetime | 是 | 建表時間 |

類別紀錄（主鍵（`pace_version`, `seg_category`））：

| 欄位 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `pace_version` | string | 是 | 所屬配速表 |
| `seg_category` | enum | 是 | 路段類別 |
| `speed_kmh` | float | 否 | 依 `method` 算出的配速，大於 0。`null` 表示該類別的路段數低於 `min_segments`，不得用其他類別的值代替 |
| `n_segments` | int | 是 | 用到的路段數 |

不變條件：

1. 每個 `seg_category`（`C1`、`C2`、`C3`）恰有一筆類別紀錄，沒有資料的類別也要有，`speed_kmh` 為 `null`。
2. `trip_ids` 只能是 `trip_role` 為 `pace` 的行程，不得包含 `holdout`；`n_trips` 等於 `trip_ids` 的個數。
3. 只使用符合契約 1 不變條件 4 的列。

**契約 4：ETA Output（ETA 輸出）。** 產生者 `pace`；使用者 `sources`、Validator、介面。一次計算（一個 `plan_id`）產生一筆表頭與每個路段一列。

表頭（主鍵 `plan_id`）：

| 欄位 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `plan_id` | string | 是 | 這次計算的代號 |
| `route_id` | string | 是 | 路線代號 |
| `departure_time` | datetime | 是 | 出發時間，也是起點檢查點的抵達時間 |
| `status` | enum | 是 | `ok` 或 `unknown` |
| `unknown_reason` | string | 視 `status` | `status` 為 `unknown` 時必填，例如路線上有路段類別沒有配速；`status` 為 `ok` 時必為 `null` |
| `margin_coeff` | float | 是 | 餘裕係數，沒有單位，不小於 0；數值不在契約內（§6.1） |
| `breaks` | list | 是 | 排定的休息，每筆含 `after_checkpoint_id` 與 `duration_s`；沒有休息時為空的 list |
| `pace_version` | string | 是 | 使用的配速表版本 |
| `catalog_version` | string | 是 | 使用的路線目錄版本 |
| `computed_at` | datetime | 是 | 計算時間 |

每個路段一列（主鍵（`plan_id`, `seg_index`））：

| 欄位 | 型別 | 必填 | 說明 |
| --- | --- | --- | --- |
| `plan_id` | string | 是 | 所屬的計算 |
| `seg_index` | int | 是 | 路段順序，對應路線路段的 `seg_index` |
| `typ_seg_time_s` | float | 否 | 這個路段的典型移動時間 |
| `break_time_s` | float | 是 | 進入這個路段之前已排定的休息時間累計；沒有休息時為 0 |
| `eta_typ` | datetime | 否 | 抵達路段終點的典型時間：`departure_time` + 累計的 `typ_seg_time_s` + `break_time_s` |
| `eta_safe` | datetime | 否 | 保守估計：`eta_typ` + `margin_coeff` × 累計的 `typ_seg_time_s`。不是 P90 |

**檢查點、休息與 ETA 的關聯（不變條件）。** 以下 n 是路線的 `n_segments`，c 是檢查點的 `after_seg_count`。

1. 每個 `plan_id` 恰有 n 列，`seg_index` 從 0 到 n − 1，不論 `status` 為何。
2. 休息的 `after_checkpoint_id` 必須是同一條路線的檢查點，而且 0 < c < n：起點與終點不排休息。`duration_s` 大於 0，同一個檢查點最多一筆休息。
3. 路段 k 的 `break_time_s` 等於所有 c ≤ k 的休息的 `duration_s` 總和。休息發生在抵達檢查點之後，所以只延後 `seg_index` ≥ c 的路段。
4. 檢查點的抵達時間：c 為 0 時是 `departure_time`；其他情況取 `seg_index` 等於 c − 1 那一列的 `eta_typ` 與 `eta_safe`。這個時間不含在該檢查點本身的休息。
5. `status` 為 `ok` 時，`eta_typ` 隨 `seg_index` 不遞減，而且每一列的 `eta_safe` 不早於 `eta_typ`。
6. `status` 為 `unknown` 時，所有列的 `typ_seg_time_s`、`eta_typ`、`eta_safe` 都是 `null`，不輸出部分估算的時間；`break_time_s` 仍照填。
7. 路線上任一路段的類別在配速表中 `speed_kmh` 為 `null` 時，`status` 必為 `unknown`。

**ID 關聯。**

| 來源欄位 | 指向 |
| --- | --- |
| 衍生路段表的 `route_id` | 路線的 `route_id` |
| 路線的 `source_trip_id`、配速表的 `trip_ids` | 衍生路段表的 `trip_id` |
| 檢查點的 `route_id`、路線路段的 `route_id` | 路線的 `route_id` |
| ETA 表頭的 `route_id` 與 `catalog_version` | 路線與路線目錄的版本 |
| ETA 表頭的 `pace_version` | 配速表的表頭 |
| ETA 路段列的 `plan_id` | ETA 表頭 |
| ETA 路段列的 `seg_index` | 同一條路線的路線路段 |
| ETA `breaks` 的 `after_checkpoint_id` | 同一條路線的檢查點 |

## 6. AI / Analytics

### 6.1 配速、ETA 與安全餘裕

- **配速表。** 以配速表使用的行程，算出每個路段類別的移動速度中位數。這是「基礎配速分析」，不是迴歸或分位數模型。
- **路段時間。** 路段典型時間 = 路段長度 ÷ 該類別的配速。
- **抵達時間。** `ETA_typ` 在第 k 點 = 出發時間 + 前 k 段典型時間總和 + 已排定的休息時間。時間以**移動時間加上排定的休息時間**計算；休息時間來自騎士設定檔或騎士當次指定，不由模型預測。
- **安全餘裕。** `ETA_safe` = `ETA_typ` + 餘裕；餘裕 = 餘裕係數 × 已騎乘的典型時間。餘裕係數是設定值，暫定在 E1 Lite 完成後依留一趟驗證的誤差決定，定案後寫進本節。

用語限制：`ETA_safe` 是**加了安全餘裕的保守估計**，不是 P90，也沒有經過 conformal 校正。文件、介面、簡報與報告都不得稱它為 P90、分位數或有覆蓋率保證的區間。E1 Lite 只會報告「實際時間落在保守估計內的趟數」這個描述性數字。

| 任務 | MVP 方法 | Baseline | 指標 |
| --- | --- | --- | --- |
| 路段與整趟時間估計 | 依路段類別的個人配速表 | 整體平均移動速度（單一數字） | 整趟移動時間的 MAE、MAPE |
| 保守估計 | 典型估計＋安全餘裕 | — | 實際時間落在保守估計內的趟數（描述性） |
| 風險判定 | 透明規則（§4.2） | — | 由 E2 的封路題與資料缺失題檢查 |
| Agent 整體 | Planner＋工具＋Validator | 只用 LLM；LLM＋工具 | 見 §6.3 |

Should：多元迴歸與 LightGBM 作為 E1 Lite 的額外比較列。Won't：分位數損失的 P50／P90 模型與 conformal 校正。

### 6.2 E1 Lite：基本 ETA baseline 比較

問題：依路段類別的個人配速表，是否比單一平均速度更接近實際騎乘時間？

| 項目 | 設計 |
| --- | --- |
| 資料 | 15–30 趟代表性行程中，配速表使用的那一部分（保留給 E2 Oracle 的行程不參與） |
| 驗證方式 | 留一趟交叉驗證：每次拿掉一趟，用其餘行程建配速表，預測被拿掉那一趟 |
| 比較對象 | B0 整體平均移動速度；M1 個人配速表 |
| Should | 多元迴歸、LightGBM；固定示範路線的 Google Maps 預估時間（人工查詢並記錄查詢日期，不經 API） |
| 指標 | 整趟移動時間的 MAE、MAPE；實際時間落在保守估計內的趟數 |

待驗證的假設 H1：M1 的整趟 MAPE 低於 B0。

配速的計算方法（資料契約審查 DC-10）：先採用不加權的中位數。M1 Spike 可以用配速表使用的行程比較「不加權」與「依長度加權」；方法與設定在正式的 E1 Lite 驗證之前固定，之後不再更動。保留給 E2 Oracle 的行程（`holdout`）不得用來選方法或調整設定。E1 Lite 只使用公開版衍生路段表的欄位，所以結果可以由公開資料重現。

正式 E1 Lite 之前的資料範圍檢查（2026-11-14 使用者指示，**尚未執行**）：只用配速行程，檢查高速的直路路段是否屬於山路旅遊配速的適用範圍。若要排除資料，必須用一致、可重現的資料品質與適用範圍規則，並在看到任何 `holdout` 的誤差之前定案；不得依 `holdout` 的誤差挑選樣本。

驗收標準（判定實驗「做完」的條件，不是成效門檻）：

1. 至少 15 趟行程完成清理與切段，並有清單記錄每趟的用途（配速表或保留）。
2. B0 與 M1 都以留一趟交叉驗證跑完，結果表列出兩者的 MAE、MAPE 與趟數。
3. 一個指令可以重現結果表。
4. 結果不論是否支持 H1 都照實寫入 §11。

### 6.3 E2：Agent 可行性實驗

問題：加上確定性工具與獨立驗證後，計畫的可行性是否提高？（即核心研究問題）

| 組別 | 內容 |
| --- | --- |
| A1 LLM Only | 只有 LLM，沒有工具、知識庫與 Validator。不得取得或使用任何工具的數值 |
| A2 LLM + Tools | LLM 可呼叫工具與知識庫，並依工具輸出自行評估候選、決定出發時間、寫出整份計畫；沒有確定性的驗證與排序 |
| A3 LLM + Tools + Validator | 完整 MVP：主程式以工具輸出填入每個候選的數值，由確定性規則驗證並排序 |

三組使用同一個模型、同一組設定與同一份輸出格式（計畫狀態、出發時間、抵達終點時間、加油安排、風險、UNKNOWN 項目），才能用同一個標準評分。三組的差別只有表中列出的項目。說明文字中的數值在三組都要能追溯來源：A2、A3 追溯到工具輸出；A1 沒有工具輸出，它的數值只由 Oracle 的數字一致率評估。A2 與 A3 共用相同的候選集合、工具、資料快照與 Plan Schema。A3 相對於 A2 增加的是「驗證輔助的確定性決策流程」，也就是確定性的候選評估、規則判定與排序；實驗報告要這樣描述，不把效果全部歸因於 Validator 這一個元件。正式的 E2 由獨立的 Runner 執行，不依賴 Streamlit 介面。

**題庫（12–15 題）。** 都在 2–3 條示範路線上，變化日期、最晚抵達終點時間、出發油量與情境。每題標示類型：

| 類型 | 內容 | Oracle 的依據 |
| --- | --- | --- |
| 真實行程題 | 重現一趟保留的實際行程（同一路線、同一方向） | 該行程的實際騎乘時間，加上當日的民用暮光終與加油站營業時間 |
| 模擬情境題 | 人工設定的限制測試：封路、油量不足、日照不足、資料缺失 | 情境設定的條件（出發油量、封路事件、最晚抵達終點時間、缺漏的資料項目） |

標準答案記錄每題預期的計畫狀態（`FEASIBLE`、`CONDITIONAL` 或 `INFEASIBLE`）。題庫要同時有預期可行與預期不可行的題目；各類型與各預期狀態的題數在題庫凍結時記錄。

**Oracle。** 獨立性與凍結要求：

- Oracle 是獨立的腳本，不匯入 Planner、Validator 或任何工具（`pace`、`sources`）的程式碼。
- 不以 Validator 的規則 1–5 評分。完整 MVP 只會輸出通過自己規則的計畫，用同一套規則評分是循環驗證。
- 題庫、標準答案與外部資料快照（氣象署預報、民用暮光終、加油站）在執行任何一組之前凍結，三組讀同一份快照。
- 真實行程的實際騎乘時間來自保留行程，那些行程不進配速表。只有在路線、方向與時間定義（移動時間，或含休息的總時間）都和題目相容時，才用來評估時間誤差；不相容就記為不適用。
- 模擬情境題只檢查限制是否被滿足。模擬情境中的時間不是實測值，不得當成真實騎乘結果報告。

**指標。** 每一組對每一題的輸出先分成兩類：**提出計畫**（輸出狀態為 `FEASIBLE` 或 `CONDITIONAL`）與**拒答**（輸出 `INFEASIBLE`、回報不可行或拒絕規劃）。A1、A2 沒有 Validator，狀態由 LLM 在輸出格式中自行宣告。

分母的符號：N 是總題數；N_F 是標準答案預期可行（`FEASIBLE` 或 `CONDITIONAL`）的題數；N_I 是預期 `INFEASIBLE` 的題數；N = N_F + N_I。

| 指標 | 分子 | 分母 |
| --- | --- | --- |
| Valid Plan Yield（有效計畫產出率） | 預期可行的題目中，提出計畫且不違反任何 Oracle 事實的題數 | N_F |
| Correct Infeasibility / Refusal Rate（不可行情境正確拒答率） | 預期不可行的題目中，拒答的題數 | N_I |
| Over-refusal Rate（可行情境過度拒答率） | 預期可行的題目中，拒答的題數 | N_F |
| Oracle 違規率 | 提出計畫且違反任一 Oracle 事實的題數；對預期不可行的題目提出計畫也算違規 | 提出計畫的題數；為 0 時記為不適用，不記為 0% |
| 輸出狀態分布 | 輸出為 `FEASIBLE`、`CONDITIONAL`、拒答的題數，分開列 | N |
| UNKNOWN 處理正確率 | 資料缺失題中，明確標示 UNKNOWN 且沒有給出該項數值的題數 | 資料缺失題的題數 |
| 數字一致率 | 計畫中與 Oracle 一致的數字個數 | 計畫中可以對照 Oracle 的數字個數 |
| 抵達終點時間誤差 | 計畫的抵達終點時間與實際行程推得的抵達終點時間之差 | 只計算時間定義相容的真實行程題 |

Oracle 違規率的分母是提出計畫的題數，所以一組即使全部拒答，也不會得到很低的違規率。它必須和 Valid Plan Yield、Over-refusal Rate 一起呈現。Valid Plan Yield 另外拆成 `FEASIBLE` 與 `CONDITIONAL` 兩部分報告。

待驗證的假設 H2：A3 的 Valid Plan Yield 高於 A2 與 A1，提出計畫中的 Oracle 違規率低於 A2 與 A1，且 Over-refusal Rate 沒有因此明顯升高。

結果表把真實行程題與模擬情境題分開列。封路題使用**模擬事件**，報告中不得寫成系統偵測到真實封路。

**時程、Pilot 與預算。**

- E2 Oracle 的規格在 M2 啟動，不等到 M4。題目類型、標準答案格式、要凍結的資料快照清單與獨立性的檢查方式在 M2 完成初版；題庫內容、標準答案與資料快照在 M4 正式執行前凍結。
- Pilot 使用 3 題獨立的開發測試案例，三組各跑一次（3 題 × 3 組）。這 3 題不屬於正式的 12–15 題，結果不計入 E2。
- Pilot 可以用於 Smoke Test、模型選型、成本估算與實作除錯，也可以據此調整提示、工具與設定。模型選型不得使用正式的 E2 題庫。
- 正式的 E2 題庫與 Oracle 在執行正式評估之前獨立凍結，不得沿用 Pilot 的題目。凍結之後若再修改任何一組的提示、工具或設定，已跑的正式結果作廢，三組全部重跑。
- 公平比較條件：三組使用相同的模型 ID、effort、max_tokens、輸出格式、題庫、資料快照與重複次數。Claude 現行模型不接受自訂的取樣參數，所以沒有 temperature 可以固定。
- 預算依 §9.1：累計達 US$24 時提醒，達 US$30 時停止新的實驗呼叫。執行時以題為單位，同一題的三組都跑完才進下一題；因預算而停止時，只報告三組都跑完的題目，並寫明實際完成的題數。

驗收標準：

1. 題庫 12–15 題、標準答案（含每題的預期狀態）與外部資料快照在執行前凍結（有 commit 可查）。
2. 三組在同一模型與設定下跑完全部題目，每次執行的輸入、輸出與工具呼叫都留存。因預算停止而完成不到 12 題時，這一項視為未達成，照實記錄。
3. 結果表列出各組的每項指標，分子與分母都以題數呈現。題數少，不做統計顯著性的宣稱。
4. 結果不論是否支持 H2 都照實寫入 §11。
5. E2 Oracle 規格的初版在 M2 完成。
6. Pilot 在正式執行前完成，成本估算有紀錄；支出不超過已核准的預算。

## 7. Domain Knowledge

五個核心思維模式（詳見 Proposal 第 3 章）與它們在 MVP 中的落點：

| 思維模式 | MVP 中的落點 |
| --- | --- |
| 以最難的路段規劃，不看平均速度 | 配速表依路段類別估計；決策用保守估計 `ETA_safe` |
| 山區天氣看時間窗 | 天氣工具依預計抵達時段查詢 |
| 日光與騎乘時數是硬限制 | 驗證規則 1 |
| 補給看抵達時有沒有開 | 驗證規則 2 |
| 山區道路狀態是動態的 | 驗證規則 4；沒有事件來源時回報 UNKNOWN |

知識庫內容（最小集合）：氣象署預報與警特報說明、公路局行車資訊、騎乘安全資料、BMW 車系規格（油箱、油耗）。以關鍵字檢索，回答時附出處。向量檢索等進階做法為 Should。

## 8. Algorithm

```text
Algorithm 1 (MVP): Plan with Deterministic Tools and Independent Validation
Input : rider request Q (form fields and free text), rider profile U, route catalog RC,
        pace table PT, knowledge base KB
Output: plan with status in {FEASIBLE, CONDITIONAL}, per-rule results, citations and a search
        status in {COMPLETE, INCOMPLETE}; or an infeasibility report; or an output validation error

01: ctx ← PLANNER_UNDERSTAND(Q, U, KB)             ▷ LLM: intent, structured breaks, fuel strategy
02: if AMBIGUOUS(ctx) ≠ ∅ then return ASK_RIDER(AMBIGUOUS(ctx))   ▷ start fuel is mandatory
03: route ← SELECT_ROUTE(RC, ctx)                  ▷ fixed routes only; else return OUT_OF_SCOPE
04: D ← CANDIDATE_DEPARTURES(ctx)                  ▷ every 15 min, earliest departure .. last that can meet the deadline
05: replans ← 0 ; best ← ∅ ; V_all ← ∅ ; search ← COMPLETE
06: loop
07:     data ← PLANNER_ACQUIRE(route, ctx, D)       ▷ LLM plans the tool calls; results are batched and cached
08:     for each batch B of at most 40 candidates of D do   ▷ every batch is evaluated; D is never cut short
09:         for each d in B do
10:             E ← PACE_TOOL(route, d, PT, ctx.breaks)      ▷ ETA_typ and ETA_safe (not a P90)
11:             plan ← FILL_PLAN(d, E, data, ctx)             ▷ numbers copied from tool outputs
12:             V ← VALIDATE(plan)                            ▷ rules 1–4: PASS / FAIL / UNKNOWN
13:             s ← STATUS(V)     ▷ FEASIBLE: all PASS; CONDITIONAL: no FAIL, some UNKNOWN; else INFEASIBLE
14:             V_all ← V_all ∪ {(d, s, V)}
15:             if s ≠ INFEASIBLE and RANK(s, d) > RANK(best) then best ← (plan, s, V)
16:     if some candidate of D was not evaluated then search ← INCOMPLETE
17:     if best ≠ ∅ or replans = MAX_REPLANS then exit loop            ▷ MAX_REPLANS = 2
18:     next ← PLANNER_REPLAN(ctx, V_all)                               ▷ LLM: breaks and refuelling only
19:     if next is invalid or not materially different from ctx then exit loop
20:     ctx ← next ; replans ← replans + 1
21: if best = ∅ then return INFEASIBILITY_REPORT(V_all, ALTERNATIVES(ctx), search)
22: text ← PLANNER_EXPLAIN(best, KB)                                    ▷ LLM: explanation with citations
23: if not TRACEABLE(text) then text ← PLANNER_EXPLAIN(best, KB)        ▷ rule 5: one regeneration at most
24: if not TRACEABLE(text) then text ← TEMPLATE(best)                   ▷ fixed template built from structured fields
25: if not TRACEABLE(text) then return OUTPUT_VALIDATION_ERROR(best)    ▷ no status shown; no new search
26: return RENDER(best, text, V_all, search)       ▷ CONDITIONAL lists every UNKNOWN rule
```

- LLM 出現在第 01、07、18、22、23 行（以及第 02 行的追問）。候選迴圈（第 08–15 行）沒有 LLM：每個候選的數值、規則判定與排序都由確定性程式執行（G1 Grill 第 2 輪）。
- Planner 仍然是 Agent：理解需求並把休息與補給策略轉成結構化資料（第 01 行）；規劃並執行多步的工具呼叫，取得預報、暮光終、加油站與路況（第 07 行）；候選全部不可行時重新規劃（第 18 行）；為結果寫出附出處的說明（第 22 行）。
- 候選從最早可出發時間開始，每 15 分鐘一個，到仍有可能在期限內抵達的最後一個為止。每批最多評估 40 個，逐批評估到涵蓋整個範圍，不得靜默截斷。工具資料批次取得或快取。
- 搜尋狀態是 COMPLETE 或 INCOMPLETE，和計畫狀態分開（第 16 行）。INCOMPLETE 時不得宣稱推薦的候選是整個範圍內最晚的可行出發時間。
- `RANK` 是字典序比較：先比計畫狀態（`FEASIBLE` 高於 `CONDITIONAL`），狀態相同時出發時間較晚的候選較高。只要有任何 `FEASIBLE` 的候選，出發較晚的 `CONDITIONAL` 候選也不會被選中。`INFEASIBLE` 的候選不會成為 `best`（第 15 行）。這個排序回答的是「最晚幾點出發還來得及」。
- 沒有 `FEASIBLE` 但有 `CONDITIONAL` 時，第 26 行回傳條件式計畫，並列出每一條 UNKNOWN 的規則與騎士要自行確認的事項。沒有可用的候選時，第 21 行回報原因與替代方案；替代方案不自動執行，也不宣稱已驗證可行。
- 重新規劃：初次評估之後最多 2 次（第 17–20 行）。只能調整休息與加油安排，不得自動更改路線、日期或使用者的時間限制；新增的加油只能選擇有資料的有效檢查點。提不出合法且有實質變化的新安排時提前停止。
- 規則 1–4 在迴圈內逐候選判定並決定計畫狀態。規則 5 是最終輸出的強制關卡（第 23–25 行）：Planner 的說明沒通過時最多重新產生一次，仍沒通過就改用由結構化欄位組裝的固定模板，模板也要通過規則 5。沒通過的文字不顯示。最終通過後，計畫才維持規則 1–4 決定的狀態。模板也沒通過時回報輸出驗證錯誤：不把計畫標示為 `FEASIBLE` 或 `CONDITIONAL`，也不重新執行候選搜尋。內部保留規則 5 的失敗紀錄與最後的結果。
- 時間餘裕是 min（民用暮光終, 最晚抵達終點時間）− 終點的 `ETA_safe`。它只用來顯示，不是排序的依據；規則 1 通過就表示餘裕不小於 0。
- 出發油量是必填：沒有提供時不進入規劃，也不以滿油代替。油量與續航全部由工具計算；只有在計畫明確安排加滿且加油站可用時，補油後才視為滿油（§4.2）。
- E2 的 A2 組不執行第 10–15 行的確定性流程：LLM 依相同的候選集合與工具輸出自行評估並決策。A1 組只有 LLM，不呼叫任何工具。

排序與候選搜尋的測試規格（實作時必須有的測試，目前**尚未實作**）：

1. 兩個候選都是 `FEASIBLE`：選出發較晚的。
2. 較晚的候選是 `CONDITIONAL`、較早的是 `FEASIBLE`：選 `FEASIBLE` 的。
3. 沒有 `FEASIBLE`、有多個 `CONDITIONAL`：選其中出發最晚的，並列出 UNKNOWN 的規則。
4. 出發最晚的候選保守估計超過期限（規則 1 為 FAIL）：不被選中。
5. 全部 `INFEASIBLE`：`best` 為空，進入重新規劃或不可行報告。
6. 把候選的評估順序打亂，選到的仍是同一個。
7. 天氣規則為 UNKNOWN、另一條規則為 FAIL：該候選是 `INFEASIBLE`，不是 `CONDITIONAL`。
8. 暮光終為 UNKNOWN、保守估計超過最晚抵達終點時間：規則 1 是 FAIL。
9. 候選超過 40 個時分批評估，選到的候選和一次評估全部候選時相同。
10. 搜尋沒有完成時，搜尋狀態是 INCOMPLETE，和計畫狀態分開輸出，不出現「最晚的可行出發時間」的說法。
11. 重新規劃提出的安排不合法，或和前一輪沒有實質差異：提前停止，不再評估。
12. 重新規劃 2 次後仍然沒有可用的候選：回報不可行，不做第 3 次。
13. 說明文字沒通過規則 5：重新產生一次；仍沒通過改用固定模板；模板也沒通過時回報輸出驗證錯誤，計畫不標示為 `FEASIBLE` 或 `CONDITIONAL`，也不重新搜尋。
14. 沒通過規則 5 的文字不會出現在輸出裡；內部紀錄保留每一次的結果。

與 Proposal §4.8 Algorithm 1 的差異：三個專責 Agent 改為工具；`BUILD_ROUTE` 與 `SEGMENT_FEATURES` 改為從路線目錄選取（第 03 行）；P50／P90 改為典型與保守估計；油量檢查改為從出發油量逐段計算；LLM 的組裝移出候選迴圈，候選的數值、規則判定與排序由確定性程式執行（第 08–15 行）；驗證結果改為三值，候選依計畫狀態與出發時間排序；移除寫入騎士記憶。Proposal 的流程圖 [docs/figures/flowchart.png](docs/figures/flowchart.png) 是縮減前的版本。

Proposal 的 Algorithm 2（配速模型更新）在 MVP 簡化為 §5 的資料處理流程加上重建配速表，不訓練分位數模型，也不計算 conformal 校正量。

## 9. Implementation Mapping

### 9.1 模組對應

規劃中的程式結構。已建立的只有資料契約驗證、`ingest`／`routes`／`pace` 的 Spike 版、測試與 M0 Smoke Test，其餘**尚未建立**；實作時依此建立並更新本表：

| 模組 | 規劃位置 | 對應 | 範圍 |
| --- | --- | --- | --- |
| GPX 匯入、裁切、清理、切段 | `src/moto_copilot/ingest/`（Spike 版已建立，門檻都是暫定值） | FR2、NFR2、§5 | Must |
| 路線目錄 | `src/moto_copilot/routes/`（Spike 版已建立） | FR1、§5 | Must |
| 配速表、ETA、安全餘裕 | `src/moto_copilot/pace/`（Spike 版已建立，餘裕係數是暫定值） | FR3、§6.1 | Must |
| 資料工具：預報、暮光終、加油站與續航、路況事件 | `src/moto_copilot/sources/` | FR4、FR5、NFR4、NFR5 | Must |
| Planner（LLM 與工具呼叫迴圈） | `src/moto_copilot/planner/` | FR1、FR6、Architecture ③ | Must |
| Validator（規則 1–5） | `src/moto_copilot/validator/` | FR6、NFR1、§4.2 | Must |
| 知識庫 | `src/moto_copilot/kb/` | §7 | Must |
| Streamlit 介面（三個畫面） | `app/` | FR7、§9.6 | Must |
| E1 Lite | `experiments/e1_lite/` | §6.2、§11 | Must |
| E2（題庫、Oracle、三組執行） | `experiments/e2/` | §6.3、§11 | Must |
| 資料契約 v0.2 的 Schema 與驗證 | `src/moto_copilot/contracts/`（已建立） | §5 | Pre-Spec Spike 的準備，不是產品功能 |
| 測試 | `tests/`（已建立：契約測試，使用模擬 fixture） | — | Must |
| LLM Tool Calling Smoke Test | `experiments/llm_smoke_test/`（已建立） | PD-5、驗收條件 L2–L6 | M0 驗證用，不是產品程式 |

Proposal 階段規劃的 `features/`（地形、曲率、道路等級特徵）不建立；路段類別的計算放在 `pace/`。原本的 `agents/` 拆成 `planner/` 與 `validator/`。

技術選擇（暫定）：Python、pandas、Streamlit 1.67.0；LLM 使用 Claude，透過 Anthropic 官方的 Python SDK 呼叫，具體模型在 Smoke Test 之後選定。scikit-learn、statsmodels、LightGBM 只在做 Should 項目時加入。

**LLM 選型（PD-5，最晚 M2 決定）。** 模型在真實 API 的 Smoke Test 與開發情境評估之後選定；目前**尚未選定**，真實 API 測試的狀態是 NOT RUN（§13.4）。Smoke Test 使用假的工具與固定的少量提示，不連接真實資料。候選模型必須通過以下全部驗收條件：

| 編號 | 驗收條件 |
| --- | --- |
| L1 | 支援以 JSON Schema 定義的工具呼叫 |
| L2 | 每個測試提示都呼叫正確的工具，參數符合 Schema |
| L3 | 能完成至少兩步的連續工具呼叫，後一步使用前一步的工具輸出 |
| L4 | 最終輸出符合結構化計畫的格式（含計畫狀態與 UNKNOWN 項目） |
| L5 | 工具回傳 UNKNOWN 時，不自行補上數值 |
| L6 | 能處理繁體中文的問題與地名 |
| L7 | 可以固定模型 ID 與可設定的生成參數，讓 E2 三組使用同一組設定。Claude 現行模型不接受自訂的取樣參數（temperature 等），能固定的是模型 ID、effort 與 max_tokens |
| L8 | 依單價與預估用量粗估，Smoke Test 加上完整 E2（三組 × 12–15 題）的費用在預算上限內 |

選型規則：候選要同時通過 L1–L8 與開發情境評估（P1–P4，見下表），在通過的候選中選費用最低者。選定的模型、測試日期與各條結果記錄在 Change Log。PD-5 最晚在 M2（11/30）完成，不阻擋 M1 的 Technical Spike。

**候選模型與測試設定（2026-11-14 定案）。** 供應商選定 Anthropic。

| 項目 | 設定 |
| --- | --- |
| 候選模型 | `claude-haiku-5-5`、`claude-sonnet-5-5`、`claude-opus-5-5`，由便宜到貴依序測試 |
| 測試範圍 | 至少測試 Haiku 與 Sonnet；Opus 只在前兩者都沒有達標時才測試 |
| Smoke 案例（L2–L6） | C1–C3，共 3 個，每個模型每個案例跑 3 次 |
| 開發情境（P1–P4） | D1–D3，共 3 個，每個模型各跑 3 次：P1 多步規劃（在候選出發時間中選出符合期限的最晚時間）、P2 工具結果的使用、P3 UNKNOWN 的處理、P4 輸出正確性（含計畫狀態）。情境使用假工具，和正式的 E2 題庫無關；不得用正式的 E2 題庫調整或選擇模型 |
| 生成參數 | effort 為 `medium`；max_tokens 為 4096，只在報告出現截斷（`truncated_runs` 大於 0）時才調高；不送取樣參數；thinking 維持模型預設 |
| 拒答的處理 | 不啟用伺服器端的 fallback：fallback 會讓另一個模型代答，而測試要量的是指定的那個模型。拒答記為該次失敗 |
| 支出控制 | 上限 US$3，由 `--max-usd` 指定。每次呼叫前以最壞情況預估，會超過上限就停止；每次呼叫後記錄實際的 Token 數與估算費用，並在整個多輪工具呼叫中累計 |
| 端點檢查 | 真實測試前檢查 `ANTHROPIC_BASE_URL`：不是 `https://api.anthropic.com` 就不執行。SDK 的 client 另外固定使用官方端點，憑證不會送到其他位置 |
| 沒有憑證時 | 狀態維持 NOT RUN，不發出任何呼叫，也不搜尋金鑰 |

**LLM API 預算（M0 決策，暫行）。**

- 整體上限暫列 US$30，涵蓋 Smoke Test 與 E2。這是預算上限，不是已核准的支出；實際支出要先經使用者核准。
- **已核准的部分：M0 Smoke Test 的實際 API 支出上限 US$3**，包含在 US$30 之內。不得超過；不足時回報，不自行追加。E2 的支出尚未核准。
- Smoke Test 的順序：先用 Mock Tools 做本地驗證（不呼叫 API），通過後才做少量的真實 API Tool Calling 測試。每次測試記錄模型、Token 數、估算費用與結果。
- 累計達 US$24 時提醒；達 US$30 時停止發出新的實驗呼叫。
- M3 開發與 Demo 期間的 LLM 費用不在這個上限內，另行估算與核准。
- L8 在 M0 只能粗估。完整 E2 的成本在 Pilot 之後重新估算（§6.3）；估算超過剩餘預算時先停下來，由使用者決定做法。若因此更換模型，要重做 Smoke Test，而且三組一起換。

### 9.2 模組依賴

| 模組 | 依賴 | 限制 |
| --- | --- | --- |
| `ingest` | 原始 GPX（版控外） | — |
| `routes` | `ingest` 的衍生路段表 | — |
| `pace` | `ingest`、`routes` | — |
| `sources` | `routes`、`pace`（需要抵達時間） | 失敗時回傳 UNKNOWN，不拋出預設值 |
| `validator` | 結構化計畫、工具輸出 | **不得匯入** `planner` 或任何 LLM 客戶端 |
| `planner` | `pace`、`sources`、`kb`、`validator` 的結果 | 不能改寫 `validator` 的結果 |
| `kb` | 知識庫文件 | — |
| `app` | `planner`；凍結後的 UI 規範（§9.6） | 版面與元件依凍結的 Prototype，不另外增加互動 |
| `experiments/e1_lite` | `ingest`、`pace` | — |
| `experiments/e2` | `planner`（三組設定） | Oracle 腳本**不得匯入** `validator`、`planner`、`pace`、`sources` |

建置順序：`ingest` → `routes` → `pace` → `sources` → `validator` → `planner` → `app`；`kb` 可平行進行；E1 Lite 在 `pace` 之後，E2 在 `planner` 之後。UI Prototype 使用 Mock Data，不依賴任何 `src/` 模組；E1 Lite 與 E2 不依賴 `app` 與 Prototype。

### 9.3 實作里程碑（2026-11-14 至 2026-12-20）

以下是計畫。M0 進行中，其餘尚未開始。期末繳交期限尚未確認（PD-6）；內部目標是 2026-12-20 完成全部交付物。2026-12-23 只是依課程講義日期推算的第 16 週上課日，不是正式繳交期限，不得當成截止日使用。G1–G3 是 §9.6 開發流程的 Gate。

| 里程碑 | 期間 | 內容 | 完成條件 |
| --- | --- | --- | --- |
| M0 | 11/14–11/16 | **Scope／Data Contract／GPX Inventory。** 範圍定案（本文件）；最小資料契約 v0.2（§5）已審查並凍結；盤點 GPX、選定 2–3 條示範路線、匯出第一批行程；建立專案骨架；申請氣象署授權碼；LLM Smoke Test 的腳本與本地驗證（真實測試與選型最晚在 M2 完成，PD-5） | 資料契約通過審查（v0.2，已完成）；示範路線與行程清單確定，每條路線有可保留的實際行程 |
| G1 | 11/17–11/19 | Grill with Docs：釐清主要需求 | 主要需求釐清完成，結論寫回本文件。2026-11-14 已提前完成三輪，使用者簽核，狀態是 APPROVED / FROZEN |
| M1 | 11/17–11/23，與 G1–G3 並行 | **GPX／Route／Pace Spike（Pre-Spec Technical Spike）。** M1-A：`ingest`，有一趟有效的 GPX 就開始（目標 11/17–11/19）；M1-B：`routes`、`pace` 與 ETA，行程對照與樣本備妥後開始（目標 11/20–11/23）；以及相關的單元測試。只限這些項目，條件見下方 | 一條示範路線能算出典型與保守抵達時間；Spike 的產出符合資料契約 |
| G2 | 11/20–11/22 | UI/UX Prototype（§9.6） | 三個畫面可操作，三份 UI 文件完成。**2026-11-15 完成** |
| G3 | 11/23 | Prototype Review / Freeze | 專題負責人審過並凍結；最晚不得晚於 11/30。**2026-11-15 APPROVED / FROZEN** |
| M2 | 11/24–11/30 | **Spec／Tickets、資料工具與 Validator。** Spec 與 Tickets（11/24 起）；`sources`（預報、暮光終、加油站與油量、路況情境）；UNKNOWN 處理；`validator` 規則 1–4、計畫狀態與候選排序，含單元測試；**E2 Oracle 規格啟動**（§6.3）；LLM 選型最晚在 11/30 完成（PD-5，API 支出上限 US$3）；每條示範路線人工加入 1–2 個有來源的真實中途檢查點 | Spec 凍結、Tickets 建立；規則 1–4 對 PASS、FAIL、UNKNOWN 三種情況都有測試；E2 Oracle 規格的初版完成；LLM 選型有紀錄 |
| M3 | 12/1–12/7 | **Planner＋Streamlit End-to-End Demo。** `planner` 工具呼叫迴圈與重新規劃；規則 5；`kb`；Streamlit MVP 整合（依凍結的 UI 規範） | 一條示範路線從 Trip Planner 到 Validation & Replanning 跑通 |
| M4 | 12/8–12/13 | **E1 Lite／E2 Results Freeze。** E2 題庫、標準答案與資料快照凍結；正式執行前完成 Pilot（3 題開發案例 × 3 組，可在 M3 進行）與成本估算；三組正式執行；E1 Lite 定稿；M3 準時才做 Should 項目 | E1 Lite 與 E2 的結果表完成並凍結；12/13 功能凍結 |
| M5 | 12/14–12/20 | **Final Handover。** README、DESIGN §10–§12、Conclusion、Final PPT、Demo（含 E4 的案例）與影片 | §9.5 的必繳項目齊全 |
| — | 12/21 之後 | 不排工作。能不能當緩衝取決於正式繳交期限（PD-6） | — |

**Pre-Spec Technical Spike（M1，已正式接受）。** 11/17–11/23 定義為 Pre-Spec Technical Spike，是「Spec 與 Tickets 之後才實作」的唯一例外。M1–M5 的既定里程碑不因 Spike 延後。

- 允許先行：GPX ingestion（`ingest`）、route catalog（`routes`）、基礎配速與 ETA（`pace`），以及這三者的單元測試。以留一趟驗證檢查配速表屬於測試，結果只作技術驗證，不是 E1 Lite 的正式結果。
- 不允許先行：`planner`、`validator`、正式的 Streamlit 開發（`app/`），以及 `sources`、`kb` 與 E2。這些一律在 Spec 與 Tickets 之後進行。
- 前提：Spike 的程式必須符合最小資料契約 v0.2（§5，Reviewed / Frozen for M1 Spike）。Spike 期間要改契約，先記入 Change Log。
- Grill、UI Prototype 與 Spike 的資料技術驗證可以平行進行。
- Spec 凍結後，Spike 的程式依 Spec 與 Tickets 檢視：符合的部分納入正式實作，不符合的部分返工並記入 Change Log。

**最小資料契約。** 四份契約（Derived Segment Table、Route Catalog、Pace Table、ETA Output）的 v0.2 寫在 §5 的「最小資料契約 v0.2」，狀態是 Reviewed / Frozen for M1 Spike。審查發現與裁決見 §13.4。

**M1 Entry Gate。** M1 分成兩個階段，不需要先匯出全部 15–30 趟才開始。

| 階段 | 可以開始的工作 | 進入條件 | 狀態（2026-11-14） |
| --- | --- | --- | --- |
| M1-A | `ingest` Spike | 資料契約 v0.2 已凍結；專案骨架已建立；至少一趟有效的 GPX 已放在版控外的資料夾 | 已達成。2026-11-14 收到 21 趟 GPX，`ingest` Spike 已執行，私有版與公開版的輸出都通過契約檢查 |
| M1-B | `routes`、`pace`、ETA | 版控外的行程對照表已建立（每趟的 `trip_id`、原始檔名、`trip_role`、`route_id`）；2–3 條示範路線已選定；配速用與保留用的行程樣本足夠 | 已達成（暫定）。2026-11-14 依規則指定：示範路線取多趟行程同方向重複騎過的路段，每條路線以日期最新的一趟為 `holdout`。M1 Review 接受兩條示範路線（其中一條只有兩趟重複騎乘）；原先的第三條是平直的高速移動路段，不適合山路旅遊的展示，不採用。Spike 的輸出通過契約檢查 |

完整的 M1 驗收仍要維持配速行程與 `holdout` 的分離：同一趟行程不得同時用於建立配速表與正式驗證。M1-A 的單趟 GPX 只用來確認 `ingest` 的輸出符合契約，不產生任何 E1 或 E2 的結果。

資料契約的 Schema 驗證在 `src/moto_copilot/contracts/`，測試在 `tests/test_contracts.py`，使用標示為模擬的 fixture；`ingest` 產生資料後可以直接用它驗證。

不屬於進入條件：LLM 選型（PD-5，期限 M2）、氣象署授權碼（M2 才需要）、UI Prototype（與 Spike 平行）。

**UI/UX Prototype Gate 與里程碑的相容性檢查。**

| 檢查項目 | 結果 | 處理 |
| --- | --- | --- |
| Gate 規定 11/24 起才進入 Implementation，但 M1 原訂 11/17–11/23 | 衝突已處理。若所有實作都等到 11/24，M1–M4 各延後約一週 | 已正式接受：M1 定義為 Pre-Spec Technical Spike，只限 `ingest`、`routes`、`pace` 與相關的單元測試，條件見上 |
| 11/17–11/23 同時進行 M1、Grill 與 Prototype | 負荷偏高：M1 約 4–5.5 人日，加上 Prototype 0.5–1 人日與 Grill | 這一週做不完時，延後的是 G2、G3，不是 M1。G3 最晚 11/30，因為 `app/` 到 12/1 才開始 |
| M2 同時有 Spec、Tickets、實作與 E2 Oracle 規格 | M2 是負荷最高的一週：約 4–5.5 人日的實作，加上 Spec 與 Tickets（約 1–1.5 人日）和 E2 Oracle 規格 | E2 Oracle 規格在 M2 只做到初版，題庫內容在 M4 凍結。G3 延後時，Spec 先涵蓋和 UI 無關的 `sources` 與規則邏輯，UI 相關部分在 G3 之後補上 |
| 12/21 之後 | 不能當成緩衝，因為正式繳交期限未確認 | 計畫以 12/20 為終點，沒有保留緩衝；期限若早於 12/20，M5 要提前（PD-6） |
| 12/1–12/7 的 Streamlit MVP 整合 | 與 M3 一致，沒有衝突 | — |
| E1 Lite、E2 | 不依賴 `app` 與 Prototype，M4 的時間沒有被佔用 | — |

### 9.4 工作量估計

「原始基準」是 Scope Reduction 時的估計（18.5–23 人日），保留作為比較基準。「修訂後」是 Design Review Fix 之後的估計。

| 項目 | 原始基準 | 修訂後 | 差異說明 |
| --- | --- | --- | --- |
| 專案骨架、資料契約、LLM Smoke Test 與選型 | 1 | 1 | 原為「待決事項定案與專案骨架」；待決事項已在設計審查處理，改放資料契約 |
| GPX 匯出、盤點、清理、切段；路線目錄 | 2–3 | 2–3 | — |
| 配速表、ETA、安全餘裕；E1 Lite | 2–2.5 | 2–2.5 | — |
| 資料工具與 UNKNOWN 處理 | 2.5–3 | 2.75–3.25 | 規則 2 改為從出發油量逐段計算，+0.25 |
| Planner 與 Validator | 3.5–4.5 | 3.5–4.5 | 計畫狀態排序在原區間內 |
| 最小知識庫 | 1 | 1 | — |
| Streamlit 介面 | 1.5–2 | 1–1.5 | 版面與元件在 Prototype 階段定案，移出 0.5 |
| UI/UX Prototype（含三份 UI 文件） | — | 0.5–1 | 新增；其中 0.5 由 Streamlit 介面移入 |
| E2（題庫、Oracle、三組執行、分析） | 2.5–3 | 2.75–3.25 | 標準答案的預期狀態與新增指標，+0.25 |
| 期末交付（README、DESIGN、Conclusion、PPT、影片） | 2.5–3 | 2.5–3 | — |
| **合計（Must）** | **18.5–23** | **19–24** | **+0.5 至 +1** |

增加的 0.5–1 人日來自三處：Prototype 淨增 0–0.5、油量檢查 0.25、E2 標準答案與指標 0.25。Must 的功能範圍沒有增加。

流程成本不在上表：Grill with Docs、Spec、Tickets 估計合計 1.5–2.5 人日（Grill 0.5–1、Spec 0.5–1、Tickets 0.5）。這是開發流程的成本，不是 Must 功能，但佔用同一段日曆時間。

Should 項目不在合計內，全部做約再加 5–7 人日（多元迴歸 0.5–1、LightGBM 1–1.5、TDX 1–1.5、氣象署警特報 0.5、進階地圖 1–1.5、進階知識檢索 1）。縮減前的完整設計估計約 33 人日（2026-11-14 的時程分析）。這些都是事前估計，不是實際工時。

### 9.5 期末必繳項目

課程規範的 Final Handover Package 不因 Scope Reduction 刪減。目前**全部尚未完成**。

| 必繳項目 | 最低要求 | 對應 |
| --- | --- | --- |
| GitHub | 完整原始碼、資料或資料來源、執行與測試方式 | 本 repo |
| README.md | 專題介紹、Installation、How to Run、Demo | README.md |
| DESIGN.md | Architecture 至 Limitations 各章 | 本文件 |
| Experiments | Dataset、Evaluation Metrics、Results、Comparison | §6.2、§6.3、§11 |
| Conclusion | Contributions、Limitations、Future Work | §12，期末補上 Contributions |
| Final PPT | 超過 20 頁 | M5 |
| Final Video | YouTube 專題簡報與 Demo，超過 10 分鐘 | M5 |

### 9.6 開發流程與 UI/UX Prototype Gate

正式開發流程：

```text
DESIGN → Grill with Docs → UI/UX Pro Max Prototype → Spec → Tickets → Implementation
```

Prototype 排在 Grill 的主要需求釐清完成之後、Spec 凍結之前。Implementation 在 Spec 與 Tickets 之後；唯一的例外是 M1 的 Pre-Spec Technical Spike（§9.3）。**Prototype 與下列檔案已經建立，並在 2026-11-15 的 G3 凍結。** 目前在 Spec 階段：`docs/spec/SPEC-001-plan-schema.md` 是供審查的草稿（Draft v0.1），尚未凍結；Tickets 尚未建立。

**範圍。** 單頁設計：Trip Planner 的輸入固定呈現在上方，Trip Result 與 Validation & Replanning 以分頁切換（G1 Grill 第 1 輪）。只涵蓋這三個畫面／狀態：

| 畫面 | 內容 |
| --- | --- |
| Trip Planner | 固定路線、日期、最早可出發時間、最晚抵達終點時間、出發油量（必填，以百分比輸入）、自然語言需求 |
| Trip Result | 建議出發時間、典型與保守 ETA、加油安排、天氣、資料來源 |
| Validation & Replanning | 逐條規則的 PASS／FAIL／UNKNOWN、計畫的 FEASIBLE／CONDITIONAL／INFEASIBLE、失敗原因與重新規劃結果 |

必須涵蓋資料缺失（UNKNOWN）與無可行解（全部 INFEASIBLE）的呈現。Prototype 只呈現 Must 範圍；地圖、下載、TDX、警特報等 Should 項目不放進 Prototype。

**設計要求。**

- 以已安裝的 `ui-ux-pro-max` Skill 建立 UI/UX Design System。
- Prototype 是可操作的原型，不是靜態圖片。
- 使用 Mock Data，不連接真實 API 或 LLM；Mock Data 依 NFR5 標示為模擬。
- 中途檢查點在 Prototype 階段使用明確標記為 simulated 的模擬檢查點，不得當成真實站點。真實的中途檢查點在 M2 人工加入，必須落在路段邊界並記錄來源。
- Streamlit 的可實作性在 Prototype 階段確認；查證過的元件與限制見 `docs/grill/g1-grill-input.md`。只使用官方支援的基礎元件，排除複雜互動。
- 只在按「規劃」時呼叫 Planner 與工具；欄位變更不自動重新規劃，舊結果標示為過期。規劃同步執行，以步驟文字顯示進度，不顯示虛構的百分比。
- 預設突出推薦的候選，其他候選放在可展開的唯讀表格。結果產生後不提供自由對話。
- Snapshot Mode 供 Demo 使用固定資料，畫面上要有明確的 simulated／snapshot 標籤。
- 狀態標籤是顏色加完整的文字，不得只以顏色區分。`CONDITIONAL` 顯示「有條件可行」，並在最上方列出 UNKNOWN 的待確認事項；人工確認不會讓規則變成 PASS。
- 搜尋狀態 COMPLETE／INCOMPLETE 另外顯示。無可行解時呈現的代表性候選不是有效的建議；替代方案不自動執行，也不宣稱已驗證可行。
- 畫面要呈現的內容與情境清單在 `docs/grill/g1-grill-input.md` 第 9 節。
- 以最終的 Streamlit MVP 做得出來為限制，不採用要改寫成 React 才能實現的互動。
- Validator 的三值狀態與來源證據是介面的核心，以獨立區塊呈現，不藏在一般對話文字裡。
- `ETA_safe` 在介面上稱為保守估計，不稱為 P90（§6.1）；降雨以自訂的三段顯示分類與高降雨機率提醒呈現，不稱為警特報，也不表示降雨強度（§4.2）。

**預計交付（Prototype 階段的產物）。**

| 檔案 | 內容 |
| --- | --- |
| `docs/ui/UI_DESIGN.md` | Design System、版面與元件規範 |
| `docs/ui/UI_FLOW.md` | 使用者操作與狀態轉換 |
| `docs/ui/UI_ACCEPTANCE.md` | UI 驗收條件、G2 的自我審查結果與 UI 工作量風險 |
| `prototype/index.html` | 可操作的原型（單一檔案、模擬資料、十四個情境） |

這四份產物已在 2026-11-15 完成（G2），並在同一天經過 G3 Audit 與專題負責人裁決：**G3 APPROVED / FROZEN**。Audit 的問題清單與裁決在 `docs/ui/G3_AUDIT_REPORT.md`；`prototype/g3-audit-check.js` 是保留下來的回歸檢查腳本。原型的資料與判定都是模擬的，不呼叫語言模型或任何 API。正式的 Streamlit 介面尚未實作。

**Gate 的通過條件（G3）。** 詳細條件由 `docs/ui/UI_ACCEPTANCE.md` 定義。最低條件：三個畫面可以用 Mock Data 操作；FEASIBLE、CONDITIONAL、INFEASIBLE 三種計畫狀態與 UNKNOWN 的說明都有對應的呈現；專題負責人審過。Spec 在凍結之後才定稿；之後的介面變更記入 Change Log。

時程見 §9.3，工作量見 §9.4。

## 10. How to Run

產品功能尚未實作。實作後在此補上：環境需求、API 金鑰設定（以環境變數提供，不進版控）、GPX 匯入步驟、啟動 Streamlit 介面、執行 E1 Lite、E2 與測試的指令。

目前可以執行的只有資料契約測試、契約驗證與 Smoke Test 的本地驗證，都不需要金鑰，也不讀取任何 GPX。在 repo 根目錄、Git Bash 下：

```bash
python -m venv .venv
.venv/Scripts/python.exe -m pip install jsonschema pytest
.venv/Scripts/python.exe -m pytest -q
PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json
.venv/Scripts/python.exe experiments/llm_smoke_test/smoke_test.py --self-test
```

UI 原型不需要安裝任何套件。用瀏覽器直接開啟 `prototype/index.html`，或啟動本機的靜態伺服器後開啟 `http://localhost:8765/`：

```bash
python -m http.server 8765 --bind 127.0.0.1 --directory prototype
```

## 11. Results

**尚無結果。** 下表是預計進行的實驗與 Proposal 原訂實驗的處置。

| 實驗 | 問題 | 狀態 |
| --- | --- | --- |
| E1 Lite | 個人配速表是否比單一平均速度更接近實際騎乘時間？ | 計畫中，未執行（§6.2） |
| E2 | 加上確定性工具與獨立驗證後，有效計畫產出率是否提高、Oracle 違規率是否下降，且沒有過度拒答？ | 計畫中，未執行（§6.3） |
| E3 風險規則的歷史封路回測 | — | 不做：沒有機器可讀的封路歷史資料。封路只以模擬情境出現在 E2 |
| E4 案例研究 | — | 不另立實驗（PD-2 定案）：示範路線的案例放在 Demo 中呈現，不產生獨立的實驗結果表 |

## 12. Limitations

| 限制 | 影響 | 對策 |
| --- | --- | --- |
| 只有一位騎士（n = 1） | 配速不能推廣到其他人 | 方法對任何匯入自己 GPX 的騎士適用，配速表各自建立 |
| 只支援 2–3 條固定示範路線 | 不能規劃任意路線 | 路線目錄可擴充；任意路線列入 Future Work |
| 保守估計是安全餘裕，不是校正過的分位數 | 沒有覆蓋率保證 | 文件與介面明確標示；只報告描述性數字 |
| 行程只有 15–30 趟、E2 只有 12–15 題 | 結果是描述性的，不能做統計推論 | 以題數與趟數呈現，不宣稱顯著性 |
| 沒有即時路況來源 | 真實日期的規則 4 為 UNKNOWN，計畫最多是 CONDITIONAL | 回答中要求騎士自行確認路況；TDX 為 Should |
| 封路只有模擬情境 | 不能宣稱偵測真實封路 | 模擬資料帶來源標記，結果分開報告 |
| 加油站是靜態快照，且不含台塑 | 營業時間可能過期；油量檢查偏保守 | 記錄快照日期；缺資料時回報 UNKNOWN |
| 油耗以 Rider Profile 的單一平均值計算 | 山路的實際油耗可能較高 | 以安全保留油量（暫定為油箱容量的 20%）吸收；不依路段類別調整 |
| 高降雨機率門檻（PoP ≥ 70%）與顯示分類是本專題自訂的暫行設定 | 沒有經過驗證；PoP 不代表降雨強度，也不等於氣象署的警特報 | 介面與報告明確標示為自訂的提醒 |
| 風險判定沒有正確答案 | 不能宣稱預測事故 | 規則透明；不做事故相關宣稱 |
| GPX 高度雜訊、車速跳點 | 速度誤差 | 車速平滑；MVP 不使用坡度 |
| GPX 含住家位置 | 隱私 | 原始檔不進版控；裁掉頭尾 |

Future Work（本次列為 Won't 的項目）：279 趟全量與完整地形路網特徵、分位數模型與 conformal 校正、多 Agent 分工、任意路線、歷史封路回測與每日資料收集、跨 Session 的騎士記憶、L3 即時串流與語音提醒。

## 13. Change Log

| 日期 | 內容 |
| --- | --- |
| 2026-10-31 | 建立 repo 與本文件（Proposal 階段）：需求、架構、資料、方法、演算法、規劃中的程式結構 |
| 2026-10-31 | 依獨立審查同步 Proposal：配速模型改預測移動時間（對數）、P50／P90 抵達時刻、E2 改以獨立 oracle 評分（§4.1、§6）；驗證規則 2、3 與 Algorithm 1 改為 Proposal 的版本（§4.2、§8） |
| 2026-11-11 | 依證據補強同步 Proposal：§1 加入 RETAIL、多 Agent 規劃系統的差異與不宣稱降低事故率；§6、§11 的 E2 加入逐一拿掉模組的消融 |
| 2026-11-14 | **Scope Reduction**：範圍由完整研究系統縮減為 Level 2 Lite 的 Agent-first MVP。全文改寫，詳見 §13.1 |
| 2026-11-14 | **Design Review Fix**：待決事項 PD-1 至 PD-6 定案或定出處理方式；四項設計修正（候選計畫排序、E2 Oracle、油量檢查、E2 指標）；加入 UI/UX Prototype Gate。詳見 §13.2 |
| 2026-11-14 | **M0 決策**：M1 定義為 Pre-Spec Technical Spike；天氣門檻、油量與 LLM 預算的暫行值；PD-6 維持未決，內部目標 12/20；E2 Oracle 規格提前到 M2 啟動。詳見 §13.3 |
| 2026-11-14 | **M0 執行**：最小資料契約 v0.1 寫入 §5（待審查）；LLM 供應商選定 Anthropic，Smoke Test 完成本地驗證與連接程式的離線檢查，真實 API 測試因執行環境沒有憑證而未執行，費用 US$0；Pilot 改用獨立的開發測試案例；M1 Spike 正式接受。詳見 §13.4 |
| 2026-11-14 | **Smoke Test 設定調整與資料契約審查**：至少測試 Haiku 與 Sonnet，Opus 只在兩者都未達標時測試；max_tokens 改為 4096；選型加入開發情境評估（P1–P4）；加入端點檢查與逐次呼叫的費用紀錄；PD-5 期限改為 M2（11/30）。真實 API 測試仍為 NOT RUN，費用 US$0。資料契約 v0.1 審查提出 DC-1 至 DC-10，尚未裁決。GPX 盤點因沒有已匯出的檔案而未進行。詳見 §9.1、§13.4 |
| 2026-11-14 | **資料契約 v0.2（Reviewed / Frozen for M1 Spike）**：DC-1 至 DC-8 全部套用；DC-9 採隱私優先，衍生路段表分成私有版與公開版；DC-10 維持不加權中位數並以 `method` 標示；ETA 輸出新增 `plan_id`；補上檢查點、休息與 ETA 的關聯不變條件。新增 M1 Entry Criteria。Smoke Test 的憑證檢查改為依 SDK 的規則尋找 `ant auth login` 的設定檔位置；真實 API 測試仍為 NOT RUN，費用 US$0。詳見 §5、§9.3、§13.4 |
| 2026-11-14 | **M1 Entry Gate 與專案骨架**：M1 拆成 M1-A（`ingest`）與 M1-B（`routes`、`pace`、ETA）；建立最小專案骨架、資料契約 v0.2 的 Schema 驗證與模擬 fixture，契約測試 68 項通過。這些測試只驗證契約與驗證程式，不是 E1 或 E2 的結果；真實 GPX 尚未提供。詳見 §9.1、§9.3、§10 |
| 2026-11-14 | **M1-A 開始**：收到 21 趟 GPX（放在 `data/bmw/`，已被 git 忽略）；建立 `ingest` 的 Spike 版，對全部行程執行後，私有版與公開版的衍生路段表都通過契約檢查。輸出只存在版控外的 `data/private/`。各行程的 `trip_role` 是暫定值，尚未建立配速表，沒有任何 E1 或 E2 的結果 |
| 2026-11-14 | **M1-B Spike**：依規則指定三條示範路線與保留行程（每條路線日期最新的一趟為 `holdout`），建立 `routes` 與 `pace` 的 Spike 版，產生路線目錄、配速表與 ETA 輸出，全部通過契約檢查。分級門檻取配速行程曲率的三分位數。依 DC-10 以配速行程比較兩種中位數，各類別的差異都在 0.2 km/h 以內，維持不加權。保留行程的騎乘時間沒有被讀取或比較；這不是 E1 或 E2 的結果。輸出只存在版控外的 `data/private/m1b/` |
| 2026-11-14 | **M1 Review**：示範路線定為兩條，原先的第三條不採用（只依配速行程與路線幾何判斷，是平直的高速移動路段）。保留行程與示範路線的幾何對齊已確認：方向一致，涵蓋整條路線；日後 Oracle 只計算相符路段的時間，不拿整趟行程對照。分級門檻、不加權中位數與餘裕係數維持暫定。私有的路線目錄與座標不公開，原始 GPX 與 `data/private/` 確認沒有被 Git 追蹤。測試共 100 項通過，屬於技術驗證紀錄，不是 E1 或 E2 的結果 |
| 2026-11-14 | **行程排除與 E1 前置檢查**：依使用者裁決，原第三條路線的保留行程標記為排除，不進配速表，也不是 E1／E2 的評估資料；排除記錄在版控外的行程清單，資料契約的 `trip_role` 不變。配速表沒有重建。新增正式 E1 Lite 之前的資料範圍檢查（§6.2），尚未執行 |
| 2026-11-14 | **G1 Grill 第 1 輪**：九項決議寫回本文件。期限改稱「最晚抵達終點時間」，一次規劃是一條單向路線；候選排序改為先比狀態、同狀態選最晚的出發時間，並新增排序的測試規格（§8）；計畫的數值由主程式從工具輸出填入，E2 三組的條件寫明（§6.3）；出發油量以百分比輸入；介面採單頁加分頁；中途檢查點在 M2 人工加入。決議的完整紀錄在 `docs/grill/g1-grill-input.md` 第 7 節。沒有新增 Must 範圍 |
| 2026-11-14 | **G1 Grill 第 2 輪**：十四項決議寫回本文件。Algorithm 1 重寫：LLM 的組裝移出候選迴圈，候選的數值、規則判定與排序由確定性程式執行，Planner 保留意圖理解、工具呼叫規劃、重新規劃與說明；候選每 15 分鐘一個，分批評估且不得截斷（§8）。E2 的 A2 由 LLM 依工具輸出自行決策，A3 使用確定性的驗證與排序，兩者共用候選、工具、快照與 Schema（§6.3）。規則 1 在期限已被違反時為 FAIL；規則 3 的範圍改為路線最後 20% 的距離（§4.2）。表單新增最早可出發時間。Plan Schema 的欄位細節留給 Spec。沒有新增 Must 範圍 |
| 2026-11-14 | **G1 Grill 第 3 輪與 Exit Review**：九項決議寫回本文件。重新規劃最多 2 次，沒有實質變化就提前停止；規則 5 成為最終輸出的強制關卡，說明沒通過時重新產生一次，再不行改用固定模板，模板也沒通過就回報輸出驗證錯誤；候選搜尋有獨立的 COMPLETE／INCOMPLETE 狀態（§4.2、§8）。介面的狀態標籤、UNKNOWN 的呈現與無可行解的畫面記在 Grill 文件。Exit Review 六項成立，G1 的狀態是 Ready for User Sign-off。交給 Spec 的 Plan Schema 欄位清單與交給 Prototype 的畫面清單在 `docs/grill/g1-grill-input.md` 第 8、9 節。沒有新增 Must 範圍，工作量估計不變 |
| 2026-11-14 | **G1 簽核**：使用者簽核 G1，狀態為 APPROVED / FROZEN，Grill 結束。無可行解時代表候選的選法定案：先取 FAIL 規則數最少的；都只違反規則 1 時取超過期限最少的，稱「最接近時間限制的候選」；其他情形以最晚的出發時間決勝，稱「代表性失敗候選」；任何 INFEASIBLE 的候選都不是有效的建議（`docs/grill/g1-grill-input.md` 第 7 節）。接著進入 G2 UI/UX Prototype |
| 2026-11-15 | **G2 UI/UX Prototype 完成**：以 `ui-ux-pro-max` Skill 產生 Design System 後取捨；`prototype/index.html` 涵蓋 Trip Planner、Trip Result、Validation & Replanning，以十四個模擬情境呈現 FEASIBLE、CONDITIONAL、INFEASIBLE、UNKNOWN、搜尋未完成、結果過期、Snapshot Mode、輸出驗證錯誤與重新規劃；三份文件在 `docs/ui/`。互動以 Streamlit 1.67.0 的標準元件為限，五項已知差異見 `docs/ui/UI_DESIGN.md` 第 8 節。Must 範圍沒有增加；UI 的工作量風險記為 R19。審查結果是製作者的自我審查，等待 G3 |
| 2026-11-15 | **G3 UI/UX Audit 與修正**（尚未裁決，G3 不視為通過）：以 `ui-ux-pro-max` Skill 的審查準則檢查原型，在 1280 與 375 像素實際開啟量測。修正 5 項 P1（模擬資料標成真實 API、Snapshot Mode 標籤和畫面上的結果矛盾、代表候選的名稱與選法說明不一致、手機寬度下標籤逐字換行、鍵盤選取候選後焦點遺失）與 9 項低風險的 P2。G1 決議與 Must 範圍沒有變更。問題清單、修改前後比較、G2 驗證紀錄的更正與待確認事項見 `docs/ui/G3_AUDIT_REPORT.md` |
| 2026-11-15 | **G3 裁決：APPROVED / FROZEN**。N1–N3 接受現狀（條件與來源證據維持展開、手機上數值卡片直排、表格橫向捲動）；N4 高降雨機率提醒維持琥珀色；N5 正式產品的 API 來源標籤用中性的灰色，實作時處理；N6 本地衍生資料與本地設定檔的來源類型交給 Spec，不得標成 API；N7 接受嚴格的代表候選命名規則。P2-1、P2-5 接受；`prototype/g3-audit-check.js` 保留為測試資產。不再開啟 UI/UX 的重新設計。接著進入 Spec 階段：先產生 Spec 供審查，尚不建立 Tickets，也不開始 Planner、Validator、Streamlit 的正式實作 |
| 2026-11-15 | **Spec 草稿（Draft v0.1，供審查）**：`docs/spec/SPEC-001-plan-schema.md` 把 G1 第 8 節的邏輯欄位清單定成欄位名稱與型別，固定規則的原因代碼與人工確認指引，並把來源證據的型別定為五種（真實 API、資料快照、模擬、本地衍生資料、本地設定檔；依 G3 裁決 N6）。Must 範圍沒有擴張。Spec 自己做的 12 項決定與 8 個待審查的問題列在文件第 10、11 節。尚未凍結；尚未建立 Tickets；Planner、Validator 與 Streamlit 的正式實作尚未開始 |

### 13.1 Scope Reduction 紀錄（2026-11-14）

**原因。** 距第 16 週報告約 5 週，完整設計估計約 33 人日，幾乎沒有餘裕。縮減後的 Must 範圍估計 18.5–23 人日，並把專題收斂到一個核心研究問題（§1）。本次只修改設計文件，沒有實作任何程式。

**本文件的實際修改。**

| 章節 | 修改 |
| --- | --- |
| 開頭、§1 | 狀態改為實作前；加入核心研究問題；說明與 Proposal 不一致時以本文件為準 |
| §2 | FR1–FR8 加上範圍與差異欄；NFR4 改為 UNKNOWN 處理；新增 NFR5；新增 Scope Matrix；Level 改為 L2 Lite |
| §3 | 新增 MVP 架構圖（Mermaid）；原圖保留供對照；新增四條設計原則 |
| §4 | 五個 Agent 改為 Planner＋工具＋Validator；驗證規則改為三值並定義計畫狀態 |
| §5 | 每個資料來源標示 MVP 範圍；新增路線目錄與路況情境檔 |
| §6 | 改為配速表與安全餘裕；新增 E1 Lite 與 E2 的設計與驗收標準 |
| §8 | Algorithm 1 改寫為 MVP 版本，列出與 Proposal 的差異 |
| §9 | 模組對應改版；新增模組依賴、里程碑、工作量估計、期末必繳項目 |
| §11、§12 | 實驗處置表；限制依 MVP 重寫；新增 Future Work |

**與 Proposal 的差異。**

| 項目 | Proposal 的承諾 | MVP | 理由 |
| --- | --- | --- | --- |
| Agent 架構 | 五個 Agent（規劃、配速、天氣、路況與補給、驗證） | 單一 Planner LLM＋確定性工具＋Validator | 配速、天氣、補給的工作本來就是確定性計算，不需要各自的 LLM；規劃與驗證分離的核心主張保留 |
| 配速 | LightGBM 分位數模型，P50／P90，conformal 校正整趟 P90 | 依路段類別的配速表，典型估計＋安全餘裕 | 分位數模型需要全量資料與完整特徵；15–30 趟不足以校正分位數 |
| 資料量與特徵 | 279 趟；DTM 坡度、OSM 道路等級、公路局幾何、歷史天氣 | 15–30 趟；由軌跡算出的簡單路段類別 | 逐趟手動匯出與地圖比對是最大的人工成本 |
| 路線 | 任意起訖與途經點 | 2–3 條固定示範路線 | 任意路線需要路網與地圖比對 |
| Google | Routes API 提供兩輪車路線與 baseline；Google Maps 儀表板 | 非必要依賴 | 兩輪車模式為 Beta，且需金鑰與帳單 |
| 路況 | TDX 即時路況 | 路況情境檔；TDX 為 Should | 封路沒有機器可讀的歷史資料；先確保缺資料時的行為正確 |
| API 失敗的處理 | 相關規則視為未通過 | 標示 UNKNOWN，計畫狀態為 CONDITIONAL（PD-1） | 沒有即時路況來源時，「視為未通過」會讓所有計畫不可行 |
| 續航檢查 | 相鄰補給點距離 ≤ 續航 ×（1 − 安全餘裕） | 從騎士的出發油量逐段計算剩餘油量（§4.2） | 原規則隱含滿油出發 |
| 天氣風險 | 抵達時段與大雨以上警特報重疊 | 氣象署預報加上自訂的高降雨機率門檻；警特報為 Should（PD-4） | 出發前的規劃看的是預報；自訂門檻不稱為官方標準 |
| E1 | 平均速度、速限、Google、MLR、LightGBM；GroupKFold 與時間外推；P90 覆蓋率 | E1 Lite：平均速度對配速表，留一趟交叉驗證 | 配合配速方法的縮減 |
| E2 | 20–30 題；只用 LLM、LLM＋知識庫、完整 Agent；另逐一拿掉配速、天氣、路況 | 12–15 題；LLM Only、LLM＋Tools、LLM＋Tools＋Validator | 三組直接對應核心研究問題；逐一拿掉模組的消融不做 |
| E3 | 以歷史封路紀錄回測風險規則 | 不做 | 沒有歷史資料 |
| E4 | 2–3 個案例與回測 | 併入 Demo，不另立實驗（PD-2） | 與 Demo 及 E1 Lite 重疊 |
| 騎士記憶 | 跨 session 記住偏好與歷史計畫 | 不做，改為靜態 Rider Profile（PD-3） | 不影響核心研究問題 |
| 介面 | 對話＋Google Maps 行程儀表板＋可下載計畫 | Streamlit 的三個畫面（§9.6） | 地圖與下載為 Should |
| L3 | 延伸，視進度 | 不做 | 時間 |

保留不變的部分：問題定位、依抵達時間查天氣與補給、規劃與驗證分離、E2 以獨立 Oracle 評分、不宣稱降低事故率、隱私處理、期末必繳項目。

**設計取捨。**

- 放棄預測方法的深度（分位數、校正），換取 Agent 可行性問題能完整做完並有對照實驗。
- 放棄任意路線，換取 Oracle 可以事先算好並凍結。
- 沒有即時路況時回報 UNKNOWN，代價是真實日期的計畫最多是 CONDITIONAL，而不是 FEASIBLE。
- Proposal「主要創新」中的 conformal 校正與多 Agent 架構不再成立；期末報告的貢獻要改以「確定性工具＋獨立驗證＋獨立 Oracle 評估」陳述，並說明範圍變更。

**待決事項（Pending Decisions）。** 已在 2026-11-14 的設計審查處理，並依 M0 決策（§13.3）更新，結果如下。

| 編號 | 問題 | 決議 | 狀態 |
| --- | --- | --- | --- |
| PD-1 | 規則為 UNKNOWN 時的計畫狀態 | 規則結果為 PASS／FAIL／UNKNOWN，計畫狀態為 FEASIBLE／CONDITIONAL／INFEASIBLE（§4.2） | 定案 |
| PD-2 | E4 案例研究是否保留 | 併入 Demo，不另立獨立實驗（§11） | 定案 |
| PD-3 | 跨 session 的騎士記憶 | 使用靜態 Rider Profile，不做跨 Session Memory（§4.1） | 定案 |
| PD-4 | 規則 3 的門檻與是否納入警特報 | 氣象署預報為 Must，警特報為 Should；PoP ≥ 70% 是專題自訂的高降雨機率提醒，不等同降雨強度或官方警特報（§4.2） | 定案；70% 與三段顯示分類是暫行值 |
| PD-5 | LLM 供應商與模型 | 真實 API 的 Smoke Test 與開發情境評估之後，依 §9.1 的選型規則選定；整體預算上限暫列 US$30，其中 Smoke Test 已核准 US$3 | 未決，最晚 M2（11/30）完成，不阻擋 M1；供應商定為 Anthropic，真實 API 測試為 NOT RUN（§13.4） |
| PD-6 | 期末繳交期限 | 待老師確認。內部以 2026-12-20 完成全部交付物；推算的 12/23 不當成正式截止日（§9.3） | 未決，待老師確認 |

同時確認為 Won't：E2 逐一拿掉模組的消融、歷史天氣作為配速特徵。

**剩餘風險。**

| 編號 | 風險 | 影響 | 因應 |
| --- | --- | --- | --- |
| R1 | 279 趟尚未盤點，不確定每條示範路線是否有足夠的實際行程可保留 | E2 的抵達終點時間誤差無法計算 | M0 先盤點；不足的路線該指標記為不適用 |
| R2 | E2 題數少，且 LLM 輸出有隨機性 | 結果不穩定 | 固定模型與設定、留存每次執行紀錄；是否重複執行在題庫定稿時決定 |
| R3 | 真實日期的規則 4 都是 UNKNOWN | Demo 中的計畫多為 CONDITIONAL | Demo 中說明原因；封路只用標示清楚的模擬情境展示 |
| R4 | 範圍與已繳交的 Proposal 不同 | 口頭提問時需要解釋 | 以本節的差異表說明；README 與簡報同步更新 |
| R5 | 氣象署預報的涵蓋期間與時間解析度有限 | 較遠日期的規則 3 為 UNKNOWN | 題庫與 Demo 的日期選在涵蓋期間內，另留資料缺失題 |
| R6 | Oracle 獨立性靠紀律維持 | 若共用程式碼，E2 會變成循環驗證 | §9.2 的匯入限制；題庫與 Oracle 在執行前凍結 |
| R7 | README、`architecture.png`、`flowchart.png` 與 Proposal 簡報仍是縮減前的內容 | 文件之間不一致 | 本次只改 DESIGN.md；README 與圖在後續變更同步 |
| R8 | 期末繳交期限未確認 | 里程碑可能要提前 | PD-6 |

### 13.2 Design Review Fix 紀錄（2026-11-14）

本輪是設計審查之後的修正，只修改本文件。沒有實作程式，沒有建立 UI Prototype 或其他文件，Must 的功能範圍沒有擴大。架構（單一 Planner LLM＋確定性工具＋獨立 Validator）、核心研究問題與核心實驗（E1 Lite、E2）都維持不變。

**四項設計修正。**

| 修正 | 內容 | 位置 |
| --- | --- | --- |
| Fix 1 候選計畫排序 | 先比計畫狀態，FEASIBLE 優先於 CONDITIONAL；狀態相同再比 SLACK；INFEASIBLE 不作為建議 | §4.2、§8 第 15–21 行 |
| Fix 2 E2 Oracle | 題目分為真實行程題與模擬情境題；Oracle 與 Planner、Validator、工具的程式碼分離；題庫、標準答案與資料快照在實驗前凍結 | §6.3、§9.2 |
| Fix 3 油量檢查 | 規則 2 改為從騎士的出發油量逐段扣除油耗，檢查抵達加油站前的剩餘油量、營業時間與補油後的續航；不預設滿油，缺資料為 UNKNOWN | §4.1、§4.2、§8 第 11 行 |
| Fix 4 E2 指標 | 新增 Valid Plan Yield、Correct Infeasibility / Refusal Rate、Over-refusal Rate 與輸出狀態分布；每項指標都定義分子與分母 | §6.3 |

**待決事項。** PD-1 至 PD-4 定案，PD-5、PD-6 定出處理方式，結果見 §13.1 的待決事項表。

**UI/UX Prototype Gate。** 開發流程改為 DESIGN → Grill with Docs → UI/UX Pro Max Prototype → Spec → Tickets → Implementation（§9.6）。Prototype 尚未建立。

**時程。** Gate 和 M1 有一項衝突，處理方式見 §9.3 的相容性檢查。M1–M5 的日期沒有延後；衝突以「M1 在 Spec 凍結前先行」的例外處理。M0 決策已有條件接受，並把 M1 定義為 Pre-Spec Technical Spike（§13.3）。

**工作量。** Must 由原始基準的 18.5–23 人日變為 19–24 人日，增加 0.5–1 人日。Grill、Spec、Tickets 的流程成本另計 1.5–2.5 人日。Should 由 4.5–6.5 變為 5–7 人日，因為加入氣象署警特報。明細見 §9.4。

**本輪新增的風險。**

| 編號 | 風險 | 影響 | 因應 |
| --- | --- | --- | --- |
| R9 | M1 在 Spec 凍結前先行 | Grill 的結論可能造成返工 | 先做最不受需求影響的 `ingest`；返工記入 Change Log |
| R10 | 11/17–11/23 同時有 M1、Grill 與 Prototype | 單週負荷偏高 | 延後 G2、G3（最晚 11/30），不延後 M1 |
| R11 | Prototype 的 0.5–1 人日包含三份 UI 文件 | 可能超出估計 | 只做三個畫面；超出時記錄實際人日 |
| R12 | 自訂的高降雨機率門檻（70%）與安全保留油量沒有驗證依據 | 判定可能過鬆或過嚴 | 明確標示為自訂的暫行設定；暫行值已由 M0 決策定出（§13.3） |
| R13 | Prototype 可能帶入 Must 以外的功能 | 範圍擴大 | Prototype 只呈現 Must 範圍（§9.6） |

**尚待確認。** 本輪列出的五項（M1 先行的例外、70% 門檻、補油與安全保留油量、LLM 預算上限、期末繳交期限）已由 M0 決策處理，結果見 §13.3。

### 13.3 M0 決策紀錄（2026-11-14）

本輪依 M0 最終決策做最小修訂，只修改本文件。沒有實作，沒有建立 Prototype 或 Tickets。Must 的功能範圍與工作量估計（19–24 人日）沒有改變。

| 決策 | 內容 | 位置 |
| --- | --- | --- |
| D1 M1 先行例外 | 有條件接受。11/17–11/23 定義為 Pre-Spec Technical Spike，只限 GPX ingestion、route catalog、基礎配速與 ETA 及相關測試；11/16 前固定最小資料契約；Planner、Validator 與正式的 Streamlit 開發仍依 Spec 與 Tickets | §9.3、§9.6 |
| D2 天氣門檻 | PoP ≥ 70% 是專題自訂的高降雨機率提醒；0–39%、40–69%、70–100% 是自訂顯示分類；PoP 不等同降雨強度或官方警特報；保留最後路段的保守驗證規則；缺資料為 UNKNOWN | §4.2 |
| D3 油量 | 出發油量必填；安全保留油量暫定為油箱容量的 20%，可調；只有計畫明確安排加滿且加油站可用時，補油後才視為滿油；計算全部由工具執行 | §4.1、§4.2、§8 |
| D4 LLM API 預算 | 上限暫列 US$30（Smoke Test＋E2），支出待核准；US$24 提醒，US$30 停止新的實驗呼叫；先做 3 題 × 3 組 Pilot 再估算完整 E2；三組維持相同模型與公平比較條件 | §6.3、§9.1 |
| D5 期限 | PD-6 維持未決；內部以 12/20 完成全部交付物；推算的 12/23 不當成正式截止日 | §9.3 |
| 里程碑 | M0–M5 依決策命名；E2 Oracle 規格提前到 M2 啟動 | §6.3、§9.3 |

**暫行值。** 以下數值是 M0 決定的暫行設定，都標示為專題自訂；之後調整要記入 Change Log：PoP 門檻 70% 與三段顯示分類、安全保留油量 20%、LLM 預算上限 US$30。

**修訂時一併處理的不一致。**

| 項目 | 原本的問題 | 處理 |
| --- | --- | --- |
| 12/21–12/22 的緩衝 | 緩衝的前提是 12/23 為截止日，和 D5 矛盾 | 移除緩衝，計畫以 12/20 為終點 |
| L8 與成本估算的時點 | L8 在 M0 就要判斷 E2 成本，但完整成本要等 Pilot | L8 改為依單價粗估；Pilot 之後重新估算 |
| 預算停止與公平比較 | 中途停止可能讓三組完成的題數不同 | 以題為單位執行，只報告三組都跑完的題目 |
| Pilot 與題庫凍結 | Pilot 若用來調整設定，會影響正式結果 | Pilot 取自已凍結的題庫，不用來調整；有修改就全部重跑 |
| 出發油量 | 上一輪允許缺出發油量時為 UNKNOWN，和「必須明確提供」不一致 | 改為必填，缺少時不進入規劃 |

**仍未解決。**

1. 開發與 Demo 期間的 LLM 呼叫不在 US$30 內，尚未編列預算。
2. Smoke Test 排在 M0（11/16 前），但支出要先經核准；未核准時 PD-5 的選型會延後。
3. M2 同時有 Spec、Tickets、資料工具、Validator 與 E2 Oracle 規格，是負荷最高的一週（§9.3）。
4. 期末繳交期限未確認；計畫沒有緩衝，期限若早於 12/20，M5 要提前（PD-6）。
5. README、`architecture.png`、`flowchart.png` 與 Proposal 簡報仍是縮減前的內容（R7）。

本節的 D1（有條件接受）、Pilot 的規則，以及「仍未解決」的第 1、2 項，已由 §13.4 更新。

### 13.4 M0 執行紀錄（2026-11-14）

**本輪決策。**

| 決策 | 內容 | 位置 |
| --- | --- | --- |
| LLM Smoke Test | 有條件核准：M0 的實際 API 支出上限 US$3，包含在整體 US$30 之內；先做本地驗證，再做少量的真實 API 測試；記錄模型、Token、估算費用與結果；不足時回報，不自行追加；M3 開發與 Demo 的費用另行估算與核准 | §9.1 |
| M1 Spike | 正式接受：11/17–11/23 先行 `ingest`、`routes`、`pace` 與相關的單元測試；Planner、Validator 與正式的 Streamlit 仍須經過 Spec 與 Tickets；M1–M5 不延後 | §9.3 |
| Data Contract | 四份最小資料契約 v0.1 寫入 §5；M1 Spike 開始前完成審查（之後已審查並更新為 v0.2） | §5 |
| E2 Pilot | 改用 3 題獨立的開發測試案例，不佔正式的 12–15 題；可用於 Smoke Test、成本估算與除錯；正式題庫與 Oracle 在正式評估前獨立凍結 | §6.3 |
| Scope Freeze | Must 維持 19–24 人日；保留 UI/UX Prototype Gate；不加入新的 Should；內部以 12/20 完成交付，正式期限待老師確認 | §2.3、§9 |

**Data Contract。** v0.2，**Reviewed / Frozen for M1 Spike**（§5）。分級門檻、`min_segments` 與 `margin_coeff` 的數值不在契約內，由 Spike 決定並以版本字串標示。

**Data Contract Review（2026-11-14）。** 對照使用端（`pace`、`sources`、Validator、E1 Lite、E2 Oracle）逐份檢查，對 v0.1 的發現如下。裁決見表後，§5 已更新為 v0.2。

| 編號 | 類型 | 發現 | 建議 |
| --- | --- | --- | --- |
| DC-1 | 缺陷 | 檢查點以浮點數 `cum_length_m` 對應路段，要求「等於」某一列的值；浮點數的相等比對不可靠 | 檢查點改用整數 `after_seg_count`（抵達前已完成的路段數，起點為 0） |
| DC-2 | 缺陷 | ETA 輸出的 `breaks` 也用浮點數 `after_cum_length_m` 定位 | 改用 `after_checkpoint_id` |
| DC-3 | 缺陷 | `moving_time_s` 沒有規定大於 0；配速是 `length_m` ÷ `moving_time_s`，等於 0 會除以零 | 規定大於 0；等於 0 的列標為 `suspect` |
| DC-4 | 缺陷 | `station_ref` 一律選填，但 `kind` 為 `fuel_station` 時沒有它就查不到營業時間 | `kind` 為 `fuel_station` 時必填 |
| DC-5 | 缺口 | 衍生路段表不含座標，但路線目錄需要路段終點座標；`routes` 實際上要讀 `ingest` 裁切後的軌跡，這個輸入不在四份契約內 | 明寫這個依賴，並註明該軌跡不進版控 |
| DC-6 | 缺口 | 行程的 `route_id` 由誰、依什麼規則指定，沒有定義 | v0.1 由人工在版控外的行程對照表指定 |
| DC-7 | 缺口 | 沒有寫不變條件 | 同一個 `trip_id` 的 `trip_role` 必須一致；一份衍生路段表只有一個 `ingest_version` 與 `category_scheme` |
| DC-8 | 結構 | 配速表的 `trip_ids`、`min_segments`、`built_at` 在每一列重複，而且 list 欄位不適合 CSV | 仿照 ETA 輸出，拆成一筆表頭與每個類別一列 |
| DC-9 | 待決定 | `start_time` 是絕對時間，公開後看得出騎士哪些日子不在家。E2 Oracle 需要實際時間，但那份資料可以只留在版控外 | 由使用者決定公開的衍生路段表保留完整時間，或只保留時段 |
| DC-10 | 待決定 | 配速取路段速度的中位數且不加權，長短路段的權重相同 | 留給 Spike 用資料比較「不加權」與「依長度加權」後決定 |

**裁決（2026-11-14，使用者）。**

| 項目 | 裁決 | 在 v0.2 的落點 |
| --- | --- | --- |
| DC-1 至 DC-8 | 全部接受，依建議修正 | 檢查點改用 `after_seg_count`；休息改用 `after_checkpoint_id`；`moving_time_s` 必須大於 0，無效路段的值為 `null`、`quality` 為 `invalid`，不進配速表；`station_ref` 在加油站時必填；路線目錄可以依賴版控外的裁切後軌跡；`route_id` 由版控外的行程對照表指定；補上不變條件；配速表拆成表頭與類別紀錄 |
| DC-9 | 隱私優先 | 衍生路段表分成私有版與公開版。私有版保留完整時間，供內部分析與 E2 Oracle 使用，不進版控；公開版不含日期與時間。公開資料不需要時段特徵，所以直接省略 |
| DC-10 | 先維持不加權的中位數 | 配速表的表頭以 `method` 標示方法。Spike 可以用配速行程比較兩種方法；正式 E1 驗證前固定，不得用 `holdout` 調整（§6.2）。這是方法選擇事項，不阻擋 Spike |
| 額外修正 | ETA 輸出新增 `plan_id` | 表頭加上 `plan_id`；路段列的主鍵改為（`plan_id`, `seg_index`）；保留 `route_id`、`departure_time`、`pace_version`、`catalog_version` 與 `unknown_reason`；檢查點、休息與 ETA 三者的關聯寫成不變條件 |

**LLM Smoke Test 紀錄。**

| 項目 | 結果 |
| --- | --- |
| 腳本 | `experiments/llm_smoke_test/smoke_test.py`。M0 驗證用，不是產品程式；工具輸出全部是模擬資料。執行環境是 repo 根目錄的 `.venv`（不進版控），已安裝 `anthropic` 2.8.0 與 `jsonschema` |
| 供應商與候選模型 | Anthropic；至少測試 `claude-haiku-5-5` 與 `claude-sonnet-5-5`，`claude-opus-5-5` 只在前兩者都沒有達標時測試。設定見 §9.1 |
| 本地驗證（Mock Tools，不呼叫 API） | 2026-11-14 通過。結果檔：`experiments/llm_smoke_test/results/local-validation-2026-11-14.json` |
| 本地驗證的內容 | 3 個 Smoke 案例（C1–C3）與 3 個開發情境（D1–D3）、3 個假工具，以腳本模擬的模型執行。正確行為在 L2–L6 與 P1–P4 的檢查全部通過；八種錯誤行為都被對應的檢查抓到，包含選錯工具、參數不符 Schema、沒有使用前一步的輸出、最終輸出不是指定格式、UNKNOWN 時自行補值、選錯出發時間、把不可行說成可行；預算保護在超過上限前停止，每次呼叫都有預估、實際 Token、費用與累計的紀錄 |
| Anthropic 連接程式 | 已撰寫，使用官方 SDK 與手動的工具呼叫迴圈。以假的 client 離線檢查通過：請求的欄位、訊息的角色交替、工具結果的回傳格式、候選模型的測試順序都正確；`ANTHROPIC_BASE_URL` 不是官方端點時會拒絕執行。這不是對真實 API 的測試 |
| 支援的驗證方式 | 腳本不強制要求 `ANTHROPIC_API_KEY`，憑證由 SDK 的官方流程解析：`ant auth login` 的設定檔（Windows 在 `%APPDATA%\Anthropic`）、環境變數 `ANTHROPIC_API_KEY`（或 repo 根目錄 `.env` 的同名項目）、`ANTHROPIC_AUTH_TOKEN`、`ANTHROPIC_PROFILE`。腳本只檢查憑證是否存在，不讀取也不輸出內容；錯誤紀錄只留錯誤類型。`ant` CLI 這條路徑依 SDK 原始碼確認，還沒有用真實的登入實測 |
| 真實 API 測試 | **NOT RUN**。執行環境沒有 Anthropic 的憑證；腳本在沒有憑證時不發出任何呼叫。目前環境的 `ANTHROPIC_BASE_URL` 是官方端點 |
| 事前成本估計 | Haiku 與 Sonnet 合計約 US$0.5；若還要測 Opus，再加約 US$1，合計約 US$1.5，在 US$3 之內。這是依 Token 用量假設算的粗估，不是實測 |
| 模型 | 無，沒有呼叫任何模型 |
| Token | 0 |
| 實際費用 | US$0；US$3 的上限沒有動用 |
| L1–L8 與 P1–P4 的判定 | 尚無。本地驗證只證明測試工具可用，不代表任何模型通過 |
| PD-5 | 維持未決 |

**M0 剩餘風險。**

| 編號 | 風險 | 影響 | 因應 |
| --- | --- | --- | --- |
| R14 | 真實 API Smoke Test 沒有 Anthropic 的憑證，狀態為 NOT RUN | PD-5 的選型還不能完成；期限是 M2（11/30），不阻擋 M1 | 憑證由使用者自行設定，不在對話中提供；候選模型與連接程式都已備妥，設定後即可在 US$3 內執行 |
| R15 | 資料契約的審查發現已裁決，契約已更新為 v0.2 並凍結 | 這項風險已解除；M1 仍受 M1-A、M1-B 的進入條件限制（§9.3） | Spike 期間的契約修改記入 Change Log |
| R16 | 示範路線只有兩條，其中一條只有兩趟重複騎乘；分級門檻、配速方法與餘裕係數都是暫定值；路段只依曲率分級，分不出快速道路與一般直路 | 樣本少，E1 Lite 與 E2 的結論只能是描述性的；直路類別混入高速行程，套到一般直路可能偏快 | 門檻與方法在正式 E1 前固定，只用配速行程；不新增道路分類功能；餘裕係數維持為待驗證的假設 |
| R17 | 氣象署授權碼尚未申請（專案骨架已建立） | M2 需要授權碼 | M2 開始前完成 |
| R18 | Smoke Test 與開發情境合計只有 6 個案例，各跑 3 次 | 對模型穩定性與規劃能力的判斷有限 | 開發情境涵蓋多步規劃與不可行的判定；M3 的 Pilot 再以真實的 Planner 檢查一次 |
| R19 | Streamlit 介面的估計是 1–1.5 人日，但原型顯示介面有 8 個畫面狀態，Trip Result 有 9 個區塊，Validation & Replanning 最多 8 個區塊 | M3 的介面整合可能超出估計 | 不調整 Must 範圍與 19–24 人日的總量；超出時依 `docs/ui/UI_ACCEPTANCE.md` 第 6 節的順序簡化，並記錄實際人日；簡化的順序由專題負責人在 G3 決定 |
