# Minimal Governance v2.2 — Adoption and Freeze Record

**Record type：** Reusable Package v2.2 的採用與凍結紀錄（Minimal Operational Governance v2.2 §5.3；Appendix D.9）。  
**Operator（acceptor）：** Momo Dai。下列決定屬 operator；本紀錄由起草工作區 work item `WL-2026-10-12_minimal-governance-v2.2-adoption` 的 Executor 依 operator 的明確指示寫入，只轉錄決定，不以 operator 的名義增加內容。  
**Effective：** 2026-10-12。

## 1. Operator 的決定

2026-10-12 指示「Minimal Governance v2.2 Full Adoption & Workspace Migration」（原文保存於起草工作區 `governance/records/outcome-contracts/WC-2026-10-12_minimal-governance-v2.2-adoption.md`，UTF-8、LF、不含結尾換行的 SHA-256 `44a6d567c3a2b67353800010f3e135eb152c81bbba32fd5843e1d3fa700e4d74`）。與本 package 有關的要點：

1. 確認採用完整的 v2.2 變更方向，包含 §2.5、§2.6、§2.7 及所有其他 v2.2 新增或修訂的內容。
2. 由 Codex 擔任 independent reviewer；有 blocking finding 時依既有治理完成修正、R2、Alternate Review／Final Adjudication。
3. Review closure 後，正式採用並凍結 Minimal Governance v2.2 母版。
4. 將 Model Profile default v2.5 納入 Reusable Package v2.2，作為跨專案參考預設；起草工作區的 default v2.6／v2.7 不升格為跨專案預設。
5. 檢查 impl-default v2、orch-default v2.1 的相容性，發現實質衝突時執行最小必要修正。
6. Package 含 Minimal v2.2、default v2.5、相容的 Implementation Profile 與 Orchestrator Contract、adoption instructions／navigation、adoption records／version provenance、新版 non-normative visualization；保留 v2.1 母版及其歷史紀錄；以起草工作區的 `master_governance/` 為目前的權威位置，記錄原 repository 暫時不可用；Notion 為發布／導航副本，建立新的 v2.2 頁面，不覆寫 v2.1。

## 2. Independent review（audit A1）

| Stage | 結果 | Record（`reviews/`） |
|---|---|---|
| R1：Codex（`gpt-6-sol`／`xhigh`） | needs-attention；三項 blocking：F1（V22-10 的全程核對在 companion 與採用專案 Bindings 中沒有對應程序）、F2（Candidate 起草 assignment 的 binding 不符且未修復）、F3（§2.5 escalation 與 exactly one Alternate Review 的計數未定義） | `AR-2026-10-12_minimal-governance-v2.2_A1-R1.md` |
| Targeted correction | F3：§2.5 規則 3 補計數規則；F1：orch-default v2.2；F2：合格的 Executor（Opus 5.5／`high`）依起草 contract 重新核對全文並承接 | Minimal v2.2 Appendix D.8 |
| R2：Codex | F2、F3 RESOLVED；F1 剩餘（A1R2-F1：orch-default v2.2 的核對只是 SHOULD，不構成 gate） | `AR-2026-10-12_minimal-governance-v2.2_A1-R2.md` |
| Correction | orch-default v2.2 §3 改為 MUST gate、fail closed；§11 MUST 宣告逐筆證據來源 | Minimal v2.2 Appendix D.8 |
| Alternate Independent Review：Opus 5.5／`xhigh` | **CLOSED**：A1R2-F1 RESOLVED；無未解 blocking；不需 Final Adjudication。三項 non-blocking（採用專案 Bindings 的對應、package references 須指向 orch-default v2.2、orch-default §11 時點摘要對齊）由採用與遷移處理 | `AR-2026-10-12_minimal-governance-v2.2_A1-ALT.md` |

Closure subject：Minimal v2.2 Candidate sha256 `01a9542a6d254b3a3469429144503d8167385e650c0d799dd03c858ae84078b9`（§1–§5 body md5 `5a407bebc0a50299b08371418d854c81`）；orch-default v2.2 sha256 `91f509179a2004a09eee9a8fd9f8630cbc98d77782abb081088757b1571d8c4d`。

## 3. Adoption edits（closure 之後的 delta）

| 檔案 | 修改 | 依據 |
|---|---|---|
| Minimal v2.2 | 標題、狀態、版本、日期、效力段（含 visualization 檔名）、標示段一句、package references 段、Appendix A.1 v2.2 列、D.7 狀態列、新增 D.9。**§1–§5 body 與 closure subject 逐位元相同**（md5 `5a407bebc0a50299b08371418d854c81`） | Metadata／record；A1ALT-F2（package references 改指 orch-default v2.2） |
| orch-default v2.2 | header Status；§11 括號內的時點列舉與 §3 對齊（義務不變）；§15 adoption 列與其後一句 | Metadata／record；A1ALT-F3 |

## 4. 採用的檔案（hash）

| 檔案 | 狀態 | md5 | sha256 |
|---|---|---|---|
| `Minimal_Operational_Governance_v2.2_Candidate.md` | Minimal v2.2，Adopted／Frozen | `3a9d1db7f683c7dfed12df51099221ed` | `f84c02a96937e47e9cfa3399296682fb24de2da77522facc5e702b34f03f26d6` |
| `references/orchestrator-contracts/default-v2.2.md` | orch-default v2.2，Adopted／Frozen | `283ab0b347b943b5f06a9ec36b1b95af` | `47ff0236a0b773582c06a1f65305a8b0a72de428637ed2cc4fa0f71f1a633980` |
| `references/model-profiles/default-v2.5.md` | default v2.5（2026-10-11 Adopted／Frozen；本 package 起作為參考預設），未修改 | `3bb566cbad663982f147367efc443e6f` | `59dfd808863221cccb90bebbd451506d6574bbee9b603df8f8a16289f5f60b27` |
| `references/model-profiles/default-v2.4.md` | default v2.4，未修改 | `5bc265e535a6e3983851b675795375cc` | `c4c36ae0ff7a5f606286669d4920503faf4de815cc333b9247032fefca45ede4` |
| `references/implementation-profiles/default-v2.md` | impl-default v2，未修改 | `825e8ae285823349fc69c9ada43cd58e` | `86ab7e969fef0ed911aa82950aaa7f248d8a1d0a539ca59d1bb9cca0cac4775a` |
| `minimal_governance_map_v2.2_zh-TW_2026-10-12.html` | v2.2 visualization（non-normative） | `a88fb3e1e99b5978f7fe120e1a07de27` | `93993d8084303a7fd588c5b4bcafc6b8e732733475054731b9dc2f71bdd57ea6` |

Frozen baselines（未修改）：Minimal v2.1 md5 `d4d458eeb6d571f1f4f3f0cc607feac9`；orch-default v2.1 md5 `1f5136b638c6a972a7e78c521ed9986b`；v2.1 map md5 `6be4f7141e56903c31e664935a76c07e`。

## 5. Provenance

- **基線來源。** Minimal v2.1、default v2.4、impl-default v2、orch-default v2.1 是原 master repository 檔案的位元複本（md5 與 Notion「Minimal Governance — Reusable Package v2.1」頁公布的值相同）；default v2.5 是 2026-10-11 在採用專案凍結的檔案。
- **權威位置。** 原 repository `D:\momo\17 - Model Governance\master_governance\` 自 2026-10-11 起不在起草環境的本機；本 package 暫以起草工作區的 `master_governance/` 為權威位置。原 repository 恢復時，以上表 hash 比對後放回。
- **Profile ID `default` 的版本號。** 起草工作區以 `default` v2.6、v2.7 作為本身的專案配置，不屬於本 package；package 日後若修訂 `default`，版本自 v2.8 起。
- **Package 的後續 audit。** 起草工作區的遷移（含本 package 的組裝與本紀錄）另受該工作區的 H-1 independent audit（A2）審查；結果記在該工作區的 worklog 與 `governance/records/audits/`。

## 6. 採用效果

依 Minimal v2.2 §5.3：新版本不自動適用任何專案；已採用 v2.1 或更早版本的專案須明確 re-pin，並處理進行中 assignments、audit 與 evidence coverage。Minimal v2.2 與 orch-default v2.2 自本日起 frozen；之後任何變更依 §5.3 留下版本、依據與授權，以新版本承載。
