"""
Database Initialization Script
Creates all tables and loads sample data for plastic manufacturing company
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mindzen_erp.core.orm import Database, Base
from mindzen_erp.core.company import Company, Branch
from mindzen_erp.core.user import User
from mindzen_erp.modules.inventory.models import (
    UOM, ProductCategory, Product, ProductUOM, CustomerGroup, ProductPrice,
    Warehouse
)
from mindzen_erp.modules.sales.models import Customer, CustomerAddress

def init_database():
    """Initialize database with all tables"""
    print("Initializing database...")
    
    # Connect to database
    db_url = os.getenv("DATABASE_URL", "sqlite:///./mindzen_erp_v2.db")
    db = Database()
    db.connect(db_url)
    
    # Create all tables
    Base.metadata.create_all(db.engine)
    
    print("[OK] All tables created successfully!")
    
    return db

def load_sample_data():
    """Load sample data for plastic manufacturing company"""
    print("\nLoading sample data...")
    
    # 1. Create Company (Saudi Arabia)
    company = Company.create({
        'name': 'Saudi Plastic Industries Co.',
        'code': 'SPIC',
        'gst_no': '300123456789003',  # Saudi VAT Number format
        'address': 'Industrial City, Riyadh',
        'city': 'Riyadh',
        'state': 'Riyadh Region',
        'pincode': '11564',
        'phone': '+966-11-1234567',
        'email': 'info@saudiplastic.sa'
    })
    print(f"✓ Created company: {company.name}")
    
    # 2. Create Branch
    branch = Branch.create({
        'company_id': company.id,
        'name': 'Head Office - Riyadh',
        'code': 'RUH-HO',
        'address': 'Industrial City, Riyadh',
        'city': 'Riyadh',
        'state': 'Riyadh Region',
        'state_code': 'SA',
        'pincode': '11564',
        'is_hq': True
    })
    print(f"✓ Created branch: {branch.name}")
    
    # 3. Create UOMs
    uom_piece = UOM.create({'name': 'Piece', 'code': 'PCS'})
    uom_carton = UOM.create({'name': 'Carton', 'code': 'CTN'})
    uom_box = UOM.create({'name': 'Box', 'code': 'BOX'})
    uom_kg = UOM.create({'name': 'Kilogram', 'code': 'KG'})
    print("✓ Created UOMs: Piece, Carton, Box, Kg")
    
    # 4. Create Product Categories
    cat_bottles = ProductCategory.create({'name': 'Plastic Bottles', 'code': 'BOTTLES'})
    cat_caps = ProductCategory.create({'name': 'Bottle Caps', 'code': 'CAPS'})
    cat_containers = ProductCategory.create({'name': 'Containers', 'code': 'CONTAINERS'})
    print("✓ Created product categories")
    
    # 5. Create Sample Products
    # Product 1: Plastic Bottle 500ml
    bottle_500ml = Product.create({
        'name': 'Plastic Bottle 500ml',
        'code': 'BTL-500',
        'category_id': cat_bottles.id,
        'description': 'PET Plastic Bottle 500ml capacity',
        'barcode': '8901234567890',
        'hsn_code': '39233010',
        'base_uom_id': uom_piece.id,
        'gst_rate': 18.00,
        'purchase_rate': 5.00,
        'sale_rate': 10.00,
        'product_type': 'finished_goods'
    })
    
    # Add UOM conversions for bottle
    ProductUOM.create({
        'product_id': bottle_500ml.id,
        'uom_id': uom_piece.id,
        'conversion_factor': 1.0,
        'is_default': True
    })
    ProductUOM.create({
        'product_id': bottle_500ml.id,
        'uom_id': uom_carton.id,
        'conversion_factor': 100.0  # 1 Carton = 100 Pieces
    })
    
    # Add pricing
    ProductPrice.create({
        'product_id': bottle_500ml.id,
        'uom_id': uom_piece.id,
        'price': 10.00
    })
    ProductPrice.create({
        'product_id': bottle_500ml.id,
        'uom_id': uom_carton.id,
        'price': 900.00  # 10% discount for carton
    })
    
    print(f"✓ Created product: {bottle_500ml.name}")
    
    # Product 2: Plastic Bottle 1L
    bottle_1l = Product.create({
        'name': 'Plastic Bottle 1 Liter',
        'code': 'BTL-1000',
        'category_id': cat_bottles.id,
        'description': 'PET Plastic Bottle 1 Liter capacity',
        'barcode': '8901234567891',
        'hsn_code': '39233010',
        'base_uom_id': uom_piece.id,
        'gst_rate': 18.00,
        'purchase_rate': 8.00,
        'sale_rate': 15.00,
        'product_type': 'finished_goods'
    })
    
    ProductUOM.create({
        'product_id': bottle_1l.id,
        'uom_id': uom_piece.id,
        'conversion_factor': 1.0,
        'is_default': True
    })
    ProductUOM.create({
        'product_id': bottle_1l.id,
        'uom_id': uom_carton.id,
        'conversion_factor': 50.0  # 1 Carton = 50 Pieces
    })
    
    ProductPrice.create({
        'product_id': bottle_1l.id,
        'uom_id': uom_piece.id,
        'price': 15.00
    })
    ProductPrice.create({
        'product_id': bottle_1l.id,
        'uom_id': uom_carton.id,
        'price': 700.00  # Bulk discount
    })
    
    print(f"✓ Created product: {bottle_1l.name}")
    
    # Product 3: Bottle Caps
    caps = Product.create({
        'name': 'Plastic Bottle Cap 28mm',
        'code': 'CAP-28',
        'category_id': cat_caps.id,
        'description': 'Screw cap for bottles',
        'barcode': '8901234567892',
        'hsn_code': '39235010',
        'base_uom_id': uom_piece.id,
        'vat_rate': 15.00,
        'purchase_rate': 1.00,
        'sale_rate': 2.00,
        'product_type': 'finished_goods'
    })
    
    ProductUOM.create({
        'product_id': caps.id,
        'uom_id': uom_piece.id,
        'conversion_factor': 1.0,
        'is_default': True
    })
    ProductUOM.create({
        'product_id': caps.id,
        'uom_id': uom_carton.id,
        'conversion_factor': 500.0  # 1 Carton = 500 Pieces
    })
    
    ProductPrice.create({
        'product_id': caps.id,
        'uom_id': uom_piece.id,
        'price': 2.00
    })
    ProductPrice.create({
        'product_id': caps.id,
        'uom_id': uom_carton.id,
        'price': 900.00
    })
    
    print(f"✓ Created product: {caps.name}")
    
    # 6. Create Customer Groups
    group_retail = CustomerGroup.create({'name': 'Retail', 'discount_percent': 0})
    group_wholesale = CustomerGroup.create({'name': 'Wholesale', 'discount_percent': 10})
    group_distributor = CustomerGroup.create({'name': 'Distributor', 'discount_percent': 15})
    print("✓ Created customer groups")
    
    # 7. Create Sample Customers
    customer1 = Customer.create({
        'name': 'Al-Rashid Trading Est.',
        'code': 'CUST-001',
        'customer_group_id': group_distributor.id,
        'phone': '+966-50-1234567',
        'email': 'rashid@trading.sa',
        'contact_person': 'Mr. Abdullah Al-Rashid',
        'vat_no': '300987654321003',
        'credit_limit': 500000.00,  # SAR
        'payment_terms': 'Net 30 days'
    })
    
    CustomerAddress.create({
        'customer_id': customer1.id,
        'address_type': 'billing',
        'address_line1': 'Al-Olaya District',
        'city': 'Riyadh',
        'state': 'Riyadh Region',
        'state_code': 'SA',
        'pincode': '12345',
        'is_default': True
    })
    
    customer2 = Customer.create({
        'name': 'XYZ Retail Store',
        'code': 'CUST-002',
        'customer_group_id': group_retail.id,
        'phone': '9876543211',
        'email': 'xyz@example.com',
        'contact_person': 'Ms. Patel',
        'gst_no': '29XYZAB1234F1Z5',
        'credit_limit': 50000.00,
        'payment_terms': 'Cash'
    })
    
    CustomerAddress.create({
        'customer_id': customer2.id,
        'address_type': 'billing',
        'address_line1': '789 Retail Plaza',
        'city': 'Bangalore',
        'state': 'Karnataka',
        'state_code': '29',
        'pincode': '560003',
        'is_default': True
    })
    
    print(f"✓ Created customers: {customer1.name}, {customer2.name}")
    
    # 8. Create Warehouses
    warehouse_main = Warehouse.create({
        'name': 'Main Warehouse',
        'code': 'WH-MAIN',
        'warehouse_type': 'store',
        'address': '123 Industrial Area',
        'city': 'Bangalore',
        'state': 'Karnataka',
        'incharge_name': 'Mr. Kumar'
    })
    
    warehouse_fg = Warehouse.create({
        'name': 'Finished Goods Store',
        'code': 'WH-FG',
        'warehouse_type': 'store',
        'address': '123 Industrial Area',
        'city': 'Bangalore',
        'state': 'Karnataka',
        'incharge_name': 'Mr. Reddy'
    })
    
    print(f"✓ Created warehouses: {warehouse_main.name}, {warehouse_fg.name}")
    
    # 9. Create Admin User
    admin = User.create({
        'name': 'Administrator',
        'username': 'admin',
        'email': 'admin@plasticindustries.com',
        'is_admin': True,
        'password_hash': ''
    })
    admin.set_password('admin')
    admin.save()
    print(f"✓ Created admin user (admin/admin)")
    
    print("\n✅ Sample data loaded successfully!")
    print("\n" + "="*60)
    print("SAMPLE DATA SUMMARY")
    print("="*60)
    print(f"Company: {company.name}")
    print(f"Products: 3 (Bottles 500ml, 1L, Caps)")
    print(f"UOMs: Piece, Carton, Box, Kg")
    print(f"Customers: 2 (ABC Distributors, XYZ Retail)")
    print(f"Warehouses: 2 (Main, Finished Goods)")
    print(f"Login: admin / admin")
    print("="*60)

if __name__ == "__main__":
    db = init_database()
    load_sample_data()
    print("\n✅ Database initialization complete!")
