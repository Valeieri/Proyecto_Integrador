

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from clientes.clientes import registrar_cliente
from clientes.consultas import listar_clientes
from datos.database import conectar_db, inicializar_base_datos


class DatabaseInitializationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "automotriz.db"

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_creates_customer_and_service_tables(self):
        inicializar_base_datos(self.database_path)

        with closing(conectar_db(self.database_path)) as conexion:
            tablas = {
                fila[0]
                for fila in conexion.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            columnas_servicios = {
                fila[1]
                for fila in conexion.execute("PRAGMA table_info(servicios)")
            }

        self.assertIn("clientes", tablas)
        self.assertIn("servicios", tablas)
        self.assertNotIn("marca", columnas_servicios)

    def test_service_requires_an_existing_customer(self):
        inicializar_base_datos(self.database_path)

        with closing(conectar_db(self.database_path)) as conexion:
            with self.assertRaises(sqlite3.IntegrityError):
                conexion.execute(
                    """
                    INSERT INTO servicios (
                        cliente_id, vehiculo, descripcion, producto, valor, fecha
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (999, "Auto", "Mantenimiento", "Aceite", 25.0, "2026-11-06"),
                )

    def test_initialization_preserves_data_for_the_next_application_start(self):
        inicializar_base_datos(self.database_path)
        registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0000551234",
            self.database_path,
        )

        inicializar_base_datos(self.database_path)
        clientes = listar_clientes(self.database_path)

        self.assertEqual(1, len(clientes))
        self.assertEqual("Ana Garcia", clientes[0]["nombre"])

    def test_migrates_existing_services_and_preserves_data_without_brand(self):
        with closing(sqlite3.connect(self.database_path)) as conexion:
            conexion.executescript(
                """
                CREATE TABLE clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL,
                    telefono TEXT NOT NULL
                );
                CREATE TABLE servicios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    vehiculo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    producto TEXT NOT NULL,
                    marca TEXT NOT NULL,
                    valor REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                );
                INSERT INTO clientes VALUES (
                    1, 'Ana Garcia', 'ana@example.com', '0000551234'
                );
                INSERT INTO servicios VALUES (
                    7, 1, 'Auto', 'Ruido al frenar', 'Pastillas',
                    'Marca anterior', 75.0, '2026-11-06'
                );
                """
            )

        inicializar_base_datos(self.database_path)

        with closing(conectar_db(self.database_path)) as conexion:
            columnas = {
                fila[1]
                for fila in conexion.execute("PRAGMA table_info(servicios)")
            }
            servicio = conexion.execute(
                """
                SELECT id, cliente_id, vehiculo, descripcion, producto, valor, fecha
                FROM servicios
                """
            ).fetchone()
            errores_claves_foraneas = conexion.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()

        self.assertNotIn("marca", columnas)
        self.assertEqual(
            (7, 1, "Auto", "Ruido al frenar", "Pastillas", 75.0, "2026-11-06"),
            servicio,
        )
        self.assertEqual([], errores_claves_foraneas)


if __name__ == "__main__":
    unittest.main()
