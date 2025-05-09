from pydantic import BaseModel

class CityRequest(BaseModel):
    city: str
