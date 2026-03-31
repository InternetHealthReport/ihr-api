from pydantic import BaseModel, ConfigDict


class NetworksDTO(BaseModel):
    number: int
    name: str
    hegemony: bool
    delay_forwarding: bool
    disco: bool

    model_config = ConfigDict(from_attributes=True)

    @staticmethod
    def from_model(asn):
        return NetworksDTO(
            number=asn.number,
            name=asn.name,
            hegemony=asn.ashash,
            delay_forwarding=asn.tartiflette,
            disco=asn.disco
        )
