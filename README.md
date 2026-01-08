# Blog

Projeto criado para Curso de Python do Luiz Otávio Miranda

# Comandos para DEV

## Criar ambiente virtual (venv)
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

# Instalar a lista de dependências do projeto
```bash
pip install -r requirements.txt
```
## Caso seja necessário atualizar a lista de dependências
```bash
pip freeze > requirements.txt
```



