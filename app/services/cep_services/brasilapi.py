import requests

from app.exceptions.cep_finder_exceptions import ServiceError
from app.utils.logger import logger


def brasilapi_parse_response(response):
    if not response.ok or response.status_code != 200:
        raise Exception('CEP não encontrado na base do brasilapi.')

    return response.json()


def extract_cep_values_from_response(response_object):
    return {
        'cep': response_object.get('cep').replace('-', ''),
        'state': response_object.get('state'),
        'city': response_object.get('city'),
        'neighborhood': response_object.get('neighborhood'),
        'street': response_object.get('street'),
        'service': 'brasilapi'
    }


def throw_application_error(error):
    raise ServiceError(
        message=error.args[0],
        service='brasilapi')


def fetch_brasilapi_service(cep_with_left_pad):
    try:
        url = f'https://brasilapi.com.br/api/cep/v1/{cep_with_left_pad}'
        headers = {'content-type': 'application/json; charset=utf-8'}

        response = requests.get(url, headers=headers, timeout=2)

        response_object = brasilapi_parse_response(response)
        return extract_cep_values_from_response(response_object)

    except Exception as err:
        logger.error(f"brasilapi Service Error - {err}")
        throw_application_error(err)
