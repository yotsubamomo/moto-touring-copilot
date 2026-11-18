# Decision record — Q-ALT-1：一般選取對「名稱符合但無法作為快照讀取」的目錄項目（CL-R1-20）；R1-4 對存放錯誤的處理（CL-R1-21）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue14-qalt1`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 第 6 節事件 75 之後）。問題來自 #14 cycle 1 Alternate Independent Review（`docs/governance/records/audit/issue-14-c1-alt.md`，`VERDICT: CLOSURE`）的 **Q-ALT-1**（required authority = Design Authority），併入 NV-SYMLINK、NV-PY313，並處理同一 record 的 NV-INTEGRATION 中屬 #16 的部分 |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-R1 v1（`derivation-spec-r1.md`）的 clarifications **CL-R1-20、CL-R1-21**，治理 §5.3 第 2 類。與 CL-R1-1～CL-R1-19 並列引用；CL-R1-20 是 CL-R1-17（`decision-20261118-issue14-c141.md` 第 5 節）的 clarification，不取代它 |
| Subject 基準 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `3b2b14d1febe7e97f5cf45d602d021d97c682c4a`；#14 最後的 implementation subject `359b948`（cycle 1 的受審 subject `c7976b5`，其後只有 record-only commit）；開始與結束時 `git status --short` 為空（本 record 除外） |
| 依據的條文 | 治理 §1.2、§2.4、§2.5（E-DA）、§3.6-A、§3.8、§4.2、§4.3、§4.4、§5.3；Bindings m3 第 2.6 節（RB-7）、第 3.2 節（E-DA）、第 7 節；`derivation-spec-r1.md` 第 4 節（CL-R1-3、CL-R1-4）、第 5 節 R1-2 列與 R1-4 列、第 6 節（SR1-AC2、SR1-AC3）；SPEC-001 §2 ID 列、7.11 第 1、3 項、第 9 節 S15、S17、S35、S74～S77、S86；`decision-20261117-high-risk-categories.md` 第 3.3、3.4、5 節（H-3、H-4）；`decision-20261118-issue14-c141.md` 第 3、5、7.2、8 節（CL-R1-15、CL-R1-17、CL-R1-19） |
| 讀過的證據 | Alternate record 全文；R2 record 全文；R1 record 的 R1-F2 段（經 R2、Alternate 引用與重讀）；`decision-20261118-issue14-c141.md` 全文；`src/moto_copilot/routing/store.py` 全文；`tests/test_routing_store.py` 第 590～719 行；`pyproject.toml`；worklog `issue-14.md` 的 D-14-8、第 6、10 節相關列；run record 事件 70～75；`derivation-spec-r1.md` 第 4～6 節；SPEC-001 §2、7.11 第 1～3 項、第 9 節相關 S；高風險 record 第 3.3、3.4、5 節；`decision-20261118-issue10-c107.md` 第 7 節（審後變更的 audit coverage 先例）；治理本文 §1.2、§2.4、§2.5、§3.6、§3.8、§4.2～§4.4、§5.3。Issue #14 原文（scratchpad `issue-14-body.md`，SHA-256 重算 `f7a83732c3b65001e170e8a337ada636f8a984f908b41743d033519a95ca7b75`，與派工所述相同）；`issue-16-body.md`（SHA-256 `105fdc981b1087b60b419690168d205064853a1a41ccde4a6cb092b6ffa8ede1`）的範圍列 |

本 record 撰寫時實際執行的（不讀 GPX、不需金鑰；探測以 stdin 執行、只用 `tests/routing_synthetic.py` 的合成快照與 `tempfile` 暫存目錄，沒有寫入 repo）：

