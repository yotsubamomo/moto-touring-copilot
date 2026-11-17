# Decision record — C-10-7：契約驗證程式以 `isinstance(..., int)` 為前提的交叉檢查遇到整數值 float 時略過（CL-B1-15、CL-R1-11）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue10-c107`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 第 6 節事件 24–25）。問題來自 #10 Executor 在 R1 correction 的 return：worklog `docs/governance/records/worklog/issue-10.md` 第 10.5 節 **C-10-7**（required authority = Design Authority） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-B1 v1（`derivation-spec-b1.md`）的 clarification／修訂 **CL-B1-15**（治理 §5.3 第 2 類）；SPEC-R1 v1（`derivation-spec-r1.md`）的 clarification **CL-R1-11**（同類）。與 CL-B1-1～CL-B1-14、CL-R1-1～CL-R1-10 並列引用 |
| Subject 基準 | 主 checkout branch `oc1-run2-b1-ui0-r1-routing`，HEAD `9185aeb1cdc47c310e3172699aa5dd2e859a10a7`（#10 最終 implementation commit 是 `93e52b8`；之後只有 record-only commit），`git status --short` 為空 |
| 依據的條文 | 治理 §1.2、§2.1、§2.4、§2.5（E-DA）、§3.3、§3.4、§3.6（A）、§3.8、§4.3、§4.4、§5.3；Bindings m3 第 2.4、2.6（RB-7）、3.2、5、7 節；OC-1 §2.1 第 2、3 項、§3.1 AB-3／AB-10／AB-13、§4.1；`derivation-spec-b1.md` §2（「這三份契約既有的不變條件」）、§5 #10 列與 E-1～E-5、§6；`derivation-spec-r1.md` §5 R1-1 列（範圍 (c)、AC (4)）；CL-B1-9 第 3 項；CL-B1-12（`decision-20261118-issue10-pace-contract.md`）§3.2、§3.4、§8、§9；`decision-20261117-high-risk-categories.md` §3.4 第 3 項、§5 |
| 讀過的證據 | Bindings m3（第 2、4、5、7 節）；治理本文上列各節；OC-1 第 2、3、4 節；`derivation-spec-b1.md` 全文；`derivation-spec-r1.md` 第 4 節、R1-1 列、第 7–9 節；CL-B1-12～14 record 全文；高風險類別 record §3.2–§5；run record 第 1–6 節；worklog `issue-10.md` 表頭、第 1–5 節、第 10 節；`audit/issue-10-c1-r1.md` 全文；`DESIGN.md` §5 契約 3（欄位表與不變條件 1–7）；`src/moto_copilot/contracts/validate.py`（helpers、`validate_derived_segments` 的主鍵段、`validate_route_catalog`、`validate_pace_table` 全文）、`schemas.py` 的整數欄位；`tests/test_contracts.py` 第 214–226 行；`git blame`、`git log` 於 `validate.py` |

本 record 撰寫時實際執行的（不讀 GPX、不需金鑰；探測程式以 stdin 執行、只讀 `tests/fixtures/contract_v02/mock_dataset.json` 這份合成 fixture，沒有寫入 repo；執行後 `git status --short` 仍為空）：

