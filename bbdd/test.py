import psycopg2
import traceback

print("Empiezo")

try:
    conn = psycopg2.connect(
        dbname="usuarios_db",
        user="admin",
        password="1234",
        host="localhost",
        port=5432
    )
    print("Conexion exitosa")
    conn.close()
except Exception as e:
    print("Error:", e)
    traceback.print_exc()

print("Fin del try")