| 指令／探測 | 結果 |
| --- | --- |
| `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`（HEAD `3b2b14d`，輸出導到 scratchpad 檔以取得 pytest 自己的 exit code） | exit 0；`1441 passed in 29.84s` |
| `.venv/Scripts/python.exe -V`；`py -0p` | 受審環境 Python 3.11.2；本機另有 3.12.14；**沒有 3.13 以後的直譯器** |
| 暫存目錄：存一個合格快照，另建名稱 `SN-ffffffffff.json` 的**子目錄**（真實檔案系統） | `snapshot_ids()` 只有合格快照；`select_snapshot_mode` 回傳合格快照，子目錄被略過、沒有停止 |
| 同一目錄：替身讓合格快照的 `Path.stat` 拋 `PermissionError(EACCES)` | 3.11.2：`SnapshotIntegrityError`（與 Alternate 第 1.1 節相同） |
| 名稱符合的子目錄：`stat.S_ISREG(os.stat(...).st_mode)`、`read_bytes()`；不存在的名稱：`os.stat` | `False`；`PermissionError`（errno 13，Windows）；`FileNotFoundError` |
| 替身讓 `os.stat` 拋 `PermissionError(EACCES)` 後呼叫 `os.path.isfile` | 3.11.2 回傳 `False`（`genericpath.isfile` 把 `OSError` 當成 `False`）。`Path.is_file()` 在 3.13 以後是否改用它：**NOT VERIFIED**（沒有 3.13 直譯器，不連網） |
| `grep` `src/`：`snapshot_ids`、`is_file` | `snapshot_ids` 只在 `store.py`（`snapshots()` 使用）；`is_file` 在 routing 只出現在 `store.py:233` |

沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有讀或執行 `experiments/`，沒有使用 `git status --ignored`，沒有呼叫 GitHub，沒有派工任何 subagent，沒有 commit。

---

## 1. 問題

`store.py:229`～`236` 的 `snapshot_ids()` 以 `_FILE_NAME.fullmatch(entry.name) and entry.is_file()` 篩選目錄列舉的項目。`Path.is_file()` 在狀態查詢得到「不存在」類錯誤時回傳 `False`，所以下列項目不成為候選，一般選取照其餘快照進行（改用較舊的快照，或回 `None`／`snapshot_missing`）：

- **(a)** 已列舉、狀態查詢時已不存在的項目（外部在列舉與查詢之間刪除）；
- **(b)** 名稱符合快照代號、但不是一般檔案的項目：子目錄、失效或循環的符號連結（以及 POSIX 的 FIFO、裝置檔等特殊檔）；
- **(c)** 狀態查詢的其他 `OSError`：3.11／3.12 的 `Path.is_file()` 對 EACCES、EIO 拋出，現行實作因此停止；若 Python 3.13 以後的 `Path.is_file()` 把全部 `OSError` 當成 `False`（NV-PY313），這些項目也會被略過。

同一個「消失」事件在狀態查詢時被略過、在讀取時停止（`snapshots()` 第 245～249 行），兩者不一致（Alternate Q-ALT-1 (c)）。要裁決的是 CL-R1-17 是否延伸到 (a)(b)(c)。

## 2. 依據

