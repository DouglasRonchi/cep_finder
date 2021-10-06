"""
This is a Exception module for cep_finder api
"""


class InvalidCepException(Exception):
    """Exception raised for errors in the input cep.

     Attributes:
         type -- the error type
         error -- generic error
         message -- explanation of the error
     """

    def __init__(self, type, error, message="Invalid CEP"):
        self.type = type
        self.error = error
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.type} - {self.error} - {self.message}'


class ServiceException(Exception):
    """Exception raised for errors in the cep service.

     Attributes:
         type -- the error type
         message -- explanation of the error
         service -- service where error occurs
    """
    def __init__(self, message, service):
        self.type = 'ServiceException'
        self.message = message
        self.service = service
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.type} - {self.message} - {self.service}'


class AllServicesNotFoundException(Exception):
    """Exception raised when all services cannot give the ok response.

     Attributes:
         type -- the error type
         message -- explanation of the error
         error -- generic error message
    """
    def __init__(self, message=None, error=None):
        self.type = 'AllServicesError'
        self.message = "Não foi possível localizar o cep em nenhum dos serviços"
        self.error = "CEP Inválido"
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.type} - {self.error} - {self.message}'


class CepNotFoundException(Exception):
    """Exception raised when cannot find information on service.

     Attributes:
         type -- the error type
         message -- explanation of the error
         service -- service where error occurs
    """
    def __init__(self, message=None, error=None, service=None):
        self.type = 'CepNotFoundError'
        self.message = "Não foi possível localizar o cep no serviço"
        self.service = service
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.type} - {self.service} - {self.message}'


class CantConnectWithServiceException(Exception):
    """Exception raised when cannot connect with service.

     Attributes:
         type -- the error type
         message -- explanation of the error
         service -- service where error occurs
    """
    def __init__(self, message=None, error=None, service=None):
        self.type = 'CantConnectWithService'
        self.message = "Não foi possível localizar o cep no serviço"
        self.service = service
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.type} - {self.service} - {self.message}'


class CantFetchResponseException(Exception):
    """Exception raised when cannot connect with service.

     Attributes:
         type -- the error type
         message -- explanation of the error
    """
    def __init__(self, message=None, error=None):
        self.type = 'CantConnectWithService'
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f'{self.type} - {self.message}'
