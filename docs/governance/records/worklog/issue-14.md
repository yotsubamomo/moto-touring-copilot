# Worklog — Issue #14（SPEC-R1 R1-2）`routing`：路線快照的模型、正規化雜湊、不可變的存放與選取

| 欄位 | 內容 |
| --- | --- |
| Work item | GitHub Issue #14（SPEC-R1 R1-2），OC-1 Formal run `run-20261117-oc1-run2` |
| Lane | Formal（Spec＋Tickets＋Orchestrator） |
| 狀態 | **R1（`audit/issue-14-c1-r1.md`）BLOCKING 的 targeted correction 已完成（`359b948`），待 R2（第 10 節）**：R1-F1、R1-F2 已修正；R1-N1 併入 C-14-6（acceptor）。pytest `1441 passed`。Ticket closure 由 Orchestrator 依 orch-default §7 判定。以下為先前狀態：**Executor 工作完成，DA 裁決已依 `decision-20261118-issue14-c141.md` 第 8 節處理，待 R1**：CL-R1-14（捨去）、CL-R1-15（同時最晚取最小 `snapshot_id`）、CL-R1-17（壞檔停止）確認現行實作；CL-R1-16 要求一般模式不重用取得時間晚於「現在」的快照，已在 `5eee704` 修改；TI-C14-5 是 tracked item；C-14-6 仍待 acceptor。pytest `1116 passed`（第 6 節 E-1）。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure。以下為先前狀態：**Executor 工作完成，回報 `NEEDS_DA`**：C-14-1（正規化的取位方式，影響 S56 的判定與所有雜湊值）需要 Design Authority 確認；C-14-2（取得時間相同時的選取）一併請 DA 確認，non-blocking。其餘範圍 (a)–(f) 完成，pytest `1112 passed`（第 6 節 E-1）。Ticket closure 由 Orchestrator 依 orch-default §7 判定，本 worklog 不宣告 closure |
| Subject | branch `oc1-run2-b1-ui0-r1-routing`；BASE `deb808d`（派工時的 HEAD，含已結案的 #13）；實作 commit **`aa4239249dde499c46a680d6e150b79f0d4a9a49`**（`aa42392`）與 **`366866c7a3683e06b5b89d3090f6d5feb80eb418`**（`366866c`，測試中的範例座標改成 0°N、0°E 附近的合成值，見第 3 節第 9 項）。CL-R1-16 的修改 commit **`5eee70472a824f2725a02afb3160eea613ea0ae9`**（`5eee704`，父 commit 是 DA record 的 `5ecf0c2`），是 R1 的受審 subject（先前的 `366866c` 是 DA 裁決前的 subject）。R1-F1、R1-F2 的 correction commit **`359b948d31b6c3253dbd70bda0d970bc17c24c0c`**（`359b948`，父 commit 是 R1 record 的 `8c1d2d1`），是**最終 implementation subject**。worklog 在另外的 record-only commits |
| 日期 | 2026-11-18 |

## 1. Contract reference

