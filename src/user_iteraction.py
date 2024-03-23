from api_connect import HeadHunterAPI
from work_with_file import WorkWithFile
from utils import print_employers
from pathlib import Path

DATA_DIR_VACANCIES = Path(__file__).parent.parent.joinpath('data', 'hh.json')

vacancy_name = input('Введите интересующую вас вакансию, например: "водитель"\n').lower()
hh_api = HeadHunterAPI(vacancy_name)
vacancies = WorkWithFile(DATA_DIR_VACANCIES).save_to_json(hh_api.get_vacancies())  # Получаем список вакансий по запросу
# и сохраняем их в файл
print_employers(DATA_DIR_VACANCIES)  # Вывод на экран названия компаний и их id



# print(hh_api.get_vacancies())
