from api_connect import HeadHunterAPI
from work_with_file import WorkWithFile
from utils import print_employers, create_company_list, sort_data
from db_creator import DBCreator

from pathlib import Path

DATA_DIR_VACANCIES = Path(__file__).parent.parent.joinpath('data', 'hh_vacancies.json')
DATA_DIR_VAC_COMP = Path(__file__).parent.parent.joinpath('data', 'hh_vac_company.json')
DATA_DIR_SORT = Path(__file__).parent.parent.joinpath('data', 'hh_vac_company_sorted.json')

vacancy_name = input('Введите интересующую вас вакансию, например: "водитель"\n').lower()
hh_vacancies = HeadHunterAPI(vacancy_name)
file_worker = WorkWithFile()
db_creat = DBCreator()
file_worker.save_to_json(DATA_DIR_VACANCIES, hh_vacancies.get_vacancies())  # Получаем список вакансий
# по запросу и сохраняем их в файл

print_employers(file_worker.data_from_json(DATA_DIR_VACANCIES))  # Вывод на экран названия компаний и их id
company_list = create_company_list()  # Создаем список компаний
hh_vacancies_company = HeadHunterAPI(vacancy_name, company_list)  # Делаем запрос к hh.ru со списком
# интересующих компаний

file_worker.save_to_json(DATA_DIR_VAC_COMP, hh_vacancies_company.get_vacancies())  # Сохраняем
# в файл

file_worker.save_to_json(DATA_DIR_SORT, sort_data(file_worker.data_from_json(DATA_DIR_VAC_COMP)))  # Сортируем
# данные и сохраняем их в файл
db_creat.create_database()  # Создаем БД
db_creat.create_table('vacancies')  # Создаем таблицу
db_creat.fill_the_table('vacancies', DATA_DIR_SORT)  # Заполняем таблицу



