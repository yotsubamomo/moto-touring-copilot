# Issue #14 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37a`）→ SPEC-R1 v1（`derivation-spec-r1.md` §2、§4、§5 R1-2 與 E-1～E-6）＋CL-R1-13（`decision-20261118-issue13-c131.md`）＋CL-R1-14～CL-R1-17（`decision-20261118-issue14-c141.md`，含 §8）→ Issue #14 |
| BASE | `deb808dc88ccbb49b97875dade5a838884e19e2c` |
| HEAD | `532c0962e1ef7ecd0d621f8230897e251aaa6299`；此專用 worktree 的 detached HEAD |
| Audit kind | **Ticket independent audit, R1, cycle 1；not a Spec Integration Audit** |
| Role | `primary_reviewer`（Codex） |
| 日期 | 2026-11-18 |
| 高風險 | H-2、H-3、H-4；核對 `decision-20261117-high-risk-categories.md` §5 |

## Assurance 與獨立性

| Property | 本次的滿足方式與證據界線 |
| --- | --- |
| Independent context | 本次為 fresh Codex thread，只收到本次 bounded pack 與 repository 指示，沒有繼承 Executor 對話；自行讀原始碼、契約、歷史、測試及正式 records。Executor 的 worklog 僅作待核對主張。沒有派 subagent。 |
| Verifiable binding | 依 Bindings m3 §3.3 O-6，由 dispatcher 核對本次 rollout 全部 `turn_context` 並把 model／effort／sandbox、thread、record SHA-256 記入 run record。**截至受審 HEAD，run record §6 只有 #14 的事件 69（Executor）、70（DA）、71（Executor correction），尚無本次「#14 R1 / cycle 1 / cx14r1 / HEAD 532c096」的 numbered dispatch／binding 欄位。**因此不虛構事件號或宣稱已核對；本項為 NV-B1，須由 dispatcher 在採用本 record 前補記並核對。引用位置：`docs/governance/records/run/run-20261117-oc1-run2.md` §6 的本次 #14 R1 派工事件（待 dispatcher 記入），前置證據為事件 69～71。 |
| Autonomous access | 自行在本 worktree 讀取 tracked files、執行 `git diff`／`git log`、完整 pytest 與記憶體探測，pack 未限制必要 coverage。沒有讀取、列出或搜尋私有資料目錄，沒有讀憑證、其他 checkout、worktree 外的明確路徑，沒有網路呼叫或執行 `experiments/` 腳本。 |
| Self-written record | 本檔由本 reviewer 自己建立；不修改實作、測試、契約、worklog 或其他 records，不 stage／commit。Dispatcher 應依 Bindings §3.3 原樣收錄並核對 SHA-256，不能代寫或改寫 findings／verdict。 |

Model evidence：Executor 為 `claude-opus-5-5`／`high`，run §6 事件 69 記 91 則、事件 71 記同一 agent `a731e697ea497fcf3` 共 129 則，觀測集合單一且符合 mapping。本 reviewer 是 **Codex**；run §1 第 4 項指定的 mapping 是 `gpt-6.1-sol`／`high`，但本次確切 model ID／effort／sandbox 的 dispatcher 實證尚待 NV-B1，不能以規定值當作觀測值。**no model diversity claim（不主張已建立 model diversity）**。本 record 的實作判斷可供 targeted correction；正式 audit gate 的採用仍須 dispatcher 完成本次 binding 核對。

## Findings

### R1-F1 — 錯誤型別的 `trip_type` 使 snapshot validation 與嚴格模式拋出 `TypeError`

