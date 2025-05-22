import numpy as np

class FK:
    def __init__(self):
        self.x = np.zeros((4, 1)) 
        self.P = np.eye(4)
        self.dt = 0.1
        self.Q = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [1, 0, 0, 1]]) * 0.5
        
        self.H = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0]])

        self.R = np.eye(2) * 1.0
        self.I = np.eye(4)


    def kalman_predict(self, vel, acc):
        vx, vy = vel[0, 0], vel[1, 0]
        ax, ay = acc[0, 0], acc[1, 0]

        A = np.array([[1, 0, self.dt, 0],
                      [0, 1, 0, self.dt],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

        B = np.array([[0.5 * self.dt**2, 0],
                      [0, 0.5 * self.dt**2],
                      [self.dt, 0],
                      [0, self.dt]])

        u = np.array([[ax], [ay]])

        self.x = A @ self.x + B @ u

        self.x[2, 0] = vx
        self.x[3, 0] = vy
        self.P = A @ self.P @ A.T + self.Q


    def kalman_update(self, location):
        z = location
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        self.P = (self.I - K @ self.H) @ self.P


    @property
    def get_position(self):
        return self.x[:2]