# 🎯 Ai-Coder: Strategic Project Goals

The objective of **Ai-Coder** is to create a fully autonomous, multi-project development platform controlled via Telegram and monitored via a SaaS Dashboard.

## 1. Autonomous Lifecycle (The "Loop")
- **Self-Correction**: The agent must run tests (pytest/vitest) after every code change. If they fail, it must analyze the logs and fix the code without human intervention.
- **DNA Logging**: Every version must be documented in `DNA.md` with a clear description of changes, specific files touched, and the resulting version tag.

## 2. Project Isolation & Context
- **Multi-Tenant Architecture**: Support switching between independent projects using `/Select`. 
- **Memory Persistence**: Each project must have its own context stored in Supabase, preventing the AI from "leaking" logic or credentials from one project to another.

## 3. Integrated Documentation (Roadmap Driven)
- **Goal Alignment**: The agent must update `ROADMAP.md` as it completes phases.
- **AI-Readable Metadata**: Maintain `dna.md` in a structured format so that any LLM reading the repo can instantly reconstruct the history and current state of the architecture.

## 4. Connectivity & Deployment
- **Supabase Backbone**: All credentials (GitHub tokens, API keys) must be stored in the `credentials` table and restored only at runtime.
- **Cloud-Native**: Designed to run on Northflank (Dockerized) while maintaining a persistent connection to the Telegram Bot API.

## 5. Learning Feedback
- **Failure Analysis**: Successes and failures must be recorded in the `autonomous_learning` table to ensure the agent does not repeat the same coding mistakes in future tasks.
