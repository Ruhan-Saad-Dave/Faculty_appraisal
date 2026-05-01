from sqlalchemy.orm import Session
from typing import Optional
from ...models.Part_B.faculty import Faculty
from ...schema.overall.faculty import FacultyUpdate

def get_faculty(db: Session, faculty_id: str) -> Optional[Faculty]:
    return db.query(Faculty).filter(Faculty.id == faculty_id).first()

def update_faculty(db: Session, faculty_id: str, faculty_data: FacultyUpdate) -> Optional[Faculty]:
    db_faculty = get_faculty(db, faculty_id)
    if not db_faculty:
        return None
    
    update_dict = faculty_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(db_faculty, key, value)
    
    db.commit()
    db.refresh(db_faculty)
    return db_faculty
