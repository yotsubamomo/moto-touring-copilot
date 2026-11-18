# Issue #14 — cycle 2 R1 independent audit（delta audit）

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37a`）→ SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md` §2、§4 DD-R1-1／DD-R1-2、CL-R1-1～CL-R1-10、§5 R1-2 與 E-1～E-6）＋CL-R1-13（`decision-20261118-issue13-c131.md`）＋CL-R1-14～CL-R1-17（`decision-20261118-issue14-c141.md`，含 §8）＋CL-R1-20／CL-R1-21（`decision-20261118-issue14-qalt1.md`）→ Issue #14 |
| BASE（cycle 2） | `c7976b5d25b0d7087b67500acc00f7d5c8f080f7`，cycle 1 最終受審 subject |
| HEAD | `6f08a5a974967568be3719dd051e8647be70e74c`；本專用 worktree 的 detached HEAD |
| Implementation subject | `665a86f1cf6b85ca84a9481b2e80d2949a8cf9d3`；`87d1eff` 更新 worklog；其餘 delta 在 record-only paths |
| Audit kind | **Ticket independent audit，R1，cycle 2（delta audit）；not a Spec Integration Audit** |
| Role／日期 | `primary_reviewer`（Codex）；2026-11-18 |
| Lane／高風險 | Formal；H-2、H-3、H-4 |

## Assurance 與獨立性

| Property | 滿足方式與證據界線 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread，沒有繼承 Executor 或前次 reviewer 對話。派工提供識別與文件入口；自行讀取契約、實作、測試、git 歷史及正式 records，將 worklog 視為待查證主張。沒有派 subagent。 |
| Verifiable binding | 依 Bindings m3 §3.3 O-6，由 dispatcher 核對本次 rollout 全部 `turn_context`、存取紀錄與自寫 record hash，記入 `docs/governance/records/run/run-20261117-oc1-run2.md` §6 的**本次「#14 cycle 2 R1／cx14c2r1／HEAD 6f08a5a」dispatch event**。截至受審 HEAD，§6 最後相關事件是 77（Executor）；沒有本次 dispatch 的事件號、thread 或 binding 欄位。事件 76 是 DA、77 是 Executor，不能充作本次 binding，也不推定下一事件號。此項待 NV-B1；不能宣稱四項 properties 已全部獲 dispatcher 實證。 |
| Autonomous access | 自行在本 worktree 讀取原始材料、查詢 git metadata、執行兩輪完整 pytest、AST 比對及 stdin 記憶體探測。沒有讀取其他 checkout 或 worktree 外的專案材料，沒有讀取、列出或搜尋 `data/`、憑證，沒有網路／GitHub 呼叫，沒有執行 `experiments/`。 |
| Self-written record | 本檔由本 reviewer 自寫，是唯一新增檔案；沒有修改實作、測試、契約、worklog 或其他 records，沒有 stage／commit。Dispatcher 應依 O-6 原樣收錄並核對 SHA-256，不得代寫或改寫 findings／verdict。 |

Model evidence：run record §6 事件 77 記載 Executor 為同一 agent `a731e697ea497fcf3`，實際觀測集合只有 (`claude-opus-5-5`, `high`)，203 則，符合 mapping。本 reviewer 是 **Codex**；Bindings §8.2 #7 的 qualified mapping 是 `gpt-6.1-sol`／`high`，但本次實際 model ID／effort／sandbox 的 dispatcher 證據尚待 NV-B1，不以規定值代替實測。**no model diversity claim（不主張 model diversity）**。正式採用本 record 作 audit gate 前須完成 NV-B1。

## 範圍與契約判準

本次依 `decision-20261118-issue14-qalt1.md` §4.4 及 run 事件 76 審查 CL-R1-20 的 delta、T-1～T-6、M-a～M-c、對一般選取的回歸與 H-2／H-3／H-4。Cycle 1 的 Alternate `VERDICT: CLOSURE` 保持其原有涵義；本次不是 R3，不重審已 closure 的其他 AC。#14 整體 BASE `deb808d` 只作歷程識別。

