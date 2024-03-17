from typing import Dict

from pydantic import BaseModel


class SettlementsByCity(BaseModel):
    calculated_population: int
    name: Dict[str, str]
