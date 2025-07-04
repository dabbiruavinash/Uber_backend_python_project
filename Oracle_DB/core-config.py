# Configuration

class Settings(BaseSettings):
    # Oracle Database Configuration
    ORACLE_USER: str = os.getenv("ORACLE_USER", "uber_user")
    ORACLE_PASSWORD: str = os.getenv("ORACLE_PASSWORD", "securepassword")
    ORACLE_DSN: str = os.getenv("ORACLE_DSN", "localhost:1521/ORCLPDB1")
    ORACLE_MIN_CONNECTIONS: int = int(os.getenv("ORACLE_MIN_CONNECTIONS", 1))
    ORACLE_MAX_CONNECTIONS: int = int(os.getenv("ORACLE_MAX_CONNECTIONS", 10))
    
    # ... rest of the settings ...