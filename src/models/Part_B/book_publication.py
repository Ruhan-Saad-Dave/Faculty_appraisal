from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from src.setup.database import Base

class BookPublication(Base):
    __tablename__ = "book_publications"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    title_and_pages = Column(String, index=True)
    book_title_editor = Column(String)
    issn_isbn = Column(String)
    publisher_type = Column(String)
    co_authors_count = Column(Integer)
    is_first_author = Column(Boolean, default=False)
    department = Column(String, nullable=True) # Added as per user request
    document = Column(String, nullable=True) # Added as per user request (Google Drive link)

    api_score_faculty = Column(Integer, default=0)
    api_score_hod = Column(Integer, default=0)
    api_score_director = Column(Integer, default=0)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    faculty = relationship("Faculty", back_populates="book_publications")