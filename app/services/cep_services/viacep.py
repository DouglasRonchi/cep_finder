import requests

from app.exceptions.cep_finder_exceptions import ServiceError
from app.utils.logger import logger


def analyze_and_parse_response(response):
    if response.ok:
        return response.json()

    raise Exception('Erro ao se conectar com o serviço ViaCEP.')


def check_for_via_cep_error(response_object):
    if response_object.get('erro'):
        raise Exception('CEP não encontrado na base do ViaCEP.')

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
    raise ServiceError(
        message=error.args[0],
        service='viacep')


def fetch_via_cep_service(cep_with_left_pad):
    try:
        url = f'https://viacep.com.br/ws/{cep_with_left_pad}/json'
        headers = {'content-type': 'application/json; charset=utf-8'}

        response = requests.get(url, headers=headers, timeout=2)

        response_object = analyze_and_parse_response(response)
        check_for_via_cep_error(response_object)
        return extract_cep_values_from_response(response_object)

    except Exception as err:
        logger.error(f"ViaCep Service Error - {err}")
        throw_application_error(err)

