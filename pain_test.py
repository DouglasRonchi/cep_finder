from app.services.cep_finder_service import CepService

with open('LOG_LOGRADOURO_SC.TXT', 'r') as file:
    for line in file:
        print(CepService().find_cep(line.split('@')[7]))
