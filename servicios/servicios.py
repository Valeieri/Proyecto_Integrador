"""Operaciones para registrar servicios."""

import math
from datetime import datetime
from pathlib import Path
from typing import Union

from validaciones.validaciones import validar_id_positivo, validar_texto_requerido
from datos.database import DATABASE_PATH, conectar_db


def _normalizar_fecha(fecha: str) -> str:
    """Validar DD/MM/AAAA y devolver la fecha en formato ISO para SQLite."""
    fecha = validar_texto_requerido(fecha, "La fecha")
    try:
        fecha_convertida = datetime.strptime(fecha, "%d/%m/%Y").date()
    except ValueError as error:
        raise ValueError(
            "La fecha debe ser valida y tener el formato DD/MM/AAAA"
        ) from error

    if fecha_convertida.strftime("%d/%m/%Y") != fecha:
        raise ValueError("La fecha debe tener el formato DD/MM/AAAA")

    return fecha_convertida.isoformat()


def _validar_importe(valor: Union[int, float, str]) -> float:
    """Convertir el importe a numero y rechazar valores negativos o no finitos."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float, str)):
        raise TypeError("El importe debe ser numerico")

    try:
        importe = float(valor)
    except ValueError as error:
        raise ValueError("El importe debe ser numerico") from error

    if not math.isfinite(importe):
        raise ValueError("El importe debe ser un numero finito")
    if importe < 0:
        raise ValueError("El importe no puede ser negativo")

    return importe


def registrar_servicio(
    cliente_id: int,
    vehiculo: str,
    descripcion: str,
    producto: str,
    valor: Union[int, float, str],
    fecha: str,
    ruta_db: Path = DATABASE_PATH,
) -> int:
    """Guardar un servicio asociado a un cliente y devolver su identificador."""
    cliente_id = validar_id_positivo(cliente_id, "cliente")
    vehiculo = validar_texto_requerido(vehiculo, "El vehiculo")
    descripcion = validar_texto_requerido(descripcion, "La descripcion del problema")
    producto = validar_texto_requerido(producto, "El producto")
    importe = _validar_importe(valor)
    fecha_iso = _normalizar_fecha(fecha)

    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            cursor = conexion.execute(
                """
                INSERT INTO servicios (
                    cliente_id, vehiculo, descripcion, producto, valor, fecha
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    cliente_id,
                    vehiculo,
                    descripcion,
                    producto,
                    importe,
                    fecha_iso,
                ),
            )
            return cursor.lastrowid
    finally:
        conexion.close()


def modificar_servicio(
    servicio_id: int,
    vehiculo: str,
    descripcion: str,
    producto: str,
    valor: Union[int, float, str],
    fecha: str,
    ruta_db: Path = DATABASE_PATH,
) -> None:
    """Actualizar los datos de un servicio sin cambiar su cliente asociado."""
    servicio_id = validar_id_positivo(servicio_id, "servicio")
    vehiculo = validar_texto_requerido(vehiculo, "El vehiculo")
    descripcion = validar_texto_requerido(descripcion, "La descripcion del problema")
    producto = validar_texto_requerido(producto, "El producto")
    importe = _validar_importe(valor)
    fecha_iso = _normalizar_fecha(fecha)

    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            cursor = conexion.execute(
                """
                UPDATE servicios
                SET vehiculo = ?, descripcion = ?, producto = ?,
                    valor = ?, fecha = ?
                WHERE id = ?
                """,
                (
                    vehiculo,
                    descripcion,
                    producto,
                    importe,
                    fecha_iso,
                    servicio_id,
                ),
            )
            if cursor.rowcount == 0:
                raise LookupError(f"No existe un servicio con ID {servicio_id}")
    finally:
        conexion.close()


def eliminar_servicio(
    servicio_id: int,
    ruta_db: Path = DATABASE_PATH,
) -> None:
    """Eliminar un servicio existente o indicar que su ID no existe."""
    servicio_id = validar_id_positivo(servicio_id, "servicio")

    conexion = conectar_db(ruta_db)
    try:
        with conexion:
            cursor = conexion.execute(
                "DELETE FROM servicios WHERE id = ?",
                (servicio_id,),
            )
            if cursor.rowcount == 0:
                raise LookupError(f"No existe un servicio con ID {servicio_id}")

            ids_restantes = [
                fila[0]
                for fila in conexion.execute(
                    "SELECT id FROM servicios ORDER BY id"
                )
            ]
            for posicion, id_anterior in enumerate(ids_restantes, start=1):
                conexion.execute(
                    "UPDATE servicios SET id = ? WHERE id = ?",
                    (-posicion, id_anterior),
                )
            for id_nuevo in range(1, len(ids_restantes) + 1):
                conexion.execute(
                    "UPDATE servicios SET id = ? WHERE id = ?",
                    (id_nuevo, -id_nuevo),
                )

            conexion.execute(
                "DELETE FROM sqlite_sequence WHERE name = 'servicios'"
            )
            if ids_restantes:
                conexion.execute(
                    """
                    INSERT INTO sqlite_sequence (name, seq)
                    VALUES ('servicios', ?)
                    """,
                    (len(ids_restantes),),
                )
    finally:
        conexion.close()