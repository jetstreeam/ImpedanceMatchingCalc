#%%
print(2**4)

n = 50 + 7j

print(n.real)
print(n.imag)

#%%
import numpy as np

f_0 = 2440e6
f_0_str = '2440MHz'
Z_0 = 50

# --- 20+0j -> 50+0j ---

Z_s1 = 20+0j
Y_s1 = 1/Z_s1
Z_t1 = 50+0j
Y_t1 = 1/Z_t1

# series L with shunt C
zs10 = 0.5*50
Ls10 = zs10/(2*np.pi*f_0)*1e9
zp10 = 1/(1.22*1/50)
Cp10 = 1/(2*np.pi*f_0*zp10)*1e12

# series C with shunt L
zs11 = 0.5*50
Cs11 = 1/(2*np.pi*f_0*zs11)*1e12
zp11 = 1/(1.22*1/50)
Lp11 = zp11/(2*np.pi*f_0)*1e9

# --- 20-10j -> 60+60j ---

Z_s2 = 20-10j
Y_s2 = 1/Z_s2
Z_t2 = 60+60j
Y_t2 = 1/Z_t2

# series L with shunt C
zs20 = 1.175*50
Ls20 = zs20/(2*np.pi*f_0)*1e9
zp20 = 1/(0.95*1/50)
Cp20 = 1/(2*np.pi*f_0*zp20)*1e12

# series C with shunt L
zs21 = 0.875*50
Cs21 = 1/(2*np.pi*f_0*zs21)*1e12
zp21 = 1/(0.65*1/50)
Lp21 = zp21/(2*np.pi*f_0)*1e9

# --- 100+75j -> 30+0j ---

Z_s3 = 100+75j
Y_s3 = 1/Z_s3
Z_t3 = 30+0j
Y_t3 = 1/Z_t3

# shunt L with series C
zp30 = 1/(0.23*1/50)
Lp30 = zp30/(2*np.pi*f_0)*1e9
zs30 = 1.23*50
Cs30 = 1/(2*np.pi*f_0*zs30)*1e12

# shunt C with series L
zp31 = 1/(0.9*1/50)
Cp31 = 1/(2*np.pi*f_0*zp31)*1e12
zs31 = 1.2*50
Ls31 = zs31/(2*np.pi*f_0)*1e9



print("-----")
print(f"Z_s1: {Z_s1:.3g}, Z_t1: {Z_t1:.3g}, Y_s1: {Y_s1:.3g}, Y_t1: {Y_t1:.3g}")
print(f"Z_s2: {Z_s2:.3g}, Z_t2: {Z_t2:.3g}, Y_s2: {Y_s2:.3g}, Y_t2: {Y_t2:.3g}")
print(f"Z_s3: {Z_s3:.3g}, Z_t3: {Z_t3:.3g}, Y_s3: {Y_s3:.3g}, Y_t3: {Y_t3:.3g}")
print("-----")
print(f"Ls1: {Ls10:.3g}nH; Cp1:{Cp10:.3g}pF")
print(f"Cs1: {Cs11:.3g}pF; Lp1:{Lp11:.3g}nH")
print(f"Ls2: {Ls20:.3g}nH; Cp2:{Cp20:.3g}pF")
print(f"Cs2: {Cs21:.3g}pF; Lp2:{Lp21:.3g}nH")
print(f"Lp3: {Lp30:.3g}nH; Cs3:{Cs30:.3g}pF")
print(f"Cp3: {Cp31:.3g}pF; Ls3:{Ls31:.3g}nH")
print("-----")






#%%
import matching_network as mn

Z_s1 = 20+0j
Z_t1 = 50+0j
f_0 = 2440e6

'''s1 = mn.L_section_matching(Z_s1, Z_t1, f_0)
s1.match()

Z_s2 = 20-10j
Z_t2 = 60+60j
s2 = mn.L_section_matching(Z_s2, Z_t2, f_0)
s2.match()'''

