from pydantic import BaseModel


class NetworkDelayLocationsDTO(BaseModel):
    type: str
    name: str
    af: int

    class Config:
        from_attributes = True
