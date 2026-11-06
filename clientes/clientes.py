
"""Operaciones para registrar y modificar clientes."""

import sqlite3
from pathlib import Path

from validaciones.validaciones import (
    validar_id_positivo,
    validar_telefono_celular,
    validar_texto_requerido,
)
from datos.database import DATABASE_PATH, conectar_db


def registrar_cliente(
    nombre: str,
    correo: str,
    telefono_celular: str,
    ruta_db: Path = DATABASE_PATH,
) -> int:
    """Guardar un cliente y devolver el identificador que asigno SQLite."""
    nombre = validar_texto_requerido(nombre, "El nombre")
    correo = validar_texto_requerido(correo, "El correo")
    telefono_celular = validar_telefono_celular(telefono_celular)

    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            cursor = conexion.execute(
                """
                INSERT INTO clientes (nombre, correo, telefono)
                VALUES (?, ?, ?)
                """,
                (nombre, correo, telefono_celular),
            )
            return cursor.lastrowid
    finally:
        conexion.close()


def modificar_cliente(
    cliente_id: int,
    nombre: str,
    correo: str,
    telefono: str,
    ruta_db: Path = DATABASE_PATH,
) -> None:
    """Actualizar un cliente existente o indicar que su ID no existe."""
    cliente_id = validar_id_positivo(cliente_id, "cliente")
    nombre = validar_texto_requerido(nombre, "El nombre")
    correo = validar_texto_requerido(correo, "El correo")
    telefono = validar_telefono_celular(telefono)

    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            cursor = conexion.execute(
                """
                UPDATE clientes
                SET nombre = ?, correo = ?, telefono = ?
                WHERE id = ?
                """,
                (nombre, correo, telefono, cliente_id),
            )
            if cursor.rowcount == 0:
                raise LookupError(f"No existe un cliente con ID {cliente_id}")
    finally:
        conexion.close()


def eliminar_cliente(
    cliente_id: int,
    ruta_db: Path = DATABASE_PATH,
) -> None:
    """Eliminar un cliente si no tiene servicios asociados."""
    cliente_id = validar_id_positivo(cliente_id, "cliente")
    conexion = conectar_db(ruta_db)
    try:
        conexion.execute("PRAGMA foreign_keys = OFF")
        with conexion:
            cliente = conexion.execute(
                "SELECT id FROM clientes WHERE id = ?",
                (cliente_id,),
            ).fetchone()
            if cliente is None:
                raise LookupError(f"No existe un cliente con ID {cliente_id}")

            cantidad_servicios = conexion.execute(
                "SELECT COUNT(*) FROM servicios WHERE cliente_id = ?",
                (cliente_id,),
            ).fetchone()[0]
            if cantidad_servicios:
                raise ValueError(
                    "No se puede eliminar el cliente porque tiene servicios "
                    "asociados. Elimina primero esos servicios si deseas "
                    "continuar."
                )

            conexion.execute(
                "DELETE FROM clientes WHERE id = ?",
                (cliente_id,),
            )
            ids_restantes = [
                fila[0]
                for fila in conexion.execute(
                    "SELECT id FROM clientes ORDER BY id"
                )
            ]
            for posicion, id_anterior in enumerate(ids_restantes, start=1):
                conexion.execute(
                    "UPDATE servicios SET cliente_id = ? WHERE cliente_id = ?",
                    (-posicion, id_anterior),
                )
                conexion.execute(
                    "UPDATE clientes SET id = ? WHERE id = ?",
                    (-posicion, id_anterior),
                )

            for id_nuevo in range(1, len(ids_restantes) + 1):
                conexion.execute(
                    "UPDATE clientes SET id = ? WHERE id = ?",
                    (id_nuevo, -id_nuevo),
                )
                conexion.execute(
                    "UPDATE servicios SET cliente_id = ? WHERE cliente_id = ?",
                    (id_nuevo, -id_nuevo),
                )

            conexion.execute(
                "DELETE FROM sqlite_sequence WHERE name = 'clientes'"
            )
            if ids_restantes:
                conexion.execute(
                    """
                    INSERT INTO sqlite_sequence (name, seq)
                    VALUES ('clientes', ?)
                    """,
                    (len(ids_restantes),),
                )

            errores_claves_foraneas = conexion.execute(
                "PRAGMA foreign_key_check"
            ).fetchall()
            if errores_claves_foraneas:
                raise sqlite3.IntegrityError(
                    "La compactación de IDs dejó referencias de servicios inválidas"
                )
    finally:
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.close()