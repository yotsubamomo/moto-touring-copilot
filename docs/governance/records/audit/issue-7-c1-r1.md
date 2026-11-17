# Issue #7 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`，acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`）→ Issue #7「B1-1 contracts」 |
| Subject BASE | `ff049661f968adace4dd017cf560316e5684440d` |
| Subject HEAD | `84fdbfc44ab13ca161758b314d637ef57ddf207e`，本 dedicated worktree 的 detached HEAD |
| Implementation | `a304ee2ac0ec3d8468e446b089216f0cb000f72b`；其後兩個 commits 僅修改 `docs/governance/records/**` |
| Audit kind | **Ticket independent audit，R1，cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`（Codex） |
| 日期 | 2026-11-17 |
| Run record | `docs/governance/records/run/run-20261117-oc1-issue7.md` |
| Executor worklog | `docs/governance/records/worklog/issue-7.md`，僅作待驗證主張與 evidence 入口 |

## Assurance 與 independence

| (a) Context independence：四項 properties | (b) 實際 models 與 binding evidence |
| --- | --- |
| **Independent context**：依本次 fresh Codex thread 的 bounded dispatch 開始；沒有 Executor 的對話或先前 Reviewer context。自行閱讀原始契約、程式、測試、diff 與 records，沒有採用 Executor verdict。 | Executor：run record §5 事件 2 記載 `gov-executor`、agentId `a9f372411c0f54099`，派工者觀測 `claude-opus-5-5`／`high`，120 則。此為 worktree 內的派工者證據，未存取外部 transcript。 |
| **Verifiable binding**：依 Bindings m3 §3.3 的 qualified Codex mapping 執行。當次全部 `turn_context`、sandbox、存取路徑及 record SHA-256 由 dispatcher 核對並填入 run record 的 **§5 事件 7「派 R1」binding 欄位**，本 record 引用該欄。 | Primary：本 review 由 **Codex** 執行；run record §1 第 4 項、§5 事件 7 宣告 mapping 為 `gpt-6.1-sol`／`high`，sandbox 機制為 `workspace-write`。在受審 HEAD 該欄仍是「派工中」，沒有本次完整 rollout 的事後核對結果；不得將預期 mapping 當成已獨立觀測的實際 model。 |
| **Autonomous access**：自行使用 worktree 內檔案、`git show`／`git diff`／`git log`，使用 PATH 的 `python` 跑測試與記憶體內合成檢查；pack 不是 coverage 上限。未讀取 worktree 外路徑、`data/`、`.env`，未使用網路。 | **no model diversity claim**。Bindings §5 未宣告 diversity 關係，且此 worktree 尚無本次完整 binding 的事後證據；不以產品名稱推定 diversity。Alternate 本次未派工。 |
| **Self-written record**：本檔由本 `primary_reviewer` 自行撰寫；唯一新增檔案就是本檔。沒有修改、stage 或 commit 實作、測試、契約或其他 records。dispatcher 依 Bindings §3.3 原樣複製並核對 hash，不得改寫本結論。 | 正式採用本 audit 前，dispatcher 仍須完成上述 R1 binding 欄位的核對。本 review 不存取 rollout 所在的 worktree 外路徑，也不自證該項外部程序已完成。 |

## 契約與受審範圍

已閱讀 root `CLAUDE.md`、Bindings m3、`.claude/agents/gov-primary-reviewer.md`，以及採用的治理本文 §2.3、§3.8、§4.1–§4.7，`impl-default` v2 §6–§7，`orch-default` v2.2 的 execution／routing／completion predicates。本文的 finding 分類與唯讀限制依上述規範；最後一行格式依本次派工指定。

契約來源包括 OC-1、SPEC-B1 v1、`decision-20261117-oc1-first-run-derivation.md`（特別是 BD-3）、CL-B1-8 的 `decision-20261117-issue7-spike-tests.md`、`decision-20261117-issue7-h2.md`，以及 `decision-20261117-high-risk-categories.md`。核對 `DESIGN.md` §5、§6.1、SPEC-RESOLUTION-001 §1.4 與相關算式／測試條款、SPEC-001 的相關停等條款、BATCH-1 索引。未將未 Freeze 的其他 Plan Schema 內容當成 #7 的新增要求。

Issue #7 使用 dispatcher 在 pack 重現的全文。`updatedAt=2026-11-15T11:10:55Z`、UTF-8 body SHA-256 `a59c9f93f6d9b6b7259948f189c2185804309b1457be968a001223606c339af7` 均為 **dispatcher-provided provenance**；與 BD-3 記載一致，未重新抓取 GitHub，也未聲稱自行核對線上 body。

實作範圍是契約 1、3、4 的已核准停等欄位、驗證、fixture 與相關測試，並包含 CL-B1-8 授權的測試拆分。ID 放寬、契約 2、產生者 #9–#11、Plan Schema、真實資料回歸、E1／E2、SPEC-B1 Spec Integration Audit 與 phase acceptance 都不是本次交付。

## Finding

### R1-F1 — 新增 numeric 欄位接受 NaN，繞過不變條件

- **Severity：Medium；blocking。** 這是 Issue #7 明文 AC／H-4 的驗證缺陷，並非風格建議：無法核對停等比例的資料仍被判定為符合契約，且輸出保有 `status=ok` 的完整 ETA。
- **契約依據**：Issue #7 AC1（短停留不得大於總停留）、AC3（`default` 必為 0.20）、AC5（可核對的停等乘式）；新增欄位須是非負 number。另見 `DESIGN.md:325` 的缺值規則、`:374`、`:484`、`:494`、`:535`，以及高風險類別 record §5 H-4 的缺漏／失敗不得放行要求。
- **程式證據**：`src/moto_copilot/contracts/validate.py:60` 的 `_is_number` 只檢查 `int/float`，接受 `float('nan')`；`:115` 的 `short > stopped`、`:199` 的 `abs(coeff - 0.20) > tolerance`、`:353` 的乘式誤差比較，遇到 NaN 都得到 False，沒有加入 violation。`schemas.py:22`、`:26` 的 `minimum` 也沒有在目前 jsonschema 行為下拒絕 NaN。
- **實際重現**：在記憶體複製既有 mock fixture，每次只更改一個欄位；使用 `python -B -` 執行下列程式（工作目錄為本 worktree）：

```python
import copy, json, sys
from pathlib import Path
sys.path.insert(0, "src")
from moto_copilot.contracts import validate_dataset, validate_pace_table

