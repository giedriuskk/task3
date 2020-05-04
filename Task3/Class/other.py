from Task3.Class import company


class Other(company.Company):
    def __init__(self, name, clutch_profile, country, website, rank, avg_rank):
        super().__init__(self, name, clutch_profile, country, website, rank)
        self.avg_rank = avg_rank

    def avg_rank(self, ranks):
        total = 0
        for i in ranks:
            total = total + i.rank
        self.avg_rank = total / len(ranks)
        print(f'Average rank of Other companies {round(self.avg_rank)}')
        return round(self.avg_rank)

    def is_not_banned(self, country):

        list_banned = ['Pakistan', 'China']

        if country in list_banned:
            return False
        else:
            return True