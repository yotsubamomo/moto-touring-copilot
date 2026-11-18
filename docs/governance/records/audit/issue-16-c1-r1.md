# Issue #16 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，接受版本 `873e37a`）→ SPEC-R1 v1（`derivation-spec-r1.md` §2、§4、§5 R1-4 與 E-1～E-6）＋`decision-20261118-issue13-c131.md` CL-R1-13＋`decision-20261118-issue14-c141.md` CL-R1-14、17、19＋`decision-20261118-issue14-qalt1.md` CL-R1-20、21＋`decision-20261118-issue15-c151.md` CL-R1-24＋`decision-20261118-issue16-c161.md` CL-R1-25～27 → Issue #16 |
| Subject | 專用 worktree，detached HEAD；BASE `bc7024b24b968e2dfb04dc38e822781dd5fb5425`；HEAD `e1ef5806695b693e7f84e12804852cc73123ebd9`。Implementation commits：`7cb4b0cabcccb6541f395f999fe5b43e1b905e91`、`f6810d2607e2f78f19020cc0ef32307dda2b23dd` |
| Audit kind | **Ticket independent audit，R1，cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`，Codex，Reviewer 自寫本 record |
| 日期 | 2026-11-18（Asia/Taipei） |
| Run／worklog | `docs/governance/records/run/run-20261117-oc1-run2.md`；`docs/governance/records/worklog/issue-16.md` |
| 結果 | 一項 Medium／blocking finding：R1-F1。既有測試兩次全數通過，但新增的三項記憶體內契約探測都失敗 |

## 1. Assurance 與 independence

依治理 §2.3、§4.3、§4.6、Bindings m3 §3.3 O-6，以及 `.claude/agents/gov-primary-reviewer.md` 執行。四項 properties 的機制與本次證據如下；不以 Executor 的 return 或 worklog 中的 PASS 作為本審查結論。

| Property | 本次滿足方式與證據界限 |
| --- | --- |
| Independent context | 本次為 fresh Codex thread，沒有繼承 Executor 對話或推理。從 bounded pack 的契約、subject 與路徑開始，自行閱讀原始檔、diff、歷史及測試；worklog 當作待驗證主張 |
| Verifiable binding | 採 Bindings §3.3 的獨立 Codex dispatch／rollout 核對機制；**當次全程 binding 的核對與寫入 run record 是 dispatcher 的責任**。引用位置為 run record §6 的本次「#16 cycle 1 R1」派工事件。受審 HEAD 的 §6 目前只到事件 **91**，尚無本次 R1 的事件、thread ID、turn_context 集合或 record hash；不得把事件 89～91 冒充本次 Reviewer binding。正式採用前須由 dispatcher 補記並核對，見 NV-BIND |
| Autonomous access | 在本 worktree 內自行取得契約、實作、測試、`git log`、`git diff`，以 PATH 的 `python` 執行兩次全套 pytest，並自行設計、執行不連網的反例。未存取 worktree 外的路徑，未讀憑證、私有資料或外部 rollout |
| Self-written record | 本檔由本次 Codex 自行撰寫；未委派 subagent，未修改實作、測試或契約。寫入前 `git status --porcelain` 為空；本次唯一新增的非快取檔案為本 record。Dispatcher 應依 Bindings §3.3 原樣採用並核對 hash |

Model 證據分開記錄：

- **Executor**：run record §6 事件 89、91，agentId `a1e2cfa52290d496f`；dispatcher 已記錄全部 assistant 訊息的集合僅有 (`claude-opus-5-5`, `high`)，事件 91 為 171 則。
- **Primary**：本次為 Codex。Run record §2 的預定 mapping 為 `gpt-6.1-sol`／`high`，但預定 mapping 不是本次實際 runtime model 的證據。本 worktree 沒有本次 rollout 核對結果；確切 model ID、effort、sandbox 與 turn 數由 dispatcher 依 NV-BIND 記錄。
- **no model diversity claim**。不以產品名稱不同或預定 mapping 推定實際 model diversity；也不宣稱已自行完成外部 binding 核對。

## 2. Findings

### R1-F1 — 非 200 回應會先丟掉可讀的國道訊號，違反 CL-R1-8 優先順序

- **Severity：Medium；blocking。Owner：#16 Executor。**
- **契約**：`docs/governance/records/decisions/derivation-spec-r1.md:73`（CL-R1-8）要求「引擎有回應時，先檢查所有可取得的國道訊號，再決定代碼」，任何方向有訊號即 `highway_in_route`，其次才是引擎錯誤或道路屬性查詢失敗等 `routing_unavailable`。同檔 §5 R1-4 範圍 (c) 與 AC 另加的優先順序、SPEC-001 4.13／7.11 第 5 項亦有此要求。
- **實作證據**：`src/moto_copilot/routing/adoption.py:367` 遇路線回應非 200 立即回傳沒有 signals 的 `engine_error`，在第 370 行 `_route_facts(body)` 之前已離開。因此即使本文有完整 `trip.summary.has_highway: true`，也不收集。第 382 行遇道路屬性回應非 200 只加 `trace_failed`；第 385 行 `_trace_facts` 僅在 200 的分支執行，所以本文中的 `motorway` 與國道名稱也丟失。第 433 行 `decide_code` 自身的優先順序正確，但已拿不到這些訊號。
- **獨立重現**：先以 stdin 的 Python 探測 `evaluate_direction`；再以 stdin 定義的 pytest plugin 於記憶體中加入三個測試，透過真正的 `get_route`、`SnapshotStore` 與合成的來回行程重現。沿用測試資料產生器與 autouse socket 封鎖，沒有修改測試檔，沒有網路。三個案例的斷言均要求 `HIGHWAY_IN_ROUTE`：

| 記憶體內測試 | 合成回應 | 實際結果 |
| --- | --- | --- |
| `review_non200_route_has_highway` | 去程 `/route` 為 HTTP 503，本文仍是完整合成路線，`has_highway = true`；回程正常 | `routing_unavailable`，reasons `('outbound:engine_error',)` |
| `review_non200_trace_motorway` | 去程路線正常；`/trace_attributes` 為 HTTP 503，本文含 `road_class = motorway`；回程正常 | `routing_unavailable`，reasons `('outbound:trace_failed',)` |
| `review_non200_trace_freeway_name` | 同上，本文道路名稱為 `Freeway` | `routing_unavailable`，reasons `('outbound:trace_failed',)` |

實際 pytest 輸出：`3 failed in 0.10s`，exit 1。三項測試在檢查代碼之前已確認沒有快照、兩個方向的路線請求都有送出。單方向探測也確認三者 `signals == ()`、`freeway_check is None`。這是既有測試沒有涵蓋的「同一筆非 200 回應同時帶可讀國道訊號」，不同於既有測試中「某方向 HTTP 錯誤、另一方向有訊號」。

**影響與 blocking 理由**：這三例沒有採用路線，也沒有存快照；缺陷是已接受契約明定的錯誤代碼與國道訊號優先順序不成立。回應訊號在判定前消失，會把「已偵測國道」呈現成一般服務失敗，因此分類為 Medium／blocking，不宣稱存在已採用國道路線的證據。

**Required fix**：讓回應是否成功與可讀國道訊號的收集分開；非 200 仍保留 `engine_error`／`trace_failed` 並禁止採用，但在決定代碼前收集本文所有可取得的國道訊號。不得因此跟隨轉址、重試、採用錯誤回應或存快照。加入上述三類非 200 與訊號並存的回歸案例，並確認無訊號的非 200 仍是 `routing_unavailable`、200 的既有採用與拒收行為不變；worklog 更新 coverage 與新 subject 的驗證結果。

Non-blocking findings：無。既有 DA tracked items 與本次無法自行取得的證據另列於第 7 節，不擅自變成新實作工作。

## 3. Subject、範圍與變更邊界

自行核對 `git rev-parse HEAD`、`git rev-parse bc7024b`、`git symbolic-ref -q HEAD`、`git log --oneline bc7024b..e1ef580`、逐 commit 的 `git log --format='%h %s' --name-only bc7024b..e1ef580`，以及 `git diff --stat`／`--name-status` 與來源 diff。

- HEAD 與 BASE 如檔首；detached HEAD 成立。BASE 之後共八個 commits，僅 `7cb4b0c`、`f6810d2` 修改 implementation／tests，其餘六個僅修改 `docs/governance/records/**`。
- `7cb4b0c`：新增 `valhalla.py`、`adoption.py`、`source.py`、`test_routing_engine.py`，`routing/__init__.py` 加說明與新 exports。沒有改寫既有 exports 的定義。
- `f6810d2`：逐項核對 `decision-20261118-issue16-c161.md` §2.4～2.6 的封閉清單；只有允許的七個 implementation／test 檔。`git diff 7cb4b0c..f6810d2 -- ...` 與去除 docstrings 後的 AST 比對證明 `source.py`、`valhalla.py` 只改 docstrings；`adoption.py` 的 delta 為 CL-R1-27、method 字串及相關說明。
- `git diff --exit-code bc7024b..e1ef580 -- src/moto_copilot/routing/canonical.py src/moto_copilot/routing/request_key.py src/moto_copilot/routing/snapshot.py src/moto_copilot/routing/store.py src/moto_copilot/routing/target_gpx.py src/moto_copilot/contracts src/moto_copilot/ingest tests/routing_synthetic.py tests/test_routing_snapshot.py tests/test_target_gpx.py pyproject.toml`：空 diff，exit 0。#14、#15 相關模組、`contracts/`、`ingest/` 的既有內容不變；全套回歸亦通過。
- `git diff bc7024b..e1ef580 -- tests/test_routing_store.py`：只改 `test_the_routing_package_imports_no_network_or_environment_modules`。以 AST 比較該檔全部頂層測試函式，也只有此函式不同。其餘測試沒有被弱化。
- 該函式現在遞迴 `rglob`；要求頂層 `http_transport.py` 存在；僅該確切路徑可 import `http`／`ssl`；其他原禁止模組仍禁止；其他 routing 模組不能引用該傳輸模組，含相對、絕對與 literal dynamic import；全部檔案仍禁止 `environ`／`getenv`。就 CL-R1-25 要求的證明範圍至少同樣嚴格，且補上原本不掃描子套件的缺口。

本次原始資料閱讀包括 `CLAUDE.md`、Bindings m3、Reviewer definition、治理本文 §2.3／§3.8／§4.1～4.7、impl-default v2 §6～7、orch-default v2.2 §7；契約與上列 clarification records；高風險 record §3、§5；first-run derivation 的分配與 exclusions；OC-1；DESIGN §5；SPEC-001 §2、4.13、4.14、5.4、7.11、指定 S 編號；新來源模組全文、相關既有 canonical／snapshot／request_key／store 介面、新測試與被修改測試、worklog 各 evidence 節。使用 `Get-Content -Encoding UTF8`、指定路徑的 `rg -n` 與 stdin Python／AST 檢查。未執行或讀取 `experiments/` 腳本；本次不需要以它們作證。

## 4. R1-4 範圍與逐項 AC 核對

以下測試名稱屬 `tests/test_routing_engine.py`，除非另列。PASS 僅指本 Ticket 分配的部分；不代表 AB 全部完成。

| 項目 | 自行核對的實作／測試 | 判定 |
| --- | --- | --- |
| 範圍 (a)：client、每方向獨立請求及道路屬性查詢 | `valhalla.py` 的固定 routing params、`route_locations`、`trace_body`；`test_cl_r1_5_each_direction_gets_its_own_positions_one_route_and_one_trace_request`、`test_the_road_attribute_query_sends_only_the_engines_own_shape`；真實傳輸的 T-1～T-10 | PASS；真實連線 NOT RUN |
| 範圍 (b)：國道四訊號、method、警告、偏移與順序 | `adoption.py`；S39、CL-R1-27、S40、S68～S70、CL-R1-19 測試 | 正常及既有拒收案例通過；非 200 訊號收集缺口見 R1-F1 |
| 範圍 (c)：錯誤代碼 | `decide_code` 及兩方向合計；`test_a_freeway_signal_with_another_reason_is_highway_in_route` | **FAIL，R1-F1**；既有組合測試通過不足以證明所有可讀回應 |
| 範圍 (d)：RouteLeg、版本、全通過才存放 | `evaluate_direction`、`source.py:188` 的 `store.put`；`test_a_round_trip_is_adopted_and_stored_once`、`test_cl_r1_6_road_names_follow_the_maneuvers_in_order_without_repeats`、`test_dd_r1_2_engine_version_and_map_data_date` | PASS |
| 範圍 (e)：Snapshot／嚴格模式與一般重用順序 | `source.py:158`、159、170；只用三個 R1-2 selectors；S17、S35 及 strict tests | PASS；不回退過期快照、不攔 store 錯誤 |
| 範圍 (f)：shared interface | `get_route` 的兩種 request、`AdoptedRoute`／`RouteFailure`；CL-R1-24 測試 | PASS，保留方向幾何、長度、名稱與各來源識別／折返資訊 |
| S15 路線部分 | `test_s35_s15_engine_failure_with_only_an_expired_snapshot_is_routing_unavailable`、`test_s15_a_snapshot_checked_with_another_method_is_not_used_when_the_engine_fails`、`assert_no_route` | PASS：錯誤結果無路線里程與道路名稱，不補造 |
| S17 | `test_s17_snapshot_mode_does_not_call_the_engine`、`test_s17_snapshot_mode_without_a_snapshot_returns_snapshot_missing`；strict mode 成功與停止案例 | PASS |
| S23 行為部分 | `test_s23_each_direction_has_its_own_request_shape_and_fetched_at_and_return_is_not_reversed` | PASS：各有 request、shape、fetched_at，回程用自己的回應 |
| S24 第一句 | `test_s24_a_fail_in_either_direction_stores_nothing_and_is_highway_in_route`，兩方向參數 | PASS（既有已形成 fail 的情形）；非 200 未形成 fail 的缺口另見 R1-F1。`leg_length_diff_flag` 排除 |
| S30 | `test_s30_route_request_is_motorcycle_with_use_highways_0_and_no_exclusion_or_elevation`、`test_s30_a_reply_with_any_warning_is_routing_unavailable` | PASS；警告與國道訊號並存由優先順序處理 |
| S35 引擎部分 | 同請求第二次不呼叫；31 天後相同／不同內容；只有過期快照且引擎失敗；回程失敗整條不存等 `test_s35_*` | PASS |
| S38 路線部分 | S23 測試與 `test_s35_s38_one_direction_failing_stores_nothing_and_has_no_route[return]` | PASS；turnaround 檢查點不在本 Ticket |
| S39 合成部分 | has_highway trip／leg、motorway、國道名稱、maneuver highway、trace 失敗等 `test_s39_*` 與 `test_maneuver_names_and_highway_flags_are_freeway_signals` | 指定合成案例 PASS；非 200 並存訊號的額外 AC 為 FAIL |
| S40 合成部分 | `test_s40_an_end_offset_of_several_kilometres_is_rejected`、`test_s40_s68_a_via_more_than_200_m_from_the_shape_is_rejected` | PASS |
| S68 | 上列 200.5／250／5000 m via offset 拒收 | PASS |
| S69 | `test_s69_two_vias_within_200_m_but_passed_in_reverse_order_are_rejected` | PASS；同兩點正序可採用 |
| S70 | `test_s70_the_road_entry_position_also_has_a_via_offset` | PASS；公路進入端納入中間位置 |
| 另加：未回報 has_highway | `test_has_highway_not_reported_is_routing_unavailable_with_no_freeway_check_value` | PASS；沒有訊號時不產生 freeway_check；truthy 非 bool 另作訊號，DA §4.3 已接受 |
| 另加：長度相差超過 2% | `test_the_road_attribute_length_must_be_within_2_percent`、`test_the_2_percent_check_is_exact_at_the_boundary` | PASS：原值／Decimal 比較，±2% 邊界與略超門檻 |
| 另加：國道優先於其他不採用原因 | 既有混合原因測試及本次三個非 200 反例 | **FAIL，R1-F1** |
| 另加：中間位置沿線里程相等拒收 | `test_cl_r1_7_vias_with_equal_along_shape_distance_are_out_of_order` | PASS |
| 另加：User-Agent／內容無個人識別 | `test_user_agent_and_request_content_hold_no_personal_information`；transport T-5、T-6 | PASS（合成資料及本層組成方式）；公開地標來源見 TI-C16-3 |
| 另加：端點不受環境變數影響 | `test_h1_the_endpoint_is_not_affected_by_env_variables`、transport T-1～T-4、T-7、T-10 | PASS |

**排除核對**：沒有做 S39「五條參考路線的 10 段」、S40「五條參考路線」及詞彙表 100 m 的實際驗收；均 NOT RUN。G-RREQ、`route_source = trip`、route catalog、RouteSummary 與 RouteError 文字沒有被本次變更收編。位置與 request_key 的對應保留為 TI-C16-3，不要求 #16 自行制定 G-RREQ 語義。

## 5. Clarifications 與高風險最低核對

| 條款 | 核對結果 |
| --- | --- |
| DD-R1-2、CL-R1-26 | `_engine_info` 從 `/status` 取得 version，缺少／失敗是固定 `unreported`；圖磚修改秒數只接受非負 int、排除 bool，轉 +08:00 日期；缺少、型別錯誤、失敗或日期超界時 null，不用 fetched_at。既有 8 種狀態回應測試通過；TI-C16-2 的對外文字不在本 Ticket |
| CL-R1-5 | 每方向使用呼叫者給的 positions，不由去程推導回程；motorcycle＋use_highways 0，不送硬性排除與高度，不重試；引擎沒有回應時停止後續請求。正常來回為 route／trace／route／trace／status |
| CL-R1-6、7、8、9 | road_names 依 maneuver 的 begin／street 名稱第一次出現順序去重；起訖到首末點、via 到線段最近點、沿線距離嚴格遞增；generic UA、顯式 HTTPS endpoint、無 env／log。CL-R1-8 非 200 訊號優先順序 **FAIL，R1-F1** |
| CL-R1-13、14 | ID 使用 R1-2 建構與對應 RS／SN 前綴，測試確認小寫 ASCII 十六進位及一對一尾碼；沒有新增接受任意 ID 的捷徑。`build_snapshot`／request_key 沿用既有唯一 canonical 規則；既有 rejection tests 亦全數通過 |
| CL-R1-17、19、21 | `source.py` 不捕捉選取的 SnapshotIntegrityError，只呼叫三個 selectors，沒有自己列目錄／exists 篩選；put 的 SnapshotStoreError／ConflictError 原樣傳出；無未存檔路線。測試包括壞檔、符合名稱的目錄、真實寫入失敗、例外不含路徑。200.04 m 原值拒收，199.96 m 可採用後存 199.9；座標轉 float，fetched_at 轉 +08:00 並截秒而不進位 |
| CL-R1-24 | target GPX 分支在 store／client／snapshot 檢查之前執行；原樣帶出 R1-3 的點序、長度、分界點、識別、實際 turnaround_m，road_names 空；不做 engine／snapshot／freeway／warnings／offset／order 處理。錯誤 code、case 與呼叫端例外傳出；相關測試及原始碼核對成立 |
| CL-R1-25 §2.3～2.6 | transport 僅頂層 http_transport.py；只用 http.client／ssl 進行網路操作；其他 routing 模組不 import 它。URL 自行 fullmatch，再檢主機、埠與三種路徑；無帳號／query／fragment／換行；無 redirect／proxy／set_tunnel／env reads；default TLS context；TIMEOUT_S = 30.0；無 retry；header 封閉清單；OSError／HTTPException 轉固定 TransportError 並 from None，finally close。T-1～T-10 全部通過；第 2.4 封閉清單與第 2.6 evidence 另見第 3、6 節 |
| CL-R1-27 | attribute reply 的 warnings 非空或非 list 時不可驗證；不存在／null／[] 不影響；同時有 motorway／國道名稱仍優先；不把 attribute warnings 放進 RouteLeg；status warnings 不影響採用。相關 12 案例通過；method v2 明寫無警告要求 |

**H-1（decision-20261117-high-risk-categories.md §5）**：自行檢查 diff、新來源、測試與 worklog，沒有憑證值或持有憑證的 header／log。`git ls-files` 僅作禁止樣式的計數，不輸出可能敏感檔名：`.env`（含變體）、`.key` 均為 0。端點轉址、proxy、TLS、timeout 的替身測試及 source inspection 通過。這個 client 沒有付費呼叫點，budget guard 不適用；未呼叫任何付費 API。

**H-2**：追蹤中的 `.gpx`、`.fit`、`data/raw/`／`data/private/`／`data/bmw/` 及全部 `data/` 路徑計數均為 0。沒有開啟、列出或搜尋 data 目錄。新增位置／形狀由 `at(x,y)` 在 0°N、0°E 附近換算，shape 由測試獨立 encoder 產生；GPX 與引擎回應手工合成，road names／版本／日期是 synthetic。沒有引入公開地標座標或真實軌跡。UA `route-client/1.0`；route wire body 只送 lat／lon／type 及固定參數，trace 只送引擎自己的 shape，status 為空物件；錯誤與 traceback 的合成座標／路徑標記檢查通過。隱私裁切／錨點代換沒有被修改，不在本 Ticket 自行新增；呼叫者位置是否公開仍由 G-RREQ／TI-C16-3 承接。真實資料的隱私與行為不作已驗證宣稱。

**H-4**：自行閱讀缺欄、無回應、HTTP 錯誤、非 JSON、malformed route／trace、warnings、缺 has_highway、2% 差異、起訖／via 偏移、順序反序／相等、壞快照、put 失敗、strict stop 等測試，均明確拒收或拋例外，沒有預設採用與過期快照回退。CL-R1-27 矛盾訊號案例亦通過；但「任何可讀回應先收集所有國道訊號」仍有 R1-F1 缺口，因此本類別不能整體記 PASS。Planner 改寫規則、計畫狀態、規則 5 畫面不是本次變更範圍，不以此 Ticket 宣稱已涵蓋。

## 6. 實際執行與 evidence sufficiency

所有命令均在本 worktree 內，以 PATH 上的 `python` 執行，未使用 `.venv` 路徑發起命令，未改動 `PYTEST_DEBUG_TEMPROOT`。`sys.executable` 的觀測為本 worktree 內的 Python，版本 3.11.2。

| 檢查／命令 | 實際結果 |
| --- | --- |
| `python -m pytest -q` | exit 0，**1918 passed in 47.74s** |
| `git status --short`（第一次全套測試後、第二次前） | 空輸出，clean |
| `python -m pytest -q -rxX` | exit 0，**1918 passed in 37.87s**；沒有 xfailed／xpassed／skipped |
| `rg -n 'xfail\|pytest\.mark\.skip\|pytest\.skip\|unittest\.skip' tests`（以 regex alternation 執行） | 0 命中，rg exit 1 為未找到；另以 AST 遍歷 tests 的 16 個 .py，xfail／skip／skipif attribute 清單為 `[]` |
| `git diff --check bc7024b..e1ef580` | exit 0 |
| `git ls-files -z` 經 stdin Python 封閉樣式計數 | env／key／gpx／fit／private_data／全部 data 路徑均 0；未讀取這些路徑的內容 |
| 逐 commit path 檢查；protected paths 空 diff；test function AST 比較；source docstring 以外 AST 比較 | 如第 3 節，均成立 |
| stdin `python -X utf8 -` 的單方向非 200 探測 | 三者都是 routing_unavailable、空 signals，見 R1-F1。最初一次探測誤將 mapping 直接傳給要求 Position 的 evaluate_direction，得到 AttributeError；改以 `position_from` 建構後成功重現。該 harness 輸入錯誤不作產品 finding |
| stdin `python -X utf8 -` 內呼叫 `pytest.main`，以記憶體 plugin 加入三個 get_route 契約反例 | exit 1，**3 failed in 0.10s**，詳見 R1-F1；不是修改追蹤中的測試，也不是全套既有測試失敗 |
| `git status --porcelain`（兩次全套測試、額外 probes 及所有檢查後，寫 record 前） | `''`，clean |

反例的可重現方法：stdin 匯入 `tests/test_routing_engine.py` 的 synthetic helpers；對來回行程分別令去程 route 回應為 `reply(route_body(OUT_POINTS, has_highway=True), 503)`，或去程 trace 為 `reply(trace_body(OUT_POINTS, road_class='motorway'), 503)`／`reply(trace_body(OUT_POINTS, names=('Freeway',)), 503)`，其餘方向使用正常合成回應。透過 `plan(engine, SnapshotStore(tmp_path))` 呼叫真正 shared interface，斷言無檔案、兩次 route 呼叫，再斷言 code 為 HIGHWAY_IN_ROUTE。記憶體 plugin 使用原測試 module 作為 collector parent，故原 autouse `no_network` fixture 生效，tmp_path 沿用本次 pytest 的 worktree 內 temp root。三例均在最後一個斷言失敗。

| Evidence 要求 | 獨立判斷 |
| --- | --- |
| E-1 | Worklog §10.4 確有 f6810d2 的完整 pytest 輸出，1918 passed；§6 保留舊 subject 1843 passed 的歷程。本次另兩次全套重跑通過，無 skip／xfail |
| E-2 | Worklog §6、§10.5 逐條列 S 編號／AC／clarifications 與測試；名稱與實際測試對應。但「國道訊號優先」coverage 不充分，新增反例失敗，必須依 R1-F1 修正並更新，不因對照表寫 PASS 就接受 |
| E-3 | 檢查新增 fixtures／helpers／diff／worklog 的 synthetic 來源一致；無真實軌跡、住家座標或新增需查來源的公開地標 |
| E-4 | FakeEngine、Scripted HTTPSConnection、Wire 的 in-memory socket 與 autouse socket 封鎖均核對；新 interpreter 的兩種 endpoint／proxy probes 也用替身，沒有真實請求。本次反例同樣封鎖網路 |
| E-5 | Worklog §10.5 詳列唯一既有測試函式改動的五個理由，引用 DA §2.2、§2.4；與 diff 相符。第 6 節「無」是 7cb4b0c 的歷程，最新節已補上，沒有誤認為最終 subject 未改測試 |
| E-6、CL-R1-25 §2.6 | Worklog §6、§10.6～10.8 有 H-1／H-2／H-4 self-verification、timeout 選值、分離 implementation／record commits、T-1～T-10、CL-R1-27、33 個 mutation dispositions 與還原聲明。測試可辨別所列 redirect／TLS／retry／exception／import／warning 變更，邊界 diff 符合要求。本次禁止修改 source，未重跑需改寫 source 的 mutation scripts；其歷史執行次數是 Executor record evidence，不冒充本次執行。H-4 仍因 R1-F1 不充分 |

## 7. NOT VERIFIED、routing 與既有 disposition

| ID | 未驗證／未執行事項與原因 | Required authority／owner |
| --- | --- | --- |
| NV-1 | 真實 Valhalla 的連線、TLS／redirect 實際行為、via 是否只回一個 leg、warnings 位置、trace/status response shape，以及 S39／S40 真實參考路線與詞彙表偏移：**NOT VERIFIED／NOT RUN**。本次明文禁止真實網路，CL-R1-1 與 CL-R1-25 §2.7 也排除。替身測試證明本地程式行為，不等於真實服務驗證 | acceptor；之後獲授權的整合 work item |
| NV-PRIVATE | 真實私有 GPX／保留行程的行為與來源隱私：**NOT VERIFIED**。沒有 RB-7 明確路徑授權，未嘗試取得。不是本 Ticket synthetic AC 的缺失 | acceptor |
| NV-BIND | 本次 Codex R1 的完整 rollout／runtime binding／record hash：**NOT VERIFIED by Reviewer**。受審 run record §6 最後為事件 91，本次 dispatch 尚未入檔。未讀 worktree 以外的 rollout。不得在正式採用時將此欄視為完成核對；應由 dispatcher 在本次 R1 事件填入 thread、全部 turn_context 的單一 model／effort／sandbox 集合、turn 數、存取範圍與 record SHA-256 | dispatcher／Orchestrator，Bindings §3.3；不需要 Reviewer 越界讀取 |
| NV-VERSION | Python 3.13 以後與真實失效符號連結的跨環境行為：本次 **NOT RUN**。本次使用 Python 3.11.2；#14 最終模組未改，沿用其版本無關邏輯與替身測試，不冒充其他版本的執行 | 之後的適用驗證；既有 DA disposition |

TI-C16-2（圖磚最後修改日期的對外文字）、TI-C16-3（G-RREQ 的 positions／request_key 一致性）沿用 DA 的 owner 與 disposition：**Design Authority**，本次沒有把它們記為已實作，也不重開 #14／#15。CL-R1-25 §8 列出的其他 TI／RV 與真實路線證據，留給各自的 derivation／整合／AB-12 工作；此 record 不作 SIA、phase acceptance 或 AB-1 端到端 PASS。

後續依治理 §4.4 由 Executor 對 R1-F1 作 targeted correction，取得新 subject 的 regression evidence，再派 R2 closure review；本 record 不修改任何來源或測試，不宣告 Ticket completion。

Verdict: BLOCKING
