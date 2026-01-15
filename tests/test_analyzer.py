import pytest
from app.services.code_analyzer import PythonAnalyzer

def test_count_lines():
    code = """
    def hello():
        print("world")
    """
    # 3 lines of code (including empty lines if split incorrectly, but strip checks for non-empty)
    # The analyzer logic: len([line for line in self.code.split('\n') if line.strip()])
    # Lines:
    # 1. (empty) -> skip
    # 2. def hello():
    # 3.     print("world")
    # 4. (empty) -> skip
    analyzer = PythonAnalyzer(code)
    assert analyzer.count_lines() == 2

def test_count_functions():
    code = """
def func1():
    pass

class MyClass:
    def method1(self):
        pass
    """
    analyzer = PythonAnalyzer(code)
    analyzer.parse()
    assert analyzer.count_functions() == 2

def test_calculate_complexity():
    # Simple function: complexity 1
    code_simple = "def foo(): pass"
    analyzer = PythonAnalyzer(code_simple)
    analyzer.parse()
    assert analyzer.calculate_complexity() == 1

    # Complex function: if + for = 1 + 1 + 1 = 3
    code_complex = """
def complex():
    if True:
        for i in range(10):
            pass
    """
    analyzer = PythonAnalyzer(code_complex)
    analyzer.parse()
    assert analyzer.calculate_complexity() == 3

def test_find_basic_issues_syntax_error():
    code = "def broken(("
    analyzer = PythonAnalyzer(code)
    analyzer.parse()
    issues = analyzer.find_basic_issues()
    assert len(issues) == 1
    assert issues[0]["type"] == "error"
    assert issues[0]["severity"] == "critical"

def test_find_basic_issues_missing_docstring():
    code = """
def no_doc():
    pass
    """
    analyzer = PythonAnalyzer(code)
    analyzer.parse()
    issues = analyzer.find_basic_issues()
    # Should find 1 issue (missing docstring)
    assert len(issues) == 1
    assert issues[0]["type"] == "style"
    assert "docstring" in issues[0]["message"]
