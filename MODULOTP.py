import random

# Diccionario que almacena los usuarios registrados y sus contraseñas
usuarios = {}
# Historial de mozos y admin
historialMozos = {}
historialAdmin = {}
# Diccionario para almacenar comisiones de cada mozo
comisionesMozos = {}
# Inicializa el diccionario para las comidas vendidas
comidasVendidas = {}
# Menú de comida inicializado como vacío
menu = {}
# Capacidad de los sectores (2 sectores con 5 mesas cada uno)
sectores = {
    'interior': 5,
    'exterior': 5
}

# Archivos de datos (rutas relativas)
archivoUsuarios = "C:/Users/Usuario/OneDrive/Documentos/GitHub/PROGRA-1/usuarios.txt"
archivoRegistros = "C:/Users/Usuario/OneDrive/Documentos/GitHub/PROGRA-1/registros.txt"
archivoMenu = "C:/Users/Usuario/OneDrive/Documentos/GitHub/PROGRA-1/comidas.txt"
archivoComisiones = "C:/Users/Usuario/OneDrive/Documentos/GitHub/PROGRA-1/comisiones.txt"
archivoMesasOcupadas = "C:/Users/Usuario/OneDrive/Documentos/GitHub/PROGRA-1/mesasocupadas.txt"
archivoSalidaComida =  "C:/Users/Usuario/OneDrive/Documentos/GitHub/PROGRA-1/salidacomida.txt"

# Definir al administrador
ADMIN_USUARIO = "ADMIN"
ADMIN_CONTRASEÑA = "12345"

def cargarUsuarios():
    '''Cargar los usuarios desde el archivo al iniciar el programa.'''
    global usuarios
    try:
        with open(archivoUsuarios, "r") as file:
            for linea in file:
                usuario, contraseña = linea.strip().split(",")
                usuarios[usuario] = contraseña
        print("Usuarios cargados exitosamente.")
    except FileNotFoundError:
        print("No se encontraron usuarios guardados.")

def guardarUsuario(usuario, contraseña):
    '''Guardar un nuevo usuario en el archivo.'''
    try:
        with open(archivoUsuarios, "a") as file:
            file.write(f"{usuario},{contraseña}\\n")
    except Exception as e:
        print(f"Error al guardar el usuario: {e}")

def cargarMenu():
    '''Cargar el menú desde el archivo al iniciar el programa.'''
    global menu
    try:
        with open(archivoMenu, "r") as file:
            for linea in file:
                if " - $" in linea:
                    comida, precio = linea.strip().split(" - $")
                    menu[comida] = int(precio)
        if menu:
            print("Menu cargado exitosamente:", menu)
    except FileNotFoundError:
        print("No se encontró el archivo del menú.")

def mostrarMenu():
    '''Mostrar el menú de comidas.'''
    for comida, precio in menu.items():
        print(f"{comida} - ${precio}")

def registrarUsuario():
    """Registrar un nuevo usuario."""
    try:
        print("Registro de nuevo usuario.")
        usuario = input("Ingrese su nombre de usuario: ")
        if usuario in usuarios:
            print("Este usuario ya está registrado.")
            return False
        contraseña = input("Ingrese su contraseña: ")
        usuarios[usuario] = contraseña
        guardarUsuario(usuario, contraseña)  
        historialMozos[usuario] = []  
        print(f"Usuario {usuario} registrado exitosamente.")
        return usuario
    except Exception as e:
        print(f"Ocurrió un error al registrar el usuario: {e}")

def login():
    """Iniciar sesión con un usuario existente."""
    try:
        print("Por favor, inicie sesión.")
        usuario = input("Usuario: ").strip()
        contraseña = input("Contraseña: ").strip()
 
        if usuario == ADMIN_USUARIO and contraseña == ADMIN_CONTRASEÑA:
            print(f"Bienvenido, {ADMIN_USUARIO}.")
            return ADMIN_USUARIO  # Usar ADMIN_USUARIO para consistencia
        elif usuario in usuarios and usuarios[usuario] == contraseña:
            print(f"Bienvenido {usuario}.")
            if usuario not in historialMozos:
                historialMozos[usuario] = []  
            return usuario
        else:
            print("Usuario o contraseña incorrectos.")
            return login()  # Recursividad para volver a intentar el login
    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return login()  # Recursividad en caso de error

