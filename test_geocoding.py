import requests
import pytest

from data import TEST_DATA_AVAILABLE_METHODS
from data import TEST_DATA_CHECK_RESPONSE_HEADERS
from data import TEST_DATA_CHECK_DIRECT_GEOCODING
from data import TEST_DATA_CHECK_REVERSE_GEOCODING
from data import TEST_DATA_CHECK_ADDITIONAL_PARAM
from data import TEST_DATA_CHECK_QUANTITY_PARAM
from data import SEARCH_API
from data import REVERSE_API


@pytest.mark.parametrize('actual_method, actual_url, actual_params', TEST_DATA_AVAILABLE_METHODS)
def test_api_http_methods(actual_method, actual_url, actual_params):
    response = requests.request(method=actual_method, url=actual_url, params=actual_params)
    assert response.status_code == 200, f'{actual_method} is not supported for you'


@pytest.mark.parametrize('actual_url, actual_params, expected_data', TEST_DATA_CHECK_RESPONSE_HEADERS)
def test_api_check_headers(actual_url, actual_params, expected_data):
    response = requests.get(url=actual_url, params=actual_params)
    actual_header_content_type = response.headers["Content-Type"]
    assert expected_data in actual_header_content_type \
           and response.status_code == 200, f'Wrong type of response header, ' \
                                            f'have {actual_header_content_type},expected {expected_data}'


@pytest.mark.parametrize('actual_params, expected_data', TEST_DATA_CHECK_DIRECT_GEOCODING)
def test_api_prove_direct_geocoding(actual_params, expected_data):
    response = requests.get(url=SEARCH_API, params=actual_params)
    actual_location = response.json()[0]['display_name']
    assert expected_data in actual_location and response.status_code == 200, \
        f'Wrong location in response, have {actual_location}, expected {expected_data}'


# @pytest.mark.skip
@pytest.mark.parametrize('actual_params, expected_data', TEST_DATA_CHECK_REVERSE_GEOCODING)
def test_api_prove_reverse_geocoding(actual_params, expected_data):
    response = requests.get(url=REVERSE_API, params=actual_params)
    actual_location = response.json()['display_name']
    assert expected_data in actual_location and response.status_code == 200, \
        f'Wrong latitude or longitude, have {actual_location}, expected {expected_data}'


@pytest.mark.parametrize('actual_url, actual_params, expected_data', TEST_DATA_CHECK_ADDITIONAL_PARAM)
def test_api_prove_additional_params_for_direct_and_reverse_output(actual_url, actual_params, expected_data):
    response = requests.get(url=actual_url, params=actual_params)
    if 'search' in actual_url:
        if 'limit' in actual_params:
            additional_param = len(response.json())
        else:
            additional_param = response.json()[0][expected_data]
    else:
        additional_param = response.json()[expected_data]
    assert additional_param and response.status_code == 200, \
        f'There is not correct additional parameter {expected_data} of output'


@pytest.mark.parametrize('actual_params, expected_data', TEST_DATA_CHECK_QUANTITY_PARAM)
def test_api_prove_additional_params_for_direct_quantity_output(actual_params, expected_data):
    response = requests.get(url=SEARCH_API, params=actual_params)
    quantity_param = len(response.json())
    assert quantity_param == expected_data and response.status_code == 200, \
        f'Something wrong with limitation, have {quantity_param}, expected {expected_data}'
