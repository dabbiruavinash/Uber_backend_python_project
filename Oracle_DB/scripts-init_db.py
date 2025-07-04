# Database Initialization Script

Create a script to initialize the database:

import cx_Oracle
from core.config import settings

def initialize_database():
    # Connect as admin to create schema and user
    admin_conn = cx_Oracle.connect(
        user="system",
        password=settings.ORACLE_ADMIN_PASSWORD,
        dsn=settings.ORACLE_DSN
    )
    
    try:
        cursor = admin_conn.cursor()
        
        # Create user
        cursor.execute(f"""
        CREATE USER {settings.ORACLE_USER} IDENTIFIED BY {settings.ORACLE_PASSWORD}
        DEFAULT TABLESPACE users
        TEMPORARY TABLESPACE temp
        QUOTA UNLIMITED ON users
        """)
        
        # Grant privileges
        cursor.execute(f"""
        GRANT CREATE SESSION, CREATE TABLE, CREATE SEQUENCE, CREATE PROCEDURE, 
              CREATE TRIGGER, CREATE VIEW, CREATE MATERIALIZED VIEW
        TO {settings.ORACLE_USER}
        """)
        
        admin_conn.commit()
        print("Database user created successfully")
        
    finally:
        admin_conn.close()

if __name__ == "__main__":
    initialize_database()