1. **CL-R1-17 的主體與理由。** 條文：名稱符合、但「讀不到、不是合法快照、內容不符」的檔案使一般選取停止，不略過。理由：快照寫入一次、不修改（7.11 第 1 項），壞的項目表示損毀或被改動；略過它可能讓選取結果變成另一個（較舊的）快照而不被發現；後果「一個壞檔會擋住該目錄的所有規劃，直到騎士處理」。條文判斷的對象是「以快照代號命名、卻無法作為快照讀取的目錄項目」。程式只以 `open(..., "xb")` 建立一般檔案（`store.py:186`），從不建立子目錄、符號連結或特殊檔，也不刪除檔案；存放沒有索引（7.11 第 1 項，CL-R1-3），目錄裡名稱符合的項目就是存放的全部內容。
2. **(b) 屬於 CL-R1-17 的理由範圍。** 名稱符合的子目錄或失效的符號連結是持續的狀態，不是一瞬間的競態；它不是程式產生的，表示目錄被改動或損壞；它也確實「讀不到」（探測：子目錄的 `read_bytes()` 是 `PermissionError`）。若它取代了原本最新的快照（例如備份還原錯誤、把檔案改成連結而目標遺失），略過它就使選取變成較舊的快照而不被發現——正是 CL-R1-17 所防的情形；而因為它持續存在，停止會讓騎士得知並處理。現行行為只因為篩選用了 `is_file()` 才把它排除，篩選條件並不是 CL-R1-17 或 D-14-7（「只處理名稱符合的檔案」，指名稱）所要求的。
3. **(c) 屬於 CL-R1-17 的「讀不到」。** 狀態查詢的 EACCES、EIO 表示存放無法讀取，與讀取時的同一錯誤（已轉成 `SnapshotIntegrityError`，R1-F2）及「目錄無法列舉」（已停止）是同一類。若被略過，一般的 Snapshot Mode 會回 `snapshot_missing`——CL-R1-17 明文禁止把這類原因呈現為 `snapshot_missing`。例如 POSIX 上目錄有讀取權限而沒有搜尋權限時，列舉成功、每個項目的 `stat` 都是 EACCES：在吞下 `OSError` 的語義下，整個存放會被當成空的。H-4（高風險 record 第 5 節）：失敗路徑的結果不得是預設值；`snapshot_missing` 與 `None` 在這裡就是以「沒有快照」代替「讀不到」。
4. **NV-PY313 與支援的 Python 版本。** `pyproject.toml` 宣告 `requires-python = ">=3.11"`，沒有上限；`DESIGN.md`、`README.md` 沒有寫 Python 版本（`grep` 無命中）。所以 3.13、3.14 在本專案宣告的支援範圍內，(c) 的結果不得取決於直譯器版本。NV-PY313 本身仍無法在本機驗證，但不需要驗證它才能裁決：只要選取路徑不使用會把 `OSError` 轉成布林值的判斷式，結果就與版本無關。探測已確認 3.11.2 的 `os.path.isfile` 會把 EACCES 當成 `False`，因此「改用 `os.path.isfile`」也不是可接受的做法。
5. **(a) 本身沒有可防的風險，但不能與 (b) 分開處理。** 同意 Alternate 第 1.3、1.4 節的事實：程式不刪除快照；狀態查詢前的刪除與「呼叫之前就刪除」得到相同的結果，而後者是契約接受的目錄狀態；停止並不能保住什麼。本 Design Authority 對 (a) 的裁決**不以「(a) 是風險」為理由**，而是：
   - 跟隨符號連結的狀態查詢對「失效的符號連結」（(b)）與「檔案已被刪除」（(a)）得到同一個 `FileNotFoundError`；要把兩者分開，需要另一次不跟隨連結的查詢（`lstat`），它本身又有同樣的競態。為了讓一個只發生在外部刪除與列舉同時進行時的情形改走另一條路而增加這段邏輯，不值得。
   - 讀取時的消失現已停止（`snapshots()` 第 249 行，R1-F2 的修正，R2 與 Alternate 都判為已解決）。(a) 也停止，同一個事件就只有一種結果，消除 Q-ALT-1 (c) 的不一致；改為兩者都略過則要修改已審過的 fail-closed 行為。
   - 代價有界：只在外部刪除與一次規劃的列舉重疊時發生，停止一次，下一次規劃照常（目錄已不含該項目）。它不是 fail open，也不會採用任何未經驗證的內容。這與 CL-R1-15 的情形不同：那裡的 fail closed 會讓一個無害且持續的狀態（同時最晚）每次都擋住規劃。
6. **不構成 E-DA/D1。** (b)(c) 由 CL-R1-17 的條文與理由、SPEC-001 7.11 第 1 項與 H-4 可以裁決。(a) 的兩種做法（停止或略過）都不違反契約、都不是 fail open，後果只差在一個暫時的競態中是否停止一次，不是「實質不同的後果」；第 5 點的理由足以選定其一。**不構成 E-DA/D2。** CL-R1-17 沒有被 FA ruling 推翻，也沒有被任何 finding 以證據爭議其內容：R2 與 Alternate 的分歧是 CL-R1-17 是否涵蓋它沒有寫到的情形，Alternate 明確把這個範圍問題 route 給 Design Authority（治理 §4.2）。

