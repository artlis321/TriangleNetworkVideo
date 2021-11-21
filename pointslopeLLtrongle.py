import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from random import random

def d(p1,p2):
    return np.linalg.norm(p1-p2)

def ang(v1,v2):
    uv1 = v1 / np.linalg.norm(v1)
    uv2 = v2 / np.linalg.norm(v2)
    dot = np.dot(uv1,uv2)
    return np.arccos(dot)

def testO(A,B,C,O):
    ang_OAB = ang(O-A,B-A)
    ang_OBA = ang(O-B,A-B)
    ang_OAC = ang(O-A,C-A)
    ang_OCA = ang(O-C,A-C)
    ang_OBC = ang(O-B,C-B)
    ang_OCB = ang(O-C,B-C)

    ang_A = (+ang_OAB+ang_OBA+ang_OAC+ang_OCA-ang_OBC-ang_OCB)/2
    ang_B = (+ang_OAB+ang_OBA-ang_OAC-ang_OCA+ang_OBC+ang_OCB)/2
    ang_C = (-ang_OAB-ang_OBA+ang_OAC+ang_OCA+ang_OBC+ang_OCB)/2

    if any([ang_A<0,ang_B<0,ang_C<0]):
        return {
            'success' : False
        }

    A1O = 1
    A1B1 = np.sin(np.pi - ang_A - ang_B) / np.sin(ang_B)
    B1O = np.sin(ang_A) / np.sin(ang_B)
    A1C1 = np.sin(np.pi - ang_A - ang_C) / np.sin(ang_C)
    C1O = np.sin(ang_A) / np.sin(ang_C)
    B1C1 = np.sin(2*ang_A) * A1B1 / np.sin(2*ang_C)

    IP = A1B1 + A1C1 + B1C1 # perimeter of inner triangle (added lines)
    II = A1O + B1O + C1O # inner segments of inner triangle (removed lines)

    AO = d(A,O)
    BO = d(B,O)
    CO = d(C,O)

    scale_max = min([AO/A1O,BO/B1O,CO/C1O])

    D_0 = 2*(AO+BO+CO)
    L_0 = AO+BO+CO

    L_max = L_0 + scale_max*(IP-II)
    D_min = D_0 + scale_max*(IP-2*II)

    return {
        'success' : True,
        'D_0' : D_0,
        'L_0' : L_0,
        'D_min' : D_min,
        'L_max' : L_max
    }

A = np.array([0,0])

B_x = 5
B = np.array([B_x,0])

C_x = 2
C_y = 3
C = np.array([C_x,C_y])

L_max_list = []
D_min_list = []
Ox_list = []
Oy_list = []

O_fpoint = np.array([2.108,1.417])
O_bisect = np.array([2.181,1.167])

for y in tqdm(np.linspace(1.16,1.42,200)):
    for x in np.linspace(2.1,2.2,200):
        if (x>y*C_x/C_y) and (x<(B_x*(1-y/C_y)+C_x*(y/C_y))):
            O = np.array([x,y])
            vals = testO(A,B,C,O)

            if vals['success']:
                #plt.plot([vals['L_0'],vals['L_max']],[vals['D_0'],vals['D_min']],color='black',lw=1)
                L_max_list.append(vals['L_max'])
                D_min_list.append(vals['D_min'])
                Ox_list.append(O[0])
                Oy_list.append(O[1])

max_array = np.array([L_max_list,D_min_list,Ox_list,Oy_list])
print("Array made")
max_array_sorted = max_array[:,np.argsort(max_array[0])]
print("Array sorted")
min_D = 100
i = 0
deletion_indices = []
for i in tqdm(range(max_array_sorted[0].size)):
    cur_D = max_array_sorted[1,i]
    if cur_D >= min_D:
        deletion_indices.append(i)
    else:
        min_D = cur_D
max_array_sorted = np.delete(max_array_sorted,deletion_indices,axis=1)
print("Array filtered")
plt.plot(max_array_sorted[0],max_array_sorted[1],color='black')
plt.scatter(max_array_sorted[0],max_array_sorted[1],color='black',s=2)

plt.plot(max_array_sorted[2],max_array_sorted[3],color='blue')
plt.scatter(max_array_sorted[2],max_array_sorted[3],color='blue',s=2)
plt.scatter([O_fpoint[0],O_bisect[0]],[O_fpoint[1],O_bisect[1]],color='red',s=5)

vals = testO(A,B,C,O_fpoint)
plt.plot([vals['L_0'],vals['L_max']],[vals['D_0'],vals['D_min']],color='red',lw=1)

vals = testO(A,B,C,O_bisect)
plt.plot([vals['L_0'],vals['L_max']],[vals['D_0'],vals['D_min']],color='red',lw=1)

plt.xlim(0,20)
plt.ylim(0,15)
plt.show()