def guardarRegistro(usuario, registro):
    """Guardar el registro de un pedido en el archivo."""
    try:
        with open(archivoRegistros, "a") as file:
            file.write(f"{usuario},{registro['sector']},{registro['comida']},{registro['precio']},{registro['comision']},{registro['calificacion']}\n")
    except Exception as e:
        print(f"Error al guardar el registro: {e}")
 
def cargarRegistros():
    """Cargar los registros de pedidos desde el archivo."""
    global historialMozos, historialAdmin
    try:
        with open(archivoRegistros, "r") as file:
            for linea in file:
                usuario, sector, comida, precio, comision, calificacion = linea.strip().split(",")
                registro = {
                    'sector': sector,
                    'comida': comida,
                    'precio': int(precio),
                    'comision': float(comision),
                    'calificacion': int(calificacion)
                }
                if usuario not in historialMozos:
                    historialMozos[usuario] = []
                historialMozos[usuario].append(registro)
                historialAdmin[usuario] = historialMozos[usuario]
    except FileNotFoundError:
        print(f"No se encontraron registros previos.")
    except Exception as e:
        print(f"Error al cargar registros: {e}")
        
def obtenerSector():
    """Seleccionar el sector para el cliente."""
    try:
        sector = int(input("Ingrese 1 para sector interior, 2 para exterior: "))
        if sector == 1:
            if sectores['interior'] > 0:
                sectores['interior'] -= 1  # Se ocupa una mesa
                return 'interior'
            elif sectores['exterior'] > 0:
                print("Sector interior lleno. Asignando al sector exterior.")
                sectores['exterior'] -= 1  # Se ocupa una mesa
                return 'exterior'
            else:
                print("Todos los sectores están llenos.")
                return None
        elif sector == 2:
            if sectores['exterior'] > 0:
                sectores['exterior'] -= 1  # Se ocupa una mesa
                return 'exterior'
            elif sectores['interior'] > 0:
                print("Sector exterior lleno. Asignando al sector interior.")
                sectores['interior'] -= 1  # Se ocupa una mesa
                return 'interior'
            else:
                print("Todos los sectores están llenos.")
                return None
        else:
            print("Opción inválida.")
            return obtenerSector()  # Recursividad en caso de opción inválida
    except ValueError:
        print("Entrada inválida. Por favor, ingrese un número válido.")
        return obtenerSector()  # Recursividad en caso de error
 
def seleccionarComida():
    """Seleccionar la comida del menú."""
    try:
        if not menu:
            print("El menú no está cargado. Verifica el archivo de menú.")
            return None, 0
 
        print("Elija su comida:")
        for comida, precio in menu.items():
            print(f"{comida}: ${precio}")
        comida = input("Ingrese el nombre de la comida: ")
        if comida in menu:
            return comida, menu[comida]
        else:
            print("Comida no disponible. Vuelva a intentarlo.")
            return seleccionarComida()  # Recursividad para volver a intentar
    except Exception as e:
        print(f"Error al seleccionar comida: {e}")
        return seleccionarComida()  # Recursividad en caso de error

# Diccionario para contar las ventas de cada comida
comidas_vendidas = {}

def registrarPedido(usuario):
    """Registrar el pedido de un cliente."""
    try:
        sector = obtenerSector()
        if sector is None:
            print("No se puede asignar un sector. Cliente rechazado.")
            return

        comida, precio = seleccionarComida()
        if comida is None:
            print("No se pudo seleccionar una comida. Pedido cancelado.")
            return
        
        # Contar la comida vendida
        if comida in comidas_vendidas:
            comidas_vendidas[comida] += 1
        else:
            comidas_vendidas[comida] = 1

        # Guardar en el archivo 'salidacomidas'
        with open("salidacomidas.txt", "a") as archivo:
            for item, cantidad in comidas_vendidas.items():
                archivo.write(f"{item}: {cantidad} vendidos\n")

        # Calcular y registrar comisión, calificación, y guardar registro
        comision = calcularComision(precio)
        calificacion = random.randint(1, 5)
        registro = {
            'sector': sector,
            'comida': comida,
            'precio': precio,
            'comision': comision,
            'calificacion': calificacion
        }
        historialMozos[usuario].append(registro)
        guardarRegistro(usuario, registro)
        
        print(f"Pedido registrado para {usuario}. Comida: {comida}, Precio: ${precio}, Comisión: ${comision:.2f}, Calificación: {calificacion}")
    except Exception as e:
        print(f"Error al registrar pedido: {e}")