## 3. 裁決（CL-R1-20）

**CL-R1-20（R1-2；CL-R1-17 的 clarification）。** 一般模式與一般的 Snapshot Mode 的選取邊界（`snapshots()`、`find_reusable`、`select_snapshot_mode`）適用下列規則：

1. **候選的範圍只以名稱決定。** 存放目錄列舉出的項目中，名稱完全符合 `SN-[0-9a-f]{10}.json` 的每一個項目都是候選，不以「是不是一般檔案」「狀態查詢是否成功」先行篩除。名稱不符合的項目照舊忽略（D-14-7 不變）。
2. **每個候選都必須讀成合格的快照，否則停止。** 候選在選取過程中出現下列任一情形，選取以 `SnapshotIntegrityError` 停止，不略過、不改選其他快照、不回傳 `None` 或 `snapshot_missing`：
   - (a) 狀態查詢或讀取時已不存在（`FileNotFoundError`，含失效的符號連結）；
   - (b) 不是一般檔案（跟隨符號連結之後；子目錄、FIFO、裝置檔等），或符號連結循環；
   - (c) 狀態查詢或讀取的任何其他 `OSError`；
   - 以及 CL-R1-17 原有的情形（不是合法 JSON、不是合法快照、`snapshot_id` 與檔名或內容雜湊不符）。
3. **版本無關。** 選取路徑不得使用會把 `OSError` 轉成布林值的判斷式來決定候選或結果：`Path.is_file()`、`Path.exists()`、`Path.is_dir()`、`os.path.isfile()`、`os.path.exists()` 等（任何 Python 版本）。狀態以明確的狀態查詢（`os.stat`／`Path.stat`，跟隨符號連結）取得，錯誤由程式自己轉換。
4. **不是一般檔案的項目在讀取前就停止。** 第 2 項 (b) 的判定在開啟檔案讀取之前完成，使特殊檔不會被開啟（POSIX 的 FIFO 開啟時會阻塞）。
5. **例外的內容。** 訊息只寫 `snapshot_id`（或不寫），不含目錄路徑或檔案內容，以 `from None` 拋出（與 R1-F2、D-14-14 相同）。
6. **不變的部分。** 嚴格模式（`select_strict`）不經目錄列舉，直接讀清單指定的檔案，不在本裁決範圍：缺檔仍是 `file_missing`，其他讀取錯誤仍是 `unreadable`。直接 `load` 不存在的代號仍是 `SnapshotNotFoundError`。`put`、`SnapshotStore.__init__` 不變（見第 4.3 節）。

CL-R1-20 的效果是：一般選取的結果只取決於「列舉時名稱符合的項目是否全部讀成合格快照」；任何一個不能，就停止並交給騎士處理。

## 4. 對 #14 的具體要求

#14 尚未結案（治理 §3.8：「無影響完成的未決 design ambiguity」；Q-ALT-1 就是這一項）。CL-R1-20 對 cycle 1 的受審 subject `c7976b5` 不成立第 2 項 (a)(b) 與第 3 項，所以 #14 須在本 Ticket 內修改後才能結案。

### 4.1 可以修改的檔案與內容（封閉清單）

1. `src/moto_copilot/routing/store.py`：
   - `snapshot_ids()` 與／或 `snapshots()`：依 CL-R1-20 第 1～5 項改寫候選的取得與檢查。具體寫法是 Executor 的 HOW（例如在 `snapshot_ids()` 以 `os.stat` 加 `stat.S_ISREG` 檢查名稱符合的每個項目，`FileNotFoundError`、其他 `OSError`、非一般檔案都轉成不含路徑的 `SnapshotIntegrityError`），但不得使用第 3 項列出的判斷式。
   - 上述兩個函式的 docstring 改寫成與 CL-R1-20 一致並引用本 record（現行「Every `snapshot_id` with a file here」的寫法須改）。
