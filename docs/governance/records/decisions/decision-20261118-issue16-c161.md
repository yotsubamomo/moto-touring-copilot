# Decision record — C-16-1：真實的 HTTPS 傳輸層屬於 R1-4（CL-R1-25）；C-16-2 `map_data_date` 的讀法（CL-R1-26）；C-16-4 道路屬性回應的警告（CL-R1-27）與其他 disposition；C-16-3 的 tracked item

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue16-c161`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 事件 89 之後）。問題來自 #16（SPEC-R1 R1-4）Executor 的 return `NEEDS_DA`：worklog `docs/governance/records/worklog/issue-16.md` 第 7 節 **C-16-1**（blocking）、C-16-2（請確認）、C-16-3（non-blocking）、C-16-4（DA 知悉） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-R1 v1（`derivation-spec-r1.md`）的 clarifications **CL-R1-25～CL-R1-27**，治理 §5.3 第 2 類。與 CL-R1-1～CL-R1-24 並列引用。CL-R1-25 是 R1-4 範圍 (a) 與 CL-R1-9 的 clarification；CL-R1-26 是 DD-R1-2 的 clarification；CL-R1-27 是 7.11 第 5 項第 (1) 款與第 7 項的 clarification。都不取代先前的條文 |
| Subject 基準 | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `58e811497d96300f36a8678d86fb212321242cf4`；#16 的 implementation subject `7cb4b0cabcccb6541f395f999fe5b43e1b905e91`（之後只有 record-only commit）；開始時 `git status --short` 為空。本 DA 在 HEAD 上執行 `.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider`：`1843 passed in 42.73s`，exit 0（只是本裁決的背景觀測，不是 #16 的 E-1） |
| 讀過的依據 | 治理 §1.2、§2.1、§2.4、§2.5、§3.3–§3.6、§3.8、§5.3；Bindings m3 第 2.2–2.6、3.2、5、7 節；OC-1 全文（§2.1、§2.3、§3.1 AB-1、AB-10、AB-13、§5 外部依賴）；`derivation-spec-r1.md` 全文；`decision-20261118-issue14-c141.md`（CL-R1-14～CL-R1-19）；`decision-20261118-issue14-qalt1.md`（CL-R1-20、CL-R1-21）；`decision-20261118-issue15-c151.md`（CL-R1-22～CL-R1-24）；`decision-20261117-high-risk-categories.md` 全文；`decision-20261117-oc1-first-run-derivation.md` 第 6 節 G-RREQ、G-RTE 列；Issue #16 原文（scratchpad `issue-16-body.md`，SHA-256 重算 `105fdc981b1087b60b419690168d205064853a1a41ccde4a6cb092b6ffa8ede1`，與派工所述及 run record 第 4 節相同）；worklog `issue-16.md` 全文；`docs/spec/SPEC-001-plan-schema.md` 4.14、7.11 全表；`DESIGN.md` §4.1 路線解析段、§5 外部資料表的路線引擎列、§9.1、§9.2 `routing` 列、§13.5 D2；`docs/cr/CR-01-appendix/checks_routing.md` 第 4 節開頭（C4 的引擎版本與圖資時間）、`lead_dispositions.md` L-3；`src/moto_copilot/routing/valhalla.py`、`adoption.py`、`source.py` 的相關段；`tests/test_routing_store.py` 第 505–546 行、`tests/test_routing_engine.py` 的 `no_network`、`NEW_MODULES` 與靜態測試；依 CL-R1-1 以 Read 閱讀 `experiments/cr01_checks/routing_client.py` 與 `routing_c4_snapshots.py` 的原始碼（沒有執行，沒有讀 `experiments/` 的其他檔案） |
| 資料 | 沒有讀取、列出或搜尋 `data/`；沒有執行 `experiments/`；沒有讀 `.env`；沒有呼叫 GitHub；沒有發出網路請求 |

本 record 撰寫時實際執行的探測（stdin，只讀標準函式庫，不連網，沒有寫入 repo；之後 `git status --short` 仍只有本 record）：

| 探測 | 結果（Python 3.11.2） |
| --- | --- |
| `inspect.getsource(http.client)` 是否含 `environ`、`getproxies`、`Location` | 三者皆 `False`：`http.client` 不讀環境變數中的代理，也不處理轉址 |
| `ssl.create_default_context()` | `check_hostname == True`、`verify_mode == 2`（`CERT_REQUIRED`） |
| `urllib.request.build_opener()` 的預設 handlers | 含 `HTTPRedirectHandler`（預設跟隨轉址）；`ProxyHandler` 在環境中有代理設定時才加入（本機目前沒有，所以未出現）。這是 `urllib.request` 的兩個轉向陷阱 |

---

## 1. 問題

1. **C-16-1（blocking）。** R1-4 範圍 (a) 是「公開 Valhalla 伺服器的 client（端點與識別依 CL-R1-9；傳輸層可替換，測試不連網）」。`7cb4b0c` 的 `ValhallaClient` 只接受呼叫者傳入的傳輸層，沒有實際送出 HTTP 請求的程式。原因：#14 的 `tests/test_routing_store.py::test_the_routing_package_imports_no_network_or_environment_modules` 對 `routing/` 的每一個頂層 `.py` 禁止 import `socket`、`http`、`urllib`、`requests`、`httpx`、`ssl`、`subprocess`，而 Executor 被禁止修改 #14 的測試。要裁決：真實傳輸層是否屬於 R1-4；若屬於，做法、可修改的檔案、H-1／H-2 的要求與 evidence。
2. **C-16-2。** `map_data_date` 取自狀態回應的 `tileset_last_modified` 是否正確，或應一律記 `null`。
3. **C-16-3。** R1-4 不檢查各方向的請求位置與 `request_key` 的地點是否對應。
4. **C-16-4。** 五處比字面更嚴或與字面讀法不同的做法，特別是「道路屬性回應的警告不算 7.11 第 7 項的警告」。

## 2. C-16-1 的裁決（CL-R1-25）

### 2.1 真實傳輸層屬於 R1-4

**判定：屬於 R1-4 範圍 (a)，不另立 Ticket，不採用 Executor 的做法 (iv)。** 依據：

1. **範圍 (a) 的字面。** 交付物是「公開 Valhalla 伺服器的 client」，並以「每個方向一次路線請求與一次道路屬性查詢」定義它的行為。不能向該伺服器送出請求的程式不是那個伺服器的 client。括號中的「傳輸層可替換，測試不連網」是對測試方式的限制：實際的傳輸層存在，測試以替身替換它；它不是把傳輸層排除在交付物之外。R1-3 的「CLI 的接線（之後的整合 Ticket）」是 derivation record 明文寫在「排除」欄的項目；R1-4 的「排除」欄沒有傳輸層，所以兩者不同類。
2. **H-1 的標示。** derivation record 把 R1-4 標為 H-1：「決定請求端點的方式……核對重點是端點不可被轉向」。轉址與環境變數中的代理是傳輸層才有的轉向途徑；若傳輸層不在 R1-4，這項 H-1 核對就沒有任何 Ticket 承擔，等於把一個已標示的高風險核對移出 audit 範圍（高風險 record 第 4 節第 2、3 項）。
3. **AB 的分配。** SPEC-R1 分配到 AB-1 的「『路線快照上的實際道路路線』的產生、檢查與保存能力」（第 7 節）。沒有真實傳輸層，產品的任何部分都無法產生實際道路路線，這項能力就沒有被任何 derived Spec 涵蓋；目前也沒有任何已 derive 的整合 Spec 可以承接（first-run derivation 第 6 節只列出 G-RREQ、G-RTE 等未 ready 的範圍）。DESIGN §9.1 末段也寫明路線引擎「以 HTTP 呼叫」，DESIGN §9.1 的 `routing` 列把路線引擎列為 `routing` 的一部分。
4. **課程要求「真正取得資料」。** 這是 `requirements_proposal.txt` 的基本要求之一（root `CLAUDE.md`「上位契約與判準」）。本裁決沒有新增任何 requirement 或 AC：它只是不讓 R1-4 已有的範圍 (a) 縮小。真正執行一次真實請求不在本裁決之內（第 2.6 節）。

做法 (iv) 會把範圍 (a) 的一部分移到一個尚不存在、沒有 owner 的 Ticket，同時讓第 2、3 點的 H-1 核對與 AB-1 的能力失去承載者；它不是本 DA 可以在不留缺口的情形下作的 derivation 修訂，所以不採用。

### 2.2 做法：(ii) 一個指名的傳輸模組，並收緊 #14 的測試

| 做法 | 判斷 |
| --- | --- |
| (i) 放進 `routing/` 的子套件，藉 `glob("*.py")` 不遞迴而不被掃到 | **不採用。** 這是利用測試的漏洞，讓測試照樣通過而不再證明它要證明的事（治理 §3.4：不得藉選擇測試方法改變驗證契約）。本裁決另要求把該測試改為遞迴掃描，封住這個漏洞 |
| (ii) 修改 #14 的測試，明定只有一個指名的傳輸模組可以 import 網路模組 | **採用**，範圍見第 2.4 節 |
| (iii) 放到 `routing/` 以外 | **不採用。** DESIGN §9.1 把路線引擎放在 `routing`；另開套件只為了避開一個測試，沒有設計上的理由，且同一條 H-1 核對要跨兩個套件 |
| (iv) 之後的整合 Ticket | **不採用**（第 2.1 節） |

**#14 的那個測試要證明什麼。** 它是 #14 worklog E-2 中「另加：快照與 `request_key` 的計算不需要網路」（R1-2 AC 的最後一句）的兩項證據之一；另一項是 `test_hashing_storage_and_selection_need_no_network`（執行期封鎖 socket）。R1-2 的 AC 只要求雜湊、存放與選取不需要網路，沒有要求整個 `routing` 套件永遠不含網路程式；「所有頂層模組都不得 import 網路模組」是 #14 Executor 為該 AC 選的證明方式，不是 SPEC-R1 的 invariant。R1-4 範圍 (a) 本來就需要網路程式，所以這個證明方式在 R1-4 加入 `routing/` 時必須改寫成「只有一個指名的模組可以，其他全部不可以」，這仍然證明 R1-2 的 AC，而且比原本更嚴（第 2.4 節第 2 項的遞迴掃描與引用限制）。

**這不重開 #14。** #14 已結案（run record 事件 80）。修改發生在 #16 的 subject 中，由 #16 的 R1 審查，並在 SPEC-R1 的 SIA 中以最終 subject 核對（第 5 節）。依治理 §3.8「審後變更需要相應驗證；可能影響原 review 結論者，由 Reviewer／Design Authority 判定必要後續」，本 DA 判定：修改不影響 #14 audit 的結論（被證明的 AC 不變，證明更嚴），不需要 #14 的新 cycle。

### 2.3 CL-R1-25：真實傳輸層的要求（R1-4；H-1、H-2、H-4）

**CL-R1-25（R1-4 範圍 (a)、CL-R1-9 的 clarification）。** R1-4 交付一個真實的 HTTPS 傳輸層，符合 `valhalla.py` 現有的 `Transport` 介面（`transport(url, body_bytes, headers) -> HttpResponse`；沒有回應時拋 `TransportError`），並提供一個建立「使用真實傳輸層、預設端點 `VALHALLA_ENDPOINT`」的 `ValhallaClient` 的方式，使之後的整合不需要自己寫網路程式。

1. **位置與依賴。** 傳輸層與上述建立方式只放在一個新模組 **`src/moto_copilot/routing/http_transport.py`**（頂層模組，不是子套件）。只使用標準函式庫的 `http.client.HTTPSConnection` 與 `ssl`；**不使用 `urllib.request`**（預設跟隨轉址，並在環境中有代理設定時使用代理，見本 record 開頭的探測），不使用 `requests`、`httpx` 或其他第三方套件，不修改 `pyproject.toml`。該模組可以 import `.valhalla` 的型別與常數。**`routing/` 中任何其他模組（含 `__init__.py`）都不 import `http_transport`**；需要真實傳輸層的呼叫者（之後的整合）明確 import `moto_copilot.routing.http_transport`。這使 `import moto_copilot.routing` 與雜湊、存放、選取、採用的程式都不載入任何網路模組。
2. **端點不可被轉向（H-1）。**
   - (a) **不跟隨轉址。** 每次呼叫恰好建立一個連線、送出一個請求；3xx 回應（含 `Location`）原樣以 `HttpResponse(status, body)` 回傳，不送第二個請求。Client 既有的處理把非 200 的路線回應記為 `engine_error`、道路屬性回應記為 `trace_failed`、狀態回應記為 `unreported`，所以 3xx 一律不被採用（H-4）。
   - (b) **不使用代理。** 不呼叫 `set_tunnel`，不讀任何環境變數；`HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`、`NO_PROXY`（大小寫皆然）與任何端點類的變數都不改變連線的主機與埠。
   - (c) **只連到 URL 指定的主機。** 傳輸層自己再檢查收到的 URL：只接受 `https://` 加主機（可帶埠）加路徑 `/route`、`/trace_attributes` 或 `/status`，不帶帳號、查詢字串、片段或換行；主機與埠的規則與 `valhalla.py` 的 `_ENDPOINT` 相同。不符合時在建立任何連線之前以 `ValueError` 拒絕（這是程式錯誤，不是引擎無回應）。連線的主機與埠只來自這個 URL。拆解 URL 不得 import `urllib`（第 2.4 節的測試仍禁止它）。
   - (d) **TLS 驗證不得關閉。** 使用 `ssl.create_default_context()` 建立的 context：`check_hostname` 為 `True`、`verify_mode` 為 `CERT_REQUIRED`；不提供關閉驗證或載入其他憑證的參數。（觀測，不是要求：在非 Windows 平台上，標準函式庫的預設信任來源可受 `SSL_CERT_FILE` 等環境變數影響；那是信任來源，不改變連線的主機，專案的執行平台是 Windows，本 record 不另列 tracked item。）
   - (e) **逾時。** 一個固定、有限、大於 0 的逾時（模組常數，值由 Executor 決定並記入 worklog），傳給 `HTTPSConnection`；不從環境或設定檔讀取。
