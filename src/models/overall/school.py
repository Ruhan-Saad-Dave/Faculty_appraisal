from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from src.setup.database import Base

class DivisionEnum(str, enum.Enum):
    ENGINEERING = "Engineering"
    NON_ENGINEERING = "Non-Engineering"

class FormTypeEnum(str, enum.Enum):
    TYPE_1 = "Type 1"
    TYPE_2 = "Type 2"
    TYPE_3 = "Type 3"

class School(Base):
    __tablename__ = "school"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    division = Column(Enum(DivisionEnum), nullable=False)
    form_type = Column(Enum(FormTypeEnum), default=FormTypeEnum.TYPE_1)

    # Relationships
    faculties = relationship("Faculty", back_populates="school")
