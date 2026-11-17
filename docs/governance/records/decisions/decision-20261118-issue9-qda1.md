# Decision record — Q-DA-1：#9 重建流程的「不開啟」範圍與檔案別名（CL-B1-11）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue9-qda1`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | Orchestrator，run `run-20261117-oc1-run2`（run record 第 6 節事件 13）。問題由 FA ruling `ruling-20261117-issue9-c1.md` 第 3.4 節 route 至 DA；源自 Alternate record `issue-9-c1-alt.md` 的 routing signal 與 worklog `issue-9.md` 的 C-9-5b |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 所屬 Spec | SPEC-B1 v1（`derivation-spec-b1.md`）。本 record 是 SPEC-B1 的一則 clarification（治理 §5.3 第 2 類），編號 **CL-B1-11**，與 CL-B1-1～CL-B1-7（`derivation-spec-b1.md` §4）、CL-B1-8（`decision-20261117-issue7-spike-tests.md`）、CL-B1-9／CL-B1-10（`decision-20261117-issue9-e1-and-trim.md`）並列引用 |
| Subject 基準 | 主 checkout branch `oc1-run2-b1-ui0-r1-routing`，HEAD `7f372cfea1e8e90bc12a88f98942990fc70be413`；`git diff --stat 09d150f..HEAD -- src tests` 沒有輸出，程式與測試等於 cycle 1 的受審 subject（程式與測試 `6f97561`） |
| Issue #9 原文 | 派工所附 scratchpad 檔，本 record 實測 SHA-256 `30a898f84957f2ddeab16cad09512c82c807857656b0ac89211e75e79fa69895`，等於 BD-3 |
| 依據的條文 | 治理 §1.2（boundary 段）、§1.5、§2.4、§2.5（能力不代替 routing；E-DA）、§3.6、§3.6-A、§5.3；Bindings m3 第 2.4、2.6（RB-7）、3.2（E-DA）、5、7 節；OC-1 §2.1、§2.3、§3.1 AB-3／AB-10／AB-11、§4.2；`derivation-spec-b1.md` §4 CL-B1-3、§5 #9 列與 E-1～E-5、§6 SB1-AC5、§7；`decision-20261117-high-risk-categories.md` §3.2、§3.3 第 1 項、§3.4、§5；first-run derivation `decision-20261117-oc1-first-run-derivation.md` 的 G-ING 與 A-4 |
| 讀過的證據 | Bindings m3；治理本文 §1.2、§1.5、§2.4、§2.5、§3.6、§5.3；OC-1 第 1–4 節；`derivation-spec-b1.md`；CL-B1-9／10 record；高風險類別 record（§3.3、§5 相關段）；first-run derivation 的 G-ING、A-4 兩列；FA ruling 全文；R1、R2、Alternate records 中與連結、stat、雜湊、去重複有關的段落（Alternate 全文）；worklog `issue-9.md` §8 C-9-5、§10.1、§10.4、C-9-5b、C-9-6；Issue #9 原文；`DESIGN.md` §5「資料處理流程（GPX）」第 5–6 項、「版控外的私有資料」表、契約 1 欄位表與「凍結之前不產生保留行程的列」、§6.2 保留行程的選取規則與 P-5 段；`SPEC-001` 第 53 行（`trip_id`）、S45；`SPEC-RESOLUTION-001` SB2-T11；`src/moto_copilot/ingest/__main__.py` 全文；`tests/test_ingest_cli.py` 的測試清單與 audit hook 的說明 |

本 record 撰寫時實際執行的（不讀 GPX、不需金鑰）：

| 指令 | 結果 |
| --- | --- |
| `sha256sum` Issue #9 原文 | 如上，等於 BD-3 |
| `git rev-parse HEAD`、`git status --short`、`git diff --stat 09d150f..HEAD -- src tests` | HEAD `7f372cf`；工作區乾淨；`src`、`tests` 無差異 |
| 自寫探測程式（session scratchpad，主 checkout 的 `.venv` Python 3.11.2，`-I -B`；在 scratchpad 內建立暫存資料夾與一個內容為 `x` 的合成檔，結束時刪除） | 一般檔 `os.stat().st_nlink == 1`，`st_file_attributes == 0x20`；`os.link` 不需特權即成功，之後兩個名稱的 `st_nlink` 都是 2；`os.symlink` 失敗，`OSError`，`winerror 1314`（缺少建立符號連結的特權） |

