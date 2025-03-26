import bcrypt

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
    print(to_encode)
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
        print(expire,"11111111111111")
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    print(encoded_jwt)
    
    return encoded_jwt
