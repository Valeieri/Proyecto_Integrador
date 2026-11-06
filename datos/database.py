"""Conexión y preparación de la base de datos SQLite."""

from pathlib import Path
import sqlite3


DATABASE_PATH = Path(__file__).resolve().parent / "automotriz.db"


def conectar_db(ruta_db: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Abrir la base de datos y habilitar la validación de claves foráneas."""
    ruta_db.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(ruta_db)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_base_datos(ruta_db: Path = DATABASE_PATH) -> None:
    """Crear las tablas si todavía no existen."""
    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL,
                    telefono TEXT NOT NULL
                )
                """
            )
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS servicios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    vehiculo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    producto TEXT NOT NULL,
                    marca TEXT NOT NULL,
                    valor REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
                """
            )
    finally:
        conexion.close()