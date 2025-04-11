
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
        




r"""
    api v1 : /lists (GET)
"""

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

r"""
    api v1 : /lists_price (GET)
"""

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


r"""
    api v1 : /update{user_id} (put)

"""

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
    


r"""
    api v1 : /add (post)
"""

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


r"""
    api v1 : /partitions (GET)
"""

def test_get_redis():
    response = requests.get(f"{BASE_URL}/partitions")
    
    match response.status_code:
        case 400:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='not type dict')
    
        case 500:
            return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='not prepare partions query')
    
    if response.status_code == 200:                  
        first = response.json()['first']
        seconde = response.json()['second']
            
        keys_first = [*first[0]]
        keys_second = [*seconde[0]]

        assert response.status_code == 200

        for val in [keys_first,keys_second]:
            assert val[0] == 'tableoid'
            assert val[1] == 'id'
            assert val[2] == 'description'     
            assert val[3] == 'price'
            
        
def test_get_typeingredis():
    response = test_get_redis()
            
    if isinstance(response,HTTPException):
        match response.status_code:
            case 400:                
                assert response.detail == 'not type dict'
                assert response.status_code == 400
            case 500:
                assert response.detail == 'not prepare partions query'
                assert response.status_code == 500
            
r"""
    api v1 : /delete (DELETE)
"""

def test_delete_book():
    user_id = 20
    response = requests.delete(f"{BASE_URL}/delete/{user_id}")
    
    if response.status_code == 200:
        assert response.status_code == 200

    else:
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='book id not found')
    
    
def test_not_delete():
    response = test_delete_book()
    
    if isinstance(response,HTTPException):
        assert response.detail == 'book id not found'
        assert response.status_code == 500