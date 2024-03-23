from abc import ABC, abstractmethod

import json


class BaseWorkWithFile(ABC):
    @abstractmethod
    def save_to_json(self, file, data_):
        pass

    @abstractmethod
    def data_from_json(self, file):
        pass

    @abstractmethod
    def delete_data_from_json(self):
        pass


class WorkWithFile(BaseWorkWithFile):
    def __init__(self):
        self.data_ = None

    def save_to_json(self, file, data_):
        """Сохраняет данные в файл"""

        self.data_ = data_
        with open(file, "w", encoding="utf-8") as f:
            json.dump(self.data_, f, ensure_ascii=False)

    def data_from_json(self, file):
        """Получает данные из файла"""

        with open(file, "r", encoding="utf-8") as f:
            data_dict = json.load(f)
            return data_dict

    def delete_data_from_json(self):
        pass


if __name__ == '__main__':
    pass