3. **送出的內容與識別（H-2；CL-R1-9）。** 方法是 `POST`；本文是 client 給的位元組，原樣送出，不增減；header 只有 client 給的（`Content-Type`、`User-Agent`）加上 `http.client` 自動加入的 `Host`、`Content-Length`、`Accept-Encoding`。不送 cookie、認證資訊或任何其他 header。
4. **失敗（H-4；CL-R1-5、CL-R1-9）。** 不重試。連線、送出、取得回應或讀取本文時的任何 `OSError`（含逾時、連線被拒、`ssl.SSLError`）與 `http.client.HTTPException`（含 `RemoteDisconnected`、`IncompleteRead`）都轉成 `TransportError`，以 `from None` 拋出；訊息是固定的文字，不含請求本文、座標、折線或回應本文。連線在 `finally` 中關閉。HTTP 錯誤狀態（4xx、5xx）不是例外，原樣回傳狀態與本文，由 client 依既有規則處理。
5. **不 log、不 `print`、不寫檔**，不保留請求或回應。原始碼不含 `environ`、`getenv`。
6. **不改變的部分。** `valhalla.py` 的端點常數、User-Agent、請求本文、`ValhallaClient` 的介面與檢查、`adoption.py` 與 `source.py` 的取得順序都不因本項改變（CL-R1-27 另有對 `adoption.py` 的修改，第 4.5 節）。

