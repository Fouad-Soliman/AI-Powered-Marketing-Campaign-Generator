from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    

    GOOGLE_API_KEY : str 
    
    class Config:
        env_file = ".env"
        
def get_settings():
    return Settings()