| 指令／探測 | 結果 |
| --- | --- |
| `git rev-parse HEAD`、`git status --short` | `9185aeb…`；乾淨 |
| `git blame -L 247,254`、`-L 125,130`、`-L 203,206 src/moto_copilot/contracts/validate.py`；`git log -- validate.py` | 三處 guard 都來自 `9b3af99`（`[Baseline] Freeze Level 2 Lite MVP before CR-01`，v0.2 Spike）；#7（`a304ee2`、`8981e9d`）與 #10（`e0f6c78`、`93e52b8`）都沒有修改這三行 |
| `validate.py` 內 `isinstance(.*int)` 的使用處 | 第 87 行（`_whole_count` 本身）、第 128、205、250 行。只盤點這一種寫法；其他以整數為前提的路徑（例如當作索引或 `range` 的參數）沒有檢查，本 record 不對它們作任何陳述 |
| 契約 3（第 250 行）：fixture 的配速表（`min_segments` 2；C3 `n_segments` 1、`speed_kmh` null），把 C3 改成 `speed_kmh` 30.0、`stop_ratio` 0.0 | `n_segments` 為 `1` → `['pace_categories: C3 has speed_kmh with fewer than min_segments segments']`；為 `1.0` → `[]`；`n_segments` `1`、`min_segments` `2.0` → `[]`；`1.0` 經 `json.dumps`／`json.loads` 後仍是 float，仍回傳 `[]` |
| 契約 3 反方向：C2（`n_segments` 2）的 `speed_kmh`、`stop_ratio` 改為 null | `n_segments` 為 `2` → `['pace_categories: C2 has enough segments but speed_kmh is null']`；為 `2.0` → `[]` |
| 契約 3：不能計數的值（`n_segments` 為 1.5、`True`、`None`、`"1"`、NaN、Infinity、−1；`min_segments` 為 2.5、`True`、`None`、`"2"`、NaN） | 12 例的結果都不是空的（schema 回報違反）。**fail-open 只發生在 schema 接受的整數值 float** |
| 契約 1（第 128 行）：fixture 中 T001 的 `seg_index` `[0,1,2]` 把最後一個加 5（`[0,1,7]`） | 全為 int → `['derived_segments: trip T001 seg_index is not 0..n-1 without gaps']`；全為 float → `[]` |
| 契約 2（第 205 行）：R01（`n_segments` 4）一個中間檢查點的 `after_seg_count` 改成 9 | `9` → `['checkpoints: R01-CP02 after_seg_count 9 is outside 0..4 (invariant 2)']`；`9.0` → `[]` |

沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下任何腳本，沒有讀保留行程。

---

## 1. 問題

`validate_pace_table` 中「類別有 `speed_kmh` 但路段數少於 `min_segments`」與「路段數足夠但 `speed_kmh` 是 null」兩項檢查（DESIGN §5 契約 3 類別紀錄 `speed_kmh` 欄：「`null` 表示該類別的路段數低於 `min_segments`，不得用其他類別的值代替」），只在 `n_segments` 與 `min_segments` 都是 Python `int` 時執行。JSON Schema 的 `integer` 接受 `1.0`，所以同一份配速表在計數寫成整數值 float 時（含 JSON 檔中寫成 `1.0`、經 `json.loads` 讀入）兩項檢查都略過，回傳 `[]`。

要裁決的是：這屬於哪個 work item、怎麼處理；若要 #10 修改，列出檔案與證據要求。

## 2. 判斷

1. **與 R1-F1 是同一類缺陷，但不在 R1-F1 的 required fix 內。** R1-F1 的 required fix 只指合計檢查（`audit/issue-10-c1-r1.md` R1-F1）。Executor 依治理 §4.4「targeted correction 不夾帶無關 scope expansion」沒有修改，並依 §2.4 route，做法正確。
2. **檢查來自 v0.2 Spike，不是 #7 或 #10 造成的。** 但它是 SPEC-B1 的範圍：`derivation-spec-b1.md` §2 引用「契約 1、契約 3、契約 4 … 這三份契約既有的不變條件」，OC-1 §2.1 第 3 項要求 Spike「依 Spec 檢視，符合的納入，不符合的返工」。契約 3 的這條規則屬 SPEC-B1，而 SPEC-B1 中目前修改 `contracts/validate.py` 契約 3 段落、而且尚未結案的只有 #10（CL-B1-12 §3.4）。
3. **涉及 #10 已標示的 H-4。** #10 的 H-4 標示是「配速為 `null` 的處理與預設值」（判定 3.4 第 3 項）。`speed_kmh` 為 null 是 ETA 回報 `unknown` 的前提（契約 4 不變條件 7）；路段數不足卻帶有速度的配速表通過契約檢查，會削弱這道 fail-closed 的防線。`create_pace_table` 自己寫出的計數是 `int`，所以這個缺陷不影響 #10 產生的檔案；受影響的是以 `validate_pace_table`／`validate_dataset`（含 `python -m moto_copilot.contracts <json>`）檢查外部提供或手寫的配速表的路徑。
4. **語義只有一種合理讀法。** DESIGN 契約 3 的 `n_segments`、`min_segments` 型別是 int，schema 以 JSON Schema `integer` 表示，它接受整數值 float。契約檢查應對 schema 接受的每一種整數表示都執行，這也是 R1-F1 修正在同一個函式中採用的做法（`_whole_count`）。另一種做法（schema 改為拒絕 `1.0`）會改變 schema 的接受範圍、需要連帶修改其他整數欄位與既有測試，而且和同一函式中已採用的修正不一致；以既有證據即可裁決，不構成 E-DA/D1。本問題不是先前 DA 決定被 FA ruling 或 Reviewer finding 推翻，不構成 E-DA/D2。
5. **同類缺陷另有兩處**（第 128、205 行，見開頭的探測）。逐項分配，避免同一類問題在 R2 或 SIA 再出現一次：
   - 第 128 行（契約 1 的主鍵：每趟 `seg_index` 是 0..n−1 不跳號）：契約 1 既有的不變條件，屬 SPEC-B1 §2；同一檔案、同一 helper、同一種修改。SPEC-B1 中唯一尚未結案、正在修改 `validate.py` 的是 #10，併入 #10。
   - 第 205 行（契約 2 不變條件 2）：契約 2 屬 SPEC-R1。R1-1（#13）的範圍 (c) 與 AC (4) 已涵蓋「契約 2 不變條件 1–5 各有一個違反的案例被拒絕」，而且 R1-1 尚未開始，它的 R1 會完整審查。併入 R1-1，不併入 #10。