---

## 1. 問題

FA ruling 第 3.4 節的 Q-DA-1，四個子題：

1. #9 的隔離要求（`DESIGN.md` §5「保留行程與被排除的行程的檔案不開啟」、CL-B1-3 第 4 項、SB1-AC5）是否要求重建流程辨識：(a) pace 項目與非 pace 項目指向同一檔案物件的不同目錄項目（hard link）；(b) 解析到非 pace 項目所指檔案的符號連結、junction 或其他 reparse point；(c) 內容相同、名稱不同的兩個檔案。
2. 以 stat、檔案識別碼、連結列舉或目錄列舉取得非 pace 項目所指檔案的 metadata，是否與「不開啟」相容。
3. 若需要辨識，屬 #9 或另一個 work item（例如 G-ING）。
4. 涉及開啟或雜湊保留行程內容的部分，required authority＝acceptor；DA 無法確立在 OC-1 boundary 內時，受影響路徑 fail-closed 至 acceptor。

不在本 record 的範圍：FA 已裁決的 R2-F1（同一目錄項目的其他拼法：預設資料串流寫法、8.3 短檔名、大小寫等）的 rework 範圍與 closure 證據（FA ruling 第 3.2 節），本 record 不改變、不重述；C-9-6（整份清單拒絕）沒有交付本 record。

## 2. 裁決要旨

| 子題 | 裁決 |
| --- | --- |
| 1(a) hard link | **#9 要辨識，且只以 pace 項目自身的資訊辨識**：pace 項目所指的目錄項目有其他 hard link（連結數大於 1）時，在開啟任何 GPX 之前拒絕（CL-B1-11 第 3 項） |
| 1(b) 符號連結等 | **pace 那一邊 #9 要辨識**：pace 項目所指的目錄項目是符號連結時，同樣在開啟任何 GPX 之前拒絕。**非 pace 那一邊**（非 pace 項目是指向 pace 檔的符號連結）**#9 不要求**，與 (c) 同類處理（第 4 項）。Junction 只能指向資料夾，`source_file` 又只能是單純檔名，不構成開檔路徑，無需另行處理 |
| 1(c) 內容相同、名稱不同 | **#9 不要求**。屬「同一趟行程的資料在清單中有兩個角色」，DESIGN §5 把它分配給第 5 步的內容去重複（G-ING）；既有資料由 acceptor 已完成的角色指定負責（第 4 項） |
| 2 metadata | 重建流程對**非 pace 項目所指的目錄項目**不作任何檔案系統操作，包括 metadata（stat／lstat、檔案識別碼、連結列舉、讀取連結目標、短檔名查詢、大小、時間）。**相容而允許的**：清單本身的字串；GPX 資料夾的目錄列舉，只使用名稱；對 pace 項目所指目錄項目的任何查詢（第 1 項）。其他工作若需要取得保留行程檔案的 metadata 或內容，DA 無法確立在 OC-1 boundary 內，fail-closed 至 acceptor（第 7 節） |
| 3 歸屬 | (a) 與 (b) 的 pace 那一邊：**#9，cycle 2 一併納入**。(c) 與非 pace 那一邊的別名：**不在 #9**；屬 G-ING（Profile 管理與內容去重複，AB-3）的範圍，連同 G-ING 第 (2) 項的雜湊來源問題 |
| 4 acceptor | 本裁決沒有任何部分需要開啟、讀取、stat 或雜湊保留行程的檔案；#9 不受 fail-closed 影響。需要 acceptor 的事項見第 7 節 |

## 3. CL-B1-11（#9）重建流程的「不開啟」範圍與檔案別名

