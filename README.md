# Companies House Analysis

This tool extracts Companies House information through API call and answer the following questions:

1. How many companies are there which match the search term “sono”?
(Note the following questions are all in the context of the set of companies from Q1)
2. Of these how many are active?
3. Of those dissolved what is the average life of the company (incorporation date to cessation date) in days?
4. When was the first limited-partnership created?
5. Which companies also have “vate” in their title?
6. Taking the digits from the premises part of the address to make a number for each company (e.g. 6-8 = 68, 14b = 14, 1st Floor 45 Main St= 145 etc) what is the sum for each company type?

## Assumptions:

* search is not case sensitive, "SONO" and "sono" are equivalent as well "vate" and "VATE"

* average life of the company is defined by the difference in day between date_of_cessation and date_of_creation 

* companies with no address information are escluded from the domain of Q6

## Set up

* clone the repo

* install the packages
```sh
pip3 install -r requirements.txt 
```

* create env variable
```sh
export companies_house_api_key=your_api_key
```
## API key authentication

The Companies House API requires authentication credentials, in the form of an API key, to be sent with each request.

Please follow the link's instructions to create your personal key

https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted/apikey_authorisation.html

## Basic Usage

To execute a script, make sure you are at the project directory

```sh
python3 main.py
```

## Run the test

To execute a script, make sure you are at the project directory

```sh
python3 test.py
```

or 

```sh
pytest test.py
```

## Consideration 

* The tool does not retain data permanently
* GetCompaniesHouseData Input and Error Handling are in place
* In case of response.status_code == 429 the message 'Too Many Requests - sleep 5 minutes' is printed, the app sleeps for 5 minutes before continuing pulling data







