import bcrypt
import jwt
import socket

from content import SECRET_KEY
from fastapi import HTTPException,status
from urllib.parse import urlparse


ALGORITHM = "HS256"

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

def verify_jwt_token(token: str) -> bool:
    
    try:
        decoded_jwt = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        if len(decoded_jwt) > 0:
            return True
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token expried"
            )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid token a signauture"
        )
    
