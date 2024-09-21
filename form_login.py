import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk


# Función para verificar el login
def verificar_login():
    usuario = entrada_usuario.get()
    contraseña = entrada_contraseña.get()

    if usuario == "admin" and contraseña == "1234":
        messagebox.showinfo("Login exitoso", "¡Bienvenido!")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos")


# Función para cargar una imagen
def cargar_imagen():
    ruta_imagen = filedialog.askopenfilename()
    if ruta_imagen:
        img = Image.open(ruta_imagen)
        img = img.resize((150, 150))
        render = ImageTk.PhotoImage(img)
        etiqueta_imagen.config(image=render)
        etiqueta_imagen.image = render


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Login")
ventana.geometry("400x500")
ventana.configure(bg="#88FFB4")

# Etiquetas y campos de entrada
etiqueta_titulo = tk.Label(ventana, text="Iniciar Sesión", font=("Calisto MT", 24, "bold"), bg="#88FFB4")
etiqueta_titulo.pack(pady=20)

etiqueta_imagen = tk.Label(ventana, bg="#88FFB4")
etiqueta_imagen.pack(pady=10)

etiqueta_usuario = tk.Label(ventana, text="Usuario", bg="#88FFB4")
etiqueta_usuario.pack(pady=5)
entrada_usuario = tk.Entry(ventana)
entrada_usuario.pack(pady=5)

etiqueta_contraseña = tk.Label(ventana, text="Contraseña", bg="#88FFB4")
etiqueta_contraseña.pack(pady=5)
entrada_contraseña = tk.Entry(ventana, show="*")
entrada_contraseña.pack(pady=5)

# Botón de login
boton_login = tk.Button(ventana, text="Login", command=verificar_login)
boton_login.pack(pady=20)

# Ejecutar la ventana
ventana.mainloop()
