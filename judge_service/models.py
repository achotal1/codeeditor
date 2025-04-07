from sqlalchemy import Column, String, Float, Integer, ForeignKey
from .database import Base

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True, index=True)
    problem_id = Column(String, index=True)
    language = Column(String)
    code = Column(String)
    status = Column(String)
    execution_time = Column(Float, nullable=True)
    memory_used = Column(Integer, nullable=True)
    stdout = Column(String, nullable=True)
    stderr = Column(String, nullable=True)
    passed_count = Column(Integer, nullable=True)
    total_count = Column(Integer, nullable=True)

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(String, primary_key=True, index=True)
    problem_id = Column(String, ForeignKey("problems.id"), index=True)
    input = Column(String)
    expected_output = Column(String) 