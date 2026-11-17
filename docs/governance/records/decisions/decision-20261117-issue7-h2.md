# Decision record — #7 是否涉及高風險類別 H-2

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261117-issue7-h2`（v1） |
| 日期 | 2026-11-17 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-issue7`（run record 第 5 節事件 4）。問題來自 #7 Executor worklog 第 8 節 concern C-1 |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-B1 v1（`derivation-spec-b1.md`）。本 record 補充第 5 節 #7 列的「高風險類別」欄（第 3 節） |
| Subject | branch `oc1-run1-contracts-v03`，BASE `ff049661f968adace4dd017cf560316e5684440d`，HEAD `3614053`（實作 commit `a304ee2`） |
| 依據的條文 | 治理 §1.2、§2.4、§4.1、§4.5、§5.1、§5.3；Bindings m3 第 2.6 節 RB-7、第 3.2 節 E-DA、第 3.7 節第 3 項、第 5 節；`decision-20261117-high-risk-categories.md` §3.2、§4、§5 |
| 讀過的證據 | `decision-20261117-high-risk-categories.md`；`derivation-spec-b1.md`；`decision-20261117-issue7-spike-tests.md`（表頭與第 1 節）；`docs/governance/records/worklog/issue-7.md`；`docs/governance/records/run/run-20261117-oc1-issue7.md`（工作目錄版本）；Bindings m3 RB-7、第 3.3 節 Codex 外送段、第 3.7 節第 3 項、第 5 節 release gate；Issue #7（`gh issue view 7`，唯讀）；`DESIGN.md` §5 契約 1（含欄位表「公開版」欄、不變條件 5、6）與 NFR2、§6.1 相關段落；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` 中 `short_stop_time_s` 的段落與第 8 節的批准；`git diff ff04966..3614053`（`schemas.py` 全部、`validate.py` 開頭與 `validate_public_private_pair`、fixture 全部、`tests/test_ingest.py` 中與公開版有關的行）；`tests/test_contracts.py` 中公開版與 `short_stop_time_s` 的測試；`src/moto_copilot/ingest/` 中 `to_public` 的位置與 `__main__.py` 對公開版的驗證呼叫。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行任何測試或 `experiments/` 腳本 |

## 1. 問題

SPEC-B1 §5 #7 列只標示 H-3、H-4。#7 Executor 在 worklog 第 8 節 C-1 指出：#7 在契約 1 的公開版 schema 新增欄位 `short_stop_time_s`，字面上符合 H-2 判定 3.2 第 2 項（「新增或修改……公開版衍生路段表的產生與欄位」），依判定程序第 2、3 項不記為「不涉及」而 route 至 Design Authority。

本 record 判定：(1) #7 是否涉及 H-2；(2) 若涉及，#7 的 independent audit（R1）應增加的最低核對範圍。

## 2. 判定

**#7 涉及 H-2（判定 3.2 第 2 項）。** SPEC-B1 §5 #7 列漏標 H-2；#7 的高風險類別改為 **H-2、H-3、H-4**。

### 2.1 依據

1. **字面符合。** `src/moto_copilot/contracts/schemas.py` 的 `_DERIVED_PUBLIC` 是契約 1 公開版欄位的唯一定義；`_record` 設 `additionalProperties: False`，所以它同時是公開版**允許出現哪些欄位**的 allowlist。#7 在其中新增 `short_stop_time_s`，就是「修改公開版衍生路段表的欄位」。判定 3.2 第 2 項以「產生與欄位」並列，修改其中之一即符合；不要求同時修改產生程式。
2. **功能上也是隱私控制。** `ingest/__main__.py` 以 `validate_derived_segments(public_rows, "public")` 與 `validate_public_private_pair` 檢查要進版控的公開版（DESIGN §5 契約 1：「公開版進版控」）；`ingest.to_public` 只移除 `start_time`，其餘欄位原樣帶入。因此擴大這份 allowlist，會直接擴大 #9 之後由私有 GPX 導出、預定進版控的公開內容。這正是 H-2 範圍中「由 GPX 導出的……時間序列」與「公開版衍生路段表」所要保護的路徑。
3. **判定程序的 fail-closed。** 即使對第 1、2 點有疑義，高風險類別 record §4 第 2 項規定無法確定時不得記為「不涉及」。
4. **欄位本身是已接受的設計，不影響「涉及」與否。** DESIGN §5 契約 1 欄位表把 `short_stop_time_s` 的「公開版」欄標為「有」，該欄位由 SPEC-RESOLUTION-001 第 8 節的裁決批准（2026-11-15）。「涉及」只決定 assurance（audit 須核對的內容與 deferral 限制），不表示這項設計有誤，也不使 #7 需要改變範圍或 AC。

