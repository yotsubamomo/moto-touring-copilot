# SPEC-R1 — Spec Integration Audit，cycle 1 R2

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，accepted commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-R1 v1（`decisions/derivation-spec-r1.md` §2、§4 DD-R1-1／2、CL-R1-1～10、§5 R1-1～4／E-1～6、§6 SR1-AC1～5 與 known-not-covered、§7 分配的 AB 部分）＋DA clarifications CL-R1-11～29 → Issues #13～#16 |
| Subject BASE | `1fd1de3585ea23f80842ac3276fe9305369b51e3` |
| Subject HEAD | `ca50bc9e2f2ec1aa635e6a59d21253b08f274d08`，本專用 worktree 的 detached HEAD |
| Audit kind | **Spec Integration Audit of SPEC-R1，R2 closure review，cycle 1；不是 Ticket audit** |
| Role | `primary_reviewer`（Codex） |
| 前次 subject／修正 | R1：`804362dc7b559867228eccbb289e22a055526bd2`；correction：`4cbc71bdc63f63e80a6295ada32b67ce2c5e5e77`；worklog：`df3e47e`；run record：`ca50bc9` |
| 日期／位置 | 2026-11-18，Asia/Taipei；`C:/Users/yotsu/AppData/Local/Temp/cxsiar1r2` |
| 結論 | **SIA-R1-F1 RESOLVED；沒有未解 blocking finding，沒有修正直接產生或暴露的新 blocking defect。** Formal binding 的外部核對仍由 dispatcher 完成，見 NV-BIND-R2。 |

本 Reviewer 自寫本 record；依本次派工使用末行 `Verdict:` 格式。本文中的 `R1 record` 指 `docs/governance/records/audit/spec-SPEC-R1-c1-r1.md`；`run` 指 `docs/governance/records/run/run-20261117-oc1-run2.md`；其餘相對記錄路徑以 `docs/governance/records/` 為根。Issue bodies 使用派工附錄原文，沒有呼叫 GitHub 或任何網路服務。

## Assurance

### (a) 四項 independence properties

| Property | 滿足方式與 evidence 界線 |
| --- | --- |
| Independent context | fresh Codex thread，未繼承 Executor 或 R1 Reviewer 的對話。自行重讀 R1 record、修正後檔案、diff、原始 validator／get_route 與測試 helper，從實際斷言及執行形成判斷。沒有委派 subagent。 |
| Verifiable binding | 依 Bindings m3 §3.3 O-6，由 dispatcher 核對本次 rollout 的全部 turn_context、model／effort／sandbox、存取路徑與作者事件，記入 run §6 的**本次「SPEC-R1 SIA cycle 1 R2／cxsiar1r2／HEAD ca50bc9」dispatch event**。目前 HEAD 的 run 最後編號是 **112**（`:190`）；本次 R2 dispatch event 尚未收錄，不能提供尚不存在的事件號。**110（`:188`）只證明 R1 binding，112 只證明 correction Executor，不代用為本次 binding**。正式採用本 record 前由 dispatcher 補登並核對，見 NV-BIND-R2；目前不宣稱四項 properties 的 binding evidence 已全部完成。 |
| Autonomous access | 本 worktree 內自行讀原始材料、git diff／history、執行 PATH 上的 Python 與 pytest；pack 是入口。沒有讀取、列出或搜尋 worktree 外路徑、私有資料或憑證；沒有執行 experiments。 |
| Self-written record | 本 Reviewer 建立本檔；唯一允許的非 ignored 增量。沒有改實作、測試、契約、worklog、其他 record 或 gates，沒有 stage／commit。dispatcher 依 O-6 核對唯一新檔、作者事件及原樣收錄 SHA-256。 |

### (b) Actual models 與 diversity

Correction Executor 的 dispatcher evidence 是 **run event 112，`:190`**：同一 `gov-executor`，agentId `a1e2cfa52290d496f`，全部 355 則 assistant 訊息觀測為 (`claude-opus-5-5`, `high`)。本次 Primary 是 **Codex**；Bindings 的 qualified mapping 為 `gpt-6.1-sol`／`high`，但本 HEAD 尚無本次實際 model id／effort／sandbox 的 dispatcher 核對。本 Reviewer 不讀 worktree 外 rollout，也不把預期 mapping 當成實際觀測。因此 **no model diversity claim**。前次 R1 的 NV-BIND 已有 event 110 補登；本次 NV-BIND-R2 是另一個待核對項目。

