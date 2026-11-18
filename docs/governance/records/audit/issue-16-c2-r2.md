# Audit record — Issue #16（SPEC-R1 R1-4 `routing`）cycle 2 R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，接受版本 `873e37a`）→ SPEC-R1 v1（`decisions/derivation-spec-r1.md` §2 引用來源、§4 DD-R1-2 與 CL-R1-1、5～9、§5 R1-4 與 E-1～E-6）＋ CL-R1-13（`decision-20261118-issue13-c131.md`）、CL-R1-14、17、19（`decision-20261118-issue14-c141.md`）、CL-R1-20、21（`decision-20261118-issue14-qalt1.md`）、CL-R1-24（`decision-20261118-issue15-c151.md`）、CL-R1-25～27（`decision-20261118-issue16-c161.md`）、CL-R1-28（`decision-20261118-issue16-c2r1f3.md`）、CL-R1-29（`decision-20261118-issue16-c165.md`）→ Issue #16（原文由 dispatch pack 提供；沒有呼叫 GitHub） |
| Subject | 本 worktree `C:/Users/yotsu/AppData/Local/Temp/cx16c2r2`；BASE **`bc7024b24b968e2dfb04dc38e822781dd5fb5425`**；HEAD **`18a5c5c8fedd03c9f5428525090c9f1aee9a2edf`**。Cycle 2 R1 subject `fb6210dbceab4b04651380d8bc23ee82d4896484`；本次 closure delta 為 `fb6210d..18a5c5c` |
| Audit kind | **Ticket R2 closure review，cycle 2；不是 Spec Integration Audit**。依治理 §4.4、Bindings §3.3、FA ruling `ruling-20261118-issue16-c1.md` Addendum A，以及 CL-R1-28 §3.2～3.4 的限定範圍 |
| Role | `primary_reviewer`（Codex） |
| 日期 | 2026-11-18（Asia/Taipei） |

## 1. Assurance

### (a) Context independence

| Property | 本次的滿足方式與證據位置 |
| --- | --- |
| Independent context | Fresh Codex thread，只收到本次 dispatch pack；沒有 Executor、cycle 2 R1 Reviewer 或其他角色的對話。重讀磁碟上的 cycle 2 R1 record、修正後來源與 diff，自行執行檢查；正式 records 與 worklog 的結論均視為待驗證主張 |
| Verifiable binding | 依 Bindings §3.3，由派工者核對本次 rollout 的全部 `turn_context`、存取路徑與 record hash，記入 run record `run/run-20261117-oc1-run2.md` §6 的**本次 cycle 2 R2 dispatch binding 欄位**。本 subject 的 run record 目前只到事件 **105**（Executor 完成 correction）；**本次 R2 的事件編號與 binding 尚未記入該版本**，不能冒稱已有事件 106 或已核對。採用本 record 前須由派工者補記並確認；見 NV-BIND。這是指定的核對機制，本 reviewer 不讀 worktree 外的 rollout 來代替派工者 |
| Autonomous access | 自行讀取 worktree 中的原始碼、測試、契約、audit／decision／worklog／run records 與 git 歷史，自行選擇 supplementary probes。全程不連網、不讀私有資料或憑證、不執行 `experiments/`。記憶體探測封鎖 socket；測試使用既有 FakeEngine／HTTPSConnection 替身與 autouse socket 封鎖 |
| Self-written record | 本檔由本 reviewer 自行寫入，是唯一新增的非 ignored 檔案。沒有修改 implementation、tests、contract、其他 record 或 gate，沒有 stage／commit。正式測試、補充探測與突變結束後、寫本檔前，`git status --short` 為空 |

### (b) Actual models 與 model diversity

| 角色 | 可取得的證據 |
| --- | --- |
| Executor | `claude-opus-5-5`／`high`；run record §6 事件 103、105，agentId `a1e2cfa52290d496f`；事件 105 記全部 assistant 訊息 324 則、只有此一 model／effort 組合。這是派工者的核對紀錄，本 reviewer 未讀其 transcript |
| Cycle 2 R1 Primary | Claude path `claude-opus-5-5`／`high`；事件 98～100 記 Codex usage limit、R-PR substitution 與該輪 `diversity_lost`。本 R2 沒有繼承其 context |
| 本 R2 Primary | **Codex**；精確 model ID、effort、sandbox 的 binding 由派工者依前表補記。Bindings 的 preferred mapping 是 `gpt-6.1-sol`／`high`，mapping 不是本次實際執行的獨立證據 |

