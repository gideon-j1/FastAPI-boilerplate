import requests


from fastapi import HTTPException,status



BASE_URL = "http://localhost:8000"

r"""
    api v1 : /register (POST)
"""

def test_create_user():
    mock_email = 'gidenon123@gmail.com'
    mcok_password = '12345'
    
    response = requests.post(f"{BASE_URL}/register",json={
        'email' : mock_email,
        'password' : mcok_password
    })
    
    if response.status_code == 200:
        assert response.status_code == 200
    
    else:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='not created user'
        )

def test_not_create():
    response = test_create_user()
    
    if isinstance(response,HTTPException):
        assert response.status_code==500
        assert response.detail=='not created user'

r"""
    api v1 : /login (POST)
"""

def test_login():
    
    import jwt
    from core.securit import ALGORITHM
    from content import SECRET_KEY
    
    mock_email = 'gidenon123@gmail.com'
    mock_password = '12345'
    
    response = requests.post(f"{BASE_URL}/login",json={
        'email' : mock_email,
        'password' : mock_password    
    })
    
    match response.status_code:
        
        case 422:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = 'empty value (email,password)'
                )
        
        case 401:
            return HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = 'user password is wrong'
            )
        
        case 404:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail ='user not found please create user'
            )
            
        case 500:
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail = 'server Error !!'
            )
    
    
    if response.status_code == 200:
        assert response.status_code == 200        
        access = response.json()['access']
        refersh = response.json()['refresh']
        
        decodedAccessInfo = jwt.decode(access,algorithms=ALGORITHM,verify=True,key=SECRET_KEY)
        decodedRefreshInfo = jwt.decode(refersh,algorithms=ALGORITHM,verify=True,key=SECRET_KEY)
       
        assert 'id' in decodedRefreshInfo
        assert 'iss' in decodedRefreshInfo
        assert 'exp' in decodedRefreshInfo
        assert 'iat' in decodedRefreshInfo        
        
        assert 'id' in decodedAccessInfo
        assert 'iss' in decodedAccessInfo
        assert 'exp' in decodedAccessInfo
        assert 'iat' in decodedAccessInfo
        
        
def test_get_typeingredis():
    response = test_login()
            
    if isinstance(response,HTTPException):
        match response.status_code:
            case 422:                
                assert response.detail == 'empty value (email,password)'
                assert response.status_code == 422
            case 401:
                assert response.detail == 'user password is wrong'
                assert response.status_code == 401
            case 404:
                assert response.detail == 'user not found please create user'
                assert response.status_code == 404
            case 500:
                assert response.detail == 'server Error !!'
                assert response.status_code == 500
