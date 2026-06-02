<div align="center">

# 🧠 Amazing PsyCoder 💻

> Von der Experiment-Idee zum produktionsreifen Code. Design → Generierung → Audit, drei zwingende Schritte. 🪄

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Stars](https://img.shields.io/github/stars/soupandpsy/AmazingPsyCoderSkills?style=social)](https://github.com/soupandpsy/AmazingPsyCoderSkills)

[**简体中文**](../README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 Warum](#-warum-es-dieses-projekt-gibt) · [⚡ Installation](#-installation) · [🚀 Schnellstart](#-schnellstart) · [🎬 Demo](#-demo) · [✨ Features](#-features) · [👥 Für wen](#-für-wen)

</div>

<br>

<table>
<tr><td align="left">

⏱️ &nbsp;Ab welchem Bildschirm beginnt die RT-Messung? Falscher Startpunkt — alle Messwerte sind unbrauchbar.<br>
⌨️ &nbsp;Ist die Tastenzuordnung vertauscht? Die Versuchsperson drückt richtig, der Code bewertet es falsch.<br>
🚦 &nbsp;Wie definiert man „korrekt" bei No-go? Drücken, wenn nicht gedrückt werden soll, nicht drücken, wenn gedrückt werden soll — die Logik verschwimmt.<br>
💾 &nbsp;Überleben die Daten einen Absturz? Speichern erst am Ende bedeutet: Absturz = alles verloren.<br>
🔤 &nbsp;Chinesische Instruktionen erscheinen als □□□ — keine CJK-Schriftart, Teilnehmer sehen nur Zeichensalat.<br>
😇 &nbsp;Es läuft, aber ist es wirklich bereit für die Datenerhebung? RT-Genauigkeit, logische Korrektheit, Datenintegrität — keine systematische Garantie.

</td></tr>
</table>

### ✨ Amazing PsyCoder löst genau das.

Keine Code-Vorlage, die Sie selbst anpassen — eher ein erfahrener Veteran der Experiment-Programmierung, der neben Ihnen sitzt. **Design klären → Code generieren → Vor der Erhebung auditieren.**

Drei zwingende Schritte. Kein Überspringen. **Kein Code wird ohne bestandenes Audit ausgeliefert.**

---

## 📖 Warum es dieses Projekt gibt

Jedes Labor hat erfahrene Kollegen, die all diese Fehler schon gemacht haben — aber dieses Wissen wird selten systematisch weitergegeben. PsychoPy Builder oder Coder? Wie funktionieren jsPsych Timeline-Variablen? Warum braucht `Screen('Flip')` `vbl + (waitframes - 0.5) * ifi`?

Allein das Verstehen der APIs dauert Wochen.

Amazing PsyCoder kodiert diese Lektionen in drei zwingende Claude Code Skills — Design-Orchestrierung (5-Phasen-Bestätigung), Code-Generierung (einheitliche Pipeline + 9-Punkte-Qualitätskontrolle) und Code-Audit (Smoke-Test-Protokoll). Egal ob Ihr Labor PsychoPy, jsPsych oder Psychtoolbox verwendet — dieselbe Pipeline erzeugt plattformgerechten Code.

---

## 🎯 Die Drei Skills

| Skill | Aufgabe | Ergebnis |
|-------|---------|----------|
| 1️⃣ **Design** `psych-experiment-programming` | 5-Phasen progressive Bestätigung: Trial-Zeitlinie → Antwortregeln → Bedingungstabelle → Block-Struktur → finale Prüfung | config YAML + Bedingungstabellen |
| 2️⃣ **Code-Gen** `psych-experiment-coder` | 4-Schichten-Prioritätsarchitektur, 9-Punkte-Qualitätstor. `time.sleep()` / `KbCheck` für RT werden direkt abgelehnt | ausführbarer Code + README |
| 3️⃣ **Audit** `psych-experiment-code-reviewer` | Smoke-Tests + Datenintegritätsprüfung + paradigmspezifische Fehlermuster-Analyse. RT-Startpunkt, Tastenzuordnung, Datensicherheit — Punkt für Punkt | Audit-Bericht + Bereitschaftslabel |

---

## ⚡ Installation

Geben Sie in Claude Code folgende Anweisung ein, und das System installiert sich automatisch:

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/AmazingPsyCoderSkills
```

Claude Code klont das Repository und registriert die Skill-Dateien in `~/.claude/skills/`. Starten Sie danach mit `/amazing-psycoder`.

<details>
<summary><b>🛠️ Manuelle Installation</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/AmazingPsyCoderSkills /tmp/AmazingPsyCoderSkills
cp -r /tmp/AmazingPsyCoderSkills/amazing-psycoder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/amazing-psycoder/psych-experiment-programming ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/amazing-psycoder/psych-experiment-coder ~/.claude/skills/
cp -r /tmp/AmazingPsyCoderSkills/amazing-psycoder/psych-experiment-code-reviewer ~/.claude/skills/
```

</details>

---

## 🚀 Schnellstart

Geben Sie in Claude Code `/amazing-psycoder` ein und beschreiben Sie Ihr Experiment:

> "I want a Stroop task, red/green/blue text, key-press response, 2 blocks of 60 trials each"

Das System leitet Sie zum Orchestrator weiter, der Sie durch den 5-Phasen-Designprozess führt. Dabei wird eine Trial-Zeitlinie generiert:

```
Window 1: Fixation          Window 2: Stimulus          Window 3: Pause
┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
│                      │    │                      │    │                      │
│          +           │ →  │     Rot (grün)       │ →  │                      │
│                      │    │                      │    │                      │
└──────────────────────┘    └──────────────────────┘    └──────────────────────┘
500ms                       2000ms                      500ms
keine Reak.                 ← Taste                     keine Reak.
                            RT-Start                    

Window 4: Feedback
┌──────────────────────┐
│                      │
│       Richtig!       │
│                      │
└──────────────────────┘
1000ms
keine Reak.
```

Nach Bestätigung der Zeitlinie wählen Sie Ihre Plattform. Ausgabe ist eine ausführbare Datei (`.py` / `.js` / `.m`) und eine Experiment-README.

---

## 🎬 Demo

### 🐍 PsychoPy — Stroop-Aufgabe

> "I want a Stroop task, red/green/blue text, judge ink color, 50:50 congruent:incongruent, 2 blocks × 60 trials"

```
Nutzer           ❯ I want a Stroop task

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Diagnose
                   Paradigma Stroop · Plattform PsychoPy bestätigen?

Nutzer           ❯ Ja, PsychoPy.

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Trial-Fenster + Antwortregeln (kritisch)
                   Tintenfarben → f=Rot j=Grün k=Blau. Trial-Zeitlinie:
                   Window 1: Fixation          Window 2: Stimulus          Window 3: Pause
                   ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────────┐
                   │                      │    │                      │    │                      │
                   │          +           │ →  │     Rot (grün)       │ →  │                      │
                   │                      │    │                      │    │                      │
                   └──────────────────────┘    └──────────────────────┘    └──────────────────────┘
                   500ms                       2000ms                      500ms
                   keine Reak.                 f / j / k                   keine Reak.
                                               ← RT-Start                  

                   Window 4: Feedback
                   ┌──────────────────────┐
                   │                      │
                   │       Richtig!       │
                   │                      │
                   └──────────────────────┘
                   1000ms
                   keine Reak.
                   Gate 1 ✅ Fenster vollständig, Antwort-Mapping bestätigt

Nutzer           ❯ Zeitlinie und Tasten passen. ITI 400-800ms zufällig.

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Bedingungen
                   Kongruent:inkongruent = 60:60 → 120-Trial Bedingungstabelle
                   Gate 2 ✅ Bedingungsspalten ausgefüllt

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Block-Struktur
                   2 Blöcke × 60 Trials · Feedback nur im Übungsblock
                   Gate 3 ✅ Config hat null [MISSING]

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Finale Prüfung
                   ┌────────────────────────────────────────────────────────┐
                   │ Design-Entscheidungsregister                           │
                   │ Paradigma Stroop · Plattform PsychoPy  ← Benutzer      │
                   │ Tasten f/j/k · 50:50 kongruent         ← Benutzer      │
                   │ ITI 400-800ms zufällig                 ← Benutzer      │
                   │ Trial-Zeitlinie 4 Fenster              ← Konvention    │
                   └────────────────────────────────────────────────────────┘
                   Gate 5 ✅ Alle bestätigt → Weiter zur Code-Generierung

Nutzer           ❯ Generieren.

Amazing PsyCoder ❯ ✅ stroop_task.py + README.md generiert
                   Parameter oben · CJK-Schriftart gesetzt · Inkrementelles Speichern
                   → Automatisch zum Code-Audit

Amazing PsyCoder ❯ 🔍 Audit bestanden · Bereitschaft: ready_for_collection
                   Bereit für die Datenerhebung.
```
---

## ✨ Features

| Feature | Beschreibung |
|---------|--------------|
| 🔬 **Häufige Fehler blockiert** | `time.sleep()`, `KbCheck` für RT — abgelehnt bevor Sie sie überhaupt sehen |
| 🚀 **Direkt lauffähig** | Alle editierbaren Parameter am Anfang der Datei — kein Suchen |
| 🌏 **CJK-Text funktioniert** | Erkennt chinesischen Text automatisch und konfiguriert Schriftarten — kein □□□ |
| 🧪 **Absturzsichere Daten** | Jeder Trial wird sofort gespeichert — Absturz verliert keine erhobenen Daten |
| 🎛️ **Ein System, drei Plattformen** | Dieselbe Pipeline, egal ob Sie PsychoPy, jsPsych oder Psychtoolbox nutzen |

**Weniger Debugging um Mitternacht, mehr Sicherheit vor der Erhebung. 🧪✨**

---

## 📦 Plattform-Unterstützung

| Plattform | Version | Einsatzbereich | Paradigmen | Demos |
|----------|---------|----------|:--:|:--:|
| 🐍 **[PsychoPy](https://psychopy.org/)** | 2024.x+ | Lokales Labor, USB HID Hardware-Zeitstempel | 27 | 45 |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | 7.x | Online-Experimente, Browser-Deployment | 25 | 23 |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | 3.0.21+ | GPU-genaue Frame-Kontrolle | 5 | 100 |

---

## 👥 Für Wen

- 👶 Wenig Programmiererfahrung, aber ein Experiment muss fertig werden
- 🎓 Studierende und Doktoranden, die Experiment-Code schreiben (oder schreiben werden)
- 🧠 Forschende in kognitiver, Verhaltens- oder Sozialpsychologie
- 🐍 PsychoPy fürs Labor · 🌐 jsPsych für online · 🧮 Psychtoolbox / MATLAB
- 😵‍💫 Schon mehrfach über RT, Randomisierung und Bedingungstabellen gestolpert — auf der Suche nach systematischer Qualitätssicherung

---

## 📦 Paradigmen-Abdeckung

**38 Paradigmen**: 14 Kern-Paradigmen (vollständige Designspezifikation) + 24 erweiterte (Referenzbeschreibungen)

| Typ | Paradigmen |
|------|-----------|
| **Kern** | Go/No-go · Navon · Priming · Stroop · Eriksen Flanker · Simon · Rating · Stop-signal · IAT · N-back · Dot-probe · Visual Search · Task Switching · EAST |
| **Erweitert** | Antisaccade · ANT · BART · Bilingual Stroop · Change Detection · Choice RT · CPT · Corsi Blocks · Cyberball · Delay Discounting · Mental Rotation · Posner Cuing · Sternberg · WCST u.a. |

---

## 📂 Dateistruktur

```
AmazingPsyCoderSkills/
├── amazing-psycoder/                  ← Orchestrator (Einstiegspunkt)
│   ├── SKILL.md
│   ├── psych-experiment-programming/  ← ① Design-Schicht (5-Phasen-Workflow + 38 Paradigmen)
│   ├── psych-experiment-coder/        ← ② Code-Generierungsschicht
│   │   ├── psychopy/
│   │   ├── jspsych/
│   │   └── psychtoolbox/
│   └── psych-experiment-code-reviewer/ ← ③ Audit-Schicht (5 Modi + Smoke-Tests)
├── docs/                              ← Mehrsprachige READMEs
└── README.md
```

---

<div align="center">

Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
