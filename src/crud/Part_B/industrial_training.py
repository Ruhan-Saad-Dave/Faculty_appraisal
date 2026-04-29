from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.Part_B.industrial_training import IndustrialTraining
from ..schema.Part_B.industrial_training import (
    IndustrialTrainingCreate,
    IndustrialTrainingUpdateFaculty,
    IndustrialTrainingUpdateHOD,
    IndustrialTrainingUpdateDirector,
)

def get_industrial_training(db: Session, training_id: int) -> Optional[IndustrialTraining]:
    return db.query(IndustrialTraining).filter(IndustrialTraining.id == training_id).first()

def get_industrial_trainings_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[IndustrialTraining]:
    return db.query(IndustrialTraining).filter(IndustrialTraining.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_industrial_trainings(db: Session, skip: int = 0, limit: int = 100) -> List[IndustrialTraining]:
    return db.query(IndustrialTraining).offset(skip).limit(limit).all()

def create_industrial_training(db: Session, training: IndustrialTrainingCreate, faculty_id: int) -> IndustrialTraining:
    db_training = IndustrialTraining(**training.model_dump(), faculty_id=faculty_id)
    db.add(db_training)
    db.commit()
    db.refresh(db_training)
    return db_training

def update_industrial_training_faculty(
    db: Session, training_id: int, training_update: IndustrialTrainingUpdateFaculty
) -> Optional[IndustrialTraining]:
    db_training = db.query(IndustrialTraining).filter(IndustrialTraining.id == training_id).first()
    if db_training:
        update_data = training_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_training, key, value)
        db.commit()
        db.refresh(db_training)
    return db_training

def update_industrial_training_hod(
    db: Session, training_id: int, training_update: IndustrialTrainingUpdateHOD
) -> Optional[IndustrialTraining]:
    db_training = db.query(IndustrialTraining).filter(IndustrialTraining.id == training_id).first()
    if db_training:
        db_training.api_score_hod = training_update.api_score_hod
        db.commit()
        db.refresh(db_training)
    return db_training

def update_industrial_training_director(
    db: Session, training_id: int, training_update: IndustrialTrainingUpdateDirector
) -> Optional[IndustrialTraining]:
    db_training = db.query(IndustrialTraining).filter(IndustrialTraining.id == training_id).first()
    if db_training:
        db_training.api_score_director = training_update.api_score_director
        db.commit()
        db.refresh(db_training)
    return db_training

def delete_industrial_training(db: Session, training_id: int) -> Optional[IndustrialTraining]:
    db_training = db.query(IndustrialTraining).filter(IndustrialTraining.id == training_id).first()
    if db_training:
        db.delete(db_training)
        db.commit()
    return db_training

def get_industrial_trainings_total_score(db: Session, faculty_id: int) -> float:
    trainings = db.query(IndustrialTraining).filter(IndustrialTraining.faculty_id == faculty_id).all()
    total_score = sum([t.api_score_faculty for t in trainings])
    return total_score
