# Final Adjudication ruling — Issue #9（SPEC-B1 B1-2 `ingest`）cycle 1

| 欄位 | 內容 |
| --- | --- |
| Ruling ID | `ruling-20261117-issue9-c1`（檔名依派工指定；實際撰寫日期 2026-11-18） |
| 角色 | `final_adjudicator`（`gov-final-adjudicator`），治理 §4.5 |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record §6 事件 12：「Alternate Review 後仍未解（R2-F1）」） |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`derivation-spec-b1.md` 的 #9 列、CL-B1-1、CL-B1-3、CL-B1-7）＋ CL-B1-8（`decision-20261117-issue7-spike-tests.md`）、CL-B1-9、CL-B1-10（`decision-20261117-issue9-e1-and-trim.md`）→ GitHub Issue #9。Issue 原文：派工所附 scratchpad 檔，本 FA 實測 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895`，等於 BD-3 |
| 高風險類別 | #9 標示 H-2、H-3、H-4（`derivation-spec-b1.md` §5；`decision-20261117-high-risk-categories.md` §3、§5） |
| 受審 subject（cycle 1） | `09d150f0f7db34b3f46790a54e167b7f617a2fac`（branch `oc1-run2-b1-ui0-r1-routing`；BASE `0c109aa`）。實作 `a281cb0`、`b4d1f84`，correction `6f97561`；其餘 commit 只改 `docs/governance/records/**`（本 FA 以 `git log 0c109aa..HEAD` 與 `git diff --stat 0c109aa..09d150f` 核對） |
| 讀過的 records | R1 `docs/governance/records/audit/issue-9-c1-r1.md`、R2 `issue-9-c1-r2.md`（Primary＝Codex）、Alternate `issue-9-c1-alt.md`；worklog `docs/governance/records/worklog/issue-9.md`（第 1–10 節）；run record §6 事件 2–12。三份 audit record 與 worklog 的結論都當成待驗證主張，本 ruling 採用的事實都另行重讀原始檔或重現 |
| 依據的條文 | 治理 §1.2（boundary 段）、§1.5、§2.4、§2.5、§4.2、§4.3、§4.4、§4.5、§4.6；orch-default v2.2 §5、§6、§7（P3–P6）；Bindings m3 §2.6 RB-7、§3.2 E-FA／E-EX、§3.6、§3.7、§5、§7；高風險 decision §5 |

## Assurance

### (a) Context independence（治理 §2.3）

| Property | 滿足方式 |
| --- | --- |
| Independent context | Fresh 的 `gov-final-adjudicator` subagent，沒有繼承 Executor、Reviewers 或 Orchestrator 的對話；pack 只有路徑與識別 |
| Verifiable binding | 有效 mapping 為 Opus 5.5／`xhigh`（F-FA；run record 事件 12）。本 FA 無法自證全部 assistant 訊息的實際 (model, effort)；依 Bindings §3.6 由派工者在採用本 ruling 前核對 transcript 並記入事件 12 |
| Autonomous access | 自行讀取契約、原始碼、BASE 與 subject 的程式、git 歷史；在 detached worktree `C:/Users/yotsu/AppData/Local/Temp/cx9r2` 以主 checkout 的 `.venv` 執行 pytest（`-B -p no:cacheprovider`，`--basetemp` 指向 session scratchpad）；在 scratchpad 以自寫程式與合成檔重現。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有讀取或執行 `experiments/`，沒有使用網路，沒有從 repo root 搜尋 |
| Self-written record | 本 ruling 由本 FA 以 Write 工具寫入。沒有修改實作、測試、契約、gates 或其他紀錄，沒有 stage／commit。Worktree 的 `git status --short --ignored` 在本 FA 執行前後相同（`?? docs/governance/records/audit/issue-9-c1-r2.md`、`!! .pytest_cache/`） |

### (b) 實際 model

