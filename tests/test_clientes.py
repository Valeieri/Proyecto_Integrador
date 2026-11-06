import tempfile
import unittest
from pathlib import Path

from clientes.clientes import (
    eliminar_cliente,
    modificar_cliente,
    registrar_cliente,
)
from clientes.consultas import buscar_clientes, listar_clientes
from datos.database import inicializar_base_datos
from servicios.historial import consultar_historial_cliente
from servicios.servicios import registrar_servicio


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database_path = Path(self.temp_dir.name) / "automotriz.db"
        inicializar_base_datos(self.database_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_registers_client_and_trims_outer_spaces(self):
        client_id = registrar_cliente(
            "  Ana Garcia  ",
            " ana@example.com ",
            " 0000551234 ",
            self.database_path,
        )

        clients = buscar_clientes("Ana", self.database_path)
        self.assertEqual(client_id, clients[0]["id"])
        self.assertEqual("Ana Garcia", clients[0]["nombre"])
        self.assertEqual("ana@example.com", clients[0]["correo"])
        self.assertEqual("0000551234", clients[0]["telefono"])

    def test_accepts_common_email_with_plus_alias_and_subdomain(self):
        registrar_cliente(
            "Ana Garcia",
            " ana.garcia+auto@mail.example.co.uk ",
            "0000551234",
            self.database_path,
        )

        clients = buscar_clientes("Ana Garcia", self.database_path)
        self.assertEqual(
            "ana.garcia+auto@mail.example.co.uk",
            clients[0]["correo"],
        )

    def test_rejects_invalid_email_formats_when_registering(self):
        for email in (
            "sin-arroba",
            "ana@",
            "@example.com",
            "ana..garcia@example.com",
            "ana@localhost",
            "ana @example.com",
        ):
            with self.subTest(email=email):
                with self.assertRaisesRegex(ValueError, "formato válido"):
                    registrar_cliente(
                        "Ana Garcia",
                        email,
                        "0000551234",
                        self.database_path,
                    )

    def test_searches_by_partial_name_or_phone(self):
        registrar_cliente("Ana Garcia", "ana@example.com", "0000551234", self.database_path)

        clients_by_name = buscar_clientes("ana", self.database_path)
        clients_by_phone = buscar_clientes("1234", self.database_path)

        self.assertEqual(1, len(clients_by_name))
        self.assertEqual(1, len(clients_by_phone))
        self.assertEqual("Ana Garcia", clients_by_phone[0]["nombre"])

    def test_accepts_ten_digit_phone_and_preserves_leading_zero(self):
        registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0123456789",
            self.database_path,
        )

        clients = buscar_clientes("Ana Garcia", self.database_path)

        self.assertEqual("0123456789", clients[0]["telefono"])

    def test_rejects_phone_longer_than_ten_digits(self):
        with self.assertRaisesRegex(ValueError, "exactamente 10 dígitos"):
            registrar_cliente(
                "Ana Garcia",
                "ana@example.com",
                "12345678901",
                self.database_path,
            )

    def test_rejects_phone_shorter_than_ten_digits(self):
        with self.assertRaisesRegex(ValueError, "exactamente 10 dígitos"):
            registrar_cliente(
                "Ana Garcia",
                "ana@example.com",
                "123456789",
                self.database_path,
            )

    def test_rejects_non_digit_phone(self):
        with self.assertRaisesRegex(ValueError, "solo dígitos"):
            registrar_cliente(
                "Ana Garcia",
                "ana@example.com",
                "1234-5678",
                self.database_path,
            )

    def test_lists_clients_for_selection(self):
        registrar_cliente("Ana Garcia", "ana@example.com", "0000551234", self.database_path)
        registrar_cliente("Bea Diaz", "bea@example.com", "0000887766", self.database_path)

        clients = listar_clientes(self.database_path)

        self.assertEqual(["Ana Garcia", "Bea Diaz"], [client["nombre"] for client in clients])

    def test_rejects_empty_registration_data_and_search_term(self):
        with self.assertRaises(ValueError):
            registrar_cliente("", "ana@example.com", "1234", self.database_path)

        with self.assertRaises(ValueError):
            buscar_clientes("   ", self.database_path)

    def test_rejects_non_text_client_data(self):
        with self.assertRaises(TypeError):
            registrar_cliente(None, "ana@example.com", "1234", self.database_path)

    def test_modifies_existing_client(self):
        client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0000551234",
            self.database_path,
        )

        modificar_cliente(
            client_id,
            "Ana Lopez",
            "ana.lopez@example.com",
            "0000987654",
            self.database_path,
        )

        clients = buscar_clientes("Ana Lopez", self.database_path)
        self.assertEqual(1, len(clients))
        self.assertEqual("ana.lopez@example.com", clients[0]["correo"])
        self.assertEqual("0000987654", clients[0]["telefono"])

    def test_rejects_overlong_phone_when_modifying_client(self):
        client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0012345678",
            self.database_path,
        )

        with self.assertRaisesRegex(ValueError, "exactamente 10 dígitos"):
            modificar_cliente(
                client_id,
                "Ana Garcia",
                "ana@example.com",
                "12345678901",
                self.database_path,
            )

    def test_rejects_invalid_email_when_modifying_client(self):
        client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0000551234",
            self.database_path,
        )

        with self.assertRaisesRegex(ValueError, "formato válido"):
            modificar_cliente(
                client_id,
                "Ana Garcia",
                "correo-invalido",
                "0000551234",
                self.database_path,
            )

        clients = listar_clientes(self.database_path)
        self.assertEqual("ana@example.com", clients[0]["correo"])

    def test_modifying_unknown_client_raises_lookup_error(self):
        with self.assertRaises(LookupError):
            modificar_cliente(
                999,
                "Ana Lopez",
                "ana.lopez@example.com",
                "0000987654",
                self.database_path,
            )

    def test_deletes_client_without_services(self):
        client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0000551234",
            self.database_path,
        )

        eliminar_cliente(client_id, self.database_path)

        self.assertEqual([], listar_clientes(self.database_path))

    def test_customer_ids_restart_at_one_after_all_customers_are_deleted(self):
        for indice in range(1, 4):
            registrar_cliente(
                f"Cliente {indice}",
                f"cliente{indice}@example.com",
                f"000000000{indice}",
                self.database_path,
            )

        for _ in range(3):
            cliente = listar_clientes(self.database_path)[0]
            eliminar_cliente(cliente["id"], self.database_path)

        new_client_id = registrar_cliente(
            "Nuevo cliente",
            "nuevo@example.com",
            "0000000004",
            self.database_path,
        )

        self.assertEqual(1, new_client_id)

    def test_compacts_customer_ids_and_preserves_service_links(self):
        first_client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0000000001",
            self.database_path,
        )
        second_client_id = registrar_cliente(
            "Bea Diaz",
            "bea@example.com",
            "0000000002",
            self.database_path,
        )
        service_id = registrar_servicio(
            second_client_id,
            "Auto",
            "Ruido al frenar",
            "Pastillas",
            75,
            "06/11/2026",
            self.database_path,
        )

        eliminar_cliente(first_client_id, self.database_path)

        clientes = listar_clientes(self.database_path)
        historial = consultar_historial_cliente(1, self.database_path)
        self.assertEqual([1], [cliente["id"] for cliente in clientes])
        self.assertEqual("Bea Diaz", clientes[0]["nombre"])
        self.assertEqual(1, len(historial))
        self.assertEqual(service_id, historial[0]["id"])
        self.assertEqual("Ruido al frenar", historial[0]["descripcion"])

        next_client_id = registrar_cliente(
            "Carla Soto",
            "carla@example.com",
            "0000000003",
            self.database_path,
        )
        self.assertEqual(2, next_client_id)

    def test_does_not_delete_client_with_service_history(self):
        client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "0000551234",
            self.database_path,
        )
        registrar_servicio(
            client_id,
            "Auto",
            "Mantenimiento",
            "Aceite",
            "25",
            "06/11/2026",
            self.database_path,
        )

        with self.assertRaisesRegex(ValueError, "servicios asociados"):
            eliminar_cliente(client_id, self.database_path)

        self.assertEqual(1, len(listar_clientes(self.database_path)))

    def test_deleting_unknown_client_raises_lookup_error(self):
        with self.assertRaises(LookupError):
            eliminar_cliente(999, self.database_path)


if __name__ == "__main__":
    unittest.main()
