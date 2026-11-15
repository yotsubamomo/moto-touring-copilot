# G3 UI/UX Audit Report

> **CR-01（2026-11-15）：** CR-01 重開了 Trip Planner 的輸入區與 [UI_CR01_DELTA.md](UI_CR01_DELTA.md) 列出的項目；其餘內容維持凍結。
> 日期：2026-11-15。對象：[prototype/index.html](../../prototype/index.html)（G2 原型）。
> 狀態：**G3 APPROVED / FROZEN（2026-11-15，專題負責人裁決）。** 裁決內容在第 7 節。原型與 UI 文件已凍結；之後的介面變更記入 DESIGN.md 的 Change Log。
> 範圍：審查與必要修正，不是重新設計。G1 決議與 Must 範圍沒有變更；沒有新增功能；沒有 Streamlit 實作。

## 1. 審查方式

### 1.1 使用 `ui-ux-pro-max` Skill 的方式

這一輪讀取了 Skill 的完整指引，走它的「Review existing UI」路徑：以 Quick Reference 的十類規則逐項檢查，再針對畫面上實際存在的問題做單一意圖的查詢。沒有重新產生 Design System。

| 規則類別（Skill 的優先順序） | 這次檢查的規則 |
| --- | --- |
| 1 Accessibility | `color-contrast`、`focus-states`、`keyboard-nav`、`form-labels`、`heading-hierarchy`、`color-not-only`、`icon-context`、`web-target-size`、`contextual-live-badge-updates` |
| 2 Touch & Interaction | `touch-target-size`、`loading-buttons`、`error-feedback`、`hover-vs-tap` |
| 4 Style Selection | `consistency`、`no-emoji-icons`、`primary-action`、`state-clarity` |
| 5 Layout & Responsive | `horizontal-scroll`、`content-priority`、`visual-hierarchy`、`compact-label-overflow`、`chip-collection-reflow`、`scroll-behavior` |
| 6 Typography & Color | `line-length`、`color-semantic`、`number-tabular`、`truncation-strategy` |
| 8 Forms & Feedback | `error-summary`、`focus-management`、`error-placement`、`required-indicators`、`error-clarity`、`submit-feedback`、`progressive-disclosure` |
| 10 Charts & Data | `data-density`、`data-table` |

第 3 類（Performance）、第 7 類（Animation）與第 9 類（Navigation）大多不適用：原型是單一檔案、沒有圖片與外部資源、只有一個 120 毫秒的顏色轉換、沒有多層導覽。

Skill 的查詢（`--domain ux`，每次一個意圖）：error summary validation、badge chip label wraps、live badge count screen reader、focus states keyboard navigation、touch target size、heading hierarchy、color not only status、loading feedback progress、table responsive mobile overflow、empty state guidance、disabled state clarity；另有 `--domain icons` 的 decorative icon aria hidden 與 `--domain product` 的 analytics dashboard decision support。

四個查詢（progressive disclosure、information density overload、visual hierarchy primary action、stale data refresh status）重試一次後仍然回傳不相關的結果。依 Skill 的規定，這幾項沒有採用查詢結果，改用 Quick Reference 的通用規則（`content-priority`、`progressive-disclosure`、`primary-action`、`data-density`）判斷。`--domain chart` 的查詢回傳的是熱力圖與樹狀圖，和這個介面無關，沒有採用。

### 1.2 實際開啟原型的檢查

- 以本機靜態伺服器開啟，在 1280×800 與 375×812 兩種視窗量測與截圖。
- 量測項目：各區塊的高度與位置、頁面與表格的橫向捲動、標籤是否換行、互動元件的尺寸。
- 鍵盤：以實際的按鍵操作走過表單（Tab）、規劃（Enter）、候選的選取（Space、方向鍵）；分頁的方向鍵以鍵盤事件驗證。
- 修改後以回歸腳本重跑十四個情境與驗收條件，兩種寬度各一次。腳本在 [prototype/g3-audit-check.js](../../prototype/g3-audit-check.js)，可以重複執行。

審查者是 Claude，也是原型的製作者。這仍然是自我審查。

## 2. 問題清單

優先度的定義：P1 會讓使用者得到錯誤或互相矛盾的資訊，或讓某種操作方式無法完成；P2 影響判斷速度或可讀性；P3 是次要的改善。

### 2.1 P1（全部已修正）

