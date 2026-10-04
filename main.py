from pathlib import Path

from fastapi import (
    FastAPI,
    Request,
    HTTPException
)

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .database import Base, engine
from .routes import auth, planners, history


# --------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# --------------------------------------------------
# SETTINGS
# --------------------------------------------------

settings = get_settings()


# --------------------------------------------------
# FASTAPI APP
# --------------------------------------------------

app = FastAPI(
    title=settings.app_name,
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.frontend_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

templates = Jinja2Templates(
    directory=BASE_DIR / "templates"
)


# --------------------------------------------------
# DATABASE STARTUP
# --------------------------------------------------

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# ROUTERS
# --------------------------------------------------

app.include_router(auth.router)
app.include_router(planners.router)
app.include_router(history.router)


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={}
    )


# --------------------------------------------------
# REGISTER PAGE
# --------------------------------------------------

@app.get("/register", response_class=HTMLResponse)
def register_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={}
    )


# --------------------------------------------------
# DASHBOARD PAGE
# --------------------------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )


# --------------------------------------------------
# HISTORY PAGE
# --------------------------------------------------

@app.get("/history", response_class=HTMLResponse)
def history_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="history.html",
        context={}
    )


# --------------------------------------------------
# PLANNER PAGES
# --------------------------------------------------

@app.get("/planner/{name}", response_class=HTMLResponse)
def planner_page(
    request: Request,
    name: str
):

    if name not in {
        "home",
        "party",
        "jewelry"
    }:
        raise HTTPException(
            status_code=404,
            detail="Planner not found"
        )

    return templates.TemplateResponse(
        request=request,
        name=f"{name}_planner.html",
        context={}
    )