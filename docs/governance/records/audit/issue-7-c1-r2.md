# Issue #7 — cycle 1 R2 scoped closure review

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（`docs/governance/records/outcome-contract.md`；acceptor 接受 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`docs/governance/records/decisions/derivation-spec-b1.md`，含 CL-B1-8 與 H-2 補充裁決）→ Issue #7「B1-1 contracts」 |
| Subject BASE | `ff049661f968adace4dd017cf560316e5684440d` |
| R1 subject | `84fdbfc44ab13ca161758b314d637ef57ddf207e` |
| R2 subject HEAD | `96b15cd01d79afd3eb7dde4dbf9b3edfdc0c57d6`；本 dedicated worktree 的 detached HEAD |
| Correction | `8981e9d32d4fb2f1c13dd4909243b88114af06a2`，只改 `src/moto_copilot/contracts/validate.py` 與 `tests/test_contracts.py` |
| Audit kind | **Ticket independent audit，R2，cycle 1，scoped closure review；不是 Spec Integration Audit** |
| Role | `primary_reviewer`（Codex） |
| 日期 | 2026-11-17 |
| R1 record | `docs/governance/records/audit/issue-7-c1-r1.md`；原 verdict BLOCKING，唯一 blocking finding 為 R1-F1 |
| Evidence 入口 | `docs/governance/records/worklog/issue-7.md` §9；`docs/governance/records/run/run-20261117-oc1-issue7.md` §5 事件 7–9 |

## Assurance 與 independence

| (a) 四項 independence properties | (b) 實際 models 與 binding evidence |
| --- | --- |
| **Independent context**：本次是 fresh Codex thread，沒有繼承 Executor 或 R1 的對話。自行從磁碟重讀 R1 全文、Required fix、修正後原始碼、測試、diff 與 worklog，不以 Executor 的「已修正」作 closure 依據。 | Executor：run record §5 事件 2、8，`gov-executor`、agentId `a9f372411c0f54099`；派工者全程觀測實際 model／effort 為 `claude-opus-5-5`／`high`，初次 120 則，correction 後共 158 則。這是本 worktree 內的 dispatcher evidence；未自行存取外部 transcript。 |
| **Verifiable binding**：依 Bindings m3 §3.3 的 qualified Codex mapping 派工。本次全部 `turn_context`、model／effort／sandbox、存取紀錄與本 record SHA-256，**由 dispatcher 核對並記入 run record §5 事件 9「派 R2」binding 欄位**；本檔引用該欄，不自行讀取 worktree 外 rollout。 | 本次 Reviewer 是 **Codex**。事件 9 宣告 mapping 為 `gpt-6.1-sol`／`high`；sandbox 為本次派工的 `workspace-write`。受審 HEAD 的事件 9 仍寫「派工中」，所以本檔不把預期 mapping 冒充已完成事後核對的實際 model 證據。正式採用本 audit 前，dispatcher 必須完成該欄核對。 |
| **Autonomous access**：自行取得 worktree 內原始契約、git 歷史、完整 correction diff 與合成 fixture，使用 PATH 的 `python` 自行跑指定 suite、R1 重現與額外檢查；pack 沒有取代原始證據。沒有讀取 worktree 外路徑、`data/`、`.env` 或任何憑證；沒有網路、GitHub 呼叫或執行 `experiments/` 腳本。 | R1：事件 7 attempt 2 已有 dispatcher binding 核對，觀測 `gpt-6.1-sol`／`high`／`workspace-write`。其 Git blob SHA-256 與該欄記載相同，見 commands。Alternate 本輪未派工。 |
| **Self-written record**：本檔由本 `primary_reviewer` 自行撰寫，唯一建立的交付檔案就是本檔；沒有修改、stage 或 commit 實作、測試、契約、R1 或其他 records。dispatcher 依 Bindings §3.3 原樣複製、核對 SHA-256，不改寫結論。 | **no model diversity claim**。Bindings §5 未宣告 diversity 關係；不以 Claude／Codex 的產品名稱推定 diversity。本次外部 binding 的最後核對仍由 dispatcher 負責。 |

