# Issue #9 — cycle 1 Alternate Independent Review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md` 的 #9 列、CL-B1-1、CL-B1-3、CL-B1-7）→ GitHub Issue #9「B1-2 `ingest`」 |
| 適用 clarification 與 decision | CL-B1-8（`decision-20261117-issue7-spike-tests.md`）、CL-B1-9、CL-B1-10（`decision-20261117-issue9-e1-and-trim.md`）、高風險類別（`decision-20261117-high-risk-categories.md` §5；#9 標示 H-2、H-3、H-4） |
| Issue 版本 | Pack 所附原文，本 reviewer 實測 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895`，等於 BD-3 的 #9 列。沒有連線查核遠端現況 |
| Subject | `09d150f0f7db34b3f46790a54e167b7f617a2fac`（branch `oc1-run2-b1-ui0-r1-routing`；BASE `0c109aaba8c8460cebea5336840cc1d556d88a71`）。實作 commit `a281cb0`、`b4d1f84`，correction `6f97561`；其餘 commit 只改 `docs/governance/records/**`（已用 `git log --name-only 0c109aa..09d150f` 核對）。主 checkout 的 HEAD `99e2e5e` 相對 subject 只多 record-only delta |
| Audit kind | **Alternate Independent Review，cycle 1**（治理 §4.4；本 cycle 唯一一次）。不是 R1／R3，不是 Spec Integration Audit，不是 Final Adjudication |
| Role | `alternate_reviewer`（`gov-alternate-reviewer`） |
| 日期／治理 | 2026-11-17；Minimal Operational Governance v2.2、Bindings m3 |
| 前序 records | R1 `docs/governance/records/audit/issue-9-c1-r1.md`、R2 `docs/governance/records/audit/issue-9-c1-r2.md`（Primary＝Codex）；worklog `docs/governance/records/worklog/issue-9.md`。三者的結論都當成待驗證主張 |

## Assurance

### (a) Context independence（治理 §2.3 的四項 properties）

| Property | 滿足方式 |
| --- | --- |
| Independent context | 本次是 fresh 的 `gov-alternate-reviewer` subagent，沒有繼承 Executor、Primary Reviewer 或 Orchestrator 的對話。Pack 只有路徑與識別。R1、R2 record 與 worklog 第 10 節由本 reviewer 自行從磁碟讀取；其中每一項本 record 採用的事實都另行重現或重讀原始檔 |
| Verifiable binding | Definition 的 frontmatter 是 `claude-fable-5-2`／`high`（Bindings §3.1，O-5）。本 reviewer 無法自證全部 assistant 訊息的實際 (model, effort)；依 Bindings §3.6，由派工者在採用本 return 前核對 transcript 並記入 run record `docs/governance/records/run/run-20261117-oc1-run2.md` §6 **事件 11**（本 reviewer 讀到時為「進行中」）。見 NV-2 |
| Autonomous access | 自行讀取契約、原始碼、diff、git 歷史；在 subject 的 detached worktree（`C:/Users/yotsu/AppData/Local/Temp/cx9r2`）以主 checkout 的 `.venv` 執行 pytest；另在 session scratchpad 以合成檔執行自己寫的重現程式與 mutation 檢查。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/`，沒有使用網路，沒有從 repo root 搜尋 |
| Self-written record | 本 record 由本 reviewer 以 Write 工具直接寫入。沒有修改實作、測試、契約、gates 或其他紀錄，沒有 stage／commit。Worktree 在審查前後的 `git status --short --ignored` 相同（只有 R2 record 未追蹤與既有的已忽略 `.pytest_cache/`）；本 reviewer 的 pytest 以 `-p no:cacheprovider --basetemp=<scratchpad>` 執行，沒有在 worktree 寫入任何檔案 |

### (b) 實際 model

| 角色 | 實際 model（證據） |
| --- | --- |
| Executor | `claude-opus-5-5`／`high`（run record §6 事件 2、7、9：agentId `a6f915a1860417bc9`，99、118、143 則） |
| Primary Reviewer（R1、R2） | Codex `gpt-6.1-sol`／`high`（run record §6 事件 8、10 的 rollout 核對） |
| Alternate Reviewer（本 review） | 有效 mapping `claude-fable-5-2`／`high`；實際觀測由派工者記入事件 11（NV-2） |

三者依紀錄不是同一個 model。Bindings §5 沒有宣告任何 diversity 關係，本 record 只記載上述事實，**不主張 model diversity**。上表引用的是派工者的核對紀錄，本 reviewer 沒有獨立讀取 transcript 或 rollout（NV-3）。

## 判斷摘要

| Finding | 原判定 | 本 reviewer 的判斷 | Blocking |
| --- | --- | --- | --- |
| R1-F1（R1 所證的三個重現與大小寫等價） | High／blocking | **已解決**（就 R1 record 所重現的情形與其 required fix 的各項） | — |
| R2-F1（R1-F1 同一 root cause 的殘餘：預設資料串流名稱） | High／blocking | **有效，未解決**。屬 implementation defect，不是 design issue。Blocking 判定成立；severity 本 reviewer 評為 Medium（理由見下），不影響 blocking | **是** |
| R1-F2 | Low／non-blocking | 已解決（同意 R2） | 否 |
| 連結與內容相同的不同檔名（worklog C-9-5b 的一部分） | Executor 記為殘餘，R2 未處置 | **不屬於 R2-F1 的 blocking 範圍**；是契約語義問題，required authority = Design Authority | 否（routing signal，治理 §4.2） |

## R1-F1 — 已解決（就 R1 所證範圍）

R1 的 required fix 有四項：開啟任何 GPX 前驗證來源與角色一致性；至少拒絕同一來源檔名的 pace／非 pace 矛盾並涵蓋大小寫等價；自動與明確選擇都補 regression tests 並以 open 事件作證；更新 worklog 的 H-2／H-3 主張。

- **程式**：`src/moto_copilot/ingest/__main__.py:58` 在 `load_manifest` 內呼叫 `_refuse_conflicting_roles`（`:74`–`:84`），早於 `select_pace_trips`（`:121`）與任何 GPX 的開啟（`:138`）。
- **重現**（本 reviewer 自寫，真實 CLI，沒有 mock；合成 GPX 與合成清單寫在 scratchpad）：

```text
R1 same name / holdout auto      pace='pace_a.gpx' other='pace_a.gpx' role=holdout  req=None      exit=2 gpx_opened=[] rows=None
R1 same name / holdout explicit  pace='pace_a.gpx' other='pace_a.gpx' role=holdout  req=['T901']  exit=2 gpx_opened=[] rows=None
R1 same name / excluded auto     pace='pace_a.gpx' other='pace_a.gpx' role=excluded req=None      exit=2 gpx_opened=[] rows=None
R1 case variant                  pace='PACE_A.GPX' other='pace_a.gpx' role=holdout  req=None      exit=2 gpx_opened=[] rows=None
     refused: the trip manifest gives the same source file a pace role and another role: T901 (pace) and T902
```

- **Regression tests 有鑑別力**（R2 的 NV-3 由本 reviewer 補做）：把 subject 的 `src`、`tests`、`pyproject.toml` 以 `git archive 09d150f` 匯出到 scratchpad，在副本上變異後跑 `tests/test_ingest_cli.py`。未變異 `26 passed`；拿掉 `:58` 的呼叫 → `11 failed, 15 passed`（10 個參數化案例與 `test_the_conflict_is_reported_by_trip_id_and_found_by_load_manifest`）；`source_key` 改為不忽略大小寫與結尾字元 → `5 failed, 21 passed`。與 worklog §10.1 的主張一致。受審檔案沒有被修改。
- **回歸**：在 worktree 執行 `python -m pytest -q -rxX` → `265 passed, 4 xfailed`，exit 0，四個 xfail 的 reason 是 `restored by #10`（1 個）與 `restored by #11`（3 個）；`--runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py` → `4 failed, 67 passed`，失敗的恰好是那四個。`tests/` 的 `xfail|skip` 只有 `test_routes_pace_eta.py:117`、`:159`、`:173`、`:182`。Correction 只改 `ingest/__main__.py` 與 `tests/test_ingest_cli.py`（`git diff 3ddbe9f..6f97561 --stat`：89 insertions、2 deletions）。

R2 把 R1-F1 記為 NOT RESOLVED，依據是 R2-F1。本 reviewer 把兩者分開記：R1 所證的情形已關閉；同一 root cause 還有未關閉的部分，以 R2-F1 識別。

## R2-F1 — 有效，未解決，blocking

### 事實：已獨立重現

真實 `load_manifest`、selection、GPX parser、`build_rows` 與 validators，清單是實際寫到磁碟的 JSON，輸出是實際寫出的檔案；以 audit hook 觀察 GPX 資料夾內的 open 事件。`samefile` 是 `os.path.samefile` 對兩個名稱的結果。

```text
R2 ::$DATA on pace entry      pace='pace_a.gpx::$DATA' other='pace_a.gpx'        role=holdout  req=None     exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$DATA on pace entry      pace='pace_a.gpx::$DATA' other='pace_a.gpx'        role=holdout  req=['T901'] exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$DATA on pace entry      pace='pace_a.gpx::$DATA' other='pace_a.gpx'        role=excluded req=None     exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$DATA on pace entry      pace='pace_a.gpx::$DATA' other='pace_a.gpx'        role=excluded req=['T901'] exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$data lower case         pace='pace_a.gpx::$data' other='pace_a.gpx'        role=holdout  req=None     exit=0 gpx_opened=['pace_a.gpx::$data'] rows=8 samefile=True
R2 ::$DATA on non-pace entry  pace='pace_a.gpx'        other='pace_a.gpx::$DATA' role=holdout  req=None     exit=0 gpx_opened=['pace_a.gpx']        rows=8 samefile=True
stream name alone (no clash)  pace='pace_a.gpx::$DATA' other=None                                           exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8
```

R2 的四個重現全部成立。本 reviewer 另確認兩點 R2 沒有列出的情形：串流寫法放在**非 pace 項目**那一邊時同樣繞過（第 6 列）；`:131` 的「plain file name」檢查不拒絕串流寫法（第 7 列）。每一例的輸出都印出 `non-pace entries not opened: 1`，與實際開啟的檔案不符。

### 同一 root cause 的另一個成員：8.3 短檔名（R2 未審）

Root cause 是 `source_key`（`:62`–`:71`）的等價關係比 `:134`–`:138` 開檔時作業系統接受的名稱寬鬆程度更窄：程式會開啟一個它沒有比對過的拼法。這不只限於串流語法。

```text
8.3 short name on pace entry  pace='PACE_L~1.GPX' other='pace_long_named_trip_a.gpx' role=holdout req=None exit=0 gpx_opened=['PACE_L~1.GPX'] rows=8 samefile=True
```

`PACE_L~1.GPX` 是 `GetShortPathNameW` 對 scratchpad 內一個合成長檔名回報的短檔名。這是環境相依的：只在該磁碟區有產生短檔名時成立，本 reviewer 只在 scratchpad 所在的磁碟區觀測到（NV-4）。Worklog §10.1 把它列為「需要 stat 或讀取非 pace 的檔案」才能偵測的殘餘；這個說法不成立，見下一小節。

### 分類：implementation defect，不是 design issue

本 reviewer 考慮過把 R2-F1 判為契約語義不足（治理 §4.2）：契約沒有定義兩個不同的 `source_file` 字串何時算同一個檔案。結論是不成立，依據如下。

1. **這個缺口是 #9 自己的實作引入的。** BASE `0c109aa` 以資料夾列表作精確比對（`by_file = {f.name: f for f in gpx_files}`、`by_file.get(trip["source_file"])`），清單中的名稱必須逐字等於一個實際的目錄項目名稱。`a281cb0` 改為直接組路徑（`source = args.gpx_dir / name`，再 `is_file()`），從此作業系統接受的任何拼法都能開檔。`git show a281cb0 -- src/moto_copilot/ingest/__main__.py` 顯示 `glob`／`by_file` 被刪、`args.gpx_dir / name` 被加。
2. **只用名稱就能關閉，不需要補契約語義。** 在本 reviewer 的合成資料夾：

```text
listing: ['alias.gpx', 'kept.gpx', 'pace_a.gpx', 'pace_b.gpx', 'pace_long_named_trip_a.gpx']
'pace_a.gpx::$DATA'  in listing=False is_file=True  Path(name).name==name: True
'PACE_L~1.GPX'       in listing=False is_file=True  Path(name).name==name: True
'PACE_A.GPX'         in listing=False is_file=True  Path(name).name==name: True
```

   串流寫法、短檔名與大小寫變體都不是目錄項目的實際名稱；它們只是同一個目錄項目的其他拼法。程式可以決定自己接受哪些拼法，這不需要 stat、讀取或雜湊任何非 pace 的檔案，也不需要新的清單欄位。所以這是 Executor 的 HOW 範圍內可修的缺陷，R1 的 required fix 所設的限制（不讀取、不雜湊非 pace 的 GPX；不做內容去重複）仍可遵守。此處只是說明可修性的證據，做法由 Executor 決定，本 reviewer 不指定。
3. **契約依據明確。** `DESIGN.md:376`「保留行程與被排除的行程的檔案不開啟」、CL-B1-3 第 4 項「清單中其他角色…的項目不開啟、不產生列」、SPEC-B1 §5 #9 列。重現中被開啟的正是清單以非 pace 角色指定的那個目錄項目（`samefile=True`），並產生了 `trip_role = pace` 的列。R1-F1 已在本 cycle 確立「清單內部矛盾時要 fail closed」是這幾條的適用方式，Executor 在 worklog §10.1 也這樣陳述；沒有任何已接受的條款把「以另一種拼法寫出的矛盾」排除在外。
4. **修正本身的宣稱被反例推翻。** `source_key` 的 docstring 寫「names that can open the same file in the GPX folder are equal」；上面的重現是直接反例。

### Blocking 與 severity

- **Blocking 成立**，依據是 accepted contract（治理 §4.3），不是發生機率。#9 標示 H-3；高風險 decision §5 對 H-3 的最低核對是「凍結前沒有開啟保留行程的程式路徑」，SPEC-B1 E-5 要求 independent audit 依這個範圍核對。這是以程式路徑是否存在為準的條件，而路徑已重現。本 reviewer 因此不能把 H-3 的這一項記為已核對通過。
- **Severity：本 reviewer 評為 Medium／blocking，不同意 High。** 觸發條件是清單中出現 `::$DATA` 或短檔名的寫法，而且同一個檔案另有一筆不同角色的項目。資料夾列表不會產生這兩種寫法，所以它們不會由複製檔名或工具產生清單而意外出現；R1-F1 的同名重複則可能由重新指定角色時留下舊列而意外發生。實際發生的機率低於 R1-F1。後果（凍結前讀取保留行程，污染不可撤銷）不變。Severity 的差異不改變 blocking 判定。
- 本 finding **沒有主張任何真實資料已被讀取、開啟或外洩**；全部證據來自合成檔。高風險 decision §5「已實際外洩」的處理不適用。
- 屬主張違反 accepted contract 條款的 finding，且在高風險類別內；治理 §4.5 與高風險 decision §5 對其 disposition 的限制由 Final Adjudicator 適用，本 reviewer 不作 disposition。

### Required fix／owner

Owner：**#9 Executor**（是否要求 rework 由 Final Adjudicator 決定）。Closure 需要的結果：

1. 重建流程不得開啟它沒有納入角色衝突比對的拼法。對同一個目錄項目的各種拼法——至少包含預設資料串流的寫法（不分大小寫，出現在 pace 項目或非 pace 項目任一邊）與 8.3 短檔名——清單若同時給它 pace 與非 pace 角色，在開啟任何 GPX 之前拒絕；或者這類拼法本身在開啟任何 GPX 之前就被拒絕。
2. 以合成資料補 regression evidence：自動選擇與 `--trips`、`holdout` 與 `excluded`、串流寫法在兩邊各一；斷言 exit 2、GPX 資料夾內沒有 open 事件、沒有輸出檔。短檔名的證據要考慮它在測試環境不一定存在；CL-B1-9 第 2 項第 iii 款不允許新增 `skip`／`xfail` 標記。
3. `source_key` 的 docstring、worklog §10.1 的殘餘清單與 §10.4 的 H-3 陳述改成與證據相符（H-3：陳述不超出證據）。目前 §10.1 沒有列出串流寫法，並把短檔名誤列為需要 stat 才能偵測。
4. 不要求 stat、讀取或雜湊非 pace 的檔案，不要求內容去重複，不要求新的清單欄位。

**提請 Final Adjudicator 注意的範圍問題**：R2 的 required fix 只點名串流語法。若 rework 只處理串流語法，8.3 短檔名這個已重現的同類成員會留下，下一個 cycle 可能以同一 root cause 再次 blocking（治理 §4.5「Cycle 起點與進展」）。本 reviewer 的判斷是 rework 範圍應以上面第 1 項的 root cause 為準。

## 不屬於 R2-F1 的部分：連結與內容重複 — required authority = Design Authority

```text
hard link alias on pace entry  pace='alias.gpx' other='kept.gpx' role=holdout req=None exit=0 gpx_opened=['alias.gpx'] rows=8 samefile=True
```

`alias.gpx` 是本 reviewer 在 scratchpad 對合成檔 `kept.gpx` 建立的 hard link。它與上面兩種拼法不同：`alias.gpx` 與 `kept.gpx` 是兩個各自存在於列表中的目錄項目，清單的字串本身沒有矛盾，要知道它們是同一個檔案必須取得非 pace 項目的檔案識別（stat）或內容。符號連結與「內容相同、檔名不同」的複本屬同一類。

本 reviewer 的判斷：

- 這一類**不是** R1-F1／R2-F1 的 required fix 所及（R1 明示不要求讀取或雜湊非 pace 的 GPX）；內容去重複在 Issue #9 的排除範圍，first-run derivation 的 G-ING 已記為未 ready。
- 「重建流程是否必須辨識以不同目錄項目指向同一檔案或同一內容的情形」「為此取得非 pace 檔案的 metadata 是否與『不開啟』相容」是契約沒有寫定的語義。本 reviewer 不補寫，也不判定它在或不在 #9 之內。依治理 §4.2 這是 routing signal，不是對 implementation 的 blocking finding。**Required authority = Design Authority**（worklog C-9-5b 已指向 DA；涉及開啟或雜湊保留行程檔案的部分，G-ING (2) 已記 required authority = acceptor）。
- Tracking owner：Orchestrator。這一項不延長本 cycle。

## R1-F2 — 已解決（non-blocking）

Worklog 第 98、305、362、471 行已改為「缺少 `stop_allow_s` 及隨它改變的時間值（`eta_typ`／`eta_safe`）」，原測試輸出保留。同意 R2 的結論。本 reviewer 沒有重做 S-4 的逐列比對，引用的是 R1、R2 兩份 record 一致的逐列結果與本次 `--runxfail` 的失敗清單。

## 高風險類別（僅就剩餘 finding 的範圍）

| 類別 | 核對 |
| --- | --- |
| H-2 | `git ls-files` 中 `.env`、`*.key`、`*.gpx`、`*.fit`、`data/` 的路徑數都是 0（只計數，不輸出檔名）。Correction 的錯誤訊息只列行程代號，不列檔名。新增測試與本 reviewer 的重現只用函式產生的合成直線軌跡（虛構原點 10.0, 20.0、2026-01-01 起算）。來源角色隔離：**未通過（R2-F1）**。以真實資料核對：NOT VERIFIED（NV-1） |
| H-3 | 「凍結前沒有開啟保留行程的程式路徑」：同名與大小寫矛盾已關閉；串流寫法與短檔名的路徑存在，**未通過（R2-F1）**。Worklog §10.4 以「名稱等價範圍內」限定其主張，但殘餘清單不完整（required fix 第 3 項）。pytest 計數與 worklog §10.3 相符（`265 passed, 4 xfailed`），沒有把 xfail 寫成通過 |
| H-4 | 一般的矛盾清單是明確拒絕（exit 2、無輸出、無部分重建），有測試。R2-F1 的情形得到 exit 0 與 pace 列，並在輸出中稱非 pace 項目未開啟，是同一個 fail-closed 缺口 |

C-9-6（矛盾時整份清單拒絕）：是 fail-closed 的做法，本 reviewer 沒有發現需要另行裁決之處，也沒有把它當成 finding。

## 執行的檢查

| 檢查 | 結果 |
| --- | --- |
| `sha256sum` Issue 原文 | 與 BD-3 相符 |
| `git -C <worktree> rev-parse HEAD`、`status --short --ignored`、`log --name-only 0c109aa..09d150f` | HEAD 為 subject；10 個 commits，只有 `a281cb0`、`b4d1f84`、`6f97561` 改 `src`／`tests` |
| R2 record 的 SHA-256（worktree 與主 checkout） | 都是 `4ab9e1dfb77ab22124fc43da66d6329e53ecb3c1697d2124d9507f1b3bfe1551`，與 run record 事件 10 相符 |
| `python -m pytest -q -p no:cacheprovider --basetemp=<scratchpad> -rxX`（worktree；確認匯入的是 worktree 的 `src`） | `265 passed, 4 xfailed in 1.03s`，exit 0 |
| 同上加 `--runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py` | `4 failed, 67 passed` |
| 自寫重現程式（scratchpad，`PYTHONPATH=<worktree>/src`，合成 GPX 取自受審測試的 `_gpx`） | 見上各節 |
| Mutation（`git archive` 的副本） | 見 R1-F1 一節 |
| 閱讀 | Bindings m3；治理本文 §2.3–§2.5、§4.1–§4.6；`derivation-spec-b1.md`；高風險 decision；CL-B1-9／10 decision；`DESIGN.md:295`–`296`、`:376`、§6.2 保留行程規則；`SPEC-001` §2、S45；`SPEC-RESOLUTION-001` SB2-T11 與 `:150`；first-run derivation 的 G-ING；`ingest/__main__.py`、`ingest/gpx.py`、`tests/test_ingest_cli.py` 全文；correction diff；BASE 的 `ingest/__main__.py`；worklog §10；run record §6 |

本 reviewer 的重現程式有一個原本打算檢查 NTFS 大小寫表與 `casefold` 差異的案例寫錯了（實際上只重跑了同名情形），沒有產生有效觀測，本 record 不引用它。

沒有重做的部分：停止分類、修剪邊界、S-1／S-2 的 AST 比對、CL-B1-10 的測試內容。這些不在 R2 後剩餘 finding 的範圍，R1、R2 的結論在此既不確認也不推翻。

## NOT VERIFIED

- **NV-1**（C-9-3）：真實行程清單的角色、以真實 GPX 重建的契約符合性、真實保留行程的實際隔離。沒有 RB-7 授權，Issue #9 也排除真實重建。Required authority = **acceptor**。
- **NV-2**：本 review 全部 assistant 訊息的實際 (model, effort)。由派工者依 Bindings §3.6 核對並記入 run record 事件 11。
- **NV-3**：Executor 與 Codex 的 binding 證據（transcript、rollout）本 reviewer 沒有獨立讀取，(b) 欄引用 run record 的核對紀錄。
- **NV-4**：真實 GPX 資料夾所在磁碟區是否產生 8.3 短檔名、真實檔名是否有短檔名別名。需要列出 `data/`，沒有授權。Required authority = **acceptor**。這只影響實際暴露的程度，不影響上面的判定。

## 後續 authority

- R2-F1 在 Alternate Review 後仍未解 → 治理 §4.4：進 **Final Adjudication**。本 reviewer 不作裁決，不開新 round，不指定 rework 的做法。
- 連結與內容重複的語義 → **Design Authority**（上節）。
- 本 record 沒有宣告 audit closure、Spec closure、phase acceptance 或任何 gate PASS。

關於最後一行的格式：派工內容要求 `Verdict: PASS` 或 `Verdict: BLOCKING`；`gov-alternate-reviewer` definition 的「紀錄」一節要求 `VERDICT: CLOSURE`／`VERDICT: UNRESOLVED (<finding 編號>)`。兩者在此同義，下面兩行都寫出，最後一行依 definition。

Verdict: BLOCKING

VERDICT: UNRESOLVED (R2-F1)
