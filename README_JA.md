<div align="center">

# 🧠 Amazing PsyCoder 💻

> 実験アイデアから本番対応のコードへ。設計 → 生成 → 監査、3つの必須ステップ。🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Stars](https://img.shields.io/github/stars/soupandpsy/AmazingPsyCoderSkills?style=social)](https://github.com/soupandpsy/AmazingPsyCoderSkills)

[**简体中文**](README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 背景](#-背景) · [⚡ インストール](#-インストール) · [🚀 クイックスタート](#-クイックスタート) · [🎬 デモ](#-デモ) · [✨ 特徴](#-特徴) · [👥 対象者](#-対象者)

</div>

<br>

<table>
<tr><td align="left">

⏱️ &nbsp;RTはどの画面から計測するのか？開始時点を間違えれば、全データが無意味になる。<br>
⌨️ &nbsp;キーマッピングが逆になっていないか？参加者は正しく押したのに、コードが誤判定する。<br>
🚦 &nbsp;No-go試行の「正解」はどう定義する？押すべき時に押さない、押してはいけない時に押す——判定が曖昧。<br>
💾 &nbsp;クラッシュしてもデータは残るのか？最後にまとめて保存する方式では、クラッシュ＝全消失。<br>
🔤 &nbsp;中国語の教示が□□□と表示される？CJKフォント未設定で、参加者には文字化けしか見えない。<br>
😇 &nbsp;動いている、しかし本当に本番収集の準備はできているか？RTの精度、ロジックの正しさ、データの信頼性——体系的な保証はない。

</td></tr>
</table>

### ✨ Amazing PsyCoder はまさにこれを解決します。

自分で修正するコードテンプレートではなく——経験豊富な実験プログラミングのベテランが隣に座っているようなものです。**設計を明確にする → コードを生成する → 収集前に監査する。**

3つの必須ステップ。スキップ不可。**監査を通過しないコードは納品されません。**

---

## 📖 背景

どの研究室にもこうした失敗を経験してきた先輩がいますが、その知識が体系的に引き継がれることは稀です。PsychoPyはBuilderかCoderか？jsPsychのタイムライン変数はどう渡す？なぜ `Screen('Flip')` は `vbl + (waitframes - 0.5) * ifi` なのか？

APIを理解するだけで数週間かかります。

Amazing PsyCoderはこれらの教訓をClaude Codeの3つの必須スキルにエンコードしました——設計オーケストレーション（5段階確認）、コード生成（統一パイプライン + 9項目の品質ゲート）、コード監査（スモークテストプロトコル）。研究室がPsychoPy、jsPsych、Psychtoolboxのどれを使っていても、同じパイプラインでプラットフォームに適したコードを生成します。

---

## 🎯 3つのスキル

| スキル | 役割 | 主な成果物 |
|-------|------|-----------|
| 1️⃣ **設計** `psych-experiment-programming` | 5段階の段階的確認：試行タイムライン → 反応ルール → 条件表 → ブロック構造 → 最終確認 | config YAML + 条件表 |
| 2️⃣ **コード生成** `psych-experiment-coder` | 4層優先度アーキテクチャ、9項目の品質ゲート。`time.sleep()` / `KbCheck`によるRT計測は即時拒否 | 実行可能コード + README |
| 3️⃣ **監査** `psych-experiment-code-reviewer` | スモークテスト + データ整合性チェック + パラダイム別障害モードスキャン。RT開始時点、キーマッピング、データ安全性を項目ごとに審査 | 監査レポート + 準備完了ラベル |

---

## ⚡ インストール

Claude Codeで以下の指示を入力すると、システムが自動的にインストールします：

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/AmazingPsyCoderSkills
```

Claude Codeがリポジトリをクローンし、4つのスキルを `~/.claude/skills/` に登録します。完了後、`/amazing-psycoder` と入力して起動します。

<details>
<summary><b>🛠️ 手動インストール</b></summary>

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

## 🚀 クイックスタート

Claude Codeで `/amazing-psycoder` と入力し、実験の内容を説明します：

> "I want a Stroop task, red/green/blue text, key-press response, 2 blocks of 60 trials each"

システムがオーケストレーターにルーティングし、5段階の設計プロセスをガイドします。この過程で、試行ウィンドウのタイムラインが生成されます：

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ 注視点     │ →  │ 刺激提示   │ →  │ 空白       │ →  │ フィードバック │
│ +         │    │ 赤 "绿"   │    │           │    │ 正解！     │
│ 500ms     │    │ 2000ms   │    │ 500ms     │    │ 1000ms    │
│           │    │ ← キー押下 │    │           │    │           │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                   RT 開始時点
```

タイムラインを確認したら、対象プラットフォームを選択します。実行可能なファイル（`.py` / `.js` / `.m`）と実験用READMEが出力されます。

---

## 🎬 デモ

### 🐍 PsychoPy — ストループ課題

> "I want a Stroop task, red/green/blue text, judge ink color, 50:50 congruent:incongruent, 2 blocks × 60 trials"

```
ユーザー         ❯ I want a Stroop task

Amazing PsyCoder ❯ 最初にいくつか確認させてください：
                   1. 3つのインク色 → 3つのキー：f=赤、j=緑、k=青。よろしいですか？
                   2. 一致試行と不一致試行の比率 50:50。よろしいですか？
                   3. 注視点 500ms、刺激最大 2000ms、フィードバック 500ms、
                      ITI 600-900ms（ランダム）。これらのデフォルト値を使いますか？

ユーザー         ❯ 最初の2つは問題なし。ITIは400-800msに変更。

Amazing PsyCoder ❯ 更新しました。試行タイムライン：
                   ┌───────────────────────────────────────────────┐
                   │ 注視点(500ms) → 刺激(2000ms/キー押下)          │
                   │ → フィードバック(500ms) → ITI(400-800ms)       │
                   └───────────────────────────────────────────────┘
                   すべて確認できましたか？コードを生成しますか？

ユーザー         ❯ 生成。

Amazing PsyCoder ❯ ✅ コード生成完了：stroop_task.py + README.md
                   パラメータは先頭に配置、FONT_CONFIG設定済み、増分保存オン。
                   監査を実行しますか？

ユーザー         ❯ 監査。

Amazing PsyCoder ❯ 🔍 監査合格。準備状態：ready_for_collection
                   データ収集を開始できます。
```

---

## ✨ 特徴

| 特徴 | 説明 |
|------|------|
| 🔬 **よくある落とし穴をブロック** | `time.sleep()`、`KbCheck`によるRT計測——目にする前に拒否されます |
| 🚀 **すぐに実行可能** | すべての編集可能なパラメータはファイル先頭に配置——探す必要なし |
| 🌏 **CJKテキストが正常動作** | 中国語テキストを自動検出しフォントを設定——□□□は表示されません |
| 🧪 **クラッシュ耐性データ保存** | 各試行が即座にディスクに保存——クラッシュしても収集済みデータは失われません |
| 🎛️ **1つのシステム、3つのプラットフォーム** | PsychoPy、jsPsych、Psychtoolboxのどれでも同じパイプライン |

**深夜のデバッグを減らし、データ収集前の確信を増やす。🧪✨**

---

## 📦 プラットフォーム対応

| プラットフォーム | バージョン | 用途 | パラダイム | デモ |
|----------|---------|----------|:--:|:--:|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 2024.x+ | ローカル実験、USB HIDハードウェアタイムスタンプ | 27 | 45 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | 7.x | オンライン実験、ブラウザ配備 | 25 | 23 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | 3.0.21+ | GPUレベルのフレーム精密制御 | 5 | 100 |

---

## 👥 対象者

- 👶 コードの経験は少ないが、実験プログラムを完成させなければならない
- 🎓 実験コードを書いている（または書こうとしている）学部生・大学院生
- 🧠 認知・行動・社会心理学の実験を行っている研究者
- 🐍 PsychoPyでローカル実験 · 🌐 jsPsychでオンライン実験 · 🧮 Psychtoolbox / MATLAB
- 😵‍💫 RT、ランダム化、条件表で同じ失敗を繰り返してきた——体系的な品質保証を求めている

---

## 📦 パラダイムカバレッジ

**38パラダイム**：14コア（完全設計仕様）+ 24拡張（参考説明）

| タイプ | パラダイム |
|------|-----------|
| **コア** | Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST |
| **拡張** | Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST 他 |

---

## 📂 ファイル構造

```
AmazingPsyCoderSkills/
├── amazing-psycoder/                  ← オーケストレーター（エントリーポイント）
├── psych-experiment-programming/      ← ① 設計層（5段階ワークフロー + 38パラダイム）
├── psych-experiment-coder/            ← ② コード生成層
│   ├── psychopy/
│   ├── jspsych/
│   └── psychtoolbox/
└── psych-experiment-code-reviewer/    ← ③ 監査層（5モード + スモークテスト）
```

---

<div align="center">

Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