**no model diversity claim**：本 record 不以 Codex 名稱或預設 mapping 代替尚待派工者核對的實際 binding。Independence 的程序與 model diversity 分開陳述；採用前的 binding 核對義務不由本 verdict 豁免。

## 2. 範圍與 subject 核對

本 R2 只核對 C2R1-F1、F2 的 required fix、隨 F1 處理的 F4、DA 授權的 F3／CL-R1-28，以及 correction 的 regression／直接暴露的 blocking defects。沒有重作無限制的完整 R1，也沒有宣告 SPEC-R1 或 OC-1 的整體 acceptance。

- 自行重讀 `audit/issue-16-c2-r1.md` 的四項 findings 與 required fixes；cycle 1 R1／R2／Alternate 的 R1-F1、R2-F1 段落；FA ruling 與 Addendum A；CL-R1-28、29；worklog §13～§14。以治理 §2.3、§3.8、§4.1～§4.7、impl-default v2 §6～§7、Bindings m3 §3.3 與高風險 decision §5 為 review 規則。
- 契約核對聚焦 derivation §2、§4、§5 R1-4／E-1～E-6、上述 clarifications，以及 SPEC-001 §2、4.14、7.11 和 R1-4 分配的合成 AC；沒有把排除的 S39／S40 真實參考路線納入已驗證範圍。
- `git rev-parse`、`git log --oneline bc7024b..18a5c5c`、BASE diff 的檔案分配／既有 exports 與測試 gate、完整 correction 的 `src/`／`tests/` diff 相符。全部 implementation commits 為 `7cb4b0c`、`f6810d2`、`65aa00c`、`022f629`、`a4f0cd9`、`ecddc57`、`9cc566a`；其餘 commits 為 record-only。

| Correction commit | 自行核對的檔案與 scope | 結果 |
| --- | --- | --- |
| `a4f0cd9` | `valhalla.py` 的 shape decoder 與說明；`adoption.py` 的道路名稱 UTF-8 判定與說明；`tests/test_routing_engine.py` 只新增 163 行 | 符合 Addendum A；處理 F1、F2 道路名稱、F4 |
| `ecddc57` | 只有 `http_transport.py` 的 context 建立與模組說明，以及 transport tests 新增 29 行；commit message 引用 C2R1-F3、CL-R1-28 | 符合 CL-R1-28 §3.1～§3.3；與 F1／F2 commit 分開 |
| `9cc566a` | `source.py` **只有 `_engine_info` 與其 docstring**；engine tests 只新增 55 行；message 引用 C2R1-F2、C-16-5、CL-R1-29 | 符合 CL-R1-29 §2.1～§2.3；沒有以 `try`／`except` 包住 `build_snapshot` |

`git diff --name-only fb6210d..18a5c5c -- <Addendum A protected paths>` 為空：`canonical.py`、`request_key.py`、`snapshot.py`、`store.py`、`target_gpx.py`、`routing/__init__.py`、`contracts/`、`ingest/`、`tests/routing_synthetic.py`、`tests/test_routing_snapshot.py`、`tests/test_routing_store.py`、`tests/test_target_gpx.py`、`pyproject.toml` 均未改。這個「未改」是相對 cycle 2 R1 subject；`__init__.py` 與 store gate 在更早的 #16 commits 中已有經審查的變更。

AST 比對證明兩個 correction 測試檔的所有既有函式／class（含 decorators、斷言與 fixtures）均未刪改。`source.py` 的既有函式只有 `_engine_info` 改變，`get_route` 中的 `ast.Try` 數量仍為 0。

## 3. 逐 finding closure

### C2R1-F1 — RESOLVED

