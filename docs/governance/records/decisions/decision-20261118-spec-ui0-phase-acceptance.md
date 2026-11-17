# Decision record — SPEC-UI0 v1 的 Design Authority phase acceptance

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-spec-ui0-phase-acceptance`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | OC-1 第二個 Formal run 的 Orchestrator：`docs/governance/records/run/run-20261117-oc1-run2.md`（事件 58 之後；orch-default v2.2 §5「phase acceptance」、§6、§7 P10） |
| Outcome Contract | OC-1（`docs/governance/records/outcome-contract.md`），acceptor 2026-11-17 針對 `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受。之後該檔只有狀態欄與第 10 節接受紀錄的轉錄（`01f3ea4`），條文未變（本次以 `git diff 873e37a..HEAD` 核對） |
| Spec | **SPEC-UI0 v1**：`derivation-spec-ui0.md`（commit `8c3c588`，至 HEAD 未修改）＝第 2 節引用的段落（Issue #12 全文、`DESIGN.md` §9.6、`UI_CR01_DELTA.md` 第 11、12 節、`ui0_decision_table.md` U-1～U-22、G3 凍結的 UI 文件中沒有變更的部分）＋CL-UI0-1～CL-UI0-5；其 clarifications：`decision-20261118-issue12-ui0.md`（C-1～C-3，CL-UI0-2 的釐清）、`decision-20261118-issue12-ui07.md`（UI0-7 的範圍、CL-UI0-4 的意思）、`decision-20261118-issue12-q1.md`（Q-1、Q-1b；第 8 節的 SIA 形式澄清）；跨 Spec 決定 `decision-20261117-oc1-first-run-derivation.md`（BD-2、BD-3、第 4 節 AB 分配）；高風險類別 `decision-20261117-high-risk-categories.md` |
| Ticket | #12（UI-0）。Issue 原文：派工所附 `issue-12-body.md`，本次實測 SHA-256 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be`，等於 BD-3。沒有呼叫 GitHub |
| 受審狀態 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `df50dfd95808857deb3cd4b6a02cf9bc88ffcfe9`（`git rev-parse HEAD` 核對；`git status` 乾淨） |
| 依據的條文 | 治理 §1.2、§2.1、§2.4、§2.5、§3.8、§4.7、§5.1、§5.3；orch-default v2.2 §5、§6、§7（P1–P10）；Bindings m3 第 2.6、5、7 節；OC-1 §2.1 第 4 項、§2.2、§3.1（AB-8、AB-10、AB-13）、§3.2、§4.2 |
| **結論** | **接受（ACCEPT）SPEC-UI0 v1 的 phase acceptance**，限第 6 節所列的分配範圍與第 8、9 節的限制。**UI Delta Review 不在本接受內，仍待 acceptor**（OC-1 §4.2；AB-8 的另一項證據）。不改變 accepted 語義；在 OC-1 boundary 內；不需要 acceptor 的接受或授權；沒有 escalation。不是 release authorization、不是 run completion、不是 OC-1 completion，也不是正式介面整合的開始條件；不變更 Issue #12 |

## 1. 問題

依治理 §3.8 與 orch-default §7 P10：SPEC-UI0 唯一的 Ticket #12 已結案、SPEC-UI0 另外派工的 Spec Integration Audit 已 closure 之後，SPEC-UI0 能否作 phase acceptance——Spec 層級的 invariants、整合行為、累積 evidence 與未結 follow-ups 是否足以接受；接受的範圍與限制為何；AB-8 中哪些部分仍待 acceptor。

## 2. 裁決

**接受。** 理由：

