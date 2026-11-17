# Issue #8 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md` §4 CL-B1-1、CL-B1-6、CL-B1-7；§5 #8 列及 E-1～E-5）→ Issue #8 B1-5 |
| Issue 版本 | 使用派工附載的原文；版本識別 SHA-256 `061ad87fb3dff17ccbcbb75a433fd2f01c7ac8ff5c226aa65bd6af157d7418e4` 與 first-run derivation §3 BD-3 第 68 行相同；沒有呼叫 GitHub 或其他網路服務 |
| Subject | 本專用 worktree 的 detached HEAD `22f7e2a8ce512dbf70f2dbcab262b3ea750d9a3f` |
| BASE | `05e0a98890f1dc5a20bb0c02c54f3f2b0c2dece0` |
| Implementation commit | `47f1cdb89214d3eba6b4a3003c89f7021c5fabe1` |
| Audit kind | **Ticket independent audit, R1, cycle 1；not a Spec Integration Audit** |
| Role | `primary_reviewer`（Codex，Bindings m3 O-6） |
| 日期 | 2026-11-18 |

## Assurance

| (a) Context independence：四項 properties | (b) Models 與 binding evidence |
| --- | --- |
| **Independent context**：本次是 fresh Codex thread，沒有繼承 Executor 的對話或推理。派工給契約、版本與檔案入口；我自行讀取實作、完整測試、diff 與歷史。Worklog 與 return 中的判斷均視為待驗證主張。 | Executor：run record `docs/governance/records/run/run-20261117-oc1-run2.md` §6 **事件 34**（第 113 行）記錄 agentId `a9c66ffc5117ca116`，派工者核對全部 89 則，唯一集合為 (`claude-opus-5-5`, `high`)。採用此派工者證據，沒有開啟 worktree 外的 transcript。 |
| **Verifiable binding**：依 Bindings §3.3，當次 rollout 的完整核對由 dispatcher 負責。當次 dispatch 的穩定引用是上述 run record §6 **事件 35**（第 114 行）。該事件在受審 HEAD 尚為「進行中」，派工者須在採用本 record 前補上 session id、全部 turn_context 的唯一 (model, effort, sandbox) 集合、存取核對與 record SHA-256。 | Primary：我為 Codex；事件 35 指定 `gpt-6.1-sol`／`high`，Bindings 要求 `workspace-write`。這是目前 repo 內的派工證據，**不是我已核對當次 rollout 的宣稱**。Qualification 通過的既有紀錄見 Bindings §8.2 #7、run record §2 #3；當次完整 binding 核對仍由 dispatcher 完成。 |
| **Autonomous access**：在 worktree 內自行取得原始契約與檔案，執行 git、PATH 上的 Python、pytest、獨立合成輸入檢查；未接受 Executor 選出的摘要作為 coverage 上限。RB-7 的禁令持續適用。首次 pytest 的預設暫存目錄探查被 sandbox 拒絕，詳見下節，後續測試暫存均限制於 worktree。 | Alternate：本次未派。Bindings §5 未宣告 D1～D4 關係；**no model diversity claim**。不以模型名稱不同代替四項 independence properties。 |
| **Self-written record**：本檔由本次 `primary_reviewer` 自行撰寫。實作、測試、契約與其他 records 均未修改，未 stage／commit。Dispatcher 應依 Bindings §3.3 原樣保存並核對 hash；本檔不能代替該項派工後核對。 | 當次 binding evidence 的承載位置為事件 35，非 Executor 的自述。該項是派工者採用產出前的責任，沒有虛報成已完成。 |

## 範圍、版本及命令

我讀取 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3、治理本文 §2.3、§3.8、§4.1～§4.7、impl-default v2 §6～§7 與 orch-default v2.2 §4～§7；以 OC-1、SPEC-B1、first-run derivation BD-1～BD-5、高風險類別 decision §3.4／§5、Issue 原文及下列 spec 條款為審查基準：SPEC-001 4.8、5.2 的規則 3 結果／條件、5.4，SPEC-RESOLUTION-001 §3.1／§3.5，G1 Q18，DESIGN §9.1，BATCH-1 §1／§2／B1-5。SPEC-001 的未 Freeze 部分沒有被視為整份已接受契約。

