# Issue #10 — cycle 1 R1 independent audit

| 欄位 | 內容 |
| --- | --- |
| Work Contract | OC-1（接受基準 `873e37ae98d701c076b1bc533c7993ca62c2dd6c`）→ SPEC-B1 v1（`derivation-spec-b1.md`，含 #10 列的三項追加驗收條件）→ Issue #10 B1-3 pace；另適用 CL-B1-8、CL-B1-9 第 3 項、CL-B1-12～14 |
| Subject | 本 dedicated worktree 的 detached HEAD；BASE `20939aac12b29c4feaecec133f779e636c598cb9`；HEAD `c47716c16b4f8c500d71e67cb2791f3fc549b06a` |
| Audit kind | **Ticket independent audit, R1, cycle 1；不是 Spec Integration Audit** |
| Role | `primary_reviewer`（Codex，Bindings m3 O-6） |
| 日期 | 2026-11-18 |
| 派工引用 | `docs/governance/records/run/run-20261117-oc1-run2.md` §6 **事件 23**（本次 #10 R1）；Executor 為事件 20、22 |
| 結論範圍 | #10 的完整 accepted scope、適用 invariants、變更風險與 E-1～E-5。沒有作 Spec phase acceptance、run completion 或 release 判定 |

## Independence 與 model assurance

| Property | 本次滿足方式／證據界線 |
| --- | --- |
| Independent context | 本次是 fresh Codex thread，未繼承 Executor 的對話或推理。派工提供契約、subject 與原始資料入口；worklog、run record 的結論都當成待驗證主張。沒有使用 subagent 或 delegated review |
| Verifiable binding | 派工依 Bindings §3.3 O-6，識別為事件 23。全部 rollout 的 model／effort／sandbox 以及存取紀錄，由 **dispatcher** 依該節核對並記入該事件。本 subject 的事件 23 尚標「進行中」；本 reviewer 不把預定 mapping 當成已觀測的 runtime 證據，也不讀 worktree 外的 rollout。正式採用本 record 仍須 dispatcher 完成該核對 |
| Autonomous access | 自行讀取本 worktree 中的治理、契約、完整受審程式、測試、fixture、git 歷史與差異，並以 PATH 上的 `python` 執行測試及獨立探測；沒有以 Executor 的摘要限制 coverage |
| Self-written record | 本檔由 reviewer 自行撰寫，是本次唯一新增的非快取檔案；沒有修改實作、測試、契約、gate、其他 record，沒有 stage 或 commit。依 Bindings，dispatcher 後續須原樣保存並核對 SHA-256 |

Executor 的實際 model 證據：run record 事件 22（第 103 行）記載 agent `a54ac9cf0e452782b` 的全部 135 則 assistant 訊息觀測為 `claude-opus-5-5`／`high`。Primary 是本次 Codex；事件 23 預定 `gpt-6.1-sol`／`high`，但本 subject 尚沒有該次 rollout 的觀測結果。因此此處是 **no model diversity claim**；不以角色 definition 的 Claude frontmatter、預定 mapping 或自述冒充本次實際 model binding。

## 契約、subject 與唯讀範圍

讀取了 root `CLAUDE.md`、`.claude/agents/gov-primary-reviewer.md`、Bindings m3，以及 package 的治理本文 §2.3、§3.8、§4.1～4.7、impl-default v2 §6～7、orch-default v2.2 的 audit／completion predicates。record 最後一行依本次明確派工使用 `Verdict: ...`。

契約來源包含 OC-1、`derivation-spec-b1.md`、first-run derivation 的 BD-3／BD-4／BD-5 與範圍分配、CL-B1-8 record、CL-B1-9 record、CL-B1-12～14 record、高風險類別 record §5；另核對 `DESIGN.md` 契約 3 與 §6.1、SPEC-RESOLUTION-001 §1.2／1.4、SPEC-001 對資料契約與餘裕係數的引用、BATCH-1 索引的共通規則與依賴。Issue 使用派工附上的原文；其所附 SHA-256 與 BD-3 的 #10 列同為 `880ef1341e090b86e826cd2a14812ab4a05b634b73385c3ccebea80e43245e65`。沒有向 GitHub 取得其他版本。

