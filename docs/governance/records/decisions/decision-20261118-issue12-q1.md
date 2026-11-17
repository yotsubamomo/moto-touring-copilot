# Decision record — Issue #12（SPEC-UI0）Q-1：路線確認區塊「資料快照」標籤的適用範圍

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue12-q1`（v1；commit 前依 Orchestrator 的 routing 加入第 7 節的追加裁決，第 1–5 節的 Q-1 結論沒有改變） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | OC-1 第二個 Formal run 的 Orchestrator（`docs/governance/records/run/run-20261117-oc1-run2.md`）。問題由 R1 record `audit/issue-12-c1-r1.md` 第 148 行的 Q-1 依治理 §4.2 route 而來；R2 record `audit/issue-12-c1-r2.md` 第 152 行確認仍 route 給 Design Authority，須在 #12 completion check（orch-default §7 P6）前處理 |
| Outcome Contract | OC-1（`docs/governance/records/outcome-contract.md`），acceptor 2026-11-17 針對 `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| Spec | SPEC-UI0 v1（`derivation-spec-ui0.md`）：Issue #12 全文＋`UI_CR01_DELTA.md` 第 11、12 節＋`ui0_decision_table.md`＋G3 凍結的 `UI_DESIGN.md`、`UI_FLOW.md`、`UI_ACCEPTANCE.md` 沒有變更的部分＋CL-UI0-1～CL-UI0-5 |
| Ticket | #12（UI-0）。Issue 原文：派工所附 `issue-12-body.md`，本次實測 SHA-256 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be`，等於 BD-3 |
| 受審 subject | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `eac676b`（本次 `git rev-parse HEAD` 核對，工作目錄乾淨） |
| 依據的條文 | 治理 §1.2、§2.4、§4.2、§5.3；Bindings m3 第 2.6、7 節；orch-default §7 P6 |
| 讀過的證據 | Issue #12 原文（第 4 節、情境清單、元件表、UI0-1、UI0-8）；`derivation-spec-ui0.md` 全文；R1 record 第 120–159 行（Q-1、NV、verdict）；R2 record 第 130–158 行；`UI_CR01_DELTA.md` 第 6、7.1 節（第 160–215 行）與第 11、12 節（第 300–427 行）；`UI_DESIGN.md` 第 31、48、82、96 行；`UI_ACCEPTANCE.md` A3、C7、E2；`UI_FLOW.md` 第 70 行；`ui0_decision_table.md` 中與快照有關的列（U-16、U-17）；`app/ui0_mock_app.py` 第 186–196、371–392、483 行；`app/ui0_scenarios.py` 第 120–170、396–401、676–797 行；`tests/test_ui0_skeleton.py` 第 1–75、425–435 行；worklog `issue-12.md` 第 124–126、182、205–262、292 行；`decision-20261118-issue12-ui07.md` 檔首與第 123 行。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/`，沒有呼叫 GitHub |
| 獨立核對 | 以 scratchpad 的一次性 AppTest script（只載入 `app/ui0_mock_app.py`，合成情境，沒有修改任何追蹤中的檔案）規劃後檢查路線確認區塊的 badge：s08、s13、s15（engine，一般模式）只有灰色「路線引擎」，沒有「資料快照」；s14（engine，Snapshot Mode）有灰色「路線引擎」與藍色「資料快照」；s08 開啟 Snapshot Mode 後規劃有「資料快照」；s14 關閉 Snapshot Mode 後規劃沒有；s10（目標 GPX）開啟 Snapshot Mode 時路線確認區塊只有「目標 GPX」，頁首有 Snapshot Mode 標籤。s09 在預設表單下因出發油量未填而停在欄位錯誤（情境本身的設計），未進入路線確認區塊 |
| **結論摘要** | Issue #12 第 4 節「路線引擎的路線帶『資料快照』的標籤」**只要求代表路線快照的情形顯示該標籤**（路線來自已保存的路線快照：Snapshot Mode；或一般模式下重用 30 天內的快照），**不要求所有 engine 模擬情境都顯示**。現行實作與證據**滿足 #12**，**不需要 targeted correction，也不需要補充 evidence**。不改變 accepted 語義；在 OC-1 boundary 內；**不需要 acceptor**；沒有 capability escalation |
| **追加裁決摘要（第 7 節，Q-1b）** | 同一句的「示範路線」是路線來源標籤的取值之一，但 #12 **沒有要求**在 Skeleton 中呈現示範路線的來源標籤或為它建立情境：CR-01 之後的 Trip Planner 沒有任何輸入能得到示範路線（CR-B1 沒有路線下拉選單；SPEC-001 7.11 第 3 項的取得順序只有目標 GPX、Snapshot Mode 與一般模式），Issue 的情境清單也沒有這一項。現行實作與證據**滿足 #12**，不需要 targeted correction 或補充 evidence。示範路線在 Streamlit 中是否、如何出現是**規格缺口**，歸之後正式整合的 `app/` Spec（Design Authority）；若要在介面上讓騎士選用示範路線，牽涉 CR-B1，需要 **acceptor**。不改變 accepted 語義；在 OC-1 boundary 內；#12 不需要 acceptor；沒有 capability escalation |
| **澄清（第 8 節，2026-11-18）** | 本 run 不採 fast path：SPEC-UI0 的 SIA 另外派工（`audit/spec-SPEC-UI0-c1-*`），phase acceptance 必須引用該 SIA 的 closure record。第 5 節「fast path，由 #12 R1 兼任」的描述以第 8 節為準；Q-1、Q-1b 的裁決不變 |

