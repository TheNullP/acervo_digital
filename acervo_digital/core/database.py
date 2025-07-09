from sqlalchemy.orm import Mapped, mapped_column, registry, sessionmaker
from sqlalchemy import ForeignKey, create_engine

from acervo_digital.core.settings import Settings


settings = Settings()
reg = registry()

engine = create_engine(settings.DB_URL)

@reg.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

@reg.mapped_as_dataclass
class Book:
    __tablename__ = 'books'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    author: Mapped[str]
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))

reg.metadata.create_all(engine)
Session =  sessionmaker(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