| 角色 | Model（證據） |
| --- | --- |
| Executor | `claude-opus-5-5`／`high`（run record 事件 2、7、9） |
| Primary Reviewer（R1、R2） | Codex `gpt-6.1-sol`／`high`（事件 8、10 的 rollout 核對） |
| Alternate Reviewer | `claude-fable-5-2`／`high`（事件 11） |
| Final Adjudicator | 有效 mapping `claude-opus-5-5`／`xhigh`；實際觀測由派工者記入事件 12 |

Bindings §5 沒有宣告 diversity 關係；本 ruling 不主張 model diversity。FA 與 Executor 的有效 mapping 是同一個 model。

### Capability escalation

E-FA：Bindings §3.2 採用 (M2)、(D1)。(M2)「同一 root cause 在新 cycle 再次進入 FA」不成立（本次是 cycle 1）。(D1)：本 FA 沒有需要升級的具體爭議面向——事實可由合成資料直接重現，契約條款明確，爭議集中在處置的種類。不提出 trigger，作出 ruling。

---

## 1. 爭議

Alternate Review 之後仍未解的是 **R2-F1**（Alternate record：`VERDICT: UNRESOLVED (R2-F1)`）。各 record 的立場：

| 項目 | R1 | R2 | Alternate |
| --- | --- | --- | --- |
| R1-F1（同一來源檔的 pace／非 pace 矛盾） | High／blocking | NOT RESOLVED，殘餘以 R2-F1 識別 | R1 所證的情形已解決；同一 root cause 的殘餘以 R2-F1 識別 |
| R2-F1（`::$DATA` 預設資料串流寫法繞過角色比對） | — | High／blocking | 有效、未解、blocking；severity 評為 Medium；屬 implementation defect，不是 design issue；另加 8.3 短檔名為同一 root cause 的成員 |
| R1-F2（worklog 對 S-4 的摘要） | Low／non-blocking | RESOLVED | 已解決 |
| 連結、內容相同的不同檔名，與取得非 pace 檔案 metadata 是否相容於「不開啟」 | — | 未審 | 不屬 R2-F1；契約未寫定，routing signal，required authority＝Design Authority |

要裁決的是：R2-F1 的處置（dismiss、rework／新 cycle、defer 或交 DA）；rework 的範圍是否以 root cause 為準（含 8.3 短檔名）；以及 Alternate 提出的 routing signal 的去向。

## 2. 依據的證據（本 FA 自行取得）

### 2.1 契約條款

- `DESIGN.md` §5 契約 1 之後（subject 第 377 行）：「研究凍結之前…`ingest` 與配速表的重建只處理配速行程：保留行程與被排除的行程的檔案不開啟」；同節資料處理流程第 6 項（第 296 行）同文。
- CL-B1-3 第 4 項：重建流程「只開啟清單中 `trip_role` 是 `pace` 的檔案；清單中其他角色…的項目不開啟、不產生列」。
- `derivation-spec-b1.md` §5 #9 列：另加「清單中非 `pace` 的項目不開啟…並以測試確認被拒絕的檔案沒有被開啟」。
- `derivation-spec-b1.md` §6 SB1-AC5：「沒有任何程式路徑會在重建時開啟非 `pace` 的行程檔案」。
- 高風險 decision §5：H-3 的 audit 最低核對範圍含「凍結前沒有開啟保留行程的程式路徑」；H-2、H-3、H-4 的 blocking finding 不得由 FA 單獨 defer。

### 2.2 程式

