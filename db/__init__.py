from datetime import date

from sqlalchemy import Integer, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

engine = create_engine("sqlite:///data.db")
SessionLocal = sessionmaker(bind=engine)


def get_session() -> Session:
    with SessionLocal() as session:
        return session


class Base(DeclarativeBase):
    """Table in DB"""

    # __abstract__ = True


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    quantity: Mapped[int]
    unit: Mapped[str]
    expiry_date: Mapped[date]
    image_url: Mapped[str]
    emoji: Mapped[str | None]
    is_hidden: Mapped[bool]
