# Binding verification — dry-run（Project Bindings 第 8.2 節 #3）

- **狀態**：**已執行（2026-11-17）。** 12 列中 11 列符合 m1 的預期。第 10 列（Fable alias）觀測為 `claude-fable-5-2`，與 m1 所列的 Fable 5.1 不符；acceptor 決定改為 Fable 5.2（Bindings m2 的 O-4）。m2 已於 2026-11-17 針對 commit `2d4c270` 接受並生效，Fable 路徑依 O-4 以 `claude-fable-5-2` 使用。
- **為什麼不沿用 `aiot-classwork` 的紀錄**：binding 證據是針對特定 repo、特定 session 與當時載入的 definitions 觀測的。本專案的 `gov-*` definitions 是 2026-11-17 改寫後的版本，必須在從本 repo 根目錄啟動的新 session 重新觀測（Bindings 第 3.6、6 節）。
- **方法**：對每一列以 Agent tool 派一次不做事的任務（指示不呼叫工具，不讀、不寫、不執行、不搜尋任何檔案，特別是 `data/`，不作任何判斷，只回一行 ack），再以 Bindings 第 3.6 節的核對指令讀取 harness 紀錄，核對 `agentType` 與全部 assistant 訊息的 (model, effort)。
- **完成條件**：每一列的觀測值集合只有一個元素，且等於預期。任何一列不符時，該 definition 不得用於正式派工，依 Bindings 第 3.1 節處理並記錄。

## 結果

| # | 對象 | 派工方式 | 預期 model／effort | agentId | 觀測（則數） | 結果 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `design_authority` | `gov-design-authority` | `claude-opus-5-5`／`high` | `a8b11034a3a67626d` | `claude-opus-5-5`／`high`（1） | 符合 |
| 2 | `executor` | `gov-executor` | `claude-opus-5-5`／`high` | `a6e51445f56fed934` | `claude-opus-5-5`／`high`（2） | 符合 |
| 3 | `executor`（fallback） | `gov-executor-fallback` | `claude-opus-4-8`／`high` | `a56f4ecdd577e5dea` | `claude-opus-4-8`／`high`（1） | 符合 |
| 4 | `primary_reviewer` | `gov-primary-reviewer` | `claude-opus-5-5`／`xhigh` | `a0f646a5499ecde0f` | `claude-opus-5-5`／`xhigh`（1） | 符合 |
| 5 | `alternate_reviewer` | `gov-alternate-reviewer` | `claude-opus-5-5`／`xhigh` | `a10d5b7af138afb0c` | `claude-opus-5-5`／`xhigh`（1） | 符合 |
| 6 | `final_adjudicator` | `gov-final-adjudicator` | `claude-opus-5-5`／`xhigh` | `a9ec105a2f26cd523` | `claude-opus-5-5`／`xhigh`（1） | 符合 |
| 7 | `orchestrator`（只核對 definition 的 binding；正式 run 由主 session 擔任） | `gov-orchestrator` | `claude-opus-5-5`／`medium` | `ada1dcce3055d7e07` | `claude-opus-5-5`／`medium`（2） | 符合 |
| 8 | `investigator` | `gov-investigator` | `claude-sonnet-5-5`／`high` | `a845a4cebc6a2eb4e` | `claude-sonnet-5-5`／`high`（1） | 符合 |
| 9 | `bounded_worker`（`standard`） | `gov-bounded-worker` | `claude-sonnet-5-5`／`high` | `a26c0694f5a6507e1` | `claude-sonnet-5-5`／`high`（1） | 符合 |
| 10 | Fable 路徑（E-DA／E-AR／E-FA 與各 fallback） | `gov-alternate-reviewer`＋`model: fable` | m1：`claude-fable-5-1`／`xhigh`。m2（O-4）：`claude-fable-5-2`／`xhigh` | `af267b8ab2ac6a0aa` | `claude-fable-5-2`／`xhigh`（1） | 對 m1 **不符**；acceptor 決定改為 Fable 5.2（O-4），對 m2 符合。m2 已生效（2026-11-17，`2d4c270`） |
| 11 | E-IN | `gov-investigator`＋`model: opus`、`effort: high` | `claude-opus-5-5`／`high` | `a43b9f2e01d831b36` | `claude-opus-5-5`／`high`（1） | 符合 |
| 12 | Haiku qualification probe（`mechanical`） | `gov-bounded-worker`＋`model: haiku`、`effort: high` | `claude-haiku-5-5`／`high` | `a08170a8bdd0eeab3` | `claude-haiku-5-5`／`high`（1） | 符合。依 Bindings 第 3.4 節，`mechanical` 自本紀錄起以 Haiku 派工 |

