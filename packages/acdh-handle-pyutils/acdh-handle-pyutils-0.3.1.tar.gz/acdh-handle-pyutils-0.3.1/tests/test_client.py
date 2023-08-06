import os
import unittest
from acdh_handle_pyutils.client import HandleClient

HANDLE_USERNAME = os.environ.get('HANDLE_USERNAME')
HANDLE_PASSWORD = os.environ.get('HANDLE_PASSWORD')
URL_TO_REGISTER = "https://id.hansi4ever.com/123"
cl = HandleClient(HANDLE_USERNAME, HANDLE_PASSWORD)
cl_one = HandleClient(HANDLE_USERNAME, HANDLE_PASSWORD, hdl_prefix='21.1234/')


class TestClient(unittest.TestCase):
    """Tests for `acdh_handle_pyutils.client` module."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001(self):
        self.assertTrue(cl.url.endswith('/'))
        self.assertTrue(cl_one.url.endswith('/'))

    def test_002_register_handle(self):
        result = cl.register_handle(URL_TO_REGISTER, full_url=False)
        self.assertTrue(cl.prefix in result)
        result = cl.register_handle(URL_TO_REGISTER, full_url=True)
        self.assertTrue(result.startswith('http'))
