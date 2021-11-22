import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm   

def d(point1,point2):
    # Short function for calculating distance between pair of points (numpy 1D lists)
    return np.linalg.norm(point1-point2)

def inner(trongle,points):
    # Calculates 'inner' length of network
    return d(points[0],points[1])+d(points[1],points[2])+d(points[2],points[0])

def outer(trongle,points):
    # Calculates 'outer' length of network
    return d(trongle[0],points[0])+d(trongle[1],points[1])+d(trongle[2],points[2])

def distance(trongle,points):
    # Calculates the distance within the network
    return inner(trongle,points) + 2*outer(trongle,points)

def length(trongle,points):
    # Calculates the total length of the network
    return inner(trongle,points) + outer(trongle,points)

def gridChoice():
    """
        Function used to test data approaches and make plots thereof.

        The core of the used approach is to test evenly spaced positions of the 3 inner points.
        The result is very inefficient, due to the 6 degrees of freedom derived.
    """
    xnum = 10 # grid size in each dimension
    ynum = 10

    trongle = np.array( [[0,0],[5,2],[1,4]] ) # set up of outer points
    xvals = np.linspace(0,5,xnum)
    yvals = np.linspace(0,4,ynum)

    xv , yv = np.meshgrid(xvals,yvals)
    xv = np.reshape(xv,xnum*ynum)
    yv = np.reshape(yv,xnum*ynum)

    pL = np.array([xv,yv]).transpose() # list of inner point candidates

    lengths = []
    distances = []
    c = 0
    countdecent = 0

    point = [1.725,2.356] # fermat point for the given triangle
    pfermat = np.array([point,point,point])
    minLlength = length(trongle,pfermat) # calculations for 'minimum length' fermat point solution
    minLdist = distance(trongle,pfermat)

    minDlength = length(trongle,trongle) # calculations for 'minimum distance' full triangle solution
    minDdist = distance(trongle,trongle)

    print(f"Testing {(xnum*ynum)**3} triplets of points:")
    for i in tqdm(range(xnum*ynum)): # goes through list of candidate inner point triplets
        for j in range(xnum*ynum):
            for k in range(xnum*ynum):
                points = [pL[i],pL[j],pL[k]]

                L = length(trongle,points)
                D = distance(trongle,points)
                if True: # optional statement used to partially filter candidates
                    if L < minDlength and D < minLdist: # ones worse than either of the boundary conditions are discarded
                        lengths.append(L)
                        distances.append(D)
                else:
                    lengths.append(L)
                    distances.append(D)

    combined = np.array([lengths,distances]) # combines lengths and distances into one array
    
    if False: # keeps only the 'lowest' values, producing a strictly decreasing sequence of points in L-D space
        combined = combined[:,np.argsort(combined[0])] # sorts the list by the lengths

        min_D = 100
        i = 0
        deletion_indices = []
        print("Filtering for strictly decreasing sequence:")
        for i in tqdm(range(combined[0].size)):
            cur_D = combined[1,i]
            if cur_D >= min_D:
                deletion_indices.append(i)
            else:
                min_D = cur_D
        combined = np.delete(combined,deletion_indices,axis=1)
        
    print(f"{combined.size} points left")

    lengths = combined[0]
    distances = combined[1]

    fig = plt.figure()
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(111)
    ax.patch.set_facecolor('black')

    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    plt.scatter(lengths,distances,s=1,color='white')

    plt.scatter(length(trongle,trongle),distance(trongle,trongle),s=10,color='red')

    plt.scatter(length(trongle,pfermat),distance(trongle,pfermat),s=10,color='red')

    plt.xlim(0,40)
    plt.ylim(0,60)
    plt.show()

gridChoice()