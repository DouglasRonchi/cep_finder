"""
This is a endpoint_cep_finder module for cep_finder api
"""
import http
from datetime import datetime

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exceptions.cep_finder_exceptions import InvalidCepException, ServiceException, AllServicesNotFoundException
from app.services.cep_finder_service import find_cep
from app.utils.logger import logger

router = APIRouter()


@router.get('/{cep_number}')
def new_ticket(cep_number: str, request: Request):
    """
    :param cep_number:
    :param request:
    :return:
    """
    try:
        logger.info(f'CEP received: {cep_number}')
        return find_cep(cep_number)

    except InvalidCepException as err:
        logger.error(f'Error: {err} in CEP Finder: {cep_number}')
        content = {
            "DateTime": f'{datetime.now()}',
            "Error": f'{err.error}',
            "Type": f'{err.type}',
            "Message": f'{err.message}'
        }
        return JSONResponse(status_code=http.HTTPStatus.BAD_REQUEST, content=content)

    except ServiceException as err:
        logger.error(f'Error: {err} in CEP Finder: {cep_number}')
        content = {
            "DateTime": f'{datetime.now()}',
            "Service": f'{err.service}',
            "Type": f'{err.type}',
            "Message": f'{err.message}'
        }
        return JSONResponse(status_code=http.HTTPStatus.BAD_REQUEST, content=content)

    except AllServicesNotFoundException as err:
        logger.error(f'Error: {err} in CEP Finder: {cep_number}')
        content = {
            "DateTime": f'{datetime.now()}',
            "Error": f'{err.error}',
            "Type": f'{err.type}',
            "Message": f'{err.message}'
        }
        return JSONResponse(status_code=http.HTTPStatus.BAD_REQUEST, content=content)

    except Exception as err:
        logger.error(f'Error: {err} in CEP Finder: {cep_number}')
        content = {
            "DateTime": f'{datetime.now()}',
            "Error": 'CEP Finder Error',
            "Type": 'Internal Error',
            "Message": 'CEP Finder internal Error'
        }
        return JSONResponse(status_code=http.HTTPStatus.BAD_REQUEST, content=content)
