"""
Company and Branch Master Models
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from mindzen_erp.core.orm import BaseModel

class Company(BaseModel):
    """Company Master"""
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    gst_no = Column(String(15))
    pan_no = Column(String(10))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    phone = Column(String(20))
    email = Column(String(100))
    logo = Column(String(500))  # Path to logo file
    is_active = Column(Boolean, default=True)
    
    # Relationships
    branches = relationship("Branch", back_populates="company")
    
    def __repr__(self):
        return f"<Company {self.name}>"


class Branch(BaseModel):
    """Branch/Location Master"""
    __tablename__ = 'branches'
    
    id = Column(Integer, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    state_code = Column(String(2))  # For GST
    pincode = Column(String(10))
    phone = Column(String(20))
    email = Column(String(100))
    is_hq = Column(Boolean, default=False)  # Is Head Office
    is_active = Column(Boolean, default=True)
    
    # Relationships
    company = relationship("Company", back_populates="branches")
    
    def __repr__(self):
        return f"<Branch {self.name}>"
