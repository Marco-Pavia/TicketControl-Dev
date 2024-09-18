import sys
import os

from cx_Freeze import setup, Executable

files = ['imagenes', 'formularios', 'rentas.db', 'config.py']
exe=Executable(script="main.py", base="Win32GUI")
setup(
    name="Prueba de Exe",
    version="1.0",
    description="Aplicacion de prueba para estacionamiento",
    author="Marco Pavía",
    options={'build_exe': {'include_files':files}},
    executables=[exe]

)