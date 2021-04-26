
"""
Function to calculate peak directivity.
Also includes some examples that are used to check result.
"""
from math import sin, sqrt, pi, log10, radians
import numpy as np
# from src.patch import *
import patch


def SqrtSinPattern(Theta, Phi, *args):
    """
    See Fig1 @ http://www.antenna-theory.com/basics/directivity.php
    Expect Directivity to be 1.05dB.
    """
    return sqrt(sin(radians(Theta)))


def SinPowerPattern(Theta, Phi, *args):
    """
    See Fig1 @ http://www.antenna-theory.com/basics/directivity.php
    Expect Directivity to be 2.707dB.
    """
    return sin(radians(Theta)) ** 5


def IsotropicPattern(Theta, Phi, *args):
    """
    Isotropic directional pattern. i.e. radiation is same in all directions.
    Expect directivity to be 0dB.
    """
    return 1


def xfrange(start, stop, step):
    """
    Creates range of float values.
    """
    i = 0
    while start + i * step < stop:
        yield start + i * step
        i += 1

def CalcDirectivity(Efficiency, RadPatternFunction, *args,theta_range=[0,180],phi_range=[0,360]):
    """
    Based on calc_directivity.m from ArrayCalc.
    Calculates peak directivity in dBi value using numerical integration.
    If the array efficiency is set to below 100% then the returned value is referred to as Gain (dB).
    Usage: ThetaMax, PhiMax = CalcDirectivity(RadPatternFunction, Efficiency)
    RadPatternFunction - antennas radiation pattern function. F(Theta, Phi)
    Efficiency - Efficiency of antenna in %. Default 100%.
    Returned values:
    ThetaMax - Theta value for direction of maximum directivity (Deg)
    PhiMax - Phi value for direction of maximum directivity (Deg)
    Integration is of the form :
    %
    %       360   180
    %     Int{  Int{  (E(theta,phi)*conj(E(theta,phi))*sin(theta) d(theta) d(phi)
    %        0     0
    %
    %         z
    %         |-theta   (theta 0-180 measured from z-axis)
    %         |/
    %         |_____ y
    %        /\
    %       /-phi       (phi 0-360 measured from x-axis)
    %      x
    %
    """
    print("Calculating Directivity for " + RadPatternFunction.__name__)

    deltheta = 2                                                                # Step value of theta (Deg)
    delphi = 2                                                                  # Step value for phi (Deg)

    dth = radians(deltheta)
    dph = radians(delphi)

    Psum = 0
    Pmax = 0
    Thmax = 0
    Phmax = 0

    for phi in xfrange(phi_range[0], phi_range[1], delphi):                                                                     # Phi Integration Loop 0-360 degrees
        for theta in xfrange(theta_range[0], theta_range[1], deltheta):                                                             # Theta Integration Loop 0-180 degrees
            eField = RadPatternFunction(theta, phi, *args)                                       # Total E-field at point
            Pthph = eField * np.conjugate(eField)                                                                             # Convert to power

            if Pthph > Pmax:
                Pmax = Pthph                                                                                # Store peak value
                Thmax = theta                                                                               # Store theta value for the maximum
                Phmax = phi                                                                                 # Store phi value for the maximum

            # print(str(theta) + "," + str(phi) + ": " + str(Pthph))
            Psum = Psum + Pthph * sin(radians(theta)) * dth * dph                                           # Summation

    Pmax = Pmax * (Efficiency / 100)                                                                        # Apply antenna efficiency

    directivity_lin = Pmax / (Psum / (4 * pi))                                                              # Directivity (linear ratio)
    directivity_dBi = 10 * log10(directivity_lin)                                                           # Directivity (dB wrt isotropic)
    Gmax = directivity_dBi
    if Efficiency < 100:                                                                                    # Gain case
        dBdiff = 10 * log10(abs(100 / Efficiency))                                                          # Difference between gain and directivity
        
        print("Directivity = " + str(directivity_dBi + dBdiff) + "dBi")                                     # Display what directivity would be for ref.
        print("Efficiency = " + str(Efficiency) + "%")
        print("Gain = " + str(directivity_dBi) + "dB")
        
    else:
        pass                                                                                                   # Directivity case
        print("Directivity = " + str(directivity_dBi) + "dBi")

    # print("At Theta = " + str(Thmax) + ", Phi = " + str(Phmax))

    return Gmax,Thmax, Phmax



if __name__ == "__main__":
    CalcDirectivity(100, SqrtSinPattern)
    print("\n\n")
    CalcDirectivity(90, SinPowerPattern)
    print("\n\n")
    CalcDirectivity(100, IsotropicPattern)

    print("\n\n")


    
    freq = 14e9
    # Er = 3.66                                                           # RO4350B
    # h = 0.101e-3
    # W, L, h, Er = patch.DesignPatch(Er, h, freq)
    # CalcDirectivity(100, patch.PatchFunction, freq, W, L, h, Er)
    # fields = patch.PatchEHPlanePlot(freq, W, L, h, Er)
    # patch.SurfacePlot(fields, freq, W, L, h, Er)

    
    W = 10.7e-3
    L = 10.47e-3
    h = 3e-3
    Er = 2.5

    print("\n\n")
    CalcDirectivity(100, patch.PatchFunction, freq, W, L, h, Er)
    fields = patch.PatchEHPlanePlot(freq, W, L, h, Er)
    patch.SurfacePlot(fields, freq, W, L, h, Er)
    
    
    freq = 14e9
    W = 10.7e-3
    L = 20.47e-3
    h = 3e-3
    Er = 2.5

    print("\n\n")
    print(CalcDirectivity(90, patch.PatchFunction, freq, W, L, h, Er))
    fields = patch.PatchEHPlanePlot(freq, W, L, h, Er)
    patch.SurfacePlot(fields, freq, W, L, h, Er)
    