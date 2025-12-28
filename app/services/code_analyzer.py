import os
from openai import OpenAI
from dotenv import load_dotenv
import ast
import json
from typing import List, Dict, Any

load_dotenv()

class PythonAnalyzer:
    """Python 코드 분석기 (AST 기반)"""
    
    def __init__(self, code: str):
        self.code = code
        self.tree = None
        
    def parse(self):
        """코드를 AST로 파싱"""
        try:
            self.tree = ast.parse(self.code)
            return True
        except SyntaxError as e:
            return False
    
    def count_functions(self) -> int:
        """함수 개수 세기"""
        if not self.tree:
            return 0
        return sum(1 for node in ast.walk(self.tree) 
                   if isinstance(node, ast.FunctionDef))
    
    def count_lines(self) -> int:
        """라인 수 세기 (빈 줄 제외)"""
        return len([line for line in self.code.split('\n') if line.strip()])
    
    def calculate_complexity(self) -> int:
        """순환 복잡도 계산 (간단 버전)"""
        if not self.tree:
            return 0
        
        complexity = 1  # 기본
        for node in ast.walk(self.tree):
            # if, for, while, try 등은 복잡도 +1
            if isinstance(node, (ast.If, ast.For, ast.While, 
                                ast.ExceptHandler, ast.With)):
                complexity += 1
        return complexity
    
    def find_basic_issues(self) -> List[Dict[str, Any]]:
        """기본 이슈 찾기"""
        issues = []
        
        if not self.tree:
            issues.append({
                "type": "error",
                "line": 1,
                "message": "Syntax error in code",
                "severity": "critical"
            })
            return issues
        
        # 함수에 docstring 없는지 체크
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                if not ast.get_docstring(node):
                    issues.append({
                        "type": "style",
                        "line": node.lineno,
                        "message": f"Function '{node.name}' is missing a docstring",
                        "severity": "low"
                    })
        
        return issues


class LLMAnalyzer:
    """LLM 기반 코드 분석기"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        self.client = OpenAI(api_key=api_key)

    async def analyze(self, code: str) -> Dict[str, Any]:
        """OpenAI를 사용하여 코드 분석"""
        prompt = f"""
        You are an expert Python code reviewer. Analyze the following python code and provide specific feedback.
        
        Code to analyze:
        ```python
        {code}
        ```
        
        Please provide the response in the following JSON format ONLY, without markdown code fencing:
        {{
            "summary": "Brief summary of the code's purpose",
            "issues": [
                {{
                    "type": "bug" | "security" | "performance" | "style",
                    "line": <line_number or 0 if general>,
                    "message": "Description of the issue",
                    "severity": "low" | "medium" | "high" | "critical",
                    "suggestion": "How to fix it"
                }}
            ],
            "refactoring_suggestion": "General suggestion for refactoring"
        }}
        """

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",  # or gpt-3.5-turbo if preferred
                messages=[
                    {"role": "system", "content": "You are a helpful and precise code review assistant. Always output valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            return {
                "summary": "Analysis failed",
                "issues": [{
                    "type": "error",
                    "line": 0,
                    "message": str(e),
                    "severity": "critical",
                    "suggestion": "Check API key or network connection"
                }],
                "refactoring_suggestion": "None"
            }