已核對治理本文 §2.3、§3.8、§4.1～§4.7、Bindings m3 §3.3／§5／§7、角色 definition 的「紀錄」、impl-default v2 §6／§7、orch-default v2.2 §6／§7。另讀 SPEC-R1 derivation 的引用集合、CL-R1-13～17／20／21、高風險 record §5、OC-1 的適用 boundary、first-run derivation、SPEC-001 的快照模型與 7.11、DESIGN §5 相關規則及 cycle 1 records。Issue #14 使用派工附錄原文，沒有呼叫外部服務驗證其 hash。

## Findings

沒有 blocking findings。

### C2-R1-N1 — worklog 未保留第二個 pytest 指令的完整輸出

- **Severity：Low／non-blocking。Owner：Issue #14 Executor。**
- 契約：`docs/governance/records/decisions/decision-20261118-issue14-qalt1.md:95` 要求在 worklog 收錄新 subject 上 `-q` 與 `-q -rxX` 的完整輸出。
- 證據：`docs/governance/records/worklog/issue-14.md:347` 起有 `-q` 的完整輸出；`:374` 對 `-q -rxX` 只寫 exit code、最後一行及文字搜尋結果，沒有完整輸出。`:339` 不能單獨補足這個記錄要求。
- 本次已獨立執行兩個指令，都是 exit 0、1456 passed，完整輸出附於本 record；沒有執行結果或產品行為的不確定性。因此這是 evidence 保存位置與完整性的缺口，列 Low，不以此延長 audit cycle；也不把 worklog 的全文要求標成已滿足。
- **Required fix／disposition：**在結案的 record-only worklog 更新補登完整 `-q -rxX` 輸出及其 subject／指令／exit code；若引用本 record 的重跑結果，須標明是 reviewer 在 HEAD `6f08a5a` 的重跑，不得冒充 Executor 在 `665a86f` 的歷史輸出。由 Executor 處理，Orchestrator 核對紀錄一致性；不需產品修正或另一輪全面 audit。

### 既有 disposition

ALT-N1 的更正已核對：worklog `:242`、`:300` 保留歷史文字並加上 superseded；§11.3（`:386` 起）明確區分 `c7976b5` 的 status/read 邊界，引用 Alternate 與 DA record，再以新 subject 的測試支持新陳述。`87d1eff` 只改 worklog，屬 record-only；沒有改寫 cycle 1 verdict。**ALT-N1 的 record-only required fix 已滿足。**

R1-N1／C-14-6 維持既有 Low／non-blocking disposition，owner＝acceptor；本次不重審歷史範例值、不重印其數值，也不判定是否改寫歷史。

## CL-R1-20 與 regression 判定