2. `tests/test_routing_store.py`：新增測試（既有測試不改；不得加 xfail／skip）。存放目錄沿用 `marked` fixture 的合成標記目錄名稱，每一項都斷言 `find_reusable` 與 `select_snapshot_mode` 都是 `SnapshotIntegrityError`、不是 `SnapshotNotFoundError`，且 `assert_path_free` 成立；有另一個相容的合格快照與沒有其他快照兩種情形都要涵蓋：
   - T-1（(b)，真實檔案系統）：名稱符合的**子目錄**。
   - T-2（(a)，真實檔案系統，不替換 `snapshot_ids`）：包住 `Path.iterdir`（或實作實際使用的列舉函式），在列舉完成之後、狀態查詢之前**真的刪除**該檔案。
   - T-3（(c)）：以替身讓實作實際使用的狀態查詢對某個名稱符合的檔案拋 `PermissionError(EACCES)` 與 `OSError(EIO)`（替身要放在實作真正呼叫的函式上，使測試在任何版本都打到同一個邊界）。
   - T-4（(a)/(b) 的失效符號連結）：以替身讓狀態查詢拋 `FileNotFoundError`、`OSError(ELOOP)`，代表失效與循環的符號連結。
   - T-5：名稱不符合的項目（例如大寫十六進位、`.json.tmp`、名稱符合的前綴加其他字）仍被忽略，選取結果不變。
   - T-6（第 4 項）：以替身證明非一般檔案的項目沒有被開啟讀取（例如 `read_bytes`／`open` 的替身沒有被以該項目呼叫）。
3. `docs/governance/records/worklog/issue-14.md`：新增一節（record-only），內容見第 4.2 節；同時處理 ALT-N1：第 10.1 節「沒有任何路徑會略過壞檔……」與第 10.3 節 H-4「列出後消失……都以 `SnapshotIntegrityError` 停止」兩句，以新的一節註明它們對 `c7976b5` 比證據寬（引用 Alternate record 與本 record），並寫明在新 subject 上依哪些測試成立。不改寫既有段落的歷程內容。

不得：修改 `select_strict`、`put`、`load`、`_read`、`_parse_snapshot_bytes`、`SnapshotStore.__init__`、`canonical.py`、`request_key.py`、`snapshot.py` 或 `src/`、`tests/` 的其他檔案；修改 `pyproject.toml`（包括 `requires-python`）；修改既有測試；新增 xfail／skip。

### 4.2 Evidence（記在 `worklog/issue-14.md` 的新一節）

| # | 證據 | 要求 |
| --- | --- | --- |
| 1 | Commit | 一個與 `359b948` 分開的 implementation commit，只含第 4.1 節第 1、2 項的檔案，message 註明 CL-R1-20。它成為 #14 新的 implementation subject |
| 2 | E-1 | 新 subject 上完整 pytest 輸出（`-q` 與 `-q -rxX`），pytest 自己的 exit code 0，摘要只有 `passed` |
| 3 | 突變 | (M-a) 恢復 `and entry.is_file()` 篩選：T-1、T-2、T-4 失敗；(M-b) 改用 `os.path.isfile(...)` 篩選：T-3 失敗；(M-c) 把非一般檔案的判定移到讀取之後或拿掉：T-6 失敗（或 T-1 失敗，寫明哪一個）。記錄每個突變失敗的測試數，還原後全部通過；還原方式不得連帶還原未 commit 的修改（事件 71 揭露的失誤） |
| 4 | 版本無關 | `grep` `src/moto_copilot/routing/store.py` 的 `is_file`、`exists(`、`is_dir(`、`isfile`、`os.path.exists`，列出每個命中並說明它不在一般選取路徑上（`put` 的 `exists()`、`__init__` 的 `is_dir()`，第 4.3 節）。在 3.13 以後的直譯器上執行：MAY；沒有執行就寫 NOT RUN，不得寫成已驗證 |
| 5 | 真實符號連結 | 在有建立符號連結權限的環境以真實失效連結探測：MAY；沒有權限就寫 NOT RUN（NV-SYMLINK），由 T-4 的替身涵蓋邏輯 |
| 6 | Diff | 相對 `c7976b5` 的 diff 只含第 4.1 節列出的檔案與內容 |
| 7 | E-2 | S35（存放與選取的部分）、S77、S17 的 `snapshot_missing` 列加上 T-1～T-6，並註明 CL-R1-17／CL-R1-20 |
| 8 | H-4 | 依高風險 record 第 5 節重新陳述：(a)(b)(c) 的每一條路徑都有測試顯示是明確錯誤而不是 `None`／`snapshot_missing`／較舊的快照 |