### 2.4 可以修改的檔案（封閉清單；C-16-1、C-16-2、C-16-4 合計）

| # | 檔案 | 允許的修改 |
| --- | --- | --- |
| 1 | `src/moto_copilot/routing/http_transport.py`（新檔） | CL-R1-25 第 1～5 項 |
| 2 | `tests/test_routing_store.py` | **只改** `test_the_routing_package_imports_no_network_or_environment_modules` 一個函式：(a) 改為遞迴掃描 `routing/` 下所有 `.py`（`rglob`），使子套件不能繞過；(b) 只有路徑恰為 `routing/http_transport.py` 的檔案可以 import `http` 與 `ssl`，它仍不得 import `socket`、`urllib`、`requests`、`httpx`、`subprocess`；其他檔案照舊全部禁止；(c) 斷言 `http_transport.py` 存在（豁免不能指向不存在的檔案而默默失效）；(d) 斷言 `http_transport.py` 以外的檔案沒有引用 `http_transport`（含 `from .http_transport import …`、`from . import http_transport` 與絕對路徑的 import）；(e) `environ`／`getenv` 的禁止照舊適用於全部檔案，含 `http_transport.py`。函式名稱可以保留或改成反映新內容的名稱。該檔的其他測試不改 |
| 3 | `tests/test_routing_engine.py` 或新檔 `tests/test_routing_transport.py` | 第 2.5 節的傳輸層測試、第 4.5 節 CL-R1-27 的測試；`NEW_MODULES` 與 `test_the_new_modules_do_not_read_env_log_print_or_import_network_modules` 納入 `http_transport`，對它只放寬 `http`、`ssl` 兩項 |
| 4 | `src/moto_copilot/routing/adoption.py` | 只限 CL-R1-27（第 4.5 節）：道路屬性回應的警告、`FREEWAY_CHECK_METHOD` 的文字、模組說明中 7.11 第 7 項的描述 |
| 5 | `src/moto_copilot/routing/source.py` | 只限註解與 docstring：`_engine_info` 的 docstring 可以引用 CL-R1-26；`frozen_entries` 的說明可以引用第 4.4 節。行為不改 |
| 6 | `src/moto_copilot/routing/valhalla.py` | 只限模組說明中「Transport」一段：改寫為「真實傳輸層在 `http_transport.py`（CL-R1-25），本模組本身不開連線」。程式碼不改 |
| 7 | `docs/governance/records/worklog/issue-16.md` | 第 2.6 節的 evidence |

