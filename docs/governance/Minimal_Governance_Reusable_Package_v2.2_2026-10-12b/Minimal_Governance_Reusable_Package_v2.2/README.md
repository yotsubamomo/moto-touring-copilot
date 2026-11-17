# Minimal Governance — Reusable Package v2.2

**Package navigation（2026-10-12）。** 現行 reusable governance package 的入口：Minimal Operational Governance v2.2 ＋ Reference Model Profile default v2.5 ＋ Implementation Profile impl-default v2 ＋ Reference Orchestrator Contract orch-default v2.2。

> **Human approves the outcome contract once; authorized Agents autonomously design, decompose, implement, review, correct and complete within that boundary.**

**權威位置。** 原 master repository `D:\momo\17 - Model Governance\master_governance\` 自 2026-10-11 起不在起草環境的本機。Package v2.2 暫以本資料夾（`SpeCoda_Local_DEV_v2/master_governance/`）為權威來源；Notion 頁面是發布／導航副本，不一致時以本資料夾的檔案為準。原 repository 恢復可用時，以下表的 hash 比對後放回，並保留本資料夾的紀錄。

**與起草工作區的關係。** 本 package 在 SpeCoda_Local_DEV_v2 起草與審查，但它是通用母版：package 內的檔案不含任何專案的 Bindings、definitions、hooks、scripts 或實際 mapping。起草工作區本身另以 Project Bindings 採用本 package（見該工作區的 `governance/`），其專案配置不屬於 package。

## Package artifacts

| Artifact | Version · Status | 檔案（相對於本資料夾） | md5 | sha256 |
|---|---|---|---|---|
| **Minimal Operational Governance**（normative authority） | **v2.2** · Adopted／Frozen 2026-10-12 | `Minimal_Operational_Governance_v2.2_Candidate.md`（檔名沿用 Candidate 字樣，狀態以 header 為準） | `3a9d1db7f683c7dfed12df51099221ed` | `f84c02a96937e47e9cfa3399296682fb24de2da77522facc5e702b34f03f26d6` |
| Reference Model Profile | **default v2.5** · Adopted／Frozen 2026-10-11 | `references/model-profiles/default-v2.5.md` | `3bb566cbad663982f147367efc443e6f` | `59dfd808863221cccb90bebbd451506d6574bbee9b603df8f8a16289f5f60b27` |
| Reference Model Profile（v2.5 以引用方式沿用的 baseline） | default v2.4 · Adopted／Frozen 2026-10-02 | `references/model-profiles/default-v2.4.md` | `5bc265e535a6e3983851b675795375cc` | `c4c36ae0ff7a5f606286669d4920503faf4de815cc333b9247032fefca45ede4` |
| Implementation Profile | **impl-default v2** · Adopted／Frozen 2026-09-22 | `references/implementation-profiles/default-v2.md` | `825e8ae285823349fc69c9ada43cd58e` | `86ab7e969fef0ed911aa82950aaa7f248d8a1d0a539ca59d1bb9cca0cac4775a` |
| Reference Orchestrator Contract | **orch-default v2.2** · Adopted／Frozen 2026-10-12 | `references/orchestrator-contracts/default-v2.2.md` | `283ab0b347b943b5f06a9ec36b1b95af` | `47ff0236a0b773582c06a1f65305a8b0a72de428637ed2cc4fa0f71f1a633980` |
| Visualization（non-normative，詳細版） | v2.2 map · 2026-10-12b | `minimal_governance_map_v2.2_zh-TW_2026-10-12b.html` | `7824e4d2da1e2565e652856ef510dfa7` | `cebe364e344981ba6543b8b944e1e3b5e8616b6748063452f5e01385a59eb70a` |
| Visualization（non-normative，Visual-First 導覽版） | v2.2 visual map · 2026-10-12 | `minimal_governance_map_v2.2_visual_zh-TW_2026-10-12.html` | `95e4d9dfdaeb7c1af1af0bbe1e778f15` | `7c1819eb21f0ab0da5aefc541bcb7ec096072624569e633fb52f4fbe6748f4ef` |

**Frozen baselines（不構成現行版本的隱性 fallback authority）：**

| Artifact | 檔案 | md5 |
|---|---|---|
| Minimal Operational Governance v2.1（Adopted／Frozen 2026-10-01；2026-10-02 header metadata update） | `Minimal_Operational_Governance_v2.1_Candidate.md` | `d4d458eeb6d571f1f4f3f0cc607feac9` |
| Reference Orchestrator Contract orch-default v2.1 | `references/orchestrator-contracts/default-v2.1.md` | `1f5136b638c6a972a7e78c521ed9986b` |
| v2.2 visualization 快照（2026-10-12 初版；Minimal v2.2 header 的 visualization 句指向此檔） | `minimal_governance_map_v2.2_zh-TW_2026-10-12.html` | `a88fb3e1e99b5978f7fe120e1a07de27` |
| v2.1 visualization 快照 | `minimal_governance_map_v2.1_zh-TW_2026-10-02.html` | `6be4f7141e56903c31e664935a76c07e` |

v2.1 的四份檔案與 Notion 上的 v2.1 頁面、「Minimal Governance — Reusable Package v2.1」頁面都未修改。

## 架構關係

```text
Minimal Operational Governance v2.2（normative authority）
        │
        ▼
