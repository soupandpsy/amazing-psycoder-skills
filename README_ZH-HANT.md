<div align="center">

# 🧠 Amazing PsyCoder 💻

> 從實驗構想到生產級程式碼，設計 → 生成 → 審計，三步強制交付。🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Stars](https://img.shields.io/github/stars/soupandpsy/AmazingPsyCoderSkills?style=social)](https://github.com/soupandpsy/AmazingPsyCoderSkills)

[**简体中文**](README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 為什麼](#-為什麼做這個專案) · [⚡ 安裝](#-安裝) · [🚀 快速開始](#-快速開始) · [🎬 Demo](#-demo) · [✨ 特點](#-特點) · [👥 適合誰](#-適合這些人)

</div>

<br>

<table>
<tr><td align="left">

⏱️ &nbsp;RT 到底從哪一屏開始算？計時起點標錯，整批反應時資料白收。<br>
⌨️ &nbsp;按鍵對映有沒有寫反？被試按對了，程式碼判錯了。<br>
🚦 &nbsp;No-go 不按鍵怎麼算正確？該按不按、不該按按了，規則不清。<br>
💾 &nbsp;程式崩了資料還在不在？跑完才儲存，崩了全丟。<br>
🔤 &nbsp;中文指導語變成 □□□ — 沒配字型，被試看到的全是亂碼。<br>
😇 &nbsp;程式碼能跑，但真的能正式採集嗎？RT 是否準確、邏輯是否正確、資料是否可靠——沒有系統性的保障。

</td></tr>
</table>

### ✨ Amazing PsyCoder 解決的就是這些。

不是給你一份程式碼範本自己改，而是像一位坐在你旁邊的實驗程式設計老手——**先幫你理清設計 → 再生成程式碼 → 最後做採集前審查**。

三步全部強制，不可跳過。**未經審計的程式碼不交付。**

---

## 📖 為什麼做這個專案

每個實驗室都有踩過這些坑的學長學姐，但他們的經驗很少被系統化地沉澱下來。PsychoPy 的 Builder 和 Coder 該用哪個？jsPsych 的 timeline 變數怎麼傳？Psychtoolbox 的 `Screen('Flip')` 為什麼要在 `vbl + (waitframes - 0.5) * ifi` 時刻翻頁？

光搞清楚 API 就要花幾週。

Amazing PsyCoder 把這些經驗編碼進了 Claude Code 的三個強制技能裡——設計編排（5 階段確認）、程式碼生成（統一流水線 + 9 項品質門）、程式碼審計（煙霧測試協定）。不管你的實驗室用 PsychoPy、jsPsych 還是 Psychtoolbox，同一套流程生成對應程式碼。

---

## 🎯 三個技能

| 技能 | 做什麼 | 關鍵輸出 |
|------|--------|---------|
| 1️⃣ **設計編排** `psych-experiment-programming` | 5 階段漸進式確認：試次時間線 → 反應規則 → 條件表 → block 結構 → 最終確認 | config YAML + 條件表 |
| 2️⃣ **程式碼生成** `psych-experiment-coder` | 4 層優先級架構生成程式碼，9 項品質門自動檢查。`time.sleep()` / `KbCheck` 測 RT 直接拒絕 | 可執行程式碼 + README |
| 3️⃣ **程式碼審計** `psych-experiment-code-reviewer` | 煙霧測試 + 資料完整性驗證 + 範式失敗模式檢查。RT 起點、按鍵對映、資料安全逐項審查 | 審計報告 + 就緒標籤 |

---

## ⚡ 安裝

在 Claude Code 中輸入以下指令，系統會自動完成安裝：

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/AmazingPsyCoderSkills
```

Claude Code 會自動 clone 倉庫，把 4 個技能註冊到 `~/.claude/skills/`。完成後輸入 `/amazing-psycoder` 即可啟動。

<details>
<summary><b>🛠️ 手動安裝</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/AmazingPsyCoderSkills /tmp/AmazingPsyCoderSkills
cp -r /tmp/AmazingPsyCoderSkills/amazing-psycoder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-programming ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-coder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/psych-experiment-code-reviewer ~/.claude/skills/
```

</details>

---

## 🚀 快速開始

在 Claude Code 中輸入 `/amazing-psycoder`，然後描述你的實驗：

> "我要做一個 Stroop 任務，紅綠藍三色，按鍵反應，2 個 block 各 60 個試次"

系統自動路由到編排器，引導完成 5 階段設計。設計過程中，系統會生成試次視窗時間線圖：

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 注視點    │ →  │ 刺激呈現  │ →  │ 空屏等待  │ →  │ 回饋      │
│ +        │    │ 紅色"綠"  │    │          │    │ 正確!     │
│ 500ms    │    │ 2000ms   │    │ 500ms    │    │ 1000ms   │
│          │    │ ← 按鍵   │    │          │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                  RT 計時起點
```

確認時間線後，指定目標平台。輸出可直接執行的平台檔案（`.py` / `.js` / `.m`）和實驗說明 README。

---

## 🎬 Demo

### 🐍 PsychoPy — Stroop 任務

> "我要做一個 Stroop，紅綠藍三色文字，按鍵判斷墨色，50:50 一致不一致，2 個 block 各 60 試次"

```
使用者           ❯ 我要做一個 Stroop 任務

Amazing PsyCoder ❯ 好的，先確認幾件事：
                   1. 三個墨色對應三個按鍵，f=紅，j=綠，k=藍，可以嗎？
                   2. 一致試次和不一致試次各佔 50%，可以嗎？
                   3. 注視點 500ms，刺激最長 2000ms，回饋 500ms，ITI 600-900ms 隨機，
                      這些時間參數按預設設定？

使用者           ❯ 前兩個沒問題。ITI 改成 400-800ms。

Amazing PsyCoder ❯ 已更新。試次時間線如下：
                   ┌──────────────────────────────────────────────┐
                   │  Fixation(500ms) → Stimulus(2000ms/按鍵)     │
                   │  → Feedback(500ms) → ITI(400-800ms)          │
                   └──────────────────────────────────────────────┘
                   以上確認無誤，開始生成程式碼？

使用者           ❯ 生成。

Amazing PsyCoder ❯ ✅ 程式碼已生成：stroop_task.py + README.md
                   參數已置頂，FONT_CONFIG 已配置，增量儲存已開啟。
                   是否需要審計？

使用者           ❯ 審計。

Amazing PsyCoder ❯ 🔍 審計通過，就緒標籤：ready_for_collection
                   可以開始採集資料了。
```

---

## ✨ 特點

| 特點 | 說明 |
|------|------|
| 🔬 **常見坑自動攔截** | `time.sleep()`、`KbCheck` 測 RT——系統直接拒絕，不讓你踩 |
| 🚀 **打開就能跑** | 所有參數置頂在檔案開頭，想調不用翻程式碼 |
| 🌏 **中文不出方框** | 自動檢測中文並配置字型，被試看到的是字不是 □□□ |
| 🧪 **崩潰不丟資料** | 每個試次結束立刻存檔，崩了已收的資料全在 |
| 🎛️ **一個系統，三個平台** | 不管用 PsychoPy、jsPsych 還是 Psychtoolbox，同一套流程 |

**少一點玄學除錯，少一點凌晨崩潰，多一點正式採集前的安全感。🧪✨**

---

## 📦 平台支援

| 平台 | 版本 | 定位 | 範式 | Demo |
|------|------|------|:--:|:--:|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 2024.x+ | 本地實驗室，USB HID 硬體時間戳 | 27 | 45 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | 7.x | 線上實驗，瀏覽器端部署 | 25 | 23 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | 3.0.21+ | GPU 級影格精確控制 | 5 | 100 |

---

## 👥 適合這些人

- 👶 不太會寫程式碼，但必須搞定實驗程式
- 🎓 正在寫或將要寫實驗程式碼的大學生、研究生
- 🧠 做認知、行為、社會心理實驗的研究者
- 🐍 PsychoPy 本地實驗 · 🌐 jsPsych 線上實驗 · 🧮 Psychtoolbox / MATLAB
- 😵‍💫 在 RT、隨機化、條件表上反覆踩過坑，希望實驗程式碼有品質保障

---

## 📦 範式覆蓋

**38 個範式**：14 個核心（完整設計規範）+ 24 個擴展（參考描述）

| 類型 | 範式 |
|------|------|
| **核心** | Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST |
| **擴展** | Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST 等 |

---

## 📂 檔案結構

```
AmazingPsyCoderSkills/
├── amazing-psycoder/                  ← 編排器（系統入口）
├── psych-experiment-programming/      ← ① 設計層（5 階段工作流 + 38 範式）
├── psych-experiment-coder/            ← ② 程式碼生成層
│   ├── psychopy/
│   ├── jspsych/
│   └── psychtoolbox/
└── psych-experiment-code-reviewer/    ← ③ 審計層（5 模式 + 煙霧測試）
```

---

<div align="center">

Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
