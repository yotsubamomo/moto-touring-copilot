# Issue #13 — cycle 1 R1 independent audit

- Work Contract：OC-1（`docs/governance/records/outcome-contract.md`）→ SPEC-R1 v1（`derivation-spec-r1.md` §2、§4、§5 R1-1 與 E-1～E-6）＋CL-R1-11（`decision-20261118-issue10-c107.md` §3.2）＋CL-R1-12、CL-R1-13（`decision-20261118-issue13-c131.md`）→ Issue #13（派工附原文，所述 SHA-256 `d432868613aac749018d14bf79e45ca06673508e9e3e8d9919c34bd432456584`）。未呼叫 GitHub。
- Subject：本專用 worktree 的 detached HEAD `e173d5c0a98b0a3384e1dbdea2867e589ebce3c9`；BASE `1fd1de3585ea23f80842ac3276fe9305369b51e3`。Implementation commits：`153adcadfdf02f3697ba47f8912ac444c1a3f8d3`、`6ec1903632a1fbff90405de2627eb9dee5d51950`。
- Audit kind：**Ticket independent audit, R1, cycle 1, not a Spec Integration Audit**。
- Role：`primary_reviewer`（Codex）；日期：2026-11-18。

## Assurance 與 binding

| 項目 | 實際證據與界限 |
| --- | --- |
| Independent context | 本次為 fresh Codex thread，輸入是 bounded pack、專案指示與受審識別，未繼承 Executor 對話；worklog 的結論只作待核對主張，自行讀取來源與執行檢查。 |
| Verifiable binding | 依 Bindings m3 §3.3 O-6，qualification 已在 §8.2 #7 記錄；本次 assignment 的 rollout、全部 turn 的 model／effort／sandbox 核對由 dispatcher 記入 `run/run-20261117-oc1-run2.md` 的本次 R1 dispatch event。本 subject 的該 run record §6 **只到事件 63，尚無本次 R1 dispatch event 或核對結果**，不能冒稱事件 61～63 是本 review 的 binding。見 NV-B1；採用本 record 前須由 dispatcher 補記核對，Reviewer 不讀 worktree 外的 rollout。 |
| Autonomous access | 在此 worktree 自行讀治理、契約、程式、測試、fixture、git 歷史與 diff，並以 PATH 的 `python` 執行測試與記憶體探測；pack 未限制必要追查。未讀取 worktree 外檔案、私有資料或憑證。 |
| Self-written record | 本檔由本 Reviewer 自寫，沒有委派或由 Executor 代寫。唯一新增檔案為本 audit record；未改實作、測試、契約或其他紀錄，未 stage／commit。dispatcher 依 Bindings §3.3 核對 status、作者事件與原樣複製的 SHA-256。 |
| Model diversity（與 independence 分開） | Executor 的實際 model 為 `claude-opus-5-5`／`high`，證據為 run record §6 事件 61、63（最後核對 113 則）；本 Reviewer 為 Codex。本 subject 尚無本次 Primary 的實際 model／effort binding 核對，不能把 run record §2 的預期 `gpt-6.1-sol` 當成執行證據：**no model diversity claim**。 |

## 審查範圍與依據

