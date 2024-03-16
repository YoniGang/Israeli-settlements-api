from datetime import datetime

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "city"
    __mapper_args__ = {"eager_defaults": True}

    settlement_symbol: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[dict] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)

    population_by_age: Mapped[list['PopulationByAge']] = relationship(
        "PopulationByAge",
        back_populates="city",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="desc(PopulationByAge.created_at)",
    )


class PopulationByAge(Base):
    __tablename__ = "population_by_age"
    __mapper_args__ = {"eager_defaults": True}

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("city.settlement_symbol"), nullable=True)
    city: Mapped['City'] = relationship("City", back_populates="population_by_age",
                                        lazy="selectin")
    data_date: Mapped[datetime] = mapped_column(index=True, nullable=False)
    range_0_5: Mapped[int]
    range_6_18: Mapped[int]
    range_19_45: Mapped[int]
    range_46_55: Mapped[int]
    range_56_64: Mapped[int]
    range_65_and_more: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
