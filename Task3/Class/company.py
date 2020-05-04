
class Company:
    def __init__(self, name, clutch_profile, country, website, rank):
        self.name = name
        self.clutch_profile = clutch_profile
        self.country = country
        self.website = website
        self.rank = rank

    def print_company_info(self):
        print(f'Name: {self.name}')
        print(f'Clutch profile: {self.clutch_profile}')
        print(f'Country: {self.country}')
        print(f'Website: {self.website}')
        print(f'Rank: {self.rank}')

        return 'Company info printed'

    def is_american(self, country):

        list_america = ['NY', 'CA', 'MA']

        if country in list_america:
            return True
        else:
            return False

    def get_rank(self):
        return self.rank

    def is_icp(self):
        if self.rank <= 2000000:
            print('Company matches defined ICP profile')