| 核對 | 證據與結論 |
| --- | --- |
| 名稱決定候選 | `src/moto_copilot/routing/store.py:225`～`:237`：先收集 `entry.name`，以 `_FILE_NAME.fullmatch` 決定完整名稱是否符合；不查 entry 的狀態、不先篩除非一般檔案。CL-R1-13 的完整 ASCII／小寫十六進位語義保持。T-5 亦證明其他名稱甚至不會進入 `os.stat`。 |
| (a) 消失／失效連結 | `store.py:254`～`:258`：明確 `os.stat` 的 `FileNotFoundError` 轉成 `SnapshotIntegrityError`；`:265`～`:268` 把 stat 成功後、load 時消失的 not-found 轉為相同完整性錯誤。T-2 保留實際列舉，真的刪除；T-4 模擬 ENOENT。另有本次獨立的 stat 成功後 read failure 探測。 |
| (b) 非一般檔案／循環連結 | `store.py:261`～`:264`：預設跟隨 symlink 的 `os.stat` 後用 `stat.S_ISREG` 判定，非一般檔案在 `load`／開檔之前停止；ELOOP 落入 `except OSError`。T-1 為真實子目錄；T-4 為 ELOOP；T-6 分別檢查子目錄與 FIFO-like entry 都未開啟。 |
| (c) 其他 OSError | `store.py:259`～`:260`：status EACCES／EIO 等一律轉成完整性錯誤，read 的 OSError 仍由未變動的 `_read` 轉換。目錄列舉本身的 OSError 仍在 `:235`～`:236` 停止。不是略過、預設值或 `snapshot_missing`。 |
| 不吞 OSError | 搜尋的唯一三筆是 `:159`（建構的 `is_dir`）、`:182`（put 的 `exists`）、`:248`（docstring）。前兩者依 DA §4.3 保持不變；一般選取的實際呼叫路徑是 selectors → `_matching` → `snapshots` → `snapshot_ids`／`os.stat`／`load`／`_read`，沒有以這類布林 predicates 選候選或結果。 |
| H-2：錯誤不帶路徑 | 新增三種 status/non-regular 例外都只寫 ID／固定文字，以 `from None` 拋出；沒有輸出 OSError 原文、檔案內容或 log。`tests/test_routing_store.py:612` 的 `assert_path_free` 檢查 formatted traceback、cause 與 suppress-context；T-1～T-4、T-6 及獨立 read 探測皆成立。 |
| H-4：不 fallback | `snapshots()` 先完成全部候選的讀取與驗證才回傳 list；selectors 不攔截錯誤，過濾相容性、期限與挑最新都在其後。候選錯誤不能因存在其他好快照而被忽略，也不能因沒有好快照而回缺快照結果。T-1～T-4、T-6 均有 with_good=True／False。 |
| CL-R1-15／16／17 與 R1-F1／F2 回歸 | AST 比對顯示 `_latest`、`_matching`、selectors、validation、load／parse／read 的函式內容未變；全套測試保留並通過 tie-break、30×24h 上下界、壞檔、I/O 及 malformed trip_type 案例。新 stat 防線沒有削弱內容驗證。 |
| H-3：嚴格模式 | `select_strict` AST 未變，仍只讀 frozen entry、先核對 bytes SHA-256，失敗為 `StrictModeStop`，不進一般列舉。S74／S75／S76／S86 與既有 strict regressions 全數通過。本次另以記憶體替身禁止列舉與 stat，驗證成功、file_missing、unreadable 三條分支。 |
| Write-once／直接 load／put | AST 比對確認 `__init__`、`put`、`path_for`、`load`、`_read`、`_parse_snapshot_bytes`、`file_sha256` 均未改。S53／S54／S55 的原檔 bytes／mtime 與 conflict、S36、put I/O 測試全數通過；直接 load 不存在的代號仍是 `SnapshotNotFoundError`。一般選取沒有新增寫入或刪除。 |

## 測試充分性與 E-1～E-6

| 要求 | 獨立核對 |
| --- | --- |
| E-1 | HEAD `6f08a5a` 上親自跑兩輪完整 pytest，皆只有 passed；implementation 與 `665a86f` 相同，後續僅 records。Executor 的 `-q` 全文可追溯；`-rxX` 保存缺口見 C2-R1-N1。沒有 xfail／skip 標記。 |
| E-2 | worklog §6 的 S35、S77、S17 三列已加入六個 `test_cl_r1_20_*` 全名與 CL-R1-17／20；所有原有 AC mapping 保留。本次只判定 delta 與回歸，不重新替 cycle 1 的其他 AC 作驗收。 |
| E-3 | 新測試沿用 `tests/routing_synthetic.py` 的手寫近零座標、`synthetic-shape-*`、虛構 engine／method／地標 ID，與 `marked` 合成目錄。新 diff 沒有真實軌跡、GPX 或公開地標資料，沒有對外傳送測試資料。 |
| E-4 | `test_hashing_storage_and_selection_need_no_network` 以 socket／create_connection／getaddrinfo fail-fast 替身執行；另一測試以 AST 排除網路與環境匯入。兩者本次通過；delta 只新增 stat 模組與本機目錄狀態處理。沒有使用網路。 |
| E-5 | AST 與文字 prefix 比對確認：只新增 `import stat` 與 appended tests，既有測試本文未改；沒有契約改版而修改既有測試的項目需要補理由。 |
| E-6 | 已對照高風險 record §5 及 worklog §11.4：H-2 的合成來源／metadata／錯誤隱私，H-3 的 strict／write-once／誠實標示，H-4 的失敗路徑與不 fallback 均核對如上。沒有把本機測試稱為 E1 Lite／E2 或真實資料驗證。 |

