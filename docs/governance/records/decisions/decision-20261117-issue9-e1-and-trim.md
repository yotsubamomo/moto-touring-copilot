# Decision record — #9 的 E-1 判定（CL-B1-9）與停等事件跨修剪邊界（CL-B1-10）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261117-issue9-e1-and-trim`（v1） |
| 日期 | 2026-11-17 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 第 6 節事件 4）。問題來自 #9 Executor 的 return：worklog `docs/governance/records/worklog/issue-9.md` 第 8 節 C-9-1、C-9-2（含第 4 節 D-9-1） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-B1 v1（`derivation-spec-b1.md`）。本 record 是 SPEC-B1 的兩則 clarification（治理 §5.3 第 2 類），編號 **CL-B1-9**（C-9-1）與 **CL-B1-10**（C-9-2），與 `derivation-spec-b1.md` 第 4 節的 CL-B1-1～CL-B1-7、`decision-20261117-issue7-spike-tests.md` 的 CL-B1-8 並列引用 |
| Subject 基準 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `bb47d7b`（實作 commit `a281cb0`，BASE `0c109aa`）。主 checkout 的工作區另有 Orchestrator 對 run record 的未 commit 修改，與本 record 的判斷無關 |
| 依據的條文 | 治理 §1.2、§2.4、§3.6（含 measurement 語義須 route 至 DA）、§3.6-A、§3.8、§5.3；orch-default v2.2 §7 P3、P6；Bindings m3 第 2.4、5、7 節；`derivation-spec-b1.md` §4 CL-B1-3、§5 E-1～E-5、§6 SB1-AC3、§7 AB-13；CL-B1-8 §2、§3.2、§3.3、§7；`decision-20261117-high-risk-categories.md` §3.4、§5 |
| 讀過的證據 | Bindings m3；治理本文 §1.2、§2.1、§2.4、§2.5、§3.3–§3.6、§5.3；orch-default v2.2 §7；run record `run-20261117-oc1-run2.md`；`derivation-spec-b1.md`；CL-B1-8 record；高風險類別 record（章節結構與 H-4）；worklog `issue-9.md`；Issue #9 原文（scratchpad 檔，本 record 撰寫時實測 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895`，等於 BD-3）；`DESIGN.md` §5「資料處理流程（GPX）」、契約 1 的欄位表、§6.1 的時間定義、§12 E1 Lite「整趟」一列；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §1.1、SB2-T3、E1 的「整趟」定義；`docs/ticket/BATCH-1-scoped-tickets.md` B1-2；`src/moto_copilot/ingest/segments.py`（`trim_ends`、`moving_path`、`allocate_stop_events`、`build_rows`）；`tests/test_ingest.py` 的測試清單與 trim 相關測試。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有讀取或執行 `experiments/` 下任何檔案 |

本 record 撰寫時在 `bb47d7b` 實際執行（不需金鑰、不讀 GPX）：

| 指令 | 結果 |
| --- | --- |
| `.venv/Scripts/python.exe -m pytest -q -rxX` | `252 passed, 4 xfailed`；4 個 XFAIL 是 CL-B1-8 的 S-3（`restored by #10`）、S-4、S-5、S-6（`restored by #11`） |
| `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py` | `4 failed, 54 passed`（58 個測試）；失敗的恰好是上列 4 個，訊息是 `margin_coeff` 為必填（配速表表頭）、`stop_allow_s` 為必填，以及 S-4 的列比對只差 `stop_allow_s` |
| `grep -rn "xfail\|skip" tests/` | 只有 `tests/test_routes_pace_eta.py` 的 4 個 CL-B1-8 標記（第 117、159、173、182 行）；沒有 `restored by #9`，沒有 `skip` |
| `git diff 0c109aa a281cb0 -- tests/test_routes_pace_eta.py tests/conftest.py tests/test_contracts.py pyproject.toml` | 空 |

**觀察（不是 finding）**：worklog 第 6 節記載同一個 `--runxfail` 指令的結果是 `4 failed, 53 passed`；本 record 在 `bb47d7b` 觀測到 `54 passed`（`--collect-only` 為 58 個）。差異的原因本 record 沒有追查；依 CL-B1-9 第 4 項，最終 subject 上的完整輸出由 Executor 重新記錄，Reviewer 核對。

---

## C-9-1 → CL-B1-9：SPEC-B1 E-1 在 #9（以及 #10）的判定

### 1. 問題

CL-B1-8 §7 的 #9 列寫「結案時移除 S-1、S-2 的標記並恢復檢查（第 3.2 節）；其 E-1 不得有本 record 的 xfail」，#10、#11 列寫「其 E-1 同上」。字面上可讀成「不得有 CL-B1-8 的任何 xfail」，涵蓋全部 6 個標記；CL-B1-8 §3.2 第 1、4 項則規定各 Ticket 只是指向自己的標記的最遲恢復點，且「上述結案條件」就是 E-1 在 #9–#11 的字面要求。#9 結束時 `tests/` 仍有 4 個指向 #10、#11 的 strict xfail。CL-B1-8 §3.3 只寫了 #7 的判定方式。要裁決的是 E-1「全數通過」在 #9 怎麼判定。

