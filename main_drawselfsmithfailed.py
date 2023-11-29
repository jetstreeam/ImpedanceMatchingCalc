#%%
from math import sqrt
import numpy as np
from smithchart import SmithChart
import matplotlib.pyplot as plt
import plotly.graph_objects as go

si_prefixes = {'0': '',
               '-18': 'a',
               '-15': 'f',
               '-12': 'p',
               '-9': 'n',
               '-6': 'u',
               '-3': 'm',
               '-2': 'm',
               '3': 'k',
               '6': 'M',
               '9': 'G'
               }

cap_lim = 0.9e-1
ind_lim = 1e-5

def addSiPrefix(number):
    """
    returns the number with added SI-Prefix
    """
    if number == 0:
        return ''
    else:
        a = str(format(number,'.2e'))               # display number in scientific notation with 3 significant figures
        exp = float(a[-3:])                         # get exponent of number
        a = str(round((float(a[:-4])) * 10**(exp%3), 6))    # adapt to multiple of 3 
        a = a.replace('.0', '') if a[-2:] == '.0' else a    # replace .0 if it is at end of number
        exp2 = str(int(exp-(exp%3)))                # get new exponent with multiple of 3    
        return(f"{a}{si_prefixes[exp2]}")           #return number with prefix out of dict

def calcL(X, f):
    """
    returns the calculated inductance or 0 if it is beyond ind_lim
    """
    return X/(2*np.pi*f) if X/(2*np.pi*f) < ind_lim else 0

def calcC(X, f):
    """
    returns the calculated capacity or 0 if it is beyond cap_lim
    """
    # or 1/(2*np.pi*f*X) < cap_lim
    if X == 0:
        return 0
    else:
        return 1/(2*np.pi*f*X)

def calcNormalReactances(Rs, Xs, Rt, Xt):
    """
    returns the calculated reactances in normal arrangement for given start and target impedances
    """
    Q = sqrt((Rs/Rt)-1+Xs**2/(Rs*Rt))
    if Rt == Rs:
        X11 = float("inf")
        X12 = float("inf")
        X21 = (-1)*(Xs+Xt)
        X22 = (-1)*(Xs+Xt)
    else:
        X11 = (Xs+Rs*Q)/(Rs/Rt-1)
        X12 = (Xs-Rs*Q)/(Rs/Rt-1)
        X21 = (-1)*(Xt+Rt*Q)
        X22 = (-1)*(Xt-Rt*Q)
    return (X11, X12, X21, X22, Q)

def calcReversedReactances(Rs, Xs, Rt, Xt):
    """
    returns the calculated reactances in reversed arrangement for given start and target impedances
    """
    Q = sqrt((Rt/Rs)-1+Xt**2/(Rs*Rt))
    if Rt == Rs:
        X11 = float("inf")
        X12 = float("inf")
        X21 = (-1)*(Xs+Xt)
        X22 = (-1)*(Xs+Xt)
    else:
        X11 = (Xt+Rt*Q)/(Rt/Rs-1)
        X12 = (Xt-Rt*Q)/(Rt/Rs-1)
        X21 = (-1)*(Xs+Rs*Q)
        X22 = (-1)*(Xs-Rs*Q)
    return (X11, X12, X21, X22, Q)

def getParallelElement(X, f):
    """
    returns the calculated parallel L or C value with units
    """
    if X == float("inf"):
        return ('no shunt element',0,'')
    elif X > 0:
        L = calcL(X,f)
        return ('Lp', L, 'H')
    else:
        C = calcC(abs(X),f)
        return ('Cp', C, 'F')

def getSerialElement(X,f):
    """
    returns the calculated serial L or C value with units
    """
    if X == float("inf"):
        return ('short',0,'')
    elif X > 0:
        L = calcL(X,f)
        return ('Ls', L, 'H')
    else:
        C = calcC(abs(X),f)
        return ('Cs', C, 'F')
        
