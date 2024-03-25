import psycopg2
import json


class DBCreator:
    """Создает БД, таблицу и заполняет ее"""

    def __init__(self, db_name='hh_ru'):

        self.db_name = db_name
        self.conn = None
        self.params = {'host': 'localhost',
                       'port': '5432',
                       'database': self.db_name,
                       'user': 'postgres',
                       'password': 'asg6515ZX'}

    def create_database(self) -> None:
        """Создает базу данных"""
        self.conn = psycopg2.connect(host='localhost', port='5432', database='postgres',
                                     user='postgres', password='asg6515ZX')
        try:
            cursor = self.conn.cursor()
            self.conn.autocommit = True
            cursor.execute(f"CREATE DATABASE {self.db_name}")
            cursor.close()
            print(f"База данных {self.db_name} успешно создана!")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Ошибка при создании базы данных:", error)
        finally:
            self.conn.close()

    def create_table(self, table_name: str) -> None:
        """Создаёт таблицу в БД"""
        self.conn = psycopg2.connect(**self.params)
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    cur.execute(f'CREATE TABLE {table_name}'
                                '(vacancy_id int PRIMARY KEY,'
                                'vacancy_name varchar(100),'
                                'company_name varchar(150),'
                                'city varchar(100),'
                                'salary_from int,'
                                'salary_to int,'
                                'currency varchar(5),'
                                'schedule varchar(50),'
                                'experience varchar(50),'
                                'requirement text,'
                                'published timestamp,'
                                'url text'
                                ')')
                    cur.close()
                    print(f"Таблица {table_name} успешно создана!")

        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def fill_the_table(self, table_name: str, data_f) -> None:
        """Заполняет созданную таблицу в БД"""
        self.conn = psycopg2.connect(**self.params)
        try:
            with self.conn as conn:
                with conn.cursor() as cur:
                    with open(data_f, 'r', encoding='UTF-8') as file:
                        data = json.load(file)
                        for d in data:
                            cur.execute(
                                f'INSERT INTO "vacancies" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                (d['vacancy_id'], d['vacancy_name'], d['company_name'],
                                 d['city'], d['salary_from'], d['salary_to'], d['currency'], d['schedule'],
                                 d['experience'], d['requirement'], d['published'], d['url']))
                    cur.close()
                    print(f"Таблица {table_name} успешно заполнена!")
        except(Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                self.conn.close()

    def drop_db(self, cur):
        cur.execute('select pg_terminate_backend(pg_stat_activity.pid) '
                    'from pg_stat_activity '
                    f'where pg_stat_activity.datname = "{self.db_name}" '
                    'and pid <>pg_backend_pid();' 
                    f'DROP DATABASE {self.db_name}'
                    )


if __name__ == '__main__':
    pass
