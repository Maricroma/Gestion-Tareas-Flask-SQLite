from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

DB_NAME = "tareas.db"

def inicializar_db():
    conexion = sqlite3.connect(DB_NAME)

    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()

@app.route("/registro", methods=["POST"])
def registro():

    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    contraseña_hash = generate_password_hash(contraseña)

    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hash)
        )

        conexion.commit()
        conexion.close()

        return jsonify({
            "mensaje": "Usuario registrado correctamente"
        }), 201

    except sqlite3.IntegrityError:

        return jsonify({
            "error": "El usuario ya existe"
        }), 409

@app.route("/login", methods=["POST"])
def login():

    datos = request.get_json()

    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")

    if not usuario or not contraseña:
        return jsonify({
            "error": "Usuario y contraseña son obligatorios"
        }), 400

    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    usuario_db = cursor.fetchone()

    conexion.close()

    if usuario_db is None:
        return jsonify({
            "error": "Credenciales incorrectas"
        }), 401

    contraseña_hash = usuario_db[2]

    if check_password_hash(contraseña_hash, contraseña):

        session["usuario"] = usuario

        return jsonify({
            "mensaje": "Inicio de sesión exitoso"
        }), 200

    return jsonify({
        "error": "Credenciales incorrectas"
    }), 401

@app.route("/tareas", methods=["GET"])
def tareas():

    if "usuario" not in session:
        return jsonify({
            "error": "Debe iniciar sesión para acceder a las tareas"
        }), 401

    usuario = session["usuario"]

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Gestión de Tareas</title>
    </head>

    <body>
        <h1>Bienvenido/a, {usuario}</h1>
        <p>Has iniciado sesión correctamente.</p>
        <p>Sistema de Gestión de Tareas</p>
    </body>
    </html>
    """

@app.route("/logout", methods=["POST"])
def logout():

    session.pop("usuario", None)

    return jsonify({
        "mensaje": "Sesión cerrada correctamente"
    }), 200

if __name__ == "__main__":
    inicializar_db()
    app.run(debug=True)