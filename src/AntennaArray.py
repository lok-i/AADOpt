import numpy as np
import math
from src.patch import cart2sph1,sph2cart1,PatchFunction,GetPatchFields,SurfacePlot


class ArrayAntenna():

    def ArrayFactor(self,ElementArray, Freq):
        """
        Summation of field contributions from each element in array, at frequency freq at theta 0°-95°, phi 0°-360°.
        Element = xPos, yPos, zPos, ElementAmplitude, ElementPhaseWeight
        Returns arrayFactor[theta, phi, elementSum]
        """

        arrayFactor = np.ones((360, 95))

        Lambda = 3e8 / Freq

        for theta in range(95):
            for phi in range(360):                                                                                                      # For all theta/phi positions
                elementSum = 1e-9 + 0j

                for element in ElementArray:                                                                                            # Summation of each elements contribution at theta/phi position.
                    relativePhase = CalculateRelativePhase(element, Lambda, math.radians(theta), math.radians(phi))                     # Find relative phase for current element
                    elementSum += element[3] * math.e ** ((relativePhase + element[4]) * 1j)                                            # Element contribution = Amp * e^j(Phase + Phase Weight)

                arrayFactor[phi][theta] = elementSum.real

        return arrayFactor

    
    def CalculateRelativePhase(self,Element, Lambda, theta, phi):
        """
        Incident wave treated as plane wave. Phase at element is referred to phase of plane wave at origin.
        Element = xPos, yPos, zPos, ElementAmplitude, ElementPhaseWeight
        theta & phi in radians
        See Eqn 3.1 @ https://theses.lib.vt.edu/theses/available/etd-04262000-15330030/unrestricted/ch3.pdf
        """
        phaseConstant = (2 * math.pi / Lambda)

        xVector = Element[0] * math.sin(theta) * math.cos(phi)
        yVector = Element[1] * math.sin(theta) * math.sin(phi)
        zVector = Element[2] * math.cos(theta)

        phaseOfIncidentWaveAtElement = phaseConstant * (xVector + yVector + zVector)

        return phaseOfIncidentWaveAtElement


    def FieldSumPatch(self,ElementArray, Freq, W, L, h, Er):
        """
        Summation of field contributions from each patch element in array, at frequency freq for theta 0°-95°, phi 0°-360°.
        Element = xPos, yPos, zPos, ElementAmplitude, ElementPhaseWeight
        Returns arrayFactor[theta, phi, elementSum]
        """
        
        arrayFactor = np.ones((360, 95))

        Lambda = 3e8 / Freq

        for theta in range(95):
            for phi in range(360):                                                                                                      # For all theta/phi positions
                elementSum = 1e-9 + 0j

                xff, yff, zff = sph2cart1(999, math.radians(theta), math.radians(phi))                                                  # Find point in far field

                for element in ElementArray:                                                                                            # For each element in array, find local theta/phi, calculate field contribution and add to summation for point
                    xlocal = xff - element[0]
                    ylocal = yff - element[1]                                                                                           # Calculate local position in cartesian
                    zlocal = zff - element[2]

                    r, thetaLocal, phiLocal = cart2sph1(xlocal, ylocal, zlocal)                                                         # Convert local position to spherical

                    patchFunction = PatchFunction(math.degrees(thetaLocal), math.degrees(phiLocal), Freq, W, L, h, Er)            # Patch element pattern for local theta, phi

                    if patchFunction != 0:                                                                                              # Sum each elements contribution
                        relativePhase = self.CalculateRelativePhase(element, Lambda, math.radians(theta), math.radians(phi))                 # Find relative phase for current element
                        elementSum += element[3] * patchFunction * math.e ** ((relativePhase + element[4]) * 1j)                        # Element contribution = Amp * e^j(Phase + Phase Weight)

                arrayFactor[phi][theta] = elementSum.real

        return arrayFactor # the pattern to plot itself


if __name__ == "__main__":
    
    # W,L,h,Er
    ArrAn = ArrayAntenna()

    elements_at = [[ 0.0,0.,0.,1.,0.],
                   [ 0.005,0.,0.,1.,0.5*np.pi],
                #    [ 0.,1.,0.,1.,1.5*np.pi],
                #    [ 0.,-1.,0.,1.,np.pi]
                   ]
    _params = [10.7e-3,10.47e-3,3e-3,2.5]
    ArrayFactor = ArrAn.FieldSumPatch(ElementArray=elements_at, 
                                      Freq=14e9, 
                                      W=_params[0],
                                      L=_params[1],
                                      h=_params[2],
                                      Er=_params[3])
    
    phi = np.arange(0,360,1)
    theta = np.arange(0,95,1)


    ArrayFactor = np.array(ArrayFactor)
    print("ArrayFac:",ArrayFactor.shape)
    SurfacePlot(Fields=ArrayFactor)
