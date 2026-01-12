"""
Sales Order Model
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
from mindzen_erp.core.orm import BaseModel

class SalesOrder(BaseModel):
    """Sales Order"""
    __tablename__ = 'sales_orders'
    
    id = Column(Integer, primary_key=True)
    order_no = Column(String(50), unique=True, nullable=False)
    order_date = Column(Date, default=date.today)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    quotation_id = Column(Integer, ForeignKey('quotations.id'))
    delivery_date = Column(Date)
    shipping_address_id = Column(Integer, ForeignKey('customer_addresses.id'))
    status = Column(String(50), default='draft')
    subtotal = Column(Numeric(15, 2), default=0)
    discount_percent = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    taxable_amount = Column(Numeric(15, 2), default=0)
    vat_amount = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    payment_terms = Column(String(100))
    advance_paid = Column(Numeric(15, 2), default=0)
    terms_and_conditions = Column(Text)
    notes = Column(Text)
    
    customer = relationship("Customer")
    quotation = relationship("Quotation")
    shipping_address = relationship("CustomerAddress")
    items = relationship("SalesOrderItem", back_populates="sales_order", cascade="all, delete-orphan")
    
    def calculate_totals(self):
        self.subtotal = sum(item.amount for item in self.items)
        self.discount_amount = self.subtotal * (self.discount_percent / 100)
        self.taxable_amount = self.subtotal - self.discount_amount
        self.vat_amount = sum(item.vat_amount for item in self.items)
        self.total_amount = self.taxable_amount + self.vat_amount


class SalesOrderItem(BaseModel):
    """Sales Order Items"""
    __tablename__ = 'sales_order_items'
    
    id = Column(Integer, primary_key=True)
    sales_order_id = Column(Integer, ForeignKey('sales_orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    uom_id = Column(Integer, ForeignKey('uoms.id'), nullable=False)
    qty = Column(Numeric(12, 2), nullable=False)
    rate = Column(Numeric(12, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    qty_delivered = Column(Numeric(12, 2), default=0)
    qty_invoiced = Column(Numeric(12, 2), default=0)
    discount_percent = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(12, 2), default=0)
    vat_rate = Column(Numeric(5, 2), default=15.00)
    vat_amount = Column(Numeric(12, 2), default=0)
    description = Column(Text)
    
    sales_order = relationship("SalesOrder", back_populates="items")
    product = relationship("Product")
    uom = relationship("UOM")
    
    def calculate_amounts(self):
        self.amount = self.qty * self.rate
        self.discount_amount = self.amount * (self.discount_percent / 100)
        taxable = self.amount - self.discount_amount
        self.vat_amount = taxable * (self.vat_rate / 100)