Z_s3 = 100+75j
Z_t3 = 30+0j
s3= mn.L_section_matching(Z_s3, Z_t3, f_0)
s3.match()






#%%
from math import sqrt
import numpy as np

Z_0 = 50
f0 = 2.44e9

'''
Z_s = 20-10j
Z_t = 60+60j
'''
'''
Z_s = 20+0j
Z_t = 50+0j
'''
Z_s = 100+75j
Z_t = 30*0j

Rl = Z_t.real
Xl = Z_t.imag

A = (Z_s.real - Z_t.real) / (Z_s.real + Z_t.real)
B = (Z_s.imag-Z_t.imag) / (Z_s.imag + Z_t.imag)

L = (B*Z_s.imag)/(2*np.pi*f0) * 1e9
C = (B*Z_s.real)/(2*np.pi*f0) * 1e12
print(f"L={L:.3g}nH C={C:.3g}pF")




#%%
from math import sqrt
import numpy as np

Z_0 = 50
f0 = 2.44e9

'''
Z_s = 20-10j
Z_t = 60+60j
'''
'''
Z_s = 20+0j
Z_t = 50+0j
'''
Z_s = 100+75j
Z_t = 30*0j

Rl = Z_t.real
Xl = Z_t.imag

# *** for Rt > Rs ***
if (Rl > Z_s.real):

    # calculate shunt susceptance
    B1 = (Xl + sqrt(Rl/Z_0)*sqrt(Rl*(Rl-Z_0)+Xl**2))/(Rl**2+Xl**2)
    B2 = (Xl - sqrt(Rl/Z_0)*sqrt(Rl*(Rl-Z_0)+Xl**2))/(Rl**2+Xl**2)

    # calculate series reactance
    X1 = (1/B1) + (Xl*Z_0)/Rl - Z_0/(B1*Rl)
    X2 = (1/B2) + (Xl*Z_0)/Rl - Z_0/(B1*Rl)

    # series L with shunt C
    Ls1 = X1/(2*np.pi*f0) if X1/(2*np.pi*f0) > 0 else X2/(2*np.pi*f0)
    Cp1 = B1/(2*np.pi*f0) if B1/(2*np.pi*f0) > 0 else B2/(2*np.pi*f0)
    Ls1 *= 1e9
    Cp1 *= 1e12
    print(f"series L with shunt C: Ls={Ls1:.3g}nH Cp={Cp1:.3g}pF")

    # series C with shunt L
    Cs1 = 1/(2*np.pi*f0*X1) if 1/(2*np.pi*f0*X1) > 0 else 1/(2*np.pi*f0*X2)
    Lp1 = 1/(2*np.pi*f0*B1) if 1/(2*np.pi*f0*B1) > 0 else 1/(2*np.pi*f0*B2)
    Lp1 *= 1e9
    Cs1 *= 1e12
    print(f"series C with shunt L: Cs={Cs1:.3g}pF Lp={Lp1:.3g}nH")

    # series C with shunt C
    Cs2 = 1/(2*np.pi*f0*X1) if 1/(2*np.pi*f0*X1) > 0 else 1/(2*np.pi*f0*X2)
    Cp2 = B1/(2*np.pi*f0) if B1/(2*np.pi*f0) > 0 else B2/(2*np.pi*f0)
    Cs2 *= 1e12
    Cp2 *= 1e12
    print(f"series C with shunt C: Cs={Cs2:.3g}pF Cp={Cp2:.3g}pF")

    # series L with shunt L
    Ls2 = X1/(2*np.pi*f0) if X1/(2*np.pi*f0) > 0 else X2/(2*np.pi*f0)
    Lp2 = 1/(2*np.pi*f0*B1) if 1/(2*np.pi*f0*B1) > 0 else 1/(2*np.pi*f0*B2)
    Ls2 *= 1e9
    Lp2 *= 1e9
    print(f"series L with shunt L: Ls={Ls2:.3g}nH Lp={Lp2:.3g}nH")