## R2 範圍與檢查

依治理 v2.2 §2.3、§3.8、§4.2～4.7、impl-default v2 §6～7、orch-default v2.2 §6～7、Bindings m3 §3.3／§5／§7 與 Reviewer definition，這次只判斷 F1 required fix、修正回歸、修正直接產生或暴露的 blocking defects，並確認既有 non-blocking disposition。沒有第二次全面 audit，沒有重開 Ticket finding，也沒有重新評估或關閉 allocation gaps。

實際重讀 root `CLAUDE.md`、Reviewer definition、Bindings、上述治理段落、R1 record 全文、SPEC-R1 §6／§7 與相關 Ticket 定義、OC-1 相關 boundary、CL-R1-22／24、修正 worklog、run 新增事件與相關紀錄；原始碼重點是 contracts schema／validator、routing/source.py 與新測試依賴的 engine helpers。未受修正影響的契約判斷與 high-risk coverage，明確承接 R1 record 下列五個範圍，不以重跑 suite 冒充重做全部原審查。

| 實際命令／檢查 | 結果 |
| --- | --- |
| `git rev-parse HEAD`；`git status --short` | HEAD 如表頭；起始 status 空白。 |
| `python -c "import sys, os; print(sys.executable); print(sys.version); print(os.environ.get('PYTEST_DEBUG_TEMPROOT'))"` | Python **3.11.2**；直譯器與 pytest temp root 均在本 worktree。只用 PATH 上的 `python` 啟動，沒有直接呼叫或讀取環境目錄；沒有覆寫 `PYTEST_DEBUG_TEMPROOT`。 |
| **`python -m pytest -q`** | **exit 0；2244 passed in 37.08s**。 |
| **`python -m pytest -q -rxX`** | **exit 0；2244 passed in 41.91s**。沒有 failed／error／xfail／xpass／skip 摘要。 |
| **`rg -n 'xfail\|skip' tests/`**；stdin Python AST 掃描 `tests/**/*.py` 的 Name／Attribute：xfail、skip、skipif、importorskip | 文字兩處：`test_contracts.py:1157` 的 docstring、`test_routing_store.py:330` 的名稱 `being_skipped`。AST markers **[]**，沒有 bypass。 |
| **`$env:PYTHONPATH='src'; python -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json`** | **exit 0**；data contracts **v0.3**；derived_segments、route_catalog、pace_table、eta_output 全部 **OK**。 |
| stdin Python `pytest.main(['-q','tests/test_integration_r1.py'], plugins=[AuditCalls()])`，以下說明呼叫觀測方式 | **exit 0；6 passed in 0.30s**；全部參數列確實執行真正的契約 validator，逐列結果如下表。 |
| `git log --oneline 1fd1de3..ca50bc9`；`git diff --stat 1fd1de3..ca50bc9 -- src tests`；stdin 取得 `git diff 1fd1de3..ca50bc9`，按 diff block 分析，再逐 commit 用 `git diff-tree --no-commit-id --name-only -r` 分類 | 89 commits：19 個 source／test commits、70 個 record-only commits。完整 diff 55 個檔案，其中 27 個 source／test／fixture 檔，**8054 insertions、25 deletions**。相較 R1 的 26 檔只增加新整合測試；原產品變更的審查承接 R1，不重新全面審查。 |
| `git log --oneline 804362d..ca50bc9`；`git diff --stat 804362d..ca50bc9`；`git diff --name-status 804362d..ca50bc9`；完整新測試 diff、run diff 與 worklog 閱讀 | 4 commits／4 檔：R1 audit、run、integration worklog、新測試。唯一非 record 檔是 `tests/test_integration_r1.py`（174 行），由 `4cbc71b` 新增。沒有修改任何既有測試。 |
| `git diff --exit-code 804362d..ca50bc9 -- src`；同區間對 `DESIGN.md README.md docs/spec .claude CLAUDE.md pyproject.toml app` 核對；`git diff 1fd1de3..ca50bc9 -- src/moto_copilot/routes/catalog.py` | 空 diff／exit 0；契約、產品與舊 catalog 都沒有 correction delta。BASE 起的 catalog 原 delta 仍僅 R1 已審的 CL-R1-12 說明與三鍵，不把合成 test catalog 當產品功能。 |
| `git diff --check 804362d..ca50bc9` | exit 0、空輸出。這不是宣稱 BASE 起所有歷史 records 的空白問題都已清理。 |
| stdin `git ls-files -z`，只比對 index 路徑字串並輸出計數 | `data/`、`.gpx`、`.fit`、檔名 `.env`、`.key` 各 **0**；沒有存取這些路徑內容。 |
| `Get-FileHash`；stdin 比對 R1 worktree bytes、LF-normalized bytes 與 `git show HEAD:<R1 record>` | 本機 checkout R1 有 205 個 CRLF；其 raw hash 為 `8f63f1c69c53a95bad957cf566e1682a48a838be9f099c123f6132d8791ab1a8`。轉 LF 後與 git blob 逐 byte 相同，SHA-256 **47193632ee493b3d86e5ecf3c07f88774f2231d49be03f928a676770b0ffafdf**，符合 event 110；沒有內容差異或改寫 R1。 |
| `Get-Content -Encoding UTF8`、指定檔案 `rg -n`、stdin AST／git probes | 用於原文、行號、helpers 與差異核對。初次 PowerShell 預設編碼顯示錯誤，已以 UTF-8 重讀；未以錯誤解碼內容判斷契約。 |