原 severity **Medium／blocking**；owner #16 Executor。Required fix：任何可解析回應中的壞 shape 都須成為讀不到的路線資料，保留其他可讀國道訊號與兩方向檢查；非 200 保留 `engine_error`，不採用、不存檔、不以該 shape 查詢。

**原始碼證據：** `src/moto_copilot/routing/valhalla.py:209`～254 在整數單位檢查累加位置與單值上界，再除以 `1e6`；所有接受的點都在 ±90／±180 度內。單值上界大於任何兩個合法點之間的 zigzag delta，不會排除合法座標跳動。非字串、空值、非法字元、截斷與越界均走 `PolylineError`。`adoption.py:191`～266 收集旗標、maneuver／name 訊號後解碼，捕捉 `PolylineError`；`:389`～462 的非 200 分支與兩方向流程維持原有語義。

**執行證據：** `tests/test_routing_engine.py:1060`～1117 的 decoder、邊界、48 組 HTTP 200／302／400／429／500／503 × 有無訊號 × 去回程 × 兩種 overflow shape 均通過；包含去程已有訊號而回程 shape 壞掉的原反例。不可讀 shape 不查 trace，另一方向仍送出，沒有路線或快照。另自行在記憶體測 4011 個值／合成字串（含 JSON 型別、孤立 surrogate、超大值與長零延續），只得到範圍內點或 `PolylineError`；300 組合法、跨座標邊界的八點 shape 精確 round trip。這些是有限補充證據，不宣稱窮舉所有資源耗盡情形。

恢復 R1 decoder 的記憶體突變被抓到：**31 failed、27 passed**。無剩餘 required fix。

### C2R1-F2 — RESOLVED（道路名稱＋CL-R1-29 狀態版本）

原 severity **Medium／blocking**；owner #16 Executor。

**道路名稱 required fix：** 寫入快照的名稱不是合法 Unicode 時，該方向記為讀不到、不採用、不存快照；其他國道訊號仍優先。`adoption.py:159`～188 以嚴格 UTF-8 判定；先執行國道名稱比對，再對不合法名稱記 `response_malformed`，並繼續收集。`tests/test_routing_engine.py:1167`～1211 的去程／回程、單向、兩種 lone surrogate、含國道字樣、合法非 ASCII 名稱及不寫入快照的道路屬性名稱對照均通過。恢復接受不合法名稱的記憶體突變：**10 failed、2 passed**。

**狀態版本 required fix（依 CL-R1-29）：** `source.py:237`～269 只有非空且可嚴格 UTF-8 編碼的字串原樣保留，否則記固定 `unreported`；不修補、替換、截斷，不影響路線採用或同一回應的 `map_data_date`。`get_route` 的 `build_snapshot` 與存放例外沒有被攔下。`tests/test_routing_engine.py:1226`～1267 的 V-1～V-3 **18 例**通過：來回／單向 × 三種不合法版本均採用並存一個快照，日期保留、status 恰好一次；Snapshot Mode／一般重用讀回結果相同；合法 é／中文／emoji 原樣保留；原本應拒收時不送 status、不存檔、代碼不變。

版本三個記憶體突變均被抓到：拿掉 UTF-8 判定 **6 failed**；修補版本 **6 failed**；一律拒絕非 ASCII **3 failed**。另以記憶體 SnapshotStore double 檢查 6 種版本，路線／日期／請求序列均符合上述規則。無剩餘 required fix；呼叫端 `ref_id`／`role` 的 TI-C165-1 依 DA disposition 排除，不擴張本 correction。

### C2R1-F4 — RESOLVED

原 severity **Low／non-blocking**；原 disposition：owner #16 Executor，隨 F1 處理，不另立 work item。Required result：stored shape 解碼錯誤維持 CL-R1-17 的 `SnapshotIntegrityError`。

同一 decoder 已將 overflow 改為 `PolylineError`，`source.py:272`～281 原有的轉換現在適用。`tests/test_routing_engine.py:1128`、`:1136` 以重新計算有效 hash 的合成壞 shape 快照，確認一般 Snapshot Mode、normal reuse、strict mode 都停止為 `SnapshotIntegrityError`，不呼叫引擎；訊息不含 shape，`from None`。兩項測試均通過；恢復舊 decoder 的突變也使這兩項失敗。沒有修改受保護的 snapshot／store 模組。Disposition：**closed with F1**。