- Subject 的 `src/moto_copilot/ingest/__main__.py`：`source_key`（第 62–71 行）只取最後的路徑成分，做 NFC、去結尾句點／空白與 `casefold`；`_refuse_conflicting_roles`（第 74–84 行）以這個 key 比對 pace 與非 pace 項目；`main` 對被選中的項目只做 `Path(name).name != name` 的檢查（第 131 行），之後以 `args.gpx_dir / name` 組路徑、`is_file()`、`read_gpx`（第 134–138 行）。
- BASE `0c109aa` 的同一檔：`gpx_files = sorted(args.gpx_dir.glob("*.gpx"))`、`by_file = {f.name: f for f in gpx_files}`、`by_file.get(trip["source_file"])`——清單名稱必須逐字等於一個列出的目錄項目名稱。`a281cb0` 改為直接組路徑。Alternate 對此的描述與原始碼相符。

### 2.3 本 FA 的獨立重現（合成資料，scratchpad）

自寫程式 `<session scratchpad>/fa9/repro_fa.py`：以 `sys.path` 匯入 worktree 的 `src`（斷言模組路徑在 worktree 內）；合成 GPX 由程式產生（虛構原點 10.0, 20.0、2026-01-01 起算的直線）；清單是實際寫到磁碟的 JSON；不 mock parser、`build_rows` 或 validators；以 audit hook 記錄 GPX 資料夾內的 `open` 事件；`samefile` 是 `os.path.samefile` 對兩個名稱的結果。執行後刪除工作目錄。

```text
R1 same name / holdout auto       pace='pace_a.gpx'                 other='pace_a.gpx'                 role=holdout  req=None    exit=2 gpx_opened=[] rows=None samefile=True
R2 ::$DATA on pace entry          pace='pace_a.gpx::$DATA'          other='pace_a.gpx'                 role=holdout  req=None    exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$DATA on pace entry          pace='pace_a.gpx::$DATA'          other='pace_a.gpx'                 role=holdout  req=['T901'] exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$DATA on pace entry          pace='pace_a.gpx::$DATA'          other='pace_a.gpx'                 role=excluded req=None    exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$DATA on pace entry          pace='pace_a.gpx::$DATA'          other='pace_a.gpx'                 role=excluded req=['T901'] exit=0 gpx_opened=['pace_a.gpx::$DATA'] rows=8 samefile=True
R2 ::$DATA on non-pace entry      pace='pace_a.gpx'                 other='pace_a.gpx::$DATA'          role=holdout  req=None    exit=0 gpx_opened=['pace_a.gpx'] rows=8 samefile=True
8.3 short name reported for synthetic probe: PACE_L~1.GPX
8.3 short name on pace entry      pace='PACE_L~1.GPX'               other='pace_long_named_trip_a.gpx' role=holdout  req=None    exit=0 gpx_opened=['PACE_L~1.GPX'] rows=8 samefile=True
8.3 short name on non-pace entry  pace='pace_long_named_trip_a.gpx' other='PACE_L~1.GPX'               role=holdout  req=None    exit=0 gpx_opened=['pace_long_named_trip_a.gpx'] rows=8 samefile=True
listing: ['pace_a.gpx', 'pace_long_named_trip_a.gpx']
  'pace_a.gpx::$DATA'  in_listing=False is_file=True plain=True key='pace_a.gpx::$data'
  'PACE_L~1.GPX'       in_listing=False is_file=True plain=True key='pace_l~1.gpx'
```

每一個 exit 0 的案例，CLI 的第一行都是 `pace trips: 1 | non-pace entries not opened: 1 | rows: 8`，與實際開啟的檔案不符。

結論：
1. R2 與 Alternate 的 `::$DATA` 重現成立，在 pace 項目或非 pace 項目任一邊都繞過。
2. Alternate 的 8.3 短檔名重現成立；本 FA 另觀測到短檔名放在**非 pace 項目**那一邊時同樣繞過（Alternate 只列了 pace 那一邊）。這是同一個目錄項目的另一種拼法，與 Alternate 對 root cause 的定義（`source_key` 的等價關係比開檔時作業系統接受的拼法窄）相符。短檔名是否產生取決於磁碟區設定，本 FA 只在 scratchpad 所在磁碟區觀測到。
3. 兩種拼法都不是目錄列表中的名稱，而作業系統會把它們解析到列表中的那個項目。所以 Alternate 的判斷成立：worklog §10.1 稱短檔名「需要 stat 或讀取非 `pace` 的檔案」才能偵測，至少在 pace 那一邊不成立；`source_key` docstring 的「names that can open the same file in the GPX folder are equal」有直接反例。

