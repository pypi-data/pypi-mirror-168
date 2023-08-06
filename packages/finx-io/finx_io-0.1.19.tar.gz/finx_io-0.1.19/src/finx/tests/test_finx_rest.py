import os
from unittest import TestCase

from finx.finx_rest import FinXRest

class TestFinxRest(TestCase):
    def test_can_connect(self):
        try:
            this_key = os.environ['FINX_API_KEY']
            finx_rest = FinXRest(this_key)
        except:
            this_key = 'public'
            finx_rest = FinXRest()
        finx_rest.connect()
        self.assertEquals(finx_rest.api_key, this_key)