不得：修改 `canonical.py`、`request_key.py`、`snapshot.py`、`store.py`、`target_gpx.py`、`__init__.py`（第 1 項不需要匯出；`__init__.py` 不 import `http_transport`）、`contracts/`、`ingest/`、`tests/routing_synthetic.py`、`tests/test_routing_snapshot.py`、`tests/test_target_gpx.py`、`tests/test_routing_store.py` 中第 2 列以外的任何內容、`pyproject.toml`；加入任何 xfail／skip；發出任何網路請求。

### 2.5 傳輸層的測試（全部不連網）

測試以替身取代 `http_transport` 模組命名空間中的 `http.client.HTTPSConnection`（記錄建構參數、`request` 的方法、路徑、本文與 header、是否呼叫 `set_tunnel`，並依序回答）；`socket.socket`、`socket.create_connection`、`socket.getaddrinfo` 照 E-4 封鎖。

| # | 測試 | 要證明的事 |
| --- | --- | --- |
| T-1 | 轉址 | 301、302、303、307、308 各帶指向另一主機的 `Location`：回傳該狀態，只建立一個連線、只送一個請求，連線的主機仍是端點的主機。經 `get_route` 的一般模式：路線請求收到 302 時是 `routing_unavailable`，沒有快照 |
| T-2 | 代理與環境變數 | 在新的直譯器中設定 `HTTP_PROXY`、`HTTPS_PROXY`、`ALL_PROXY`、`NO_PROXY`（大小寫）與端點類變數（沿用 `test_h1_the_endpoint_is_not_affected_by_env_variables` 的作法），以真實傳輸層加替身連線送出：替身收到的主機與埠是 `VALHALLA_ENDPOINT` 的主機與 443（或預設埠），沒有 `set_tunnel` |
| T-3 | TLS | 傳給連線的 context `check_hostname` 是 `True`、`verify_mode` 是 `ssl.CERT_REQUIRED` |
| T-4 | 逾時 | 傳給連線的逾時是有限、大於 0 的值，等於模組常數；替身拋 `TimeoutError` 時是 `TransportError` |
| T-5 | 失敗的轉換 | 在建立連線、`request`、`getresponse`、`read` 各處拋 `OSError`、`ConnectionRefusedError`、`ssl.SSLError`、`http.client.RemoteDisconnected`、`http.client.IncompleteRead`：都是 `TransportError`、沒有第二次呼叫、連線被關閉；`traceback.format_exception` 的輸出不含合成座標的字串、不含請求本文 |
| T-6 | 內容與 header | 方法是 `POST`、路徑是 `/route`／`/trace_attributes`／`/status`、本文與 client 給的位元組相同、header 只有第 2.3 節第 3 項列出的項目 |
| T-7 | URL 的拒絕 | `http://`、帶帳號、帶查詢、帶片段、沒有路徑、其他路徑、結尾換行：在建立連線之前 `ValueError`（替身連線沒有被建構） |
| T-8 | HTTP 錯誤狀態 | 4xx、5xx 原樣回傳，不是例外 |
| T-9 | 建立方式 | 第 2.3 節開頭的建立方式得到的 `ValhallaClient` 端點是 `VALHALLA_ENDPOINT`，傳輸層是真實傳輸層；以它跑一次一般模式的來回行程（替身連線回答合成回應），結果與 `FakeEngine` 的同一情形相同 |
| T-10 | 靜態 | 第 2.4 節第 2、3 列修改後的兩個靜態測試 |

### 2.6 Evidence（記在 `worklog/issue-16.md`）

| # | 證據 | 要求 |
| --- | --- | --- |
| 1 | Commit | 一個與 `7cb4b0c` 分開的 implementation commit，只含第 2.4 節第 1～6 列的檔案，message 註明 CL-R1-25、CL-R1-27。它成為 #16 新的 implementation subject。worklog 另以 record-only commit |
| 2 | E-1 | 新 subject 上的完整 `.venv/Scripts/python.exe -m pytest -q` 輸出，exit 0，摘要只有 `passed` |
| 3 | E-2 | 範圍 (a) 與 AC「另加：端點不受環境變數影響」「請求的 User-Agent 與內容不含個人識別資訊」兩列加上 T-1～T-10；CL-R1-27 的列（第 4.5 節）；DD-R1-2 列改為引用 CL-R1-26 |
| 4 | E-4 | 寫明傳輸層測試以替身連線取代 `HTTPSConnection`，socket 照舊封鎖；沒有任何網路請求 |
| 5 | E-5 | 逐項列出 `tests/test_routing_store.py` 中那一個函式的修改與理由（引用本 record 第 2.2、2.4 節），並寫明 R1-2 AC「快照與 `request_key` 的計算不需要網路」仍由該測試與 `test_hashing_storage_and_selection_need_no_network` 證明 |
| 6 | E-6 H-1 | 第 2.3 節第 2 項 (a)～(e) 各對應的測試；worklog 第 6 節「真實傳輸層不存在（C-16-1）……NOT VERIFIED」改寫為以 T-1～T-4、T-7 證明；`git ls-files` 不含 `.env`、`*.key` |
| 7 | E-6 H-2 | T-5、T-6；diff 中的座標全部是合成值 |
| 8 | 突變 | 至少下列突變各被至少一個測試抓到：改用 `urllib.request.urlopen`；`check_hostname = False` 或 `CERT_NONE`；把 3xx 改成再送一次請求到 `Location`；加入一次重試；例外不加 `from None` 而把本文放進訊息；讓 `source.py` 或 `__init__.py` import `http_transport`；把 `http_transport.py` 移到子套件；忽略道路屬性回應的警告（CL-R1-27）。原始碼的還原方式與 `7cb4b0c` 時相同（記憶體中的原文寫回，結束時 SHA-256 相同） |
| 9 | Diff | 相對 `7cb4b0c` 的 diff 只含第 2.4 節列出的檔案與內容 |
| 10 | 真實請求 | **NOT RUN**。worklog NV-1 維持 NOT VERIFIED／NOT RUN（第 2.7 節） |

