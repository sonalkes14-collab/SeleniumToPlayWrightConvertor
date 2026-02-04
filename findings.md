# Findings: Research, Discoveries, and Constraints

## Research Areas

### Selenium WebDriver (Java)
- **Key Concepts to Convert:**
  - WebDriver initialization
  - Element locators (By.id, By.xpath, By.cssSelector, etc.)
  - Actions (click, sendKeys, getText, etc.)
  - Waits (implicit, explicit, fluent)
  - Assertions (JUnit/TestNG)
  - Page Object Model patterns
  - Test lifecycle methods (@Before, @After, @Test)

### Playwright (TypeScript)
- **Equivalent Concepts:**
  - Browser/Page/Context initialization
  - Locators (page.locator, getByRole, getByText, etc.)
  - Actions (click, fill, textContent, etc.)
  - Auto-waiting mechanism
  - Expect assertions
  - Page Object Model patterns
  - Test lifecycle (beforeEach, afterEach, test)

## Key Discoveries

### Selenium to Playwright Conversion Mappings

#### 1. **Locator Strategies**
| Selenium Java | Playwright TypeScript |
|--------------|----------------------|
| `driver.findElement(By.id("btn"))` | `page.locator('#btn')` or `page.getById('btn')` |
| `driver.findElement(By.name("username"))` | `page.locator('[name="username"]')` |
| `driver.findElement(By.className("btn-primary"))` | `page.locator('.btn-primary')` |
| `driver.findElement(By.cssSelector(".btn"))` | `page.locator('.btn')` |
| `driver.findElement(By.xpath("//button"))` | `page.locator('//button')` |
| `driver.findElement(By.linkText("Click"))` | `page.getByRole('link', { name: 'Click' })` |
| `driver.findElement(By.tagName("button"))` | `page.locator('button')` |

#### 2. **Actions**
| Selenium Java | Playwright TypeScript |
|--------------|----------------------|
| `element.click()` | `await element.click()` |
| `element.sendKeys("text")` | `await element.fill('text')` |
| `element.clear()` | `await element.clear()` |
| `element.getText()` | `await element.textContent()` |
| `element.getAttribute("href")` | `await element.getAttribute('href')` |
| `element.isDisplayed()` | `await element.isVisible()` |
| `element.isEnabled()` | `await element.isEnabled()` |
| `element.submit()` | `await element.press('Enter')` |

#### 3. **Waits (Critical Difference!)**
| Selenium Java | Playwright TypeScript |
|--------------|----------------------|
| `driver.manage().timeouts().implicitlyWait(10, SECONDS)` | ❌ Remove - Playwright auto-waits |
| `new WebDriverWait(driver, 10).until(...)` | ❌ Usually unnecessary - auto-wait |
| `ExpectedConditions.visibilityOf(element)` | `await element.waitFor({ state: 'visible' })` |
| `ExpectedConditions.elementToBeClickable(element)` | ❌ Auto-handled by click() |
| `Thread.sleep(1000)` | `await page.waitForTimeout(1000)` (discouraged) |

#### 4. **Navigation**
| Selenium Java | Playwright TypeScript |
|--------------|----------------------|
| `driver.get("https://example.com")` | `await page.goto('https://example.com')` |
| `driver.navigate().back()` | `await page.goBack()` |
| `driver.navigate().forward()` | `await page.goForward()` |
| `driver.navigate().refresh()` | `await page.reload()` |
| `driver.getCurrentUrl()` | `page.url()` |
| `driver.getTitle()` | `await page.title()` |

#### 5. **Assertions**
| Selenium Java (JUnit) | Playwright TypeScript |
|----------------------|----------------------|
| `assertEquals(expected, actual)` | `expect(actual).toBe(expected)` |
| `assertTrue(element.isDisplayed())` | `await expect(element).toBeVisible()` |
| `assertFalse(element.isDisplayed())` | `await expect(element).toBeHidden()` |
| `assertNotNull(element)` | `await expect(element).not.toBeNull()` |
| `assertEquals("text", element.getText())` | `await expect(element).toHaveText('text')` |

#### 6. **Browser/Driver Management**
| Selenium Java | Playwright TypeScript |
|--------------|----------------------|
| `WebDriver driver = new ChromeDriver()` | `const browser = await chromium.launch()` |
| `driver.manage().window().maximize()` | `const context = await browser.newContext({ viewport: null })` |
| `driver.quit()` | `await browser.close()` |
| `driver.switchTo().frame(0)` | `await page.frameLocator('iframe')` |
| `driver.switchTo().alert().accept()` | `page.on('dialog', dialog => dialog.accept())` |

#### 7. **Test Lifecycle**
| Selenium Java (JUnit) | Playwright TypeScript |
|----------------------|----------------------|
| `@Before` / `@BeforeEach` | `test.beforeEach(async ({ page }) => {})` |
| `@After` / `@AfterEach` | `test.afterEach(async ({ page }) => {})` |
| `@BeforeClass` | `test.beforeAll(async () => {})` |
| `@AfterClass` | `test.afterAll(async () => {})` |
| `@Test` | `test('test name', async ({ page }) => {})` |

## Technical Constraints

### Parsing Limitations
1. **No Full Java AST:** Using regex-based parsing means we can't handle all Java syntax edge cases
2. **Context Sensitivity:** Variable assignments and scope tracking is limited
3. **Custom Methods:** User-defined helper methods won't be automatically converted
4. **Complex Expressions:** Nested method calls may require manual review

### Language Differences
1. **Async/Await:** All Playwright operations are async, Selenium is synchronous
2. **Type System:** Java static typing vs TypeScript's structural typing
3. **Error Handling:** Try-catch patterns differ between languages
4. **Null Handling:** Java null vs TypeScript undefined/null

### Playwright Specifics
1. **Auto-waiting:** Fundamentally different from Selenium's explicit waits
2. **Locator Strategy:** Playwright encourages different locator patterns
3. **Page Object Model:** Structure differs between frameworks
4. **Test Isolation:** Playwright Test has built-in isolation, Selenium doesn't

## Conversion Challenges

### High Complexity Patterns
1. **Custom Wait Conditions:** Complex ExpectedConditions need manual conversion
2. **Actions Class:** Advanced mouse/keyboard interactions (drag-drop, hover chains)
3. **JavaScript Execution:** `JavascriptExecutor` usage needs case-by-case handling
4. **Multiple Windows/Tabs:** Different APIs for window handling
5. **File Upload/Download:** Different mechanisms in Playwright
6. **Screenshots:** Different APIs and options

### Medium Complexity Patterns
1. **Select Dropdowns:** `Select` class vs Playwright's locator methods
2. **Alerts/Dialogs:** Event-based handling in Playwright
3. **Cookies Management:** Different API structure
4. **Browser Capabilities:** ChromeOptions vs Playwright launch options

### Edge Cases
1. **Implicit Waits:** Need to be completely removed (anti-pattern in Playwright)
2. **Stale Element References:** Playwright handles differently with auto-retry
3. **Flaky Tests:** Playwright's auto-waiting may fix some, break others
4. **Page Load Strategies:** Different concepts between frameworks

## Dependencies
- Java parser/AST library (TBD)
- TypeScript code generator (TBD)
- Pattern matching engine (TBD)

## References
- Selenium WebDriver Documentation
- Playwright Documentation
- Java to TypeScript syntax mapping
