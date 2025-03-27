import bcrypt

try:    
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.fernet import Fernet
except ImportError:
    raise ImportError("Please install cryptography")
r"""
    [x] : hash save
    [x] : hash check
    [] : 복호화해서 비밀번호 원래상태로 만들고 입력한 비밀번호랑 비교해서 
        동일하면 True
"""

# 로그인할때 해싱으로 디비에 저장되어있는 비번 검증용 
def verify_password(password: str , hashed_password: str)-> bool:
    
    client_p = password.encode("utf-8")
    db_p = hashed_password.encode("utf-8")

    return bcrypt.checkpw(
        client_p,db_p
    )
    
def save_hash_password(passoword: str) -> str:
    
    bytes = passoword.encode("utf-8")
    
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes,salt)
        
    return hash.decode("utf-8")


try:
    from datetime import datetime, timedelta, timezone
    import jwt
    
except ImportError:
    raise ImportError("Please install jwt or import datetime")

from core.schemas import Token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def create_access_token(
    data: dict , 
    expires_delta: timedelta | None =None,
) -> Token:

    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
        
    return encoded_jwt