### 2. 裁決

1. **CL-B1-8 §7 的 #9 列中「本 record 的 xfail」指 `reason` 為 `restored by #9` 的標記（S-1、S-2）**，不是全部 6 個。#10、#11 列的「同上」同理：#10 指 `restored by #10`（S-3），#11 指 `restored by #11`（S-4～S-6）。這是 CL-B1-8 §3.2 第 1、4 項本來的意思；§7 的表格是它的摘要，兩者以 §3.2 為準。
2. **E-1 在 #9 依下列全部條件判定為滿足；任一不成立即不滿足：**
   1. 最終 subject 上 `.venv/Scripts/python.exe -m pytest -q` 的 exit code 是 0。
   2. 摘要行只出現 `passed` 與 `xfailed`；`failed`、`error`、`xpassed`、`skipped` 都是 0 或不出現。
   3. `-rxX` 列出的每一個 xfail 都帶 CL-B1-8 的標記，`reason` 是 `restored by #10` 或 `restored by #11`，且對應 CL-B1-8 §2 的 S-3～S-6；數目不超過 4。`tests/` 中沒有 `restored by #9` 的標記，沒有任何其他 `xfail`／`skip` 標記（CL-B1-8 §3.4 K-1 的 grep）。
   4. 以 `.venv/Scripts/python.exe -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py` 證明剩下的 xfail 遮住的仍只是 v0.3 的產生者缺口：失敗的恰好是那些 xfail 測試，每一個的失敗訊息只涉及 CL-B1-8 §3.3 第 4 項列舉的 v0.3 項目。理由：xfail 不分失敗原因；#9 修改了 `ingest`，必須證明它沒有在這 4 個測試中引入新的失敗原因而被標記遮住。
   5. S-1、S-2 依 CL-B1-8 §3.2 第 1、3 項恢復：原斷言不帶標記通過，原文不變或在 E-4 逐項交代；S-3～S-6 的測試與標記在 #9 沒有修改（對 BASE 的 diff）。
   6. 第 i、iii、iv 項的**完整輸出**記在 #9 worklog 的 E-1。結果陳述照實寫出數目，例如「`N passed, M xfailed`（依 CL-B1-8、CL-B1-9）」，不得寫成「全數通過」；xfail 不得陳述為通過（H-3）。
3. **E-1 在 #10 的判定**：同第 2 項，以「`restored by #11`、S-4～S-6、數目不超過 3、沒有 `restored by #9` 或 `#10` 的標記」代入；`--runxfail` 的範圍加上 #10 新增或修改的測試檔。**E-1 在 #11**：`tests/` 中沒有 CL-B1-8 的任何標記，pytest 沒有 `xfailed`，即字面的「全數通過」。
4. **Spec 層級不變**：SB1-AC3 與 AB-13 仍依 CL-B1-8 §3.2 第 5 項按字面判定——`tests/` 中不得留有任何 CL-B1-8 標記，pytest 沒有 `xfailed`。本 record 沒有放寬它。
5. **適用時點**：第 2 項的判定以 #9 的最終 subject 為準。CL-B1-10 第 3 項要求 #9 增加測試，所以 `bb47d7b` 的輸出不是 #9 的最終 E-1 證據，Executor 在最終 subject 重跑並記錄。

### 3. 理由

- 「全部 6 個」的讀法無法成立：S-3～S-6 的恢復需要修改 `pace/` 的 `build_pace_table` 與 `compute_eta`（CL-B1-8 §1、§2），而 Issue #9 的範圍只有 `src/moto_copilot/ingest/segments.py` 與重建流程；#10 依賴 #9、#11 依賴 #10（`derivation-spec-b1.md` §5）。依這個讀法 #9 在依賴圖上永遠無法結案，也會迫使 #9 越出自己的範圍。所以只有第 2 項第 1 款一種合理解讀，屬治理 §3.6-A「既有來源只有一種合理解讀而尚未寫下」。
- 第 2 項的條件與 CL-B1-8 §3.3 對 #7 的判定同構，只把允許的標記集合換成「指向後續 Ticket 的標記」，並保留以 `--runxfail` 證明遮住的只是缺口的要求。這維持 CL-B1-8 的設計目的：既有檢查一項都不消失，恢復的時點與責任可機械追蹤。
- orch-default §7 P3：gate 在某 Ticket 的適用方式只能源於 DA 不改變 accepted 語義的 clarification；本 record 即是。它不是 waiver：未恢復的檢查仍由 #10、#11 與 Spec 層級的字面條件攔住。

