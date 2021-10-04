import requests

from app.exceptions.cep_finder_exceptions import ServiceError
from app.utils.logger import logger


def analyze_and_parse_response(response):
    if response.ok:
        return response.json()

    raise Exception('Erro ao se conectar com o serviço WideNet.')


def check_for_wide_net_error(response_object):
    if response_object.get('ok') == False or response_object.get('status') != 200:
        raise Exception('CEP não encontrado na base do WideNet.')

    return response_object


def extract_cep_values_from_response(response_object):
    return {
        'cep': response_object.get('code').replace('-', ''),
        'state': response_object.get('state'),
        'city': response_object.get('city'),
        'neighborhood': response_object.get('district'),
        'street': response_object.get('address'),
        'service': 'widenet'
    }


def throw_application_error(error):
    raise ServiceError(
        message=error.args[0],
        service='widenet')


def fetch_wide_net_service(cep_with_left_pad):
    try:
        url = f'https://ws.apicep.com/busca-cep/api/cep/{cep_with_left_pad}.json'
        headers = {'content-type': 'application/json; charset=utf-8'}

        response = requests.get(url, headers=headers, timeout=2)

        response_object = analyze_and_parse_response(response)
        check_for_wide_net_error(response_object)
        return extract_cep_values_from_response(response_object)

    except Exception as err:
        logger.error(f"WideNet Service Error - {err}")
        throw_application_error(err)
