
# Backend - Eletro Rápida ⚡

Este é o backend do sistema Eletro Rápida, desenvolvido com Django e Django REST Framework. Ele fornece toda a lógica de autenticação, gerenciamento de usuários, componentes eletrônicos, registros de log e geração de estatísticas para o dashboard.

---

## 1. 🛠️ Preparação do Ambiente

### a. Dependências Necessárias

- Python 3.12+
- pip
- PostgreSQL
- Virtualenv (opcional, mas recomendado)
- Git

### b. Orientações para preparar o sistema operacional

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv postgresql libpq-dev git -y
```

#### Windows
- Instalar Python pelo site oficial: https://www.python.org/downloads/
- Instalar PostgreSQL: https://www.postgresql.org/download/
- Instalar Git: https://git-scm.com/download/win

> 💡 Recomenda-se o uso do Windows Terminal, PowerShell ou Git Bash.

---

## 2. 🐳 Execução com Docker Compose

### a. Pré-requisitos

- Docker: https://www.docker.com/products/docker-desktop
- Docker Compose incluído no Docker Desktop

### b. Comandos

#### Subir o ambiente:
```bash
docker-compose up --build
```

#### Parar o ambiente:
```bash
docker-compose down
```

### c. Estrutura do `docker-compose.yml`
```yaml
version: '3.9'

services:
  backend:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DEBUG=True
      - DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 backend
    networks:
      - eletrorapida_net

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: "Nome do Banco"
      POSTGRES_USER: "Usuário"
      POSTGRES_PASSWORD: "Senha"
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    networks:
      - eletrorapida_net

volumes:
  postgres_data:

networks:
  eletrorapida_net:
    driver: bridge
```

---

## 3. 🔧 Execução Manual (Sem Docker)

### a. Passo a passo

```bash
# Clone o repositório
git clone https://github.com/seu_usuario/eletro-rapida-backend.git
cd eletro-rapida-backend

# Crie um ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure o banco de dados (PostgreSQL)
# Crie o banco com os dados definidos em settings.py (v4, postgres, postgres)

# Rode as migrações
python manage.py migrate

# Crie um superusuário (opcional)
python manage.py createsuperuser

# Rode o servidor
python manage.py runserver
```

---

## 4. 🔐 Endpoints e Autenticação

- Documentação Swagger disponível em: `http://localhost:8000/swagger/`
- Autenticação via JWT com o endpoint: `POST /auth/login/`

---

## 5. 📁 Estrutura dos Apps

- `authentication`: controle de login/logout com JWT
- `users`: gestão de usuários
- `components`: CRUD de componentes eletrônicos
- `dashboard`: estatísticas de uso e alertas
- `logs`: registro de atividades

---

## 6. 🧠 Observações

- O backend está preparado para rodar em containers e expor sua API ao frontend via hostname `backend` no ambiente Docker.
- Para execução local, use `localhost` ou `127.0.0.1` nas URLs da API.