不構成 E-DA/D1（另一種讀法不是合理設計）；不構成 E-DA/D2（CL-B1-8 沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或爭議，本問題是 Executor 對文字的提問）。

---

## C-9-2 → CL-B1-10：停等事件跨過修剪邊界

### 4. 問題

CL-B1-3 第 2 項：停等事件依**整個事件**的長度分類；事件跨過路段邊界時，各段計入自己那部分的秒數。修剪（`trim_ends`，每端去掉 `trim_m` 的路徑長度）以累計距離決定邊界；停止步之間的 GPS 漂移也會累加距離，所以邊界可能落在一個停等事件中間。Executor 的實作（D-9-1）只以修剪範圍內的步組成事件，分類依範圍內那部分的長度。要裁決的是：跨修剪邊界的事件依範圍內的步或依修剪前的完整事件分類，或此事屬 Executor 的 HOW。

### 5. 這不是 Executor 的 HOW

事件長度決定該段秒數進 `moving_time_s`（假停留）、`short_stop_time_s` 或只進 `stopped_time_s`，是契約 1 欄位的 measurement 語義；治理 §3.6 把「實作必須猜測尚未確定的 measurement 語義」列為須 route 至 Design Authority 的情況。既有來源沒有明寫修剪邊界的處理，所以由本 record 寫定。

### 6. 裁決

1. **停等事件只由修剪後軌跡（`trim_ends` 留下的點）中的步組成。** 修剪範圍以外的步不屬於任何事件，也不影響任何事件的長度或分類。跨過修剪邊界的停等事件，其長度是修剪範圍內那些停止步的時間總和，依這個長度分類（假停留／短停留／長停留）。兩端相同。
2. 跨越修剪邊界本身的那一步（修剪範圍最後一個被去掉的點到第一個保留的點，以及終端的對稱情形）不屬於修剪後軌跡，不計入任何時間。這與 SB2-T3「整趟的移動時間加停留時間等於修剪後的總歷時」一致。
3. **驗證（SPEC-B1 對 #9 的另加驗收條件，屬 verification contract）**：#9 以一個合成軌跡的測試表現第 1 項——修剪邊界落在一個停等事件中間，且修剪前的完整事件與範圍內部分落在不同的分類（例如完整事件 180 秒以上、範圍內部分不到 180 秒）；斷言範圍內的秒數依範圍內部分的長度分類，範圍外的秒數不出現在任何欄位，移動加停留仍等於修剪後的總歷時，並通過契約 1 的檢查。構造方式（漂移的大小、`trim_m` 的值、測前端或後端）是 Executor 的 HOW。測試名稱與結果列入 worklog 的 E-2。
4. CL-B1-3 第 2 項的「整個事件」指修剪後軌跡中的整個事件；它處理的是路段邊界（資料內部的切分），不是修剪邊界（資料範圍的外緣）。CL-B1-3 其他各項不變。

### 7. 理由

- **流程順序**：`DESIGN.md` §5「資料處理流程（GPX）」是先裁掉頭尾（第 1 步）、再分離移動與停留（第 3 步）；`segments.py` 的模組說明與 `build_rows` 也是先修剪、後分離。停等事件在第 3 步才形成，它的輸入就是修剪後的軌跡。
- **資料範圍的定義**：契約 1 的 `seg_index` 是「裁掉頭尾之後」的順序；SB2-T3 的總和以「修剪後的總歷時」為準；E1 的「整趟」定義為「一個 GPX 檔修剪後的記錄範圍內」（SPEC-RESOLUTION-001、`DESIGN.md` §12）；`routes` 使用的 `moving_path` 也是同一段修剪後軌跡。所有衍生量都以修剪後的範圍為一趟行程的資料範圍，修剪邊界因此與 GPX 記錄本身的起訖地位相同：記錄開始前已在停的時間，本來就只以記錄到的長度計。
- **依完整事件分類的讀法不合理**：它會讓修剪範圍內的輸出依賴修剪範圍外（住家與工作地點附近，H-2 的區域）的資料，與修剪的目的相反；同一段修剪後軌跡也不再能單獨重現它的衍生列。它也與上兩點的資料範圍定義不一致。所以只有第 6 項一種合理解讀（治理 §3.6-A），不構成 E-DA/D1。
- **影響有界**：每趟最多兩個事件（兩端各一）會受影響，而且只在邊界恰好落在停等中時發生。SB-2 的 3 秒與 180 秒門檻與試算不因此改變。
- Executor 在 D-9-1 也引用了 AC 3；AC 3 只約束「哪些秒數被計入」，不決定分類，本 record 的依據是上面三點。Executor 引用的參考程式（`experiments/cr01_checks/data_common.py` 的 `segment_stops` 在修剪後的軌跡上組成事件）本 record 沒有閱讀，**未核對**，裁決也不依賴它。
- 第 6 項第 3 款的測試：H-4 涵蓋移動時間的計算路徑（`derivation-spec-b1.md` §5 #9 列），本裁決固定的是會改變欄位值的邊界情形，以測試釘住可防止之後的修改（例如改為先分離、後修剪）悄悄改變分類；成本是一個合成測試。