## 範圍與依據

依治理本文 §2.3、§4.1–§4.6、Implementation Profile `impl-default` v2 §6–§7、`orch-default` v2.2 §6–§7 與 Bindings m3 §3.3、§5、§7 執行。已讀 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、OC-1、SPEC-B1 derivation、CL-B1-8、H-2 補充裁決、高風險類別裁決，以及 first-run derivation 的 BD-3；核對 `DESIGN.md` §5 與 SPEC-RESOLUTION-001 §1.4 的相關定義。最後一行格式依本次派工指定。

Issue #7 使用本次 pack 重現的全文。`updatedAt=2026-11-15T11:10:55Z`、UTF-8 body SHA-256 `a59c9f93f6d9b6b7259948f189c2185804309b1457be968a001223606c339af7` 是 dispatcher-provided provenance，與本地 BD-3 相符；沒有重新取得線上 Issue。

本輪只判定 R1-F1 closure、correction 對 Issue #7 AC／CL-B1-8／所觸及 H-2、H-3、H-4 的回歸，以及 correction 直接產生或暴露的新缺陷。沒有重開完整 R1、重設計資料契約、擴張 Must，或驗收 #9–#11／SPEC-B1 整合與 phase acceptance。

`git log` 顯示 R1 之後依序是 `881fd7a`（R1／run records）、`8981e9d`（correction）、`527e45e`（worklog）、`96b15cd`（run record）。除 `8981e9d` 外，全部只改 Bindings §7 的 `docs/governance/records/**`。Record-only 路徑不豁免對 evidence 內容的核對；本輪的實作與測試結果涵蓋指定 R2 HEAD。

## R1-F1：RESOLVED

原 finding 為 **Medium，blocking**：新增 numeric 欄位可攜入 NaN，使比較無法成立卻沒有 violation；`stop_allow_s=NaN` 還會在 ETA 算術拋例外。Required fix 要求四個欄位明確拒絕非有限值，不能只略過計算；保留合法 0、nullable 與一秒容差，新增 regression tests 並重跑 CL-B1-8。

修正證據：

- `validate.py:68` 的 `_non_finite_errors` 在不變條件之前回報明確 violation；呼叫位置為 `:104`（`short_stop_time_s`）、`:206`／`:207`（pace `margin_coeff`／`stop_ratio`）、`:290`／`:291`（ETA `margin_coeff`／`stop_allow_s`）。
- `:132`、`:217`、`:357`、`:368`、`:385`、`:388` 讓已回報的非有限值不再進入對應算術；`:375` 對 ETA 單獨使用非有限 `stop_ratio` 的路徑另行回報「cannot be checked」，沒有默默略過比例驗證。
- `tests/test_contracts.py:645`、`:653`、`:660`、`:667`、`:674`、`:684` 新增六個測試函式、36 個參數化案例，涵蓋 NaN／正負 infinity、兩種 margin basis、dataset／單獨 validator、沒有配速表、ok／unknown 列及 `json.loads` 非標準 literal。這些案例全部在本次完整 suite 中實際通過。
- 自行照 R1 的程式重跑四個 NaN 案例，得到下表；另作 45 項獨立檢查，涵蓋 public／private、直接呼叫／dataset、兩種 basis、ETA 有／無配速表、JSON literals。全部明確拒絕、沒有例外；dataset 的輸入序列化前後相同，沒有補成 0 或 null。

| R1 重現（每次只改一個欄位） | R2 實際結果 |
| --- | --- |
| 第一筆 `short_stop_time_s=NaN` | `derived_segments(public)[0]: short_stop_time_s is not a finite number (nan)` |
| C2 `stop_ratio=NaN` | pace category 回報非有限值；ETA 的 C2 兩列分別回報 `stop_allow_s cannot be checked`，沒有完整空 report 的 false acceptance |
| pace header `margin_coeff=NaN`，basis 仍是 default | pace table 回報 `margin_coeff is not a finite number`；dataset 另保留兩個 ETA header mismatch。**pace alone 也有 violation** |
| 第一筆 `stop_allow_s=NaN` | `eta_segments[0]: stop_allow_s is not a finite number (nan)`；沒有原本的 `ValueError` |

