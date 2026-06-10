<div align="center">

# 🧠 Amazing PsyCoder 💻

> Lass die Hürde des Programmierens in der Psychologieforschung komplett verschwinden.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Codex](https://img.shields.io/badge/Codex-Skill-green)](https://github.com/openai/codex)
[![Hermes](https://img.shields.io/badge/Hermes-Skill-orange)](https://github.com/NousResearch/hermes-agent)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-red)](https://github.com/openclaw/openclaw)
[![agentskills.io](https://img.shields.io/badge/agentskills.io-standard-333)](https://agentskills.io)
[![Stars](https://img.shields.io/github/stars/soupandpsy/amazing-psycoder-skills?style=social)](https://github.com/soupandpsy/amazing-psycoder-skills)

[**简体中文**](../README.md) · [**繁體中文**](README_ZH-HANT.md) · [**English**](README_EN.md) · [**日本語**](README_JA.md) · [**Deutsch**](README_DE.md) · [**Français**](README_FR.md)

<br>

[📖 Warum](#-warum-es-dieses-projekt-gibt) · [👥 Für Wen](#-für-wen) · [⚡ Installation](#-installation) · [🚀 Schnellstart](#-schnellstart) · [🧪 Experiment](#-experiment-programmierung) · [📊 Datenanalyse](#-datenanalyse) · [🎬 Demo](#-demo) · [📂 Dateistruktur](#-dateistruktur)

</div>

<br>

<table>
<tr><td align="center">

🔬 &nbsp;Bevor aus einer Idee ein lauffähiges Experiment wird, muss man erst Python, JavaScript oder MATLAB lernen.<br>
📦 &nbsp;Der Legacy-Code aus dem Labor läuft auf dem nächsten Rechner nicht mehr — keiner kennt die Abhängigkeiten, keiner traut sich an die Logik.<br>
📊 &nbsp;Statistische Methoden werden nach Gewohnheit gewählt — „wir nehmen halt ANOVA". Eine Rückfrage des Reviewers, und man fängt von vorne an.<br>
🔁 &nbsp;Die Analyseergebnisse kriegt nur man selbst reproduziert — anderer Rechner, anderer Seed, andere Schlussfolgerung.<br>
✂️ &nbsp;Experiment und Analyse machen oft verschiedene Leute — nach der Erhebung stellt sich heraus: Beim Design hat niemand an die Auswertung gedacht.<br>
📝 &nbsp;Das Journal verlangt eine Erklärung zur Reproduzierbarkeit — aber der Code wurde nie geprüft, nie dokumentiert, nie unabhängig validiert.

</td></tr>
</table>

<div align="center">

### ✨ Genau dafür ist Amazing PsyCoder da.

Du musst weder Python können noch Statistik verstehen. Du bringst deine Ideen und deine Daten mit — Amazing PsyCoder führt dich Schritt für Schritt durchs Design, generiert den Code und prüft alles, bevor es ernst wird. Was du am Ende in den Händen hältst, läuft auf Anhieb, und die Analyse hält auch dem Blick des Reviewers stand.

</div>

---

## 📖 Warum es dieses Projekt gibt

Auf dem Weg von der ersten Idee bis zur tatsächlichen Datenerhebung und Auswertung gibt es zwei Dinge, die am meisten Zeit kosten.

**Erstens: Experiment-Programmierung.** Bevor sich eine Hypothese testen lässt, muss das Experiment erst einmal programmiert werden. PsychoPy Builder ist zu unflexibel, für den Coder braucht man Python; jsPsych setzt JavaScript und Timeline-Logik voraus; Psychtoolbox erfordert MATLAB und Frame-Synchronisation. Fragen wie „Ab welchem Bildschirm startet die RT?" oder „Wie verhindere ich vertauschte Tasten?" oder „Wie speichere ich so, dass bei einem Absturz nichts verloren geht?" — das kostet Wochen. Von der Idee bis zum lauffähigen Experiment geht mehr Zeit verloren als für das eigentliche Experimentdesign.

**Zweitens: Datenanalyse.** Die Daten sind da — aber welche statistische Methode passt? Within-Subject-Design: gepaarter t-Test oder gemischtes Modell? Genauigkeit nahe der Decke — ist ANOVA noch zulässig? Und wenn der Reviewer fragt: „Warum diese Methode?" — was antwortet man dann? Läuft das Skript auf einem anderen Rechner überhaupt noch?

Das ist keine Frage des Könnens, sondern eine Frage der richtigen Werkzeuge. Programmieren und Auswerten sollten die Forschung erleichtern, nicht aufhalten.

Amazing PsyCoder kodiert dieses Erfahrungswissen in 7 Skills — 1 Orchestrator plus 6 Sub-Skills, die den kompletten Weg abdecken: vom Experiment bis zur publikationsreifen Analyse. Folgt dem [agentskills.io](https://agentskills.io) Standard und unterstützt Claude Code / Codex / Hermes / OpenClaw.

Zeit für die Forschung. Nicht für die Technik.

---

## 👥 Für Wen

- 🎓 Psychologie-Studierende und Doktoranden, die ein Experiment programmieren müssen oder bald werden
- 🧠 Forschende in kognitiver, Verhaltens- oder Sozialpsychologie
- 😵‍💫 Wer bei RT, Randomisierung und Bedingungstabellen schon mehrfach gestolpert ist und sich eine systematische Qualitätssicherung wünscht
- 📊 Wer nach der Datenerhebung unsicher ist, welche Statistik die richtige ist — und ein durchdachtes Analyseverfahren möchte
- 📝 Wer vor der Einreichung die Reproduzierbarkeit der Analyse bestätigen will — braucht ein unabhängiges Audit
- 🐍 PsychoPy · 🌐 jsPsych · 🧮 Psychtoolbox / MATLAB Nutzer

---

## ⚡ Installation

Gib den Befehl für deine Plattform direkt in den KI-Chat ein:

**Claude Code**

```
Install Amazing PsyCoder for me: https://github.com/soupandpsy/amazing-psycoder-skills
```

**Codex**

```
$skill-installer
```

Repo-URL eingeben: `https://github.com/soupandpsy/amazing-psycoder-skills`

**Hermes**

```
hermes skills install https://github.com/soupandpsy/amazing-psycoder-skills
```

**OpenClaw**

```
npm i -g clawhub && clawhub install amazing-psycoder
```

Danach `/amazing-psycoder` eingeben.

<details>
<summary><b>Terminal-Installation (plattformübergreifend)</b></summary>

<br>

```bash
git clone https://github.com/soupandpsy/amazing-psycoder-skills
cd amazing-psycoder-skills/amazing-psycoder
./install.sh           # erkennt die Plattform automatisch
# oder manuell: ./install.sh claude | codex | hermes | openclaw
```

</details>

---

## 🚀 Schnellstart

Nach der Installation gib `/amazing-psycoder` ein und beschreibe direkt, was du vorhast:

> "Ich möchte eine Stroop-Aufgabe machen, rot/grün/blau, Tastenreaktion" → startet automatisch das Experiment-Design

> "Hilf mir bei der Stroop-Datenanalyse: Unterscheiden sich kongruente und inkongruente RTs?" → startet automatisch das Analyse-Design

Du musst nicht angeben, welcher Skill zuständig ist — der Orchestrator erkennt deinen Bedarf automatisch. Danach führt dich der Skill Schritt für Schritt: Design bestätigen, Methode auswählen, Code generieren, Audit prüfen. Du musst nur die Fragen beantworten, die er dir stellt.

---

## 🧪 Experiment-Programmierung

Von der ersten Idee zum erhebungsbereiten Experiment — in drei Schritten: Design, Code, Audit.

### Skills

| # | Skill | Aufgabe | Wichtige Details |
|---|-------|---------|------------------|
| ① | **Design** `psy-exp-designer` | Aus einer Experiment-Idee eine komplette Designspezifikation machen | 5-Phasen-Bestätigung. Phase 2 generiert eine Trial-Fenster-Zeitlinie — Dauer, Tasten, RT-Startpunkt auf einen Blick. 5 harte Gates. 38 Paradigmen-Referenzen |
| ② | **Code** `psy-exp-coder` | Aus der Designspezifikation lauffähigen Code generieren | 4-Schichten-Prioritätsarchitektur. 9-Punkte-Qualitätstor: `time.sleep()`, `KbCheck` für RT — werden direkt abgelehnt. 12-Schritt-Codevorlage, Parameter oben |
| ③ | **Audit** `psy-exp-reviewer` | Die letzte Prüfung vor der Datenerhebung | 5 Prüfmodi. Smoke-Test-Protokoll. Paradigmen-Fehlermuster-Check. Bei Nichtbestehen: konkreter Reparaturpfad. Bereitschaftslabel: `ready_for_collection` |

### Plattformen

| Plattform | Besonderheit |
|-----------|-------------|
| 🐍 **[PsychoPy](https://psychopy.org/)** | Python-Ökosystem, USB-HID-Hardware-Zeitstempel, RT-Präzision im Millisekundenbereich. Erste Wahl fürs lokale Labor |
| 🌐 **[jsPsych](https://www.jspsych.org/v7/)** | JavaScript-Ökosystem, läuft im Browser, keine Installation nötig. Erste Wahl für Online-Experimente |
| 🧮 **[Psychtoolbox](http://psychtoolbox.org/)** | MATLAB-Ökosystem, GPU-genaue Frame-Kontrolle. Erste Wahl bei höchsten Timing-Anforderungen |

### Paradigmen-Abdeckung

**38 Paradigmen**, jedes nach einheitlicher Meta-Logik aufbereitet: Wann verwenden → Kernlogik → Muss bestätigt werden → Nicht voraussetzen → Trial-Fenster-Zeitlinie → Bedingungstabelle → Datenanalyse → Varianten & Referenzen.

| Kategorie | Paradigmen |
|-----------|-----------|
| 🎯 **Aufmerksamkeit & Inhibitionskontrolle** | Stroop · Eriksen Flanker · Simon · Go/No-go · Stop-signal · ANT · Posner Cuing · Visual Search · Dot-probe · Navon · CPT · Antisaccade |
| 🧠 **Gedächtnis & Arbeitsgedächtnis** | N-back · Sternberg · Corsi Blocks · Change Detection · Drag and Drop |
| 🔄 **Exekutive Funktionen & kognitive Flexibilität** | Task Switching · WCST · Choice RT |
| 👥 **Soziale Kognition & Emotion** | Cyberball · Climate Reflection · Phone a Friend · Rating · Priming · IAT · EAST |
| 💰 **Entscheidung & Belohnung** | BART · Delay Discounting · Rating to Choice · Ultimatum Game |
| 👁️ **Wahrnehmung & Psychophysik** | Psychophysics Staircase · Multisensory Nature · Mental Rotation |
| 🌱 **Entwicklung & individuelle Unterschiede** | Children Flanker · Bilingual Stroop · Numerical Stroop · Writing Distraction |

---

## 📊 Datenanalyse

Sind die Daten erst einmal da, geht es ebenfalls in drei Schritten weiter: Analyse designen, Code generieren, Reproduzierbarkeit prüfen.

### Skills

| # | Skill | Aufgabe | Wichtige Details |
|---|-------|---------|------------------|
| ④ | **Analyse-Design** `psy-ana-designer` | Ausgehend von der wissenschaftlichen Frage ein vollständiges Analysekonzept entwerfen | 5-Phasen-Bestätigung. Phase 2 klärt die Datenorganisation (Einzeldateien oder zusammengefasst? Benennung? CSV/Excel/TSV?). Phase 3 vergleicht Methoden entlang 12 Dimensionen. Config-YAML als Single Source of Truth |
| ⑤ | **Analyse-Code** `psy-ana-coder` | Aus dem Analysekonzept reproduzierbare Skripte generieren | Phase-0-Validierung → R/Python bestätigen → 12-Schritt-Generierung. 10-Punkte-Qualitätstor. R: tidyverse/lme4/ggplot2. Python: pandas/statsmodels/seaborn. Alles Config-gesteuert |
| ⑥ | **Analyse-Audit** `psy-ana-reviewer` | Die letzte Prüfung vor der Publikation | 4 Prüfmodi. Automatisches Einlese-Protokoll. Prüfung auf statistische Korrektheit + Reproduzierbarkeit + Annahmen. Anti-Pattern-Erkennung für R und Python. Bei Nichtbestehen: Reparaturpfad. Bereitschaftslabel: `ready_for_publication` |

### Plattformen

| Plattform | Besonderheit |
|-----------|-------------|
| 📊 **[R](https://www.r-project.org/)** | Der Standard für statistische Berechnungen. tidyverse + lme4 + ggplot2 + RMarkdown. Erste Wahl für akademische Publikationen |
| 🐍 **[Python](https://www.python.org/)** | Universelles Scientific Computing. pandas + statsmodels + seaborn + Jupyter. Reproduzierbare Analyse |

### Analysemethoden

**60 Methoden, 48 Diagrammtypen**. Jede Methodenentscheidung durchläuft einen 12-Dimensionen-Vergleich: Power · Fehler-1.-Art-Kontrolle · Datennutzung · Ausreißer-Sensitivität · Annahmen-Robustheit · Interpretierbarkeit · Akzeptanz im Feld · Effektstärken-Vergleichbarkeit · Reproduzierbarkeit · Erweiterbarkeit · Stichprobengrößen-Restriktion · Rechnerische Umsetzbarkeit.

| Kategorie | Methoden (Beispiele) |
|-----------|---------------------|
| **Mittelwertsvergleiche** | Gepaarter/unabhängiger t-Test, Within-/Between-Subject-ANOVA, gemischte ANOVA, ANCOVA, MANOVA |
| **Gemischte Modelle** | Lineares gemischtes Modell (LMM), logistisches gemischtes Modell (GLMM), Gamma-GLMM, gekreuzte Zufallseffekte |
| **Mediation & Moderation** | Mediationsanalyse, Moderationsanalyse, moderierte Mediation, Strukturgleichungsmodelle |
| **Regression & Längsschnitt** | Multiple Regression, Quantilsregression, Wachstumskurven, Cross-Lagged-Panel, Zeitreihen |
| **Korrelation & Klassifikation** | Pearson/Spearman-Korrelation, Repeated-Measures-Korrelation, Chi-Quadrat-Test, kanonische Korrelation |
| **Nonparametrisch & Robust** | Wilcoxon, Friedman, Permutationstests, Bootstrap, robuste Regression |
| **Bayes-Statistik** | Bayes-t-Test, Bayes-ANOVA, bayesianisches gemischtes Modell |
| **Messung & Skalierung** | Reliabilitätsanalyse (α/ω/ICC), explorative/konfirmatorische Faktorenanalyse, multidimensionale Skalierung |
| **Signalentdeckung & Diagnostik** | d', ROC-Kurve, psychometrische Funktion |
| **RT- & Entscheidungsmodellierung** | Ex-Gaussian-Verteilung, Drift-Diffusions-Modell (DDM) |
| **Metaanalyse & Power** | Metaanalyse, Poweranalyse, Äquivalenztests |
| **Spezielle Verfahren** | Multiple Imputation, LASSO/Ridge, Netzwerkanalyse, Clusteranalyse, latente Klassenanalyse |

---

## 🎬 Demo

### 🐍 PsychoPy — Stroop-Aufgabe

> "Ich möchte eine Stroop-Aufgabe, rote/grüne/blaue Schrift, Tastendruck beurteilt die Druckfarbe, 50:50 kongruent:inkongruent, 2 Blöcke mit je 60 Durchgängen"

```
Nutzer           ❯ Ich möchte eine Stroop-Aufgabe

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Diagnose
                   Paradigma Stroop · Plattform PsychoPy bestätigen?

Nutzer           ❯ Ja, PsychoPy.

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Trial-Fenster + Antwortregeln (kritisch)
                   Tintenfarben → f=Rot j=Grün k=Blau. Trial-Zeitlinie:
                      Window 1: Fixation            Window 2: Stimulus             Window 3: Pause     
                   ┌──────────────────────┐      ┌──────────────────────┐      ┌──────────────────────┐
                   │                      │      │                      │      │                      │
                   │          +           │  →   │     Rot (grün)      │  →   │                      │
                   │                      │      │                      │      │                      │
                   └──────────────────────┘      └──────────────────────┘      └──────────────────────┘
                            500ms                         2000ms                        500ms          
                         keine Reak.                    f / j / k                    keine Reak.       
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

### 📊 R — Stroop-Datenanalyse

> "Hilf mir mit den Stroop-Daten: Unterscheiden sich die RTs zwischen kongruenten und inkongruenten Bedingungen?"

```
Nutzer           ❯ Hilf mir mit den Stroop-Daten: kongruente vs. inkongruente RTs?

Amazing PsyCoder ❯ 🟢 Phase 1/5 · Experiment & wissenschaftliche Frage verstehen
                   Bitte gib die Experiment-Config an oder beschreibe das Design

Nutzer           ❯ Within-Subject, UV: condition(kongruent/inkongruent), AV: rt+acc. 30 Vpn

Amazing PsyCoder ❯ 🟢 Phase 2/5 · Datenstruktur verstehen
                   Wie sind die Daten gespeichert? Eine Datei pro Vpn oder zusammengefasst?

Nutzer           ❯ Eine CSV pro Vpn, Benennung sub-001_stroop.csv
                   Spalten: subject_id, condition, rt, acc, trial

Amazing PsyCoder ❯ Bestätigt: 30 Vpn × 1 Datei pro Vpn. Gate 2 ✅

Amazing PsyCoder ❯ 🟢 Phase 3/5 · Datencharakteristika + Methode auswählen
                   RT rechtsschief? Genauigkeit nahe der Decke?

Nutzer           ❯ RT etwas rechtsschief, Genauigkeit ca. 95%

Amazing PsyCoder ❯ Genauigkeit nahe der Decke → glmer(binomial) für acc
                   Für RT, 12-Dimensionen-Vergleich A vs. B:

                   ┌────────────┬─────────────────────┬─────────────────────┐
                   │ Dimension   │ A: Gepaarter t-Test  │ B: Gemischtes Modell │
                   ├────────────┼─────────────────────┼─────────────────────┤
                   │ Power       │ 30 Punkte (Vpn-Mw.)  │ 1800 Punkte (Trials) │
                   │ Datennutzung│ Pro Vpn 1 Wert       │ Alle Trials         │
                   │ Erweiterbar │ Kovariate → Neustart │ Formel ergänzen     │
                   │ Interpret.  │ d=0.5 jeder versteht │ Zufallseffekte erkl. │
                   └────────────┴─────────────────────┴─────────────────────┘

                   Fokus auf Power & Erweiterbarkeit → B. Fokus auf Einfachheit → A.

Nutzer           ❯ B

Amazing PsyCoder ❯ Gate 3 ✅ Methode gewählt (mit 12-Dimensionen-Begründung)

Amazing PsyCoder ❯ 🟢 Phase 4/5 · Analysedetails
                   Bereinigung: RT 150-2000ms · korrekte Trials · Vpn acc<60% aus.
                   · ±2.5 SD Trial-Ausschluss · Grafik: Raincloud + individuelle Linien ⚠️

Nutzer           ❯ Bestätigt

Amazing PsyCoder ❯ 🟢 Phase 5/5 · Finale Prüfung
                   ┌──────────────────────────────────────────────────┐
                   │ Analyse-Entscheidungsregister                     │
                   │ Fragestellung: kongruent vs. inkongruent  ← Nutzer│
                   │ Methode: lmer (Nutzer wählte B)          ← Nutzer│
                   │ RT 150-2000ms · Vpn acc<60%              ← Default│
                   │ Grafik: Raincloud + indiv. Linien        ← Default│
                   └──────────────────────────────────────────────────┘
                   Gate 5 ✅ analysis_config.yaml gespeichert → Code-Generierung

Nutzer           ❯ Generieren.

Amazing PsyCoder ❯ ✅ analysis.R + report.Rmd generiert
                   Config-gesteuert · 10-Punkte-Qualitätstor · 12-Schritt-Skript
                   → Automatisch zum Analyse-Audit

Amazing PsyCoder ❯ 🔍 Audit bestanden · Bereitschaft: ready_for_publication
```

---

## 📂 Dateistruktur

```
amazing-psycoder-skills/
├── amazing-psycoder/                  ← Orchestrator (System-Einstieg, v1.3)
│   ├── SKILL.md · PLATFORMS.md · install.sh
│   │
│   │   # 🧪 Experiment-Programmierung
│   ├── psy-exp-designer/              ← ① Experiment-Design (5 Phasen + 38 Paradigmen + 9 Referenzdateien)
│   ├── psy-exp-coder/                 ← ② Experiment-Code (PsychoPy/jsPsych/Psychtoolbox)
│   └── psy-exp-reviewer/              ← ③ Experiment-Audit (5 Modi + Smoke-Test + Recovery-Loop)
│   │
│   │   # 📊 Datenanalyse
│   ├── psy-ana-designer/              ← ④ Analyse-Design (5 Phasen + 60 Methoden + 48 Diagramme)
│   ├── psy-ana-coder/                 ← ⑤ Analyse-Code (R/Python)
│   └── psy-ana-reviewer/              ← ⑥ Analyse-Audit (4 Modi + Einlese-Protokoll + Recovery-Loop)
│
├── docs/                              ← Mehrsprachige READMEs (简/繁/英/日/德/法)
└── README.md
```

---

<div align="center">

💡 Ideen oder Vorschläge? Schreib an [tangdingyi04@outlook.com](mailto:tangdingyi04@outlook.com)<br>
🪄 Made by [soupandpsy](https://github.com/soupandpsy) · MIT License

</div>
