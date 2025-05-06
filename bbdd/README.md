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