# *** for Rt < Rs ***
else:
    # calculate shunt susceptance
    B1 = (1/Z_0)*sqrt((Z_0-Rl)/Rl)
    B2 = (-1/Z_0)*sqrt((Z_0-Rl)/Rl)

    # calculate series reactance
    X1 = sqrt(Rl*(Z_0-Rl))-Xl
    X2 = (-1)*sqrt(Rl*(Z_0-Rl))-Xl

    # shunt C with series L
    Ls1 = X1/(2*np.pi*f0) if X1/(2*np.pi*f0) > 0 else X2/(2*np.pi*f0)
    Cp1 = B1/(2*np.pi*f0) if B1/(2*np.pi*f0) > 0 else B2/(2*np.pi*f0)
    Ls1 *= 1e9
    Cp1 *= 1e12
    print(f"shunt C with series L: Cp={Cp1:.3g}pF Ls={Ls1:.3g}nH")

    # shunt L with series C
    Cs1 = 1/(2*np.pi*f0*X1) if 1/(2*np.pi*f0*X1) > 0 else 1/(2*np.pi*f0*X2)
    Lp1 = 1/(2*np.pi*f0*B1) if 1/(2*np.pi*f0*B1) > 0 else 1/(2*np.pi*f0*B2)
    Lp1 *= 1e9
    Cs1 *= 1e12
    print(f"shunt L with series C: Lp={Lp1:.3g}nH Cs={Cs1:.3g}pF")

    # series C with shunt C
    Cs2 = 1/(2*np.pi*f0*X1) if 1/(2*np.pi*f0*X1) > 0 else 1/(2*np.pi*f0*X2)
    Cp2 = B1/(2*np.pi*f0) if B1/(2*np.pi*f0) > 0 else B2/(2*np.pi*f0)
    Cs2 *= 1e12
    Cp2 *= 1e12
    print(f"shunt C with series C: Cp={Cp2:.3g}pF Cs={Cs2:.3g}pF")

    # series L with shunt L
    Ls2 = X1/(2*np.pi*f0) if X1/(2*np.pi*f0) > 0 else X2/(2*np.pi*f0)
    Lp2 = 1/(2*np.pi*f0*B1) if 1/(2*np.pi*f0*B1) > 0 else 1/(2*np.pi*f0*B2)
    Ls2 *= 1e9
    Lp2 *= 1e9
    print(f"shunt L with series L: Lp={Lp2:.3g}nH Ls={Ls2:.3g}nH")




























#%%

import plotly.graph_objects as go

fig = go.Figure()

fig = go.Figure(go.Scattersmith(
    imag=[1],
    real=[1],
    marker_symbol='x',
    marker_size=10,
    
    marker_color="red",
    subplot="smith1"
))


fig.update_layout(
    smith=dict(
        realaxis_gridcolor='red',
        imaginaryaxis_gridcolor='blue'
    )
)


fig.show()


#%%




import plotly as ply
import plotly.graph_objects as go
import numpy as np


def calc_circle(c, r):
  theta = np.linspace(0, 2*np.pi, 1000)
  print(c + r*np.exp(1.0j*theta))
  return c + r*np.exp(1.0j*theta)

c,r= 1,1

fig = go.Figure(go.Scattersmith(imag=np.imag(calc_circle(c, r)), 
                                    real=np.real(calc_circle(c, r)),
                                    marker_color="blue",
                                    showlegend=True,
                                    name='Hello'))
fig.show()





#%%

%matplotlib inline

# get the example data file path in skrf
# you can add a path to your own file instead
import skrf as rf
from skrf import Network
import os
skrfpath = os.path.dirname(rf.__file__)
#datafile = os.path.join(skrfpath, 'data', 'ntwk1.s2p')
datafile = os.path.join(os.curdir, 'PMA-5454+.s2p')
print(datafile)

# create a network object with
# rf.Network(/path/to/filename.s2p)
nw = rf.Network(datafile)

ring_slot = nw
ring_slot.plot_s_smith()


# print it
print(nw)

