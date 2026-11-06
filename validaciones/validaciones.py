"""Validaciones de datos compartidas por los modulos del proyecto."""

import re


EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
    r"(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,63}"
)


def validar_texto_requerido(valor: str, campo: str) -> str:
    """Quitar espacios externos y rechazar campos vacios o no textuales."""
    if not isinstance(valor, str):
        raise TypeError(f"{campo} debe ser texto")

    valor = valor.strip()
    if not valor:
        raise ValueError(f"{campo} no puede estar vacio")

    return valor


def validar_correo(correo: str) -> str:
    """Validar un correo común con parte local y dominio completos."""
    correo = validar_texto_requerido(correo, "El correo")
    parte_local, separador, _dominio = correo.partition("@")
    if (
        not separador
        or len(correo) > 254
        or len(parte_local) > 64
        or not EMAIL_PATTERN.fullmatch(correo)
    ):
        raise ValueError(
            "El correo debe tener un formato válido, por ejemplo "
            "nombre@dominio.com"
        )

    return correo


def validar_telefono_celular(telefono: str) -> str:
    """Aceptar teléfonos compuestos por exactamente diez dígitos."""
    telefono = validar_texto_requerido(telefono, "El teléfono celular")
    if not telefono.isascii() or not telefono.isdigit():
        raise ValueError("El teléfono celular debe contener solo dígitos")
    if len(telefono) != 10:
        raise ValueError("El teléfono celular debe tener exactamente 10 dígitos")

    return telefono


def validar_id_positivo(identificador: int, entidad: str) -> int:
    """Comprobar que un identificador sea un entero positivo."""
    if isinstance(identificador, bool) or not isinstance(identificador, int):
        raise TypeError(f"El ID de {entidad} debe ser un entero")
    if identificador <= 0:
        raise ValueError(f"El ID de {entidad} debe ser positivo")

    return identificador
