# Derivation record — SPEC-UI0：UI-0 Mock-data Skeleton

| 欄位 | 內容 |
| --- | --- |
| Record ID | `derivation-spec-ui0`（v1，2026-11-17） |
| Spec | **SPEC-UI0 v1**＝第 2 節列出的既有段落（commit `873e37a` 的內容）＋本 record 第 4 節的 DA clarifications |
| 決定者 | Design Authority（`gov-design-authority`；binding 由派工者核對） |
| Outcome Contract | OC-1，acceptor 2026-11-17 針對 commit `873e37ae98d701c076b1bc533c7993ca62c2dd6c` 接受 |
| 跨 Spec 的決定 | [`decision-20261117-oc1-first-run-derivation.md`](decision-20261117-oc1-first-run-derivation.md) |
| Lane | Formal；只有一張 Ticket，採單 Ticket fast path（Bindings 第 5 節） |
| Ticket | #12（UI-0），原樣引用（雜湊見 decision record BD-3） |

## 1. 依據的 Outcome Contract 條款

- OC-1 §2.1 第 4 項：UI-0 Mock-data Skeleton 與之後的正式整合；UI Delta Review 由 acceptor 進行。
- OC-1 §2.2：不修改 G3 Frozen Baseline（`prototype/index.html` 與 `docs/ui/` 中標示 G3 Frozen 的文件）；UI 差異只寫在 `docs/ui/UI_CR01_DELTA.md`。
- OC-1 §3.1：AB-8、AB-10、AB-13 的部分。
- OC-1 §4.2：UI Delta Review 保留給 acceptor。

## 2. Spec 的內容（引用）

| 來源（commit `873e37a`） | 引用的段落 |
| --- | --- |
| GitHub Issue #12 | 全文（自足的介面行為、固定文字、14 個合成情境、元件對應、UI0-1～UI0-10、排除範圍） |
| `DESIGN.md` §9.6 | CR-01 的 UI Gate；設計要求（模擬標示、狀態標籤、保守估計與降雨用語） |
| `docs/ui/UI_CR01_DELTA.md` | 第 11 節（介面驗收條件）、第 12 節（元件對應） |
| `docs/cr/CR-01-appendix/ui0_decision_table.md` | 22 項的裁決（U-1～U-22） |
| G3 凍結的 `docs/ui/UI_DESIGN.md`、`UI_FLOW.md`、`UI_ACCEPTANCE.md` | 沒有變更的部分照凍結的設計（只讀） |

固定文字以 Issue #12 為準（UI0-3）。Issue 中部分文字在 SPEC-001 5.5 標為「提案」；它們在 UI-0 中是供 acceptor 檢視的模擬畫面文字，是否採用由 UI Delta Review 決定，不因 UI-0 結案而成為定案的產品文字。

## 3. Boundary determination

**在 OC-1 boundary 內。** 依據：OC-1 §2.1 第 4 項明列；#12 是 acceptor 2026-11-15 依 CR-01 UI Gate 的裁決建立的 Ticket；UI-0 需要的 SB-6、SB-10 部分已由 UI-0 對照表確認（SB-6、SB-10 的說明欄），Skeleton 不碰 SB-6 的確切樣式與 SB-10 的剩餘範圍（decision record BD-2）；只用模擬資料，不呼叫任何 API，不讀 `data/`。

## 4. DA clarifications（SPEC-UI0 的一部分）

**CL-UI0-1 位置與依賴。** 程式放在 `app/`（DESIGN §9.1）。只依賴 Streamlit 1.67.0 與標準函式庫；不匯入 `src/moto_copilot/` 的任何模組（DESIGN §9.2：UI Prototype 使用 Mock Data，不依賴 `src/`）。Streamlit 依賴的加入方式由 Executor 決定，不新增其他 framework。

**CL-UI0-2 檔案上傳。** `st.file_uploader` 收到的內容不解析、不寫入磁碟、不顯示檔名以外的任何內容，也不記錄到 log；按「更新 Profile」後只顯示合成的處理結果。測試與檢視只用合成或空的 `.gpx` 檔，不使用騎士的檔案。

**CL-UI0-3 UI0-10 的紀錄位置。** UI0-10 的簡短紀錄寫在該 Ticket 的 worklog（`docs/governance/records/worklog/issue-12.md`）。本 Ticket 不修改 `docs/ui/` 的任何檔案（含 `UI_CR01_DELTA.md`）與 `prototype/`；和 `UI_CR01_DELTA.md` 不一致的地方只記錄，由 UI Delta Review 之後的工作處理。

