import folium

def displayMap(logsFilePath, zoom=15):
    Allpoints = []
    Checkpoints = []

    # Lecture du fichier texte AllPoints.txt
    with open(f"{logsFilePath}/AllPoints.txt", mode='r') as fileAllpoints:
        for line in fileAllpoints:
            row = line.strip().split()
            if len(row) >= 2:
                lat, lon, t, dX, dY = map(float, row)
                Allpoints.append((lat, lon))

    if not Allpoints:
        print("La liste des points est vide.")
        return
    
    # Lecture du fichier texte Checkpoints.txt
    with open(f"{logsFilePath}/Checkpoints.txt", mode='r') as fileCheckpoints:
        for line in fileCheckpoints:
            row = line.strip().split(",")
            if len(row) >= 2:
                lat, lon, t, dX, dY = map(float, row)
                Checkpoints.append((lat, lon))

    if not Checkpoints:
        print("La liste des checkpoints est vide.")
        return

    # Centre initial de la carte sur le premier point
    center_lat, center_lon = Allpoints[0]
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)

    # Ajout des marqueurs pour les checkpoints
    for i, (lat, lon) in enumerate(Checkpoints):
        if i == 0:
            colorMarker = "green"
        elif i == len(Checkpoints) - 1:
            colorMarker = "red"
        else:
            colorMarker = "blue"
        folium.Marker(
            location=[lat, lon],
            popup=f"Checkpoint {i+1}: ({lat:.6f}, {lon:.6f})",
            tooltip=f"Checkpoint {i+1}",
            icon=folium.Icon(color=colorMarker)
        ).add_to(m)

    # Trace une ligne reliant les points
    if len(Allpoints) > 1:
        folium.PolyLine(
            Allpoints,
            color="blue",
            weight=2.5,
            opacity=1
        ).add_to(m)

    # Sauvegarde la carte dans un fichier HTML
    map_file = f"{logsFilePath}/map.html"
    m.save(map_file)
    print(f"La carte a été sauvegardée dans le fichier {map_file}. Ouvrez ce fichier dans votre navigateur pour voir le résultat.")

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de chemin vers les fichiers de logs
    logs_path = "/path/to/logs"
    displayMap(logs_path)
