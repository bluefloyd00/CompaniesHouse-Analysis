import unittest
from unittest import mock
from api import GetCompaniesHouseData
import json
from main import count_sono_companies
from main import active_sono_companies
from main import first_limited_partnership_created_date
from main import companies_sono_and_vate
from main import sum_premises_digit_by_company_type
from main import average_life_of_dissolved


def data_generator(number):
    list_ = []
    for i in range(number):
        list_.append({'key_{}'.format(i): 'value_{}'.format(i)})
    return json.dumps({"items": list_, 'start_index': number})

class TestGetCompaniesHouseDataInput(unittest.TestCase):
    """ Testing GetCompaniesHouseData Input and Error Handling """


    def test_words_error(self):
        """ Expects an error as the words param is null """
        self.assertRaisesRegex(ValueError,
                               "words argument can not be null",
                               GetCompaniesHouseData)

    def test_date_format_error(self):
        """ Expects an error as the per_page is > 100 """
        self.assertRaisesRegex(ValueError,
                               "Per page argument can not be greater than 100",
                               GetCompaniesHouseData, words='test', per_page=200)

def mocked_requests_get(*args, **kwargs):
    """ Mocks API responses from GetCompaniesHouseData """
    class MockResponse:
        """ Mock Response Class """
        def __init__(self, content, status_code):
            self.content = content
            self.status_code = status_code

    if args[0] == 'http://my_url.com/search?q=test&items_per_page=3':
        return MockResponse(data_generator(3), 200)
    elif args[0] == 'http://my_url.com/search?q=test&items_per_page=4':
        return MockResponse(data_generator(4), 200)
    else:
        raise ValueError("Test URL is not set")


class TestGetCompaniesHouseDataDowloader(unittest.TestCase):

    def setUp(self):
        self.gcd = GetCompaniesHouseData(words='test', per_page=4)
    
    def test_downloader(self):
        """ Tests that all the pages are downloaded endpoint"""
        with mock.patch('api.GetCompaniesHouseData.set_endpoint') as mocked_endpoints, \
            mock.patch('requests.get') as mocked_requests:
            mocked_endpoints.side_effect = ['http://my_url.com/search?q=test&items_per_page=3',
                                            'http://my_url.com/search?q=test&items_per_page=4']
            mocked_requests.side_effect = mocked_requests_get
            companies = self.gcd.download()
            calls = [mock.call('http://my_url.com/search?q=test&items_per_page=3',
                                data=self.gcd.data,
                                headers=self.gcd.header)]
            mocked_requests.assert_has_calls(calls, any_order=False)

            companies = self.gcd.download()
            calls = [mock.call('http://my_url.com/search?q=test&items_per_page=4',
                                data=self.gcd.data,
                                headers=self.gcd.header)]
            mocked_requests.assert_has_calls(calls, any_order=False)

class TestMain(unittest.TestCase):

    def test_sono_companies(self):
        mock_sono_data = [            
            {'title': 'Sono1'},
            {'title': 'Sonoko 2'},
            {'title': 'test Sonoko Sono'}
        ]
        self.assertEqual( count_sono_companies( mock_sono_data) , 3)


    def test_active_sono_companies(self):
        mock_sono_data = [            
            {'title': 'Sono1', 'company_status': 'active'},
            {'title': 'Sonoko 2', 'company_status': 'dissolved'},
            {'title': 'test Sonoko Sono', 'company_status': 'active'}
        ]
        self.assertEqual( active_sono_companies( mock_sono_data) , 2)

    def test_average_life_of_dissolved(self):
        mock_sono_data = [            
            {'title': 'Sono1', 'company_status': 'active',  'date_of_cessation': '2015-12-22', 'date_of_creation': '2014-07-28' },
            {'title': 'Sonoko 2', 'company_status': 'dissolved',  'date_of_cessation': '2015-12-22', 'date_of_creation': '2014-07-28'},
            {'title': 'test Sonoko Sono', 'company_status': 'active', 'date_of_cessation': '2015-12-22', 'date_of_creation': '2014-07-28'}
        ]
        self.assertTrue( average_life_of_dissolved( mock_sono_data) , 363)

    def test_first_limited_partnership_created_date(self):
        mock_sono_data = [            
            {'title': 'Sonotest1', 'company_status': 'active', 'company_type': 'limited-partnership', 'date_of_creation': '2013-04-22'},
            {'title': 'Sonoko test2', 'company_status': 'dissolved', 'company_type': 'limited-partnership', 'date_of_creation': '2013-04-21'},
            {'title': 'test Sonoko Sono', 'company_status': 'active' , 'company_type': 'ltd', 'date_of_creation': '2013-04-21'}
        ]
        self.assertEqual( first_limited_partnership_created_date( mock_sono_data) , '2013-04-21')
    
    def test_count_of_sono_and_vate(self):
        mock_sono_data = [            
            {'title': 'Sono1', 'company_status': 'active'},
            {'title': 'Sono vate', 'company_status': 'dissolved'},
            {'title': 'SonoVATE', 'company_status': 'active'}
        ]
        self.assertEqual( companies_sono_and_vate( mock_sono_data) , ['Sono vate', 'SonoVATE'])

    def test_sum_premises_digit_by_company_type(self):
        mock_sono_data = [            
            {'title': 'Sono1', 'company_type': 'ltd', 'address': {'address_line_1': 'Minterne Waye', 'premises': '6-8'}},
            {'title': 'Sono vate', 'company_type': 'limited-partnership', 'address': {'address_line_1': 'Minterne Waye', 'premises': '14b '}},
            {'title': 'SonoVATE', 'company_type': 'ltd', 'address': {'address_line_1': 'Minterne Waye', 'premises': '1st Floor 45 Main St'}},
            {'title': 'SonoVATE2', 'company_type': 'ltd', 'address': {'address_line_1': 'Minterne Waye', 'premises': 'test '}},
            {'title': 'SonoVATE5', 'company_type': 'ltd', 'address': {'address_line_1': 'Minterne Waye'}},
            {'title': 'SonoVATE4', 'company_type': 'ltd'}
        ]
        self.assertEqual( sum_premises_digit_by_company_type( mock_sono_data) , {'ltd': 213, 'limited-partnership': 14})

if __name__ == "__main__":
    unittest.main()