### 2.2 為何 SPEC-B1 原先沒有標示

`derivation-spec-b1.md` 對 #7 只評估了 `pace_version` 的樣式（H-3）與契約 4 的 `unknown` 不變條件（H-4），沒有對契約 1 公開版的欄位變更逐項套用判定 3.2。高風險類別 record §8 對 `contracts`（B1-1）的初步判斷是「視其變更是否碰到上述路徑」，derivation 時應作出而未作出這項判定。這是 derivation 的遺漏，以本 record 補正。

### 2.3 不構成 capability escalation

- 不是 E-DA/D1：判定 3.2 第 2 項的字面與 §4 第 2 項的 fail-closed 規則已足以裁決，沒有兩個後果實質不同而證據無法裁決的合理選項。
- 不是 E-DA/D2：對 SPEC-B1 #7 列的質疑來自 Executor 的 concern，不是 Final Adjudicator ruling 或經 route 的 Reviewer finding。

## 3. 對 SPEC-B1 的影響

- SPEC-B1 v1 §5 #7 列的「高風險類別」欄，以本 record 為準讀作：**H-2**（契約 1 公開版的欄位 allowlist 新增 `short_stop_time_s`，判定 3.2 第 2 項）、**H-3**、**H-4**（後兩者與原標示相同）。
- #7 的範圍、AC、依賴、CL-B1-1、CL-B1-2、CL-B1-8 與 E-1～E-4 都不變。E-5 的「標示的高風險類別」自此包含 H-2。
- 依高風險類別 record §4 第 3 項，Orchestrator 依本標示機械處理，不自行降級。
- 本 record 不修改 `derivation-spec-b1.md`；之後引用 SPEC-B1 #7 的高風險類別時，同時引用本 record。

## 4. R1 的最低核對範圍變化

R1 對 #7 原有的 H-3、H-4 最低核對範圍不變（高風險類別 record §5）。**增加 H-2**，以下各項依 §5 的 H-2 項目，針對 #7 的 diff 具體化。不新增 round 或 audit instance；R1 的 audit record 須逐項寫明結果與依據。

| # | 核對內容 | 對應 §5 H-2 項目 |
| --- | --- | --- |
| H2-R1 | 在 subject HEAD 執行 `git ls-files`：不含 Bindings 第 5 節 release gate 所列路徑（`.env`、`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/`），也沒有任何 `data/` 下的路徑 | `git ls-files` |
| H2-R2 | `git diff ff04966..<subject HEAD>` 的全部新增內容（`src/`、`tests/`、fixture，以及同一範圍內新增的 records：worklog、run record、CL-B1-8 record）中，座標、軌跡、逐點時間、行程時間都是合成資料並可追溯來源。至少確認：(a) fixture 沒有新增或修改任何座標，`private_start_times` 沒有變更；(b) fixture 新增的 `short_stop_time_s`、`stop_ratio`、`stop_allow_s` 與重算的 `eta_typ`／`eta_safe` 可由 fixture 自身既有的值依 DESIGN §5／§6.1 的算式推出（worklog E-3 列出推導，R1 自行重算，不採信敘述）；(c) `tests/test_contracts.py` 新增的測試只用 fixture 或字面的合成值；(d) worklog 第 6 節輸出 4 來自 repo 外的暫存腳本，R1 無法檢視該腳本，只核對輸出內容：其中的數值只能是合成產生者呼叫（`straight(...)` 等）與 fixture 的結果，不得出現看似真實行程的時間、日期或座標 | diff、fixture、紀錄與 evidence 中的座標、軌跡、時間 |
| H2-R3 | **公開版 allowlist 的變更只有這一項而且只能帶數值。** (a) `_DERIVED_PUBLIC` 相對 BASE 只新增 `short_stop_time_s`，其 schema 是非負數（不接受字串、日期或時間），與 DESIGN §5 契約 1「公開版：有」一致；沒有新增或放寬其他公開欄位；(b) `_record` 的 `additionalProperties: False` 與「私有版＝公開版＋`start_time`」的結構不變；(c) `test_public_version_rejects_start_time` 與 `test_public_rows_hold_no_date_time_or_coordinates` 沒有被刪除或放寬；(d) `validate_public_private_pair` 仍逐欄比對公開版的全部欄位（因此涵蓋新欄位），沒有被修改成略過任何欄位 | 隱私控制本身（判定 3.2 第 2 項的對象） |
| H2-R4 | #7 沒有新增或修改開啟 GPX、FIT、`data/` 下檔案或寫出衍生輸出的程式：`contracts` 的 diff 沒有新增檔案 I/O，契約 CLI 的讀取路徑不變；`src/moto_copilot/ingest/`、`pace/`、`routes/` 與 `.gitignore` 在 diff 中沒有變更 | 判定 3.2 第 1、6 項（確認不涉及） |
| H2-R5 | 以下 §5 H-2 項目對 #7 不適用，R1 依 diff 證據逐項記為 N/A 並寫明依據，不得靜默略過：送往第三方的內容符合 NFR2（#7 沒有任何對外請求）；隱私裁切與錨點代換有測試（#7 沒有碰 `ingest` 的裁切與路線請求） | 送往第三方；隱私裁切與錨點代換 |
| H2-R6 | R1 不讀 `data/`。需要私有資料才能核對的項目（例如以真實行程產生的公開版列帶 `short_stop_time_s` 後的實際揭露程度），依 Bindings 第 3.7 節第 3 項記為 NOT VERIFIED，回報 required authority = acceptor，不記為已驗證。#7 本身不產生、不提交任何真實的公開版列，所以這類項目不屬 #7 的 closure 條件 | Bindings 第 3.7 節第 3 項 |

