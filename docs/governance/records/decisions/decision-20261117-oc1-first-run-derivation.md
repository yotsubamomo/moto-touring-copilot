# Decision record — OC-1 第一個 Formal run 的 derivation 規劃、boundary determination 與尚未 ready 的範圍

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261117-oc1-first-run-derivation`（v1） |
| 日期 | 2026-11-17 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | 無角色主 session（Bindings 第 3.5 節），只作派工介面。acceptor 2026-11-17 指示原文：「派 DA」，指 Bindings m2 第 8.2 節 #6 |
| Outcome Contract | OC-1（`docs/governance/records/outcome-contract.md`），acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受；條文以該 commit 為準 |
| 依據的條文 | 治理 §1.2、§1.5、§2.1、§2.4、§3.1、§3.3–§3.6、§4.1、§4.7、§5.1–§5.3；orch-default v2.2 §3、§6、§7、§12；Bindings m2 第 2.3–2.6、4、5、7、8.1、8.2 節；`decision-20261117-high-risk-categories.md` 第 3–5 節 |
| 本 record 的伴隨紀錄 | Spec 的 derivation records：[`derivation-spec-b1.md`](derivation-spec-b1.md)、[`derivation-spec-ui0.md`](derivation-spec-ui0.md)、[`derivation-spec-r1.md`](derivation-spec-r1.md)。本 record 承載跨 Spec 的決定；各 Spec 的依據、Tickets、AC 與 H 標示在各自的 derivation record |
| 讀過的證據 | OC-1；Bindings m2；高風險類別 decision record；治理本文 §1.2–§5.4；orch-default v2.2 全文；root `CLAUDE.md`；`DESIGN.md` §1–§9.6；`docs/spec/SPEC-001-plan-schema.md` 全文；`docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md` §0–§5；`docs/cr/CR-01-appendix/lead_dispositions_resolution.md` §6.4–§8.6；`docs/cr/CR-01-appendix/ui0_decision_table.md`（裁決與各列標題）；`docs/ticket/` 兩份索引；`docs/handoff/HANDOFF-2026-11-17.md`；`docs/grill/g1-grill-input.md` 的 Q18 列；GitHub Issues #7–#12（唯讀，`gh issue view`）；`src/moto_copilot/` 的 `contracts/schemas.py`、`contracts/validate.py`（函式清單）、`ingest/segments.py`、`ingest/__main__.py`、`pace/table.py`；`experiments/cr01_checks/` 的 `data_common.py`、`data_sb2_stop_allowance.py`、`routing_client.py`、`routing_c4_snapshots.py` 中與門檻、餘裕係數、道路名稱、User-Agent 有關的原始碼行（只讀原始碼，沒有執行）；`.gitignore`、`pyproject.toml`。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行任何 `experiments/` 腳本 |

## 1. 問題

1. 第一個 Formal run 可以引用哪些既有 Spec 段落與 Issues（#7–#12），它們是否 implementation-ready，不足之處是什麼。
2. 每份引用或 derive 的契約是否在 OC-1 boundary 內，分配到哪幾項 AB。
3. 每張 Ticket 的高風險類別、dependencies、AC 與充分證據要求。
4. OC-1 中目前沒有票的 Must 範圍，哪些現在可以 derive 成 implementation-ready 的 Tickets，哪些尚未 ready、各缺什麼。
5. 第一個 Formal run 的 Tickets 與執行順序（並行度 1）。

## 2. 裁決摘要

1. **Derive 三份 Spec**，都是 OC-1 內的 derived contracts，都 implementation-ready（含各自 derivation record 中的 DA clarifications）：
   - **SPEC-B1**（停等寬放與規則 3 的範圍判定）：Tickets #7、#9、#10、#11、#8，原樣引用。見 [`derivation-spec-b1.md`](derivation-spec-b1.md)。
   - **SPEC-UI0**（UI-0 Mock-data Skeleton）：Ticket #12，原樣引用；單 Ticket fast path。見 [`derivation-spec-ui0.md`](derivation-spec-ui0.md)。
   - **SPEC-R1**（路線來源：契約 v0.3 的其餘部分與 `routing`）：新 Tickets R1-1～R1-4，定義在 [`derivation-spec-r1.md`](derivation-spec-r1.md)；Issues 依 OC-1 D-3 另行建立。
2. Boundary：三份 Spec 都在 OC-1 §2.1 第 1–4 項之內（第 3 節 BD-1～BD-5）。沒有需要 acceptor 重新授權的項目。
3. **沒有關閉任何 Spec Blocker，沒有修訂 `docs/spec/` 的任何檔案，沒有宣告 SPEC-001 的 Freeze。** 需要的文字同步列在第 7 節，作為建議。
4. 第一個 Formal run 的組成與順序見第 5 節；尚未 ready 的範圍與缺口見第 6 節。

## 3. Boundary determinations

### BD-1 OC-1 取代「凍結之前只建立 BATCH-1」的 Ticket 閘門

**問題。** acceptor 2026-11-15 的 Q-5 裁決（`lead_dispositions_resolution.md` §7.4）把各文件的「凍結之前不建立 Tickets」改為「除了這一批之外，凍結之前不建立其他 Tickets」，SPEC-001 §11.1、§12 也這樣寫（之後 acceptor 另以 CR-01 的 UI Gate 裁決建立了 #12）。OC-1 §4.1 則授權 Design Authority derive「`routing`、`routes`、`sources`、`planner`、`validator`、`kb`、`app/`、E1 Lite、E2 等目前沒有票的工作」的 Spec 與 Tickets；§5 把閘門寫成「SB-3、4、5、6、10 涵蓋的部分，在 Blocker 關閉前不得納入 Formal run 的 Tickets」；§8 列出仍然有效的既有指示，其中有「不宣告完整的 SPEC-001 Freeze」，沒有「凍結之前不建立其他 Tickets」。

**判定：在 boundary 內。OC-1 的閘門（逐項 Spec Blocker 是否關閉）取代 Q-5 的閘門（SPEC-001 是否整份凍結），用於 derive 新的 Tickets。**

依據：
- OC-1 是 acceptor 在 Q-5 之後（2026-11-17）以治理的接受程序接受的 Outcome Contract；Bindings 第 8.1 節規定治理之前的產出是輸入，不是治理下的 accepted contract。
- 若 Q-5 的閘門仍然有效，加上 OC-1 §8 保留的「不宣告完整的 SPEC-001 Freeze」，OC-1 §4.1 明文列舉的那些 Tickets 在本契約內永遠不能 derive；這個讀法使 §4.1 的列舉失去作用，不是合理的解讀。
- 兩個閘門的目的相同：不讓 Tickets 決定尚未定案的語義。OC-1 §5 與 Bindings 第 8.1 節以逐項 Blocker 保留這個目的；本 record 另以 BD-2 界定 SB-10 的剩餘範圍，避免把未審查的內容帶進 Tickets。
- 不改變 accepted 語義：OC-1 的 scope、constraints、acceptance 都沒有被擴張；新 Tickets 都在 §2.1 的範圍內。

SPEC-001 §11.1、§12 中「除了這一批之外，凍結之前不建立其他 Tickets」的文字，在本 record 生效後不再約束 OC-1 內的 derivation；文字同步見第 7 節 RV-1。acceptor 若要恢復 Q-5 的閘門，那是 OC-1 的變更（治理 §5.3），不是本 record 能決定的。

### BD-2 SB-10 的剩餘範圍

SB-10 的說明是「SPEC-001 第 10 節、第 11.2 節，以及 5.5 中不在對照表內的文字仍待審查」。第 10 節的狀態欄有許多「待審查」是在後來的裁決之前寫的，其中不少項目的實質內容已由之後的 acceptor 裁決定案，並且屬於已 CLOSED 的 Blockers。

**判定：** SB-10 在本 record 中的剩餘範圍是：
1. SPEC-001 第 10 節中，狀態仍為「待審查」、而且實質內容沒有被之後的 acceptor 裁決定案的決定。這裡的裁決指 P-1～P-11 與修正 1–5（SPEC-001 §11.1）、SPEC-RESOLUTION-001 第 8 節、O-1～O-5、Q-1～Q-5、Q-3 七項與後續九項（處置 §5、§7–§9）、UI-0 對照表 U-1～U-22。
2. 第 11.2 節中沒有標為「已解決／已裁決／已定案」的 OQ（OQ-2～OQ-8、OQ-13～OQ-15）。
3. 5.5 中標為「提案」而且不在 UI-0 對照表內的文字。

實質內容已由上述裁決定案、而且屬於已 CLOSED 的 SB-1、SB-2、SB-7、SB-8、SB-9 範圍者，不因第 10 節的「待審查」字樣而算在 SB-10 之內。各 Spec 碰到的第 10 節項目，逐項對照寫在各自的 derivation record（SPEC-R1 第 3 節）。

這不是關閉 SB-10；SB-10 的剩餘範圍仍然擋住依賴它的 Tickets（第 6 節）。依據：界定一份 derived Spec 中哪些內容已定案，是治理 §2.4 的 contract-sufficiency 判斷，屬 Design Authority；Bindings 第 2.6 節沒有把 Spec review 保留給 acceptor。

### BD-3 既有 Issues #7–#12 的引用方式

- 原樣引用，不修改（OC-1 D-3、§4.2）。Issues 是可變的來源，依治理 §1.2 記錄本次引用的版本：以 `gh issue view <n> --json body,updatedAt` 取得的 `body` 字串，UTF-8 編碼後的 SHA-256。

| Issue | `updatedAt` | `body` 的 SHA-256 |
| --- | --- | --- |
| #7 | 2026-11-15T11:10:55Z | `a59c9f93f6d9b6b7259948f189c2185804309b1457be968a001223606c339af7` |
| #8 | 2026-11-15T11:10:56Z | `061ad87fb3dff17ccbcbb75a433fd2f01c7ac8ff5c226aa65bd6af157d7418e4` |
| #9 | 2026-11-15T11:10:58Z | `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895` |
| #10 | 2026-11-15T11:10:59Z | `880ef1341e090b86e826cd2a14812ab4a05b634b73385c3ccebea80e43245e65` |
| #11 | 2026-11-15T11:11:01Z | `3f4b1caecfcc81bb152ea217ec376857c0e6f6dab9c207148412d96da026f8e4` |
| #12 | 2026-11-15T15:52:44Z | `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be` |

  Executor 在 grounding 時若發現雜湊不同，表示 Issue 在本 record 之後被改過：route 至 Design Authority，不自行採用新內容。
- Issue 內文中兩句共通規則，在治理下的意義（不是修改 Issue）：
  - 「在 PR 中列出修改的理由」：改為在該 Ticket 的 worklog（`docs/governance/records/worklog/issue-<n>.md`）列出。Agents 不開 PR（RB-1）。
  - 「遇到規格沒有寫的事，停下來回報，不自行補上」：依治理 §2.4、§3.3 route（語義與 boundary 交 Design Authority，接受與授權交 acceptor）。在 Orchestrator run 中這是 routing，不是 run 的停止。
- Issues 內文的「SPEC-001 還沒有凍結」「規格文件尚未 push」維持原意，不影響 implementation readiness：readiness 以本 record 與各 derivation record 為準。

### BD-4 Lane

三份 Spec 都是 Formal（OC-1 §6；Bindings 第 4 節：MVP 的模組實作屬 Formal；治理 §3.6-C：多個 execution units 與 dependencies）。SPEC-UI0 只有一張 Ticket，仍是 Formal（治理 §3.4：不設 Formal-lite），採單 Ticket fast path（Bindings 第 5 節）。

### BD-5 Spec 的識別與版本

- 三份 Spec 都以「引用」構成（治理 §3.4「reference to applicable effective Spec」）：Spec 的內容＝各 derivation record 列出的既有段落（以 commit `873e37a` 的內容為準；這些檔案自 `5a66287` 起沒有改過，與 `01f3ea4` 相同）＋該 derivation record 的 DA clarifications 與 Ticket 定義。
- 版本以 derivation record 的版本標示（本次都是 v1）。之後的修訂依治理 §5.3 第 2 類由 Design Authority 以新版本記錄，並寫明對進行中工作與既有 evidence 的影響。
- 既有段落中與本次 Spec 有關、但標為「草案」「提案」「待確認」而且不在 BD-2 定案範圍內的內容，不屬於這三份 Spec，除非 derivation record 明確寫入。

## 4. AB 的分配（OC-1 §3.1）

「部分」的確切內容寫在各 derivation record。全部 derived Specs 合起來尚未涵蓋整個 acceptance boundary；剩餘部分由之後的 derivation 分配（第 6 節）。

| AB | SPEC-B1 | SPEC-UI0 | SPEC-R1 | 尚未分配的部分與原因 |
| --- | --- | --- | --- | --- |
| AB-1 端到端流程 | — | — | 部分（路線快照上的實際道路路線的產生能力，不含端到端的執行證據） | 端到端整合與實際執行的證據：依賴 `routes`、`sources`、`validator`、`planner`、`app/`；Planner 的實際執行 BLOCKED（OC-1 §9.1 C-1） |
| AB-2 FR1 | — | — | 部分（路線引擎的路線、來回與單向、目標 GPX、明確的路線錯誤） | 行程描述的解析、追問、期限語意、詞彙表解析：依賴 `planner`（C3）、`kb`、SB-6、SB-10 |
| AB-3 FR2 | 部分（停等分類與配速表的重建核心、`user-` 版本） | — | — | 多檔上傳、合併去重複、行程清單、涵蓋度摘要：第 6 節 G-ING |
| AB-4 FR3 | 主要部分（典型與保守估計、停等寬放、餘裕係數） | — | — | 介面與文件的用語檢查隨 `app/` 與 AB-12 |
| AB-5 FR4 | — | — | — | BLOCKED：SB-3、SB-4、SB-5、氣象署授權碼（RB-3） |
| AB-6 FR5 | — | — | — | 加油站投影規則與資料格式、路況情境檔：第 6 節 G-RTE、G-SRC |
| AB-7 FR6 | 部分（規則 3 的範圍判定） | — | — | 規則 1、2、4、5、計畫狀態、排序、重新規劃、匯入限制：SB-10、SB-3／4 |
| AB-8 FR7 | — | 部分（UI-0 Skeleton，供 UI Delta Review） | — | UI Delta Review（acceptor）與正式整合 |
| AB-9 知識庫 | — | — | — | 沒有 Spec；實際執行 BLOCKED（C-1） |
| AB-10 NFR | 部分（ETA 的 UNKNOWN 傳遞、保留行程拒絕、只用合成資料） | 部分（模擬標示、隱私說明的文字） | 部分（對第三方只送公開地標、路線錯誤的 fail-closed） | 其餘模組的 NFR |
| AB-11 實驗的程式與凍結 | 部分（`research-` 版本不覆寫、保留行程拒絕） | — | 部分（路線快照嚴格模式的機制） | E1 Lite、E2 的 Spec、凍結清單格式、Oracle、題庫 |
| AB-12 文件 | — | — | — | 文件的 Spec 在功能接近完成時 derive |
| AB-13 整合條件 | 部分（本 Spec 的 pytest、SIA、phase acceptance） | 部分（同左） | 部分（同左） | 其餘 Spec 的同類條件；最後的 release gate |

## 5. 第一個 Formal run

### 5.1 組成與順序（並行度 1）

| 順序 | 項目 | Spec | 前提 |
| --- | --- | --- | --- |
| 1 | #7 B1-1 `contracts`（契約 1、3、4 的 v0.3 欄位） | SPEC-B1 | — |
| 2 | #9 B1-2 `ingest`（停等事件） | SPEC-B1 | #7 |
| 3 | #10 B1-3 `pace`（配速表） | SPEC-B1 | #7、#9 |
| 4 | #11 B1-4 `pace`（ETA） | SPEC-B1 | #7、#10 |
| 5 | #8 B1-5 規則 3 的範圍判定 | SPEC-B1 | — |
| 6 | SPEC-B1 的 Spec Integration Audit → Design Authority phase acceptance | SPEC-B1 | 1–5 結案 |
| 7 | #12 UI-0 Skeleton（R1 兼作 Spec Integration Audit，須在派工時就指定） | SPEC-UI0 | — |
| 8 | R1-1 `contracts`（ID 樣式與契約 2 的 v0.3） | SPEC-R1 | #7；Issue 已建立 |
| 9 | R1-2 `routing`（路線快照的模型、雜湊、存放與選取） | SPEC-R1 | R1-1；Issue 已建立 |
| 10 | R1-3 `routing`（目標路線 GPX） | SPEC-R1 | R1-1、#9；Issue 已建立 |
| 11 | R1-4 `routing`（路線引擎的請求與採用、共用介面） | SPEC-R1 | R1-2、R1-3；Issue 已建立 |
| 12 | SPEC-R1 的 Spec Integration Audit → Design Authority phase acceptance | SPEC-R1 | 8–11 結案 |

- #8 與 #12 沒有依賴，排序只為了讓 SPEC-B1 先整合、UI-0 在 acceptor 預定的 UI Delta Review（暫定 11/28）之前完成。Orchestrator 依 dependencies 計算 frontier；上表的先後在依賴之外只是建議，不是 gate。
- SPEC-R1 的 Tickets 在 GitHub Issue 建立之前不能啟動（Bindings 第 7 節：Ticket 本體在 GitHub Issues）。建立方式依 OC-1 §4.1、D-3：建立前檢查重複；Issue 內文引用 `derivation-spec-r1.md` 的 Ticket 定義、SPEC-R1、所分配的 AB 與 AC。Issue 未建立不影響 SPEC-B1、SPEC-UI0。
- 啟動 run 仍需 acceptor 指定 Orchestrator（Bindings 第 3.5 節），以及 orch-default §3 的其他前提。

### 5.2 Audit

- 每張 Ticket 一次 independent audit（Bindings 第 5 節）。每份 Spec 一次 Spec Integration Audit；SPEC-UI0 走單 Ticket fast path，SPEC-B1 與 SPEC-R1 各自另派。
- 高風險類別依各 derivation record 的逐票標示處理（高風險類別 decision record 第 4 節第 3 項、第 5 節）。Orchestrator 依標示機械處理，不自行降級。
- 本 record 沒有新增 audit round 或 audit instance。

## 6. 尚未 ready 的範圍與缺口

「誰可以解決」只指出需要的 authority，不代表已授權或已排程。

| 代號 | 範圍 | 狀態 | 缺什麼 | 誰可以解決 |
| --- | --- | --- | --- | --- |
| G-CON | `contracts`：Plan Schema 的 JSON Schema（SPEC-001 §3–§4） | 未 ready | SB-10 剩餘範圍（SD-1～SD-13、SD-17、SD-19～SD-24 中未定案的部分；OQ-2 油耗單位、OQ-3 加油時間、OQ-8 Schema 的位置）；WeatherSegment 的預報時段欄位與 `R3_AREA_UNMAPPED`（SB-3、SB-4） | SB-10 部分：Design Authority（逐項審查，以 decision record 定案）；SB-3／SB-4 部分：要等 C3 |
| G-ING | `ingest` 的 Profile 管理：多檔上傳、合併、以內容去重複、行程清單接續編號、涵蓋度摘要（FR2、DESIGN §5 資料處理流程第 5–6 項） | 未 ready | (1) 「以內容去重複」的鍵沒有定義（檔案位元組的雜湊，或正規化軌跡的雜湊）；(2) 「內容和保留行程或被排除的行程相同的檔案略過」需要那些行程的內容雜湊，而凍結前不得開啟那些檔案，雜湊從哪裡來沒有定義（行程清單是否已記錄雜湊：NOT VERIFIED，需要讀私有資料）；(3) 上傳檔案的保存位置與保存期間（H-2 判定第 5 項）沒有定義 | (1)(3)：Design Authority；(2)：若需要開啟或雜湊保留行程的檔案，required authority = acceptor（RB-7） |
| G-RREQ | 路線請求的解析：PlaceRef → 送給引擎的位置；起點錨點；目的地是公路時的進入端與另一端；回程是否經過進入端 | 未 ready | 公路與地標詞彙表的 Spec（欄位、座標定義、入口與另一端）；目的地是公路時回程請求的組成（7.11 第 2 項只寫「目的地、倒序的途經點、起點」，沒有說進入端）；Rider Profile 的出發錨點欄位 | Design Authority（詞彙表與 Rider Profile 的 Spec）；詞彙表選哪些公路與地標見 G-KB |
| G-RTE | `routes` 的 CR-01 部分：由幾何建立路線目錄、折返點切段、檢查點（起點、終點、折返點、途經點、加油站）與編號、`ridden_share_pct`、RI-1～RI-3 | 未 ready（可在 SPEC-R1 結案後 derive） | 加油站投影的規則沒有定義（距路線多遠算沿線、投影到哪一個路段邊界、加油站快照的欄位）；依賴 SPEC-R1 的介面與 #10 的 `category_scheme` 格式（`derivation-spec-b1.md` CL-B1-4）；鄉鎮對應屬 SB-3 | Design Authority（投影規則、routes 的 Spec）；鄉鎮對應要等 C3 |
| G-SRC | `sources`：預報、暮光終、加油站與油量、路況事件 | 未 ready | 預報：SB-3、SB-4、SB-5；氣象署授權碼（RB-3）。暮光終：同一授權碼；「路線所在地」取哪個地點沒有定義。加油站：政府資料開放平臺資料集的欄位與營業時間格式 NOT VERIFIED；Rider Profile 的油耗單位與加油時間（OQ-2、OQ-3）。路況事件：情境檔的格式沒有定義 | 授權碼：acceptor（RB-3）；SB-3／4／5：C3；其餘：Design Authority |
| G-VAL | `validator` 的其餘部分：規則 1、2、4、5，計畫狀態、排序、候選評估、匯入限制 | 未 ready | RuleResult、原因代碼與指引（SD-2、SD-3、SD-4、SD-10、SD-11、SD-19 屬 SB-10 剩餘範圍）；規則 5 的顯示格式（OQ-6）與道路寫法的固定樣式（5.4 寫「清單由 Tickets 補齊」，屬治理 §3.4 所說的把必要選擇留給下游）；規則 3 的原因代碼與優先順序（SB-3、SB-4） | SB-10 與 5.4 的清單：Design Authority；規則 3 的原因代碼：要等 C3 |
| G-PLN | `planner` 與「主程式」的確定性部分（休息需求的對應、預設休息、候選迴圈、重新規劃的合法性） | 未 ready | SB-5／C3 BLOCKED（Anthropic 憑證，RB-3；C3 的 US$3 已授權）；模型選定（PD-5，在 C3 之後）；開發與 Demo 的 LLM 支出未授權（OC-1 §9.1 C-1、D-5、RB-4）；SB-6（7.12 第 1、3–7 項待審查；第 2 項的驗收案例已裁決）；「主程式」沒有模組對應（DESIGN §9.1 只有 `planner` 與 `validator`）；依賴 G-RTE、G-SRC、G-VAL | 憑證與支出：acceptor；SB-6 與模組對應：Design Authority；C3 的執行：在 RB-3、RB-4 的範圍內 |
| G-KB | `kb`：最小知識庫（關鍵字檢索、附出處）與公路與地標詞彙表 | 未 ready | 沒有 Spec；詞彙表的公路與地標要選哪些（DESIGN §5「以騎過的路為主」，需要騎士本人的選擇，或確認改用 SPEC-RESOLUTION-001 §3.2 的五條公開參考路線）；知識庫深度待老師確認（OC-1 §5，不擋開始）；AB-9 的實際執行 BLOCKED（C-1） | Spec：Design Authority；公路的選擇：acceptor；支出：acceptor |
| G-APP | `app/` 的正式整合 | 未 ready | UI Delta Review 通過（acceptor，AB-8）；依賴後端各模組 | acceptor（Review）；之後 Design Authority derive |
| G-E1 | E1 Lite 的程式、分析計畫與凍結 | 未 ready | 沒有 Spec：分析計畫中「熟悉與不熟悉的分界、`suspect` 路段的處理、路線引擎時間的路段選取規則」尚未寫定（DESIGN §6.2）；凍結清單的格式；隔離的評估腳本的設計。以真實行程執行需要 RB-7 的授權；正式執行保留給 acceptor（OC-1 §4.2） | Spec：Design Authority；資料與執行：acceptor |
| G-E2 | E2 的題庫格式、Oracle、Runner、三組設定 | 未 ready | 沒有 Spec（Oracle 規格初版預定在 M2）；時間相依的 Oracle 是否實作尚未決定；依賴 `planner`（C3）與 `sources`（SB-3、SB-4）；Pilot 與正式執行的支出未授權（D-5） | Spec 與時間相依 Oracle 的取捨：Design Authority；支出與正式執行：acceptor |
| G-REG | 停等寬放的回歸檢查（SPEC-RESOLUTION-001 §1.6：以真實配速行程做留一趟） | 未 ready | 需要讀取配速行程（RB-7） | acceptor（RB-7 的明確授權） |
| G-DOC | `README.md`、`DESIGN.md` 依實際狀態更新（AB-12） | 尚未 derive | 依實作進度；Installation、How to Run 要實際跑過 | Design Authority 在功能接近完成時 derive |

補充：
- SB-6 與 SB-10 的剩餘範圍不需要 acceptor 也能關閉（Bindings 第 2.6 節不保留 Spec review）；關閉的條件是規格與驗收條件實際完成，並由 Design Authority 以 decision record 寫明依據。本 record 沒有作這件事。
- SB-3、SB-4、SB-5 依賴 C3 的真實 API 驗證；C3 維持 BLOCKED／NOT RUN，直到真的以真實 API 執行過。

## 7. Spec 的修訂

本 record 與三份 derivation record **沒有修改 `docs/spec/`、`DESIGN.md` 或任何 Issue**。建議的文字同步（不是本次裁決生效的條件；由之後的 Spec 修訂或 AB-12 的文件工作處理，修改 `DESIGN.md` 要在相應的 work item 內進行）：

| 代號 | 位置 | 建議 |
| --- | --- | --- |
| RV-1 | SPEC-001 §11.1、§12；`docs/ticket/BATCH-1-scoped-tickets.md` 檔首 | 註明「除了這一批之外，凍結之前不建立其他 Tickets」已由 OC-1 §4.1、§5 取代（本 record BD-1） |
| RV-2 | SPEC-001 4.12、4.14 的 `road_names` | 寫入 `derivation-spec-r1.md` CL-R1-6 的定義 |
| RV-3 | DESIGN §5 契約 2「`target_gpx` 的雜湊由修改契約 2 的 Ticket 提出」 | 寫入 `derivation-spec-r1.md` DD-R1-1 的決定（不新增欄位） |
| RV-4 | DESIGN §5 契約 3、§6.1 | 寫入 `derivation-spec-b1.md` CL-B1-4 的 `category_scheme` 格式 |
| RV-5 | SPEC-001 第 9 節 S39、S40 | 標明「五條參考路線」「詞彙表每個地標的偏移」屬整合或詞彙表的驗收，不屬於 R1-4 |

## 8. 是否改變 accepted 語義

**否。**
- 三份 Spec 都在 OC-1 §2.1 第 1–4 項之內，沒有新增 Must、沒有恢復 Scope Reduction、沒有引入 Should。
- BD-1 是對 OC-1 條文的解讀，結果與 OC-1 §4.1 的明文一致；它不擴張 scope，也不放寬任何 constraint。
- DA clarifications 都是 derived contract 的設計細節（治理 §5.3 第 2 類），不改變 OC-1 的 intent、scope、constraints 或 acceptance semantics。
- 沒有豁免任何 audit；沒有改變高風險類別的判定或 assurance 要求。

## 9. 需要其他 authority 的事項

沒有任何一項擋住第 5 節的 run。下列是之後的路徑需要的：

| # | 事項 | Authority | 理由 |
| --- | --- | --- | --- |
| A-1 | BD-1 的判定（OC-1 取代 Q-5 的 Ticket 閘門） | acceptor（只供知悉；不需要回覆即生效） | acceptor 若要恢復 Q-5 的閘門，屬 OC-1 的變更（治理 §5.3） |
| A-2 | 指定主 session 為 Orchestrator，啟動 run | acceptor | Bindings 第 3.5 節 |
| A-3 | 建立 R1-1～R1-4 的 GitHub Issues | OC-1 §4.1、D-3 已授權 Agents（不需要 acceptor） | Bindings 第 7 節 |
| A-4 | 停等寬放的回歸檢查（G-REG）；Profile 管理的去重複若需要保留行程的內容雜湊（G-ING (2)） | acceptor | RB-7 |
| A-5 | Anthropic 憑證、氣象署授權碼 | acceptor | RB-3 |
| A-6 | 開發、Demo、Pilot、正式 E2 的 LLM 支出（OC-1 §9.1 C-1） | acceptor | RB-4、D-5 |
| A-7 | 詞彙表選哪些公路與地標（G-KB） | acceptor | DESIGN §5 要求以騎過的路為主，需要騎士本人的選擇；Agents 不讀私有資料推測 |
| A-8 | UI-0 完成後的 UI Delta Review | acceptor | OC-1 §4.2、AB-8 |

## 10. 受影響的 work items 與 evidence

- **GitHub Issues #7–#12**：在 SPEC-B1、SPEC-UI0 中原樣引用；Issues 的內容與狀態不由 Agents 修改（OC-1 D-3）。結案紀錄寫在 worklog 與 audit record（OC-1 §4.2）。
- **新 Tickets R1-1～R1-4**：定義在 `derivation-spec-r1.md`，Issues 尚未建立。
- **Spike 程式**（`contracts`、`ingest`、`pace`）：由 SPEC-B1 依 Spec 收編或返工（OC-1 §2.1 第 3 項）。`routes` 的 Spike 這次不動。
- **既有 100 個測試**：會因契約 v0.3 而修改；修改理由記在各 Ticket 的 worklog（BD-3）。
- **`DESIGN.md` 的實作狀態陳述**（例如 §6.1、§9.1 的「尚未實作」）：SPEC-B1 結案後會過時，屬少報而不是多報；由 AB-12 的文件工作更新，不在本次的 Tickets 內。
- **Bindings 第 8.2 節 #6**：本 record 與三份 derivation record 完成 Design Authority 的 derivation；狀態欄的轉錄依 Bindings 慣例由無角色 session 依 acceptor 指示進行。

本 record 沒有讀取 `data/` 或 `.env`，沒有執行任何測試或腳本，沒有寫入 GitHub，沒有派工任何 subagent，沒有 commit。
