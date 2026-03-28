-- ==============================================================================
-- Criação das tabelas
-- Banco compatível: MySQL 8.0
-- Origem dos dados:
-- - 02_base_consolidada_2025.csv 
-- - 04_base_enriquecida_2025.csv 
-- - despesas_agregadas.csv 
-- Objetivo:
-- Criar a estrutura de tabelas para carga e análise dos dados de despesas da ANS
-- ==============================================================================

CREATE DATABASE IF NOT EXISTS ans_despesas
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
USE ans_despesas;

CREATE TABLE operadoras (
    id_operadora INT PRIMARY KEY AUTO_INCREMENT,
    reg_ans INT NOT NULL,
    cnpj CHAR(14),
    razao_social VARCHAR(255),
    modalidade VARCHAR(100),
    uf CHAR(2),
    
    UNIQUE (reg_ans),
    INDEX idx_operadoras_uf (uf)
);

CREATE TABLE despesas_consolidadas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    id_operadora INT NOT NULL,
    ano INT NOT NULL,
    trimestre VARCHAR(7) NOT NULL,
    valor_despesas DECIMAL(15,2) NOT NULL,
        
    INDEX idx_ano_trimestre (ano, trimestre),
    
    CONSTRAINT fk_despesas_operadora
    FOREIGN KEY (id_operadora)
    REFERENCES operadoras(id_operadora),
    
    UNIQUE (id_operadora, ano, trimestre) 
);

CREATE TABLE despesas_agregadas (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    id_operadora INT NOT NULL,
    total_despesas DECIMAL(15,2),
    media_trimestral DECIMAL(15,2),
    desvio_padrao DECIMAL(15,2),
    
    INDEX idx_agregadas_operadora (id_operadora),
    
    CONSTRAINT fk_agregadas_operadora
    FOREIGN KEY (id_operadora)
    REFERENCES operadoras(id_operadora)
);