import json
import unittest
from http import HTTPStatus
from unittest.mock import Mock, patch

from app.endpoints.endpoint_cep_finder import new_ticket
from app.services.cep_finder_service import find_cep


class TestEndpointCepFinder(unittest.TestCase):
    @patch('app.endpoints.endpoint_cep_finder.CepService')
    def test_success(self,
                     cep_service_mock):
        """
        Args:
            cep_service_mock:
        """
        address_information = Mock(
            cep='03047000',
            state='SP',
            city='SÃ£o Paulo',
            neighborhood='SÃ£o Paulo Capital',
            street='21 de Abril',
            service='someservice',
        )
        find_cep.return_value = address_information
        response = new_ticket("03047000", Mock())
        self.assertEqual(response.cep, '03047000')
        self.assertEqual(response.state, 'SP')
        self.assertEqual(response.city, 'SÃ£o Paulo')
        self.assertEqual(response.neighborhood, 'SÃ£o Paulo Capital')
        self.assertEqual(response.street, '21 de Abril')
        self.assertEqual(response.service, 'someservice')

    @patch('app.endpoints.endpoint_cep_finder.datetime')
    def test_cep_finder_error(self, datetime_mock):
        """
        Args:
            datetime_mock:
        """
        datetime_mock.now.return_value = '2021-10-03 09:01:57.145399'
        response = new_ticket("030470008", Mock())
        self.assertEqual(json.loads(response.body),
                         {"DateTime": "2021-10-03 09:01:57.145399", "Error": "CEP deve conter exatamente 8 caracteres.",
                          "Type": "validation_error", "Message": "CEP informado possui mais do que 8 caracteres."})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    @patch('app.services.cep_services.correios.requests')
    @patch('app.services.cep_services.viacep.requests')
    @patch('app.services.cep_services.widenet.requests')
    @patch('app.services.cep_services.brasilapi.requests')
    @patch('app.endpoints.endpoint_cep_finder.datetime')
    def test_all_services_error(self,
                                datetime_mock,
                                brasilapi_requests_mock,
                                widenet_requests_mock,
                                viacep_requests_mock,
                                correios_requests_mock,
                                ):
        """
        Args:
            datetime_mock:
            brasilapi_requests_mock:
            widenet_requests_mock:
            viacep_requests_mock:
            correios_requests_mock:
        """
        datetime_mock.now.return_value = '2021-10-03 09:18:20.618856'
        response = Mock(ok=False, status_code=400)
        correios_requests_mock.post.return_value = response
        viacep_requests_mock.post.return_value = response
        widenet_requests_mock.post.return_value = response
        brasilapi_requests_mock.post.return_value = response
        response = new_ticket("03047000", Mock())
        self.assertEqual(json.loads(response.body),
                         {'DateTime': '2021-10-03 09:18:20.618856',
                          'Error': 'CEP InvÃ¡lido',
                          'Message': 'NÃ£o foi possÃ­vel localizar o cep em nenhum dos serviÃ§os',
                          'Type': 'AllServicesError'})
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)


if __name__ == '__main__':
    unittest.main()
