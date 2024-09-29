from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config

frontend_router = APIRouter()

# Load environment variables
config = Config('.env')

# Set up OAuth
oauth = OAuth(config)
oauth.register(
    name='okta',
    server_metadata_url=f'{config("OKTA_DOMAIN")}/.well-known/openid-configuration',
    client_id=config('OKTA_CLIENT_ID'),
    client_secret=config('OKTA_CLIENT_SECRET'),
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Set up templates
templates = Jinja2Templates(directory="templates")

@frontend_router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    user = request.session.get('user')
    if user:
        return RedirectResponse(url='/dashboard')
    return templates.TemplateResponse("index.html", {"request": request})

@frontend_router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.okta.authorize_redirect(request, redirect_uri)

@frontend_router.get('/auth')
async def auth(request: Request):
    token = await oauth.okta.authorize_access_token(request)
    user = await oauth.okta.parse_id_token(request, token)
    request.session['user'] = dict(user)
    return RedirectResponse(url='/dashboard')

@frontend_router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/')
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@frontend_router.post("/update_data")
async def update_data(request: Request, data: str = Form(...)):
    user = request.session.get('user')
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    # Here you would call your API to update data
    return RedirectResponse(url='/dashboard', status_code=status.HTTP_303_SEE_OTHER)

@frontend_router.get('/logout')
async def logout(request: Request):
    request.session.pop('user', None)
    return RedirectResponse(url='/')