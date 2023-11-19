#%%

from math import sqrt
import numpy as np
import skrf as rf
from skrf import Network
import os

Z_0 = 50
f0 = 2.44e9

cap_lim = 0.9e-1
ind_lim = 1e-5

def calcL(X, f=f0):
    # returns the calculated inductance or 0 if it is beyond ind_lim
    return X/(2*np.pi*f) if X/(2*np.pi*f) < ind_lim else 0

def calcC(X, f=f0):
    # returns the calculated capacity or 0 if it is beyond cap_lim
    return 1/(2*np.pi*f*X) if 1/(2*np.pi*f*X) < cap_lim else 0

def calcNormalReactances(Rs, Xs, Rt, Xt):
    # returns the calculated reactances in normal arrangement for given start and target impedances
    Q = sqrt((Rs/Rt)-1+Xs**2/(Rs*Rt))
    X11 = (Xs+Rs*Q)/(Rs/Rt-1)
    X12 = (Xs-Rs*Q)/(Rs/Rt-1)
    X21 = (-1)*(Xt+Rt*Q)
    X22 = (-1)*(Xt-Rt*Q)
    return (X11, X12, X21, X22, Q)

def calcReversedReactances(Rs, Xs, Rt, Xt):
    # returns the calculated reactances in reversed arrangement for given start and target impedances
    Q = sqrt((Rt/Rs)-1+Xt**2/(Rs*Rt))
    X11 = (Xt+Rt*Q)/(Rt/Rs-1)
    X12 = (Xt-Rt*Q)/(Rt/Rs-1)
    X21 = (-1)*(Xs+Rs*Q)
    X22 = (-1)*(Xs-Rs*Q)
    return (X11, X12, X21, X22, Q)

def getParallelElement(X):
    # returns the calculated parallel L or C value with units
    if X > 0:
        L = calcL(X)
        return ('Lp', L, 'nH')
    else:
        C = calcC(abs(X))
        return ('Cp', C, 'pF')

def getSerialElement(X):
    # returns the calculated serial L or C value with units
    if X > 0:
        L = calcL(X)
        return ('Ls', L, 'nH')
    else:
        C = calcC(abs(X))
        return ('Cs', C, 'pF')
        
# define start and target impedance pairs
Zpairs = [{'Z_s': 20+0j, 'Z_t': 50+0j, 'Z_0': 50},
            {'Z_s': 20-10j, 'Z_t': 60+60j, 'Z_0': 50},
            {'Z_s': 100+75j, 'Z_t': 30+0, 'Z_0': 50j},
            {'Z_s': 15+50j, 'Z_t': 50+0j, 'Z_0': 30},
            {'Z_s': 15+50j, 'Z_t': 50-10j, 'Z_0': 30},
            {'Z_s': 30-45j, 'Z_t': 45-30j, 'Z_0': 30},
            {'Z_s': 120+0j, 'Z_t': 60+0j, 'Z_0': 50}
          ]
'''
{'Z_s': 13+60j, 'Z_t': 13-60j},
{'Z_s': 60-30j, 'Z_t': 60+0j},
{'Z_s': 60+20j, 'Z_t': 60+80j}
'''

# iterate all impedance pairs and print calculated networks
for p in Zpairs:
    r = {}

    print("---------------------------")
    print(f"Zs: {p['Z_s']}, Zt: {p['Z_t']}\n")

    Rs = p['Z_s'].real
    Xs = p['Z_s'].imag
    Rt = p['Z_t'].real
    Xt = p['Z_t'].imag
    Z0 = p['Z_0']

    # Rs > Rt
    if Rs > Rt:
        r['normal'] = calcNormalReactances(Rs,Xs,Rt,Xt)
        if abs(Xt) >= sqrt(Rt*(Rs-Rt)):
            r['reversed'] = calcReversedReactances(Rs,Xs,Rt,Xt)

    # Rs < Rt
    else:
        r['reversed'] = calcReversedReactances(Rs,Xs,Rt,Xt)
        if abs(Xs) >= sqrt(Rs*(Rt-Rs)):
            # Normal and reversed
            r['normal'] = calcNormalReactances(Rs,Xs,Rt,Xt)
    
    # print resulting networks
    if 'normal' in r.keys():
        X11, X12, X21, X22, Q = r['normal']

        ParElem1_name, ParElem1_value, ParElem1_unit = getParallelElement(X11)
        SerElem1_name, SerElem1_value, SerElem1_unit = getSerialElement(X21)
        ParElem2_name, ParElem2_value, ParElem2_unit = getParallelElement(X12)
        SerElem2_name, SerElem2_value, SerElem2_unit = getSerialElement(X22)

        ParElem1_value = ParElem1_value * 1e9 if ParElem1_name == 'Lp' else ParElem1_value * 1e12
        SerElem1_value = SerElem1_value * 1e9 if SerElem1_name == 'Ls' else SerElem1_value * 1e12
        ParElem2_value = ParElem2_value * 1e9 if ParElem2_name == 'Lp' else ParElem2_value * 1e12
        SerElem2_value = SerElem2_value * 1e9 if SerElem2_name == 'Ls' else SerElem2_value * 1e12

        print(f"{ParElem1_name}: {ParElem1_value:.3g}{ParElem1_unit} {SerElem1_name}: {SerElem1_value:.3g}{SerElem1_unit}")
        print(f"{ParElem2_name}: {ParElem2_value:.3g}{ParElem2_unit} {SerElem2_name}: {SerElem2_value:.3g}{SerElem2_unit}")

    if 'reversed' in r.keys():
        X11, X12, X21, X22, Q = calcReversedReactances(Rs,Xs,Rt,Xt)

        ParElem1_name, ParElem1_value, ParElem1_unit = getParallelElement(X11)
        SerElem1_name, SerElem1_value, SerElem1_unit = getSerialElement(X21)
        ParElem2_name, ParElem2_value, ParElem2_unit = getParallelElement(X12)
        SerElem2_name, SerElem2_value, SerElem2_unit = getSerialElement(X22)

        ParElem1_value = ParElem1_value * 1e9 if ParElem1_name == 'Lp' else ParElem1_value * 1e12
        SerElem1_value = SerElem1_value * 1e9 if SerElem1_name == 'Ls' else SerElem1_value * 1e12
        ParElem2_value = ParElem2_value * 1e9 if ParElem2_name == 'Lp' else ParElem2_value * 1e12
        SerElem2_value = SerElem2_value * 1e9 if SerElem2_name == 'Ls' else SerElem2_value * 1e12

        print(f"{SerElem1_name}: {SerElem1_value:.3g}{SerElem1_unit} {ParElem1_name}: {ParElem1_value:.3g}{ParElem1_unit}")
        print(f"{SerElem2_name}: {SerElem2_value:.3g}{SerElem2_unit} {ParElem2_name}: {ParElem2_value:.3g}{ParElem2_unit}")

