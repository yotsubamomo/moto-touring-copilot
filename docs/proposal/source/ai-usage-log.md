# AI 使用紀錄（提示詞摘要）

> 本專題 Proposal 階段使用 Claude Code（Claude Opus 5.5）的主要指令紀錄。依時間排列；組員的指令以原文或摘要記錄，Claude 派給子代理的研究指令以摘要記錄。完整對話可由 Claude Code 匯出。
> 本檔不放進 Proposal 文件；Proposal 附錄 A 有摘要說明。

## 2026-10-24：選題

| 組員的指令 | Claude 的工作 |
| --- | --- |
| 「final project 的資料可以先看一下」 | 讀取 `final_project/docs/` 的作業規範、課程專題說明、寫作方法、架構圖 |
| 「先一起討論 final project 要做什麼領域的 Agent」 | 依選題條件提出候選方向 |
| 提供工作背景、可用硬體、時間預算 | 依背景調整候選方向，推薦車用相近的題目 |
| 「老師的題目架構是 1~10 個方向，先整理成 .md，每一項要決定做到什麼程度」 | 寫成 `doc/brief/architecture-scope.md` |
| 「把 A 電池健康和 H 車輛能耗偵探放進短名單深入比較」 | 派兩個子代理分別研究，抽查關鍵事實後寫成 `doc/brief/shortlist-a-vs-h.md` |
| 「先驗看看」 | 下載 VED 資料集，以多元迴歸做流程驗證，寫成 `doc/brief/spike-ved.md` |

## 2026-10-25：改從手邊資產出發，定案

| 組員的指令 | Claude 的工作 |
| --- | --- |
| 「先回到第一項，看我們手邊擁有什麼東西，再去延伸」 | 盤點資產，提出 D1 重機旅遊規劃顧問，寫成 `doc/brief/asset-inventory.md` |
| 「幫我比較 D1 和 H」 | 派子代理研究 D1，抽查後寫成 `doc/brief/compare-d1-vs-h.md` |
| 「⑧ 定案 D1，依它排 ①–⑦、⑩ 的檔位」 | 填入建議檔位 |
| 「③ 使用延伸，⑦ 用標準但要含 Google Map，其他照建議」 | 更新範圍文件，寫給組員的摘要 `doc/brief/project-summary.md` |

## 2026-10-31：Proposal 與簡報

| 組員的指令 | Claude 的工作 |
| --- | --- |
| 決定：中文為主、另開新 repo、Word + PDF、Proposal 階段不做 GPX 驗證 | 寫成 `doc/brief/proposal-plan.md` |
| 「開始起草」 | 派三個子代理平行起草，並要求每個數字與引用都要開啟原始頁面查證、無法查證就刪除或標註：(1) Introduction 證據查證與 A–F 草稿；(2) Related Work（一半 AI、一半領域知識、Article Summary Table、Research Gap）；(3) Deep Research（5 思維模式、3 爭論、10 問題）。完成後抽查關鍵引用 |
| 「接著起草」 | Claude 撰寫 Proposed Scheme（架構、多 Agent、數學模型、流程圖、Pseudocode、評估計畫） |
| 「寫 Abstract 並組 Word」 | 撰寫 Abstract；合併各章、統一參考文獻、產生 Word 與 PDF |
| 「開始寫簡報」 | 依作業規範的簡報內容順序撰寫 `slides.md`：15 頁投影片與逐字稿，逐字稿約每分鐘 260–300 字 |
| 「做 PPT 和影片」 | 產生 PPT、AI 旁白與有字幕的影片；為簡報另畫橫式架構圖與流程圖 |
| 「對於 proposal 再做最終檢查」 | 對照老師文件逐條檢查，寫成 `doc/acceptance/proposal-checklist.md` |
| 「處理建議項目」 | 補上課程框架對應、精簡 Abstract、加入本附錄與紀錄、修正摘要表用詞 |
