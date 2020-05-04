from Task3.Class.company import Company
import json


# Data read from json
def read_from_json(file_name):

    companies = []
    with open(file_name) as json_data:
        data = json.load(json_data)

    for company in data:
        companies.append(
            Company(company['name'], company['clutch_profile'], company['country'], company['website'], company['rank']))

    return companies


# Data write into json
def write_to_json(companies, file_name):

    company_list = []

    for company in companies:

        json_block = {'name': company.name, 'clutch_profile': company.clutch_profile, 'country': company.country,
                      'website': company.website, 'rank': company.rank}

        company_list.append(json_block)

    with open(file_name, 'w') as data_output:
        json.dump(company_list, data_output, indent=2)