### 2.7 不在 R1-4 的部分

- **真實請求的執行**（對公開伺服器實際送出請求、五條參考路線、真實伺服器的回應形狀，worklog NV-1）：不在 R1-4，也不在 SPEC-R1。依據：CL-R1-1「本 Spec 的 AC 不需要任何真實的路線請求」；R1-4 的排除欄（S39、S40 的參考路線屬整合或詞彙表的驗收，RV-5）；送出的位置必須是公開地標（DESIGN §13.5 D2、NFR2），而地標座標來自尚未 derive 的詞彙表（G-RREQ、G-KB）。第一次真實請求屬於 AB-1 的端到端證據與之後的整合驗收；它在哪一個 work item、以什麼授權執行，由該 work item 的派工與 acceptor 的指示決定，本 record 不授權、也不要求它。
- 因此 SPEC-R1 結案時，「路線快照上的實際道路路線」的產生**能力**在 SPEC-R1 中具備（含真實傳輸層），但**實際取得**的證據仍是 NOT RUN；SIA 與 phase acceptance 不得把它記為已驗證，AB-1 在端到端證據存在前不得記為 PASS（OC-1 §3.2）。

## 3. C-16-2 的裁決（CL-R1-26）：確認 D-16-16

**CL-R1-26（DD-R1-2 的 clarification）。** `map_data_date` 取自路線引擎狀態回應的 `tileset_last_modified`（Unix 秒；非負整數、不是布林值）在 +08:00 的日期。沒有這個欄位、型別或範圍不符、狀態請求失敗或沒有回應時是 `null`，不以取得日期或其他資訊代替。

依據：
1. **它是引擎回報的值。** DD-R1-2 與 4.14 禁止的是以「取得日期」（我方的 `fetched_at`）代替，以及在引擎沒有回報時推測。`tileset_last_modified` 是引擎在狀態回應中回報、它目前使用的圖磚的最後修改時間；它不是我方的時間，也不是推測。
2. **專案先前就以這個欄位當作圖資時間。** C4 的參考原始碼（`routing_c4_snapshots.py` 第 103–104 行）從狀態回應取 `version` 與 `tileset_last_modified` 作為引擎資訊；C4 的紀錄（`checks_routing.md` 第 4 節）寫「引擎版本 3.9.1，圖資時間 2026-11-14（UTC）」。lead 的處置 L-3「快照另記引擎版本與圖資日期」與 SPEC-RESOLUTION-001（「快照的圖資日期顯示在來源證據，過期與否看得到」）都以這個值可以取得為前提。
3. **另一讀法的後果。** 「Valhalla 沒有回報圖資日期，一律 `null`」會讓 4.14 的欄位對唯一的引擎永遠是空的，使 SPEC-RESOLUTION-001 所說「過期與否看得到」無法成立；它不比本讀法更 fail closed（`map_data_date` 不參與任何採用的判定），只是丟掉引擎已回報的資訊。所以既有來源只有本讀法合理（治理 §3.6-A），不構成 E-DA/D1。
4. **+08:00。** SPEC-001 §2 的時間一律以 Asia/Taipei 表示；C4 紀錄的 UTC 日期是技術檢查的寫法，不是契約。

後果與限制：
- `map_data_date` 在 `snapshot_id` 的雜湊範圍內。伺服器重建圖磚之後，30 天後重新取得的同一條路線即使折線相同，也會是新的快照與新的 `route_id`。這符合 7.11 第 1 項「內容不同（折線或任何其他內容）：新的代號、新的檔案」，不影響一般模式的重用（以 `request_key` 比對）。目前沒有任何已存的快照，本裁決不影響既有資料。
- 用語：這個日期是「引擎回報的圖磚最後修改日期」。之後在來源證據（SPEC-001 第 715 行附近的 `version`）或介面上顯示時，不得把它說成 OpenStreetMap 資料的擷取日期，也不得說成圖資「已確認為最新」（TI-C16-2，第 6 節）。
- `source.py` 的 `_engine_info` 與 `test_dd_r1_2_engine_version_and_map_data_date` 已符合本裁決，**不需要修改程式或測試**；docstring 可以引用本 record（第 2.4 節第 5 列）。

## 4. C-16-4 的 disposition

### 4.1 `Freeway` 不分大小寫：接受

7.11 第 5 項第 (3) 款列的樣式是 `國道|高速公路|Freeway`。不分大小寫只會多抓到 `freeway`、`FREEWAY` 等寫法，任何多抓到的都是國道訊號，方向是 fail closed（修正 B）。`FREEWAY_CHECK_METHOD` 的文字已寫明「case-insensitive」，方法字串如實反映門檻。