## 1. 問題

Issue #12 第 4 節列出路線確認區塊的內容：「路線來源與標籤（路線引擎的路線帶『資料快照』的標籤；目標 GPX；示範路線）」。`UI_CR01_DELTA.md` 第 11.1 節 CR-R3（SPEC-UI0 引用的段落）則以條件寫成：Snapshot Mode 下路線來自已保存的快照時有「資料快照」標籤；一般模式下重用 30 天內的快照時也有。實作只在顯示中結果的表單 snapshot 為真、且路線來源是 engine 時顯示該 badge。

要裁決：Issue 該句是要求所有 engine 模擬情境都顯示「資料快照」badge，還是只要求代表快照的情境；依此，現行實作與證據是否滿足 #12。

## 2. 事實與來源（獨立核對）

1. **Issue 的句子本身有兩種讀法。** 括號內以分號列出三種來源：「路線引擎的路線帶『資料快照』的標籤」「目標 GPX」「示範路線」。字面可讀成「engine 路線一律帶快照標籤」，也可讀成「engine 路線（可能）帶快照標籤」。句子沒有寫條件，也沒有寫「一律」。
2. **同一份 Spec 的其他引用段落寫明條件。** SPEC-UI0 引用 `UI_CR01_DELTA.md` 第 11、12 節。CR-R1：「路線來源與路線快照的標籤」，來源標籤與快照標籤是兩個項目。CR-R3：「Snapshot Mode 下路線來自已保存的路線快照，路線確認區塊有『資料快照』的標籤……一般模式下重用 30 天內的路線快照時，也有這個標籤。」
3. **Issue 第 4 節是 DELTA 第 6 節的濃縮。** 位置（追問之下、過期提示之上，兩個分頁都看得到）與「不是按鈕，不增加強制的點擊」逐句對應 DELTA 第 6 節。該節的表把兩者分開：「路線來源的標籤：『路線引擎』『目標路線 GPX』『示範路線』三者之一，灰色」；「路線快照的標籤：路線來自路線快照時顯示『資料快照』（藍色）」。第 7.1 節第 207 行也以「一般模式下，請求相同、30 天內取得的路線快照會直接重用……這時路線確認區塊有『資料快照』的標籤」為條件。DELTA 第 6、7.1 節不是 SPEC-UI0 引用的段落，這裡只用來說明 Issue 句子的來源，不作為 #12 的額外要求。
4. **G3 凍結的設計要求資料模式的標籤如實。** Issue 寫明 G3 沒有變更的部分（含狀態標籤、來源證據）照凍結的設計做。`UI_DESIGN.md` 第 31 行：「模擬資料、資料快照與真實 API 各有標籤」；`UI_ACCEPTANCE.md` A3：三者「各有不同的標籤」；E2：Snapshot Mode 標籤「描述畫面上的結果，和結果的資料模式、來源類型一致」。
5. **Issue 的 14 個情境沒有一項指定「engine 路線一律帶快照標籤」。** 與快照有關的只有情境 11 的 `snapshot_missing`（Snapshot Mode 下沒有快照）；情境 8、9、13 的描述沒有提到快照。
6. **實作。** `app/ui0_mock_app.py` 第 371–380 行：`snapshot` 取自 `ss["plan_inputs"]`（產生目前結果時的表單），engine 路線一律顯示灰色「路線引擎」，`snapshot` 為真時再加藍色「資料快照」；目標 GPX 顯示灰色「目標 GPX」。頁首（第 186–196 行）與「採用的條件」（第 483 行）也以同一個 `plan_inputs` 描述資料模式。情境 s14 的表單 `snapshot=True`、路線來源 engine（`app/ui0_scenarios.py` 第 401、782 行）。實際行為見檔首「獨立核對」。
7. **證據。** worklog 第 217 行把 CR-R3 記為「Snapshot Mode 時的『資料快照』標籤（PASS，情境 14）」，「快照的重用與嚴格模式」列為整合後驗收；第 292 行 K8 的瀏覽器逐步紀錄（開啟 Snapshot Mode 後規劃）寫明「路線確認有『資料快照』標籤」。pytest 沒有斷言這個 badge 的測試；Issue 與 SPEC-UI0 的 E-1～E-6 也沒有要求這項的自動化測試。