### 4.3 不需要修改的相鄰程式（判斷）

- `SnapshotStore.__init__` 的 `path.is_dir()`：若被當成 `False`，結果是 `SnapshotStoreError`（停止），不是 fail open。
- `put` 的 `path.exists()`：若錯誤被當成 `False`，接著的 `open(..., "xb")` 會因檔案存在而得到 `FileExistsError` 並走內容比對，或得到其他 `OSError` 而成為 `SnapshotStoreError`；不會覆寫，也不會把失敗當成成功。`test_r1_f2_put_errors_carry_no_path_and_write_nothing` 以替身取代 `Path.exists` 本身，在各版本都打到同一個邊界。
- 嚴格模式：見 CL-R1-20 第 6 項。POSIX 上清單指定的檔名若是 FIFO，`read_bytes` 會阻塞；這不是 fail open，專案的執行平台是 Windows，嚴格模式的修改也不在 Q-ALT-1 的範圍，本 record 不要求修改，也不列為 tracked item。

### 4.4 Audit coverage（治理 §3.8、§4.4）

#14 cycle 1 已由 Alternate Review 達成 audit closure（subject `c7976b5`），那個結論不因本 record 改變：它判斷的是當時的契約。第 4.1 節的修改是 audit closure 之後由 Design Authority 的 clarification 帶來的變更，不是 cycle 1 的 targeted correction，也不是 R3。治理 §3.8 規定審後變更需要相應的驗證、必要的後續由 Reviewer／Design Authority 判定；高風險 record 第 3.4 節 (a) 要求 H-4 程式的結案後修正經 independent audit。本 record 判定：

1. CL-R1-20 的 delta 以 **#14 cycle 2** 審查：R1 是對該 delta 的完整獨立審查，範圍是第 3 節 CL-R1-20 的各項、第 4.1 節的修改與測試、第 4.2 節的 evidence、`store.py` 一般選取路徑的回歸（CL-R1-15、CL-R1-16、CL-R1-17 與 R1-F1、R1-F2 的既有行為），以及 H-2（例外不含路徑）、H-4。它不重審 cycle 1 已 closure 的其他 AC，不是無限制的全面 audit。之後依治理 §4.4（blocking → targeted correction → R2 → exactly one Alternate → Final Adjudication）。
2. Cycle 2 R1 的派工內容須含本 record、`decision-20261118-issue14-c141.md` 與 Alternate record；Reviewer 不得把「改用 `os.path.isfile` 或其他吞下 `OSError` 的判斷式」記為可接受的實作。
3. 派工時機與 Reviewer 的選擇由 Orchestrator 依 Bindings 決定。

## 5. 對 R1-4（#16）的要求（CL-R1-21）

**CL-R1-21（R1-4；CL-R1-17、CL-R1-20 的延伸要求，併入 #16 的派工）。**

