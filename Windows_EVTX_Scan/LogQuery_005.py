import os
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view

def clear_screen():
    # Función para limpiar la pantalla según el sistema operativo
    os.system('cls' if os.name == 'nt' else 'clear')

def search_events(log_directory, search_terms, output_path):
    # Muestra un mensaje en la consola
    print("Iniciando el script...")

    # Abre el archivo de salida
    print(f"Abriendo el archivo de salida {output_path}...")
    with open(output_path, 'w') as output_file:
        print("Archivo de salida abierto correctamente.")

        # Inicializa un contador de eventos
        event_count = 0

        # Itera sobre los archivos .evtx en el directorio
        for filename in os.listdir(log_directory):
            if filename.endswith(".evtx"):
                log_path = os.path.join(log_directory, filename)

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
                        print(f"Procesando evento {event_count} en {filename}...")

                        # Busca el valor en el evento
                        if any(term in record_xml for term in search_terms):
                            # Escribe la línea de separación con el número del evento en el archivo de salida
                            output_file.write(f"------------------- Evento {event_count} ({filename}) -------------------\n")

                            # Escribe la información del evento en el archivo de salida si se encuentra el valor
                            output_file.write(record_xml)
                            print(f"Valor encontrado en el evento {event_count}. Información del evento escrita en el archivo de salida.")

    # Muestra un mensaje en la consola
    print("La búsqueda ha finalizado.")

# Directorio que contiene los archivos de registro
log_directory = "C:\\_TMP\\Log-Seba"

# Ruta del archivo de salida para eventos buscados
output_searched_path = "C:\\_TMP\\Log-Seba\\Resultado_Eventos_Buscados.txt"

# Lista de términos de búsqueda
search_terms = []

# Menú de acciones
while True:
    clear_screen()
    print("\nMenú de Acciones:")
    print("1 - Agregar término a buscar.")
    print("0 - Iniciar Búsqueda.")
    print("\nTérminos Agregados:", " | ".join(search_terms))

    choice = input("Seleccione una opción (1, 0): ")

    if choice == '1':
        # Agregar término a buscar
        search_term = input("Ingrese el término que desea buscar: ")
        search_terms.append(search_term)
    elif choice == '0':
        # Iniciar la búsqueda
        search_events(log_directory, search_terms, output_searched_path)
        break
    else:
        print("Opción no válida. Por favor, ingrese 1 o 0.")