**CL-UI0-4 UI0-6、UI0-7 的證據。** 375 像素寬度與鍵盤操作要有實際在瀏覽器中檢查的紀錄（截圖的路徑或逐步的操作紀錄，畫面只含合成資料）。執行環境無法啟動瀏覽器或 Streamlit 時，該 AC 記為 BLOCKED 並寫明缺少的能力，不記為 PASS，也不以推測代替（治理 §1.5 第 4 項）；這兩項之後仍由 acceptor 在 UI Delta Review 實際檢視。

**CL-UI0-5 UI0-8 的範圍。** 「整合後驗收」的條目只列出、不實作；Skeleton 不得以模擬的判定邏輯冒充 Validator（不寫計算規則結果或計畫狀態的程式，狀態一律寫在情境資料中）。

## 5. Ticket

| Ticket | 範圍與 AC | 補充 | 依賴 | AB | 高風險類別 |
| --- | --- | --- | --- | --- | --- |
| **#12 UI-0** Streamlit Mock-data Skeleton | Issue #12 的範圍、六個畫面區塊、14 個情境與 UI0-1～UI0-10 | CL-UI0-1～CL-UI0-5 | 無 | AB-8、AB-10、AB-13 的部分 | **H-2**（Streamlit 的 GPX 上傳元件：檔案內容的保存與顯示，判定 3.2 第 5 項；畫面不得出現真實資料，判定 3.2 第 4 項）、**H-3**（介面文字中的受約束宣稱：保守估計、降雨機率門檻、隱私說明、國道檢查、模擬標示，判定 3.3 第 4 項；UI0-10 紀錄中的結果陳述，判定 3.3 第 3 項）。不涉及 H-1（沒有憑證與設定值的顯示）；不涉及 H-4（狀態寫在情境資料中，沒有判定邏輯，CL-UI0-5；若實作中出現判定邏輯，Executor route 至 Design Authority） |

充分證據要求：
- E-1：`.venv/Scripts/python.exe -m pytest -q` 全數通過（本 Ticket 若新增測試，一併列出）。
- E-2：Streamlit 實際啟動的紀錄；14 個情境逐一操作的紀錄（截圖路徑或操作紀錄）。
- E-3：UI0-1～UI0-10 逐條的結果，記在 worklog（CL-UI0-3）；做不到的元件逐項列出替代做法（UI0-2）。
- E-4：固定文字和 Issue #12 逐字比對的方法與結果（UI0-3）。
- E-5：畫面、截圖與 diff 中沒有真實的行程資料、座標、騎乘日期時間或私有路線名稱（UI0-9）。
- E-6：H-2、H-3 依 `decision-20261117-high-risk-categories.md` 第 5 節的核對範圍作 self-verification 並記錄。

## 6. Spec 層級的驗收與單 Ticket fast path

- 本 Spec 只有 #12，#12 的 R1 兼作 Spec Integration Audit。依 Bindings 第 5 節，**派工 R1 時就要指定它兼作 Spec Integration Audit**，record 逐項記載治理 §4.7 的五個範圍並明寫「本 record 同時是 Spec Integration Audit」；不得事後重新標示。
- Spec 層級的 AC：#12 依 orch-default §7 結案；UI0-1～UI0-10 有證據；本 Spec 分配到的 AB 部分（第 7 節）有對應的證據；沒有修改 G3 Frozen Baseline 與 `docs/ui/`。
- 本 Spec 不是 OC-1 最後一份未結的 Spec，所以 SIA 不需要核對全部 derived Specs 的分配涵蓋。

## 7. 分配到的 Outcome Contract acceptance boundary 部分

| AB | 本 Spec 分配到的部分 |
| --- | --- |
| AB-8 | UI-0 Skeleton 的實作與供 UI Delta Review 使用的紀錄。不含 UI Delta Review 本身（acceptor 的決定與紀錄是 AB-8 的另一項證據）與之後的正式整合 |
| AB-10 | NFR5：每個情境標示為模擬；隱私說明採 U-7 裁決後的文字 |
| AB-13 | 本 Spec 的 pytest、Spec Integration Audit（fast path）closure、Design Authority phase acceptance |

## 8. 受影響的工作

- 新增 `app/`（目前不存在）與 Streamlit 依賴。
- UI Delta Review 之後的正式整合 Tickets 會以本 Skeleton 為起點；本 Skeleton 中的模擬資料與情境選單不得帶進正式整合的產品路徑（之後的 `app/` Spec 決定）。

## 9. Implementation readiness

**Implementation-ready。** Issue #12 是自足的規格（畫面、文字、情境、元件與驗收條件）；第 4 節固定了位置、上傳內容的處理、紀錄位置與證據的取得方式。沒有依賴未關閉的 Spec Blocker 的剩餘範圍。
