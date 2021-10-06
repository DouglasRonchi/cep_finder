"""
This is a AddressInformation module for cep_finder api
"""
from pydantic import BaseModel


class AddressInformation(BaseModel):
    """Address Information Model Class"""
    cep: str
    state: str
    city: str
    neighborhood: str
    street: str
    service: str
