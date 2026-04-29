from sqlalchemy import Column, Integer, String, ForeignKey, Text, Double
from sqlalchemy.orm import relationship
from ....setup.database import Base
from ..faculty import Faculty  # Import Faculty model for relationship

class ProductDevelopment(Base):
    __tablename__ = "product_developments"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("faculty.id"))
    product_description = Column(Text, nullable=False)
    usage_type = Column(String(50), nullable=False) # Used in Lab / Commercialized
    api_score_faculty = Column(Double, default=0.0)
    api_score_hod = Column(Double, default=0.0)
    api_score_director = Column(Double, default=0.0)

    faculty = relationship("Faculty", back_populates="product_developments")
