# Issue #13 — cycle 1 R2 closure review

- Work Contract：OC-1（`docs/governance/records/outcome-contract.md`）→ SPEC-R1 v1（`decisions/derivation-spec-r1.md` §2 引用段落、§4 DD-R1-1／DD-R1-2、CL-R1-1～10、§5 R1-1 與 E-1～E-6）＋CL-R1-11（`decision-20261118-issue10-c107.md` §3.2）＋CL-R1-12／13（`decision-20261118-issue13-c131.md`）→ Issue #13（本次 pack 附原文，所述 body SHA-256 `d432868613aac749018d14bf79e45ca06673508e9e3e8d9919c34bd432456584`；未呼叫 GitHub）。
- Subject：本專用 worktree，detached HEAD `be76a977f9b8561b27f28640f180923103f4537b`；BASE `1fd1de3585ea23f80842ac3276fe9305369b51e3`；R1 subject `e173d5c0a98b0a3384e1dbdea2867e589ebce3c9`。Correction commit `3c065f8`；整體 implementation commits `153adca`、`6ec1903`、`3c065f8`。
- Audit kind：**Ticket R2 closure review, cycle 1, not a Spec Integration Audit**。
- Role：`primary_reviewer`（Codex）；日期：2026-11-18。

## Assurance 與 binding

| 項目 | 滿足方式、證據與界限 |
| --- | --- |
| Independent context | 本次為 fresh Codex thread，未繼承 Executor 或 R1 的對話。從磁碟重讀 `audit/issue-13-c1-r1.md` 全文、修正後 source／test、worklog §9 與 git diff；Executor 的結論均作待驗證主張。 |
| Verifiable binding | Bindings m3 §3.3 O-6 與 §8.2 #7 記錄 Codex qualification。當次 rollout 的所有 turn model／effort／sandbox、存取路徑與作者事件由 dispatcher 核對並在 run record 的**本次 R2 dispatch event**記錄。受審 `run/run-20261117-oc1-run2.md:142–143` 只有事件 **64（R1）及 65（Executor correction）**，尚無 R2 dispatch event；不能虛構事件 66 或引用 64 作本次 binding。見 NV-B2：採用本 record 前由 dispatcher 補記並核對，四項 independence 的完整成立仍以該核對為必要條件。 |
| Autonomous access | 自行取得 worktree 內治理、契約、程式、fixture、測試與 git 歷史；在記憶體載入 BASE／R1／HEAD 的追蹤中程式進行比較。沒有以 Executor 挑選的摘要代替原始證據；未讀取任何 worktree 外路徑、私有資料或憑證。 |
| Self-written record | 本 Reviewer 自行撰寫本檔，沒有委派、由 Executor 代寫或修改受審物。唯一新增檔案為本 audit record，未 stage／commit。dispatcher 依 §3.3 核對 status、rollout 作者事件與原樣複製的 SHA-256。 |
| Model diversity（與 independence 分列） | Executor 實際 model／effort：`claude-opus-5-5`／`high`，run 事件 65 記錄同一 agent `a95eaf00e5bb8b468` 的 128 則觀測；事件 61、63 是前段證據。本 Reviewer 是 Codex；受審 run 尚無本次 Primary 的實際 model／effort 核對，不能以事件 64 的 `gpt-6.1-sol` 或預期 mapping 充當本次執行證據。**no model diversity claim**。 |

## 範圍與依據

依治理 v2.2 §2.3、§3.8、§4.1～4.7、Bindings §3.3、implementation profile §6～7 與 orch-default v2.2 的 subject／closure 規則，僅判斷 R1-F1 是否解決、修正有無回歸、以及直接產生或暴露的 blocking defect。不是第二次不限範圍的 R1；不作 phase acceptance、Ticket completion 或 release 決定。角色 definition 的紀錄要求依循 `.claude/agents/gov-primary-reviewer.md`，最後一行採本次派工明定的 `Verdict:` 格式。

契約核對聚焦 SPEC-R1 §5 R1-1 的新增來源欄位、AC (3)、AC (5)、E-1～E-6；對照 DESIGN §5 契約 2 不變條件 5、SPEC-001 §2 ID 與 §9 S37／S58，以及 CL-R1-11～13。其餘 DD／CL、first-run derivation、SPEC-B1 CL-B1-2、CL-B1-8 與 high-risk decision §5 用於確認既有範圍與證據規則，沒有把 R1-2～R1-4、G-RTE 或文件同步納入本次補做要求。

已讀 root `CLAUDE.md`、Bindings、角色定義、R1 record、worklog（含 §9）、run 事件 61～65、上述契約及治理適用段落。初次 PowerShell `Get-Content` 未明定 UTF-8，輸出有亂碼，後續以 `-Encoding utf8` 重讀；長輸出截斷的關鍵條款以指定檔案的分段讀取補查。

## 實際檢查

全部命令在本 worktree 執行。使用 PATH 上的 `python`，未以 `.venv` 路徑啟動 Python、未覆寫 `PYTEST_DEBUG_TEMPROOT`。記憶體檢查確認 `sys.executable` 位於本 worktree 內；觀測 `PYTEST_DEBUG_TEMPROOT=C:/Users/yotsu/AppData/Local/Temp/cx13r2/.venv/tmp`。

