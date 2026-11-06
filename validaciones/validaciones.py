"""Validaciones de datos compartidas por los modulos del proyecto."""


def validar_texto_requerido(valor: str, campo: str) -> str:
    """Quitar espacios externos y rechazar campos vacios o no textuales."""
    if not isinstance(valor, str):
        raise TypeError(f"{campo} debe ser texto")

    valor = valor.strip()
    if not valor:
        raise ValueError(f"{campo} no puede estar vacio")

    return valor


def validar_telefono_celular(telefono: str) -> str:
    """Aceptar teléfonos compuestos por un máximo de diez dígitos."""
    telefono = validar_texto_requerido(telefono, "El teléfono celular")
    if not telefono.isascii() or not telefono.isdigit():
        raise ValueError("El teléfono celular debe contener solo dígitos")
    if len(telefono) > 10:
        raise ValueError("El teléfono celular no puede tener más de 10 dígitos")

    return telefono


def validar_id_positivo(identificador: int, entidad: str) -> int:
    """Comprobar que un identificador sea un entero positivo."""
    if isinstance(identificador, bool) or not isinstance(identificador, int):
        raise TypeError(f"El ID de {entidad} debe ser un entero")
    if identificador <= 0:
        raise ValueError(f"El ID de {entidad} debe ser positivo")

    return identificador
