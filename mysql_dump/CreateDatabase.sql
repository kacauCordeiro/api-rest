USE mybd;

 CREATE TABLE IF NOT EXISTS TIME (
                    ID_TIME_TM INT(8) NOT NULL AUTO_INCREMENT,
                    DS_TIME_TM VARCHAR(100) NOT NULL UNIQUE,
                    DS_LOCALIDADE_TM VARCHAR(100) NOT NULL,
                    CLASSIFICACAO_TIME_TM VARCHAR(12) NOT NULL,
                    DT_CADASTRO datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
                PRIMARY KEY(ID_TIME_TM)
                );

            
 CREATE TABLE IF NOT EXISTS JOGADOR (
                    ID_JOGADOR_JG INT(8) NOT NULL AUTO_INCREMENT,
                    NM_JOGADOR_JG VARCHAR(100) NOT NULL,
                    DT_NASCIMENTO_JG datetime NOT NULL,
                    PS_JOGADOR_JG VARCHAR(12),
                    ID_TIME_JG INT(8) NOT NULL,
                PRIMARY KEY (ID_JOGADOR_JG),
                FOREIGN KEY (ID_TIME_JG) REFERENCES TIME(ID_TIME_TM),
                UNIQUE KEY IX_2 (NM_JOGADOR_JG, ID_TIME_JG)
                );


 CREATE TABLE IF NOT EXISTS TRANSFERENCIA (
                    ID_TRANSFER_TFR INT(8) NOT NULL AUTO_INCREMENT,
                    ID_JOGADOR_TFR INT(8) NOT NULL,
                    ID_TIME_ORIGEM_TFR  INT(8) NOT NULL,
                    ID_TIME_DESTINO_TFR INT(8) NOT NULL,
                    VL_TRANSFER_TFR VARCHAR(15) NOT NULL,
                    DT_TRANSFER_TFR datetime,
                PRIMARY KEY (ID_TRANSFER_TFR),
                FOREIGN KEY (ID_TIME_ORIGEM_TFR) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_TIME_DESTINO_TFR) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_JOGADOR_TFR) REFERENCES JOGADOR(ID_JOGADOR_JG)
                );

 CREATE TABLE IF NOT EXISTS TORNEIO (
                    ID_TORNEIO_TO INT(8) NOT NULL AUTO_INCREMENT,
                    NM_TORNEIO_TO VARCHAR(100) NOT NULL UNIQUE,
                PRIMARY KEY (ID_TORNEIO_TO)
                );

CREATE TABLE IF NOT EXISTS PARTIDAS (
                    ID_PARTIDA_PT INT(8) NOT NULL AUTO_INCREMENT,
                    DS_PARTIDA_PT VARCHAR(255) NOT NULL,
                    ESTADIO_PT VARCHAR(255) NOT NULL,
                    ID_TIME_PT INT(8) NOT NULL,
                    ID_TIME_RIVAL_PT INT(8) NOT NULL,
                    ID_TORNEIO_PT INT(8) NOT NULL,
                PRIMARY KEY (ID_PARTIDA_PT),
                FOREIGN KEY (ID_TIME_PT) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_TIME_RIVAL_PT) REFERENCES TIME(ID_TIME_TM),
                FOREIGN KEY (ID_TORNEIO_PT) REFERENCES TORNEIO(ID_TORNEIO_TO)
                );

CREATE TABLE IF NOT EXISTS EVENTOS (
                    ID_EVENTO_EV INT(8) NOT NULL AUTO_INCREMENT,
                    ID_PARTIDA_EV INT(8) NOT NULL,
                    ID_TIME_EV INT(8),
                    ID_JOGADOR_EV  INT(8),
                    TP_EVENTO_EV VARCHAR(50) NOT NULL,
                    JSON_EVENTO_EV JSON,
                    DS_EVENTO_EV VARCHAR(200),
                    DT_EVENTO_EV datetime,
                    QT_GOL_TIME_EV  INT(8),
                    QT_GOL_RIVAL_EV  INT(8),
                PRIMARY KEY (ID_EVENTO_EV),
                FOREIGN KEY (ID_PARTIDA_EV) REFERENCES PARTIDAS(ID_PARTIDA_PT),
                FOREIGN KEY (ID_JOGADOR_EV) REFERENCES JOGADOR(ID_JOGADOR_JG),
                FOREIGN KEY (ID_TIME_EV) REFERENCES TIME(ID_TIME_TM)
                );

