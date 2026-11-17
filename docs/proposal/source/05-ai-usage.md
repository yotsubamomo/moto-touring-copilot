# 附錄 A：AI 使用說明

依作業規範「AI is OK」：本提案在研究、撰寫與製作過程中使用 AI 工具。下表說明每項工作中 AI 做了什麼，以及哪些由組員決定、如何驗證。主要指令與提示詞紀錄放在 GitHub：`final_project/doc/proposal/ai-usage-log.md`。

| 工作 | 使用的工具 | AI 做了什麼 | 組員決定與驗證方式 |
| --- | --- | --- | --- |
| 選題與範圍 | Claude Code（Claude Opus 5.5） | 盤點候選題目並比較；以公開資料集 VED 做流程可行性檢查；檢查一趟實際 GPX 的資料格式 | 題目與 ①–⑩ 各項範圍由組員逐項決定，紀錄在 `doc/brief/architecture-scope.md` |
| 證據與文獻 | Claude Code（含網頁搜尋與子代理） | 搜尋官方統計、論文與新聞；起草 Introduction、Related Work、Deep Research | 每個數字與引用都對照原始頁面，查證紀錄保存在各章 Markdown 原稿；無法查證者刪除或標註 |
| 系統設計 | Claude Code | 起草架構圖、多 Agent 分工、數學模型、流程圖、Pseudocode、評估計畫 | 設計取捨（整趟 P90 校正、驗證規則、承諾範圍）由組員審閱 |
| 文件與簡報製作 | Claude Code 撰寫的產生程式；pandoc、python-pptx、mermaid-cli | 把 Markdown 原稿轉成 Word、PDF、PPT 與圖 | 產生程式放在 `final_project/tools/`，可重現 |
| 簡報影片 | Microsoft Edge 線上朗讀（zh-TW-HsiaoChenNeural）、ffmpeg | 依逐字稿產生 AI 旁白、字幕與影片 | 逐字稿由組員審閱 |

AI 產出的內容都經過人工審閱。本提案不含任何實驗結果，預期成果均標示為待驗證。
