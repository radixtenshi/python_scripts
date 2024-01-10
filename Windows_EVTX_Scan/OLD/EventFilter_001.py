import os
import win32evtlog

# Define la carpeta que contiene los archivos de registro
log_folder = "C:\\_TMP\\Log-Seba\\"

# Define la ruta del archivo de salida
output_path = "C:\\_TMP\\Log-Seba\\resultado.evtx"

# Define los ID de evento que quieres buscar. En este ejemplo no pregunta el ID de forma interactiva.
event_ids = [1234, 5678]  # Reemplaza estos números con los ID de evento que estás buscando

# Define la consulta
query = "*[System["
for i, event_id in enumerate(event_ids):
    query += f"(EventID={event_id})"
    if i < len(event_ids) - 1:
        query += " or "
query += "]]"

# Exporta los eventos
for filename in os.listdir(log_folder):
    if filename.endswith(".evtx"):
        log_path = os.path.join(log_folder, filename)
        win32evtlog.EvtExportLog(None, log_path, query, output_path, win32evtlog.EvtExportLogChannelPath)