## 3. 裁決

### 3.1 Issue 該句的適用範圍

**只要求代表路線快照的情形顯示「資料快照」標籤。** 「路線引擎的路線帶『資料快照』的標籤」的意思是：路線引擎這類路線，在它取自已保存的路線快照時，帶這個標籤。快照只會是 engine 路線（目標 GPX 與示範路線不是快照），所以句子把標籤掛在 engine 這一項之下。它不是要求所有 engine 路線都帶這個標籤。

理由：

1. 這是唯一能和同一份 Spec 的 CR-R1、CR-R3 同時成立的讀法（事實 1、2）；兩段沒有衝突，不需要依治理 §5.3 處理 precedence。
2. 「一律帶標籤」的讀法會把不是來自快照的路線標成「資料快照」，和 G3 凍結的 A3、E2（資料模式的標籤要和結果一致）牴觸（事實 4），也使路線確認區塊的來源標示不實。Issue 要求 G3 沒有變更的部分照凍結的設計做，所以這個讀法不是合理的設計選項。
3. Issue 的情境清單沒有任何一項支持「一律帶標籤」（事實 5）；句子的來源（DELTA 第 6、7.1 節）也是有條件的（事實 3）。

所以這不是兩個以上合理設計的實質分歧，不構成 E-DA/D1；本 Design Authority 先前也沒有對同一問題作過決定，不構成 E-DA/D2。

### 3.2 對 Skeleton 的具體意思

- 結果對應 Snapshot Mode（產生結果時 Snapshot Mode 開啟）且路線來自路線引擎時：路線確認區塊有「資料快照」標籤。情境 s14 代表這個狀態；任何 engine 情境在開啟 Snapshot Mode 後規劃也一樣。
- 一般模式的 engine 路線：沒有「資料快照」標籤。
- 目標 GPX 路線：沒有「資料快照」標籤，不論 Snapshot Mode。
- 一般模式下重用 30 天內快照的情形：是否重用由後端決定（SPEC-001 第 7.11 節第 3 項），Skeleton 沒有後端（CL-UI0-5、Issue 排除範圍），Issue 的 14 個情境也沒有列這一項。它的呈現和 Snapshot Mode 用同一個標籤。worklog 把「快照的重用」列為整合後驗收，符合 UI0-8；**不要求為它另加情境**，加了也不是 #12 的要求。
- DELTA 第 6 節的「附快照的時間」：Issue 第 4 節沒有寫，DELTA 第 6 節也不是 SPEC-UI0 引用的段落，所以不是 #12 的要求。Skeleton 的來源證據一律寫「模擬，沒有取得時間」，和 G3 的模擬標示一致。快照時間怎麼呈現屬之後正式整合的 Spec（owner：該 Spec 的 Design Authority），不由本 record 新增到 #12。

