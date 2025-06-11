FROM python:3.13

# Crear carpeta
RUN mkdir /django

# Setear el directorio de trabajo
WORKDIR /django

# Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Actualizar pip
RUN pip install --upgrade pip

# Copiar y dar permisos
COPY ../django/requirements.txt .
COPY ../django/entrypoint.sh .
RUN chmod +x entrypoint.sh

# Instalar deps
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto
COPY ../django/app ./app
COPY ../django/manage.py .

# Exponer y lanzar
EXPOSE 8000
ENTRYPOINT ["./entrypoint.sh"]
