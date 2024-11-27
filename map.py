import folium
import csv

def displayMap(logsFilePath, zoom=15):
    Allpoints = []
    Checkpoints = []

    # Lecture du fichier CSV AllPoints
    with open(f"{logsFilePath}/AllPoints.csv", mode='r') as csvfileAllpoints:
        csvReaderAllpoints = csv.reader(csvfileAllpoints, delimiter=',')
        header = next(csvReaderAllpoints, None)  # Ignore la ligne d'en-tête

        for row in csvReaderAllpoints:
            if len(row) >= 2:
                # Convertir chaque ligne en un tuple (lat, lon, t, dX, dY) et l'ajouter à la liste
                lat, lon, t, dX, dY = map(float, row)
                Allpoints.append((lat, lon))

    if not Allpoints:
        print("La liste des points est vide.")
        return
    
    # Lecture du fichier CSV Checkpoints
    with open(f"{logsFilePath}/Checkpoints.csv", mode='r') as csvfileCheckpoints:
        csvReaderCheckpoints = csv.reader(csvfileCheckpoints, delimiter=',')
        header = next(csvReaderCheckpoints, None)  # Ignore la ligne d'en-tête

        for row in csvReaderCheckpoints:
            if len(row) >= 2:
                # Convertir chaque ligne en un tuple (lat, lon, t, dX, dY) et l'ajouter à la liste
                lat, lon, t, dX, dY = map(float, row)
                Checkpoints.append((lat, lon))

    if not Allpoints:
        print("La liste des points est vide.")
        return
    

    # Centre initial de la carte sur le premier point
    center_lat, center_lon = Allpoints[0]
    m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)

    # Ajoute un marqueur pour chaque point
    for i, (lat, lon) in enumerate(Checkpoints):
        print(i)
        if i == 0 : 
            colorMarker = "green"
        elif i ==len(Checkpoints)-1 : colorMarker = "red"
        else : colorMarker = "blue"
        folium.Marker(
            location=[lat, lon],
            popup=f"Point {i+1}: ({lat:.6f}, {lon:.6f})",
            tooltip=f"Point {i+1}",
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
    # Liste d'exemple : des points à Paris
    points = [
        [48.8566, 2.3522],  # Paris
        [48.8584, 2.2945],  # Tour Eiffel
        [48.8738, 2.2950],  # Arc de Triomphe
        [48.852968, 2.349902]  # Cathédrale Notre-Dame
    ]

    # Affiche la carte avec les points et les lignes
    displayMap(points)


