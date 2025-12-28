from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analysis import AnalysisResult, Issue
from typing import Dict, Any, List

async def save_analysis_result(
    db: AsyncSession,
    code: str,
    language: str,
    basic_stats: Dict[str, int],
    basic_issues: List[Any],
    ai_feedback: Dict[str, Any] = None
):
    # 1. AnalysisResult 생성
    analysis_result = AnalysisResult(
        code_snippet=code,
        language=language,
        lines_count=basic_stats.get("lines", 0),
        functions_count=basic_stats.get("functions", 0),
        complexity=basic_stats.get("complexity", 1),
    )

    if ai_feedback:
        analysis_result.ai_summary = ai_feedback.get("summary")
        analysis_result.ai_refactoring_suggestion = ai_feedback.get("refactoring_suggestion")

    db.add(analysis_result)
    await db.flush() # ID 생성을 위해 flush

    # 2. Issues 저장
    # 2.1 Basic Issues
    for issue_data in basic_issues:
        issue = Issue(
            analysis_id=analysis_result.id,
            type=issue_data.type,
            line=issue_data.line,
            message=issue_data.message,
            severity=issue_data.severity,
            suggestion=issue_data.suggestion
        )
        db.add(issue)
    
    # 2.2 AI Issues
    if ai_feedback and "issues" in ai_feedback:
        for ai_issue in ai_feedback["issues"]:
            # AI 결과 형식이 다를 수 있으므로 안전하게 처리
            issue = Issue(
                analysis_id=analysis_result.id,
                type=ai_issue.get("type", "unknown"),
                line=ai_issue.get("line", 0),
                message=ai_issue.get("message", "No message"),
                severity=ai_issue.get("severity", "medium"),
                suggestion=ai_issue.get("suggestion")
            )
            db.add(issue)

    await db.commit()
    await db.refresh(analysis_result)
    return analysis_result
