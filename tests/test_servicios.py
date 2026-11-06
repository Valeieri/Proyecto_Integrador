import sqlite3
import tempfile
import unittest
from pathlib import Path

from clientes.clientes import registrar_cliente
from datos.database import inicializar_base_datos
from servicios.historial import consultar_historial_cliente
from servicios.servicios import (
    eliminar_servicio,
    modificar_servicio,
    registrar_servicio,
)


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "automotriz.db"
        inicializar_base_datos(self.database_path)
        self.client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0000551234",
            self.database_path,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_records_service_and_returns_client_history_by_date(self):
        registrar_servicio(
            self.client_id,
            "Auto",
            "Mantenimiento",
            "Aceite",
            0,
            "05/11/2026",
            self.database_path,
        )
        registrar_servicio(
            self.client_id,
            "Auto",
            "Cambio de pieza",
            "Filtro",
            "125.50",
            "06/11/2026",
            self.database_path,
        )

        history = consultar_historial_cliente(self.client_id, self.database_path)

        self.assertEqual(2, len(history))
        self.assertEqual("2026-11-06", history[0]["fecha"])
        self.assertEqual(125.5, history[0]["valor"])
        self.assertEqual("2026-11-05", history[1]["fecha"])
        self.assertEqual(0.0, history[1]["valor"])

    def test_rejects_invalid_service_data(self):
        with self.assertRaises(ValueError):
            registrar_servicio(
                self.client_id,
                "   ",
                "Mantenimiento",
                "Aceite",
                10,
                "06/11/2026",
                self.database_path,
            )

        with self.assertRaises(ValueError):
            registrar_servicio(
                self.client_id,
                "Auto",
                "Mantenimiento",
                "Aceite",
                10,
                "31/02/2026",
                self.database_path,
            )

        for importe in (-1, "no es numero"):
            with self.subTest(importe=importe):
                with self.assertRaises(ValueError):
                    registrar_servicio(
                        self.client_id,
                        "Auto",
                        "Mantenimiento",
                        "Aceite",
                        importe,
                        "06/11/2026",
                        self.database_path,
                    )

    def test_rejects_service_for_unknown_client(self):
        with self.assertRaises(sqlite3.IntegrityError):
            registrar_servicio(
                999,
                "Auto",
                "Mantenimiento",
                "Aceite",
                10,
                "06/11/2026",
                self.database_path,
            )

    def test_modifies_service_without_changing_its_client(self):
        service_id = registrar_servicio(
            self.client_id,
            "Auto",
            "Mantenimiento",
            "Aceite",
            25,
            "05/11/2026",
            self.database_path,
        )

        modificar_servicio(
            service_id,
            "SUV",
            "Cambio de pieza",
            "Filtro",
            50,
            "06/11/2026",
            self.database_path,
        )

        history = consultar_historial_cliente(self.client_id, self.database_path)
        self.assertEqual(1, len(history))
        self.assertEqual(service_id, history[0]["id"])
        self.assertEqual("SUV", history[0]["vehiculo"])
        self.assertEqual("2026-11-06", history[0]["fecha"])
        self.assertEqual(50.0, history[0]["valor"])

    def test_deletes_service_and_reports_unknown_ids(self):
        service_id = registrar_servicio(
            self.client_id,
            "Auto",
            "Mantenimiento",
            "Aceite",
            25,
            "05/11/2026",
            self.database_path,
        )

        eliminar_servicio(service_id, self.database_path)

        history = consultar_historial_cliente(self.client_id, self.database_path)
        self.assertEqual([], history)
        with self.assertRaises(LookupError):
            eliminar_servicio(999, self.database_path)
        with self.assertRaises(LookupError):
            modificar_servicio(
                999,
                "Auto",
                "Mantenimiento",
                "Aceite",
                25,
                "05/11/2026",
                self.database_path,
            )

    def test_compacts_service_ids_after_deleting_an_earlier_service(self):
        service_ids = [
            registrar_servicio(
                self.client_id,
                "Auto",
                descripcion,
                "Aceite",
                valor,
                "06/11/2026",
                self.database_path,
            )
            for descripcion, valor in (
                ("Primer servicio", 10),
                ("Segundo servicio", 20),
                ("Tercer servicio", 30),
            )
        ]

        eliminar_servicio(service_ids[0], self.database_path)

        historial = consultar_historial_cliente(
            self.client_id,
            self.database_path,
        )
        servicios_por_id = {
            servicio["id"]: servicio["descripcion"]
            for servicio in historial
        }
        self.assertEqual(
            {1: "Segundo servicio", 2: "Tercer servicio"},
            servicios_por_id,
        )

        siguiente_id = registrar_servicio(
            self.client_id,
            "Auto",
            "Cuarto servicio",
            "Aceite",
            40,
            "07/11/2026",
            self.database_path,
        )
        self.assertEqual(3, siguiente_id)


if __name__ == "__main__":
    unittest.main()
