from pydantic import BaseModel


class AddressInformation(BaseModel):
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    service: str
