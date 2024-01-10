import os
from Evtx.Evtx import Evtx
from xml.etree import ElementTree as ET

# Función de limpieza de pantalla.
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 2)  # Añadimos líneas en blanco para mejorar la visibilidad después de la limpieza


# Función que busca eventos.
def buscar_eventos(source, event_id, subtipo):
    output_directory = os.path.join(source, "output")
    os.makedirs(output_directory, exist_ok=True)

    total_eventos_revisados = 0

    for filename in os.listdir(source):
        if filename.endswith(".evtx"):
            filepath = os.path.join(source, filename)
            output_filename = f"Events_{event_id}_Type_{subtipo}.txt"
            output_filepath = os.path.join(output_directory, output_filename)


            print("\nIniciando la búsqueda...")
            event_count = 0



            with open(output_filepath, "w", encoding="utf-8") as output_file:
                output_file.write(f"Event Log: {filename}\n\n")

                with Evtx(filepath) as log:
                    clear_screen()
                    print("Archivo de registro abierto correctamente.")
                    input("Presione Enter para iniciar la busqueda...")
                    
                    print(f"Iniciando búsqueda en {filename}")
                    for i, record in enumerate(log.records(), start=1):
                        total_eventos_revisados += 1
                        xml_data = record.xml()
                        root = ET.fromstring(xml_data)
                        
                        print("leyendo evento N:", total_eventos_revisados, "En:", {filename} )


                        event_id_element = root.find(".//EventID")
                        if event_id_element is not None and int(event_id_element.text) == event_id:
                            subtype_element = root.find(f".//Data[@Name='LogonType'][.='{subtipo}']")
                            if subtype_element is not None:
                                output_file.write(xml_data)
                                output_file.write("\n\n")

                    print(f"Se revisaron {i} eventos en {filename}")

    print(f"\nBúsqueda completada. Total de eventos revisados: {total_eventos_revisados}")

# Función Menú
def mostrar_menu():
    clear_screen()
    print("Seleccione el evento que desea buscar:")
    print("1 - EventID 4624 - LogOn")
    print("2 - EventID 4647 - LogOff")

# Función Principal
def main():
    source = input("Ingrese el directorio de origen de los archivos .evtx: ")
    mostrar_menu()
    opcion_evento = int(input("Ingrese el número de evento: "))

    if opcion_evento == 1:
        event_id = 4624
        clear_screen()
        print("Seleccione el sub-tipo:")
        print("2 - Logon interactivo")
        print("3 - Logon de red")
        print("5 - Service")
        print("7 - Desbloqueo de estación de trabajo")
        print("10 - Remote Interactive (remote desktop)")
        subtipo = int(input("Ingrese el número de sub-tipo: "))
        print(f"\nBúsqueda iniciada para EventID {event_id} - Subtipo {subtipo}")
    elif opcion_evento == 2:
        event_id = 4647
        clear_screen()
        subtipo = 0  # No hay subtipos para el evento 4647
        print(f"\nBúsqueda iniciada para EventID {event_id}")
    else:
        print("Opción no válida.")
        return

    buscar_eventos(source, event_id, subtipo)

if __name__ == "__main__":
    main()
