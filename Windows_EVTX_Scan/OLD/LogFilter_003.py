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

# Intenta crear el directorio de destino si no existe
output_folder = os.path.dirname(output_path)
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Construye la consulta
query = "*[System["
for i, event_id in enumerate(event_ids):
    query += f"(EventID={event_id})"
    if i < len(event_ids) - 1:
        query += " or "
query += "]]"

# Guarda la consulta en un archivo temporal
query_file_path = "C:\\_TMP\\Log-Seba\\CONSOLIDADO\\consulta.xml"
with open(query_file_path, 'w') as query_file:
    query_file.write(query)

# Crea un script de PowerShell para exportar los eventos
ps_script = f'''
$consulta = Get-Content "{query_file_path}" | Out-String
Get-ChildItem "{log_folder}" -Filter "*.evtx" | ForEach-Object {{
    wevtutil epl Security "$_" "{output_path}" /uni:false /q:$consulta
}}
'''

# Guarda el script de PowerShell en un archivo temporal
ps_script_path = "C:\\_TMP\\Log-Seba\\CONSOLIDADO\\export.ps1"
with open(ps_script_path, 'w') as ps_script_file:
    ps_script_file.write(ps_script)

# Ejecuta el script de PowerShell
subprocess.run(['powershell', '-File', ps_script_path], shell=True, check=True)

# Elimina los archivos temporales
os.remove(query_file_path)
os.remove(ps_script_path)