| 實際命令／檢查 | 結果 |
| --- | --- |
| `git rev-parse HEAD`、`git rev-parse 05e0a98 47f1cdb` | 與表首的三個完整 SHA 相符，exit 0 |
| `git log --oneline --name-only 05e0a98..22f7e2a` | 共三個 commits：`47f1cdb` 新增兩個 validator 原始碼及 `tests/test_rule3.py`；`725956d` 只新增 worklog；`22f7e2a` 只更新 run record。後兩者均為 Bindings §7 的 record-only paths |
| `git diff 05e0a98..22f7e2a`，另按 `src/ tests/ pyproject.toml`、run record 分讀；`git diff --stat 05e0a98..22f7e2a` | 共 5 檔，735 行新增；實作及測試為 3 檔、547 行新增。已逐檔閱讀全部新增原始碼、404 行測試與 186 行 worklog；沒有既有測試／fixture／gate 的變更 |
| `git diff --exit-code 873e37a..22f7e2a -- DESIGN.md docs/spec/SPEC-001-plan-schema.md docs/spec/SPEC-RESOLUTION-001-sb2-sb8-sb9.md docs/grill/g1-grill-input.md docs/ticket/BATCH-1-scoped-tickets.md` | 無輸出，exit 0；讀到的引用來源與 SPEC-B1 指定版本相同 |
| `git diff --check 05e0a98..22f7e2a` | 無輸出，exit 0 |
| `python --version` | Python 3.11.2；使用 PATH，沒有使用 `.venv` |
| 初次 `python -m pytest -q` | exit 1，`458 passed, 97 errors in 31.66s` |
| 初次 `python -m pytest -q -rxX` | exit 1，`458 passed, 97 errors in 30.09s` |
| 限定暫存位置後 `python -m pytest -q` | exit 0，`555 passed in 2.55s`，完整輸出如下 |
| 限定暫存位置後 `python -m pytest -q -rxX` | exit 0，`555 passed in 2.21s`，完整輸出如下；沒有 XFAIL／XPASS／skip |
| `rg -n -i 'xfail|skip' tests/` | 無輸出，exit 1（沒有命中），確認 tests/ 無相關標記 |
| `Get-Content`（初讀）及 `python -c` 的 `Path.read_text(encoding='utf-8')` 配合行號 | 初讀 PowerShell 的預設編碼造成中文亂碼，已以 UTF-8 重讀；未修改檔案。`rg -n` 查詢限於明確的治理檔、spec、G1、DESIGN、BATCH-1 與 tests/ |
| `python -c` 獨立合成輸入及 AST 檢查 | 29,892 組整數範圍／分類組合全通過；9 個十進位邊界／相鄰 float 案例通過；9 個不合法來回 k 均為 ValueError；載入的 rule3 原始碼位於本 worktree；父 package initializer 無 imports，rule3 只匯入標準函式庫 |
| 寫 record 前 `git status --short --untracked-files=all` | 無輸出；寫入後的末次核對應只有本 audit record 新增，忽略的 pytest／Python caches 不列入 tracked delta |

首次兩個 pytest 程序因工具在 10 秒回傳 session 而短暫重疊，均已等待完成；沒有把其部分輸出當成成功。兩者的 setup errors 來自 pytest `tmp_path` 對預設外部暫存根目錄的探查，錯誤為 `PermissionError: [WinError 5]`。這次預設探查被 sandbox 拒絕；我沒有自行列舉、讀取或修復該外部目錄。它不是本次產品斷言失敗，也沒有被記為 PASS。後續兩次重跑序列執行，以各自獨立的 worktree 內暫存目錄完成。這項初始嘗試保留於此，供 dispatcher 作存取紀錄核對，不能由最終測試通過抹去。

成功重跑的 PowerShell 設定如下；第二次將 `r1-tmp-q` 換成 `r1-tmp-rx`，末行加 `-rxX`。只設定子程序環境，未修改 pytest 設定檔。

```powershell
$env:PYTEST_ADDOPTS = '--basetemp=.pytest_cache/r1-tmp-q'
$env:TMP = Join-Path (Get-Location) '.pytest_cache'
$env:TEMP = $env:TMP
python -m pytest -q
```

第一次成功重跑完整 stdout：

```text
........................................................................ [ 12%]
........................................................................ [ 25%]
........................................................................ [ 38%]
........................................................................ [ 51%]
........................................................................ [ 64%]
........................................................................ [ 77%]
........................................................................ [ 90%]
...................................................                      [100%]
555 passed in 2.55s
```

