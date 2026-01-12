"""
Warehouse and Stock Management Models
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from mindzen_erp.core.orm import BaseModel

class Warehouse(BaseModel):
    """Warehouse Master"""
    __tablename__ = 'warehouses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    warehouse_type = Column(String(50), default='store')
    address = Column(Text)
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    incharge_name = Column(String(200))
    phone = Column(String(20))
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<Warehouse {self.name}>"


class StockLedger(BaseModel):
    """Stock Ledger"""
    __tablename__ = 'stock_ledger'
    
    id = Column(Integer, primary_key=True)
    posting_date = Column(DateTime, default=datetime.now, nullable=False)
    posting_time = Column(DateTime, default=datetime.now, nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)
    qty = Column(Numeric(12, 4), nullable=False)
    qty_after_transaction = Column(Numeric(12, 4), default=0)
    incoming_rate = Column(Numeric(12, 4), default=0)
    valuation_rate = Column(Numeric(12, 4), default=0)
    stock_value = Column(Numeric(15, 2), default=0)
    stock_value_difference = Column(Numeric(15, 2), default=0)
    batch_no = Column(String(100))
    voucher_type = Column(String(100), nullable=False)
    voucher_no = Column(String(100), nullable=False)
    
    product = relationship("Product")
    warehouse = relationship("Warehouse")


class StockEntry(BaseModel):
    """Stock Entry"""
    __tablename__ = 'stock_entries'
    
    id = Column(Integer, primary_key=True)
    entry_no = Column(String(50), unique=True, nullable=False)
    entry_date = Column(DateTime, default=datetime.now)
    entry_type = Column(String(50), nullable=False)
    from_warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    to_warehouse_id = Column(Integer, ForeignKey('warehouses.id'))
    status = Column(String(50), default='draft')
    purpose = Column(Text)
    remarks = Column(Text)
    
    from_warehouse = relationship("Warehouse", foreign_keys=[from_warehouse_id])
    to_warehouse = relationship("Warehouse", foreign_keys=[to_warehouse_id])
    items = relationship("StockEntryItem", back_populates="stock_entry", cascade="all, delete-orphan")


class StockEntryItem(BaseModel):
    """Stock Entry Line Items"""
    __tablename__ = 'stock_entry_items'
    
    id = Column(Integer, primary_key=True)
    stock_entry_id = Column(Integer, ForeignKey('stock_entries.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    uom_id = Column(Integer, ForeignKey('uoms.id'), nullable=False)
    qty = Column(Numeric(12, 2), nullable=False)
    qty_in_base_uom = Column(Numeric(12, 4), nullable=False)
    rate = Column(Numeric(12, 4), default=0)
    amount = Column(Numeric(15, 2), default=0)
    batch_no = Column(String(100))
    
    stock_entry = relationship("StockEntry", back_populates="items")
    product = relationship("Product")
    uom = relationship("UOM")
