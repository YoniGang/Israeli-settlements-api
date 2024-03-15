from typing import Annotated

import requests
from fastapi import FastAPI, Depends, APIRouter
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.db.models import City

app = FastAPI(title="mavens Data Assignment")

api_router = APIRouter()

app.include_router(api_router)

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/postgres"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as asc_session:
        yield asc_session


session = DbDependency = Annotated[AsyncSession, Depends(get_session)]

MARCH_2024_CITIES_URL = "https://data.gov.il/api/3/action/datastore_search?resource_id=5c78e9fa-c2e2-4771-93ff-7f400a12f7ba&"


@app.get("/init")
async def init(db: DbDependency):
    # TODO implement data collection, preprocessing and DB initialization logic
    # You can use this DB connection string "postgresql+asyncpg://user:password@db:5432/postgres"

    # first save all updates cities
    res = requests.get(MARCH_2024_CITIES_URL)
    json_res = res.json()
    cities = json_res["result"]["records"]
    cities_to_add = []
    for city in cities:
        if city["שם_ישוב_לועזי"] != " ":
            cities_to_add.append({"settlement_symbol": int(city["סמל_ישוב"].strip()),
                                  "name": {"en": city["שם_ישוב_לועזי"].strip(), "he": city["שם_ישוב"].strip()}})
    insert_stmt = insert(City).values(cities_to_add)
    try:
        await db.execute(statement=insert_stmt)
        await db.commit()
    except IntegrityError:
        print("Cities already exists")

    # session.
    return "Ok"


@app.get("/settlements")
async def get_settlements(month: int, year: int, min_age: int, max_age: int, min_population: int):
    # TODO implement DB querying and response creation logic
    return
