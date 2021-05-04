
import math
import numpy as np


class Grid():
    def __init__(self,n_patches,Wmax,Lmax,clearence):

        # uniformly distribute a perfect square at the centre, for symmetricity
        self.n_patches = n_patches
        if  math.isqrt(n_patches) ** 2 != n_patches :
            print("Warning: Patches are lost as no. of patches is not a perfect square")
        
        self.max_possible_square = int(math.sqrt(self.n_patches))
        print(self.max_possible_square)
        self.Wmax = Wmax
        self.Lmax = Lmax
        self.clearence = clearence

    def get_path_pos(self):
        
        half_width = 0
        half_length = 0
        if self.n_patches > 1:
            half_width = (self.max_possible_square - 1)*0.5*(self.clearence+self.Wmax)
            half_length = (self.max_possible_square - 1)*0.5*(self.clearence+self.Lmax)
        
        k = 0
        x = [0]*self.max_possible_square*self.max_possible_square
        y = [0]*self.max_possible_square*self.max_possible_square
        for i in range(self.max_possible_square):
            for j in range(self.max_possible_square):
                print(k)
                x[k] = -half_width + i*(self.Wmax+self.clearence)
                y[k] = -half_length + j*(self.Wmax+self.clearence)
                k+=1


        return x,y

class Spiral():
    def __init__(self,n_patches,Wmax,Lmax,clearence):

        # uniformly distribute a perfect square at the centre, for symmetricity
        self.n_patches = n_patches
        self.Wmax = Wmax
        self.Lmax = Lmax
        self.inter_rect_clearence = clearence*math.sqrt(2.0)

    def get_path_pos(self):
        
        '''
        x^2 + y^2 = r^2

        x = r cos(theta)
        
        y = r cos(theta)
        '''

        # first patch is in origin
        theta = 0.
        r = 0.
        x = [0]*self.n_patches
        y = [0]*self.n_patches

        '''
        Variant 1 
                  |dx| >= Wmax + c/2 
                  |dy| >= Lmax + c/2 
            dr = constant
            dtheta = constant
        '''
        dtheta = np.radians(1)
        dr = 1.0e-4
        for k in range(1,self.n_patches):
            prev_patch_pos = np.array([x[k-1],y[k-1]])
            curr_patch_pos = np.array([x[k],y[k]])
            while abs(x[k]-x[k-1]) < (self.Wmax + 0.5*self.inter_rect_clearence) or \
                  abs(y[k]-y[k-1]) < (self.Lmax + 0.5*self.inter_rect_clearence):
                r += dr
                theta += dtheta
                x[k] = r*math.cos(theta)
                y[k] = r*math.sin(theta)
            
            if k != self.n_patches -1:
                x[k+1] = x[k]
                y[k+1] = y[k]

        '''
        Variant 2 (yset to solve)
        
        -> dx = cos(theta)dr - r sin(theta)dtheta  
        -> dy = sin(theta)dr + r cos(theta)dtheta

        constraint 
                  |dx| = Wmax + c/2 
                  |dy| = Lmax + c/2 

        dr = variable
        dtheta = variable
        '''

        # for k in range(1,self.n_patches):
        #     '''
        #     solve:

        #     mod{ ( cos(theta) -r sin(theta) ) (dr)         } = Wmax + c/2 
        #        { ( sin(theta) +r cos(theta) ) (dtheta)     }   lmax + c/2

        #     =>            A        *        x          = +b   , solve for x
        #                   A        *        x          = -b   , solve for x

        #     '''
        #     A = np.array([
        #                 [math.cos(theta), -r*math.sin(theta)],
        #                 [math.sin(theta), +r*math.cos(theta)],
        #                 ])
        #     b_plus = np.array([ self.Wmax + 0.5*self.inter_rect_clearence, 
        #                         self.Lmax + 0.5*self.inter_rect_clearence
        #                       ])
            
        #     b_minus = np.array([ 
        #                        -(self.Wmax + 0.5*self.inter_rect_clearence), 
        #                        -(self.Lmax + 0.5*self.inter_rect_clearence)
        #                        ])
        #     deltas_pos = np.linalg.solve(A, b_plus)
        #     deltas_neg = np.linalg.solve(A, b_minus)

        #     print('plus gradients',deltas_pos )
        #     print('minus gradients',deltas_neg )

        #     # r += deltas_pos[0]
        #     theta += deltas_pos[1]

        #     r += deltas_neg[0]
        #     # theta += deltas_neg[1]

        #     x[k] = r*math.cos(theta)
        #     y[k] = r*math.sin(theta)
            
        #     if k != self.n_patches -1:
        #         x[k+1] = x[k]
        #         y[k+1] = y[k]


        return x,y



if __name__ == "__main__":

    g = Grid(n_patches=4,
                Wmax=10.0e-3,
                Lmax=10.0e-3,
                clearence= 0)
    x,y = g.get_params_range()
    print('x:',x)
    print('y:',y)
