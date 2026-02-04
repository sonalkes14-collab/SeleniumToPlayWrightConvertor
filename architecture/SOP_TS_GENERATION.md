# SOP: TypeScript Generation & Formatting

## Goal
Assemble converted snippets into a valid, runnable Playwright Test file.

## Logic
1. **Header Assembly:** Add required imports (`import { test, expect } from '@playwright/test';`).
2. **Structure:** Wrap tests in `test('name', async ({ page }) => { ... });`.
3. **Cleanup:** Remove redundant Selenium-style waits that Playwright handles automatically.
4. **Deterministic Templates:** Use Python's `string.Template` for HTML reporting to avoid `{}` collisions with CSS. Use `${var}` or `$var` delimiters.
5. **Unicode Safety:** Avoid emojis in terminal/CLI logs for Windows compatibility. Use standard ASCII markers.

## Edge Cases
- **CSS Brace Collision:** Using `.format()` on HTML with embedded CSS will fail. Always use `Template`.
- **Markdown Handling:** LLMs often wrap code in backticks. The generation layer must strip these to avoid syntax errors in the final `.ts` file.

