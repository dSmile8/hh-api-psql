from abc import ABC, abstractmethod

import json
from pathlib import Path
from api_connect import HeadHunterAPI

DATA_DIR_VACANCIES = Path(__file__).parent.parent.joinpath('data', 'hh.json')


class BaseWorkWithFile(ABC):
    @abstractmethod
    def save_to_json(self, data_):
        pass

    @abstractmethod
    def data_from_json(self):
        pass

    @abstractmethod
    def delete_data_from_json(self):
        pass


class WorkWithFile(BaseWorkWithFile):

    def __init__(self, file):
        self.file = file

    def save_to_json(self, data_):
        """Сохраняет данные в файл"""

        self.data_ = data_
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(self.data_, f, ensure_ascii=False)

    def data_from_json(self):
        """Получает данные из файла"""

        with open(self.file, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
            return data_dict

    def delete_data_from_json(self):
        pass


if __name__ == '__main__':
    hh = HeadHunterAPI('Python', [4305039])
    WorkWithFile(DATA_DIR_VACANCIES).save_to_json(hh.get_vacancies())
    # print(WorkWithFile(DATA_DIR_VACANCIES).data_from_json())

    data = WorkWithFile(DATA_DIR_VACANCIES).data_from_json()
    for d in data['items']:
        print(f"{d['employer']['name']}\n{d['employer']['id']}\n{d['employer']['alternate_url']}\n")