原始材料包括 `pace/table.py`、`pace/__init__.py`、`contracts/validate.py` 的受影響路徑、`contracts/schemas.py`、五個測試檔與 `conftest.py`、既有 mock fixture、`ingest/segments.py` 的分類邊界。只閱讀 `experiments/cr01_checks/data_common.py` 的 `tercile_thresholds` 與 `data_sb2_stop_allowance.py` 的相關來源；**沒有匯入或執行任何 experiments 腳本**。

`git status --short` 起始為空。`git log --oneline 20939aa..c47716c`、`git diff --stat 20939aa..c47716c` 與各 commit 的 `git diff-tree --no-commit-id --name-only -r <SHA>` 證實：只有 `be0074d`、`e0f6c78` 改動程式／測試；其他五個 commit 都只改 `docs/governance/records/**`。`git diff --name-only e0f6c78..HEAD` 只有 run record 與 worklog。因此本次實際覆蓋 HEAD 所含的兩次 implementation，而非只審第一版。

`validate.py` 的 diff 只有不變條件 3 的段落與模組說明；`pace_eligible`、不變條件 2、其他驗證、`ingest_version` 檢查沒有修改。S-3 只移除 xfail 兩行，內文未改；S-4～S-6 與其標記沒有變動。兩個原有配速斷言因重新分類而修改，理由在 worklog §6 E-4；rework 對新測試的修改與 S-3 恢復理由在 §9.4。

## Reviewer 實際執行的檢查

全部命令在此 worktree 內執行；使用 PATH 上的 `python`，沒有使用 `.venv`。每個 pytest 程序設定 `PYTHONDONTWRITEBYTECODE=1`，並透過 `PYTEST_ADDOPTS=--basetemp=.pytest_cache/<本次名稱>` 把合成暫存檔限制在 worktree。沒有改 pytest 設定檔。

| 指令／檢查 | 實際結果 |
| --- | --- |
| `git rev-parse HEAD`、`git rev-parse 20939aa`、`git status --short` | SHAs 如表頭；初始工作區乾淨 |
| `git log --oneline 20939aa..c47716c`、`git diff 20939aa..c47716c -- <受審路徑>`、上述逐 commit 檔案核對 | 9 個變更檔；implementation 範圍與 CL-B1-12 的擴大範圍相符；record-only delta 已分辨 |
| 第一次 `python -m pytest -q`（basetemp `.pytest_cache/r1-default`） | `290 passed, 3 xfailed, 97 errors in 3.64s`。原因是 reviewer 指定的 basetemp 父目錄 `.pytest_cache` 尚不存在，`tmp_path` setup 出現 `FileNotFoundError [WinError 3]`；不是產品測試斷言失敗。該輪結束後 pytest 已建立快取父目錄 |
| 重跑 `python -m pytest -q`（basetemp `.pytest_cache/r1-default-retry`） | exit 0；**`387 passed, 3 xfailed in 1.89s`**；沒有 error、skip、XPASS |
| `python -m pytest -q -rxX`（basetemp `.pytest_cache/r1-reasons`） | exit 0；**`387 passed, 3 xfailed in 1.88s`**；XFAIL 清單如下 |
| `python -m pytest -q --runxfail tests/test_ingest.py tests/test_ingest_cli.py tests/test_routes_pace_eta.py tests/test_pace_table.py tests/test_contracts.py`（basetemp `.pytest_cache/r1-runxfail`） | exit 1（預期）；**`3 failed, 387 passed in 1.89s`**。只有 S-4～S-6，細節如下 |
| `rg -n 'xfail\|skip' tests` | 只有 `test_routes_pace_eta.py:163,177,186` 的三個 `strict=True` xfail；都指向 #11，沒有指向 #9／#10 或其他 skip／xfail |
| `git ls-files`，在記憶體比對 release gate 的禁止樣式，不輸出禁止路徑內容 | `.env`、`*.gpx`、`*.fit`、`data/raw/`、`data/private/`、`data/bmw/` 的 tracked 命中數 **0**；另核對 `*.key` 命中數 **0**。這是 git metadata 核對，沒有開啟、列舉或搜尋私有資料目錄 |
| 對 `git diff 20939aa..c47716c -- src/ tests/ docs/governance/records/` 新增行作憑證樣式與用語核對 | 憑證賦值樣式命中 0；P90／分位數／官方警特報命中都是限制、否定或核對陳述，沒有禁止的正面宣稱。沒有網路／第三方傳送的新程式路徑 |
| `git diff --check 20939aa..c47716c` | exit 2，僅 worklog 摘錄 pytest 的 `E` 行有尾端空白（126、141、158、175、392、409、426 行）；沒有把這些日誌空白列為產品缺陷 |
| `git diff --check 20939aa..c47716c -- src/ tests/` | exit 0 |
| `python -`：JSON Schema／計數探測（下節完整重現） | 確認 R1-F1：整數總數錯誤被拒絕，同值的 float 總數錯誤卻回傳 `[]`；JSON round trip 後仍重現 |
| `python -`：獨立合成資料 oracle 與失敗矩陣 | CL-B1-13 的 8 折、30 個不合法／缺漏數值案例、4 種非 pace 角色、4 類不合格列的整數計數檢查，結果如下 |

