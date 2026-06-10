<div align="center">

# 🧠 Amazing PsyCoder 💻

> Faites disparaître complètement la barrière du code dans la recherche en psychologie.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-green)](https://github.com/openai/codex)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-red)](https://github.com/openclaw/openclaw)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-333)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/soupandpsy/amazing-psycoder-skills?style=social)](https://github.com/soupandpsy/amazing-psycoder-skills)

[**简体中文**](../README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 Pourquoi](#-pourquoi-ce-projet) · [👥 Public](#-public) · [⚡ Installation](#-installation) · [🚀 Démarrage rapide](#-démarrage-rapide) · [🧪 Programmation d'expériences](#-programmation-dexpériences) · [📊 Analyse de données](#-analyse-de-données) · [🎬 Démo](#-démo) · [📂 Structure](#-structure-des-fichiers)

</div>

<br>

<table>
<tr><td align="center">

🔬 &nbsp;Pour transformer une idée en expérience capable de collecter des données, il faut d'abord apprendre Python, JavaScript ou MATLAB.<br>
📦 &nbsp;Le code hérité du labo ne tourne plus dès qu'on change d'ordinateur — personne ne sait quelles dépendances installer, personne n'ose toucher à la logique.<br>
📊 &nbsp;On choisit ses statistiques par habitude — « tout le monde utilise l'ANOVA » — et une remarque de reviewer suffit à tout recommencer.<br>
🔁 &nbsp;Les résultats ne sortent que sur votre machine : changez d'environnement ou de graine aléatoire, et les conclusions changent.<br>
✂️ &nbsp;Ceux qui programment l'expérience et ceux qui l'analysent ne sont souvent pas les mêmes — on récolte les données pour découvrir que l'analyse n'a pas été pensée en amont.<br>
📝 &nbsp;Le journal exige une déclaration de reproductibilité, mais le code n'a jamais été audité, documenté, ni vérifié par un tiers.

</td></tr>
</table>

<div align="center">

### ✨ C'est exactement ce que résout Amazing PsyCoder.

Pas besoin de savoir programmer, pas besoin d'être statisticien. Vous apportez vos idées et vos données — il vous guide pas à pas pour confirmer le design, générer le code, et auditer le résultat. Le code que vous obtenez est prêt à lancer, et vos analyses tiennent face aux reviewers les plus exigeants.

</div>

---

## 📖 Pourquoi ce projet

Pour un chercheur en psychologie, deux choses prennent un temps démesuré entre le moment où l'idée germe et celui où les résultats sont prêts à publier.

**La première : programmer l'expérience.** Vous voulez tester une hypothèse, il faut d'abord coder la tâche. PsychoPy Builder n'est pas assez flexible, PsychoPy Coder demande d'apprendre Python ; jsPsych demande JavaScript et sa logique de timeline ; Psychtoolbox demande MATLAB et la synchronisation d'images. Définir correctement « à partir de quel écran on mesure le TR », « comment mapper les touches sans les inverser », « comment sauvegarder les données sans tout perdre au moindre crash » — rien que ça, c'est des semaines. Le temps passé entre l'idée et le premier lancement dépasse souvent celui consacré à la conception même de l'expérience.

**La deuxième : analyser les données.** Les données sont là — mais quelle méthode choisir ? Un test t apparié ou un modèle mixte pour un plan intra-sujets ? L'ANOVA tient-elle quand la précision est proche du plafond ? Que répondre au reviewer qui demande « pourquoi cette méthode » ? Et si on change d'ordinateur, est-ce que le script tourne encore ?

Ce n'est pas une question de compétence — c'est une question d'outils. Coder et analyser devraient faciliter la recherche, pas la freiner.

Amazing PsyCoder encode l'expérience accumulée en programmation d'expériences et en analyse de données dans 7 skills — 1 orchestrateur et 6 sous-skills, conformes au standard ouvert agentskills.io, compatibles avec Claude Code / Codex / Hermes / OpenClaw.

Pour que vous puissiez vous concentrer sur ce qui compte vraiment : la recherche.

---

## 👥 Public

- 🎓 Étudiants en psychologie, licence ou master, qui écrivent ou s'apprêtent à écrire du code d'expérience
- 🧠 Chercheurs en psychologie cognitive, comportementale ou sociale
- 😵‍💫 Ceux qui ont déjà buté sur des problèmes de TR, de randomisation ou de tableaux de conditions — et qui veulent une assurance qualité systématique
- 📊 Ceux qui ont des données mais hésitent sur la méthode statistique, et cherchent une démarche d'analyse structurée
- 📝 Ceux qui veulent confirmer la reproductibilité de leur analyse avant soumission — besoin d'un audit indépendant
- 🐍 Utilisateurs de PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB

---

## ⚡ Installation

Dans votre chat IA, tapez la commande correspondant à votre plateforme :

**Claude Code**

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/amazing-psycoder-skills
```

**Codex**

```
$skill-installer
```

Entrez l'URL du dépôt : `https://github.com/soupandpsy/amazing-psycoder-skills`

**Hermes**

```
hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills
```

**OpenClaw**

```
npm i -g clawhub && clawhub install amazing-psycoder
```

Une fois installé, tapez `/amazing-psycoder` pour démarrer.

<details>
<summary><b>Installation via le terminal (toutes plateformes)</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
./install.sh           # Détecte automatiquement votre plateforme
# ou précisez : ./install.sh claude | codex | hermes | openclaw
```

</details>

---

## 🚀 Démarrage rapide

Une fois installé, lancez `/amazing-psycoder` et décrivez ce que vous voulez faire :

> "Je veux créer une tâche Stroop, trois couleurs rouge/vert/bleu, réponse par touche" → lance automatiquement la conception d'expérience

> "Analyse mes données Stroop, y a-t-il une différence de TR entre congruent et incongruent ?" → lance automatiquement la conception d'analyse

Pas besoin de choisir quel skill utiliser — l'orchestrateur détermine automatiquement ce dont vous avez besoin. Ensuite, le skill vous guide pas à pas : confirmer le design, choisir la méthode, générer le code, auditer. Vous n'avez qu'à répondre aux questions qu'il vous pose.

---

## 🧪 Programmation d'expériences

De l'idée au code prêt pour la collecte, en trois étapes — concevoir, générer, auditer.

### Skills

| # | Skill | Ce qu'il fait | Détails clés |
|---|------|--------|---------|
| ① | **Conception** `psy-exp-designer` | Transforme votre idée en spécification complète de design | Confirmation progressive en 5 phases. La Phase 2 génère la timeline des fenêtres d'essai — durée de chaque écran, touches de réponse, point de départ du TR, tout est visuel. 5 portes de validation. 38 paradigmes de référence |
| ② | **Génération de code** `psy-exp-coder` | Produit le code exécutable à partir de la spécification | Architecture à 4 niveaux de priorité. 9 portes qualité automatiques : `time.sleep()`, `KbCheck` pour le TR sont rejetés sans appel. Template en 12 étapes, paramètres en haut du fichier |
| ③ | **Audit de code** `psy-exp-reviewer` | Dernière vérification avant la collecte | 5 modes de revue. Protocole de test de fumée. Vérification des modes de défaillance par paradigme. Si ça ne passe pas, le chemin de correction est indiqué. Label final : `ready_for_collection` |

### Plateformes

| Plateforme | Particularités |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Écosystème Python, timestamps matériels USB HID, précision du TR à la milliseconde. Premier choix pour le laboratoire |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | Écosystème JavaScript, le navigateur comme environnement d'exécution, aucune installation. Premier choix pour les expériences en ligne |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | Écosystème MATLAB, contrôle image par image au niveau GPU. Quand la précision temporelle est critique |

### Paradigmes couverts

**38 paradigmes**, chacun organisé selon une même logique : Quand l'utiliser → Logique centrale → À confirmer absolument → Ne pas supposer → Timeline des fenêtres d'essai → Tableau de conditions → Analyse de données → Variantes et références.

| Catégorie | Paradigmes |
|------|------|
| 🎯 **Attention et contrôle inhibiteur** | Stroop · Eriksen Flanker · Simon · Go/No-go · Stop-signal · ANT · Posner Cuing · Visual Search · Dot-probe · Navon · CPT · Antisaccade |
| 🧠 **Mémoire et mémoire de travail** | N-back · Sternberg · Corsi Blocks · Change Detection · Drag and Drop |
| 🔄 **Fonctions exécutives et flexibilité cognitive** | Task Switching · WCST · Choice RT |
| 👥 **Cognition sociale et émotion** | Cyberball · Climate Reflection · Phone a Friend · Rating · Priming · IAT · EAST |
| 💰 **Décision et récompense** | BART · Delay Discounting · Rating to Choice · Ultimatum Game |
| 👁️ **Perception et psychophysique** | Psychophysics Staircase · Multisensory Nature · Mental Rotation |
| 🌱 **Développement et différences individuelles** | Children Flanker · Bilingual Stroop · Numerical Stroop · Writing Distraction |

---

## 📊 Analyse de données

Une fois les données collectées, même logique en trois étapes — concevoir le plan d'analyse, générer le code, auditer la reproductibilité.

### Skills

| # | Skill | Ce qu'il fait | Détails clés |
|---|------|--------|---------|
| ④ | **Conception d'analyse** `psy-ana-designer` | Part de la question scientifique pour concevoir un plan d'analyse complet | Confirmation progressive en 5 phases. La Phase 2 vérifie l'organisation des fichiers (un par participant ou consolidé, règle de nommage, CSV/Excel/TSV). La Phase 3 compare les méthodes sur 12 dimensions pour choisir la plus adaptée. Le fichier config YAML sert de source unique de vérité |
| ⑤ | **Code d'analyse** `psy-ana-coder` | Génère le script reproductible à partir du plan d'analyse | Phase 0 : validation de la config → confirmation R ou Python → génération du script en 12 étapes. 10 portes qualité. R : tidyverse/lme4/ggplot2. Python : pandas/statsmodels/seaborn. Tout est piloté par la config |
| ⑥ | **Audit d'analyse** `psy-ana-reviewer` | Dernière vérification avant publication | 4 modes de revue. Protocole d'ingestion automatique. Audit de la justesse statistique + reproductibilité + vérification des hypothèses. Détection des anti-patterns R et Python. Si ça ne passe pas, le chemin de correction est indiqué. Label final : `ready_for_publication` |

### Plateformes

| Plateforme | Particularités |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | Le standard du calcul statistique. tidyverse + lme4 + ggplot2 + RMarkdown. Premier choix pour la publication académique |
| 🐍 **[Python](https://www.python.org/)** | Calcul scientifique généraliste. pandas + statsmodels + seaborn + Jupyter. Pour des analyses reproductibles |

### Méthodes d'analyse

**60 méthodes d'analyse, 48 types de graphiques**. Chaque méthode est évaluée sur 12 dimensions : puissance statistique · contrôle des faux positifs · utilisation des données · sensibilité aux valeurs aberrantes · robustesse des hypothèses · interprétabilité · acceptation dans le domaine · comparabilité des tailles d'effet · reproductibilité · extensibilité · contrainte de taille d'échantillon · faisabilité computationnelle.

| Catégorie | Exemples |
|------|------|
| **Comparaison de moyennes** | Test t apparié/indépendant, ANOVA intra/inter-sujets, ANOVA mixte, ANCOVA, MANOVA |
| **Modèles mixtes** | Modèle linéaire mixte (LMM), GLMM logistique, Gamma GLMM, effets aléatoires croisés |
| **Médiation et modération** | Analyse de médiation, analyse de modération, médiation modérée, modèles d'équations structurelles |
| **Régression et longitudinal** | Régression multiple, régression quantile, courbes de croissance, panels croisés décalés, séries temporelles |
| **Corrélation et classification** | Corrélation Pearson/Spearman, corrélation mesures répétées, test du chi-carré, corrélation canonique |
| **Non-paramétrique et robuste** | Wilcoxon, Friedman, tests de permutation, Bootstrap, régression robuste |
| **Bayésien** | Test t bayésien, ANOVA bayésienne, modèle mixte bayésien |
| **Mesure et échelles** | Analyse de fiabilité (α/ω/ICC), analyse factorielle exploratoire/confirmatoire, échelonnement multidimensionnel |
| **Détection du signal et diagnostic** | d', courbes ROC, fonctions psychométriques |
| **Modélisation du TR et de la décision** | Distribution Ex-Gaussienne, modèle de diffusion (DDM) |
| **Méta-analyse et puissance** | Méta-analyse, analyse de puissance, test d'équivalence |
| **Méthodes spécialisées** | Imputation multiple, LASSO/Ridge, analyse de réseaux, analyse de clusters, analyse de classes latentes |

---

## 🎬 Démo

### 🐍 PsychoPy — Tâche de Stroop

> "Je veux une tâche Stroop, texte rouge/vert/bleu, juger la couleur d'encre, 50:50 congruent:incongruent, 2 blocs × 60 essais"

```
Utilisateur      ❯ Je veux une tâche Stroop

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Diagnostic
                   Paradigme Stroop · Confirmer PsychoPy ?

Utilisateur      ❯ Oui, PsychoPy.

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Fenêtres d'essai + Règles de réponse (critique)
                   Couleurs d'encre → f=rouge j=vert k=bleu. Timeline :
                      Window 1: Fixation            Window 2: Stimulus             Window 3: Pause     
                   ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
                   │                      │      │                      │      │                      │
                   │          +           │  →   │     Rouge (vert)     │  →   │                      │
                   │                      │      │                      │      │                      │
                   └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                            500ms                         2000ms                        500ms          
                         pas de rép.                   f / j / k                    pas de rép.      
                                                     ← Début du TR                                   

                      Window 4: Feedback   
                   ┌──────────────────────┐
                   │                      │
                   │      Correct !       │
                   │                      │
                   └──────────────────────┘
                            1000ms         
                         pas de rép.      
                   Gate 1 ✅ Fenêtres complètes, mapping de réponse confirmé

Utilisateur      ❯ Timeline et touches OK. ITI 400-800ms aléatoire.

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Conditions
                   Congruent:incongruent = 60:60 → Table de 120 essais générée
                   Gate 2 ✅ Colonnes de condition remplies

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Blocs
                   2 blocs × 60 essais · Feedback en pratique seulement
                   Gate 3 ✅ Config zéro [MISSING]

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Revue finale
                   ┌──────────────────────────────────────────────────────────┐
                   │ Registre des Décisions de Conception                     │
                   │ Paradigme Stroop · Plateforme PsychoPy  ← utilisateur    │
                   │ Touches f/j/k · 50:50 congruent         ← utilisateur    │
                   │ ITI 400-800ms aléatoire                 ← utilisateur    │
                   │ Timeline essai 4 fenêtres               ← convention     │
                   └──────────────────────────────────────────────────────────┘
                   Gate 5 ✅ Tout confirmé → Routage vers la génération

Utilisateur      ❯ Générer.

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md généré
                   Params en haut · Police CJK configurée · Sauvegarde incrémentielle
                   → Routage automatique vers l'audit

Amazing PsyCoder ❯ 🔍 Audit réussi · État : ready_for_collection
                   Prêt pour la collecte de données.
```

### 📊 R — Analyse des données Stroop

> "Analyse mes données Stroop, différence de TR entre congruent et incongruent ?"

```
Utilisateur      ❯ Analyse mes données Stroop, TR congruent vs incongruent

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Comprendre l'expérience et la question scientifique
                   Fournissez la config d'expérience ou décrivez le plan

Utilisateur      ❯ Intra-sujets, VI: condition(congruent/incongruent), VD: tr+acc. 30 participants

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Comprendre la structure des données
                   Comment sont stockées les données ? Un fichier par participant ou consolidé ?

Utilisateur      ❯ Un CSV par participant, nommé sub-001_stroop.csv
                   Colonnes: subject_id, condition, rt, acc, trial

Amazing PsyCoder ❯ Confirmé : 30 participants × 1 fichier chacun. Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Caractéristiques des données + méthodes
                   TR asymétrique à droite ? Précision proche du plafond ?

Utilisateur      ❯ TR un peu asymétrique, précision autour de 95%

Amazing PsyCoder ❯ Précision proche du plafond → glmer(binomial) pour l'analyse d'acc
                   Pour le TR, comparaison 12 dimensions A vs B :

                   ┌────────────┬─────────────────────┬──────────────────────┐
                   │ Dimension  │ A: Test t apparié   │ B: Modèle mixte      │
                   ├────────────┼─────────────────────┼──────────────────────┤
                   │ Puissance  │ 30 points (moy par S)│ 1800 points (essais) │
                   │ Util. données│ Compressé 1 pt/S   │ Tous les essais      │
                   │ Extensibilité│ Ajout covariable →  │ Ajouter + dans formule│
                   │ Interprét.  │ d=0.5 compréhensible│ Expliquer effets aléa.│
                   └────────────┴─────────────────────┴──────────────────────┘

                   Priorité puissance et extensibilité → B. Priorité simplicité → A.

Utilisateur      ❯ B

Amazing PsyCoder ❯ Gate 3 ✅ Méthode choisie (avec justification 12 dimensions)

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Détails d'analyse
                   Nettoyage: TR 150-2000ms · essais corrects · S acc<60% exclus
                   · ±2.5 SD essais exclus · Graphiques: raincloud + lignes individuelles ⚠️

Utilisateur      ❯ Confirmer

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Revue finale
                   ┌──────────────────────────────────────────────────────────┐
                   │ Registre des Décisions d'Analyse                         │
                   │ Question: congruent vs incongruent TR     ← utilisateur   │
                   │ Méthode: lmer (utilisateur a choisi B)    ← utilisateur   │
                   │ TR 150-2000ms · S acc<60% exclus          ← défaut ⚠️     │
                   │ Graphiques: raincloud + lignes indiv.     ← défaut ⚠️     │
                   └──────────────────────────────────────────────────────────┘
                   Gate 5 ✅ Sauvegarde analysis_config.yaml → Routage code

Utilisateur      ❯ Générer.

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd généré
                   Piloté par config · 10 points qualité · Structure script 12 étapes
                   → Routage automatique vers l'audit d'analyse

Amazing PsyCoder ❯ 🔍 Audit réussi · État : ready_for_publication
```

---

## 📂 Structure des fichiers

```
amazing-psycoder-skills/
├── amazing-psycoder/                  ← Orchestrateur (point d'entrée système, v1.3)
│   ├── SKILL.md · PLATFORMS.md · install.sh
│   │
│   │   # 🧪 Programmation d'expériences
│   ├── psy-exp-designer/              ← ① Conception (5 phases + 38 paradigmes + 9 fichiers de référence)
│   ├── psy-exp-coder/                 ← ② Génération de code (PsychoPy/jsPsych/Psychtoolbox)
│   └── psy-exp-reviewer/              ← ③ Audit (5 modes + test de fumée + boucle de correction)
│   │
│   │   # 📊 Analyse de données
│   ├── psy-ana-designer/              ← ④ Conception d'analyse (5 phases + 60 méthodes + 48 graphiques)
│   ├── psy-ana-coder/                 ← ⑤ Génération de code d'analyse (R/Python)
│   └── psy-ana-reviewer/              ← ⑥ Audit d'analyse (4 modes + protocole d'ingestion + boucle de correction)
│
├── docs/                              ← READMEs multilingues (简/繁/EN/JA/DE/FR)
└── README.md
```

---

<div align="center">

💡 Une idée ou une suggestion ? Écrivez-nous à [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
