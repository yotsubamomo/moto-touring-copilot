# docs/governance

本 repo 採用的治理規範與 Project Bindings。整個 repo 都適用治理，沒有 governance flag；適用範圍見 [`project-bindings.md`](project-bindings.md) 第 0 節。

| 檔案 | 內容 |
| --- | --- |
| [`project-bindings.md`](project-bindings.md) | 本 repo 的 Project Bindings：適用範圍、權限來源、角色與模型、lane、assurance、紀錄位置。**從這裡開始讀。** 第 1 節列出哪些 package 檔案是生效的規範。 |
| [`Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/`](Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2/README.md) | Minimal Governance — Reusable Package v2.2 的位元複本（以 package 內的 `MD5SUMS`、`SHA256SUMS` 核對），不在本 repo 修改。只有 Bindings 第 1 節列出的四份是生效規範：Minimal Operational Governance v2.2、Model Profile `default` v2.5（連同其引用的 v2.4 章節）、`impl-default` v2、`orch-default` v2.2；其他檔案只供參考。 |
| [`binding-verification.md`](binding-verification.md) | `gov-*` definitions 的 binding dry-run 紀錄。 |
| `records/` | 工作紀錄：Outcome Contract、decisions、worklog、audit、run records。結構見 Bindings 第 7 節；資料夾在產出該類紀錄時才建立。 |

六個角色、`executor` fallback 與兩個 bounded assignments（`gov-investigator`、`gov-bounded-worker`）的 agent definitions 在 [`.claude/agents/`](../../.claude/agents/)，檔名以 `gov-` 開頭。

## 來源

Package 與 Bindings 在 2026-11-17 由 `aiot-classwork` 的 `docs/governance/` 移植。Package 是位元複本；Bindings 依本專案改寫為 m1，差異記在 Bindings 第 9 節。`aiot-classwork` 的 binding dry-run 紀錄沒有複製過來，本專案要在自己的 session 重新驗證（Bindings 第 8.2 節）。

核對 package 複本：

```bash
cd docs/governance/Minimal_Governance_Reusable_Package_v2.2_2026-10-12b/Minimal_Governance_Reusable_Package_v2.2 && sha256sum -c SHA256SUMS
```