第二次成功重跑完整 stdout（`-rxX`）：

```text
........................................................................ [ 12%]
........................................................................ [ 25%]
........................................................................ [ 38%]
........................................................................ [ 51%]
........................................................................ [ 64%]
........................................................................ [ 77%]
........................................................................ [ 90%]
...................................................                      [100%]
555 passed in 2.21s
```

額外的 `python -c` 檢查沒有建立測試檔或修改產品。整數路線是 `[1]`、`[2,8,10]`、`[1,7,8,9,10]`、`[2,3,6,8,9,10]`；每條窮舉 `LOW/MEDIUM/HIGH_ALERT/None` 的全部組合，單向與每個合法來回 k 都測。獨立預期單向 mask 用 `5 * end > 4 * T`（整數運算，沒有引用產品的 Fraction helper），來回用 k 個 False 接 n-k 個 True；只取 mask 內分類集合，依 HIGH_ALERT／None 是否存在決定 FAIL／UNKNOWN／PASS，逐次比對完整回傳 tuple，共 29,892 次。

額外浮點檢查取 `(end,T) = (0.8,1.0)、(0.232,0.29)、(8000.64,10000.8)`；每組的 end 本身及 `math.nextafter(end, -inf/+inf)`，以兩段路線驗證第一段 mask 依序為 False／False／True、第二段為 True。額外非法 k 為 `None,-1,0,3,4,True,False,1.0,'1'`，路線 `[1,2,3]`，每次必須 ValueError。AST 直接解析父 `__init__.py` 及 validator 的兩檔；輸出分別為無 imports、`__future__/math/fractions/typing`、相對匯入 `rule3`，與完整原始碼一致。

## Issue AC 與補充驗收逐項判斷

下表測試均位於 `tests/test_rule3.py`，已包含在本次兩個 555 passed 的完整執行中。

| 條件 | 原始證據／對應測試 | 判定 |
| --- | --- | --- |
| AC1／SB9-T1：只有去程有提醒時 PASS | 第 33～37 行 `test_round_trip_with_an_alert_only_on_the_outbound_leg_passes`；同時斷言六段 mask 與 PASS | PASS |
| AC2／SB9-T2：範圍內有提醒優先 FAIL，即使同時缺值 | 第 40～60 行兩種 trip_type 的 `test_*_alert_in_range_fails_even_with_missing_rain_probability`；第 219～235 行測 HIGH_ALERT／None 不同順序。產品 `rule3.py:78`～84 先檢查提醒 | PASS |
| AC3／SB9-T3：無提醒但範圍內缺值時 UNKNOWN | 第 63～71 行 `test_no_alert_but_missing_rain_probability_in_range_is_unknown`，兩種 trip_type；僅驗結果，未擴張為 reason codes 驗收 | PASS |
| AC4／SB9-T4：單向最後 20%，跨入也算 | 第 75～97 行 12 個手算範圍；第 100～137 行 overlap 定義與六條路線的分類窮舉；產品 `rule3.py:122`～124。Reviewer 的整數交叉乘法檢查也相符 | PASS |
| AC5／SB9-T5：範圍外缺值不影響 | 第 149～178 行 `test_segments_outside_the_range_do_not_affect_the_result` 及 `test_missing_rain_probability_only_outside_the_range_still_passes`；窮舉範圍外含缺值／提醒的分類，範圍內固定。產品先按 mask 過濾 | PASS |
| §5 額外 AC：恰等於 0.8 × T 不在範圍內 | 第 78、85、88 行整數與十進位邊界；Reviewer 額外三個精確邊界及相鄰 floats。無 `>=` 或 epsilon 擴張 | PASS |
| §5 額外 AC：來回 k 不合法時明確錯誤 | 第 203～213 行 `test_round_trip_with_an_invalid_outbound_count_is_an_error`、`test_round_trip_with_one_segment_has_no_valid_outbound_count`；產品 `rule3.py:127`～134，k 的型別及 0 < k < n 都核對 | PASS |
| §5 額外 AC：不匯入禁用模組 | 第 303～404 行 checker 自測、兩個檔案的 static import checks、fresh interpreter runtime check；產品實際 imports 只有標準函式庫與本模組，沒有任何 LLM client。父 package 無 imports；不僅依賴有限的禁用名稱清單作結論 | PASS |

