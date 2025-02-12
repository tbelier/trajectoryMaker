import numpy as np
import os

script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
# Charger le tableau depuis le fichier .npy
loaded_array = np.load(f"/home/tbelier/Documents/GIT/trajectoryMaker/Missions/2025-02-12/10:53:44/AllPointsXYCSTheta.npy")

print(loaded_array)
