# Binding verification — dry-run（Project Bindings 第 8.2 節 #3）

- **狀態**：**尚未執行。** 本檔目前只列出要做的項目；下表的「觀測」與「結果」欄在實際派工並核對 transcript 之後才填。
- **為什麼不沿用 `aiot-classwork` 的紀錄**：binding 證據是針對特定 repo、特定 session 與當時載入的 definitions 觀測的。本專案的 `gov-*` definitions 是 2026-11-17 改寫後的版本，必須在從本 repo 根目錄啟動的新 session 重新觀測（Bindings 第 3.6、6 節）。
- **方法**：對每一列以 Agent tool 派一次不做事的任務（指示不讀、不寫、不執行、不裁決，只回一行 ack），再以 Bindings 第 3.6 節的核對指令讀取 harness 紀錄，核對 `agentType` 與全部 assistant 訊息的 (model, effort)。
- **完成條件**：每一列的觀測值集合只有一個元素，且等於預期。任何一列不符時，該 definition 不得用於正式派工，依 Bindings 第 3.1 節處理並記錄。

## 待執行項目

| # | 對象 | 派工方式 | 預期 model／effort | agentId | 觀測 | 結果 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `design_authority` | `gov-design-authority` | `claude-opus-5-5`／`high` | — | — | 未執行 |
| 2 | `executor` | `gov-executor` | `claude-opus-5-5`／`high` | — | — | 未執行 |
| 3 | `executor`（fallback） | `gov-executor-fallback` | `claude-opus-4-8`／`high` | — | — | 未執行 |
| 4 | `primary_reviewer` | `gov-primary-reviewer` | `claude-opus-5-5`／`xhigh` | — | — | 未執行 |
| 5 | `alternate_reviewer` | `gov-alternate-reviewer` | `claude-opus-5-5`／`xhigh` | — | — | 未執行 |
| 6 | `final_adjudicator` | `gov-final-adjudicator` | `claude-opus-5-5`／`xhigh` | — | — | 未執行 |
| 7 | `orchestrator`（只核對 definition 的 binding；正式 run 由主 session 擔任） | `gov-orchestrator` | `claude-opus-5-5`／`medium` | — | — | 未執行 |
| 8 | `investigator` | `gov-investigator` | `claude-sonnet-5-5`／`high` | — | — | 未執行 |
| 9 | `bounded_worker`（`standard`） | `gov-bounded-worker` | `claude-sonnet-5-5`／`high` | — | — | 未執行 |
| 10 | Fable 路徑（E-DA／E-AR／E-FA 與各 fallback） | `gov-alternate-reviewer`＋`model: fable` | Profile 所列為 `claude-fable-5-1`／`xhigh`；alias 實際解析值以觀測為準（Bindings 第 3.1 節「Fable alias」） | — | — | 未執行 |
| 11 | E-IN | `gov-investigator`＋`model: opus` | `claude-opus-5-5`／`high` | — | — | 未執行 |
| 12 | Haiku qualification probe（`mechanical`） | `gov-bounded-worker`＋`model: haiku`、`effort: high` | `claude-haiku-5-5`／`high` | — | — | 未執行 |

## 執行紀錄

（執行後在這裡記：日期、執行的 session-id、definitions 的 commit、核對指令的原樣輸出、每次 dry-run 的工具呼叫數、`git status` 前後是否變化。）
