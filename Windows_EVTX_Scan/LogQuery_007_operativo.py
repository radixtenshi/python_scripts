import os
from Evtx.Evtx import Evtx
from Evtx.Views import evtx_file_xml_view

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def formatear_nombre_archivo(texto):
    # Reemplazar "\" por "_" para evitar problemas en el nombre del archivo de salida
    texto_formateado = texto.replace("\\", "_")
    return texto_formateado


def search_events(log_directory, search_terms, output_searched_path):

    # Crea una cadena con los términos de búsqueda separados por guiones bajos
    search_terms_str = '_'.join(formatear_nombre_archivo(term) for term in search_terms)
    print(search_terms_str)
    # Define el nombre del archivo de destino con los términos de búsqueda
    output_filename = "Resultado_de_" + search_terms_str + ".txt"

    
    # Combina la ruta del directorio con el nombre del archivo
    output_searched_path = os.path.join(log_directory, output_filename)
    #print(output_searched_path)


    clear_screen()
    print("\nAcciones:")
    print("Terminos a buscar:", ", ".join(search_terms))
    print("Archivos de origen:", log_directory)
    print("Archivo de destino:", output_searched_path)
    print("----------------------------------------------")
    print("1 - Volver al menu.")
    print("0 - Iniciar Búsqueda.")
    choice = input("Seleccione una opción (1, 0): ")

    if choice == '1':
        return search_terms, output_searched_path
    else:
        print("\nIniciando la búsqueda...")

        event_count = 0

        with open(output_searched_path, 'w') as output_file:
            for filename in os.listdir(log_directory):
                if filename.endswith(".evtx"):
                    log_path = os.path.join(log_directory, filename)

                    with Evtx(log_path) as log:
                        clear_screen()
                        print("Archivo de registro abierto correctamente.")
                        input("Presione Enter para iniciar la busqueda...")
                        # Lee y procesa los eventos
                        print("Leyendo eventos...")
                        for record_xml, record in evtx_file_xml_view(log.get_file_header()):
                            # Incrementa el contador de eventos
                            event_count += 1

                            # Muestra un mensaje en la consola
                            print(f"Procesando evento {event_count} en {filename}...")

                            # Busca el valor en el evento
                            if any(term in record_xml for term in search_terms):
                                output_file.write(f"------------------- Evento {event_count} ({filename}) -------------------\n")
                                output_file.write(record_xml)

def main_menu(search_terms, output_searched_path):
    log_directory = "C:\\_TMP\\Log-Seba"




    while True:
        clear_screen()
        print("\nMenú de Acciones:")
        print("1 - Agregar término a buscar.")
        print("0 - Iniciar Búsqueda.")
        print("\nTérminos Agregados:", " | ".join(search_terms))

        choice = input("Seleccione una opción (1, 0): ")

        if choice == '1':
            search_term = input("Ingrese el término que desea buscar: ")
            search_terms.append(search_term)
        elif choice == '0':
            search_events(log_directory, search_terms, output_searched_path)
            #input("Presione Enter para volver al menú...")
            #search_terms = []
            continue
        else:
            print("Opción no válida. Por favor, ingrese 1 o 0.")

if __name__ == "__main__":
    search_terms = []
    output_searched_path = [] 
    main_menu(search_terms, output_searched_path)