1. **SIA 已 closure（P10 的前半）。** 本 run 依 acceptor 指示第 4 項不採單 Ticket fast path（run record 第 1 節；`decision-20261118-issue12-q1.md` 第 8 節）。另外派工的 SIA 最後有效 record `spec-SPEC-UI0-c1-r2.md` 為 Reviewer closure（`Verdict: PASS`）：唯一 blocking 的 SIA-R1-F1 RESOLVED、SIA-R1-N1 RESOLVED，沒有未解 blocking，沒有新增 finding（第 3 節）。本 record 引用之，不豁免、不取代它；**不**引用 #12 的 Ticket audit records 作為 SIA closure。
2. **#12 依 orch-default §7 P1–P8 結案**（run record §8.1），P9 留在 phase 層並由 SIA 滿足；結案後的 SIA correction（`1ce4640`）不是 Ticket 重開，已由 SIA R2 審查 closure 與回歸（第 4 節）。
3. **Spec 層級的 invariants 與整合行為**在 SIA R1／R2 的審查與本 DA 的獨立核對中都成立，限於合成資料與 Skeleton 的範圍（第 5 節）。
4. **`derivation-spec-ui0.md` §6 的四項 Spec 層級 AC 都有 evidence**，合起來涵蓋 §7 分配給本 Spec 的 AB 部分（第 6 節）。本 DA 在 HEAD `df50dfd` 重跑的 gates 與 SIA R2 的結果一致。
5. **未結 follow-ups 都有 owner 與 authority，沒有任何一項是 SPEC-UI0 Spec AC 的未完成部分**：它們或屬 acceptor 的 UI Delta Review、或屬之後正式整合的 `app/` Spec（G-APP）、或需 acceptor 的 RB-7 授權（第 7、8 節）。沒有影響本 Spec 完成的未決 design ambiguity。
6. **不需要 escalation。** Phase acceptance 的後果可由現有 evidence 裁決（E-DA/D1 不成立）。本 DA 先前就 SPEC-UI0 所作的決定沒有被 FA ruling 或 Reviewer finding 推翻或實質爭議：SIA-R1-F1 是對最終 Spec subject 的 coverage finding，指向 Executor 的交付，不是推翻 DA 決定；SIA-R1-N1 指出 `decision-20261118-issue12-q1.md` 對 SIA 形式的描述與本 run 不符，DA 以第 8 節澄清、原裁決不變，SIA R2 判為 RESOLVED；`derivation-spec-ui0.md` §6 的 fast path 是 MAY，被 acceptor 的 run 指示選擇不用，不是被推翻（E-DA/D2 不成立）。本 run 沒有 FA ruling 涉及 SPEC-UI0。

## 3. 所引用的 Spec Integration Audit closure record

| 項目 | 內容 |
| --- | --- |
| **Closure record** | `docs/governance/records/audit/spec-SPEC-UI0-c1-r2.md` — Spec Integration Audit of SPEC-UI0，cycle 1，R2 closure review；`primary_reviewer` Codex 自寫；最後一行 `Verdict: PASS` |
| Closure record 的 SHA-256 | `07114d721cd82098c3e6c5bfbcd9d1d0ed66dcc8b0441b521141ca34b7002867`（本 DA 以 `git show HEAD:<path> \| sha256sum` 與工作目錄檔案核對，兩者相同，且等於 run record 事件 58 記載的值；commit `7bc54c0`） |
| **Subject** | BASE `3906e077ab850c027d7833b30d3eebfa16f67761`，HEAD **`53011947731ed511c55bb97be54588bcf96b79ef`** |
| 同一 audit instance 的 R1 | `docs/governance/records/audit/spec-SPEC-UI0-c1-r1.md`，subject `ca07b7c1a680fe309e9aa82321c3a9af269f1a3e`，`Verdict: BLOCKING`（SIA-R1-F1 Medium／blocking：`UI_CR01_DELTA.md` §11.3 明列的「Planner 的補充說明沒通過規則 5」合成呈現缺漏；SIA-R1-N1 Low／non-blocking）；SHA-256 `db4cb35bdcd0f90efe193dc7c110dddcf8fc1d8eb688d6a3f9019958ac0572b3`（等於事件 55） |
| 修正 | `1ce4640`：`app/ui0_mock_app.py`（補充說明只在資料有值時顯示）、`app/ui0_scenarios.py`（`PLAN_SUPPLEMENT_FAILED`、情境 s16，寫定資料）、`tests/test_ui0_skeleton.py`（3 個 regression tests）；#12 Executor，同一 worklog identity（事件 56；`worklog/issue-12.md` 第 12 節）。SIA-R1-N1：`decision-20261118-issue12-q1.md` 第 8 節（事件 57，10 行新增、0 行刪除） |
| Flow | R1 BLOCKING → targeted correction → R2 PASS。沒有 Alternate Review、沒有 FA；獨立 audit instance，不是 #12 Ticket audit 的 R3 |
| Binding 與存取的派工者核對 | R1：事件 55（含 record 自行揭露的 pytest 暫存目錄存取偏差，被 sandbox 拒絕、沒有取得內容）；R2：事件 58。兩者的 rollout `turn_context` 集合都只有 (`gpt-6.1-sol`, `high`, `workspace-write`)，worktree 只多出各自的 record，原樣複製後 hash 相同。R2 record 的 NV-R2-SIA-1（「binding 由 dispatcher 核對」）由事件 58 填入。本 DA 只核對這些紀錄存在且一致，不重查外部 rollout |
| Subject 與目前 HEAD 的關係 | 目前 HEAD `df50dfd`；`git diff --name-status 5301194..df50dfd` 只有 `docs/governance/records/audit/spec-SPEC-UI0-c1-r2.md`（新增）與 `docs/governance/records/run/run-20261117-oc1-run2.md`（修改），都是 Bindings 第 7 節的 record-only paths（orch-default §7 P7 fast path）。`1ce4640..df50dfd` 也只有 record-only paths。`3906e07..df50dfd` 的非 record delta 只有 `app/` 四個檔、`tests/test_ui0_skeleton.py`、`.streamlit/config.toml`、`pyproject.toml` |

