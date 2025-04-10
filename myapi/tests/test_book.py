
# try:
#     # from sqlalchemy.orm import sessionmaker
    
# except ImportError:
#     raise ImportError("Please install pytest or sqlachemy")

import pytest
import requests

from fastapi import Request

from database.database import engine,async_session,get_db
from sqlalchemy.ext.asyncio import AsyncSession



@pytest.mark.asyncio
async def test_client():
    async for db in get_db():
        assert isinstance(db,AsyncSession)
        assert db.bind == async_session.kw["bind"]
        await db.close()


def test_lists():
    response = requests.get('http://localhost:8000/lists')
    
    lists = response.json()['data']    
    keys = [n.keys() for n in lists]
    

    dict_keys = keys[0]
    payload_key = [*dict_keys]
    
    assert response.status_code == 200
    assert payload_key[0] == 'description'
    assert payload_key[1] == 'price'
    assert payload_key[2] == 'id'  
    
      
    
