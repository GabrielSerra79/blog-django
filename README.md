# Blog

Projeto criado para Curso de Python do Luiz Otávio Miranda

<br>

# Referências
* [DOCS Djangoproject](https://docs.djangoproject.com/en/6.0/)
    - [Class Based Views](https://docs.djangoproject.com/en/6.0/ref/class-based-views/)

* [Python-dotenv](https://pypi.org/project/python-dotenv/)

* [Django-axes](https://django-axes.readthedocs.io/en/latest/2_installation.html)

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

## Acessar help dentro do container
```bash
docker compose run --rm djangoapp python manage.py --help
```

<br>

# Para deploy no server Postgress
Dentro do server entre no postgress
```bash
sudo -u postgres psql
```

Criar Usuario com as permições
```sql
create role blog_user with login superuser createdb createrole password 'senha_senha';
```

Criar Database
```sql
create database blog_data_base with owner blog_user;
```

Dar permições para o user na database
```sql
grant all privileges on database blog_data_base to blog_user;
```

Sair do postgres
```sql
/q
```

Reiniciar o Postgress
```bash
sudo systemctl restart postgresql
```

## Criar o arquivo .env
Copiar o arquivo de exemplo e edita-lo (na pasta blogapp)
```bash
cd dotenv_files
cp .env-example .env
nano .env
```

## Config do Django
Criar e ativar venv (em ~/blogapp)
```bash
python3 -m venv venv
. venv/bin/activate
```

Instalar dependencias
```bash
pip install -r djangoapp/requirements.txt
```

## Preparar o Django
em ~blogapp/djangoapp
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
```

criar usuário
```bash
python manage.py createsuperuser
```

Verrificar se tem algum erro ao rodar o server
```bash
python manage.py runserver
```
Parar o serviço

## Config do Gunicorn
Executar passo a passo
```bash
###############################################################################
# Replace
# blog the name of the gunicorn file you want
# __YOUR_USER__ your user name
# blogapp the folder name of your project
# project the folder name where you find a file called wsgi.py
#
###############################################################################
# Criando o arquivo blog.socket
sudo nano /etc/systemd/system/blog.socket

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=gunicorn blog socket

[Socket]
ListenStream=/run/blog.socket

[Install]
WantedBy=sockets.target

###############################################################################
# Criando o arquivo blog.service
sudo nano /etc/systemd/system/blog.service

###############################################################################
# Conteúdo do arquivo
[Unit]
Description=Gunicorn daemon (You can change if you want)
Requires=blog.socket
After=network.target

[Service]
User=__YOUR_USER__
Group=www-data
Restart=on-failure
WorkingDirectory=/home/__YOUR_USER__/cursos_udemy/blog_django/blogapp/djangoapp
ExecStart=/home/__YOUR_USER__/cursos_udemy/blog_django/blogapp/venv/bin/gunicorn \
          --error-logfile /home/__YOUR_USER__/cursos_udemy/blog_django/blogapp/gunicorn-error-log \
          --enable-stdio-inheritance \
          --log-level "debug" \
          --capture-output \
          --access-logfile - \
          --workers 6 \
          --bind unix:/run/blog.socket \
          project.wsgi:application

[Install]
WantedBy=multi-user.target

###############################################################################
# Ativando
sudo systemctl start blog.socket
sudo systemctl enable blog.socket

# Checando
sudo systemctl status blog.socket
curl --unix-socket /run/blog.socket localhost
sudo systemctl status blog

# Restarting
sudo systemctl restart blog.service
sudo systemctl restart blog.socket
sudo systemctl restart blog

# After changing something
sudo systemctl daemon-reload

# Debugging
sudo journalctl -u blog.service
sudo journalctl -u blog.socket
```

## Config NGINX
Executar os comandos a seguir
```bash
# https://www.nginx.com/blog/using-free-ssltls-certificates-from-lets-encrypt-with-nginx/
#
# REPLACES
# 192.168.15.21 = Replace with your domain
# /home/gabrielserra/cursos_udemy/blog_django/blogapp/djangoapp = Replace with the path to the folder for the project
# /home/gabrielserra/cursos_udemy/blog_django/blogapp/data/web/static = Replace with the path to the folder for static files
# /home/gabrielserra/cursos_udemy/blog_django/blogapp/data/web/media = Replace with the path to the folder for media files
# blog = Replace with your unix socket name (don't add .socket)


# Set timezone
# List - timedatectl list-timezones
# sudo timedatectl set-timezone America/Sao_Paulo#


cd /etc/nginx/sites-available/
sudo nano blogip

## Conteudo do arquivo
# HTTP
server {
  listen 80;
  listen [::]:80;
  server_name 192.168.15.21;

  # Add index.php to the list if you are using PHP
  index index.html index.htm index.nginx-debian.html index.php;

  # ATTENTION: /home/gabrielserra/cursos_udemy/blog_django/blogapp/data/web/static
  location /static {
    autoindex on;
    alias /home/gabrielserra/cursos_udemy/blog_django/blogapp/data/web/static;
  }

  # ATTENTION: /home/gabrielserra/cursos_udemy/blog_django/blogapp/data/web/media
  location /media {
    autoindex on;
    alias /home/gabrielserra/cursos_udemy/blog_django/blogapp/data/web/media;
  }

  # ATTENTION: blog
  location / {
    proxy_pass http://unix:/run/blog.socket;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_cache_bypass $http_upgrade;
  }

  # deny access to .htaccess files, if Apache's document root
  # concurs with nginx's one
  #
  location ~ /\.ht {
    deny all;
  }

  location ~ /\. {
    access_log off;
    log_not_found off;
    deny all;
  }

  gzip on;
  gzip_disable "msie6";

  gzip_comp_level 6;
  gzip_min_length 1100;
  gzip_buffers 4 32k;
  gzip_proxied any;
  gzip_types
    text/plain
    text/css
    text/js
    text/xml
    text/javascript
    application/javascript
    application/x-javascript
    application/json
    application/xml
    application/rss+xml
    image/svg+xml;

  access_log off;
  #access_log  /var/log/nginx/192.168.15.21-access.log;
  error_log   /var/log/nginx/192.168.15.21-error.log;
}
## FIM DO CONTEUDO DO ARQUIVO

# Lincar os arquivos
cd ../sites-enabled
sudo ln -s /etc/nginx/sites-available/blogip /etc/nginx/sites-enabled/blogip

# reiniciar NGINX
sudo systemctl restart nginx
```
