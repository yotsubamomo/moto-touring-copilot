# Issue #16 — cycle 1 R2 closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，接受版本 `873e37a`）→ SPEC-R1 v1（`docs/governance/records/decisions/derivation-spec-r1.md` §2、§4、§5 R1-4 與 E-1～E-6）＋`decision-20261118-issue13-c131.md` CL-R1-13＋`decision-20261118-issue14-c141.md` CL-R1-14、17、19＋`decision-20261118-issue14-qalt1.md` CL-R1-20、21＋`decision-20261118-issue15-c151.md` CL-R1-24＋`decision-20261118-issue16-c161.md` CL-R1-25～27 → Issue #16 |
| Subject | 專用 worktree，detached HEAD；BASE `bc7024b24b968e2dfb04dc38e822781dd5fb5425`；HEAD `07996828afaa0db3a7d477a05528fe993dc46d49`。R1 subject `e1ef5806695b693e7f84e12804852cc73123ebd9`；targeted correction `65aa00c` |
| Audit kind | **Ticket R2 closure review，cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`，Codex；Reviewer 自寫本 record |
| 日期 | 2026-11-18（Asia/Taipei） |
| Records | Run：`docs/governance/records/run/run-20261117-oc1-run2.md`；R1：`docs/governance/records/audit/issue-16-c1-r1.md`；worklog：`docs/governance/records/worklog/issue-16.md` §11 |
| 結果 | **R1-F1：NOT RESOLVED（closure 所需條件未全數成立）**。原三類反例已通過，但修正直接引入非 200 本文解析的 blocking regression，詳見 R2-F1。既有全套測試兩次各 2015 passed；獨立新增的記憶體內檢查為 4 failed、5 passed |

## 1. Assurance、binding 與 independence

依治理 §2.3、§3.8、§4.2～4.7、Bindings m3 §3.3 O-6、Reviewer definition 與 impl-default v2 §6～7 執行；R2 的範圍依治理 §4.4，不重作第二次全面 R1，不作 SIA、phase acceptance 或 Ticket completion。

| Property | 滿足機制與本次證據界限 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread；未繼承 Executor 或 R1 的對話與推理。自行重讀磁碟上的 R1 record、修正後來源、diff、worklog 與原始測試。Executor 的 PASS 與 return 均作待驗證主張 |
| Verifiable binding | 使用 Bindings §3.3 的 Codex dispatch／rollout 機制。**本次 R2 的 binding 證據由 dispatcher 記入 run record §6「#16 cycle 1 R2」派工事件**。受審 HEAD 的 §6 目前止於事件 **93**，沒有本次 R2 事件號、thread、turn_context 集合或 record hash，因此此處引用該待補記事件，不虛構為事件 94。事件 92 是 R1、93 是 correction，均不是本次 binding。正式採用前由 dispatcher 補記核對，見 NV-BIND |
| Autonomous access | 自行取得本 worktree 內契約、來源、測試、git 歷史及差異；以 PATH 的 `python` 重跑兩次全套測試，並自行設計反例與修正前後比對。未讀取 worktree 外路徑、私有資料、憑證或外部 rollout；沒有網路請求 |
| Self-written record | 本檔由本次 Codex 自行撰寫，未派 subagent；未修改實作、測試、契約或 gates，未 stage／commit。兩次全套測試及所有額外 probes 後，寫本檔前 `git status --porcelain` 為空。本次唯一新增的非快取檔案是本 record；dispatcher 依 Bindings §3.3 原樣採用並核對 SHA-256 |

Model evidence 分開陳述：

- **Executor**：run record §6 事件 89、91、93，agentId `a1e2cfa52290d496f`；事件 93 記錄全部 202 則 assistant 訊息的 model／effort 集合只有 (`claude-opus-5-5`, `high`)，dispatcher 判定符合。這與 worklog §11.1 的自我觀測分開看待。
- **Primary**：本次是 Codex。預定 mapping 與先前 qualification 不是本次實際 runtime model 的核對證據；確切 model ID、effort、sandbox、turn 數及 record hash 由 dispatcher 在本次 R2 派工事件記錄。未越界自行讀 rollout。
- **no model diversity claim**。本 record 不以產品名稱或 R1 的 binding 推定本次實際 model diversity。

## 2. R1-F1 closure 核對

R1-F1 原為 Medium／blocking，owner＝#16 Executor。Required fix 是把成功狀態與可讀國道訊號收集分開，非 200 保留 `engine_error`／`trace_failed`、永不採用，在決定代碼前收集所有可取得的訊號；禁止 redirect、retry、snapshot；補三類 regression、無訊號錯誤及 200 行為證據。派工另要求不可讀／非 JSON 本文不得拋例外。

| Required fix／regression | 本次實證 | 判定 |
| --- | --- | --- |
| 非 200 路線回應仍收集 `has_highway`，保留 `engine_error` | `adoption.py:368`～373；新增 `test_r1_f1_a_non_200_route_reply_with_a_freeway_signal_is_highway_in_route`，亦涵蓋 maneuver highway／國道名稱，302、400、429、500、503；獨立重跑 R1 的 route 503 反例通過 | 原反例已修正；含不可計算長度時仍失敗，見 R2-F1 |
| 非 200 道路屬性回應收集 motorway／Freeway，保留 `trace_failed` | `adoption.py:387`～392；新增 `test_r1_f1_a_non_200_road_attribute_reply_with_a_freeway_signal_is_highway_in_route`；獨立重跑 R1 的兩個 trace 503 反例通過 | 原反例已修正；同樣有 R2-F1 |
| 非 200 永不採用、不存快照、不根據錯誤 shape 發查詢；兩方向合計決碼 | 新增 never-adopted、跨方向訊號與錯誤混合案例通過；獨立三類反例及兩個無訊號案例確認無 route／snapshot、action 次序和 error reason | 所測案例通過；R2-F1 會在回程檢查前中斷 |
| 無訊號的非 200 維持 `routing_unavailable` | 新增 route／trace without-signal tests 與獨立兩例通過 | 一般案例通過；大整數長度變成例外，見 R2-F1 |
| 不可讀／非 JSON 本文不拋例外 | 新增 route 的 11 種 body × 3 種 status、trace 的 9 種 body × 2 種 status 均通過；但未涵蓋有效 JSON 中超出浮點表示範圍的整數 | **不足；R2-F1 blocking** |
| 200 採用／拒收行為不變 | 既有 engine 測試／helper 的 AST 均未改；全套兩次通過；以 R1 來源在記憶體中與 HEAD 比較 195 組 200 route／trace 組合，DirectionOutcome 所有欄位一致 | 在本次比對及既有案例內通過 |
| redirect／retry／過期回退沒有引入 | 傳輸層與 `source.py` 相對 R1 為空 diff；T-1～T-10、S17／S35、no-retry、store／strict tests 在全套中通過 | 在本次 synthetic regression 範圍通過 |

**R1-F1：NOT RESOLVED。** 這不是說原三個重現仍失敗；它們已通過。無法 closure 的原因是新的訊號收集會被非訊號數值欄位的解析例外中斷，仍無法滿足「先收集所有可取得訊號，再回傳路線錯誤」及無回歸要求。其具體 blocking 證據集中記為 R2-F1，不重複計算兩項獨立缺陷。

## 3. Finding R2-F1 — 非 200 的新增訊號收集被無關數值欄位的 OverflowError 中斷

- **Severity：Medium；blocking。Owner：#16 Executor。** 這是 correction 直接產生的 regression，屬治理 §4.4 的 R2 範圍。
- **契約依據**：CL-R1-8（`derivation-spec-r1.md:73`）、R1-4 範圍 (c)、額外 AC 的國道訊號優先順序、SPEC-001 4.13／7.11 第 5 項；派工及 worklog §11.1 的不可讀本文不拋例外要求。H-4 要求服務失敗／無法驗證時回傳明確路線錯誤。
- **來源證據**：`src/moto_copilot/routing/adoption.py:372` 與 `:392` 為 correction 新增的兩個呼叫。兩者為了取得 signals，呼叫還會解析長度等採用資料的 `_route_facts`／`_trace_facts`。`adoption.py:187`／`:276` 先經 `:118` 的 `_real`；`math.isfinite(value)` 會把 Python int 轉成 float，對 `10**400` 拋 `OverflowError: int too large to convert to float`。這是約 401 位數的合法 JSON 整數，`ValhallaClient._parse_json` 正常讀成 int，並非無法解析的 JSON。
- **可重現輸入**：沿用 `tests/test_routing_engine.py` 的 synthetic helpers，去程 HTTP 503，其他回應正常。route 情形把 `route_body(OUT_POINTS, has_highway=signal)['trip']['summary']['length']` 改成 `10**400`；trace 情形把 `trace_body(OUT_POINTS, road_class='motorway' if signal else 'primary')['edges'][0]['length']` 改成 `10**400`。`signal` 各取 False、True，共四例。訊號為 True 時，國道旗標／motorway 已是可讀的明確訊號；長度無效不應阻止取得它。

| 本文／訊號 | R1 `e1ef580`，同一 evaluate_direction 輸入 | HEAD `0799682`，evaluate_direction 及真實 get_route |
| --- | --- | --- |
| route 503，無訊號，超大長度 | reasons `('engine_error',)`、無 leg | 未捕捉的 OverflowError；預期 `routing_unavailable` |
| route 503，has_highway=true，超大長度 | reasons `('engine_error',)`、無 leg（原 R1-F1） | 未捕捉的 OverflowError；預期 `highway_in_route` 並保留 engine_error |
| trace 503，無訊號，超大 edge length | reasons `('trace_failed',)`、無 leg | 未捕捉的 OverflowError；預期 `routing_unavailable` |
| trace 503，motorway，超大 edge length | reasons `('trace_failed',)`、無 leg（原 R1-F1） | 未捕捉的 OverflowError；預期 `highway_in_route` 並保留 trace_failed |

修正前來源以 `git show e1ef580:src/moto_copilot/routing/adoption.py` 讀入獨立的記憶體 module，沒有 checkout、覆寫或執行舊版外部腳本。四例都證明：非 200 路徑原先能產生明確錯誤結果，correction 才使它們進入數值解析並拋例外。200 的同類數值問題不是本次另外展開的 finding；本項只依新增的非 200 行為判定。

透過真實 shared interface 的記憶體 pytest plugin（掛在原 test module 下，沿用 autouse socket 封鎖與 tmp_path）得到：

```text
.....FFFF                                                                [100%]
FAILED tests/test_routing_engine.py::review_r2_route_signalFalse_hugeTrue
FAILED tests/test_routing_engine.py::review_r2_route_signalTrue_hugeTrue
FAILED tests/test_routing_engine.py::review_r2_motorway_signalFalse_hugeTrue
FAILED tests/test_routing_engine.py::review_r2_motorway_signalTrue_hugeTrue
4 failed, 5 passed, 274 deselected in 0.22s
```

四個失敗皆是 `get_route → _ask_engine → evaluate_direction → _route_facts／_trace_facts → _real → math.isfinite` 的 OverflowError。Harness 在 finally 確認 store 仍空；沒有採用或存快照的證據。另五例為 R1 原三類反例、route／trace 無訊號的普通 503，全部通過，並確認 error reasons、無路線、請求次數及兩方向行為。

**影響與 blocking 理由**：錯誤回應中一個無法計算的長度會使整次規劃拋出例外，而不是契約的路線錯誤；已有國道訊號時也無法傳回正確 code，回程檢查被中斷。沒有已採用國道路線的證據，故為 Medium；它直接違反 accepted code／failure 語義，不能因既有 suite 全綠而作 non-blocking。

**Required fix**：讓非 200 的可讀訊號收集不受無關採用資料（例如長度、時間、shape）計算失敗中斷。對無法表示／無效數值保持保守拒收，收集其餘可讀國道訊號，再保留 `engine_error`／`trace_failed`：有訊號回 `highway_in_route`，無訊號回 `routing_unavailable`；不得只把例外一律轉成 routing_unavailable 而再次丟掉國道訊號。加入上述四類回歸證據，保持非 200 不採用、無 snapshot、無 redirect／retry、200 行為不變，更新 worklog。具體實作 HOW 由 Executor 決定。

Non-blocking findings：無。既有 tracked items 延續 DA 的 disposition 與 owner，不延長 cycle。

## 4. Subject 與審查邊界

- `git rev-parse HEAD`／`git rev-parse bc7024b` 與檔首相符；`git symbolic-ref -q HEAD` 無輸出、exit 1，為 detached HEAD。開始與測試後 worktree 均 clean。
- 自行讀 `git log --oneline bc7024b..0799682`、`git diff --stat bc7024b..0799682`、`git log --format='%h %s' --name-only e1ef580..0799682`、`git diff e1ef580..0799682 -- src/ tests/` 與 `--numstat`。整體 implementation commits 為 `7cb4b0c`、`f6810d2`、`65aa00c`；本次 R2 的行為 delta 僅為 `adoption.py` 12 additions／3 deletions，測試新增 116 行。其餘 delta 僅為 R1 record、run record、worklog §11；沒有 scope expansion。
- `git diff --exit-code e1ef580..0799682 -- src/moto_copilot/routing/valhalla.py src/moto_copilot/routing/http_transport.py src/moto_copilot/routing/source.py src/moto_copilot/routing/store.py tests/test_routing_transport.py tests/test_routing_store.py`：空 diff、exit 0。
- `git diff --exit-code bc7024b..0799682 -- src/moto_copilot/routing/canonical.py src/moto_copilot/routing/request_key.py src/moto_copilot/routing/snapshot.py src/moto_copilot/routing/store.py src/moto_copilot/routing/target_gpx.py src/moto_copilot/contracts/ src/moto_copilot/ingest/ tests/routing_synthetic.py tests/test_routing_snapshot.py tests/test_target_gpx.py pyproject.toml`：空 diff、exit 0。
- AST 比對 R1 與 HEAD 的 engine 測試檔全部既有頂層函式（含 helper）：changed／removed 清單 `[]`。本次沒有以弱化既有測試處理 finding。

閱讀範圍：CLAUDE.md、Bindings 與 Reviewer definition；治理本文上述節、impl-default §6～7、orch-default v2.2 §6～7；R1 record 全文及 findings／assurance 重讀；run record §6 事件 89～93；worklog §11 與相關前節；derivation 的引用範圍、CL-R1-5～9、R1-4／E-1～E-6；派工所列 decision records 的適用 clarification／排除與 tracked-item 段落；高風險 record §5；OC-1 AB-1／2／10／13、DESIGN §5 相關規則、SPEC-001 4.13／4.14／7.11 與指定 S 列。自行讀目前 adoption 全文、valhalla 的解析／請求／shape、source 的 shared interface 與採用存放路徑、http_transport 全文、新增 regression tests、既有 helpers 與傳輸測試。使用 `Get-Content -Encoding UTF8`、指定路徑的 `rg -n`、stdin Python。未讀或執行 experiments，未作真實路線、詞彙表或私有 GPX 驗收。

## 5. 實際執行與 evidence sufficiency

全部命令在本 worktree 內執行；只以 PATH 的 `python` 啟動 Python／pytest，未使用環境目錄路徑啟動，未改動 PYTEST_DEBUG_TEMPROOT。以 sys.executable 相對 cwd 的斷言確認 interpreter 在本 worktree，版本 3.11.2。

| 命令／檢查 | 實際結果 |
| --- | --- |
| `python -m pytest -q` | exit 0，**2015 passed in 46.64s** |
| `python -m pytest -q -rxX` | exit 0，**2015 passed in 38.43s**；無 xfailed／xpassed／skipped 摘要 |
| `rg -n 'xfail\|\bskipif\b\|pytest\.skip\|pytest\.mark\.skip\|unittest\.skip\|@skip\b' tests/`（實際用 regex alternation） | 無命中；rg exit 1 表示未找到。另以 AST 遍歷 tests 下 16 個 Python 檔，skip／skipif／xfail 的 Name／Attribute 清單 `[]` |
| `git diff --check bc7024b..0799682` | 空輸出、exit 0 |
| 上節的 git 歷史、diff、protected paths、AST 比對 | 結果如 §4；既有 engine 測試函式無變動 |
| stdin `python -X utf8 -`：四個非 200 大整數長度的單方向 probes | route 與 trace 均重現 OverflowError；詳 §3 |
| stdin `python -X utf8 -`：git-show 舊 module 與 HEAD 比對 | 四例 R1 均回 error outcome、HEAD 均拋 OverflowError；195 組 200 outcome 完全一致 |
| stdin `python -X utf8 -`，呼叫 `pytest.main(['tests/test_routing_engine.py','-q','-k','review_r2_','--tb=short'], plugins=[ReviewPlugin()])` | exit 1，**4 failed, 5 passed, 274 deselected in 0.22s**；未寫測試檔，失敗為獨立契約 probes，不是既有 suite 失敗 |
| `git ls-files -z` 只作封閉樣式計數 | `.env`、`.key`、`.gpx`、`.fit`、全部 data 路徑的計數均為 0；未讀取這些路徑的內容、未輸出檔名 |
| `git status --short`／`git status --porcelain` | 開始、兩次 suite 及全部 probes 後、寫 record 前均無輸出，clean |

執行過的非產品失敗也如實記錄：第一次單方向 probe 只把 tests 加到 sys.path，匯入時 ModuleNotFoundError；將本 worktree 的 src 加入 sys.path 後才得到 §3 結果。最初 PowerShell 預設編碼讀中文顯示亂碼，後續以 UTF8 重讀。尋找 orch-default 時先試不存在的 `orchestrator-contracts/orch-default-v2.2.md`，再以明確 references 路徑的 `rg --files` 找到並讀取 `orchestrator-contracts/default-v2.2.md`。這些不作產品 finding。

| Evidence | 獨立核對結果 |
| --- | --- |
| E-1 | Worklog §11.3 有 correction `65aa00c` 的完整 pytest 輸出（2015 passed in 38.98s）及第二輪摘要；本次另兩次重跑通過。不能單憑此宣告 closure |
| E-2 | §11.4 的測試名稱與新增案例相符，97 案例涵蓋原三類、無訊號、不可讀 body 與跨方向組合；既有 177 個 engine 案例加 97＝274，transport 63。涵蓋不足處由本次 R2-F1 反例證明 |
| E-3 | 新增案例只用既有 synthetic route／trace helpers 或手寫 bytes；未增真實座標／軌跡、公開地標或 GPX。Reviewer probes 同源，只增加數值常數 |
| E-4 | 核對 FakeEngine、autouse socket 封鎖與 scripted HTTPSConnection／in-memory wire；probes 亦封鎖 socket，pytest plugin 沿用原 module fixtures。沒有真實網路請求 |
| E-5 | correction 無修改任何既有測試函式，AST 清單為空；R1 已審的 store 測試例外未再變動 |
| E-6 | §11.5 有 H-4 self-verification 及 mutation claim；與源碼／測試核對後，不能接受其中「每一種非 200 都是明確錯誤代碼」的概括，反例見 R2-F1。37 次 mutation 是 Executor 歷史紀錄；本次禁止改來源，沒有重跑 mutation，不冒充獨立執行 |

## 6. H-1／H-2／H-4 correction regression

依高風險 decision record §5 作本次有界核對，不重開既有 closure 或擴張 Must：

- **H-1**：傳輸層、client 端點及請求組成與 R1 空 diff。來源只有一連線／一 request、不跟隨 Location、不讀環境／proxy、不重試；default TLS context、有限固定 timeout、header 封閉清單、固定 TransportError／from None 保留。T-1～T-10 與 endpoint／import guards 在兩次 suite 通過。correction 的 302 tests 亦不增加 action。delta 無憑證／認證 header，追蹤禁止樣式計數為 0；無付費呼叫，額度控制不適用。真實 TLS／伺服器仍 NV-1。
- **H-2**：新增 fixture 與 probes 的幾何由 at(x,y) 及既有 synthetic encoder 產生；沒有新的個人資料來源、log、print 或落盤行為。route 只送呼叫者位置與固定參數，trace 只送成功路線回應自己的 shape，status 是空物件；UA 仍為 generic 名稱。correction 不根據非 200 shape 發出查詢，error outcomes 只含 codes；T-5／T-6 及不含合成座標的例外測試通過。私有路線、隱私裁切／錨點來源不在本 correction 重新實作，公開地標與 request_key 對應沿用 TI-C16-3 的 DA disposition，真實隱私效果 NV-PRIVATE。
- **H-4**：正常 200、warning／國道矛盾、缺 has_highway、trace 長度、offset／via order、snapshot／strict stop 的既有測試通過；來源與存放邊界未改。新增非 200 一般案例維持拒收、無 snapshot；但 malformed 數值使新增分支拋例外，未完成明確錯誤與訊號優先處理，因此 **本次 H-4 regression 核對不通過（R2-F1）**。不宣稱 Planner／計畫狀態／規則 5 的整合已驗證。

## 7. NOT VERIFIED 與後續 authority

| ID | 未驗證事項／原因 | Required authority／owner |
| --- | --- | --- |
| NV-1 | 真實 Valhalla 連線、TLS／redirect 的實際服務行為、回應形狀，以及 S39／S40 真實參考路線與詞彙表偏移：**NOT VERIFIED／NOT RUN**。派工禁止網路，CL-R1-1、CL-R1-25 §2.7 亦排除；fake 通過不等於真實執行 | acceptor；之後獲授權的整合 work item |
| NV-PRIVATE | 真實 GPX、holdout、真實位置來源與私有資料隱私效果：**NOT VERIFIED**。無 RB-7 明確路徑授權，未嘗試取得 | acceptor |
| NV-BIND | 本次 R2 的全部 rollout、實際 runtime tuple、存取核對、原樣採用 hash：**NOT VERIFIED by Reviewer**。受審 run record 最後是事件 93，尚無本次派工事件；R1 的事件 92 不代替 R2。正式採用前依 §1 在本次 R2 事件補記；不是要求 Reviewer 越界讀取 | dispatcher／Orchestrator，Bindings §3.3 |
| NV-MUTATION | worklog 的 37 次 source mutation 歷史執行未由本次重跑；本次只能讀取歷史 claims、檢查測試及做不改檔的 probes | Executor 的 self-verification record；本次沒有新增修改來源的授權 |

TI-C16-2（圖磚最後修改日期的對外文字）、TI-C16-3（G-RREQ 的位置／request_key 一致性）、RV-12～RV-14 沿用 DA 的 disposition 與 owner＝Design Authority；不當作新 non-blocking finding，也不宣稱已涵蓋。Python 其他版本與真實符號連結等先前平台限制，本次沒有新增驗證或改寫其狀態。

因 R2 仍有 blocking，下一步由 **Orchestrator 依治理 §4.4 派 exactly one Alternate Independent Review（fresh context）**，獨立判斷 R1-F1 的 closure 與 R2-F1。此處不自行加 R3、不授權新 cycle，也不以全套 pytest 通過取代 finding disposition。

Verdict: BLOCKING
