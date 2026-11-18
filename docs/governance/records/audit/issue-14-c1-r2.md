# Issue #14 — cycle 1 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37a`）→ SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md` §2、§4、§5 R1-2 與 E-1～E-6）＋CL-R1-13（`decision-20261118-issue13-c131.md`）＋CL-R1-14～CL-R1-17（`decision-20261118-issue14-c141.md`，含 §8）→ Issue #14 |
| BASE | `deb808dc88ccbb49b97875dade5a838884e19e2c` |
| HEAD | `c7976b5d25b0d7087b67500acc00f7d5c8f080f7`；本專用 worktree 的 detached HEAD |
| R1 subject／record | `532c0962e1ef7ecd0d621f8230897e251aaa6299`；`docs/governance/records/audit/issue-14-c1-r1.md`，已從磁碟重讀 |
| Correction | `359b948`：`routing/snapshot.py`、`routing/store.py`、兩個測試檔；`d4a9c4c`：worklog §10；其後至 HEAD 只有 record-only delta |
| Audit kind | **Ticket independent audit，R2 closure review，cycle 1；not a Spec Integration Audit** |
| Role | `primary_reviewer`（Codex） |
| 日期／高風險 | 2026-11-18；H-2、H-3、H-4 |

## Assurance 與獨立性

| Property | 滿足方式與證據界線 |
| --- | --- |
| Independent context | 本次為 fresh Codex thread，沒有繼承 Executor 或 R1 reviewer 的對話。自行重讀 R1 record、修正後檔案、diff、契約及測試；worklog 的結論只作待驗證主張。沒有派 subagent。 |
| Verifiable binding | 依 Bindings m3 §3.3 O-6，由 dispatcher 核對本次 rollout 的全部 `turn_context`、存取紀錄與自寫 record hash，再記入 `docs/governance/records/run/run-20261117-oc1-run2.md` §6 **本次「#14 R2／cycle 1／cx14r2／HEAD c7976b5」dispatch event**。截至受審 HEAD，§6 只有事件 69～73 與較早事件，**尚無本次 R2 的事件號與 binding 欄位**；不把事件 72（R1）或 73（Executor correction）冒作本次證據，不推定下一事件號。此項待 NV-B1，不能宣稱四項 properties 已全部獲 dispatcher 實證。 |
| Autonomous access | 自行讀取本 worktree 的必要原始材料、git 歷史與差異，執行兩輪完整測試及記憶體探測。沒有讀取、列出或搜尋 worktree 外路徑、私有資料或憑證，沒有網路／GitHub 呼叫，沒有執行 `experiments/` 腳本。 |
| Self-written record | 本檔由本 reviewer 自己撰寫，是唯一新增檔案；不修改實作、測試、契約、worklog 或其他 records，不 stage／commit。Dispatcher 應依 §3.3 原樣收錄並核對 SHA-256，不得代寫／改寫 findings 或 verdict。 |

Model evidence：run record §6 事件 69、71、73 記載 Executor 為同一 agent `a731e697ea497fcf3`，實際觀測 `claude-opus-5-5`／`high`，最後核對 161 則、集合單一。本 reviewer 是 **Codex**；Bindings §8.2 #7 與既有 run 的 mapping 是 `gpt-6.1-sol`／`high`，但本次實際 model ID／effort／sandbox 尚無 dispatcher 的 run-record 證據，不以規定值當作觀測值。**no model diversity claim（不主張 model diversity）**。正式採用本 record 前仍須完成 NV-B1；下列 blocking 判斷有獨立可重現的產品證據。

## Findings 與 closure 判定

### R1-F1 — RESOLVED

- 原 severity：Medium／blocking；owner：Issue #14 Executor。本項已無未解 required fix。
- `src/moto_copilot/routing/snapshot.py:238` 先檢查字串型別與 enum，`:264` 才允許查 `LEG_DIRECTIONS`；`[]`、`{}` 不再進入不可 hash 的 lookup。
- 已讀並實跑新增 validator／builder／put／load／一般選取／strict tests。`tests/test_routing_store.py:585` 的 strict regression 以壞檔 bytes 實算 SHA-256，並核對 `file_sha256`，不是以 hash mismatch 提早停止；另有相容好快照，仍得到 `StrictModeStop(reason='invalid_snapshot')`。
- 另以 stdin 記憶體探測獨立重做 `[]`、`{}`：validator 回報 `$.trip_type`、builder／put 為 `SnapshotValidationError`、load 為 `SnapshotIntegrityError`、strict 使用相同壞 bytes 的實際 SHA-256 得到 `invalid_snapshot`。沒有寫檔。
- `_parse_snapshot_bytes` 的 JSON／validation 防線沒有把錯誤當作成功；未發現此修正引入回歸。

