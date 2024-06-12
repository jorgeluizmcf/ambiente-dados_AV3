import mysql.connector
import time
import pandas as pd
import random 
from decimal import Decimal


# Função para conectar ao banco de dados MySQL
def connect_mysql():
    conn = mysql.connector.connect(
        host="localhost",  # ou o endereço do seu servidor MySQL
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

def inserir_dados(conn, use_transaction):
    cursor = conn.cursor()
    insert_query = "INSERT INTO tabela_exemplo (coluna1, coluna2) VALUES (%s, %s);"
    
    start_time = time.time()
    
    if use_transaction:
        conn.start_transaction()
    
    for i in range(10000):
        cursor.execute(insert_query, (f'valor{i}', f'valor{i}'))
    
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

inserir_dados_loja(conn, use_transaction=True, data = steam_loja)


# Fechar a conexão
conn.close()