## CL-B1-1、CL-B1-6、CL-B1-7 與 H-4

| 條款 | 核對及結論 |
| --- | --- |
| CL-B1-1 | 本 delta 僅合成累計距離與手寫分類，沒有讀私有資料的產品路徑；既有測試未改，不涉及修改理由補件。Reviewer 未執行 experiments/、未使用真實 GPX、未讀保留行程。沒有自行加入尚未定案的 schema 或理由代碼 |
| CL-B1-6 item 1 | `src/moto_copilot/validator/rule3.py` 為單一純函式的公開入口；只用標準函式庫。`validator/__init__.py:7` 僅 re-export；沒有建立其他規則骨架。第 291～298 行測試確認輸入不變、重複呼叫相同、list／tuple 相容。AST／runtime 檢查均通過 |
| CL-B1-6 item 2 | `rule3.py:54`～85 接受同序累計終點、trip_type、k、每段分類或 None，回傳同序 bool tuple 與三值結果。tuple 是不可變的同序清單表示，未改變契約要求；不是被排除的 WeatherSegment／RuleResult schema。型別、長度與範圍不合法時拒絕 |
| CL-B1-6 item 3 | `rule3.py:99`～101 與 122～124 依輸入十進位表示精確比較 4/5 × T；第 140～146 行測單向忽略 k。Reviewer 認為 `repr`／Fraction 是嚴格邊界的實作 HOW：沒有加容差、沒有另定安全範圍。C-8-3 的上游累加捨入限制成立，但本函式不應猜測呼叫者未提供的精度；未發現需裁決的 material ambiguity |
| CL-B1-6 item 4 | 合法 k 的範圍是所有 index ≥ k，與距離無關；第 184～200 行特別測不均勻距離及回程早於最後 20% 的提醒仍 FAIL。非法 k 的錯誤如上；不會因空回程而 vacuous PASS |
| CL-B1-6 item 5 | 完整核對 FAIL > UNKNOWN > PASS，MEDIUM 視為有值且非提醒。產品只讀範圍內分類；AC2／AC3／AC5 與 Reviewer 窮舉相符 |
| CL-B1-7 | 逐讀三個新增程式／測試檔、worklog 與 run record 新增兩列。沒有將保守估計稱 P90／百分位數，也沒有將 70% 提醒當作官方警特報或危險標準。`rule3.py:3`～6 明示為專題策略；第 18 行明示 PASS 不代表去程無雨。沒有把本地檢查稱為 E1 Lite／E2 的結果 |
| H-4：缺漏、失敗、逾時、超出涵蓋範圍 | 本純函式的此類輸入抽象是 None；不在此票判別缺漏原因。範圍內缺值且無提醒為 UNKNOWN，有提醒仍 FAIL；範圍外缺值依契約忽略。第 241～285 行覆蓋空路線、非正／非遞增距離、NaN／inf、非序列、分類長度不符／未知分類、未知 trip_type；第 203～213 行覆蓋非法 k。均為明確錯誤，未預設 PASS。沒有 API／timeout 執行路徑，因此不能把這些測試當成實際預報失敗或 timeout 整合已驗證 |
| H-4：Planner 改寫規則結果／計畫狀態 | 模組未匯入 Planner，回傳 NamedTuple 與不可變 bool tuple；本票沒有 Planner 合併或計畫狀態流程。前者已核對，後者不在 Ticket operating scope，保留 G-VAL 後續驗收，未宣稱整個產品已保證不可改寫 |
| H-4：規則 5 未通過不顯示計畫狀態 | 本票沒有規則 5、計畫狀態、模板或 UI；不適用於本 Ticket，未標該整合行為 PASS |
| H-4：矛盾或無法驗證時不採用路線 | 本票沒有路線採用流程；不適用於本 Ticket，未標產品路線採用 gate PASS |

## E-1～E-5 的 evidence sufficiency