## 4. Ticket closure（Spec 層級 AC 第 1 項）

| Ticket | 最後有效 Ticket audit record | 受審 subject | 最後實作 commit（Ticket） | Completion predicates |
| --- | --- | --- | --- | --- |
| #12 | `audit/issue-12-c1-r2.md`（PASS；attempt 2，事件 51；SHA-256 `f81c482d…`，本次核對與事件 51 相同） | `ca91406` | `619268a` | run record §8.1 #12：P1–P8 成立，P9 留 phase 層 |

- 結案後的 SIA correction `1ce4640` 修改了 `app/`、`tests/`；它是 SIA 的契約內 rework（orch-default §6），由 SIA R2 審查（run record §8.1 #12 下方的註記）。Ticket 的 R1-F1、R1-F2 沒有被重開。
- `e836c99`、`ca91406`、`619268a`、`ca07b7c`、`1ce4640`、`5301194` 都是 HEAD 的祖先（本 DA 以 `git merge-base --is-ancestor` 核對）。`619268a..1ce4640` 的實作 delta 只有上述三個檔；`ca07b7c..HEAD` 中 `app/ui0_texts.py`、`app/ui0_guard.py`、`.streamlit/config.toml`、`pyproject.toml` 沒有變更（`git diff --quiet` exit 0）。
- 已 route 的設計問題都有 record（P6）：C-1～C-3 → `decision-20261118-issue12-ui0.md`；K9-F／K3-B → `decision-20261118-issue12-ui07.md`；Q-1／Q-1b → `decision-20261118-issue12-q1.md`。

## 5. Spec 層級的 invariants 與整合行為

本 Spec 只有一張 Ticket，沒有跨 Ticket 的資料鏈；下列是 SPEC-UI0 本身（Issue #12＋CL-UI0-1～5＋OC-1 §2.2）要求在最終整合 subject 上同時成立的 invariants。

| # | Invariant | Evidence | 判定與限制 |
| --- | --- | --- | --- |
| I-1 | CL-UI0-1：程式在 `app/`，只依賴 Streamlit 1.67.0 與標準函式庫，不匯入 `src/moto_copilot/` | SIA R1 CL-UI0-1 列；SIA R2 AST import 檢查；本 DA 核對 `app/*.py` 的 import 只有 `__future__`、`datetime`、`re`、`streamlit` 與 `app/` 內的模組；`pyproject.toml` 的 `ui = ["streamlit==1.67.0"]` | 成立 |
| I-2 | CL-UI0-2（依 `decision-20261118-issue12-ui0.md` §3.2、§4.2 釐清）：app 不讀、不解析、不保存、不 log 上傳內容，只顯示檔案數與合成結果 | SIA R1 CL-UI0-2 列；本 DA 核對 `on_update_profile` 只取 `len(files)`；`app/` 中沒有 `open(`、`.read(`、`getvalue`、`getbuffer`、`print(`、`logging` | 成立，**限 app 的範圍**：元件自身列出的檔名與大小、框架超過 1 MiB 時的暫存行為不在此 invariant 內（DA record C-2、C-3），其動態生命週期 NOT VERIFIED（第 8 節） |
| I-3 | CL-UI0-5：沒有判定邏輯；規則結果、計畫狀態、候選標籤都寫在情境資料中 | SIA R1 CL-UI0-5 列；SIA R2 對 s16 的 literal 核對；本 DA 閱讀 `1ce4640` 的 diff：s16 的規則 5 是寫定的 `PASS`（表示留下來的模板通過），renderer 只依 `planner_note is not None` 決定是否顯示，沒有讀取或計算規則結果 | 成立。H-4 不涉及（derivation §5 的判定維持） |
| I-4 | OC-1 §2.2、CL-UI0-3：不修改 G3 Frozen Baseline、`docs/ui/`、`prototype/` | 本 DA 核對 `git diff --quiet 3906e07..HEAD -- docs/ui prototype src docs/requirement` 與 `git diff --quiet 873e37a..HEAD -- DESIGN.md docs/ui docs/cr/CR-01-appendix/ui0_decision_table.md` 都 exit 0 | 成立 |
| I-5 | UI0-3：固定文字與 Issue #12 逐字相同 | Executor E-4（雙向比對）；SIA R1、R2 的人工逐項對照；`app/ui0_texts.py` 自 SIA R1 subject 起未變更 | 成立。SPEC-001 5.5 標為「提案」的文字只是供 acceptor 檢視的模擬畫面文字，不因本接受而成為定案的產品文字（derivation §2） |
| I-6 | NFR5／UI0-9：每個情境標示為模擬，只用合成資料 | 本 DA 核對 24 個情境的 `label` 都含「模擬」；SIA R1 AB-10 列、SIA R2 AB-10 列；`git ls-files` 禁止路徑 0 | 成立（合成資料範圍） |
| I-7 | H-3 的受約束宣稱：保守估計不稱 P90 或百分位數；高降雨機率提醒不稱為官方警特報；隱私說明不宣稱檔案只留在使用者的電腦上；不與 Google Maps 比較；不描述折返判斷已驗證 | SIA R1 H-3 段；本 DA 以限定在 `app/` 的搜尋核對：唯一命中是 `ui0_texts.py:178` 的否定句（「不是氣象署的警特報」） | 成立 |

