from pydantic import BaseModel

class CountryDTO(BaseModel):
    code: str
    name: str

    class Config:
        from_attributes = True  