### 2.4 Regression 基準（觀測，不是 gate 判定）

在 worktree（`09d150f`）執行 `python -B -m pytest -q -p no:cacheprovider --basetemp=<scratchpad> -rxX`：`265 passed, 4 xfailed in 1.01s`，exit 0；四個 xfail 的 reason 是 CL-B1-8 的 `restored by #10`（1 個）與 `restored by #11`（3 個）。與 R2、Alternate 的觀測相同。E-1 是否成立由 Reviewer 依 CL-B1-9 判定，本 ruling 不作判定。

## 3. 裁決

### 3.1 R2-F1（含 R1-F1 的殘餘）：不 dismiss、不 defer、不是 design issue；要求 targeted rework，並以它授權新的 bounded cycle（cycle 2）

**不 dismiss。** Dismiss 需要推翻 finding 主張的證據。本 FA 在合成資料上獨立重現：清單以非 pace 角色指定的目錄項目，在凍結前的重建中被開啟並產生 `trip_role = pace` 的列。這直接違反第 2.1 節的 DESIGN §5、CL-B1-3 第 4 項與 SB1-AC5（「沒有任何程式路徑」）。沒有任何已接受的條款把「以另一種拼法寫出的矛盾清單」排除在外；R1-F1 已在本 cycle 確立清單內部矛盾要 fail closed，Executor 的 correction 也採此做法（worklog §10.1、C-9-6，R2 與 Alternate 都沒有對它提出 finding）。

**不 defer。** 治理 §4.5 的四個條件須同時成立：
1. 條件 1 **不成立**：R2-F1 主張違反 accepted contract 條款（DESIGN §5 的隔離要求、CL-B1-3 第 4 項、SPEC-B1 §5 #9 列與 SB1-AC5）。這類 finding 只能 dismiss、要求 rework，或作為 contract change 交 DA 與 acceptor。
2. 另外，#9 屬 H-2、H-3、H-4；依治理 §4.5 與高風險 decision §5，deferral 須另有 Design Authority 確認，FA 不得單獨 defer。
條件 1 已不成立，所以沒有評估條件 2–4，也沒有向 DA 請求 deferral 確認。

**不是 design／requirement issue。** 同意 Alternate 的分類，依據：
- 缺口由 #9 的實作引入（BASE 以列表逐字比對；`a281cb0` 改為直接組路徑），不是契約沒有定義的行為。
- 修正只需要決定程式接受哪些名稱拼法、以及在開啟任何 GPX 之前如何比對或拒絕，這屬 Executor 的 HOW（治理 §2.4），與 D-9-5「`source_file` 必須是單純檔名」同類——都是更嚴格的拒絕，不改變任何欄位、角色或分類的定義。
- 可修性有證據：兩種拼法都不在目錄列表中（第 2.3 節），R1 與 Alternate 都確認修正不需要讀取、雜湊非 pace 的檔案。
所以不需要新的契約語義，不 route 至 DA。（連結與內容重複是另一個問題，見第 3.4 節。）

**Severity。** R2 評 High，Alternate 評 Medium；兩者都判定 blocking，blocking status 沒有爭議。處置不因 High 或 Medium 而不同，本 ruling 不裁決 severity，也不覆寫任一方的評定。

**R1-F1 的表述。** R2 記 NOT RESOLVED，Alternate 記「R1 所證範圍已解決」；兩者都以 R2-F1 識別剩下的部分，實質一致。本 ruling 把 R1-F1／R2-F1 視為**同一 root cause 的一個未解 blocking 問題**，作一個處置；R1-F1 不另行關閉，隨 R2-F1 進入 cycle 2。本 FA 確認 R1 record 的三個重現情形在 `09d150f` 都被拒絕（第 2.3 節第一列；Alternate 的重現與 mutation 檢查相同）。

