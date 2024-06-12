import mysql.connector
from flask import Flask, make_response, jsonify, request
import os
import pandas as pd
import random 
from decimal import Decimal
import string
import datetime
import time

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', '180102'),
    database=os.getenv('MYSQL_DB', 'steam')
)

# Inicialização do aplicativo Flask
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Definição de uma rota de exemplo
@app.route('/')
def index():
    return make_response(jsonify({"message": "Bem-vindo à API Steam"}), 200)

# Rotas para realizar SELECTs dados do banco de dados
@app.route('/loja', methods=['GET'])
def get_loja():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Loja")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    loja = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(loja), 200)

@app.route('/desenvolvedora', methods=['GET'])
def get_desenvolvedora():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM desenvolvedora")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    desenvolvedora = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(desenvolvedora), 200)

@app.route('/publicadora', methods=['GET'])
def get_publicadora():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM publicadora")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    publicadora = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(publicadora), 200)

@app.route('/usuario', methods=['GET'])
def get_usuario():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    usuario = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(usuario), 200)

# Rota para atualizar um usuário específico
@app.route('/usuario_update/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    idade = data.get('idade')

    cursor = mydb.cursor(dictionary=True)

    sql = "UPDATE usuario SET username = %s, email = %s, idade = %s WHERE id = %s"
    values = (nome, email, idade, id)

    cursor.execute(sql, values)
    mydb.commit()

    cursor.close()

    if cursor.rowcount == 0:
        return make_response(jsonify({"message": "Usuário não encontrado!"}), 404)

    return make_response(jsonify({"message": "Usuário atualizado com sucesso!"}), 200)

# Funções para manipulação de dados no banco de dados
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
                
        cursor.execute(insert_query, (
            i+1,
            ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10)),
            f"{''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))}@example.com",
            ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            random.randint(0, 100),
            random_date_str,
            datetime.datetime.now().strftime("%Y-%m-%d")
            )
        )
    
    if use_transaction:
        conn.commit()
    
    end_time = time.time()
    duration = end_time - start_time
    return duration

def inserir_dados_loja(conn, use_transaction, data):
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
    
    for i, row in data.iterrows():
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
    insert_query = """
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
    insert_query = """
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

# Exemplos de utilização das funções

# Inserir dados na tabela de desenvolvedora e publicadora
# inserir_dados_dev(mydb, use_transaction=True, data=steam_loja)
# inserir_dados_pub(mydb, use_transaction=True, data=steam_loja)
# inserir_dados_loja(mydb, use_transaction=True, data=steam_loja)

# Consulta
query = "SELECT * FROM Loja"
results = realizar_consulta(mydb, query)
print(results)

# Update
update_query = "UPDATE Loja SET original_price = 0 WHERE original_price > 100"
rows_updated = realizar_update(mydb, update_query)
print(rows_updated)

# Delete
delete_query = "DELETE FROM Loja WHERE original_price = 0"
rows_deleted = realizar_delete(mydb, delete_query)
print(rows_deleted)

# Inserir dados do usuário e calcular o tempo de execução
time_1 = inserir_dados_usuario(mydb, use_transaction=True)
print(f"Tempo de execução da inserção de dados do usuário com transaction: {time_1:.2f} segundos")

# Deletar todos os registros da tabela de usuários
delete_query = "DELETE FROM usuario"
rows_deleted = realizar_delete(mydb, delete_query)
print(rows_deleted)

# Inserir dados do usuário sem transaction e calcular o tempo de execução
time_2 = inserir_dados_usuario(mydb, use_transaction=False)
print(f"Tempo de execução da inserção de dados do usuário sem transaction: {time_2:.2f} segundos")

# Fechar a conexão
mydb.close()

# Rodar o aplicativo Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