| 命令／檢查 | 實際結果 |
| --- | --- |
| `git rev-parse HEAD`；`git status --short` | HEAD 與派工一致；開始時 status 為空。 |
| `git log --oneline 1fd1de3..be76a97`；`git log --format='%h' --name-only e173d5c..be76a97` | BASE 後 11 commits；R1 後 4 commits。唯一 source／test correction 為 `3c065f8`；`e5dfe5e`、`b0491d2`、`be76a97` 均只改 `docs/governance/records/**`。 |
| `git diff e173d5c..be76a97 --name-only`；`git diff e173d5c..be76a97 -- src/ tests/`；run record 的同範圍 diff | 只有 validate helper 的型別守衛與 test 的四個參數案例，以及 R1、worklog、run records；沒有附帶實作。 |
| `git diff --stat 1fd1de3..be76a97`；`git diff 1fd1de3..be76a97 -- src/ tests/` | 13 files，1103 insertions、26 deletions；整體 diff 用於定位與確認修正未撤回既有變更，未另作不限範圍 audit。schema、producer 三鍵、fixture、既有斷言均未被 R2 correction 改動。 |
| `python -m pytest -q` | exit 0；**879 passed in 25.77s**。 |
| `python -m pytest -q -rxX` | exit 0；**879 passed in 17.18s**，無 failed／error／xfailed／xpassed／skipped 摘要。 |
| `$env:PYTHONPATH='src'` 後 `python -m moto_copilot.contracts tests/fixtures/contract_v02/mock_dataset.json` | exit 0；`data contracts v0.3`；derived_segments、route_catalog、pace_table、eta_output 全部 `OK`。 |
| `rg -n 'xfail\|skip' tests/` | 唯一命中 `tests/test_contracts.py:1157` docstring 的英文 `skipped`，描述來源交叉檢查跳過；不是 pytest 標記。未將文字命中誤報為 skip。 |
| `rg -n 'pytest\.(mark\.(xfail\|skip\|skipif)\|xfail\|skip\|importorskip)\|from pytest import.*(skip\|xfail)' tests/`；另以 Python AST 掃描 tests 下所有 `.py` 的 Name／Attribute | rg 無命中（exit 1）；AST 無 xfail／skip／skipif／importorskip 標記或呼叫。確認沒有測試 bypass。 |
| 指定檔案 `Get-Content -Encoding utf8`、`Select-Object -Skip/-First/-Last`、`rg -n`；指定 package references 目錄 `rg --files` | 核對治理、contract、worklog、R1、run、source／test 行號與設定；`pyproject.toml` 的 pytest 路徑仍為 src／tests。未執行 experiments。 |
| `$env:PYTHONPATH='src'; @'…'@ \| python -` 記憶體 regression 探測（下述） | exit 0；13 種 invalid JSON 值 × 兩個 APIs 全部回傳 schema-only violation，helper 回傳空 list。 |
| 同一記憶體探測：R1 helper 與 HEAD 的行為比較 | 8 種原本不拋錯的來源值 × 4 種 route_id × 4 種 reference 組合＝**128 cases 相同**。 |
| 同一探測：`git show <BASE/R1/HEAD>:src/.../schemas.py`、`validate.py` 及各自 mock fixture，以 `compile`／`exec` 在記憶體載入 | C-13-7 六個欄位位置 × `[]`／`{}` × 三版＝**36 個相同 TypeError**；沒有匯出檔案、沒有執行歷史腳本或讀取其他 checkout。 |
| 同一探測：R1 與 HEAD 所有頂層既有函式 AST 比對（忽略位置） | 唯一不同函式為 `_route_source_errors`。沒有吞掉例外的 correction，其他 validator 函式不變。 |

記憶體 regression 探測將 fixture 的 `routes[0].route_source` 逐一設為 `[]`、`{}`、`['trip']`、`{'trip':'trip'}`、`None`、`True`、`False`、`0`、`7`、`1.5`、空字串、`unknown`、`Trip`，每次 deepcopy 後經 `json.loads(json.dumps(x))`。直接 catalog API 斷言只有一筆 `routes[0] schema: route_source: … is not one of …`；dataset API 斷言四個 report keys 完整、route_catalog 與直接結果相同、其他三份為空；另斷言 helper 回傳 `[]`。這些是實際 assertions，未只檢查「沒有例外」。schema 的 `ROUTE_SOURCES` 另斷言精確等於三個合法字串。

128-case 比較的來源值為 `trip`、`routing`、`target_gpx`、`unknown`、空字串、`None`、`True`、`7`；route_id 為 R01、合法 RS／RG、bad；references 為四種有值／null 與一致／不一致組合。合法來源的檢查路徑不因新守衛而改變；suite 亦涵蓋合法三種來源、ID／snapshot 一致性、契約 2 不變條件 1～5、CL-R1-11 與 producer 三鍵。

## Finding closure

### R1-F1 — RESOLVED

- 原 severity：**Medium / blocking**；本次狀態：**RESOLVED**，沒有殘留 blocking。
- 依據：R1-1 範圍 (b)、AC (3) 及驗證 API 回傳 violations 的行為；R1 record 的 required fix。
- Evidence：`src/moto_copilot/contracts/validate.py:187–192` 在任何 dict lookup 前先作 `isinstance(source, str)`，Python `or` 短路使非字串不執行 membership。非法字串也返回空交叉檢查結果，由 `validate_route_catalog:210–211` 的 schema 階段回報。`schemas.py:13`、`:84` 的三值 enum 未放寬，沒有 try／except 吞掉錯誤。
- Regression evidence：`tests/test_contracts.py:1154–1166` 的四例都先 JSON round trip，再呼叫 catalog／dataset APIs，檢查 schema violation、交叉檢查沒有誤執行、四份 report 完整、其他契約結果不變；至少 `[]`、`{}` 皆有。879-test suite 兩次通過，加上上述 13-value 探測與 128-case 比較。
- Required fix 核對：安全型別／合法值守衛、schema 報告、跳過來源交叉檢查、不放寬 enum、不吞例外、兩 API 的 array／object round-trip regression、worklog §9 與完整 pytest／`-rxX`／CLI 證據，均已滿足。沒有額外 required fix。

## Correction 直接產生或暴露缺陷的核對

**沒有新的 blocking 或 non-blocking findings。** C-13-7 維持既有 tracked concern，不重開為本次 finding：

- 獨立使用每版自身 schemas、validator 與 fixture，分別把 routes.route_id、route_segments.route_id、checkpoints.route_id、checkpoints.checkpoint_id、derived_segments.route_id、eta_headers.route_id 的第一筆改成 `[]`／`{}`。三版均在 `validate_dataset` 拋同型、同訊息的 TypeError。
- `validate.py:53` 的 `_duplicates` 與 catalog 的主鍵／route_ids 集合邏輯（`:212–222`）是既有路徑；R1 已能在合法來源下獨立重現 ID 的錯誤型別失敗。新守衛只依 `route_source` 提前返回 helper，不更動 ID 值、集合操作或 API 呼叫順序。這些案例在不觸發 R1-F1 的輸入就存在，不是修復它之後才到達的新路徑。
- 結論：C-13-7 雖在 Executor correction 期間的廣泛探測被發現，**不是本 correction 直接產生或暴露的 blocking defect**。本次只判斷其與 correction 的因果關係，不對其範圍外風險作全面接受。
- Disposition／owner：依 run 事件 65、worklog §9.3／9.6，保留 tracked item，由 **Design Authority** 在後續 contracts 工作處理；本 R2 不擴張 required fix，也不將它記為已修復。TI-C13-2、RV-6、RV-7 同樣維持 DA 原 disposition；沒有新增實作授權。

## 共通證據與限制

E-1：worklog §9.4 保存兩次完整 stdout（879 passed）與 CLI；本次獨立重跑一致。E-2：原 §6 的 AC／S37／S58 mapping 保留，§9 明列 R1-F1 regression；本次補核 correction 的證據充足。E-3：新增案例僅修改合成 fixture 副本的來源欄位，無新座標、軌跡或真實雜湊。E-4：correction 無傳輸、遠端 schema reference 或網路 client；探測與 CLI 均本機。E-5：correction 只新增一個參數化測試，不改既有測試；原契約改版理由保留於 §6。E-6：R1-1 的「不涉及」未改變：型別守衛不讀寫憑證或私有資料、不決定輸出位置（H-1／H-2）、不改 holdout／實驗／宣稱（H-3）、不改產品規則結果、狀態或路線採用（H-4）。沒有以測試全綠宣稱真實騎乘或整份 Spec 已驗收。

## NOT VERIFIED 與 required authority

- **NV-B2 — dispatcher／Orchestrator**：受審 run 尚無本次 R2 dispatch event 與 binding 核對。採用本 record 前依 Bindings §3.3 補記本次 session、全部 turn 的實際 model／effort／sandbox、存取與作者事件、status 及原樣複製 hash；不得借用事件 64。Reviewer 不讀 worktree 外 rollout。這是 audit 採用所需核對，並非本次新 implementation finding。
- **NV-PRIV — acceptor**：真實 GPX／私有路線、holdout 及所有需要私有資料的行為未驗證；未授權且不在本票合成測試 AC 內。未嘗試取得資料。
- **NV-EXP — 後續執行 work item；需要私有資料時 authority＝acceptor**：C-13-6／DA record §6 的 experiments 實際行為仍未驗證；本次未執行任何 experiments 腳本。
- **NV-ACCESS — dispatcher／Orchestrator**：Executor 的歷史 transcript 不在 worktree，未獨立重查 C-13-3 的原始存取；僅讀 run 事件 61～65 與持久化揭露。事件 64 補足的是 R1 的 dispatcher 核對，不能推作本次或 Executor 歷次存取的獨立證明。

本結論僅涵蓋上述 Ticket R2 subject 與 correction。R1-F1 已解決，未發現 correction 引入回歸或直接產生／暴露的新 blocking defect；正式採用本 record 仍須完成 NV-B2 的 dispatcher 核對。

Verdict: PASS
