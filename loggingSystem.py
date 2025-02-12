from roblib import *
from map import displayMap
from datetime import datetime
import os

def convert_xy2latlon(x, y, lat0, lon0):
    R = 6378137  # Rayon moyen de la Terre en mètres
    lat0_rad = np.radians(lat0)
    dlat = x / R
    dlon = y / (R * np.cos(lat0_rad))
    lat = lat0 + dlat * 180 / np.pi
    lon = lon0 + dlon * 180 / np.pi
    return lat, lon

class LoggingSystem():
    def __init__(self, fullTrajectory, lat0, lon0,doXYCSTheta=True):
        self.doXYCSTheta = doXYCSTheta
        self.architecture = self.fileArchitecture()
        self.fileCheckpoints = open(f"{self.architecture}/Checkpoints.txt", mode='w')
        self.fileAllPoints = open(f"{self.architecture}/AllPoints.txt", mode='w')
        self.fileAllPointsXY = open(f"{self.architecture}/AllPointsXY.txt", mode='w')
        self.fileAllPointsXyNpyPath = f"{self.architecture}/AllPointsXY.npy"
        self.fileAllPointsXyCSThetaNpyPath = f"{self.architecture}/AllPointsXYCSTheta.npy"
        self.fullTrajectory = fullTrajectory
        self.lat0, self.lon0 = lat0, lon0

    def writeDesiredTrajectory(self, createmap=True, txy=True):
        points = self.fullTrajectory.points
        for k in range(len(points)):
            x, y, t, dx, dy = points[k]
            lat, lon = convert_xy2latlon(x, y, self.lat0, self.lon0)
            self.fileAllPoints.write(f"{lat},{lon},{t},{dx},{dy}\n")
            self.fileAllPointsXY.write(f"{x},{y}\n")
            
        self.fileAllPoints.close()
        self.fileAllPointsXY.close()

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
        print(np.array(points)[:,:2])
        np.save(self.fileAllPointsXyNpyPath, np.array(points)[:,:2])

        if self.doXYCSTheta == True: # from pathFollowing2DPython
            loaded_array = np.load(self.fileAllPointsXyNpyPath)
            print(f"Doing XYCSTheta from file at location : {loaded_array}")
            LX = loaded_array[:,0]
            LY = loaded_array[:,1]

            Lx, Ly, Lc, Ls, Ltheta = [0],[0],[0],[0],[0]
            for k in range(1,len(LX)-1):
                xk_1, xk = LX[k-1], LX[k] 
                yk_1, yk = LY[k-1], LY[k] 

                sk_1 = Ls[-1]
                sk = sk_1 + np.sqrt((yk_1-yk)**2+(xk_1-xk)**2)

                thetak_1 = Ltheta[-1]
                thetak = np.arctan2(yk-yk_1, xk-xk_1)

                ck = (thetak-thetak_1)/sk

                Lx.append(xk)
                Ly.append(yk)
                Lc.append(ck)
                Ls.append(sk)
                Ltheta.append(thetak)
                

            array = np.column_stack((Lx,Ly,Lc,Ls,Ltheta))
            print(array)
            print(f"Doing XYCSTheta from file at location : {self.fileAllPointsXyCSThetaNpyPath}")
            np.save(self.fileAllPointsXyCSThetaNpyPath, array)


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
