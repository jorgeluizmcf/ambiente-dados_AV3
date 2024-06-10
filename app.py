import mysql.connector
from flask import Flask, make_response, jsonify, request

# Conexão com o banco de dados
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='steam',
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

@app.route('/biblioteca', methods=['GET'])
def get_biblioteca():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM biblioteca")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    biblioteca = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(biblioteca), 200)


@app.route('/compra', methods=['GET'])
def get_compra():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM compra")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    compra = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(compra), 200)


@app.route('/desenvolvedora', methods=['GET'])
def get_desenvolvedora():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM desenvolvedora")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    desenvolvedora = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(desenvolvedora), 200)


@app.route('/itens_compra', methods=['GET'])
def get_itens_compra():
    cursor = mydb.cursor(dictionary=True)
    cursor.execute("SELECT * FROM itens_compra")  # Ajuste esta consulta conforme a estrutura do seu banco de dados
    itens_compra = cursor.fetchall()
    cursor.close()
    return make_response(jsonify(itens_compra), 200)


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


# Rotas para realizar UPDATE no banco de dados

@app.route('/usuario_update/<int:id>', methods=['PUT'])
def update_usuario(id):
    data = request.get_json()
    nome = data.get('nome')
    email = data.get('email')
    idade = data.get('idade')

    cursor = mydb.cursor(dictionary=True)
    
    sql = "UPDATE usuario SET nome = %s, email = %s, idade = %s WHERE id = %s"
    values = (nome, email, idade, id)
    
    cursor.execute(sql, values)
    mydb.commit()
    
    cursor.close()
    
    if cursor.rowcount == 0:
        return make_response(jsonify({"message": "Usuário não encontrado!"}), 404)
    
    return make_response(jsonify({"message": "Usuário atualizado com sucesso!"}), 200)


# Rodar o aplicativo Flask
if __name__ == '__main__':
    app.run(debug=True)