| 編號 | 問題 | 依據 | 修正 |
| --- | --- | --- | --- |
| P1-1 | 來源證據中有兩列模擬資料標成「真實 API」，而且用的是和 PASS 相同的綠色。說明只在表格下方的一行小字 | G1 Q31；`color-semantic` | 每一列的標籤都是「模擬」。正式產品預計標示的類型改成標籤旁的文字（例如「正式產品：真實 API」） |
| P1-2 | 頁面頂端的 Snapshot Mode 標籤跟著勾選框即時變動。規劃後切換勾選框，頂端的標籤和下方舊結果的資料模式、來源類型互相矛盾；兩個方向都會發生 | G1 第 9 節；`consistency` | 頂端的標籤改為描述畫面上的結果。勾選框的變更由過期提示說明 |
| P1-3 | 代表候選的名稱與「選法」說明和實際的選取條件不一致。其他候選還違反別的規則時，說明仍寫「所有候選都只違反規則 1」；名稱「最接近時間限制的候選」也可能不成立（另一個候選超過期限更少，只是多違反一條規則） | G1 Q27 | 只有在全部候選都只違反規則 1 時才使用「最接近時間限制的候選」；其他情形稱「代表性失敗候選」，說明照實描述選法。選取的邏輯沒有改變 |
| P1-4 | 375 像素時，表格內的狀態標籤逐字換行，「中降雨機率」變成五行直排，「模擬」變成兩行 | `compact-label-overflow`、`chip-collection-reflow` | 標籤不換行；只有頁面頂端的整句標籤可以換行。這個問題是 G2 修正頂端標籤時造成的 |
| P1-5 | 用鍵盤選取候選後，焦點掉到頁面本體，無法繼續用鍵盤操作表格 | `keyboard-nav`、`focus-management` | 重新繪製後把焦點放回選取的那一列 |

### 2.2 P2（低風險，已修正）

| 編號 | 問題 | 依據 | 修正 |
| --- | --- | --- | --- |
| P2-1 | 選取候選後，變動的逐條規則結果在表格上方，選取當下在畫面之外（量測：距離視窗頂端 −431 像素），看不到任何回饋 | `error-feedback`、`submit-feedback` | 選取的候選的規則結果顯示在表格下方、可展開區塊之內。上方固定顯示推薦的候選（無可行解時是代表候選） |
| P2-2 | 規劃完成後，進度區塊仍然完整展開，夾在按鈕與結果之間（375 像素時高 238 像素） | `content-priority` | 完成後收合成一行（52 像素） |
| P2-3 | 過期提示沒有說是哪個欄位變了 | `error-clarity` | 列出變更的欄位，並說明下方結果的資料模式與來源仍是上次的 |
| P2-4 | 必填的星號沒有說明；欄位錯誤時沒有 `aria-invalid` | `required-indicators`、`error-placement` | 表單上方加「* 必填欄位」；錯誤的欄位加上 `aria-invalid` |
| P2-5 | 「其他候選（共 N 個）」的數量其實包含推薦的候選；無可行解時，表格沒有標出哪一列是代表候選 | `consistency` | 標題改為「全部候選」；代表候選那一列加上標籤 |
| P2-6 | 保守估計的卡片寫「不是 P90」。騎士不需要知道這個術語，而且畫面上不應出現 P90 | DESIGN §6.1 | 改為「典型估計加上安全餘裕」 |
| P2-7 | 單選鈕與勾選框是 20 像素，小於 24 像素 | `web-target-size` | 改為 24 像素 |
| P2-8 | 1280 像素時內文一行約 66 個全形字 | `line-length` | 段落、清單與說明文字的寬度上限設為 46em（約 46 個全形字，和 Streamlit 置中版面的寬度相同） |
| P2-9 | 表格橫向捲動時，表格的說明文字跟著表格變寬，右半邊被切掉。這是修正 P1-4 時發現的 | `truncation-strategy` | 說明文字的寬度固定為可見區域的寬度 |

### 2.3 P2（沒有修改；裁決見第 7 節）

這幾項會動到 G1 的呈現方式，或無法確定 Streamlit 做得到，所以沒有修改。