原始 fixture 的 `validate_dataset` 各組 violations 都是空清單。獨立將第二段 allowance 偏移 −1.0001、−1、0、1、1.0001 秒，比例算式 violation 依序為 True、False、False、False、True，含端點的一秒容差保留。合法 0、null 對應、缺欄、default／loo_rule、休息只算一次與 safe margin 的既有測試未被修改，且在 suite 通過。沒有未解的 R1-F1 blocking 部分。

## 新 finding

### R2-F1 — finite-number helper 對超大整數拋出 OverflowError

- **Severity：Low；non-blocking。** 這是 correction 新引入的 validator 介面回歸。輸入需為超出 float 範圍的極端整數（例如 `10**309`）；已重現的後果是中止驗證，沒有 false PASS、補值或正常騎乘量級的錯誤 ETA。依治理 §4.3 的 Low 分類記錄，不延長本 cycle，也不把它當成 R1-F1 的殘留 fail-open。
- **依據**：Issue #7 的 `short_stop_time_s` 為非負 number／AC1；`validate.py:6` 的公開介面約定是回傳 violation list。schema 沒有對 number 設此 float 上限。這裡不新增數值上限或要求一般畸形輸入的全面健全化。
- **證據**：`validate.py:75` 新增的 `math.isfinite(value)` 會先將 Python int 轉成 float；`10**309` 因而拋 `OverflowError: int too large to convert to float`，尚未到 `:132` 的 AC1 比較。`:65` 的 helper 也有相同轉型限制。以 `git show 84fdbfc:src/moto_copilot/contracts/validate.py` 載入記憶體作直接差分，沒有修改檔案：

| 合成輸入 | R1 validator | R2 validator |
| --- | --- | --- |
| fixture 第一列只改 `short_stop_time_s=10**309` | 回傳 `short_stop_time_s is greater than stopped_time_s (invariant 6)` | `OverflowError: int too large to convert to float` |
| 同列 `short_stop_time_s` 與 `stopped_time_s` 都改為 `10**309` | `[]` | 同一 `OverflowError` |

- **Required fix**：讓新增有限性檢查不因 finite int 轉成 float 而拋例外；保留 R1-F1 的 NaN／infinity 拒絕，以及 `short > stopped` 的 violation 行為，加入上述整數輸入的 regression case。不要求擴張其他舊欄位的算術支援。
- **Disposition／owner**：作為 non-blocking follow-up 記於本 record，owner＝#7 Executor（由 Orchestrator 追蹤；若成為新的 work item，仍須適用接受與授權）。本輪不修改實作或測試。這不是對 blocking finding 的 deferral，也不替任何尚未通過的 gate 標 PASS。

除此之外，沒有 correction 造成或暴露的新 finding。Worklog C-6 所列 `stopped_time_s`、`typ_seg_time_s` 等既有非有限值行為沒有在 delta 被改動；R1 Required fix 明確不要求順帶重寫，故不將它們重新包裝為 R2 finding。

## 自行執行的 commands 與結果

所有命令的 cwd 都是本 worktree；沒有使用 `.venv`。`python -B -` 代表 PowerShell here-string 經 stdin 執行，沒有建立暫存腳本。閱讀命令前設定 `[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)`；Python 輸出需要中文時另設程序環境變數 `PYTHONIOENCODING=utf-8`。初次中文顯示亂碼／過長輸出處已以 UTF-8 與較小範圍重讀，沒有把亂碼當成檔案內容。

