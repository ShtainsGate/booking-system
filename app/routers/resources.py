from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ResourceCreate, Resource
from app.crud import create_resource, get_resource, get_resources

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/", response_model=Resource)
def create_resource_endpoint(resource: ResourceCreate, db: Session = Depends(get_db)):
    return create_resource(db=db, resource=resource)

@router.get("/{resource_id}", response_model=Resource)
def read_resource(resource_id: int, db: Session = Depends(get_db)):
    db_resource = get_resource(db, resource_id=resource_id)
    if not db_resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return db_resource

@router.get("/", response_model=list[Resource])
def read_resources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_resources(db, skip=skip, limit=limit)

__all__ = ["router"]