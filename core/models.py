from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class User(BaseModel):
    __tablename__ = "core_users"
    
    username = Column(String(150), unique=True, index=True, nullable=False)
    email = Column(String(254), unique=True, index=True, nullable=False)
    first_name = Column(String(30))
    last_name = Column(String(150))
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    date_joined = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class Category(BaseModel):
    __tablename__ = "core_categories"
    
    name = Column(String(100), nullable=False)
    description = Column(Text)
    slug = Column(String(100), unique=True, index=True)

class Post(BaseModel):
    __tablename__ = "core_posts"
    
    title = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("core_users.id"))
    category_id = Column(Integer, ForeignKey("core_categories.id"))
    is_published = Column(Boolean, default=False)
    published_at = Column(DateTime)
    
    # Relationships would be defined here in SQLAlchemy
    # author = relationship("User", back_populates="posts")
    # category = relationship("Category", back_populates="posts")