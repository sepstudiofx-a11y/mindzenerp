from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn
import os
from pathlib import Path

from mindzen_erp.core import Engine, ConfigManager
from mindzen_erp.core.orm import Database
from mindzen_erp.modules.crm.controllers import LeadController

# Initialize Engine & DB
engine = Engine()
engine.initialize()
engine.discover_modules()
engine.install_module('crm')

# Database Connection (Default to SQLite for simple local run, override for Postgres)
# For Postgres: postgresql://user:password@localhost/dbname
db_url = os.getenv("DATABASE_URL", "sqlite:///./mindzen_erp.db")
Database().connect(db_url)

app = FastAPI(title="MindZen ERP")

# Paths
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request, 
        "active_module": "dashboard"
    })

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
    # Convert types
    if 'expected_revenue' in data:
        data['expected_revenue'] = float(data['expected_revenue'])
    
    controller = LeadController(engine)
    controller.create_lead(data)
    
    # Redirect to list view
    from starlette.responses import RedirectResponse
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

def start():
    uvicorn.run("mindzen_erp.web:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
