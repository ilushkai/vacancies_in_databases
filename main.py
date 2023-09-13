from src.utils import *
from src.DBCreater import *
from config.config import config
import psycopg2


def main():
    db_name = 'vacancies'
    params = config()

    vac = get_vacancies('python', 30)
    vac_data = parse_vacancies(vac)
    print('Сбор данных выполнен')

    create_database(params, db_name)
    print(f"БД {db_name} успешно создана")

    params.update({'dbname': db_name})
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                create_table(cur)
                print("Таблицы employers и vacancies успешно созданы")

                fill_data(cur, vac_data)
                print("Таблицы успешно заполнены")

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    user_interface(params)


if __name__ == '__main__':
    main()
