import requests

from app.exceptions.cep_finder_exceptions import ServiceError
from app.utils.logger import logger


def analyze_and_parse_response(response):
    if response.ok:
        return parse_success_xml(response.text)
    raise Exception('CEP não encontrado na base do correios.')


def extract_cep_values_from_response(response_object):
    return {
        'cep': response_object.get('cep').replace('-', ''),
        'state': response_object.get('state'),
        'city': response_object.get('city'),
        'neighborhood': response_object.get('neighborhood'),
        'street': response_object.get('street'),
        'service': 'correios'
    }


def parse_success_xml(xml_string):
    try:
        if xml_string == '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><ns2:consultaCEPResponse xmlns:ns2="http://cliente.bean.master.sigep.bsb.correios.com.br/"/></soap:Body></soap:Envelope>':
            raise Exception('CEP não encontrado na base do correios.')
        return_statement = xml_string.replace('/\r?\n|\r/g', '')
        clean_return_statement = return_statement.replace('<return>', '').replace('</return>', '')
        parsed_return_statement = clean_return_statement
        xml_object = {
            'cep': parsed_return_statement[parsed_return_statement.find('<cep>') + 5:parsed_return_statement.find('</cep>')],
            'state': parsed_return_statement[parsed_return_statement.find('<uf>') + 4:parsed_return_statement.find('</uf>')],
            'city': parsed_return_statement[parsed_return_statement.find('<cidade>') + 8:parsed_return_statement.find('</cidade>')],
            'neighborhood': parsed_return_statement[parsed_return_statement.find('<bairro>') + 8:parsed_return_statement.find('</bairro>')],
            'street': parsed_return_statement[parsed_return_statement.find('<end>') + 5:parsed_return_statement.find('</end>')],
        }
        return xml_object
    except Exception as err:
        raise Exception('Não foi possível interpretar o XML de resposta.')


def throw_application_error(error):
    raise ServiceError(
        message=error.args[0],
        service='correios')


def fetch_correios_service(cep_with_left_pad):
    try:
        url = f'https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente'
        headers = {'content-type': 'text/xml; charset=UTF-8',
                   'cache-control': 'no-cache'}
        body = f'<?xml version="1.0"?>\n<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:cli="http://cliente.bean.master.sigep.bsb.correios.com.br/">\n  <soapenv:Header />\n  <soapenv:Body>\n    <cli:consultaCEP>\n      <cep>{cep_with_left_pad}</cep>\n    </cli:consultaCEP>\n  </soapenv:Body>\n</soapenv:Envelope>'

        response = requests.post(url, headers=headers, data=body, timeout=2)

        response_object = analyze_and_parse_response(response)
        return extract_cep_values_from_response(response_object)

    except Exception as err:
        logger.error(f"correios Service Error - {err}")
        throw_application_error(err)
