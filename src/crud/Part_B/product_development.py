from sqlalchemy.orm import Session
from typing import List, Optional

from src.models.Part_B.product_development import ProductDevelopment
from src.schema.Part_B.product_development import (
    ProductDevelopmentCreate,
    ProductDevelopmentUpdateFaculty,
    ProductDevelopmentUpdateHOD,
    ProductDevelopmentUpdateDirector,
)

def get_product_development(db: Session, product_id: int) -> Optional[ProductDevelopment]:
    return db.query(ProductDevelopment).filter(ProductDevelopment.id == product_id).first()

def get_product_developments_by_faculty(db: Session, faculty_id: int, skip: int = 0, limit: int = 100) -> List[ProductDevelopment]:
    return db.query(ProductDevelopment).filter(ProductDevelopment.faculty_id == faculty_id).offset(skip).limit(limit).all()

def get_all_product_developments(db: Session, skip: int = 0, limit: int = 100) -> List[ProductDevelopment]:
    return db.query(ProductDevelopment).offset(skip).limit(limit).all()

def create_product_development(db: Session, product: ProductDevelopmentCreate, faculty_id: int) -> ProductDevelopment:
    db_product = ProductDevelopment(**product.model_dump(), faculty_id=faculty_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product_development_faculty(
    db: Session, product_id: int, product_update: ProductDevelopmentUpdateFaculty
) -> Optional[ProductDevelopment]:
    db_product = db.query(ProductDevelopment).filter(ProductDevelopment.id == product_id).first()
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def update_product_development_hod(
    db: Session, product_id: int, product_update: ProductDevelopmentUpdateHOD
) -> Optional[ProductDevelopment]:
    db_product = db.query(ProductDevelopment).filter(ProductDevelopment.id == product_id).first()
    if db_product:
        db_product.api_score_hod = product_update.api_score_hod
        db.commit()
        db.refresh(db_product)
    return db_product

def update_product_development_director(
    db: Session, product_id: int, product_update: ProductDevelopmentUpdateDirector
) -> Optional[ProductDevelopment]:
    db_product = db.query(ProductDevelopment).filter(ProductDevelopment.id == product_id).first()
    if db_product:
        db_product.api_score_director = product_update.api_score_director
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product_development(db: Session, product_id: int) -> Optional[ProductDevelopment]:
    db_product = db.query(ProductDevelopment).filter(ProductDevelopment.id == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product

def get_product_developments_total_score(db: Session, faculty_id: int) -> float:
    products = db.query(ProductDevelopment).filter(ProductDevelopment.faculty_id == faculty_id).all()
    total_score = sum([p.api_score_faculty for p in products])
    return total_score
