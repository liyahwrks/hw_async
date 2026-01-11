from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, select
from models.base import Base

class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False) 
    username = Column(String(50), nullable=False)  
    email = Column(String(100), nullable=False) 
    
    posts = relationship(
        "Post", 
        back_populates="user",
        cascade="all, delete-orphan", 
        lazy="selectin" 
    )
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    def __str__(self):
        return f"{self.name} (@{self.username})"


class Post(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, 
        ForeignKey("user.id", ondelete="CASCADE"),  
        nullable=False
    ) 
    title = Column(String(200), nullable=False)  
    body = Column(Text, nullable=False) 
    
    user = relationship(
        "User", 
        back_populates="posts",
        lazy="joined"  
    )
    
    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title[:20]}...', user_id={self.user_id})>"