本節是 SPEC-B1 的 clarification，Executor、Reviewer 與 Spec Integration Audit 以本節為準。「重建流程」依 CL-B1-3 第 4 項。

1. **「不開啟」的範圍。** CL-B1-3 第 4 項、SB1-AC5 與 `DESIGN.md` §5 所說的「不開啟」，在凍結前的重建流程中指：重建流程不對**清單中非 `pace` 項目所指的目錄項目**作任何檔案系統操作——開啟內容、讀取、雜湊，以及 metadata 查詢（stat／lstat、檔案識別碼、連結列舉、讀取連結目標、短檔名查詢、大小、時間）都在內。下列三種不是對非 pace 項目的操作，允許：
   1. 使用清單本身的字串（`trip_id`、`source_file`、`trip_role` 等）。
   2. 列舉 `--gpx-dir` 資料夾中的目錄項目，**只使用名稱**；列舉結果附帶的其他屬性（大小、時間等）不得使用、記錄或輸出。
   3. 對 **pace 項目所指的目錄項目**作 metadata 查詢或名稱解析（例如取得它的連結數、是否為符號連結、它的短檔名）；它本來就是要開啟的檔案。
2. **同一目錄項目的其他拼法**：依 FA ruling 第 3.2 節（R2-F1 的 rework），本 record 不改變。第 1 項的允許範圍同樣適用於該 rework：凡是只使用清單字串、目錄列舉的名稱，或 pace 項目自身資訊的做法，不需要再 route 至 DA；使用非 pace 項目所指目錄項目的任何資訊的做法，依第 1 項不得採用。
3. **pace 那一邊的連結別名。** 在開啟任何 GPX 的內容之前，重建流程對**每一個被選中的 pace 項目**確認它所指的目錄項目：(i) 不是符號連結；(ii) hard link 的連結數是 1。任一 pace 項目不符時，整次重建拒絕：exit 2、不寫出衍生路段表與報告、沒有任何 GPX 的內容被開啟；錯誤訊息只列出行程代號，不列檔名（與 R1-F1 修正的訊息一致，H-2）。所有被選中的 pace 項目都通過檢查之後，才開啟第一個 GPX。自動選擇與 `--trips` 明確指定都適用。
   - 理由：這兩種情形正是 pace 項目可能與某個非 pace 項目（或任何其他目錄項目）是同一個檔案物件的情形，而且只用 pace 項目自身的資訊就能判定，不碰任何非 pace 項目。連結數大於 1 時無法得知另一個名稱是誰，所以一律拒絕；兩個 pace 項目互為 hard link、或 pace 檔另有清單以外的 hard link 時也拒絕，這是 fail-closed 一側的誤拒，代價是一則明確的錯誤（H-4）。
   - 做法（以何種 API 取得連結數與連結種類、拒絕的程式位置、錯誤類型）是 Executor 的 HOW。
4. **#9 不要求、也不得以第 1 項禁止的方式處理的情形（殘餘，分配給 G-ING）。** (i) 內容相同、名稱不同的兩個檔案（複本）；(ii) 非 pace 項目本身是指向 pace 檔的符號連結；(iii) 其他「不同目錄項目承載同一趟行程的資料、而 pace 項目自身看不出來」的情形。這些都是同一趟行程在清單中同時有 pace 與非 pace 角色；辨識它們需要非 pace 項目的 metadata 或內容。重建流程以行程清單為 `trip_id` 與角色的唯一來源（SPEC-001 第 2 節；CL-B1-3 第 5 項的理由），不保證不同目錄項目承載不同的行程。
5. **威脅模型。** 第 3 項防的是騎士自己的資料或工具造成的意外污染，不是蓄意的竄改：檢查與開檔之間檔案被替換（TOCTOU）不在要求內。
6. **SB1-AC5 的讀法。** 「沒有任何程式路徑會在重建時開啟非 `pace` 的行程檔案」指：(i) 不開啟清單中非 pace 項目所指的目錄項目（不論以哪一種會被作業系統解析到它的拼法，FA ruling 第 3.2 節）；(ii) 不開啟本身是符號連結或連結數大於 1 的 pace 項目（第 3 項）；(iii) 對非 pace 項目不作第 1 項所列的任何操作。第 4 項的殘餘不在 SB1-AC5 之內，Spec Integration Audit 不得把它記為已涵蓋，也不得以它為由判定 SB1-AC5 不成立。

