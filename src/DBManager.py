import psycopg2


class DBManager:
    def __init__(self, params):
        self.conn = psycopg2.connect(**params)
        self.conn.autocommit = True
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество
           вакансий у каждой компании."""

        self.cur.execute(
            """
            SELECT client, count(*)
            FROM vacancies
            GROUP BY client
            ORDER BY count(*) DESC
            """
        )
        result = self.cur.fetchall()
        for i in result:
            print(f'Компания: {i[0]} Количество: {i[1]}')

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
           названия вакансии и зарплаты и ссылки на вакансию."""

        self.cur.execute(
            """
            select employer_id, client, title, salary_from, salary_to, link from vacancies
            """
        )
        result = self.cur.fetchall()
        for i in result:
            print(f"{i[0]}, {i[1]}, {i[2]}, {self.format_salary(i)},"
                  f" Ссылка на вакансию: {i[5]}")

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        self.cur.execute(
            """
            SELECT AVG(salary_from) as от, AVG(salary_to) as до FROM vacancies;
            """
        )
        result = self.cur.fetchall()
        for i in result:
            print(f"Средняя зарплата от {int(i[0])} до {int(i[1])}")

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата
           выше средней по всем вакансиям."""

        self.cur.execute(
            """
            SELECT * FROM vacancies 
            WHERE salary_from > (SELECT AVG(salary_from+salary_to) FROM vacancies) 
            OR salary_to > (SELECT AVG(salary_from+salary_to) FROM vacancies)
            """
        )
        result = self.cur.fetchall()
        for i in result:
            print(f"{i[0]}, {i[1]}, {i[2]} {self.format_salary(i)},"
                  f"{i[6]}, {i[7]}, {i[8]}")

    def get_vacancies_with_keyword(self, search_query):
        """Получает список всех вакансий, в названии которых содержатся
           переданные в метод слова, например python."""

        self.cur.execute(
            f"SELECT * FROM vacancies WHERE title LIKE '%{search_query}%'"
        )
        result = self.cur.fetchall()
        for i in result:
            print(f"{i[0]}, {i[1]}, {i[2]} {self.format_salary(i)},"
                  f"{i[6]}, {i[7]}, {i[8]}")

    @staticmethod
    def format_salary(item):
        if item[3] is None:
            return f"Зарплата до {item[4]} руб."
        if item[4] is None:
            return f"Зарплата от {item[2]} руб."
        return f"Зарплата от {item[3]} до {item[4]} руб."

    def close(self):
        self.cur.close()
        self.conn.close()
