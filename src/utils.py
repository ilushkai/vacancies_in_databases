import requests
from src.DBManager import DBManager


def get_vacancies(search_query, quantity):
    """Получение списка вакансий"""

    base_url = 'https://api.hh.ru/vacancies?employer_id='
    employer_id = ['4837179', '3359636', '10301008', '10073113', '2633363',
                   '3428160', '205152', '1910584', '2771696', '51900', '4138182', '3131901']
    all_vacancies = []
    for i in employer_id:
        url = f'{base_url}{i}'
        params = {
            'text': search_query,
            'per_page': quantity,
            "only_with_salary": True,
        }

        try:
            response = requests.get(url, params)
            data = response.json()
            if "items" not in data:
                print("Error: No vacancies found.")
                return []
            all_vacancies.extend(data['items'])
        except requests.exceptions.RequestException as e:
            print("Error: ", e)
            return []

    return all_vacancies


def parse_vacancies(vacancies):
    """Выборка нужных параметров"""
    parsed_vacancies = []
    for vacancy in vacancies:
        parsed_vacancy = {
            "employer_id": vacancy['employer']['id'],
            "title": vacancy['name'],
            "client": vacancy['employer']['name'],
            "salary_from": vacancy.get('salary', {}).get('from'),
            "salary_to": vacancy.get('salary', {}).get('to'),
            "currency": vacancy.get('salary', {}).get('currency'),
            "type_of_work": vacancy['employment']['name'],
            "experience": vacancy['experience']['name'],
            "link": vacancy['alternate_url'],
        }
        parsed_vacancies.append(parsed_vacancy)

    return parsed_vacancies


def user_interface(params):
    """Пользовательский интерфейс"""

    db = DBManager(params)

    input("""\nДобро пожаловать! Нажмите Enter для продолжения...""")
    while True:
        user_input = input("""
        1. Получить список всех компаний и количество вакансий у каждой компании
        2. Получить список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты и ссылки на вакансию
        3. Получить среднюю зарплату по вакансиям
        4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям
        5. Получить список всех вакансий по ключевым словам
        0. Выйти из программы
        
        Ввод пользователя:  """)

        if user_input == '0':
            db.close()
            return
        elif user_input == '1':
            db.get_companies_and_vacancies_count()
        elif user_input == '2':
            db.get_all_vacancies()
        elif user_input == '3':
            db.get_avg_salary()
        elif user_input == '4':
            db.get_vacancies_with_higher_salary()
        elif user_input == '5':
            search_query = input("Введите ключевые слова через пробел: ")
            db.get_vacancies_with_keyword(search_query)
