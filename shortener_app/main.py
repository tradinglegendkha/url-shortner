from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.datastructures import URL

from . import models, schemas, crud
from .database import SessionLocal, engine
from .config import get_settings
app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def raise_not_found(request):
    message = f"URL '{request.url}' doesn't exist"
    raise HTTPException(status_code=404, detail=message)

def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    if not validators.url(url.target_url):
        raise_bad_request(message="Your provided URL is not valid")
    """
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = "".join(secrets.choice(chars) for _ in range(5))
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    db_url = models.URL (
        target_url = url.target_url, key=key, secret_key=secret_key
    )"""
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key

    return db_url


@app.get("/{url_key}")
def forward_to_target_url (
        url_key: str,
        request: Request, 
        db: Session = Depends(get_db)
    ):
    if db_url:= crud.get_db_url_by_key(db=db, url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        raise_not_found(request)

@app.get (
    "/admin.{secret_key}",
    name="administration info",
    response_model=schemas.URLInfo
)
def get_url_info (
    secret_key: str, reqest: Request, db: Session = Depends(get_db)
):
    if db_url:= crud.get_db_url_by_secret_key(db, secret_key=secret_key):
        db_url.url = db_url.key
        db_url.admin_url = db_url.secret_key
        return db_url
    else:
        raise_not_found(request)
