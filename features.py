import numpy as np
import math
from fractions import Fraction
from scipy.odr import *

class featuresDetection:
    def __init__(self):
        # variables
        self.EPSILON = 10
        self.DELTA = 501
        self.SNUM = 6
        self.PMIN = 20
        self.GMAX = 20
        self.SEED_SEGMENTS = []
        self.LINE_SEGMENTS = []
        self.LASERPOINTS = []
        self.LINE_PARAMS = None
        self.NP = len(self.LASERPOINTS) - 1
        self.LMIN = 20 # najmanja duzina line segmenta
        self.LR = 0 # prava duzina line segmenta
        self.PR = 0 # broj laser pointova u line segmentu

    def euklidijanovaDistancaizmedjuPoints(self, point1, point2):
        Px = (point1[0]-point2[0])**2
        Py = (point1[1]-point2[1])**2
        return math.sqrt(Px+Py)
    
    def distancaPointaodLinije(self, params, point):
        A, B, C = params
        distance = abs(A*point[0] + B*point[1] + C)/ math.sqrt(A**2+B**2)
        return distance
    
    def line2points(self, m, b): ######
        x=5
        y=m*x+b
        x2=2000
        y2=m*x2+b
        return [(x, y), (x2, y2)]
    
    def lineFormGen2SlopeIntercept(self, A, B, C): #########
        m = -A/B
        B = -C/B
        return m, B
    
    def lineFormSi2Gen(self, m, B):  ##########
        A, B, C = -m, 1, -B
        if A<0:
            A, B, C = -A, -B, -C

        den_a = Fraction(A).limit_denominator(1000).as_integer_ratio()[1]
        den_c = Fraction(C).limit_denominator(1000).as_integer_ratio()[1]

        Gcd = np.gcd(den_a, den_c)

        lcm = den_c*den_a / Gcd

        A = A*lcm
        B = B*lcm
        C = C*lcm

        return A, B, C
    
    def lineInterceptGenForm(self, params1, params2):
        a1, b1, c1 = params1
        a2, b2, c2 = params2

        x = (c1*b2 - b1*c2)/(b1*a2-a1*b2)
        y = (a1*c2-a2*c1)/(b1*a2-b2*a1)

        return x, y