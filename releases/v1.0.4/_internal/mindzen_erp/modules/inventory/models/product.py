"""
Product Master Models with Multi-UOM Support
Critical for Plastic Manufacturing Company
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from mindzen_erp.core.orm import BaseModel

class UOM(BaseModel):
    """Unit of Measure Master (Piece, Carton, Box, Kg, etc.)"""
    __tablename__ = 'uoms'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)  # e.g., "Piece", "Carton"
    code = Column(String(20), nullable=False, unique=True)   # e.g., "PCS", "CTN"
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<UOM {self.name}>"


class ProductCategory(BaseModel):
    """Product Category (e.g., Bottles, Caps, Containers)"""
    __tablename__ = 'product_categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True)
    parent_id = Column(Integer, ForeignKey('product_categories.id'))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    parent = relationship("ProductCategory", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        return f"<ProductCategory {self.name}>"


class Product(BaseModel):
    """Product Master - Core of the ERP"""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    code = Column(String(100), unique=True, nullable=False)  # SKU
    category_id = Column(Integer, ForeignKey('product_categories.id'))
    
    # Product Details
    description = Column(Text)
    barcode = Column(String(100))
    hsn_code = Column(String(20))  
    
    # Base UOM (smallest unit, e.g., "Piece")
    base_uom_id = Column(Integer, ForeignKey('uoms.id'), nullable=False)
    
    # Tax & Pricing (Saudi Arabia VAT)
    vat_rate = Column(Numeric(5, 2), default=15.00)  # Standard VAT 15% in Saudi Arabia
    purchase_rate = Column(Numeric(12, 2))
    sale_rate = Column(Numeric(12, 2))  # Default selling price in base UOM
    
    # Inventory Control
    reorder_level = Column(Numeric(12, 2), default=0)
    reorder_qty = Column(Numeric(12, 2), default=0)
    
    # Product Type
    product_type = Column(String(50), default='finished_goods')  # finished_goods, raw_material, semi_finished
    
    is_active = Column(Boolean, default=True)
    
    # Relationships
    category = relationship("ProductCategory", back_populates="products")
    base_uom = relationship("UOM", foreign_keys=[base_uom_id])
    uom_conversions = relationship("ProductUOM", back_populates="product", cascade="all, delete-orphan")
    prices = relationship("ProductPrice", back_populates="product", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Product {self.name}>"
    
    def get_price_for_uom(self, uom_id, customer_group_id=None):
        """Get selling price for a specific UOM"""
        for price in self.prices:
            if price.uom_id == uom_id:
                if customer_group_id and price.customer_group_id == customer_group_id:
                    return price.price
                elif not price.customer_group_id:  # Default price
                    return price.price
        return self.sale_rate


class ProductUOM(BaseModel):
    """Product UOM Conversions (e.g., 1 Carton = 100 Pieces)"""
    __tablename__ = 'product_uoms'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    uom_id = Column(Integer, ForeignKey('uoms.id'), nullable=False)
    conversion_factor = Column(Numeric(12, 4), nullable=False)
    is_default = Column(Boolean, default=False)
    
    product = relationship("Product", back_populates="uom_conversions")
    uom = relationship("UOM")
    
    def __repr__(self):
        return f"<ProductUOM {self.product_id} - {self.uom_id}>"


class CustomerGroup(BaseModel):
    """Customer Groups for pricing (Retail, Wholesale, Distributor)"""
    __tablename__ = 'customer_groups'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    discount_percent = Column(Numeric(5, 2), default=0)
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<CustomerGroup {self.name}>"


class ProductPrice(BaseModel):
    """Product Pricing by UOM and Customer Group"""
    __tablename__ = 'product_prices'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    uom_id = Column(Integer, ForeignKey('uoms.id'), nullable=False)
    customer_group_id = Column(Integer, ForeignKey('customer_groups.id'))
    price = Column(Numeric(12, 2), nullable=False)
    
    product = relationship("Product", back_populates="prices")
    uom = relationship("UOM")
    customer_group = relationship("CustomerGroup")
    
    def __repr__(self):
        return f"<ProductPrice {self.product_id} - {self.uom_id}: SAR {self.price}>"