### 4.2 `motorway` 只要出現就算：接受

第 (2) 款是「道路等級為 `motorway` 的里程是 0」。長度為 0（或讀不到長度而另記無法驗證）的 `motorway` 路段，是道路屬性說「這裡有國道等級的路段」而長度說「沒有里程」，屬訊號互相矛盾；修正 B 規定矛盾時 fail closed。S39 的「道路屬性含 `motorway` 路段時是 `fail`」也以出現陳述。

### 4.3 leg summary 的 `has_highway` 也算：接受

第 (4) 款是「引擎回報的 `has_highway` 是 `false`」，沒有限定是 trip 的 summary。leg summary 的旗標同樣是引擎回報的 `has_highway`；任一個為真就是國道訊號。trip summary 沒有布林值時記為沒有回報（無法驗證），非布林的真值另記為國道訊號，也接受（fail closed）。

### 4.4 凍結清單必須搭配 `snapshot_mode=True`：接受

7.11 第 3 項的狀態欄寫「指定了凍結清單就是嚴格模式」（lead 寫定的觸發方式）。`get_route` 在「給了凍結清單而 `snapshot_mode=False`」時以 `ValueError` 拒絕，不以一般模式執行、不呼叫引擎、不忽略清單。拒絕不是嚴格模式以外的任何取得方式，所以不違反「指定了清單就不經過一般的選擇」；它防止的是清單被默默忽略（fail open）。這是介面的 HOW。之後 E2 Runner 與凍結 Demo 的 Spec（TI-C14-5）以 `snapshot_mode=True` 加清單呼叫；該 Spec 若希望只給清單就進入嚴格模式，可以改成那樣，但不得改成忽略清單或以一般模式執行。

### 4.5 道路屬性回應的警告：**不接受**，改為 CL-R1-27

D-16-11 把 7.11 第 7 項的「回應」讀成只有路線回應，道路屬性查詢回應中的警告不影響採用。本 DA 判定這個讀法不符合 7.11 第 5、7 項與 H-4：

1. 第 7 項寫「回應出現任何警告就不採用」，沒有限定是哪一個回應；第 3 項 (c) 把「回應沒有警告」列為採用前的三項檢查之一，而道路屬性查詢是同一個採用判定中對同一個引擎送出的請求（第 3 項 (c)「再做道路屬性查詢（第 5 項）」）。
2. 第 7 項存在的理由是：引擎以警告表示它忽略了請求的一部分（C4 的「排除被忽略警告」）。道路屬性回應有警告，表示引擎可能忽略了查詢的一部分（例如過濾條件或比對方式），回傳的道路等級、名稱與長度是否完整就無法確立。第 5 項規定「沒有國道的訊號但無法驗證（查詢失敗……）時也不採用」；H-4 的最低核對範圍是「路線採用的檢查在訊號矛盾或無法驗證時不採用」。
3. 兩種讀法的後果：D-16-11 可能在國道檢查的資料不完整時記為 `pass` 並採用（fail open，而且在輸出上看不出來）；CL-R1-27 可能在公開伺服器對道路屬性查詢附帶無害的警告時使路線不被採用（可用性的損失，會以明確的 `routing_unavailable` 出現）。專案對採用條件的既定取捨是後者（修正 B、第 6 項「這一條沒有例外」、H-4）。所以既有來源可以裁決，不構成 E-DA/D1。若之後的真實請求（NV-1）顯示公開伺服器對道路屬性查詢固定附帶某種警告，放寬它要以該證據另行經 Design Authority 的 derivation，並改變 `freeway_check_method`。

**CL-R1-27（R1-4；7.11 第 5 項第 (1) 款與第 7 項的 clarification）。**
1. 道路屬性查詢的回應（HTTP 200、本文是物件）最上層有 `warnings` 而且它不是空清單（含不是清單的任何值），這次查詢就不算「成功」：這個方向的國道檢查**無法驗證**，不產生 `freeway_check` 的值，沒有國道訊號時是 `routing_unavailable`，不存快照。`warnings` 不存在、是 `null` 或空清單時沒有影響（與路線回應的處理一致）。
2. 同一個回應中的國道訊號（`motorway`、國道名稱）照樣收集；有任何國道訊號時仍是 `highway_in_route`（CL-R1-8 的優先順序）。
3. 道路屬性回應的警告不寫入 RouteLeg 的 `warnings`（4.14 的 `warnings` 是路線回應的警告；有警告的方向本來就不存檔）。
4. 狀態回應（`/status`）不是採用的檢查，它的警告不影響採用，只依 DD-R1-2／CL-R1-26 取版本與日期。
5. `FREEWAY_CHECK_METHOD` 的文字加上這個條件（例如「a road attribute reply without warnings」）。目前沒有任何已存的快照，改變字串不影響既有資料。
6. 測試（合成回應）：道路屬性回應帶一筆警告、多筆警告、非清單的 `warnings`（字串、物件）→ `routing_unavailable`、`freeway_check` 不產生值、沒有快照、請求次數不變；帶警告而且含 `motorway` 路段或國道名稱 → `highway_in_route`；空清單與 `null` → 不影響採用；來回行程只有回程的道路屬性回應有警告 → 整條不存檔。突變「忽略道路屬性回應的警告」被抓到（第 2.6 節第 8 項）。

## 5. C-16-3 的 disposition：tracked item TI-C16-3

