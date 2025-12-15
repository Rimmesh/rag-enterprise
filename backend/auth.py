from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError
from passlib.context import CryptContext
import os
import json

# ---- JWT CONFIG ----
SECRET_KEY = os.getenv("AUTH_SECRET_KEY", "super-secret-dev-key")  # change for prod
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 1 day

USERS_PATH = "data/users.json"

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------- MODELS ----------
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[EmailStr] = None
    role: Optional[str] = None


# ---------- UTILS: USERS STORAGE (JSON FILE) ----------
def load_users() -> Dict[str, dict]:
    if not os.path.exists(USERS_PATH):
        return {}
    with open(USERS_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(users: Dict[str, dict]):
    os.makedirs(os.path.dirname(USERS_PATH), exist_ok=True)
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user(email: str) -> Optional[dict]:
    users = load_users()
    return users.get(email)


# ---------- DEPENDENCY ----------
def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(email)
    if user is None:
        raise credentials_exception

    return UserOut(email=user["email"], name=user["name"], role=role)


# ---------- ENDPOINTS ----------
@router.post("/register", response_model=UserOut)
def register(user: UserCreate):
    users = load_users()

    if user.email in users:
        raise HTTPException(status_code=400, detail="User already exists")

    # First user becomes admin, others are user
    role = "admin" if len(users) == 0 else "user"

    users[user.email] = {
        "email": user.email,
        "name": user.name or user.email.split("@")[0],
        "password_hash": hash_password(user.password),
        "role": role,
    }
    save_users(users)

    return UserOut(email=user.email, name=users[user.email]["name"], role=role)


@router.post("/login", response_model=Token)
def login(credentials: UserLogin):
    user = get_user(credentials.email)
    if not user or not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(
        {"sub": credentials.email, "role": user["role"]}
    )
    return Token(access_token=token)


@router.get("/me", response_model=UserOut)
def read_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
