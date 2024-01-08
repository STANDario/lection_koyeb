from typing import List

from fastapi import Depends, Path, HTTPException, status, APIRouter, Query
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import User
from src.schemas import DogResponse, DogModel, DogVaccinatedModel
from src.repository import dogs as repository_dogs
from src.services.auth import auth_service
from src.services.roles import RoleAccess, Role


router = APIRouter(prefix="/dogs", tags=["dogs"])

allowed_operation_get = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_create = RoleAccess([Role.admin, Role.moderator, Role.user])
allowed_operation_update = RoleAccess([Role.admin, Role.moderator])
allowed_operation_delete = RoleAccess([Role.admin])


@router.get("/", response_model=List[DogResponse], dependencies=[Depends(allowed_operation_get),
                                                                 Depends(RateLimiter(times=2, seconds=5))])
async def get_dogs(limit: int = Query(10, le=500), offset: int = 0, db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    dogs = await repository_dogs.get_dogs(limit, offset, db)
    return dogs


@router.get("/{dog_id}", response_model=DogResponse, dependencies=[Depends(allowed_operation_get)])
async def get_dogs(dog_id: int = Path(ge=1), db: Session = Depends(get_db),
                   current_user: User = Depends(auth_service.get_current_user)):
    dog = await repository_dogs.get_dog_by_id(dog_id, db)
    if dog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return dog


@router.post("/", response_model=DogResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(allowed_operation_create)])
async def create_dog(body: DogModel, db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    dog = await repository_dogs.create(body, db)
    return dog


@router.put("/{dog_id}", response_model=DogResponse, dependencies=[Depends(allowed_operation_update)], description="Only moderators and admin")
async def update_dog(body: DogModel, dog_id: int = Path(ge=1), db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    dog = await repository_dogs.update(body, db, dog_id)
    if dog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return dog


@router.delete("/{dog_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(allowed_operation_delete)])
async def delete_dog(dog_id: int = Path(ge=1), db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    dog = await repository_dogs.remove(dog_id, db)
    if dog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return dog


# Якщо зміни відбуваються не повністю, а частково, то можна зробити так
@router.patch("/{dog_id}/vaccinated", response_model=DogResponse, dependencies=[Depends(allowed_operation_update)])
async def vaccinated_dog(body: DogVaccinatedModel, dog_id: int = Path(ge=1), db: Session = Depends(get_db),
                         current_user: User = Depends(auth_service.get_current_user)):
    dog = await repository_dogs.update_vaccinated(body, dog_id, db)
    if dog is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return dog
