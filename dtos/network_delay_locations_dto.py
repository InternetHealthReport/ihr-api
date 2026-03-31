from pydantic import BaseModel, ConfigDict


class NetworkDelayLocationsDTO(BaseModel):
    type: str
    name: str
    af: int

    model_config = ConfigDict(from_attributes=True)
