import re
from multiprocessing import Process
from multiprocessing.pool import ThreadPool

from app.exceptions.cep_finder_exceptions import CepFinderError, AllServicesNotFound
from app.models.address_information_model import AddressInformation
from app.services.cep_services.brasilapi import fetch_brasilapi_service
from app.services.cep_services.correios import fetch_correios_service
from app.services.cep_services.index import get_available_services
from app.services.cep_services.viacep import fetch_via_cep_service
from app.services.cep_services.widenet import fetch_wide_net_service

CEP_SIZE = 8


class CepService:
    @staticmethod
    def __validate_input_type(cep_raw_value):
        cep_type_of = type(cep_raw_value)

        if cep_type_of == int or cep_type_of == str:
            return str(cep_raw_value)

        raise CepFinderError(
            error='Erro ao inicializar a instância do CepPromise.',
            type='validation_error',
            message='Você deve chamar o construtor utilizando uma String ou um Number.'
        )

    @staticmethod
    def __remove_special_characters(cep_raw_value):
        return "".join(re.findall('[\d+]', cep_raw_value))

    @staticmethod
    def __left_pad_with_zeros(cep_clean_value: str):
        return cep_clean_value.zfill(8)

    @staticmethod
    def __validate_input_length(cep_with_left_pad):
        if len(cep_with_left_pad) == CEP_SIZE:
            return cep_with_left_pad

        raise CepFinderError(
            error=f'CEP deve conter exatamente {CEP_SIZE} caracteres.',
            type='validation_error',
            message=f'CEP informado possui mais do que {CEP_SIZE} caracteres.'
        )

    def __cep_validator(self, cep_raw_value):
        self.__validate_input_type(cep_raw_value)
        cep_raw_value = self.__remove_special_characters(cep_raw_value)
        cep_with_left_pad = self.__left_pad_with_zeros(cep_raw_value)
        valid_cep = self.__validate_input_length(cep_with_left_pad)
        return valid_cep

    def find_cep(self, cep_number):
        cep_number = self.__cep_validator(cep_number)
        providers_services = get_available_services()
        # Search in available services:
        # pool = ThreadPool(processes=4)
        # async_result = pool.apply_async(fetch_brasilapi_service, (cep_number))
        # async_result = pool.apply_async(fetch_correios_service, (cep_number))
        # async_result = pool.apply_async(fetch_via_cep_service, (cep_number))
        # async_result = pool.apply_async(fetch_wide_net_service, (cep_number))
        # return async_result.get()

        for provider in providers_services:
            try:
                response = provider(cep_number)
                return AddressInformation(**response)
            except:
                pass

        raise AllServicesNotFound()
