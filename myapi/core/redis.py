from database.database import redis_client
from typing import Dict,Any
import json

def add_redis_item(
    token: Dict[Any,Any] = None) -> None:
   
    payload = {
        "id" : token["id"],
        "key" : token["exp"],
        "access" : token["access"],
        "refresh" : token["refresh"]
    }
    
    json_data = json.dumps(payload)
        
    redis_client.rpush("mytoken", json_data) 

    return {"message" : "성공입니다."}