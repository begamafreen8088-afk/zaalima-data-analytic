from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:password@db:5432/churndb")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    id = Column(Integer, primary_key=True, index=True)
    tenure = Column(Float)
    monthly_charges = Column(Float)
    churn_prediction = Column(Integer)
    churn_probability = Column(Float)
    risk_level = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")

def log_prediction(db, data: dict):
    log = PredictionLog(**data)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

if __name__ == "__main__":
    init_db()
