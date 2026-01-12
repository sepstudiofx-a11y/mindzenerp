# MindZen ERP - User Workflow Guide

## 1. Getting Started
1.  Navigate to the `dist/MindZenERP` folder.
2.  Double-click **MindZenERP.exe**.
3.  A black console window will open. **Do not close this window** as it runs the server.
4.  The application Splash Screen will appear.
5.  Wait 3 seconds for the Login Screen.

## 2. Login
*   **Username:** `admin` (Pre-filled)
*   **Password:** `admin` (Pre-filled)
*   Click **Log In** to access the Dashboard.

## 3. Sales Workflow (Selling to Customers)
1.  **Create Customer:** Go to **Sales > Customers** and click **New Customer**. Fill details and Save.
2.  **Create Invoice:**
    *   Go to **Sales > New Invoice**.
    *   Select a **Customer** from the dropdown.
    *   Click **Add Item**.
    *   Select a **Product**, enter **Qty** and **Rate**.
    *   Click **Generate & Print Bill**.
    *   *Result:* Invoice is saved to the system.

## 4. Purchase Workflow (Buying from Vendors)
1.  **Create Vendor:** Go to **Purchase > Vendors** (ensure vendors exist in master).
2.  **Record Bill:**
    *   Go to **Purchase > New Bill** (or `/purchase/invoices/new`).
    *   Select a **Vendor**.
    *   Click **Add Item**.
    *   Enter product cost details.
    *   Click **Save Purchase Invoice**.
    *   *Result:* Vendor Bill is recorded.

## 5. Troubleshooting
*   If the app closes immediately: Check if another instance is already running.
*   If "Port 8000" error appears: Close any other open black console windows and try again.
