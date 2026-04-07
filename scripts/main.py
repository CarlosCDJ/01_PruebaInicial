import sqlite3
from datetime import datetime
from pathlib import Path

nombre_proyecto = "01_PruebaInicial"

carpeta_scripts = Path(__file__).resolve().parent
carpeta_proyecto = carpeta_scripts.parent

ruta_entrada = carpeta_proyecto / "entradas" / "entrada.txt"
ruta_salida = carpeta_proyecto / "Resultados" / "salida.txt"
ruta_bd = carpeta_proyecto / "data" / "historial.db"

with open(ruta_entrada, "r", encoding="utf-8") as f:
    contenido = f.read()

numero_caracteres = len(contenido)
numero_lineas = len(contenido.splitlines())
contenido_mayusculas = contenido.upper()

salida = ""
salida = salida + "=== INICIO DEL ARCHIVO ===\n"
salida = salida + "Generado por el script del proyecto " + nombre_proyecto + "\n"
salida = salida + "Número de líneas: " + str(numero_lineas) + "\n"
salida = salida + "Número de caracteres: " + str(numero_caracteres) + "\n"
salida = salida + "\n"
salida = salida + "--- CONTENIDO ORIGINAL ---\n"
salida = salida + contenido
salida = salida + "\n"
salida = salida + "--- CONTENIDO EN MAYÚSCULAS ---\n"
salida = salida + contenido_mayusculas

with open(ruta_salida, "w", encoding="utf-8") as f:
    f.write(salida)

conexion = sqlite3.connect(str(ruta_bd))
cursor = conexion.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ejecuciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora TEXT,
    archivo_entrada TEXT,
    numero_lineas INTEGER,
    numero_caracteres INTEGER
)
""")

columnas_a_comprobar = [
    ("proyecto", "TEXT"),
    ("archivo_salida", "TEXT"),
    ("estado", "TEXT"),
    ("comentario", "TEXT"),
]

cursor.execute("PRAGMA table_info(ejecuciones)")
columnas_existentes = cursor.fetchall()

nombres_columnas_existentes = []

for columna in columnas_existentes:
    nombres_columnas_existentes.append(columna[1])

for nombre_columna, tipo_columna in columnas_a_comprobar:
    if nombre_columna not in nombres_columnas_existentes:
        sql = "ALTER TABLE ejecuciones ADD COLUMN " + nombre_columna + " " + tipo_columna
        cursor.execute(sql)

fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
estado = "OK"
comentario = "Generación de salida y registro en SQLite"

cursor.execute("""
INSERT INTO ejecuciones (
    fecha_hora,
    archivo_entrada,
    numero_lineas,
    numero_caracteres,
    proyecto,
    archivo_salida,
    estado,
    comentario
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", (
    fecha_hora,
    str(ruta_entrada),
    numero_lineas,
    numero_caracteres,
    nombre_proyecto,
    str(ruta_salida),
    estado,
    comentario
))

conexion.commit()
conexion.close()

print("Archivo de salida generado")
print("Registro guardado en SQLite")