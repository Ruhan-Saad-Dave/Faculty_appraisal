from sqlalchemy.orm import Session
from typing import List, Optional
from ...models.overall.finalization import Enclosure, Declaration
from ...schema.overall.finalization import EnclosureCreate, DeclarationCreate

# Enclosures CRUD
def get_enclosures_by_faculty(db: Session, faculty_id: str) -> List[Enclosure]:
    return db.query(Enclosure).filter(Enclosure.faculty_id == faculty_id).all()

def create_enclosure(db: Session, faculty_id: str, enclosure: EnclosureCreate, document_path: Optional[str] = None) -> Enclosure:
    db_enclosure = Enclosure(**enclosure.model_dump(), faculty_id=faculty_id, document=document_path)
    db.add(db_enclosure)
    db.commit()
    db.refresh(db_enclosure)
    return db_enclosure

def delete_enclosure(db: Session, enclosure_id: str) -> bool:
    db_enclosure = db.query(Enclosure).filter(Enclosure.id == enclosure_id).first()
    if db_enclosure:
        db.delete(db_enclosure)
        db.commit()
        return True
    return False

# Declaration CRUD
def get_declaration_by_faculty(db: Session, faculty_id: str) -> Optional[Declaration]:
    return db.query(Declaration).filter(Declaration.faculty_id == faculty_id).first()

def create_or_update_declaration(db: Session, faculty_id: str, declaration: DeclarationCreate) -> Declaration:
    db_declaration = get_declaration_by_faculty(db, faculty_id)
    if db_declaration:
        for key, value in declaration.model_dump().items():
            setattr(db_declaration, key, value)
    else:
        db_declaration = Declaration(**declaration.model_dump(), faculty_id=faculty_id)
        db.add(db_declaration)
    
    db.commit()
    db.refresh(db_declaration)
    return db_declaration