R1-4 不檢查各方向的請求位置（`positions` 的代號與角色）與 `request_key` 的地點（`origin`、`destination`、`via`、`entry_ref_id`）是否對應，**維持**，不要求 #16 修改。理由：對應規則本身未定義——去程與回程的位置組成、目的地是公路時的進入端與另一端、回程是否經過進入端，都是 G-RREQ 的未 ready 內容（first-run derivation 第 6 節；7.11 第 2 項只寫「目的地、倒序的途經點、起點」）。R1-4 自行定一條對應檢查，就是在 G-RREQ 之前替它決定語義。CL-R1-5 已把位置定為呼叫者提供，CL-R1-2 把地點指紋定為只對呼叫者給的物件計算；兩者的一致由呼叫者負責是 SPEC-R1 的既有分工。

風險：呼叫者若給了不一致的兩者，快照會存在不對應的 `request_key` 下並被之後的規劃重用（H-4 的重用）。目前沒有任何呼叫者（G-RREQ 尚未實作），風險是潛在的。

| 代號 | 內容 | Owner |
| --- | --- | --- |
| **TI-C16-3** | G-RREQ（路線請求的解析）的 derivation 必須定義：各方向請求位置的組成規則，以及由哪一層、以什麼規則核對「位置的代號、角色、順序」與「`request_key` 的 `origin`、`destination`、`via`、`entry_ref_id`」一致；不一致時 fail closed（不送請求、不存快照）。在那之前，任何呼叫 `get_route` 一般模式的新程式都屬 G-RREQ 的範圍，不得在其 Spec 之前自行組成位置 | Design Authority（G-RREQ 的 derivation） |

在被接受並授權前只是 tracked item（治理 §1.2），不阻擋 #16。SPEC-R1 的 SIA 不得把它記為已涵蓋。

## 6. Tracked items 與文字同步

| 代號 | 內容 | Owner |
| --- | --- | --- |
| TI-C16-2 | 之後組裝來源證據（SPEC-001 的 `version`／`source`）或介面文字的 Spec：`map_data_date` 描述為「引擎回報的圖磚最後修改日期」，不得稱為 OpenStreetMap 資料的擷取日期或「已確認最新」的圖資 | Design Authority（整合 Spec 的 derivation） |
| TI-C16-3 | 第 5 節 | Design Authority（G-RREQ） |
| — | NV-1：真實伺服器的回應形狀（`via` 型態是否只回一個 leg、警告的位置、`trace_attributes` 的欄位、狀態回應的欄位）。第一次真實請求時核對；與 CL-R1-27 的放寬條件相連（第 4.5 節第 3 點） | 之後的整合驗收（第 2.7 節） |

文字同步（併入 first-run derivation 第 7 節的清單；不是任何裁決生效的條件；owner 與時機同 RV-6～RV-11：Design Authority，最早在 SPEC-R1 phase acceptance 之後，於 AB-12 的文件工作中執行）：

| 代號 | 位置 | 建議 |
| --- | --- | --- |
| RV-12 | SPEC-001 7.11 第 7 項 | 註明 CL-R1-27：道路屬性查詢回應的警告使國道檢查無法驗證 |
| RV-13 | SPEC-001 4.14 `map_data_date` | 註明 CL-R1-26：取自引擎狀態回應的圖磚最後修改時間，+08:00 的日期 |
| RV-14 | `DESIGN.md` §9.1 `routing` 列的「規劃位置」 | 標示已建立，並註明真實傳輸層在 `routing/http_transport.py`（CL-R1-25） |

## 7. 對 #16 的具體要求（同一 Ticket、cycle 1；R1 派工之前完成）

1. 依第 2.3～2.6 節實作 CL-R1-25 並取得 evidence；依第 4.5 節實作 CL-R1-27。
2. C-16-2 不需要修改（第 3 節）；C-16-3 不需要修改（第 5 節）；C-16-4 的第 4.1～4.4 節不需要修改。
3. Worklog：D-16-1 改寫為引用 CL-R1-25（真實傳輸層在 `http_transport.py`）；D-16-11 改寫為 CL-R1-27；D-16-16 引用 CL-R1-26；D-16-8、D-16-17 引用第 4.1～4.4 節；第 7 節 C-16-1～C-16-4 的狀態改為引用本 record，C-16-3 改為 TI-C16-3；第 9 節剩餘工作更新。
4. Executor 只修改第 2.4 節列出的檔案。若實作中發現第 2.3 節的任何一項無法以 `http.client` 滿足，停下並 route 至 Design Authority，不改用其他套件、不放寬要求。

**R1 的派工。** Orchestrator 派 #16 的 R1 時，派工內容須含本 record，以及 `decision-20261118-issue14-c141.md`、`decision-20261118-issue14-qalt1.md`、`decision-20261118-issue15-c151.md`（worklog 第 8 節已列）。R1 對 H-1 的核對（高風險 record 第 5 節「端點不可被環境變數或設定轉向」）包含第 2.3 節第 2 項 (a)～(e)；對 H-2 包含第 2.3 節第 3 項；對 H-4 包含 3xx 與傳輸失敗不被採用、CL-R1-27。R1 另須核對 `tests/test_routing_store.py` 的修改只限第 2.4 節第 2 列，並且沒有放寬對其他模組的禁止。不得把 `urllib.request`、子套件放置或「只交付可替換傳輸層」記為另一個可接受的實作。

## 8. 對 SPEC-R1 Spec Integration Audit 與之後 Specs 的影響

