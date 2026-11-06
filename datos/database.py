"""Conexión y preparación de la base de datos SQLite."""

from pathlib import Path
import sqlite3


DATABASE_PATH = Path(__file__).resolve().parent / "automotriz.db"


def conectar_db(ruta_db: Path = DATABASE_PATH) -> sqlite3.Connection:
    """Abrir la base de datos y habilitar la validación de claves foráneas."""
    ruta_db.parent.mkdir(parents=True, exist_ok=True)
    conexion = sqlite3.connect(ruta_db)
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_base_datos(ruta_db: Path = DATABASE_PATH) -> None:
    """Crear el esquema y migrar a IDs de servicio únicos por cliente."""
    conexion = conectar_db(ruta_db)
    try:
        conexion.execute("PRAGMA foreign_keys = OFF")
        with conexion:
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    correo TEXT NOT NULL,
                    telefono TEXT NOT NULL
                )
                """
            )
            conexion.execute(
                """
                CREATE TABLE IF NOT EXISTS servicios (
                    id INTEGER NOT NULL,
                    cliente_id INTEGER NOT NULL,
                    vehiculo TEXT NOT NULL,
                    descripcion TEXT NOT NULL,
                    producto TEXT NOT NULL,
                    valor REAL NOT NULL,
                    fecha TEXT NOT NULL,
                    PRIMARY KEY (cliente_id, id),
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                )
                """
            )
            informacion_columnas = list(
                conexion.execute("PRAGMA table_info(servicios)")
            )
            columnas = {fila[1] for fila in informacion_columnas}
            claves_primarias = tuple(
                fila[1]
                for fila in sorted(
                    (fila for fila in informacion_columnas if fila[5]),
                    key=lambda fila: fila[5],
                )
            )
            if "marca" in columnas or claves_primarias != ("cliente_id", "id"):
                conexion.execute(
                    "ALTER TABLE servicios RENAME TO servicios_anteriores"
                )
                conexion.execute(
                    """
                    CREATE TABLE servicios (
                        id INTEGER NOT NULL,
                        cliente_id INTEGER NOT NULL,
                        vehiculo TEXT NOT NULL,
                        descripcion TEXT NOT NULL,
                        producto TEXT NOT NULL,
                        valor REAL NOT NULL,
                        fecha TEXT NOT NULL,
                        PRIMARY KEY (cliente_id, id),
                        FOREIGN KEY (cliente_id) REFERENCES clientes (id)
                    )
                    """
                )
                servicios_anteriores = conexion.execute(
                    """
                    SELECT cliente_id, vehiculo, descripcion, producto,
                           valor, fecha
                    FROM servicios_anteriores
                    ORDER BY cliente_id, id
                    """
                ).fetchall()
                siguiente_id_por_cliente = {}
                for servicio in servicios_anteriores:
                    cliente_id = servicio[0]
                    siguiente_id = siguiente_id_por_cliente.get(cliente_id, 0) + 1
                    conexion.execute(
                        """
                        INSERT INTO servicios (
                            id, cliente_id, vehiculo, descripcion,
                            producto, valor, fecha
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (siguiente_id, *servicio),
                    )
                    siguiente_id_por_cliente[cliente_id] = siguiente_id
                conexion.execute("DROP TABLE servicios_anteriores")
    finally:
        conexion.execute("PRAGMA foreign_keys = ON")
        conexion.close()