呼叫觀測 plugin 只在 targeted pytest 執行期間，以 proxy 包住**新測試模組**持有的 `validate_route_catalog` reference；proxy 呼叫原函式、原樣回傳 errors，只計數「空 errors／非空 errors」，於 teardown 恢復 reference 並斷言預期次數。沒有改檔、沒有替換 validator 結果、沒有修改產品 source。原生兩次 full suite 沒有使用此 plugin。

| pytest row | 真正 validator 的零違反次數 | 被拒案例次數 |
| --- | --- | --- |
| `test_the_catalog_check_rejects_a_broken_identity` | 1 | 3（不同 hex、錯誤來源、錯誤 checkpoint prefix） |
| `test_sr1_ac2_engine_routes_in_every_mode_carry_a_valid_contract_identity[round_trip]` | 4 | 0 |
| 同測試 `[one_way]` | 4 | 0 |
| `test_sr1_ac2_target_gpx_routes_carry_a_valid_contract_identity[one_way]` | 1 | 0 |
| 同測試 `[round_trip_detected]` | 1 | 0 |
| 同測試 `[round_trip_rider_between_points]` | 1 | 0 |

## Finding closure

### SIA-R1-F1 — RESOLVED

- **Severity：Medium／原 blocking；本次狀態 RESOLVED。Owner：SPEC-R1 整合 rework Executor。** 契約依據為 SPEC-R1 `derivation-spec-r1.md:145`，required fix 完整承接 R1 record `:158` 的 F1，不降低條件。
- **真實共用入口**：新測試 `:104` 起，兩種 trip type 的 first／reuse 經 `eng.plan`，其定義 `test_routing_engine.py:247` 明確呼叫真實 `get_route`；Snapshot／strict 直接呼叫 `get_route`（新測試 `:129`、`:136`）；GPX 三列同樣經共用入口（`:155`～`:174`）。不是只用手寫 IDs 代替整合結果。
- **契約串接**：`catalog_for`（`:53`～`:70`）原樣承載回傳的 route_id、route_source、snapshot_id、trip_type，source_trip_id 為 null；從該 route_id 組合 checkpoint_id，來回含 turnaround。`assert_contract_identity`（`:73`～`:88`）呼叫真正 `validate_route_catalog(...) == []`，再核對 ID patterns、checkpoint prefix、RS／SN hex、target_gpx_ref。validator（`src/moto_copilot/contracts/validate.py:187`、`:209`、`:267`、`:269`）實際執行來源參照 invariant 5、ID／source 格式、hex、turnaround invariant 4、前綴檢查。DD-R1-1 沒有新增 target_gpx 雜湊契約欄位；target_gpx_ref 是 route 結果上的獨立斷言，沒有偷偷擴張契約 2。
- **首次 store 與不發引擎請求**：first assert 每方向 route／trace_attributes 與 status 的確切序列、唯一 snapshot 檔、load 後 request_key／trip_type（`:108`～`:120`）；reuse 的 calls 是空且結果相等（`:123`～`:126`）。Snapshot／strict 的 transport 被呼叫就丟 AssertionError，strict 列含 request_key、snapshot_id、實際 file SHA-256；各結果都經 validator，末尾仍只有一個 snapshot（`:128`～`:142`）。
- **GPX 與兩點間 rider turnaround**：`:146`～`:152` 計算落兩點之間、距所有現有累計位置逾 1 m 的指定位置；`:160`～`:172` 經真實 R1-3 與 R1-4，比對 route_id／ref／實際 turnaround_m／source／原序 points，rider 列斷言採用值不是指定 m，兩方向共用分界點。Untouchable store 與 refusing transport 保證不走 snapshot／engine，目錄空白。符合 CL-R1-22／24 的既有規則；沒有以新 test catalog 定義 G-RTE。
- **每列都驗證、斷言非空殼**：五個真正 route 參數列有上述 **11 次零違反 validator calls**；另有 1 次手寫有效 identity 與 3 次被拒的負向 guard。AST 確認五個 call sites 在 `:120`、`:126`、`:131`、`:139`、`:174`，無 bypass，原生 suite 全數通過。
- **Required fix disposition**：所需 pytest evidence 與 worklog 已具備；full suite／CLI 已獨立重跑。F1 所有要求已滿足，沒有剩餘 F1 修正。Executor worklog 的五種 mutation 是其 self-verification；本次未讀外部 scratchpad 或重跑突變，不以該主張作獨立執行證據。

