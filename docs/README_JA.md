<div align="center">

# 🧠 Amazing PsyCoder 💻

> 心理学研究者がコードではなく、研究上の問いにより集中できるように。

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

[📖 なぜ](#-なぜこのプロジェクトなのか) · [👥 対象者](#-対象者) · [⚡ インストール](#-インストール) · [🚀 クイックスタート](#-クイックスタート) · [🧪 実験プログラミング](#-実験プログラミング) · [📊 データ分析](#-データ分析) · [🎬 デモ](#-デモ) · [📂 ファイル構造](#-ファイル構造)

</div>

<br>

## 📖 なぜこのプロジェクトなのか

<h3 align="center">🔍 研究設計からデータ分析までに生じる一般的な課題</h3>

🔬 研究アイデアをデータ収集可能な実験プログラムにするには、Python、JavaScript、または MATLAB が必要になることがあります。<br>
📦 研究室にある既存コードは、実行環境が変わると動かなくなる場合があり、依存関係や中核ロジックの保守も容易ではありません。<br>
📊 統計手法を慣例だけで選ぶと、研究上の問い、変数の型、データ構造との対応を説明しにくくなります。<br>
🔁 ソフトウェアのバージョンや依存環境を記録しなければ、別の PC で分析を再現できないことがあります。<br>
✂️ 実験設計と分析計画が切り離されていると、データ収集後に予定した分析を実行できないと判明する場合があります。

<h3 align="center">🧱 研究を進める上での二つの主要課題</h3>

**一つ目：実験プログラミング。** 仮説を検証するには、実験設計をプログラムに変換する必要があります。PsychoPy Builder は一部の複雑な設計では柔軟性が足りない場合があり、Coder には Python、jsPsych には JavaScript とタイムラインの知識、Psychtoolbox には MATLAB と表示同期の知識が必要です。RT の計測起点、キーマッピング、中断後のデータ保存は、明示的に設計して個別に確認する必要があります。

**二つ目：データ分析。** 分析計画はデータ収集前から検討し、取得後に実際のデータ構造に合わせて実装することが望まれます。被験者内計画には対応のある t 検定と混合モデルのどちらが適切か。正答率が上限に近い場合はどうモデル化するか。手法の選択理由をどう説明するか。別の PC で同じ結果を再現できるか。これらは研究目的、データ階層、ソフトウェア環境に基づいて判断します。

これらの課題は、プログラミングだけでなく、研究設計、統計的推論、データ管理、再現可能性にも関係します。

<h3 align="center">✨ Amazing PsyCoder が支援すること</h3>

実験のアイデア、既存の設計、または手元のデータから始められます。Amazing PsyCoder は、研究上の規則の確認、コード生成、問題の確認を段階的に支援します。必要に応じて、設定、データ説明、除外基準の根拠、実行記録は利用者が提供します。AI の出力だけを「データ収集可能」「発表可能」とは判定しません。実験は収集用 PC で試行し、分析は実際に実行して出力を確認する必要があります。

Amazing PsyCoder は 7 つの Skill、すなわち 1 つの入口 Skill と 6 つの専門 Skill で構成され、[agentskills.io](https://agentskills.io) のオープン標準に準拠しています。Claude Code、Codex、Hermes、OpenClaw という 4 つの AI エージェントにインストールできます。

研究そのものに、時間を返しましょう。

---

## 👥 対象者

- 🎓 これから実験コードを書く（あるいは今まさに書いている）心理学の学部生・大学院生
- 🧠 認知・行動・社会心理学の実験を行っている研究者
- 😵‍💫 RT、ランダム化、条件表の問題を繰り返し経験し、一般的なリスクを体系的に確認したい研究者
- 📊 データを集めたあと、どの統計手法を使えばいいか確信が持てず、体系的な分析計画を求めている
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB ユーザー

---

## ⚡ インストール

リポジトリ付属のインストーラーを推奨します。7 つの Skill を事前に確認し、途中で失敗した場合は以前のファイルを復元します。

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
```

**Claude Code**

```bash
./install.sh claude
```

インストール後は `/amazing-psycoder` を使用します。既定の保存先：`${CLAUDE_CONFIG_DIR:-~/.claude}/skills`。

**Codex**

```bash
./install.sh codex
```

インストール後は `$amazing-psycoder` を使用します。既定の保存先：`~/.agents/skills`。

**Hermes**

```bash
./install.sh hermes
```

インストール後は `/amazing-psycoder` を使用します。既定の保存先：`~/.hermes/skills`。

**OpenClaw**

```bash
./install.sh openclaw
```

インストール後はタスクをそのまま説明し、OpenClaw エージェントに Skill を選択させます。既定の保存先：`~/.openclaw/skills`。

<details>
<summary><b>プロジェクト単位のインストールと確認</b></summary>

<br>

```bash
./install.sh --scope project --project-dir /path/to/repo claude
./install.sh --scope project --project-dir /path/to/repo codex
./install.sh --scope project --project-dir /path/to/workspace openclaw
./install.sh --check codex
```

Hermes には現在、安定したプロジェクト単位の Skill ディレクトリがないため、ユーザー単位のみ対応します。詳細は [`PLATFORMS.md`](../amazing-psycoder/PLATFORMS.md) を参照してください。

</details>

---

## 🚀 クイックスタート

インストール後、利用する AI エージェントで Amazing PsyCoder を呼び出し、やりたいことを説明してください：

> 「Stroop 課題を作りたい。赤・緑・青、キー押し反応」→ 自動的に実験設計へ

> 「Stroop データを分析して、一致と不一致の RT に差があるか見て」→ 自動的に分析設計へ

> 「この実験コードを確認し、特に RT 起点とデータ保存を見て」→ 自動的にコード確認へ

通常は専門 Skill を指定する必要はありません。入口 Skill が依頼内容から設計、コード生成、または確認を選びます。実験を作りたいのかデータを分析したいのか判断できない場合は、先に確認します。

---

## 🧪 実験プログラミング

アイデアから試行を始められる実験コードまで、三つのステップ——設計、生成、確認。

### スキル

| # | スキル | 役割 | ポイント |
|---|------|------|---------|
| ① | **設計** `psy-exp-designer` | 実験アイデアを完全な設計仕様にまとめる | 5 段階の段階的確認。Phase 2 で試行ウィンドウのタイムライン図を生成。各画面の持続時間・キー・RT 起点が一目でわかる。5 つの Gate チェックポイント。38 パラダイム参照 |
| ② | **コード生成** `psy-exp-coder` | 設計仕様から実行可能なコードを生成 | 4 層優先度アーキテクチャ。納品前に 10 項目の品質ゲートで、計時、反応、保存、終了処理、依存関係などの重大なリスクを確認 |
| ③ | **コード確認** `psy-exp-reviewer` | 確認済みの設計とコードが一致するか確認 | 収集用 PC での試行記録がなければ「データ収集可能」とは判定しない |

### プラットフォーム

| プラットフォーム | 特徴 |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 実験室 PC 上の Python 実験。タイミングは対象機で検証が必要 |
| 🌐 **[jsPsych](https://www.jspsych.org/)** | ブラウザ／オンライン実験。実際のブラウザと参加者端末でテストが必要 |
| 🧮 **[Psychtoolbox](https://psychtoolbox.org/)** | MATLAB/Octave 実験。表示や機器を細かく制御できるが、同期とハードウェア校正は必要 |

### 実験設計リファレンス

**38 の実験設計リファレンス**。各項目は統一した流れで整理されています：使用する場面 → コアロジック → 確認必須項目 → 仮定してはいけないこと → 試行ウィンドウタイムライン → 条件表 → データ分析 → バリエーションと参考文献。

これは設計を明確にするための資料であり、**38 × 3 のジェネレーターが三つのプラットフォームすべてで実機検証済みという意味ではありません**。

| カテゴリ | パラダイム |
|------|------|
| 🎯 **注意と抑制制御** | Stroop · Eriksen Flanker · Simon · Go/No-go · Stop-signal · ANT · Posner Cuing · Visual Search · Dot-probe · Navon · CPT · Antisaccade |
| 🧠 **記憶とワーキングメモリ** | N-back · Sternberg · Corsi Blocks · Change Detection · Drag and Drop |
| 🔄 **実行機能と認知的柔軟性** | Task Switching · WCST · Choice RT |
| 👥 **社会認知と感情** | Cyberball · Climate Reflection · Phone a Friend · Rating · Priming · IAT · EAST |
| 💰 **意思決定と報酬** | BART · Delay Discounting · Rating to Choice · Ultimatum Game |
| 👁️ **知覚と心理物理** | Psychophysics Staircase · Multisensory Nature · Mental Rotation |
| 🌱 **発達と個人差** | Children Flanker · Bilingual Stroop · Numerical Stroop · Writing Distraction |

---

## 📊 データ分析

分析計画はデータ収集前に設計でき、データ取得後にさらに具体化できます。流れは、分析計画の設計、コード生成、実行結果の確認という三つのステップです。

### スキル

| # | スキル | 役割 | ポイント |
|---|------|------|---------|
| ④ | **分析設計** `psy-ana-designer` | 科学的な問いから出発し、完全な分析計画を設計 | 5 段階で、ファイル構成と被験者・刺激・セッションの階層を確認。Phase 3 では今回の判断を変え得る点だけを比較し、候補が本当に拮抗する場合や影響の大きい選択に限って完全な 12 次元比較を使う |
| ⑤ | **分析コード** `psy-ana-coder` | 分析計画から再現可能なスクリプトを生成 | Phase 0 で config を検証 → R/Python を確認 → 12 ステップで生成。10 項目の品質ゲート。R：tidyverse/lme4/ggplot2。Python：pandas/statsmodels/seaborn。すべて config 駆動 |
| ⑥ | **分析監査** `psy-ana-reviewer` | 静的なコード確認と、実行後の結果確認を分ける | コードだけの確認は最大でも `ready_for_execution`。`ready_for_publication` には、クリーンな環境での成功実行とログ、表、図、依存関係、環境情報の確認が必要 |

### 分析言語と実行環境

| 言語と実行環境 | 特徴 |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | 統計モデリングと学術レポート。必要に応じて lme4、ggplot2、Quarto、R Markdown などを利用 |
| 🐍 **[Python](https://www.python.org/)** | 一般的なデータ処理、統計分析、可視化、Jupyter ワークフロー |

### 分析手法

**60 の手法リファレンスと 48 のグラフ・リファレンス**は候補を探すための資料で、自動処方ではありません。今回の判断に影響する点を比較し、候補が本当に拮抗する場合や影響の大きい選択に限って完全な 12 次元比較を使います。

| カテゴリ | 手法例 |
|------|------|
| **平均比較** | 対応のある／ない t 検定、被験者内／間 ANOVA、混合 ANOVA、ANCOVA、MANOVA |
| **混合モデル** | 線形混合モデル（LMM）、ロジスティック混合モデル（GLMM）、Gamma GLMM、交差変量効果 |
| **媒介・調整** | 媒介分析、調整分析、調整付き媒介、構造方程式モデル |
| **回帰と縦断** | 重回帰、分位点回帰、成長曲線、交差遅延パネル、時系列 |
| **相関と分類** | Pearson/Spearman 相関、反復測定相関、カイ二乗検定、正準相関 |
| **ノンパラメトリックと頑健** | Wilcoxon、Friedman、並べ替え検定、ブートストラップ、頑健回帰 |
| **ベイズ** | ベイズ t 検定、ベイズ ANOVA、ベイズ混合モデル |
| **測定と尺度** | 信頼性分析（α/ω/ICC）、探索的／確認的因子分析、多次元尺度法 |
| **信号検出と診断** | d'、ROC 曲線、心理測定関数 |
| **RT と意思決定モデル** | Ex-Gaussian 分布、ドリフト拡散モデル（DDM） |
| **メタ分析と検出力** | メタ分析、検出力分析、同等性検定 |
| **特殊手法** | 多重代入、LASSO/Ridge、ネットワーク分析、クラスター分析、潜在クラス分析 |

---

## 🎬 デモ

### 🧪 実験 · PsychoPy Stroop

> 「Stroop 課題を作りたい。赤・緑・青の文字で、インクの色をキー押し判定。一致：不一致 = 50:50、2 ブロック各 60 試行」

```
ユーザー         ❯ Stroop 課題を作りたい

Amazing PsyCoder ❯ 🟢 Phase 1/5 · 診断
                   パラダイム Stroop · PsychoPy を使用しますか？

ユーザー         ❯ はい、PsychoPy で。

Amazing PsyCoder ❯ 🟢 Phase 2/5 · 試行ウィンドウ＋反応ルール（最重要）
                   インク色 赤・緑・青 → f=赤 j=緑 k=青。試行タイムライン：
                       Window 1: 注視点             Window 2: 刺激提示              Window 3: 空白     
                   ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
                   │                      │      │                      │      │                      │
                   │          +           │  →   │      赤色の「緑」    │  →   │                      │
                   │                      │      │                      │      │                      │
                   └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                            500ms                         2000ms                        500ms          
                           反応なし                     f / j / k                      反応なし        
                                                      ← RT 起点                                       

                        Window 4: フィードバック     
                   ┌──────────────────────┐
                   │                      │
                   │        正解！        │
                   │                      │
                   └──────────────────────┘
                            1000ms         
                           反応なし         
                   Gate 1 ✅ ウィンドウ完全、反応マッピング確認済

ユーザー         ❯ タイムラインとキーは問題なし。ITI 400-800ms ランダムで。

Amazing PsyCoder ❯ 🟢 Phase 3/5 · 条件表
                   一致：不一致 = 60：60 → 120 試行の条件表を生成。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 4/5 · ブロック構造
                   2 ブロック × 60 試行 · フィードバックは練習ブロックのみ。Gate 3 ✅

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最終審査
                   ┌──────────────────────────────────────────────┐
                   │ 設計決定レジストリ                            │
                   │ パラダイム Stroop · プラットフォーム PsychoPy ← ユーザー │
                   │ キー f/j/k · 一致：不一致 50:50      ← ユーザー │
                   │ ITI 400-800ms ランダム                ← ユーザー │
                   │ 試行タイムライン 4 ウィンドウ          ← 慣例   │
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ すべて確認 → コード生成へ

ユーザー         ❯ 生成して。

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md 生成完了
                   パラメータ先頭 · CJK フォント設定済 · 増分保存 → 監査へ自動ルーティング

Amazing PsyCoder ❯ 🔍 静的コード確認では重大な問題は見つかりませんでした。
                   収集用 PC で試行できますが、まだデータ収集は開始できません。

ユーザー         ❯ 起動・終了、短い全体実行、データ完全性、中断復旧を実機で確認しました。

Amazing PsyCoder ❯ 🔍 実行記録と保存データを確認しました。
                   準備状態：ready_for_collection
                   本番のデータ収集を開始できます。
```

### 📊 分析 · R Stroop

> 「Stroop データを分析して、一致条件と不一致条件の RT に有意差があるか見てほしい」

```
ユーザー         ❯ Stroop データを分析して、一致と不一致の RT に差があるか

Amazing PsyCoder ❯ 🟢 Phase 1/5 · 実験と科学的问题の理解
                   実験 config を提供するか、実験デザインを説明してください

ユーザー         ❯ 被験者内、IV: condition（一致／不一致）、DV: rt+acc。30 名

Amazing PsyCoder ❯ 🟢 Phase 2/5 · データ構造の理解
                   データはどう保存されていますか？被験者ごと？まとめて？

ユーザー         ❯ 被験者ごと 1 CSV、命名: sub-001_stroop.csv
                   列: subject_id, stimulus, condition, rt, acc, trial

Amazing PsyCoder ❯ stimulus は被験者ごとに異なりますか。それとも同じ刺激セットを
                   複数の被験者が見ますか？

ユーザー         ❯ 全員が同じ 60 個の色単語の組み合わせを見ます。
                   各被験者には反復試行があります。

Amazing PsyCoder ❯ 被験者内と刺激内の両方に反復があることを確認。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · まず推定対象を決め、その後に手法を選択
                   主な推定対象：母集団における「不一致 − 一致」の平均 RT 差。

                   RT の主モデル：
                   rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)

                   正答率は二項混合モデルによる補助分析にできます。
                   対応のある t 検定は簡単ですが、被験者平均に集約した問いになります。
                   変量効果を安定して推定できない場合は、事前に決めた順で簡略化し、
                   診断結果を報告します。

ユーザー         ❯ 推定対象、式、被験者／刺激の階層を確認します。
                   RT は混合モデル、正答率は補助分析にしてください。

Amazing PsyCoder ❯ Gate 3 ✅ 推定対象、式、階層、代替案を確認

Amazing PsyCoder ❯ 🟢 Phase 4/5 · クリーニング、実行環境、出力
                   課題仕様または事前登録にある RT、欠測、除外ルールを確認します。
                   根拠なしに固定閾値や SD ルールを自動挿入しません。

ユーザー         ❯ 事前登録では、RT 主分析は正答かつ RT が欠測でない試行のみ。
                   固定 RT 範囲、SD 除外、被験者の自動除外は行いません。
                   log-RT 感度分析も行います。研究室環境は R 4.4.1、
                   renv.lock、R Markdown です。

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最終審査
                   ┌──────────────────────────────────────────────┐
                   │ 分析決定レジストリ                            │
                   │ 科学的问题: 一致 vs 不一致 RT      ← ユーザー │
                   │ 式：被験者ランダム傾き＋刺激ランダム切片        │
                   │ クリーニング：事前登録ルールと各段階の件数記録  │
                   │ 環境：R 4.4.1 + renv.lock          ← ユーザー │
                   │ 出力：差、区間、診断、図              ← ユーザー │
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ analysis_config.yaml 保存 → コード生成へ

ユーザー         ❯ 生成して。

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd + renv.lock 生成完了
                   依存バージョンを記録し、静的コード確認を完了

Amazing PsyCoder ❯ 🔍 準備状態：ready_for_execution
                   コードは実行できますが、結果を論文に使える段階ではありません。

ユーザー         ❯ クリーン環境で実行し、ログ、表、図、バージョン情報を用意しました。

Amazing PsyCoder ❯ 🔍 実行結果を確認しました。
                   準備状態：ready_for_publication
```

---

## 📂 ファイル構造

```text
amazing-psycoder-skills/
├── amazing-psycoder/                  ← メイン入口（v1.4.0）
│   ├── SKILL.md                       ← ルーティングと全体ルール
│   ├── PLATFORMS.md · install.sh      ← プラットフォーム説明とインストーラー
│   ├── STANDALONE.md                  ← Agent 内で直接利用
│   ├── PSYCODER_STUDIO.md             ← Web サイト統合
│   ├── runtime/                       ← Web 用ルールと機能範囲
│   ├── scripts/ · tests/              ← 自動チェック
│   ├── requirements-dev.txt           ← 検証用依存バージョン
│   │
│   │   # 🧪 実験プログラミング
│   ├── psy-exp-designer/              ← ① 実験設計（5 段階 + 38 の設計資料）
│   ├── psy-exp-coder/                 ← ② 実験コード生成（PsychoPy/jsPsych/Psychtoolbox）
│   └── psy-exp-reviewer/              ← ③ 実験コード確認
│   │
│   │   # 📊 データ分析
│   ├── psy-ana-designer/              ← ④ 分析設計（60 手法 + 48 図表の資料）
│   ├── psy-ana-coder/                 ← ⑤ 分析コード生成（R/Python）
│   └── psy-ana-reviewer/              ← ⑥ 分析コードと出力の確認
│
├── docs/                              ← 翻訳 README（繁/英/日/独/仏）
├── .github/                           ← 自動テスト
└── README.md                          ← 簡体字中国語のトップページ
```

---

<div align="center">

💡 ご意見・ご提案がございましたら、こちらまでご連絡ください：[tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
