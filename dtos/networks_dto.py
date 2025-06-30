from pydantic import BaseModel


class NetworksDTO(BaseModel):
    number: int
    name: str
    hegemony: bool
    delay_forwarding: bool
    disco: bool

    class Config:
        from_attributes = True

    @staticmethod
    def from_model(asn):
        return NetworksDTO(
            number=asn.number,
            name=asn.name,
            hegemony=asn.ashash,
            delay_forwarding=asn.tartiflette,
            disco=asn.disco
        )
