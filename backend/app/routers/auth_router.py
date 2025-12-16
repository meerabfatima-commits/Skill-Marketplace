# backend/app/routers/auth_routers.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import user as user_model
from schemas import user as user_schema
from app.database import SessionLocal
from utils.hashing import hash_password, verify_password
from utils.jwt_handler import create_access_token
from utils.validators import is_valid_email

router = APIRouter(prefix="/auth", tags=["auth"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# REGISTER
# -----------------------------
@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    print("REGISTER HIT")
    # Validate email
    if not is_valid_email(user.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check if email already exists
    existing_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    db_user = user_model.User(
        username=user.username,
        email=user.email,
        password=hash_password(user.password),
        is_provider=user.is_provider
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# -----------------------------
# LOGIN
# -----------------------------
@router.post("/login")
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(user_model.User).filter(user_model.User.email == user.email).first()
    
    # Verify user and password
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Create JWT token
    token = create_access_token({"user_id": db_user.id, "is_provider": db_user.is_provider})
    return {"access_token": token, "token_type": "bearer"}