**為什麼是新 cycle，而不是在 cycle 1 內修正。** Cycle 1 已用完 R1、R2 與唯一一次 Alternate Review（治理 §4.4，不得有 R3／R4）。修正後的 subject 需要 independent audit 才能 closure，而唯一合法的路徑是新的 bounded cycle（治理 §4.5「Cycle 起點與進展」；orch-default §6「新 cycle」）。實質理由：一個已重現、契約依據明確、可在 #9 範圍內以 HOW 修正的 implementation defect；同一 root cause 尚未經過任何新 cycle，所以治理 §4.5 的進展限制還沒有觸及。

### 3.2 Rework 的範圍與 closure 所需的證據

Owner：**#9 Executor**（`gov-executor`，同一 worklog identity `docs/governance/records/worklog/issue-9.md`）。範圍以 **root cause** 為準，不只限於 R2 點名的串流寫法。這採用 Alternate record R2-F1 一節的 required fix（Alternate 在同一 finding 內把 8.3 短檔名列為同一 root cause 的成員）；只修串流寫法會留下已重現的 8.3 案例，cycle 2 會以同一 root cause 再次 blocking。

**要達成的結果（不是做法；做法由 Executor 決定）：**
1. 重建流程不得開啟它沒有納入角色衝突比對的拼法。對清單中任何會被作業系統解析到同一個目錄項目的拼法，不論出現在 pace 項目或非 pace 項目，只要清單同時給該目錄項目 pace 與非 pace 角色，就在開啟任何 GPX 之前拒絕；或者這類拼法本身在開啟任何 GPX 之前就被拒絕。已知的成員至少有：預設資料串流寫法（`::$DATA`，不分大小寫），以及 8.3 短檔名；兩者都要涵蓋兩邊。
2. 不得開啟、讀取或雜湊非 pace 項目所指的檔案。凡是依賴以 stat、檔案識別碼、連結列舉或內容取得「非 pace 項目所指檔案」資訊的做法，都落在第 3.4 節交給 DA 的問題（Q-DA-1）之內，DA 作成 decision record 之前不得採用；Executor 無法確定自己的做法是否屬於這一類時，依治理 §2.4 route 至 DA，不自行推定。
3. 不擴張範圍：不實作內容去重複（Issue #9 排除範圍；G-ING）、不新增清單欄位、不實作上傳。這些只在 DA 依 Q-DA-1 另有裁決時，依該裁決處理。

**Closure 證據（cycle 2 的 Reviewer 據此判定，本 ruling 不預判結果）：**
1. 合成資料的 regression tests：自動選擇與 `--trips`；`holdout` 與 `excluded`；串流寫法與 8.3 短檔名各在 pace 那一邊與非 pace 那一邊。每一例斷言 exit 2、GPX 資料夾內沒有 `open` 事件、沒有輸出檔。
2. 8.3 短檔名的證據不得依賴測試所在磁碟區是否產生短檔名，也不得新增 `skip`／`xfail` 標記（CL-B1-9 第 2 項第 iii 款；CL-B1-8 §3.4 K-1）。Executor 在 worklog 寫明這項證據如何不依賴環境；若執行所在磁碟區有短檔名，另記一次實際觀測。
3. R1-F1 的既有 regression tests 保留並通過；`segments.py`、`tests/test_ingest.py` 的停等與修剪行為不因 rework 改變（若有改變，在 worklog 寫明理由）。
4. E-1 依 CL-B1-9 第 2 項，在 cycle 2 的最終 subject 重跑，並把完整輸出記在 worklog（含 `-rxX` 與 `--runxfail` 的三個檔案範圍）；結果照實寫數目，不寫「全數通過」。
5. 陳述與證據相符（H-3）：`source_key` 的 docstring（或取代它的程式說明）、worklog §10.1 的殘餘清單與 §10.4 的 H-3 陳述改為與實際行為一致；殘餘只列真正不在 rework 範圍內的情形，並引用 Q-DA-1。
6. 高風險類別的 self-verification 依高風險 decision §5（H-2、H-3、H-4）更新並記錄。

