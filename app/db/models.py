from sqlalchemy import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "city"
    __mapper_args__ = {"eager_defaults": True}

    settlement_symbol: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[dict] = mapped_column(JSON, nullable=True)


class PopulationByAge(Base):
    __tablename__ = "population_by_age"
    __mapper_args__ = {"eager_defaults": True}
