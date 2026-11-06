"""Controles de la pestaña de clientes."""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from clientes.clientes import (
    eliminar_cliente,
    modificar_cliente,
    registrar_cliente,
)
from clientes.consultas import buscar_clientes, listar_clientes


def crear_pestana_clientes(contenedor: ttk.Frame) -> None:
    """Agregar el formulario, la búsqueda y la tabla de clientes."""
    nombre_var = tk.StringVar()
    correo_var = tk.StringVar()
    telefono_var = tk.StringVar()
    busqueda_var = tk.StringVar()
    cliente_id_var = tk.StringVar(value="Ninguno")
    estado_var = tk.StringVar(value="Listo.")

    formulario = ttk.LabelFrame(
        contenedor,
        text="Datos del cliente",
        style="Panel.TLabelframe",
    )
    formulario.pack(fill="x", pady=(0, 16))

    campos = (
        ("Nombre", nombre_var),
        ("Correo", correo_var),
        ("Teléfono celular (10 dígitos)", telefono_var),
    )
    for columna in (1, 3, 5):
        formulario.columnconfigure(columna, weight=1)

    for indice, (etiqueta, variable) in enumerate(campos):
        columna = indice * 2
        ttk.Label(formulario, text=etiqueta).grid(
            row=0,
            column=columna,
            sticky="w",
            padx=(0, 8),
        )
        ttk.Entry(formulario, textvariable=variable).grid(
            row=1,
            column=columna,
            sticky="ew",
            padx=(0, 12),
            pady=(4, 12),
        )

    botones = ttk.Frame(formulario)
    botones.grid(row=2, column=0, columnspan=6, sticky="ew")
    ttk.Label(
        botones,
        text="ID seleccionado:",
    ).pack(side="left")
    ttk.Label(
        botones,
        textvariable=cliente_id_var,
    ).pack(side="left", padx=(4, 16))

    def limpiar_formulario() -> None:
        nombre_var.set("")
        correo_var.set("")
        telefono_var.set("")
        cliente_id_var.set("Ninguno")
        for elemento in tabla.selection():
            tabla.selection_remove(elemento)
        estado_var.set("Formulario limpio.")

    def actualizar_tabla(clientes) -> None:
        for elemento in tabla.get_children():
            tabla.delete(elemento)

        for indice, cliente in enumerate(clientes):
            tabla.insert(
                "",
                "end",
                values=(
                    cliente["id"],
                    cliente["nombre"],
                    cliente["correo"],
                    cliente["telefono"],
                ),
                tags=("fila_par" if indice % 2 == 0 else "fila_impar",),
            )

    def cargar_clientes() -> None:
        try:
            clientes = listar_clientes()
        except sqlite3.Error as error:
            estado_var.set(f"No se pudo cargar la lista de clientes: {error}")
            return

        actualizar_tabla(clientes)
        estado_var.set(f"Clientes registrados: {len(clientes)}")

    def mostrar_todos() -> None:
        busqueda_var.set("")
        cargar_clientes()

    def buscar() -> None:
        termino = busqueda_var.get().strip()
        if not termino:
            cargar_clientes()
            return

        try:
            resultados = buscar_clientes(termino)
        except (ValueError, sqlite3.Error) as error:
            estado_var.set(f"No se pudo completar la búsqueda: {error}")
            return

        actualizar_tabla(resultados)
        estado_var.set(f"Resultados encontrados: {len(resultados)}")

    def guardar() -> None:
        try:
            nuevo_id = registrar_cliente(
                nombre_var.get(),
                correo_var.get(),
                telefono_var.get(),
            )
        except (TypeError, ValueError, sqlite3.Error) as error:
            estado_var.set(f"No se pudo guardar el cliente: {error}")
            return

        busqueda_var.set("")
        cargar_clientes()
        limpiar_formulario()
        estado_var.set(f"Cliente guardado con ID {nuevo_id}.")

    def modificar() -> None:
        if cliente_id_var.get() == "Ninguno":
            estado_var.set("Selecciona un cliente de la tabla para modificarlo.")
            return

        try:
            modificar_cliente(
                int(cliente_id_var.get()),
                nombre_var.get(),
                correo_var.get(),
                telefono_var.get(),
            )
        except (TypeError, ValueError, LookupError, sqlite3.Error) as error:
            estado_var.set(f"No se pudo modificar el cliente: {error}")
            return

        busqueda_var.set("")
        cargar_clientes()
        limpiar_formulario()
        estado_var.set("Cliente actualizado.")

    def eliminar() -> None:
        if cliente_id_var.get() == "Ninguno":
            estado_var.set("Selecciona un cliente de la tabla para eliminarlo.")
            return

        cliente_id = int(cliente_id_var.get())
        if not messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Deseas eliminar a {nombre_var.get()}? "
            "Esta acción no se puede deshacer.",
            parent=contenedor,
        ):
            return

        try:
            eliminar_cliente(cliente_id)
        except (TypeError, ValueError, LookupError, sqlite3.Error) as error:
            estado_var.set(f"No se pudo eliminar el cliente: {error}")
            return

        busqueda_var.set("")
        limpiar_formulario()
        cargar_clientes()
        estado_var.set("Cliente eliminado.")

    ttk.Button(
        botones,
        text="Guardar cliente",
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

    busqueda = ttk.Frame(contenedor)
    busqueda.pack(fill="x", pady=(0, 10))
    ttk.Label(
        busqueda,
        text="Buscar por nombre o teléfono:",
    ).pack(side="left", padx=(0, 10))
    entrada_busqueda = ttk.Entry(busqueda, textvariable=busqueda_var)
    entrada_busqueda.pack(side="left", fill="x", expand=True)
    entrada_busqueda.bind("<Return>", lambda _evento: buscar())
    ttk.Button(
        busqueda,
        text="Buscar",
        command=buscar,
    ).pack(side="left", padx=(8, 0))
    ttk.Button(
        busqueda,
        text="Mostrar todos",
        command=mostrar_todos,
    ).pack(side="left", padx=(8, 0))

    tabla_marco = ttk.Frame(contenedor)
    tabla_marco.pack(fill="both", expand=True)
    columnas = ("id", "nombre", "correo", "telefono")
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
        "nombre": "Nombre",
        "correo": "Correo",
        "telefono": "Teléfono",
    }
    anchos = {"id": 60, "nombre": 200, "correo": 280, "telefono": 150}
    for columna in columnas:
        tabla.heading(columna, text=titulos[columna])
        tabla.column(columna, width=anchos[columna], anchor="w")
    tabla.column("id", anchor="center", stretch=False)

    desplazamiento = ttk.Scrollbar(
        tabla_marco,
        orient="vertical",
        command=tabla.yview,
    )
    tabla.configure(yscrollcommand=desplazamiento.set)
    tabla.pack(side="left", fill="both", expand=True)
    desplazamiento.pack(side="right", fill="y")

    def seleccionar_cliente(_evento) -> None:
        seleccion = tabla.selection()
        if not seleccion:
            return

        valores = tabla.item(seleccion[0], "values")
        cliente_id_var.set(valores[0])
        nombre_var.set(valores[1])
        correo_var.set(valores[2])
        telefono_var.set(valores[3])
        estado_var.set(f"Cliente {valores[0]} seleccionado.")

    tabla.bind("<<TreeviewSelect>>", seleccionar_cliente)
    ttk.Label(
        contenedor,
        textvariable=estado_var,
        style="Status.TLabel",
    ).pack(anchor="w", pady=(10, 0))
    cargar_clientes()
