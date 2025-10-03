"""
Complete PostgreSQL + SQLAlchemy Setup with User Model
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# ==========================================
# STEP 1: DATABASE CONNECTION
# ==========================================

# Database connection string format:
# postgresql://username:password@host:port/database_name

DATABASE_URL = "postgresql://postgres:your_password@localhost:5432/myapp_db"

# Create engine - this manages the database connection pool
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to True to see SQL queries (useful for debugging)
    pool_size=5,  # Number of connections to keep open
    max_overflow=10  # Maximum number of connections to create beyond pool_size
)

# ==========================================
# STEP 2: CREATE BASE CLASS
# ==========================================

# Base class for all models
Base = declarative_base()

# ==========================================
# STEP 3: CREATE SESSION FACTORY
# ==========================================

# SessionLocal is a factory for creating database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # Don't auto-commit transactions
    autoflush=False    # Don't auto-flush changes
)

# ==========================================
# STEP 4: DEFINE USER MODEL
# ==========================================

class User(Base):
    """
    User model representing the 'users' table in database
    
    Each class variable becomes a column in the table
    """
    __tablename__ = "users"  # Table name in database
    
    # Primary Key - auto-incrementing ID
    id = Column(Integer, primary_key=True, index=True)
    
    # User fields
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of User object"""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def __str__(self):
        """Human-readable string"""
        return f"{self.username} ({self.email})"


# ==========================================
# STEP 5: CREATE TABLES IN DATABASE
# ==========================================

def create_tables():
    """Create all tables defined by Base subclasses"""
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully!")


# ==========================================
# STEP 6: DATABASE SESSION MANAGEMENT
# ==========================================

def get_db():
    """
    Dependency function to get database session
    Use this pattern to ensure sessions are properly closed
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ==========================================
# STEP 7: CRUD OPERATIONS
# ==========================================

class UserCRUD:
    """Database operations for User model"""
    
    @staticmethod
    def create_user(db, username: str, email: str, password: str, full_name: str = None):
        """Create a new user"""
        # In production, hash the password using bcrypt or similar
        user = User(
            username=username,
            email=email,
            full_name=full_name,
            hashed_password=f"hashed_{password}"  # NEVER store plain passwords!
        )
        db.add(user)
        db.commit()
        db.refresh(user)  # Refresh to get the generated ID
        return user
    
    @staticmethod
    def get_user_by_id(db, user_id: int):
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_user_by_email(db, email: str):
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db, username: str):
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_all_users(db, skip: int = 0, limit: int = 100):
        """Get all users with pagination"""
        return db.query(User).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_user(db, user_id: int, **kwargs):
        """Update user fields"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def delete_user(db, user_id: int):
        """Delete user"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False


# ==========================================
# STEP 8: EXAMPLE USAGE
# ==========================================

def main():
    """Example usage of the User model"""
    
    print("=" * 50)
    print("PostgreSQL + SQLAlchemy User Model Demo")
    print("=" * 50)
    
    # Create tables
    create_tables()
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # CREATE - Add new users
        print("\n1. Creating users...")
        user1 = UserCRUD.create_user(
            db,
            username="john_doe",
            email="john@example.com",
            password="secure123",
            full_name="John Doe"
        )
        print(f"   Created: {user1}")
        
        user2 = UserCRUD.create_user(
            db,
            username="jane_smith",
            email="jane@example.com",
            password="secure456",
            full_name="Jane Smith"
        )
        print(f"   Created: {user2}")
        
        # READ - Get user by ID
        print("\n2. Reading user by ID...")
        user = UserCRUD.get_user_by_id(db, user1.id)
        print(f"   Found: {user}")
        print(f"   Details: ID={user.id}, Active={user.is_active}, Created={user.created_at}")
        
        # READ - Get user by email
        print("\n3. Reading user by email...")
        user = UserCRUD.get_user_by_email(db, "jane@example.com")
        print(f"   Found: {user}")
        
        # READ - Get all users
        print("\n4. Reading all users...")
        all_users = UserCRUD.get_all_users(db)
        for u in all_users:
            print(f"   - {u}")
        
        # UPDATE - Update user
        print("\n5. Updating user...")
        updated_user = UserCRUD.update_user(
            db,
            user1.id,
            full_name="John Doe Updated",
            is_superuser=True
        )
        print(f"   Updated: {updated_user}")
        print(f"   Is Superuser: {updated_user.is_superuser}")
        
        # DELETE - Delete user
        print("\n6. Deleting user...")
        deleted = UserCRUD.delete_user(db, user2.id)
        print(f"   Deleted: {deleted}")
        
        # Verify deletion
        print("\n7. Verifying deletion...")
        remaining_users = UserCRUD.get_all_users(db)
        print(f"   Remaining users: {len(remaining_users)}")
        for u in remaining_users:
            print(f"   - {u}")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    
    finally:
        db.close()
        print("\n✓ Database session closed")


if __name__ == "__main__":
    main()