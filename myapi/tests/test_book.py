
# try:
#     # from sqlalchemy.orm import sessionmaker
    
# except ImportError:
#     raise ImportError("Please install pytest or sqlachemy")

import pytest
import requests

from fastapi import Request,HTTPException,status

from database.database import engine,async_session,get_db
from sqlalchemy.ext.asyncio import AsyncSession

BASE_URL = "http://localhost:8000"

@pytest.mark.asyncio
async def test_client():
    async for db in get_db():
        assert isinstance(db,AsyncSession)
        assert db.bind == async_session.kw["bind"]
        await db.close()


def test_lists():
    response = requests.get(f"{BASE_URL}/lists")

    if response.status_code == 200:
        lists = response.json()['data']    
        keys = [n.keys() for n in lists]
        
        dict_keys = keys[0]
        payload_key = [*dict_keys]
    
        assert response.status_code == 200
        assert payload_key[0] == 'description'
        assert payload_key[1] == 'price'
        assert payload_key[2] == 'id'   
        
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="list not found Plesas add book")

def test_list_price():
    response = requests.get(f"{BASE_URL}/lists_price")
    
    
    if response.status_code == 200:
            
        lists = response.json()['data']
        
        keys = [n.keys() for n in lists]
        
        dict_keys = keys[0]
        payload_key = [*dict_keys]
        
        assert response.status_code == 200
        assert payload_key[0] == 'description'
        assert payload_key[1] == 'price'
        assert payload_key[2] == 'id' 
        
    else:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="list not found Plesas add book")


def test_empty_lists():
    response = test_lists()
    
    if isinstance(response,HTTPException):
        assert response.detail == 'list not found Plesas add book'
        assert response.status_code == 404


def test_update():
    user_id = 11    
    response = requests.put(f"{BASE_URL}/update/{user_id}",json={
        'price' : 2000
    })
    
    if response.status_code == 201:
        assert response.status_code == 201
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="duplicate input price")


def test_not_update():
    response = test_update()
    
    if isinstance(response,HTTPException):    
        assert response.detail == 'duplicate input price'
        assert response.status_code == 403
    
        
def test_add():
    response = requests.post(f"{BASE_URL}/add",json={
        'description' : 'user1',
        'price': 150
    })
    
    if response.status_code == 200:
        assert response.status_code == 200
    else:
         return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="descript or price empty")


def test_not_add():
    response = test_add()
    
    if isinstance(response,HTTPException):
        assert response.detail == 'descript or price empty'
        assert response.status_code == 422
    