1. **選取的例外照 CL-R1-17 向上傳遞。** CL-R1-20 使 `SnapshotIntegrityError` 也來自已消失、非一般檔案與狀態查詢失敗的項目。R1-4 不得依例外的訊息或成因分辨處理；不論哪一種，都不得攔下後改用其他快照、改呼叫路線引擎、重試選取，或轉成 `snapshot_missing`／`routing_unavailable`／其他路線錯誤代碼。重試選取在競態下等於改用其他快照，同樣禁止。
2. **只經 R1-2 的選取函式。** R1-4 取得快照只經 `find_reusable`、`select_snapshot_mode`、`select_strict`；不得自己列舉存放目錄、呼叫 `snapshot_ids()`／`snapshots()` 篩選候選，或以 `exists()`／`is_file()` 等判斷式先行檢查快照檔。
3. **存放的其他錯誤也停止。** `put` 的失敗（`SnapshotConflictError`，以及寫入或狀態查詢失敗的 `SnapshotStoreError`，D-14-14）與 `SnapshotStore` 建構時的 `SnapshotStoreError`，R1-4 都讓它向上傳遞：不回傳未存檔的路線，不轉成 `routing_unavailable` 或其他路線錯誤代碼，不改寫到其他目錄。理由：7.11 第 3 項 (c) 的採用與存檔是同一步（「每個方向都通過三項檢查才採用並存檔」）；7.11 第 1 項要求結果記錄的 `snapshot_id` 指向已保存的快照，騎士之後才能以 Snapshot Mode 重現（S15 的「騎士可以切到 Snapshot Mode」）；未存檔就回傳，結果中的 `snapshot_id` 會指向不存在的檔案。這是既有條文的唯一合理解讀（治理 §3.6-A），回應 Alternate 的 NV-INTEGRATION 中「#16 對 `SnapshotStoreError` 的處理未規定」。
4. **嚴格模式的 `StrictModeStop`** 照 CL-R1-4 向上傳遞，不回退（不變）。
5. **例外訊息與 log** 不含存放目錄的路徑或檔案內容（CL-R1-17 不變）。向騎士顯示的文字仍屬之後的整合 Spec（`decision-20261118-issue14-c141.md` 第 7.3 節）。
6. **#16 的證據。** 以替身或合成存放證明：(i) 一般模式的選取拋 `SnapshotIntegrityError` 時，傳輸層沒有被呼叫，例外原樣傳出；(ii) 一般的 Snapshot Mode 同一情形不回 `snapshot_missing`；(iii) `put` 拋 `SnapshotStoreError`／`SnapshotConflictError` 時沒有回傳路線、沒有路線錯誤代碼、例外不含路徑。
7. **派工時機。** #16 的派工內容須含本 record 與 `decision-20261118-issue14-c141.md`。#16 依賴 R1-2，派工時 R1-2 的介面以 #14 cycle 2 的結果為準；#16 不依賴 CL-R1-20 的實作細節，只依賴「選取失敗一律是 `SnapshotIntegrityError`」這個介面，所以 Orchestrator MAY 在 #14 cycle 2 完成前派 #16，但 #16 的結案與 SPEC-R1 SIA 須以 #14 的最終 subject 為準。

## 6. 對 SPEC-R1 Spec Integration Audit 的影響

- SR1-AC2：整合路徑上，一般模式與 Snapshot Mode 遇到 CL-R1-20 的任一情形時停止並傳出 `SnapshotIntegrityError`，R1-4 沒有攔下（CL-R1-21 第 1、2 項）；`put` 的失敗沒有被轉成路線結果或路線錯誤（第 3 項）。
- SR1-AC3：「不採用的情形都不存快照」照舊；另核對存檔失敗時沒有產生路線。
- SIA 不得把下列項目記為已涵蓋：3.13 以後直譯器上的實際執行（NOT RUN，除非 #14 第 4.2 節第 4 項有證據）；真實失效符號連結（NV-SYMLINK，除非有證據）；向騎士顯示的壞檔文字（之後的整合 Spec）；TI-C14-1、TI-C14-5、RV-8、RV-9、RV-10。

### 文字同步（併入 first-run derivation 第 7 節的清單；不是任何裁決生效的條件）

| 代號 | 位置 | 建議 |
| --- | --- | --- |
| RV-10 | SPEC-001 7.11 第 3 項的狀態欄 | 註明 CL-R1-17、CL-R1-20：一般選取遇到名稱符合而無法讀成合格快照的項目時停止；CL-R1-21：R1-4 不攔下存放錯誤 |