| 命令／檢查 | 實際結果 |
| --- | --- |
| `git rev-parse HEAD` | 指定 R2 SHA `96b15cd01d79afd3eb7dde4dbf9b3edfdc0c57d6` |
| `git status --short --untracked-files=all`（開始、寫 record 前與交付核對） | 開始與寫入前乾淨；交付核對僅本 R2 record 新增，沒有追蹤檔異動 |
| `git log --format=oneline --name-only 84fdbfc..96b15cd` | 四個 commits；只有 correction 改實作／測試，其餘 record-only，見前文 |
| `git diff --stat 84fdbfc..96b15cd`；`git diff --numstat 84fdbfc..96b15cd` | 5 files、590 insertions、14 deletions；validate 32+/7−、tests 69+，其餘三個 records |
| `git diff 84fdbfc..96b15cd -- src/moto_copilot/contracts/validate.py tests/test_contracts.py` | 自行讀完整兩檔 delta；新增 finite check／guards 與六個 regression test 函式；沒有刪改原 assertions |
| `git diff 84fdbfc..96b15cd -- docs/governance/records/worklog/issue-7.md docs/governance/records/run/run-20261117-oc1-issue7.md`（另分檔及以 `Select-Object` 重讀） | worklog §9 correction／結果／concerns；run 事件 7–9；沒有以 Executor 主張代替本次重跑 |
| `python --version` | `Python 3.11.2` |
| **`python -m pytest -q`** | **exit 0；`229 passed, 6 xfailed in 0.95s`** |
| **`python -m pytest -q -rxX`** | **exit 0；`229 passed, 6 xfailed in 0.72s`**；恰為下表 S-1～S-6，無 skipped／xpassed／error |
| **`python -m pytest -q --runxfail`** | **exit 1；`6 failed, 229 passed in 0.74s`**；執行的是整個 suite，失敗集合恰為下表六個，沒有額外 failure |
| `python -B -`：R1-F1 原始 reproduction（`copy.deepcopy` fixture；四個 NaN 欄位；dataset 與 pace alone） | 所有結果見 closure 表；不再 false acceptance 或拋例外 |
| `python -B -`：獨立非有限值 matrix／輸入不變性／原 fixture／±1 秒邊界 | 45 項拒絕檢查通過、沒有例外；原 fixture 全部空 violations；五個容差結果如前文 |
| `python -B -`：記憶體內 R1／R2 validator 對 `10**309` 的兩案例差分；內含 `git show 84fdbfc:src/moto_copilot/contracts/validate.py` | 兩個 R2 OverflowError，R1 分別是 AC1 violation 與空 list，證實 R2-F1 為 delta 引入 |
| `python -B -`：自行呼叫 S-1～S-6 的合成產生者並檢視全部 violations／S-4 每欄差異 | counts／差異見下表；unexpected violations 全部 `[]`，沒有僅依 pytest 截斷的第一個錯誤作判定 |
| `rg -n 'xfail|skip' tests/`；`python -B -` AST 檢查 decorators | 六個 strict xfail，owners／reason 前綴符合；沒有 skip；`test_contracts.py` 無 xfail／skip |
| `python -B -`：AST 比較 `git show 84fdbfc:tests/test_contracts.py` 與 HEAD | 原有 93 個頂層測試／helper 函式內容全部未變；新增 `target_of` 與六個 non-finite 測試函式 |
| `git diff --name-only 84fdbfc..96b15cd -- src/moto_copilot/contracts/schemas.py tests/fixtures/contract_v02/mock_dataset.json tests/test_ingest.py tests/test_routes_pace_eta.py` | 無輸出；相關 R1 coverage 的產物在 correction 未變 |
| `git diff --name-only ff04966..96b15cd -- src/moto_copilot/ingest src/moto_copilot/pace src/moto_copilot/routes tests/conftest.py pyproject.toml .gitignore src/moto_copilot/contracts/__main__.py` | 無輸出；沒有修改產生者、全域測試設定、CLI 或 I/O 路徑 |
| `python -B -`：`git ls-files -z` 僅輸出禁止 pattern 計數；`git diff 84fdbfc..96b15cd` 全部新增行的長 token／private-key header pattern 檢查 | `.env`、GPX/FIT、任何 `data/`、`*.key` 計數各 0；兩類憑證值候選各 0。沒有開啟或輸出禁止資料路徑內容 |
| `Get-FileHash -LiteralPath docs/governance/records/audit/issue-7-c1-r1.md -Algorithm SHA256`；`python -B -` 對照 `git show HEAD:<R1 record>` | worktree bytes 為 `e56449780c7e35a0b6692e5c22e099acf19a1175b03ec8dae00aaaef49ca4bd3`（206 個 CRLF）；Git blob 為 `5fd036f66435064d85b4669dc6070b6e8b5e0da8e5226764bc628beb4bd74e41`，與事件 7 相符。僅將 worktree CRLF 正規化成 LF 後逐 byte 等於 Git blob；沒有內容差異 |
| `git diff --check 84fdbfc..96b15cd` | 非 0；只有 worklog 新增 pytest 原始輸出中的六行 trailing whitespace（583、598、614、629、646、663）。不是配置的 gate 或功能回歸，不另列 finding |
| `Get-Content -LiteralPath <下列明確檔案> -Encoding UTF8`（必要時 `Select-Object -Skip/-First/-Last`）；`python -B -` 讀治理指定 sections | 已自行讀取，沒有改檔。檔案／範圍清單如下；過長輸出以分段與聚焦讀取補足 |
| `rg -n` 搜尋 `DESIGN.md`、SPEC-RESOLUTION-001 的上述 numeric／缺值條款；搜尋 `validate.py` finite helper／guard 與 `test_contracts.py` 相應 tests | 確認欄位、容差、schema 範圍與本檔引用行號；搜尋沒有從 repo root 開始 |
| `apply_patch` 建立本檔；寫入後 `python -B -` 驗證 record／狀態 | 首次 verifier 的中文比對字串經 PowerShell stdin 變成 `?`，exit 1（`AssertionError: R1-F1?RESOLVED`）；改以 ASCII／Unicode escape 比對後重新核對。唯一新增本檔；檔尾依派工為 `Verdict: PASS`，沒有 stage／commit |

