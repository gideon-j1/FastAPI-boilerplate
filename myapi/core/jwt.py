import time
import secrets

try:
    from datetime import datetime, timedelta, timezone
    import jwt
    
except ImportError:
    raise ImportError("Please install jwt or import datetime")

from core.schemas import Token

from content import SECRET_KEY

ALGORITHM = "HS256"

def create_token(
    data: dict , 
    expires_delta: timedelta | None =None,
) -> Token:

    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=20)
    
    iat = int(time.time())
    
    to_encode.update({
        "exp": expire,
        "iat": iat
    })
        
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return Token(
        access_token=encoded_jwt,
        expires_at=to_encode['exp'],
        refresh_token=encoded_jwt,
        refresh_token_expires_at=to_encode['exp']
    )
