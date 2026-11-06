"""Ventana principal del sistema de gestion automotriz."""

import tkinter as tk
from tkinter import ttk

from interfaz.clientes import crear_pestana_clientes
from interfaz.servicios import crear_pestana_servicios


BACKGROUND = "#0B1220"
SURFACE = "#111B2E"
PANEL = "#121D31"
INPUT = "#0D1729"
BORDER = "#263550"
ACCENT = "#14B8A6"
ACCENT_HOVER = "#0F9F92"
TEXT = "#F1F5F9"
MUTED_TEXT = "#9AA9BF"


def crear_ventana_principal() -> tk.Tk:
    """Crear la ventana principal con pestañas para clientes y servicios."""
    ventana = tk.Tk()
    ventana.title("Gestión automotriz")
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    ancho = min(1120, max(900, ancho_pantalla - 80))
    alto = min(680, max(650, alto_pantalla - 100))
    posicion_x = max(0, (ancho_pantalla - ancho) // 2)
    posicion_y = max(0, (alto_pantalla - alto) // 2)
    ventana.geometry(f"{ancho}x{alto}+{posicion_x}+{posicion_y}")
    ventana.minsize(900, 650)
    ventana.configure(background=BACKGROUND)

    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure("TFrame", background=BACKGROUND)
    estilo.configure("Panel.TFrame", background=PANEL)
    estilo.configure("Toolbar.TFrame", background=BACKGROUND)
    estilo.configure(
        "TLabelframe",
        background=PANEL,
        foreground=TEXT,
        bordercolor=BORDER,
        borderwidth=1,
        relief="solid",
        padding=16,
    )
    estilo.configure(
        "Panel.TLabelframe",
        background=PANEL,
        foreground=TEXT,
        bordercolor=BORDER,
        borderwidth=1,
        relief="solid",
        padding=16,
    )
    estilo.configure(
        "TLabelframe.Label",
        background=PANEL,
        foreground="#5EEAD4",
        font=("Segoe UI Semibold", 10),
    )
    estilo.configure(
        "Panel.TLabelframe.Label",
        background=PANEL,
        foreground="#5EEAD4",
        font=("Segoe UI Semibold", 10),
    )
    estilo.configure(
        "TLabel",
        background=BACKGROUND,
        foreground=TEXT,
        font=("Segoe UI", 10),
    )
    estilo.configure(
        "Header.TFrame",
        background=SURFACE,
    )
    estilo.configure(
        "Eyebrow.TLabel",
        background=SURFACE,
        foreground="#5EEAD4",
        font=("Segoe UI Semibold", 9),
    )
    estilo.configure(
        "Title.TLabel",
        background=SURFACE,
        foreground=TEXT,
        font=("Segoe UI Semibold", 22),
    )
    estilo.configure(
        "Subtitle.TLabel",
        background=SURFACE,
        foreground=MUTED_TEXT,
        font=("Segoe UI", 10),
    )
    estilo.configure(
        "Muted.TLabel",
        background=BACKGROUND,
        foreground=MUTED_TEXT,
    )
    estilo.configure(
        "Badge.TLabel",
        background="#0E2C35",
        foreground="#5EEAD4",
        font=("Segoe UI Semibold", 9),
        padding=(11, 7),
    )
    estilo.configure(
        "Status.TLabel",
        background=BACKGROUND,
        foreground="#5EEAD4",
        font=("Segoe UI", 9),
        padding=(2, 5),
    )
    estilo.configure(
        "TNotebook",
        background=BACKGROUND,
        borderwidth=0,
    )
    estilo.configure(
        "TNotebook.Tab",
        background=SURFACE,
        foreground=MUTED_TEXT,
        padding=(20, 11),
        font=("Segoe UI Semibold", 10),
    )
    estilo.configure(
        "TEntry",
        fieldbackground=INPUT,
        foreground=TEXT,
        insertcolor=TEXT,
        bordercolor=BORDER,
        padding=(9, 8),
    )
    estilo.configure(
        "TCombobox",
        fieldbackground=INPUT,
        foreground=TEXT,
        bordercolor=BORDER,
        padding=(8, 7),
        arrowcolor=MUTED_TEXT,
    )
    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", INPUT)],
        foreground=[("readonly", TEXT)],
        selectbackground=[("readonly", INPUT)],
        selectforeground=[("readonly", TEXT)],
    )
    estilo.configure(
        "Treeview",
        background="#0E192B",
        fieldbackground="#0E192B",
        foreground=TEXT,
        rowheight=32,
        borderwidth=0,
        font=("Segoe UI", 10),
    )
    estilo.configure(
        "Treeview.Heading",
        background="#1A2941",
        foreground=TEXT,
        font=("Segoe UI Semibold", 9),
        padding=(10, 10),
        relief="flat",
    )
    estilo.configure(
        "TScrollbar",
        background=SURFACE,
        troughcolor=BACKGROUND,
        borderwidth=0,
        arrowcolor=MUTED_TEXT,
    )
    estilo.configure(
        "Accent.TButton",
        background=ACCENT,
        foreground="#062522",
        padding=(13, 9),
        borderwidth=0,
        font=("Segoe UI Semibold", 9),
    )
    estilo.configure(
        "TButton",
        background=SURFACE,
        foreground=TEXT,
        padding=(12, 9),
        bordercolor=BORDER,
        borderwidth=1,
        font=("Segoe UI Semibold", 9),
    )
    estilo.configure(
        "Danger.TButton",
        background="#542331",
        foreground="#FECACA",
        padding=(12, 9),
        borderwidth=0,
        font=("Segoe UI Semibold", 9),
    )
    estilo.map(
        "Accent.TButton",
        background=[("active", ACCENT_HOVER)],
        foreground=[("active", "#042522")],
    )
    estilo.map(
        "TButton",
        background=[("active", "#1D2B42")],
        bordercolor=[("focus", ACCENT)],
    )
    estilo.map(
        "Danger.TButton",
        background=[("active", "#713044")],
    )
    estilo.map(
        "Treeview",
        background=[("selected", "#0F766E")],
        foreground=[("selected", "#F0FDFA")],
    )
    estilo.map(
        "TNotebook.Tab",
        background=[("selected", ACCENT), ("active", "#1D2B42")],
        foreground=[("selected", "#062522"), ("active", TEXT)],
    )
    estilo.map(
        "TEntry",
        fieldbackground=[("focus", "#132139")],
        bordercolor=[("focus", ACCENT)],
    )

    encabezado = ttk.Frame(ventana, style="Header.TFrame", padding=(24, 18))
    encabezado.pack(fill="x", padx=20, pady=(16, 10))
    titulo = ttk.Frame(encabezado, style="Header.TFrame")
    titulo.pack(side="left", fill="x", expand=True)
    ttk.Label(
        titulo,
        text="GESTIÓN AUTOMOTRIZ / CONTROL DE SERVICIOS",
        style="Eyebrow.TLabel",
    ).pack(anchor="w", pady=(0, 5))
    ttk.Label(
        titulo,
        text="Clientes y servicios",
        style="Title.TLabel",
    ).pack(anchor="w")
    ttk.Label(
        titulo,
        text="Administra clientes, trabajos e historial desde un solo lugar.",
        style="Subtitle.TLabel",
    ).pack(anchor="w", pady=(5, 0))
    ttk.Label(
        encabezado,
        text="BASE LOCAL  ·  SQLITE",
        style="Badge.TLabel",
    ).pack(side="right", anchor="n", padx=(16, 0))

    pestañas = ttk.Notebook(ventana)
    pestañas.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    clientes = ttk.Frame(pestañas, padding=14)
    servicios = ttk.Frame(pestañas, padding=14)
    pestañas.add(clientes, text="Clientes")
    pestañas.add(servicios, text="Servicios")

    crear_pestana_clientes(clientes)

    actualizar_clientes_servicios = crear_pestana_servicios(servicios)

    def actualizar_al_abrir_servicios(_evento: tk.Event) -> None:
        if pestañas.select() == str(servicios):
            actualizar_clientes_servicios()

    pestañas.bind("<<NotebookTabChanged>>", actualizar_al_abrir_servicios)

    return ventana