"""Controles de la pestaña de servicios."""

import sqlite3
import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Dict, Optional

from clientes.consultas import listar_clientes
from datos.database import DATABASE_PATH
from servicios.historial import consultar_historial_cliente
from servicios.servicios import (
    eliminar_servicio,
    modificar_servicio,
    registrar_servicio,
)


def crear_pestana_servicios(
    contenedor: ttk.Frame,
    ruta_db: Path = DATABASE_PATH,
) -> None:
    """Agregar el formulario y el historial de servicios."""
    cliente_var = tk.StringVar()
    servicio_id_var = tk.StringVar(value="Ninguno")
    vehiculo_var = tk.StringVar()
    descripcion_var = tk.StringVar()
    producto_var = tk.StringVar()
    marca_var = tk.StringVar()
    valor_var = tk.StringVar()
    fecha_var = tk.StringVar(value=date.today().strftime("%d/%m/%Y"))
    estado_var = tk.StringVar(value="Selecciona un cliente para ver su historial.")
    clientes_por_opcion: Dict[str, int] = {}

    formulario = ttk.LabelFrame(
        contenedor,
        text="Datos del servicio",
        style="Panel.TLabelframe",
    )
    formulario.pack(fill="x", pady=(0, 16))
    for columna in (1, 3, 5):
        formulario.columnconfigure(columna, weight=1)

    ttk.Label(formulario, text="Cliente").grid(
        row=0,
        column=0,
        sticky="w",
        padx=(0, 8),
    )
    cliente_combo = ttk.Combobox(
        formulario,
        textvariable=cliente_var,
        state="readonly",
    )
    cliente_combo.grid(
        row=1,
        column=0,
        columnspan=6,
        sticky="ew",
        pady=(4, 12),
    )

    campos = (
        ("Vehículo", vehiculo_var),
        ("Descripción", descripcion_var),
        ("Producto", producto_var),
        ("Marca", marca_var),
        ("Valor", valor_var),
        ("Fecha (DD/MM/AAAA)", fecha_var),
    )
    for indice, (etiqueta, variable) in enumerate(campos):
        fila = 2 + (indice // 3) * 2
        columna = (indice % 3) * 2
        ttk.Label(formulario, text=etiqueta).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=(0, 8),
        )
        ttk.Entry(formulario, textvariable=variable).grid(
            row=fila + 1,
            column=columna,
            sticky="ew",
            padx=(0, 12),
            pady=(4, 12),
        )

    botones = ttk.Frame(formulario)
    botones.grid(row=6, column=0, columnspan=6, sticky="ew")
    ttk.Label(botones, text="ID seleccionado:").pack(side="left")
    ttk.Label(botones, textvariable=servicio_id_var).pack(
        side="left",
        padx=(4, 16),
    )

    tabla_marco = ttk.Frame(contenedor)
    tabla_marco.pack(fill="both", expand=True)
    columnas = (
        "id",
        "vehiculo",
        "descripcion",
        "producto",
        "marca",
        "valor",
        "fecha",
    )
    tabla = ttk.Treeview(
        tabla_marco,
        columns=columnas,
        show="headings",
        selectmode="browse",
    )
    tabla.tag_configure("fila_par", background="#0E192B")
    tabla.tag_configure("fila_impar", background="#121F34")
    titulos = {
        "id": "ID",
        "vehiculo": "Vehículo",
        "descripcion": "Descripción",
        "producto": "Producto",
        "marca": "Marca",
        "valor": "Valor",
        "fecha": "Fecha",
    }
    anchos = {
        "id": 55,
        "vehiculo": 120,
        "descripcion": 170,
        "producto": 120,
        "marca": 110,
        "valor": 90,
        "fecha": 100,
    }
    for columna in columnas:
        tabla.heading(columna, text=titulos[columna])
        tabla.column(
            columna,
            width=anchos[columna],
            anchor="w",
            stretch=columna in ("descripcion", "vehiculo"),
        )
    tabla.column("id", anchor="center", stretch=False)

    desplazamiento_vertical = ttk.Scrollbar(
        tabla_marco,
        orient="vertical",
        command=tabla.yview,
    )
    desplazamiento_horizontal = ttk.Scrollbar(
        contenedor,
        orient="horizontal",
        command=tabla.xview,
    )
    tabla.configure(
        yscrollcommand=desplazamiento_vertical.set,
        xscrollcommand=desplazamiento_horizontal.set,
    )
    tabla.pack(side="left", fill="both", expand=True)
    desplazamiento_vertical.pack(side="right", fill="y")
    desplazamiento_horizontal.pack(fill="x")

    def limpiar_formulario() -> None:
        vehiculo_var.set("")
        descripcion_var.set("")
        producto_var.set("")
        marca_var.set("")
        valor_var.set("")
        fecha_var.set(date.today().strftime("%d/%m/%Y"))
        servicio_id_var.set("Ninguno")
        for elemento in tabla.selection():
            tabla.selection_remove(elemento)

    def actualizar_tabla(servicios) -> None:
        for elemento in tabla.get_children():
            tabla.delete(elemento)

        for indice, servicio in enumerate(servicios):
            fecha_vista = date.fromisoformat(servicio["fecha"]).strftime("%d/%m/%Y")
            tabla.insert(
                "",
                "end",
                values=(
                    servicio["id"],
                    servicio["vehiculo"],
                    servicio["descripcion"],
                    servicio["producto"],
                    servicio["marca"],
                    f'{float(servicio["valor"]):.2f}',
                    fecha_vista,
                ),
                tags=("fila_par" if indice % 2 == 0 else "fila_impar",),
            )

    def obtener_cliente_id() -> Optional[int]:
        return clientes_por_opcion.get(cliente_var.get())

    def recargar_historial() -> None:
        cliente_id = obtener_cliente_id()
        limpiar_formulario()
        if cliente_id is None:
            actualizar_tabla([])
            estado_var.set("Primero registra o selecciona un cliente.")
            return

        try:
            historial = consultar_historial_cliente(cliente_id, ruta_db)
        except (ValueError, sqlite3.Error) as error:
            actualizar_tabla([])
            estado_var.set(f"No se pudo cargar el historial: {error}")
            return

        actualizar_tabla(historial)
        estado_var.set(f"Servicios encontrados: {len(historial)}")

    def cargar_clientes() -> None:
        cliente_actual = cliente_var.get()
        try:
            clientes = listar_clientes(ruta_db)
        except sqlite3.Error as error:
            estado_var.set(f"No se pudo cargar la lista de clientes: {error}")
            return

        clientes_por_opcion.clear()
        opciones = []
        for cliente in clientes:
            opcion = (
                f'{cliente["id"]} - {cliente["nombre"]} '
                f'({cliente["telefono"]})'
            )
            opciones.append(opcion)
            clientes_por_opcion[opcion] = cliente["id"]

        cliente_combo["values"] = opciones
        if opciones:
            if cliente_actual in clientes_por_opcion:
                cliente_var.set(cliente_actual)
            else:
                cliente_var.set(opciones[0])
            recargar_historial()
        else:
            cliente_var.set("")
            recargar_historial()

    def guardar() -> None:
        cliente_id = obtener_cliente_id()
        if cliente_id is None:
            estado_var.set("Selecciona un cliente antes de guardar el servicio.")
            return

        try:
            nuevo_id = registrar_servicio(
                cliente_id,
                vehiculo_var.get(),
                descripcion_var.get(),
                producto_var.get(),
                marca_var.get(),
                valor_var.get(),
                fecha_var.get(),
                ruta_db,
            )
        except (TypeError, ValueError, sqlite3.Error) as error:
            estado_var.set(f"No se pudo guardar el servicio: {error}")
            return

        recargar_historial()
        limpiar_formulario()
        estado_var.set(f"Servicio guardado con ID {nuevo_id}.")

    def modificar() -> None:
        if servicio_id_var.get() == "Ninguno":
            estado_var.set("Selecciona un servicio de la tabla para modificarlo.")
            return

        try:
            modificar_servicio(
                int(servicio_id_var.get()),
                vehiculo_var.get(),
                descripcion_var.get(),
                producto_var.get(),
                marca_var.get(),
                valor_var.get(),
                fecha_var.get(),
                ruta_db,
            )
        except (TypeError, ValueError, LookupError, sqlite3.Error) as error:
            estado_var.set(f"No se pudo modificar el servicio: {error}")
            return

        recargar_historial()
        limpiar_formulario()
        estado_var.set("Servicio actualizado.")

    def eliminar() -> None:
        if servicio_id_var.get() == "Ninguno":
            estado_var.set("Selecciona un servicio de la tabla para eliminarlo.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Deseas eliminar el servicio seleccionado?",
            parent=contenedor,
        )
        if not confirmar:
            return

        try:
            eliminar_servicio(int(servicio_id_var.get()), ruta_db)
        except (TypeError, ValueError, LookupError, sqlite3.Error) as error:
            estado_var.set(f"No se pudo eliminar el servicio: {error}")
            return

        recargar_historial()
        limpiar_formulario()
        estado_var.set("Servicio eliminado.")

    def seleccionar_servicio(_evento) -> None:
        seleccion = tabla.selection()
        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")
        servicio_id_var.set(valores[0])
        vehiculo_var.set(valores[1])
        descripcion_var.set(valores[2])
        producto_var.set(valores[3])
        marca_var.set(valores[4])
        valor_var.set(valores[5])
        fecha_var.set(valores[6])
        estado_var.set(f"Servicio {valores[0]} seleccionado.")

    ttk.Button(
        botones,
        text="Guardar servicio",
        style="Accent.TButton",
        command=guardar,
    ).pack(side="right", padx=(8, 0))
    ttk.Button(
        botones,
        text="Modificar seleccionado",
        command=modificar,
    ).pack(side="right", padx=(8, 0))
    ttk.Button(
        botones,
        text="Eliminar seleccionado",
        style="Danger.TButton",
        command=eliminar,
    ).pack(side="right", padx=(8, 0))
    ttk.Button(
        botones,
        text="Limpiar",
        command=limpiar_formulario,
    ).pack(side="right")
    ttk.Button(
        botones,
        text="Actualizar clientes",
        command=cargar_clientes,
    ).pack(side="left", padx=(8, 0))

    cliente_combo.bind("<<ComboboxSelected>>", lambda _evento: recargar_historial())
    tabla.bind("<<TreeviewSelect>>", seleccionar_servicio)
    ttk.Label(
        contenedor,
        textvariable=estado_var,
        style="Status.TLabel",
    ).pack(anchor="w", pady=(10, 0))

    cargar_clientes()
