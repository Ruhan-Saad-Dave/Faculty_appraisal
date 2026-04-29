from sqlalchemy import Column, Integer, String, Text, Double, ForeignKey, Enum
from sqlalchemy.orm import relationship
from ..setup.database import Base
import enum

class IndexingEnum(str, enum.Enum):
    SCOPUS = "Scopus"
    SCI = "SCI"
    SCIE = "SCIE"
    UGC = "UGC"

class JournalPublication(Base):
    __tablename__ = "journal_publications"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id")) # Assuming a faculty table exists

    sr_no = Column(Integer, index=True)
    title_with_page_nos = Column(Text)
    journal_details = Column(Text)
    issn_isbn_no = Column(String(50))
    indexing = Column(Enum(IndexingEnum), default=IndexingEnum.SCOPUS)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    # Relationship to Faculty (assuming a Faculty model will be created later)
    # faculty = relationship("Faculty", back_populates="journal_publications")
