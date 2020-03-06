import os
import json
from datetime import datetime, timedelta
import requests
import time
import logging

class GetCompaniesHouseData:
    """ GetCompaniesHouseData Downloader.
    Arguments:
    - words (string): The term being searched for.
    - per_page (integer): The number of search results to return per page. Integer lower than 100.
    Default value: 50 """
    def __init__(self, words=None, per_page=None, start_index=None):
        self.start_index = start_index
        self.per_page = per_page
        self.words = words
        self.base_url = "https://api.companieshouse.gov.uk"
        self.data = "{'Accept': 'application/json'}"
        self.header = {}
        self.query = None
        self.endpoint = None
        self.input_validation()
        self.set_api_config()
        

    def validate_words(self):
        """ Validates word arg """
        if self.words is None:
            raise ValueError("words argument can not be null")
        else:
            pass

    def validate_per_page(self):
        """ Validates per_page arg and sets per_page if argument is being passed """
        if self.per_page is not None:
            if self.per_page > 100:
                raise ValueError("Per page argument can not be greater than 100")
            else:
                pass
        else:
            self.per_page = 50

    def input_validation(self):
        """ Validates survey_id and start_date """
        self.validate_words()
        self.validate_per_page()
        

    def set_header(self):
        """ Sets header using the access_key """
        self.header['Authorization'] = self.access_key

    def set_query(self):
        """ Sets query params """
        self.query = """/search/companies?q={}&items_per_page={}&start_index={}""".format( self.words, self.per_page, self.start_index)

    def set_api_config(self):
        """ Sets the header, path and query needed to make the api call"""
        try:
            self.access_key = os.environ["companies_house_api_key"]
        except KeyError:
            raise KeyError("company_house_api_key env variable needed")
        self.set_header()
        self.set_query()

    def set_endpoint(self):
        """ Sets the end point using the base_url, path, query """
        self.set_query()
        endpoint = self.base_url + self.query
        return endpoint

    def api_call(self, endpoint):
        """ Make the API request """
        while True:
            response = requests.get(
                endpoint, 
                data=self.data, 
                headers=self.header)
            if response.status_code == 200:
                data = json.loads(response.content)
                break
            if response.status_code == 429:
                self.sleep()
                pass
            else:
                data = []
                raise ValueError("HTTP Error {}".format(response.status_code))
                
        return data

    def download(self):
        """ Gets the responses based on page_number """               
        endpoint = self.set_endpoint()
        responses = self.api_call(endpoint)
        return responses

    def download_all(self):
        print("Download - started")
        ls = []
        while True:  
            response = self.download()    
            if response['items'] == []:
                print("Done")
                break
            else:
                ls.extend(response['items'])            
                self.start_index = response['start_index'] + self.per_page
        return ls

    def sleep(self):
        print('Too Many Requests - sleep 5 minutes')
        time.sleep(300) # sleep 5 minutes 