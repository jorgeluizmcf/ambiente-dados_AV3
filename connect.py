import mysql.connector
import time
import pandas as pd
import random 
from decimal import Decimal
import string
import datetime

def connect_mysql():
    conn = mysql.connector.connect(
        host="localhost",  
        port = 3306,
        user="root",
        password="180102",
        database="steam"
    )
    return conn

conn = connect_mysql()
steam_loja = pd.read_csv('dados do kaggle - Loja.csv')
steam_loja.dropna(inplace=True)


def realizar_consulta(conn, _query):
    cursor = conn.cursor()
    cursor.execute(_query)
    results = cursor.fetchall()
    return results

def realizar_update(conn,update_query):
    cursor = conn.cursor()
    cursor.execute(update_query)
    conn.commit()
    return cursor.rowcount

def realizar_delete(conn,delete_query):
    cursor = conn.cursor()
    cursor.execute(delete_query)
    conn.commit()
    return cursor.rowcount

def inserir_dados_usuario(conn, use_transaction):
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO usuario ( 
        `id`,
        `username`,
        `email`,
        `senha`,
        `saldo`,
        `data_nasc`,
        `data_criacao`)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    
    start_time = time.time()
    
    if use_transaction:
        conn.start_transaction()
    
    for i in range(10000):
        start_date = datetime.date(1970, 1, 1)
        end_date = datetime.date(2002, 12, 31)

        random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

        # Format the random date as string in the desired format
        random_date_str = random_date.strftime("%Y-%m-%d")

        random_date_str
                
        cursor.execute(insert_query, (
            i+1,
            #random name,
            ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10)),
            #random email,
            f"{''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))}@example.com",
            #random password,
            ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            #random saldo,
            random.randint(0, 100),
            # Generate random birth dates between 01/01/1970 and 31/12/2002
            random_date_str,
            #random data_criacao,
            datetime.datetime.now().strftime("%Y-%m-%d")
            )
        )
    
    if use_transaction:
        conn.commit()
    
    end_time = time.time()
    duration = end_time - start_time
    return duration


def inserir_dados_loja(conn, use_transaction,data):
    cursor = conn.cursor()
    insert_query = """
        INSERT INTO Loja
        (`app_id`,
        `title`,
        `release_date`,
        `genres`,
        `categories`,
        `developer_id`,
        `publisher_id`,
        `original_price`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    start_time = time.time()
    
    if use_transaction:
        conn.start_transaction()
    
    for i,row in data.iterrows():
        cursor.execute(insert_query, (
            int(row['app_id']), 
            row['title'], 
            row['release_date'],
            row['genres'], 
            row['categories'], 
            int(row['developer_id']), 
            int(row['publisher_id']), 
            Decimal(row['original_price'].replace(',', '.'))
        ))
    
    if use_transaction:
        conn.commit()
    
    end_time = time.time()
    duration = end_time - start_time
    return duration

def inserir_dados_pub(conn, use_transaction, data):
    cursor = conn.cursor()
    insert_query ="""
        INSERT INTO publicadora 
        (id, nome) 
        VALUES (%s, %s);
     """
    data = data['publisher_id'].unique()
    start_time = time.time()
    
    if use_transaction:
        conn.start_transaction()
    
    for row in data:
        cursor.execute(insert_query, (
            int(row), 
            random.choice(['Valve', 'Ubisoft', 'EA', 'Rockstar', 'Bethesda', 'Square Enix', 'CD Projekt', 'Konami', 'Capcom', 'Activision'])
        ))
    
    if use_transaction:
        conn.commit()
    
    end_time = time.time()
    duration = end_time - start_time
    return duration

def inserir_dados_dev(conn, use_transaction ,data):
    cursor = conn.cursor()
    insert_query ="""
        INSERT INTO desenvolvedora 
        (id, nome) 
        VALUES (%s, %s);
     """
    data = data['developer_id'].unique()
    start_time = time.time()
    
    if use_transaction:
        conn.start_transaction()
    
    for row in data:
        cursor.execute(insert_query, (
            int(row), 
            random.choice(['Valve', 'Ubisoft', 'EA', 'Rockstar', 'Bethesda', 'Square Enix', 'CD Projekt', 'Konami', 'Capcom', 'Activision'])
        ))
    
    if use_transaction:
        conn.commit()
    
    end_time = time.time()
    duration = end_time - start_time
    return duration
        

# inserir_dados_dev(conn, use_transaction=True,data=steam_loja)
# inserir_dados_pub(conn, use_transaction=True,data=steam_loja)
# inserir_dados_loja(conn, use_transaction=True, data = steam_loja)

# Consulta
query = "SELECT * FROM Loja"
results = realizar_consulta(conn, query)
print(results)

# Update
update_query = "UPDATE Loja SET original_price = 0 WHERE original_price > 100"
rows_updated = realizar_update(conn, update_query)
print(rows_updated)


# Delete
delete_query = "DELETE FROM Loja WHERE original_price = 0"
rows_deleted = realizar_delete(conn, delete_query)
print(rows_deleted)


time_1 = inserir_dados_usuario(conn, use_transaction=True)
print(f"Tempo de execução da inserção de dados do usuário com transaction: {time_1:.2f} segundos")

# Deletar todos os registros da tabela de usuarios
delete_query = "DELETE FROM usuario"
rows_deleted = realizar_delete(conn, delete_query)
print(rows_deleted)

    
time_2 = inserir_dados_usuario(conn, use_transaction=False)
print(f"Tempo de execução da inserção de dados do usuário sem transaction: {time_2:.2f} segundos")
# Fechar a conexão
conn.close()