### 3.3 現行實作與證據是否滿足 #12

**滿足。** 實作的條件（engine 路線且結果的 snapshot 為真）就是第 3.2 節的意思（事實 6 與獨立核對）。badge 以「產生結果時的表單」為準，不跟著勾選框的目前狀態變，和 E2 一致。worklog 第 217 行 CR-R3 的 PASS 與整合後驗收的分法、第 292 行 K8 的瀏覽器紀錄，足以支持這一項（事實 7）。

- **targeted correction：不需要。**
- **補充 evidence：不需要。** 沒有新增測試或瀏覽器紀錄的要求；Issue 與 SPEC-UI0 都沒有要求這一項的自動化測試。
- **worklog：不需要修改。**

## 4. 語義、boundary 與 authority

- **不改變 accepted 語義。** 這是 SPEC-UI0 內引用段落之間的適用性釐清（治理 §5.3 的 derived contract clarification）；沒有新增 requirement、AC、情境或 scope，也沒有放寬任何既有要求。
- **在 OC-1 boundary 內。** 依 `derivation-spec-ui0.md` 第 3 節的 boundary determination；本裁決只解讀 #12 已有的內容。
- **不需要 acceptor 的接受或授權。** 沒有 contract change，也沒有觸及 Bindings 第 2.6 節保留的動作。acceptor 的 UI Delta Review 仍可對標籤的呈現提出意見，那是 OC-1 §4.2 保留給 acceptor 的另一件事，不由本 record 代行。
- **沒有 capability escalation**（見第 3.1 節末段）。

## 5. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #12（UI-0） | R1 的 Q-1 已處理：對 #12 沒有要求。Orchestrator 在 completion check（orch-default §7 P6）可引用本 record 作為 Q-1 的 disposition |
| SPEC-UI0 的 SIA（fast path，由 #12 R1 兼任）與 phase acceptance | Q-1 的追蹤以本 record 關閉；phase acceptance 仍須依 Bindings 第 5 節引用已 closure 的 SIA record，本 record 不代替 |
| 之後正式整合的 `app/` Spec | 一般模式重用快照時的標籤、快照時間的呈現，依 CR-R3 與 DELTA 第 6 節在該 Spec 處理；本 record 沒有為它新增要求 |

Evidence：本 record 檔首「獨立核對」所列的 AppTest 結果（一次性 script，在 session scratchpad，沒有加入 repo）；worklog 第 217、292 行。

## 6. 範圍外的觀察（已轉為第 7 節的裁決）

本 record 初稿在這裡記下同一句的第三種來源「示範路線」：實作只區分 engine 與目標 GPX 兩種來源標籤，14 個情境也沒有示範路線的情境；R1、R2 都沒有提出，初稿沒有裁決，交 Orchestrator 決定是否 route。Orchestrator 之後把它正式 route 給 Design Authority，要求在 #12 的 P6 前裁決，裁決在第 7 節。它仍不是 R1／R2 的 finding。

## 7. 追加裁決 Q-1b：「示範路線」來源標籤在 #12 的要求

### 7.1 問題

Issue #12 第 4 節同一句列出的第三種來源「示範路線」，在 #12 是否有要求；實作只區分 engine 與目標 GPX，也沒有示範路線的情境，這樣是否滿足 #12。若不滿足，對 #12 的具體要求是什麼；若是規格缺口或在 #12 範圍外，歸屬是什麼。

### 7.2 事實與來源（獨立核對）

本節另外讀過：`SPEC-001-plan-schema.md` 第 51、179、440–475、651–652、716、725、841 行；`DESIGN.md` 第 4、83、272、1462 行；`ui0_decision_table.md` U-13（第 55 行）；`UI_DESIGN.md` 第 120 行；以 `示範路線` 搜尋 `docs/ui/`、`docs/spec/`、`app/` 與 worklog 的結果。