第 2、7 列各有 2 則 assistant 訊息，集合仍只有一個元素。

## m3 的重新驗證（Bindings 第 8.2 節 #7，**已執行，2026-11-17**）

在 m3 commit 之後開的新 session 執行，因為 definition 的變更只在 session 啟動時載入。m3 接受前做的觀測只算預備，不構成 m3 的 binding 證據，直到 m3 生效。

**結論**：六列都符合。第 13–16 列符合，O-5 的四個 Claude reviewer 派工方式可用於正式派工。第 17–18 列的第一輪（兩次嘗試）因 Codex 認證錯誤而 BLOCKED；acceptor 重新登入 Codex 後重跑，兩列都符合：預設 model `<M>` 觀測為 `gpt-6.1-sol`，以 `--model gpt-6.1-sol --effort high --write` 呼叫時 rollout 的 `turn_context` 只有 (`gpt-6.1-sol`, `high`, `workspace-write`)，worktree 只多出 probe 檔，沒有讀取 worktree 以外的路徑（見執行紀錄）。依 Bindings 第 3.3 節，`<M>` 是 `gpt-6.1-sol`，之後每次呼叫都以 `--model gpt-6.1-sol` 固定。第 8.2 節 #7 的狀態欄等 acceptor 同意後再轉錄。

| # | 對象 | 派工方式 | 預期 | 觀測 | 結果 |
| --- | --- | --- | --- | --- | --- |
| 13 | `primary_reviewer`（Claude path 首項，O-5） | `gov-primary-reviewer` | `claude-opus-5-5`／`high` | agentId `afda6265804a57b33`：`claude-opus-5-5`／`high`（2） | 符合 |
| 14 | `primary_reviewer`（Claude path 第二項） | `gov-primary-reviewer`＋`model: fable` | `claude-fable-5-2`／`high` | agentId `a64263ce67f55181b`：`claude-fable-5-2`／`high`（1） | 符合 |
| 15 | `alternate_reviewer`（O-5） | `gov-alternate-reviewer` | `claude-fable-5-2`／`high` | agentId `ae9ca051c77ccd80a`：`claude-fable-5-2`／`high`（1） | 符合 |
| 16 | `alternate_reviewer`（fallback） | `gov-alternate-reviewer`＋`model: opus` | `claude-opus-5-5`／`high` | agentId `a60491b2732785c59`：`claude-opus-5-5`／`high`（2） | 符合 |
| 17 | Codex qualification：預設 model | companion `task --fresh`，不帶 `--model`，effort `high`，專用 worktree | 記錄觀測到的 model `<M>` | 第一輪：兩次嘗試的 `turn_context` 都是 (`gpt-6-sol`, `high`, `read-only`)，turn 因認證錯誤失敗（BLOCKED）。重跑（重新登入後）：thread `01a1e8bd-39a4-7e42-86b7-c2af46076ad6`，1 個 `turn_context`：(`gpt-6.1-sol`, `high`, `read-only`)，回覆 `ack`，0 次工具呼叫 | 符合。`<M>` ＝ `gpt-6.1-sol`（以完成的 turn 為準；第一輪的 `gpt-6-sol` 不採用） |
| 18 | Codex qualification：binding | companion `task --fresh --write --model <M> --effort high`，專用 worktree，要求只寫一個 probe 檔 | rollout 全部 `turn_context` 為 (`<M>`, `high`, `workspace-write`)；worktree 只多出 probe 檔；沒有讀取 worktree 以外的路徑 | thread `01a1e8bd-a8a1-7ad1-8f12-d0c3cc7f1a98`，1 個 `turn_context`：(`gpt-6.1-sol`, `high`, `workspace-write`)。1 次工具呼叫：`apply_patch` 新增 `probe.txt`（相對路徑）。worktree 的 `git status` 只有 `?? probe.txt`。複製到主 checkout 之外後 SHA-256 相同 | 符合 |

