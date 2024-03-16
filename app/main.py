from datetime import datetime
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.constant import SQLALCHEMY_DATABASE_URL, MARCH_2024_CITIES_URL, MARCH_2024_SETTLEMENTS
from app.db.models import City, PopulationByAge
from app.managers import InitManager

app = FastAPI(title="mavens Data Assignment")

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as asc_session:
        yield asc_session


session = DbDependency = Annotated[AsyncSession, Depends(get_session)]

# It's not the best design but for the purpose of the exersice, I settled.
SETTLEMENT_SYMBOLS_ADDED = set()


def cities_manipulation_function(record, data_to_add, extra_data=None):
    if record["שם_ישוב_לועזי"] == " ":
        return
    SETTLEMENT_SYMBOLS_ADDED.add(int(record["סמל_ישוב"].strip()))
    data_to_add.append({"settlement_symbol": int(record["סמל_ישוב"].strip()),
                        "name": {
                            "en": " ".join([st.capitalize() for st in record["שם_ישוב_לועזי"].strip().split()]),
                            "he": record["שם_ישוב"].strip()}})


def settlements_manipulation_function(record, data_to_add, date=None):
    if record["סמל_ישוב"] not in SETTLEMENT_SYMBOLS_ADDED:
        return

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
                        "data_date": date
                        })


@app.get("/init")
async def init(db: DbDependency):
    # TODO implement data collection, preprocessing and DB initialization logic
    # You can use this DB connection string "postgresql+asyncpg://user:password@db:5432/postgres"

    cities_manager = InitManager(db=db, table_to_change=City, data_manipulation_function=cities_manipulation_function)
    await cities_manager.delete_all_data()
    await cities_manager.get_data(MARCH_2024_CITIES_URL)

    settlement_manager = InitManager(db=db, table_to_change=PopulationByAge,
                                     data_manipulation_function=settlements_manipulation_function)
    await settlement_manager.delete_all_data()
    await settlement_manager.get_data(MARCH_2024_SETTLEMENTS,
                                      extra_data_for_manipulation_function=datetime.strptime("10/03/2024",
                                                                                             '%d/%m/%Y'))

    # first save all updates cities
    # cities_res = requests.get(MARCH_2024_CITIES_URL)
    # cities_json_res = cities_res.json()
    # cities = cities_json_res["result"]["records"]
    # cities_to_add = []
    # for city in cities:
    #     if city["שם_ישוב_לועזי"] != " ":
    #         cities_to_add.append({"settlement_symbol": int(city["סמל_ישוב"].strip()),
    #                               "name": {
    #                                   "en": " ".join([st.capitalize() for st in city["שם_ישוב_לועזי"].strip().split()]),
    #                                   "he": city["שם_ישוב"].strip()}})
    # insert_stmt = insert(City).values(cities_to_add)
    # try:
    #     await db.execute(statement=insert_stmt)
    #     await db.commit()
    # except IntegrityError:
    #     print("Cities already exists")

    # march_settlement_res = requests.get(MARCH_2024_SETTLEMENTS)
    # march_settlement_json_res = march_settlement_res.json()
    # march_settlement = march_settlement_json_res["result"]["records"]
    # print(march_settlement)

    return "Ok"


@app.get("/settlements")
async def get_settlements(month: int, year: int, min_age: int, max_age: int, min_population: int):
    # TODO implement DB querying and response creation logic
    return
