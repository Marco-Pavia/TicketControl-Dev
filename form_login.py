import tkinter as tk
from tkinter import ttk, messagebox
import util.generic as utl
import util.util_imagenes as util_img
from PIL import UnidentifiedImageError
import sqlite3

class FormLoginDesigner:
    def verificar(self):
        usuario = self.usuario.get()
        contraseña = self.password.get()

        conn = sqlite3.connect('rentas.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE name =? AND password=?", (usuario, contraseña))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            print("Login exitoso")
            self.login_exitoso = True  # Marcar que el login fue exitoso
            self.ventana.destroy()  # Cerrar la ventana de login
        else:
            messagebox.showerror(message="Verifique su usuario y contraseña", title="Error")
            self.login_exitoso = False

    def es_login_exitoso(self):
        return self.login_exitoso

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title('Inicio de sesión')
        self.ventana.geometry('800x500')
        self.ventana.config(bg='#fcfcfc')
        self.ventana.resizable(width=0, height=0)

        self.login_exitoso = False  # Inicialmente no se ha realizado el login
        utl.centrar_ventana(self.ventana, 800, 500)

        try:
            self.logo = util_img.leer_imagen("imagen.png", (560, 136))
        except FileNotFoundError:
            print("Error: Imagen de perfil no encontrada.")
            self.logo = None
        except UnidentifiedImageError:
            print("Error al cargar la imagen, formato no soportado")
            self.logo = None

        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10, bg='#3a7ff6')
        frame_logo.pack(side="left", expand=tk.YES, fill=tk.BOTH)

        if self.logo is None:
            label_logo = tk.Label(frame_logo, text="Logo no disponible", bg='#3a7ff6', font=("Arial", 20))
            label_logo.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            label = tk.Label(frame_logo, text="Imagen de logo no encontrada", bg='#3a7ff6', font=("Arial", 20))
            label.place(x=0, y=0, relwidth=1, relheight=1)

        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form.pack(side="right", expand=tk.YES, fill=tk.BOTH)

        frame_form_top = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='black')
        frame_form_top.pack(side="top", fill=tk.X)
        title = tk.Label(frame_form_top, text="Inicio de sesión", font=('Times', 30), fg="#666a88", bg='#fcfcfc', pady=50)
        title.pack(expand=tk.YES, fill=tk.BOTH)

        frame_form_fill = tk.Frame(frame_form, height=50, bd=0, relief=tk.SOLID, bg='#fcfcfc')
        frame_form_fill.pack(side="bottom", expand=tk.YES, fill=tk.BOTH)

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_usuario.pack(fill=tk.X, padx=20, pady=5)
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.usuario.pack(fill=tk.X, padx=20, pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 14), fg="#666a88", bg='#fcfcfc', anchor="w")
        etiqueta_password.pack(fill=tk.X, padx=20, pady=5)
        self.password = ttk.Entry(frame_form_fill, font=('Times', 14), show="*")
        self.password.pack(fill=tk.X, padx=20, pady=10)

        inicio = tk.Button(frame_form_fill, text="Iniciar sesión", font=('Times', 15), bg='#3a7ff6', bd=0, fg="#fff", command=self.verificar)
        inicio.pack(fill=tk.X, padx=20, pady=20)
        inicio.bind("<Return>", (lambda event: self.verificar()))

        self.ventana.mainloop()

if __name__ == "__main__":
    app = FormLoginDesigner()
