"""Punto de entrada de la aplicacion."""

from datos.database import inicializar_base_datos
from interfaz.menu import crear_ventana_principal


def main() -> None:
    """Preparar la base de datos y ejecutar la interfaz."""
    inicializar_base_datos()
    ventana = crear_ventana_principal()
    ventana.mainloop()


if __name__ == "__main__":
    main()