base = json.loads(Path("tests/fixtures/contract_v02/mock_dataset.json")
                  .read_text(encoding="utf-8"))
for field in ("short_stop_time_s", "stop_ratio", "margin_coeff", "stop_allow_s"):
    d = copy.deepcopy(base)
    target = (d["derived_segments"][0] if field == "short_stop_time_s" else
              d["pace_categories"][1] if field == "stop_ratio" else
              d["pace_header"] if field == "margin_coeff" else d["eta_segments"][0])
    target[field] = float("nan")
    try:
        print(field, validate_dataset(d))
    except Exception as exc:
        print(field, type(exc).__name__, str(exc))
    if field == "margin_coeff":
        print("pace alone", validate_pace_table(
            d["pace_header"], d["pace_categories"], d["derived_segments"]))
```

獨立執行所見：

```text
short_stop_time_s: derived_segments=[], route_catalog=[], pace_table=[], eta_output=[]
stop_ratio:        derived_segments=[], route_catalog=[], pace_table=[], eta_output=[]
margin_coeff:     pace alone=[] (margin_basis remains default)
stop_allow_s:     ValueError: cannot convert float NaN to integer
```

`margin_coeff` 的整份 dataset 另外會由 AC7 抓到 ETA 與 pace 表頭不同；這不補足 `validate_pace_table` 自己接受 `default/NaN` 的缺陷。`stop_ratio` 的整份 dataset 則完全沒有 violation，因而實際繞過 AC5。`stop_allow_s` 會在 `validate.py:357` 的新累計算術拋例外，沒有遵守本模組「回傳 violation list」的介面（`:6`）。

此例不需要讀取或製作任何 GPX。NaN 不是標準 JSON 的合法 number，但目前 public validators 接受 Python dict，而且現有 CLI `__main__.py:25` 使用未限制 `parse_constant` 的 `json.loads`；獨立檢查 `json.loads('{"stop_ratio": NaN}')` 確實得到 NaN。現有入口沒有先拒絕它，不能把入口過濾當成已成立的前提。

**Required fix（owner：#7 Executor）**：在本票新增／修改的 numeric 欄位與相關不變條件運算前，明確將非有限值記為 violation／明確拒絕；僅讓 `_is_number` 回 False 後略過比較還不充分。涵蓋 `short_stop_time_s`、`stop_ratio`、`margin_coeff`、`stop_allow_s`，保留合法 0、nullable 與一秒容差；不得把非有限值補成 0 或 null，也不要求順帶重寫其他既有畸形輸入處理。加入可捕捉上述 false acceptance／例外的回歸案例，重跑 E-1 與 CL-B1-8 檢查，更新 worklog。必要時同時確認 NaN／正負 infinity 在 public validator 路徑上均會被拒絕。後續由 R2 核對 correction；本 record 沒有實作修正。

沒有其他獨立 finding。未作 deferral、adjudication 或 contract change；R1-F1 是契約違反，不能用 defer 代替修正（治理 §4.5）。

## 自行執行的 commands 與結果

下列 commands 全部只在本 worktree 執行。PATH 的 `python --version` 為 `Python 3.11.2`。未使用 `.venv`；沒有安裝依賴、網路呼叫或執行 `experiments/` 腳本。`python -B -` 表示程式透過 stdin 執行，沒有建立暫存腳本。

| Check | Commands／方法 | 實際結果 |
| --- | --- | --- |
| Subject | `git rev-parse HEAD`；`git log --oneline ff049661f968adace4dd017cf560316e5684440d..84fdbfc44ab13ca161758b314d637ef57ddf207e` | HEAD 與指定 SHA 一致；依序為 `f644757`（啟動 records）、`a304ee2`（實作）、`3614053`（worklog）、`84fdbfc`（run／H-2 records） |
| 完整變更範圍 | `git diff --stat ff04966..84fdbfc`、各檔 `git diff ff04966..84fdbfc -- <明確路徑>`；原檔以 `Get-Content -Encoding UTF8 -LiteralPath ...`／`python -B -` 編號閱讀 | 10 files，1131 insertions、40 deletions；已核對兩個 contracts 檔、三個 tests、fixture，以及四份新增／更新 records，包含其 evidence 內容 |
| Record-only delta | `git log --format=oneline --name-only a304ee2..84fdbfc` | 後兩個 commits 全部位於 `docs/governance/records/**`；符合 Bindings §7／P7，不把兩者當成未測試的 implementation delta |
| E-1 | `python -m pytest -q` | exit 0；`193 passed, 6 xfailed in 0.65s` |
| Xfail 清單 | `python -m pytest -q -rxX` | exit 0；`193 passed, 6 xfailed in 0.64s`；六個測試／reason 見下表，無 skipped、xpassed、error |
| Xfail 還原執行 | `python -m pytest -q --runxfail tests/test_ingest.py tests/test_routes_pace_eta.py` | exit 1；`6 failed, 31 passed in 0.45s`；失敗者恰為下表六個，非一般 gate 失敗或額外 regression |
| 被遮住的全部違反 | `python -B -`：匯入 worktree 內 `test_ingest`／`test_routes_pace_eta`，重做 S-1～S-6 的合成產生者呼叫，列出／核對全部 violations，並逐欄比較 S-4 | S-1 private/public 各 8、S-2 8、S-3 5、S-5 2、S-6 P-A/P-B 各 5；unexpected violations 全部為 `[]`，詳見下段 |
| AST／原文 preservation | `python -B -`：以 `git show ff04966:<test path>` 對照 HEAD，逐函式比較 AST、拆分前後 Assert 集合，並人工閱讀 test diff | BASE ingest 14、routes/pace/ETA 18 個測試；只改 S-1～S-6，其他 26 個未變；S-1～S-5 的 Assert 集合保留，S-6 原 assertions 不變；原文與準備步驟的 diff 符合 CL-B1-8 |
| Markers | `rg -n 'xfail\|skip' tests/`（實際使用 regex alternation `xfail|skip`）；`python -B -` 解析 decorator keywords | 只有六個 `xfail`、全部 `strict=True`、reason 開頭與 owner 正確；沒有 skip；`test_contracts.py` 的 xfail 數 0 |
| Schema／privacy 結構 | `python -B -`：在記憶體載入 BASE schemas 與 HEAD schemas，比較 `_DERIVED_PUBLIC`、private、契約 2 與 ID 定義 | 公開 allowlist 唯一新增 `short_stop_time_s`，舊欄位 schema 不變，`additionalProperties=False`；private 只多 `start_time`；ROUTE／ROUTE_SEGMENT／CHECKPOINT／三種舊 ID pattern／CONTRACT_VERSION 均不變 |
| Fixture 獨立重算 | `python -B -`：以 BASE fixture JSON 對照 HEAD；直接由 fixture 自身合成數值計算比例、停等寬放、累計與抵達時間，不呼叫 production ETA 取得預期答案 | 結果見 H2-R2；routes／route_segments／checkpoints／private_start_times 全部不變，所有新數值可追溯 |
| 精確容差邊界 | `python -B -`：fixture 第二段 allowance 分別偏移 −1.0001、−1、0、1、1.0001 秒，篩出乘式 violation | 依序為 True、False、False、False、True；符合含端點的一秒容差；與 NaN finding 分別判定 |
| 非有限值 | `python -B -`：上方 R1-F1 重現與分別呼叫 validators | `short_stop_time_s`／`stop_ratio` 的 dataset 被完全接受；`default/NaN` pace 被接受；`stop_allow_s=NaN` 拋 ValueError |
| 追蹤路徑 | `python -B -` 內以 `git ls-files -z` 讀 git index 並只輸出違禁 pattern 的計數，不開啟該等資料路徑 | `.env`、GPX/FIT、任何 `data/`、`*.key` 計數全部 0；亦涵蓋 H2-R1 指定的三個 data 子目錄 |
| 未改動的程式／設定 | `git diff --name-only ff04966..84fdbfc -- src/moto_copilot/ingest src/moto_copilot/pace src/moto_copilot/routes .gitignore pyproject.toml tests/conftest.py src/moto_copilot/contracts/__main__.py` | 無輸出；沒有擴大產生者、CLI I/O 或全域測試設定 |
| 文句與 I/O 檢查 | `rg -n` 僅搜尋指定 docs／src／tests 路徑；閱讀新增 lines、docstrings、errors、worklog；`python -B -` 掃描完整 diff 新增行的憑證值 pattern 及 I/O 呼叫 | 沒有新增憑證值候選（`sk-ant-`／`sk-proj-` 長值、private-key header 計數 0）；沒有新增檔案 I/O／外部請求；沒有違反 CL-B1-7 的能力宣稱 |
| Whitespace | `git diff --check ff04966..84fdbfc` | exit 1；只有 worklog 的 pytest 原始輸出行 136、151、167、182、199、216 有 trailing whitespace。這是保留原始輸出，非功能缺陷、非已配置 gate，不另列 finding |
| 寫入限制 | `git status --short --untracked-files=no`（開始）；`git status --short --untracked-files=all`（寫檔前／交付核對） | 開始與寫檔前皆乾淨；交付僅允許本 audit record 為新增檔案 |

完整 `pytest -q` 輸出：

```text
........................................................................ [ 36%]
........................................................................ [ 72%]
......................x........x.............x....x.xx.                  [100%]
193 passed, 6 xfailed in 0.65s
```

### CL-B1-8：S-1～S-6 與 K-1～K-6

下表測試完整路徑的前綴是 `tests/`；每個 reason 的共同開頭為 `v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #<n>`，實際 `-rxX` 輸出均符合。

| ID | Xfail 測試 | restore owner | 獨立核對的失敗內容 |
| --- | --- | --- | --- |
| S-1 | `test_ingest.py::test_rows_conform_to_the_contract_in_both_versions__v03_contract` | #9 | private/public 各 8 則，全部僅缺必填 `short_stop_time_s`；原測試保留 public/private 比對及無 start_time 的斷言 |
| S-2 | `test_ingest.py::test_points_with_a_repeated_time_are_dropped__v03_contract` | #9 | 8 則，全部僅缺該欄；原測試的重複時間清理斷言照常執行 |
| S-3 | `test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract` | #10 | 缺 `margin_coeff`、`margin_basis` 各一，`stop_ratio` 三則；新測試的版本字面值按裁決改成 `user-01`，原測試不改；速度／數量／method assertions 保留 |
| S-4 | `test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract` | #11 | header 比較 True；seg 0 只差 `stop_allow_s`，seg 1–3 只差它與 `eta_typ`／`eta_safe`；原 header equality assertion 保留 |
| S-5 | `test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract` | #11 | 2 則，僅缺 `stop_allow_s`；原 `unknown`／C3 reason／所有時間 null 的 assertions 保留且通過 |
| S-6 | `test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks` | #11 | P-A、P-B 各 4 則缺 `stop_allow_s` 加 1 則因該缺欄而發生的 `has a null time although status is ok`；不拆分符合裁決 |

- **K-1：符合**。封閉清單恰好六個 strict xfail，owners、reason 都符合；沒有 skip。
- **K-2：符合**。S-1～S-5 的其餘 assertions 留在原名；移動 assertions 原文未改。S-3 新準備步驟的 `pace_version` 改名是唯一允許的字面值修改；不是把輸出補欄位以偽裝符合契約。
- **K-3：符合**。另外 26 個既有測試的函式內容未改，也未標記。
- **K-4：符合 CL-B1-8 的 #7 gate 定義**。三個 required pytest commands 結果如上，expanded failures 只涉及允許的 producer gap；不是全部 tests passed。這不會消除另行發現的 R1-F1。
- **K-5：符合**。沒有 `ingest/`、`pace/`、`routes/` 變更，也未改全域測試設定。
- **K-6：符合**。本票 `test_contracts.py` 沒有 xfail／skip。

CL-B1-8 §3.2 的恢復期限在 markers 與 worklog E-4／R-2 皆可追溯；#9、#10、#11 未在本次實作，**不得**由本次摘要宣稱已恢復，SPEC-B1 的 SB1-AC3／release gate 也尚未完成。

## Issue #7 AC、SPEC-B1 補充與 evidence

| 條件 | 程式／測試與獨立判定 |
| --- | --- |
| AC1：`short_stop_time_s ≤ stopped_time_s` | `validate.py:114`；`test_short_stops_cannot_exceed_all_stops`、`test_short_stops_above_zero_stops_are_rejected`、`test_short_stops_may_equal_all_stops`、required/type tests 全部通過；**整體未滿足：NaN 繞過，R1-F1** |
| AC2：speed null ⇔ ratio null，可為 0 | `validate.py:222`；`test_stop_ratio_must_be_null_when_speed_is_null`、`test_stop_ratio_must_have_a_value_when_speed_has_one`、`test_stop_ratio_may_be_zero` 與 required/type tests 通過。Null 對應邏輯符合；numeric 值有效性有 R1-F1，不據此宣稱欄位完整合格 |
| AC3：basis 與 coefficient | schema enum、`validate.py:197`；`test_margin_basis_has_two_values_only`、`test_default_margin_must_be_0_20`、`test_loo_rule_margin_accepts_multiples_of_0_05`／`rejects_other_values` 等通過，正常浮點倍數與下限可用；**整體未滿足：default/NaN 被接受，R1-F1** |
| AC4：version pattern | `validate.py:25`、`:190` 的 fullmatch 與 categories 相等檢查；accept 5、reject 16 個參數化案例通過，含結尾換行、全形數字及舊 fixture 名稱；符合，不要求版本自動編號／不可覆寫在本票實作 |
| AC5：ok ETA 的三個算式、一秒容差 | `validate.py:334` 起改用含 allowance 累計，檢查乘式、絕對時刻、逐段差及 safe−typ；`test_stop_allow_is_stop_ratio_times_typical_time`、`test_stop_allow_tolerates_one_second`、`test_eta_typ_steps_follow_typical_time_allowance_and_new_breaks`、`test_eta_typ_step_counts_a_new_break_once`、`test_eta_safe_margin_covers_the_allowance`／`tolerates_one_second` 與低 margin 測試通過；fixture 自行重算及 ±1 邊界符合。**整體未滿足：NaN ratio 下乘式無法核對卻接受，R1-F1** |
| AC6：unknown 時 allowance／typ／safe 都 null | `validate.py:324`；`test_unknown_plan_must_not_carry_a_stop_allowance`（含 0）、`test_unknown_plan_with_every_time_null_passes` 及既有 `test_unknown_plan_must_not_carry_any_time` 通過；符合，沒有把 null 補成 0 |
| AC7：同時提供 pace／ETA 時 margin 必須相等 | `validate.py:296` 在 unknown 分支之前比較；兩種 status 的 `test_eta_margin_must_equal_the_pace_table_margin`、dataset 檢查與缺 margin 的測試通過；符合。未提供配速表時不捏造 coefficient／ratio 來核對 |
| 契約 4 margin 下限與 fixture 改名 | `test_eta_margin_is_at_least_0_05`、`test_eta_margin_of_0_05_is_allowed` 通過；fixture 中六個 version 引用一致為 `user-01`，沒有擴大 ID 樣式或契約 2 |
| CL-B1-1 | 測試與本次 audit 只用合成資料；修改既有測試的理由已列 worklog。沒有讀取／執行私有資料或 experiments |
| CL-B1-2 | `schemas.py:11` 的 `CONTRACT_VERSION="0.2"` 未改，fixture meta 亦同；`test_fixture_is_marked_as_mock` 通過；docstrings 說明只加停等部分，沒有宣稱完整 v0.3 |
| CL-B1-7 | 新增／修改的 errors、程式說明與 worklog 沒有把保守 ETA 說成百分位數，也沒有把 70% 門檻說成官方警特報；提及限制／禁止詞是在否定宣稱，不是能力宣稱 |
| CL-B1-8 | 已逐項核對上段 K-1～K-6 及 §3.3 六項；許可與 evidence 都足以解釋既有 producer gaps，沒有擴張豁免 |

所有列名的既有 pytest 案例均在本次完整 suite 中實際執行；`test_contracts.py` 沒有任何標記，其 162 個案例都在 193 passed 內。新增案例缺少 R1-F1 的輸入，測試通過不等於該 finding 已解決。

| Evidence requirement | 結論 |
| --- | --- |
| E-1 | worklog §6 輸出 1–4 具備 required commands 完整輸出；本次獨立重跑與 expanded checks 的測試集合、數量、failure cause 一致，符合 CL-B1-8 的 #7 定義。未把 xfailed 記成 passed |
| E-2 | worklog §6 E-2 逐項列出 7 AC、CL-B1-2／7／8、下限與 fixture 對應 tests；traceability 存在。其「PASSED」只證明列出的案例，不能據以接受 R1-F1 的未涵蓋情況 |
| E-3 | fixture 自身與 `straight`／`at` 皆標示合成，差異與算式自行核對，見 H2-R2；沒有新增真實座標／軌跡／行程清單的證據 |
| E-4 | worklog §6 E-4 的十列涵蓋 S-1～S-6、checkpoint 預期時刻、公式竄改值、docstring、fixture；與 diff 一致。沒有用修改既有 assertions 掩蓋 regression |
| E-5 | worklog §6 E-5 明列 H-3、H-4 self-verification，亦有 H-2 段；H-2 decision §5 明確採認該段為 self-verification。紀錄存在且沒有冒充 audit；其 H-4 充分性仍受 R1-F1 否定 |

## H-2：H2-R1～H2-R6

| Check | 結論與依據 |
| --- | --- |
| H2-R1 | git index forbidden-pattern counts 全為 0：`.env`、`*.gpx`、`*.fit`、任何 `data/`（因此也含 `data/raw/`、`data/private/`、`data/bmw/`）。僅檢查 index，沒有開啟資料檔 |
| H2-R2(a) | BASE／HEAD fixture 的 routes、route_segments、checkpoints、private_start_times 完全相同；diff 沒有新增／修改座標或逐點軌跡 |
| H2-R2(b) | `short_stop_time_s` 的非零值 12、30 分別取自 fixture 原有 stopped 值；其他 7 列為 0，都是合成情境的選擇，沒有聲稱從真實事件推得。只取 T001/T002、quality=ok 的可計時列：C1 的 moving=150、short=0 ⇒ ratio=0；C2 moving=160、short=12 ⇒ ratio=0.075；C3 只有 1 段、低於 min_segments=2 ⇒ speed 與 ratio 均 null。2 趟使用 default/0.20 合乎 fixture 情境 |
| H2-R2(b)，ETA | 由 fixture 自行算 allowance＝0、9、18、0，RIDE＝180、309、567、927 秒，累計休息＝0、0、600、600 秒。以原有合成出發時刻 07:00:00 得 typ＝07:03:00、07:05:09、07:19:27、07:25:27；精確 safe＝07:03:36、07:06:10.8、07:21:20.4、07:28:32.4。fixture 取整秒後誤差＝0、0.2、0.4、0.4 秒，均在一秒內 |
| H2-R2(c) | `test_contracts.py` 新案例只修改 fixture 或使用字面合成值／既有合成日期，沒有新增真實位置、行程或 I/O |
| H2-R2(d) | 已讀 worklog 輸出 4 的所有內容；其中時間均能對應 fixture，violations 與欄位差異由 worktree 內合成呼叫重現。原 repo 外暫存腳本未讀取，來源本體未驗證；不把它當成唯一證據 |
| H2-R3(a)(b) | 公開 allowlist 唯一新增 `short_stop_time_s`，schema 要求非負 number，拒絕字串／日期／時間；原欄位 schema、`additionalProperties=False` 與 private＝public＋start_time 結構不變。Numeric 的非有限值漏洞是 R1-F1，不代表允許新的位置欄位 |
| H2-R3(c)(d) | `test_public_version_rejects_start_time`、`test_public_rows_hold_no_date_time_or_coordinates` 未改且通過；`validate_public_private_pair` 未改，仍逐欄比較 public items，因此新欄位亦被比較 |
| H2-R4 | contracts diff 無新 I/O、開啟 GPX/FIT 或衍生輸出寫入；CLI、ingest、pace、routes、.gitignore 均無變更 |
| H2-R5：第三方內容 | **N/A**：本票沒有新增／修改任何對外請求、prompt、header 或第三方內容；沒有需要對新外送 payload 套 NFR2 的路徑 |
| H2-R5：裁切／錨點代換 | **N/A**：本票沒有改 ingest 裁切或路線請求／錨點代換；既有合成裁切測試在 suite 中執行，但不宣稱完成未納入本票的錨點整合驗收 |
| H2-R6 | **NOT VERIFIED**：真實行程公開列新增此欄位後的實際揭露程度需要私有資料，未獲本票明確路徑授權，未讀取。required authority＝**acceptor**。#7 沒有產生／提交真實公開列，依 H-2 decision 此項不是 #7 closure 條件 |

## H-3 與 H-4 最低 audit checks

| 類別／最低項目 | 結論 |
| --- | --- |
| H-3：結果／狀態可追溯 | required suite、xfail 展開與 fixture 重算已自行核對；worklog 如實區分 passed／xfailed、self-verification／audit。外部 mutation 原始執行與 rollout 不在 worktree，列在 NOT VERIFIED，沒有以 Executor 完成敘述替代本次測試 |
| H-3：保留行程隔離 | #7 沒有新增開啟任何行程的路徑，shared `pace_eligible` 未改；`validate_pace_table` 仍要求 trip role 是 pace。既有 `test_holdout_trip_must_not_enter_the_pace_table` 與 `test_holdout_trip_is_refused` 正常執行。Fixture 的 T003 是既有**合成** holdout，沒有讀取真實保留行程。實際 ingest 重建流程的 #9 修正不因本票被宣稱完成 |
| H-3：E1／E2 與用語 | 本次沒跑 E1／E2；測試、Spike、技術檢查沒有寫成 E1／E2 的正式結果。CL-B1-2／7 的版本與能力宣稱如上，沒有新的 Google Maps 準確度、折返驗證、隱私只留本機或官方警特報宣稱 |
| H-4：缺漏／失敗／涵蓋不足 | 缺新增必填欄位會出 schema violation；unknown 不得含 0 或其他 allowance；ok 的 null allowance 被拒絕；配速類別沒有 ratio、表頭 margin 缺漏時可回報違反。以上正常 null／缺欄案例有測試。但 **非有限值是未守住的失敗路徑，R1-F1 blocking**，故不能將 H-4 整體標為通過 |
| H-4：逾時／外部失敗 | **N/A**：修改的 contracts 是同步資料驗證，沒有外部 client、重試或逾時路徑 |
| H-4：Planner 不得改寫結果 | **N/A**：本票不涉及 Planner、規則結果或計畫狀態的合併；沒有對此作整合宣稱 |
| H-4：規則 5 未通過不得顯示狀態 | **N/A**：本票沒有規則 5／介面顯示路徑 |
| H-4：路線矛盾／無法驗證時不採用 | **N/A**：契約 2、routing、routes 未改，本票不是路線採用條件的驗收 |

## NOT VERIFIED、限制與後續 authority

1. **本次完整 model／effort／sandbox binding 與 rollout 存取紀錄**：檔案在 worktree 外，依禁令未讀。由 dispatcher 按 Bindings §3.3 核對並記入 run record §5 事件 7 的 R1 binding 欄位後，才能採用為合格 audit；本 record 不把「派工中」當成已核對結果。
2. **Executor 的原始 mutation 暫存腳本及歷史執行**：worklog 有 M1～M13 摘要，原始腳本／逐次執行證據不在 worktree；沒有重做會修改 implementation 的 mutation。相關主張不作本 finding／gate 的獨立證據。worklog 輸出 4 的腳本本體亦未驗證，但其合成結果已由本次獨立重現。
3. **私有資料與真實公開列的揭露程度**：見 H2-R6；required authority＝acceptor。沒有私有資料、外洩或憑證的實際發現，不推測存在外洩。
4. **Issue 線上版本**：只使用 dispatcher-provided 全文與 provenance，沒有網路查證；本地 BD-3 對應一致。
5. **E1／E2、真實 GPX 回歸、#9–#11 的產生者完成與 SPEC-B1 的整合／phase acceptance**：NOT RUN／不屬本 audit；六個 xfail 不是它們完成的證據。既有畸形 break／datetime 輸入的通用健全化沒有在本票擴張處理；R1-F1 則直接涉及本票新增欄位。

目前需要的是由 Orchestrator 將 **R1-F1 route 至 #7 Executor 作 targeted correction**，之後進 R2 closure review。沒有需要自行裁定的新設計語義，也沒有在本次新增驗收條件或要求 Spec Integration Audit。正式 binding 的最後核對由 dispatcher 負責；若對 finding 的 blocking／evidence 有爭議，依治理 §4.3 route Final Adjudicator，實質契約語義爭議先交 Design Authority。

Verdict: BLOCKING