| 編號 | 問題 | 量測 | 可行的做法 |
| --- | --- | --- | --- |
| N1 | Trip Result 偏長。決策需要的內容（狀態、待確認事項、四個數值）在最上方約 300 像素；其餘都是佐證 | 1280：2.1–2.3 個畫面；375：3.4–3.7 個畫面。「採用的條件」354 像素、「來源證據」約 300 像素，兩者約占四成 | 把「採用的條件」與「來源證據」放進預設收合的 `st.expander`。G1 要求來源證據以獨立區塊呈現，收合是否符合要由專題負責人判斷 |
| N2 | 375 像素時四張數值卡片直排，高 479 像素 | 超過半個畫面 | `st.columns` 在窄畫面也會直排，原型和 Streamlit 的行為一致。要改成兩欄需要先確認 Streamlit 1.67.0 的元件做得到 |
| N3 | 375 像素時 Trip Result 有三個表格、Validation & Replanning 有兩個表格需要橫向捲動；自訂分類與來源類型的欄位要捲動才看得到 | 來源證據表寬 712 像素，可見區域 309 像素 | `st.dataframe` 在手機上也是橫向捲動。可以考慮手機上減少欄位，留給 Spec |
| N4 | 「高降雨機率提醒」的標籤和 CONDITIONAL 一樣是琥珀色。它出現在前段或中段時計畫可能是 FEASIBLE | — | 改用灰色加警告圖示，或維持現狀 |
| N5 | 正式產品的「真實 API」標籤該用什麼顏色 | — | 建議用灰色或藍色，不用綠色；綠色保留給 PASS 與 FEASIBLE |
| N6 | 個人配速表與 Rider Profile 在正式產品中的來源類型。G1 只定了真實 API、資料快照與模擬三種 | 原型標示為「正式產品：待 Spec 定義」 | 留給 Spec |
| N7 | G1 Q27 第 2 點的「候選」指的是全部候選，還是 FAIL 數最少的那一組 | P1-3 採用較嚴格的解讀：全部候選 | 請確認。兩種解讀只影響名稱，不影響選到哪一個候選 |

### 2.4 P3（沒有修改）

| 問題 | 依據 |
| --- | --- |
| 結果區沒有自己的 h2 標題，分頁內的 h3 直接接在 Trip Planner 的 h2 之後 | `heading-hierarchy` |
| 分頁不支援 Home 與 End 鍵 | `keyboard-nav` |
| 375 像素時兩個分頁折成兩列（Streamlit 的分頁是橫向捲動） | `chip-collection-reflow` |
| 過期提示以隱藏屬性切換，螢幕閱讀器不一定會播報；規劃期間結果區沒有忙碌狀態的標示 | `contextual-live-badge-updates` |
| 沒有跳到主要內容的連結 | `skip-links` |
| 推薦的是最晚的可行出發時間，時間餘裕可能是 0 分，畫面上沒有另外說明 | `error-clarity`；排序方式是 G1 的決議 |
| 待確認事項排在數值卡片之前，CONDITIONAL 時數值卡片從 192 像素（1280）或 304 像素（375）開始 | `content-priority`；位置是 G1 Q24 的決議，不修改 |
| 沒有深色模式 | `dark-mode-pairing`；由 Streamlit 的主題決定 |

## 3. 修改前後的比較

### 3.1 行為

| 項目 | 修改前 | 修改後 |
| --- | --- | --- |
| 來源類型的標籤 | 模擬、模擬、模擬、真實 API、真實 API、模擬 | 每一列都是「模擬」，旁邊註明正式產品的類型 |
| 一般模式規劃後勾選 Snapshot Mode | 頂端出現 Snapshot Mode 標籤；下方仍是一般模式的結果 | 頂端沒有 Snapshot Mode 標籤；過期提示寫「上次規劃後變更了：Snapshot Mode」 |
| Snapshot Mode 規劃後取消勾選 | 頂端的標籤消失；下方仍是資料快照的結果 | 頂端維持「目前顯示的結果使用固定的資料快照」；出現過期提示 |
| 候選 16:40 只違反規則 1，16:55 與 17:10 還違反規則 3 | 最接近時間限制的候選；選法寫「所有候選都只違反規則 1」 | 代表性失敗候選；選法寫明其他候選還違反別的規則 |
| 候選 17:10 只違反規則 1，16:40 與 16:55 還違反規則 3（超過期限較少） | 最接近時間限制的候選（17:10） | 代表性失敗候選（17:10） |
| 用鍵盤選取候選 | 焦點掉到頁面本體 | 焦點留在選取的那一列，可以繼續用方向鍵 |
| 選取候選後的回饋 | 表格上方的內容變動，在畫面之外 | 表格下方出現「選取的候選」與它的四條規則結果 |
| 375 像素的表格標籤 | 逐字換行 | 單行 |

### 3.2 量測

高度的單位是像素。畫面數是高度除以視窗高度。

| 項目 | 1280×800 修改前 | 修改後 | 375×812 修改前 | 修改後 |
| --- | --- | --- | --- | --- |
| Trip Result，FEASIBLE | 1616 | 1679 | 3181 | 2733 |
| Trip Result，CONDITIONAL | 1712 | 1774 | 3233 | 2881 |
| Trip Result，搜尋未完成 | 1779 | 1842 | 3352 | 3000 |
| Trip Result，INFEASIBLE | 964 | 1001 | 1660 | 1442 |
| Validation & Replanning，CONDITIONAL | 1083 | 1083 | 1383 | 1384 |
| Validation & Replanning，INFEASIBLE | 1775 | 1775 | 2296 | 2297 |
| 規劃完成後的進度區塊 | 沒有單獨量測 | 52 | 238 | 52 |
| 分頁列距離頁面頂端（規劃後） | 1174 | 1072–1094 | 1787 | 1614–1659 |

- 手機上 Trip Result 短了 10%–14%，原因是表格內的標籤不再直排。
- **桌面上 Trip Result 長了約 60 像素（約 4%）。** 原因是內文的行寬上限讓說明文字變成兩行，以及來源類型欄位變寬後有一列換行。這是可讀性與長度之間的取捨；決策區（最上方約 300 像素）沒有變動。
- Validation & Replanning 的長度沒有變動。選取候選後，可展開區塊內會多出那個候選的規則結果。

## 4. 修改後的驗證

回歸腳本在 1280 與 375 兩種寬度各跑一次，檢查對象是最後一版檔案：

| 檢查 | 結果 |
| --- | --- |
| 十四個情境的計畫狀態與搜尋狀態標籤 | 全部符合 |
| 每個情境、兩個分頁：頁面沒有橫向捲動、標籤沒有換行、沒有過大的圖示、沒有小於 24 像素的互動元件 | 全部通過 |
| 每個情境：規劃期間按鈕停用、步驟文字沒有百分比、完成後進度收合 | 全部通過 |
| 每個情境：來源證據沒有「真實 API」的標籤、畫面上沒有 P90、結果區沒有輸入對話的元件 | 全部通過 |
| 情境專屬的條件（待確認事項、UNKNOWN 四項、搜尋未完成、固定模板、輸出驗證錯誤、重新規劃、降雨、暮光、追問、衝突、兩種無可行解） | 全部通過 |
| 代表候選：兩個情境，加上兩個混合違規的案例 | 全部通過 |
| Snapshot Mode：一般模式規劃、切換、重新規劃、再切換四個步驟 | 全部通過 |
| 結果過期：列出變更的欄位、保留舊結果、改回原值後提示消失 | 全部通過 |
| 欄位錯誤三種：摘要取得焦點、欄位旁的錯誤、`aria-invalid`、摘要連結把焦點移到欄位 | 全部通過 |
| 分頁的方向鍵 | 通過 |
| 沒有外部網址、沒有表情符號；主控台沒有錯誤 | 通過 |

腳本回報 0 項失敗。另外以實際按鍵確認：表單的 Tab 順序和畫面順序一致、走過的每個元件都有 3 像素的焦點框、按 Enter 可以規劃、規劃後焦點移到結果、Space 與方向鍵可以選取候選而且焦點不會遺失。

### 4.1 更正 G2 的驗證紀錄

G2 最後一次重跑時，檢查腳本切換分頁用了錯誤的識別碼，兩個分頁都被隱藏，因此有兩項結果無效：

- **F3（兩個分頁都沒有橫向捲動）**：當時實際上沒有檢查到分頁的內容。這一輪已經正確地重新驗證。
- **C5（畫面上不出現 P90）**：當時回報「整頁找不到 P90」是錯的；保守估計的卡片寫著「不是 P90」。這一輪已移除並重新驗證（P2-6）。

另外，D5（選取候選）在 G2 是以腳本點擊驗證的，沒有發現鍵盤焦點遺失的問題（P1-5）。

## 5. 剩餘的風險與沒有驗證的項目