## 執行紀錄（第 1–12 列）

- **日期**：2026-11-17
- **Session**：`6ccb50de-5234-4a2d-8637-7a94bc585260`，從本 repo 根目錄啟動。主 session 是無角色 session（Bindings 第 3.5 節），只作派工介面。
- **Definitions 的 commit**：`39e77ec`（`git log -1 -- .claude/agents` 的結果）。執行時 HEAD 是 `6de249d`，分支 `docs-scope-reduction-mvp`。
- **Frontmatter**：九個 definitions 都綁定完整的 model id 與 effort，沒有使用 `inherit`。環境變數沒有 `CLAUDE_CODE_SUBAGENT_MODEL`，專案的 `.claude/` 沒有 settings 檔。
- **工具呼叫數**：12 次 dry-run 都是 0 次。
- **`git status` 前後**：都是 `## docs-scope-reduction-mvp`、`?? receipts/`、`?? review-receipts/`，沒有變化。這兩個未追蹤的資料夾在 dry-run 之前就已存在（建立時間 2026-11-17 14:05），不是 dry-run 產生的。
- **Root session**：核對時主 session 的觀測值是 `claude-opus-5-5`／`high`（29 則）。這只是當時的狀態，不構成任何角色的 activation。
- **Fable 的處理**：觀測到 `claude-fable-5-2` 後停止使用 Fable 路徑，交由 acceptor 決定（Bindings m1 第 3.1 節）。acceptor 2026-11-17 決定（原文）：「gov-alternate-reviewer＋model: fable ，改為Fable 5.2」。這個決定寫成 Bindings m2 的 O-4，變更紀錄在 Bindings 第 9 節。

核對指令（Bindings 第 3.6 節）的原樣輸出：

```text
root-session 6ccb50de-5234-4a2d-8637-7a94bc585260 {('claude-opus-5-5', 'high'): 29}
agent-a08170a8bdd0eeab3 gov-bounded-worker {('claude-haiku-5-5', 'high'): 1}
agent-a0f646a5499ecde0f gov-primary-reviewer {('claude-opus-5-5', 'xhigh'): 1}
agent-a10d5b7af138afb0c gov-alternate-reviewer {('claude-opus-5-5', 'xhigh'): 1}
agent-a26c0694f5a6507e1 gov-bounded-worker {('claude-sonnet-5-5', 'high'): 1}
agent-a43b9f2e01d831b36 gov-investigator {('claude-opus-5-5', 'high'): 1}
agent-a56f4ecdd577e5dea gov-executor-fallback {('claude-opus-4-8', 'high'): 1}
agent-a6e51445f56fed934 gov-executor {('claude-opus-5-5', 'high'): 2}
agent-a845a4cebc6a2eb4e gov-investigator {('claude-sonnet-5-5', 'high'): 1}
agent-a8b11034a3a67626d gov-design-authority {('claude-opus-5-5', 'high'): 1}
agent-a9ec105a2f26cd523 gov-final-adjudicator {('claude-opus-5-5', 'xhigh'): 1}
agent-ada1dcce3055d7e07 gov-orchestrator {('claude-opus-5-5', 'medium'): 2}
agent-af267b8ab2ac6a0aa gov-alternate-reviewer {('claude-fable-5-2', 'xhigh'): 1}
```

## 執行紀錄（第 13–18 列，m3）

