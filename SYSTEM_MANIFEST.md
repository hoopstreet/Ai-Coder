# 🛰️ AI-CODER SYSTEM MANIFEST (CONTEXT BRIDGE)
### 🎯 Purpose
This document ensures continuity between different AI Agent sessions.

### 🛠️ CORE ARCHITECTURE FLOW
1. **Trigger**: Telegram Bot (`bot/main.py`)
2. **Brain**: Gemini-2.5-Flash (`core/ai_brain.py`)
3. **Injection**: `core/injector.py`
4. **CLI**: `/usr/local/bin/gemini` (with 🌀 visual feedback)

### ⚡ AI INTERACTION PROTOCOL (v1.7.6)
- **Format**: Provide full raw bash code blocks (e.g., cat << 'EOF').
- **Mobile Friendly**: Split long scripts into multiple parts.
- **No UI Editors**: Do not rely on "file preview" buttons; prioritize terminal-ready text.
- **Remote Targets**: Use absolute paths (`/root/Ai-Coder/...`).

### ⚡ UPGRADE HIGHLIGHTS (v1.7.5)
- **Git PAT Bypass**: Remote origin is hardcoded with token.
- **DNA Logging**: Evolutionary history preserved in DNA.md.
