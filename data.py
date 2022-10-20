import pytest


SEARCH_API = 'https://nominatim.openstreetmap.org/search'
REVERSE_API = 'https://nominatim.openstreetmap.org/reverse'

TEST_DATA_AVAILABLE_METHODS = [
    ('GET', SEARCH_API, ''),
    ('OPTIONS', SEARCH_API, ''),
    ('GET', REVERSE_API, 'lat=51.10502&lon=71.50158&format=json'),
    ('OPTIONS', REVERSE_API, 'lat=51.10502&lon=71.50158&format=json'),
    # negative
    pytest.param('PUT', SEARCH_API, 'q=Russia&format=json',
                 marks=pytest.mark.skip('Available methods should be "POST,OPTIONS"')),
    pytest.param('DELETE', REVERSE_API, 'lat=51.10502&lon=71.50158&',
                 marks=pytest.mark.skip('Available methods should be "POST,OPTIONS"')),
    pytest.param('GET', SEARCH_API, 123, marks=pytest.mark.xfail),
]

TEST_DATA_CHECK_RESPONSE_HEADERS = [
    (SEARCH_API, '', 'text/html'),  # testing response format in /search section
    (SEARCH_API, 'format=', 'application/json'),
    (SEARCH_API, 'format=json', 'application/json'),
    (SEARCH_API, 'format=geojson', 'application/json'),
    (SEARCH_API, 'format=xml', 'text/xml'),
    (SEARCH_API, 'format=html', 'text/html'),
    (SEARCH_API, 'format=jsonv2', 'application/json'),
    (SEARCH_API, 'format=geocodejson', 'application/json'),
    (REVERSE_API, 'lat=51.10502&lon=71.50158', 'text/xml'),  # testing response format in /reverse section
    (REVERSE_API, 'lat=51.10502&lon=71.50158&format=', 'text/xml'),
    (REVERSE_API, 'lat=51.10502&lon=71.50158&format=json', 'application/json'),
    (REVERSE_API, 'lat=51.10502&lon=71.50158&format=geojson', 'application/json'),
    (REVERSE_API, 'lat=51.10502&lon=71.50158&format=xml', 'text/xml'),
    (REVERSE_API, 'lat=51.10502&lon=71.50158&format=html', 'text/html'),
    (REVERSE_API, 'lat=51.10502&lon=71.50158&format=jsonv2', 'application/json'),
    (REVERSE_API, 'lat=51.10502&lon=71.50158&format=geocodejson', 'application/json'),
    # negative part
    pytest.param(SEARCH_API, 'format=123', 'application/json', marks=pytest.mark.xfail),
    pytest.param(REVERSE_API, 'lat=51.10502&lon=71.50158&format=123', 'text/xml', marks=pytest.mark.xfail),
    pytest.param(SEARCH_API, 'format=json', 'text/xml', marks=pytest.mark.xfail),
    pytest.param(REVERSE_API, 'lat=51.10502&lon=71.50158&format=html', 'text/xml', marks=pytest.mark.xfail),
]

TEST_DATA_CHECK_DIRECT_GEOCODING = [
    ('q=Красная Площадь&format=json', 'Красная площадь'),  # testing q=query
    ('q=Казахстан Астана 010000&format=json', 'район Есиль'),
    ('q=Лувр&accept-language=en&format=json', 'Louvre'),  # testing accept-language priority
    ('city=Paris&format=json', 'Paris'),  # testing single param
    ('street=72 Будапештская&postalcode=192284&format=json', 'Купчино'),
    ('country=Russia&city=Санкт-Петербург&state=Санкт-Петербург&street=Малая Балканская&county=Балканский&format=json', '192289'),
    ('street=-40 Будапештская&format=json', 'Россия'),  # testing negative number
    ('street=Москва&countrycodes=us&format=json', 'United States'),  # testing countrycodes=<countrycode> and negative number
    # negative part
    pytest.param('q=', '', marks=pytest.mark.xfail),
    pytest.param('Moscow', '', marks=pytest.mark.xfail),
    pytest.param('q=123', '', marks=pytest.mark.xfail),
    pytest.param('q=Moscow&accept-language=ru&format=json', 'Moscow', marks=pytest.mark.xfail),
    pytest.param('coutry=Germany&format=json', 'Germany', marks=pytest.mark.xfail),
    pytest.param('postcode=Moscow&format=json', 'Moscow', marks=pytest.mark.xfail),
    pytest.param('street=0 Будапештская&format=json', 'Купчино', marks=pytest.mark.xfail),
]

TEST_DATA_CHECK_REVERSE_GEOCODING = [
    ('lat=56&lon=38&format=json', 'Щёлково'),
    ('lat=-17&lon=-48&format=json', 'Brasil'),
    #negative
    pytest.param('lat=56,4343&lon=38,3252&format=json', 'Щёлково', marks=pytest.mark.xfail),
    pytest.param('lat=-181&lon=190&format=json', '', marks=pytest.mark.xfail),
    pytest.param('&format=json', '', marks=pytest.mark.xfail),
    pytest.param('lat=&lon=&format=json', '', marks=pytest.mark.xfail),
    pytest.param('lat=-181&format=json', '', marks=pytest.mark.xfail),
    pytest.param('lat=nine&lon=four&format=json', '', marks=pytest.mark.xfail)
]

TEST_DATA_CHECK_ADDITIONAL_PARAM = [
    (SEARCH_API, 'q=Saint-Petersburg&extratags=1&format=json', 'extratags'),  # testing additional output param
    (SEARCH_API, 'q=Saint-Petersburg&addressdetails=1&format=json', 'address'),
    (SEARCH_API, 'q=Saint-Petersburg&namedetails=1&format=json', 'namedetails'),
    (REVERSE_API, 'lat=56&lon=38&extratags=1&format=json', 'extratags'),
    (REVERSE_API, 'lat=56&lon=38&addressdetails=1&format=json', 'address'),
    (REVERSE_API, 'lat=56&lon=38&namedetails=1&format=json', 'namedetails'),
    pytest.param(SEARCH_API, 'q=Saint-Petersburg&format=json', 'namedetails', marks=pytest.mark.xfail),
    pytest.param(SEARCH_API, 'q=Saint-Petersburg&extratags&format=json', 'extratags', marks=pytest.mark.xfail),
]

TEST_DATA_CHECK_QUANTITY_PARAM = [
    ('q=Saint-Petersburg&limit=1&format=json', 1),  # testing limit param
    ('q=Saint-Petersburg&limit=0&format=json', 1),
    ('q=Moscow&limit=51&format=json', 50),
    ('q=Moscow&limit=50&format=json', 50),
    ('q=Saint-Petersburg&format=json', 10),
    ('q=Saint-Petersburg&limit=-1&format=json', 1),
    pytest.param('q=Saint-Petersburg&limit&format=json', 10, marks=pytest.mark.xfail),
    pytest.param('q=Saint-Petersburg&limit=0.1&format=json', 1, marks=pytest.mark.xfail),
    pytest.param('q=Saint-Petersburg&limit=one&format=json', 1, marks=pytest.mark.xfail),
]
