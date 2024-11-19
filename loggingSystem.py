from roblib import *
import csv
from map import displayMap
from datetime import datetime
import os

def convert_xy2latlon(x,y,lat0,lon0):
    # Rayon moyen de la Terre en mètres
    R = 6378137  

    # Conversion de lat0 en radians
    lat0_rad = np.radians(lat0)

    # Calcul des décalages en latitude et longitude
    dlat = y / R
    dlon = x / (R * cos(lat0_rad))

    # Conversion des décalages en degrés
    lat = lat0 + dlat*180/pi
    lon = lon0 + dlon*180/pi

    return lat, lon

class LoggingSystem():
    def __init__(self, fullTrajectory, lat0, lon0):
        # Créer un fichier CSV pour écrire les données
        self.architecture = self.fileArchitecture()
        self.csvFileCheckpoints = open(f"{self.architecture}/Checkpoints.csv", mode='w', newline='')
        self.csvWriterCheckpoints = csv.writer(self.csvFileCheckpoints, delimiter=',')
        self.csvWriterCheckpoints.writerow(['lat', 'lon', 't', 'dX', 'dY'])

        self.csvFileAllPoints = open(f"{self.architecture}/AllPoints.csv", mode='w', newline='')
        self.csvWriterAllPoints = csv.writer(self.csvFileAllPoints, delimiter=',')
        self.csvWriterAllPoints.writerow(['lat', 'lon', 't', 'dX', 'dY'])

        self.fullTrajectory = fullTrajectory
        self.lat0, self.lon0 = lat0, lon0

        

    def writeDesiredTrajectory(self, createmap = True):
        points = self.fullTrajectory.points
        self.latlogged, self.lonlogged = [], []
        for k in range(len(points)):
            x,y,t,dx,dy = points[k]
            lat,lon = convert_xy2latlon(x,y,self.lat0,self.lon0)
            self.csvWriterAllPoints.writerow([lat,lon,t,dx,dy])
        
        self.csvFileAllPoints.close()
        for k in range(len(self.fullTrajectory.Lpolynome)):
            polyK = self.fullTrajectory.Lpolynome[k]
            x,y,t,dx,dy = polyK.X[0],polyK.Y[0],polyK.t[0],polyK.dotX[0],polyK.dotY[0]
            lat,lon = convert_xy2latlon(x,y,self.lat0,self.lon0)
            self.csvWriterCheckpoints.writerow([lat,lon,t,dx,dy])

        # I also add the last line which was not taken into account as I only took the first line :
        x,y,t,dx,dy = polyK.X[-1],polyK.Y[-1],polyK.t[-1],polyK.dotX[-1],polyK.dotY[-1]
        lat,lon = convert_xy2latlon(x,y,self.lat0,self.lon0)
        self.csvWriterCheckpoints.writerow([lat,lon,t,dx,dy])
        self.csvFileCheckpoints.close()

    def fileArchitecture(self):
        now = datetime.now()
        today_date = now.date()
        current_time = str(now.time())

        # Chemin absolu du fichier script actuel
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)

        folder_path = f"{script_dir}/Missions/{today_date}/{current_time[:8]}"
        print(f"folder_path : {folder_path}")
        os.makedirs(folder_path, exist_ok=True)
        return folder_path
            
# Exemple d'utilisation
if __name__ == "__main__":
    x, y = 10, 50   # Coordonnées en mètres
    lat0, lon0 = 48.198805, -3.013673  # Référence : Paris (latitude et longitude)
    
    lat, lon = convert_xy2latlon(x,y,lat0,lon0)
    points = [[lat0, lon0],
              [lat,   lon]]
    displayMap(points)
    print(f"Latitude : {lat}, Longitude : {lon}")