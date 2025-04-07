from sqlalchemy import Column, String, Float, Integer, ForeignKey, JSON, Table, Boolean
from sqlalchemy.orm import relationship
from problem_service.database import Base

# Association table for problem-topic many-to-many relationship
problem_topic = Table(
    'problem_topic',
    Base.metadata,
    Column('problem_id', String, ForeignKey('problems.id')),
    Column('topic', String)
)

class Problem(Base):
    __tablename__ = "problems"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    difficulty = Column(String, nullable=False)
    acceptance_rate = Column(Float, nullable=False)
    topics = Column(JSON, nullable=True)
    examples = Column(JSON, nullable=True)
    constraints = Column(String, nullable=True)
    templates = Column(JSON, nullable=True)
    premium = Column(Boolean, default=False)  # Whether it's a premium problem
    likes = Column(Integer, default=0)
    dislikes = Column(Integer, default=0)
    frequency = Column(Float, default=0.0)  # Frequency of appearance in interviews
    has_examples = Column(Boolean, default=True)  # Whether examples are available in description

    test_cases = relationship("TestCase", back_populates="problem")
    submissions = relationship("Submission", back_populates="problem")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(String, primary_key=True, index=True)
    problem_id = Column(String, ForeignKey("problems.id"))
    input = Column(String, nullable=False)
    expected_output = Column(String, nullable=False)
    is_hidden = Column(Boolean, default=False)
    time_limit = Column(Integer)  # in milliseconds
    memory_limit = Column(Integer)  # in MB
    order = Column(Integer)  # to maintain test case sequence

    problem = relationship("Problem", back_populates="test_cases")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String, primary_key=True)
    problem_id = Column(String, ForeignKey("problems.id"))
    language = Column(String)
    code = Column(String)
    status = Column(String)
    created_at = Column(String)
    execution_time = Column(Float)
    memory_used = Column(Float)
    passed_count = Column(Integer)
    total_count = Column(Integer)

    problem = relationship("Problem", back_populates="submissions") 