**整合行為。** SIA R1 範圍 3 與 SIA R2 範圍 3 涵蓋 Skeleton 內的整條互動：Profile 更新 → 舊結果過期而不自動規劃；表單 → 欄位錯誤／輸入保護／規劃；一輪追問 → 選用寫定的模擬計畫；路線確認 → 兩個分頁；UNKNOWN、七則路線錯誤、評估失敗、無可行解；以及 SIA-R1-F1 修正後的「固定模板保留、未通過的補充說明與其 caption 省略」，與 s04b／s16 反覆切換沒有殘留（SIA R2 的獨立 AppTest，含以舊 renderer 載入新 s16 的 negative control）。沒有後端整合；這是本 Spec 的設計範圍，不是缺口。

**瀏覽器證據對 s16 的涵蓋（本 DA 的判斷）。** s16 是 `1ce4640` 新增的情境，沒有在瀏覽器中操作（worklog §12.2「瀏覽器操作：NOT RUN」；SIA R2 NV-R2-SIA-2）。本 DA 判定這不影響 UI0-6、UI0-7 在最終 subject 上的成立：該修正沒有新增 widget、版面或鍵盤路徑，只在既有的 Trip Result 分頁省略一段文字與一行 caption（與 DELTA 第 285 行「只差一段文字，不是另一種版面」一致）；s16 經由既有的情境選單選取，鍵盤路徑與其他情境相同。依治理 §3.8「審後變更需要相應驗證」，s16 的相應驗證是 3 個 regression tests 與 SIA R2 的 AppTest，足以涵蓋這個 delta。s16 在瀏覽器中的實際呈現仍列為 acceptor 在 UI Delta Review 可檢視的事項（第 8 節 NV-B）。

## 6. 分配到的 AB 部分與累積 evidence（`derivation-spec-ui0.md` §6、§7）

本節陳述的是 **SPEC-UI0 分配部分**的 evidence 狀態；依 OC-1 §3.2，任何一項 AB 的 PASS 須所有分配到它的 derived Spec AC 都結案、證據都存在，SPEC-UI0 單獨不能使任何 AB 整體 PASS。

**Spec 層級 AC（derivation §6）：**

| Spec 層級 AC | 狀態與 evidence |
| --- | --- |
| #12 依 orch-default §7 結案 | 成立（第 4 節） |
| UI0-1～UI0-10 有證據 | 成立，各依其有效範圍：SIA R2「derivation §6、§7 的明確判定」表（UI0-8 FAIL→PASS、UI0-10 待補→PASS，其餘沿用 SIA R1）；UI0-6／UI0-7 以 Executor 的瀏覽器逐步紀錄（E-2、K1～K12）為據，UI0-7 的範圍依 `decision-20261118-issue12-ui07.md` §3.1、§4.2 |
| 本 Spec 分配到的 AB 部分有對應的證據 | 成立（下表） |
| 沒有修改 G3 Frozen Baseline 與 `docs/ui/` | 成立（第 5 節 I-4） |

