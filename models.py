from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///auto_apply.db")
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    hr_name = Column(String(255))
    hr_email = Column(String(255), nullable=False)
    role = Column(String(255))
    notes = Column(Text)
    applications = relationship("Application", back_populates="company")

class Application(Base):
    __tablename__ = "applications"
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default="SENT")  # SENT/FAILED
    error_message = Column(Text)
    company = relationship("Company", back_populates="applications")

def init_db():
    Base.metadata.create_all(engine)