# 🛰️ AI-CODER SYSTEM MANIFEST (CONTEXT BRIDGE)
### 🎯 Purpose
This document ensures continuity between different AI Agent sessions. If you are a new Agent, read this first.

### 🛠️ CORE ARCHITECTURE FLOW
1. **Trigger**: Telegram Bot (`bot/main.py`) receives a command.
2. **Orchestration**: Command is routed to `agent.py` or `core/orchestrator.py`.
3. **Brain**: Requests are processed by `core/ai_brain.py` using Gemini-2.5-Flash.
4. **Injection**: Resulting code is physically written to `/root/Ai-Coder/projects/[project_name]` via `core/injector.py`.
5. **CLI**: Manual overrides and shell tasks are handled via `/usr/local/bin/gemini`.

### ⚡ UPGRADE HIGHLIGHTS (v1.7.5)
- **iSH Spinner**: CLI uses 🌀 to provide visual feedback on mobile.
- **Git PAT Bypass**: Remote origin is set to `https://[TOKEN]@github.com/...` for passwordless sync.
- **DNA Logging**: Every version upgrade is appended to `DNA.md` with timestamps.

### 📂 FILE MAP
- `/root/Ai-Coder/core/`: The engine (Brain, Injector, Orchestrator).
- `/root/Ai-Coder/bot/`: Telegram polling service.
- `/root/Ai-Coder/projects/`: Isolated dev environments.
- `/usr/local/bin/gemini`: The system-wide Agent CLI.
