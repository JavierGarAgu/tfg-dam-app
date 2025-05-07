levantar docker

```bash
docker-compose up --force-recreate
```

tumbarlo

```bash
docker-compose down -v
```

meterse en su bd

```bash
docker exec -it django_postgres_db psql -U admin -d usuarios_db
```

ver tablas

```bash
\d usuarios
```

EN LA SHELL DE MANAGE.PY

```bash
python manage.py shell
```

Comprobar hashes de contraseña

```python
# Definir las variables comunes
usuario_nombre = "juan"
password_texto_plano = "clave123"

# Paso 1: Obtener el usuario por su nombre
usuario = Usuario.objects.get(usuario=usuario_nombre)
print(f"Usuario: {usuario}")

# Paso 2: Obtener y guardar la contraseña de "juan"
print(f"Contraseña almacenada: {usuario.password}")

# Paso 3: Comparar el hash almacenado con el hash de la contraseña proporcionada
from django.contrib.auth.hashers import check_password
es_valido = check_password(password_texto_plano, usuario.password)
print(f"La contraseña es válida: {es_valido}")

# Paso 4: Mostrar el hash de la contraseña proporcionada
from django.contrib.auth.hashers import make_password
hash_de_contraseña = make_password(password_texto_plano)
print(f"Hash de la contraseña proporcionada: {hash_de_contraseña}")
```

salir con `exit()`

