import bcrypt

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
