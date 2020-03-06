import api
import pandas as pd
import pprint
from collections import Counter
import pandas as pd
import re
import numpy as np

def search_for(words):
    match_search_sono = api.GetCompaniesHouseData(words=words, per_page=100)
    ch_list_sono = match_search_sono.download_all()
    # list( map( pprint.pprint, ch_list_sono) )
    return  ch_list_sono

def count_sono_companies(lst):
    return len(lst)

def active_sono_companies(lst):
    return len(list(filter(lambda x: x['company_status']=='active', lst)))

def average_life_of_dissolved(lst):
    lst_incorporated = list(filter(lambda x: x['company_status']=='dissolved', lst))
    df = pd.DataFrame(lst_incorporated)
    df['date_of_cessation'] = pd.to_datetime(df['date_of_cessation'], format='%Y-%m-%d')
    df['date_of_creation'] = pd.to_datetime(df['date_of_creation'], format='%Y-%m-%d')
    df['days'] = df['date_of_cessation'] - df['date_of_creation']   
    return df['days'].mean().days

def first_limited_partnership_created_date(lst):
    list_limited_partnership = list(filter(lambda x: x['company_type']=='limited-partnership', lst))
    return sorted(list_limited_partnership, key = lambda i: i['date_of_creation'],reverse=False)[0]['date_of_creation']

def companies_sono_and_vate(lst):
    ch_list_sono_and_vate = list(filter(lambda x: 'vate' in x['title'].lower(), lst))
    return list(map(lambda x: x['title'], ch_list_sono_and_vate))

def sum_premises_digit_by_company_type(lst):
    df = pd.DataFrame(lst)
    df = df[df['address'].notna()]
    df['premises_num'] = df.apply(lambda x: int("".join(re.findall(r'\d+', x['address'].get('premises', "0"))) or 0), axis=1)
    return df[['premises_num', 'company_type']].groupby(['company_type']).sum().to_dict()['premises_num']

def main():
    extract_sono_companies = search_for('sono')
    print('1 - How many companies are there which match the search term “sono": {}'.format(count_sono_companies(extract_sono_companies)))
    print('2 - Of these how many are active?": {}'.format(active_sono_companies(extract_sono_companies)))
    print('3 - Of those dissolved what is the average life of the company (incorporation date to cessation date) in days?": {}'.format(average_life_of_dissolved(extract_sono_companies)))
    print('4 - When was the first limited-partnership created?": {}'.format(first_limited_partnership_created_date(extract_sono_companies)))
    print('5 - Which companies also have “vate” in their title?": \n {}'.format(companies_sono_and_vate(extract_sono_companies)))
    print('6 - Taking the digits from the premises part of the address to make a number for each company (e.g. 6-8 = 68, 14b = 14, 1st Floor 45 Main St= 145 etc) what is the sum for each company type?": ')
    pprint.pprint(sum_premises_digit_by_company_type(extract_sono_companies))

if __name__ == "__main__":
    main()