- **SR1-AC2**：共用介面的一般模式除了 `FakeEngine` 之外，另有以真實傳輸層加替身連線走通的路徑（T-9）；整合路徑上的 `route_id`、`snapshot_id` 規則不變。
- **SR1-AC3**：不採用的情形包含 3xx、傳輸失敗與 CL-R1-27 的道路屬性警告；國道訊號的優先順序在這些情形下仍成立。
- **SR1-AC4**：「測試全程沒有網路請求」涵蓋傳輸層的測試（替身連線、socket 封鎖）；「不含請求的座標」涵蓋傳輸層的例外（T-5）。R1-2 的 AC「快照與 `request_key` 的計算不需要網路」在最終 subject 上由修改後的靜態測試（遞迴、單一豁免、引用限制）與執行期的 socket 封鎖測試證明；SIA 以 #16 的最終 subject 核對這一點，因為 #14 的那個測試在 #16 中被修改。
- **SIA 不得記為已涵蓋**：真實請求的結果與真實伺服器的回應形狀（NV-1，NOT RUN）；五條參考路線；TI-C16-2、TI-C16-3；RV-12～RV-14；以及先前 records 已列出的 TI-C14-1、TI-C14-5、TI-C15-1、RV-6～RV-11。
- **AB**：SPEC-R1 分配到的 AB-1 部分（實際道路路線的產生、檢查與保存能力）因 CL-R1-25 而在 SPEC-R1 內完整；AB-1 本身的 PASS 仍需端到端的實際執行證據（OC-1 §3.2），不在 SPEC-R1。AB-10 的 NFR2（只送公開地標位置、通用的 User-Agent）在傳輸層由 T-6 證明，位置是否為公開地標由 G-RREQ 負責（TI-C16-3）。AB-13 不變。
- **之後的 Specs**：G-RREQ 處理 TI-C16-3；整合 Spec 處理 TI-C16-2，並以 `moto_copilot.routing.http_transport` 建立真實的 client；`routes`（G-RTE）以 R1-4 的共用介面為輸入，不受本 record 影響。

## 9. 是否改變 accepted 語義、boundary、authority、escalation

- **是否改變 accepted 語義：否。** CL-R1-25 是 R1-4 範圍 (a)「公開 Valhalla 伺服器的 client」與其 H-1 標示的直接讀法，不新增 Must、requirement 或 AC，也不恢復任何 Scope Reduction；它保持 SPEC-R1 已分配的 AB-1 部分不被縮小。修改 #14 的一個測試是證明方式的改寫，被證明的 R1-2 AC 不變。CL-R1-26 是 DD-R1-2 與 4.14 的唯一合理讀法；CL-R1-27 是 7.11 第 5、7 項在 fail closed 原則下的讀法，使採用條件更嚴而不是更寬。第 4.1～4.4 節接受的做法都是 fail closed 方向的 HOW。都屬治理 §5.3 第 2 類，不觸發 acceptor 核准。它們不建立其他工作依賴的新設計基線：`Transport` 介面、`ValhallaClient`、`get_route` 的形狀不變；`FREEWAY_CHECK_METHOD` 的字串改變發生在任何快照存檔之前。
- **Boundary：在 OC-1 boundary 內。** 全部屬 OC-1 §2.1 第 1 項（`routing`）、§2.3 的技術選擇（公開的 Valhalla 伺服器）與 SPEC-R1 已分配的 AB-1、AB-2、AB-10、AB-13 部分。真實請求的執行不在本 record 的授權之內（第 2.7 節）。
- **需要 acceptor：否**（本 record 的各項裁決）。第一次真實請求由之後負責它的 work item 依派工與 acceptor 的指示處理，不是本裁決的條件。
- **Escalation：沒有。** C-16-1、C-16-2、C-16-4 第 4.5 節都考慮過兩種以上的設計，但既有來源（範圍 (a) 與排除欄、H-1 標示、AB 的分配、C4 紀錄與 L-3、7.11 第 5～7 項、修正 B、H-4）足以裁決，不構成 E-DA/D1；沒有任何先前的 DA 決定被 FA ruling 或經 route 的 Reviewer finding 推翻或爭議，不構成 D2。

## 10. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #16（R1-4） | 依第 2、4.5、7 節修改；新的 implementation subject 取代 `7cb4b0c`。`7cb4b0c` 的 evidence（E-1 的 1843 passed、M1～M23 突變、E-3 合成資料）保留為歷程，在新 subject 上重新取得 E-1 並補第 2.6 節的項目。R1 尚未派工，所以這是 R1 之前的實作補足，不是 targeted correction |
| #14（R1-2，已結案） | `tests/test_routing_store.py` 的一個測試函式在 #16 中被修改（第 2.2、2.4 節）；#14 的 closure 與 audit 結論不變，不開新 cycle（治理 §3.8，本 DA 判定） |
| #15（R1-3，已結案） | 不受影響 |
| SPEC-R1 SIA 與 phase acceptance | 第 8 節 |
| 高風險類別 | R1-4 的標示（H-1、H-2、H-4）不變；本 record 界定其中 H-1 的傳輸層核對內容 |
| 之後的 Specs | G-RREQ（TI-C16-3）、整合 Spec（TI-C16-2、NV-1、RV-14） |

`derivation-spec-r1.md` 與先前的 CL records 沒有被修改；SPEC-R1 v1 的引用集合由本 record 補上 CL-R1-25～CL-R1-27。

Decision: C-16-1 — 真實的 HTTPS 傳輸層屬於 R1-4 範圍 (a)（CL-R1-25）：放在唯一的 `routing/http_transport.py`，只用 `http.client`＋`ssl`，不跟隨轉址、不用代理、不讀環境變數、TLS 驗證、固定逾時、不重試、例外不含內容；`tests/test_routing_store.py` 中那一個靜態測試改為遞迴掃描、單一豁免、禁止其他模組引用。C-16-2 — 確認 `tileset_last_modified` 的 +08:00 日期（CL-R1-26），不需修改。C-16-3 — TI-C16-3（G-RREQ）。C-16-4 — 4.1～4.4 接受；道路屬性回應的警告不接受，改為使國道檢查無法驗證（CL-R1-27）。不改變 accepted 語義；在 OC-1 boundary 內；不需要 acceptor；沒有 escalation。