### 3.1 #9 cycle 2 的 closure 證據（SPEC-B1 對 #9 的另加驗收條件，屬 verification contract）

以下與 FA ruling 第 3.2 節的 closure 證據並列，由 cycle 2 的 Reviewer 判定；本 record 不預判結果。

| 編號 | 證據 |
| --- | --- |
| L-1 | 以真實的 hard link（測試中以 `os.link` 對合成檔建立；本 record 開頭的執行表觀測到在此環境不需特權即可建立）走完整的 CLI，至少三例：(1) pace 項目是 `holdout` 項目所指檔案的另一個 hard link，自動選擇；(2) 同 (1)，`--trips` 指定該 pace 行程；(3) 方向相反——pace 項目是原檔、非 pace（`excluded`）項目是另一個 hard link 名稱。每一例斷言 exit 2、audit hook 觀測到 GPX 資料夾內沒有任何 `open` 事件、沒有輸出檔，且錯誤訊息不含檔名 |
| L-2 | 符號連結的情形以一個走完整 CLI 的測試表現，其證據**不得依賴建立符號連結的特權**（本 record 觀測到 `os.symlink` 在此環境以 `winerror 1314` 失敗）；做法是 Executor 的 HOW（例如在測試中替換作業系統對該目錄項目的回答），在 worklog 寫明。執行環境可以建立真實符號連結時，另記一次實際觀測；不能時記 NOT RUN。不得新增 `skip`／`xfail` 標記（CL-B1-9 第 2 項第 iii 款；CL-B1-8 §3.4 K-1） |
| L-3 | 一般的 pace 檔（連結數 1、不是符號連結）照常重建：既有的 `test_only_pace_entries_are_opened_and_the_result_passes_the_contract`、`test_requested_pace_trips_are_the_only_ones_opened` 與 `test_non_pace_entries_sharing_a_file_and_distinct_pace_files_are_not_a_conflict` 不改斷言而通過；若需修改，在 worklog 逐項列出理由（E-4） |
| L-4 | 第 1 項的符合性：worklog 列出重建流程在開啟 GPX 之前與之時所作的每一種檔案系統操作，以及各自作用在哪一類目錄項目（清單、資料夾列舉、pace 項目）；Reviewer 以閱讀程式核對沒有任何操作作用在非 pace 項目所指的目錄項目。Python 的 `open` audit 事件不涵蓋 stat 類呼叫，所以這一項不能只以既有的 audit hook 證明 |
| L-5 | 陳述與證據相符（H-3）：`ingest/__main__.py` 的模組說明與相關 docstring、worklog §10.1 的殘餘清單與 §10.4 的 H-3 陳述，改為與 CL-B1-11 一致；殘餘只列第 4 項的情形並引用本 record；不再寫「偵測這些需要 stat 或讀取非 pace 的檔案」這種把 hard link 與符號連結並列為無法處理的說法。C-9-5b 由本 record 取代 |
| L-6 | E-2 加列 CL-B1-11 第 3 項對應的測試名稱與結果；E-5 的 H-2、H-3、H-4 self-verification 涵蓋第 3 項與第 1 項 |

## 4. 理由