| 要求 | 獨立判斷 |
| --- | --- |
| E-1 | Worklog 第 71～103 行保存 `47f1cdb` 上兩個指定 `.venv` 命令的完整 stdout、exit 0 及無 xfail／skip 的陳述；implementation 此後未變。Reviewer 按本次派工改用 PATH Python，限定暫存後兩次獨立重現 555 passed。沒有假稱已使用或驗證外部 `.venv` |
| E-2 | Worklog 第 111～126 行逐條映射五個 Issue AC、三個額外 AC、CL-B1-6 的 range/result/purity 及 H-4 到測試。已自行核對實際斷言與執行結果，足以支持本票 coverage |
| E-3 | Worklog 第 147～149 行交代合成來源；tests 第 3～5 行及所有新案例可追溯為人工距離／分類，沒有座標、軌跡、真實時間、行程識別或外部預報。差異僅此三個程式／測試新增檔及 records，不需私有資料支持 |
| E-4 | Worklog 第 151～153 行記「沒有」。git diff 確認既有測試無修改，成立 |
| E-5 | Worklog 第 155～164 行記錄 H-4 self-verification；我按高風險 decision §5 最低核對範圍逐項核對如上。H-1／H-2 的新產品路徑不涉及；依 SPEC-B1 §5 #8 列，不因分類判定而新增 H-3 門檻宣稱工作。沒有以 Executor 的 mutation 表代替獨立驗證 |

## Findings 與既有 follow-ups

**沒有 finding：blocking 0，non-blocking 0；無 required fix。** 全套初次執行的暫存權限錯誤經 confined rerun 解決，沒有 evidence 顯示為本 delta 的產品缺陷；它的執行限制已完整揭露。沒有用未驗證的 mutation 數字或其他 Ticket 的 PASS 作為本票驗收的依據。

Worklog 第 181～184 行的 C-8-1（k 的產生與 WeatherSegment 整合，owner：Design Authority／G-VAL）、C-8-2／C-8-4（既有文件現況文字，owner：AB-12）、C-8-3（上游浮點捨入，owner：後續 producer／整合工作；有 material ambiguity 時 Design Authority）維持既有 tracked items。這些沒有構成本 Ticket 的新增 finding 或未決契約問題，也不在本次新增工作。C-8-3 的本票處理理由見 CL-B1-6 item 3 列。

## NOT VERIFIED、NOT RUN 與 required authority

| ID | 項目／理由 | Required authority／處理 |
| --- | --- | --- |
| NV-1 | Executor worklog 第 128～145 行的 14 個 mutation 原始腳本／原始輸出不在 worktree，**NOT VERIFIED**；只核對到記錄的主張，未讀取所引用的外部路徑，未修改產品重跑 mutations | Executor／dispatcher 可在已授權範圍提供可審原始證據。非 E-1～E-5 必要條件，本 verdict 不依賴該數字 |
| NV-2 | 真實騎乘資料、真實路線與預報之結果及上游 k 產生的正確性，**NOT VERIFIED／NOT RUN**；合成測試不能證明真實資料結果，且沒有私有資料授權 | **acceptor**（RB-7，必須明確路徑授權；holdout 解封另受凍結限制）。本票不需要這些資料才能驗收 |
| NV-3 | Primary 當次完整 rollout binding／存取核對及本檔原樣複製 hash，**NOT VERIFIED by reviewer**；受審 HEAD 的事件 35 尚為進行中，且禁止存取 worktree 外路徑 | **dispatcher／Orchestrator**，依 Bindings §3.3 在採用產出前核對並更新事件 35。須連同上列初次 pytest 暫存探查核對；不能以本 verdict 代替 qualification／全程 binding 驗證 |
| NV-4 | E2 Oracle、E1 Lite／E2 正式執行、reason codes、WeatherSegment／RuleResult schema、鄉鎮對應、預報讀取、其他 Validator 規則及 UI，**NOT RUN**，均為 Issue 排除範圍 | 後續適用 Spec／Design Authority；正式實驗執行權限為 acceptor。本地的分類窮舉不是 E2 Oracle 或正式實驗結果 |
| NV-5 | 跨 Ticket 整合、SPEC-B1 全部 Spec AC、SIA closure 與 phase acceptance，本次未執行 | Orchestrator 另派 `primary_reviewer` 作 SIA，再由 Design Authority 作 phase acceptance；本 R1 不兼作 SIA、不宣告整份 SPEC-B1 完成 |

本結論僅為上述 subject 的 Ticket R1：五個 Issue AC、三個補充 AC、適用 clarifications 與證據要求均有足夠證據；沒有需 targeted correction 的 blocking finding。Audit 產出的正式採用仍須完成 dispatcher 的 binding 與存取核對；不以本 record 宣告 work item／run／release completion。

Verdict: PASS
