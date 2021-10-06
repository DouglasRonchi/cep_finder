import aiohttp

from app.exceptions.cep_finder_exceptions import ServiceException, CepNotFoundException, CantConnectWithServiceException
from app.utils.logger import logger


def analyze_and_parse_response(response):
    if response.ok:
        return response.json()

    raise CantConnectWithServiceException('Erro ao se conectar com o serviço ViaCEP.', service="ViaCep")


def check_for_via_cep_error(response_object):
    if response_object.get('erro'):
        raise CepNotFoundException('CEP não encontrado na base do ViaCEP.', service="ViaCep")

    return response_object


def extract_cep_values_from_response(response_object):
    return {
        'cep': response_object.get('cep').replace('-', ''),
        'state': response_object.get('uf'),
        'city': response_object.get('localidade'),
        'neighborhood': response_object.get('bairro'),
        'street': response_object.get('logradouro'),
        'service': 'viacep'
    }


def throw_application_error(error):
    raise ServiceException(
        message=error.args[0],
        service='viacep')


async def fetch_via_cep_service(cep_with_left_pad):
    try:
        url = f'https://viacep.com.br/ws/{cep_with_left_pad}/json'
        headers = {'content-type': 'application/json; charset=utf-8'}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response_object = await analyze_and_parse_response(response)

        check_for_via_cep_error(response_object)
        return extract_cep_values_from_response(response_object)

    except Exception as err:
        logger.error(f"ViaCep Service Error - {err}")
        throw_application_error(err)

