from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view

# Define la ruta del archivo de registro
log_path = "C:\\_TMP\\Log-Seba\\Archive-Security-2024-01-02-11-42-47-445.evtx"

# Define el valor que quieres buscar
search_value = "gmacchi"

# Define la ruta del archivo de salida
output_path = "C:\\_TMP\\Log-Seba\\resultado.txt"

# Muestra un mensaje en la consola
print("Iniciando el script...")

# Abre el archivo de salida
print(f"Abriendo el archivo de salida {output_path}...")
with open(output_path, 'w') as output_file:
    print("Archivo de salida abierto correctamente.")

    # Inicializa un contador de eventos
    event_count = 0

    # Abre el archivo de registro
    print(f"Abriendo el archivo de registro {log_path}...")
    with Evtx(log_path) as log:
        print("Archivo de registro abierto correctamente.")

        # Lee y procesa los eventos
        print("Leyendo eventos...")
        for record_xml, record in evtx_file_xml_view(log.get_file_header()):
            # Incrementa el contador de eventos
            event_count += 1

            # Muestra un mensaje en la consola
            print(f"Procesando evento {event_count}...")

            # Busca el valor en el evento
            if search_value in record_xml:
                # Escribe la información del evento en el archivo de salida si se encuentra el valor
                output_file.write(record_xml)
                print(f"Valor encontrado en el evento {event_count}. Información del evento escrita en el archivo de salida.")

# Muestra un mensaje en la consola
print("El script ha finalizado.")
