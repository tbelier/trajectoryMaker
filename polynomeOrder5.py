from roblib import *

# Génère les coefficients d'un polynôme d'ordre 5
def coef_polynoms_order5(t0, t1, x0, x1, dx0, dx1, ddx0, ddx1): 
    A = np.array([
        [t0**5, t0**4, t0**3, t0**2, t0, 1],
        [t1**5, t1**4, t1**3, t1**2, t1, 1],
        [5*t0**4, 4*t0**3, 3*t0**2, 2*t0, 1, 0],
        [5*t1**4, 4*t1**3, 3*t1**2, 2*t1, 1, 0],
        [20*t0**3, 12*t0**2, 6*t0, 2, 0, 0],
        [20*t1**3, 12*t1**2, 6*t1, 2, 0, 0],
    ])
    B = np.array([x0, x1, dx0, dx1, ddx0, ddx1])
    return np.linalg.solve(A, B)

class PolynomeOrder5(): 

    def __init__(self, t0, x0, y0, dx0, dy0, t1, x1, y1, dx1, dy1):
        self.t0, self.x0, self.y0, self.dx0, self.dy0 = t0, x0, y0, dx0, dy0
        self.t1, self.x1, self.y1, self.dx1, self.dy1 = t1, x1, y1, dx1, dy1

        # Calcul les coefficients des polynômes axe par axe
        self.ax, self.bx, self.cx, self.dx, self.ex, self.fx = coef_polynoms_order5(
            self.t0, self.t1, self.x0, self.x1, self.dx0, self.dx1, 0, 0
        )
        self.ay, self.by, self.cy, self.dy, self.ey, self.fy = coef_polynoms_order5(
            self.t0, self.t1, self.y0, self.y1, self.dy0, self.dy1, 0, 0
        )

        self.X, self.Y, self.dotX, self.dotY = self.propateOverTime()

    def propateOverTime(self, n=100):
        t = np.linspace(self.t0, self.t1, n)
        self.t = t

        # Polynôme pour X
        X = self.ax * t**5+ self.bx * t**4+ self.cx * t**3+ self.dx * t**2+ self.ex * t+ self.fx
        dotX = 5 * self.ax * t**4+ 4 * self.bx * t**3+ 3 * self.cx * t**2+ 2 * self.dx * t+ self.ex

        # Polynôme pour Y
        Y = self.ay * t**5+ self.by * t**4+ self.cy * t**3+ self.dy * t**2+ self.ey * t+ self.fy
        dotY = 5 * self.ay * t**4+ 4 * self.by * t**3+ 3 * self.cy * t**2+ 2 * self.dy * t+ self.ey

        return X, Y, dotX, dotY

    def displayPositionXY(self, drawArrows=False):
        X, Y, dotX, dotY = self.X, self.Y, self.dotX, self.dotY
        
        figure("Position Over Time")
        plot(X, Y, label="Trajectory")
        plot([X[0], X[-1]], [Y[0], Y[-1]], 'ro', label="Waypoints") 
        
        if drawArrows:
            for k in range(0, len(X), len(X) // 20):  # Dessine une flèche tous les ~5%
                quiver(X[k], Y[k], dotX[k], dotY[k], color="green", width=0.001)
        legend()

    def displaySpeedOverTime(self):
        figure("Speed of X and Y over time")
        plot(self.t, self.dotX, label="dotX(t)")
        plot(self.t, self.dotY, label="dotY(t)")
        legend()

    def display(self, L):
        if "position" in L:
            self.displayPositionXY()
        if "positionArrows" in L:
            self.displayPositionXY(True)
        if "speed" in L:
            self.displaySpeedOverTime()