6. **不採用的歸屬：**

| 做法 | 不採用的理由 |
| --- | --- |
| 重開 #7 | #7 已在前一個 run 結案；缺陷早於 #7，#7 的 7 項 AC 不涉及這兩條檢查。CL-B1-12 §3.4 對同一檔案已採同一原則：不重開 #7 |
| Tracked item，SPEC-B1 結案後再處理 | 在 acceptor 接受前不得執行（治理 §1.2），已知的 fail-open 會留過 SPEC-B1 的 SIA 與 phase acceptance；而這項修改在 OC-1 boundary 內，可由 DA 直接 derive 進仍在進行的 Ticket，不需要另一份契約 |
| 留給 SPEC-B1 的 SIA | SIA 是 audit，不是修改的載體；到時只會成為 finding 再 rework，subject 在 SIA 之後再變 |
| R2 之後才改 | R2 closure 之後再改 subject，又需要另一次審查；Orchestrator 在 R2 前取得裁決正是為了避免這種情形 |
| 另建 Ticket | 修改只有兩行、與 #10 已修改的同一函式與 helper 相同；另建 Ticket 會讓同一檔案的同類修改分在兩個 subject，協調成本高於收益 |

## 3. 裁決

### 3.1 CL-B1-15（SPEC-B1，併入 #10）

契約驗證程式中，以「值是整數」為前提的交叉檢查，對 schema 接受的每一種整數表示都要執行：以 `validate.py` 既有的 `_whole_count` 取得計數（`int` 照用，有限且為整數的 float 轉成 `int`，其他值不可計數）。

1. **契約 3（`validate_pace_table` 第 247–254 行）**：`n = _whole_count(rec.get("n_segments"))`、`minimum = _whole_count(header.get("min_segments"))`；兩者都可計數時執行現行的兩項檢查，比較方式與訊息不變。任一不可計數時不執行這兩項，也**不另加訊息**：開頭的探測顯示這些值都已由 schema 回報違反，結果不會是 `[]`。
2. **契約 1（`validate_derived_segments` 第 128 行）**：以 `_whole_count` 轉換每個 `seg_index`；全部可計數時以轉換後的值做現行的不跳號檢查，訊息不變。有任何不可計數的值時不執行此項（schema 已回報），不另加訊息。
3. 其他檢查、schema、`pace_eligible`、R1-F1 修正後的不變條件 3 一段都不變。契約 2 第 205 行**不在** #10（見 3.2）。

### 3.2 CL-R1-11（SPEC-R1，併入 R1-1／#13）