### C2R1-F3／CL-R1-28 — RESOLVED

原 severity **Low／non-blocking**、routing signal；原 owner Design Authority。DA 已由 `decision-20261118-issue16-c2r1f3.md` 解釋並要求消除 keylog 寫檔，run record 事件 102 採同輪獨立 commit、由本 R2 限定核對。不是將 F3 升級為新的 blocking finding。

**Required result 與來源：** `http_transport.py:76`～89 明確建立 `SSLContext(PROTOCOL_TLS_CLIENT)`、設 `CERT_REQUIRED`、`check_hostname = True`，再 `load_default_certs(Purpose.SERVER_AUTH)`；沒有呼叫 `create_default_context()`，沒有設定 keylog 路徑、載入額外憑證或降低 TLS 屬性。模組說明依 CL-R1-28 區分本模組的禁止讀環境變數與 OpenSSL 的信任來源限制。其他傳輸邏輯未改。

**CL-R1-28 §3.2／§3.3 evidence：**

- T-11（`tests/test_routing_transport.py:436`）核對列出的十項安全屬性與 `cert_store_stats()` 全部等於同一直譯器、無 `SSLKEYLOGFILE` 時的標準 default；`keylog_filename is None`。
- T-12（`:449`）在 pytest 暫存目錄設定合成 keylog 路徑，分別請求 route／trace_attributes／status（全為替身連線），三個 contexts 都沒有 keylog，檔案不存在。
- T-1～T-10、T-3、靜態 import／環境變數 gates 在全套中維持通過。Commit `ecddc57` 的 scope、獨立性與 message 符合要求；worklog §13.3～§13.7 已記 E-1、E-6、diff 與突變。
- 本 reviewer 自行重跑五種記憶體 TLS 突變，每種在 T-11／T-12 子集中至少 **1 failed**：改回 default；default 後清除 keylog；不載 default certs；CERT_OPTIONAL；關閉 hostname check。前兩種都由 T-12 抓到，包含「先建立再清除仍留下檔案」的情形。沒有真實 handshake。

Disposition：**DA clarification implemented and verified**。TI-C2R1F3-1 仍 tracked，owner Design Authority（SIA／之後文件）；不延長本 cycle。

## 4. Regression、風險與 evidence

