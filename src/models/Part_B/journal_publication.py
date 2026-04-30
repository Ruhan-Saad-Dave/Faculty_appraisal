from sqlalchemy import Column, Integer, String, Text, Double, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from src.setup.database import Base

class IndexingEnum(str, enum.Enum):
    SCOPUS = "Scopus"
    SCI = "SCI"
    SCIE = "SCIE"
    UGC = "UGC"

class JournalPublication(Base):
    __tablename__ = "published_papers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    faculty_id = Column(UUID(as_uuid=True), ForeignKey("faculty.id")) 

    sr_no = Column(Integer, index=True)
    title_with_page_nos = Column(Text)
    journal_details = Column(Text)
    issn_isbn_no = Column(String(50))
    indexing = Column(Enum(IndexingEnum), default=IndexingEnum.SCOPUS)
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)
    department = Column(String, nullable=True)
    document = Column(String, nullable=True)

    # Relationship to Faculty (assuming a Faculty model will be created later)
    # faculty = relationship("Faculty", back_populates="journal_publications")
