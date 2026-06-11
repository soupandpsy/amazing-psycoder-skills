<div align="center">

# 🧠 Amazing PsyCoder 💻

> 讓心理學研究的程式碼門檻徹底消失。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
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

<h3 align="center">🔍 當前心理學研究面臨的痛點</h3>

🔬 一個 idea 要變成能收資料的實驗程式，得先學 Python 或 JavaScript 或 MATLAB。<br>
📦 實驗室祖傳程式碼換台電腦就崩，沒人說得清依賴、沒人改得動邏輯。<br>
📊 統計方法靠習慣選——「大家都用 ANOVA」，審稿人一句質疑就得從頭再來。<br>
🔁 分析結果只有自己跑得出來，換個環境換個隨機種子結論可能就變了。<br>
✂️ 做實驗和做分析的經常是兩撥人——收完資料才發現設計時根本沒想好怎麼分析。

<h3 align="center">🧱 實驗推進落地的兩大門檻</h3>

**第一道：實驗編程。** 想驗證一個假設，得先把實驗寫出來。PsychoPy 的 Builder 不夠靈活，Coder 要學 Python；jsPsych 要學 JavaScript 和 timeline 邏輯；Psychtoolbox 要學 MATLAB 和幀同步。光是搞清楚「RT 從哪一屏開始算」「按鍵映射怎麼不反」「資料怎麼存崩了不丟」就要花幾週。一個 idea 從腦子裡到能跑起來，中間耗掉的時間比設計實驗本身還長。

**第二道：資料分析。** 資料收回來了，該用什麼統計方法？被試內設計用配對 t 還是混合模型？正確率接近天花板 ANOVA 還能用嗎？審稿人問「為什麼用這個方法」時怎麼回答？程式碼換了台電腦還能不能跑出一樣的結果？

這些不是能力問題，是缺少合適的工具。寫程式碼和做分析應該讓研究更順利，不應該成為卡住你的地方。

<h3 align="center">✨ Amazing PsyCoder 的解決方案</h3>

不需要你會 Python，不需要你懂統計，你只需要把實驗想法和資料交給它——它會引導你一步步確認設計、生成程式碼、完成審計。最終拿到的程式碼打開就能跑，分析結果期刊審稿人也挑不出毛病。

