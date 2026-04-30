from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db, get_current_user, User
from ....setup.storage_utils import upload_file_to_supabase
from ....schema.Part_B.book_publication import (
    BookPublicationCreate,
    BookPublicationUpdateFaculty,
    BookPublicationUpdateHOD,
    BookPublicationUpdateDirector,
    BookPublicationResponse,
    BookPublicationSummary,
)
from ....crud.Part_B import book_publication as crud_book_publication
from ....models.Part_B.book_publication import BookPublication as DBBookPublication

router = APIRouter()

@router.post("/book-publications", response_model=BookPublicationResponse, status_code=status.HTTP_201_CREATED)
async def create_book_publication(
    title_and_pages: str = Form(...),
    book_title_editor: str = Form(...),
    issn_isbn: str = Form(...),
    publisher_type: str = Form(...),
    co_authors_count: int = Form(...),
    is_first_author: bool = Form(False),
    department: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create book publications")
    
    document_path = None
    if file:
        document_path = await upload_file_to_supabase(file, current_user.id)
    
    publication = BookPublicationCreate(
        title_and_pages=title_and_pages,
        book_title_editor=book_title_editor,
        issn_isbn=issn_isbn,
        publisher_type=publisher_type,
        co_authors_count=co_authors_count,
        is_first_author=is_first_author,
        department=department,
        document=document_path
    )
    
    return crud_book_publication.create_book_publication(db=db, publication=publication, faculty_id=current_user.id)

@router.get("/book-publications/faculty/{faculty_id}", response_model=List[BookPublicationResponse])
def read_book_publications_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's book publications")
    
    publications = crud_book_publication.get_book_publications_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return publications

@router.get("/book-publications", response_model=List[BookPublicationResponse])
def read_all_book_publications(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all book publications")
    
    publications = crud_book_publication.get_all_book_publications(db, skip=skip, limit=limit)
    return publications

@router.put("/book-publications/{publication_id}", response_model=BookPublicationResponse)
def update_book_publication(
    publication_id: int,
    publication_update: BookPublicationUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_publication = crud_book_publication.get_book_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Publication not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_publication = crud_book_publication.update_book_publication_faculty(db, publication_id, publication_update)
    elif "hod" in current_user.roles:
        if not isinstance(publication_update, BookPublicationUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_publication = crud_book_publication.update_book_publication_hod(db, publication_id, publication_update)
    elif "director" in current_user.roles:
        if not isinstance(publication_update, BookPublicationUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_publication = crud_book_publication.update_book_publication_director(db, publication_id, publication_update)
    elif "faculty" in current_user.roles and db_publication.faculty_id == current_user.id:
        updated_publication = crud_book_publication.update_book_publication_faculty(db, publication_id, publication_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this book publication")

    if updated_publication is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update book publication")
    return updated_publication

@router.delete("/book-publications/{publication_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book_publication(
    publication_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_publication = crud_book_publication.get_book_publication(db, publication_id)
    if db_publication is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book Publication not found")

    if "admin" not in current_user.roles and db_publication.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this book publication")
    
    crud_book_publication.delete_book_publication(db, publication_id)
    return {"message": "Book Publication deleted successfully"}

@router.get("/book-publications/summary/{faculty_id}", response_model=BookPublicationSummary)
def get_book_publications_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_book_publication.get_book_publications_total_score(db, faculty_id)
    return BookPublicationSummary(total_score=total_score)