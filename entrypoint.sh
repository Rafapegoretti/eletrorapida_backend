#!/bin/sh

echo "Aplicando migrações..."
python manage.py migrate

echo "Coletando arquivos estáticos (se houver)..."
python manage.py collectstatic --noinput

echo "Criando superusuário padrão (se não existir)..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Senai@2025')
END

echo "Iniciando o servidor Django..."
python manage.py runserver 0.0.0.0:8000