用語掃描的第一個 reviewer stdin 小程式因 PowerShell 將中文字 regex 轉碼成問號，出現 `re.error: nothing to repeat`；改用 ASCII 的 Unicode escapes 後完成掃描。此前已完成的 tracked path、commit 範圍與憑證樣式計數不受影響。沒有以該失敗掃描作通過證據。

`-rxX` 的完整 XFAIL 集合是：

```text
XFAIL tests/test_routes_pace_eta.py::test_eta_reproduces_the_mock_fixture__v03_contract
XFAIL tests/test_routes_pace_eta.py::test_eta_is_unknown_when_a_category_has_no_pace__v03_contract
XFAIL tests/test_routes_pace_eta.py::test_eta_output_passes_the_contract_with_and_without_breaks
```

三個 reason 都是 `v0.3 producer gap (decision-20261117-issue7-spike-tests): restored by #11; compute_eta does not write stop_allow_s yet`。`--runxfail` 的 S-4 在第 167 行做列比對，第一列只差 fixture 的 `stop_allow_s: 0.0`；S-5 第 182 行回報兩個 `stop_allow_s` 必填缺漏；S-6 第 191 行回報 `stop_allow_s` 必填／status ok 時缺值，沒有其他原因。這三個 xfail **不是通過**，不是 E1／E2 的實驗結果。

獨立 oracle 在 stdin 建立 8 趟、每趟一個 1000 m／曲率 100 的合成路段；移動秒數為 `[61,64,70,77,80,85,91,97]`，短停留為 `[0,3,6,9,12,15,18,21]`。以 mock row 的公開欄位形狀建立，另確認 `validate_derived_segments(..., 'public') == []`。逐折自行計算其餘 7 趟速度的 median、取小數兩位、合併停等比例，再算 `actual/predicted-1`；與 `loo_folds` 的 8 個 r 在 `1e-12` 內相等，且與未捨入速度的答案有差異。各折門檻 `(100,100)`，header 為 `0.20/loo_rule`（此值由規則算出，不是 default）。

同一探測對四個使用欄位各測 `None`、bool、字串、NaN、Infinity、負數、缺鍵，另測長度／移動時間為 0，**30 例全部 ValueError**；`holdout`、`excluded`、`unknown`、`None` 四種角色全部拒絕。D-10-9 的缺移動時間路徑也因此核對：不默默漏掉該列、不補值，與修訂後 CL-B1-4 的明確錯誤要求相容，沒有在此補作設計決定。

