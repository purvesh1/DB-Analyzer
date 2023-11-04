from dotenv import load_dotenv
import os
import abc

load_dotenv()

class Singleton(abc.ABCMeta, type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Config(metaclass=Singleton):
    def __init__(self):
        self.debug_mode = False
        self.llm_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
        self.token_limit = int(os.getenv("TOKEN_LIMIT", 4000))
        self.temperature = int(os.getenv("OPENAI_TEMPERATURE", 0))
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.hf_api_key = os.getenv("HF_API_KEY")
        
        self.pg_password = os.getenv("DB_PASSWORD")
        self.pg_host = os.getenv("PG_HOST", "127.0.0.1")
        self.pg_user = os.getenv("PG_USER", "postgres")
        self.pg_port = int(os.getenv("PG_PORT", "5432"))
        self.pg_database = os.getenv("PG_DATABASE", "capstone_test")

    def set_openai_api_key(self, value: str):
        self.openai_api_key = value

    def set_google_api_key(self, value: str):
        self.google_api_key = value

    def set_debug_mode(self, value: bool):
        self.debug_mode = value

    def set_pg_password(self, value: str):
        self.pg_password = value

    def set_pg_host(self, value: str):
        self.pg_host = value

    def set_pg_user(self, value: str):
        self.pg_user = value

    def set_pg_port(self, value: int):
        self.pg_port = value

    def set_pg_database(self, value: str):
        self.pg_database = value

cfg = Config()