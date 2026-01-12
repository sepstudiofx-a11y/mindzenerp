"""
MindZen ERP Core Usage Workflow
This document outlines the standard operation procedures for the complete ERP system.
"""

# Standard ERP Operations Workflow

## 1. Master Data Setup
1. **Company & Branch**: Configure company ownership (Saudi/GCC for Zakat, Foreign for CIT) and branch details.
2. **UOM & Products**: Set up Units of Measure (Cartons, Pieces) and Product Masters with conversion factors.
3. **Customers & Groups**: Define customer groups (Wholesale, Retail) and VAT Registration Numbers.

## 2. Sales Cycle
1. **Quotation**: Generate professional quotes for customers.
2. **Sales Order**: Confirm orders and track delivery dates.
3. **VAT Invoice**: Generate ZATCA-compliant invoices with 15% VAT.

## 3. Inventory Management
1. **Stock Entries**: Record material receipts, issues, and transfers between warehouses.
2. **Stock Valuation**: Real-time tracking of inventory value in base UOM (Pieces).

## 4. Finance & Zakat
1. **General Ledger**: Automatic posting of sales and purchase transactions.
2. **Zakat Calculation**: Annual 2.5% calculation on Zakat pool for Saudi/GCC owners.
3. **Income Tax**: 20% calculation on profit for foreign owners.

---
// turbo-all
# Automation Workflows

To verify system integrity, run:
```bash
python scripts/verify_erp.py
```