### SIA-R1-N1 — RESOLVED（紀錄缺漏）；平台 verification 仍 open

**Severity：Low／non-blocking。** R1 record `:166`～`:171` 所要求的 owner、scope authority、evidence 建立位置，已在 **run event 111，`:189`** 補登：合併 #14 NV-PY313／#16 NV-PY；owner＝**Orchestrator**（routing／紀錄），required authority＝**Design Authority**（確認 `requires-python >=3.11` 的支援與驗證範圍；本地 `pyproject.toml:9` 確有該宣告），evidence 建立於後續平台驗證 work item 的 worklog。此項紀錄修正已滿足 required fix，不要求本 cycle 安裝或測其他 Python。實際 3.13+／其他平台維持 **NOT RUN**，後續執行者由合法派工具名。只有需要變更環境權限時才 route acceptor。integration worklog §8 仍寫「補登不在本次」，是 Executor 記錄時點，不能覆寫其後 run event 111 的已補登事實。

### SIA-R1-G01～G13 — 沿原 disposition 保留 OPEN

下表只確認既有 routing，不重評 finding、分配或 required fix。**共同 severity＝Medium／non-blocking（設計 routing signal），owner／required authority＝Design Authority；Orchestrator 負責派工。Required fix 沿 R1 各原列的 DA determination／後續 derivation 與 evidence 安排，涉及 acceptor 保留權限時仍交 acceptor。** R1 record `:132`～`:155` 的原判斷、各列證據及限制，已由 run event 110（`:188`）收錄；未見任何取代 disposition 的 correction。沒有把本次 F1 closure 當成缺口已補齊。

| Finding | 沿用的原 finding／required fix evidence | Disposition／owner |
| --- | --- | --- |
| SIA-R1-G01 | R1 record `:140` | OPEN；DA routing 保留 |
| SIA-R1-G02 | R1 record `:141` | OPEN；DA routing 保留 |
| SIA-R1-G03 | R1 record `:142` | OPEN；DA routing 保留 |
| SIA-R1-G04 | R1 record `:143` | OPEN；DA routing 保留 |
| SIA-R1-G05 | R1 record `:144` | OPEN；DA routing 保留 |
| SIA-R1-G06 | R1 record `:145` | OPEN；DA routing 保留 |
| SIA-R1-G07 | R1 record `:146` | OPEN；DA routing 保留 |
| SIA-R1-G08 | R1 record `:147` | OPEN；DA routing 保留 |
| SIA-R1-G09 | R1 record `:148` | OPEN；DA routing 保留 |
| SIA-R1-G10 | R1 record `:149` | OPEN；DA routing 保留 |
| SIA-R1-G11 | R1 record `:150` | OPEN；DA routing 保留 |
| SIA-R1-G12 | R1 record `:151` | OPEN；DA routing 保留 |
| SIA-R1-G13 | R1 record `:152` | OPEN；DA routing 保留 |