另分別加入 suspect、invalid、holdout、`trip_ids` 外的 pace 列：正確的整數總數通過，多計該列時全部回報 invariant 3。這補核對了 CL-B1-12 minimum checks 中的 invalid 情形；**不能**據此宣稱所有表示方式的總數都受到檢查，R1-F1 正是反例。

## 逐項驗收與 evidence 判定

下表的 PASS 只代表所列行為與證據；整體 R1 仍有 blocking findings。

| Issue #10 AC／追加條件 | Reviewer 核對與判定 |
| --- | --- |
| AC1：合併停等比例；速度 null 時比例 null | PASS。`test_stop_ratio_is_short_stops_over_moving_time_of_the_timed_segments` 手算各類別的 Σ短停留／Σ移動時間，排除長停留；`test_stop_ratio_is_null_when_speed_is_null_and_zero_when_there_are_no_short_stops` 核對 null 與 0 的區別 |
| AC2：拒絕保留行程 | PASS。`test_a_trip_that_is_not_a_confirmed_pace_trip_is_refused` 核對三個入口與不寫檔；mixed role、重複、未知 trip 與計算前拒絕的測試亦通過；另有上述角色探測 |
| AC3：固定曲率清單→固定門檻 | PASS。`test_a_fixed_curvature_list_gives_fixed_thresholds` 涵蓋 n=1、2、9 與 Python ties-to-even；與只讀參考實作的 n//3、2n//3 規則一致 |
| AC4：固定殘差、每折重算、缺配速排除、少於 8 折 default | PASS。固定殘差與 floor／rounding 測試、每折不同門檻的案例、held trip 無可計時列、類別不足、以 counted folds 而非 n_trips 決定 default 的測試全部通過 |
| AC5：header 係數由同批行程算出 | PASS。`test_header_margin_equals_the_rule_on_the_same_trips_with_8_counted_folds` 手算 r3=13/120→0.15；另有不使用受測 margin 函式算期望值的 rounded-speed oracle |
| AC6：新版本新檔、兩開頭各自遞增、既有內容不變 | PASS。`test_each_build_is_a_new_version_and_file_numbered_per_prefix` 作 bytes snapshot；最大編號延續與 99→100 測試通過。writer 使用 exclusive `open('x')`，目錄無預設位置 |
| AC7：已存在 research 版本報錯不覆寫 | PASS。既有 research 與不同補零位數同編號測試通過 |
| AC8：選 built_at 最晚的 user | PASS。測試最晚者不是最大編號；tie 選較大號；research 不參與；錯誤時間／檔內版本明確拒絕 |
| 追加1：category_scheme 格式 | PASS。`test_category_scheme_has_the_fixed_format` 與實際建表斷言，格式 `curv-tercile-<整數>-<整數>` |
| 追加2：同一固定殘差的 7／8 折分界 | PASS。`test_margin_rule_on_a_fixed_residual_list` 直接測 7／8；header 另有 7 折 default 與 8 折 loo_rule 測試 |
| 追加3：沒有可計時列就不建立、不寫檔 | PASS。`test_no_timed_segment_means_no_thresholds_and_no_table`；writer 在建表與驗證成功之前不開輸出檔 |

