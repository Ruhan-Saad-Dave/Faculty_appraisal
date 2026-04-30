from sqlalchemy.orm import Session
from typing import List, Optional

from ...models.Part_A.industry_connect import IndustryConnect
from ...schema.Part_A.industry_connect import (
    IndustryConnectCreate,
    IndustryConnectUpdateFaculty,
    IndustryConnectUpdateHOD,
    IndustryConnectUpdateDirector,
)

def get_industry_connect(db: Session, id: int) -> Optional[IndustryConnect]:
    return db.query(IndustryConnect).filter(IndustryConnect.id == id).first()

def get_industry_connect_by_faculty(db: Session, faculty_id: int) -> List[IndustryConnect]:
    return db.query(IndustryConnect).filter(IndustryConnect.faculty_id == faculty_id).all()

def create_industry_connect(
    db: Session, connect: IndustryConnectCreate, faculty_id: int
) -> IndustryConnect:
    db_connect = IndustryConnect(**connect.model_dump(), faculty_id=faculty_id)
    db.add(db_connect)
    db.commit()
    db.refresh(db_connect)
    return db_connect

def update_industry_connect_faculty(
    db: Session, id: int, connect_update: IndustryConnectUpdateFaculty
) -> Optional[IndustryConnect]:
    db_connect = get_industry_connect(db, id)
    if db_connect:
        update_data = connect_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_connect, key, value)
        db.commit()
        db.refresh(db_connect)
    return db_connect

def update_industry_connect_hod(
    db: Session, id: int, connect_update: IndustryConnectUpdateHOD
) -> Optional[IndustryConnect]:
    db_connect = get_industry_connect(db, id)
    if db_connect:
        db_connect.api_score_hod = connect_update.api_score_hod
        db.commit()
        db.refresh(db_connect)
    return db_connect

def update_industry_connect_director(
    db: Session, id: int, connect_update: IndustryConnectUpdateDirector
) -> Optional[IndustryConnect]:
    db_connect = get_industry_connect(db, id)
    if db_connect:
        db_connect.api_score_director = connect_update.api_score_director
        db.commit()
        db.refresh(db_connect)
    return db_connect

def delete_industry_connect(db: Session, id: int) -> bool:
    db_connect = get_industry_connect(db, id)
    if db_connect:
        db.delete(db_connect)
        db.commit()
        return True
    return False

def get_industry_connect_total_score(db: Session, faculty_id: int) -> float:
    entries = get_industry_connect_by_faculty(db, faculty_id)
    return sum([e.api_score_faculty for e in entries])
