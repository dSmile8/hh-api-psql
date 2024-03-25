def print_employers(data) -> None:
    """Выводит в консоль список компаний и их id из запроса"""

    for dat in data['items']:
        for k, v in dat['employer'].items():
            if k == 'id':
                print(f"{dat['employer']['name']} - {v}")


def create_company_list() -> list:
    """Создает список из id компаний"""

    company_list = []
    while True:
        try:
            company_name = int(input('Введите id компаний из предоставленного списка. Что-бы закончить'
                                     ' ввод компаний, введите 0 - ноль.'))
            if company_name == 0:
                break
            else:
                company_list.append(company_name)
        except ValueError:
            print('Вводить нужно число, внимательней!')
    return company_list


def sort_data(data):
    """Создает отсортированный список вакансий, с нужными параметрами"""

    data_list = []
    for i in data['items']:
        if i['salary'] is None:
            salary_from = None
            salary_to = None
            currency = None
        else:
            salary_to = i['salary']['to']
            salary_from = i['salary']['from']
            currency = i['salary']['currency']

        data_dict = {
            'vacancy_id': i['id'],
            'vacancy_name': i['name'],
            'city': i['area']['name'],
            'salary_from': salary_from,
            'salary_to': salary_to,
            'currency': currency,
            'published': i['published_at'],
            'url': i['alternate_url'],
            'company_name': i['employer']['name'],
            'requirement': i['snippet']['requirement'],
            'schedule': i['schedule']['name'],
            'experience': i['experience']['name'],
        }
        data_list.append(data_dict)
    return data_list


if __name__ == '__main__':
    pass
