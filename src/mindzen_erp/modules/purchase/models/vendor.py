"""
Vendor Model for Saudi Arabia
"""
from sqlalchemy import Column, Integer, String, Boolean, Text
from mindzen_erp.core.orm import BaseModel

class Vendor(BaseModel):
    """Vendor Master"""
    __tablename__ = 'vendors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    contact_person = Column(String(200))
    email = Column(String(100))
    phone = Column(String(50))
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100), default='Saudi Arabia')
    
    # Saudi Specifics
    vat_no = Column(String(15))  # Vendor VAT Registration
    commercial_reg = Column(String(20)) # CR Number
    
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Vendor {self.name}>"
