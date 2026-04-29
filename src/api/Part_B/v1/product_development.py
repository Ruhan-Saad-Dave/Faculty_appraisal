from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ....setup.dependencies import get_db
from ....schema.Part_B.product_development import (
    ProductDevelopmentCreate,
    ProductDevelopmentUpdateFaculty,
    ProductDevelopmentUpdateHOD,
    ProductDevelopmentUpdateDirector,
    ProductDevelopmentResponse,
    ProductDevelopmentSummary,
)
from ....crud.Part_B import product_development as crud_product_development
from ....models.Part_B.product_development import ProductDevelopment as DBProductDevelopment

router = APIRouter()

# Placeholder for authentication and authorization
class User:
    def __init__(self, id: int, roles: List[str]):
        self.id = id
        self.roles = roles

def get_current_user():
    # This is a mock user for demonstration. Replace with actual authentication.
    return User(id=1, roles=["faculty"]) # Default to faculty for now

@router.post("/product-developments", response_model=ProductDevelopmentResponse, status_code=status.HTTP_201_CREATED)
def create_product_development(
    product: ProductDevelopmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "faculty" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to create product developments")
    
    return crud_product_development.create_product_development(db=db, product=product, faculty_id=current_user.id)

@router.get("/product-developments/faculty/{faculty_id}", response_model=List[ProductDevelopmentResponse])
def read_product_developments_by_faculty(
    faculty_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's product developments")
    
    products = crud_product_development.get_product_developments_by_faculty(db, faculty_id=faculty_id, skip=skip, limit=limit)
    return products

@router.get("/product-developments", response_model=List[ProductDevelopmentResponse])
def read_all_product_developments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view all product developments")
    
    products = crud_product_development.get_all_product_developments(db, skip=skip, limit=limit)
    return products

@router.put("/product-developments/{product_id}", response_model=ProductDevelopmentResponse)
def update_product_development(
    product_id: int,
    product_update: ProductDevelopmentUpdateFaculty, # Default to faculty update schema
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = crud_product_development.get_product_development(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Development entry not found")

    # Role-based update logic
    if "admin" in current_user.roles:
        updated_product = crud_product_development.update_product_development_faculty(db, product_id, product_update)
    elif "hod" in current_user.roles:
        if not isinstance(product_update, ProductDevelopmentUpdateHOD):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="HOD can only update api_score_hod")
        updated_product = crud_product_development.update_product_development_hod(db, product_id, product_update)
    elif "director" in current_user.roles:
        if not isinstance(product_update, ProductDevelopmentUpdateDirector):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Director can only update api_score_director")
        updated_product = crud_product_development.update_product_development_director(db, product_id, product_update)
    elif "faculty" in current_user.roles and db_product.faculty_id == current_user.id:
        updated_product = crud_product_development.update_product_development_faculty(db, product_id, product_update)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this product development entry")

    if updated_product is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to update product development entry")
    return updated_product

@router.delete("/product-developments/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_development(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = crud_product_development.get_product_development(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product Development entry not found")

    if "admin" not in current_user.roles and db_product.faculty_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this product development entry")
    
    crud_product_development.delete_product_development(db, product_id)
    return {"message": "Product Development entry deleted successfully"}

@router.get("/product-developments/summary/{faculty_id}", response_model=ProductDevelopmentSummary)
def get_product_developments_summary(
    faculty_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if "admin" not in current_user.roles and current_user.id != faculty_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this faculty's summary")
    
    total_score = crud_product_development.get_product_developments_total_score(db, faculty_id)
    return ProductDevelopmentSummary(total_score=total_score)
