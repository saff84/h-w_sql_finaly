import psycopg2

class Client:
    def __init__(self, first_name, last_name, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = []


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
        id_client INIT NOT NULL REFERENCES client(id),
        phone VARCHAR(50));
        ''')
        conn.commit()
    pass

def add_client(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute('''
                INSERT INTO clients(
                first_name,last_name,email)
                VALUES(
                %s, %s, %s);
                ''',(first_name, last_name, email))
        client = conn.fetchone() # вопросик по возврату id после загрузки данных по клиенту
    client_id = client[0]
    return client_id

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        for i in phone:
            cur.execute('''
            INSERT INTO phones(
            client_id,
            phone)
            VALUES(
            %s, %s);
            ''', (client_id,i))
        conn.commit()
    pass

def change_client(conn, client_id, first_name=None, last_name=None, email=None, phones=None):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass


with psycopg2.connect(database="clients_db", user="postgres", password="postgres") as conn:


    pass  # вызывайте функции здесь

conn.close()