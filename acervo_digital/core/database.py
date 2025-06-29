from sqlalchemy.orm import Mapped, mapped_column, registry, sessionmaker
from sqlalchemy import create_engine


reg = registry()

engine = create_engine('postgresql+psycopg://docker:docker@0.0.0.0:5435/docker')

@reg.mapped_as_dataclass
class User:
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]


reg.metadata.create_all(engine)
Session =  sessionmaker(engine)


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