### R1-F2 — NOT RESOLVED：列舉後、讀取前的狀態檢查仍會靜默略過消失的檔案

- **Severity：Medium；blocking。Owner：Issue #14 Executor。**這是原 R1-F2 required fix 的殘留，沒有另開一次全面審查或把它改列為無關新需求。
- 契約依據：R1-F2 Required fix 明列讀取／列舉／檔案狀態、列出後消失，以及不得略過、回傳 `None`／`snapshot_missing` 或改選其他快照；CL-R1-17（DA record §5），H-3／H-4。
- **已修好的部分：**`store.py:203` 的 `_read` 把 EACCES／EIO 轉為 `SnapshotIntegrityError`；`:248` 把 `snapshot_ids()` 已產出 ID 後、`load` 時消失轉為相同完整性錯誤；`:354` 的 strict 轉為 `StrictModeStop(reason='unreadable')`，明確缺檔分支仍為 `file_missing`。新增測試及獨立探測均確認這些分支的訊息與一般 formatted traceback 不帶原始 OS 路徑或合成座標，`__cause__ is None` 且 suppress context。
- **未解的程式證據：**`src/moto_copilot/routing/store.py:232` 已從 `iterdir()` 得到符合快照檔名的項目，但 `:233` 仍用 `entry.is_file()` 篩選。此環境的 Python 3.11.2 在 `Path.stat()` 拋 `FileNotFoundError` 時，`is_file()` 會回 `False`；因此外層 `:235` 的 `except OSError` 接不到錯誤，該 ID 不會進入 `snapshots()` 的 `:245`～`:249`。檔案消失被當成不參與候選，不是停止。
- **測試缺口：**`tests/test_routing_store.py:668` 把整個 `SnapshotStore.snapshot_ids` 換成直接回傳 ID 的 lambda，繞過真正的 `iterdir`／`is_file` 邊界；它能測到較晚的 read race，測不到這個較早的 status race。兩輪 1441 個測試全綠不能證明此 required fix 全部解決。
- **獨立重現：**保留正式 `snapshot_ids()`、`snapshots()`、兩個 selector 與真正的 `Path.is_file()`，只以 `Path.iterdir` 列出合法檔名、以 `Path.stat` 對消失項目拋合成 `FileNotFoundError`，好檔讀取回傳合成 bytes。結果如下，均未拋 `SnapshotIntegrityError`：

| 列舉情形 | `snapshot_ids()` | `find_reusable` | `select_snapshot_mode` |
| --- | --- | --- | --- |
| 消失項目＋相容好檔 | 只剩 `SN-38b8ca32a0` | 回傳好檔 `SN-38b8ca32a0` | 回傳好檔 `SN-38b8ca32a0` |
| 只有消失項目 | `[]` | `None` | `snapshot_missing` |

- **影響：**修正已承諾的一般選取 fail-closed 邊界仍有洞；遇到已被目錄列舉、隨後失去的快照時，可靜默選用其他快照或啟動一般缺快照流程。這不是 strict 的新 regression，也沒有主張真實私有資料已外洩。
- **Required fix：**讓符合檔名、已由目錄列舉取得的項目，在狀態查詢時消失／失敗也於一般選取邊界成為不含路徑與內容的 `SnapshotIntegrityError`，不經由會把此錯誤隱藏成 `False` 的篩選而略過。補保留正式 `snapshot_ids()` 與 `is_file`／狀態查詢流程的 regression：`iterdir` 已產出合法名稱、隨後 stat 為 `FileNotFoundError`，有相容好檔及沒有好檔時，兩種一般選取都必須停止；同時維持既有其他 I/O、strict、traceback 隱私與 write-once 檢查。直接 `load` 未存在 ID 的 not-found API 可保留。

### R1-N1 — 延續既有 non-blocking disposition

原 severity：Low／non-blocking；owner：acceptor。併入既有 C-14-6，由 acceptor 決定歷史與 records 的公開前處置；本次不是 correction requirement，不要求 Executor 改寫先前紀錄，不延長 cycle，也不重印該示例座標。證據位置仍為 R1 record 的 R1-N1、worklog §10.4、run §6 事件 69、70、72、73。沒有新增 non-blocking finding。

