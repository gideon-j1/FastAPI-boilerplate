from database.database import redis_client
from typing import Dict,Any


def add_redis_item(
    token: Dict[Any,Any] = None) -> None:
        
    item = redis_client.set(f"{token["access"]}" , f"{token["refresh"]}")
    
    return {"message" : "성공입니다."}