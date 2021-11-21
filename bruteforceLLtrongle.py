import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm   

def d(point1,point2):
    return np.linalg.norm(point1-point2)

def inner(trongle,points):
    return d(points[0],points[1])+d(points[1],points[2])+d(points[2],points[0])

def outer(trongle,points):
    return d(trongle[0],points[0])+d(trongle[1],points[1])+d(trongle[2],points[2])

def distance(trongle,points):
    return inner(trongle,points) + 2*outer(trongle,points)

def length(trongle,points):
    return inner(trongle,points) + outer(trongle,points)

def gridChoice():
    xnum = 10
    ynum = 10

    trongle = np.array( [[0,0],[5,2],[1,4]] )
    xvals = np.linspace(0,5,xnum)
    yvals = np.linspace(0,4,ynum)

    xv , yv = np.meshgrid(xvals,yvals)
    xv = np.reshape(xv,xnum*ynum)
    yv = np.reshape(yv,xnum*ynum)

    pL = np.array([xv,yv]).transpose()
    print(pL.shape)

    lengths = []
    distances = []
    c = 0
    countdecent = 0

    point = [1.725,2.356]
    pfermat = np.array([point,point,point])
    minLlength = length(trongle,pfermat)
    minLdist = distance(trongle,pfermat)

    minDlength = length(trongle,trongle)
    minDdist = distance(trongle,trongle)

    for i in tqdm(range(xnum*ynum)):
        for j in range(xnum*ynum):
            for k in range(xnum*ynum):
                points = [pL[i],pL[j],pL[k]]

                L = length(trongle,points)
                D = distance(trongle,points)
                if L < minDlength and D < minLdist:
                    flag = True
                    for i in range(len(lengths)):
                        if L > lengths[i] and D > distances[i]:
                            flag = False
                    if flag:
                        lengths.append(L)
                        distances.append(D)

    print(lengths)
    print(distances)

    filteredLengths = []
    filteredDistances = []

    for j in range(len(lengths)):
        flag = True
        L = lengths[j]
        D = lengths[j]
        for i in range(len(lengths)):
            if L > lengths[i] and D > distances[i]:
                flag = False
        if flag:
            filteredLengths.append(L)
            filteredDistances.append(D)

    fig = plt.figure()
    fig.patch.set_facecolor('black')
    ax = fig.add_subplot(111)
    ax.patch.set_facecolor('black')

    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')

    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    plt.scatter(filteredLengths,filteredDistances,s=1,color='white')

    plt.scatter(length(trongle,trongle),distance(trongle,trongle),s=10,color='red')

    plt.scatter(length(trongle,pfermat),distance(trongle,pfermat),s=10,color='red')

    plt.xlim(0,40)
    plt.ylim(0,60)
    plt.show()

gridChoice()