**4.1 為什麼 (c) 與非 pace 那一邊的別名不在 #9。**
- `DESIGN.md` §5 的資料處理流程把兩件事分在兩步：第 5 步「新上傳的檔案併入行程清單，以內容去重複…內容和保留行程或被排除的行程相同的檔案以內容去重複略過，不重新歸為配速行程」；第 6 步「以配速行程重建配速表…保留行程與被排除的行程的檔案不開啟」。同一趟行程以不同檔案出現在不同角色，契約明文由第 5 步的內容去重複處理。§6.2 P-5 段也是同一分工（「介面上傳歷史 GPX 時，內容和保留行程…相同的檔案以內容去重複略過」）。
- Issue #9 的排除範圍明列「歷史 GPX 的多檔上傳與去重複」；first-run derivation 把內容去重複列為 G-ING（未 ready），其中第 (2) 項（保留行程的內容雜湊從哪裡來）已記 required authority＝acceptor。
- 辨識這些情形需要非 pace 項目的 metadata 或內容；第 1 項不允許（理由見 4.3）。
- 既有的 21 個檔案的角色是依 §6.2 的規則、在 acceptor 主導下指定的（2026-11-15，只讀起始時間），行程清單是角色的唯一來源。重建流程以清單為準，是既有來源唯一合理的分工。

所以這部分只有一種合理解讀，屬治理 §3.6-A「既有來源只有一種合理解讀而尚未寫下」。

**4.2 為什麼 (a) 與 (b) 的 pace 那一邊要在 #9。**
- 這兩種情形與 (c) 不同：開啟的是**同一個檔案物件**。pace 項目若是保留行程檔案的 hard link 或符號連結，重建流程讀到的就是保留行程的檔案本身。字面上落在 `DESIGN.md` §5「保留行程…的檔案不開啟」與 SB1-AC5「沒有任何程式路徑」之內，也落在高風險類別 H-3 判定第 1 項「任何可能在凍結前開啟保留行程的程式路徑」與 §5 的最低核對範圍之內。
- 可以只用 pace 項目自身的資訊、在開檔前判定（連結數、是否為符號連結），不碰任何非 pace 項目，所以與第 1 項及 R1、R2、Alternate、FA 都要求的「不讀取、不雜湊非 pace 的檔案」相容。本 record 在此環境觀測到 hard link 的連結數可由標準函式庫取得、測試可以在不需特權的情形下建立 hard link（本 record 開頭的執行表）。
- 成本有界：一項開檔前的檢查與數個合成測試，在 #9 的範圍（「凍結之前的重建流程只處理配速行程」）之內，不新增清單欄位、不實作去重複或上傳。
- 另一種合理設計是「#9 只以名稱為準，連結全部歸入殘餘」。兩者的差別是：一個已知、可在開檔前以低成本判定、而且讀到的就是保留行程檔案本身的路徑，留著還是關閉。H-3 的污染不可撤銷（`DESIGN.md` §6.2），H-4 要求不確定時 fail closed；在可判定、成本低、又不需要額外權限的情況下保留這條路徑沒有對應的好處。這是依既有證據與已確認的高風險類別作出的設計判斷，不是證據無法裁決的分歧，所以不構成 E-DA/D1。
- 非 pace 那一邊的符號連結（非 pace 項目指向 pace 檔）不一樣：pace 檔本身是一般檔案，重建讀到的是 pace 檔的內容；問題在於清單讓同一份資料同時有兩個角色，與 (c) 同類，且只能從非 pace 項目看出來。

**4.3 為什麼非 pace 項目的 metadata 不用。**
- 需要性：第 3 項只用 pace 項目自身的資訊；FA 的 rework 依 Alternate 與 FA 的可修性證據，也可以只用名稱（第 3 節第 2 項）。#9 沒有任何要求需要非 pace 項目的 metadata。
- 資訊內容：檔案大小與時間會透露行程的長度與日期。§6.2 連「讀取保留行程的起始時間」都是在 acceptor 主導下、記錄在案的一次性動作；OC-1 §2.3 與 RB-7 第 (2) 項規定保留行程在凍結前不得讀取、解封由 acceptor 決定。在 Windows 上取得檔案識別碼或連結數也要對該檔案開一個 handle。是否把這些算作「讀取」，DA 不能代 acceptor 認定（第 7 節）。
- 目錄列舉只使用名稱是相容的：名稱就是清單裡已有的 `source_file`，列舉不開啟任何目錄項目；BASE `0c109aa` 的重建流程也以列舉比對名稱。

