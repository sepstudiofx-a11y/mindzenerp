"""
Sales Invoice Model
"""
from sqlalchemy import Column, Integer, String, Date, Numeric, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import date
from mindzen_erp.core.orm import BaseModel

class SalesInvoice(BaseModel):
    """Sales Invoice"""
    __tablename__ = 'sales_invoices'
    
    id = Column(Integer, primary_key=True)
    invoice_no = Column(String(50), unique=True, nullable=False)
    invoice_date = Column(Date, default=date.today)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    sales_order_id = Column(Integer, ForeignKey('sales_orders.id'))
    customer_vat_no = Column(String(15))
    invoice_type = Column(String(50), default='regular')
    status = Column(String(50), default='draft')
    subtotal = Column(Numeric(15, 2), default=0)
    discount_amount = Column(Numeric(15, 2), default=0)
    taxable_amount = Column(Numeric(15, 2), default=0)
    vat_amount = Column(Numeric(15, 2), default=0)
    round_off = Column(Numeric(10, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    payment_status = Column(String(50), default='unpaid')
    paid_amount = Column(Numeric(15, 2), default=0)
    balance_amount = Column(Numeric(15, 2), default=0)
    due_date = Column(Date)
    terms_and_conditions = Column(Text)
    notes = Column(Text)
    irn = Column(String(100))
    ack_no = Column(String(50))
    ack_date = Column(Date)
    
    customer = relationship("Customer")
    sales_order = relationship("SalesOrder")
    items = relationship("SalesInvoiceItem", back_populates="invoice", cascade="all, delete-orphan")
    
    def calculate_totals(self):
        self.subtotal = sum(item.amount for item in self.items)
        self.taxable_amount = self.subtotal - self.discount_amount
        self.vat_amount = sum(item.vat_amount for item in self.items)
        exact_total = self.taxable_amount + self.vat_amount
        self.total_amount = round(exact_total, 2)
        self.round_off = self.total_amount - exact_total
        self.balance_amount = self.total_amount - self.paid_amount


class SalesInvoiceItem(BaseModel):
    """Sales Invoice Item"""
    __tablename__ = 'sales_invoice_items'
    
    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('sales_invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    uom_id = Column(Integer, ForeignKey('uoms.id'), nullable=False)
    product_name = Column(String(300))
    hsn_code = Column(String(20))
    qty = Column(Numeric(12, 2), nullable=False)
    rate = Column(Numeric(12, 2), nullable=False)
    amount = Column(Numeric(15, 2), nullable=False)
    discount_percent = Column(Numeric(5, 2), default=0)
    discount_amount = Column(Numeric(12, 2), default=0)
    taxable_amount = Column(Numeric(15, 2), default=0)
    vat_rate = Column(Numeric(5, 2), default=15.00)
    vat_amount = Column(Numeric(12, 2), default=0)
    total_amount = Column(Numeric(15, 2), default=0)
    
    invoice = relationship("SalesInvoice", back_populates="items")
    product = relationship("Product")
    uom = relationship("UOM")
    
    def calculate_amounts(self):
        self.amount = self.qty * self.rate
        self.discount_amount = self.amount * (self.discount_percent / 100)
        self.taxable_amount = self.amount - self.discount_amount
        self.vat_amount = self.taxable_amount * (self.vat_rate / 100)
        self.total_amount = self.taxable_amount + self.vat_amount
