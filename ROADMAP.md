# 🧬 AI-Coder — Production ROADMAP.md

## 🎯 SYSTEM PURPOSE
Build a Telegram-triggered AI Developer System that:
* Plans → codes → tests → fixes → documents → deploys
* Works across multiple isolated projects
* Uses GitHub as source of truth & Supabase for memory/credentials

## 🧱 CORE PRINCIPLES (MANDATORY)
1. **GitHub-Centric**: iSH is only the control interface.
2. **Project Isolation**: Contexts (DNA/Roadmap) never mix.
3. **Deterministic Flow**: /Task -> Plan -> Confirm -> Code.
4. **Safety First**: Analyze -> Inject -> Refine (Rewrite is last resort).

## 🎛️ TELEGRAM COMMAND SYSTEM
* **/Select**: Load repo, memory, and credentials for a project.
* **/Add_Project**: Register new repo and initialize DNA/Roadmap.
* **/Task**: AI generates Plan & Roadmap; requires User Confirmation.
* **/Code**: Strict pipeline: Analyze -> Plan Match -> Code -> Test -> Fix -> Git Push.

## 🧬 DNA & DOCUMENTATION
* **DNA.md**: Source of truth for evolution. Every /Code appends a version, task summary, and test results.
* **ROADMAP.md**: Defines goals. AI must follow strictly and update progress.

## 🧠 AI BEHAVIOR RULES
* Pre-Code Analysis is MANDATORY.
* Strategy: Inject > Extend > Refactor > Rewrite.
* Auto-detect errors and trigger iterative fixing loops.
