# Blog

Projeto criado para Curso de Python do Luiz Otávio Miranda

<br>

# Comandos para DEV

## - Criar ambiente virtual (venv)
Criar o ambiente venv
```bash
python3 -m venv venv
```

Ativar o ambiente virtual
```bash
. venv/bin/activate
```
Desativar ambiente virtual
```bash
deactivate
```
Para entrar na (venv) automaticamente ao acessar o diretório do projeto com o ```direnv``` instalado criar o arquivo ```.envrc``` na raiz do projeto com o comando
```bash
echo "source ./venv/bin/activate" > .envrc
```
Dar a permissão para o direnv
```bash
direnv allow
```

Atualizar o pip do venv
```bash
pip install pip --upgrade
```
<br>

## - Instalar a lista de dependências do projeto
```bash
pip install -r requirements.txt
```
### Caso seja necessário atualizar a lista de dependências
```bash
pip freeze > requirements.txt
```
<br>

## - Config Docker
em ```/dotenv_files/``` criar o arquivo ```.env``` com base no arquivo [.env-example](./dotenv_files/.env-example)
```python
# Criar secret_key:
# python -c "import string as s;from secrets import SystemRandom as SR;print(''.join(SR().choices(s.ascii_letters + s.digits + s.punctuation, k=64)));"
SECRET_KEY="CHANGE-ME"

# 0 False, 1 True
DEBUG="1"

# Comma Separated values
ALLOWED_HOSTS="127.0.0.1, localhost"

DB_ENGINE="django.db.backends.postgresql"
POSTGRES_DB="CHANGE-ME"
POSTGRES_USER="CHANGE-ME"
POSTGRES_PASSWORD="CHANGE-ME"
POSTGRES_HOST="psql"
POSTGRES_PORT="5432"
```

### Criar Docker (container / image)
```bash
docker compose up --build
```
Se for necessário recriar
```bash
docker compose up --build --force-recreate
```

### Subir o Docker (Postgres / Django)
```bash
docker compose up

docker compose up -d #Oculto - não exibe logs
```
### Descer o Docker
```bash
docker compose down
```

## Criar superuser no Django
```bash
docker compose run --rm djangoapp python manage.py createsuperuser
```