Project Bindings（§5.1：選用、pin、overrides、reserved boundaries）
        │
        ├── Reference Model Profile — default v2.5（role／bounded-assignment mapping、capability escalation、availability fallback；沿用 v2.4 部分章節）
        ├── Implementation Profile — impl-default v2（reusable implementation HOW）
        └── Reference Orchestrator Contract — orch-default v2.2（reusable control-plane HOW）
        │
        ▼
Project-specific Runtime / Skills / Harness
```

- **Minimal v2.2 是唯一的 normative authority。** 只有它定義 authority、roles、Outcome Contract 與 derived contracts、audit semantics、worklog 與 boundaries。
- **其他三份是從屬的 reusable references。** 只提供 mapping 與 HOW，不修改 Minimal 的 authority 或 normative semantics。
- **Project Bindings 決定專案實際採用與 overrides。**
- **Lightweight direct execution 不啟動 Orchestrator run**；orch-default 只在 Formal lane 啟動 run。

## v2.2 相對 v2.1 的差異

保留 v2.1 的全部條文與章節編號。新增與修改的段落在本文以〔v2.2 新增／修改 V22-nn〕標示；逐條帳、來源、新增規範用語的推導與刻意不納入的內容見 Minimal v2.2 Appendix D。

| 項目 | 內容 |
|---|---|
| §2.5（新） | Model 能力分層與選型原則；成本不得弱化 assurance；能力不代替 routing；capability escalation 的宣告與六項規則（含作 verdict 前退回的派工不計為 Alternate Review／Final Adjudication）；escalation 與可用性替代分開記錄；qualification-gated mapping；effort／mode 的變更 |
| §2.6（新） | Bounded assignments（worker、investigator、advisor）：沒有 authority；輸出是呼叫者待核對的輸入；決定不外包；不構成正式 review；Orchestrator 只用於控制面；範圍；紀錄 |
| §2.7（新） | Session 角色啟用與無角色 session：無角色 session 不取得 authority、其派工不構成 activation basis；受治理的工作以角色進行；明確進入角色；一次一個角色；離開角色；紀錄 |
| §2.2 | Binding 核對涵蓋 assignment 執行期間的全部工作（V22-10）；context independence 與 model diversity 分開陳述（V22-11）；mapping 加 escalation 宣告（V22-07） |
| 其他 | §1.1、§1.3、§2.1、§2.3、§3.7、§4.6、§5.1、§5.2、§5.4 的配套修改 |
| orch-default v2.2 | 由 v2.1 逐位元複製，只把 binding 核對延伸到全程，並設為採用 return 與作 routing、gate、persist、completion 依據前的 MUST gate（fail closed）；Bindings MUST 宣告可逐筆觀察的證據來源 |
| Model Profile | Package 的參考預設由 default v2.4 改為 default v2.5（Executor 預設 Sonnet 5.5，Fable 5.1 改為有界 escalation，新增三個 bounded assignments） |

## 採用方式

1. 專案 Bindings 依 Minimal v2.2 §5.1 記錄 governance adoption（v2.2）、Model Profile（`default` `v2.5`）、Implementation Profile（`impl-default` `v2`）、Orchestrator Contract（`orch-default` `v2.2`）與各自 overrides；無 override 記 `none`。
2. Bindings 列明：root role session 核對 model／effort 的方式與證據位置；可逐筆觀察實際 model 與 effort／mode 的證據來源（orch-default v2.2 §11）；採用的 capability escalation 與 qualification-gated resolution；bounded assignments 的 definitions（含允許的呼叫者）；符合 §2.3 四項 properties 的 independent dispatch 機制。
3. Model Profile v2.5 全部 identifier 有預設值，無 `TBD`；`primary_reviewer` 的 Codex 與 `mechanical` 的 Haiku 為 qualification-gated，未通過前依 Profile 的 resolution。Binding 仍須以專案自身證據驗證。
4. Reserved boundaries（opt-in）、lane policy、assurance policy、work records 位置由 Bindings 宣告（§5.1–§5.2）。
5. 新版本不自動適用任何專案。已採較早版本的專案依 Minimal §5.3 自行 re-pin，留下版本、依據與授權，並處理進行中 assignments、audit 與 evidence coverage。

## 版本沿革

| 日期 | 事件 |
|---|---|
| 2026-09-22 | Package v2：Minimal v2.0、Model Profile default v2、impl-default v2、orch-default v2 |
| 2026-09-23～09-29 | Model Profile default v2.1、v2.2、v2.3 |
| 2026-10-01 | Package v2.1：Minimal v2.1 ＋ orch-default v2.1 |
| 2026-10-02 | Model Profile default v2.4（Minimal v2.1 header metadata update 改指 v2.4） |
| 2026-10-11 | Model Profile default v2.5 Adopted／Frozen（於採用專案，原 repository 不可用） |
| 2026-10-12 | **Package v2.2**：Minimal v2.2 ＋ orch-default v2.2 Adopted／Frozen；package Profile 改為 default v2.5；impl-default v2 不變。依據：independent review A1（Codex R1 → correction → Codex R2 → correction → Alternate Review：CLOSED）與 operator 授權 |
| 2026-10-12 | Visualization 維護（non-normative，不改任何規範檔）：詳細版 map 2026-10-12b 補回初版精簡掉、但仍有效的內容（escalation trigger、availability fallback 共同規則與各列、Codex 規則、self-verification 清單、package 架構圖與 reference 內容卡）；另新增以圖為主的 Visual-First map，完整規則收在可展開區塊。兩份都依 Minimal v2.2、default v2.5（＋v2.4）、impl-default v2、orch-default v2.2 產生並對照核對；初版保留為快照。依據：Acceptor 2026-10-12 指示 |

**Profile ID `default` 的版本號。** 起草工作區另以 `default` v2.6、v2.7 作為本身的專案配置（Executor Opus 5.5、advisor 一律 `high`），它們不屬於本 package。Package 日後若修訂 `default`，版本自 v2.8 起，以免與該工作區的版本混淆。

## 紀錄

| 紀錄 | 位置 |
|---|---|
| Adoption and Freeze Record | [records/Minimal_Governance_v2.2_Adoption_and_Freeze_Record.md](records/Minimal_Governance_v2.2_Adoption_and_Freeze_Record.md) |
| Independent review A1（R1、R2、Alternate） | [records/reviews/](records/reviews/)（起草工作區 `governance/records/audits/` 中原檔的位元複本） |
| 變更帳與採用紀錄（文件內） | Minimal v2.2 Appendix D（D.8 審查與修正、D.9 採用）；orch-default v2.2 §15 |

## 已知未處理

- impl-default v2 的 header 仍標 Minimal v2.0，§11 引用 Profile default v2：凍結時的版本化陳述，與 v2.2 相容（A1 未發現衝突）；§11「核對 definition 與 assignment」可雙讀，留待 impl-default 下次修訂。
- default v2.5 的 header 仍標 Minimal v2.1，並註明「暫存於採用專案」：凍結時的版本化陳述；本 package 已以 `references/model-profiles/default-v2.5.md` 承載。
- orch-default v2.2 §2 對 Profile 版本（default v2.3）的引用沿用 v2.1 原文，是版本化陳述；採用專案的 Profile 以其 Bindings 為準。
- 本資料夾中各檔的相對連結指向原 master repository 的配置；原 repository 的歷史紀錄檔（例如 v2.0、v2.1 的 review records）不在本資料夾。
- `references/model-profiles/default-v2.5.md` 的 header 與 `records/reviews/` 的三份 review records 是位元複本，其中的相對連結指向起草工作區 SpeCoda_Local_DEV_v2 的紀錄（`governance/records/ADOPTION-2026-10-11.md`、`governance/records/outcome-contracts/WC-2026-10-12_minimal-governance-v2.2-adoption.md`、`governance/records/audits/DISPATCH-2026-10-12_minimal-governance-v2.2_A1-ALT.md` 等），在本資料夾中沒有對應檔。為保留 hash 不改寫這些複本；單獨搬移 package 時，以本 README 的 artifacts 表（hash）與 `records/Minimal_Governance_v2.2_Adoption_and_Freeze_Record.md` 追溯，原紀錄保存在該工作區（含其 NAS 備份）。
