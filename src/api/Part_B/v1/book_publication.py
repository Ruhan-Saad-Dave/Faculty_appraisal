from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from ....setup.dependencies import get_db
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

# Placeholder for authentication and authorization
# In a real application, this would involve actual user authentication and role checking
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # This is a mock user for demonstration. Replace with actual authentication.
    # For testing different roles, you can modify this.
    # Example: return User(id=1, roles=["faculty"])
    # Example: return User(id=2, roles=["admin"])
    # Example: return User(id=3, roles=["hod"])
    # Example: return User(id=4, roles=["director"])
    return User(id=1, roles=["faculty"]) # Default to faculty for now

@router.post("/book-publications", response_model=BookPublicationResponse, status_code=status.HTTP_201_CREATED)
def create_book_publication(
    publication: BookPublicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create book publications")
    
    # Assuming the faculty_id for creation comes from the authenticated user
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