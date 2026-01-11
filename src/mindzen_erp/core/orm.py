"""
ORM - SQLAlchemy Implementation with PostgreSQL
"""

import logging
import os
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import create_engine, Column, Integer, DateTime, String, Boolean, Float, inspect
from sqlalchemy.orm import sessionmaker, declarative_base, Session, ScopedSession
from sqlalchemy.sql import func
from datetime import datetime

logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
SqlBase = declarative_base()

class Database:
    """Database connection manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = None
            cls._instance.SessionLocal = None
        return cls._instance
    
    def connect(self, connection_string: str):
        """Connect to PostgreSQL"""
        try:
            self.engine = create_engine(connection_string)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
            # Create tables
            SqlBase.metadata.create_all(bind=self.engine)
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    @contextmanager
    def get_session(self):
        """Provide a transactional scope around a series of operations."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# Type variable for model classes
T = TypeVar('T', bound='BaseModel')

class BaseModel(SqlBase):
    """
    Base model Class mixed with SQLAlchemy Declarative Base.
    """
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def find_by_id(cls: Type[T], record_id: int) -> Optional[T]:
        db = Database()
        with db.get_session() as session:
            return session.query(cls).filter(cls.id == record_id).first()

    @classmethod
    def find_all(cls: Type[T], limit: int = 100) -> List[T]:
        db = Database()
        with db.get_session() as session:
            return session.query(cls).limit(limit).all()

    @classmethod
    def find_by(cls: Type[T], **criteria) -> List[T]:
        db = Database()
        with db.get_session() as session:
            query = session.query(cls)
            for key, value in criteria.items():
                if hasattr(cls, key):
                    query = query.filter(getattr(cls, key) == value)
            return query.all()

    @classmethod
    def create(cls: Type[T], data: Dict[str, Any]) -> T:
        db = Database()
        with db.get_session() as session:
            # Filter data to only include valid columns
            valid_columns = {c.key for c in inspect(cls).mapper.column_attrs}
            clean_data = {k: v for k, v in data.items() if k in valid_columns}
            
            instance = cls(**clean_data)
            session.add(instance)
            session.flush() # Flush to get ID
            session.refresh(instance)
            
            # We need to detach the instance from the session to return it
            # Otherwise accessing attributes outside the session context might fail
            session.expunge(instance)
            return instance

    def save(self) -> 'BaseModel':
        db = Database()
        with db.get_session() as session:
            session.add(self)
            session.commit()
            session.refresh(self)
            session.expunge(self)
            return self

    def delete(self) -> bool:
        if self.id is None:
            return False
        db = Database()
        with db.get_session() as session:
            instance = session.query(self.__class__).get(self.id)
            if instance:
                session.delete(instance)
                return True
        return False
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}

    # Shim for the previous 'validate' method pattern if needed, 
    # though usually handled in controller/pydantic now.
    def validate(self) -> List[str]:
        return []
