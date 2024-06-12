DROP SCHEMA IF EXISTS steam;

CREATE SCHEMA steam;

USE steam;

-- Tabela: desenvolvedora
CREATE TABLE desenvolvedora (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome VARCHAR(55) NOT NULL
);

-- Tabela: publicadora
CREATE TABLE publicadora (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    nome VARCHAR(55) NOT NULL
);

-- Tabela: Loja
CREATE TABLE Loja (
    app_id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    title VARCHAR(55) NOT NULL,
    release_date DATE NOT NULL,
    genres VARCHAR(255) NOT NULL,
    categories VARCHAR(255) NOT NULL,
    developer_id INT NOT NULL,
    publisher_id INT NOT NULL,
    original_price DECIMAL(4,2) NOT NULL,
    FOREIGN KEY (developer_id) REFERENCES desenvolvedora(id),
    FOREIGN KEY (publisher_id) REFERENCES publicadora(id)
);

-- Tabela: usuario
CREATE TABLE usuario (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    username VARCHAR(55) NOT NULL,
    email VARCHAR(55) NOT NULL,
    senha VARCHAR(55) NOT NULL,
    saldo DECIMAL(10,2),
    data_nasc DATE NOT NULL,
    data_criacao DATE NOT NULL
);

-- Tabela: biblioteca
CREATE TABLE biblioteca (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usuario_id INT NOT NULL,
    app_id INT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id),
    FOREIGN KEY (app_id) REFERENCES Loja(app_id)
);


-- Tabela: compra
CREATE TABLE compra (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    usuario_id INT NOT NULL,
    valor DECIMAL(10,2) NOT NULL,
    data_compra DATE NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id)
);

-- Tabela: itens_compra
CREATE TABLE itens_compra (
    id INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    app_id INT NOT NULL,
    compra_id INT NOT NULL,
    FOREIGN KEY (app_id) REFERENCES Loja(app_id),
    FOREIGN KEY (compra_id) REFERENCES compra(id)
);