**分配的 AB 部分（derivation §7）：**

| AB | SPEC-UI0 分配部分 | 累積 evidence | 分配部分的狀態 |
| --- | --- | --- | --- |
| AB-8 | UI-0 Skeleton 的實作與供 UI Delta Review 使用的紀錄 | `app/`、`tests/test_ui0_skeleton.py`；#12 Ticket audit closure；SIA closure；`worklog/issue-12.md` 第 6、7、9.2、10–12 節（供 acceptor 檢視的結果、替代、限制與 tracked items） | **分配部分自本 record 起完成。** **UI Delta Review 本身（acceptor 的實際檢視、決定與紀錄）是 AB-8 的另一項證據，不在本分配內，仍待 acceptor**（OC-1 §2.1 第 4 項、§4.2；first-run derivation §4、A-8）。之後的正式介面整合也不在本分配內（G-APP）。**AB-8 整體不是 PASS** |
| AB-10 | NFR5：每個情境標示為模擬；隱私說明採 U-7 裁決後的文字 | SIA R1、R2 的 AB-10 列；第 5 節 I-6、I-7 | 已具 evidence（合成資料）。其餘 NFR（NFR1–NFR4 在其他模組的部分）不在本分配內 |
| AB-13 | 本 Spec 的 pytest、Spec Integration Audit closure、Design Authority phase acceptance | pytest（下表）；SIA closure（第 3 節）；本 record | **分配部分自本 record 起完成。** 本 run 不採 fast path，SIA 是另外派工的 audit instance。Bindings 第 5 節的 release gate 與其他 Spec 的同類條件不在本分配內 |

**本 DA 在 HEAD `df50dfd`（主 checkout，`git status` 乾淨）親自執行的 gates：**

| 指令／檢查 | 結果 |
| --- | --- |
| `.venv/Scripts/python.exe -m pytest -q -rxX` | **614 passed in 15.56s**；沒有 xfailed／xpassed／skipped |
| `.venv/Scripts/python.exe -m pytest -q tests/test_ui0_skeleton.py` | 58 passed |
| `grep -rnE "xfail\|pytest\.mark\.skip\|importorskip" tests/` | 0 筆 |
| `git ls-files` 中 `.env`（含變體）、`*.gpx`、`*.fit`、`*.key`、`data/` 開頭的路徑計數（只比對路徑字串） | 0 |
| `git diff 3906e07..HEAD` 新增行中長 `sk-ant-` 值、private-key header、長 `api_key=` 值樣式的計數 | 0（不宣稱此樣式能辨識所有秘密形式） |
| `git diff --quiet` 對 `docs/ui`、`prototype`、`src`、`docs/requirement`（自 BASE）與 `DESIGN.md`、`docs/ui`、`ui0_decision_table.md`（自 `873e37a`） | 都 exit 0 |
| 限定在 `app/` 的 P90／百分位／分位數／Google Maps／警特報／只留在／這台電腦／本機／已驗證 搜尋 | 只有 `ui0_texts.py:178` 的否定句 |

614＝SPEC-B1 結束時的 556＋`tests/test_ui0_skeleton.py` 的 58。SIA R2 以 worktree 內 `.venv`（PATH 首位）執行同一 suite（614 passed）；本 DA 以主 checkout 的 `.venv` 重跑，結果一致。

## 7. 仍 open 的 follow-ups／tracked items

下列都**不是已完成的項目**，也不是 SPEC-UI0 Spec AC 的未完成部分。依治理 §1.2，follow-up 與 non-blocking finding 產生的後續事項在 acceptor 接受並授權前只是 tracked items，不得作為新工作執行；屬 OC-1 boundary 內、由 DA 之後 derive 進某份 derived contract 的，以該 derivation record 的 boundary determination 為據。

