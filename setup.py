import sys
import os
from cx_Freeze import setup, Executable

# Lista de archivos y directorios a incluir
files = ['imagenes', 'formularios', 'util', 'rentas.db', 'config.py']

# Opción de build_exe
build_exe_options = {
    'include_files': files,
    'packages': ['os', 'win32print', 'win32api', 'win32com'],  # Agrega los paquetes que necesites
}

# Definición del ejecutable
exe = Executable(script="main.py", base="Win32GUI")

# Configuración del setup
setup(
    name="Prueba de Exe",
    version="1.0",
    description="Aplicacion de prueba para estacionamiento",
    author="Marco Pavía",
    options={'build_exe': build_exe_options},
    executables=[exe]
)