| Clarification／evidence | Reviewer 判定 |
| --- | --- |
| CL-B1-1 | 此次 audit 僅合成資料；既有測試改動的理由可在 worklog E-4 追溯。沒有修改 Issue／Draft Spec 或擴張 Must |
| CL-B1-4 items 1、3（修訂後） | PASS。取列需要 pace／ok／seg_category 非 null；分類重新依曲率，不沿用衍生類別。曲率 null、長度或移動時間 0 等明確錯誤，不略過。relabelled 類別、seg_category null 與重算不同分類的 writer 測試通過 |
| CL-B1-4 items 2、4、5 | PASS。門檻、scheme 格式、Σ／Σ 與 min_segments 的實作／測試一致 |
| CL-B1-4 items 6、7；CL-B1-13 | PASS。每折只用其餘行程；held trip 以該折門檻分類；使用 `_category_pace` 同一路徑的兩位速度與未捨入比例。第三大 r、0.05 floor／步長與 `1e-9` 浮點 guard 符合只讀參考來源 |
| CL-B1-4 items 8～10；CL-B1-14 | PASS。明確目錄、數值編號 identity、user 禁指定號、research 同號拒絕、latest user 同數值雙檔報錯、不確認為 pace 的 trip 在計算前拒絕。沒有 user 時回傳 None；research fallback 屬凍結清單，不在 #10 |
| CL-B1-7 | PASS。新增或修改文字無禁止宣稱；模組的 `not a P90` 是否定句 |
| CL-B1-8 §3.2：S-3 恢復 | PASS。S-3 保留獨立函式，移除標記後內文未改，仍帶 derived rows 驗證契約；一般與 --runxfail 都通過。worklog §9.4 有明確記錄 |
| CL-B1-9 item 3：E-1 機器結果與允許標記 | PASS。此次 387 passed／3 xfailed，僅 S-4～S-6；--runxfail 只有該三項缺口，沒有放寬 S-4～S-6 |
| CL-B1-12 §3.2：合計一律檢查 | **FAIL，R1-F1。** Python int 案例通過不足以涵蓋 schema 接受的整數值 float |
| CL-B1-12 §3.2：同 scheme 才逐類別 | PASS。原 fixture、既有 eligible-count 測試及 `test_the_same_scheme_still_checks_each_category` 涵蓋通過／違反；不同 scheme 正確總數而不同分配可通過。沒有解析 scheme、重分類或聲稱驗證器核對重算後逐類別計數 |
| CL-B1-12 §8 minimum checks | 除 R1-F1 外，指定正反案例、不合格／其他 trip 列計數、null curvature 不寫檔、writer 帶 rows 驗證、S-3 及限定 validate.py delta 均已看到；invalid 類型另以 reviewer 探測補驗 |
| E-1：worklog 記錄完整輸出 | **未滿足，R1-F2。** 摘要與失敗原因經本次重跑確認，但 worklog 自述對 --runxfail 輸出作縮寫，raw stdout 不在可核對的 tracked evidence |
| E-2 | PASS。worklog §6 E-2 加 §9.2 逐 AC／追加條件列出測試與結果；本次重跑驗證。其記載的中間版結果與最終版有區分；表中通過案例不推翻 R1-F1 |
| E-3 | PASS（合成來源與受審 delta）。新測試的長度、時間、曲率、T101 等為手寫常數；新增 contracts 測試為 mock 副本；fixture 的 `_meta.mock=true` 並明示所有數字／座標／時間為編造。fixture 檔案未改，受審 delta 無真實騎乘資料 |
| E-4 | PASS。worklog §6 E-4 與 §9.4 逐項交代兩個舊斷言、S-3、rework 測試變更；未用標記掩蓋不受影響的斷言 |
| E-5 | 已有逐類別 self-verification（§6 E-5、§9.5），本次獨立核對見下；其中「合計守住不合格列」並非無條件成立，R1-F1 必須修正 |

## 高風險最低核對

