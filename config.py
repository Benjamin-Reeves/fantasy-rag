"""Configuration management for the fantasy football RAG system."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration class for database and API settings."""
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'fantasy_football')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    
    # Vector Database Configuration
    VECTOR_DIMENSION = int(os.getenv('VECTOR_DIMENSION', 1536))
    
    @property
    def db_connection_string(self):
        """Get database connection string."""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
