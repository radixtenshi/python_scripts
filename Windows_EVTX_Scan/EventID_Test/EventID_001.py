import os
from Evtx.Evtx import Evtx
from xml.etree import ElementTree as ET

# Función de limpieza de pantalla.
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
# Función que busca eventos.
def buscar_eventos(source, event_id, subtipo):
    output_directory = os.path.join(source, "output")
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(source):
        if filename.endswith(".evtx"):
            filepath = os.path.join(source, filename)
            output_filename = f"Events_{event_id}_Type_{subtipo}.txt"
            output_filepath = os.path.join(output_directory, output_filename)

            with open(output_filepath, "w", encoding="utf-8") as output_file:
                output_file.write(f"Event Log: {filename}\n\n")

                with Evtx(filepath) as log:
                    for record in log.records():
                        xml_data = record.xml()
                        root = ET.fromstring(xml_data)
                        
                        event_id_element = root.find(".//EventID")
                        if event_id_element is not None and int(event_id_element.text) == event_id:
                            subtype_element = root.find(f".//Data[@Name='LogonType'][.='{subtipo}']")
                            if subtype_element is not None:
                                output_file.write(xml_data)
                                output_file.write("\n\n")

# Función Menú
def mostrar_menu():
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
        print("Seleccione el sub-tipo:")
        print("2 - Logon interactivo")
        print("3 - Logon de red")
        print("5 - Service")
        print("7 - Desbloqueo de estación de trabajo")
        print("10 - Remote Interactive (remote desktop)")
        subtipo = int(input("Ingrese el número de sub-tipo: "))
    elif opcion_evento == 2:
        event_id = 4647
        subtipo = 0  # No hay subtipos para el evento 4647
    else:
        print("Opción no válida.")
        return

    buscar_eventos(source, event_id, subtipo)
    print("Búsqueda completada. Los resultados se han guardado en archivos de texto.")

if __name__ == "__main__":
    main()