| 核對 | 自行取得的證據與結論 |
| --- | --- |
| R1-F1 | `adoption.py:399`～402、`:417`～423 仍收集非 200 本文訊號，保留 `engine_error`／`trace_failed`，永不採用；`test_r1_f1_*` 保留並通過。**RESOLVED，未回歸** |
| R2-F1 | `adoption.py:121`～133 的 `_real` 仍拒絕不可表示為 float 的 int；既有三個數值欄位、HTTP 200／非 200、兩方向與訊號回歸測試保留並通過。**RESOLVED，未回歸** |
| 修正直接產生／暴露的 blocking defect | 自行加測 48 組 response matrix：200／503 × 去回程 × 壞 shape／兩種名稱欄位 × 無訊號／has_highway／maneuver highway／國道名稱。均返回預期代碼，兩方向都檢查、沒有 status 或 snapshot。查詢與採用流程未被 broad catch 遮蔽。**未發現新的 blocking defect** |
| H-1 | TLS 修正依上節；端點、URL 檢查、無 proxy／redirect／retry、固定 timeout 與 header 邏輯均未改且 T-1～T-10 通過。Correction diff 沒有憑證值、log 或含敏感本文的例外；`git ls-files` 的 `.env`、`*.key`、`*.gpx`、`*.fit` 樣式計數為 0。無付費呼叫。**限定本 R2 的 regression 核對通過** |
| H-2 | Correction 沒有改請求內容或 User-Agent；T-5／T-6 與 engine privacy tests 通過。新增資料沿用 0°N／0°E 附近合成幾何、合成回應／版本／日期／shape；沒有新地標或私有來源。隱私裁切、錨點代換屬 G-RREQ／TI-C16-3，不冒稱本 Ticket 已驗證；真實 GPX 見 NV-PRIVATE |
| H-4 | 壞 shape／名稱與無法驗證的回應均不採用，國道訊號仍優先；警告、2% 長度、偏移、順序、200.04 m 原值拒收、兩方向失敗不存檔、過期不回退、strict／store error 與 target_gpx 隔離測試均在全套通過。狀態版本依 CL-R1-29 視為未回報，仍須先通過所有採用檢查。**本 correction 的 H-4 核對通過** |
| E-1 | Worklog §14.4 記 implementation subject `9cc566a` 的完整 2238 passed 輸出；之後至 HEAD 只有 records。Reviewer 在本 HEAD 用 PATH 的 `python` 完整重跑兩種指定指令，均 2238 passed |
| E-2 | 既有 AC 對應不刪改；worklog §13.4、§14.3 列本次 closure／T-11、12／V-1～3 與測試名稱、結果，與實際斷言及數量一致：2148＋70＋2＋18＝2238 |
| E-3／E-4 | 新增案例來源說明與 diff 一致，FakeEngine／HTTPSConnection doubles 與 socket 封鎖保留。Reviewer 的 probes 僅用合成值與記憶體替身，沒有外部請求 |
| E-5 | 本 correction 沒有改既有測試。更早 CL-R1-25 准許的 store gate 修改僅為指定函式，本輪未再動它；不重開 #14 |
| E-6 | Worklog §13.7、§14.6 有相應 self-verification；舊版本例外句已標為被 §14.6 取代，最新陳述限已測的道路名稱、版本與 shape，不宣稱窮舉。Reviewer 自行核對如上 |

## 5. 實際命令與結果

所有命令都在本 worktree；使用 PATH 的 `python`（3.11.2），沒有直接呼叫 `.venv` 路徑或覆寫 `PYTEST_DEBUG_TEMPROOT`。

| 命令／檢查 | 結果 |
| --- | --- |
| `git status --short`；`git rev-parse HEAD`；`git rev-parse bc7024b` | 初始 CLEAN；SHAs 如檔首 |
| `git log --oneline bc7024b..18a5c5c`；`git diff --stat bc7024b..18a5c5c`；`git diff bc7024b..18a5c5c -- src/moto_copilot/routing/__init__.py tests/test_routing_store.py` | subject／較早的 exports、gate 與 commit 分配如 §2 |
| `git diff fb6210d..18a5c5c -- src/`；同範圍兩個 routing 測試檔 diff；`git show --format=fuller --stat a4f0cd9`／`ecddc57`／`9cc566a` | 只有授權的六個 source／test paths；各 commit 與 record 分開，無 scope expansion |
| Protected paths 的 `git diff --name-only fb6210d..18a5c5c -- ...`；AST 比對既有 functions／classes | protected diff EMPTY；兩個測試檔既有定義變更數 0；source 只有 `_engine_info` 改變 |
| `python -m pytest -q` | **2238 passed in 38.38s**，exit 0 |
| `python -m pytest -q -rxX` | **2238 passed in 31.30s**，exit 0；沒有 xfailed／xpassed／skipped 摘要 |
| `rg -n 'xfail\|skipif\|pytest\.skip\|pytest\.importorskip\|mark\.skip\|__test__\|unittest\.skip' tests/`（各選項以 regex alternation 搜尋）；另以 AST 掃描 xfail／skip／skipif／importorskip attributes | 均 0 筆；沒有相關標記 |
| `python -`，stdin supplementary probes（§3～§4） | decoder 4011 值、合法 shape 300 組、response matrix 48 組、版本 6 組全部通過；socket 封鎖；沒有新增 probe 檔案 |
| `python -`，stdin 記憶體突變 harness，內呼叫 `pytest.main(['-q','--tb=no','-p','no:cacheprovider', <routing test file>, '-k', <selection>])` | 10 種突變全部 KILLED（預期 exit 1）；失敗數如 §3。只替換記憶體 function bindings，ExitStack 復原；沒有寫回來源 |
| 突變還原後：`python -m pytest -q tests/test_routing_engine.py tests/test_routing_transport.py -k 'r1_f1 or r2_f1 or c2r1 or cl_r1_29 or t11 or t12'` | **320 passed, 240 deselected in 1.11s**，exit 0；deselected 為命令刻意選取子集，沒有 skip |
| `git diff --check fb6210d..18a5c5c`；`git diff --exit-code -- src/ tests/`；寫 record 前 `git status --short` | 全部 exit 0、無輸出；工作目錄 CLEAN |

