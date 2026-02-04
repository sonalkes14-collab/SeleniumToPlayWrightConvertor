import re
import os

class JavaSeleniumParser:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r', encoding='utf-8') as f:
            self.content = f.read()

    def get_class_name(self):
        match = re.search(r'public class (\w+)', self.content)
        return match.group(1) if match else "ConvertedTest"

    def extract_methods(self):
        """
        Extracts methods annotated with @Test, @Before, etc.
        Returns a list of dicts: {'name': str, 'body': str, 'annotation': str}
        """
        methods = []
        # Simple regex to find methods with annotations
        # This is a bit naive but works for standard Selenium patterns
        pattern = r'@(\w+)\s+public void (\w+)\(\)\s*\{([\s\S]*?)\n\s*\}'
        matches = re.finditer(pattern, self.content)
        
        for match in matches:
            methods.append({
                'annotation': match.group(1),
                'name': match.group(2),
                'body': match.group(3).strip()
            })
        return methods

if __name__ == "__main__":
    # Test stub
    sample_content = """
    @Test
    public void myTest() {
        driver.get("url");
        driver.findElement(By.id("id")).click();
    }
    """
    # Write sample for testing the tool itself
    temp_file = ".tmp/sample_test.java"
    os.makedirs(".tmp", exist_ok=True)
    with open(temp_file, "w") as f:
        f.write(sample_content)
    
    parser = JavaSeleniumParser(temp_file)
    print(parser.extract_methods())
