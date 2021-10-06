"""
This is cep_finder_service module for cep_finder api
"""
import asyncio
import re
from datetime import datetime

from app.exceptions.cep_finder_exceptions import InvalidCepException, AllServicesNotFoundException
from app.models.address_information_model import AddressInformation
from app.services.cep_services.brasilapi import fetch_brasilapi_service
from app.services.cep_services.correios import fetch_correios_service
from app.services.cep_services.index import get_available_services
from app.services.cep_services.viacep import fetch_via_cep_service
from app.services.cep_services.widenet import fetch_wide_net_service
from app.utils.logger import logger

CEP_SIZE = 8


def validate_input_type(cep_raw_value):
    """
    :param cep_raw_value:
    :return:
    """
    cep_type_of = type(cep_raw_value)

    if cep_type_of in (int, str):
        return str(cep_raw_value)

    raise InvalidCepException(
        error='Erro ao inicializar a instância do CepPromise.',
        type='validation_error',
        message='Você deve chamar o construtor utilizando uma String ou um Number.'
    )


def remove_special_characters(cep_raw_value):
    """
    :param cep_raw_value:
    :return:
    """
    return "".join(re.findall(r'[\d+]', cep_raw_value))


def left_pad_with_zeros(cep_clean_value: str):
    """
    :param cep_clean_value:
    :return:
    """
    return cep_clean_value.zfill(8)


def validate_input_length(cep_with_left_pad):
    """
    :param cep_with_left_pad:
    :return:
    """
    if len(cep_with_left_pad) == CEP_SIZE:
        return cep_with_left_pad

    raise InvalidCepException(
        error=f'CEP deve conter exatamente {CEP_SIZE} caracteres.',
        type='validation_error',
        message=f'CEP informado possui mais do que {CEP_SIZE} caracteres.'
    )


def cep_validator(cep_raw_value):
    """
    :param cep_raw_value:
    :return:
    """
    validate_input_type(cep_raw_value)
    cep_raw_value = remove_special_characters(cep_raw_value)
    cep_with_left_pad = left_pad_with_zeros(cep_raw_value)
    valid_cep = validate_input_length(cep_with_left_pad)
    return valid_cep


def find_cep(cep_number):
    """
    :param cep_number:
    :return:
    """
    cep_number = cep_validator(cep_number)
    providers_services = get_available_services()
    logger.debug(f"Available providers: {providers_services}")

    # Search in available services:
    async def task_viacep(cep_number: str):
        """
        :param cep_number:
        :return:
        """
        print("Starting Service task_viacep")
        await asyncio.sleep(2)
        start = datetime.now()
        result = await fetch_via_cep_service(cep_number)
        finish = datetime.now()
        print(f"VIACEP Request time: {finish - start}")
        return AddressInformation(**result)

    async def task_widenet(cep_number: str):
        """
        :param cep_number:
        :return:
        """
        print("Starting Service task_widenet")
        await asyncio.sleep(2)
        start = datetime.now()
        result = await fetch_wide_net_service(cep_number)
        finish = datetime.now()
        print(f"WIDENET Request time: {finish - start}")
        return AddressInformation(**result)

    async def task_brasilapi(cep_number: str):
        """
        :param cep_number:
        :return:
        """
        print("Starting Service task_brasilapi")
        await asyncio.sleep(2)
        start = datetime.now()
        result = await fetch_brasilapi_service(cep_number)
        finish = datetime.now()
        print(f"BRASILAPI Request time: {finish - start}")
        return AddressInformation(**result)

    async def task_correios(cep_number: str):
        """
        :param cep_number:
        :return:
        """
        print("Starting Service task_correios")
        await asyncio.sleep(2)
        start = datetime.now()
        result = await fetch_correios_service(cep_number)
        finish = datetime.now()
        print(f"CORREIOS Request time: {finish - start}")
        return AddressInformation(**result)

    async def main(cep_number: str):
        """
        :param cep_number:
        :return:
        """
        task1 = asyncio.create_task(task_viacep(cep_number))
        task2 = asyncio.create_task(task_widenet(cep_number))
        task3 = asyncio.create_task(task_brasilapi(cep_number))
        task4 = asyncio.create_task(task_correios(cep_number))

        result_of_task1 = await task1
        result_of_task2 = await task2
        result_of_task3 = await task3
        result_of_task4 = await task4

        # TODO implement this exception
        if not result_of_task1:
            raise AllServicesNotFoundException()

        return result_of_task1, result_of_task2, result_of_task3, result_of_task4

    return asyncio.run(main(cep_number))