### 3.3 新 bounded cycle（cycle 2）的授權

- **相對 cycle 1 受審 subject 的實質改變**（cycle 1：`09d150f`，程式與測試 subject `6f97561`）：
  1. `src/moto_copilot/ingest/__main__.py`：清單 `source_file` 的接受規則與角色衝突比對改變，達成第 3.2 節的結果 1–2。
  2. `tests/test_ingest_cli.py`（或同類測試檔）：第 3.2 節 closure 證據第 1–2 項的合成 regression tests。
  3. 程式說明與 worklog 的陳述更正（第 3.2 節 closure 證據第 5 項）。
  4. 若 DA 對 Q-DA-1 的 decision record 要求 #9 作出變更，依該 record 一併納入。
  只有 record-only 的 delta（`docs/governance/records/**`）而沒有第 1、2 項的程式與測試 delta 時，不構成實質改變，**不得**開始 cycle 2（治理 §4.5：「Subject 與契約皆未改變時，不得開新 cycle」）。
- **起點與流程**：cycle 2 從 **R1** 開始，是完整的 independent audit（治理 §4.4：R1 完整審查 accepted work scope，不限於本 ruling 的 finding），之後依 R2、exactly one Alternate、FA 的順序。`primary_reviewer` 依 Bindings O-6／§3.3 的當次可用性解析。R1 的 bounded pack 加入本 ruling 的路徑與 Q-DA-1 的 decision record 路徑。
- **R1 的派工時點**：cycle 2 R1 的受審 subject 要包含上面第 4 項（若適用），所以 cycle 2 的 R1 在 Q-DA-1 的 DA decision record 存在之後才派工。DA 與 Executor 的派工順序由 Orchestrator 決定；先派 DA 可以讓 Executor 一次完成第 3.2 節與 DA 可能增加的要求。
- **進展限制**（治理 §4.5）：若同一 root cause（重建流程開啟它沒有納入角色衝突比對的拼法）在 cycle 2 的 R2 之後仍未解，該問題不再視為 rework 可解的 implementation defect；之後的 FA 必須把它作為 design／requirement issue 交 DA，或在 disposition 邊界內處置，**不得**再以 rework 授權 cycle 3。屆時同一 root cause 在新 cycle 再次進入 FA，構成 E-FA (M2)，由 Orchestrator 機械套用（Bindings §3.2）。
- **Executor 的 mapping**：Profile E-EX (M3) 描述的情形（同一 root cause 在一次 targeted correction 後仍以 implementation defect 存在）在此成立，但 Bindings §3.2 宣告 E-EX 不適用（O-1：escalated mapping 等於有效 mapping），Executor 仍是 `claude-opus-5-5`／`high`。這只是提醒，不是本 ruling 的決定。

### 3.4 Routing：連結、內容相同的不同檔名，與非 pace 檔案的 metadata（Q-DA-1）

FA 在此只釐清 routing，不取得實質決定權（治理 §2.4）。Alternate 的判斷——這不屬 R2-F1，而是契約沒有寫定的語義，依治理 §4.2 是 routing signal、不是對 implementation 的 blocking finding——本 FA 同意：hard link 的兩個名稱是兩個各自存在於列表中的目錄項目，清單字串本身沒有矛盾，要辨識它們必須取得檔案識別或內容；這超出 R1-F1／R2-F1 required fix 的範圍（R1 明示不要求讀取或雜湊非 pace 的 GPX）。