R1-1 實作契約 2 不變條件 2 的檢查時（`validate_route_catalog`，現行第 205 行），`after_seg_count` 與路線的 `n_segments` 都以 `_whole_count` 取得計數；兩者都可計數時做範圍檢查，訊息不變；不可計數時由 schema 回報，不另加訊息。R1-1 AC (4) 中不變條件 2 的違反案例，另加一例以整數值 float（含 JSON round trip）表示的超出範圍值，同樣被拒絕。R1-1 的其他範圍、AC 與「高風險類別：不涉及」不變。R1-1 以含 #10 最終 commit 的 HEAD 為 BASE（CL-B1-12 §9），`_whole_count` 已存在，不得回復 #10 對 `validate.py` 的修改。

## 4. 是否改變 accepted 語義

**否。** DESIGN 契約 1、2、3 的欄位型別、不變條件與 `speed_kmh` 欄的規則都不變；本裁決只讓既有的檢查對 schema 已接受的整數表示照常執行，不新增或移除任何 Must、AB、AC 的判準或 gate。沒有建立其他工作將依賴的新設計基線：「整數值 float 視為計數」是 JSON Schema `integer` 的既有語義，R1-F1 的修正已在同一函式採用。

## 5. Boundary determination

**在 OC-1 boundary 內。** CL-B1-15：OC-1 §2.1 第 2 項（`contracts` 更新到 v0.3）、第 3 項（Spike 的收編或返工）；SPEC-B1 §2 引用的三份契約既有不變條件；已分配給 SPEC-B1 的 AB-3、AB-10、AB-13 部分。CL-R1-11：同上第 2 項；SPEC-R1 R1-1 已分配的 AB-2、AB-13 部分。只用合成資料與既有 fixture（OC-1 §2.3）。不涉及 RB-1～RB-7。**不需要 acceptor。**

## 6. 對 #10 的具體要求（同一 Ticket、cycle 1；在 R2 派工之前完成）

| 檔案 | 要求 |
| --- | --- |
| `src/moto_copilot/contracts/validate.py` | 只改第 3.1 節第 1、2 項的兩處；模組說明可補一句。其他函式與檢查不變，第 205 行不改 |
| `tests/test_contracts.py` | 只新增測試（fixture 的副本，在測試內修改）。契約 3：(i) C3 `n_segments` `1.0`、帶 `speed_kmh`（與非 null 的 `stop_ratio`）→ 回報 `C3 has speed_kmh with fewer than min_segments`；(ii) `n_segments` `1`、`min_segments` `2.0` → 同上；(iii) C2 `n_segments` `2.0`、`speed_kmh` 與 `stop_ratio` 為 null → 回報 `C2 has enough segments but speed_kmh is null`；(iv) (i)–(iii) 各以原物件與 JSON round trip 後的資料執行；(v) 全部計數寫成整數值 float、內容正確的配速表 → 這兩項檢查沒有違反；(vi) 第 3.1 節第 1 項不可計數的值（至少 1.5、`True`、`None`、`"1"`、NaN）→ 結果不是空的。契約 1：(vii) 某趟的 `seg_index` 全為 float 且跳號 → 回報 `seg_index is not 0..n-1 without gaps`；全為 float 且不跳號 → 沒有該違反；各以 JSON round trip 執行一次 |
| `docs/governance/records/worklog/issue-10.md` | 新增一節：引用本 record（CL-B1-15）；C-10-7 標為已裁決；E-2 加入上列測試；E-4 寫明沒有修改既有測試（若有，逐項寫理由）；突變檢查：把兩處換回 `isinstance(..., int)` 的寫法時新增測試失敗的數目，還原後全部通過；E-5 依下列高風險核對更新 |

- **Commit**：與 `93e52b8` 分開的一個 implementation commit，只含上列程式與測試檔，message 註明 CL-B1-15。它成為 #10 的最終 implementation subject。
- **E-1**：在新的最終 subject 依 CL-B1-9 第 3 項重新執行三個命令（`-q`、`-q -rxX`、`--runxfail` 加五個測試檔），完整 stdout、exit code 與 subject 識別原樣記在 worklog（R1-F2 的要求同樣適用：不縮寫、不改字）。第 10.3 節的 `93e52b8` 輸出保留為歷程，不再是最終 E-1。
- **不改**：`schemas.py`、`pace/`、`ingest/`、`routes/`、fixture、`conftest.py`、`pyproject.toml`、`DESIGN.md`、任何 Issue 內文。
- **高風險類別**：#10 的 H-2、H-3、H-4 標示不變。契約 3 的修改落在 H-4（判定 3.4 第 3 項）：self-verification 須顯示路段數不足卻有速度、路段數足夠卻沒有速度，在每一種 schema 接受的計數表示下都回報違反，不可計數的值不會得到 `[]`。契約 1 的修改不涉及 H-1～H-3，也不是決策關卡（H-4）的程式。