- **Severity：Medium；blocking。Owner：Issue #14 Executor。**
- 契約：R1-2 範圍 (c)、S23 的欄位型別檢查；CL-R1-4 的專用停止例外；CL-R1-17 的壞檔處理；H-3／H-4。
- 證據：`src/moto_copilot/routing/snapshot.py:261` 對 `trip_type` 做 `LEG_DIRECTIONS` 的 dict membership；前面的 enum 檢查雖已記錄錯誤，仍繼續執行。合法 JSON 型別 `[]`、`{}` 不可 hash，因而使 `validate_snapshot` 中斷，沒有回傳 validation errors。`store.py:138` 沒有把這個失敗轉成 `SnapshotIntegrityError`，`store.py:319` 的嚴格模式也只轉換 `SnapshotIntegrityError`。
- 獨立重現：從 `routing_synthetic.snapshot()` 複製快照，把 `trip_type` 分別改成 `[]`、`{}`。直接呼叫 validator；再把該 JSON bytes 注入 `Path.read_bytes`，呼叫 `load` 與 `select_strict`（frozen entry 的 SHA-256 使用這份 bytes 實算）。三個入口各自得到 `TypeError: unhashable type: 'list'`／`'dict'`，共 6 次；並非 `SnapshotValidationError`／`SnapshotIntegrityError`／`StrictModeStop`。
- 影響：結構檢查不能對 JSON 輸入履行其錯誤回報介面；嚴格模式遇到此類壞檔繞過專用停止訊號。這些探測沒有選到其他快照，但「有拋任意例外」不足以滿足契約明定的錯誤介面。
- **Required fix：**在按行程型態查 directions 前先確認型別與 enum 合法；讓 `validate_snapshot` 對此類 JSON 值回報欄位錯誤，`build_snapshot`／`put` 正常拒絕，讀檔時為 `SnapshotIntegrityError`、嚴格模式為 `StrictModeStop`。補 `[]`、`{}` 的 validator、builder／put、一般選取與 strict regression cases；strict case 使用與壞檔相符的檔案 SHA-256，並證明沒有 fallback。不要求修改既有 `contracts/` 或其他 Ticket。

### R1-F2 — 檔案讀取失敗未統一轉成契約指定的停止例外，且會帶出原始路徑

- **Severity：Medium；blocking。Owner：Issue #14 Executor。**
- 契約：CL-R1-4；CL-R1-17（名稱符合但讀不到的快照須以 `SnapshotIntegrityError` 停止；錯誤訊息不含存放目錄路徑／內容）；H-2／H-3／H-4。
- 證據：`src/moto_copilot/routing/store.py:192`／`:193` 的 `load` 只處理 `FileNotFoundError`；`:312`／`:313` 的 strict read 也只處理同一例外。`PermissionError` 等其他 `OSError` 會直接逸出。`:210` 的全目錄載入也沒有把「已列出、之後消失」的 `SnapshotNotFoundError` 轉成完整性錯誤。
- 獨立重現：記憶體中讓 `snapshot_ids()` 回傳一個合法 ID，並用 `patch.object(Path, 'read_bytes', side_effect=PermissionError(...))` 模擬無權限讀取。`find_reusable`、`select_snapshot_mode`、`select_strict` 三者全部得到原始 `PermissionError`；其 `str()` 含完整合成路徑，包含刻意放入目錄名稱的兩個合成座標字串。沒有真正建立或讀取該路徑。另模擬列出後 `FileNotFoundError`，兩個一般選取入口得到 `SnapshotNotFoundError`；strict 的 missing-file case 正確得到 `StrictModeStop(reason='file_missing')`。
- 影響：無權限或 I/O 故障時不能依 CL-R1-17 所要求的例外介面向上傳遞；strict 也沒有履行專用停止例外的約定。原始 OS 例外會把 caller 的目錄名稱帶到錯誤訊息。這是以合成內容證明的資訊帶出路徑，**不是私有資料已實際外洩的主張**。
- **Required fix：**把讀取／列舉／檔案狀態等相關 I/O 錯誤在一般選取邊界轉成不含路徑或內容的 `SnapshotIntegrityError`；strict 邊界轉成 `StrictModeStop`，保留明確 missing-file 分支即可。不要略過壞檔、回傳 `snapshot_missing`、回傳 `None` 或改選其他快照；公開錯誤與正常 traceback 不應透過未抑制的 exception chaining 再帶出原始路徑。補合成的 `PermissionError`、其他讀取 `OSError`、列出後消失等測試，核對例外型別、訊息與無 fallback。可保留直接 `load` 對未存在 ID 的專用 not-found API，但選取已發現的檔案時須符合 CL-R1-17。

### R1-N1 — 最終 worklog 仍引用看似真實地理位置的歷史範例

- **Severity：Low；non-blocking。Owner：acceptor（既有 C-14-6）。**
- 證據：`docs/governance/records/worklog/issue-14.md:37` 仍完整引用先前一對落在台灣範圍的手寫示例座標；`:145`、`:214` 仍有其數值前綴。`aa42392` → `366866c` 的歷史與 run 事件 69、70 已揭露 C-14-6。最終 `src/moto_copilot/routing/` 與三個新增測試檔已沒有那組範例；測試使用近零合成值與 placeholder shapes。
- 沒有證據認定該示例來自私有騎乘資料；不得因為座標看似真實，就宣稱已發生私有資料外洩。也不能只說「最終 subject 完全沒有看似真實的座標」而漏掉 worklog。
- **Disposition：**併入既有 C-14-6，由 acceptor 決定公開前的 records／歷史處置；不要求 Executor 在本次 correction 改寫歷史或刪改既有紀錄，不延長 cycle。本 reviewer 不重印該示例座標。