def calcularComision(monto):
    """Calcular la comisión del mozo basada en el monto."""
    try:
        return (monto * 5) / 100
    except Exception as e:
        print(f"Error al calcular la comisión: {e}")
 
def finalizarJornada():
    """Finalizar la jornada laboral, vaciar las mesas y guardar el total de comisiones."""
    try:
        # Reiniciar la capacidad de los sectores
        global sectores, mesas_ocupadas
        sectores = {'interior': 5, 'exterior': 5}
        mesas_ocupadas = {'interior': 0, 'exterior': 0}

        # Calcular las comisiones totales y guardarlas en el archivo 'comisiones'
        with open("comisiones.txt", "w") as archivo:
            for mozo, registros in historialMozos.items():
                total_comision = sum(registro['comision'] for registro in registros)
                archivo.write(f"Mozo: {mozo}, Comisión total: ${total_comision:.2f}\n")

        actualizarMesasOcupadas()  # Actualiza el estado de las mesas
        print("La jornada ha terminado. Las mesas han sido vaciadas y las comisiones guardadas.")
    except Exception as e:
        print(f"Error al finalizar la jornada: {e}")

def verHistorial(usuario):
    """Ver el historial de pedidos. El admin ve todos los registros, los mozos solo los suyos."""
    try:
        if usuario == ADMIN_USUARIO:  # Cambio a ADMIN_USUARIO para consistencia
            print("Historial de todos los mozos:")
            for mozo, registros in historialAdmin.items():
                print(f"Mozo: {mozo}")
                for registro in registros:
                    print(registro)
        else:
            if usuario not in historialMozos:
                print(f"No hay historial para el usuario {usuario}.")
            else:
                print(f"Historial de {usuario}:")
                for registro in historialMozos[usuario]:
                    print(registro)
    except Exception as e:
        print(f"Error al ver el historial: {e}")

def menuPrincipal():
    """Menú principal del programa."""
    while True:
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")
 
        if opcion == "1":
            usuario = login()
            if usuario:
                gestionarPedidos(usuario)
        elif opcion == "2":
            registrarUsuario()
        elif opcion == "3":
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida.")
            menuPrincipal()
 
def gestionarPedidos(usuario):
    """Gestión de pedidos para el mozo o administrador."""
    while True:
        print("1. Registrar pedido")
        print("2. Ver historial de pedidos")
        print("3. Finalizar jornada")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrarPedido(usuario)
        elif opcion == "2":
            verHistorial(usuario)
        elif opcion == "3":
            finalizarJornada()  # Asegúrate de que esta opción se esté eligiendo
        elif opcion == "4":
            break
        else:
            print("Opción no válida.")

def guardarComidasVendidas():
    """Guardar la cantidad de comidas vendidas en un archivo."""
    try:
        print("Comidas vendidas antes de guardar:", comidasVendidas)  # Verifica el contenido
        with open("salidacomidas.txt", "w") as file:
            for comida, cantidad in comidasVendidas.items():
                file.write(f"{comida}: {cantidad}\n")
        print("Cantidad de comidas vendidas guardada exitosamente en 'salidacomidas.txt'.")
    except Exception as e:
        print(f"Error al guardar las comidas vendidas: {e}")

# Variables para el control de mesas en cada sector
mesas_ocupadas = {'interior': 0, 'exterior': 0}
mesas_totales = {'interior': 5, 'exterior': 5}  # Suponiendo 5 mesas en cada sector

