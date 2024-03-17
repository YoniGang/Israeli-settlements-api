import datetime

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/postgres"

MARCH_2024_CITIES_URL = ("https://data.gov.il/api/3/action/datastore_search?"
                         "resource_id=5c78e9fa-c2e2-4771-93ff-7f400a12f7ba&")

MARCH_2024_SETTLEMENTS_URL = ("https://data.gov.il/api/3/action/datastore_search?"
                              "resource_id=64edd0ee-3d5d-43ce-8562-c336c24dbc1f")

APRIL_2019_SETTLEMENTS_URL = ("https://data.gov.il/api/3/action/datastore_search?"
                              "resource_id=a5e7080d-3c37-49c2-8cd0-cb2724809216")

MAY_2019_SETTLEMENTS_URL = ("https://data.gov.il/api/3/action/datastore_search?"
                            "resource_id=578c8312-0a87-4eba-a5d0-be8734e9d72f")

JUNE_2019_SETTLEMENTS_URL = ("https://data.gov.il/api/3/action/datastore_search?"
                             "resource_id=16f0eeb0-31a0-4edb-bc9d-c9477133c740")

JULY_2019_SETTLEMENTS_URL = ("https://data.gov.il/api/3/action/datastore_search?"
                             "resource_id=9e6a8edd-6a70-496c-8048-b213406e186c")

RANGES_MIN_MAX_AGE = {
    "range_0_5": (0, 5),
    "range_6_18": (6, 18),
    "range_19_45": (19, 45),
    "range_46_55": (46, 55,),
    "range_56_64": (56, 64),
    "range_65_and_more": (65, 200)  # I assume there is no person above 200 years old
}

today = datetime.date.today()

NOW_YEAR = today.year
NOW_MONTH = today.month
