import numpy as np
import math
from src.directivity import *
from src.patch import *

# from directivity import *
# from patch import *


class LineAntenna():
    def __init__(self,vector):
        if isinstance(vector,np.ndarray):
            self._vector = vector
        else:
            self._vector = np.array(vector)
  
    def update_vector(self,vector):
        if isinstance(vector,np.ndarray):
            self._vector = vector
        else:
            self._vector = np.array(vector)
              
    def get_azimulth_and_elevation(self):
        
        v1 = self._vector
        '''
        v2 = np.array([0,0,0])
        v = v1 - v2

        a = np.degrees(np.arctan(v[0]/v[1])) # angle with positive y axis
        e = np.degrees(np.arctan(v[2]/v[1])) # 90 - angle with z azis, i.e. angle with the xy plane or commonly called as H-Plane
        '''
        r, theta, phi = cart2sph1(self._vector[0], self._vector[1], self._vector[2])

        theta = np.degrees(theta) # elevation
        phi = np.degrees(phi) # azimuth

        # print('r = ',r,'azimuth = '+str(phi)+', elevation = '+str(theta))
        return phi,theta

    def get_gain(self):
        azimuth,elevation = self.get_azimulth_and_elevation()
        Directivity,Gain = CalcDirectivityAt(10, SinPowerPattern,g_theta=elevation,g_phi=azimuth)
        print(Directivity,Gain)
        return Gain


class PatchAntenna():
    def __init__(self,efficiency,frequency_of_operation):
        self._eff = efficiency
        self._freq = frequency_of_operation
        self.W = 0.0
        self.L = 0.0
        self.h = 0.0
        self.Er = 0.0
    def update_parameters(self,new_params):
        self.W = new_params[0]
        self.L = new_params[1]
        self.h = new_params[2]
        self.Er = new_params[3]

    def calculate_max_gain(self):

        Gain_max, Th_max,Phi_max = CalcDirectivity(self._eff, PatchFunction,self._freq, 
                                                   self.W, self.L, self.h, self.Er)
        return Gain_max,Th_max,Phi_max

    def plot_radiation_field(self):
        fields = PatchEHPlanePlot(self._freq, self.W, self.L, self.h, self.Er)
        SurfacePlot(fields, self._freq, self.W, self.L, self.h, self.Er)



if __name__ == "__main__":
    
    a = LineAntenna([0,0,1])
    a.update_vector([1.0,1.0,1.0])
    a.get_azimulth_and_elevation()
    a.get_gain()

    # W,L,h,Er
    p = PatchAntenna(efficiency=90,frequency_of_operation= 14e9)
    new_params = [10.7e-3,10.47e-3,3e-3,2.5]

    p.update_parameters(new_params)
    print(p.calculate_max_gain())
    p.plot_radiation_field()