# Función para actualizar el archivo de mesas ocupadas
def actualizarMesasOcupadas():
    try:
        with open("mesasocupadas.txt", "w") as archivo:
            archivo.write(f"Interior - Ocupadas: {mesas_ocupadas['interior']}, Desocupadas: {mesas_totales['interior'] - mesas_ocupadas['interior']}\n")
            archivo.write(f"Exterior - Ocupadas: {mesas_ocupadas['exterior']}, Desocupadas: {mesas_totales['exterior'] - mesas_ocupadas['exterior']}\n")
    except Exception as e:
        print(f"Error al actualizar el archivo mesasocupadas: {e}")

def registrarPedido(usuario):
    """Registrar el pedido de un cliente."""
    try:
        sector = obtenerSector()
        if sector is None:
            print("No se puede asignar un sector. Cliente rechazado.")
            return

        # Asignar la mesa al sector
        if not asignarMesa(sector):
            print("No se pudo asignar una mesa. Pedido cancelado.")
            return

        comida, precio = seleccionarComida()
        if comida is None:
            print("No se pudo seleccionar una comida. Pedido cancelado.")
            return
        
        # Contar la comida vendida
        if comida in comidas_vendidas:
            comidas_vendidas[comida] += 1
        else:
            comidas_vendidas[comida] = 1

        # Guardar en el archivo 'salidacomidas'
        with open("salidacomidas.txt", "a") as archivo:
            for item, cantidad in comidas_vendidas.items():
                archivo.write(f"{item}: {cantidad} vendidos\n")

        # Calcular y registrar comisión, calificación, y guardar registro
        comision = calcularComision(precio)
        calificacion = random.randint(1, 5)
        registro = {
            'sector': sector,
            'comida': comida,
            'precio': precio,
            'comision': comision,
            'calificacion': calificacion
        }
        historialMozos[usuario].append(registro)
        guardarRegistro(usuario, registro)
        
        print(f"Pedido registrado para {usuario}. Comida: {comida}, Precio: ${precio}, Comisión: ${comision:.2f}, Calificación: {calificacion}")
    except Exception as e:
        print(f"Error al registrar pedido: {e}")

# Asignar mesa debe llamar a actualizarMesasOcupadas automáticamente
def asignarMesa(sector):
    """Asigna una mesa en el sector solicitado y actualiza el archivo."""
    if sector == 'interior' and mesas_ocupadas['interior'] < mesas_totales['interior']:
        mesas_ocupadas['interior'] += 1
    elif sector == 'exterior' and mesas_ocupadas['exterior'] < mesas_totales['exterior']:
        mesas_ocupadas['exterior'] += 1
    else:
        print(f"No hay mesas disponibles en el sector {sector}.")
        return False

    actualizarMesasOcupadas()  # Asegúrate de que se llama aquí
    return True

# Función para desocupar todas las mesas al finalizar la jornada
def finalizarJornadaMesas():
    """Vacía todas las mesas y actualiza el archivo al finalizar la jornada."""
    global mesas_ocupadas
    mesas_ocupadas = {'interior': 0, 'exterior': 0}
    actualizarMesasOcupadas()  # Actualiza el archivo mostrando todas las mesas desocupadas
    print("La jornada ha terminado. Todas las mesas han sido desocupadas.")

def guardarComisionesFinales():
    """Guarda las comisiones totales de cada mozo al finalizar la jornada en el archivo 'comisiones.txt'."""
    try:
        with open("comisiones.txt", "w") as archivo:
            archivo.write("Comisiones Totales por Mozo\n")
            archivo.write("-" * 30 + "\n")
            for mozo, registros in historialMozos.items():
                total_comisiones = sum(registro['comision'] for registro in registros)
                archivo.write(f"{mozo}: ${total_comisiones:.2f}\n")
        print("Comisiones finales guardadas en 'comisiones.txt'.")
    except Exception as e:
        print(f"Error al guardar comisiones finales: {e}")

def cerrarJornada():
    """Cierra la jornada y guarda las comisiones finales."""
    guardarComisionesFinales()
    # Otras operaciones para cerrar la jornada
    print("Jornada cerrada.")