from pathlib import Path
from pydantic import BaseModel,AnyHttpUrl , Field , ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine.url import URL
from functools import lru_cache

import os

PROJECT_DIR = Path(__file__).parent.parent.parent
DOTENV = os.path.join(os.path.dirname(__file__), ".env")

class Secuirte(BaseModel):
    allowed_hosts: list[str] = ["localhost", "127.0.0.1"]
    backend_cors_origins: list[AnyHttpUrl] = []

class Database(BaseModel):
    hostname: str = Field(default='postgres')
    username: str = Field(default='postgres')
    password: str = Field(default='')
    port: int = Field(default=5432)
    db: str = Field(default='postgres')
    
    # class Config:
    #     env_file = DOTENV


class Settings(BaseModel):
    # securit: Secuirte
    database: Database = Field(default_factory=Database)
    
    @property
    def sqlalchemy_database_url(self) -> URL:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.database.username,
            password=self.database.password,
            host=self.database.hostname,
            port=self.database.port,
            database=self.database.db,
        )   
         
    model_config = SettingsConfigDict(
       env_file = DOTENV
    )
    
    
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    try:
        return Settings()
    
    except ValidationError as e:
        print(repr(e.errors()))