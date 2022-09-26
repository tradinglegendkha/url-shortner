from sqlalchemy.orm import Session
from . import crud
import secrets
import string

def create_random_key(length: int = 5) -> str:
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unqiue_random_key(db: Session) -> str:
    key = create_random_key()
    while crud.get_db_url_by_secret_key(db, key):
        key = create_random_key()
    return key