"""
Finance and Accounting Models
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from mindzen_erp.core.orm import BaseModel

class AccountGroup(BaseModel):
    """Chart of Accounts - Groups (Assets, Liabilities, Equity, Income, Expense)"""
    __tablename__ = 'account_groups'
    
    name = Column(String(200), nullable=False)
    code = Column(String(20), unique=True)
    parent_id = Column(Integer, ForeignKey('account_groups.id'))
    is_active = Column(Boolean, default=True)
    
    parent = relationship("AccountGroup", remote_side="[AccountGroup.id]", backref="children")

class Ledger(BaseModel):
    """General Ledger Master"""
    __tablename__ = 'ledgers'
    
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True)
    group_id = Column(Integer, ForeignKey('account_groups.id'), nullable=False)
    opening_balance = Column(Numeric(15, 2), default=0)
    current_balance = Column(Numeric(15, 2), default=0)
    is_active = Column(Boolean, default=True)
    
    group = relationship("AccountGroup")