# define start and target impedance pairs
Zpairs = [{'Z_s': 20+0j, 'Z_t': 50+0j, 'Z_0': 50, 'f_0': 2.44e9},
            {'Z_s': 20-10j, 'Z_t': 60+60j, 'Z_0': 50, 'f_0': 2.44e9},
            {'Z_s': 100+75j, 'Z_t': 30+0, 'Z_0': 50j, 'f_0': 2.44e9},
            {'Z_s': 15+50j, 'Z_t': 50+0j, 'Z_0': 30, 'f_0': 2.44e9},
            {'Z_s': 15+50j, 'Z_t': 50-10j, 'Z_0': 30, 'f_0': 2.44e9},
            {'Z_s': 30-45j, 'Z_t': 45-30j, 'Z_0': 30, 'f_0': 2.44e9},
            {'Z_s': 120+0j, 'Z_t': 60+0j, 'Z_0': 50, 'f_0': 2.44e9},
            {'Z_s': 13+60j, 'Z_t': 13-60j, 'Z_0': 60, 'f_0': 2.44e9},
            {'Z_s': 60-30j, 'Z_t': 60+0j, 'Z_0': 60, 'f_0': 2.44e9},
            {'Z_s': 60+20j, 'Z_t': 60+80j, 'Z_0': 60, 'f_0': 2.44e9}
          ]

Zpairs = [{'Z_s': 20-10j, 'Z_t': 60+60j, 'Z_0': 50, 'f_0': 2.44e9}
          ]


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
    f0 = p['f_0']

    # Rs = Rt
    if Rs == Rt:
        r['normal'] = calcNormalReactances(Rs,Xs,Rt,Xt)
        r['reversed'] = calcReversedReactances(Rs,Xs,Rt,Xt)
    # Rs > Rt
    elif Rs > Rt:
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
        ParElem1_name, ParElem1_value, ParElem1_unit = getParallelElement(X11,f0)
        SerElem1_name, SerElem1_value, SerElem1_unit = getSerialElement(X21,f0)
        ParElem2_name, ParElem2_value, ParElem2_unit = getParallelElement(X12,f0)
        SerElem2_name, SerElem2_value, SerElem2_unit = getSerialElement(X22,f0)

        print(f"{ParElem1_name}: {addSiPrefix(ParElem1_value)}{ParElem1_unit}, {SerElem1_name}: {addSiPrefix(SerElem1_value)}{SerElem1_unit}")
        print(f"{ParElem2_name}: {addSiPrefix(ParElem2_value)}{ParElem2_unit}, {SerElem2_name}: {addSiPrefix(SerElem2_value)}{SerElem2_unit}")

    if 'reversed' in r.keys():
        X11, X12, X21, X22, Q = r['reversed']
        ParElem1_name, ParElem1_value, ParElem1_unit = getParallelElement(X11,f0)
        SerElem1_name, SerElem1_value, SerElem1_unit = getSerialElement(X21,f0)
        ParElem2_name, ParElem2_value, ParElem2_unit = getParallelElement(X12,f0)
        SerElem2_name, SerElem2_value, SerElem2_unit = getSerialElement(X22,f0)

        print(f"{SerElem1_name}: {addSiPrefix(SerElem1_value)}{SerElem1_unit}, {ParElem1_name}: {addSiPrefix(ParElem1_value)}{ParElem1_unit}")
        print(f"{SerElem2_name}: {addSiPrefix(SerElem2_value)}{SerElem2_unit}, {ParElem2_name}: {addSiPrefix(SerElem2_value)}{ParElem2_unit}")


        fig, ax = plt.subplots(figsize=(8.0, 8.0))

        s1 = SmithChart(fig=fig, ax=ax)
        #s1.markZ(20+30j)

        z_s = np.linspace(0,X21/Z0,100) + Xs/Z0
        r_s = np.ones_like(z_s)*Rs/Z0


        start = (r_s[-1]+1j*z_s[-1])

        way = 1/np.linspace(1/start,(1/(X11/Z0)),100)
        
        r_s=np.append(r_s,way.real)
        z_s=np.append(z_s,way.imag)

        res = (z_s+r_s*1j)*50

        print(res)

        for i in res:
            print(i)
            s1.markZ(complex(i.real, i.imag))
        
        s1.markZ(20-10j)