1. **示範路線是什麼。** SPEC-001 4.12：`route_source` 有三個值，`trip`（由騎過的行程建立的示範路線，也就是 R01／R02 fixture）、`routing`、`target_gpx`。CR-01 的 D1（`DESIGN.md` 第 1462 行）把兩條示範路線降為 Demo 與測試用的 fixture；它們由騎過的 GPX 裁切（`DESIGN.md` 第 272 行）。
2. **DELTA 第 6 節的標籤。** 「路線來源的標籤：『路線引擎』『目標路線 GPX』『示範路線』三者之一，灰色」，對應 `route_source` 的三個值。Issue 第 4 節的括號是這張表的濃縮（見第 2 節事實 3）。
3. **CR-01 之後的 Trip Planner 沒有得到示範路線的輸入。** CR-B1：「沒有路線下拉選單。」G3 原型的「路線下拉選單（兩條示範路線）」（`UI_DESIGN.md` 第 120 行）已列為不再代表要做的介面（DELTA 第 12 節末段）。SPEC-001 7.11 第 3 項「取得路線的順序」只有三條：(a) 有目標路線 GPX、(b) Snapshot Mode、(c) 一般模式（`request_key` → 快照重用或呼叫路線引擎），沒有一條會得到 `route_source = trip`。
4. **Issue 的情境與文字。** 14 個情境沒有示範路線的一項。和示範路線有關的固定文字只有路權提醒「目標 GPX 或示範路線」那一則（U-13），它和目標 GPX 共用；情境 10（s10）顯示這一則。
5. **實作。** `app/ui0_mock_app.py` 第 377–382 行：`route["source"] == "engine"` 顯示「路線引擎」，其餘一律顯示「目標 GPX」；路權提醒也以 engine／非 engine 二分（第 389 行）。情境資料中的路線來源只有 `engine` 與 `gpx`（`app/ui0_scenarios.py` 第 163、228、286、347、401、457 行）。worklog 沒有提到示範路線。

### 7.3 裁決

**#12 沒有要求在 Skeleton 中呈現示範路線的來源標籤，也沒有要求示範路線的情境。** 「示範路線」在這一句中是路線來源標籤的取值之一（事實 2），用來寫明標籤的完整集合；它不是 #12 要求做出來的一個畫面狀態。

理由：

1. **在 CR-01 之後的介面中，這個狀態沒有可達的輸入。** Trip Planner 沒有路線下拉選單（CR-B1），路線的取得順序也不會得到示範路線（事實 3）。Skeleton 要呈現它，就得假設一個契約沒有寫的取得方式（例如恢復下拉選單，或由行程描述選用 fixture）。前者違反 CR-B1，後者是新增 requirement；兩者都不是 #12 內合理的設計選項。
2. **Issue 的驗收條件不依賴它。** UI0-1 的「每個狀態都有對應的合成情境」是指 Issue 列出、在這個介面中可以到達的狀態；情境清單沒有示範路線（事實 4）。和示範路線有關的唯一固定文字與目標 GPX 共用，已由 s10 呈現；UI0-3 的逐字比對不受影響。
3. 所以 #12 內只有一種合理的讀法；另一種讀法（要求示範路線的情境）需要上述契約外的取得方式，不構成 E-DA/D1。本 Design Authority 先前沒有對這個問題作過決定，不構成 E-DA/D2。

**現行實作與證據滿足 #12。** Skeleton 能到達的兩種來源（engine、目標 GPX）都有正確的灰色標籤與對應的路權提醒（事實 5；第 1–5 節的 AppTest 核對涵蓋 s08、s10、s13～s15）。

- **targeted correction：不需要。** 不要求加入示範路線的標籤分支或情境。
- **補充 evidence：不需要。**
- **worklog：不需要修改。** 這不是和 Issue 不一致的地方（UI0-10），因為 #12 沒有這項要求。

### 7.4 規格缺口與歸屬