## 範圍、來源與實際檢查

已讀 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3（含 O-6 與 independent dispatch）、治理 v2.2 §2.3、§3.8、§4.1～§4.7、impl-default v2 §6～§7、orch-default v2.2 §6～§7；OC-1、first-run derivation、SPEC-R1 derivation、兩份適用 CL records、高風險 record、run record 與 #14 worklog；核對 DESIGN §5 的 ID／私有資料／路線快照／選取摘要及 SPEC-001 §2、4.14、7.11、所分配的 §9 S 編號。Issue #14 依派工原文核對 R1-2 與 E-1～E-6，使用 pack 的 body SHA-256 `f7a83732c3b65001e170e8a337ada636f8a984f908b41743d033519a95ca7b75`；沒有向 GitHub 查詢其現況。

完整閱讀五個 `routing` 模組、三個新增測試檔。`git diff deb808d..532c096` 中，實作／測試是八個新檔；另三個變更路徑都在 record-only 範圍。以 Python 讀取完整 git diff，逐檔確認全部新增行恰等於已讀的最終檔案、沒有刪除行；沒有以 worklog 摘要代替 code review。`git log --name-only` 證明只有 `aa42392`、`366866c`、`5eee704` 修改實作／測試；其餘 post-BASE commits 只改 `docs/governance/records/**`。

| 檢查／指令 | 實際結果 |
| --- | --- |
| `git rev-parse HEAD`、`git rev-parse deb808d`、`git status --short` | SHAs 如檔首；起始狀態 clean。 |
| `git log --oneline deb808d..532c096`、`git log --format='%h %s' --name-only deb808d..532c096` | 8 commits；實作／record-only 分布如上。 |
| `git diff --stat deb808d..532c096`、`git diff --name-status deb808d..532c096`、完整 diff 的逐檔新增行比對 | 11 files changed, 2490 insertions(+), 1 deletion(-)；八個新實作／測試檔逐檔比對成立。 |
| `git diff 366866c..532c096 -- src/moto_copilot/routing tests/test_routing_store.py` | 僅 CL-R1-16 下界、引用註解、3 個新測試函式（4 cases），符合 DA §8.1 封閉清單；既有測試未修改。 |
| `git diff --check deb808d..532c096` | 無輸出，exit 0。 |
| **`python -m pytest -q`** | **`1116 passed in 22.72s`，exit 0。**使用 PATH 的 python，沒有改 `PYTEST_DEBUG_TEMPROOT`。 |
| **`python -m pytest -q -rxX`** | **`1116 passed in 18.31s`，exit 0。**沒有 failed／error／xfailed／xpassed／skipped 摘要。 |
| `rg -n 'xfail\|skip' tests`；另以 Python AST 掃描 `tests/**/*.py` 的 skip／skipif／xfail／importorskip attributes 與 calls | 廣搜只有兩處一般英文文字（測試名稱 `being_skipped`、contracts docstring 的 `skipped`）；AST 結果 `[]`，無 markers 或 skip calls。 |
| 測試後及記憶體探測後的 `git status --short`／`git status --porcelain=v1` | 全部無輸出，clean；沒有新增可見 snapshot artifacts。測試以既定 ignored pytest 暫存位置工作，沒有改寫來源或 fixture。 |
| `git ls-files -- .env '*.key' '*.gpx' '*.fit' 'data/raw/*' 'data/private/*' 'data/bmw/*'`；另對 `git ls-files` 的索引路徑字串做 `(^\|/)data/\|\.(gpx\|fit\|key)$\|(^\|/)\.env`（ignore case）篩選 | 都無命中；僅核對 git metadata，未讀取／列出私有資料目錄。 |
| 最終新檔 diff 的座標 literal 篩選及逐檔閱讀 | 台灣範圍 literal 篩選 0 筆；synthetic inputs 是近零值、SYN 代號、placeholder shapes。records 的殘留另見 R1-N1。 |
| stdin 記憶體探測：合成 snapshot 的 `trip_type=[]`／`{}`；`Path.read_bytes` 替身；validator／load／strict | 6 次原始 `TypeError`，R1-F1。沒有寫入檔案。 |
| stdin 記憶體探測：`PermissionError`、列出後 `FileNotFoundError`；兩種一般選取與 strict | R1-F2 的例外與訊息結果；沒有真正碰觸所模擬的檔案路徑。 |
| stdin 獨立 CL-R1-14 assertions（負值向零、`0.3`、負零、公尺一位、定點六位、以手寫 bytes 經 hashlib 核對 SHA-256） | 全部 PASS，沒有重用被測函式生成 expected bytes。 |
| stdin 記憶體突變：以 `inspect.getsource(find_reusable)` 取得本 worktree 程式，僅在記憶體拿掉下界；`pytest.main(['-q','--tb=no','tests/test_routing_store.py','-k','test_cl_r1_16'])` | **`3 failed, 1 passed, 52 deselected in 0.09s`**，預期 pytest exit 1；失敗是未來 1 秒、1 天與只有一個 leg 在未來的 cases，恰等於取得時間的 case 仍通過。探測 wrapper exit 0，最後還原記憶體函式；沒有修改磁碟檔案。 |

