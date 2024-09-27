from formularios.form_login import FormLoginDesigner
from formularios.form_maestro_design import FormularioMaestroDesign

def main():
    # Ejecutar el formulario de login
    login = FormLoginDesigner()
    login.ventana.mainloop()  # Muestra la ventana de login

    # Solo si el login es exitoso, se ejecuta FormularioMaestroDesign
    if login.es_login_exitoso():
        maestro = FormularioMaestroDesign()  # Inicia el formulario maestro
        maestro.mainloop()  # Ciclo principal de la aplicación principal

if __name__ == "__main__":
    main()