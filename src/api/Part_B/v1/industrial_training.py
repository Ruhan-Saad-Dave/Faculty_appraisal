from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, get_current_user, User
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.industrial_training import (
    IndustrialTrainingCreate,
    IndustrialTrainingUpdateFaculty,
    IndustrialTrainingUpdateHOD,
    IndustrialTrainingUpdateDirector,
    IndustrialTrainingResponse,
    IndustrialTrainingSummary,
)
from ....crud.Part_B import industrial_training as crud_industrial_training
from ....models.Part_B.industrial_training import IndustrialTraining as DBIndustrialTraining

router = APIRouter()

@router.post("/industrial-trainings", response_model=IndustrialTrainingResponse, status_code=status.HTTP_201_CREATED)
async def create_industrial_training(
    company_industry: str = Form(...),
    duration_days: int = Form(...),
    nature_of_training: str = Form(...),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create industrial training entries")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    training = IndustrialTrainingCreate(
        company_industry=company_industry,
        duration_days=duration_days,
        nature_of_training=nature_of_training,
        department=department,
        document=document_path
    )
    
    return crud_industrial_training.create_industrial_training(db=db, training=training, faculty_id=current_user.id)

@router.get("/industrial-trainings/faculty/{faculty_id}", response_model=List[IndustrialTrainingResponse])
def read_industrial_trainings_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's industrial training entries")
    
    trainings = crud_industrial_training.get_industrial_trainings_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return trainings

@router.get("/industrial-trainings", response_model=List[IndustrialTrainingResponse])
def read_all_industrial_trainings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all industrial training entries")
    
    trainings = crud_industrial_training.get_all_industrial_trainings(db, skip=skip, limit=limit)
    return trainings

@router.put("/industrial-trainings/{training_id}", response_model=IndustrialTrainingResponse)
def update_industrial_training(
    training_id: int,
    training_update: IndustrialTrainingUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_training = crud_industrial_training.get_industrial_training(db, training_id)
    if db_training is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Industrial Training entry not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_training = crud_industrial_training.update_industrial_training_faculty(db, training_id, training_update)
    elif "hod" in current_user.roles:
        if not isinstance(training_update, IndustrialTrainingUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_training = crud_industrial_training.update_industrial_training_hod(db, training_id, training_update)
    elif "director" in current_user.roles:
        if not isinstance(training_update, IndustrialTrainingUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_training = crud_industrial_training.update_industrial_training_director(db, training_id, training_update)
    elif "faculty" in current_user.roles and db_training.faculty_id == current_user.id:
        updated_training = crud_industrial_training.update_industrial_training_faculty(db, training_id, training_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this industrial training entry")

    if updated_training is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update industrial training entry")
    return updated_training

@router.delete("/industrial-trainings/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_industrial_training(
    training_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_training = crud_industrial_training.get_industrial_training(db, training_id)
    if db_training is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Industrial Training entry not found")

    if "admin" not in current_user.roles and db_training.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this industrial training entry")
    
    crud_industrial_training.delete_industrial_training(db, training_id)
    return {"message": "Industrial Training entry deleted successfully"}

@router.get("/industrial-trainings/summary/{faculty_id}", response_model=IndustrialTrainingSummary)
def get_industrial_trainings_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_industrial_training.get_industrial_trainings_total_score(db, faculty_id)
    return IndustrialTrainingSummary(total_score=total_score)