**Route 至 Design Authority（Q-DA-1）**，要 DA 以 decision record 回答：
1. #9 的隔離要求（DESIGN §5「保留行程與被排除的行程的檔案不開啟」、CL-B1-3 第 4 項、SB1-AC5）是否要求重建流程辨識下列情形：(a) pace 項目與非 pace 項目指向同一檔案物件的不同目錄項目（hard link）；(b) 解析到非 pace 項目所指檔案的符號連結、junction 或其他 reparse point；(c) 內容相同、名稱不同的兩個檔案。
2. 以 stat、檔案識別碼、連結列舉或目錄列舉取得非 pace 項目所指檔案的 metadata，是否與「不開啟」相容。
3. 若需要辨識，屬 #9 或另一個 work item（例如 first-run derivation G-ING 的 Profile 管理與去重複）。
4. 涉及開啟或雜湊保留行程內容的部分，依 G-ING (2) 與 RB-7，required authority＝acceptor；DA 無法確立在 OC-1 boundary 內時，受影響路徑依治理 §1.2 fail-closed 至 acceptor。

Tracking owner：Orchestrator。Q-DA-1 已 route，依 orch-default §7 P6，#9 結案前須有對應的 decision record。

### 3.5 R1-F2

R2 與 Alternate 都記為已解決（non-blocking）。沒有爭議，FA 不作處置，不覆寫。

### 3.6 C-9-6（矛盾清單整份拒絕）

R2 與 Alternate 都沒有對它提出 finding，沒有交付裁決的爭議。本 ruling 不處理。

## 4. 每條未解 blocking finding 的處置

| Finding | 處置 | Owner | 依據 | 後續 authority |
| --- | --- | --- | --- | --- |
| R2-F1（與 R1-F1 的殘餘為同一 root cause；Alternate 列入的 8.3 短檔名為其成員） | **要求 targeted rework，並以它授權新的 bounded cycle（cycle 2）**。不 dismiss（證據支持違反）；不 defer（條件 1 不成立；高風險類別）；不是 design issue | #9 Executor（rework）；Orchestrator（派工與 cycle 2） | 第 2 節證據；第 3.1–3.3 節 | cycle 2 的 Primary Reviewer（R1 完整 audit）；同一 root cause 在 cycle 2 R2 後仍未解時，依治理 §4.5 交 DA 或在 disposition 邊界內處置 |

不屬 blocking finding、但在本 ruling 中 route 的項目：

| 項目 | 去向 | Tracking owner |
| --- | --- | --- |
| Q-DA-1（連結、內容重複、非 pace 檔案的 metadata；源自 Alternate 的 routing signal 與 worklog C-9-5b） | Design Authority；開啟或雜湊保留行程內容的部分為 acceptor（RB-7） | Orchestrator |

## 5. 本 ruling 沒有做的事

- 沒有把任何 gate 標為 PASS；沒有判定 E-1、E-2–E-5、SB1-AC5 或 H-2／H-3／H-4 的核對結果。第 2.4 節的 pytest 只是重現的基準。
- 沒有修改或隱性放寬任何 requirement、AC、invariant 或 gate：第 3.2 節的結果 1 是既有隔離要求在已重現情形下的適用，closure 證據都引用既有條款（CL-B1-8、CL-B1-9、高風險 decision §5）。
- 沒有覆寫任何 Reviewer 的結論：R2 與 Alternate 的 blocking 判定一致；severity 的差異不裁決；R1-F1 的表述兩方實質一致。
- 沒有裁決 Outcome Contract boundary：Q-DA-1 交 DA，fail-closed 的路徑依治理 §1.2。
- 沒有指定修正的做法。

## 6. NOT VERIFIED