## 7. Audit coverage（治理 §3.8、§4.4）

這次修改是 R1 之後由 DA 修訂 derived contract 帶來的變更，不是 Executor 的 targeted correction 夾帶的 scope。治理 §3.8 規定審後變更需要相應的驗證，必要的後續由 Reviewer／Design Authority 判定。本 record 判定：

1. #10 cycle 1 的 R2 以含 CL-B1-15 的最終 subject 為受審 subject，派工 pack 包含本 record。R2 除了治理 §4.4 的三項（R1-F1、R1-F2 是否解決、有沒有回歸、修正直接產生或暴露的 blocking defect；C-10-7 正是 R1-F1 修正所暴露的同類缺陷），另須對 CL-B1-15 的 delta 作獨立審查，範圍限於第 3.1 節的兩處程式、第 6 節的測試與證據要求、E-1，以及 `validate.py` 沒有其他變更。這是該 delta 的第一次獨立審查，不是擴大為無限制的全面 audit，也不是新增 audit round 或 cycle reset。
2. R2 之後仍有未解的 blocking（不論來自 R1 findings 或 CL-B1-15 的 delta）時，依治理 §4.4 派 exactly one Alternate Review，不增加 R3。
3. 契約 1 的修改也在 SPEC-B1 SIA 的範圍內（SB1-AC3 的 `validate_dataset`）。SIA 不得把契約 2 第 205 行記為 SPEC-B1 已涵蓋：它屬 R1-1。

## 8. 受影響的 work items 與 evidence

| Work item／evidence | 影響 |
| --- | --- |
| #10 B1-3 | 範圍依第 3.1、6 節擴大；CL-B1-12 §8「`validate.py` 只改不變條件 3 一段」的限制由本 record 放寬，只多出第 3.1 節的兩處。Issue #10 的內文與 8 項 AC 不改（OC-1 D-3）。最終 implementation subject 由 `93e52b8` 改為 CL-B1-15 的 commit；`93e52b8` 上的 `404 passed, 3 xfailed` 與第 10.3 節的 E-1 成為中間結果 |
| #10 R2（尚未派工） | 依第 7 節派工；pack 加入本 record |
| #7 B1-1（已結案） | 不重開。缺陷早於 #7，#7 的 AC 與 evidence 不受影響 |
| #11 B1-4 | 不變。它的 ETA 以 fixture 的 `int` 計數為輸入，不受影響 |
| R1-1（#13，SPEC-R1） | 依第 3.2 節（CL-R1-11）多一項要求；Issue #13 內文不改（Issue 與 derivation record 不一致時以 derivation record 及其 clarifications 為準，run record 第 4 節）。R1-1 的 pack 須包含本 record |
| SPEC-B1 SIA | SB1-AC3 不受影響：fixture 的計數都是 `int`。第 7 節第 3 項的限制適用 |
| 其他以整數為前提的路徑 | 本 record 只盤點 `isinstance(..., int)` 的寫法（第 128、205、250 行）；其他路徑沒有檢查，不宣稱已無同類問題 |

`derivation-spec-b1.md`、`derivation-spec-r1.md` 與先前的 CL records 沒有被修改；SPEC-B1 v1 的引用集合由本 record 補上 CL-B1-15，SPEC-R1 v1 補上 CL-R1-11。

## 9. 需要其他 authority 的事項

無。兩項裁決都不改變 accepted 語義，都在 OC-1 boundary 內，不需要 acceptor；不觸發 escalation（第 2 節第 4 項）。真實行程上的行為仍是 NOT VERIFIED（RB-7，required authority = acceptor），不在本 record 範圍。

本 record 只執行了開頭表格中的指令；沒有修改程式、測試、Spec、Issue 或其他 record，沒有派工任何 subagent，沒有 commit。