閱讀清單：`CLAUDE.md`、`docs/governance/project-bindings.md`（含 §3.3、§5、§7）、`.claude/agents/gov-primary-reviewer.md`；上述 R1、worklog（特別是 §9）與 run records；OC-1、`derivation-spec-b1.md`、`decision-20261117-issue7-spike-tests.md`、`decision-20261117-issue7-h2.md`、`decision-20261117-high-risk-categories.md`、`decision-20261117-oc1-first-run-derivation.md`；採用 package 的治理 §2.3、§4.1–§4.7、impl-default v2 §6–§7、orch-default v2.2 §4–§7（中文 sections 已以 UTF-8 重讀所用條文）；`validate.py`、`schemas.py` 相關定義、`test_contracts.py` correction／既有測試名稱、`test_ingest.py`／`test_routes_pace_eta.py` 合成 helper 與六個 gap tests、`tests/conftest.py`、`pyproject.toml`、mock fixture；`DESIGN.md` §5 共通規則／契約 3、4，以及 SPEC-RESOLUTION-001 §1.4。以上路徑皆在本 worktree。

## CL-B1-8 與 E-1

| ID | 本次實際 xfail（`tests/` 下）／restore owner | 自行展開全部失敗的結果 |
| --- | --- | --- |
| S-1 | `test_ingest.py::test_rows_conform_to_the_contract_in_both_versions__v03_contract`，#9 | private／public 各 8 則，全部只是缺 `short_stop_time_s` |
| S-2 | `test_ingest.py::test_points_with_a_repeated_time_are_dropped__v03_contract`，#9 | 8 則，全部只是缺 `short_stop_time_s` |
| S-3 | `test_routes_pace_eta.py::test_pace_table_matches_the_mock_fixture__v03_contract`，#10 | 5 則：header 缺 `margin_coeff`／`margin_basis`，三類別缺 `stop_ratio` |
| S-4 | `test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract`，#11 | header 相等；seg 0 只差 `stop_allow_s`，seg 1–3 只差該欄與 `eta_typ`／`eta_safe` |
| S-5 | `test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract`，#11 | 2 則，僅缺 `stop_allow_s` |
| S-6 | `test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks`，#11 | P-A／P-B 各 5 則：四個缺 `stop_allow_s`，加一個因缺欄而來的 `null time although status is ok` |

六個 reason 全部以 `v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #<n>` 開頭，owner 與上表一致。