| 測試 | 本次檢查與結果 |
| --- | --- |
| T-1（`:757`） | 真實 snapshot-named directory；2 cases；兩個 selector 都停止。 |
| T-2（`:765`） | `Path.iterdir` 包裝先保存 entries 再實際 unlink，未替換 `snapshot_ids`；兩個 selector 各刪一次；2 cases。`SnapshotNotFoundError` 與 `SnapshotIntegrityError` 是 sibling classes，所以此測試的 raises 也排除前者。 |
| T-3（`:796`） | 替身命中實作真正使用的 `os.stat`，EACCES／EIO × with_good；4 cases。 |
| T-4（`:810`） | 同一個 status 邊界的 ENOENT／ELOOP × with_good；4 cases；是邏輯替身，不宣稱真實 symlink 實跑。 |
| T-5（`:819`） | 不合名稱仍忽略；對其他名稱設定 failing stat，不影響兩個 selector 的合法結果；1 case。 |
| T-6（`:843`） | 真實子目錄與 stat 回報 FIFO 的一般檔案，移除子目錄再跑一次，確保沒有被子目錄的先行停止遮蔽 FIFO；read_bytes／open 記錄沒有開啟兩者；2 cases。 |

T-1～T-6 共 15 cases，1456＝1441＋15。前三種 mutation 的獨立重跑證實測試具有偵測能力。

## 實際執行的指令與結果

全部工作目錄皆為本專用 worktree；測試只呼叫 PATH 的 `python`，沒有直接呼叫另一個環境的直譯器，也沒有更改 `PYTEST_DEBUG_TEMPROOT`。

| 指令／檢查 | 實際結果 |
| --- | --- |
| `git rev-parse HEAD`；stdin Python 以 `git rev-parse c7976b5` 核對 BASE | 分別等於表首完整 SHA；detached subject 符合派工。 |
| `git status --short`（開始、兩輪測試及探測後） | 全部空白；在建立本 record 前沒有 snapshot 檔或其他未追蹤變更。 |
| `git log --oneline c7976b5..6f08a5a`；`git log --format=fuller --name-only c7976b5..6f08a5a` | 六個 commits；唯一實作 commit 是 `665a86f`，只改 store.py／test_routing_store.py；其餘僅 `docs/governance/records/**`。 |
| `git diff --stat c7976b5..6f08a5a`；`git diff c7976b5..6f08a5a -- src/moto_copilot/routing/store.py tests/test_routing_store.py`；同範圍 worklog diff | 7 files；store +24/−9、測試 +159；其餘 records。已逐項讀取實作／測試 delta 及 ALT-N1、E-2、§11 的 record-only 變更。 |
| `git diff --check c7976b5..6f08a5a` | exit 0，無輸出。 |
| `python -m pytest -q` | exit 0；`1456 passed in 22.31s`。全文如下。 |
| `python -m pytest -q -rxX` | exit 0；`1456 passed in 17.65s`，沒有 xfail／xpass／skip 摘要。全文如下。 |
| `rg -n 'xfail\|skip' tests/` | 兩筆普通文字：`test_contracts.py:1157` docstring、`test_routing_store.py:330` 測試名稱；均非 marker。 |
| `rg -n 'pytest\.mark\.(xfail\|skip\|skipif)\|pytest\.(xfail\|skip\|importorskip)\|from pytest import.*(xfail\|skip)' tests/` | exit 1，0 matches。另以 stdin Python AST 掃描 tests 的 attribute 與 from-import，命中 0；沒有 xfail／skip markers 或執行呼叫。 |
| `rg -n 'is_file\|exists\(\|is_dir\(\|isfile\|os\.path\.exists' src/moto_copilot/routing/store.py` | 只有 `:159`、`:182`、`:248`，位置與判斷如上。 |
| `@'…'@ \| python -`：從 `git show <BASE>:…/store.py` 與 HEAD 建 AST 比對 functions／methods | 唯一改動 `SnapshotStore.snapshot_ids`、`SnapshotStore.snapshots`。其他函式未改。canonical.py／request_key.py／snapshot.py／pyproject.toml 的 git diff 為空。 |
| 同一 stdin 檢查既有測試 | 去掉 HEAD 新增的 `import stat` 後，文字以 BASE 完整內容開頭；既有測試原文未改。 |
| 同一 stdin 查詢 `git ls-files`，僅在記憶體比對禁止路徑 | `data/`、`.env`、`.gpx`、`.fit`、`.key` 命中 0；只讀 git metadata，沒有列出或讀取對應私有目錄。 |
| 同一 stdin 檢查 runtime | Python 3.11.2；`sys.executable` 位於本 worktree 內的判定為 True。沒有探查其他安裝路徑。 |
| `@'…'@ \| python -`：記憶體 mutation runner（下述方式） | M-a／M-b／M-c 的失敗數與 worklog §11.2 相符；最後復原的 store suite 84 passed。外層 script 的 assertions 全通過、exit 0。 |
| `@'…'@ \| python -`：stat 成功後 read failure 探測 | 模擬 ENOENT／EACCES／EIO／ELOOP × with_good True／False × 兩個 selector；16 次都是 path-free `SnapshotIntegrityError`，沒有 fallback。全部以合成 bytes／虛擬 worktree 內路徑，不寫檔。 |
| stdin strict regression 探測（修正 harness 後重跑） | 禁止 `snapshot_ids` 與 `os.stat`；合法 frozen bytes 成功，ENOENT → file_missing、EACCES／EIO → unreadable；全部無路徑且不 fallback。 |

