from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import os
from pathlib import Path
from typing import List, Optional

from mindzen_erp.core import Engine, ConfigManager
from mindzen_erp.core.orm import Database
from mindzen_erp.modules.crm.controllers import LeadController
from mindzen_erp.modules.sales.controllers import SaleController

# Initialize Engine & DB
engine = Engine()
engine.initialize()
engine.discover_modules()
engine.install_module('crm')
engine.install_module('sales')

# Database Connection
db_url = os.getenv("DATABASE_URL", "sqlite:///./mindzen_erp.db")
Database().connect(db_url)

app = FastAPI(title="MindZen ERP")

# Paths
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# --- DASHBOARD ---
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "active_module": "dashboard"
    })

# --- CRM ROUTES ---
@app.get("/crm/leads", response_class=HTMLResponse)
async def list_leads(request: Request):
    controller = LeadController(engine)
    leads = controller.list_leads()
    return templates.TemplateResponse("crm/leads.html", {
        "request": request, 
        "leads": leads,
        "active_module": "crm"
    })

@app.get("/crm/leads/new", response_class=HTMLResponse)
async def new_lead_form(request: Request):
    return templates.TemplateResponse("crm/lead_form.html", {
        "request": request,
        "lead": None,
        "active_module": "crm"
    })

@app.post("/crm/leads", response_class=HTMLResponse)
async def create_lead(request: Request):
    form = await request.form()
    data = dict(form)
    if 'expected_revenue' in data:
        data['expected_revenue'] = float(data['expected_revenue'])
    
    controller = LeadController(engine)
    controller.create_lead(data)
    return RedirectResponse(url="/crm/leads", status_code=303)

@app.get("/crm/leads/{lead_id}", response_class=HTMLResponse)
async def edit_lead_form(request: Request, lead_id: int):
    controller = LeadController(engine)
    lead = controller.get_lead(lead_id)
    return templates.TemplateResponse("crm/lead_form.html", {
        "request": request,
        "lead": lead,
        "active_module": "crm"
    })

@app.post("/crm/leads/{lead_id}", response_class=HTMLResponse)
async def update_lead(request: Request, lead_id: int):
    form = await request.form()
    data = dict(form)
    if 'expected_revenue' in data:
        data['expected_revenue'] = float(data['expected_revenue'])
        
    controller = LeadController(engine)
    controller.update_lead(lead_id, data)
    return RedirectResponse(url="/crm/leads", status_code=303)

# --- SALES ROUTES ---
@app.get("/sales/quotations", response_class=HTMLResponse)
async def list_quotations(request: Request):
    controller = SaleController(engine)
    orders = controller.list_orders()
    return templates.TemplateResponse("sales/quotations.html", {
        "request": request, 
        "orders": orders,
        "active_module": "sales"
    })

@app.get("/sales/quotations/new", response_class=HTMLResponse)
async def new_quotation_form(request: Request):
    return templates.TemplateResponse("sales/quotation_form.html", {
        "request": request,
        "order": None,
        "active_module": "sales"
    })

@app.post("/sales/quotations", response_class=HTMLResponse)
async def create_quotation(request: Request):
    form = await request.form()
    data = dict(form)
    controller = SaleController(engine)
    controller.create_order(data)
    return RedirectResponse(url="/sales/quotations", status_code=303)

@app.get("/sales/quotations/{order_id}", response_class=HTMLResponse)
async def edit_quotation_form(request: Request, order_id: int):
    controller = SaleController(engine)
    order = controller.get_order(order_id)
    return templates.TemplateResponse("sales/quotation_form.html", {
        "request": request,
        "order": order,
        "active_module": "sales"
    })

@app.post("/sales/quotations/{order_id}/confirm", response_class=HTMLResponse)
async def confirm_quotation(request: Request, order_id: int):
    controller = SaleController(engine)
    controller.confirm_order(order_id)
    return RedirectResponse(url=f"/sales/quotations/{order_id}", status_code=303)

def start():
    uvicorn.run("mindzen_erp.web:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
