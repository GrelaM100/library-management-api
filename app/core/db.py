from sqlmodel import Session, SQLModel, create_engine, select

from app.core.config import settings

engine = create_engine(str(settings.sqlalchemy_database_uri))


def init_db(session: Session) -> None:
    SQLModel.metadata.create_all(engine)
