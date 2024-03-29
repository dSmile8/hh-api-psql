from api_connect import HeadHunterAPI
from work_with_file import WorkWithFile
from utils import print_employers, create_company_list, sort_data
from db_creator import DBCreator
from db_manager import DBManager

from pathlib import Path
import psycopg2

DATA_DIR_VACANCIES = Path(__file__).parent.parent.joinpath('data', 'hh_vacancies.json')
DATA_DIR_VAC_COMP = Path(__file__).parent.parent.joinpath('data', 'hh_vac_company.json')
DATA_DIR_SORT = Path(__file__).parent.parent.joinpath('data', 'hh_vac_company_sorted.json')


def user_iteraction():
    file_worker = WorkWithFile()
    db_name = input(
        'Введите имя создаваемой БД, если хотите оставить имя БД по умолчанию(hh_ru), просто нажмите  Enter ')
    db_creat = DBCreator(db_name)
    print('Выберете действия:\n'
          '1) Выбрать id компаний из списка самостоятельно по интересующей Вас вакансии\n'
          '2) Выбрать интересующие вас вакансии из списка компаний по умолчанию? (100 вакансий)\n'
          '3) Выбрать все вакансии компаний по умолчанию (10 компаний)\n')
    while True:
        try:
            action1 = int(
                input('Для выбора варанта введите цифры:\n'
                      '1 - вариант #1\n'
                      '2 - вариант #2\n'
                      '3 - вариант #3\n'
                      ))
            if action1 == 1:
                vacancy_name = input('Введите интересующую вас вакансию, например: "водитель"\n').lower()
                hh_vacancies_ = HeadHunterAPI(vacancy_name)
                file_worker.save_to_json(DATA_DIR_VACANCIES, hh_vacancies_.get_vacancies())  # Получаем список вакансий
                # по запросу и сохраняем их в файл
                print_employers(
                    file_worker.data_from_json(DATA_DIR_VACANCIES))  # Вывод на экран названия компаний и их id
                company_list = create_company_list()  # Создаем список компаний
                print(company_list)
                hh_vacancies_company_ = HeadHunterAPI(vacancy_name, company_list)  # Делаем запрос к hh.ru со списком
                # интересующих компаний
                file_worker.save_to_json(DATA_DIR_VAC_COMP, hh_vacancies_company_.get_vacancies())  # Сохраняем
                # в файл
                break
            if action1 == 2:
                vacancy_name = input('Введите интересующую вас вакансию, например: "водитель"\n').lower()
                hh_vacancies_company_ = HeadHunterAPI(vacancy_name, HeadHunterAPI.get_default_company_list())
                file_worker.save_to_json(DATA_DIR_VAC_COMP, hh_vacancies_company_.get_vacancies())
                break
            if action1 == 3:
                vacancy_name = None
                hh_vacancies_company_ = HeadHunterAPI(vacancy_name, HeadHunterAPI.get_default_company_list())
                file_worker.save_to_json(DATA_DIR_VAC_COMP, hh_vacancies_company_.get_vacancies())
                break
        except ValueError:
            print("Внимательней, нужно ввести ЧИСЛО 1 либо 0")
            continue

    file_worker.save_to_json(DATA_DIR_SORT, sort_data(file_worker.data_from_json(DATA_DIR_VAC_COMP)))  # Сортируем
    # данные и сохраняем их в файл
    db_creat.create_database()  # Создаем БД
    db_creat.create_table('vacancies')  # Создаем таблицу
    db_creat.fill_the_table('vacancies', DATA_DIR_SORT)  # Заполняем таблицу

    dbm = DBManager(db_creat.db_name)
    try:
        with dbm.conn as conn:
            with conn.cursor() as cur:
                while True:
                    answer1 = input('Хотите получить список всех компаний и количество вакансий у каждой компании?'
                                    '(y/n)').lower()
                    if answer1 == 'y':
                        for i in dbm.get_companies_and_vacancies_count(cur):
                            print(i)
                        break
                    if answer1 == 'n':
                        break
                    else:
                        continue
                while True:
                    answer2 = input(
                        'Хотите получить список всех вакансий с указанием названия компании, названия вакансии'
                        'и зарплаты и ссылки на вакансию?'
                        '(y/n)').lower()
                    if answer2 == 'y':
                        for i in dbm.get_all_vacancies(cur):
                            print(i)
                        break
                    if answer2 == 'n':
                        break
                    else:
                        continue

                while True:
                    answer3 = input('Хотите получить среднюю зарплату по вакансиям? (y/n)').lower()
                    if answer3 == 'y':
                        print(f'\n Средняя зарплата по всем вакансиям: {dbm.get_avg_salary(cur)}')
                        break
                    if answer3 == 'n':
                        break
                    else:
                        continue
                while True:
                    answer4 = input('Хотите получить список всех вакансий, у которых зарплата '
                                    'выше средней по всем вакансиям? (y/n)').lower()
                    if answer4 == 'y':
                        for i in dbm.get_vacancies_with_higher_salary(cur):
                            print(i)
                        break
                    if answer4 == 'n':
                        break
                    else:
                        continue
                while True:
                    answer5 = input('Хотите получить список всех вакансий, в названии которых содержатся переданные'
                                    ' в метод слова, например python? (y/n)').lower()
                    if answer5 == 'y':
                        vacancy_input = input('Введите нужное слово').lower()
                        for i in dbm.get_vacancies_with_keyword(cur, vacancy_input):
                            print(i)
                        break
                    if answer5 == 'n':
                        break
                    else:
                        continue
                cur.close()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    pass