- **仍然是自我審查。** 螢幕閱讀器、其他瀏覽器、實體手機的觸控、橫向畫面、文字放大到 200%、減少動態的系統設定，都沒有測試。
- **視覺審查有限。** 截圖是在預覽窗格內以 0.6–0.7 倍檢視的，沒有人在正常尺寸的螢幕上看過。
- **Streamlit 的呈現沒有驗證。** 修改都對應到標準元件（見下表），但沒有實際建出頁面。
- **手機上的資訊量仍然偏多。** Trip Result 在 375 像素時還有 3.4–3.7 個畫面（N1、N2、N3）。
- **UI 的工作量風險（R19）沒有變小。** 這一輪沒有增加區塊，但也沒有減少。

修改和 Streamlit 1.67.0 的對應：

| 修改 | Streamlit 的做法 |
| --- | --- |
| 來源類型的文字 | `st.dataframe` 或 `st.table` 的文字欄位 |
| 頂端的資料模式標籤描述畫面上的結果 | 從 session state 中保存的結果讀取，以 `st.badge` 顯示 |
| 過期提示列出變更的欄位 | 比對 session state 中的輸入，以 `st.warning` 顯示 |
| 進度完成後收合 | `st.status` 完成後收合 |
| 選取的候選的規則結果在表格下方 | `st.expander` 內放 `st.dataframe` 與 `st.container(border=True)`，沒有巢狀的可展開區塊 |
| 必填的說明 | `st.caption` |
| 內文的行寬 | Streamlit 置中版面的預設寬度 |
| 鍵盤焦點的處理、標籤不換行、表格說明的寬度 | 只和原型有關，Streamlit 的元件自行處理 |

## 6. 需要專題負責人確認的事項（已裁決，見第 7 節）

1. **N7**：G1 Q27 第 2 點的解讀。目前採用「全部候選都只違反規則 1 才稱為最接近時間限制的候選」。
2. **N1**：Trip Result 的「採用的條件」與「來源證據」要不要預設收合。
3. **P2-1**：選取的候選的規則結果改到表格下方、上方固定顯示推薦的候選。這改變了 G2 文件描述的行為，沒有改變 G1 Q26。
4. **P2-5**：可展開區塊的標題由「其他候選」改為「全部候選」。
5. **N4、N5**：高降雨機率提醒與「真實 API」標籤的顏色。
6. **N6**：個人配速表與 Rider Profile 的來源類型，留給 Spec 是否可以。
7. **N2、N3**：手機上的數值卡片與表格是否接受現狀。
8. [prototype/g3-audit-check.js](../../prototype/g3-audit-check.js) 是這一輪新增的檢查腳本，不是產品的一部分。要不要保留在 repo 裡。
9. G3 的結論：通過並凍結，或列出要修改的項目。

## 7. G3 裁決（2026-11-15）

**G3 最終裁決：APPROVED / FROZEN。** 5 項 P1 已修正，G3 回歸測試通過。裁決由專題負責人作出。

| 項目 | 裁決 | 後續 |
| --- | --- | --- |
| N1 | 「採用的條件」與「來源證據」維持展開。不再調整原型 | 無 |
| N2 | 接受手機上四張數值卡片直排 | 無 |
| N3 | 接受手機上表格在容器內橫向捲動 | 精簡欄位可以留給 Spec |
| N4 | 保留高降雨機率提醒的琥珀色與文字警示 | 無 |
| N5 | 正式產品的 API 來源標籤使用中性的灰色，不用綠色 | 正式介面實作時處理 |
| N6 | 本地衍生資料與本地設定檔的來源類型交給 Spec 定義，不能誤標為 API | Spec |
| N7 | 接受目前的嚴格命名規則：全部候選都只違反規則 1 才稱為「最接近時間限制的候選」 | 寫入 Spec |
| P2-1 | 接受：選取的候選的規則結果顯示在表格下方，上方固定顯示推薦的候選 | 無 |
| P2-5 | 接受：可展開區塊的標題是「全部候選」 | 無 |
| `prototype/g3-audit-check.js` | 保留，作為測試資產 | 無 |

凍結之後：

- 不再開啟 UI/UX 的重新設計。
- 已接受的 P2 與 P3 不再修改。
- 接著進入 Spec 階段。Spec 以凍結的 DESIGN.md、G1 決議與這裡的 UI 文件為輸入。
