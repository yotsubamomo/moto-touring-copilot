# Issue #14 — cycle 1 Alternate Independent Review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37a`）→ SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md` 第 4 節、第 5 節 R1-2 列與 E-1～E-6）＋ CL-R1-13（`decision-20261118-issue13-c131.md`）＋ CL-R1-14～CL-R1-17（`decision-20261118-issue14-c141.md`）→ GitHub Issue #14（SPEC-R1 R1-2 `routing`） |
| Issue 版本 | 派工所附原文 `issue-14-body.md`，本 reviewer 實算 SHA-256 `f7a83732c3b65001e170e8a337ada636f8a984f908b41743d033519a95ca7b75`，與派工所述相同。沒有連線查核 GitHub 現況 |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`，HEAD **`c7976b5d25b0d7087b67500acc00f7d5c8f080f7`**（R2 的受審 subject）；BASE `deb808dc88ccbb49b97875dade5a838884e19e2c`。實作 commits `aa42392`、`366866c`、`5eee704`、`359b948`；其餘只改 `docs/governance/records/**`（以 `git log --name-only deb808d..5aabd31` 核對）。主 checkout HEAD `5aabd31` 相對 subject 只多 record-only delta（R2 record 與 run record） |
| Audit kind | **Alternate Independent Review，cycle 1**（治理 §4.4；本 cycle 唯一一次）。不是 R1／R3，不是 Spec Integration Audit，不是 Final Adjudication |
| Role | `alternate_reviewer`（`gov-alternate-reviewer`） |
| 日期／治理 | 2026-11-18；Minimal Operational Governance v2.2、Bindings m3 |
| 高風險類別 | H-2、H-3、H-4（`decision-20261117-high-risk-categories.md` 第 5 節） |
| 前序 records | R1 `docs/governance/records/audit/issue-14-c1-r1.md`（SHA-256 `f201a68c…`，BLOCKING：R1-F1、R1-F2）；R2 `docs/governance/records/audit/issue-14-c1-r2.md`（SHA-256 `fb6573d6…`，BLOCKING：R1-F1 RESOLVED、R1-F2 NOT RESOLVED）；worklog `docs/governance/records/worklog/issue-14.md`；run record `run-20261117-oc1-run2.md` §6 事件 69～74。四者的結論都當成待驗證主張 |

## Assurance

### (a) Context independence（治理 §2.3 的四項 properties）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Fresh 的 `gov-alternate-reviewer` subagent，沒有繼承 Executor、Primary Reviewer 或 Orchestrator 的對話。Pack 只有路徑與識別。R1、R2 record、worklog、DA record 由本 reviewer 自行從磁碟讀取；本 record 採用的每一項事實都另行重現或重讀原始檔 |
| Verifiable binding | Definition 的 frontmatter 是 `claude-fable-5-2`／`high`（Bindings 第 3.1 節，O-5）。本 reviewer 無法自證全部 assistant 訊息的實際 (model, effort)；依 Bindings 第 3.6 節由派工者在採用本 return 前核對 transcript 並記入 run record §6 的本次派工事件。本 reviewer 讀到的 run record（HEAD `5aabd31`）最後一筆是事件 74，尚無本次事件，不推定事件號。見 NV-B1 |
| Autonomous access | 自行讀取契約、原始碼、diff、git 歷史；在 subject 的 detached worktree `C:/Users/yotsu/AppData/Local/Temp/cx14r2`（`c7976b5`）以其 `.venv`（Python 3.11.2）執行 pytest 與 stdin 探測；探測只用 `tests/routing_synthetic.py` 的合成快照，實體檔只建立在 session scratchpad 的暫存目錄（執行後自動移除）。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有讀或執行 `experiments/`，沒有使用網路或 GitHub，沒有從 repo root 搜尋，沒有使用 `git status --ignored` |
| Self-written record | 本 record 由本 reviewer 以 Write 工具直接寫入主 checkout。沒有修改實作、測試、契約、gates 或其他紀錄，沒有 stage／commit。Worktree 的 `git status --short` 在審查前後相同（只有 R2 record 未追蹤） |

### (b) 實際 model

| 角色 | 實際 model（證據） |
| --- | --- |
| Executor | `claude-opus-5-5`／`high`：run record §6 事件 69、71、73（agentId `a731e697ea497fcf3`，最後核對 161 則，集合單一）。派工者的核對紀錄，本 reviewer 沒有讀 transcript |
| Primary Reviewer（R1、R2） | Codex `gpt-6.1-sol`／`high`／`workspace-write`：run record §6 事件 72（R1，thread `01a1ec42-…`）、事件 74（R2，thread `01a1ec55-…`）。派工者的核對紀錄，本 reviewer 沒有讀 rollout |
| Alternate Reviewer（本 review） | `claude-fable-5-2`（definition 與 harness 對本 session 的宣告）；effort 與全部訊息的實際值待派工者核對（NV-B1） |

三個角色紀錄的 model 各不相同；Bindings 第 5 節沒有宣告任何 diversity 關係，本 record **不主張 model diversity**，也不以它支持任何結論。

## 判斷摘要

| 項目 | R2 的結論 | 本 review 的判斷 |
| --- | --- | --- |
| R1-F1 | RESOLVED | **已解決**（獨立重現，第 2 節） |
| R1-F2：R1 record 舉證的三項缺陷（未轉換的讀取 `OSError`、例外帶出路徑、已列出後於讀取時消失的例外型別） | 已修好 | **已解決**（獨立重現，第 1.1 節） |
| R1-F2 殘留：`snapshot_ids()` 的 `entry.is_file()` 使「已列舉、狀態查詢時已不存在」的項目不成為候選 | NOT RESOLVED；Medium／blocking | **觀察到的行為屬實；blocking 的分類不成立（分類有誤）**。已接受的契約條文沒有規定這個情形必須停止，R2 引用的依據是 R1 的 Required fix 文字而不是契約；在宣告的 operating scope 內沒有可指出的額外實質風險。改列 Low／non-blocking。其中的語義問題（CL-R1-17 是否要延伸到「已列舉但不存在或不是一般檔案」的項目）屬 Design Authority，是 routing signal，不是對 implementation 的 blocking finding（治理 §4.2）（第 1.2～1.5 節） |
| D-14-14（`put` 的 `OSError` 轉換） | 屬 targeted correction 可接受的範圍，無 regression | **成立**（第 3 節） |
| R1-N1 | 併入 C-14-6，non-blocking | 沿用，不重審（owner：acceptor） |

沒有未解的 blocking finding。

## 1. R1-F2

### 1.1 R1 record 舉證的缺陷：已解決

R1-F2 的「證據」與「影響」段指出三件事。逐項在 `c7976b5` 重現（第 5 節探測 B；替身只模擬 OS 錯誤，快照檔是 scratchpad 暫存目錄內的合成檔，目錄名稱含合成的標記字串）：

| R1-F2 的缺陷 | `c7976b5` 的行為 | 程式位置 |
| --- | --- | --- |
| 讀取的 `PermissionError`／其他 `OSError` 直接逸出 | `load`、`file_sha256`、`find_reusable`、`select_snapshot_mode`：`SnapshotIntegrityError`（EACCES、EIO 各一）；`select_strict`：`StrictModeStop(reason='unreadable')`；缺檔仍是 `file_missing` | `store.py:203`～`215`、`:349`～`356` |
| 原始 OS 例外帶出呼叫者的目錄名稱 | 上列每個例外的 `traceback.format_exception` 全文都不含標記字串，`__cause__ is None` | 同上（`from None`） |
| 已列出、讀取時已不存在：`SnapshotNotFoundError` 沒有轉成完整性錯誤 | 以**真實刪除**重現（`snapshot_ids()` 回傳之後、讀取之前刪掉該檔）：`find_reusable` 得到 `SnapshotIntegrityError`；直接 `load` 未存在的 ID 仍是 `SnapshotNotFoundError` | `store.py:245`～`249` |
| 目錄無法列舉 | `iterdir` EACCES：兩種一般選取都是 `SnapshotIntegrityError`，不含路徑 | `store.py:229`～`236` |
| 狀態查詢的 EACCES、EIO（檔案仍在） | `snapshot_ids()` 與兩種一般選取都是 `SnapshotIntegrityError`（Python 3.11.2；3.12.14 的 `Path.is_file` 原始碼相同） | `store.py:233`～`236` |

### 1.2 殘留的行為：屬實

R2 的重現以替身讓 `Path.stat` 拋 `FileNotFoundError`。本 reviewer 改用真實檔案系統重現，不替換 `stat`、`is_file` 或 `snapshot_ids`（探測 B 第 1、3 項）：存放目錄有同一 `request_key` 的舊、新兩個合成快照；包住 `Path.iterdir`，在目錄列舉完成之後、狀態查詢之前真的刪掉較新的檔案。

| 情形 | `snapshot_ids()` | `find_reusable` | `select_snapshot_mode` |
| --- | --- | --- | --- |
| 兩個檔案都在（基準） | 兩個 | 較新者 | 較新者 |
| 較新者在列舉後、狀態查詢前被刪 | 只有較舊者 | 較舊者 | 較舊者 |
| **同一次刪除在呼叫之前完成** | 只有較舊者 | 較舊者 | 較舊者 |
| 只有一個檔案，列舉後被刪 | `[]` | `None` | `snapshot_missing` |
| 較新者在狀態查詢後、讀取前被刪 | — | `SnapshotIntegrityError` | （緊接的下一次呼叫）較舊者 |

所以 R2 對程式行為的描述正確：`store.py:233` 的 `entry.is_file()` 在 `stat` 得到 ENOENT 時回傳 `False`，該項目不成為候選，外層的 `except OSError` 接不到。R2 指出的測試缺口也屬實：`tests/test_routing_store.py:662`～`679` 以 lambda 取代 `snapshot_ids`，只涵蓋讀取時的消失。

另有兩點 R2 record 沒有寫到的事實，影響這項 finding 的定性：

1. **這一行不是 correction 引入或暴露的。** `and entry.is_file()` 自 `aa42392` 起就在（`aa42392`、`366866c`、`532c096` 的 `store.py:206`），docstring 一直是「Every `snapshot_id` with a file here. Other files in the directory are ignored.」。DA 作 CL-R1-17 裁決時讀的是含這個篩選的 `store.py`；R1 的受審版本行為相同，R1-F2 的「證據」段沒有舉這一行。
2. **被略過的只有「狀態查詢時不存在或不是一般檔案」的項目。** 探測 B 第 4、6 項：名稱符合的**子目錄**不成為候選（持續狀態）；`stat` 的 ENOENT、ELOOP、Windows 錯誤 21、1921（替身）不成為候選；`stat` 的 EACCES、EIO 會停止。存在的一般檔案，不論讀不到、不是合法 JSON、不是合法快照、`snapshot_id` 與檔名或內容不符，全部停止（第 1.1 節、第 2 節與既有測試）。

### 1.3 契約是否要求這個情形停止

R2 列的契約依據依序是：R1-F2 的 Required fix、CL-R1-17、H-3／H-4。

- **Required fix 不是 accepted contract。** 它是 Reviewer 對修正方式的指示；blocking 必須依 accepted contract 或宣告 operating scope 內的具體實質風險（治理 §4.3），Reviewer 不得自行補寫 requirement（治理 §4.2）。R2 要驗證的是 finding 所指的缺陷是否解決（治理 §4.4），不是 Required fix 的字面是否逐字滿足。
- **CL-R1-17 的原文**（`decision-20261118-issue14-c141.md` 第 5 節）：「存放目錄中名稱符合 `SN-[0-9a-f]{10}.json`、但讀不到、不是合法快照、內容的 `snapshot_id` 與檔名不同或與內容雜湊不符的**檔案**，使一般模式與一般的 Snapshot Mode 都以 `SnapshotIntegrityError` 停止，不略過。」理由段：「**壞檔**表示損毀或被改動。略過它可能讓選取結果變成另一個（較舊的）快照而不被發現」；後果段：「一個壞檔會擋住該目錄的所有規劃，**直到騎士處理**」。條文的主體是存放目錄裡存在的壞檔，後果以「留在目錄裡、等騎士處理」為前提。狀態查詢時已不存在的項目，不是目錄裡的壞檔，也沒有可處理的對象。條文沒有提到列舉與讀取之間的競態。
- **存放沒有索引是契約本身的規定**（SPEC-001 7.11 第 1 項「不另建索引檔或版本號」；CL-R1-3）。因此「某個快照檔不在了」在任何時候都無法被一般選取察覺，契約對這個目錄狀態規定的結果就是「用其餘相容的快照，沒有時回 `snapshot_missing`／一般模式改呼叫引擎」（7.11 第 3 項）。第 1.2 節的表顯示，殘留情形的結果與「同一次刪除在呼叫之前完成」的結果逐項相同，也就是契約對刪除後目錄狀態所規定的結果。
- **H-4 的最低核對**（高風險 record 第 5 節）：失敗路徑的結果不得是 PASS 或預設值。殘留情形回傳的要不是一個存放時通過 4.14 值檢查、`request_key` 與檢查方法相容（一般模式另在 30 天內）的已保存快照，就是 `None`（交由 R1-4 呼叫引擎並重新檢查）或明確的 `snapshot_missing`。沒有任何未經驗證的內容被採用。**H-3**：嚴格模式不經 `snapshot_ids()`，直接讀清單指定的檔案，缺檔是 `file_missing`（已驗證），不受影響。

結論：已接受的契約條文沒有規定「已列舉、狀態查詢時已不存在」必須停止。R2 把它當成契約違反，依據不足。

### 1.4 是否有宣告 operating scope 內的具體實質風險

- 程式不刪除快照檔（7.11 第 1 項；`put` 以 `xb` 建立，本 reviewer 讀過 `store.py` 全文，沒有刪除或覆寫的路徑）。殘留情形只會在外部行為者於一次目錄列舉與緊接的狀態查詢之間刪除檔案時發生。
- 即使發生，結果與「稍早一刻刪除」相同（第 1.2 節），而後者是契約接受的。停止並不能保住什麼：探測 B 第 2 項顯示，讀取時消失而停止之後，緊接的下一次選取就回傳較舊的快照。這與 CL-R1-17 所防的情形不同：壞檔留在目錄裡，每次選取都會停止，騎士因此得知。
- DA 在同一份 record 對 CL-R1-15 的理由是「停止執行（fail closed）會讓一個無害的情形擋住規劃，沒有對應的風險可防」。本 reviewer 不以此代替 DA 對本題的判斷，只用來說明：在這份契約裡，fail closed 是針對可指出的風險，不是對所有異常一律停止。

本 reviewer 找不到殘留情形相對於契約已接受的「檔案被刪除」多出來的風險。

### 1.5 判定

1. **R1-F2（R1 record 舉證的缺陷）：已解決。**
2. **R2 的殘留項目：分類有誤。** 行為屬實，但不違反 accepted contract 的條款，也沒有 operating scope 內的具體實質風險，不符合治理 §4.3 的 blocking 條件。改列 **Low／non-blocking**（ALT-N1，第 4 節）。
3. **其中的語義問題屬 Design Authority。** 「已列舉但狀態查詢時不存在、或名稱符合但不是一般檔案（子目錄、失效的符號連結）的項目，一般選取要不要停止」是 CL-R1-17 與 D-14-7 沒有寫到的情形。要不要把 CL-R1-17 延伸到這裡，是契約語義的決定，不是 Reviewer 可以用 Required fix 補上的（治理 §4.2）。本 reviewer 不代作這個決定，記為 **Q-ALT-1，required authority = Design Authority**（第 4 節）。依治理 §4.2，它是 routing signal，不是對 implementation 的 blocking finding，不延長本 cycle。

本 reviewer 的判斷只到「現行條文不成立違反、風險不成立 blocking」為止。DA 若裁決這類項目也必須停止，那是 CL-R1-17 的 clarification，後續依治理 §4.5、§5.3 處理，不由本 record 決定。

## 2. R1-F1：RESOLVED 成立

- `snapshot.py:238` 先檢查 `trip_type` 是字串且在列舉值內，`:264` 只有成立時才查 `LEG_DIRECTIONS`；`store.py:142`～`145` 另把驗證過程的 `TypeError`／`ValueError`／`RecursionError` 轉成 `SnapshotIntegrityError`。
- 探測 A：`trip_type` 換成 `[]`、`{}`、`[["one_way"]]`、`{"one_way": 1}`、`1`、`1.5`、`null`、`true`、`"x"` 九種值。每一種：`validate_snapshot` 回報 `$.trip_type` 的欄位錯誤（沒有拋例外）；`put` 是 `SnapshotValidationError`；壞檔寫入暫存目錄後，`load`、`find_reusable`、`select_snapshot_mode` 都是 `SnapshotIntegrityError`（目錄中另有同一請求的合格快照，沒有被改用）；`select_strict` 以壞檔位元組實算的 SHA-256（等於 `file_sha256`）得到 `StrictModeStop(reason='invalid_snapshot')`，`__cause__` 為 `None`；壞檔位元組不變。`build_snapshot` 直接給 `[]`、`{}`：`SnapshotValidationError`。
- 探測 A 後半：頂層不是物件的 JSON（`[]`、`"x"`、`1`、`null`、`true`）、空物件、`legs` 型別錯誤、非 UTF-8、`NaN`、重複鍵、十萬層巢狀，經 `_parse_snapshot_bytes` 全部是 `SnapshotIntegrityError`。
- 探測 C：對 `one_way` 與 `round_trip` 合成快照的每一個節點（含巢狀）逐一換成 18 種 JSON 值，共 2466 個案例；`validate_snapshot` 全部回傳清單，`_parse_snapshot_bytes` 只出現 `SnapshotIntegrityError` 或成功，沒有其他例外型別。沒有發現 R1-F1 的同類位置。

## 3. D-14-14：R2 的判斷成立

- 範圍：`store.py:180`～`194`，`put` 的 `path.exists()` 與寫入的 `OSError`（`FileExistsError` 除外）轉成不含路徑的 `SnapshotStoreError`（`from None`）。它與 R1-F2 是同一個缺陷類別（同一個 store 的 I/O 邊界把帶路徑的 OS 例外原樣丟出，R1-F2「影響」段、H-2），不是無關的 scope expansion 或重新設計（治理 §4.4）。
- DA record 第 8.1 節的「不得修改 `put`、`load`、壞檔處理」是該節標題所示「R1 派工之前」CL-R1-16 修改的封閉清單；R1-F2 本身就要求修改 `load` 與壞檔處理，所以它不限制 R1 之後的 targeted correction。
- 探測 B 第 9 項：`open` 的 EACCES、ENOSPC 與 `exists` 的 EACCES 都是 `SnapshotStoreError`，traceback 不含標記字串，目錄內容不變；`exists()` 回 `False` 而檔案已在（exclusive-create 的競態）時 `FileExistsError` 仍走內容比對，`created=False`、沿用舊檔的 `fetched_at`，舊檔位元組與 mtime 不變；一般的新增與重複寫入結果不變。完整 pytest 通過（第 5 節）。沒有發現 regression。
- 介面事實（不是 finding）：`put` 的 I/O 失敗現在是 `SnapshotStoreError`（基底類別，不是 `SnapshotIntegrityError`）。CL-R1-17 對 R1-4 的要求只寫了 `SnapshotIntegrityError`；#16 遇到寫入失敗時怎麼處理，屬 #16 與 DA（NV-INTEGRATION）。

## 4. Non-blocking 項目與 routing

| ID | 內容 | Severity／blocking | Owner 與 disposition |
| --- | --- | --- | --- |
| **Q-ALT-1** | CL-R1-17（與 D-14-7「只處理名稱符合的檔案」）沒有寫到的情形：(a) 已列舉、狀態查詢時已不存在的項目；(b) 名稱符合但不是一般檔案的項目（子目錄；失效或循環的符號連結）；(c) 同一個「消失」事件在狀態查詢時被略過、在讀取時停止，兩者不一致。現況：(a)(b) 不成為候選，選取照其餘快照進行。請 DA 決定維持現況，或把 CL-R1-17 延伸到這些項目 | 契約語義的 routing signal（治理 §4.2）；不是 blocking finding | **Required authority = Design Authority。** 不是 #14 audit closure 的條件，不延長本 cycle。R1-4（#16）使用同一組選取函式，建議在 #16 的派工內容定案前、最晚在 SPEC-R1 的 Spec Integration Audit 前取得裁決；時點由 Orchestrator 依 routing 規則決定 |
| **ALT-N1** | Worklog 第 10.1 節「沒有任何路徑會略過壞檔、回傳 `snapshot_missing`／`None` 或改選其他快照」與第 10.3 節 H-4「列出後消失……都以 `SnapshotIntegrityError` 停止」，對讀取時的消失成立，對狀態查詢時的消失不成立；對應的測試以 lambda 取代 `snapshot_ids`，沒有涵蓋後者（R2 已指出）。陳述比證據寬 | Low／non-blocking | Owner：#14 Executor。在結案的 worklog 更新（record-only）把這兩句改成與實際行為一致，並引用本 record 與 Q-ALT-1；不需要修改程式或測試，除非 DA 對 Q-ALT-1 另有裁決 |
| R1-N1 | Worklog 中仍引用先前的手寫範例座標 | Low／non-blocking（R1、R2 既有） | 沿用：併入 C-14-6，owner acceptor。本 review 沒有重審，也不重印該數值 |

## 5. 實際執行的檢查

全部在 worktree `cx14r2`（`git rev-parse HEAD` ＝ `c7976b5d…`）以 `./.venv/Scripts/python.exe`（3.11.2）執行；探測以 stdin 傳入，沒有寫入任何追蹤中的檔案。

| 檢查 | 結果 |
| --- | --- |
| `git log --format='%h %s' --name-only deb808d..5aabd31` | 實作／測試只在 `aa42392`、`366866c`、`5eee704`、`359b948`；其餘只改 `docs/governance/records/**` |
| `git diff 532c096..c7976b5 -- src/moto_copilot/routing/snapshot.py src/moto_copilot/routing/store.py`（全文閱讀）；`store.py` 全文、`tests/test_routing_store.py:540`～`719`、`tests/routing_synthetic.py` 全文 | Correction 的內容如第 1.1、2、3 節所述 |
| `git show <c>:src/moto_copilot/routing/store.py` 對 `aa42392`、`366866c`、`532c096` 比對 `is_file()` | 三者第 206 行都有 `and entry.is_file()` |
| `python -m pytest -q -rxX -p no:cacheprovider`（`PYTEST_DEBUG_TEMPROOT` ＝ worktree 內 `.venv/tmp`；輸出導到 scratchpad 檔以取得 pytest 自己的 exit code） | **exit 0；`1441 passed in 28.77s`**；輸出中 `xfail`／`xpass`／`skipped`／`error`／`failed` 0 筆。較早一次以管線執行的結果是 `1441 passed in 29.88s`，那次印出的 exit code 是 `tail` 的，不採用 |
| `python -m pytest -q -p no:cacheprovider tests/test_routing_store.py tests/test_routing_snapshot.py -k "r1_f1 or r1_f2 or broken_file or cl_r1_16 or s75 or s86 or s74"` | `334 passed, 228 deselected in 0.99s` |
| 探測 A（R1-F1：九種 `trip_type` 值 × validator／`put`／`load`／兩種一般選取／strict 實算 SHA；12 種壞文件經 `_parse_snapshot_bytes`） | 如第 2 節；全部是契約指定的例外，沒有其他例外型別 |
| 探測 B（R1-F2：真實刪除的兩種競態、只有一個檔案、名稱符合的子目錄、六種 `stat` 錯誤、三種讀取錯誤 × 一般選取／`load`／`file_sha256`／strict、`iterdir` EACCES、`put` 的三種 OS 錯誤與 exclusive-create 競態） | 如第 1.1、1.2、3 節 |
| 探測 B 第 5 項：失效的符號連結（真實檔案系統） | **NOT RUN**：`os.symlink` 失敗（WinError 1314，沒有建立符號連結的權限）。以 `stat` 的 ENOENT、ELOOP 替身代替，見 NV-SYMLINK |
| 探測 C（R1-F1 的獨立 sweep，2466 個案例） | 非契約例外 0 筆 |
| `Path.is_file` 的原始碼與 ENOENT／EACCES／EIO 行為：本機 Python 3.11.2 與 3.12.14（`-I`，只用標準庫與替身，不碰任何檔案） | 兩版相同：ENOENT → `False`；EACCES、EIO → 拋出。`_IGNORED_ERRNOS` ＝ (2, 20, 9, 10062)，`_IGNORED_WINERRORS` ＝ (21, 123, 1921) |
| `sha256sum`：Issue 原文、R1 record、R2 record（worktree 與主 checkout 各一） | Issue 原文同派工所述；R2 record 兩處相同（`fb6573d6…`），等於 run record 事件 74 所記 |
| 審查後 `git status --short`（worktree；主 checkout 在寫本 record 之前） | Worktree 只有 `?? docs/governance/records/audit/issue-14-c1-r2.md`；主 checkout 為空 |

## 6. NOT VERIFIED 與 required authority

| ID | 項目與原因 | Required authority |
| --- | --- | --- |
| NV-B1 | 本次 Alternate 派工的實際 (model, effort) 與全部 assistant 訊息的集合；run record 尚無本次事件。Executor 與 Primary 的 binding 也只引用派工者在 run record 的核對紀錄，本 reviewer 沒有讀 transcript 或 rollout（在允許的讀取範圍之外） | 派工者／Orchestrator（Bindings 第 3.6 節），採用本 record 前核對並記入 run record |
| NV-SYMLINK | 名稱符合的失效符號連結在真實檔案系統上的行為：沒有建立符號連結的權限，未執行。第 1.2 節對它的描述來自 `stat` 替身，不是實測 | 併入 Q-ALT-1（Design Authority）；需要實測時由 Executor 在有權限的環境提供 evidence |
| NV-PY313 | Python 3.13 以後的 `Path.is_file()`。本 reviewer 的印象是 3.13 起它改以 `os.path.isfile` 實作，會把全部 `OSError` 當成 `False`；若屬實，第 1.1 節最後一列（`stat` 的 EACCES、EIO 會停止）在 3.13 以後不成立，存在但無法查詢狀態的檔案也會不成為候選。本機只有 3.11、3.12，**沒有驗證**；`DESIGN.md` §10 沒有寫 Python 版本，`pyproject.toml` 不在本次允許的讀取範圍。本 record 的判斷只對受審環境（`.venv`，Python 3.11.2）成立 | 併入 Q-ALT-1（Design Authority：是否需要固定支援的 Python 版本，或不依賴 `is_file()` 的錯誤處理） |
| NV-PRIV | 沒有讀任何私有騎乘資料、住家位置或保留行程；沒有授權路徑，本票也不需要。C-14-6／R1-N1 的歷史處置不在本 review 範圍 | acceptor（RB-7；歷史處置另涉 RB-6） |
| NV-INTEGRATION | #15、#16、凍結清單的檔案格式（TI-C14-5）、E2／Demo Runner 與端到端整合不在本 review 範圍，沒有執行。#16 對 `SnapshotStoreError`（`put` 的 I/O 失敗）的處理未規定 | Design Authority 與後續 Ticket 的 Reviewer |
| NV-SCOPE | 本 review 只判斷 R2 後剩餘的 finding、R1-F1 的 RESOLVED 與 D-14-14，沒有重跑完整 R1，沒有重審 R1 record 判為符合的各項 AC，也沒有重做 Executor 的突變檢查 M1～M19 | —（治理 §4.4 的範圍） |

## 7. 沒有做的事

沒有修改或 stage 任何檔案（本 record 除外）；沒有重新設計，沒有作 Final Adjudication，沒有代 Design Authority 裁決 Q-ALT-1；沒有提出 capability escalation（本專案不採用 E-AR；證據與分析足以判定剩餘的 finding）。本 record 不宣告 Ticket closure、SPEC-R1 的 Spec Integration Audit、AB 的整體驗收或任何 E1 Lite／E2 的結果；audit closure 不豁免治理 §3.8 的其他完成條件。

VERDICT: CLOSURE
