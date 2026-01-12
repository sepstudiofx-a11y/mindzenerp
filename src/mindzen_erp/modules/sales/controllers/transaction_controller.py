"""
Sales & Purchase Controllers with Zakat/Tax & Multi-UOM
"""
from mindzen_erp.modules.sales.models import (
    Customer, SalesInvoice, SalesInvoiceItem
)
from mindzen_erp.modules.purchase.models import (
    Vendor, PurchaseInvoice, PurchaseInvoiceItem
)
from mindzen_erp.modules.inventory.models import Product, UOM, ProductUOM
from datetime import date

class TransactionController:
    """Base Controller for Sales/Purchase Transactions"""
    def __init__(self, engine=None):
        self.engine = engine

class SalesInvoiceController(TransactionController):
    """Sales Invoice Management"""
    
    def create_invoice(self, data, items_data):
        last_inv = SalesInvoice.find_all()
        data['invoice_no'] = f"SINV-{len(last_inv) + 1:05d}"
        invoice = SalesInvoice.create(data)
        
        for item_data in items_data:
            product = Product.find_by_id(item_data['product_id'])
            item = SalesInvoiceItem.create({
                'invoice_id': invoice.id,
                'product_id': item_data['product_id'],
                'uom_id': item_data['uom_id'],
                'qty': item_data['qty'],
                'rate': item_data['rate'],
                'tax_rate': product.vat_rate, # From product master
            })
            item.calculate_amounts()
            item.save()
            
        invoice.calculate_totals()
        invoice.save()
        return invoice

class PurchaseInvoiceController(TransactionController):
    """Purchase Invoice Management"""
    
    def create_invoice(self, data, items_data):
        last_inv = PurchaseInvoice.find_all()
        data['purchase_no'] = f"PINV-{len(last_inv) + 1:05d}"
        invoice = PurchaseInvoice.create(data)
        
        for item_data in items_data:
            item = PurchaseInvoiceItem.create({
                'invoice_id': invoice.id,
                'product_id': item_data['product_id'],
                'uom_id': item_data['uom_id'],
                'qty': item_data['qty'],
                'rate': item_data['rate'],
            })
            item.calculate_amounts()
            item.save()
            
        invoice.calculate_totals()
        invoice.save()
        return invoice