- **日期**：2026-11-17
- **Session**：`2d8ad5bb-45c7-44c1-98fa-9c8acadcb142`，從本 repo 根目錄啟動，m3 commit 之後才開。主 session 是無角色 session（Bindings 第 3.5 節），只作派工介面。
- **Definitions 的 commit**：`368c858`（`git log -1 -- .claude/agents` 的結果）。執行時 HEAD 是 `0ccfa7c`，分支 `docs-scope-reduction-mvp`。
- **Frontmatter**：`gov-primary-reviewer` 是 `claude-opus-5-5`／`high`，`gov-alternate-reviewer` 是 `claude-fable-5-2`／`high`。九個 definitions 都綁定完整的 model id 與 effort，沒有使用 `inherit`。環境變數沒有 `CLAUDE_CODE_SUBAGENT_MODEL`，專案的 `.claude/` 只有 `agents/`，沒有 settings 檔。
- **第 13–16 列的工具呼叫數**：四次 dry-run 都是 0 次，都只回一行 `ack`。第 13、16 列各有 2 則 assistant 訊息，集合仍只有一個元素。
- **Root session**：核對時主 session 的觀測值是 `claude-opus-5-5`／`high`（20 則）。這只是當時的狀態，不構成任何角色的 activation。
- **`git status`**：執行前後未追蹤的都是 `docs/governance/records/decisions/receipts/`、`docs/governance/records/decisions/review-receipts/`、`receipts/`、`review-receipts/`，這四個資料夾在本次執行之前就已存在。本次執行只修改本檔。（此句指第一輪；重跑同樣只修改本檔。）

核對指令（Bindings 第 3.6 節）的原樣輸出：

```text
root-session 2d8ad5bb-45c7-44c1-98fa-9c8acadcb142 {('claude-opus-5-5', 'high'): 20}
agent-a60491b2732785c59 gov-alternate-reviewer {('claude-opus-5-5', 'high'): 2}
agent-a64263ce67f55181b gov-primary-reviewer {('claude-fable-5-2', 'high'): 1}
agent-ae9ca051c77ccd80a gov-alternate-reviewer {('claude-fable-5-2', 'high'): 1}
agent-afda6265804a57b33 gov-primary-reviewer {('claude-opus-5-5', 'high'): 2}
```

### Codex（第 17–18 列）

- **CLI 與登入**：`codex --version` 輸出 `codex-cli 0.169.0`；`codex login status` 在嘗試前後都輸出 `Logged in using ChatGPT`。Companion 是 codex plugin 1.0.6 的 `scripts/codex-companion.mjs`。沒有讀取 `~/.codex/auth.json`。
- **Worktree**：第一次 `git worktree add --detach` 用 session scratchpad 之下的路徑，因 Windows 路徑長度限制（`PKG/` 內的長檔名回報 `Filename too long`）失敗，沒有建立 worktree（`git worktree list` 只有主 checkout）。改用 `C:/Users/yotsu/AppData/Local/Temp/cxprobe-20261117` 後建立成功（detached，`0ccfa7c`）；worktree 內沒有 `data/` 與 `.env`。
- **嘗試 1**：`task --fresh --effort high "<no-op 提示>"`，不帶 `--model`、不帶 `--write`。Thread `01a1e8b3-7bd8-7802-9405-853a675637c7`，rollout `~/.codex/sessions/2026/11/17/rollout-2026-11-17T16-50-46-01a1e8b3-7bd8-7802-9405-853a675637c7.jsonl`。Companion 先回報多次 `Reconnecting... n/5`，最後的錯誤原文：`Your access token could not be refreshed because your refresh token was already used. Please log out and sign in again.`，`Turn failed.`
- **嘗試 2**（同一指令，用來排除暫時性錯誤）：thread `01a1e8b5-253f-7fc1-8514-36c2c75ef718`，rollout `~/.codex/sessions/2026/11/17/rollout-2026-11-17T16-52-28-01a1e8b5-253f-7fc1-8514-36c2c75ef718.jsonl`。錯誤原文與嘗試 1 相同，`Turn failed.`
- **Rollout 內容**：兩份 rollout 各有 1 個 `turn_context`，都是 model `gpt-6-sol`、effort `high`、sandbox `read-only`，cwd 是上述 worktree。兩份都沒有 function call 或 shell call（0 次工具呼叫），也沒有 model 回應。
- **Worktree 的處理**：嘗試後 `git status --porcelain` 為空。`git worktree remove` 已把 worktree 從 git 移除（`git worktree list` 只剩主 checkout）、刪除其內容，但空目錄本身回報 `Permission denied`／`Device or resource busy`，推測是 companion 留下的程序仍以它為 cwd。空目錄留在原處，沒有終止任何程序。
- **觀察**：`codex login status` 顯示已登入，但 token refresh 失敗。只看 login status 不足以確認 Codex 當次可用；Bindings 第 3.3 節 (2) 已要求同時引用該次呼叫的錯誤原文。
- **結果**：重新登入屬 RB-3（第三方帳號操作），由 acceptor 進行。acceptor 重新登入後，第 17、18 列要重跑；在那之前 Codex 的 qualification 未完成。

