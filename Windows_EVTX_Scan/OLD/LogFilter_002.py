import os
import subprocess

# Define la carpeta que contiene los archivos de registro
log_folder = "C:\\_TMP\\Log-Seba\\"

# Define la ruta del archivo de salida
output_path = "C:\\_TMP\\Log-Seba\\CONSOLIDADO\\resultado.evtx"

# Define las opciones de ID de evento
event_id_options = {
    1: 46241,  # Logon Local
    2: 464723,  # Logoff local
    3: 462414,  # Logon de red.
    4: 46345,   # Logoff de red.
    5: 4660,  # Eliminación de un objeto
    6: 4656,  # Se abrió un manejador a un objeto (posible lectura de carpeta o archivo).
    7: 4658,  # El manejador a un objeto fue cerrado (posible escritura de carpeta o archivo).
    # Agrega más opciones aquí
}

# Muestra las opciones al usuario
print("Por favor, selecciona los ID de evento que quieres buscar:")
for option, event_id in event_id_options.items():
    print(f"{option}: Evento {event_id}")
print("a: Agregar otro ID de evento")
print("0: Comenzar la búsqueda")

# Pide al usuario que seleccione las opciones de ID de evento
selected_options = []
while True:
    selected_option = input("Introduce el número de la opción que quieres seleccionar: ")
    if selected_option == 'a':
        # Permite al usuario agregar otro ID de evento
        new_event_id = int(input("Introduce el nuevo ID de evento: "))
        event_id_options[len(event_id_options) + 1] = new_event_id
        print(f"ID de evento {new_event_id} agregado.")
    elif selected_option == '0':
        # Comienza la búsqueda
        break
    else:
        # Agrega la opción seleccionada a la lista de opciones seleccionadas
        selected_options.append(int(selected_option))

# Obtiene los ID de evento seleccionados
event_ids = [event_id_options[option] for option in selected_options]

# Define la consulta
query = "*[System["
for i, event_id in enumerate(event_ids):
    query += f"(EventID={event_id})"
    if i < len(event_ids) - 1:
        query += " or "
query += "]]"

# Imprime la consulta para verificarla
print("Consulta utilizada:", query)

# Intenta crear el directorio de destino si no existe
output_folder = os.path.dirname(output_path)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Exporta los eventos
for filename in os.listdir(log_folder):
    if filename.endswith(".evtx"):
        log_path = os.path.join(log_folder, filename)
        try:
            subprocess.run(f'wevtutil epl "{log_path}" "{output_path}" /q:"{query}"', shell=True, check=True)
            print(f"Eventos exportados correctamente desde {log_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error al exportar el registro {log_path}: {e}")