讀取過程有一次 Python stdout 的 `cp950` Unicode 輸出失敗（exit 1），與測試無關；之後改用 UTF-8 的讀取／輸出重新核對相關段落。沒有把失敗的讀取當作通過證據。

## 逐項契約與 AC 判定

表內測試名稱省略所在模組的共同前綴：snapshot tests＝`tests/test_routing_snapshot.py`；store tests＝`tests/test_routing_store.py`。既有 1116 個測試通過，不代表新增反例已被涵蓋。

| 條款／AC | 獨立核對與結論 |
| --- | --- |
| 範圍 (a)，SPEC-001 §2，CL-R1-14，S56 | `canonical.py` 統一 UTF-8、sort keys、無空白；`Decimal(repr(value))`＋`ROUND_DOWN`，公尺鍵含外層 `_m` 一位、其他 float 六位，fixed-point、零無負號、NaN／infinity 拒絕、int／bool／string／null 不變。`test_canonical_json_*`、`test_s56_*` 與獨立 assertions 通過。 |
| 範圍 (b)，S36／S53／S54／S58 的 ID／hash 部分 | `hash_scope` 只去除 snapshot_id 與每個 leg 的 fetched_at，其餘內容進入共用 canonical SHA-256；SN- 與 RS- 使用相同前 10 碼。`test_s36_s54_any_change_inside_the_hash_scope_gives_a_new_snapshot_id`（15 cases）、`test_s36_snapshot_id_and_fetched_at_are_outside_the_hash_scope`、`test_s53_same_content_with_other_fetch_times_has_the_same_snapshot_id`、三個 `test_s58_*` 正例通過。 |
| CL-R1-13，S58 的完整字串／ASCII 要求 | snapshot validator／route_id_for／store path／FrozenEntry 共用嚴格 ID 驗證；結尾換行、空白、非 ASCII 數字、大寫／錯誤長度皆有拒絕測試，`test_s58_cl_r1_13_bad_snapshot_ids_are_rejected`、兩個 store 的 `test_cl_r1_13_*` 通過。 |
| 範圍 (c)，S23 結構，DD-R1-2 | 欄位集合、必填、可空、整數與 float／bool 區分、去回 legs 筆數與順序、無高度欄位均有測試；`engine_version='unreported'` 與 `map_data_date=None` 合法。`test_s23_*` 與 `test_dd_r1_2_*` 正例通過，**完整型別錯誤介面不符合：R1-F1**。引擎狀態取得版本屬 #16，不冒稱本票已測。 |
| 範圍 (d)，CL-R1-2，S37／S71／S72／S73 | `request_key_content` 只取引用代號及各自 canonical definition 的 SHA-256 前 16 碼，包含 entry_ref_id 指紋、trip_type、起訖、依序 via 與 routing_params；不含座標值、不用整份詞彙表版本。`test_s37_s73_*`、`test_s71_*`、`test_s72_*`、`test_request_key_covers_every_part_of_the_request`、`test_request_key_ignores_place_names_and_kinds_and_holds_no_coordinates` 通過。詞彙表物件內容仍由後續 Spec 定義。 |
| 範圍 (e)，CL-R1-3，S36／S53／S54／S55 | `put` 以 `xb` exclusive create，不覆寫、不刪除、不建 index；同內容（不計 fetched_at）沿用舊 bytes、mtime、取得時間；不同內容有新 ID／新檔，模擬短 hash 碰撞報 SnapshotConflictError。`test_s53_*`、`test_s54_*`、兩個 `test_s55_*`、`test_a_written_file_is_not_changed_by_later_puts_loads_or_selections` 通過。 |
| 範圍 (f)，S35 的存放／一般重用部分 | 同 key、每個方向 method 相同、取得時間為各 leg 最晚者，篩選 `0 <= age <= 30x24h` 後取最新；31 天不重用，同內容重取仍保持舊檔，新內容另存。`test_s35_*`、`test_the_30_day_window_is_30_times_24_hours`、`test_the_acquisition_time_is_the_latest_fetched_at_of_the_legs`、`test_normal_mode_needs_the_same_request_key` 通過。 |
| CL-R1-16 與 DA §8.1／§8.2 | 三個 `test_cl_r1_16_*` 函式的 4 cases 通過：未來 1 秒／1 天不重用、任一 leg 在未來不重用、恰為 now 可重用；Snapshot Mode 對同一 future snapshot 仍可選。獨立記憶體突變證實下界確實被測試捕捉。 |
| S17／S76／S77，一般 Snapshot Mode | 無相容快照回 snapshot_missing；不限 age；排除其他 key／任一 method 不同的快照，選取得時間最新者。`test_s17_*`、`test_s76_*`、`test_s77_*` 通過。 |
| CL-R1-15，兩種一般選取的 deterministic tie | `_latest` 先按 snapshot_id 排序後取 acquired_at 的 max，因此同時最新時取字典順序最小 ID；`test_equal_acquisition_times_resolve_to_the_smallest_snapshot_id` 通過；strict 不走此排序。 |
| CL-R1-4，S36／S74／S75／S76／S86，strict | 不列舉其他 snapshot，只讀 frozen entry 指定檔案；以讀到的同一份 bytes 做 SHA-256 與解析，核對 key／method，不受 30 天期限或較新檔影響。缺 entry、衝突／不合法 entry、缺檔、改一 byte、hash／key／method 不符、一般壞檔皆有測試且通過。**專用例外的覆蓋不足：R1-F1、R1-F2**。 |
| CL-R1-17，壞檔不略過 | 對 invalid JSON、重複鍵、改內容、錯檔名、空 object 有 SnapshotIntegrityError 測試；`test_a_broken_file_stops_selection_instead_of_being_skipped` 通過。**讀不到及部分結構錯誤不能給出約定例外：R1-F1、R1-F2**。未觀察到實際 fail-open 選取，仍不能宣稱所有失敗路徑已滿足契約。 |
| 另加：no network、caller-supplied storage、temporary tests | `test_hashing_storage_and_selection_need_no_network` 禁 socket／DNS 下完成 hash／storage／三種 selection；AST import check 無網路／環境設定入口；`SnapshotStore` 的 directory 必填、無版控內預設位置，檔名只能為合法 ID，path traversal 拒絕。所有寫檔測試用 tmp_path；相關測試通過。 |
| 排除範圍 | 沒有引擎 client、國道判定演算法、偏移計算、目標 GPX、凍結清單檔案格式、詞彙表定義、路線目錄產生。S17／S23／S35 的 #16 行為部分未冒列為 #14 已完成；CL-R1-18、CL-R1-19 的 #15／#16 要求未冒列已驗證。本次不作 SIA 或 AB 整體 PASS。 |