- **規格缺口。** CR-01 把示範路線降為 Demo 與測試用的 fixture、拿掉了路線下拉選單，但沒有寫明示範路線在 Streamlit 介面中是否還會出現、怎麼出現（例如只用於測試與 CLI，或另有 Demo 的入口）。DELTA 第 6 節的三值標籤和 SPEC-001 的 `route_source = trip` 都假設它可能出現在結果中。
- **歸屬：之後正式整合的 `app/` Spec（owner：該 Spec 的 Design Authority）。** 該 Spec 要決定 `route_source = trip` 的結果是否會在介面上顯示；若會，路線確認區塊要依 DELTA 第 6 節顯示「示範路線」標籤，不能沿用 Skeleton「非 engine 就是目標 GPX」的二分（Skeleton 的模擬資料與情境依 `derivation-spec-ui0.md` 第 8 節不帶進正式整合的產品路徑）。
- **需要 acceptor 的情形。** 若結論是要讓騎士在介面上選用示範路線，這會牴觸 CR-B1（acceptor 2026-11-15 的裁決），屬 contract change（治理 §5.3），**required authority = acceptor**。acceptor 也可以在 UI Delta Review 提出這一點；那是 OC-1 §4.2 保留給 acceptor 的事，本 record 不代行。
- 這些都不擋 #12，也不是 #12 的要求。

### 7.5 語義、boundary、authority 與受影響的工作

- **不改變 accepted 語義**：只解讀 #12 已有的內容，沒有新增或放寬 requirement、AC 或情境。**在 OC-1 boundary 內**（`derivation-spec-ui0.md` 第 3 節）。**#12 不需要 acceptor**。**沒有 capability escalation**。
- **#12**：Q-1b 有了 disposition，對 #12 沒有要求；Orchestrator 在 P6 可以和 Q-1 一起引用本 record。
- **SPEC-UI0 的 SIA 與 phase acceptance**：同第 5 節；本 record 不代替已 closure 的 SIA record。
- **之後正式整合的 `app/` Spec**：第 7.4 節的規格缺口。

## 8. 澄清（2026-11-18）：本 run 的 SPEC-UI0 SIA 是另外派工的

本節依 SPEC-UI0 SIA R1 record `docs/governance/records/audit/spec-SPEC-UI0-c1-r1.md` 的 SIA-R1-N1（Low／non-blocking，owner 為本 record 的 Design Authority）加入。第 1–7 節的原文與裁決（Q-1、Q-1b）都不變；本節只更正其中對 SIA 形式的描述。

- **要更正的描述。** 第 5 節表格第二列寫「SPEC-UI0 的 SIA（fast path，由 #12 R1 兼任）」；第 7.5 節的「同第 5 節」沿用了這個描述。這和本 run 的實際做法不符。
- **本 run 的實際做法（已核對）。** acceptor 對本 run 的指示第 4 項是「Ticket 的 R1 不兼作 SIA，SIA 一律另外派工」。所以本 run 對 SPEC-UI0 **不採 fast path**：#12 的 R1、R2 是一般的 Ticket audit；SPEC-UI0 的 Spec Integration Audit 另外派工，record 是 `docs/governance/records/audit/spec-SPEC-UI0-c1-*`（R1 是 `spec-SPEC-UI0-c1-r1.md`，`Verdict: BLOCKING`；之後還有 R2）。依據：run record `run-20261117-oc1-run2.md` 第 1 節（第 29 行）、事件 46、事件 55 與 P9 列。`derivation-spec-ui0.md` 第 6 節的 fast path 是 Bindings 第 5 節的可選做法（治理 §4.7「MAY」）；本 run 依 acceptor 的指示不採用，derivation record 本身不改。
- **對 phase acceptance 的意思。** SPEC-UI0 的 Design Authority phase acceptance **必須引用另外派工的 SIA（`spec-SPEC-UI0-c1-*`）中已 closure 的 record**，不得引用 #12 的 Ticket audit record（`issue-12-c1-r1.md`、`issue-12-c1-r2.md`）作為 SIA closure。第 5、7.5 節「本 record 不代替已 closure 的 SIA record」的意思不變。
- **對本 record 結論的影響。** 沒有。Q-1、Q-1b 的 disposition 仍適用於 #12 的 P6，也可以由 SPEC-UI0 的 SIA 引用；本節不改變 accepted 語義，不需要 acceptor。
