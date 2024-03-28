from abc import ABC, abstractmethod
import requests


class ApiVacancyService(ABC):

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def connecting_to_api(self):
        pass


class HeadHunterAPI(ApiVacancyService):

    def __init__(self, name: str, company_id: list = None):
        self.__url = 'https://api.hh.ru/vacancies'
        self.__name = name
        self.__company_id = company_id
        self.__params = {
            'text': self.__name,
            'per_page': 100,  # количество вакансий
            'area': '113',  # Регион. Необходимо передавать id из справочника /areas.
            'employer_id': company_id,  # id компании
        }

    def connecting_to_api(self):
        """Подключаемся к апи HH.ru"""
        return requests.get(self.__url, params=self.__params)

    def get_vacancies(self):
        """
        Метод получает список вакансий
        """
        return self.connecting_to_api().json()

    @classmethod
    def get_default_company_list(cls):
        company_id_list = []
        params = {'area': '113',
                  'sort_by': 'by_vacancies_open',
                  'per_page': 1}
        data = requests.get('https://api.hh.ru/employers', params=params).json()
        for i in data['items']:
            company_id_list.append(i['id'])
        return company_id_list

    @property
    def url(self):
        return self.__url

    @property
    def name(self):
        return self.__name

    @property
    def company_id(self):
        return self.__company_id

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @company_id.setter
    def company_id(self, new_id):
        self.__company_id = new_id


if __name__ == '__main__':
    a = HeadHunterAPI.get_default_company_list()
    hh = HeadHunterAPI('Python', a)
    print(hh.connecting_to_api())
    print(hh.get_vacancies())