- **Ticket**：Issue #14 的內文。Orchestrator 提供的 scratchpad 原文檔（`issue-14-body.md`）UTF-8 SHA-256 `f7a83732c3b65001e170e8a337ada636f8a984f908b41743d033519a95ca7b75`，Executor 以 `sha256sum` 重算相同，等於派工內容所述 run record 第 4 節的值。沒有呼叫 GitHub，沒有修改 Issue。
- **Spec**：SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md`）：第 2 節引用段落；第 4 節 DD-R1-2（`engine_version` 取不到時為 `unreported`、`map_data_date` 可為 null）、CL-R1-1（資料與網路）、CL-R1-2（`request_key` 的地點指紋）、CL-R1-3（存放與 30 天）、CL-R1-4（嚴格模式與凍結清單）；第 5 節 R1-2 列（範圍 (a)–(f)、AC、排除、高風險類別 H-2、H-3、H-4）與 E-1～E-6。
- **CL-R1-13**：`decision-20261118-issue13-c131.md` §3.1：ID 樣式的語義是完整字串、ASCII 數字、小寫十六進位；R1-2 以測試證明拒絕結尾換行、前後空白與非 ASCII 數字（同 record 第 6 節 R1-2 列）。
- **規格來源**：`docs/spec/SPEC-001-plan-schema.md` §2 的「ID」「雜湊與正規化」「隱私」列；4.13 `snapshot_missing`；4.14 RouteSnapshot／RouteLeg 全部；5.4 的重用期限、`request_key` 地標指紋、雜湊正規化精度三列；7.11 第 1、3、4 項；第 9 節 S17、S23、S35、S36、S37、S53–S56、S58、S71–S77、S86。`DESIGN.md` §5「路線快照」摘要（參考）。`contracts/schemas.py` 的 `SNAPSHOT_ID_PATTERN`、`ROUTE_ID_PATTERN`、`TRIP_TYPES`（只匯入，沒有修改）。
- **高風險類別**：`decision-20261117-high-risk-categories.md` §3.2–§3.4、§5；R1-2 標為 H-2、H-3、H-4（第 6 節 E-6）。
- **CL-R1-14～CL-R1-17、TI-C14-5**：`decision-20261118-issue14-c141.md`（v1，2026-11-18，HEAD `5ecf0c2` 時已 commit）。CL-R1-14 確認正規化的取位是以最短十進位表示為準的捨去（向零）；CL-R1-15 確認同時最晚時取 `snapshot_id` 字典順序最小者；CL-R1-16 規定一般模式的 30 天內是 `0 ≤ 現在 − 取得時間 ≤ 30 × 24 小時`；CL-R1-17 接受壞檔時停止；TI-C14-5 是凍結清單欄位對應的 tracked item。第 8.1 節是修改的封閉清單，第 8.2 節是 evidence。這是執行中的契約 clarification（DA 依治理 §5.3 第 2 類），不是 Executor 的決定。CL-R1-18、CL-R1-19 屬 R1-3、R1-4，本 Ticket 不涉及。

## 2. Executing role and binding reference

- 角色：`executor`，由 Orchestrator（run `run-20261117-oc1-run2`，root session `4aa33b53-7e44-4d34-b9b8-e631fb6f55c2`）以 `gov-executor` 派工。有效 mapping：`claude-opus-5-5`／`high`（Bindings O-1）。沒有 escalation、沒有替代。
- Binding 證據（Bindings 第 3.6 節）：`~/.claude/projects/D--nchu-2026-AIoT-git-repository-moto-touring-copilot/4aa33b53-7e44-4d34-b9b8-e631fb6f55c2/subagents/agent-a731e697ea497fcf3.{meta.json,jsonl}`；`meta.json` 的 `agentType` 是 `gov-executor`，`description` 是「Executor: implement Issue #14 R1-2」。
- Executor 自行觀測（`366866c` 之後、寫本 worklog 之前，以第 3.6 節的掃描方式）：agentId `a731e697ea497fcf3`，(`claude-opus-5-5`, `high`) 83 則，集合只有一個元素。CL-R1-16 的修改（同一個 agent，以 SendMessage 續派）在 `5eee704` 之後再觀測一次：(`claude-opus-5-5`, `high`) 118 則，集合仍只有一個元素。**這是自我觀測，不是派工者的核對**；之後的訊息不在這個數字內，Orchestrator 採用本 return 前須自行核對全部 assistant 訊息。
- Bounded assignments：沒有使用 `gov-investigator` 或 `gov-bounded-worker`，沒有派工任何 subagent。

## 3. Work performed

1. 讀取 Bindings m3（全文）、derivation-spec-r1（全文）、CL-R1-12／CL-R1-13 record（全文）、高風險類別 record §3.2–§5、Issue #14 原文（核對雜湊）、SPEC-001 §2、4.1（RouteRequest、PlaceRef）、4.13、4.14、5.4、7.11、第 9 節的相關 S 編號、`DESIGN.md` §5 的路線快照摘要與確定性規則表、`contracts/schemas.py`、`contracts/__init__.py`、`validate_route_catalog` 的簽名、`tests/conftest.py`、worklog `issue-13.md`（格式參考）、`docs/conventions/git-commit-rules.md`。沒有讀 `experiments/` 的任何檔案（包括 CL-R1-1 允許閱讀的兩個 routing 腳本）。
2. 基準：`deb808d` 上 `.venv/Scripts/python.exe -m pytest -q` 為 `879 passed`。
3. 新建 `src/moto_copilot/routing/canonical.py`（範圍 (a)）：SPEC-001 §2 的正規化 JSON（UTF-8、鍵依字典順序、沒有空白；值以公尺計時取一位小數，其他浮點數（含經緯度）取六位；整數不變；`-0.0` 寫成 `0.0`；拒絕 NaN、無限大與非 JSON 型別）、`canonical_bytes`、`sha256_hex`、`normalized`。取位方式見 D-14-1（C-14-1）。
4. 新建 `src/moto_copilot/routing/snapshot.py`（範圍 (b)、(c)）：`hash_scope`（去掉 `snapshot_id` 與各方向的 `fetched_at`）、`compute_snapshot_id`（`SN-`＋前 10 碼）、`route_id_for`（`RS-`＋同樣的 10 碼）、`validate_snapshot`（4.14 的欄位、型別、可否為空、`legs` 的筆數與順序、沒有高度欄位、`snapshot_id` 與內容一致，以及 4.14 對已存快照的值：D-14-4）、`acquired_at`（各方向 `fetched_at` 最晚者，CL-R1-3）、`build_snapshot`（組裝、計算代號、檢查並回傳正規化後的快照）。
5. 新建 `src/moto_copilot/routing/request_key.py`（範圍 (d)）：`place_fingerprint`（座標定義物件正規化 JSON 的 SHA-256 前 16 碼）、`request_key_content`、`request_key`（`trip_type`、`origin`、`destination`、依序的 `via`、`routing_params`；每個地點是代號加指紋，`entry_ref_id` 有值時另帶它的指紋；CL-R1-2）。
6. 新建 `src/moto_copilot/routing/store.py`（範圍 (e)、(f)）：`SnapshotStore`（呼叫者給的既有目錄，沒有預設值；一個 `snapshot_id` 一個檔案 `<snapshot_id>.json`，內容是整份快照的正規化 JSON；以 `open(..., "xb")` 建立，不覆寫、不修改、不刪除；內容相同沿用既有檔案而不寫入；以既有代號寫入不同內容時 `SnapshotConflictError`）；`find_reusable`（一般模式的重用）、`select_snapshot_mode`（一般的 Snapshot Mode，沒有時回傳 `snapshot_missing`）、`select_strict`（嚴格模式，任何問題都以專用的 `StrictModeStop` 停止，不回退，CL-R1-4）。
7. 新建 `src/moto_copilot/routing/__init__.py`（匯出）、`tests/routing_synthetic.py`（合成輸入）、`tests/test_routing_snapshot.py`、`tests/test_routing_store.py`（共 233 個測試案例）。沒有修改任何既有檔案或既有測試。
8. 自我驗證：全套 pytest、contracts CLI、19 個突變檢查（第 6 節 E-6）。依 SA-1 在 topic branch 作本機 commit `aa42392`；commit 前確認暫存的只有上列 8 個新檔，不含 `.env`、GPX、FIT 或 `data/`。
9. 複查 diff 時發現 `tests/test_routing_snapshot.py` 用 `23.1…`、`120.…` 當作正規化的範例值，其中一組（`{"lat": 23.12345678, "lon": 120.5}`）成對時落在台灣境內。它們是手寫的數值，不是騎乘資料，但為了讓所有座標都可證明是合成的（E-3），改成 0°N、0°E 附近的值（S56 的各組比較關係不變），`canonical.py` 註解中的例子一併修改。本機 commit `366866c`，暫存的只有這兩個檔案。修改後全套 pytest 與突變檢查重跑（第 6 節）。
10. 讀取 DA record `decision-20261118-issue14-c141.md` 全文後，依其第 8.1 節修改（CL-R1-16）：`store.py` 的 `find_reusable` 只重用 `timedelta(0) <= now - acquired_at(s) <= REUSE_WINDOW` 的快照，docstring 改寫為同一定義並引用該 record；`_latest` 的 docstring 與 `canonical.py` 中 `_ROUNDING` 上方的註解改為引用該 record（CL-R1-15、CL-R1-14），只改註解文字；`tests/test_routing_store.py` 新增 3 個測試函式（4 個案例），既有測試沒有修改。`_ROUNDING`、`_format_float`、S56／S71 的測試、Snapshot Mode、嚴格模式、`put`、`load`、壞檔處理與 `request_key` 都沒有改；沒有加 xfail／skip。本機 commit `5eee704`，暫存的只有這三個檔案。
    - 程序紀錄：第一次跑突變檢查時，在修改尚未 commit 的狀態下以 `git checkout -- store.py` 還原突變，連同未 commit 的修改一起還原了；發現後重新套用修改，確認 diff 後才 commit，再對 committed 的檔案重跑突變檢查（第 9 節 #3）。最終 subject 的內容以 `git diff 366866c 5eee704` 為準（第 9 節 #4）。
11. 沒有 push、沒有開 PR、沒有碰 GitHub；沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有執行 `experiments/` 下的任何腳本；沒有發出網路請求。

## 4. Decisions and assumptions

| # | 決定 | 依據 |
| --- | --- | --- |
| D-14-1 | 取位方式：以浮點數的最短十進位表示（`repr`）為準，**捨去**多出的位數（`ROUND_DOWN`），不四捨五入。寫成固定位數（`12.0`、`0.123456`） | SPEC-001 §2 只寫「取小數六位／一位」，沒有寫取位方式。捨去是唯一能使 S56 兩句都對所有數值成立的讀法：第六位不同的一定不同、只有第七位以後不同的一定相同。四捨五入在進位邊界兩側都會違反（例如 `0.1234561` 與 `0.1234569` 只有第七位不同，四捨五入後是 `0.123456` 與 `0.123457`）；S71 同理。這個選擇決定所有 `snapshot_id`／`request_key` 的值，屬契約語義，回報 DA 確認（C-14-1）。實作集中在 `canonical.py` 的 `_ROUNDING` 一個常數。**DA 已確認：CL-R1-14（`decision-20261118-issue14-c141.md` 第 2.2 節），程式不改** |
| D-14-2 | 「以公尺計的長度與偏移」：浮點數自己的鍵，或外層物件／清單的鍵，以 `_m` 結尾 | SPEC-001 §2 的命名規則（`_m` 是公尺）；4.14 的 `endpoint_offset_m`（`start`、`end`）與 `via_offset_m` 都由外層的鍵決定單位。快照中以公尺計的浮點數只有這兩個欄位；`distance_m` 是整數。其他浮點數（含經緯度）一律六位，所以不需要辨認哪些鍵是經緯度 |
| D-14-3 | `request_key` 的內容：`{"trip_type", "origin", "destination", "via", "routing_params"}`，每個地點是 `{"ref_id", "fingerprint", "entry_ref_id", "entry_fingerprint"}`（沒有 `entry_ref_id` 時兩者為 null）；PlaceRef 的 `kind`、`name` 不進鍵；被引用的代號沒有座標定義時報錯；`request_key` 是完整的 64 碼十六進位 | 7.11 第 4 項「每個地點以代號加指紋表示」「完全相同才算同一個請求」；CL-R1-2。鍵的 JSON 形狀是 HOW，只要求確定性與 S37、S71–S73 的性質 |
| D-14-4 | `validate_snapshot` 除了 4.14 的結構，也要求已存快照的值：`has_highway` 是 `false`、`freeway_check` 是 `pass`、`warnings` 是空清單、每個偏移介於 0 與 200 m。`put` 與讀檔都經過這個檢查 | 4.14「存成快照的方向一定是 `false`」「每個方向都是 `pass`」「兩個值都不超過 200 m」；7.11 第 6、7 項（有警告就不採用、才存成快照，沒有例外）。這是存放層的 fail-closed 防線，不取代 R1-4 的採用檢查；R1-4 依規則只會存合格的快照，所以不改變任何合法流程 |
| D-14-5 | 沒有高度欄位：快照與各方向的欄位集合是封閉的（多出的欄位都拒絕）；另外整份快照（含 `request`、`routing_params`）中任何名稱含 `elevation`、`altitude`、`height` 或等於 `ele` 的鍵都拒絕 | 4.14「RouteLeg 沒有高度欄位」「MVP 不向路線引擎要求高度」；`request`、`routing_params` 是 R1-4 組成的自由物件，只檢查封閉欄位會漏掉放在裡面的高度 |
| D-14-6 | 檔案格式：`<snapshot_id>.json`，內容是整份快照（含 `snapshot_id` 與 `fetched_at`）的正規化 JSON（UTF-8，沒有結尾換行）。`build_snapshot` 回傳的快照已是正規化後的值，所以記憶體中的快照、檔案與雜湊一致 | 4.14「實體檔案格式由 Tickets 決定」；CL-R1-3「檔案位元組決定凍結清單所記的 SHA-256」 |
| D-14-7 | 存放目錄必須已存在，程式不建立目錄；只處理名稱完全符合 `SN-[0-9a-f]{10}.json` 的檔案，其他檔案忽略 | CL-R1-3（沒有預設位置，寫到呼叫者提供的目錄）；不在呼叫者沒有指定的地方建立任何東西 |
| D-14-8 | 目錄中名稱符合、但讀不到、不是合法快照、內容的 `snapshot_id` 與檔名不同或與內容雜湊不符的檔案：`SnapshotIntegrityError`，一般模式與 Snapshot Mode 都停止，不略過 | Fail closed：略過壞檔可能讓選取結果變成另一個（較舊的）快照而不被發現。規格沒有寫壞檔的處理，這是 HOW 的保守選擇；列為 C-14-4 供 DA 知悉。**DA 已接受：CL-R1-17（`decision-20261118-issue14-c141.md` 第 5 節）** |
| D-14-9 | 一般模式與 Snapshot Mode 的「相容」：快照**每個方向**的 `freeway_check_method` 都等於現行方法 | 7.11 第 3 項以快照為單位判斷；`freeway_check_method` 逐方向記錄。任一方向不同即不相容（fail closed） |
| D-14-10 | 30 天：`now - 取得時間 <= timedelta(days=30)`（固定 +08:00，沒有日光節約，等於 30 × 24 小時），邊界上算 30 天內。`now` 由呼叫者注入，必須帶時區；預設是 +08:00 的現在。取得時間晚於 `now`（時鐘倒退）時差為負，依字面算 30 天內。**已由 CL-R1-16 改為 `0 ≤ now − 取得時間 ≤ 30 × 24 小時`：取得時間晚於 `now` 的快照，一般模式不重用；Snapshot Mode 與嚴格模式不變（`5eee704`）** | CL-R1-3 的字面定義；列為 C-14-3 供 DA 知悉。DA 裁決：`decision-20261118-issue14-c141.md` 第 4 節 |
| D-14-11 | 「取得時間最晚」有多個快照同時最晚時，取 `snapshot_id` 字典順序最小者，結果不受目錄順序影響 | 規格沒有寫；同一個請求在同一時刻取得不同內容的快照幾乎不會發生，但 H-4 要求選取有確定的結果。回報 DA 確認（C-14-2）。**DA 已確認：CL-R1-15（`decision-20261118-issue14-c141.md` 第 3 節）** |
| D-14-12 | 嚴格模式的輸入：`FrozenEntry(request_key, snapshot_id, sha256)` 或含這三個鍵的物件；整份清單有任何格式不合的項目即停止（`invalid_entry`）；同一個 `request_key` 有完全相同的重複項目時視為一項，有不同項目時停止（`ambiguous_entry`）；讀到的檔案 `request_key` 不是查詢的鍵時停止（`request_key_mismatch`）。`StrictModeStop` 不繼承任何路線錯誤或 `ValueError`，帶 `reason` | CL-R1-4（項目以資料傳入，凍結清單的檔案格式不在本 Spec；停止以專用例外表示，不回傳 `route_error`、不回退）。欄位名稱 `sha256` 是 HOW；之後的 E2／Demo Spec 定義凍結清單格式時可對應。DA：tracked item TI-C14-5（`decision-20261118-issue14-c141.md` 第 6 節） |
| D-14-13 | 錯誤訊息只寫欄位與規則，不寫值；`request_key` 的錯誤只寫代號，不寫座標 | SPEC-001 §2 隱私列；SR1-AC4（例外與 log 不含請求的座標）；`request` 可能含位置 |

## 5. Artifacts

| 檔案 | 變更（`deb808d` → `366866c`） |
| --- | --- |
| `src/moto_copilot/routing/__init__.py` | 新檔：匯出 |
| `src/moto_copilot/routing/canonical.py` | 新檔：正規化 JSON 與 SHA-256（範圍 (a)） |
| `src/moto_copilot/routing/snapshot.py` | 新檔：`snapshot_id`、`RS-`、結構檢查、`build_snapshot`（範圍 (b)、(c)） |
| `src/moto_copilot/routing/request_key.py` | 新檔：`request_key` 與地點指紋（範圍 (d)） |
| `src/moto_copilot/routing/store.py` | 新檔：寫入一次的存放、三種選取（範圍 (e)、(f)） |
| `tests/routing_synthetic.py` | 新檔：合成輸入（不是測試檔，pytest 不收集） |
| `tests/test_routing_snapshot.py` | 新檔：範圍 (a)–(d) 的測試 |
| `tests/test_routing_store.py` | 新檔：範圍 (e)、(f)、沒有網路、沒有預設位置的測試 |

`git diff --stat deb808d aa42392`：8 files changed, 2043 insertions(+)。`aa42392` → `366866c`：`canonical.py`、`tests/test_routing_snapshot.py`，9 insertions(+), 9 deletions(-)（只改範例數值與註解）。沒有修改既有檔案。

`366866c` → `5eee704`（CL-R1-16）：`src/moto_copilot/routing/store.py`（`find_reusable` 的下界與 docstring、`_latest` 的 docstring）、`src/moto_copilot/routing/canonical.py`（`_ROUNDING` 上方的註解）、`tests/test_routing_store.py`（新增 3 個測試函式），3 files changed, 32 insertions(+), 7 deletions(-)。

## 6. Verification

### E-1 pytest（subject `5eee704`，最終）

`.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`，exit 0，完整輸出：

```text
........................................................................ [  6%]
........................................................................ [ 12%]
........................................................................ [ 19%]
........................................................................ [ 25%]
........................................................................ [ 32%]
........................................................................ [ 38%]
........................................................................ [ 45%]
........................................................................ [ 51%]
........................................................................ [ 58%]
........................................................................ [ 64%]
........................................................................ [ 70%]
........................................................................ [ 77%]
........................................................................ [ 83%]
........................................................................ [ 90%]
........................................................................ [ 96%]
....................................                                     [100%]
1116 passed in 16.31s
```

- 1116 ＝ 基準 879 ＋ 本 Ticket 新增 237（`366866c` 的 233 個加上 CL-R1-16 的 4 個案例）。摘要只有 `passed`。
- `grep -rnE "xfail|pytest\.mark\.skip|importorskip" tests/`：0 筆。`git ls-files | grep -iE "(^|/)data/|\.gpx$|\.fit$|(^|/)\.env"`：0 筆。`git status --short`（pytest 與突變檢查之後）：空。

以下是 DA 裁決前 subject `366866c` 的結果（保留作紀錄）：`1112 passed in 28.76s`，exit 0。

- 1112 ＝ 基準 879 ＋ 本 Ticket 新增 233（`--collect-only` 兩個新測試檔：`233 tests collected`）。摘要只有 `passed`。
- `grep -rnE "xfail|pytest\.mark\.skip|importorskip" tests/`：0 筆。
- `PYTHONPATH=src .venv/Scripts/python.exe -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`：exit 0，四項 `OK`。
- `git ls-files | grep -iE "(^|/)data/|\.gpx$|\.fit$|(^|/)\.env"`：0 筆。`git status --short`（pytest 與突變檢查之後）：空，測試沒有在 repo 內留下檔案（存放一律在 `tmp_path`）。

### E-2 AC 對 S 編號

測試檔簡稱：`snap` ＝ `tests/test_routing_snapshot.py`，`store` ＝ `tests/test_routing_store.py`。全部 PASS（E-1）。

| AC | 測試 | 結果 |
| --- | --- | --- |
| S36（以既有代號寫入不同內容報錯、檔案不變；凍結清單雜湊不符時停止；同一內容同一代號；雜湊範圍內任何內容不同則不同，範圍不含 `snapshot_id` 與 `fetched_at`） | `store::test_s55_s36_different_content_under_an_existing_id_is_an_error_and_the_file_is_unchanged`、`store::test_s75_s36_a_sha256_mismatch_stops_without_fallback`、`snap::test_s53_same_content_with_other_fetch_times_has_the_same_snapshot_id`、`snap::test_s36_s54_any_change_inside_the_hash_scope_gives_a_new_snapshot_id`（15 種欄位）、`snap::test_s36_snapshot_id_and_fetched_at_are_outside_the_hash_scope` | PASS |
| S37 中 `request_key` 的部分（途經點順序對調得到不同的鍵） | `snap::test_s37_s73_swapping_the_order_of_the_vias_changes_the_request_key` | PASS |
| S53 | `snap::test_s53_same_content_with_other_fetch_times_has_the_same_snapshot_id`、`store::test_s53_same_content_later_reuses_the_existing_file_without_writing`（位元組與 mtime 不變、沒有新檔、回傳的是舊檔與它的 `fetched_at`） | PASS |
| S54 | `snap::test_s36_s54_any_change_inside_the_hash_scope_gives_a_new_snapshot_id`、`store::test_s54_different_content_is_a_new_file_and_the_old_file_is_unchanged` | PASS |
| S55 | `store::test_s55_s36_different_content_under_an_existing_id_is_an_error_and_the_file_is_unchanged`（以替換 `compute_snapshot_id` 模擬 10 碼碰撞）、`store::test_s55_a_misnamed_existing_file_stops_the_write_and_is_not_overwritten` | PASS |
| S56 | `snap::test_s56_coordinates_differing_in_the_sixth_decimal_hash_differently`、`snap::test_s56_coordinates_differing_only_after_the_sixth_decimal_hash_the_same`（含進位邊界兩側的一組）、`snap::test_s56_offsets_in_metres_use_one_decimal_place`、`snap::test_canonical_json_six_places_for_coordinates_and_other_floats`、`snap::test_canonical_json_one_place_for_values_in_metres` | PASS，**但取位方式待 DA 確認（C-14-1）** |
| S58 中 `snapshot_id` 的部分（含 CL-R1-13） | `snap::test_s58_generated_ids_match_the_section_2_patterns`、`snap::test_s58_snapshot_id_is_sn_plus_first_10_hex_of_the_hash_scope`、`snap::test_s58_ids_pass_the_contract_2_checks_for_a_routing_route`（`RS-`／`SN-` 通過 R1-1 的 `validate_route_catalog`，十六進位部分相同）、`snap::test_s58_cl_r1_13_bad_snapshot_ids_are_rejected`（結尾換行、前後空白、阿拉伯–印度數字、全形數字、大寫、長度不符）、`store::test_cl_r1_13_store_paths_accept_only_snapshot_ids`、`store::test_cl_r1_13_strict_mode_stops_on_a_malformed_frozen_entry` | PASS |
| S71 | `snap::test_s71_a_referenced_landmark_moved_within_six_decimals_changes_the_request_key`（途經點與公路進入端）、`snap::test_s71_a_change_after_the_sixth_decimal_does_not_change_the_request_key` | PASS |
| S72 | `snap::test_s72_an_unreferenced_landmark_change_leaves_the_request_key_unchanged`（改動、新增、刪除未引用的定義） | PASS |
| S73 | `snap::test_s37_s73_swapping_the_order_of_the_vias_changes_the_request_key` | PASS |
| S74 | `store::test_s74_the_frozen_list_wins_over_a_later_snapshot` | PASS |
| S75 | `store::test_s75_a_missing_listed_file_stops_without_fallback`、`store::test_s75_s36_a_sha256_mismatch_stops_without_fallback`（目錄中另有相容的快照，仍停止） | PASS |
| S76 | `store::test_s76_normal_mode_does_not_reuse_a_snapshot_checked_with_another_method`（含只有一個方向不同）、`store::test_s76_snapshot_mode_with_only_incompatible_snapshots_returns_snapshot_missing`、`store::test_s76_strict_mode_stops_on_another_freeway_check_method` | PASS |
| S77 | `store::test_s77_snapshot_mode_takes_the_latest_compatible_snapshot_with_no_age_limit`（較新但方法不同、另一個請求的快照都不採用） | PASS |
| S86 | `store::test_s86_no_frozen_entry_for_the_request_stops_without_using_any_snapshot`（空清單與只有其他請求的清單） | PASS |
| S35 中屬於存放與選取的部分 | `store::test_s35_a_31_day_old_snapshot_is_not_reused`、`store::test_s35_a_snapshot_within_30_days_is_reused`、`store::test_the_30_day_window_is_30_times_24_hours`、`store::test_s35_normal_mode_takes_the_newest_of_several_fresh_snapshots`、`store::test_s35_refetch_after_31_days_same_content_keeps_one_file_and_snapshot_mode_uses_it`、`store::test_s35_refetch_after_31_days_different_content_adds_a_file_and_the_old_one_stays_usable`（兩種情形舊檔位元組不變；Snapshot Mode 仍可使用舊檔：內容相同時一般的 Snapshot Mode 取到舊檔，內容不同時舊檔經凍結清單以嚴格模式取得）；CL-R1-16：`store::test_cl_r1_16_a_snapshot_acquired_after_now_is_not_reused`（晚 1 秒、晚 1 天：一般模式回傳 `None`，一般的 Snapshot Mode 仍選到它）、`store::test_cl_r1_16_a_snapshot_acquired_exactly_now_is_reused`（經過時間 0 的邊界）、`store::test_cl_r1_16_one_leg_after_now_makes_the_snapshot_not_reusable` | PASS |
| S23 中屬於結構的部分 | `snap::test_s23_valid_one_way_and_round_trip_snapshots`、`snap::test_s23_every_snapshot_field_is_required`（8 欄）、`snap::test_s23_every_leg_field_is_required`（13 欄）、`snap::test_s23_legs_count_and_order_follow_the_trip_type`（7 種錯誤的筆數與順序）、`snap::test_s23_snapshot_has_no_elevation_fields`（6 種位置）、`snap::test_s23_snapshot_field_types`、`snap::test_s23_leg_field_types`、`snap::test_stored_directions_satisfy_the_adoption_values_of_4_14`、`snap::test_dd_r1_2_map_data_date_may_be_null_and_engine_version_may_be_unreported` | PASS |
| S17 中「沒有對應快照時回傳 `snapshot_missing`」 | `store::test_s17_snapshot_mode_without_a_matching_snapshot_returns_snapshot_missing` | PASS |
| 另加：快照與 `request_key` 的計算不需要網路 | `store::test_hashing_storage_and_selection_need_no_network`、`store::test_the_routing_package_imports_no_network_or_environment_modules` | PASS |
| 另加：存放位置由呼叫者提供，測試使用暫存目錄 | `store::test_store_needs_a_caller_given_existing_directory`、`store::test_put_writes_only_inside_the_given_directory`；所有 store 測試以 `tmp_path` 建立 `SnapshotStore` | PASS |

S35、S17、S23 中屬於引擎呼叫與採用行為的部分屬 R1-4，本 Ticket 沒有涵蓋（derivation-spec-r1 第 5 節）。

### E-3 合成資料的來源

- 全部輸入在 `tests/routing_synthetic.py` 與兩個測試檔內手寫：座標是 0°N、0°E 附近（大西洋幾內亞灣的海上，沒有道路）的虛構值（`0.1xxxxx`、`0.2xxxxx`）；折線是 `synthetic-shape-...` 的占位字串，不是任何引擎的回應；代號 `SYN-...`、道路名稱 `Synthetic Road N`、引擎名稱 `synthetic-engine` 與檢查方法 `synthetic-freeway-check-v1/v2` 都是虛構的。沒有 GPX，沒有真實的引擎回應，沒有公開地標的座標。
- `366866c` 之前，`aa42392` 的 `tests/test_routing_snapshot.py` 有手寫的範例值 `23.1…`、`120.…`（第 3 節第 9 項），已在 `366866c` 改掉；它們也是手寫的數值，不是騎乘資料，且留在 `aa42392` 的歷史中（尚未 push）。
- diff 中沒有真實的軌跡、住家附近的座標或私有路線：`git diff deb808d 366866c` 只新增上列 8 個檔案，`grep -nE "23\.1|120\.|121\.|24\.|22\."` 對新檔在 `366866c` 為 0 筆。

### E-4 沒有網路請求

- `routing` 套件沒有任何網路程式：`test_the_routing_package_imports_no_network_or_environment_modules` 以 AST 檢查五個模組都沒有匯入 `socket`、`http`、`urllib`、`requests`、`httpx`、`ssl`、`subprocess`，原始碼也沒有 `environ`／`getenv`。
- `test_hashing_storage_and_selection_need_no_network` 以 monkeypatch 讓 `socket.socket`、`socket.create_connection`、`socket.getaddrinfo` 一被呼叫就失敗，在這個狀態下執行 `request_key`、`build_snapshot`、`put`、三種選取，全部成功。
- 本 Ticket 沒有傳輸層（引擎呼叫屬 R1-4），所以沒有替身需要注入。

### E-5 修改的既有測試

沒有。本 Ticket 只新增檔案；`git diff --stat deb808d 366866c` 沒有任何既有檔案。

### E-6 高風險類別的 self-verification（高風險 record §5 的清單）

**H-2 私有騎乘資料與位置**（判定 3.2 第 1 項：決定衍生輸出寫到哪裡）
- 寫入位置：只有 `SnapshotStore.put` 寫檔，目錄由呼叫者給，`__init__` 沒有預設值（`test_store_needs_a_caller_given_existing_directory` 以 `inspect.signature` 核對）；不建立目錄（D-14-7）；檔名只能是驗證過的 `SN-` 代號，`../` 等路徑被拒絕（`test_cl_r1_13_store_paths_accept_only_snapshot_ids`）；`test_put_writes_only_inside_the_given_directory` 核對沒有寫到目錄以外。全部測試以 `tmp_path` 執行，`git status` 在測試後為空。
- 外送：沒有任何網路程式（E-4）。快照含折線，本 Ticket 沒有把它放進任何輸出、log 或送往第三方的內容；`routing` 不寫 log。
- 訊息：錯誤訊息只寫欄位與規則（D-14-13）；`test_validation_messages_do_not_echo_values` 核對座標、偏移與列舉值不出現在訊息中，`test_request_key_rejects_incomplete_requests` 核對 `request_key` 的錯誤不含座標。`request_key` 本身不含座標（`test_request_key_ignores_place_names_and_kinds_and_holds_no_coordinates`）。
- `git ls-files` 不含 release gate 所列路徑（E-1）；fixture 與測試的座標都是合成的（E-3）。
- 不涉及 GPX：本 Ticket 沒有開啟 GPX 或 `data/` 的程式。

**H-3 實驗與宣稱的誠信**（判定 3.3 第 2 項：嚴格模式是 E2 與凍結 Demo 使用的凍結快照機制）
- 嚴格模式只採用清單指定的快照，核對檔案位元組的 SHA-256，任何問題以 `StrictModeStop` 停止，從不查詢其他快照：S74、S75、S76、S86 的測試，以及 `request_key_mismatch`、`invalid_snapshot`、`ambiguous_entry`、`invalid_entry` 各有測試；檔案多一個位元組也停止。突變 M6（拿掉 SHA-256 核對）、M7（沒有項目時改用一般選取）、M15（不檢查方法）都被測試抓到。
- 檔案寫入一次、不修改、不刪除：`test_a_written_file_is_not_changed_by_later_puts_loads_or_selections`；突變 M16b（改成覆寫）被四個測試抓到。凍結清單所記的 SHA-256 因此不會因為之後的重新取得而失效。
- 沒有開啟保留行程的程式路徑；沒有 E1 Lite／E2 的結果或狀態陳述。本 worklog 中的「PASS」只指 pytest 的實際執行結果（E-1）。程式說明沒有把國道檢查稱為道路主管機關的驗證，沒有任何啟發式門檻的驗證宣稱。

**H-4 決策關卡的 fail-closed 語義**（判定 3.4 第 4 項：快照的重用與 Snapshot Mode 的選取）
- 失效的三個條件各有測試：`request_key` 不同（`test_normal_mode_needs_the_same_request_key`）、超過 30 天（S35，含 30 × 24 小時的邊界與「取得時間是各方向最晚的 `fetched_at`」）、檢查方法不同（S76，含只有回程不同）。另依 CL-R1-16，取得時間晚於「現在」的快照不被一般模式重用（3 個 `test_cl_r1_16_*` 測試；突變 M19）。
- 沒有相容快照時：一般模式回傳 `None`（由 R1-4 呼叫引擎），Snapshot Mode 回傳 `snapshot_missing`，嚴格模式停止；都不回傳預設值或其他快照。
- 讀不到或不合法的快照檔：停止而不略過（`test_a_broken_file_stops_selection_instead_of_being_skipped`；D-14-8）。被改過的檔案（內容與 `snapshot_id` 不符）被拒絕（`test_load_rejects_missing_tampered_and_misnamed_files`）。
- 存放層拒絕 4.14 不允許存的值（`has_highway = true`、`freeway_check = fail`、有警告、偏移超過 200 m；D-14-4），突變 M11 被抓到。
- 取得時間相同時的選取是確定的（`test_equal_acquisition_times_resolve_to_the_smallest_snapshot_id`），規則已由 DA 確認（CL-R1-15）。

**突變檢查**（scratchpad 腳本 `issue14_mutations.py`：每次改 committed 檔案的一處，跑兩個新測試檔，再以 `git checkout --` 還原；在 `366866c` 上重跑，之後 `git status --short` 為空。M19 在 `5eee704` 上對 committed 的檔案執行）

| # | 突變 | 結果 |
| --- | --- | --- |
| M1 | 取位改為四捨五入（`ROUND_HALF_EVEN`） | 被抓到（`test_canonical_json_six_places_for_coordinates_and_other_floats`；S56 的進位邊界組同樣會失敗） |
| M2 | 公尺值改為六位 | 被抓到 |
| M3 | `fetched_at` 納入雜湊範圍 | 被抓到 |
| M4 | 拿掉 30 天的限制 | 被抓到（S35） |
| M5 | 不比對檢查方法 | 被抓到（S76） |
| M6 | 嚴格模式不核對 SHA-256 | 被抓到（S75） |
| M7 | 嚴格模式沒有項目時改用一般選取 | 被抓到（S86） |
| M8 | 以既有代號寫入不同內容時不報錯 | 被抓到（S55） |
| M9 | `request_key` 中的途經點依代號排序 | 被抓到 |
| M10 | 指紋改為整份定義的雜湊 | 被抓到（S72） |
| M11 | 接受 `has_highway = true` | 被抓到 |
| M12 | 不檢查 `legs` 的筆數與順序 | 被抓到（S23） |
| M13 | 不檢查巢狀的高度欄位 | 被抓到（S23） |
| M14 | 取最舊而非最新 | 被抓到 |
| M15 | 嚴格模式不檢查方法 | 被抓到（S76） |
| M16 | 拿掉「檔案已存在」的檢查 | 存活：`open(..., "xb")` 本身就拒絕覆寫並轉到比對，行為不變（等價突變）。另以 M16b（同時改成 `"wb"`）確認：4 個測試失敗（S53、S55 兩個、S35） |
| M17 | 不檢查 `snapshot_id` 與內容一致 | 被抓到 |
| M18 | `snapshot_id` 樣式改用接受結尾換行的 `$` | 被抓到（CL-R1-13） |
| M19 | 拿掉 CL-R1-16 的下界（`timedelta(0) <= now - acquired_at(s) <= REUSE_WINDOW` 改回 `now - acquired_at(s) <= REUSE_WINDOW`） | 被抓到：3 failed, 53 passed（`test_cl_r1_16_a_snapshot_acquired_after_now_is_not_reused[ahead0]`、`[ahead1]`、`test_cl_r1_16_one_leg_after_now_makes_the_snapshot_not_reusable`）；還原後 `git status --short` 為空 |

這些是 self-verification，不是 independent audit。

## 7. Concerns

| # | 內容 | 建議的 owner／authority | 是否阻擋 |
| --- | --- | --- | --- |
| **C-14-1** | **正規化的取位方式。** SPEC-001 §2「經緯度取小數六位；以公尺計的長度與偏移取小數一位；其他浮點數取小數六位」沒有寫是捨去還是四捨五入。兩種讀法都合理，但會得到不同的 `snapshot_id`／`request_key`，且只有捨去能使 S56（與 S71）的陳述對所有數值成立（D-14-1）。實作採捨去（以最短十進位表示為準，`ROUND_DOWN`），集中在 `canonical.py` 的 `_ROUNDING`。請 DA 裁決：(a) 確認捨去（不需改程式）；或 (b) 改為四捨五入（改一個常數，並把 S56 的測試改成不跨進位邊界的數值，同時說明 S56 在邊界附近不成立）。目前沒有任何已存的快照或凍結清單，改動不影響既有資料 **狀態：已裁決——CL-R1-14 確認捨去，程式不改（`decision-20261118-issue14-c141.md` 第 2 節）。** | Design Authority | 已解決（原為「是」） |
| C-14-2 | **取得時間相同時的選取。** 7.11 第 3 項「取其中最新的一個」「取得時間最晚的一個」沒有處理同時最晚的情形。實作取 `snapshot_id` 字典順序最小者（D-14-11）。請 DA 確認，或改為其他確定的規則（例如視為無法選取而停止）。**狀態：已裁決——CL-R1-15 確認（同 record 第 3 節）。** | Design Authority | 否 |
| C-14-3 | 取得時間晚於 `now`（時鐘倒退）時，依 CL-R1-3 的字面算 30 天內而可重用（D-14-10）。若 DA 認為應該 fail closed（不重用未來時間的快照），是一行的修改。**狀態：已裁決——CL-R1-16 要求下界，已在 `5eee704` 修改（同 record 第 4、8 節；第 9 節 evidence）。** | Design Authority（知悉） | 否 |
| C-14-4 | 目錄中有壞檔時，一般模式與 Snapshot Mode 都停止而不略過（D-14-8）。這會讓一個壞檔擋住所有規劃，直到使用者處理；規格沒有寫，選擇保守的做法。**狀態：已裁決——CL-R1-17 接受（同 record 第 5 節）。** | Design Authority（知悉） | 否 |
| C-14-5 | 凍結清單項目的欄位名稱（`request_key`、`snapshot_id`、`sha256`）是本 Ticket 的 HOW（D-14-12）；凍結清單的檔案格式屬之後的 E2／Demo Spec，該 Spec 要對應或轉換這三個欄位。**狀態：tracked item TI-C14-5，owner＝Design Authority（同 record 第 6 節）；本 Ticket 沒有動作。** | Design Authority（之後的 E2／Demo Spec） | 否 |
| C-14-6 | `aa42392` 的歷史含手寫的範例值 `23.1…`、`120.…`（第 3 節第 9 項、E-3）。它們不是騎乘資料，也不是由私有資料導出；`366866c` 已改成 0°N、0°E 附近的值。分支尚未 push。是否需要在 push 前整理歷史（RB-6，改寫歷史保留給 acceptor）由 acceptor 決定；Executor 判斷不需要。**狀態：仍待 acceptor（DA record 第 9 節明列不在其裁決範圍）。** | acceptor（知悉） | 否 |

## 8. 剩餘工作

- Orchestrator 依 Bindings 第 3.3、3.7 節派本 Ticket 的 R1：受審 subject `5eee704`；派工內容須含 `decision-20261118-issue13-c131.md` 與 `decision-20261118-issue14-c141.md`（後者第 8.3 節）。
- C-14-6 由 acceptor 決定。
- R1-4 會使用本 Ticket 的介面：`build_snapshot`、`SnapshotStore.put`、`find_reusable`、`select_snapshot_mode`、`select_strict`、`request_key`；CL-R1-17、CL-R1-19 對 R1-4 的要求見 DA record 第 5、7.2 節。
- 先前的剩餘工作「C-14-1 的 DA 裁決」已完成（CL-R1-14，程式不改）。

## 9. `decision-20261118-issue14-c141.md` 第 8.2 節的 evidence

| # | 證據 | 結果 |
| --- | --- | --- |
| 1 | D-14-1、D-14-10、D-14-11 與 C-14-1～C-14-5 的狀態 | 第 4 節 D-14-1（CL-R1-14）、D-14-8（CL-R1-17）、D-14-10（CL-R1-16）、D-14-11（CL-R1-15）、D-14-12（TI-C14-5）與第 7 節 C-14-1～C-14-5 的狀態都改為引用該 record；C-14-6 維持 acceptor 待決 |
| 2 | E-1 | 第 6 節 E-1：subject `5eee704`，`1116 passed in 16.31s`，exit 0，摘要只有 `passed`；沒有 xfail／skip |
| 3 | 突變 | M19（第 6 節 E-6）：拿掉下界後，第 8.1 節第 2 項的新測試失敗（3 failed, 53 passed：未來 1 秒、未來 1 天、一個方向在未來）；經過時間 0 的邊界測試在突變下仍通過，符合預期（上界不受影響） |
| 4 | Diff | `git diff --stat 366866c 5eee704 -- src tests`：只有 `src/moto_copilot/routing/canonical.py`（2 行，`_ROUNDING` 上方的註解）、`src/moto_copilot/routing/store.py`（`find_reusable` 的下界與 docstring、`_latest` 的 docstring）、`tests/test_routing_store.py`（新增 22 行，3 個測試函式，既有測試沒有改）；3 files changed, 32 insertions(+), 7 deletions(-)。`366866c`..`5eee704` 的其他變更只在 record-only 路徑（DA record、run record、本 worklog）。`_ROUNDING`、`_format_float`、S56／S71 的測試、Snapshot Mode、嚴格模式、`put`、`load`、壞檔處理、`request_key` 都沒有改 |
| 5 | E-2 | 第 6 節 E-2 的 S35 列加上 3 個 `test_cl_r1_16_*` 測試 |

## 10. R1 的 targeted correction（cycle 1；R1-F1、R1-F2）

依據：`docs/governance/records/audit/issue-14-c1-r1.md`（R1 BLOCKING，受審 HEAD `532c096`）的 R1-F1、R1-F2 與各自的 Required fix；Orchestrator 的派工（HEAD `8c1d2d1`）。R1-N1 依 R1 record 的 disposition 併入 C-14-6（acceptor）：本次沒有改寫歷史，也沒有修改先前的 worklog 內容。

### 10.1 修改（`8c1d2d1` → `359b948`）

| Finding | 修改 | 檔案 |
| --- | --- | --- |
| R1-F1 | `validate_snapshot` 先檢查 `trip_type` 是字串且在列舉值內（`trip_type_ok`），只有成立時才以它查 `LEG_DIRECTIONS`；`[]`、`{}` 等值成為 `$.trip_type` 的欄位錯誤，`build_snapshot`／`put` 以 `SnapshotValidationError` 拒絕。讀檔時（`_parse_snapshot_bytes`）另把驗證過程的 `TypeError`、`ValueError`、`RecursionError` 與 JSON 解析的 `RecursionError` 轉成 `SnapshotIntegrityError`（防線，修正後的驗證不會再拋出這些例外），嚴格模式因此以既有的 `StrictModeStop(reason="invalid_snapshot")` 停止 | `src/moto_copilot/routing/snapshot.py`、`store.py` |
| R1-F2 | 新增 `SnapshotStore._read`：沒有檔案 → `SnapshotNotFoundError`；其他 `OSError`（含 `PermissionError`）→ `SnapshotIntegrityError`。`load`、`file_sha256` 都經過它。`snapshot_ids` 的列舉（`iterdir`／`is_file`）失敗 → `SnapshotIntegrityError`。`snapshots()`（一般模式與一般 Snapshot Mode 的選取邊界）把「已列出、讀取時已不存在」的 `SnapshotNotFoundError` 轉成 `SnapshotIntegrityError`。嚴格模式保留 `file_missing` 分支，其他讀取 `OSError` → `StrictModeStop(reason="unreadable")`。這些例外都以 `from None` 抛出，訊息只寫 `snapshot_id`，不含路徑或檔案內容；JSON 錯誤原本的 `from exc` 也改為 `from None`。沒有任何路徑會略過壞檔、回傳 `snapshot_missing`／`None` 或改選其他快照 | `store.py` |
| R1-F2（同一類，D-14-14） | `put` 的檔案狀態（`path.exists()`）與寫入的 `OSError`（`FileExistsError` 除外，它照舊轉到比對）轉成不含路徑的 `SnapshotStoreError`（`from None`） | `store.py` |

| # | 決定 | 依據 |
| --- | --- | --- |
| D-14-14 | R1-F2 的 Required fix 列出讀取、列舉與檔案狀態；`put` 的 `exists()` 與寫入也會把帶路徑的 `OSError` 原樣丟出，屬同一類缺陷（H-2：例外帶出呼叫者的目錄名稱），一併轉換並加測試。不改變 `put` 的任何成功路徑、不覆寫、不刪除的行為 | R1-F2 的影響段（原始 OS 例外把 caller 的目錄名稱帶到錯誤訊息）；D-14-13（錯誤訊息不寫值）。若 R2 認為超出 targeted correction 的範圍，可以單獨撤回這一項，不影響 R1-F1、R1-F2 的修正 |
| D-14-15 | `StrictModeStop` 的 reason 新增 `unreadable`（檔案存在但讀不到），與 `file_missing` 分開 | CL-R1-4 只要求專用的停止例外；兩種原因對騎士的處理不同（一個是檔案不見，一個是權限或 I/O） |
| D-14-16 | 直接呼叫 `load` 讀一個從未存在的 ID 仍是 `SnapshotNotFoundError`（R1-F2 允許保留的專用 not-found API）；只有在選取邊界、已列出的檔案消失時才轉成 `SnapshotIntegrityError` | R1-F2 Required fix 末句；CL-R1-17 |

### 10.2 新增的測試（既有測試沒有修改）

- `tests/test_routing_snapshot.py`：
  - `test_r1_f1_a_list_or_object_trip_type_is_a_field_error`（`[]`、`{}`、`[["one_way"]]`、`{"one_way": 1}`；validator 回報 `$.trip_type`，`build_snapshot` 拒絕）。
  - 三個 sweep：快照的每個欄位、回程的每個欄位、整個 leg 與巢狀值，換成 14 種 JSON 值（`[]`、`{}`、`[[]]`、`[{}]`、`{"a": []}`、`{"a": {}}`、`null`、`true`、`false`、`0`、`-1`、`1.5`、`""`、`"x"`）時 `validate_snapshot` 都回傳清單而不拋出例外。
- `tests/test_routing_store.py`：
  - R1-F1：`test_r1_f1_put_rejects_a_list_or_object_trip_type`（不寫任何檔案）；`test_r1_f1_load_and_normal_selection_stop_on_a_list_or_object_trip_type`（`load`、`find_reusable`、`select_snapshot_mode` 都是 `SnapshotIntegrityError`；同一請求另有合格的相容快照，也不被改用；壞檔位元組不變）；`test_r1_f1_strict_mode_stops_on_a_list_or_object_trip_type_with_the_real_sha256`（凍結清單用壞檔實算的 SHA-256，等於 `file_sha256`；結果是 `invalid_snapshot`，目錄中另有合格快照也不回退）。
  - R1-F2（存放目錄名稱是合成的 `synthetic-dir-0.000001N-0.000001E`，用來證明路徑不會出現）：`test_r1_f2_a_read_error_stops_normal_selection_without_a_path`（`PermissionError`／`EACCES` 與 `OSError`／`EIO`；`load`、`find_reusable`、`select_snapshot_mode`、`file_sha256` 都是 `SnapshotIntegrityError` 而不是 not-found，目錄中另有合格快照也不改用）；`test_r1_f2_a_read_error_stops_strict_mode_without_a_path`（同兩種錯誤；`StrictModeStop(reason="unreadable")`）；`test_r1_f2_a_file_listed_and_then_gone_stops_normal_selection`（列出後消失 → `SnapshotIntegrityError`「no longer there」；直接 `load` 未存在的 ID 仍是 `SnapshotNotFoundError`）；`test_r1_f2_a_directory_that_cannot_be_listed_stops_normal_selection`；`test_r1_f2_put_errors_carry_no_path_and_write_nothing`。
  - 每個 R1-F2 測試以 `traceback.format_exception` 核對完整 traceback（含 chained cause）不含目錄名稱，並核對 `__cause__ is None`、`__suppress_context__`；替身先確認原始 OS 例外的文字確實含該名稱，證明測試有意義。替身只以 monkeypatch 模擬 `Path.read_bytes`、`Path.iterdir`、`Path.exists`、`open` 的失敗，沒有變更任何檔案權限。
- 兩個新測試檔共 562 個案例（修正前 237 個）。

### 10.3 Verification

**E-1**（subject `359b948`）`.venv/Scripts/python.exe -m pytest -q`，exit 0，完整輸出：

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
........................................................................ [ 94%]
........................................................................ [ 99%]
.                                                                        [100%]
1441 passed in 31.82s
```

