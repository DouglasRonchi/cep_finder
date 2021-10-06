"""
This is a index module for cep_finder api
"""
from app.services.cep_services.brasilapi import fetch_brasilapi_service
from app.services.cep_services.correios import fetch_correios_service
from app.services.cep_services.viacep import fetch_via_cep_service
from app.services.cep_services.widenet import fetch_wide_net_service


def get_available_services():
    """
    :return: list of available services
    """
    return [
        fetch_correios_service,
        fetch_via_cep_service,
        fetch_wide_net_service,
        fetch_brasilapi_service
    ]
