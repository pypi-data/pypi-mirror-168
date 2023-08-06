from verisure.session import base_url_func
from collections import namedtuple

class TestBaseUrlFunc:
    Response = namedtuple("Response", ['status_code', 'text'])


    def test_success(self):
        # m-api01 should be used first time
        post = base_url_func(lambda x:\
            TestBaseUrlFunc.Response(status_code=200, text="200")\
            if x == 'https://m-api01.verisure.com'\
            else TestBaseUrlFunc.Response(status_code=300, text="300"))
        response = post("")
        assert response.status_code == 200

        # m-api01 should be used again since it worked first time
        post = base_url_func(lambda x:\
            TestBaseUrlFunc.Response(status_code=200, text="200")\
            if x == 'https://m-api01.verisure.com'\
            else TestBaseUrlFunc.Response(status_code=300, text="300"))
        response = post("")
        assert response.status_code == 200

    def test_switch(self):
        # m-api01 will fail and m-api02 should be used
        post = base_url_func(lambda x:\
            TestBaseUrlFunc.Response(status_code=300, text="300")\
            if x == 'https://m-api01.verisure.com'\
            else TestBaseUrlFunc.Response(status_code=200, text="200"))
        response = post("")
        assert response.status_code == 200

        # m-api02 should be used again since it worked last time
        post = base_url_func(lambda x:\
            TestBaseUrlFunc.Response(status_code=300, text="300")\
            if x == 'https://m-api01.verisure.com'\
            else TestBaseUrlFunc.Response(status_code=200, text="200"))
        response = post("")
        assert response.status_code == 200

        