診斷過程有兩次 reviewer harness 問題，沒有當作產品失敗或通過證據：(1) 一次 stdin 文件擷取因 console 的 cp950 編碼在 Unicode 字元中止，改為 `sys.stdout.reconfigure(encoding='utf-8')` 重讀；(2) strict 探測第一次在仍禁止全域 `os.stat` 時格式化 traceback，traceback 的 linecache 也用 stat，觸發替身的 AssertionError。已把 traceback 檢查移到 patch context 外，重跑上述 strict 四個案例成功。兩次皆未修改檔案。較早的完整 read-failure 16 cases 已成功，未以未完成的 strict 部分宣稱通過。

### E-1：本次完整輸出

`python -m pytest -q`，exit 0：

```text
........................................................................ [  4%]
........................................................................ [  9%]
........................................................................ [ 14%]
........................................................................ [ 19%]
........................................................................ [ 24%]
........................................................................ [ 29%]
........................................................................ [ 34%]
........................................................................ [ 39%]
........................................................................ [ 44%]
........................................................................ [ 49%]
........................................................................ [ 54%]
........................................................................ [ 59%]
........................................................................ [ 64%]
........................................................................ [ 69%]
........................................................................ [ 74%]
........................................................................ [ 79%]
........................................................................ [ 84%]
........................................................................ [ 89%]
........................................................................ [ 93%]
........................................................................ [ 98%]
................                                                         [100%]
1456 passed in 22.31s
```

`python -m pytest -q -rxX`，exit 0：

```text
........................................................................ [  4%]
........................................................................ [  9%]
........................................................................ [ 14%]
........................................................................ [ 19%]
........................................................................ [ 24%]
........................................................................ [ 29%]
........................................................................ [ 34%]
........................................................................ [ 39%]
........................................................................ [ 44%]
........................................................................ [ 49%]
........................................................................ [ 54%]
........................................................................ [ 59%]
........................................................................ [ 64%]
........................................................................ [ 69%]
........................................................................ [ 74%]
........................................................................ [ 79%]
........................................................................ [ 84%]
........................................................................ [ 89%]
........................................................................ [ 93%]
........................................................................ [ 98%]
................                                                         [100%]
1456 passed in 17.65s
```

### 獨立重跑 M-a～M-c（只在記憶體）

以 `inspect.getsource`／`textwrap.dedent` 取得受審方法原文，在 `dict(store_module.__dict__)` namespace 中 `compile`／`exec` 修改後的方法並暫時指派回 `SnapshotStore`。每輪呼叫 `pytest.main(['-q', '--tb=no', '--disable-warnings', 'tests/test_routing_store.py'])`，plugin 計算 call-phase passed／failed；`finally` 恢復兩個原方法，最後再跑原方法的 store suite。沒有寫 mutation script、沒有改 tracked file、沒有使用 git 還原。

