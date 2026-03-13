---
name: keyword-model-router
description: Hard keyword routing for model/tool selection. Trigger when message includes whole-word WIN or GO. WIN routes to GPT-5.4 subagent; GO routes to Gemini CLI.
read_when:
  - User message contains whole-word WIN
  - User message contains whole-word GO
allowed-tools: sessions_spawn, exec
---

# Keyword Model Router

Apply this skill before normal reasoning when the user message includes trigger keywords.

## Trigger rules (case-insensitive, whole-word only)

- `WIN` matches as an independent token, even when surrounded by punctuation or CJK text.
- `GO` matches as an independent token, even when surrounded by punctuation or CJK text.
- Valid trigger examples:
  - `WIN 修复这个`
  - `请WIN处理`
  - `WIN: 优化`
  - `（WIN）看看`
  - `GO 查一下`
  - `请GO处理`
  - `GO: 运行`
  - `（GO）看看`
- Do NOT match substrings (for example: `window`, `going`, `google`).
- If both appear, prioritize `WIN`.

## Mandatory behavior

### 1) WIN path

1. Remove only the trigger token `WIN` from the user message.
2. Immediately call `sessions_spawn` with:
   - `model: "openai-codex/gpt-5.4"`
   - task = remaining user request
   - `wait: true`
3. Return subagent result to user, with an explicit completion notice:
   - `WIN -> GPT-5.4`
   - success or failure
   - completed work summary
   - changed files if code was modified
4. Do NOT answer directly with MiniMax when WIN is present.
5. Do NOT require the human to ask for manual `spawn`; `WIN` itself must trigger this path.

### 2) GO path

1. Remove only the trigger token `GO` from the user message.
2. Run Gemini CLI via `exec`:
   - First try: `gemini -p "<prompt>"`
   - Fallback if needed: `gemini --prompt "<prompt>"`
3. Return Gemini output directly, and add a final status line that confirms `GO -> Gemini CLI` plus success or failure.
4. If command fails, return concise error + next fix action.

## Scope

- This skill only handles routing for `WIN` and `GO`.
- For non-trigger messages, continue normal model/skill flow.