Amazing PsyCoder 把實驗編程和資料分析的經驗編碼進了 7 個技能——1 個編排器加 6 個子技能，遵循 [agentskills.io](https://agentskills.io) 開放標準，支援 Claude Code / Codex / Hermes / OpenClaw。

**把時間還給研究本身。**

---

## 👥 適合這些人

- 🎓 正在或準備寫實驗程式碼的心理學大學生、研究生
- 🧠 做認知、行為、社會心理實驗的研究者
- 😵‍💫 在 RT、隨機化、條件表上反覆踩過坑，希望實驗程式碼有品質保障
- 📊 收完資料不確定該用什麼統計方法，希望有系統化分析方案
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB 使用者

---

## ⚡ 安裝

在 AI 對話中直接輸入對應平台的命令：

**Claude Code**

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/amazing-psycoder-skills
```

**Codex**

```
$skill-installer
```

輸入倉庫地址：`https://github.com/soupandpsy/amazing-psycoder-skills`

**Hermes**

```
hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills
```

**OpenClaw**

```
npm i -g clawhub && clawhub install amazing-psycoder
```

安裝後輸入 `/amazing-psycoder` 即可啟動。

<details>
<summary><b>終端安裝（所有平台通用）</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
./install.sh           # 自動檢測平台並安裝
# 或手動指定: ./install.sh claude | codex | hermes | openclaw
```

</details>

---

## 🚀 快速開始

安裝後輸入 `/amazing-psycoder`，直接描述你想做什麼：

> 「我要做一個 Stroop 任務，紅綠藍三色，按鍵反應」→ 自動進入實驗設計

> 「幫我分析 Stroop 資料，一致和不一致 RT 有沒有差異」→ 自動進入分析設計

不需要指定用哪個技能——編排器根據你的需求自動判斷。之後 skill 會一步步引導你：確認設計、選擇方法、生成程式碼、審計檢查。你只需要回答它提出的問題。

---

## 🧪 實驗編程

從想法到可採集資料的實驗程式碼，分三步走——設計、生成、審計。

### 技能

| # | 技能 | 做什麼 | 關鍵細節 |
|---|------|--------|---------|
| ① | **設計編排** `psy-exp-designer` | 把實驗想法變成完整設計規範 | 5 階段漸進確認。Phase 2 生成試次視窗時間線圖，每屏時長、按鍵、RT 起點一目了然。5 道 Gate 硬門禁。38 範式參考 |
| ② | **程式碼生成** `psy-exp-coder` | 從設計規範生成可執行程式碼 | 4 層優先級架構。9 項品質門自動攔截：`time.sleep()`、`KbCheck` 測 RT 直接拒絕。12 步程式碼模板，參數置頂 |
| ③ | **程式碼審計** `psy-exp-reviewer` | 採集前最後一關 | 5 種審查模式。煙霧測試協定。範式失敗模式檢查。不通過給修復路徑。就緒標籤：`ready_for_collection` |

### 平台

| 平台 | 特點 |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Python 生態，USB HID 硬體時間戳，毫秒級 RT 精度。本地實驗室首選 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | JavaScript 生態，瀏覽器即執行，無需安裝。線上實驗首選 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | MATLAB 生態，GPU 級幀精確控制。對時序精度要求極致時首選 |

### 範式覆蓋

**38 個範式**，每個按統一元邏輯整理：何時使用 → 核心邏輯 → 必須確認 → 不要假設 → 試次視窗時間線 → 條件表 → 資料分析 → 變體與參考。

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

資料收回來後，同樣分三步走——設計分析方案、生成程式碼、審計可重複性。

### 技能

| # | 技能 | 做什麼 | 關鍵細節 |
|---|------|--------|---------|
| ④ | **分析設計** `psy-ana-designer` | 從科學問題出發，設計完整分析方案 | 5 階段漸進確認。Phase 2 確認資料檔案組織（多檔案/單檔案、命名規則、CSV/Excel/TSV）。Phase 3 用 12 維度對比選擇最優方法。Config YAML 為唯一事實源 |
| ⑤ | **分析程式碼** `psy-ana-coder` | 從分析方案生成可重複腳本 | Phase 0 驗證 config → 確認 R/Python → 12 步腳本生成。10 項品質門。R：tidyverse/lme4/ggplot2。Python：pandas/statsmodels/seaborn。程式碼全部 config 驅動 |
| ⑥ | **分析審計** `psy-ana-reviewer` | 發表前最後一關 | 4 種審查模式。攝入協定自動檢測。統計正確性 + 可重複性 + 假設檢定審查。R/Python 雙平台反模式檢查。不通過給修復路徑。就緒標籤：`ready_for_publication` |

### 平台

| 平台 | 特點 |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | 統計計算標準。tidyverse + lme4 + ggplot2 + RMarkdown。學術出版首選 |
| 🐍 **[Python](https://www.python.org/)** | 通用科學計算。pandas + statsmodels + seaborn + Jupyter。可重複分析 |

### 分析方法

**60 種分析方法，48 種圖表類型**。每個方法選擇經過 12 維度對比：統計效力 · 假陽性控制 · 資料利用率 · 異常值敏感度 · 假設穩健性 · 可解釋性 · 領域接受度 · 效應量可比性 · 可重複性 · 可擴展性 · 樣本量約束 · 計算可實現性。

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

Amazing PsyCoder ❯ 🔍 審計通過 · 就緒標籤：ready_for_collection
                   可開始資料採集。
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
                   列: subject_id, condition, rt, acc, trial

Amazing PsyCoder ❯ 已確認：30 被試 × 每個被試 1 檔案。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · 資料特點 + 匹配方法（核心階段）
                   RT 有右偏嗎？正確率有沒有接近天花板？

使用者           ❯ RT 有點右偏，正確率大概 95%

Amazing PsyCoder ❯ 正確率接近天花板 → glmer(binomial) 做 acc 分析
                   對 RT，12 維度比較 A vs B：

                   ┌────────────┬─────────────────┬─────────────────┐
                   │ 維度       │ A: 配對 t 檢定   │ B: 線性混合模型  │
                   ├────────────┼─────────────────┼─────────────────┤
                   │ 統計效力   │ 30 點（被試均值）│ 1800 點（全試次）│
                   │ 資料利用率 │ 每個被試壓縮為 1 點│ 全部試次參與   │
                   │ 可擴展性   │ 加協變數需重做   │ 公式加 + 即可    │
                   │ 可解釋性   │ d=0.5 人人懂     │ 需解釋隨機效應   │
                   └────────────┴─────────────────┴─────────────────┘

                   側重效力和可擴展 → 選 B。側重簡單 → 選 A。

使用者           ❯ 選 B

Amazing PsyCoder ❯ Gate 3 ✅ 方法已選（附 12 維度比較理由）

Amazing PsyCoder ❯ 🟢 Phase 4/5 · 分析細節
                   清洗: RT 150-2000ms · 正確試次 · 被試 acc<60% 排除
                   · ±2.5 SD 試次排除 · 圖表: 雨雲圖+個體連線 ⚠️

使用者           ❯ 確認

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最終審查
                   ┌──────────────────────────────────────────────┐
                   │ 分析決策註冊表                               │
                   │ 科學問題: 一致 vs 不一致 RT       ← 使用者確認  │
                   │ 方法: lmer (使用者選 B)            ← 使用者確認  │
                   │ RT 150-2000ms · 被試 acc<60%       ← 預設 ⚠️   │
                   │ 圖表: 雨雲圖 + 個體連線            ← 預設 ⚠️   │
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ 儲存 analysis_config.yaml → 路由至程式碼生成

使用者           ❯ 生成。

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd 已生成
                   Config 驅動 · 10 項品質門 · 12 步腳本結構 → 路由至審計

Amazing PsyCoder ❯ 🔍 審計通過 · 就緒標籤：ready_for_publication
```

---

## 📂 檔案結構

```
amazing-psycoder-skills/
├── amazing-psycoder/                  ← 編排器（系統入口，v1.3）
│   ├── SKILL.md · PLATFORMS.md · install.sh
│   │
│   │   # 🧪 實驗編程
│   ├── psy-exp-designer/              ← ① 實驗設計（5 階段 + 38 範式 + 9 參考檔案）
│   ├── psy-exp-coder/                 ← ② 實驗程式碼生成（PsychoPy/jsPsych/Psychtoolbox）
│   └── psy-exp-reviewer/              ← ③ 實驗審計（5 模式 + 煙霧測試 + 修復迴圈）
│   │
│   │   # 📊 資料分析
│   ├── psy-ana-designer/              ← ④ 分析設計（5 階段 + 60 方法 + 48 圖表）
│   ├── psy-ana-coder/                 ← ⑤ 分析程式碼生成（R/Python 雙平台）
│   └── psy-ana-reviewer/              ← ⑥ 分析審計（4 模式 + 攝入協定 + 修復迴圈）
│
├── docs/                              ← 多語言 README（簡/繁/英/日/德/法）
└── README.md
```

---

<div align="center">

💡 有想法或建議？歡迎來信 [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
