"""
This is a brasilapi module for cep_finder api
"""
import aiohttp

from app.exceptions.cep_finder_exceptions import ServiceException, CepNotFoundException
from app.utils.logger import logger


def brasilapi_parse_response(response):
    if not response.ok or response.status != 200:
        raise CepNotFoundException('CEP não encontrado na base do brasilapi.', service="BrasilAPI")

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
    raise ServiceException(
        message=error.args[0],
        service='brasilapi')


async def fetch_brasilapi_service(cep_with_left_pad):
    try:
        url = f'https://brasilapi.com.br/api/cep/v1/{cep_with_left_pad}'
        headers = {'content-type': 'application/json; charset=utf-8'}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response = await brasilapi_parse_response(response)

        return extract_cep_values_from_response(response)

    except Exception as err:
        logger.error(f"brasilapi Service Error - {err}")
        throw_application_error(err)
