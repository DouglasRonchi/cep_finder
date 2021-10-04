from fastapi import FastAPI

from app.api_cep_finder import cep_finder_api_router
from app.utils.logger import logger

logger.info(f"Starting CEP Finder")
app = FastAPI(title='CEP Finder')

app.include_router(cep_finder_api_router, prefix="/cep")
