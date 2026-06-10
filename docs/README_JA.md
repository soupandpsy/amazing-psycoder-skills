<div align="center">

# 🧠 Amazing PsyCoder 💻

> 心理学研究におけるコーディングの壁を完全になくす。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
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

<table>
<tr><td align="left">

🔬 &nbsp;アイデアを実験プログラムにするには、まず Python や JavaScript、MATLAB を学ばなければならない。<br>
📦 &nbsp;研究室の先輩から引き継いだコードが別の PC で動かない——依存関係も誰も把握しておらず、ロジックにも手を付けられない。<br>
📊 &nbsp;統計手法は習慣で選んでいる——「みんな ANOVA を使っているから」。査読者に問われれば、また最初からやり直し。<br>
🔁 &nbsp;分析結果は自分の環境でしか再現できない。環境や乱数シードが変われば、結論も変わりうる。<br>
✂️ &nbsp;実験を作る人と分析する人が別——データを集め終わってから「設計段階で分析まで考えていなかった」と気づく。<br>
📝 &nbsp;投稿時に再現可能性の宣誓を求められるが、コードは監査も記録も、独立した検証もされていない。

</td></tr>
</table>

### ✨ Amazing PsyCoder は、まさにこれを解決します。

Python を書けなくても、統計に詳しくなくても大丈夫。あなたは実験のアイデアとデータを持ち込むだけでいい——そこから先は、設計の確認、コードの生成、監査までを段階的にサポートします。最終的に届くコードはそのまま実行でき、分析結果は査読者にも通用するものになります。

---

## 📖 なぜこのプロジェクトなのか

心理学の研究者がアイデアを持ってから、実際にデータを取り、結果を出すまで——その道のりで最も時間を取られるのは、たいてい次の二つです。

**一つ目：実験プログラミング。** 仮説を検証するには、まず実験をプログラムしなければなりません。PsychoPy の Builder では柔軟性が足りず、Coder を使うには Python が必要。jsPsych なら JavaScript とタイムラインロジック、Psychtoolbox なら MATLAB とフレーム同期——「RT の計測起点はどの画面か」「キーマッピングが逆転していないか」「クラッシュしてもデータが残る保存方法は」——こうした問題を一つひとつ潰すだけで何週間も溶けていきます。アイデアが頭の中から動くコードになるまでに、実験そのものを考えるより多くの時間がかかることも珍しくありません。

**二つ目：データ分析。** データは集めた。では、どの統計手法を使うべきか？被験者内計画に paired t か混合モデルか？正答率が天井に近いとき ANOVA は妥当か？査読者に「なぜこの手法を選んだのか」と問われたとき、どう説明するか？別の PC でも同じ結果が出るという確信はあるか？

これは能力の問題ではありません。適切な道具がなかっただけです。コードを書くことも分析することも、研究を前に進めるためのものであって、立ち止まる理由になるべきではない。

Amazing PsyCoder は、実験プログラミングとデータ分析の知見を 7 つのスキルにエンコードしました——1 つのオーケストレーターと 6 つのサブスキル。agentskills.io のオープン標準に準拠し、Claude Code / Codex / Hermes / OpenClaw に対応しています。

研究そのものに、時間を返しましょう。

---

## 👥 対象者

- 🎓 これから実験コードを書く（あるいは今まさに書いている）心理学の学部生・大学院生
- 🧠 認知・行動・社会心理学の実験を行っている研究者
- 😵‍💫 RT、ランダム化、条件表で何度もつまずいてきた——実験コードの品質保証がほしい
- 📊 データを集めたあと、どの統計手法を使えばいいか確信が持てず、体系的な分析計画を求めている
- 📝 投稿前に分析の再現性を確認したい——第三者による監査が必要
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB ユーザー

---

## ⚡ インストール

AI チャットに直接、お使いのプラットフォームのコマンドを入力してください：

**Claude Code**

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/amazing-psycoder-skills
```

**Codex**

```
$skill-installer
```

リポジトリ URL を入力：`https://github.com/soupandpsy/amazing-psycoder-skills`

**Hermes**

```
hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills
```

**OpenClaw**

```
npm i -g clawhub && clawhub install amazing-psycoder
```

インストール後、`/amazing-psycoder` で起動します。

