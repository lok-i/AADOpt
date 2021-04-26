import numpy as np
import math
import sys
from src.patch import cart2sph1,sph2cart1,PatchFunction,GetPatchFields,SurfacePlot
from src.directivity import CalcDirectivity

class PatchAntennaArray():
    def __init__(self,n_patches,param_range,Freq=14e9,Er=2.5):

        if n_patches <= 0:
            raise Exception("n_patches cannot be <=0")
        self._n_patches = n_patches
        self.element_array = np.zeros((n_patches,8))
        self._freq = Freq
        self._er = Er
        self.c_radiation_pattern = []
        
        param_to_array_index = {key:index for (key,index) in zip(param_range.keys(),np.arange(8)) }
        # min_limit = {key:0 for key in param_range.keys() }
        # max_limit = {key:0 for key in param_range.keys() }
        
        params_to_opt_min = []
        params_to_opt_max = []
        self.params_to_opt_indices = []
        for key in param_range.keys():
            if 'equal_to' in param_range[key].keys():
                self.element_array[:,param_to_array_index[key]] = param_range[key]['equal_to']
            else:
                params_to_opt_min.append(param_range[key]['greater_than'])
                params_to_opt_max.append(param_range[key]['lesser_than'])
                self.params_to_opt_indices.append(param_to_array_index[key])

        self.params_to_opt_range = [[_min,_max] for (_min,_max) in zip(params_to_opt_min,params_to_opt_max)]*n_patches
        self.opt_param_vector = np.zeros(len(self.params_to_opt_range))

    def update_array_params(self,opt_param_vector):

        nth_element = 0
        for i in range(self._n_patches):
            for j in self.params_to_opt_indices:
                self.element_array[i,j] = opt_param_vector[nth_element]
                nth_element+=1


    
    def set_element_prop(self,element_id,pos=[0.,0.,0.],A=1,beta=0.0):
        # to add geometric properties aswell later on
        self.element_array[element_id][0] = pos[0]
        self.element_array[element_id][1] = pos[1]
        self.element_array[element_id][2] = pos[2]
        self.element_array[element_id][3] = A
        self.element_array[element_id][4] = beta

    def CalculateRelativePhase(self,element, Lambda, theta, phi):
        """
        Incident wave treated as plane wave. Phase at element is referred to phase of plane wave at origin.
        Element = xPos, yPos, zPos, ElementAmplitude, ElementPhaseWeight
        theta & phi in radians
        See Eqn 3.1 @ https://theses.lib.vt.edu/theses/available/etd-04262000-15330030/unrestricted/ch3.pdf
        """
        phaseConstant = (2 * math.pi / Lambda)

        xVector = element[0] * math.sin(theta) * math.cos(phi)
        yVector = element[1] * math.sin(theta) * math.sin(phi)
        zVector = element[2] * math.cos(theta)

        phaseOfIncidentWaveAtElement = phaseConstant * (xVector + yVector + zVector)

        return phaseOfIncidentWaveAtElement

    def CalculateFieldSumPatch(self):
        """
        Summation of field contributions from each patch element in array, at frequency freq for theta 0°-95°, phi 0°-360°.
        Element = xPos, yPos, zPos, ElementAmplitude, ElementPhaseWeight
        Returns arrayFactor[theta, phi, elementSum]
        """
        
        arrayFactor = np.ones((360, 95))

        Lambda = 3e8 / self._freq
        # print("Calulating Fields ...")
        for theta in range(95):
            for phi in range(360):                                                                                                      # For all theta/phi positions
                elementSum = 1e-9 + 0j

                xff, yff, zff = sph2cart1(999, math.radians(theta), math.radians(phi))                                                  # Find point in far field

                for element in self.element_array:
                    xlocal = xff - element[0]
                    ylocal = yff - element[1]                                                                                           # Calculate local position in cartesian
                    zlocal = zff - element[2]
                    r, thetaLocal, phiLocal = cart2sph1(xlocal, ylocal, zlocal)                                                         # Convert local position to spherical

                    patchFunction = PatchFunction(math.degrees(thetaLocal), math.degrees(phiLocal),                                     # Patch element pattern for local theta, phi
                                    self._freq, element[5], element[6], element[7], self._er)            

                    if patchFunction != 0:                                                                                              # Sum each elements contribution
                        relativePhase = self.CalculateRelativePhase(element,Lambda, math.radians(theta), math.radians(phi))                 # Find relative phase for current element
                        elementSum += element[3] * patchFunction * math.e ** ((relativePhase + element[4]) * 1j)                        # Element contribution = Amp * e^j(Phase + Phase Weight)

                arrayFactor[phi][theta] = elementSum.real
        
        self.c_radiation_pattern = arrayFactor
    
    def RadPatternFunction(self,thetaInDeg, phiInDeg):
        if len(self.c_radiation_pattern) == 0:
            raise Exception("Radiation Pattern hasn't been calculated. call CalculateFieldSumPatch() ")
        else:
            return self.c_radiation_pattern[phiInDeg][thetaInDeg]

    def get_gain(self):
        Gain,_,_ = CalcDirectivity(Efficiency=100,
                    RadPatternFunction=self.RadPatternFunction,
                    theta_range=[0,95],
                    to_print=False
                    )
        return Gain

    def plot_radiation_pattern(self):

        if len(self.c_radiation_pattern) == 0:
            raise Exception("Radiation Pattern hasn't been calculated. call CalculateFieldSumPatch() ")
        else:
            SurfacePlot(Fields=self.c_radiation_pattern)


if __name__ == "__main__":
    
    # W,L,h,Er

    param_opt_range = {'x':{'greater_than':0,'lesser_than':10},
                    'y':{'greater_than':-5,'lesser_than':0},
                    'z':{'equal_to':0},
                    'A':{'greater_than':0.,'lesser_than':5.},
                    'beta':{'equal_to':0.},
                    'W':{'equal_to':10.7e-3},
                    'L':{'equal_to':10.47e-3},
                    'h':{'equal_to':3e-3},}

    PatchArray = PatchAntennaArray(n_patches=2,
                                Freq=14e9,
                                Er=2.5,
                                param_range=param_opt_range)
    print('Opt_values_range:\n',len(PatchArray.params_to_opt_range))
    # print('Max_opt_values:',PatchArray.params_to_opt_range[:][1])

    print('initial_elements:\n',PatchArray.element_array)
    update_to = [0.,0.,1.,0.,0.,1.]
    PatchArray.update_array_params(update_to)
    print('updates_elements:\n',PatchArray.element_array)


    # for i in range(PatchArray._n_patches):
    #     PatchArray.set_element_prop(i,A=(i+1))

    PatchArray.CalculateFieldSumPatch()
    print(PatchArray.get_gain())
    PatchArray.plot_radiation_pattern()




