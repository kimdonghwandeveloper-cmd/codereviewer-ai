from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.code_analyzer import PythonAnalyzer, LLMAnalyzer
from app.core.database import get_db
from app.services.db_service import save_analysis_result

router = APIRouter(prefix="/api", tags=["analyze"])

class CodeAnalysisRequest(BaseModel):
    code: str
    language: str = "python"
    use_ai: bool = True  # AI 사용 여부 옵션

class Issue(BaseModel):
    type: str
    line: int
    message: str
    severity: str
    suggestion: Optional[str] = None # AI 제안 추가

class CodeAnalysisResponse(BaseModel):
    lines: int
    functions: int
    complexity: int
    issues: List[Issue]
    ai_feedback: Optional[Dict[str, Any]] = None # AI 분석 결과 추가
    saved_id: Optional[int] = None # 저장된 DB ID

@router.post("/analyze", response_model=CodeAnalysisResponse)
async def analyze_code(
    request: CodeAnalysisRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    코드를 분석하고 이슈를 반환하며 결과를 DB에 저장합니다.
    """
    if request.language != "python":
        raise HTTPException(
            status_code=400, 
            detail="Currently only Python is supported"
        )
    
    # Python 분석기 사용 (기본 AST)
    analyzer = PythonAnalyzer(request.code)
    analyzer.parse()
    
    basic_issues = [
        Issue(**issue) for issue in analyzer.find_basic_issues()
    ]
    
    response = CodeAnalysisResponse(
        lines=analyzer.count_lines(),
        functions=analyzer.count_functions(),
        complexity=analyzer.calculate_complexity(),
        issues=basic_issues
    )

    # AI 분석 수행
    ai_result = None
    if request.use_ai:
        try:
            llm = LLMAnalyzer()
            ai_result = await llm.analyze(request.code)
            response.ai_feedback = ai_result
        except Exception as e:
            response.ai_feedback = {"error": str(e)}

    # DB 저장
    try:
        saved_result = await save_analysis_result(
            db=db,
            code=request.code,
            language=request.language,
            basic_stats={
                "lines": response.lines,
                "functions": response.functions,
                "complexity": response.complexity
            },
            basic_issues=basic_issues,
            ai_feedback=ai_result
        )
        response.saved_id = saved_result.id
    except Exception as e:
        print(f"DB Save Error: {e}")
        # DB 저장이 실패해도 분석 결과는 반환
        pass

    return response