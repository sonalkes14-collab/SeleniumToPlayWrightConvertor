# SOP: Java Parsing for Selenium

## Goal
Extract structured test data from Selenium Java source files.

## Input
- `.java` file path

## Logic
1. **Identify Class:** Extract class name and package.
2. **Scan Imports:** Identify Selenium and Test Framework (JUnit/TestNG) imports.
3. **Parse Methods:** Extract methods annotated with `@Test`, `@Before...`, `@After...`.
4. **Context Extraction:** Identify `WebDriver` variable names to handle conversion context.

## Edge Cases
- **Inner Classes:** Ignore for now, focus on main test class.
- **Helper Methods:** If a method isn't a test but is called by a test, mark for manual review or include in prompt context.
- **Multiple Classes per File:** Only handle the public test class.