- **K-1**：符合；封閉清單恰好六個 strict xfail、沒有 skip。
- **K-2、K-3**：correction 沒有改兩個拆分測試檔，故 R1 已核對的原文 preservation／其他 26 個測試 coverage 沒有被 delta 破壞；相關測試本次亦執行。不將此表冒充重新做過 BASE 全面 R1。
- **K-4**：符合 #7 特定 E-1 判定；三個 required pytest commands 與全部 gap 檢查如上。`--runxfail` 的非零是刻意還原六個已許可 gap，沒有額外失敗。
- **K-5**：BASE 至 HEAD 的產生者與全域設定 diff 為空。
- **K-6**：契約測試無 xfail／skip；198 個 contract cases 都在 229 passed 中。

CL-B1-8 §3.3 的六項 E-1 條件：一般 pytest exit 0；摘要只有 passed／xfailed；六個 xfailed 與 markers 一一對應；展開只有上述 gap；worklog §9.4 C1-1～C1-3 保留 Executor 的完整輸出；§6 E-4、§9.3／§9.5 有拆分與新增測試的理由。各項與本次獨立結果一致，沒有把 xfailed 稱為 passed。新增 36 個 passed 對應 correction regression cases。

這僅滿足 #7 的 CL-B1-8 E-1 定義。#9／#10／#11 的恢復期限、SPEC-B1 SB1-AC3 的無 xfail 要求與 Bindings release gate 都沒有因此完成或被放寬。

## Issue #7 AC 的 correction regression coverage

| AC／限制 | R2 scoped 判定 |
| --- | --- |
| AC1 short ≤ stopped | 普通非負數的比較與邊界測試未改且通過；NaN／infinity 現有明確 violation，R1-F1 解決。極端整數的介面回歸另列 Low R2-F1，不隱藏成「所有數值皆已驗證」 |
| AC2 speed null ⇔ ratio null，可為 0 | 原判定未改，`test_stop_ratio_must_be_null_when_speed_is_null`、`...must_have_a_value_when_speed_has_one`、`...may_be_zero` 通過；新增 finite check 不把 null 或 0 當成非有限值 |
| AC3 basis／margin | default／loo_rule／倍數與下限案例通過；兩種 basis 的三種非有限值都有直接拒絕證據，不是只靠跨表不相等拒絕 |
| AC4 pace_version | schema／fullmatch 與原測試函式未改，suite 通過；沒有擴張版本或 ID 樣式 |
| AC5 三項 ETA 算式／一秒容差 | 新 guard 只避開已回報的無效值；有限值的乘式、累計、相鄰差、休息與 safe margin 測試通過。另自行驗證含端點的一秒容差；ETA 單獨拿到非有限 ratio 也明確回報不能驗證 |
| AC6 unknown 全 null | 原 null／unknown 測試通過；unknown 列塞入 NaN／infinity 也回報非有限值，沒有在 unknown 分支前漏掉檢查 |
| AC7 兩份 header margin 相等 | 原比較在 unknown 分支之前，correction 未改；ok／unknown 的 mismatch 測試通過，非有限 header 不因算術 guard 而被放行 |
| Scope／CL-B1-1、2、7 | 沒有修改 schema、fixture、ID、契約 2、產生者或 CLI；仍是 contract v0.2 加已核准停等欄位，沒有重算配速／margin。僅用合成資料，沒有新增超出證據的能力宣稱 |

## 所觸及 H-2／H-3／H-4 的最低核對

