-- Criando o database
CREATE DATABASE impacto_ia_redes_sociais;

-- Usando o database
USE impacto_ia_redes_sociais;

-- Criando tabela estudantes
CREATE TABLE estudantes (
id_estudante VARCHAR(10) PRIMARY KEY,
idade INT,
genero VARCHAR(20),
escolaridade VARCHAR(20)
);

-- Criando tabela habitos
CREATE TABLE habitos (
id_habito INT AUTO_INCREMENT PRIMARY KEY,
id_estudante VARCHAR(10),
horas_redes_sociais DECIMAL(5,2),
horas_ia DECIMAL(5,2),
horas_sono DECIMAL(5,2),
horas_atividade_fisica DECIMAL (5,2),
FOREIGN KEY (id_estudante) REFERENCES estudantes(id_estudante)
); 


-- Criando tabela saude
CREATE TABLE saude (
id_saude INT AUTO_INCREMENT PRIMARY KEY,
id_estudante VARCHAR(10),
pontuacao_mental DECIMAL(5,2),
pontuacao_fisica DECIMAL(5,2),
FOREIGN KEY (id_estudante) REFERENCES estudantes(id_estudante)
); 