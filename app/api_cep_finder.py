from fastapi import APIRouter

from app.endpoints import endpoint_cep_finder

cep_finder_api_router = APIRouter()
cep_finder_api_router.include_router(endpoint_cep_finder.router, prefix="", tags=["cep_finder"])