| 類別 | 核對結果與限制 |
| --- | --- |
| H-2 | release gate 禁止 tracked 路徑命中 0；檢閱 diff、fixture 與 worklog 的資料來源為合成／既有 mock。新增 pace 路徑只寫 caller 指定的現有目錄，沒有網路傳送、GPX 讀取或私有位置欄位。全套含既有兩端修剪及 public/private 欄位隔離測試。錨點代換不在本次程式 delta／#10 工作範圍，沒有把它或整個產品隱私流程宣稱為本票已實作；真實資料隱私需 acceptor，見 NOT VERIFIED |
| H-3 | 保留／非 pace 的 trip 在計算前拒絕；research/user 分離與不覆寫有 bytes 比對及 exclusive writer；未改凍結／holdout 解封程式。狀態區分中間 BLOCKED、rework、待 R1；沒有把 xfail、Spike 或此次測試當 E1／E2。R1-F1 是 verifier false clean，R1-F2 是完整 evidence 要求，不接受 Executor 的概括符合陳述替代證據 |
| H-4 | 無可計時列、null 曲率、數值缺漏／無效、角色不明、目錄不存在、重複 user identity、錯誤 built_at／檔內版本都有錯誤路徑；配速不足保留 null，不以其他類別補值；少於 8 counted folds 才 default 0.20。30 例獨立輸入探測通過，但總數驗證仍存在 R1-F1 的 fail-open。Planner、規則 5、計畫狀態與路線採用不在此票 delta，不對其完整性作結論 |

## Findings

### R1-F1 — schema 接受的整數值 float 會完全略過總數檢查

- **Severity：Medium；blocking。Owner：#10 Executor。**
- 契約：CL-B1-12 §3.2 第 1 項「合計（一律檢查）」、同 record §8 的正反驗證要求，以及 H-3／H-4。這是 #10 新增檢查的具體 false clean，不是新增型別偏好或要求驗證器重算門檻。
- 證據：`src/moto_copilot/contracts/validate.py:261` 只在每個 count 都是 Python `int` 時才做合計。`contracts/schemas.py:111` 使用 JSON Schema `integer`；實際採用的 `Draft202012Validator` 接受 `3.0`。不同 scheme 時逐類別檢查也不執行，所以總數不符仍能回傳 `[]`。`tests/test_contracts.py:248` 的正反測試只用 Python int。
- 實測：同一份 mock 派生資料有 5 個合格列，重算表的正確分配為 `[1,2,2]`。把最後一個 n 改成 `3` 得 invariant 3；改成 `3.0`（總數仍是 6）卻完全沒有違反。`json.dumps`／`json.loads` 後仍重現，因此不是只有手建 Python 物件才有的情況。

重現命令：在此 worktree，設定 `PYTHONPATH=src`、`PYTHONDONTWRITEBYTECODE=1` 後以 `python -` 執行以下 stdin（不寫檔）：

```python
import copy, json
from pathlib import Path
from jsonschema import Draft202012Validator
from moto_copilot.contracts import validate_pace_table, schemas
d = json.loads(Path('tests/fixtures/contract_v02/mock_dataset.json').read_text(encoding='utf-8'))
h, c = copy.deepcopy(d['pace_header']), copy.deepcopy(d['pace_categories'])
h['category_scheme'] = 'curv-tercile-20-150'
for rec, n, speed, ratio in zip(c, [1, 2, 2], [None, 52.5, 40.5], [None, 0.1, 0.0]):
    rec.update(n_segments=n, speed_kmh=speed, stop_ratio=ratio)
print('baseline', validate_pace_table(h, c, d['derived_segments']))
c[2]['n_segments'] = 3
print('integer_total_6', validate_pace_table(h, c, d['derived_segments']))
c[2]['n_segments'] = 3.0
print('float_schema_errors', [e.message for e in Draft202012Validator(schemas.PACE_CATEGORY).iter_errors(c[2])])
print('float_total_6', validate_pace_table(h, c, d['derived_segments']))
for rec in c:
    rec['n_segments'] = float(rec['n_segments'])
print('json_roundtrip_total_6', validate_pace_table(h, json.loads(json.dumps(c)), d['derived_segments']))
```

實際輸出：

```text
baseline []
integer_total_6 ['pace_categories: n_segments add up to 6, but 5 rows are eligible (invariant 3)']
float_schema_errors []
float_total_6 []
json_roundtrip_total_6 []
```

