<div align="center">

# 🧠 Amazing PsyCoder 💻

> 讓心理學研究者更專注於研究問題，而不是程式碼。

[![Version](https://img.shields.io/badge/version-v1.4.0-2563eb.svg)](../amazing-psycoder/SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](../LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-green)](https://github.com/openai/codex)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-red)](https://github.com/openclaw/openclaw)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-333)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/soupandpsy/amazing-psycoder-skills?style=social)](https://github.com/soupandpsy/amazing-psycoder-skills)

[**简体中文**](../README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 為什麼](#-為什麼做這個專案) · [👥 適合誰](#-適合這些人) · [⚡ 安裝](#-安裝) · [🚀 快速開始](#-快速開始) · [🧪 實驗編程](#-實驗編程) · [📊 資料分析](#-資料分析) · [🎬 Demo](#-demo) · [📂 檔案結構](#-檔案結構)

</div>

<br>

## 📖 為什麼做這個專案

<h3 align="center">🔍 心理學研究從設計到分析的常見困難</h3>

🔬 研究想法要轉化為可用於收集資料的實驗程式，研究者往往還需要掌握 Python、JavaScript 或 MATLAB。<br>
📦 實驗室已有程式碼可能因執行環境改變而無法使用，依賴關係與核心邏輯也常常難以維護。<br>
📊 如果統計方法主要依照慣例選擇，研究者可能難以說明方法與研究問題、變項類型和資料結構之間的關係。<br>
🔁 如果沒有記錄軟體版本和依賴環境，分析結果可能難以在其他電腦上重現。<br>
✂️ 如果實驗設計與分析計畫彼此脫節，可能在資料收集後才發現現有設計無法支援原定分析。

<h3 align="center">🧱 研究進行中的兩類主要困難</h3>

**第一類：實驗編程。** 為了檢驗假設，需要把實驗設計轉化為程式。PsychoPy Builder 在部分複雜設計中可能不夠靈活，使用 Coder 需要 Python；jsPsych 需要 JavaScript 和時間線邏輯；Psychtoolbox 需要 MATLAB 和顯示同步知識。反應時間從哪個畫面開始計算、按鍵如何映射、程式中斷後如何保留資料，都需要明確設計並逐項檢查。

**第二類：資料分析。** 分析計畫最好在資料收集前開始規劃，並在取得資料後依照實際結構落實。被試內設計應使用配對 t 檢定還是混合模型？正確率接近上限時應如何建模？為什麼選擇這個方法？換一台電腦後能否重現相同結果？這些問題需要結合研究目標、資料層級和軟體環境回答。

這些困難不只涉及編程，也涉及實驗設計、統計推論、資料管理和研究重現。

<h3 align="center">✨ Amazing PsyCoder 如何提供協助</h3>

你可以先描述實驗想法、已有設計或現有資料。Amazing PsyCoder 會逐步協助你確認研究規則、生成程式碼並檢查問題；在需要時，你仍須提供設定、資料說明、排除依據和執行記錄。系統不會只憑 AI 輸出就宣稱「可以收資料」或「可以發表」：實驗仍須在正式電腦試跑，分析也必須真正執行並檢查結果。

Amazing PsyCoder 由 7 個 Skill 組成——1 個總入口加 6 個專業 Skill。它遵循 [agentskills.io](https://agentskills.io) 開放標準，可安裝到 Claude Code、Codex、Hermes 和 OpenClaw 這四個 AI Agent 中。

**把時間還給研究本身。**

---

## 👥 適合這些人

- 🎓 正在或準備寫實驗程式碼的心理學大學生、研究生
- 🧠 做認知、行為、社會心理實驗的研究者
- 😵‍💫 經常遇到 RT、隨機化或條件表問題，希望系統化檢查常見風險
- 📊 收完資料不確定該用什麼統計方法，希望有系統化分析方案
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB 使用者

---

## ⚡ 安裝

建議使用倉庫內的安裝腳本。它會先檢查 7 個 Skill；中途失敗時會還原舊檔案。

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
```

**Claude Code**

```bash
./install.sh claude
```

安裝後使用 `/amazing-psycoder`。預設位置：`${CLAUDE_CONFIG_DIR:-~/.claude}/skills`。

**Codex**

```bash
./install.sh codex
```

安裝後使用 `$amazing-psycoder`。預設位置：`~/.agents/skills`。

**Hermes**

```bash
./install.sh hermes
```

安裝後使用 `/amazing-psycoder`。預設位置：`~/.hermes/skills`。

**OpenClaw**

```bash
./install.sh openclaw
```

安裝後直接描述任務，由 OpenClaw Agent 匹配 Skill。預設位置：`~/.openclaw/skills`。

<details>
<summary><b>專案級安裝與安裝檢查</b></summary>

<br>

```bash
./install.sh --scope project --project-dir /path/to/repo claude
./install.sh --scope project --project-dir /path/to/repo codex
./install.sh --scope project --project-dir /path/to/workspace openclaw
./install.sh --check codex
```

Hermes 目前沒有穩定的專案級 Skill 目錄，因此只提供使用者級安裝。詳見 [`PLATFORMS.md`](../amazing-psycoder/PLATFORMS.md)。

</details>

---

## 🚀 快速開始

安裝後，在對應的 AI Agent 中呼叫 Amazing PsyCoder，並直接描述你想做什麼：

> 「我要做一個 Stroop 任務，紅綠藍三色，按鍵反應」→ 自動進入實驗設計

> 「幫我分析 Stroop 資料，一致和不一致 RT 有沒有差異」→ 自動進入分析設計

> 「幫我檢查這份實驗程式碼，特別看 RT 起點和資料儲存」→ 自動進入程式碼檢查

通常不需要指定使用哪個專業 Skill。總入口會依照任務內容選擇設計、程式碼生成或檢查；如果無法判斷你要設計實驗還是分析資料，它會先向你確認。

---

## 🧪 實驗編程

從想法到可以開始試跑的實驗程式碼，分三步——設計、生成、檢查。

### 技能

| # | 技能 | 做什麼 | 關鍵細節 |
|---|------|--------|---------|
| ① | **設計編排** `psy-exp-designer` | 把實驗想法變成完整設計規範 | 5 階段漸進確認。Phase 2 生成試次視窗時間線圖，每屏時長、按鍵、RT 起點一目了然。5 道 Gate 硬門禁。38 範式參考 |
| ② | **程式碼生成** `psy-exp-coder` | 從設計規範生成可執行程式碼 | 4 層優先級架構。交付前用 10 項品質門檢查計時、反應、儲存、清理、依賴和其他阻斷風險 |
| ③ | **程式碼檢查** `psy-exp-reviewer` | 檢查程式碼是否符合已確認設計 | 沒有正式電腦的試跑記錄時，不會宣稱「可以開始收資料」 |

### 平台

| 平台 | 特點 |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 在實驗室電腦執行的 Python 實驗；計時仍需在目標設備驗證 |
| 🌐 **[jsPsych](https://www.jspsych.org/)** | 瀏覽器或線上實驗；需在實際瀏覽器和參與者設備測試 |
| 🧮 **[Psychtoolbox](https://psychtoolbox.org/)** | MATLAB/Octave 實驗；可精細控制顯示和設備，但仍須同步與硬體校準 |

### 實驗設計參考

**38 個實驗設計參考**，每個按統一思路整理：何時使用 → 核心邏輯 → 必須確認 → 不要假設 → 試次視窗時間線 → 條件表 → 資料分析 → 變體與參考。

這些參考用來協助確認實驗，**不等於 38 × 3 個生成器都已在三種平台的正式設備上驗證**。

| 類別 | 範式 |
|------|------|
| 🎯 **注意與抑制控制** | Stroop · Eriksen Flanker · Simon · Go/No-go · Stop-signal · ANT · Posner Cuing · Visual Search · Dot-probe · Navon · CPT · Antisaccade |
| 🧠 **記憶與工作記憶** | N-back · Sternberg · Corsi Blocks · Change Detection · Drag and Drop |
| 🔄 **執行功能與認知靈活性** | Task Switching · WCST · Choice RT |
| 👥 **社會認知與情緒** | Cyberball · Climate Reflection · Phone a Friend · Rating · Priming · IAT · EAST |
| 💰 **決策與獎勵** | BART · Delay Discounting · Rating to Choice · Ultimatum Game |
| 👁️ **感知與心理物理** | Psychophysics Staircase · Multisensory Nature · Mental Rotation |
| 🌱 **發展與個體差異** | Children Flanker · Bilingual Stroop · Numerical Stroop · Writing Distraction |

---

## 📊 資料分析

分析方案可以在資料收集前規劃，也可以在取得資料後進一步落實，分三步——設計分析方案、生成程式碼、檢查執行結果。

### 技能

| # | 技能 | 做什麼 | 關鍵細節 |
|---|------|--------|---------|
| ④ | **分析設計** `psy-ana-designer` | 從科學問題出發，設計完整分析方案 | 5 階段漸進確認。Phase 2 確認檔案組織與被試、刺激、場次的資料層級。Phase 3 只比較會影響目前決策的重點；只有候選方法確實接近或選擇影響很大時，才使用完整 12 維度比較 |
| ⑤ | **分析程式碼** `psy-ana-coder` | 從分析方案生成可重複腳本 | Phase 0 驗證 config → 確認 R/Python → 12 步腳本生成。10 項品質門。R：tidyverse/lme4/ggplot2。Python：pandas/statsmodels/seaborn。程式碼全部 config 驅動 |
| ⑥ | **分析審計** `psy-ana-reviewer` | 把靜態程式碼檢查與實際結果檢查分開 | 只看程式碼最多到 `ready_for_execution`；還要在乾淨環境成功執行，並檢查日誌、表格、圖、依賴鎖與環境，才可能到 `ready_for_publication` |

### 分析語言與環境

| 語言與環境 | 特點 |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | 統計建模與學術報告，可按需要使用 lme4、ggplot2、Quarto 和 R Markdown |
| 🐍 **[Python](https://www.python.org/)** | 通用資料處理、統計分析、視覺化和 Jupyter 工作流程 |

### 分析方法

**60 種方法參考、48 種圖表參考**用來尋找候選方案，不是自動處方。只比較真正會影響目前選擇的重點；候選方法確實接近或選擇影響很大時，才使用完整 12 維度比較。

| 類別 | 方法舉例 |
|------|------|
| **均值比較** | 配對/獨立 t 檢定、被試內/間 ANOVA、混合 ANOVA、ANCOVA、MANOVA |
| **混合模型** | 線性混合模型（LMM）、邏輯混合模型（GLMM）、Gamma GLMM、交叉隨機效應 |
| **中介調節** | 中介分析、調節分析、有調節的中介、結構方程模型 |
| **迴歸與縱向** | 多元迴歸、分位數迴歸、增長曲線、交叉滯後面板、時間序列 |
| **相關與分類** | Pearson/Spearman 相關、重複測量相關、卡方檢定、典型相關 |
| **非參與穩健** | Wilcoxon、Friedman、置換檢定、Bootstrap、穩健迴歸 |
| **貝葉斯** | 貝葉斯 t 檢定、貝葉斯 ANOVA、貝葉斯混合模型 |
| **測量與量表** | 信度分析（α/ω/ICC）、探索性/驗證性因素分析、多維標度法 |
| **信號檢測與診斷** | d'、ROC 曲線、心理測量函數 |
| **RT 與決策建模** | Ex-Gaussian 分佈、漂移擴散模型（DDM） |
| **元分析與效力** | 元分析、效力分析、等效性檢定 |
| **專項方法** | 多重插補、LASSO/Ridge、網絡分析、聚類分析、潛在類別分析 |

---

## 🎬 Demo

### 🧪 實驗 · PsychoPy Stroop

> "我要做一個 Stroop，紅綠藍三色文字，按鍵判斷墨色，50:50 一致不一致，2 block 各 60 試次"

```
使用者           ❯ 我要做一個 Stroop 任務

Amazing PsyCoder ❯ 🟢 Phase 1/5 · 診斷
                   範式 Stroop · 確認使用 PsychoPy？

使用者           ❯ 對，PsychoPy。

Amazing PsyCoder ❯ 🟢 Phase 2/5 · 試次視窗 + 反應規則（最關鍵）
                   墨色紅綠藍 → f=紅 j=綠 k=藍。試次時間線：
                       Window 1: 注視點             Window 2: 刺激呈現            Window 3: 空屏等待   
                   ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
                   │                      │      │                      │      │                      │
                   │          +           │  →   │       紅色"綠"       │  →   │                      │
                   │                      │      │                      │      │                      │
                   └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                            500ms                         2000ms                        500ms          
                            無反應                      f / j / k                       無反應         
                                                        ← RT起點                                      
 
                        Window 4: 回饋     
                   ┌──────────────────────┐
                   │                      │
                   │        正確!         │
                   │                      │
                   └──────────────────────┘
                            1000ms         
                            無反應         
                   Gate 1 ✅ 視窗完整、反應映射已確認

使用者           ❯ 時間線和按鍵沒問題。ITI 400-800ms 隨機。

Amazing PsyCoder ❯ 🟢 Phase 3/5 · 條件表
                   一致:不一致 = 60:60 → 120 試次條件表已生成。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Block 結構
                   2 blocks × 60 trials · 回饋僅練習 block。Gate 3 ✅

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最終審查
                   ┌──────────────────────────────────────────────┐
                   │ 設計決策註冊表                               │
                   │ 範式 Stroop · 平台 PsychoPy    ← 使用者確認  │
                   │ 按鍵 f/j/k · 一致:不一致 50:50 ← 使用者確認  │
                   │ ITI 400-800ms 隨機             ← 使用者確認  │
                   │ 試次時間線 4 視窗              ← 範式慣例    │
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ 全部確認 → 路由至程式碼生成

使用者           ❯ 生成。

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md 已生成
                   參數置頂 · CJK 字體已配置 · 增量儲存 → 自動路由至審計

Amazing PsyCoder ❯ 🔍 靜態程式碼檢查沒有發現必須修正的問題。
                   現在可以在正式電腦試跑，但還不能直接開始收資料。

使用者           ❯ 已完成啟動退出、短程完整執行、資料完整性與中斷恢復檢查。

Amazing PsyCoder ❯ 🔍 已檢查試跑記錄與資料檔案。
                   就緒狀態：ready_for_collection
                   可以開始正式收資料。
```

### 📊 分析 · R Stroop

> "幫我分析 Stroop 資料，一致和不一致條件的 RT 有沒有顯著差異"

```
使用者           ❯ 幫我分析 Stroop 資料，一致和不一致 RT 有沒有差異

Amazing PsyCoder ❯ 🟢 Phase 1/5 · 理解實驗與科學問題
                   請提供實驗 config 或描述實驗設計

使用者           ❯ 被試內，IV: condition(一致/不一致)，DV: rt+acc。30 被試

Amazing PsyCoder ❯ 🟢 Phase 2/5 · 理解資料結構
                   資料怎麼存的？每個被試一個檔案還是彙總？

使用者           ❯ 每個被試一個 CSV，命名 sub-001_stroop.csv
                   列: subject_id, stimulus, condition, rt, acc, trial

Amazing PsyCoder ❯ stimulus 是每位被試各自不同，還是同一組刺激會給多人看？

使用者           ❯ 所有被試都會看到同一組 60 個顏色詞組合，
                   而且每位被試都有重複試次。

Amazing PsyCoder ❯ 已確認：資料同時在被試和刺激層級重複。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · 先定義要估計什麼，再選方法
                   主要估計目標：總體上，不一致減一致的平均 RT 差。

                   RT 主模型：
                   rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)

                   正確率可作二項分布混合模型的補充分析。
                   配對 t 檢定較簡單，但回答的是彙總後的被試平均問題。
                   如果隨機效應不能穩定估計，會按事先寫明的順序簡化並報告診斷。

使用者           ❯ 確認估計目標、公式，以及被試／刺激資料層級。
                   RT 用混合模型，正確率作補充分析。

Amazing PsyCoder ❯ Gate 3 ✅ 估計目標、公式、資料層級與備選方案已確認

Amazing PsyCoder ❯ 🟢 Phase 4/5 · 清理規則、執行環境與輸出
                   請提供任務說明或預註冊中的 RT、缺失與排除規則。
                   沒有依據時，不會自動套用固定門檻或 SD 規則。

使用者           ❯ 預註冊規定：RT 主分析只用正確且 RT 非缺失的試次；
                   不做固定 RT 上下限、SD 剔除或自動排除被試；
                   另做 log-RT 敏感性分析。實驗室使用 R 4.4.1、
                   renv.lock 和 R Markdown。

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最終審查
                   ┌──────────────────────────────────────────────┐
                   │ 分析決策註冊表                               │
                   │ 科學問題: 一致 vs 不一致 RT       ← 使用者確認  │
                   │ 公式：被試隨機斜率 + 刺激隨機截距   ← 使用者確認 │
                   │ 清理：預註冊規則並記錄每一步數量    ← 使用者確認 │
                   │ 環境：R 4.4.1 + renv.lock          ← 使用者確認 │
                   │ 輸出：條件差、區間、診斷與圖表      ← 使用者確認 │
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ 儲存 analysis_config.yaml → 路由至程式碼生成

使用者           ❯ 生成。

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd + renv.lock 已生成
                   已記錄依賴版本並完成靜態程式碼檢查

Amazing PsyCoder ❯ 🔍 就緒狀態：ready_for_execution
                   程式碼可以執行，但結果還不能直接寫進論文。

使用者           ❯ 已在乾淨環境執行，並提供記錄、表格、圖與版本資訊。

Amazing PsyCoder ❯ 🔍 已檢查執行結果。
                   就緒狀態：ready_for_publication
```

---

## 📂 檔案結構

```text
amazing-psycoder-skills/
├── amazing-psycoder/                  ← 總入口（v1.4.0）
│   ├── SKILL.md                       ← 任務分流與全域規則
│   ├── PLATFORMS.md · install.sh      ← 平台說明與安裝器
│   ├── STANDALONE.md                  ← 直接在 Agent 中使用
│   ├── PSYCODER_STUDIO.md             ← 網站接入說明
│   ├── runtime/                       ← 網站規則與能力範圍
│   ├── scripts/ · tests/              ← 自動檢查
│   ├── requirements-dev.txt           ← 完整檢查的依賴版本
│   │
│   │   # 🧪 實驗編程
│   ├── psy-exp-designer/              ← ① 實驗設計（5 階段 + 38 個設計參考）
│   ├── psy-exp-coder/                 ← ② 實驗程式碼生成（PsychoPy/jsPsych/Psychtoolbox）
│   └── psy-exp-reviewer/              ← ③ 實驗程式碼檢查
│   │
│   │   # 📊 資料分析
│   ├── psy-ana-designer/              ← ④ 分析設計（60 個方法 + 48 個圖表參考）
│   ├── psy-ana-coder/                 ← ⑤ 分析程式碼生成（R/Python）
│   └── psy-ana-reviewer/              ← ⑥ 分析程式碼與輸出檢查
│
├── docs/                              ← 翻譯版 README（繁/英/日/德/法）
├── .github/                           ← 自動測試
└── README.md                          ← 簡體中文首頁
```

---

<div align="center">

💡 有想法或建議？歡迎來信 [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