- `.venv/Scripts/python.exe -m pytest -q -rxX`：exit 0，`1441 passed in 30.72s`；輸出中沒有 `xfail`、`xpass`、`skipped`、`error`、`failed`（`grep -ciE` 為 0）。
- `grep -rnE "xfail|pytest\.mark\.skip|importorskip" tests/`：0 筆。`git ls-files | grep -iE "(^|/)data/|\.gpx$|\.fit$|(^|/)\.env"`：0 筆。兩次 pytest 之後 `git status --short`：空。
- 1441 ＝ `5eee704` 的 1116 ＋ 本次新增 325。

**修正前重現**：把 `src/moto_copilot/routing/snapshot.py`、`store.py` 暫時換回 `5eee704` 的版本（實作已 commit 之後才換，再以 `git checkout HEAD --` 還原，之後 `git status --short` 為空），只跑 R1 相關的新測試：`23 failed, 302 passed`。失敗的正是 R1-F1 的 validator／builder／put／load／選取／strict 案例與全部 R1-F2 案例；sweep 只在 `trip_type` 欄位失敗，其他欄位在修正前就不會拋出例外，所以 R1-F1 沒有其他同類位置。

**E-6 補充**
- H-2：store 的例外不再帶出路徑或檔案內容（R1-F2 的測試以完整 traceback 核對）；測試只用合成的目錄名稱、近零座標與 placeholder shape。
- H-3：嚴格模式遇到型別錯誤的壞檔（雜湊相符）與讀不到的檔案，都以 `StrictModeStop` 停止，不回退。
- H-4：一般模式與一般 Snapshot Mode 遇到型別錯誤的檔案、讀取錯誤、列出後消失、目錄無法列舉，都以 `SnapshotIntegrityError` 停止，不略過、不回傳 `None`／`snapshot_missing`、不改選其他快照（CL-R1-17）。

**Diff**：`git diff --stat 5eee704 359b948 -- src tests`：`snapshot.py` 7 行、`store.py` 84 行、兩個測試檔新增 221 行；`5eee704`..`359b948` 的其他變更只在 record-only 路徑（R1 record、run record、本 worklog）。

**Binding 自我觀測**：同一個 agent `a731e697ea497fcf3`（以 SendMessage 續派），`359b948` 之後：(`claude-opus-5-5`, `high`) 158 則，集合只有一個元素。這是自我觀測，Orchestrator 須自行核對。

**程序紀錄**：結束時為了確認工作目錄乾淨，我執行了一次 `git status --short --ignored`。它的輸出列出了被忽略的頂層名稱，其中有 `.env` 與 `data/` 兩個名稱。這只是 git 對忽略項目的狀態，沒有列出 `data/` 的內容，也沒有讀取 `.env`；之後的檢查只用 `git status --short`。

### 10.4 Concerns

- C-14-6（含 R1-N1）：仍待 acceptor。
- D-14-14（`put` 的 I/O 轉換）超出 R1-F2 Required fix 的字面列舉；若 R2 認為不屬 targeted correction，可單獨撤回。
- 沒有新的 blocking 問題。

