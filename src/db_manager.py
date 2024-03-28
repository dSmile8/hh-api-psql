import psycopg2
from config import config
from db_creator import DBCreator


class DBManager:
    def __init__(self, name='hh_ru'):
        self.name = name
        self.params = config()
        self.conn = psycopg2.connect(**self.params, database=self.name)

    def get_companies_and_vacancies_count(self, cur) -> list:
        """Получает список всех компаний и количество вакансий у каждой компании"""
        list_ = []
        cur.execute('SELECT company_name, COUNT(*) '
                    'from vacancies '
                    'GROUP BY company_name')
        rows = cur.fetchall()
        print('\n Компания, Количество вакансий')
        for row in rows:
            list_.append(row)
        return list_

    def get_all_vacancies(self, cur) -> list:
        """Получает список всех вакансий с указанием названия компании, названия вакансии
        и зарплаты и ссылки на вакансию"""
        list_ = []
        cur.execute('SELECT company_name, vacancy_name, salary_from, salary_to, url FROM vacancies')
        rows = cur.fetchall()
        print('\n Компания, Вакансия, Зарплата_от, Зарплата_до, ссылка')
        for row in rows:
            list_.append(row)
        return list_

    def get_avg_salary(self, cur) -> int:
        """Получает среднюю зарплату по вакансиям"""
        cur.execute('SELECT (AVG(salary_from) + AVG(salary_to)) / 2 FROM vacancies')
        rows = cur.fetchall()
        avg_salary = int((rows[0][0]))
        return avg_salary

    def get_vacancies_with_higher_salary(self, cur) -> list:
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        list_ = []
        cur.execute('SELECT vacancy_name, url'
                    ' FROM vacancies WHERE (salary_from + salary_to) / 2 > '
                    '(SELECT (AVG(salary_from) + AVG(salary_to)) / 2 FROM vacancies)'
                    )
        rows = cur.fetchall()
        for row in rows:
            list_.append(row)
        return list_

    def get_vacancies_with_keyword(self, cur, words) -> list:
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python"""
        list_ = []
        cur.execute(f"SELECT vacancy_name, company_name, city, url FROM vacancies WHERE vacancy_name ILIKE '%{words}%'")
        rows = cur.fetchall()
        for row in rows:
            list_.append(row)
        return list_


if __name__ == '__main__':
    pass
