from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

app = FastAPI(title="mavens Data Assignment")

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/postgres"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db():
    db = async_session()
    try:
        yield db
    finally:
        await db.close()

@app.get("/init")
async def init():
    # TODO implement data collection, preprocessing and DB initialization logic
    # You can use this DB connection string "postgresql+asyncpg://user:password@db:5432/postgres"
    return "Ok"


@app.get("/settlements")
async def get_settlements(month: int, year: int, min_age: int, max_age: int, min_population: int):
    # TODO implement DB querying and response creation logic
    return
