import numpy as np
# from src.directivity import *
# from src.patch import *

from directivity import *
# from patch import *


class Antenna():
    def __init__(self,vector):
        self._vector = np.array(vector)
  
    def update_vector(self,vector):
        self._vector = np.array(vector)
  
    def get_azimulth_and_elevation(self):
        
        v1 = self._vector
        v2 = np.array([0,0,0])
        v = v1 - v2

        a = np.degrees(np.arctan(v[0]/v[1])) # angle with positive y axis
        e = np.degrees(np.arctan(v[2]/v[1])) # 90 - angle with z azis, i.e. angle with the xy plane or commonly called as H-Plane

        # print('azimuth = '+str(a)+', elevation = '+str(e))
        return a,e

    def get_gain(self):
        azimuth,elevation = self.get_azimulth_and_elevation()
        Directivity,Gain = CalcDirectivityAt(10, SinPowerPattern,g_theta=elevation,g_phi=azimuth)
        print(Directivity,Gain)
        return Gain


if __name__ == "__main__":
    a = Antenna([0,0,1])
    a.update_vector([0.5,0.5,0.38])
    a.get_azimulth_and_elevation()
    a.get_gain()