<details>
<summary><b>ターミナルからのインストール（全プラットフォーム共通）</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
./install.sh           # プラットフォームを自動検出してインストール
# または手動指定: ./install.sh claude | codex | hermes | openclaw
```

</details>

---

## 🚀 クイックスタート

インストール後、`/amazing-psycoder` と入力し、やりたいことをそのまま説明してください：

> 「Stroop 課題を作りたい。赤・緑・青、キー押し反応」→ 自動的に実験設計へ

> 「Stroop データを分析して、一致と不一致の RT に差があるか見て」→ 自動的に分析設計へ

どのスキルを使うか指定する必要はありません——オーケストレーターがあなたのニーズに応じて自動判定します。その後、スキルが段階的にガイドします：設計の確認、手法の選択、コードの生成、監査チェック。あなたは質問に答えるだけです。

---

## 🧪 実験プログラミング

アイデアからデータ収集可能な実験コードまで、三つのステップ——設計、生成、監査。

### スキル

| # | スキル | 役割 | ポイント |
|---|------|------|---------|
| ① | **設計** `psy-exp-designer` | 実験アイデアを完全な設計仕様にまとめる | 5 段階の段階的確認。Phase 2 で試行ウィンドウのタイムライン図を生成。各画面の持続時間・キー・RT 起点が一目でわかる。5 つの Gate チェックポイント。38 パラダイム参照 |
| ② | **コード生成** `psy-exp-coder` | 設計仕様から実行可能なコードを生成 | 4 層優先度アーキテクチャ。9 項目の品質ゲートが自動チェック——`time.sleep()` や `KbCheck` で RT 計測しているコードは即時拒否。12 ステップのコードテンプレート、パラメータはファイル先頭に集約 |
| ③ | **コード監査** `psy-exp-reviewer` | 本番収集前の最終チェック | 5 種の監査モード。スモークテストプロトコル。パラダイム別の失敗モードチェック。不合格時は修正パスを提示。合格ラベル：`ready_for_collection` |

### プラットフォーム

| プラットフォーム | 特徴 |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Python エコシステム。USB HID ハードウェアタイムスタンプ、ミリ秒精度の RT 計測。ローカル実験の第一選択 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | JavaScript エコシステム。ブラウザさえあれば動作、インストール不要。オンライン実験の第一選択 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | MATLAB エコシステム。GPU レベルのフレーム精密制御。厳密なタイミング精度が求められる場合の第一選択 |

### パラダイムカバレッジ

**38 パラダイム**。各パラダイムは統一されたメタロジックで整理されています：使用する場面 → コアロジック → 確認必須項目 → 仮定してはいけないこと → 試行ウィンドウタイムライン → 条件表 → データ分析 → バリエーションと参考文献。

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

データを集めた後も、同じく三つのステップ——分析計画の設計、コード生成、再現性の監査。

### スキル

| # | スキル | 役割 | ポイント |
|---|------|------|---------|
| ④ | **分析設計** `psy-ana-designer` | 科学的问题から出発し、完全な分析計画を設計 | 5 段階の段階的確認。Phase 2 でデータファイルの構成を確認（ファイル分割／統合、命名規則、CSV/Excel/TSV）。Phase 3 では 12 次元の比較により最適な手法を選択。Config YAML が唯一のファクトソース |
| ⑤ | **分析コード** `psy-ana-coder` | 分析計画から再現可能なスクリプトを生成 | Phase 0 で config を検証 → R/Python を確認 → 12 ステップで生成。10 項目の品質ゲート。R：tidyverse/lme4/ggplot2。Python：pandas/statsmodels/seaborn。すべて config 駆動 |
| ⑥ | **分析監査** `psy-ana-reviewer` | 発表前の最終チェック | 4 種の監査モード。データ取り込みプロトコルの自動検出。統計的正しさ＋再現性＋仮説検定の審査。R/Python 両プラットフォームのアンチパターンチェック。不合格時は修正パスを提示。合格ラベル：`ready_for_publication` |

### プラットフォーム

| プラットフォーム | 特徴 |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | 統計計算の標準。tidyverse + lme4 + ggplot2 + RMarkdown。学術出版の第一選択 |
| 🐍 **[Python](https://www.python.org/)** | 汎用科学計算。pandas + statsmodels + seaborn + Jupyter。再現可能な分析 |

### 分析手法

**60 の分析手法、48 のチャートタイプ**。各手法の選択は 12 次元の比較に基づきます：統計的検出力 · 偽陽性制御 · データ利用率 · 外れ値感度 · 仮定の頑健性 · 解釈可能性 · 分野での受容度 · 効果量の比較可能性 · 再現性 · 拡張性 · サンプルサイズ制約 · 計算実現可能性。

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

Amazing PsyCoder ❯ 🔍 監査合格 · 準備状態：ready_for_collection
                   データ収集を開始できます。
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
                   列: subject_id, condition, rt, acc, trial

Amazing PsyCoder ❯ 確認済：30 被験者 × 各 1 ファイル。Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · データ特性＋手法マッチング（中核段階）
                   RT に右裾の偏りは？正答率は天井付近？

ユーザー         ❯ RT はやや右裾、正答率は 95% くらい

Amazing PsyCoder ❯ 正答率が天井付近 → glmer(binomial) で acc 分析
                   RT について、12 次元で A と B を比較：

                   ┌────────────┬───────────────────┬───────────────────┐
                   │ 次元       │ A: 対応のある t   │ B: 線形混合モデル  │
                   ├────────────┼───────────────────┼───────────────────┤
                   │ 統計的検出力│ 30 点（被験者平均）│ 1800 点（全試行）  │
                   │ データ利用率│ 被験者ごと 1 点に圧縮│ 全試行が参加    │
                   │ 拡張性     │ 共変量追加は再計算  │ 式に + するだけ   │
                   │ 解釈性     │ d=0.5 誰でもわかる │ 変量効果の説明必要 │
                   └────────────┴───────────────────┴───────────────────┘

                   検出力と拡張性を重視 → B。シンプルさ重視 → A。

ユーザー         ❯ B で

Amazing PsyCoder ❯ Gate 3 ✅ 手法選択済（12 次元比較の理由付き）

Amazing PsyCoder ❯ 🟢 Phase 4/5 · 分析詳細
                   クリーニング: RT 150-2000ms · 正答試行 · 被験者 acc<60% 除外
                   · ±2.5 SD 試行除外 · チャート: 雨雲プロット＋個人線 ⚠️

ユーザー         ❯ 確認

Amazing PsyCoder ❯ 🟢 Phase 5/5 · 最終審査
                   ┌──────────────────────────────────────────────┐
                   │ 分析決定レジストリ                            │
                   │ 科学的问题: 一致 vs 不一致 RT      ← ユーザー │
                   │ 手法: lmer（ユーザーが B 選択）    ← ユーザー │
                   │ RT 150-2000ms · 被験者 acc<60%     ← デフォルト ⚠️│
                   │ チャート: 雨雲＋個人線             ← デフォルト ⚠️│
                   └──────────────────────────────────────────────┘
                   Gate 5 ✅ analysis_config.yaml 保存 → コード生成へ

ユーザー         ❯ 生成して。

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd 生成完了
                   Config 駆動 · 10 項目品質ゲート · 12 ステップ構成 → 監査へ自動ルーティング

Amazing PsyCoder ❯ 🔍 監査合格 · 準備状態：ready_for_publication
```

---

## 📂 ファイル構造

```
amazing-psycoder-skills/
├── amazing-psycoder/                  ← オーケストレーター（システムエントリポイント、v1.3）
│   ├── SKILL.md · PLATFORMS.md · install.sh
│   │
│   │   # 🧪 実験プログラミング
│   ├── psy-exp-designer/              ← ① 実験設計（5 段階 + 38 パラダイム + 9 参照ファイル）
│   ├── psy-exp-coder/                 ← ② 実験コード生成（PsychoPy/jsPsych/Psychtoolbox）
│   └── psy-exp-reviewer/              ← ③ 実験監査（5 モード + スモークテスト + リカバリーループ）
│   │
│   │   # 📊 データ分析
│   ├── psy-ana-designer/              ← ④ 分析設計（5 段階 + 60 手法 + 48 チャート）
│   ├── psy-ana-coder/                 ← ⑤ 分析コード生成（R/Python 両対応）
│   └── psy-ana-reviewer/              ← ⑥ 分析監査（4 モード + 取り込みプロトコル + リカバリーループ）
│
├── docs/                              ← 多言語 README（簡/繁/英/日/独/仏）
└── README.md
```

---

<div align="center">

💡 ご意見・ご提案がございましたら、こちらまでご連絡ください：[tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
