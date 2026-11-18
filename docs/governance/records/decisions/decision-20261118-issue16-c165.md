# Decision record — C-16-5：狀態回應的 `version` 不是合法 Unicode 文字時（CL-R1-29）；呼叫端位置的 `ref_id`／`role` 含孤立 surrogate 的 disposition

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue16-c165`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 事件 103）。問題來自 #16（SPEC-R1 R1-4）Executor 的 return `NEEDS_DA`：worklog `docs/governance/records/worklog/issue-16.md` 第 13.8 節 **C-16-5**（C2R1-F2 的 blocking 殘餘）與同節的「觀察」列 |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-R1 v1（`derivation-spec-r1.md`）的 clarification **CL-R1-29**，治理 §5.3 第 2 類。它是 DD-R1-2（`derivation-spec-r1.md` 第 57 行）「引擎沒有回報時」的 clarification，與 CL-R1-26 並列，不取代它們 |
| Subject 基準 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `805aa4603014a6b4a172dd36052457f63b0d23ae`（`c8aac07` 之後的 record-only commit）；#16 的 cycle 2 implementation commits `a4f0cd9`（C2R1-F1、F2 道路名稱、F4）、`ecddc57`（CL-R1-28）。開始時 `git status --short` 為空 |
| 讀過的依據 | 治理 §1.2、§2.4、§3.6、§3.8、§4.4、§5.3；`derivation-spec-r1.md` 第 57 行（DD-R1-2）與 R1-4 列；`issue-16-c2-r1.md` C2R1-F2 全文（含 required fix）；`ruling-20261118-issue16-c1.md` 第 2.1 節與 Addendum A；`decision-20261118-issue16-c161.md` 第 3 節（CL-R1-26）、第 5 節（TI-C16-3）；`decision-20261118-issue15-c151.md` 第 5 節（CL-R1-24）；`decision-20261117-oc1-first-run-derivation.md` G-RREQ 列；worklog `issue-16.md` 第 13 節全文與 D-16-16；`src/moto_copilot/routing/source.py`（模組說明、`EngineRouteRequest`、`get_route`、`_positions`、`_engine_info`）；`adoption.py` 第 425–463 行（RouteLeg 的組成）；`valhalla.py` 第 80–107 行（`position_from`）；`snapshot.py` 的 `validate_snapshot`、`build_snapshot`；`canonical.py` 的 `canonical_bytes`；`request_key.py` 第 95–107 行；SPEC-001 4.14 `engine_version` 列 |
| 資料 | 沒有讀取、列出或搜尋 `data/`；沒有讀或執行 `experiments/`；沒有讀 `.env`；沒有呼叫 GitHub；沒有發出網路請求 |

本 record 撰寫時實際執行的探測（stdin，合成值，不連網，沒有寫入 repo）：

| # | 探測 | 結果 |
| --- | --- | --- |
| P-1 | `SnapshotValidationError`、`RequestKeyError`、`CanonicalError` 的 MRO | 三者都是 `ValueError` 的子類別 |
| P-2 | `position_from({"ref_id": "A\ud800", "role": "start", "lat": 0.0, "lon": 0.0})` | 接受，回傳 `Position`（只檢查是非空字串） |

---

## 1. 問題

1. **C-16-5（blocking 殘餘）。** 狀態回應的 `version` 是含孤立 surrogate 的字串（JSON `\ud800`）時，`_engine_info` 把它當作有回報的版本，`build_snapshot` 寫 canonical JSON 時拋 `SnapshotValidationError`，`get_route` 既不回傳路線也不回傳代碼，違反 R1-4 範圍 (f)。Executor 提出兩種讀法：(i) 視為「引擎沒有回報」，記 `unreported`，路線照常採用；(ii) 不採用路線（例如 `routing_unavailable`）。
2. **觀察。** 呼叫端給的請求位置的 `ref_id`／`role` 含孤立 surrogate 時，`build_snapshot` 也拋 `SnapshotValidationError`。要判定：這是 R1-4 之外的呼叫端輸入（G-RREQ），還是 #16 必須處理的事。

## 2. C-16-5 的裁決（CL-R1-29）：採 (i)

**CL-R1-29（DD-R1-2 的 clarification）。** 狀態回應的 `version` 只有在它是非空字串、而且是合法的 Unicode 文字（能以嚴格的 UTF-8 編碼，也就是不含孤立 surrogate）時，才是「引擎回報的版本」，並原樣記錄。其他情形，包括不是字串、空字串、含孤立 surrogate，都屬 DD-R1-2 的「引擎沒有回報」，記固定字串 `unreported`。不得修補、替換、跳脫或截斷回報的值（不用 `errors="replace"`、`surrogatepass` 或類似做法），也不得以其他資訊代替。這項判定不影響路線的採用、錯誤代碼、reasons，也不影響 `map_data_date`：`tileset_last_modified` 照 CL-R1-26 從同一個回應讀取。

依據：

1. **DD-R1-2 要的是一個可保存、不推測的值。** 4.14 規定 `engine_version` 是不可為空的 string；SPEC-001 §2 的 canonical JSON 以 UTF-8 寫出。含孤立 surrogate 的字串不是 Unicode 文字，不能寫成快照，所以它不是一個能記錄的「回報的版本」。把它當作沒有回報，正是 DD-R1-2 已定義的處理：固定字串，不推測、不以其他資訊代替。如果修補成另一個字串，就是在記錄一個引擎沒有回報的值，DD-R1-2 禁止這樣做。
2. **與已接受的處理一致。** D-16-16 已把「不是字串或空字串」、HTTP 錯誤、不是 JSON、**狀態請求完全沒有回應**都記為 `unreported`，而路線照常採用（`source.py` `_engine_info`；cycle 1 與 cycle 2 R1 都核對過 DD-R1-2）。也就是說，在現行的設計裡，引擎版本取不到從來不是不採用的理由。一個無法使用的版本字串，比狀態請求整個失敗還輕；採 (ii) 會出現「狀態請求失敗時採用，版本字串壞掉時不採用」的不一致，而且沒有任何來源支持這樣做。
3. **(ii) 不比 (i) 更 fail closed。** `engine_version` 不參與 7.11 第 5～8 項的任何採用檢查，也不參與國道訊號的判定（與 CL-R1-26 對 `map_data_date` 的分析相同）；它只進入 `snapshot_id` 的雜湊與來源證據。在 (i) 下，路線是在各方向的採用檢查全部通過之後才被採用，版本欄位誠實記為 `unreported`。H-4 要求的「無法驗證時不採用」，對象是採用檢查，不是說明性的中繼資料。
4. **不構成 E-DA/D1。** 兩種讀法的後果確實不同，但現有來源（DD-R1-2 的字面、4.14 的型別、D-16-16 已接受的對稱處理）足以裁決，只有 (i) 與它們一致（治理 §3.6-A）。也不是 E-DA/D2：本 DA 先前沒有對這個情形作過決定。

### 2.1 對 #16 的要求（C2R1-F2 的 targeted correction 的一部分，在 FA Addendum A 的範圍內）

本項是 C2R1-F2（blocking）required fix 的狀態版本部分，不是新的 scope。它依 Addendum A 第 2、4 項進行，之後與 C2R1-F1、F2 的其他部分一起進 cycle 2 R2。

**可以修改的檔案（封閉清單）：**

| # | 檔案 | 允許的修改 |
| --- | --- | --- |
| 1 | `src/moto_copilot/routing/source.py` | 只限 `_engine_info`：版本的判定改為 CL-R1-29（例如在非空字串的檢查之外，以 `version.encode("utf-8")` 是否成功判定），以及該函式的 docstring 引用 CL-R1-29。`get_route` 不加任何包住 `build_snapshot` 的 `try`／`except`（那會把其他錯誤一併吞掉），其他程式碼與模組說明不改 |
| 2 | `tests/test_routing_engine.py` | 新增第 2.2 節的測試；既有測試（含 `test_dd_r1_2_engine_version_and_map_data_date`、`test_c2r1_f2_*`、`test_r1_f1_*`、`test_r2_f1_*`）不刪改、不放寬 |
| 3 | `docs/governance/records/worklog/issue-16.md` | 第 2.3 節的 evidence；第 13.7 節 H-4 的例外句與第 13.8 節 C-16-5 的狀態改寫 |

不得：修改 `snapshot.py`、`canonical.py` 或 Addendum A 第 3 項列出的其他受保護檔案；修改 `valhalla.py`、`adoption.py`、`http_transport.py` 來實現本項；加入任何 xfail／skip；發出任何網路請求。

### 2.2 測試（全部不連網；沿用既有的 `FakeEngine` 與合成產生器；本文以 `\u` 跳脫的 ASCII JSON 送出）

| # | 情形 | 要證明的事 |
| --- | --- | --- |
| V-1 | 來回行程與單向，各方向都通過，狀態回應的 `version` 是 `"\ud800"`、`"\udfff"`、`"3.9.1\ud800"`（後者是「部分合法」的字串） | 沒有例外；回傳採用的路線；存了一個快照，`engine_version == "unreported"`；`map_data_date` 仍等於同一回應 `tileset_last_modified` 的 +08:00 日期；請求序列以一次 `status` 結束；快照讀回後（`_from_snapshot`、或以同一 `request_key` 的一般模式重用）與存入時相同 |
| V-2 | 對照：合法的非 ASCII 版本字串（例如 `"3.9.1-é"`、含中文字的字串） | 原樣記錄，不被改成 `unreported`（防止過度拒收） |
| V-3 | 對照：有國道訊號或採用檢查失敗的情形中，狀態版本含孤立 surrogate | 結果仍依 CL-R1-8（`highway_in_route`／`routing_unavailable`），不送狀態請求，沒有快照（行為不變） |

### 2.3 Evidence（記在 `worklog/issue-16.md`）

| # | 證據 | 要求 |
| --- | --- | --- |
| 1 | Commit | 一個只含第 2.1 節第 1、2 列的 implementation commit（與 `a4f0cd9`、`ecddc57` 分開），message 註明 C2R1-F2（狀態版本）、C-16-5 與 CL-R1-29（本 record）。worklog 另以 record-only commit |
| 2 | E-1 | 最終 subject 上完整的 `.venv/Scripts/python.exe -m pytest -q`，exit 0，摘要只有 `passed` |
| 3 | 突變 | 下列各被至少一個測試抓到：拿掉 UTF-8 的判定（V-1 以 `SnapshotValidationError` 失敗）；改為以替換字元修補版本（V-1 的 `unreported` 斷言）；把所有非 ASCII 版本都記為 `unreported`（V-2）。原始碼的還原方式與先前相同（記憶體中的原文寫回，結束時 SHA-256 相同） |
| 4 | Diff | 本項的 commit 只含第 2.1 節第 1、2 列；`source.py` 的 diff 只在 `_engine_info` |
| 5 | E-6 H-4 | 第 13.7 節「例外：狀態回應的 `version`……」一句，改寫為以 V-1～V-3 證明。之後的陳述只能宣稱已測試的範圍：寫入快照、且來自引擎回應的字串欄位（轉向的道路名稱、`engine_version`、shape）不會使 `get_route` 拋出未捕捉的例外；不宣稱窮舉 |
| 6 | 真實請求 | **NOT RUN**；真實伺服器是否會回傳這類字串，仍是 NV-1 |

## 3. 呼叫端位置的 `ref_id`／`role` 的 disposition

**判定：這是呼叫端的輸入錯誤，屬 G-RREQ，不是 C2R1-F2 的一部分，也不是 #16 本次必須處理的事。#16 本次 correction 不得修改它**（治理 §4.4：targeted correction 聚焦 blocking findings，不夾帶無關的 scope）。

依據：

1. **來源不同。** C2R1-F2 與範圍 (f) 的問題，是「引擎回應的內容」使共用介面拋出例外。`ref_id`、`role` 是呼叫端在 `EngineRouteRequest.positions` 中提供的；`valhalla.py` 的模組說明與 CL-R1-5 寫明代號與角色「留在程式內」，不送給引擎。FA ruling 第 2.1 節列出可以向上傳出例外的情形，其中包含「呼叫端輸入的錯誤」；`_positions` 與 `position_from` 對格式不符的位置拋 `ValueError`，這在 cycle 1 與 cycle 2 R1 都被接受。
2. **後果是 fail closed。** 這種情形下拋出的 `SnapshotValidationError` 是 `ValueError` 的子類別（P-1），也就是呼叫端輸入錯誤的同一類例外：沒有存檔、沒有回傳路線，也不會被誤記成路線錯誤代碼。同類的地點代號錯誤（`origin`／`destination`／`via` 的 `ref_id`）在計算 `request_key` 時就以 `RequestKeyError`（同樣是 `ValueError`）停止，發生在任何請求之前。
3. **剩下的瑕疵是時點。** 位置的代號在 `position_from` 中只檢查是非空字串（P-2），所以錯誤要到引擎回應之後、組成快照時才被發現。在那之前已經送出了請求，但請求內容只有呼叫端自己給的座標，不含代號或角色，沒有改變送往第三方的內容（H-2 不受影響）。請求位置怎麼組成、代號從哪裡來（詞彙表的代號、出發錨點），是 TI-C16-3 已指定給 G-RREQ 的範圍。在那之前，任何呼叫 `get_route` 一般模式的新程式都屬 G-RREQ。

**Tracked item TI-C165-1**（第 5 節）：G-RREQ 的 derivation 要定義請求位置 `ref_id`／`role` 的合法值（來自詞彙表或固定角色清單、是合法的 Unicode 文字），並規定在送出任何請求**之前**拒絕不合法的值。這是 TI-C16-3 的補充。

## 4. 高風險分類（`decision-20261117-high-risk-categories.md`）

| 類別 | 判定 |
| --- | --- |
| H-4 | **涉及。** 改變的是 `get_route` 在一類合法可解析的引擎回應上的結果：從未捕捉的例外，改為採用的路線，版本誠實記為 `unreported`。採用檢查與代碼的判定不變（V-3） |
| H-3 | 涉及的程度只到陳述：`unreported` 是 DD-R1-2 的固定值，不推測；第 2.3 節第 5 項限制 worklog 不得過度宣稱 |
| H-1、H-2 | 不涉及。端點、傳輸層、送往第三方的內容與 header 都不變 |

## 5. Tracked items

| ID | 內容 | Owner |
| --- | --- | --- |
| **TI-C165-1** | 第 3 節：G-RREQ 定義請求位置 `ref_id`／`role` 的合法值，並在送出任何請求之前拒絕不合法的值（含孤立 surrogate）。這是 TI-C16-3 的補充；在那之前，R1-4 以 `ValueError`（含 `SnapshotValidationError`）fail closed 的現行行為是可接受的呼叫端輸入錯誤 | Design Authority（G-RREQ 的 derivation） |

## 6. 性質、boundary 與 authority

- **是否改變 accepted 語義：否。** OC-1 的 intent、scope、constraints 與 acceptance semantics 都不變；沒有新增 requirement、AC 或 scope。CL-R1-29 是 SPEC-R1 中 DD-R1-2（derivation decision）的 clarification，屬治理 §5.3 第 2 類，不需要 acceptor 核准。
- **Boundary：在 OC-1 boundary 內。** 變更只限 SPEC-R1 已分配的 R1-4 範圍 (d)、(f)，檔案在 FA Addendum A 第 2 項的範圍內；不涉及 Bindings 第 2.6 節保留的動作、私有資料、憑證或付費呼叫。
- **需要其他 authority：** 無須 acceptor。本項依 Addendum A 第 4 項由 DA 決定語義；派工與 R2 的安排由 Orchestrator 依 run 的流程進行。
- **Escalation：無**（第 2 節第 4 點）。

## 7. 受影響的工作與 evidence

| 對象 | 影響 |
| --- | --- |
| #16（SPEC-R1 R1-4） | C2R1-F2 的 targeted correction 增加第 2.1～2.3 節；完成後由 cycle 2 R2 一併核對 C2R1-F2 的 closure |
| D-16-16（worklog） | 「非空字串」的判定加上「合法的 Unicode 文字」（CL-R1-29）；其他部分與 CL-R1-26 不變 |
| `issue-16-c2-r1.md` | C2R1-F2 的 required fix 中「版本的處置」由本 record 決定；該 record 的結論不變 |
| 既有快照 | 目前沒有任何已存的快照；CL-R1-29 只改變以前會拋例外的情形，不影響任何 `snapshot_id` |
| TI-C16-3 | 由 TI-C165-1 補充 |
| SPEC-R1 SIA | 以最終 subject 核對 CL-R1-29 與 TI-C165-1 |
| 其他 Tickets | 無 |
