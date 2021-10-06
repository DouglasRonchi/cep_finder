import unittest
from unittest.mock import patch

from app import main


class TestMain(unittest.TestCase):
    @patch('app.main.logger')
    @patch('app.main.FastAPI')
    @patch('app.main.cep_finder_api_router')
    def test_main(self,
                  cep_finder_router_mock,
                  fastapi_mock,
                  logger_mock):
        """
        Args:
            cep_finder_router_mock:
            fastapi_mock:
            logger_mock:
        """
        self.assertTrue(main.app)


if __name__ == '__main__':
    unittest.main()