| ID | 內容 | 來源 | Owner／required authority |
| --- | --- | --- | --- |
| C-5、C-6、C-7 | Issue 沒有寫定的畫面文字與未選行程型態時的「期限」標籤（C-5，含 C-1 的「未決定（模擬；規格沒有定義這個組合）」）；模擬結果不隨表單重算（C-6）；`st.dataframe` 內建的「Download as CSV」（C-7） | `worklog/issue-12.md` §9.2、§11.5；`decision-20261118-issue12-ui0.md` §2.2 | **acceptor**（UI Delta Review）。tracked；不代表已接受為產品行為 |
| SPEC-001 5.5 提案文字 | Skeleton 中屬 SPEC-001 5.5「提案」的文字是否採用 | `derivation-spec-ui0.md` §2 | **acceptor**（UI Delta Review） |
| C-1 整合語義 | 同一輪追問中由回覆才成為途經點的休息，其方向題（選項 A）與下限不變式；SPEC-001 4.1、4.2、5.5 與第 9 節的修訂；H-4 標示 | `decision-20261118-issue12-ui0.md` §2.4 | 之後正式整合的 Spec（G-APP／Planner），Design Authority；方向題模板是提案文字，由 acceptor 確認 |
| C-2、C-3 整合條件 | 真實檔名不得出現在截圖、Demo、README、evidence 與紀錄；上傳資料的保存契約（記憶體期間、保存位置、刪除、框架暫存行為）；不得宣稱「不寫入磁碟」「只留在記憶體」；H-2 標示 | `decision-20261118-issue12-ui0.md` §3.3、§4.4 | 之後的整合 Spec（G-APP／G-ING），Design Authority；部署到騎士電腦以外的主機時 fail-closed 至 **acceptor**（RB-7） |
| Q-1 整合部分 | 一般模式重用 30 天內快照時的標籤、快照時間的呈現 | `decision-20261118-issue12-q1.md` §3.2、§5 | 之後的 `app/` 整合 Spec，Design Authority |
| Q-1b | 示範路線在 Streamlit 中是否、如何出現；「示範路線」來源標籤 | `decision-20261118-issue12-q1.md` §7.4 | 之後的 `app/` 整合 Spec，Design Authority；要讓騎士選用示範路線時牴觸 CR-B1，**acceptor**（contract change） |
| K9、逐元件鍵盤要求 | `st.date_input` 日曆彈窗在本環境中焦點進不去（原因未確定）；正式整合是否加入逐元件的鍵盤要求 | `decision-20261118-issue12-ui07.md` §3.3、§7；UI0-2 限制 7 | acceptor 可在 UI Delta Review 提出；屬 DELTA 11.2「驗收清單定稿時確認」的事項，由整合 Spec 的 Design Authority 處理；改變 P-11 的 accepted 語義時經 **acceptor** |
| Skeleton 不進產品路徑 | 本 Skeleton 的模擬資料、情境選單與「Skeleton 控制」不得帶進正式整合的產品路徑 | `derivation-spec-ui0.md` §8 | 之後的 `app/` 整合 Spec，Design Authority |
| WL-1（記錄一致性） | `worklog/issue-12.md` 最後更新於 `8b27799`（SIA R2 之前）：檔首「狀態」列與第 7 節 UI0-8 列仍寫「待 SIA R2／是否 closure 由 SIA R2 判定」，沒有記載 SIA R2 的結果。權威的 closure 紀錄是 SIA R2 record 與 run record 事件 58，所以不影響本接受 | 本 DA 核對（`git log 8b27799..HEAD -- docs/governance/records/worklog/issue-12.md` 無輸出） | Orchestrator 追蹤；是否派 #12 Executor 作 record-only 更新由 Orchestrator 決定。不是 phase acceptance 的條件，也不是新工作的授權 |
| C-4、C-8 | root `.streamlit/config.toml`；另加的情境 15 | `worklog/issue-12.md` §11.5 | 資訊；R1 判定在範圍內，無待辦 |

## 8. NOT VERIFIED 與需要 acceptor 的事項