## D-14-14 與 regression 範圍

**D-14-14 屬於 targeted correction 可接受的範圍。**它在同一個 snapshot store 的 `put` 狀態查詢／寫入邊界，抑制與 R1-F2 相同的 caller 路徑帶出風險；未新增資料來源、成功路徑、重試、覆寫或刪除。`SnapshotStoreError` 用於寫入失敗合理，沒有把失敗轉成 created／reuse 成功。

`store.py:186` 仍為 `xb` exclusive create；`:190` 的 `FileExistsError` 仍走既有內容比對；`:198`～`:201` 沒有改動。同內容保留舊 bytes／mtime／`fetched_at`、新內容另存、衝突拒絕、不改舊檔等既有測試皆通過。另以記憶體替身令 `exists=False`、`open` 拋 `FileExistsError`、讀取回傳既有相同 bytes，核對 `created=False` 且沿用既有 snapshot，PASS。新增的 `put` OS-error tests 確認無路徑、無寫入。未發現 D-14-14 引入 blocking regression；R1-F2 殘留位於另一個 `snapshot_ids()` 邊界。

本次只審 R1-F1／F2 closure、這些修正直接產生或暴露的 blocking defect 及其 regression。沒有重審全部 Ticket AC，也不宣稱 SPEC-R1 SIA、AB 整體驗收、E1 Lite／E2 或整合完成。

## 已讀來源與實際檢查

已讀 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3（特別是 §3.3、§5、§7、§8.2）；生效 package 的治理 §2.3、§3.8、§4.1～§4.7，impl-default v2 §6～§7、orch-default v2.2 §6～§7；R1 record；SPEC-R1 derivation、first-run derivation 的相關條款；CL-R1-13、CL-R1-14～17、DA §8、TI-C14-5 與後續 #15／#16 限制；高風險 record §5；OC-1 對應 AB；SPEC-001 §2、4.14、7.11 及所分配 S 編號，DESIGN §5 摘要；run 事件 69～73、worklog 的 evidence 與 §10。Issue #14 使用派工原文及其宣告 hash `f7a83732c3b65001e170e8a337ada636f8a984f908b41743d033519a95ca7b75`，沒有對外查詢。

