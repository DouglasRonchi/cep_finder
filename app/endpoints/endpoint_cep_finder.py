import http
from datetime import datetime

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exceptions.cep_finder_exceptions import CepFinderError, ServiceError, AllServicesNotFound
from app.services.cep_finder_service import CepService
from app.utils.logger import logger

router = APIRouter()


@router.get('/{cep_number}')
def new_ticket(cep_number: str, request: Request):
    try:
        logger.info(f'CEP received: {cep_number}')
        return CepService().find_cep(cep_number)

    except CepFinderError as err:
        logger.error(f'Error: {err} in CEP Finder: {cep_number}')
        content = {
            "DateTime": f'{datetime.now()}',
            "Error": f'{err.error}',
            "Type": f'{err.type}',
            "Message": f'{err.message}'
        }
        return JSONResponse(status_code=http.HTTPStatus.BAD_REQUEST, content=content)

    except ServiceError as err:
        logger.error(f'Error: {err} in CEP Finder: {cep_number}')
        content = {
            "DateTime": f'{datetime.now()}',
            "Service": f'{err.service}',
            "Type": f'{err.type}',
            "Message": f'{err.message}'
        }
        return JSONResponse(status_code=http.HTTPStatus.BAD_REQUEST, content=content)

    except AllServicesNotFound as err:
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
