from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Enum, Double
from sqlalchemy.orm import relationship
from ....setup.database import Base
from ..faculty import Faculty  # Import Faculty model for relationship

class BookPublication(Base):
    __tablename__ = "book_publications"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    chapter_title = Column(Text, nullable=False)
    book_details = Column(Text, nullable=False)
    isbn = Column(String(50), nullable=False)
    publisher_type = Column(String(50), nullable=False) # ENUM / String
    co_author_count = Column(Integer, nullable=False)
    is_first_author = Column(Boolean, nullable=False)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty", back_populates="book_publications")