| 指令／檢查 | 實際結果 |
| --- | --- |
| `git status --short`、`git rev-parse HEAD`、`git rev-parse deb808d` | 起始 clean；完整 SHAs 如檔首。 |
| `git log --oneline deb808d..c7976b5`、`git log --format='%h %s' --name-only deb808d..c7976b5` | 核對整體四個 implementation commits 為 `aa42392`、`366866c`、`5eee704`、`359b948`；其餘只改 records。 |
| `git diff --stat 532c096..c7976b5`；`git diff 532c096..c7976b5 -- src/moto_copilot/routing/snapshot.py src/moto_copilot/routing/store.py tests/test_routing_snapshot.py tests/test_routing_store.py` | 全 delta 7 檔、501 insertions、25 deletions；完整讀取四檔 correction diff 與修正後兩個模組、synthetic helper、相關舊／新測試。 |
| `git diff --name-status deb808d..c7976b5`、`git diff --stat deb808d..c7976b5`；stdin 以 subprocess 讀 `git diff deb808d..c7976b5 -- src tests` 做逐檔變更分類 | 共 12 檔、2966 insertions、1 deletion；src／tests 為八個新增檔，沒有修改 BASE 已有程式或測試。整體差異核對用於界定 correction，不另作第二次全面 audit。 |
| stdin `git diff --name-only 359b948..d4a9c4c` 及 `d4a9c4c..c7976b5` | 分別只有 `worklog/issue-14.md` 與 run record，均為 Bindings §7 record-only paths。 |
| `git diff --check 532c096..c7976b5` 及 `git diff --check deb808d..c7976b5` | 各 exit 2，唯一輸出 `docs/governance/records/worklog/issue-14.md:313: new blank line at EOF.`，不是實作錯誤或必要 gate failure；不增列 non-blocking finding。 |
| `python -c "import sys; print(sys.version); print(sys.executable)"` | PATH 的 Python 3.11.2，直譯器在本 worktree 內。沒有用明確虛擬環境路徑呼叫 Python，沒有改 `PYTEST_DEBUG_TEMPROOT`。 |
| **`python -m pytest -q`** | **exit 0；`1441 passed in 34.21s`**。 |
| **`python -m pytest -q -rxX`** | **exit 0；`1441 passed in 29.17s`**。沒有 failed／error／xfailed／xpassed／skipped 摘要。 |
| `rg -n 'xfail\|skip' tests`；stdin AST 讀 `tests/**/*.py`，檢查 skip／skipif／xfail／importorskip 的 Attribute／Name | 廣搜只有 `being_skipped` 測試名稱與 contracts docstring 的一般英文 `skipped`；AST 結果 `[]`，無這些 markers／calls。 |
| 兩輪 pytest 後與記憶體探測後的 `git status --short`／`git status --porcelain=v1` | 無輸出，clean；沒有新增可見 snapshot 檔案或變更 fixture。測試只使用既定 ignored pytest 暫存位置。 |
| stdin 對 `git ls-files` 的索引字串篩選 `(^\|/)data/\|\.(gpx\|fit\|key)$\|(^\|/)\.env$`（ignore case） | 0 命中；只讀 git metadata，沒有查詢或列出私有資料目錄。 |
| stdin R1-F1 獨立 assertions | 兩個 JSON 值的 validator／builder／put／load／strict real-SHA 檢查皆 PASS，詳 R1-F1。 |
| stdin R1-F2 read EACCES／EIO、stat EACCES／EIO 與 traceback assertions | 轉換與路徑抑制 PASS；一般 read／selection／file_sha256 為完整性錯誤，strict 為 unreadable；stat 的 EACCES／EIO 也會停止。 |
| stdin 保留真正 `Path.is_file()` 的 stat-ENOENT 探測 | 四個一般選取結果違反 required fix：有好檔時兩者改選，無好檔時分別回 None／snapshot_missing，詳 R1-F2。 |
| stdin D-14-14 exclusive-create race assertions | PASS；`FileExistsError` 仍沿用同內容既有檔，`created=False`，沒有真實 I/O。 |
| 寫入後 stdin 以 UTF-8 讀回 record、核對 findings 狀態與最後一行、計算 SHA-256；`git status --porcelain=v1` | 首次檢查的 stdin 字面 em dash 受 console 編碼改寫，標題比對 assertion 失敗；改用 ASCII `\u2014` escape 重跑後全部 PASS。Git 僅有 `?? docs/governance/records/audit/issue-14-c1-r2.md`；hash 由工具輸出供 dispatcher 核對，不把 self-hash 寫回本檔。 |

最初以 PowerShell 預設編碼讀中文時顯示亂碼，已改 `Get-Content -Encoding UTF8` 重讀必要原文；部分 Python stdout 的中文亦受 console 編碼影響，契約判斷以 UTF-8 重讀的原文為準。沒有把顯示亂碼當作契約內容或測試失敗。

## R1-F2 獨立重現方法

以下為實際 stdin 探測中重現殘留缺陷的部分，可在本 worktree 用 PowerShell here-string 傳給 `python -`；沒有建立 snapshot 或其他來源檔。`Path.stat` 的替身模擬列舉完成後檔案消失，沒有替換被審的 `snapshot_ids()` 或 `Path.is_file()`。

```python
import errno, stat, sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path[:0] = ['src', 'tests']
import routing_synthetic as syn
from moto_copilot.routing import (
    SnapshotStore, canonical_bytes, find_reusable, select_snapshot_mode,
)
store = object.__new__(SnapshotStore)
store.directory = Path.cwd() / '__r2_synthetic_virtual__'
good = syn.snapshot(shape_suffix='r2-good')
gone = syn.snapshot(shape_suffix='r2-disappeared')
good_path = store.path_for(good['snapshot_id'])
gone_path = store.path_for(gone['snapshot_id'])
data = canonical_bytes(good)
now = datetime.fromisoformat('2026-11-18T12:00:00+08:00')

def fake_stat(path, *args, **kwargs):
    if path == gone_path:
        raise FileNotFoundError(errno.ENOENT, 'synthetic disappeared', str(path))
    assert path == good_path
    return SimpleNamespace(st_mode=stat.S_IFREG)

def fake_read(path):
    assert path == good_path
    return data

for with_good in (True, False):
    observed = [gone_path, good_path] if with_good else [gone_path]
    with patch.object(Path, 'iterdir', lambda _: iter(observed)), \
         patch.object(Path, 'stat', fake_stat), \
         patch.object(Path, 'read_bytes', fake_read):
        ids = store.snapshot_ids()
        a = find_reusable(store, good['request_key'], syn.METHOD, now=now)
        b = select_snapshot_mode(store, good['request_key'], syn.METHOD)
        print(with_good, ids, a['snapshot_id'] if a else None,
              b.snapshot['snapshot_id'] if b.snapshot else b.route_error)
```

