"""
Enhanced Sales Controllers with Multi-UOM Support
"""
from mindzen_erp.modules.sales.models import (
    Customer, Quotation, QuotationItem,
    SalesOrder, SalesOrderItem,
    SalesInvoice, SalesInvoiceItem
)
from mindzen_erp.modules.inventory.models import Product, UOM, ProductUOM
from datetime import date, timedelta

class CustomerController:
    """Customer Management"""
    
    def __init__(self, engine=None):
        self.engine = engine
    
    def create_customer(self, data):
        """Create new customer"""
        customer = Customer.create(data)
        return customer
    
    def list_customers(self):
        """List all active customers"""
        return Customer.find_by(is_active=True)
    
    def get_customer(self, customer_id):
        """Get customer by ID"""
        return Customer.find_by_id(customer_id)


class QuotationController:
    """Quotation Management"""
    
    def __init__(self, engine=None):
        self.engine = engine
    
    def create_quotation(self, data, items_data):
        """Create new quotation with line items"""
        # Generate quotation number
        last_quot = Quotation.find_all()
        quot_no = f"QT-{len(last_quot) + 1:05d}"
        
        data['quotation_no'] = quot_no
        data['quotation_date'] = date.today()
        data['valid_till'] = date.today() + timedelta(days=30)
        data['status'] = 'draft'
        
        quotation = Quotation.create(data)
        
        # Add line items
        for item_data in items_data:
            product = Product.find_by_id(item_data['product_id'])
            uom = UOM.find_by_id(item_data['uom_id'])
            
            item = QuotationItem.create({
                'quotation_id': quotation.id,
                'product_id': item_data['product_id'],
                'uom_id': item_data['uom_id'],
                'qty': item_data['qty'],
                'rate': item_data.get('rate', product.sale_rate),
                'vat_rate': product.vat_rate,
                'discount_percent': item_data.get('discount_percent', 0)
            })
            
            item.calculate_amounts()
            item.save()
        
        quotation.calculate_totals()
        quotation.save()
        
        return quotation
    
    def list_quotations(self):
        """List all quotations"""
        return Quotation.find_all()
    
    def get_quotation(self, quotation_id):
        """Get quotation by ID"""
        return Quotation.find_by_id(quotation_id)
    
    def convert_to_sales_order(self, quotation_id):
        """Convert quotation to sales order"""
        quotation = self.get_quotation(quotation_id)
        
        # Create sales order from quotation
        order_controller = SalesOrderController(self.engine)
        order_data = {
            'customer_id': quotation.customer_id,
            'quotation_id': quotation.id,
            'payment_terms': quotation.customer.payment_terms
        }
        
        items_data = []
        for item in quotation.items:
            items_data.append({
                'product_id': item.product_id,
                'uom_id': item.uom_id,
                'qty': item.qty,
                'rate': item.rate,
                'discount_percent': item.discount_percent
            })
        
        sales_order = order_controller.create_sales_order(order_data, items_data)
        
        # Update quotation status
        quotation.status = 'accepted'
        quotation.save()
        
        return sales_order


class SalesOrderController:
    """Sales Order Management"""
    
    def __init__(self, engine=None):
        self.engine = engine
    
    def create_sales_order(self, data, items_data):
        """Create new sales order"""
        # Generate order number
        last_order = SalesOrder.find_all()
        order_no = f"SO-{len(last_order) + 1:05d}"
        
        data['order_no'] = order_no
        data['order_date'] = date.today()
        data['status'] = 'draft'
        
        order = SalesOrder.create(data)
        
        # Add line items
        for item_data in items_data:
            product = Product.find_by_id(item_data['product_id'])
            
            item = SalesOrderItem.create({
                'sales_order_id': order.id,
                'product_id': item_data['product_id'],
                'uom_id': item_data['uom_id'],
                'qty': item_data['qty'],
                'rate': item_data.get('rate', product.sale_rate),
                'vat_rate': product.vat_rate,
                'discount_percent': item_data.get('discount_percent', 0)
            })
            
            item.calculate_amounts()
            item.save()
        
        order.calculate_totals()
        order.save()
        
        return order
    
    def list_orders(self):
        """List all sales orders"""
        return SalesOrder.find_all()
    
    def get_order(self, order_id):
        """Get sales order by ID"""
        return SalesOrder.find_by_id(order_id)
    
    def confirm_order(self, order_id):
        """Confirm sales order"""
        order = self.get_order(order_id)
        order.status = 'confirmed'
        order.save()
        return order


class SalesInvoiceController:
    """Sales Invoice Management"""
    
    def __init__(self, engine=None):
        self.engine = engine
    
    def create_invoice_from_order(self, order_id):
        """Create invoice from sales order"""
        order = SalesOrder.find_by_id(order_id)
        
        # Generate invoice number
        last_invoice = SalesInvoice.find_all()
        invoice_no = f"INV-{len(last_invoice) + 1:05d}"
        
        invoice = SalesInvoice.create({
            'invoice_no': invoice_no,
            'invoice_date': date.today(),
            'customer_id': order.customer_id,
            'sales_order_id': order.id,
            'customer_vat_no': order.customer.vat_no,
            'status': 'draft',
            'payment_status': 'unpaid'
        })
        
        # Add line items from order
        for order_item in order.items:
            item = SalesInvoiceItem.create({
                'invoice_id': invoice.id,
                'product_id': order_item.product_id,
                'uom_id': order_item.uom_id,
                'product_name': order_item.product.name,
                'hsn_code': order_item.product.hsn_code,
                'qty': order_item.qty,
                'rate': order_item.rate,
                'vat_rate': order_item.vat_rate,
                'discount_percent': order_item.discount_percent
            })
            
            item.calculate_amounts()
            item.save()
        
        invoice.calculate_totals()
        invoice.save()
        
        return invoice
    
    def list_invoices(self):
        """List all invoices"""
        return SalesInvoice.find_all()
    
    def get_invoice(self, invoice_id):
        """Get invoice by ID"""
        return SalesInvoice.find_by_id(invoice_id)
    
    def post_invoice(self, invoice_id):
        """Post invoice and update stock"""
        invoice = self.get_invoice(invoice_id)
        
        # TODO: Create stock ledger entries
        # For each invoice item, reduce stock
        
        invoice.status = 'posted'
        invoice.save()
        
        return invoice


__all__ = [
    'CustomerController',
    'QuotationController',
    'SalesOrderController',
    'SalesInvoiceController'
]
