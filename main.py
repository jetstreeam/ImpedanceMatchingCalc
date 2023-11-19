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
    Q = sqrt((Rs/Rt)-1+Xs**2/(Rs*Rt))
    X11 = (Xs+Rs*Q)/(Rs/Rt-1)
    X12 = (Xs-Rs*Q)/(Rs/Rt-1)
    X21 = (-1)*(Xt+Rt*Q)
    X22 = (-1)*(Xt-Rt*Q)
    return (X11, X12, X21, X22, Q)

def calcReversedReactances(Rs, Xs, Rt, Xt):
    Q = sqrt((Rt/Rs)-1+Xt**2/(Rs*Rt))
    X11 = (Xt+Rt*Q)/(Rt/Rs-1)
    X12 = (Xt-Rt*Q)/(Rt/Rs-1)
    X21 = (-1)*(Xs+Rs*Q)
    X22 = (-1)*(Xs-Rs*Q)
    return (X11, X12, X21, X22, Q)

def calcSparameters(impedances, z0, z11, z12, z21, z22):
    
    Rs = impedances['Z_s'].real
    Xs = impedances['Z_s'].imag
    Rt = impedances['Z_t'].real
    Xt = impedances['Z_t'].imag
    Z0 = impedances['Z_0']

    X11, X12, X21, X22, Q = calcNormalReactances(Rs,Xs,Rt,Xt)
    
    #print(Rs,Xs,Rt,Xt)

    #print(X11,X12,X21,X22)
    # for X1
    frequencies = np.linspace(1,10,100) * 1e9

    if X11 > 0:
        L = calcL(X11)        
        Z11 = np.ones_like(frequencies)*Rs + 1j*(np.ones_like(frequencies)*Xs + 2*np.pi*frequencies*L)
    else:
        C = calcC(abs(X11))
        Z11 = np.ones_like(frequencies)*Rs + 1j*(np.ones_like(frequencies)*Xs - 1/(2*np.pi*frequencies*C))

    # for X2
    if X21 > 0:
        L = calcL(X21)
        Z21 = np.ones_like(frequencies)*Rs + 1j*(np.ones_like(frequencies)*Xs + 2*np.pi*frequencies*L)
    else:
        C = calcC(abs(X21))
        Z21 = np.ones_like(frequencies)*Rs + 1j*(np.ones_like(frequencies)*Xs - 1/(2*np.pi*frequencies*C))
    
    z11=np.array([1j*z.imag for z in Z11])
    z12=z11
    z21=z11
    z22=np.zeros_like(frequencies)+z11+1j*Z21.imag
    z0 = np.ones_like(z11)*impedances['Z_0']
    
    s11 = ((z11-z0)*(z22+z0)-z12*z21)/((z11+z0)*(z22+z0)-z12*z21)
    s12 = (2*z12*z0)/((z11+z0)*(z22+z0)-z12*z21)
    s21 = (2*z21*z0)/((z11+z0)*(z22+z0)-z12*z21)
    s22 = ((z11+z0)*(z22-z0)-z12*z21)/((z11+z0)*(z22+z0)-z12*z21)

    tot = np.column_stack((frequencies/1000000000,s11.real,s11.imag,s21.real,s21.imag,s12.real,s12.imag,s22.real,s22.imag))

    with open('mynetwk.s2p', 'w', encoding='utf-8') as f:
        f.writelines('! Created Thu Nov 11 11:09:06 2010\n')
        f.writelines('!\n')
        f.writelines('!Created with skrf (http://scikit-rf.org).\n')
        f.writelines('# GHz S RI R 50.0\n')
        f.writelines('!freq ReS11 ImS11 ReS21 ImS21 ReS12 ImS12 ReS22 ImS22\n')
        
        for l in tot:
            cc = ' '.join([str(t) for t in l])+'\n'
            f.writelines(cc)

    
    return (s11, s12, s21, s22)

def getParallelElement(X):
    if X > 0:
        L = calcL(X)
        if L == 0:
            return(f"Lp: open")
        else:
            L*=1e9
            return(f"Lp: {L:.3g}nH")
    else:
        C = calcC(abs(X))
        if C == 0:
            return(f"Cp: open")
        else:
            C*=1e12
            return(f"Cp: {C:.3g}pF")

def getSerialElement(X):
    if X > 0:
        L = calcL(X)
        if L == 0:
            return(f"Ls: short")
        else:
            L*=1e9
            return(f"Ls: {L:.3g}nH")
    else:
        C = calcC(abs(X))
        if C == 0:
            return(f"Cs: short")
        else:
            C*=1e12
            return(f"Cs: {C:.3g}pF")
        


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

for p in Zpairs:
    layout = ''
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
        print(f"{getParallelElement(X11)} {getSerialElement(X21)}")
        print(f"{getParallelElement(X12)} {getSerialElement(X22)}\n")
    if 'reversed' in r.keys():
        X11, X12, X21, X22, Q = calcReversedReactances(Rs,Xs,Rt,Xt)
        print(f"{getSerialElement(X21)} {getParallelElement(X11)}")
        print(f"{getSerialElement(X22)} {getParallelElement(X12)}\n")

