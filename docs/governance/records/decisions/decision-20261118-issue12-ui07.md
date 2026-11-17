# Decision record — Issue #12（SPEC-UI0）UI0-7：日曆彈窗（K9-F）與 BLOCKED 的結案效果（K3-B）

| 欄位 | 內容 |
| --- | --- |
| Record ID | `decision-20261118-issue12-ui07`（v1） |
| 日期 | 2026-11-18 |
| 決定者 | Design Authority（`design_authority`，以 `gov-design-authority` 派工；binding 由派工者依 Bindings 第 3.6 節核對並記錄，本 record 不自述 binding） |
| 派工來源 | OC-1 第二個 Formal run 的 Orchestrator：`docs/governance/records/run/run-20261117-oc1-run2.md` §6 事件 46–48（事件 48：契約語義與 sufficiency 的分類，治理 §2.4 DA-first） |
| Outcome Contract | OC-1（`docs/governance/records/outcome-contract.md`），acceptor 2026-11-17 針對 `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| Spec | SPEC-UI0 v1（`derivation-spec-ui0.md`，commit `8c3c588`），含 CL-UI0-1～CL-UI0-5；`decision-20261118-issue12-ui0.md` 對 CL-UI0-2 的釐清 |
| Ticket | #12（UI-0）。Issue 原文：派工所附 `issue-12-body.md`，本次實測 SHA-256 `79614ef79554b1601e40538772fc1f84d29a64d49fe6a334371f856127be18be`，等於 BD-3 |
| 受審 subject | branch `oc1-run2-b1-ui0-r1-routing`，HEAD `314376f`（本次 `git rev-parse HEAD` 核對，工作目錄乾淨）；實作 commit `6a278b4`，correction commit `619268a` |
| 依據的條文 | 治理 §1.2、§1.5、§2.4、§3.6、§3.8、§4.2、§4.5、§5.2、§5.3；orch-default v2.2 §6、§7（P3–P6）、§8、§9；Bindings m3 第 2.4、2.6、5 節 |
| 讀過的證據 | Bindings m3 全文；治理 §1、§2.4、§3.6、§3.8、§4.1–§4.2、§5.2–§5.3；orch-default v2.2 §6–§9；OC-1 §2.1、§3.1（AB-8、AB-10、AB-13）、§3.2、§4.2；`derivation-spec-ui0.md` 全文；`decision-20261118-issue12-ui0.md` 全文；R1 record `audit/issue-12-c1-r1.md` 全文（R1-F2、NV-1）；worklog `worklog/issue-12.md` 全文（第 6 節 E-2、第 7 節、第 10 節 K1～K12、10.3）；run record 檔首、第 1 節、事件 42–48；Issue #12 原文；`docs/ui/UI_CR01_DELTA.md` 第 11.2 節與第 419 行（只讀）；`docs/ui/UI_ACCEPTANCE.md` F3、F4 列與第 3.4 節（只讀）；`DESIGN.md` 第 1085、1494 行（§9.6、P-11）；`docs/cr/CR-01-proposal-alignment.md` 第 370 行（P-11 裁決）、`docs/cr/CR-01-appendix/ui0_decision_table.md` 第 73 行；`app/ui0_mock_app.py` 第 265–280 行（`st.date_input` 的用法）；`.venv` 內 Streamlit 1.67.0 前端 `static/static/js/DateInput.BHx02NDa.js`（日曆彈窗的屬性）。沒有讀取、列出或搜尋 `data/`，沒有讀 `.env`，沒有執行 `experiments/`，沒有啟動 Streamlit 或瀏覽器 |
| **結論摘要** | **K9-F**：UI0-7 以「操作」（騎士要完成的事）為單位，不要求標準元件的每一種指標裝置用的替代介面都能用鍵盤操作；「選日期」已可只用鍵盤完成（K10），日曆彈窗沒有困住焦點。**#12 不需要修正程式**；K9 在 worklog 改記為元件的限制與觀察，不是 UI0-7 的 FAIL。**K3-B**：(1) 一般規則：在 #12 範圍內的 AC 有任何部分記為 BLOCKED 時，#12 **不能**結案；BLOCKED 加上之後的 UI Delta Review 不是 orch-default §7 的 disposition。(2) 本件：作業系統的原生檔案對話框不是 Skeleton 的畫面，不在 #12 的 UI0-7 範圍內；#12 的範圍是「開啟選檔」的頁面控制項與選檔之後的頁面操作，已有 K3、K5、K6 的紀錄。K3-B 改記為範圍外的 NOT VERIFIED，不擋 #12。兩項都不改變 accepted 語義、在 OC-1 boundary 內、**不需要 acceptor 的接受或授權**；交 acceptor 的資訊見第 7 節。沒有 capability escalation |

## 1. 問題

1. **K9-F**：worklog 第 10.2 節 K9 觀察到 `st.date_input` 的日曆彈窗可以用 Enter／Space 打開，但鍵盤焦點進不了彈窗（Tab 離開時彈窗關閉，方向鍵沒有作用，Escape 關閉並把焦點還給按鈕）；K10 以年／月／日欄位只用鍵盤改了日期。UI0-7「所有操作都可以只用鍵盤完成」是否要求日曆彈窗本身可用鍵盤操作；若是，#12 的修正是否在範圍與 CL-UI0-1 內可行，或屬 contract change。
2. **K3-B**：在作業系統的檔案對話框中只用鍵盤選取多個 GPX，內建瀏覽器工具無法操作，Executor 依 CL-UI0-4 記為 BLOCKED。一項 AC 有部分依 CL-UI0-4 記為 BLOCKED 時，#12 能否依 orch-default §7 結案（以 BLOCKED 加上 acceptor 的 UI Delta Review 作為該部分的 disposition），或必須等 acceptor 檢視。

## 2. 事實與來源（獨立核對）

### 2.1 UI0-7 的來源與它的強度

- Issue #12 UI0-7：「所有操作都可以只用鍵盤完成。」Issue 的目的段：驗證「畫面與操作流程、Streamlit 1.67.0 的元件是否可行、375 像素的手機寬度與鍵盤操作」。上傳一節：「歷史 GPX 的上傳**只驗證元件的操作**：可以選取多個檔案、按下『更新 Profile』」。元件一節：「只用標準元件」。日期欄是「其他欄位不變」所列的 G3 欄位。
- UI0-7 的上游是 acceptor 2026-11-15 的審查處置 **P-11**（`CR-01-proposal-alignment.md` 第 370 行、`DESIGN.md` 第 1494 行）：「**保留基本的驗收**：375 像素寬度沒有整頁溢出、可以用鍵盤操作」。`UI_CR01_DELTA.md` 第 11.2 節把它寫成「操作都可以只用鍵盤完成」，並寫明「F3、F4 原文中**超出這兩項的部分**是否沿用，在 Streamlit 的驗收清單定稿時確認」。G3 的 F4 原文是「分頁可以用鍵盤操作；互動元件有看得見的焦點樣式」（`UI_ACCEPTANCE.md`）。
- 所以 UI0-7 是 acceptor 明示的「基本」要求：每一項操作可以只用鍵盤完成。比它更嚴的逐元件要求（例如焦點樣式、每個控制項的每種互動）尚未被採用，留到之後的 Streamlit 驗收清單定稿時決定。

### 2.2 K9／K10 的紀錄

- K9：`Choose date` 按鈕可用 Enter／Space 打開彈窗（`role=dialog`，文字「Use arrow keys to navigate dates. Enter to select. Escape to close.」）；焦點留在按鈕；方向鍵無作用；Tab 讓焦點到下一個欄位並關閉彈窗；Escape 關閉並把焦點還給按鈕。Executor 記為「FAIL（本環境觀察）」。
- K10：Shift+Tab 到日欄、↑ 改日；Shift+Tab 到月欄、輸入 `11`；日期 2026/12/06 → 2026/12/07 → 2026/11/07，過期提示列出「日期」。這些欄位就在同一個 `st.date_input` 內，位於一般的 Tab 順序中。
- Streamlit 1.67.0 前端 `DateInput.BHx02NDa.js`：彈窗容器有 `role="dialog"`、`aria-modal="true"`、`aria-label="Choose date"`、上述的操作說明文字與 `onKeyDown` 處理，日曆以 `focusedValue` 管理焦點。也就是說，元件的設計**預期**彈窗可用鍵盤操作；K9 的現象是本環境（內建瀏覽器工具送出的按鍵與焦點）中的元件行為還是工具的限制，本次沒有實測，**原因未確定**。
- App 的用法是預設的 `st.date_input("日期", value=…, key=…)`（`app/ui0_mock_app.py` 第 273 行），沒有自訂。

### 2.3 K3／K3-B／K4～K6 的紀錄

- K3：在「Upload」按鈕上按 Enter、Space，各送出一次選檔請求 `{multiple: true, accept: "application/streamlit,.gpx"}`（以 capture listener 記錄並取消，避免在桌面留下對話框）。頁面控制項可以用鍵盤啟動：PASS。
- K3-B：對話框內的選檔沒有執行。缺少的能力：內建瀏覽器工具只能操作頁面，不能操作作業系統的對話框，也沒有上傳工具。
- K4：以程式放入三個合成檔（明標「不是鍵盤」）。K5：只用鍵盤移除一個檔案。K6：只用鍵盤按「更新 Profile」並得到合成的處理結果。
- 作業系統的檔案對話框不是 Streamlit 或 app 畫出的內容；#12 無法修改它的行為。

### 2.4 結案的規則

- 治理 §3.8：結案前 MUST 確認 self-verification、必要 gates 與 evidence requirements 已滿足，且沒有影響完成的未決 design ambiguity。
- orch-default §7 P3：evidence 與 gate 結果存在；「gate 不適用或移除，只能源於 DA 不改變 accepted 語義的 clarification（§3.6-A）或經原 acceptance authority 接受的 contract change」。§7 末段：「Required gates 與 disposition 是不同事。Disposition 處理 findings（§4.5），不改變任何 gate 結果」。
- OC-1 §3.2：AB 的 PASS 要求分配到的 derived AC 都依 orch-default §7 結案；「任一分配到的 AC 未結案、證據缺漏」即 FAIL 或未完成；BLOCKED 是如實記錄未完成的方式，不是完成。
- OC-1 §2.1 第 4 項、AB-8、§4.2：UI Delta Review 是 acceptor 的動作，是 AB-8 的**另一項**證據（`derivation-spec-ui0.md` 第 7 節），不在本 run（run record 第 1 節第 6 項）。
- R1 record R1-F2：「CL-UI0-4 保留後續 UI Delta Review，不等於免除 Ticket 的鍵盤證據要求」；「若要把缺少的 evidence 排除於 Ticket closure，須由相應 authority 作明確 clarification／contract change，Reviewer 不代為豁免」。

## 3. K9-F 的裁決

### 3.1 UI0-7 的意思

UI0-7 的單位是**操作**：騎士在畫面上要完成的每一件事（選情境、上傳與更新 Profile、輸入行程描述、選行程型態、設定日期與時間、輸入油量、規劃、回覆追問、切換分頁、展開區塊……），都要有一條只用鍵盤就能完成的路徑。它**不**要求標準元件為指標裝置另外提供的替代介面（這裡是日曆彈窗）本身也能用鍵盤操作，條件是：

1. 完成同一件事的鍵盤路徑存在，而且在該元件內、位於一般的 Tab 順序中，不需要先使用指標裝置；
2. 那個替代介面不會困住焦點，也不會讓已輸入的值遺失或改變（不形成 keyboard trap）。

依據：P-11 的原文是「保留**基本的**驗收……可以用鍵盤操作」；DELTA 11.2 寫明超出「操作都可以只用鍵盤完成」的 F4 部分尚未沿用；Issue 的鍵盤驗證目的是確認標準元件的操作流程可行，且要求「只用標準元件」。把 UI0-7 讀成「每個元件的每種互動都可用鍵盤」，會把 DELTA 11.2 明示尚未採用的逐元件要求提前加進 #12，這是補寫 requirement（治理 §4.2、§5.3），不是解讀。

### 3.2 套用到 K9／K10

- 「設定日期」這項操作可以只用鍵盤完成：K10 在同一個 `st.date_input` 的年／月／日欄位完成，位於一般 Tab 順序中（條件 1 成立）。
- 日曆彈窗沒有困住焦點：Tab 離開、Escape 關閉並把焦點還給按鈕，日期值沒有因此改變（條件 2 依 K9 的紀錄成立）。
- 所以 **K9 不是 UI0-7 的 FAIL**。它是元件在本環境中觀察到的限制，應記在 UI0-2 的限制與 UI0-10 的紀錄，交 UI Delta Review 檢視。

### 3.3 對 #12 的修正要求：無程式修正

- 不要求 #12 更換 `st.date_input` 或修改 `app/`、`tests/`。
- 為了回答派工的問題（若 UI0-7 要求彈窗本身可用鍵盤）：在 CL-UI0-1 內技術上有可行的做法（例如以 `st.text_input` 或 `st.selectbox` 等標準元件代替日期元件），但那會把 G3 沒有變更的日期欄改成另一種互動、偏離 Issue 的「其他欄位不變」，而且只是為了滿足一項未被採用的逐元件要求。本裁決不採用那種讀法，所以這個問題不成立，也不構成 contract change。
- 之後的正式整合若要把「標準元件的替代介面也要可用鍵盤」列為驗收條件，那是 DELTA 11.2 所說「驗收清單定稿時確認」的事項，由該整合 Spec 處理；若它改變 P-11 的 accepted 語義，依治理 §5.3 經 acceptor。

## 4. K3-B 與 BLOCKED 的結案效果

### 4.1 一般規則（回答派工的第一種情形）

一項在 #12 範圍內的 AC 有任何部分依 CL-UI0-4 記為 BLOCKED 時：

1. 該 AC 的 evidence requirement **沒有被滿足**（治理 §3.8；orch-default §7 P3；OC-1 §3.2）。BLOCKED 是如實記錄未完成的方式，不是完成，也不是 disposition。
2. 「BLOCKED 加上之後由 acceptor 進行的 UI Delta Review」**不能**作為 orch-default §7 的 disposition：disposition 只處理 findings（§4.5），不能讓 evidence requirement 或 gate 成立；UI Delta Review 是 AB-8 的另一項證據、在本 run 之外，不是 #12 的 evidence。
3. 因此 #12 **不能結案**。缺少的能力無法由授權內的 Agent 或工具取得、又沒有合法替代時，這是治理 §1.5 第 4 項的 boundary：只停止 #12 與依賴它的路徑（SPEC-UI0 的 SIA 與 phase acceptance；orch-default §6 要求全部 Ticket 結案後才派 SIA），寫 stop report，**required authority = acceptor**（由 acceptor 提供該證據或能力，或以 contract change 改變該 AC）；不依賴 #12 的路徑（SPEC-R1）繼續。
4. 這是 CL-UI0-4 原本的意思：CL-UI0-4 寫「記為 BLOCKED……不記為 PASS」，沒有寫可以因此結案；它的末句「這兩項之後仍由 acceptor 在 UI Delta Review 實際檢視」是指 UI Delta Review **另外**還會檢視，不是用它代替 #12 的證據。本節只是寫明這一點，不改變 CL-UI0-4。
5. 與 run 的 terminus 不同：run record 第 1 節的 terminus 允許 run 在「已記錄的 BLOCKED」下結束，那是 run completion，不是 work item completion（治理 §3.8「Run completion、work item completion、phase acceptance 與 release authorization MUST 分別陳述」）。

### 4.2 本件：K3-B 不在 #12 的 UI0-7 範圍內

**裁決**：#12 的 UI0-7 涵蓋 Skeleton 在頁面上的操作，也就是 app 與 Streamlit 畫出、#12 能夠影響的介面。作業系統的原生檔案對話框不是 Skeleton 的一部分，它的鍵盤操作性不是 #12 的交付內容，#12 也無法改變它。就「選取多個 GPX、按『更新 Profile』」這項操作，#12 的 UI0-7 要求的是：

- (a) 開啟選檔的頁面控制項可以只用鍵盤到達並啟動，而且送出的選檔請求允許多選、限 `.gpx` —— K3（PASS 的紀錄）；
- (b) 檔案選定之後的頁面操作（檔案清單、移除、「更新 Profile」、處理結果）可以只用鍵盤完成 —— K5、K6（PASS 的紀錄；K4 以程式放入檔案只作為對話框邊界的代替，已明標不是鍵盤操作）。

依據：Issue 上傳一節「只驗證**元件**的操作」；Issue 的鍵盤驗證目的是 Streamlit 元件與畫面的操作流程；P-11 是對 Streamlit 介面的「基本」驗收。三者的對象都是本專案的畫面，沒有任何來源要求本專案證明作業系統對話框的鍵盤操作性。

**效果**：K3-B 不是 #12 範圍內的 BLOCKED，第 4.1 節的一般規則對它不觸發。worklog 把它改記為「範圍外，NOT VERIFIED：作業系統的原生檔案對話框中只用鍵盤多選」，並寫明 #12 的範圍由 K3、K5、K6 涵蓋。它不再是 #12 結案的阻礙；它也**不是** PASS，不得寫成「已驗證可只用鍵盤多選」。

### 4.3 依本裁決，UI0-7 的現況

依第 3 節與第 4.2 節，UI0-7 在 #12 範圍內沒有 BLOCKED 或 FAIL 的部分。各操作是否都有足夠的鍵盤證據、R1-F2 是否 RESOLVED，**由 R2 判定**（治理 §2.4：evidence sufficiency 屬 Reviewer）；本 record 不替 Reviewer 判定 PASS，也不關閉 R1-F2。

## 5. 是否改變 accepted 語義、boundary determination、escalation

| 項目 | 改變 accepted 語義 | 依據 | Boundary |
| --- | --- | --- | --- |
| K9-F（第 3 節） | **否**。治理 §5.3 第 2 類：對 derived AC（UI0-7）的 clarification。它採用 P-11「基本的驗收」與 DELTA 11.2「操作都可以只用鍵盤完成」的原意，沒有刪除 acceptor 已採用的任何要求；DELTA 11.2 明示尚未採用的逐元件要求不在 UI0-7 內 | 第 2.1、3.1 節 | 在 OC-1 boundary 內（§2.1 第 4 項；AB-8 的 Skeleton 部分） |
| K3-B 一般規則（第 4.1 節） | **否**。只寫明治理 §3.8、orch-default §7 與 CL-UI0-4 已有的意思 | 第 2.4、4.1 節 | 在 OC-1 boundary 內 |
| K3-B 本件（第 4.2 節） | **否**。界定 UI0-7 的對象是 Skeleton 的畫面；作業系統對話框從來不是 #12 的交付內容，所以這不是縮減 scope，也不是移除 gate（orch-default §7 P3 所說的 §3.6-A clarification 的類型）。OC-1 的 acceptance semantics（AB-8：Skeleton 的 AC＋acceptor 的 UI Delta Review）不變 | 第 2.1、2.3、4.2 節 | 在 OC-1 boundary 內；不涉及 reserved boundary（RB-1～RB-7） |

- **不需要 acceptor 的接受或授權**：兩項裁決都在 Design Authority 的 contract-sufficiency authority 內（治理 §2.4、§3.6-A），且可由現有來源裁決。為此另設「先問 acceptor」的 gate，會是治理 §5.2 禁止的臨時 gate。
- **沒有 capability escalation**：K9-F 的兩種讀法（以操作為單位／以每個元件的每種互動為單位）後果不同，但 P-11「基本的驗收」與 DELTA 11.2 的明文可以裁決，不構成 E-DA/D1；K3-B 的範圍由 Issue 上傳一節的「只驗證元件的操作」裁決，同樣不構成 D1。R1-F2 指出 CL-UI0-4 不免除 Ticket 的鍵盤證據要求，這與 CL-UI0-4 的原意一致（第 4.1 節第 4 點），沒有推翻 Design Authority 的先前決定；本件的範圍問題在此之前沒有 Design Authority 的決定，不構成 E-DA/D2。

## 6. 對 #12 的要求（具體檔案與證據）

**不修改** `app/`、`tests/`、`.streamlit/`、`pyproject.toml`；不需要新的瀏覽器操作。只要求 Executor（同一 worklog identity）更新 `docs/governance/records/worklog/issue-12.md`，每一處都引用本 record：

1. **檔首「狀態」列**：移除「仍有 BLOCKED 與 FAIL 項目……required authority = acceptor」的敘述，改寫為依本 record 的現況（待 R2）。
2. **第 7 節 UI0-7 列**：結果改依本 record 第 3、4 節記載——K9 不是 UI0-7 的 FAIL（日期以 K10 只用鍵盤完成）；K3-B 不在 #12 的 UI0-7 範圍內，改記為範圍外的 NOT VERIFIED；#12 範圍內的上傳操作由 K3、K5、K6 涵蓋。結果欄由 Executor 依紀錄如實填寫，並註明最終判定屬 R2；不得寫成「作業系統對話框中可只用鍵盤多選」。
3. **第 7 節 UI0-2 的「元件的對應、替代與限制」表**：新增一列限制——「`st.date_input` 的日曆彈窗：本環境中鍵盤焦點進不了彈窗（K9），沒有困住焦點；日期可以在同一元件的年／月／日欄只用鍵盤修改（K10）。元件前端有 `role=dialog` 與鍵盤操作說明，本環境的現象是元件還是工具造成的未確定」。
4. **第 10.2 節 K9 列的判定欄與第 10.3 節的表**：K9-F 由「FAIL（本環境觀察）」改為「觀察／元件限制，不是 UI0-7 的 FAIL（本 record 第 3 節）」；K3-B 由「BLOCKED，required authority = acceptor」改為「#12 範圍外，NOT VERIFIED（本 record 第 4.2 節）；acceptor 可在 UI Delta Review 檢視（CL-UI0-4 末句）」。第 10.3 節末句「UI0-7 因 K3-B（BLOCKED）與 K9-F（FAIL）不能標為 PASS」改為依本 record 的敘述。原先的判定以「已由本 record 取代」標明，不刪除歷史。
5. **第 7 節 UI0-10 列與第 9.1 節**：反映上述變更；第 9.1 節「UI0-7 的 NOT VERIFIED 項目……由 acceptor 在 UI Delta Review 進行」保留，限定為 K3-B 與 K9 的觀察。

證據要求：上述 worklog 更新是 record-only 變更（Bindings 第 7 節，orch-default §7 P7），不改變受審的實作 subject（仍是 `619268a`）。R2 的 bounded pack 應加入本 record；R2 依本 record 評估 R1-F2，R1-F1 照原流程核對。本 record 沒有處理 R1 record 的 Q-1（「資料快照」標籤的適用性，required authority = Design Authority）與 NV-1～NV-4；它們照原 routing。

## 7. 交 acceptor 的事項（資訊，不是 required authority）

列入 completion report；都不擋 #12 或 SPEC-UI0，也不需要 acceptor 在本 run 內動作：

1. **作業系統的原生檔案對話框中只用鍵盤多選 GPX：沒有任何人驗證過（NOT VERIFIED）。** #12 不以它為結案條件（第 4.2 節）。CL-UI0-4 末句：acceptor 在 UI Delta Review 實際檢視 UI0-6、UI0-7 時可以一併檢查。
2. **日曆彈窗在本環境中無法以鍵盤進入（K9）**，原因未確定；日期可只用鍵盤修改。是否要求正式整合的介面讓彈窗本身可用鍵盤操作，屬 DELTA 11.2「驗收清單定稿時確認」的事項，acceptor 可在 UI Delta Review 提出。
3. 若 acceptor 認為 P-11 的原意包含作業系統對話框或每個元件的每種互動，那是 acceptor 對 accepted 語義的說明，以 acceptor 為準；受影響的路徑是 #12 的結案與 SPEC-UI0 的 phase acceptance，屆時重新 route 至 Design Authority 評估影響（治理 §5.3）。本 record 依第 2.1 節的明文判斷這個可能性低，所以不 fail-closed。

## 8. 受影響的 work items 與 evidence

- **#12**：worklog 依第 6 節更新；之後 R2（Orchestrator 派工，pack 加入本 record）。沒有程式或測試的修改要求。
- **SPEC-UI0**：CL-UI0-4 依第 4.1 節第 4 點寫明其意思，版本與其他內容不變；SIA 與 phase acceptance 可引用本 record。UI0-7 的範圍依第 3.1、4.2 節。
- **之後的正式整合 Spec（`app/`）**：鍵盤驗收條件沿用第 3.1 節的操作單位與兩個條件；上傳的鍵盤驗收以第 4.2 節 (a)、(b) 界定頁面的範圍；是否加入逐元件要求由該 Spec 依 DELTA 11.2 處理。
- **Evidence**：本 record 只讀紀錄與原始碼；K9、K10、K3～K6 的現象沿用 Executor 在 worklog 的瀏覽器紀錄，本次沒有重做。Streamlit 前端的彈窗屬性是讀原始碼所得，不代表本環境的實際行為。

本 record 沒有讀取 `data/` 或 `.env`，沒有派工任何 subagent，沒有修改其他檔案，沒有 commit。