### Codex 重跑（第 17–18 列，acceptor 重新登入後）

- **日期與 session**：2026-11-17，同一個 session `2d8ad5bb-45c7-44c1-98fa-9c8acadcb142`。acceptor 在對話中回覆「Re-logged in, rerun」後執行。`codex login status` 輸出 `Logged in using ChatGPT`。沒有讀取 `~/.codex/auth.json`。
- **Worktree**：`git worktree add --detach C:/Users/yotsu/AppData/Local/Temp/cxprobe2-20261117 HEAD`。執行時 HEAD 是 `f1c7bb6`（分支 `docs-scope-reduction-mvp`），`.claude/agents` 仍是 `368c858`。建立後 `git status --porcelain` 為空，worktree 內沒有 `data/` 與 `.env`。
- **第 17 列**：`task --fresh --effort high "<no-op 提示>"`，不帶 `--model`、不帶 `--write`。Thread `01a1e8bd-39a4-7e42-86b7-c2af46076ad6`，rollout `~/.codex/sessions/2026/11/17/rollout-2026-11-17T17-01-18-01a1e8bd-39a4-7e42-86b7-c2af46076ad6.jsonl`。`turn_context` 1 個：(`gpt-6.1-sol`, `high`, `read-only`)。回覆 `ack`，0 次工具呼叫。
- **與第一輪的差異**：第一輪（重新登入前）失敗的兩個 turn 的 `turn_context` 是 `gpt-6-sol`；重新登入後完成的 turn 是 `gpt-6.1-sol`。預設 model 可能隨帳號或 Codex 的設定而變，所以 Bindings 第 3.3 節規定之後以 `--model <M>` 固定，不依賴預設。
- **第 18 列**：`task --fresh --write --model gpt-6.1-sol --effort high "<probe 提示>"`；提示要求只在 worktree 根目錄建立 `probe.txt`（內容一行 `codex binding probe 2026-11-17`），不讀、不列、不搜尋其他檔案，不執行測試或 git，不存取 worktree 以外的路徑（特別是 `data/`、`.env`）。Thread `01a1e8bd-a8a1-7ad1-8f12-d0c3cc7f1a98`，rollout `~/.codex/sessions/2026/11/17/rollout-2026-11-17T17-01-46-01a1e8bd-a8a1-7ad1-8f12-d0c3cc7f1a98.jsonl`。
  - `turn_context` 1 個：(`gpt-6.1-sol`, `high`, `workspace-write`)，集合只有一個元素，等於預期。
  - 存取紀錄：rollout 只有 1 次工具呼叫（`custom_tool_call` `exec`，內容是 `apply_patch` 的 `*** Add File: probe.txt`，相對路徑），沒有 shell 指令，沒有讀取任何檔案，沒有存取 worktree 以外的路徑。
  - Worktree：`git status --porcelain --untracked-files=all` 只有 `?? probe.txt`；檔案內容是 `codex binding probe 2026-11-17` 加換行。
  - Self-written record 的流程：把 `probe.txt` 原樣複製到 session scratchpad（不是主 checkout，因為 probe 檔不是紀錄，不進 repo），兩者 SHA-256 都是 `0d39ece1d09ddfbbdc6674b35a13cd3035b514f73263820a9009259de5532292`。
- **Worktree 的處理**：`git worktree remove --force` 把 worktree 從 git 移除並刪除其內容（`git worktree list` 只剩主 checkout），但空目錄本身同樣回報 `Permission denied`，第一輪留下的 `cxprobe-20261117` 空目錄也仍是 `Device or resource busy`。兩個空目錄留在原處，沒有終止任何程序；主 checkout 的 `git status` 不受影響。
- **觀察**：companion 在兩次重跑都輸出 `Turn completion inferred after the main thread finished and subagent work drained.`；rollout 內沒有任何 subagent 或額外 thread 的紀錄。
