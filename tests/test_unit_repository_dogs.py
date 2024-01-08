import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Dog, Owner
from src.schemas import DogModel, DogVaccinatedModel
from src.repository.dogs import get_dogs, get_dog_by_id, create, remove, update, update_vaccinated


class TestCatsRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.owner = Owner(id=1, email="test@test.com")

    async def test_get_dogs(self):
        cats = [Dog(), Dog(), Dog()]
        self.session.query(Dog).limit().offset().all.return_value = cats
        result = await get_dogs(10, 0, self.session)
        self.assertEqual(result, cats)

    async def test_create_dog(self):
        body = DogModel(
            nickname="Simon",
            age=5,
            vaccinated=True,
            description="Дуже багато гавкає",
            owner_id=self.owner.id,
        )
        result = await create(body, self.session)
        self.assertEqual(result.nickname, body.nickname)
        self.assertTrue(hasattr(result, "id"))        # Якщо у результата є атрибут id, тоді буде True