實際觀察：`True` 情形兩者均回 `SN-38b8ca32a0`；`False` 情形回 `None` 與 `snapshot_missing`。預期依原 R1-F2 required fix 應為兩者皆 `SnapshotIntegrityError`。這個差異足以否定 closure，不以 Executor 的「沒有新的 blocking 問題」作證。

## E-1～E-6 與 H-2／H-3／H-4

| 項目 | 本次有界核對結果 |
| --- | --- |
| E-1 | Worklog §10.3 有 subject `359b948` 的完整 1441 passed 輸出及另一次 `-rxX`；本 reviewer 已自行重跑上述兩條指定 commands。 |
| E-2 | Worklog §6 保留 R1-2 各 S 編號對應，§9 記 CL-R1-16，§10.2 補 R1-F1／F2 測試名稱與行為。對應測試實際通過，但未涵蓋 stat-ENOENT，不能據此宣稱 R1-F2 已全部 PASS。 |
| E-3 | Correction 新測試可追溯至 `routing_synthetic.py` 的手寫近零座標、SYN 代號、placeholder shape；錯誤探測也是合成 marker。沒有讀真實軌跡；歷史示例處置沿用 R1-N1／C-14-6。 |
| E-4 | Correction 沒有新增傳輸層；完整測試包含禁止 socket／DNS 的既有 test。Reviewer 沒有發出網路請求。 |
| E-5 | Correction 只增加測試（snapshot +44 行、store +177 行），既有測試斷言未刪改，沒有 xfail／skip；整體對 BASE 是新增檔案。 |
| E-6／H-2 | caller 指定目錄、write-once 與索引檢查維持；新增 read／strict／put I/O 錯誤的公開訊息與正常 traceback 不含合成目錄／座標。未主張對私有資料來源完成外部比對。 |
| E-6／H-3 | strict 實際壞檔 SHA 核對後以 invalid_snapshot 停止，缺檔、hash mismatch、unreadable、method mismatch 等既有／新測試皆通過，不回退。沒有把 pytest／合成探測寫成 E1 Lite 或 E2 結果。 |
| E-6／H-4 | 一般 read／late-disappearance／permission 邊界多數已修；**status 時消失仍靜默略過，R1-F2 blocking**。其餘既有期限下界、method、tie-break、strict no-fallback 測試均在完整測試內通過，未發現 correction 對這些成功或拒絕路徑造成 regression。 |

## NOT VERIFIED 與後續 authority

| ID | 原因／界線 | Required authority |
| --- | --- | --- |
| NV-B1 | 本次 R2 dispatch 的 rollout／實際 model、effort、sandbox、存取核對與 record SHA-256 尚未記入受審 HEAD 的 run record。Reviewer 不得到 worktree 外取得 rollout，也不能自行補造 dispatch event。正式採用前須依 Bindings §3.3 補記本次事件並核對 mapping。 | dispatcher／Orchestrator |
| NV-PRIV | 未讀任何私有騎乘資料、住家位置或 holdout，沒有取得可授權比對的明確路徑；對真實資料來源及隔離的外部核對不作已驗證主張。C-14-6 的歷史／records 處置也仍保留。 | acceptor（RB-7；歷史處置另涉 RB-6） |
| NV-INTEGRATION | #15／#16、凍結清單檔案格式 TI-C14-5、E2／Demo Runner 及端到端整合不在這次 R2 closure 範圍，未實跑。 | Design Authority 與相應後續 Spec／Reviewer；私有資料另需 acceptor |
| NV-MUT | 未重建 Executor §10.3 曾在其他工作環境執行的換版／突變過程，亦未讀其 scratchpad；只自行核對最終實作、測試與本檔記載的獨立探測。 | 若需歷史執行細節，由 Executor 提供可在本 worktree 核對的 evidence，Reviewer 核對 |

R1-F1 已 RESOLVED；R1-F2 的 status-race required fix 尚 NOT RESOLVED。依治理 §4.4 與 orch-default §6，R2 仍 blocking 時由 Orchestrator 派 **exactly one Alternate Independent Review**，fresh context；不自行增加 R3／R4。本 reviewer 沒有修改 correction、作設計裁決或代替 Orchestrator 派工。

Verdict: BLOCKING