| # | 項目 | Required authority |
| --- | --- | --- |
| NV-1（C-9-3） | 真實行程清單的角色、以真實 GPX 重建的契約符合性、真實保留行程的實際隔離 | acceptor（RB-7；Issue #9 也排除真實重建） |
| NV-2 | 真實 GPX 資料夾所在磁碟區是否產生 8.3 短檔名、真實檔名是否有短檔名別名（Alternate NV-4）。只影響實際暴露程度，不影響本 ruling | acceptor（RB-7，需要列出 `data/`） |
| NV-3 | 本 FA 全部 assistant 訊息的實際 (model, effort) | 派工者（Bindings §3.6），記入 run record 事件 12 |
| NV-4 | Executor、Codex、Alternate 的 binding 證據（transcript、rollout）。本 FA 沒有獨立讀取，第 (b) 欄引用 run record 的核對紀錄 | — |

本 ruling 不依賴任何私有資料；沒有證據顯示真實資料已被開啟或外洩。高風險 decision §5「已實際外洩」的處理不適用。

## 7. 下一步

1. **Orchestrator**：核對本 FA 的 binding，記入 run record 事件 12，並原樣 commit 本 ruling。
2. **Orchestrator → Design Authority**：派 Q-DA-1（第 3.4 節）。
3. **Orchestrator → #9 Executor**（`gov-executor`，同一 worklog identity）：派第 3.2 節的 rework；若 DA 的 decision record 已存在，一併引用。
4. **Orchestrator → Primary Reviewer**：subject 包含第 3.3 節第 1–2 項（與適用時的第 4 項）、且 Q-DA-1 的 decision record 存在之後，派 cycle 2 R1（fresh，完整 audit），pack 引用本 ruling。
5. #9 結案仍依 orch-default §7（P3：失敗的 gate 不因本 ruling 而視為滿足；P6：Q-DA-1 須有 decision record）。

## 8. 執行紀錄

| 指令／動作 | 結果 |
| --- | --- |
| `sha256sum` Issue #9 原文 | `30a898f8…a69895`，等於 BD-3 |
| `git rev-parse HEAD`、`git status --short --ignored`、`git log --oneline 0c109aa..HEAD`（worktree） | HEAD `09d150f`；只有 R2 record 未追蹤與已忽略的 `.pytest_cache/`；10 個 commits |
| `git diff --stat 0c109aa..09d150f` | 8 個路徑；產品與測試只有 `ingest/__main__.py`、`ingest/segments.py`、`tests/test_ingest.py`、`tests/test_ingest_cli.py`；`DESIGN.md` 未改 |
| `git show 0c109aa:src/moto_copilot/ingest/__main__.py` | BASE 以列表逐字比對（第 2.2 節） |
| 閱讀 | 本 definition；Bindings m3；治理本文 §1.2、§1.5、§2.4、§2.5、§4.2–§4.6；orch-default v2.2 §5–§7；Profile default v2.5 的 E-FA、E-EX 列；OC-1 鏈上的 derivation、CL-B1-8／9／10、高風險 decision；first-run derivation 的 G-ING；`DESIGN.md` 第 290–298、370–380 行；SPEC-001 的 `trip_id` 列；R1、R2、Alternate records；worklog 第 1–10 節；run record §6；subject 的 `ingest/__main__.py`、`tests/test_ingest_cli.py` 全文 |
| `.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider --basetemp=<scratchpad>/fa9/pt -rxX`（worktree） | `265 passed, 4 xfailed`，exit 0 |
| `.venv/Scripts/python.exe -B <scratchpad>/fa9/repro_fa.py`（`PYTHONDONTWRITEBYTECODE=1`） | 第 2.3 節 |

沒有讀取、列出或搜尋 `data/`；沒有讀 `.env`；沒有讀取或執行 `experiments/` 下的任何檔案；沒有修改受審檔案、契約或其他紀錄；沒有派工任何 subagent；沒有 commit。

Ruling: R2-F1（含 R1-F1 殘餘，同一 root cause）— targeted rework，授權 cycle 2（自 R1 起）；Q-DA-1 route 至 Design Authority。
