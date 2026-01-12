"""
Admin and System Configuration Models
"""
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from mindzen_erp.core.orm import BaseModel

class Currency(BaseModel):
    """Currency Master"""
    __tablename__ = 'currencies'
    
    name = Column(String(100), nullable=False)
    code = Column(String(10), unique=True, nullable=False) # e.g. SAR, USD
    symbol = Column(String(10))
    is_active = Column(Boolean, default=True)

class Country(BaseModel):
    """Country Master"""
    __tablename__ = 'countries'
    
    name = Column(String(200), nullable=False, unique=True)
    code = Column(String(10), unique=True, nullable=False) # ISO Code
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    is_active = Column(Boolean, default=True)
    
    currency = relationship("Currency")

class FinancialYear(BaseModel):
    """Financial Year Master"""
    __tablename__ = 'financial_years'
    
    name = Column(String(100), nullable=False) # e.g. "FL 2024-25"
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_closed = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
