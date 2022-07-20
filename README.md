![Logo of the project](http://logo_link)

## api-rest
 
...Este projeto é uma api-rest (Nível de maturidade 2) que possui o objetivo de fornecer ao consumidor recursos para criar e manipular dados do tipo TIME (time de futebol), JOGADOR (que pertencerá sempre a um único time), TORNEIOS (eventos esportivos), PARTIDAS (partidas entre os times, referente a um torneio especifico), TRANSFERENCIAS (É possível trasferir jogadores de um time para outro), EVENTOS (Cada partida poderá gerar diversos eventos como: inicio, fim, prorrogação, gol, falta...). Para a mensageria dos eventos, utilizei o RabbitMQ, publicando em uma fila única todos os eventos. Os dados são persistidos em uma instância local de MySQL, e caso o usuário do recurso não possua IDE para acessar o banco de dados completo, é possível acessar utilizando o adminer, que sobe junto ao docker-compose como um recurso adicional.
 
 
## Technology
Docker
Liguandgem de programação predominante: Python3.9
Frameworks: FastApi e uvicorn 
Banco de dados: Mysql (image docker mysql:5.7)
Mensageria: RabbitMQ (image docker rabbitmq:3-management)

## Pré-requisitos
Para trabalharmos com o ambiente docker é necessário ter instalado e configurado na sua máquina:
- docker
- docker-compose
Para rodar a aplicação é necessário ter instalado Python3.9 ouy superior.
Os demais recursos serão instalados via docker automáticamente e estão dispostos no arquivo /requirements/requirements.txt

### Trabalhando com containers

Neste projeto, todos os containers são iniciados com o docker-compose. Siga os passos abaixo: 
- Crie um arquivo .env na raiz do projeto com o conteúdo abaixo:
APP_PORT=3000
MYSQL_USER=root
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=champions
MYSQL_PASSWORD=

RABBIT_HOST=
RABBIT_USER=
RABBIT_PASSWORD=
RABBIT_PORT=
RABBIT_QUEUE_RESPONSE=
RABBIT_VHOST=

- Execute: docker network create api-rest
- Execute: docker compose up

### Recomendado

Após clonar o projeto, crie um ambiente virtualenv no diretório do projeto.

```bash=
# Instale o virtualenv
pip3 install virtualenv

# Crie um virtualenv
python3.9 -m venv .venv

# Ative o virtualenv
source .venv/bin/activate

# Quando quiser sair e só usar
deactivate
```

## Links:
