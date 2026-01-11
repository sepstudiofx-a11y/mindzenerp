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

def start():
    uvicorn.run("mindzen_erp.web:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start()
