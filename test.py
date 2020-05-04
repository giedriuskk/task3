from Task3.Class.american import American
from Task3.Class.company import Company
from Task3.Class.other import Other
import read_write

def unittest():
    for item in companies:
        item.print_company_info()
        if Company.is_american(Company, item.country):
            american_list.append(item)
        else:
            if Other.is_not_banned(Other, item.country):
                other_list.append(item)
    try:
        Other.avg_rank(Other, other_list)
        American.avg_rank(American, american_list)
    except:
        pass


# DEMO
companies = []
american_list = []
other_list = []

companies = read_write.read_from_json('test.json')
unittest()
read_write.write_to_json(companies, 'test.json')
