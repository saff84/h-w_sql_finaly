import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS clients(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        last_name VARCHAR(50),
        email VARCHAR(50) UNIQUE);
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phones(
        id SERIAL PRIMARY KEY,
        client_id INT NOT NULL REFERENCES clients(id),
        phone VARCHAR(50));
        ''')
        conn.commit()
        print('Успешно созданы связи')
    pass


def add_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute('''
                INSERT INTO clients(first_name,last_name,email) VALUES(%s, %s, %s);
                ''', (first_name, last_name, email))
        conn.commit()
    client_id = select_client_id(email)
    print('Успешно добавлен')

    return client_id


def select_client_id(email):
    with conn.cursor() as cur:
        cur.execute('''
                SELECT id FROM clients
                WHERE email = %s;
                ''', (email,))
        return cur.fetchone()[0]


def add_phones(conn, client_id, phone):

    with conn.cursor() as cur:
        for i in phone:
            cur.execute('''
            INSERT INTO phones(
            client_id,
            phone)
            VALUES(
            %s, %s);
            ''', (client_id, i))
        conn.commit()
        print('Успешно добавлены')
    pass


def add_phone(conn, client_id, phone):

    with conn.cursor() as cur:

        cur.execute('''
        INSERT INTO phones(
        client_id,
        phone)
        VALUES(
        %s, %s);
        ''', (client_id, phone))
        conn.commit()
        print('Успешно добавлено')
    pass


def change_client(conn):
    id = int(input('Введите id клиента: '))
    a = int(input('Введите что будем менять имя - 1, фамилию - 2 или емайл - 3: '))
    b = input('Введите на что меняем: ')
    if a == 1:
        with conn.cursor() as cur:
            cur.execute('''
                    UPDATE clients
                    SET first_name = %s
                    WHERE id = %s;
                    ''', (b, id))
        conn.commit()
        print('Успешно изменено')

    elif a == 2:
        with conn.cursor() as cur:
            cur.execute('''
                    UPDATE clients
                    SET last_name = %s
                    WHERE id = %s;
                    ''', (b, id))
        conn.commit()
        print('Успешно изменено')

    elif a == 3:
        with conn.cursor() as cur:
            cur.execute('''
                    UPDATE clients
                    SET email = %s
                    WHERE id = %s;
                    ''', (b, id))
        conn.commit()
        print('Успешно изменено')

    pass


def delete_phone(conn):
    client_id = int(input('Введите id клиента чьи телефоны удаляем: '))
    with conn.cursor() as cur:
        cur.execute('''
        DELETE FROM phones
        WHERE client_id = %s; ''', (client_id,))
    conn.commit()

    print('Успешно удалено')
    pass


def delete_client(conn):
    client_id = int(input('Введите id клиента которого удаляем: '))
    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM phones
            WHERE client_id = %s; ''', (client_id,))

    with conn.cursor() as cur:
        cur.execute('''
            DELETE FROM clients
            WHERE id = %s; ''', (client_id,))

    conn.commit()
    print('Успешно удален')

    pass


def find_client(conn):
    a = int(input(
        'Введите то чем будем искать по имени - 1, фамилии - 2, емайлу - 3 или по телефону - 4: '))
    b = input('Введите данные для поиска: ')
    if a == 1:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT first_name, last_name FROM clients
                    WHERE first_name = %s;
                    ''', (b,))
            cur.fetchone()

    elif a == 2:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT first_name, last_name FROM clients
                    WHERE last_name = %s;
                    ''', (b,))
            cur.fetchone()

    elif a == 3:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT first_name, last_name FROM clients
                    WHERE email = %s;
                    ''', (b,))
            cur.fetchone()

    elif a == 4:
        with conn.cursor() as cur:
            cur.execute('''
                    SELECT first_name, last_name FROM clients c
                    JOIN phones p ON c.id = p.client_id
                    WHERE phone LIKE %s;
                    ''', (b,))
            print(cur.fetchone())

    pass


if __name__ == '__main__':

    to_do = int(input('''Давайте выберем что будем делать:
                            1 - Создадим структуру БД;
                            2 - Добавим нового клиента;
                            3 - Добавми телефон для существуещего клиента;
                            4 - Изменим данные клиента
                            5 - Удалим телефон у существуещего клиента;
                            6 - Удалим клиента;
                            7 - Найдем клиента;


                            Ваш выбор: '''))

    with psycopg2.connect(database="clients_db", user="postgres", password="310884") as conn:
        if to_do == 1:
            create_db(conn)

        elif to_do == 2:
            name = input('Введите Имя: ')
            surname = input('Введите Фамилию: ')
            email = input('Введите email: ')
            phone = []
            p = ''
            while True:
                p = input(
                    'Введите номер телефона, прекратить ввод телефонов - введите n: ')
                if p == 'n':
                    break
                else:
                    phone.append(p)

            client_id = add_client(conn, name, surname, email)
            print(client_id)
            add_phones(conn, client_id, phone)

        elif to_do == 3:
            client_id = int(input('Введите номер клиента: '))
            phone = input('Введите номер телефона: ')
            add_phone(conn, client_id, phone)

        elif to_do == 4:
            change_client(conn)

        elif to_do == 5:
            delete_phone(conn)

        elif to_do == 6:
            delete_client(conn)

        elif to_do == 7:
            find_client(conn)

    conn.close()
