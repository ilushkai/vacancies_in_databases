import psycopg2

companies = {
    4837179: "ИОТ",
    3359636: "Juzt Studio",
    10301008: "Инвайр",
    10073113: "Дунаев Михаил Алексеевич",
    2633363: "Финансово-правовой альянс",
    205152: "Mindbox",
    1910584: "Мир сайтов",
    2771696: "АйТи Мегастар",
    51900: "Siberian Wellness",
    3428160: "HardQode",
    4138182: "Topface Media",
    3131901: "РСХБ-Интех",

}


def create_database(params, db_name) -> None:
    """Создает новую базу данных."""
    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {db_name};")
    cur.execute(f"CREATE DATABASE {db_name};")

    cur.close()
    conn.close()


def create_table(cur):
    """Создает новую таблицу vacancies"""

    cur.execute("""
        DROP TABLE IF EXISTS employers;
        CREATE TABLE employers (
            employer_id VARCHAR(10) PRIMARY KEY,
            employer VARCHAR(50)
        )
    """)

    cur.execute("""
        DROP TABLE IF EXISTS vacancies;
        CREATE TABLE vacancies (
            employer_id VARCHAR(10) NOT NULL REFERENCES employers (employer_id),
            title varchar,
            client varchar,
            salary_from int,
            salary_to int,
            currency varchar,
            type_of_work varchar,
            experience varchar,
            link text
        )
    """)


def fill_data(cur, vac_data):
    """Заполняет таблицу данными"""
    for i, k in companies.items():
        cur.execute(
            """
            INSERT INTO employers (employer_id, employer)
            VALUES (%s, %s)
            """,
            (i, k)
        )

    for i in vac_data:
        cur.execute(
            """
            INSERT INTO vacancies (employer_id, title, client, salary_from, salary_to, currency, type_of_work, experience, link)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (i['employer_id'], i['title'], i['client'], i['salary_from'], i['salary_to'],
             i['currency'], i['type_of_work'], i['experience'], i['link'])
        )


def add_foreign_key(cur):
    """Добавляем foreign key в таблицу"""
    cur.execute("ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers "
                "FOREIGN KEY (employer_id) REFERENCES employers (employer_id);")
