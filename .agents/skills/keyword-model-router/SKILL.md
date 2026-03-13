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

- `WIN` matches: `(^|\\s)WIN(\\s|$)`
- `GO` matches: `(^|\\s)GO(\\s|$)`
- Do NOT match substrings (for example: `window`, `going`, `google`).
- If both appear, prioritize `WIN`.

## Mandatory behavior

### 1) WIN path

1. Remove only the trigger token `WIN` from the user message.
2. Immediately call `sessions_spawn` with:
   - `model: "openai-codex/gpt-5.4"`
   - task = remaining user request
   - `wait: true`
3. Return subagent result to user.
4. Do NOT answer directly with MiniMax when WIN is present.

### 2) GO path

1. Remove only the trigger token `GO` from the user message.
2. Run Gemini CLI via `exec`:
   - First try: `gemini --model gemini-2.0-flash "<prompt>"`
   - Fallback if needed: `gemini "<prompt>"`
3. Return Gemini output directly.
4. If command fails, return concise error + next fix action.

## Scope

- This skill only handles routing for `WIN` and `GO`.
- For non-trigger messages, continue normal model/skill flow.
