from roblib import *
from polynomeOrder5 import PolynomeOrder5

class FullTrajectory():

    def __init__(self,L):
        self.Lpolynome = []
        for k in range(len(L)-1):
            tk, xk, yk, dxk, dyk = L[k]
            tk1, xk1, yk1, dxk1, dyk1 = L[k+1]
            polynomeK = PolynomeOrder5(tk, xk, yk, dxk, dyk,tk1, xk1, yk1, dxk1, dyk1)
            self.Lpolynome.append(polynomeK)
            
            self.createPoints()

    def displayPositionXY(self, drawArrows = False):
        print(f"len(self.Lpolynome) : {len(self.Lpolynome)}")
        for k in range(len(self.Lpolynome)):
            Y, X, dotY, dotX = self.Lpolynome[k].X, self.Lpolynome[k].Y, self.Lpolynome[k].dotX, self.Lpolynome[k].dotY
            
            figure("Position Over Time")
            if k==0:
                plot(X, Y, label="Trajectory")
                plot([X[0], X[-1]], [Y[0], Y[-1]], 'ro', label="Waypoints") 
            else :
                plot(X, Y)
                plot([X[0], X[-1]], [Y[0], Y[-1]], 'ro')  
            if drawArrows:
                for k in range(0, len(X), len(X) // 20):  # Dessine une flèche tous les ~5%
                    quiver(X[k], Y[k], dotX[k], dotY[k], color="green", width=0.001)
        legend()
        axis("equal")


    def createPoints(self):
        self.points = []
        
        for polynome in self.Lpolynome:
            X, Y, t, dX, dY = polynome.X, polynome.Y, polynome.t, polynome.dotX, polynome.dotY
            for k in range(len(X)):
                self.points.append([X[k],Y[k],t[k],dX[k], dY[k]])



    def displaySpeedNOverTime(self):
        figure("Speed of N over time")
        for k in range(len(self.Lpolynome)):
            t, dotN = self.Lpolynome[k].t, self.Lpolynome[k].dotY
            if k == 0 : plot(t, dotN, label="dotN(t)")
            else : plot(t, dotN)
        legend()

    def displaySpeedEOverTime(self):
        figure("Speed of E over time")
        for k in range(len(self.Lpolynome)):
            t, dotE = self.Lpolynome[k].t, self.Lpolynome[k].dotX
            if k == 0 :
                plot(t, dotE, label="dotY(t)")
            else :
                plot(t, dotE)
        legend()

    def display(self, L):
        if "position" in L:
            self.displayPositionXY()
        if "positionArrows" in L:
            self.displayPositionXY(True)
        if "speedN" in L:
            self.displaySpeedNOverTime()
        if "speedE" in L:
            self.displaySpeedEOverTime()