這裡的 routing 是既有紀錄指定 authority；本次沒有向 DA 發送訊息或執行外部派工，也不宣稱 DA 已收到新的 assignment 或完成 determination。這些 non-blocking findings 不延長 cycle；其存在仍使 OC-1 整體 boundary 不能宣告完成。

## 五個 §4.7 範圍在 closure 後的狀態

| 範圍 | R2 結論與 evidence |
| --- | --- |
| 1. 跨 Ticket invariants | F1 對 R1-1 ↔ R1-2／3／4 的 identity／reference／checkpoint 契約鏈缺口已補，以上每模式／每列真實驗證成立。其他 identity 正規化、選取與停止、target passthrough、CL-R1-25 的 invariants，承接 **R1 record `:64`～`:72`**；產品無 delta，原測試全數重跑通過。 |
| 2. Spec-level AC coverage 與所分配 AB | 五條 AC 如下表。AB-2 的契約整合 evidence 缺口已消除。AB-1 仍限產生／檢查／保存能力，AB-10 仍限本層，AB-11 仍限 strict 機制；承接 **R1 record `:99`～`:107`** 的其餘判斷。AB-13 的 pytest 與本次技術 SIA closure evidence 已具備，formal binding 尚須 dispatcher 補核，**DA phase acceptance 尚未執行**，所以 AB-13 分配部分尚未全部完成。Spec AC 整體的既有 allocation mapping 沒有被改寫。 |
| 3. 整合行為 | correction 新增首次 store／reuse／Snapshot／strict／target GPX 與契約的連線；全部通過。其他整合失敗路徑與 H-1～H-4 最低核對結論承接 **R1 record `:109`～`:118`**，由完整 suite 回歸；只新增合成資料測試、封鎖 sockets／DNS、使用 transport doubles，沒有引入新產品 I/O、採用規則或宣稱。 |
| 4. 最終 subject verification／audit coverage | **ca50bc9** 上兩次完整 suite、CLI 與 targeted instrumented check 均已獨立執行。R1 原 source coverage（**R1 record `:120`～`:124`**）加本次唯一 test delta 的 scoped review，涵蓋目前整合 subject；不拿舊版本 pytest 代替本 HEAD。未發現 regression 或 correction 直接暴露的 blocking defect。 |
| 5. Traceability／boundary 與累積分配 | correction 明確只對 SR1-AC2／SIA-R1-F1，沒有改契約、Must、產品 catalog、Plan Schema 或保留權限；traceability 承接 **R1 record `:126`～`:155`**。SPEC-B1＋SPEC-UI0＋SPEC-R1 合計未覆蓋全部 OC-1 boundary 的原結論不變；G01～G13 均維持 open、DA routing，不重新評估、不因本 PASS 解除。 |

| Spec AC | Closure 後 status | Evidence／界線 |
| --- | --- | --- |
| SR1-AC1 | **PASS** | 承接 R1 record `:80`、`:86`～`:95` 的四票 closure／E-1～6／run §8.1 核對。correction 未改 Tickets 或其實作，suite 無 bypass；不重開原結案。 |
| SR1-AC2 | **PASS** | 本次 F1 closure：新測試的所有模式與 GPX 列、實際 validator calls、首次存放／無引擎重用與選取、checkpoint prefix／來源參照／RS-SN hex 全部有獨立執行 evidence。 |
| SR1-AC3 | **PASS（本 Spec 的合成路線層）** | 承接 R1 record `:82`；產品無 delta，拒收／錯誤路徑 tests 在 full suite 回歸通過；沒有擴張為所有可能輸入的窮舉證明。 |
| SR1-AC4 | **PASS（依已分配層級）** | 承接 R1 record `:83`；新增測試 `:41`～`:48` 封鎖 socket／連線／DNS，FakeEngine／refusing transport 不連網，GPX 為 bytes 及合成幾何；沒有新增產品 logging 或外送路徑。內部 AdoptedRoute／snapshot 幾何不等於 PlanResult／LLM 輸出，後者仍未分配。 |
| SR1-AC5 | **PASS** | 承接 R1 record `:84`；新測試及 worklog 沒有把 synthetic results／heuristic 當真實驗證，沒有改道路來源或研究宣稱。 |