**4.4 不構成 E-DA/D2。** 本 record 涉及的先前 DA 決定（CL-B1-3 第 4 項、SB1-AC5）沒有被 FA ruling 或經 route 的 Reviewer finding 推翻或實質爭議：FA 與 Alternate 都是適用它們，並指出契約對連結與內容重複沒有寫定。本 record 是補寫，不是推翻。

## 5. 是否改變 accepted 語義

**否。**
- OC-1 的 accepted 語義是「保留行程在分析方法與模型設定凍結前不得讀取」（§2.3）與 RB-7。第 3 項使重建流程在一種原本會讀到保留行程檔案本身的情形下拒絕，是更嚴格的適用；第 1 項把「不開啟」寫定為連 metadata 都不碰，也是更嚴格的一側。
- 第 4 項的殘餘分配依 `DESIGN.md` §5 第 5、6 步原有的分工，不新增、不移除任何 Outcome Contract 的 requirement、AC 或 scope，也沒有把任何 accepted 要求改為不適用：它寫定的是 #9 的重建流程**本來就沒有被分配**的部分。
- CL-B1-11 屬 SPEC-B1 這個 derived contract 的 clarification，加上一組 verification contract（第 3.1 節），是治理 §5.3 第 2 類，不觸發 acceptor 核准。沒有豁免任何 audit 或 gate；沒有改變高風險類別的標示。

## 6. Boundary determination

**在 OC-1 boundary 內。**
- #9 的變更：屬 OC-1 §2.1 第 1、3 項（`ingest`、`tests`、Spike 的收編）與 SPEC-B1 已分配的 AB-10、AB-11 部分（「保留行程不進重建」「保留行程拒絕」）；在 Issue #9 的範圍「凍結之前的重建流程只處理配速行程…不開啟檔案」之內；測試只用合成資料（OC-1 §2.3）；不新增 Must 或 Should。
- 第 4 項的殘餘：分配到 G-ING，G-ING 屬 AB-3（FR2：多檔上傳、合併去重複），本來就在 OC-1 §2.1 第 1 項；本 record 沒有新增範圍。
- 本 record 沒有任何部分需要開啟、讀取、stat 或雜湊保留行程或被排除行程的檔案，也不需要讀取 `data/`。

## 7. 需要其他 authority 的事項

| # | 事項 | Required authority | 處理 |
| --- | --- | --- | --- |
| A-1 | 任何在凍結前取得保留行程或被排除行程檔案的 metadata（大小、時間、檔案識別碼、連結資訊）或內容（開啟、雜湊）的設計，包括 G-ING 為了跨角色的內容去重複而需要的雜湊或識別資訊 | **acceptor**（OC-1 §2.3；RB-7 第 (2) 項；G-ING (2)；first-run derivation A-4） | DA 無法確立這類存取在 OC-1 boundary 內（「不得讀取」是否涵蓋 metadata 屬 acceptor 的認定）。受影響的路徑——G-ING 中需要它的部分——依治理 §1.2 fail-closed 至 acceptor，只停止該路徑。**不影響 #9**：#9 依 CL-B1-11 不需要它 |
| A-2 | 真實的 GPX 資料夾與行程清單中，是否已有跨角色的 hard link、符號連結或內容相同的檔案（第 4 項的殘餘在既有資料上是否實際存在） | **acceptor**（RB-7；需要列出或讀取 `data/`，比對內容另需 A-1 的決定） | NOT VERIFIED。Issue #9 排除以真實 GPX 重建（C-9-3／NV-1 已記 acceptor）。建議 Orchestrator 在 acceptor 授權第一次以真實資料重建之前，把本項連同 FA ruling 的 NV-2（8.3 短檔名）一併告知 acceptor；acceptor 可依自己對資料夾的了解確認，Agents 不自行查證 |

不需要 escalation：E-DA/D1、D2 都不成立（第 4.2、4.4 節）。

## 8. 受影響的 work items 與 evidence

