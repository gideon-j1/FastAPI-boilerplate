from fastapi.responses import JSONResponse
from fastapi import Request , HTTPException


class UnicornException(Exception):
    def __init__(self, status_code: int):
        self.status_code = status_code        
        self.unicorn_excpetion_handler()

    def unicorn_excpetion_handler(self) -> None:
        
        if self.status_code == 500:
            raise HTTPException({"message" : f"{self.status_code} error@@@@@@@@@@@@@@@@@@@@@"})
        
        if self.status_code == 404:
            raise HTTPException({"message" : f"{self.status_code} error@@@@@@@@@@@@@@@@@@@@@"})

        if self.status_code == 400:
            raise HTTPException({"message" : f"{self.status_code} error@@@@@@@@@@@@@@@@@@@@@"})