## NOT VERIFIED、NOT RUN 與保留事項

| Item | 理由與狀態 | Owner／required authority |
| --- | --- | --- |
| NV-BIND-R2 | **NOT VERIFIED，正式採用前必要**：本 HEAD 沒有本次 R2 dispatch／binding event。不得以 event 110 或 112 代用。 | **dispatcher／Orchestrator** 補登本次 thread、全部 turn_context 集合、存取／唯一新檔／作者事件、原樣收錄 SHA-256，依 O-6 判斷有效性。本 Reviewer 不讀外部 rollout。 |
| NV-1／RV-5 | 真實 Valhalla／TLS／redirect／server response、五條參考路線與詞彙表偏移 **NOT RUN／NOT VERIFIED**，本次禁止任何網路。 | **acceptor**；之後合法整合 work item 執行，承接 R1 record `:193`。 |
| NV-PRIV／NV-PRIVATE | 真實 GPX／holdout／位置／部署 store 路徑／heuristic 真實表現／裁切與錨點外送 **NOT VERIFIED**；沒有取得資料。 | **acceptor RB-7**，承接 R1 record `:194`。 |
| NV-PY313／NV-PY；NV-SYMLINK | Python 3.13+／其他平台、真實失效或循環連結 **NOT RUN**；只執行目前 3.11.2。N1 解決只指具名承接。 | **Orchestrator** routing／後續受派 Executor，scope **DA**；需環境權限變更才交 acceptor。承接 R1 record `:186`～`:187`，更新以 event 111 為準。 |
| TI-C2R1F3-1 | SSL_CERT_FILE／SSL_CERT_DIR 信任來源限制不變；**OPENSSL_CONF 影響 NOT VERIFIED**。correction 沒改 transport。 | **DA**，沿 R1 record tracked items，不宣稱完全不受環境變數影響。 |
| NV-MUT | 外部 scratchpad mutation logs **NOT VERIFIED／未重跑**；worklog 的五項 KILLED 仍是 Executor evidence。 | 本 Reviewer 清楚限定獨立 evidence 範圍；本次無 source mutation，不新增後續要求。 |
| 其他原 tracked items | R1 record `:173`～`:197` 的歷史存取／experiments、C-14-6 座標處置、契約／文件／UI／上游輸入／E2 等 follow-up，全部沿原 owner／authority／NOT VERIFIED disposition，未因 test-only correction 解除。 | 沿原逐列 authority：dispatcher／Orchestrator、DA 或 acceptor；不另創授權或冒稱已派工。 |

SPEC-R1 §6 known-not-covered **逐項保留**：真實參考路線、詞彙表、路線請求解析、產品路線目錄／檢查點產生／ridden_share_pct、RouteSummary、RouteError 文字。另保留 CL-R1-22 §2.4 的稀疏點偏移及整數公尺 identity 限制、TI-C15-1／RV-11、CLI／UI／PlanResult／LLM 整合、凍結清單格式／E2 Runner。合成測試 checkpoint 是 identity carrier，不是這些項目的 implementation evidence。

本 record 的 PASS 表示本次 scoped closure review 無未解 blocking；不作 DA phase acceptance、OC-1 completion、run completion 或 release 決定。正式使用仍須 dispatcher 完成本次 binding；G01～G13 與所有 acceptor 保留事項依原 authority 承接。

交付核對：`git status --short` 只有 `?? docs/governance/records/audit/spec-SPEC-R1-c1-r2.md`；`git diff --exit-code` 為 exit 0，沒有追蹤檔變更。stdin Python 檢查五個 scopes、SR1-AC1～5、G01～G13、NV-BIND-R2、UTF-8／LF 與末行 verdict 均成立；record 的 SHA-256 另由工具輸出供 dispatcher 原樣收錄核對。

Verdict: PASS
