"""
Purchase Invoice Model
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
from mindzen_erp.core.orm import BaseModel

class PurchaseInvoice(BaseModel):
    """Purchase Invoice / Bill"""
    __tablename__ = 'purchase_invoices'
    
    id = Column(Integer, primary_key=True)
    purchase_no = Column(String(50), unique=True, nullable=False)
    vendor_invoice_no = Column(String(50)) # Invoice number from vendor
    invoice_date = Column(Date, default=date.today)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)
    status = Column(String(50), default='draft') # draft, posted, cancelled
    
    # Totals
    subtotal = Column(Numeric(15, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    taxable_amount = Column(Numeric(15, 2), default=0)
    tax_amount = Column(Numeric(15, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    
    notes = Column(Text)
    
    vendor = relationship("Vendor")
    items = relationship("PurchaseInvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    
    def calculate_totals(self):
        self.subtotal = sum(item.amount for item in self.items)
        self.taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = sum(item.tax_amount for item in self.items)
        self.total_amount = round(self.taxable_amount + self.tax_amount, 2)


class PurchaseInvoiceItem(BaseModel):
    """Purchase Invoice Item"""
    __tablename__ = 'purchase_invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('purchase_invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    uom_id = Column(Integer, ForeignKey('uoms.id'), nullable=False)
    qty = Column(Numeric(12, 2), nullable=False)
    rate = Column(Numeric(12, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    tax_rate = Column(Numeric(5, 2), default=15.00)
    tax_amount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    
    invoice = relationship("PurchaseInvoice", back_populates="items")
    product = relationship("Product")
    uom = relationship("UOM")
    
    def calculate_amounts(self):
        self.amount = self.qty * self.rate
        self.tax_amount = self.amount * (self.tax_rate / 100)
        self.total_amount = self.amount + self.tax_amount
