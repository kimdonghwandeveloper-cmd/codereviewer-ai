from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    code_snippet = Column(Text)
    language = Column(String(50))
    lines_count = Column(Integer)
    functions_count = Column(Integer)
    complexity = Column(Integer)
    ai_summary = Column(Text, nullable=True)
    ai_refactoring_suggestion = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    issues = relationship("Issue", back_populates="analysis", cascade="all, delete-orphan")

class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("analysis_results.id"))
    type = Column(String(50))
    line = Column(Integer)
    message = Column(Text)
    severity = Column(String(20))
    suggestion = Column(Text, nullable=True)

    analysis = relationship("AnalysisResult", back_populates="issues")