| ID | 事項 | 狀態 | Required authority |
| --- | --- | --- | --- |
| **UDR** | **UI Delta Review**：acceptor 實際檢視 Skeleton 並作決定、留下紀錄（AB-8 的另一項證據；`DESIGN.md` §9.6：通過之前不開始正式的介面與後端整合） | **未進行（不在本 run）**；本 record 不代行 | **acceptor**（OC-1 §4.2） |
| NV-A | UI0-6、UI0-7 由 reviewer 親自重跑：SIA R1、R2 與 Ticket R2 的 reviewer 都沒有瀏覽器，評估的是 Executor 的逐步紀錄；原始 transcript／截圖不在 audit worktree（Executor 沒有截圖） | NOT VERIFIED（reviewer 親自重跑） | **acceptor**（CL-UI0-4 末句：UI Delta Review 實際檢視）；需要補原始 evidence 時 owner 是 #12 Executor |
| NV-B | s16 在瀏覽器中的呈現（第 5 節末段） | NOT RUN（瀏覽器）；AppTest 有 evidence | **acceptor**（UI Delta Review 可檢視） |
| NV-C | K3-B：作業系統原生檔案對話框中只用鍵盤多選 GPX | NOT VERIFIED；#12 範圍外，不是 PASS | **acceptor**（UI Delta Review 可檢視） |
| NV-D | 真實 GPX 的上傳、保存、隱私裁切與錨點代換；框架暫存檔的動態生命週期；正式 API 與後端行為 | NOT VERIFIED／NOT RUN（本 Spec 排除；本 run 沒有 RB-7 授權） | **acceptor**（RB-7）；保存與整合的語義由之後整合 Spec 的 Design Authority |
| A-UI07 | 若 acceptor 在 UI Delta Review 表示 P-11 的原意包含作業系統對話框或每個元件的每種互動 | 未決（`decision-20261118-issue12-ui07.md` §7 第 3 點判斷可能性低，不 fail-closed） | **acceptor** 說明 accepted 語義；屆時 #12 結案與**本 phase acceptance 的 UI0-7 部分**重新 route 至 Design Authority 評估影響（治理 §5.3） |
| A-ACC-1 | Issue #12 在 GitHub 上的狀態（仍 OPEN）與內容 | 本 record 不變更 | **acceptor**（OC-1 D-3、§4.2） |
| A-ACC-2 | Push、PR、合併；release gate 的最終判定 | 未執行 | **acceptor**（RB-1；Bindings 第 5 節） |

## 9. 不屬本 Spec、不得記為已涵蓋的範圍

- UI Delta Review 本身與其結果；AB-8 的整體 PASS。
- 正式的介面與後端整合（G-APP），包括 Profile 的實際處理（多檔合併、去重複、重建配速表、涵蓋度的實際判定；G-ING）、規則 1–5 的實際判定與計畫狀態（G-VAL）、Planner 的追問與補充說明的實際產生（G-PLN）、路線引擎與快照的實際行為（SPEC-R1、G-RTE）。UI0-8 清單中「整合後驗收」一欄的全部條目。
- Skeleton 中的情境資料與畫面文字作為產品行為或定案文字：它們只是供 acceptor 檢視的模擬。
- 真實資料、真實 API、付費呼叫；E1 Lite、E2 的任何結果（本 Spec 沒有任何實驗數字）。
- `README.md`、`DESIGN.md` 對 `app/` 實作狀態與執行方式的陳述（AB-12；`DESIGN.md` 第 3 行仍寫「尚未實作」，屬 AB-12 的文件工作）。
- OC-1 整體的 acceptance boundary 分配核對：SPEC-R1 仍未結，first-run derivation 第 6 節的 G-* 尚未分配；SPEC-UI0 不是 OC-1 最後一份未結 Spec，本 record 不作全部 derived Specs 的合計核對。

## 10. 是否改變 accepted 語義

**否。**
- 本 record 只依既有 evidence 判定 SPEC-UI0 的 phase acceptance，沒有修改 OC-1 的 intent、scope、constraints 或 acceptance semantics，沒有修改 SPEC-UI0 的 AC、invariant 或 gate。
- 第 5 節對 s16 瀏覽器證據涵蓋的判斷，是治理 §3.8 下對審後 delta 所需相應驗證的判定，不移除 UI0-6、UI0-7 或 CL-UI0-4 的任何要求；s16 的瀏覽器呈現仍列為 acceptor 可檢視的事項。
- 第 7 節的整合條件都是既有 DA records（`decision-20261118-issue12-ui0.md`、`-ui07.md`、`-q1.md`）與 `derivation-spec-ui0.md` §8 已寫定的分工的重申，屬治理 §5.3 第 2 類，不新增 Must。
- 沒有豁免任何 audit 或 gate；沒有 defer 任何 blocking finding；沒有改變高風險類別（#12 的 H-2、H-3 標示維持，H-1、H-4 不涉及）或 assurance 要求；沒有代行 acceptor 的 UI Delta Review。

**Boundary：在 OC-1 boundary 內**（`derivation-spec-ui0.md` 第 3 節；OC-1 §2.1 第 4 項）。本接受沒有新的 boundary 疑義；SIA R1、R2 範圍 5 都判定 traceability 與 boundary PASS，沒有 boundary finding。**不需要 acceptor 的接受或授權**（phase acceptance 是 Design Authority 的權責，治理 §2.1、§3.8）；acceptor 的 UI Delta Review 是另一件事，見第 8 節。