## E-1～E-6 與高風險最低核對

| 證據 | 核對結果 |
| --- | --- |
| E-1 | Worklog §6 記錄 subject 5eee704 的完整 pytest 輸出 `1116 passed in 16.31s`，採 `-p no:cacheprovider`。其後只有 record-only delta。本次自行以派工指定兩條 PATH python commands 重跑皆 1116 passed；沒有 xfail／skip。 |
| E-2 | Worklog §6 E-2 每項 S 編號都有測試名稱與結果；S35 已加入 CL-R1-16 cases；逐項核對如上。但既有全綠 evidence 不能覆蓋 R1-F1／F2 的新增反例。S56 列仍有舊的「待 DA 確認」字樣，但同檔 §7、§9 已明文引用生效 CL-R1-14，沒有未決取位語義。 |
| E-3 | Fixture、shape、engine／method 皆可追溯至手寫 synthetic helper，無 GPX／真實引擎回應；最終 src／tests 沒有先前真實地理範圍示例，records 殘留見 R1-N1。私人來源的外部比對不作推斷，見 NV-PRIV。 |
| E-4 | 新模組無 network imports／calls，socket／DNS refusal 測試實跑通過；本 reviewer 沒有發出任何網路請求。 |
| E-5 | 對照 BASE，沒有修改任何既有測試；只新增三個測試檔。相對 366866c 的 correction 也只新增 4 cases，理由是 CL-R1-16。 |
| E-6 | Worklog 明列 H-2／H-3／H-4 的 self-verification；本 reviewer 自行核對下列最低項，不以其結論代替證據。歷史 M1～M18 的 scratchpad 執行未逐次重演，見 NV-MUT。M19 的實際效果已獨立重現。 |

