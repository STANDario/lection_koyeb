from sqlalchemy.orm import Session

from src.database.models import Dog
from src.schemas import DogModel, DogVaccinatedModel


async def get_dogs(limit: int, offset: int, db: Session):
    dogs = db.query(Dog).limit(limit).offset(offset).all()
    return dogs


async def get_dog_by_id(dog_id: int, db: Session):
    dog = db.query(Dog).filter_by(id=dog_id).first()
    return dog


async def create(body: DogModel, db: Session):
    dog = Dog(**body.dict())
    db.add(dog)
    db.commit()
    db.refresh(dog)
    return dog


async def update(body: DogModel, db: Session, dog_id: int):
    dog = await get_dog_by_id(dog_id, db)
    if dog:
        dog.nickname = body.nickname
        dog.age = body.age
        dog.vaccinated = body.vaccinated
        dog.description = body.description
        dog.owner_id = body.owner_id
        db.commit()
    return dog


async def remove(dog_id: int, db: Session):
    dog = await get_dog_by_id(dog_id, db)
    if dog:
        db.delete(dog)
        db.commit()
    return dog


async def update_vaccinated(body: DogVaccinatedModel, dog_id: int, db: Session):
    dog = await get_dog_by_id(dog_id, db)
    if dog:
        dog.vaccinated = body.vaccinated
        db.commit()
    return dog