Owner 與時機同 RV-6～RV-9：Design Authority，最早在 SPEC-R1 phase acceptance 之後，於 AB-12 的文件工作中執行。

## 7. 是否改變 accepted 語義、boundary、authority、escalation

- **是否改變 accepted 語義：否。** CL-R1-20 是本 Design Authority 先前的 CL-R1-17 的 clarification：(b)(c) 落在 CL-R1-17 的條文（「讀不到」）與理由之內，(a) 以規則一致與不可區分為由一併停止；CL-R1-21 是 7.11 第 1、3 項與 CL-R1-17 對 R1-4 的唯一合理解讀。都不改變 OC-1 的 intent、scope、constraints 或 acceptance semantics，不新增 Must、requirement 或 AC（治理 §5.3 第 2 類）。它們不建立新的設計基線：#16 依賴的介面（選取失敗是 `SnapshotIntegrityError`、存放失敗是 `SnapshotStoreError`）不變。
- **Boundary：在 OC-1 boundary 內。** 屬 OC-1 §2.1 第 1 項（`routing`）與 SPEC-R1 已分配的 AB-1、AB-2、AB-11、AB-13 部分（`derivation-spec-r1.md` 第 7 節）；沒有恢復 Scope Reduction。
- **需要 acceptor：否**（本 record 的各項裁決）。C-14-6 仍保留給 acceptor，本 record 不處理。
- **Escalation：沒有。** 不是 E-DA/D1，也不是 D2（第 2 節第 6 點）。
- **對 cycle 1 結論的關係。** 本 record 不推翻 Alternate 的 `VERDICT: CLOSURE`，也不改判 R2 的 finding；那是 Reviewer 對當時契約的判斷，屬 Reviewer 的權限。本 record 只決定契約語義，並依治理 §3.8 判定審後變更的 audit coverage（第 4.4 節）。

## 8. 受影響的 work items 與 evidence

| Work item／evidence | 影響 |
| --- | --- |
| #14（R1-2） | 依第 4 節修改；新的 implementation subject 取代 `359b948`；cycle 1 的 evidence（E-1 的 1441 passed、R1-F1／R1-F2 的測試與探測）保留為歷程，在新 subject 上以第 4.2 節重新取得 E-1。CL-R1-20 的 delta 以 cycle 2 審查（第 4.4 節）。ALT-N1 由第 4.1 節第 3 項處理 |
| #16（R1-4） | 派工內容加入本 record；CL-R1-21 的要求與證據（第 5 節） |
| #15（R1-3） | 不受影響（不經快照存放） |
| SPEC-R1 SIA | 第 6 節 |
| 高風險類別 | R1-2（H-2、H-3、H-4）與 R1-4（H-1、H-2、H-4）的標示不變 |
| NV-PY313、NV-SYMLINK | 不再影響契約判斷：CL-R1-20 第 3 項使結果與版本無關，T-4 以替身涵蓋失效連結；兩者的實測仍是 NOT VERIFIED，除非第 4.2 節第 4、5 項提供證據 |

`derivation-spec-r1.md` 與先前的 CL records 沒有被修改；SPEC-R1 v1 的引用集合由本 record 補上 CL-R1-20、CL-R1-21。

Decision: Q-ALT-1 — CL-R1-20。CL-R1-17 延伸到 (a)(b)(c)：名稱符合的每個目錄項目都是候選，任何一個不存在、不是一般檔案、狀態查詢或讀取失敗，一般選取都以不含路徑的 `SnapshotIntegrityError` 停止；不得使用吞下 `OSError` 的判斷式。#14 在本 Ticket 內修改（第 4 節），以 cycle 2 審查該 delta。CL-R1-21：R1-4 讓選取與存放錯誤向上傳遞。不改變 accepted 語義；在 OC-1 boundary 內；不需要 acceptor；沒有 escalation。
