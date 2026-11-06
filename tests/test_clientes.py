import tempfile
import unittest
from pathlib import Path

from clientes.clientes import modificar_cliente, registrar_cliente
from clientes.consultas import buscar_clientes, listar_clientes
from datos.database import inicializar_base_datos


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
            " 00551234 ",
            self.database_path,
        )

        clients = buscar_clientes("Ana", self.database_path)
        self.assertEqual(client_id, clients[0]["id"])
        self.assertEqual("Ana Garcia", clients[0]["nombre"])
        self.assertEqual("ana@example.com", clients[0]["correo"])
        self.assertEqual("00551234", clients[0]["telefono"])

    def test_searches_by_partial_name_or_phone(self):
        registrar_cliente("Ana Garcia", "ana@example.com", "00551234", self.database_path)

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
        with self.assertRaisesRegex(ValueError, "más de 10 dígitos"):
            registrar_cliente(
                "Ana Garcia",
                "ana@example.com",
                "12345678901",
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
        registrar_cliente("Ana Garcia", "ana@example.com", "00551234", self.database_path)
        registrar_cliente("Bea Diaz", "bea@example.com", "00887766", self.database_path)

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
            "00551234",
            self.database_path,
        )

        modificar_cliente(
            client_id,
            "Ana Lopez",
            "ana.lopez@example.com",
            "00987654",
            self.database_path,
        )

        clients = buscar_clientes("Ana Lopez", self.database_path)
        self.assertEqual(1, len(clients))
        self.assertEqual("ana.lopez@example.com", clients[0]["correo"])
        self.assertEqual("00987654", clients[0]["telefono"])

    def test_rejects_overlong_phone_when_modifying_client(self):
        client_id = registrar_cliente(
            "Ana Garcia",
            "ana@example.com",
            "12345678",
            self.database_path,
        )

        with self.assertRaisesRegex(ValueError, "más de 10 dígitos"):
            modificar_cliente(
                client_id,
                "Ana Garcia",
                "ana@example.com",
                "12345678901",
                self.database_path,
            )

    def test_modifying_unknown_client_raises_lookup_error(self):
        with self.assertRaises(LookupError):
            modificar_cliente(
                999,
                "Ana Lopez",
                "ana.lopez@example.com",
                "00987654",
                self.database_path,
            )


if __name__ == "__main__":
    unittest.main()