### 8. 實作符合性（DA 的閱讀，不是 audit）

`build_rows` 在 `trim_ends` 之後只以 `pts = kept[start:end]` 建立步清單，`allocate_stop_events` 只接收這些步；依閱讀，`a281cb0` 的行為符合第 6 項第 1、2 款。現有測試中沒有修剪邊界落在停等事件中間的案例（`test_trim_removes_the_requested_distance_from_both_ends` 與 SB2-T3 的測試不涵蓋），所以第 3 款的測試尚未存在。實作是否符合由 R1 判定。

---

## 9. 是否改變 accepted 語義

**否（兩項皆然）。**
- CL-B1-9 只解決 CL-B1-8 §7 表格摘要與 §3.2 本文之間的字面差異，並把 §3.3 的判定方式延伸到 #9、#10。AB-13「pytest 全數通過」在 Spec 層級按字面保留；沒有放寬、豁免或移除任何 gate。
- CL-B1-10 寫定既有來源（`DESIGN.md` §5 的流程順序、契約 1、SB2-T3、E1 的「整趟」定義）唯一合理的讀法，不改變停等事件、三種分類或兩個門檻的定義；它增加的是 SPEC-B1 對 #9 的一個驗證條件（derived contract 的 verification contract，治理 §5.3 第 2 類），不是 Outcome Contract 的 AC。
- 沒有新增 Must、scope 或 invariant；沒有改變高風險類別的標示；沒有豁免任何 audit。

## 10. Boundary determination

在 OC-1 boundary 內：兩項都在 OC-1 §2.1 第 1–3 項（`ingest`、`tests`、Spike 的收編）與 SPEC-B1 已分配的 AB-3、AB-10、AB-13 部分之內；新增的驗證只用合成資料（OC-1 §2.3）。不需要 acceptor。

## 11. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #9 B1-2 | (a) 依 CL-B1-10 第 6 項第 3 款增加一個合成測試（targeted addition，`tests/test_ingest.py` 或同類檔案），列入 E-2。(b) 在最終 subject 依 CL-B1-9 第 2 項重跑並記錄 E-1 的完整輸出（含 `-rxX` 與 `--runxfail`），並處理本 record 開頭的計數差異觀察。(c) D-9-1 由本 record 取代為契約內容；worklog 引用 CL-B1-9、CL-B1-10。新增測試會改變受審 subject 的 identity，所以 R1 以新增後的 subject 為準 |
| #9 R1（Orchestrator 派工） | Bounded pack 加入本 record 路徑；R1 依 CL-B1-9 第 2 項核對 E-1，依 CL-B1-10 核對修剪邊界的行為與測試 |
| #10 B1-3 | E-1 依 CL-B1-9 第 3 項（允許 S-4～S-6）；S-3 的恢復依 CL-B1-8 §3.2 不變 |
| #11 B1-4 | E-1 依 CL-B1-9 第 3 項（字面全數通過） |
| SPEC-B1 Spec Integration Audit | SB1-AC3 依 CL-B1-8 §3.2 第 5 項按字面核對；SB1-AC2 的整合軌跡不受 CL-B1-10 限制（它不要求修剪邊界的案例） |
| 之後的 `pace` 與 E1 Lite | 衍生路段表的停等欄位以修剪後軌跡為範圍；與 E1 的「整趟」定義一致，無需調整 |
| 既有 evidence | `bb47d7b` 的 `252 passed, 4 xfailed` 是 #9 的中間結果，不是最終 E-1 證據（CL-B1-9 第 5 項）。#7 的 evidence 不受影響 |

`derivation-spec-b1.md` 與 CL-B1-8 record 沒有被修改；SPEC-B1 v1 的引用集合由本 record 補上 CL-B1-9、CL-B1-10，Orchestrator 與 Reviewer 以本 record 路徑引用。

## 12. 需要其他 authority 的事項

無。本 record 不需要 acceptor，也不觸發 escalation。C-9-3（以真實行程重建的契約符合性，NOT VERIFIED，RB-7）與 C-9-4（AB-12 文件工作）不在本次派工範圍，維持 run record 第 6 節事件 5、6 的處理。

本 record 只執行了上表的 pytest、`grep` 與 `git diff`（不需金鑰、不讀 GPX）；沒有讀取 `data/` 或 `.env`，沒有讀取或執行 `experiments/` 下的任何檔案，沒有修改程式、測試、Spec、Issue 或其他 record，沒有派工任何 subagent，沒有 commit。
