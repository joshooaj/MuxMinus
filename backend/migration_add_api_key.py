"""Add API key support to User model.

This migration adds the api_key column to the users table to support REST API access.

Run this migration manually:
```bash
docker compose exec backend python migration_add_api_key.py
```
"""

import sys
from sqlalchemy import create_engine, text
import os

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://demucs:demucs@postgres:5432/demucs")

def migrate():
    """Add api_key column to users table."""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("Adding api_key column to users table...")
        
        # Check if column already exists
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='users' AND column_name='api_key'
        """))
        
        if result.fetchone():
            print("  ✓ api_key column already exists, skipping migration")
            return
        
        # Add the api_key column
        conn.execute(text("""
            ALTER TABLE users 
            ADD COLUMN api_key VARCHAR UNIQUE
        """))
        
        # Create index on api_key for faster lookups
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_users_api_key 
            ON users(api_key)
        """))
        
        conn.commit()
        print("  ✓ Migration completed successfully")

if __name__ == "__main__":
    try:
        migrate()
        print("\n✅ Migration successful!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
