<div align="center">

# 🧠 Amazing PsyCoder 💻

> Pour que les chercheurs en psychologie se concentrent davantage sur leurs questions de recherche que sur le code.

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

[📖 Pourquoi](#-pourquoi-ce-projet) · [👥 Public](#-public) · [⚡ Installation](#-installation) · [🚀 Démarrage rapide](#-démarrage-rapide) · [🧪 Programmation d'expériences](#-programmation-dexpériences) · [📊 Analyse de données](#-analyse-de-données) · [🎬 Démo](#-démo) · [📂 Structure](#-structure-des-fichiers)

</div>

<br>

## 📖 Pourquoi ce projet

<h3 align="center">🔍 Difficultés courantes de la conception de l'étude à l'analyse des données</h3>

🔬 Transformer une question de recherche en expérience capable de collecter des données demande souvent de maîtriser Python, JavaScript ou MATLAB.<br>
📦 Le code déjà présent dans un laboratoire peut cesser de fonctionner lorsque l'environnement change ; ses dépendances et sa logique centrale sont aussi parfois difficiles à maintenir.<br>
📊 Lorsqu'une méthode statistique est choisie surtout par habitude, il devient difficile d'expliquer son adéquation avec la question, le type de variable et la structure des données.<br>
🔁 Sans versions logicielles et dépendances documentées, une analyse peut être difficile à reproduire sur un autre ordinateur.<br>
✂️ Si la conception expérimentale et le plan d'analyse sont séparés, on peut découvrir après la collecte que le plan ne permet pas l'analyse prévue.

<h3 align="center">🧱 Deux difficultés principales dans la conduite d’une recherche</h3>

**Première difficulté : programmer l'expérience.** Tester une hypothèse demande de traduire le plan en programme. PsychoPy Builder peut manquer de souplesse pour certains plans complexes ; Coder demande Python, jsPsych demande JavaScript et la logique de timeline, et Psychtoolbox demande MATLAB ainsi que des connaissances en synchronisation d'affichage. Le début de mesure du TR, l'association des touches et la sauvegarde après une interruption doivent être définis explicitement et vérifiés séparément.

**Deuxième difficulté : analyser les données.** Le plan d'analyse devrait idéalement être préparé avant la collecte, puis mis en œuvre selon la structure réelle des données. Faut-il un test t apparié ou un modèle mixte pour un plan intra-sujets ? Comment modéliser une précision proche du plafond ? Comment justifier le choix de la méthode ? Le résultat est-il reproductible sur un autre ordinateur ? Ces décisions dépendent de l'objectif scientifique, de la hiérarchie des données et de l'environnement logiciel.

Ces difficultés concernent non seulement la programmation, mais aussi le plan d'étude, l'inférence statistique, la gestion des données et la reproductibilité.

<h3 align="center">✨ Comment Amazing PsyCoder vous accompagne</h3>

Vous pouvez commencer par une idée d'expérience, un plan existant ou des données déjà disponibles. Amazing PsyCoder vous aide progressivement à confirmer les règles de recherche, générer le code et rechercher les problèmes. Lorsque c'est nécessaire, vous fournissez encore les configurations, la description des données, les sources des règles d'exclusion et les journaux d'exécution. Une sortie d'IA seule n'est jamais considérée comme « prête pour la collecte » ou « prête pour publication » : l'expérience doit être testée sur la machine de collecte, et l'analyse doit réellement être exécutée puis examinée.

Amazing PsyCoder comprend 7 Skills—1 Skill d'entrée et 6 Skills spécialisés—et suit le standard ouvert [agentskills.io](https://agentskills.io). Il peut être installé dans quatre agents IA : Claude Code, Codex, Hermes et OpenClaw.

Pour que vous puissiez vous concentrer sur ce qui compte vraiment : la recherche.

---

## 👥 Public

- 🎓 Étudiants en psychologie, licence ou master, qui écrivent ou s'apprêtent à écrire du code d'expérience
- 🧠 Chercheurs en psychologie cognitive, comportementale ou sociale
- 😵‍💫 Chercheurs confrontés à des problèmes de TR, de randomisation ou de tableaux de conditions et souhaitant vérifier systématiquement les risques courants
- 📊 Ceux qui ont des données mais hésitent sur la méthode statistique, et cherchent une démarche d'analyse structurée
- 🐍 Utilisateurs de PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB

---

## ⚡ Installation

Utilisez de préférence l'installateur du dépôt. Il vérifie les 7 Skills avant toute modification et restaure les anciens fichiers si l'installation échoue.

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
```

**Claude Code**

```bash
./install.sh claude
```

Après l'installation, utilisez `/amazing-psycoder`. Dossier par défaut : `${CLAUDE_CONFIG_DIR:-~/.claude}/skills`.

**Codex**

```bash
./install.sh codex
```

Après l'installation, utilisez `$amazing-psycoder`. Dossier par défaut : `~/.agents/skills`.

**Hermes**

```bash
./install.sh hermes
```

Après l'installation, utilisez `/amazing-psycoder`. Dossier par défaut : `~/.hermes/skills`.

**OpenClaw**

```bash
./install.sh openclaw
```

Après l'installation, décrivez la tâche et laissez l'agent OpenClaw associer le Skill. Dossier par défaut : `~/.openclaw/skills`.

<details>
<summary><b>Installation par projet et vérification</b></summary>

<br>

```bash
./install.sh --scope project --project-dir /path/to/repo claude
./install.sh --scope project --project-dir /path/to/repo codex
./install.sh --scope project --project-dir /path/to/workspace openclaw
./install.sh --check codex
```

Hermes ne dispose pas encore d'un dossier de Skill stable au niveau projet ; seule l'installation utilisateur est proposée. Voir [`PLATFORMS.md`](../amazing-psycoder/PLATFORMS.md).

</details>

---

## 🚀 Démarrage rapide

Une fois l'installation terminée, invoquez Amazing PsyCoder dans l'agent IA concerné et décrivez ce que vous voulez faire :

> "Je veux créer une tâche Stroop, trois couleurs rouge/vert/bleu, réponse par touche" → lance automatiquement la conception d'expérience

> "Analyse mes données Stroop, y a-t-il une différence de TR entre congruent et incongruent ?" → lance automatiquement la conception d'analyse

> "Vérifie ce code d'expérience, notamment le début du TR et la sauvegarde" → lance automatiquement la revue du code

Il n'est généralement pas nécessaire de choisir un Skill spécialisé. Le Skill d'entrée sélectionne la conception, la génération de code ou la revue selon la demande. S'il ne peut pas déterminer si vous souhaitez créer une expérience ou analyser des données, il demande d'abord une précision.

---

## 🧪 Programmation d'expériences

De l'idée au code prêt pour un essai, en trois étapes — concevoir, générer, vérifier.

### Skills

| # | Skill | Ce qu'il fait | Détails clés |
|---|------|--------|---------|
| ① | **Conception** `psy-exp-designer` | Transforme votre idée en spécification complète de design | Confirmation progressive en 5 phases. La Phase 2 génère la timeline des fenêtres d'essai — durée de chaque écran, touches de réponse, point de départ du TR, tout est visuel. 5 portes de validation. 38 paradigmes de référence |
| ② | **Génération de code** `psy-exp-coder` | Produit le code exécutable à partir de la spécification | Architecture à 4 niveaux de priorité. Avant livraison, 10 contrôles vérifient le timing, les réponses, la sauvegarde, le nettoyage, les dépendances et les autres risques bloquants |
| ③ | **Revue du code** `psy-exp-reviewer` | Compare le code au plan confirmé | Sans essai enregistré sur la machine de collecte, aucune autorisation de collecter n'est annoncée |

### Plateformes

| Plateforme | Particularités |
|------|------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Expériences Python en laboratoire ; le timing doit être validé sur la machine cible |
| 🌐 **[jsPsych](https://www.jspsych.org/)** | Expériences web ou en ligne ; test nécessaire sur les navigateurs et appareils réels |
| 🧮 **[Psychtoolbox](https://psychtoolbox.org/)** | Expériences MATLAB/Octave avec contrôle fin de l'affichage et des appareils ; synchronisation et calibration restent nécessaires |

### Références de conception expérimentale

**38 références de conception expérimentale**, chacune organisée selon une même logique : Quand l'utiliser → Logique centrale → À confirmer absolument → Ne pas supposer → Timeline des fenêtres d'essai → Tableau de conditions → Analyse de données → Variantes et références.

Cela ne signifie **pas** que 38 × 3 générateurs ont été vérifiés sur des machines réelles pour les trois plateformes.

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

L'analyse peut être planifiée avant la collecte puis précisée lorsque les données sont disponibles : concevoir le plan d'analyse, générer le code et vérifier les résultats exécutés.

### Skills

| # | Skill | Ce qu'il fait | Détails clés |
|---|------|--------|---------|
| ④ | **Conception d'analyse** `psy-ana-designer` | Part de la question scientifique pour concevoir un plan d'analyse complet | En cinq phases, confirme l'organisation des fichiers et la hiérarchie participants–stimuli–sessions. La Phase 3 compare seulement les critères qui peuvent changer la décision ; les 12 dimensions complètes sont réservées aux choix réellement proches ou à fort impact |
| ⑤ | **Code d'analyse** `psy-ana-coder` | Génère le script reproductible à partir du plan d'analyse | Phase 0 : validation de la config → confirmation R ou Python → génération du script en 12 étapes. 10 portes qualité. R : tidyverse/lme4/ggplot2. Python : pandas/statsmodels/seaborn. Tout est piloté par la config |
| ⑥ | **Audit d'analyse** `psy-ana-reviewer` | Sépare la revue statique du code de la revue des résultats exécutés | Une revue statique atteint au maximum `ready_for_execution`. `ready_for_publication` exige aussi une exécution réussie en environnement propre et la revue des journaux, tableaux, figures, dépendances et informations d'environnement |

### Langages et environnements d'analyse

| Langage et environnement | Particularités |
|------|------|
| 📊 **[R](https://www.r-project.org/)** | Modélisation statistique et rapports scientifiques, avec par exemple lme4, ggplot2, Quarto et R Markdown |
| 🐍 **[Python](https://www.python.org/)** | Traitement général des données, analyse statistique, visualisation et workflows Jupyter |

### Méthodes d'analyse

**60 références de méthodes et 48 références de graphiques** servent à trouver des candidats, pas à prescrire automatiquement une méthode. On compare les points qui peuvent changer la décision ; les 12 dimensions complètes ne sont utilisées que si les options sont réellement proches ou si le choix est lourd de conséquences.

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

Amazing PsyCoder ❯ 🔍 La revue statique n'a trouvé aucun problème bloquant.
                   Le test sur la machine de collecte peut commencer, mais pas la collecte.

Utilisateur      ❯ Démarrage, fin, essai court, intégrité et reprise ont été testés.

Amazing PsyCoder ❯ 🔍 Journaux d'exécution et données sauvegardées vérifiés.
                   État : ready_for_collection
                   La collecte peut commencer.
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
                   Colonnes: subject_id, stimulus, condition, rt, acc, trial

Amazing PsyCoder ❯ Les stimuli sont-ils propres à chaque participant, ou le même
                   ensemble est-il présenté à plusieurs participants ?

Utilisateur      ❯ Tous voient les mêmes 60 combinaisons couleur-mot, avec des
                   essais répétés pour chaque participant.

Amazing PsyCoder ❯ Confirmé : répétitions à la fois par participant et par stimulus.
                   Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Définir l'estimand, puis choisir la méthode
                   Estimand principal : différence moyenne de TR dans la population,
                   incongruent moins congruent.

                   Modèle principal de TR :
                   rt ~ condition + (1 + condition | subject_id) + (1 | stimulus)

                   La précision peut être une analyse complémentaire avec un modèle
                   mixte binomial. Le test t apparié est plus simple, mais répond à
                   une question agrégée sur les moyennes par participant.
                   Si les effets aléatoires ne sont pas estimables de façon stable,
                   suivre un ordre de simplification défini à l'avance et le documenter.

Utilisateur      ❯ Je confirme l'estimand, la formule et la hiérarchie
                   participant/stimulus. Modèle mixte pour le TR, précision en complément.

Amazing PsyCoder ❯ Gate 3 ✅ Estimand, formule, hiérarchie et alternatives confirmés

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Nettoyage, environnement et sorties
                   Indiquez les règles de TR, données manquantes et exclusion tirées
                   du protocole ou du pré-enregistrement. Aucun seuil fixe sans source.

Utilisateur      ❯ Le pré-enregistrement prévoit : analyse principale du TR sur les
                   essais corrects avec TR non manquant ; pas de bornes fixes, de
                   suppression par SD ni d'exclusion automatique de participants.
                   Ajouter une sensibilité log-TR. Le labo utilise R 4.4.1,
                   renv.lock et R Markdown.

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Revue finale
                   ┌──────────────────────────────────────────────────────────┐
                   │ Registre des Décisions d'Analyse                         │
                   │ Question: congruent vs incongruent TR     ← utilisateur   │
                   │ Formule : pente participant + intercept stimulus          │
                   │ Nettoyage : pré-enregistrement + compte à chaque étape    │
                   │ Environnement : R 4.4.1 + renv.lock       ← utilisateur   │
                   │ Sorties : effet, intervalle, diagnostic, graphiques       │
                   └──────────────────────────────────────────────────────────┘
                   Gate 5 ✅ Sauvegarde analysis_config.yaml → Routage code

Utilisateur      ❯ Générer.

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd + renv.lock générés
                   Versions des dépendances enregistrées · revue statique terminée

Amazing PsyCoder ❯ 🔍 État : ready_for_execution
                   Le code peut être exécuté, mais les résultats ne sont pas publiables.

Utilisateur      ❯ Exécution propre avec journal, tableaux, figures et versions.

Amazing PsyCoder ❯ 🔍 Sorties vérifiées · État : ready_for_publication
```

---

## 📂 Structure des fichiers

```text
amazing-psycoder-skills/
├── amazing-psycoder/                  ← Point d'entrée principal (v1.4.0)
│   ├── SKILL.md                       ← Routage et règles globales
│   ├── PLATFORMS.md · install.sh      ← Plateformes et installateur
│   ├── STANDALONE.md                  ← Utilisation directe dans un agent
│   ├── PSYCODER_STUDIO.md             ← Intégration web
│   ├── runtime/                       ← Contrats web et portée fonctionnelle
│   ├── scripts/ · tests/              ← Vérifications automatiques
│   ├── requirements-dev.txt           ← Dépendances de validation
│   │
│   │   # 🧪 Programmation d'expériences
│   ├── psy-exp-designer/              ← ① Conception (5 phases + 38 références)
│   ├── psy-exp-coder/                 ← ② Génération de code (PsychoPy/jsPsych/Psychtoolbox)
│   └── psy-exp-reviewer/              ← ③ Revue du code d'expérience
│   │
│   │   # 📊 Analyse de données
│   ├── psy-ana-designer/              ← ④ Conception d'analyse (60 méthodes + 48 graphiques)
│   ├── psy-ana-coder/                 ← ⑤ Génération de code d'analyse (R/Python)
│   └── psy-ana-reviewer/              ← ⑥ Revue du code et des sorties d'analyse
│
├── docs/                              ← README traduits (繁/EN/JA/DE/FR)
├── .github/                           ← Tests automatiques
└── README.md                          ← Page principale en chinois simplifié
```

---

<div align="center">

💡 Une idée ou une suggestion ? Écrivez-nous à [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
