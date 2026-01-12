"""
Inventory Module Controllers
"""
from mindzen_erp.modules.inventory.models import (
    Product, ProductCategory, UOM, ProductUOM, ProductPrice,
    Warehouse, StockLedger, StockEntry
)

class ProductController:
    """Product Master Controller"""
    
    def __init__(self, engine=None):
        self.engine = engine
    
    def create_product(self, data):
        """Create new product with UOM conversions"""
        product = Product.create(data)
        return product
    
    def list_products(self, category_id=None, product_type=None):
        """List all products with filters"""
        query = Product.find_all()
        
        if category_id:
            query = [p for p in query if p.category_id == category_id]
        if product_type:
            query = [p for p in query if p.product_type == product_type]
        
        return query
    
    def get_product(self, product_id):
        """Get product by ID"""
        return Product.find_by_id(product_id)
    
    def add_uom_conversion(self, product_id, uom_id, conversion_factor):
        """Add UOM conversion for product"""
        conversion = ProductUOM.create({
            'product_id': product_id,
            'uom_id': uom_id,
            'conversion_factor': conversion_factor
        })
        return conversion
    
    def set_product_price(self, product_id, uom_id, price, customer_group_id=None):
        """Set price for product in specific UOM"""
        price_entry = ProductPrice.create({
            'product_id': product_id,
            'uom_id': uom_id,
            'customer_group_id': customer_group_id,
            'price': price
        })
        return price_entry


class WarehouseController:
    """Warehouse Management Controller"""
    
    def __init__(self, engine=None):
        self.engine = engine
    
    def create_warehouse(self, data):
        """Create new warehouse"""
        warehouse = Warehouse.create(data)
        return warehouse
    
    def list_warehouses(self):
        """List all active warehouses"""
        return Warehouse.find_by(is_active=True)
    
    def get_stock_balance(self, product_id, warehouse_id=None):
        """Get current stock balance for product"""
        query = StockLedger.find_by(product_id=product_id)
        
        if warehouse_id:
            query = [s for s in query if s.warehouse_id == warehouse_id]
        
        if query:
            # Return the latest balance
            latest = sorted(query, key=lambda x: x.posting_date, reverse=True)[0]
            return latest.qty_after_transaction
        
        return 0
    
    def get_stock_summary(self, warehouse_id=None):
        """Get stock summary for all products"""
        # This would typically be a complex query
        # For now, return basic structure
        products = Product.find_all()
        summary = []
        
        for product in products:
            balance = self.get_stock_balance(product.id, warehouse_id)
            if balance > 0:
                summary.append({
                    'product': product,
                    'balance': balance,
                    'uom': product.base_uom
                })
        
        return summary


__all__ = ['ProductController', 'WarehouseController']
