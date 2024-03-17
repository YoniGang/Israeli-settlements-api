from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import parse_obj_as
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.constant import SQLALCHEMY_DATABASE_URL, MARCH_2024_CITIES_URL, MARCH_2024_SETTLEMENTS_URL, \
    APRIL_2019_SETTLEMENTS_URL, MAY_2019_SETTLEMENTS_URL, JUNE_2019_SETTLEMENTS_URL, JULY_2019_SETTLEMENTS_URL
from app.db.models import City, PopulationByAge
from app.managers import InitManager
from app.schemas import SettlementsByCity
from app.utils import get_ranges_by_min_max_age, validate_input

app = FastAPI(title="mavens Data Assignment")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as asc_session:
        yield asc_session


session = DbDependency = Annotated[AsyncSession, Depends(get_session)]

# It's not the best design but for the purpose of the exercise, I settled.
SETTLEMENT_SYMBOLS_ADDED = set()


def cities_manipulation_function(record, data_to_add, extra_data=None):
    if record["שם_ישוב_לועזי"] == " ":
        return
    settlement_symbol = int(record["סמל_ישוב"].strip())
    SETTLEMENT_SYMBOLS_ADDED.add(settlement_symbol)
    data_to_add.append({"settlement_symbol": settlement_symbol,
                        "name": {
                            "en": " ".join([st.capitalize() for st in record["שם_ישוב_לועזי"].strip().split()]),
                            "he": record["שם_ישוב"].strip()}})


def settlements_manipulation_function(record, data_to_add, date_dict=None):
    if record["סמל_ישוב"] not in SETTLEMENT_SYMBOLS_ADDED:
        return
    print(record["סמל_ישוב"])
    # because it could be 0-5 or 0-6 in the data.
    range_0_5 = record.get("גיל_0_5")
    range_0_5 = range_0_5 if range_0_5 is not None else record.get("גיל_0_6")
    data_to_add.append({"city_id": record["סמל_ישוב"],
                        "range_0_5": range_0_5,
                        "range_6_18": record["גיל_6_18"],
                        "range_19_45": record["גיל_19_45"],
                        "range_46_55": record["גיל_46_55"],
                        "range_56_64": record["גיל_56_64"],
                        "range_65_and_more": record["גיל_65_פלוס"],
                        "data_year": date_dict["year"],
                        "data_month": date_dict["month"]
                        })


@app.get("/init")
async def init(db: DbDependency):
    # TODO implement data collection, preprocessing and DB initialization logic
    # You can use this DB connection string "postgresql+asyncpg://user:password@db:5432/postgres"

    cities_manager = InitManager(db=db, table_to_change=City, data_manipulation_function=cities_manipulation_function)
    settlement_manager = InitManager(db=db, table_to_change=PopulationByAge,
                                     data_manipulation_function=settlements_manipulation_function)
    # Delete the old data to add the new one
    await settlement_manager.delete_all_data()
    await cities_manager.delete_all_data()

    await cities_manager.get_data(MARCH_2024_CITIES_URL)

    await settlement_manager.get_data(MARCH_2024_SETTLEMENTS_URL,
                                      extra_data_for_manipulation_function={"year": 2024, "month": 3})

    await settlement_manager.get_data(APRIL_2019_SETTLEMENTS_URL,
                                      extra_data_for_manipulation_function={"year": 2019, "month": 4})

    await settlement_manager.get_data(MAY_2019_SETTLEMENTS_URL,
                                      extra_data_for_manipulation_function={"year": 2019, "month": 5})

    await settlement_manager.get_data(JUNE_2019_SETTLEMENTS_URL,
                                      extra_data_for_manipulation_function={"year": 2019, "month": 6})

    await settlement_manager.get_data(JULY_2019_SETTLEMENTS_URL,
                                      extra_data_for_manipulation_function={"year": 2019, "month": 7})

    return "Ok"


@app.get("/settlements")
async def get_settlements(db: DbDependency, month: int, year: int, min_age: int, max_age: int, min_population: int):
    is_valid, error_msg = validate_input(month, year, min_age, max_age, min_population)
    if not is_valid:
        print(error_msg)
        raise ValueError(error_msg)

    ranges_to_include = get_ranges_by_min_max_age(min_age, max_age)

    stmt = select(City.name, text(f"{ranges_to_include} as population")) \
        .join(PopulationByAge, City.settlement_symbol == PopulationByAge.city_id) \
        .filter(PopulationByAge.data_month == month, PopulationByAge.data_year == year,
                text(f"{ranges_to_include} >= {min_population}"))

    results = await db.execute(stmt)

    # Fetch all the results
    rows = results.fetchall()
    res_dict = [{"calculated_population": row[1], "name": row[0]} for row in rows]

    return parse_obj_as(list[SettlementsByCity], res_dict)
