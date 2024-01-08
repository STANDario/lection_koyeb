import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func, event, Enum
from sqlalchemy.orm import relationship, declarative_base


Base = declarative_base()


class Role(enum.Enum):               # Треба щоб роздати ролі користувачам
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


class Dog(Base):
    __tablename__ = "dogs"
    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String, index=True)
    age = Column(Integer)
    vaccinated = Column(Boolean, default=False)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=True)
    owner = relationship("Owner", backref="dogs")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())


@event.listens_for(Dog, "before_insert")
def updated_vaccinated(mapper, conn, target):
    if target.nickname == "Boris":
        target.vaccinated = True


@event.listens_for(Dog, "before_update")
def updated_vaccinated(mapper, conn, target):
    if target.nickname == "Dudona":
        target.vaccinated = True


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    roles = Column("roles", Enum(Role), default=Role.user)         # Передаємо сюди наші ролі
    confirmed = Column(Boolean, default=False)