INSERT IGNORE INTO TIME (DS_TIME_TM,DS_LOCALIDADE_TM, CLASSIFICACAO_TIME_TM) VALUES ('Athletico', 'Curitiba', 'A'),('Azuriz', 'Pato Branco', 'B'),
('Cianorte', 'Cianorte', 'B'),('Coritiba', 'Curitiba', 'A'),('FC Cascavel', 'Cascavel', 'B'),('Londrina', 'Londrina', 'B'),('Maringá', 'Maringá', 'B'),
('Operário Ferroviário', 'Ponta Grossa', 'B'),('Paraná', 'Curitiba', 'B'),('Rio Branco', 'Paranaguá', 'B'),('São-Joseense', 'São José dos Pinhais', 'B'),
('União', 'Francisco Beltrão', 'B');


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Bento', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Khellven', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Pedro Henrique', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Nico Hernández', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Abner', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Hugo Moura', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Christian', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('David Terans', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Cuello', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Pablo', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Canobbio', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' )),
('Vitor Roque', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Athletico' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Caio', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Adilson', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Léo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Williams Bahia', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Igor Bosel', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Cayo Tenório', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Saulo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Salazar', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Jamerson Bahia', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Zé Pedro', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Jota', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' )),
('Mateus Raffler', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Azuriz' ));

INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Sílvio', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Bruno', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Gabriel Coutinho', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Carlos Itambé', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Vítor verícimo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Eduardo Doma', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Montoya', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Maurício', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Bruno Leite', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Patric Calmon', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Michel', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' )),
('Rael', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Cianorte' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Rafael Willian', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Matheus Alexandre', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Henrique', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Luciano Castán', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Egídio', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Willian Farias', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Galarza', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Thonny Anderson', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Neilton', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Alef Manga', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Léo Gamalho', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' )),
('Pikachu', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Coritiba' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Douglas', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('André Luiz', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Willian Gomes', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Diego Giaretta', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Jamerson', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Itallo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Fernando', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Libano', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Doka', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Carlinhos', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Wilian Simões', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' )),
('Eduardo', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'FC Cascavel' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Matheus Nogueira', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Rafael França', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Augusto', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Saimon', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Eltinho', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('João Paulo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Jhonny Lucas', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Mossoró', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Marcelinho', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Douglas Lima', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Caprini', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' )),
('Salatiel', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Londrina' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Zanetti', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Dheimison', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Vilar', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Áquila', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Brito', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Matheus Rocha', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Kadu', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Paulinho', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Ronald', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Raphinha', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Marcos Vinicius', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' )),
('Diogo Vitor', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Maringá' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('César Kurowski', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Lucas Fernandes', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Conrado Hilgemberg', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Lucas Moro', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Eduardo Risden', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Simão', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Thiago Braga', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Vanderlei', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Arnaldo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Lucas Mendes', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Fabiano', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' )),
('Alemão', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Paraná' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('João Paulo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Welison Ferreira', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Nayan', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Guilerme Dias', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Gabriel Neves', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Caubi', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Murilo Cavalcante', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Nathan Barbosa', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('William Monteiro', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Marcinho', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Rafael Henrique', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('João Celeri', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('João Paulo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Welison Ferreira', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Nayan', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Guilerme Dias', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Gabriel Neves', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Caubi', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Murilo Cavalcante', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Nathan Barbosa', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('William Monteiro', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Marcinho', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('Rafael Henrique', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' )),
('João Celeri', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'Rio Branco' ));


INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Lucas Macanhan', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Yago', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Valsir', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Léo Alaba', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Thiago Araújo', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Eduardo Biazus', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Guilherme Almeida', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Bruno Oliveira', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Julio Vaz', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Fernando Timbó', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Dirceu', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' )),
('Alex Jhonatta', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'São-Joseense' ));

INSERT IGNORE INTO JOGADOR (NM_JOGADOR_JG, DT_NASCIMENTO_JG, PS_JOGADOR_JG, ID_TIME_JG)
VALUES
('Elias', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Lucas Alves', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Neneca', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Alan', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Arthur Clemente de Souza', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Iury Cabral', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Odail', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Vinicius Matheus', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Wellington Reis', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Willian Barão', '1998-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Adriano', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' )),
('Alaor', '1994-10-28 00:00', '', (SELECT ID_TIME_TM FROM TIME WHERE DS_TIME_TM = 'União' ));


