

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

        self.assertIn("clientes", tablas)
        self.assertIn("servicios", tablas)

    def test_service_requires_an_existing_customer(self):
        inicializar_base_datos(self.database_path)

        with closing(conectar_db(self.database_path)) as conexion:
            with self.assertRaises(sqlite3.IntegrityError):
                conexion.execute(
                    """
                    INSERT INTO servicios (
                        cliente_id, vehiculo, descripcion, producto,
                        marca, valor, fecha
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (999, "Auto", "Mantenimiento", "Aceite", "Marca", 25.0, "2026-11-06"),
                )

    def test_initialization_preserves_data_for_the_next_application_start(self):
        inicializar_base_datos(self.database_path)
        registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "00551234",
            self.database_path,
        )

        inicializar_base_datos(self.database_path)
        clientes = listar_clientes(self.database_path)

        self.assertEqual(1, len(clientes))
        self.assertEqual("Ana Garcia", clientes[0]["nombre"])


if __name__ == "__main__":
    unittest.main()