**Finding 的處理（高風險類別 record §5）。** H-2 的 blocking finding 不得由 Final Adjudicator 單獨 defer。主張私有資料已進入 git 歷史或已提交紀錄的 finding 不得 defer，受影響路徑停止並 route 至 acceptor。R1 若認為公開版帶 `short_stop_time_s` 這項**設計**本身有隱私疑慮，那是對已接受設計（DESIGN §5 契約 1、SPEC-RESOLUTION-001 第 8 節）的質疑，以 finding 提出並 route 至 acceptor（contract change，治理 §5.3），不在 #7 內以實作變更處理。

**R1 的資料外送。** R1 由 Codex 執行，Codex 會把讀到的內容送往 OpenAI（Bindings 第 3.3 節）。本 record 不改變其範圍：bounded pack 照常寫明 RB-7 的禁令，只含追蹤中的 repo 內容。

## 5. Executor 的 self-verification（E-5）

本 record 不要求重新派工 Executor。Worklog 第 6 節 E-5 已有一段 H-2 的 self-verification（Executor 當時記為「不構成 H-2 的判定」）；該段自此視為 E-5 對 H-2 的 self-verification。它是否充分由 R1 判斷，本 record 不作判定；self-verification 不得記為 audit（治理 §2.3）。

## 6. 是否改變 accepted 語義

**否。**

- 決定高風險類別及其 assurance 要求是治理 §5.1 指定給 Design Authority 的權限，高風險類別 record §4 第 3 項由 Design Authority 在 Formal 中逐票標示；補標 H-2 在此權限內。
- 沒有改變 OC-1 的 intent、scope、constraints 或 acceptance semantics，也沒有改變 Issue #7 的範圍、AC，或 DESIGN §5 契約 1 的欄位與「公開版」標示。`short_stop_time_s` 進入公開版是 acceptor 已批准的設計（SPEC-RESOLUTION-001 第 8 節）。
- 不放寬任何 reserved boundary；不授權任何 `data/` 的讀取或私有資料的公開（RB-7）。

因此不需要 acceptor。

## 7. 受影響的 work items 與 evidence

| 項目 | 影響 |
| --- | --- |
| #7（run `run-20261117-oc1-issue7`） | 高風險類別為 H-2、H-3、H-4。R1 的 bounded pack 須引用本 record 並納入第 4 節 H2-R1～H2-R6。R1 尚未派工（run record 事件 4），沒有既有 audit 需要重做 |
| Run record 事件 4 | 由 Orchestrator 記錄本裁決與 record 路徑；Orchestrator 只核對 record 存在 |
| SPEC-B1 的 Spec Integration Audit（不在本 run） | 對 #7 的 H-2 涵蓋，以本 record 的標示為準 |
| #9（B1-2，已標 H-2） | 不改標示。提醒：#9 完成後 `ingest` 會以真實 GPX 產生帶 `short_stop_time_s` 的公開版列；把任何真實的公開版衍生路段表放進 git 時，仍須依高風險類別 record §3.2 末段由該 work item 向 acceptor 確認 RB-7(3) 的授權範圍。這是既有的未決事項，本 record 沒有判定，也沒有擴大或縮小它 |
| #8、#10、#11 | 不受影響 |
| Executor worklog C-1 | 由本 record 回覆。本 record 不修改 worklog |

## 8. 需要其他 authority 的事項

無。本 record 不需要 acceptor，也不需要 escalation。

本 record 沒有執行任何測試或腳本，沒有讀取 `data/` 或 `.env`，沒有派工任何 subagent，沒有修改程式、測試、Spec、Issue 或其他 record，沒有 commit。
