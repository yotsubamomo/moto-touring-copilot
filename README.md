# Moto Touring Copilot 重機旅遊規劃顧問

用騎士自己的歷史行程學出個人配速，結合中央氣象署天氣、交通部路況、地形與加油站資料，由多個 Agent 分工規劃、互相驗證，回答「照我的騎法，幾點出發才能在天黑前回家、中途哪裡加油、哪一段有風險」。

> 物聯網應用與資料分析（AIoT-DA）期末專題。目前為 **Proposal 階段**，尚未實作。

## 文件

| 文件 | 說明 |
| --- | --- |
| [DESIGN.md](DESIGN.md) | 系統設計：需求、架構、元件、資料、方法、演算法、規劃中的程式結構 |
| [Proposal（PDF）](docs/proposal/proposal.pdf) | 完整提案：Abstract、Introduction、Related Work、Deep Research、Proposed Scheme |
| [Proposal 簡報（PPTX）](docs/proposal/proposal-slides.pptx) | 16 頁，逐字稿在備忘稿 |
| Proposal 簡報影片 | YouTube（上傳後補上連結） |

## 系統概要

![系統架構](docs/figures/architecture.png)

- **個人配速模型：** 以騎士自己的 GPX 行程訓練，逐段預測騎乘時間並輸出 P50 / P90 區間，和 Google Maps 兩輪車預估時間比較。
- **依抵達時間查風險：** 天氣、日落、路況與加油站營業時間，都用「預計抵達該路段的時間」查詢。
- **規劃與驗證分離：** LLM 負責理解與規劃，驗證 Agent 以確定性規則檢查日照、續航、天氣與路況，不通過就重新規劃。

## 安裝與執行

尚未實作。實作後會在這裡與 [DESIGN.md §10](DESIGN.md#10-how-to-run) 補上安裝、設定與執行方式。

## 資料與隱私

騎士的原始 GPX 含住家等位置資訊，**不放進本 repo**（見 `.gitignore`）。公開的只會是裁掉起訖附近路段後的衍生資料。外部 API 金鑰以環境變數提供，不進版控。

## 選題與 Proposal 原稿

選題過程、範圍決策與 Proposal 的 Markdown 原稿在課程 repo：[yotsubamomo/aiot-classwork](https://github.com/yotsubamomo/aiot-classwork) 的 `final_project/`。

## AI 使用

本專題依課程規範使用 AI 工具輔助研究、撰寫與製作，使用方式與驗證說明見 Proposal 附錄 A。