| Work item | 影響 |
| --- | --- |
| #9 B1-2 cycle 2 rework（`gov-executor`，worklog `issue-9.md`） | FA ruling 第 3.2 節的 rework **加上** CL-B1-11 第 3 項的檢查與第 3.1 節 L-1～L-6 的證據。FA ruling 第 3.2 節第 2 項中「依賴 stat、檔案識別碼、連結列舉或內容取得非 pace 項目所指檔案資訊」的做法，依 CL-B1-11 第 1 項**不得採用**；只用清單字串、目錄列舉的名稱或 pace 項目自身資訊的做法可以直接採用，不需再 route。不實作內容去重複、不新增清單欄位、不實作上傳（維持 FA 第 3.2 節第 3 項）。這是 FA ruling 第 3.3 節第 4 項所說「DA 的 decision record 要求 #9 作出的變更」 |
| #9 cycle 2 R1（Primary Reviewer） | Bounded pack 加入本 record 路徑；R1 依 CL-B1-11 第 1、3、6 項與第 3.1 節核對，並依 FA ruling 第 3.2 節核對 R2-F1 的 rework。第 4 項的殘餘不是 #9 的 finding 對象 |
| SPEC-B1 Spec Integration Audit | SB1-AC5 依 CL-B1-11 第 6 項判定；第 4 項的殘餘列入「已知不在本 Spec 涵蓋內、SIA 不得記為已涵蓋」的項目（與 `derivation-spec-b1.md` §6 末段並列） |
| G-ING（之後的 Profile 管理 Spec；目前未 ready） | 其 derivation 必須涵蓋 CL-B1-11 第 4 項的殘餘：上傳時與保留行程或被排除行程相同的檔案（含連結形式）的辨識，以及非 pace 項目為別名的情形；所需的雜湊或識別資訊來源依第 7 節 A-1 由 acceptor 決定。Tracking owner：Orchestrator（本 run 不納入 G-ING；在 run record 記下本 record 對 G-ING 範圍的補充，供之後的 derivation 引用） |
| #10 B1-3 | 不受影響：`pace` 的保留行程拒絕依衍生路段表的 `trip_role`（CL-B1-4 第 10 項），不開啟 GPX |
| E1 Lite／E2 的隔離評估腳本（AB-11） | 不受影響：它們在凍結後才使用保留行程 |
| AB-12 的文件工作 | `DESIGN.md` 的實作狀態與限制（§12）在 #9 結案後更新時，應如實寫出第 4 項的殘餘與它的歸屬；不得寫成重建流程已能辨識內容重複 |
| 既有 evidence | cycle 1 的測試與 R1-F1 的 regression tests 不受影響，仍須保留並通過（FA ruling 第 3.2 節 closure 證據第 3 項）。worklog C-9-5b 與 §10.1 的殘餘陳述由本 record 取代（第 3.1 節 L-5）。`6f97561` 不是 #9 的最終 subject |

`derivation-spec-b1.md`、CL-B1-8／9／10 records 與 FA ruling 沒有被修改；SPEC-B1 v1 的引用集合由本 record 補上 CL-B1-11，Orchestrator 與 Reviewer 以本 record 路徑引用。

---

本 record 只執行了開頭執行表所列的指令與 scratchpad 內的合成檔探測；沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有讀取或執行 `experiments/` 下的任何檔案，沒有讀取保留行程，沒有從 repo root 搜尋，沒有修改程式、測試、Spec、Issue 或其他 record，沒有派工任何 subagent，沒有 commit。

Decision: Q-DA-1 — CL-B1-11。#9 cycle 2 須加上 pace 項目的連結別名檢查（hard link 連結數大於 1、符號連結 → 開啟任何 GPX 前拒絕）與 L-1～L-6 的證據；對非 pace 項目不作任何檔案系統操作（含 metadata），目錄列舉只用名稱；內容重複與非 pace 那一邊的別名不在 #9，歸 G-ING；取得保留行程 metadata 或內容的設計 fail-closed 至 acceptor。不改變 accepted 語義；在 OC-1 boundary 內。
