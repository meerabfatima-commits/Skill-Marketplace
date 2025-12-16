from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    pw_bytes = password.encode("utf-8")[:72]  # truncate to 72 bytes
    return pwd_context.hash(pw_bytes)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
