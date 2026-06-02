<div align="center">

# 🧠 Amazing PsyCoder 💻

> De l'idée d'expérience au code prêt pour la production. Design → Génération → Audit, trois étapes obligatoires. 🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Stars](https://img.shields.io/github/stars/soupandpsy/AmazingPsyCoderSkills?style=social)](https://github.com/soupandpsy/AmazingPsyCoderSkills)

[**简体中文**](README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 Pourquoi](#-pourquoi-ce-projet-existe) · [⚡ Installation](#-installation) · [🚀 Démarrage rapide](#-démarrage-rapide) · [🎬 Démo](#-démo) · [✨ Fonctionnalités](#-fonctionnalités) · [👥 Public](#-public)

</div>

<br>

<table>
<tr><td align="left">

⏱️ &nbsp;À partir de quel écran mesure-t-on le TR ? Un mauvais point de départ — toutes les données sont inutilisables.<br>
⌨️ &nbsp;Les touches sont-elles inversées ? Le participant appuie correctement, le code marque faux.<br>
🚦 &nbsp;Comment définit-on « correct » en No-go ? Appuyer quand il ne faut pas, ne pas appuyer quand il faut — la logique est floue.<br>
💾 &nbsp;Les données survivent-elles à un crash ? Sauvegarde uniquement à la fin = crash = tout est perdu.<br>
🔤 &nbsp;Les instructions en chinois affichent □□□ — pas de police CJK, les participants voient du texte illisible.<br>
😇 &nbsp;Ça tourne, mais est-ce vraiment prêt pour la collecte ? Précision du TR, justesse logique, fiabilité des données — aucune garantie systématique.

</td></tr>
</table>

### ✨ Amazing PsyCoder résout exactement cela.

Pas un modèle de code à adapter soi-même — plutôt un vétéran de la programmation d'expériences assis à vos côtés. **Clarifier le design → Générer le code → Auditer avant la collecte.**

Trois étapes obligatoires. Aucune ne peut être sautée. **Aucun code n'est livré sans avoir passé l'audit.**

---

## 📖 Pourquoi ce projet existe

Chaque laboratoire a des anciens qui ont fait toutes ces erreurs, mais ce savoir est rarement transmis systématiquement. PsychoPy Builder ou Coder ? Comment fonctionnent les variables de timeline jsPsych ? Pourquoi `Screen('Flip')` a-t-il besoin de `vbl + (waitframes - 0.5) * ifi` ?

Rien que comprendre les API prend des semaines.

Amazing PsyCoder encode ces leçons dans trois skills Claude Code obligatoires — orchestration du design (confirmation en 5 phases), génération de code (pipeline unifié + 9 points de contrôle qualité) et audit de code (protocole de test de fumée). Que votre laboratoire utilise PsychoPy, jsPsych ou Psychtoolbox, le même pipeline génère du code adapté à la plateforme.

---

## 🎯 Les Trois Skills

| Skill | Rôle | Résultat clé |
|-------|------|-------------|
| 1️⃣ **Design** `psych-experiment-programming` | Confirmation progressive en 5 phases : timeline d'essai → règles de réponse → tableau de conditions → structure des blocs → revue finale | config YAML + tableaux de conditions |
| 2️⃣ **Génération** `psych-experiment-coder` | Architecture à 4 niveaux de priorité, 9 points de contrôle qualité. `time.sleep()` / `KbCheck` pour le TR rejetés immédiatement | code exécutable + README |
| 3️⃣ **Audit** `psych-experiment-code-reviewer` | Tests de fumée + vérification d'intégrité des données + analyse des modes de défaillance par paradigme. Point de départ du TR, mappage des touches, sécurité des données — examinés un par un | rapport d'audit + label de préparation |

---

## ⚡ Installation

Dans Claude Code, entrez l'instruction suivante et le système s'installera automatiquement :

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/AmazingPsyCoderSkills
```

Claude Code clonera le dépôt et enregistrera les fichiers de skill dans `~/.claude/skills/`. Une fois terminé, tapez `/amazing-psycoder` pour lancer.

<details>
<summary><b>🛠️ Installation manuelle</b></summary>

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

## 🚀 Démarrage rapide

Dans Claude Code, tapez `/amazing-psycoder` et décrivez votre expérience :

> "I want a Stroop task, red/green/blue text, key-press response, 2 blocks of 60 trials each"

Le système vous dirige vers l'orchestrateur qui vous guide à travers le processus de design en 5 phases. Une timeline d'essai est générée :

```
┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Fixation      │ →  │ Stimulus      │ →  │ Pause         │ →  │ Feedback      │
│ +             │    │ Rouge (vert)  │    │               │    │ Correct !     │
│ 500ms         │    │ 2000ms        │    │ 500ms         │    │ 1000ms        │
│               │    │ ← touche      │    │               │    │               │
└───────────────┘    └───────────────┘    └───────────────┘    └───────────────┘
                  Début du TR
```

Après avoir confirmé la timeline, choisissez votre plateforme. Un fichier exécutable (`.py` / `.js` / `.m`) et un README d'expérience sont générés.

---

## 🎬 Démo

### 🐍 PsychoPy — Tâche de Stroop

> "I want a Stroop task, red/green/blue text, judge ink color, 50:50 congruent:incongruent, 2 blocks × 60 trials"

```
Utilisateur      ❯ I want a Stroop task

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Diagnostic
                   Paradigme Stroop · Confirmer PsychoPy ?

Utilisateur      ❯ Oui, PsychoPy.

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Fenêtres d'essai + Règles de réponse (critique)
                   Couleurs d'encre → f=rouge j=vert k=bleu. Timeline :
                   ┌───────────────┐    ┌───────────────┐    ┌───────────────┐    ┌───────────────┐
                   │ Fixation      │ →  │ Stimulus      │ →  │ Pause         │ →  │ Feedback      │
                   │ +             │    │ Rouge (vert)  │    │               │    │ Correct !     │
                   │ 500ms         │    │ 2000ms        │    │ 500ms         │    │ 1000ms        │
                   │ pas de rép.   │    │ ← déb. TR     │    │ pas de rép.   │    │ pas de rép.   │
                   └───────────────┘    └───────────────┘    └───────────────┘    └───────────────┘
                                     Début du TR
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
---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|---------|-------------|
| 🔬 **Pièges courants bloqués** | `time.sleep()`, `KbCheck` pour le TR — rejetés avant même que vous les voyiez |
| 🚀 **Prêt à l'emploi** | Tous les paramètres modifiables en haut du fichier — pas besoin de chercher |
| 🌏 **Texte CJK fonctionnel** | Détection automatique du chinois et configuration des polices — pas de □□□ |
| 🧪 **Données anti-crash** | Chaque essai sauvegardé immédiatement — un crash ne fait pas perdre les données collectées |
| 🎛️ **Un système, trois plateformes** | Même pipeline, que vous utilisiez PsychoPy, jsPsych ou Psychtoolbox |

**Moins de débogage à minuit, plus de confiance avant la collecte. 🧪✨**

---

## 📦 Plateformes supportées

| Plateforme | Version | Cas d'usage | Paradigmes | Démos |
|----------|---------|----------|:--:|:--:|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 2024.x+ | Laboratoire local, horodatages matériels USB HID | 27 | 45 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | 7.x | Expériences en ligne, déploiement navigateur | 25 | 23 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | 3.0.21+ | Contrôle précis au niveau GPU | 5 | 100 |

---

## 👥 Public

- 👶 Peu d'expérience en programmation, mais doit livrer une expérience
- 🎓 Étudiants en licence et master qui écrivent (ou vont écrire) du code d'expérience
- 🧠 Chercheurs en psychologie cognitive, comportementale ou sociale
- 🐍 PsychoPy en local · 🌐 jsPsych en ligne · 🧮 Psychtoolbox / MATLAB
- 😵‍💫 Déjà tombé dans les mêmes pièges de TR, randomisation et tableaux de conditions — à la recherche d'une assurance qualité systématique

---

## 📦 Paradigmes couverts

**38 paradigmes** : 14 principaux (spécifications de conception complètes) + 24 étendus (descriptions de référence)

| Type | Paradigmes |
|------|-----------|
| **Principaux** | Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST |
| **Étendus** | Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST et plus |

---

## 📂 Structure des fichiers

```
AmazingPsyCoderSkills/
├── amazing-psycoder/                  ← Orchestrateur (point d'entrée)
├── psych-experiment-programming/      ← ① Couche design (workflow 5 phases + 38 paradigmes)
├── psych-experiment-coder/            ← ② Couche génération de code
│   ├── psychopy/
│   ├── jspsych/
│   └── psychtoolbox/
└── psych-experiment-code-reviewer/    ← ③ Couche audit (5 modes + tests de fumée)
```

---

<div align="center">

Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
