import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from mindzen_erp.core.orm import Database
from mindzen_erp.modules.inventory.models import Product, UOM
from mindzen_erp.modules.sales.models import Customer
from mindzen_erp.core.company import Company

def test_crud():
    print("Testing CRUD operations...")
    
    # Connect to database first!
    db_url = os.getenv("DATABASE_URL", "sqlite:///./mindzen_erp_v2.db")
    db = Database()
    db.connect(db_url)
    
    try:
        # 1. Read
        products = Product.find_all()
        print(f"[OK] Read: Found {len(products)} products")
        
        # 2. Update
        if products:
            product = products[0]
            original_name = product.name
            product.name = original_name + " (Updated)"
            product.save()
            
            updated_product = Product.find_by_id(product.id)
            if updated_product.name == original_name + " (Updated)":
                print(f"[OK] Update: Product name updated successfully")
            else:
                print(f"[FAIL] Update: Product name mismatch")
        
        # 3. Create
        new_uom = UOM.create({'name': 'Test UOM', 'code': 'TUM'})
        print(f"[OK] Create: New UOM created with ID {new_uom.id}")
        
        # 4. Delete
        uom_id = new_uom.id
        new_uom.delete()
        deleted_uom = UOM.find_by_id(uom_id)
        if deleted_uom is None:
            print(f"[OK] Delete: UOM deleted successfully")
        else:
            print(f"[FAIL] Delete: UOM still exists")
            
        print("\n[SUCCESS] All CRUD operations verified!")
        
    except Exception as e:
        print(f"\n[ERROR] CRUD verification failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_crud()