Required fix：讓合計檢查涵蓋 schema 所接受的合法整數數值表示；或對不能計數的表示明確回報違反，不能讓 schema 與後續 guard 一起放行錯誤總數。新增 regression cases：不同 scheme、正確／多計／少計的整數值 float（含 JSON round trip）、混合 int／float；保留同 scheme 逐類別檢查，非法型別仍明確拒絕。不得藉修正擴大為 scheme 解析或重新分類。修正後重跑本票 E-1 與相關 tests，再進 R2。

### R1-F2 — worklog 沒有保存要求的完整 --runxfail 輸出

- **Severity：Medium；blocking。Owner：#10 Executor。**
- 契約：SPEC-B1 §5 E-1、CL-B1-9 §2 第 2.vi／第 3 項、CL-B1-12 record §8 明定完整輸出記入 worklog。這是明訂的 durable evidence requirement，不是要求增加測試或新的報告形式。
- 證據：`docs/governance/records/worklog/issue-10.md:439` 明寫「後兩個 `data = {...}` 以『同上』縮寫」，並將 raw output 指向未版控的 Executor scratchpad；同段也改寫 mock 名稱。§9.3 的輸出因此不是規定的完整轉錄。raw scratchpad 不在此 worktree，未讀取，也不能拿其存在自述替代 evidence。
- 本次已獨立確認三個失敗的實際原因與摘要一致，**不主張 Executor 虛構結果或機器 gate 失敗**；但這不自動滿足「完整輸出記在 worklog」的不同要求。不能將本項標為已滿足而交由結案。
- Required fix：在 R1-F1 修正後的最終 implementation subject，重新執行 E-1 所要求的三個命令，將完整 stdout、exit code、subject 識別保存在同一 worklog，不用「同上」或人工改寫取代原文；只執行合成測試。保留既有歷程並明確指認新的最終 evidence。Reviewer R2 核對輸出與最終 subject 相符，不需要去讀 worktree 外的 scratchpad。

Non-blocking findings：無。以上兩項都未解決，沒有 deferral 或 gate waiver。

## NOT VERIFIED／NOT RUN 與 required authority

| 項目 | 狀態、原因與 authority |
| --- | --- |
| 真實配速行程重建、留一趟、回歸（G-REG），以及私有位置／保留行程隔離的真實資料驗證 | **NOT VERIFIED／NOT RUN**。Issue 排除範圍與 RB-7；沒有明確私有檔案授權，也沒有嘗試取得資料。required authority = **acceptor** |
| E1 Lite、E2 與 holdout 解封 | **NOT RUN**。不在本票驗收；required authority = **acceptor**。本次數字只有合成測試意義 |
| 本次 Codex rollout 的實際 model／effort／sandbox、完整存取紀錄 | **NOT VERIFIED by reviewer**。由 dispatcher 依 Bindings §3.3 在 run 事件 23 記錄；本 subject 事件仍進行中，不讀外部 rollout。required authority／執行責任 = **dispatcher（Orchestrator）** |
| Executor 的未版控 raw stdout 與 mutation 操作歷程 | **NOT VERIFIED**。worktree 不含該 scratchpad／操作原始紀錄；沒有外部存取。本次自行重跑一般 tests、xfail 與探測，不把 mutation 自述當獨立證據。完整 stdout 缺口依 R1-F2 由 **Executor** 在最終 subject 補齊 |
| SPEC-B1 跨 Ticket 整合、SB1-AC2／AC3 完成與 phase acceptance | **NOT RUN as SIA**。本派工明確不是 SIA；#11 的三個缺口仍在。由 **Orchestrator** 在各票結案後另派 Spec Integration Audit，再交 **Design Authority** phase acceptance。未對 RI-1～RI-3、freeze list 或產品的 research fallback 作完成宣稱 |

兩項 blocking findings 的下一步為 #10 Executor targeted correction 與 evidence 更新，再由 Primary 作 R2 scoped closure review；不需要本 reviewer 修改程式或作新的設計裁決。

Verdict: BLOCKING