已讀 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md` 的角色／紀錄規則、Project Bindings m3（含 O-6、assurance、record-only paths）；package v2.2 治理 §2.3、§3.8、§4.1～§4.7，impl-default v2 §6、§7，以及 orch-default v2.2 的 audit dispatch／closure／subject identity 規則。最後一行採本次派工明定的 `Verdict:` 格式。

契約追溯核對 OC-1 §2.1 item 2、AB-2、AB-13；SPEC-R1 的引用段落、DD-R1-1／DD-R1-2、CL-R1-1～10、R1-1 與共通證據要求；CL-R1-11～13；`DESIGN.md` §5 共通規則、契約 1、2、4；SPEC-001 §2 ID、§9 S37／S58。亦核對 first-run derivation 的範圍與 G-RTE、SPEC-B1 CL-B1-2、CL-B1-8、high-risk decision §5、run 事件 61～63 與 Issue #13 worklog。DD-R1-2、CL-R1-2～10 是其他 R1 Tickets 的要求，未據此擴張 #13。

`git log` 與各 commit 的檔案清單證實 BASE 後只有兩個 implementation commits；其餘均在 `docs/governance/records/**`。完整 source／test delta 涵蓋 contracts 四個檔案、`routes/catalog.py`、fixture、`tests/test_contracts.py`、`test_eta.py`、`test_integration_b1.py`。未更動 Plan Schema、RouteSnapshot schema、request_key、目標 GPX 雜湊欄位、路段／檢查點產生規則。沒有把 Spike 收編、真實路線驗證或 Spec integration 宣告為已完成。

## 實際檢查與結果

所有命令在此 worktree 執行；未覆寫 `PYTEST_DEBUG_TEMPROOT`，未直接以 `.venv` 路徑啟動 Python。`sys.executable` 的觀測值是 `C:\Users\yotsu\AppData\Local\Temp\cx13r1\.venv\Scripts\python.exe`（只觀測直譯器識別，沒有讀取該目錄內容）。PowerShell 的 `Get-Content` 後續明定 UTF-8，修正首次預設解碼造成的亂碼；過長輸出以指定來源的分段讀取與 `rg -n` 補查。

| 命令／檢查 | 結果 |
| --- | --- |
| `git rev-parse HEAD`、`git log --oneline 1fd1de3..HEAD`、`git log --format='%h %s' --name-only 1fd1de3..e173d5c` | HEAD 與派工一致；7 個 commits，兩個實作，其餘 record-only。 |
| `git diff --stat 1fd1de3..e173d5c`；`git diff 1fd1de3..e173d5c -- src/ tests/`；另分別重讀 schemas／validate／fixture／tests diff | 12 files changed，872 insertions、26 deletions；修改範圍如上。 |
| `git diff 153adca..6ec1903 -- src/moto_copilot/routes/catalog.py`；對照 BASE 的同檔 diff | 僅三個鍵、引用 CL-R1-12 的一行註解、模組說明第一行。無介面、import、路段、checkpoint 或演算法變更。 |
| `git diff 1fd1de3..e173d5c -- tests/test_routes_pace_eta.py` | 空；原契約符合性測試未改。commit 清單也證實 CL-R1-12 的 implementation commit 沒有改任何測試。 |
| `python -m pytest -q` | exit 0；**875 passed in 31.42s**。 |
| `python -m pytest -q -rxX` | exit 0；**875 passed in 26.08s**；無 failed、error、xfailed、xpassed、skipped。 |
| `rg -n 'xfail\|skip' tests/` | 無輸出；未找到任何 xfail／skip 標記。 |
| PowerShell `$env:PYTHONPATH='src'`，接著 `python -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json` | exit 0；`data contracts v0.3`；derived_segments、route_catalog、pace_table、eta_output 全部 `OK`。 |
| `git show 1fd1de3:src/moto_copilot/contracts/validate.py` 與 HEAD 在記憶體以 `ast.parse` 比對所有既有函式（不含位置資訊） | 唯一有變更的既有函式為 `validate_route_catalog`；其餘既有函式 AST 相同，包含 `_whole_count`、契約 1／3／4，#10 修正未回復。 |
| `rg -n` 檢查 contracts 的 pattern 使用處、函式／測試名稱、`$ref`／網路 client 字樣；讀 `tests/conftest.py`、`pyproject.toml` 與 CLI | pattern 共用於要求的所有欄位；沒有遠端 schema reference；新增測試與本機 CLI 沒有網路傳輸。未改 pytest 全域設定、fixture 載入或測試選取。 |
| `PYTHONPATH=src` 的記憶體 ID 探測（`@'…'@ \| python -`） | **7,600 assertions PASS**：R00～R99、RS／RG 的 4 種合法 hex、各自 CP00／01／99／000／100／999、4 種 SN；每個值另拒絕前置空白與尾隨 LF／CR／CRLF／U+2028／U+2029／空白／tab／NUL。CP 編號的產生順序不在本票範圍，未將 pattern 當作編號規則。 |
| `PYTHONPATH=src` 的錯誤型別探測，使用 fixture 的 deepcopy／JSON round trip，詳見 R1-F1 | `route_source=[]`、`{}`、`['trip']`：schema 可回報 enum violation，但兩個驗證 API 均拋出 TypeError。7、False、`'unknown'` 則正常回傳 schema 違反。 |
| `git status --short`（開始與所有驗證後、寫 record 前） | 均為空。寫入本檔後另核對唯一新增檔案。 |

一次以 PowerShell wildcard 傳入 orchestrator-contracts 路徑的 `rg` 因路徑語法失敗（os error 123）；隨即以明確目錄 `rg --files` 找出 `default-v2.2.md` 並直接讀取，沒有影響上述驗證。沒有執行 `experiments/`、發出網路請求或新增探測腳本。

## AC、範圍與 evidence sufficiency

| 條款 | 獨立核對結論 |
| --- | --- |
| 範圍 (a)、AC (1)、S37／S58 的契約部分、CL-R1-13 | `schemas.py:24–32` 的三個 pattern 在 Python `re.search` 下是完整字串、ASCII 數字、小寫 hex；套用到契約 1 nullable route_id、契約 2 三表 route_id／checkpoint_id、契約 4 route_id／break checkpoint。`test_s37_s58_every_route_id_format_passes_in_contracts_1_2_and_4`、各 invalid ID 測試、`test_checkpoint_id_has_two_or_three_digits`、`test_s58_a_snapshot_id_of_another_format_is_rejected` 通過，並有上述獨立邊界探測；R01／R02 維持有效。依語法結構判讀接受集合與 §2＋CL-R1-13 一致，沒有把有限探測說成窮舉所有 hex。 |
| 範圍 (b) | nullable references、三個新必填鍵、兩個 enums、turnaround 均有 schema 與測試；合法資料行為成立。**錯誤 route_source 型別的驗證有 R1-F1，不能將此範圍整體記為完成。** |
| AC (2) | `validate.py:268–273` 比對 checkpoint_id 去除 CP suffix 的前綴，兩欄先通過 pattern 才交叉檢查。`test_checkpoint_id_starts_with_its_route_id` 與 `test_checkpoint_id_of_an_rs_route_starts_with_that_route_id`（含同格式不同 hex）通過。 |
| AC (3) | `_route_source_errors` 對合法來源核對 trip／R、routing／RS、target_gpx／RG，RS 與 SN 的 10 碼相等；兩項一致性測試通過。錯誤來源字串回傳 schema violation；array／object 的完整拒絕報告受 R1-F1 阻擋。 |
| 範圍 (c)、AC (4) | `test_each_contract_2_invariant_has_a_rejected_violation` 五例皆通過。不變條件 3 是同位置可多 checkpoint、以 ID 區別，重複主鍵案例正確表達其違反；沒有新增同位置唯一限制。invariant 4 的缺少／兩個 turnaround、端點、one_way 有 turnaround 均拒絕；內部唯一 turnaround 合法。invariant 5 六種 reference 組合違反皆拒絕。 |
| CL-R1-11 | `validate.py:245–251` 兩個計數均經 `_whole_count`，不可計數由 schema 報錯；`test_invariant_2_counts_whole_number_floats` 包含 5.0／9.0、n=4.0 與 JSON round trip，超界拒絕，界內合法。AST 比對證實未回復 #10 修改。 |
| 範圍 (d)、(e)、AC (5) | CONTRACT_VERSION 為 0.3；fixture metadata 與兩條路線三鍵同步，未改座標、時間與其他數值；`test_fixture_is_marked_as_mock`、`test_r01_and_r02_stay_valid_trip_routes`、`test_mock_fixture_conforms_to_every_contract`、CLI 測試與兩次完整 suite 通過。 |
| 範圍 (f)、CL-R1-12、V-1～V-7 | diff 符合 §5.1 封閉清單；未改測試或加標記，原 `test_build_route_conforms_to_the_catalog_contract` 通過。worklog §3、§5、§6、§8 正確記錄修正、V-1～V-7、歷史失敗與後續通過；三鍵描述既有單向 trip 結構，未收編 G-RTE。 |
| E-1 | worklog §6 保存完整最終 stdout `875 passed in 27.42s` 與舊失敗歷程，沒有把舊失敗作通過證據；本次兩次獨立重跑一致通過。 |
| E-2 | worklog §6 逐 AC 列測試名稱／案例與 S37、S58；對照實際測試及本次 suite 結果成立。但新增邊界缺陷仍須修正，現有 mapping 並不能排除 R1-F1。 |
| E-3 | 新 ID 常數明記 invented；新增案例改 mock fixture 副本，fixture／conftest 明示所有數值是合成；改動沒有新增座標、GPX 或真實軌跡，沒有公開地標座標需另引用。 |
| E-4 | worklog 說明與 source 相符：字串／整數與本機 schema 檢查；無 `$ref`，新增 subprocess 只執行本機 fixture CLI；未引入網路路徑。 |
| E-5 | diff 的既有測試更動均在 worklog 逐項列理由：版本斷言 0.2→0.3；ETA catalog R05～R07 與 integration R08 補三個必填鍵；模組說明改版。原斷言強度未降低；CL-R1-12 未改任何測試。 |
| E-6 | 與 DA 的「不涉及」一致：沒有憑證／私有資料讀寫或輸出位置選擇（H-1／H-2）；沒有 holdout、實驗結果或研究宣稱改動（H-3）；沒有規則 1～5、計畫狀態、路線採用、snapshot 選取或休息需求變更（H-4）。契約欄位驗證不等於產品 Validator 的規則判定。沒有未標示的高風險路徑擴張。 |

## Finding

### R1-F1 — 新增的 route_source 交叉檢查會使合法 JSON 錯誤型別中止整份驗證

- Severity：**Medium / blocking**。
- Owner／required fix authority：Issue #13 Executor（契約內 targeted correction）。
- 契約依據：R1-1 範圍 (b) 的 `route_source` enum 驗證、AC (3) 的來源一致性拒絕，以及 `contracts/validate.py:8–9` 的驗證 API 行為（回傳 violation list）。這是本票新加欄位與 helper 的缺陷，不要求全面重寫舊 validator。
- 證據：`src/moto_copilot/contracts/validate.py:187–191` 在 `source not in _REFERENCES_SET` 對任意 JSON 值做 dict membership。`[]`、`{}`、`['trip']` 不可 hash，拋出 `TypeError`。`validate_route_catalog` 雖已在第 209 行取得 schema 違反，仍在第 266 行呼叫此 helper，導致先前報告遺失；`validate_dataset:507–509` 也因此無法回傳 report。`schemas.py:84` 的 enum validator 本身能正常辨識這些錯誤值。
- 實際重現（`PYTHONPATH=src`，以下 Python 透過 PowerShell here-string 傳給 `python -`；不建立檔案）：

```python
import copy, json
from jsonschema import Draft202012Validator
from moto_copilot.contracts import schemas as S
from moto_copilot.contracts.validate import validate_dataset, validate_route_catalog
d = json.load(open('tests/fixtures/contract_v02/mock_dataset.json', encoding='utf-8'))
for value in ([], {}, ['trip']):
    x = copy.deepcopy(d)
    x['routes'][0]['route_source'] = value
    x = json.loads(json.dumps(x))
    print([e.message for e in Draft202012Validator(S.ROUTE).iter_errors(x['routes'][0])])
    try:
        validate_dataset(x)
    except Exception as e:
        print(type(e).__name__, str(e))
```

實測三個 schema 輸出均為 `<value> is not one of ['trip', 'routing', 'target_gpx']`；兩個 array 的 dataset 結果是 `TypeError unhashable type: 'list'`，object 是 `TypeError unhashable type: 'dict'`。另一輪對 `validate_route_catalog` 的直接呼叫同樣重現，數字、布林與未知字串則正常回傳 violation list。

- 影響與 blocking 理由：輸入只是新欄位的錯誤 JSON 型別，卻無法取得既定的違反報告，連同資料集其他契約的驗證也中止。不能以現有 suite 全綠代替 enum 驗證 API 的完整性；此為範圍內可重現的實作缺陷，不是設計語義問題，也不構成 H-4 的產品 fail-open 宣稱。
- Required fix：對 `route_source` 的型別／合法值先作安全判定，使任何 schema 不接受的來源值由 schema 回報並跳過交叉檢查，不再因 dict membership 拋錯；不得以放寬 enum 或吞掉整份驗證例外處理。新增 array／object（至少 `[]`、`{}`）經 JSON round trip 的 regression cases，斷言直接 catalog API 與 dataset API 回傳對應的 schema violation。保留既有合法來源、來源／ID 一致性、不變條件與三鍵 producer 修正；更新 worklog，重跑完整 pytest、`-rxX` 與 fixture CLI，交 R2 核對。

沒有其他新 non-blocking findings。既有 TI-C13-2、RV-6、RV-7 的 disposition／owner 維持 DA record §3.2、§4：owner Design Authority，後續 contracts derivation／AB-12 文件工作處理，不是 #13 補做要求。C-13-3 的已揭露搜尋偏差由 run 事件 61 記錄且事件 62 明示不在 DA 裁決內；未取得 transcript，未另宣稱已獨立核對該次存取。

## NOT VERIFIED 與後續 authority

- **NV-B1（dispatcher）**：本次 Primary 的 rollout binding、session id、實際 model／effort／sandbox、作者事件及原樣複製 hash 未在受審 run record 出現。禁止讀取 worktree 外路徑，因此本 Reviewer 不自行核對或虛構 dispatch event 編號。required authority＝Orchestrator／dispatcher，依 Bindings §3.3 在採用本 record 前補記本次 R1 dispatch event 並核對；不以本檔自稱 Codex 取代 binding 證據。
- **NV-PRIV（acceptor）**：沒有核對真實 GPX／私有路線、holdout 或任何需要私有資料的行為；無授權且不屬本票 AC 的充分證據要求。required authority＝acceptor；本次完全沒有取得這些資料。
- **NV-EXP（後續執行 work item）**：`experiments/` 呼叫 `build_route` 的實際行為未執行、未核對；依 CL-R1-12 record §6 與 worklog C-13-6，歸之後執行它們的 work item，需要私有資料時 required authority＝acceptor。本 record 未執行任何 experiments 腳本。
- **NV-ACCESS（dispatcher）**：run 事件 61 所述 Executor 歷次存取與 C-13-3 的 transcript 不在此 worktree，未獨立重查；僅核對已持久化的揭露與處置記錄，未把它說成存取紀錄全面通過。

本結論限上述 Ticket subject；未作 Spec Integration Audit、phase acceptance、Ticket closure 或 release 決定。現有 suite 與 CLI 通過，但 R1-F1 尚未修正。

Verdict: BLOCKING