## 11. 狀態（分開陳述，治理 §3.8）

- **SPEC-UI0 phase acceptance**：**接受**（本 record）。orch-default §7 P10 的兩個條件（SIA closure、DA phase acceptance record 引用之）自本 record 起都存在。
- **SPEC-UI0 的 Spec completion**：Spec 層級的 completion predicates 由 Orchestrator 依 record 核對，本 record 不代為宣告 run 的狀態更新。
- **UI Gate／AB-8**：**未通過**。UI Delta Review 待 acceptor；通過之前不開始正式的介面與後端整合（`DESIGN.md` §9.6；first-run derivation G-APP）。
- **Run completion**（`run-20261117-oc1-run2`）：未完成；SPEC-R1 仍在 frontier。
- **OC-1 completion**：未完成；AB-1、AB-2、AB-5、AB-6、AB-8、AB-9、AB-12 等未分配或未結。
- **Release authorization**：沒有。合併進 `main` 由 acceptor 進行（RB-1）。
- **Issue #12**：不變更，保留給 acceptor。

## 12. 受影響的 work items 與 evidence

- run record §5 frontier 第 7 列（SPEC-UI0 SIA → DA phase acceptance）：本 record 是其 phase acceptance。
- **SPEC-R1（#13–#16）**：不受影響。`derivation-spec-r1.md` 沒有修改 `app/` 的 Ticket；SPEC-UI0 不匯入 `src/`。之後任何修改 `app/ui0_*.py` 或 `tests/test_ui0_skeleton.py` 的 Ticket，須在其 self-verification 中保持該測試全數通過；只有出現新的 integration-level evidence 顯示 SPEC-UI0 的 invariants 被破壞時，才由 Design Authority 判定是否需要重新驗證本 Spec。本 record 不因其他 Spec 的後續 delta 自動失效，也不為它們背書。
- **之後正式整合的 `app/` Spec（G-APP）**：derive 前須先有 acceptor 的 UI Delta Review 紀錄（AB-8、DESIGN §9.6）；derive 時須納入第 7 節的整合條件（C-1、C-2、C-3、Q-1、Q-1b、K9、Skeleton 不進產品路徑）與 acceptor 在 UI Delta Review 中的決定。
- **AB-12（G-DOC）**：`DESIGN.md`、`README.md` 對 `app/` 的實作狀態與啟動方式（`streamlit run app/ui0_mock_app.py`）的陳述。
- **SPEC-B1**：不受影響（`decision-20261118-spec-b1-phase-acceptance.md` 第 12 節已記 SPEC-UI0 不影響 SPEC-B1；本次 pytest 包含 SPEC-B1 的全部測試，仍通過）。
- **Completion report（交 acceptor）**：第 8 節的 UDR、NV-A～NV-D、A-UI07，以及第 7 節 owner 為 acceptor 的項目。

## 13. 執行紀錄

本 DA 讀了 Bindings m3、治理 §1.2、§2.1、§2.4、§2.5、§3.8、§4.7、§5.3、orch-default v2.2 §6–§7、OC-1 §2–§4、`derivation-spec-ui0.md`、first-run derivation 的 BD-2、BD-3 與第 4 節、高風險類別 record §4–§5、三份 #12 DA records 全文、SPEC-B1 的 phase acceptance record（格式）、SIA R1／R2 records 全文、run record 第 1、5、6（事件 38–58）、8.1 節、`worklog/issue-12.md` 第 1–9 節與第 11–12 節、`UI_CR01_DELTA.md` 第 11.3 節與 CR-C3 列、`DESIGN.md` §9.6 與相關行、`app/` 的 import 與上傳 callback、`1ce4640` 的 `app/` diff、`.streamlit/config.toml`、`pyproject.toml`。執行了第 6 節所列的 pytest、`git` 核對、Issue 原文的 SHA-256、audit records 的 SHA-256 與限定在 `app/`、`tests/` 的文字搜尋。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/` 下的任何腳本，沒有讀保留行程，沒有呼叫 GitHub；沒有修改程式、測試、worklog、Issue、`docs/ui/`、`prototype/` 或其他 record；沒有派工任何 subagent；沒有 commit。

Decision: SPEC-UI0 v1 phase acceptance — ACCEPT（引用 SIA closure `audit/spec-SPEC-UI0-c1-r2.md`，subject `5301194`）。UI Delta Review 仍待 acceptor；不改變 accepted 語義；不是 release authorization。