| 類別 | 最低範圍的獨立結論 |
| --- | --- |
| H-2 | Git index 無禁止 paths；caller 明確指定儲存目錄，無 tracked-path 預設，ID traversal 拒絕，tests 暫存寫入；無第三方傳輸／log calls，request_key 只放指紋。無 GPX 裁切／錨點代換程式，該部分不適用本票，不能宣稱已驗證。正常 validation messages 不回顯值，但 **I/O exception 的路徑帶出見 R1-F2**；座標來源與 records 殘留見 R1-N1／NV-PRIV。 |
| H-3 | Strict 以檔案 bytes 的 SHA-256 核對、沒有重新序列化後才比 hash；舊檔 write-once，較新檔不覆蓋 frozen choice。沒有 holdout 讀取程式，也沒有把 pytest／突變當成 E1 Lite／E2 的結果；沒有違反 root 用語規則的新增能力宣稱。**嚴格模式專用停止介面仍缺 R1-F1／F2**。 |
| H-4 | 過期、未來、key／method 不同、缺 frozen entry、hash mismatch 均有拒絕測試；tie-break 確定；bad-file 的一般分支有測試；存放也拒絕 highway／fail／warning／offset 越界。**錯誤型別與不可讀路徑的明確錯誤介面有 R1-F1／F2**。Planner、規則 1～5、timeout 的外部 client 不在本票，不新增相關驗收要求。 |

## NOT VERIFIED／authority 與後續

| ID | 項目、原因、required authority |
| --- | --- |
| NV-B1 | 本次 Primary 的完整 rollout binding、fresh 啟動外部證據、存取紀錄與 record hash 尚未在受審 run record 中記入；依禁令不讀 worktree 外 rollout。**Required authority＝dispatcher／Orchestrator**，採用本 record 前依 Bindings §3.3 核對並在本次 #14 R1 dispatch event 記錄；不冒用 Executor／DA 的事件作 Primary binding。 |
| NV-PRIV | 未與任何真實 GPX、住家位置或 holdout 比對；沒有其明確路徑授權，且本票不需真實騎乘資料。合成資料判斷限於 tracked final artifacts／歷史的可見來源。**Required authority＝acceptor（RB-7）**；C-14-6 的歷史／公開處置同樣由 acceptor 保留（RB-6／RB-7），不自行改寫。 |
| NV-MUT | 未取得或執行 Executor 在其他位置的 scratchpad mutation script，無法逐次獨立證實歷史 M1～M18 的所有執行細節。**Required authority＝Issue #14 Executor 提供 worktree 內的 evidence，由 Reviewer 核對**；目前不把這些歷史敘述當作獨立驗證。所需功能已自行讀碼及重跑測試，M19 另已獨立重演，不以此項代替或豁免 findings。 |
| NV-INTEGRATION | #15／#16、E2／Demo Runner、凍結清單檔案格式與真正端到端操作未在本 Ticket 審查執行。**Required authority＝Design Authority／後續 Spec 的 Reviewer**；TI-C14-5、TI-C14-1、RV-6～RV-9 仍屬既有後續責任，不宣稱本票或 SIA 已處理。 |

Targeted correction 由 #14 Executor 處理 R1-F1、R1-F2，提供新 subject 與針對上述反例的 regression evidence，再交 R2。R1-N1 維持既有 acceptor disposition；本 reviewer 沒有修改受審產物或作設計裁決。正式採用本 record 前須完成 NV-B1。

Verdict: BLOCKING
