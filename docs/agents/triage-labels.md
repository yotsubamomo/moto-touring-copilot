# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Label in mattpocock/skills | Label in our tracker | Meaning                                  |
| -------------------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.

In practice this repo only uses `/to-spec` and `/to-tickets`, so `ready-for-agent` is the label that actually gets applied. The labels must exist in the GitHub repo before `gh issue edit --add-label` will accept them.

> 本 repo 目前只有 GitHub 的預設標籤（其中只有 `wontfix` 與上表同名）；`needs-triage`、`needs-info`、`ready-for-agent`、`ready-for-human` 還沒有建立。需要用到時先建立標籤，建立標籤屬於對 tracker 的變更，由 acceptor 決定。
