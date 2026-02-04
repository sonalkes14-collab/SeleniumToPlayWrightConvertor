import os
import sys
from tools.java_parser import JavaSeleniumParser
from tools.call_ollama import call_ollama

import datetime

def coordinate_conversion(java_file_path):
    print(f"--- Starting conversion for: {java_file_path}")
    
    if not os.path.exists(java_file_path):
        print(f"[ERROR] File not found: {java_file_path}")
        return

    # 1. Parse Java
    parser = JavaSeleniumParser(java_file_path)
    class_name = parser.get_class_name()
    methods = parser.extract_methods()
    
    print(f"[INFO] Found {len(methods)} methods in class {class_name}")

    # 2. Convert each method
    converted_tests = []
    
    # SYSTEM PROMPT REFINEMENT: Explicitly forbid surrounding test wrapper
    system_prompt = (
        "You are an expert Selenium-to-Playwright converter. "
        "CONVERT ONLY THE LOGIC inside the Java method. "
        "DO NOT include 'test(...)', 'await context.newPage()', or 'import' statements. "
        "DO NOT include ANY markdown formatting like ```typescript. "
        "ONLY PROVIDE THE JS/TS STATEMENTS. "
        "Assume the 'page' object is already available."
    )

    for method in methods:
        print(f"--- Converting method: {method['name']}...")
        java_code = method['body']
        
        conversion_prompt = f"Convert this Java Selenium logic into Playwright TypeScript statements:\n\n{java_code}"
        converted_code = call_ollama(conversion_prompt, system_prompt)
        
        # Robust stripping of LLM fluff
        if "```" in converted_code:
            # Extract content between triple backticks
            parts = converted_code.split("```")
            if len(parts) >= 3:
                # Code is in second part (e.g. ```typescript\ncode\n```)
                converted_code = parts[1].strip()
                # Remove language identifier if present (e.g. "typescript")
                if converted_code.startswith("typescript"):
                    converted_code = converted_code[len("typescript"):].strip()
                elif converted_code.startswith("ts"):
                    converted_code = converted_code[len("ts"):].strip()
                elif converted_code.startswith("javascript"):
                    converted_code = converted_code[len("javascript"):].strip()
                elif converted_code.startswith("js"):
                    converted_code = converted_code[len("js"):].strip()
            else:
                # Just one or two sets of backticks, take the most likely part
                converted_code = parts[-1].strip()
        else:
            converted_code = converted_code.strip()
        
        # Final cleanup of any potential leftover backticks
        converted_code = converted_code.replace("```", "").strip()
        
        converted_tests.append({
            'name': method['name'],
            'body': converted_code,
            'type': method['annotation']
        })

    # 3. Assemble TS File
    ts_content = "import { test, expect } from '@playwright/test';\n\n"
    
    for test_item in converted_tests:
        if test_item['type'] in ['BeforeMethod', 'BeforeEach', 'Before']:
            ts_content += f"test.beforeEach(async ({{ page }}) => {{\n  {test_item['body'].replace(chr(10), chr(10)+'  ')}\n}});\n\n"
        elif test_item['type'] in ['AfterMethod', 'AfterEach', 'After']:
            ts_content += f"test.afterEach(async ({{ page }}) => {{\n  {test_item['body'].replace(chr(10), chr(10)+'  ')}\n}});\n\n"
        elif test_item['type'] == 'Test':
            ts_content += f"test('{test_item['name']}', async ({{ page }}) => {{\n  {test_item['body'].replace(chr(10), chr(10)+'  ')}\n}});\n\n"

    # 4. Save Output
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    file_slug = class_name.lower()
    ts_output_path = os.path.join(output_dir, f"{file_slug}.spec.ts")
    
    with open(ts_output_path, "w", encoding='utf-8') as f:
        f.write(ts_content)
    
    # 5. GENERATE STYLIZED REPORT (Phase 4)
    from string import Template
    report_template_path = "architecture/REPORT_TEMPLATE.html"
    report_output_path = os.path.join(output_dir, f"{file_slug}_report.html")
    
    if os.path.exists(report_template_path):
        with open(report_template_path, 'r') as f:
            template = Template(f.read())
        
        report_html = template.substitute(
            date=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            source_file=java_file_path,
            methods_found=len(methods),
            methods_converted=len(converted_tests),
            manual_reviews=sum(1 for t in converted_tests if "TODO" in t['body']),
            output_file=f"{file_slug}.spec.ts",
            output_code=ts_content.replace("<", "&lt;").replace(">", "&gt;")
        )
        
        with open(report_output_path, 'w', encoding='utf-8') as f:
            f.write(report_html)
        print(f"[STYLE] Professional report generated: {report_output_path}")

    print(f"[SUCCESS] Conversion complete! File saved to: {ts_output_path}")



if __name__ == "__main__":
    if len(sys.argv) > 1:
        coordinate_conversion(sys.argv[1])
    else:
        print("Usage: python main_coordinator.py <path_to_java_file>")
