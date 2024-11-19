from roblib import *
from fullTrajectory import FullTrajectory
from loggingSystem import LoggingSystem
from map import displayMap
import os

def Snake(): 
    lat0, lon0 = 48.19910780663803, -3.0163647006417404
    #     tk, xk, yk, dxk, dyk
    X = [[ 0,  0,  0,   0,  0],
        [90,   90,  0,   1,  0],
        [110, 100,  10,   0,  1],
        [130,  90,  20,  -1,  0],
        [220,  10,  20,  -1, -0],
        [240,  0,  30,   0,  1],
        [260,  10,  40,   1,  0],
        [350,  90,  40,   1,  0],
        [370,  100, 50,   0,  1],
        [390,  90,  60,  -1,  0],
        [480,  0,  60,  -1,  0]]
    return lat0,lon0,X

def DockingFaceFromSW(): 
    lat0, lon0 = 48.199, -3.0157
    #     tk, xk, yk, dxk, dyk
    X = [[ 0,  -50,  -20,   0,  0],
         [90,   40,  -20,   1,  0],
         [110, 50,  -10,   0,  1],
         [130,  40,  0,  -1,  0],
         [220,  0,  0,  0,  0]]
    return lat0,lon0,X

def DockingFaceFromSE(): 
    lat0, lon0 = 48.199, -3.0157
    #     tk, xk, yk, dxk, dyk
    X = [[ 0,  50,  -20,   0,  0],
         [90,   -40,  -20,   -1,  0],
         [110, -50,  -10,   0,  1],
         [130,  -40,  0,  1,  0],
         [220,  0,  0,  0,  0]]
    return lat0,lon0,X

def DockingFaceFromNW():
    lat0, lon0 = 48.199, -3.0157
    #     tk, xk, yk, dxk, dyk
    X = [[ 0,  -50,  20,   0,  0],
         [90,   40,  20,   1,  0],
         [110, 50,  10,   0,  -1],
         [130,  40,  0,  -1,  0],
         [220,  0,  0,  0,  0]]
    return lat0,lon0,X

def DockingFaceFromNE():
    lat0, lon0 = 48.199, -3.0157
    #     tk, xk, yk, dxk, dyk
    X = [[ 0,  50,  20,   0,  0],
         [90,   -40,  20,   -1,  0],
         [110, -50,  10,   0,  -1],
         [130,  -40,  0,  1,  0],
         [220,  0,  0,  0,  0]]
    return lat0,lon0,X

def DockingFaceFromNE_withAngle(delta_x, delta_y, delta_theta):
    lat0, lon0 = 48.199, -3.0157
    #     tk, xk, yk, dxk, dyk
    Nxy = np.sqrt(delta_x**2+delta_y**2)
    X = [[110, 20+delta_x,  0+delta_y,   cos(delta_theta+arctan2(delta_y,delta_x)+np.pi),  sin(delta_theta+arctan2(delta_y,delta_x)+np.pi)],
         [130,  20,  0,  -1,  0],
         [220,  0,  0,  0,  0]]
    return lat0,lon0,X


if __name__ == "__main__":

    # Chemin absolu du fichier script actuel
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    
    # Choix de la mission à réaliser
    lat0, lon0, X  = DockingFaceFromNE_withAngle(7,7,np.pi/4)

    fullTraj = FullTrajectory(X)
    fullTraj.display(["positionArrows", "speedX", "speedY"])
    
    logsFile = LoggingSystem(fullTraj, lat0, lon0)
    logsFile.writeDesiredTrajectory()

    displayMap(logsFile.architecture)
    show()
