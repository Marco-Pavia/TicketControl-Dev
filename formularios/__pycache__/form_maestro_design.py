import tkinter as tk
import datetime
from PIL import Image, ImageTk
from mailjet_rest import Client
from fpdf import FPDF
from tkinter import messagebox
from tkinter import font, ttk, StringVar, PhotoImage
from datetime import datetime
import util.util_ventana as util_ventana
import util.util_imagenes as util_img
from tkinter import Toplevel, IntVar
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import win32print
import win32ui
import win32con
import sqlite3
class FormularioMaestroDesign(tk.Tk):
    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen("./imagenes/perfil.png", (560, 136))
        self.perfil = util_img.leer_imagen("./imagenes/logo.png", (100, 100))
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.crear_secciones()
        self.mostrar_seccion("inicio")  #Crear pantalla de inicio o inicar con frame inicio


        self.db_connection = sqlite3.connect('rentas.db')
        self.db_cursor = self.db_connection.cursor()
        self.create_table_tickets()

    def config_window(self):
        # Configuración inicial de la ventana Tkinter
        self.title('Sistema de Control de Tickets')
        self.iconbitmap("./imagenes/logo.ico")
        w, h = 1400, 750
        util_ventana.centrar_ventana(self, w, h)

    def paneles(self):
        # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    def controles_barra_superior(self):
        # Configuración de la barra superior
        font_awesome = font.Font(family='FontAwesome', size=12)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Autotransportes Banderilla")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=24)
        self.labelTitulo.pack(side=tk.LEFT)

        # Botón del menú lateral
        self.buttonMenuLateral = tk.Button(self.barra_superior, text="\uf0c9", font=font_awesome,
                                           command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT)

        # Etiqueta de información
        self.labelTitulo = tk.Label(self.barra_superior, text="Soporte Técnico: 2294733415")
        self.labelTitulo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelTitulo.pack(side=tk.RIGHT)

        # Menú en la barra superior
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

        # Menú desplegable para la gestión de espacios
        menu_gestion = tk.Menu(self.menu_bar, tearoff=0)
        menu_gestion.add_command(label="Rentar Espacio", command=self.rentar_espacio)
        menu_gestion.add_command(label="Liberar Espacio", command=self.solicitar_folio_liberacion)
        menu_gestion.add_command(label="Cancelar Ticket", command=self.solicitar_folio_cancelacion)
        menu_gestion.add_command(label="Generar Corte del día", command=self.generar_corte_diario)

        # Añadir el menú de gestión a la barra de menús
        self.menu_bar.add_cascade(label="Gestión de Estacionamiento", menu=menu_gestion)

    def crear_secciones(self):
        # Crear los frames para las diferentes secciones dentro del cuerpo principal
        self.secciones = {
            "inicio": tk.Frame(self.cuerpo_principal, bg="white"),
            "informacion": tk.Frame(self.cuerpo_principal, bg="white"),
            "configuracion": tk.Frame(self.cuerpo_principal, bg="white"),
            "cerrar_sesion": tk.Frame(self.cuerpo_principal, bg="white"),
        }
        self.sub_secciones = {
            "tickets": tk.Frame(self.secciones["inicio"], bg="lightblue"),
            "salidas": tk.Frame(self.secciones["inicio"], bg="lightcoral"),
            "cancelado": tk.Frame(self.secciones["inicio"], bg="lightcoral"),
        }
        #Función menu fijo
        self.menu_superior = tk.Frame(self.secciones["inicio"], bg="blue", height=100)
        self.menu_superior.pack(side="top", fill="x")
        #Botón tickets
        self.boton_Tickets = tk.Button(self.menu_superior, text="Entrada",
                                       command=lambda: self.mostrar_sub_seccion('tickets'))
        self.boton_Tickets.pack(side="left", padx=10, pady=10)
        #Botón Entradas-Salidas
        self.boton_entradas_salidas = tk.Button(self.menu_superior, text="Salidas",
                                                command=lambda: self.mostrar_sub_seccion('salidas'))
        self.boton_entradas_salidas.pack(side="left", padx=10, pady=10)
        #Botón Reportes
        self.boton_reportes = tk.Button(self.menu_superior, text="Tickets Cancelados",
                                        command=lambda: self.mostrar_sub_seccion('cancelado'))
        self.boton_reportes.pack(side="left", padx=10, pady=10)


        # Cargar la imagen y colocarla en la sección de inicio
        image = Image.open("./imagenes/imagen.png")
        self.imagen_inicio = ImageTk.PhotoImage(image)
        self.label_imagen = tk.Label(self.secciones["inicio"], image=self.imagen_inicio)
        self.label_imagen.pack(pady=20)  # Ajusta padding y posicionamiento

        # Inicialmente, oculta todas las secciones
        for seccion in self.secciones.values():
            seccion.pack_forget()
        # Subseccion tickets
        self.tree = ttk.Treeview(self.sub_secciones["tickets"],
                                 columns=("estado", "folio", "placas", "marca", "modelo", "color", "telefono", "hora", "precio"), show='headings')
        self.tree.heading("estado", text="Estado")
        self.tree.heading("folio", text="Folio")
        self.tree.heading("placas", text="Placas")
        self.tree.heading("marca", text="Marca")
        self.tree.heading("modelo", text="Modelo")
        self.tree.heading("color", text="Color")
        self.tree.heading("telefono", text="Telefono")
        self.tree.heading("hora", text="Hora de Registro")
        self.tree.heading("precio", text="Precio $")
        self.tree.pack(fill="both", expand=True)


        self.tree_entradas = ttk.Treeview(self.sub_secciones["salidas"],
                                          columns=(
                                          "estado", "folio", "placas", "marca", "modelo", "color", "telefono", "hora",
                                          "salida", "precio"), show='headings')
        self.tree_entradas.heading("estado", text="Estado")
        self.tree_entradas.heading("folio", text="Folio")
        self.tree_entradas.heading("placas", text="Placas")
        self.tree_entradas.heading("marca", text="Marca")
        self.tree_entradas.heading("modelo", text="Modelo")
        self.tree_entradas.heading("color", text="Color")
        self.tree_entradas.heading("telefono", text="Telefono")
        self.tree_entradas.heading("hora", text="Entrada")
        self.tree_entradas.heading("salida", text="Salida")
        self.tree_entradas.heading("precio", text="Precio $")
        self.tree_entradas.pack(fill="both", expand=True)

        self.tree_cancelado = ttk.Treeview(self.sub_secciones["cancelado"],
                                          columns=(
                                              "estado", "folio", "placas", "motivo", "comentario", "hora",
                                              "precio"), show='headings')
        self.tree_cancelado.heading("estado", text="Estado")
        self.tree_cancelado.heading("folio", text="Folio")
        self.tree_cancelado.heading("placas", text="Placas")
        self.tree_cancelado.heading("motivo", text="Motivo")
        self.tree_cancelado.heading("comentario", text="Observación")
        self.tree_cancelado.heading("hora", text="Hora Cancelación")
        self.tree_cancelado.heading("precio", text="Precio $")
        self.tree_cancelado.pack(fill="both", expand=True)

        # Sección "Información"
        label_informacion = tk.Label(self.secciones["informacion"], text="Frame de Información en proceso",
                                       font=("Arial", 20))
        label_informacion.pack(expand=True)
        # Sección "Configuración"
        label_configuracion = tk.Label(self.secciones["configuracion"], text="Frame de Configuración en proceso",
                                       font=("Arial", 20))
        label_configuracion.pack(expand=True)
        # Sección "Cerrar Sesión"
        label_cerrar = tk.Label(self.secciones["cerrar_sesion"], text="Frame de Cerrar Sesión en proceso",
                                       font=("Arial", 20))
        label_cerrar.pack(expand=True)
        # Inicialmente, oculta todas las secciones
        for seccion in self.sub_secciones.values():
            seccion.pack_forget()
    def mostrar_seccion(self, seccion):
        # Oculta todas las secciones principales
        for s in self.secciones.values():
            s.pack_forget()
        # Oculta todas las subsecciones
        for sub in self.sub_secciones.values():
            sub.pack_forget()
        # Muestra la sección seleccionada
        if seccion in self.secciones:
            self.secciones[seccion].pack(fill='both', expand=True)
            if seccion == 'inicio':
                self.mostrar_widgets_inicio()
        else:
            print(f"No existe la sección {seccion}")

    def mostrar_sub_seccion(self, sub_seccion):
        # Oculta todas las subsecciones
        for sub in self.sub_secciones.values():
            sub.pack_forget()

        # Muestra la subsección correspondiente
        if sub_seccion in self.sub_secciones:
            self.sub_secciones[sub_seccion].pack(fill='both', expand=True)

            # Manejo de la imagen
            if sub_seccion == 'tickets':
                self.label_imagen.pack_forget()  # Ocultar imagen en tickets
            elif sub_seccion == 'salidas':
                self.label_imagen.pack_forget()  # Ocultar imagen en salidas
            elif sub_seccion == 'cancelado':
                self.label_imagen.pack_forget()  # Ocultar imagen en cancelado

            # Actualizar los tickets si es la subsección de "tickets"
            if sub_seccion == 'tickets':
                self.actualizar_seccion_inicio()
            # Actualizar las salidas si es la subsección de "salidas"
            elif sub_seccion == 'salidas':
                self.actualizar_seccion_salidas()
            elif sub_seccion == 'cancelado':
                self.actualizar_seccion_cancelados()
        else:
            print(f"No existe la subsección {sub_seccion}")

    def mostrar_widgets_inicio(self):
        # Asegúrate de que todos los widgets se muestren cuando estemos en 'inicio'
        self.boton_Tickets.pack(pady=5)
        self.boton_entradas_salidas.pack(pady=5)
        self.boton_reportes.pack(pady=5)
        self.label_imagen.pack(pady=20)
        self.tree.pack(fill="both", expand=True)

    def controles_menu_lateral(self):
        # Configuración del menú lateral
        ancho_menu = 20
        alto_menu = 2
        font_awesome = font.Font(family='FontAwesome', size=15)

        # Etiqueta de perfil
        self.labelPerfil = tk.Label(self.menu_lateral, image=self.perfil, bg=COLOR_MENU_LATERAL)
        self.labelPerfil.pack(side=tk.TOP, pady=10)

        # Botones del menú lateral
        self.buttonDashBoard = tk.Button(self.menu_lateral, command=lambda: self.mostrar_seccion("inicio"))
        self.buttoninfo = tk.Button(self.menu_lateral, command=lambda: self.mostrar_seccion("informacion"))
        self.buttonProfile = tk.Button(self.menu_lateral, command=lambda: self.mostrar_seccion("configuracion"))
        self.buttoncerrar = tk.Button(self.menu_lateral, command=lambda: self.mostrar_seccion("cerrar_sesion"))
        buttons_info = [
            ("Inicio", "\uf109", self.buttonDashBoard),
            ("Información", "\uf108", self.buttoninfo),
            ("Configuracion", "\uf007", self.buttonProfile),
            ("Cerrar Sesión", "\uf109", self.buttoncerrar),
        ]

        for text, icon, button in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)

    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo, bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def configurar_boton_menu(self, button, text, icon, font_awesome, ancho_menu, alto_menu):
        button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        # Asociar eventos Enter y Leave con la función dinámica
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        # Cambiar estilo al pasar el ratón por encima
        button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

    def on_leave(self, event, button):
        # Restaurar estilo al salir el ratón
        button.config(bg=COLOR_MENU_LATERAL, fg='white')

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')

    def imprimir_texto(self, texto):
        try:
            printer_name = win32print.GetDefaultPrinter()
            hprinter = win32print.OpenPrinter(printer_name)
            try:
                # Crear el objeto de impresión
                hdc = win32ui.CreateDC()
                hdc.CreatePrinterDC(printer_name)
                hdc.StartDoc("Recibo")
                hdc.StartPage()

                # Configurar el modo de mapa y el fondo
                hdc.SetMapMode(win32con.MM_TEXT)
                hdc.SetBkMode(win32con.TRANSPARENT)

                # Ajustar el tamaño de la fuente y márgenes
                font_size = 30  # Ajusta el tamaño de la fuente aquí
                font = win32ui.CreateFont({
                    "name": "Arial",
                    "height": font_size,
                })
                hdc.SelectObject(font)

                # Medir la altura de una línea de texto
                text_metrics = hdc.GetTextExtent("Ay")
                line_height = text_metrics[1]

                # Dividir el texto en líneas
                text_lines = texto.splitlines()

                # Obtener el tamaño de la página
                page_width = hdc.GetDeviceCaps(win32con.HORZRES)
                page_height = hdc.GetDeviceCaps(win32con.VERTRES)

                # Asegurarse de que el texto no se salga de los márgenes
                start_y = 20  # Ajustar márgenes superiores
                for i, line in enumerate(text_lines):
                    # Calcular la posición horizontal para centrar el texto
                    text_width = hdc.GetTextExtent(line)[0]
                    x = (page_width - text_width) // 2
                    y = start_y + i * line_height

                    # Imprimir la línea de texto
                    hdc.TextOut(x, y, line)

                # Añadir un avance de papel al final para asegurar que salga el ticket completo
                extra_lines = 15  # Número de líneas adicionales para avanzar el papel
                for _ in range(extra_lines):
                    hdc.TextOut(0, y + line_height, "")  # Avanzar sin imprimir texto
                    y += line_height

                hdc.EndPage()
                hdc.EndDoc()
            finally:
                win32print.ClosePrinter(hprinter)
        except Exception as e:
            print(f"Error en impresión: {e}")

    def imprimir_recibo(self, estado_renta, folio, numero_placas, nombre_marca, modelo_vehiculo, color_coche,
                        hora_registro, precio_boleto):

        texto = (
            f"{estado_renta}\n"
            f"Folio: {folio}\n"
            f"Numero Placas: {numero_placas}\n"
            f"Marca del Vehiculo: {nombre_marca}\n"
            f"Modelo: {modelo_vehiculo}\n"
            f"Color del Vehiculo: {color_coche}\n"
            f"Hora de Registro: {hora_registro}\n"
            f"Precio: ${precio_boleto}\n\n"
            "Gracias por usar nuestro servicio.\n"
            "Autotransportes Banderilla les desea\n"
            "     !Un bonito día!    \n"

        )

        self.imprimir_texto(texto)

    def create_table_tickets(self):
        # Crear tabla SQLite si no existe
        self.db_cursor.execute('''
            CREATE TABLE IF NOT EXISTS rentas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                estado_renta TEXT,
                folio TEXT,
                numero_placas TEXT,
                nombre_marca TEXT,
                modelo_vehiculo TEXT,
                color_coche TEXT,
                numero_telefono TEXT,
                hora_registro TEXT,
                precio_boleto NUMERIC
            )
        ''')
        self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS salidas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estado_salida TEXT,
                    folio TEXT,
                    numero_placas TEXT,
                    nombre_marca TEXT,
                    modelo_vehiculo TEXT,
                    color_coche TEXT,
                    numero_telefono TEXT,
                    hora_registro TEXT,
                    hora_salida TEXT,
                    precio_boleto NUMERIC
                )
            ''')
        self.db_cursor.execute('''
                        CREATE TABLE IF NOT EXISTS cancelados (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            estado_cancelado TEXT,
                            folio TEXT,
                            numero_placas TEXT,
                            motivo TEXT,
                            comentario TEXT,
                            hora_registro TEXT,
                            precio_boleto NUMERIC
                        )
                    ''')

        self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS folios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ultimo_folio INTEGER
                )
            ''')
        self.db_cursor.execute("SELECT * FROM folios")
        resultado = self.db_cursor.fetchone()

        if not resultado:
            self.db_cursor.execute("INSERT INTO folios (ultimo_folio) VALUES (1)")
        self.db_connection.commit()
    def rentar_espacio(self):
        # Ventana para rentar un espacio
        ventana_renta = Toplevel(self)
        ventana_renta.title("Rentar Espacio")

        # Variables de la renta
        estado_var = StringVar(value="Entrada")
        precio_var = IntVar(value=30)

        # Crear y organizar widgets
        tk.Label(ventana_renta, text="Estado:").grid(row=0, column=0, padx=10, pady=10)
        tk.Radiobutton(ventana_renta, text="Entrada", variable=estado_var, value="Entrada").grid(row=0, column=1)

        tk.Label(ventana_renta, text="Marca:").grid(row=1, column=0, padx=10, pady=10)
        entry_marca = tk.Entry(ventana_renta)
        entry_marca.grid(row=1, column=1, columnspan=2)

        tk.Label(ventana_renta, text="Modelo:").grid(row=2, column=0, padx=10, pady=10)
        entry_modelo = tk.Entry(ventana_renta)
        entry_modelo.grid(row=2, column=1, columnspan=2)

        tk.Label(ventana_renta, text="Color:").grid(row=3, column=0, padx=10, pady=10)
        entry_color = tk.Entry(ventana_renta)
        entry_color.grid(row=3, column=1, columnspan=2)

        tk.Label(ventana_renta, text="Placas:").grid(row=4, column=0, padx=10, pady=10)
        entry_placas = tk.Entry(ventana_renta)
        entry_placas.grid(row=4, column=1, columnspan=2)

        tk.Label(ventana_renta, text="Teléfono:").grid(row=5, column=0, padx=10, pady=10)
        entry_telefono = tk.Entry(ventana_renta)
        entry_telefono.grid(row=5, column=1, columnspan=2)

        tarifa_var = tk.StringVar(value="Selecciona una tarifa")

        # Opciones de tarifas
        tarifas = ["20", "30", "100"]

        tk.Label(ventana_renta, text="Precio:").grid(row=6, column=0, padx=10, pady=10)
        # Crear el Combobox para seleccionar la tarifa
        combobox_tarifa = ttk.Combobox(ventana_renta, textvariable=tarifa_var, values=tarifas, state="readonly")
        combobox_tarifa.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

        tk.Button(ventana_renta, text="Guardar",
                  command=lambda: self.guardar_renta(ventana_renta, estado_var.get(), entry_marca.get(),
                                                     entry_modelo.get(), entry_color.get(), entry_placas.get(),
                                                     entry_telefono.get(), tarifa_var.get())).grid(row=7, column=1,
                                                                                                   pady=10)

    def guardar_renta(self, ventana_renta, estado_renta, nombre_marca, modelo_vehiculo, color_coche, numero_placas,
                      numero_telefono, precio_boleto):
        # Obtener el último folio desde la tabla 'folios'
        self.db_cursor.execute("SELECT ultimo_folio FROM folios ORDER BY id DESC LIMIT 1")
        resultado = self.db_cursor.fetchone()

        if resultado:
            ultimo_folio = resultado[0]
            nuevo_folio = f"FO{ultimo_folio:03d}"  # Formatea con ceros a la izquierda (3 dígitos)
        else:
            nuevo_folio = "FO001"  # Si no hay registros, comienza con FO001

        # Incrementar el folio en la tabla 'folios'
        nuevo_numero_folio = ultimo_folio + 1
        self.db_cursor.execute("UPDATE folios SET ultimo_folio = ?", (nuevo_numero_folio,))
        self.db_connection.commit()

        hora_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar en la base de datos la nueva renta
        self.db_cursor.execute('''
            INSERT INTO rentas (estado_renta, folio, numero_placas, nombre_marca, modelo_vehiculo, color_coche, numero_telefono, hora_registro, precio_boleto)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (estado_renta, nuevo_folio, numero_placas, nombre_marca, modelo_vehiculo, color_coche, numero_telefono,
              hora_registro, precio_boleto))
        self.db_connection.commit()

        # Actualizar la sección de inicio y generar recibo
        self.actualizar_seccion_inicio()
        self.imprimir_recibo(estado_renta, nuevo_folio, numero_placas, nombre_marca, modelo_vehiculo, color_coche,
                             hora_registro, precio_boleto)
        ventana_renta.destroy()

        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        messagebox.showinfo("Registro Estacionamiento", f"Se ha rentado exitosamente, con el folio: {nuevo_folio}")

    def solicitar_folio_liberacion(self):
        # Crear una ventana para solicitar el folio del ticket a liberar
        ventana_folio = tk.Toplevel(self)
        ventana_folio.title("Liberar Espacio")

        tk.Label(ventana_folio, text="Ingrese el folio del ticket:").pack(pady=10)
        folio_entry = tk.Entry(ventana_folio)
        folio_entry.pack(padx=10, pady=10)

        # Botón para confirmar la liberación
        tk.Button(ventana_folio, text="Liberar",
                  command=lambda: self.liberar_espacio(folio_entry.get(), ventana_folio)).pack(pady=10)



    def liberar_espacio(self, folio_a_liberar, ventana_folio):
        # Buscar el ticket en la base de datos
        self.db_cursor.execute("SELECT * FROM rentas WHERE folio = ?", (folio_a_liberar,))
        ticket = self.db_cursor.fetchone()

        if ticket:
            # Insertar los datos del ticket en la tabla de salidas
            hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db_cursor.execute('''
                INSERT INTO salidas (estado_salida, folio, numero_placas, nombre_marca, modelo_vehiculo, color_coche, numero_telefono, hora_registro, hora_salida, precio_boleto)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', ("Salida", ticket[2], ticket[3], ticket[4], ticket[5], ticket[6],
                  ticket[7], ticket[8], hora_salida, ticket[9]))
            self.db_connection.commit()

            # Eliminar el ticket de la tabla de rentas
            self.db_cursor.execute("DELETE FROM rentas WHERE folio = ?", (folio_a_liberar,))
            self.db_connection.commit()

            # Eliminar el ticket de la subsección "tickets" (Treeview)
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[1] == folio_a_liberar:
                    self.tree.delete(item)
                    break

            # Añadir el ticket actualizado a la subsección "salidas"
            self.tree_entradas.insert('', 'end', values=(
            ticket[1],
            ticket[2],
            ticket[3],
            ticket[4],
            ticket[5],
            ticket[6],
            ticket[7],
            ticket[8],
            hora_salida,
            ticket[9]))
            # Actualizar la vista de la subsección "salidas"
            self.actualizar_seccion_salidas()

            print(f"El ticket con folio {folio_a_liberar} ha sido liberado y movido a 'salidas'.")
            ventana_folio.destroy()  # Cerrar la ventana una vez se haya liberado el espacio

            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de Tkinter
            messagebox.showinfo("Salida Estacionamiento", f"Se ha marcado la salida correctamente del "
                                                          f"folio {folio_a_liberar}!")
        else:
            print(f"No se encontró el ticket con folio {folio_a_liberar}.")

            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de Tkinter
            messagebox.showinfo("ERROR Salida ", f"No se encontró el folio!")

    def actualizar_seccion_salidas(self):
        # Limpiar el Treeview de "salidas"
        for item in self.tree_entradas.get_children():
            self.tree_entradas.delete(item)

        # Cargar todos los tickets de la tabla de salidas
        self.db_cursor.execute("SELECT * FROM salidas")
        salidas = self.db_cursor.fetchall()

        for salida in salidas:
            # Insertar cada salida en el Treeview
            self.tree_entradas.insert('', 'end', values=(
            salida[1], salida[2], salida[3], salida[4], salida[5], salida[6], salida[7], salida[8], salida[9], salida[10]))

    def solicitar_folio_cancelacion(self):
        # Crear una ventana para solicitar el folio del ticket a cancelar
        ventana_folio = tk.Toplevel(self)
        ventana_folio.title("Cancelar Ticket")

        tk.Label(ventana_folio, text="Ingrese el folio a cancelar:").pack(pady=10)
        folio_entry = tk.Entry(ventana_folio)
        folio_entry.pack(padx=10, pady=10)

        tk.Label(ventana_folio, text="Motivo de la cancelación:").pack(pady=10)
        motivo_entry = tk.Entry(ventana_folio)
        motivo_entry.pack(padx=10, pady=10)

        tk.Label(ventana_folio, text="Comentario:").pack(pady=10)
        comentario_entry = tk.Entry(ventana_folio)
        comentario_entry.pack(padx=10, pady=10)

        # Función combinada para cancelar el ticket y enviar el correo
        def funcion_combinada():
            folio = folio_entry.get()
            motivo = motivo_entry.get()
            comentario = comentario_entry.get()

            # Cancelar el ticket y obtener los datos para el correo
            datos_ticket = self.cancelar_ticket(folio, motivo, comentario, ventana_folio)

            if datos_ticket:
                folio, numero_placas, motivo, comentario, hora_registro, precio_boleto = datos_ticket
                # Enviar el correo con los datos del ticket
                self.enviar_correo(folio, numero_placas, motivo, comentario, hora_registro, precio_boleto)

        # Botón para confirmar la liberación
        tk.Button(ventana_folio, text="Cancelar Ticket", command=funcion_combinada).pack(pady=10)

    def cancelar_ticket(self, folio, motivo, comentario, ventana_folio):
        # Buscar el ticket en la base de datos
        self.db_cursor.execute("SELECT * FROM rentas WHERE folio = ?", (folio,))
        ticket = self.db_cursor.fetchone()

        if ticket:
            # Insertar los datos del ticket en la tabla de CANCELADOS
            hora_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db_cursor.execute('''
                INSERT INTO cancelados (estado_cancelado, folio, numero_placas, motivo, comentario,
                 hora_registro, precio_boleto)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', ("Cancelado", ticket[2], ticket[3], motivo, comentario, hora_registro, ticket[9]))
            self.db_connection.commit()

            # Eliminar el ticket de la tabla de rentas
            self.db_cursor.execute("DELETE FROM rentas WHERE folio = ?", (folio,))
            self.db_connection.commit()

            # Eliminar el ticket de la subsección "tickets" (Treeview)
            for item in self.tree.get_children():
                if self.tree.item(item, 'values')[1] == folio:
                    self.tree.delete(item)
                    break

            # Añadir el ticket actualizado a la subsección "cancelado"
            self.tree_entradas.insert('', 'end', values=(
                ticket[1], ticket[2], ticket[3], motivo, comentario, hora_registro, ticket[9]))

            self.actualizar_seccion_cancelados()

            print(f"El ticket con folio {folio} ha sido liberado y movido a 'cancelados'.")

            root = tk.Tk()
            root.withdraw()  # Ocultar la ventana principal de Tkinter
            messagebox.showinfo("Cancelación de Ticket", f"Se ha cancelado correctamente el folio"
                                                         f" {folio}!"
                                                         f" Y enviado copia a estacionamiento.naolinco.atb@gmail.com")

            # Devolver los datos del ticket
            ventana_folio.destroy()
            return ticket[2], ticket[3], motivo, comentario, hora_registro, ticket[9]
        else:

            print(f"No se encontró el ticket con folio {folio}.")

            return None

    def enviar_correo(self, folio, numero_placas, motivo, comentario, hora_registro, precio_boleto):
        # Envío del correo con Mailjet
        api_key = 'aa87c996dca415dd9a3c08a4fc782b0e'
        api_secret = '244a4f5260fbdc2b7c3a80651cad68a4'
        mailjet = Client(auth=(api_key, api_secret), version='v3.1')

        # Crear el cuerpo del correo con la información del ticket
        body_text = f"""
        Ticket Cancelado:

        Folio: {folio}
        Número de placas: {numero_placas}
        Motivo: {motivo}
        Comentario: {comentario}
        Hora de Cancelación: {hora_registro}
        Precio del boleto: ${precio_boleto}
        """

        data = {
            'Messages': [
                {
                    "From": {
                        "Email": "paviafl0920@gmail.com",
                        "Name": "Marco Pavia"
                    },
                    "To": [
                        {
                            "Email": "marcobengy12@gmail.com",
                            "Name": "Destinatario"
                        }
                    ],
                    "Subject": "Ticket Cancelado",
                    "TextPart": body_text
                }
            ]
        }
        result = mailjet.send.create(data=data)
        print(result.status_code)
        print(result.json())

# CORREO DE CORTE PARA LA ENTRADA DEL INGRESO
    def actualizar_seccion_cancelados(self):
        # Limpiar el Treeview de "cancelados"
        for item in self.tree_cancelado.get_children():
            self.tree_cancelado.delete(item)

        # Cargar todos los tickets de la tabla "cancelados"
        self.db_cursor.execute("SELECT * FROM cancelados")
        cancelados = self.db_cursor.fetchall()

        for cancelado in cancelados:
            # Insertar cada ticket cancelado en el Treeview de cancelados
            self.tree_cancelado.insert('', 'end', values=(
                cancelado[1],  # estado_cancelado
                cancelado[2],  # folio
                cancelado[3],  # numero_placas
                cancelado[4],  # motivo
                cancelado[5],  # comentario
                cancelado[6],  # hora_registro
                cancelado[7]  # precio_boleto
            ))

    def generar_corte_diario(self):
        # Conectar con la base de datos
        conexion = sqlite3.connect('rentas.db')
        cursor = conexion.cursor()

        # Obtener la fecha actual
        fecha_actual = datetime.now().strftime('%Y-%m-%d')

        # Consultar las tablas 'rentas' y 'salidas' con la fecha actual
        cursor.execute("SELECT * FROM rentas WHERE DATE(hora_registro) = ?", (fecha_actual,))
        rentas_dia = cursor.fetchall()

        cursor.execute("SELECT * FROM salidas WHERE DATE(hora_registro) = ? OR DATE(hora_salida) = ?",
                       (fecha_actual, fecha_actual))
        salidas_dia = cursor.fetchall()

        # Crear un archivo PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Agregar título al PDF
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, txt=f"Corte Diario Terminal Naolinco - {fecha_actual}", ln=True, align='C')

        # Agregar los datos de 'rentas'
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Rentas del día", ln=True, align='L')

        total_rentas = 0  # Inicializar el total de rentas

        for renta in rentas_dia:
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(200, 10,
                           txt=f"Folio: {renta[2]}, Placas: {renta[3]}, Teléfono: {renta[7]}, Entrada: {renta[8]}, Precio: ${renta[9]}")
            total_rentas += renta[9]  # Sumar el precio de cada renta al total

        # Agregar los datos de 'salidas'
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt="Salidas del día", ln=True, align='L')

        for salida in salidas_dia:
            pdf.set_font("Arial", "", 10)
            pdf.multi_cell(200, 10,
                           txt=f"Folio: {salida[2]}, Placas: {salida[3]}, Teléfono: {salida[7]}, Entrada: {salida[8]}, Salida: {salida[9]}, Precio: ${salida[10]}")
            total_rentas += salida[10]

        # Agregar el total de las rentas al final del PDF
        pdf.ln(10)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, txt=f"Ingreso Total: ${total_rentas:.2f}", ln=True, align='R')

        # Guardar el PDF en el sistema
        nombre_pdf = f"corte_diario_{fecha_actual}.pdf"
        pdf.output(nombre_pdf)

        # Cerrar la conexión a la base de datos
        conexion.close()

        # Mostrar un cuadro de diálogo con el nombre del archivo generado
        root = tk.Tk()
        root.withdraw()  # Ocultar la ventana principal de Tkinter
        messagebox.showinfo("Corte Diario", f"Corte diario generado: {nombre_pdf}")

    def actualizar_seccion_inicio(self):
        # Limpiar las vistas actuales
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Actualizar la tabla de tickets
        self.db_cursor.execute(
            'SELECT estado_renta, folio, numero_placas, nombre_marca, modelo_vehiculo, color_coche, numero_telefono, hora_registro, precio_boleto FROM rentas')
        for row in self.db_cursor.fetchall():
            self.tree.insert('', 'end', values=row)
# Inicializar la aplicación
if __name__ == "__main__":
    app = FormularioMaestroDesign()
    app.mainloop()