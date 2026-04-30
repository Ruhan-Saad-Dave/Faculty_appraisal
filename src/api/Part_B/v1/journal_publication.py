from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, get_current_user, User
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.journal_publication import (
    JournalPublicationCreate,
    JournalPublicationUpdateFaculty,
    JournalPublicationUpdateHOD,
    JournalPublicationUpdateDirector,
    JournalPublicationResponse,
    JournalPublicationSummary,
)
from ....models.Part_B.journal_publication import IndexingEnum
from ....crud.Part_B import journal_publication as crud_journal_publication

router = APIRouter()

@router.post("/journal-publications", response_model=JournalPublicationResponse, status_code=status.HTTP_201_CREATED)
async def create_journal_publication(
    sr_no: Optional[int] = Form(None),
    title_with_page_nos: Optional[str] = Form(None),
    journal_details: Optional[str] = Form(None),
    issn_isbn_no: Optional[str] = Form(None),
    indexing: Optional[IndexingEnum] = Form(None),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create journal publications")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    publication = JournalPublicationCreate(
        sr_no=sr_no,
        title_with_page_nos=title_with_page_nos,
        journal_details=journal_details,
        issn_isbn_no=issn_isbn_no,
        indexing=indexing,
        department=department,
        document=document_path
    )
    
    return crud_journal_publication.create_journal_publication(db=db, publication=publication, faculty_id=current_user.id)

@router.get("/journal-publications/faculty/{faculty_id}", response_model=List[JournalPublicationResponse])
def read_journal_publications_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's journal publications")
    
    publications = crud_journal_publication.get_journal_publications_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return publications

@router.get("/journal-publications", response_model=List[JournalPublicationResponse])
def read_all_journal_publications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all journal publications")
    
    publications = crud_journal_publication.get_all_journal_publications(db, skip=skip, limit=limit)
    return publications

@router.put("/journal-publications/{publication_id}", response_model=JournalPublicationResponse)
def update_journal_publication(
    publication_id: int,
    publication_update: JournalPublicationUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_publication = crud_journal_publication.get_journal_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Publication not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        # Admin can update anything, so we can use the faculty update schema for now
        # or a more comprehensive admin update schema if needed.
        updated_publication = crud_journal_publication.update_journal_publication_faculty(db, publication_id, publication_update)
    elif "hod" in current_user.roles:
        # HOD can only update api_score_hod
        if not isinstance(publication_update, JournalPublicationUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_publication = crud_journal_publication.update_journal_publication_hod(db, publication_id, publication_update)
    elif "director" in current_user.roles:
        # Director can only update api_score_director
        if not isinstance(publication_update, JournalPublicationUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_publication = crud_journal_publication.update_journal_publication_director(db, publication_id, publication_update)
    elif "faculty" in current_user.roles and db_publication.faculty_id == current_user.id:
        # Faculty can update their own entries (title, journal details, ISSN, indexing)
        updated_publication = crud_journal_publication.update_journal_publication_faculty(db, publication_id, publication_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this journal publication")

    if updated_publication is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update journal publication")
    return updated_publication

@router.delete("/journal-publications/{publication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_journal_publication(
    publication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_publication = crud_journal_publication.get_journal_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Journal Publication not found")

    if "admin" not in current_user.roles and db_publication.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this journal publication")
    
    crud_journal_publication.delete_journal_publication(db, publication_id)
    return {"message": "Journal Publication deleted successfully"}

@router.get("/journal-publications/summary/{faculty_id}", response_model=JournalPublicationSummary)
def get_journal_publications_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_journal_publication.get_journal_publications_total_score(db, faculty_id)
    return JournalPublicationSummary(total_score=total_score)
