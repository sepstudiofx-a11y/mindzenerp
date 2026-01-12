"""
Customer Master Models
"""
from sqlalchemy import Column, Integer, String, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from mindzen_erp.core.orm import BaseModel

class Customer(BaseModel):
    """Customer Master"""
    __tablename__ = 'customers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    code = Column(String(100), unique=True, nullable=False)
    customer_group_id = Column(Integer, ForeignKey('customer_groups.id'))
    phone = Column(String(20))
    email = Column(String(100))
    contact_person = Column(String(200))
    vat_no = Column(String(15))
    commercial_reg = Column(String(20))
    credit_limit = Column(Numeric(15, 2), default=0)
    payment_terms = Column(String(100))
    is_active = Column(Boolean, default=True)
    
    customer_group = relationship("CustomerGroup")
    addresses = relationship("CustomerAddress", back_populates="customer", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Customer {self.name}>"


class CustomerAddress(BaseModel):
    """Customer Addresses (Billing, Shipping)"""
    __tablename__ = 'customer_addresses'
    
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    address_type = Column(String(50), nullable=False)
    address_line1 = Column(String(300))
    address_line2 = Column(String(300))
    city = Column(String(100))
    state = Column(String(100))
    state_code = Column(String(2))
    pincode = Column(String(10))
    country = Column(String(100), default='Saudi Arabia')
    is_default = Column(Boolean, default=False)
    
    customer = relationship("Customer", back_populates="addresses")
