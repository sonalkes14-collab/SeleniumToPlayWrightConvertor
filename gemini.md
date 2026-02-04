# Project Constitution: Selenium to Playwright Converter

## Purpose
This document serves as the **single source of truth** for:
- Data schemas
- Behavioral rules
- Architectural invariants

## Data Schemas

### Final Input Schema (Actual)
```typescript
interface JavaMethod {
  name: string;        // Extracted Method name
  annotation: string;  // @Test, @BeforeMethod, etc.
  body: string;        // Raw Java source logic
}
```

### Final Output Schema (Actual)
```typescript
interface PlaywrightSpec {
  file: string;        // .spec.ts filename
  content: string;     // Concatenated async tests
  report: string;      // HTML stylized dashboard
}
```

### Self-Annealing Behavioral Rules
1. **Unicode Safety:** Never use emojis in CLI output; use ASCII-safe headers (e.g., `[INFO]`, `---`).
2. **Template Determinism:** Use `string.Template` (Python) and `$` delimiters for HTML to avoid collisions with CSS curly braces `{}`.
3. **LLM Sanitization:** Always apply a triple-backtick stripping bridge to CodeLlama responses to ensure raw code injection.


### Conversion Rule Schema
```typescript
interface ConversionRule {
  id: string;                    // Unique rule identifier
  seleniumPattern: string;       // Regex or AST pattern to match
  playwrightTemplate: string;    // Output template
  category: RuleCategory;        // Type of conversion
  complexity: number;            // 1-10 difficulty rating
  examples: ConversionExample[];
}

type RuleCategory = 
  | 'locator'           // Element finding
  | 'action'            // Clicks, typing, etc.
  | 'wait'              // Synchronization
  | 'assertion'         // Validations
  | 'navigation'        // Page navigation
  | 'lifecycle'         // Setup/teardown
  | 'browser'           // Browser/driver management
  | 'advanced';         // Complex patterns

interface ConversionExample {
  selenium: string;              // Selenium Java code
  playwright: string;            // Playwright TypeScript code
  notes?: string;                // Explanation
}

interface ConversionContext {
  inputFile: InputFile;
  currentMethod: TestMethod;
  variables: Map<string, string>; // Variable name mappings
  pageObjects: Map<string, string>; // POM conversions
}
```

### CLI Input/Output Schema
```typescript
interface CLIInput {
  sourcePath: string;            // Input directory or file
  outputPath: string;            // Output directory
  options: {
    framework: 'playwright-test' | 'jest' | 'mocha';
    preserveStructure: boolean;  // Keep directory structure
    verbose: boolean;            // Detailed logging
    dryRun: boolean;             // Preview without writing
  };
}

interface CLIOutput {
  summary: {
    filesProcessed: number;
    filesConverted: number;
    filesFailed: number;
    totalWarnings: number;
  };
  results: FileConversionResult[];
}

interface FileConversionResult {
  inputFile: string;
  outputFile: string;
  status: 'success' | 'partial' | 'failed';
  warnings: ConversionWarning[];
  conversionTime: number;        // milliseconds
}
```

## Behavioral Rules

### Conversion Principles
1. **Preserve Intent:** Maintain the original test logic and purpose
2. **Idiomatic Output:** Generate Playwright code following best practices
3. **Explicit Over Implicit:** Make conversions clear and traceable
4. **Fail Safely:** When conversion is uncertain, flag for manual review
5. **Maintain Structure:** Preserve test organization and hierarchy

### Code Quality Standards
- Generated TypeScript must be valid and runnable
- Follow Playwright best practices (auto-waiting, modern locators)
- Maintain readability and maintainability
- Include comments for complex conversions

## Architectural Invariants

### Core Components (TBD)
1. **Parser:** Analyze Selenium Java code
2. **Converter:** Transform to intermediate representation
3. **Generator:** Produce Playwright TypeScript code
4. **Validator:** Verify output correctness

### Design Constraints
- Stateless conversion (no side effects)
- Modular, extensible architecture
- Clear separation of concerns
- Testable components

### Technology Stack
- **Language:** TypeScript/Node.js (for cross-platform CLI tool)
- **Parser:** Regex-based pattern matching with fallback to simple AST analysis
- **Testing:** Jest for unit tests, sample Selenium projects for integration tests
- **CLI Framework:** Commander.js for argument parsing
- **Code Generation:** Template-based with string interpolation
- **Build Tool:** TypeScript compiler (tsc) + npm scripts

## Discovery Questions & Answers ✅

### 1. **North Star Vision**
**A Node.js CLI tool that converts Selenium Java test files into idiomatic Playwright TypeScript files, preserving test structure while applying modern best practices.**

### 2. **Integrations & Versions**
- **Selenium:** Support versions 3.x and 4.x
- **Playwright:** Target latest stable version (1.40+)
- **Test Framework:** Playwright Test (primary), with optional Jest output
- **Java:** Parse Java 8+ syntax
- **Assertions:** Convert JUnit 4/5 and TestNG assertions to Playwright expect()

### 3. **Source of Truth**
- **Input:** User provides directory path or individual .java files via CLI
- **Sample Projects:** Will create sample Selenium test files for validation
- **Format:** Standard Selenium WebDriver Java test classes

### 4. **Delivery Payload**
- **Output Location:** New `output/` directory (configurable via CLI)
- **File Structure:** Mirrors input directory structure
- **Naming:** `TestClass.java` → `test-class.spec.ts`
- **Additional Files:** 
  - `conversion-report.json` - Detailed conversion results
  - `warnings.log` - Issues requiring manual review

### 5. **Behavioral Rules for Ambiguity**
- **Complex Waits:** Add `// TODO: Review custom wait conversion` comment
- **Unsupported Patterns:** Add `// MANUAL: Original code - [original]` comment
- **Prioritize:** Readability and Playwright best practices over 1:1 mapping
- **Modern Locators:** Prefer `getByRole`, `getByText` over CSS selectors when possible
- **Auto-waiting:** Remove explicit waits where Playwright handles automatically
- **Fail Strategy:** Convert what's possible, flag rest for manual review (don't fail entire file)

## Maintenance Log (Phase 5)

| Date | Change | Description | Impact |
|------|--------|-------------|--------|
| 2026-02-04 | Initial Release | End-to-end Selenium-to-Playwright pipeline with CodeLlama. | Baseline |
| 2026-02-04 | Stylization | Added HTML Report Generator and Prompt Refinement. | Professional UI |
| 2026-02-04 | Deployment | Finalized Batch Trigger system. | Workflow Automation |

### Long-term Stability Rules
1. **Model Lock:** Always use `codellama` (or higher-parameter variant) for consistent logical conversion.
2. **Context Integrity:** Maintain the 3-layer architecture; never put LLM prompts directly in the parser.
3. **Backup:** Always keep raw conversion responses in `.tmp/` for 24 hours.

## Status
- **Phase:** 5 (Deployment Complete) ✅
- **Schema Defined:** ✅ Yes
- **Blueprint Approved:** ✅ Yes
- **Ready for Development:** ✅ Yes
- **Production Status:** 🛰️ Live / Trigger Ready

---
**✅ PROJECT COMPLETE: The converter is now in production/deployment mode.**


