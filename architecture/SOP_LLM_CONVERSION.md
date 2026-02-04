# SOP: LLM Conversion (Ollama + CodeLlama)

## Goal
Leverage CodeLlama via Ollama to perform high-quality code translation from Selenium Java to Playwright TypeScript.

## Input
- Java code snippet (method body or class block)
- Conversion Context (variable mappings)

## Prompting Strategy
1. **System Role:** "You are an expert SDET specialized in migrating legacy Selenium WebDriver Java suites to modern Playwright TypeScript."
2. **Context:** Provide the standard mapping rules (e.g., `By.id` -> `page.locator`).
3. **Constraint:** "Return ONLY the converted TypeScript code. Use async/await. Do not use generic browser types; use Playwright's Page object."
4. **Verification:** Ask the model to add `// TODO:` for parts it's unsure about.

## Tool Logic
- Call `tools/call_ollama.py` with the structured prompt.
- Save raw responses to `.tmp/` for debugging.