執行透明性：最初一次 `pytest -q` 的工具輸出只取到部分進度，未保留可回收的 session id，因此沒有把它算成完整通過證據；上表的 38.38s 是隨後取得完整結束狀態的重跑。一次 git metadata 的 stdin harness 因 subprocess 預設 cp950 解碼英文 commit 中的 en-dash 而中止；改為明確 UTF-8 後完成，這是 harness 錯誤，不是產品失敗。沒有修改檔案來排除上述問題。

## 6. NOT VERIFIED 與既有 tracked items

| ID | 項目／理由 | Required authority／owner |
| --- | --- | --- |
| NV-1 | 真實 Valhalla 連線、TLS handshake、實際伺服器回應、S39／S40 參考路線與詞彙表：**NOT RUN**；dispatch 與 CL-R1-1 禁止真實請求。合成通過不代表 AB-1 端到端證據成立 | acceptor；之後獲授權的整合 work item |
| NV-PRIVATE | 真實 GPX、holdout、私有位置與其裁切／錨點外送行為：**NOT VERIFIED**，沒有 RB-7 路徑授權，也沒有嘗試取得 | acceptor |
| NV-BIND | 本 R2 的精確 model／effort／sandbox 與完整 rollout 存取稽核：由派工者在本次 dispatch 的 run record event 補核；目前 subject 只有至事件 105，不能提供未存在的事件編號。Executor 的實際 model 亦只依該 run record 的派工者證據引用 | 派工者／Orchestrator，依 Bindings §3.3、§3.6，**採用本 record 前完成** |
| NV-MUT | Worklog 的外部 scratchpad `mutate16d.py`／`mutate16e.py` 與較早 39 個突變沒有讀取或原樣執行；本 reviewer 另以記憶體重現本 correction 的 10 種關鍵突變。未重跑的 A5／A6 與較早突變不冒稱已獨立執行 | 本 record 已限定 verification coverage；不另增工作 |
| NV-PY | Python 3.11.2 以外版本／其他平台的安全 default、信任來源與檔案系統行為未執行；T-11 仍保留原嚴格比較 | 之後的平台驗證；本次無需額外 authority |
| TI-C2R1F3-1 | default trust 仍可受 `SSL_CERT_FILE`／`SSL_CERT_DIR` 影響；`OPENSSL_CONF` 影響 **NOT VERIFIED**。不宣稱傳輸層完全不受環境變數影響 | Design Authority，SPEC-R1 SIA／之後文件 |
| TI-C16-2／TI-C16-3／TI-C165-1 | 圖磚最後修改日期的用語；請求位置與 request_key 地點對應；呼叫端 `ref_id`／`role` 在發請求前的合法值檢查。依既有 DA disposition 留在指定後續範圍，不擴張本 Ticket correction | Design Authority，G-RREQ／之後文件與 SIA |

本 R2 沒有新增 blocking 或 non-blocking finding；原四項 closure 如 §3。下一步由 Orchestrator 完成本 dispatch binding 核對、原樣採用 record，並依既定流程推進。此 verdict 不代替 Spec Integration Audit、DA phase acceptance、真實服務驗收或任何 release authorization。

沒有讀取、列出或搜尋 `data/`，沒有讀 `.env` 或任何憑證，沒有讀取 worktree 外的檔案；沒有執行 `experiments/`，沒有 GitHub 或其他網路呼叫；沒有派 subagent、stage 或 commit。唯一新增檔案為本 record（另有測試正常產生的 ignored 暫存／cache）。

Verdict: PASS
