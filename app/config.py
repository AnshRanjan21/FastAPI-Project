from pydantic_settings import BaseSettings #basesettings-has-moved-to-pydantic-settings

class Settings(BaseSettings):   #using pydantic to validate our env variables, this is us defining a schema essentially
    DATABASE_HOSTNAME: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str  
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"

settings=Settings() 

    #all env vars are passed as strings
    #all these assigned values are just default placeholder values
    #if we remove any default value then it will check for them in enviornment variables and if not present throw error
    #it massively helps when working with a lot of env vars
    #all env vars are in written in CAPS, but here these should be fine as pydantic will convert them into uppercase before checking
    #we cannot have things like password, secret key, etc hardcoded into out code, hence we are using env vars