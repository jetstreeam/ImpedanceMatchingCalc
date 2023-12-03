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
    if number == float("inf"):
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
        return ('inf',float("inf"),'')
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
        return ('inf',float("inf"),'')
    elif X > 0:
        L = calcL(X,f)
        return ('Ls', L, 'H')
    else:
        C = calcC(abs(X),f)
        return ('Cs', C, 'F')

def printFormater(nameShunt:str, nameSerial:str, valueShunt:float, valueSerial:float, unitShunt:str, unitSerial:str, networktype='normal'):
    """
    prints a found network
    """
    if abs(valueShunt) == float("inf"):
        shunt = f"no shunt element"
    else:
        shunt = f"{nameShunt}: {addSiPrefix(valueShunt)}{unitShunt}"
    if abs(valueSerial) == 0:
        serial = f"no serial element"
    else:
        serial = f"{nameSerial}: {addSiPrefix(valueSerial)}{unitSerial}"

    if networktype == 'normal': 
        return f"{shunt}, {serial}"
    else:
        return f"{serial}, {shunt}"

def plotSmithChart(Z:dict, networks:list):
    """
    plots the smithchart for given values
    """
    
    fig, axes = plt.subplots(nrows=int(np.ceil(len(networks)/2)), ncols=2, figsize=(16.0, np.ceil(len(networks)/2)*8))

    for ax, i in zip(np.array(axes).flatten(), np.arange(len(np.array(axes).flatten()))):
        
        print(networks[i], i)
        schart = SmithChart(fig=fig, ax=ax, Z0=Z['Z_0'])
        schart.markZ(Z['Z_s'], c='r')
        schart.set_zstart_text(Z['Z_s'])
        schart.markZ(Z['Z_t'], c='g')
        schart.set_ztarget_text(Z['Z_t'])
        

# define start and target impedance pairs
Zpairs = [{'Z_s': 20+0j, 'Z_t': 50+0j, 'Z_0': 50, 'f_0': 2.44e9},
            {'Z_s': 20-10j, 'Z_t': 60+60j, 'Z_0': 50, 'f_0': 2.44e9},
            {'Z_s': 100+75j, 'Z_t': 30+0, 'Z_0': 50j, 'f_0': 2.44e9},
            {'Z_s': 15+50j, 'Z_t': 50+0j, 'Z_0': 30, 'f_0': 2.44e9},
            {'Z_s': 15+50j, 'Z_t': 50-10j, 'Z_0': 30, 'f_0': 2.44e9},
            {'Z_s': 30-45j, 'Z_t': 45-30j, 'Z_0': 30, 'f_0': 2.44e9},
            {'Z_s': 13+60j, 'Z_t': 13-60j, 'Z_0': 60, 'f_0': 2.44e9},
            {'Z_s': 60-30j, 'Z_t': 60+0j, 'Z_0': 60, 'f_0': 2.44e9},
            {'Z_s': 60+20j, 'Z_t': 60+80j, 'Z_0': 60, 'f_0': 2.44e9}
          ]

#Zpairs = [{'Z_s': 100+75j, 'Z_t': 30+0, 'Z_0': 50j, 'f_0': 2.44e9}]

# iterate all impedance pairs and print calculated networks
for pair in Zpairs:
    reactances = {}
    networks = []

    print("---------------------------")
    print(f"Zs: {pair['Z_s']}, Zt: {pair['Z_t']}\n")

    Rs = pair['Z_s'].real
    Xs = pair['Z_s'].imag
    Rt = pair['Z_t'].real
    Xt = pair['Z_t'].imag
    Z0 = pair['Z_0']
    f0 = pair['f_0']

    # Rs = Rt
    if Rs == Rt:
        reactances['normal'] = calcNormalReactances(Rs,Xs,Rt,Xt)
        reactances['reversed'] = calcReversedReactances(Rs,Xs,Rt,Xt)
    # Rs > Rt
    elif Rs > Rt:
        reactances['normal'] = calcNormalReactances(Rs,Xs,Rt,Xt)
        if abs(Xt) >= sqrt(Rt*(Rs-Rt)):
            reactances['reversed'] = calcReversedReactances(Rs,Xs,Rt,Xt)

    # Rs < Rt
    else:
        reactances['reversed'] = calcReversedReactances(Rs,Xs,Rt,Xt)
        if abs(Xs) >= sqrt(Rs*(Rt-Rs)):
            # Normal and reversed
            reactances['normal'] = calcNormalReactances(Rs,Xs,Rt,Xt)

    # print resulting networks
    if 'normal' in reactances.keys():
        print(f"Network: normal")
        X11, X12, X21, X22, Q = reactances['normal']

        ParElem1_name, ParElem1_value, ParElem1_unit = getParallelElement(X11,f0)
        SerElem1_name, SerElem1_value, SerElem1_unit = getSerialElement(X21,f0)
        ParElem2_name, ParElem2_value, ParElem2_unit = getParallelElement(X12,f0)
        SerElem2_name, SerElem2_value, SerElem2_unit = getSerialElement(X22,f0)

        networks.append(printFormater(nameShunt=ParElem1_name, nameSerial=SerElem1_name, 
                valueShunt=ParElem1_value, valueSerial=SerElem1_value,
                unitShunt=ParElem1_unit, unitSerial=SerElem1_unit, networktype='normal'))
        
        if ParElem1_value != ParElem2_value and SerElem1_value != SerElem2_value:
            networks.append(printFormater(nameShunt=ParElem2_name, nameSerial=SerElem2_name, 
                    valueShunt=ParElem2_value, valueSerial=SerElem2_value,
                    unitShunt=ParElem2_unit, unitSerial=SerElem2_unit, networktype='normal'))
    
    if 'reversed' in reactances.keys():
        print(f"Network: reversed")
        X11, X12, X21, X22, Q = reactances['reversed']

        ParElem1_name, ParElem1_value, ParElem1_unit = getParallelElement(X11,f0)
        SerElem1_name, SerElem1_value, SerElem1_unit = getSerialElement(X21,f0)
        ParElem2_name, ParElem2_value, ParElem2_unit = getParallelElement(X12,f0)
        SerElem2_name, SerElem2_value, SerElem2_unit = getSerialElement(X22,f0)

        networks.append(printFormater(nameShunt=ParElem1_name, nameSerial=SerElem1_name, 
                valueShunt=ParElem1_value, valueSerial=SerElem1_value,
                unitShunt=ParElem1_unit, unitSerial=SerElem1_unit, networktype='reversed'))
        
        if ParElem1_value != ParElem2_value and SerElem1_value != SerElem2_value:
            networks.append(printFormater(nameShunt=ParElem2_name, nameSerial=SerElem2_name, 
                    valueShunt=ParElem2_value, valueSerial=SerElem2_value,
                    unitShunt=ParElem2_unit, unitSerial=SerElem2_unit, networktype='reversed'))
    
    plotSmithChart(Z=pair, networks=networks)
