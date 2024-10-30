import MODULOTP

def main():
    try:
        MODULOTP.cargarUsuarios()  # Carga los usuarios desde el archivo
        MODULOTP.cargarMenu()      # Carga el menú desde el archivo

        while True:
            print("\n--- Menú Principal ---")
            print("1. Iniciar sesión")
            print("2. Registrarse")
            print("3. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                usuario = MODULOTP.login()  # Iniciar sesión
                if usuario == MODULOTP.ADMIN_USUARIO:
                    MODULOTP.verHistorial(usuario)  # Función del módulo para admin
                elif usuario in MODULOTP.usuarios:
                    MODULOTP.gestionarPedidos(usuario)  # Función del módulo para usuarios
                else:
                    print("Credenciales incorrectas. Intente de nuevo.")
            elif opcion == "2":
                MODULOTP.registrarUsuario()  # Registrar un nuevo usuario
                print("Registro exitoso. Por favor, inicie sesión.")
            elif opcion == "3":
                print("Saliendo del sistema...")
                break  # Salir del bucle y finalizar el programa
            else:
                print("Opción no válida, intente de nuevo.")

    except FileNotFoundError as fnf_error:
        print(f"Error: Archivo no encontrado: {fnf_error}. Asegúrese de que todos los archivos requeridos están disponibles.")
    except ValueError as ve:
        print(f"Error de valor: {ve}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()


