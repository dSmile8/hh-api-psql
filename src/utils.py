from work_with_file import WorkWithFile
from pathlib import Path

DATA_DIR_VACANCIES = Path(__file__).parent.parent.joinpath('data', 'hh.json')


def print_employers(data):
    data1 = WorkWithFile(data).data_from_json()

    for dat in data1['items']:
        for k, v in dat['employer'].items():
            if k == 'id':
                print(f"{dat['employer']['name']} - {v}")


def create_company_list():
    company_list = []
    while True:
        try:
            company_name = int(input('Введите id компаний из предоставленного списка. Что-бы закончить'
                                     ' ввод компаний, напишите 0 - ноль'))
            if company_name == 0:
                break
            else:
                company_list.append(company_name)
        except ValueError:
            print('Вводить нужно число, внимательней!')
    return company_list




if __name__ == '__main__':
    # print_employers(DATA_DIR_VACANCIES)
    print(create_company_list())
