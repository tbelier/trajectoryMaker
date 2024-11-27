from roblib import *
from map import displayMap
from datetime import datetime
import os

def convert_xy2latlon(x, y, lat0, lon0):
    R = 6378137  # Rayon moyen de la Terre en mètres
    lat0_rad = np.radians(lat0)
    dlat = y / R
    dlon = x / (R * np.cos(lat0_rad))
    lat = lat0 + dlat * 180 / np.pi
    lon = lon0 + dlon * 180 / np.pi
    return lat, lon

class LoggingSystem():
    def __init__(self, fullTrajectory, lat0, lon0):
        self.architecture = self.fileArchitecture()
        self.fileCheckpoints = open(f"{self.architecture}/Checkpoints.txt", mode='w')
        self.fileAllPoints = open(f"{self.architecture}/AllPoints.txt", mode='w')
        self.fullTrajectory = fullTrajectory
        self.lat0, self.lon0 = lat0, lon0

    def writeDesiredTrajectory(self, createmap=True):
        points = self.fullTrajectory.points
        for k in range(len(points)):
            x, y, t, dx, dy = points[k]
            lat, lon = convert_xy2latlon(x, y, self.lat0, self.lon0)
            self.fileAllPoints.write(f"{lat},{lon},{t},{dx},{dy}\n")
        
        self.fileAllPoints.close()

        for k in range(len(self.fullTrajectory.Lpolynome)):
            polyK = self.fullTrajectory.Lpolynome[k]
            x, y, t, dx, dy = polyK.X[0], polyK.Y[0], polyK.t[0], polyK.dotX[0], polyK.dotY[0]
            lat, lon = convert_xy2latlon(x, y, self.lat0, self.lon0)
            self.fileCheckpoints.write(f"{lat},{lon},{t},{dx},{dy}\n")

        # Ajout de la dernière ligne non prise en compte
        x, y, t, dx, dy = polyK.X[-1], polyK.Y[-1], polyK.t[-1], polyK.dotX[-1], polyK.dotY[-1]
        lat, lon = convert_xy2latlon(x, y, self.lat0, self.lon0)
        self.fileCheckpoints.write(f"{lat},{lon},{t},{dx},{dy}\n")

        self.fileCheckpoints.close()

    def fileArchitecture(self):
        now = datetime.now()
        today_date = now.date()
        current_time = str(now.time())
        script_path = os.path.abspath(__file__)
        script_dir = os.path.dirname(script_path)
        folder_path = f"{script_dir}/Missions/{today_date}/{current_time[:8]}"
        print(f"folder_path : {folder_path}")
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

# Exemple d'utilisation
if __name__ == "__main__":
    x, y = 10, 50   # Coordonnées en mètres
    lat0, lon0 = 48.198805, -3.013673  # Référence : latitude et longitude
    lat, lon = convert_xy2latlon(x, y, lat0, lon0)
    points = [[lat0, lon0], [lat, lon]]
    displayMap(points)
    print(f"Latitude : {lat}, Longitude : {lon}")
