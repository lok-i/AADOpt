import numpy as np
import math
import sys
from src.patch import cart2sph1,sph2cart1,PatchFunction,GetPatchFields,SurfacePlot


class PatchAntennaArray():
    def __init__(self,n_patches, Freq=14e9,Er=2.5,IdenticalPatches=True,I_W=10.7e-3,I_L=10.47e-3,I_h=3e-3):

        if n_patches <= 0:
            raise Exception("n_patches cannot be <=0")
        self._n_patches = n_patches
        self.element_array = np.zeros((n_patches,8))
        self._freq = Freq
        self._er = Er
        self.element_array[:,3] = 1. #default amplitude is 1
        if IdenticalPatches:
            self.element_array[:,5] = I_W
            self.element_array[:,6] = I_L
            self.element_array[:,7] = I_h
        
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
        print("Calulating Fields ...")
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

        return arrayFactor # the pattern to plot itself


if __name__ == "__main__":
    
    # W,L,h,Er
    AnArr = PatchAntennaArray(n_patches=2,Freq=14e9,Er=2.5,IdenticalPatches=True)

    # for i in range(AnArr._n_patches):
    #     AnArr.set_element_prop(i,A=(i+1))

    print(AnArr.element_array)
    ArrayFactorXFields = AnArr.CalculateFieldSumPatch()
    SurfacePlot(Fields=ArrayFactorXFields)





