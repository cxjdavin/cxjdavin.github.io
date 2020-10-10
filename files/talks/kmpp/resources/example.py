import numpy as np
A = [(0.25,0), (0,0.25), (0.65,0.4), (0.15,0.6)]
B = [(0.25,1.5), (-0.15,1.2), (-0.3,1.7)]
C = [(2,0.1), (2.2,-0.1), (2.45,0.3), (2.7,0.4), (3.1,-0.2), (3.35,0.5), (3.55,0.1), (3.7,0.2)]
D = [(2,1.1), (2.2,1.1), (2.45,1.3), (2.7,1.4), (3.1,1.2), (3.35,1.5), (3.55,1.1)]

AB = np.array(A+B)
CD = np.array(C+D)
A = np.array(A)
B = np.array(B)
C = np.array(C)
D = np.array(D)

centroidA = sum(A)/len(A)
centroidB = sum(B)/len(B)
centroidC = sum(C)/len(C)
centroidD = sum(D)/len(D)
centroidAB = sum(AB)/len(AB)
centroidCD = sum(CD)/len(CD)

# >>> centroidA
# array([0.2625, 0.3125])
# >>> centroidB
# array([-0.06666667,  1.46666667])
# >>> centroidC
# array([2.88125, 0.1625 ])
# >>> centroidD
# array([2.76428571, 1.24285714])
# >>> centroidAB
# array([0.12142857, 0.80714286])
# >>> centroidCD
# array([2.82666667, 0.66666667])