| Mutation | 記憶體內替換 | 實際結果 |
| --- | --- | --- |
| M-a | 在名稱篩選後加 `and (self.directory / name).is_file()` | pytest exit 1；14 failed, 70 passed in 0.58s。T-1 2、T-2 2、T-3 4、T-4 4、T-6 2 失敗；包含 DA 指定的 T-1／T-2／T-4。 |
| M-b | 在名稱篩選後加 `and os.path.isfile(self.directory / name)` | pytest exit 1；14 failed, 70 passed in 0.62s；同樣的 14 cases，包含 DA 指定的 T-3 4 cases。 |
| M-c | 將 `if not stat.S_ISREG(mode):` 改成 `if False:` | pytest exit 1；2 failed, 82 passed in 0.60s；只有 T-6 的 2 cases 失敗。T-1 仍可由 read directory 的 OSError 停止，不能單獨證明 before-open；T-6 確實區分這件事。 |
| 恢復後 | 指派回兩個原方法，執行 store suite | pytest exit 0；84 passed in 0.48s；前後 git status 都空白。 |

## NOT VERIFIED／NOT RUN 與 required authority

| ID | 狀態、理由、影響與 authority |
| --- | --- |
| NV-B1 | **NOT VERIFIED：本次 binding 的 dispatcher 實證。**引用位置為 run record §6 本次「#14 cycle 2 R1／cx14c2r1／HEAD 6f08a5a」dispatch event（尚未編號／收錄）。Required authority＝dispatcher／Orchestrator，依 Bindings §3.3 核對完整 rollout 的 model／effort／sandbox、存取紀錄與 record hash；正式採用前補記，不得以先前 R1／R2 或 qualification 的證據替代。本 reviewer 不讀取 worktree 外的 rollout。 |
| NV-PY313 | **NOT RUN／NOT VERIFIED：Python 3.13 以後的實跑。**本次 Python 3.11.2，沒有安裝或探查其他 interpreter。DA §4.2 #4 明列 MAY，§8 說其實測不再影響契約判斷；本實作不依賴會吞 OSError 的 predicate，T-3 的替身位於實際 os.stat 邊界，M-b 亦可抓出吞錯退化。因此不阻擋本 delta 的結論，不能宣稱已在 3.13+ 通過。若後續要建立跨版本實跑證據，交受派的 Executor，環境與範圍由 Orchestrator 安排；契約解釋 authority＝DA。 |
| NV-SYMLINK | **NOT RUN／NOT VERIFIED：真實失效／循環 symlink 的執行。**worklog 記建立連結無權限，本次沒有重做建立權限探測；只確認 T-4 的 ENOENT／ELOOP 替身及程式預設跟隨連結的 stat 語義。DA §4.2 #5 列 MAY，替身是必需證據，已通過；不阻擋本次結論。真實連結驗證需後續受派 Executor 在具權限環境執行；權限／環境變更由 acceptor 處理，契約解釋 authority＝DA。 |
| NV-PRIV | **NOT VERIFIED：真實騎乘資料、真實使用者的快照存放與部署路徑。**本次只用合成資料與 git metadata；沒有授權讀私有資料。Required authority＝acceptor（RB-7）。不把合成測試的 PASS 當作真實資料驗證；也不主張實際外洩。 |
| NV-INTEGRATION | **NOT VERIFIED（本 audit scope 之外）：#16 是否依 CL-R1-21 原樣傳出選取／put 錯誤、不重試或呼叫引擎，以及 E2／Demo 凍結清單與整合行為。**交 #16 Executor、後續 SPEC-R1 SIA 與 DA；本 Ticket R1 不代替這些驗證。Required authority＝DA（契約／整合 scope），正式 E1 Lite／E2 執行與私有資料權限＝acceptor。 |

本 verdict 僅代表此 delta 與回歸未見 blocking findings；不取代 dispatcher binding 核對、worklog evidence 補登、Ticket completion predicates、Spec Integration Audit 或 phase acceptance。建立本 record 後只應新增本檔，沒有其他 tracked modifications。

Verdict: PASS