| 項目 | Correction delta 的結果 |
| --- | --- |
| H2-R1 | Git index 的 `.env`、GPX/FIT、任何 `data/`（涵蓋 raw／private／bmw）計數全為 0；未開啟禁止資料路徑 |
| H2-R2(a)(b) | fixture 在 R1→R2 沒有改動，沒有新增座標、軌跡或 private_start_times。未為本次 closure 重做完整 R1 fixture 推導；correction 只拒絕非有限值，原 fixture 本次 validator 檢查仍全部空 violations |
| H2-R2(c)(d) | 新六個測試使用現有 mock fixture／字面 NaN、infinity；JSON 文字由同一 fixture 取得。新增 worklog 數值與時間對應既有合成 fixture／gap tests，沒有新真實騎乘值；本次自行重現其 correction 與 gap 結果 |
| H2-R3 | 公開 allowlist／private＝public＋start_time／additionalProperties／pair 比較未改；既有 public privacy tests 未改且通過。新增數值拒絕沒有放寬隱私控制；Low 整數例外亦不會產生新的公開欄位 |
| H2-R4 | 無產品檔案 I/O／GPX／FIT／衍生檔寫出或 CLI 變更；產生者、.gitignore 均無變更 |
| H2-R5 第三方內容 | **N/A**：delta 沒有產品外部請求、prompt、header 或第三方 payload |
| H2-R5 裁切／錨點 | **N/A**：delta 沒有隱私裁切／路線請求／錨點代換變更；不宣稱完成其整合驗收 |
| H2-R6 | **NOT VERIFIED**：真實公開列的揭露程度需要私有資料；本次不讀取，required authority＝acceptor。依 H-2 裁決這不是 #7 closure 條件 |
| H-3 evidence／狀態 | 本次三個 pytest、reproduction 與合成 gap 檢查支持相應 worklog 陳述；mutation 歷史執行沒有被冒充自行驗證。沒有將 xfail 寫為通過、或把 correction／Spike 數字稱為 E1 Lite／E2 結果 |
| H-3 holdout／版本／用語 | 沒有新增開啟行程的路徑、沒有改角色拒絕或版本分離；既有合成 holdout 拒絕測試在 suite 通過。schema 版本未改；新增文字沒有百分位數、Google Maps 準確度、官方警特報、折返已驗證或隱私只留本機的能力宣稱 |
| H-4 缺漏／無法驗證 | 新欄位非有限值明確 violation，沒有預設值或 false PASS；缺欄、null、未知類別 ratio、unknown 輸出等既有測試仍通過。新增 finite-int 例外已另列 Low finding，未將整個輸入空間宣稱全面健全化 |
| H-4 逾時／外部失敗 | **N/A**：同步 contracts 驗證沒有新增 client、逾時或重試路徑 |
| H-4 Planner 不得改寫結果 | **N/A**：correction 沒有 Planner／計畫狀態合併路徑 |
| H-4 規則 5 顯示關卡 | **N/A**：correction 不涉及規則 5 或介面 |
| H-4 路線矛盾／採用條件 | **N/A**：correction 不涉及契約 2、routing 或 routes 採用條件 |

## NOT VERIFIED 與 closure 的界線

1. **本次 R2 完整 binding／rollout／原樣轉錄核對**：worktree 外資料未存取；由 dispatcher 依 Bindings §3.3 填入 run record §5 **事件 9 binding 欄位**後，才能採用為合格 audit。這是正式採用的程序前提，沒有以「派工中」自證通過。
2. **Executor mutation 的原始暫存腳本及歷史執行**：worklog 有 F1～F4／M1～M13 輸出，但未自行讀取外部腳本、未做會修改檔案的 mutation；只作待驗證主張，不是本次 closure 的獨立證據。
3. **私有資料與真實公開列**：H2-R6，NOT VERIFIED；required authority＝acceptor。沒有實際外洩發現，也沒有自行取得私有資料。
4. **線上 Issue 版本**：只採 dispatcher-provided body 與 provenance，沒有網路查證。
5. **E1 Lite／E2、真實 GPX 回歸、#9–#11 完成、SPEC-B1 Spec Integration Audit／phase acceptance 與 release**：NOT RUN／不在本 audit 範圍；不得由本 record 推論已完成。

R1-F1 已 RESOLVED。R2 範圍內沒有未解 blocking finding；R2-F1 為 Low、non-blocking，已有 disposition 與 owner。本 record 的 PASS 是本 Ticket 的 R2 audit closure 判定，不取代 dispatcher binding 核對、orch-default §7 其餘 work item predicates、SPEC-B1 整合與 phase acceptance 或 acceptor 的 release 授權。沒有作 contract change、blocking deferral 或替代他方 authority。

Verdict: PASS
