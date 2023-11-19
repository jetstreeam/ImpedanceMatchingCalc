#%%

import numpy as np  # for np.allclose() to check that S-params are similar
import skrf as rf
rf.stylely()

'''# reference LC circuit made in Designer
LC_designer = rf.Network('designer_capacitor_30_80MHz_simple.s2p')

# scikit-rf: manually connecting networks
line = rf.media.DefinedGammaZ0(frequency=LC_designer.frequency, z0=50)
LC_manual = line.inductor(24e-9) ** line.capacitor(70e-12)

# scikit-rf: using Circuit builder
port1 = rf.Circuit.Port(frequency=LC_designer.frequency, name='port1', z0=50)
port2 = rf.Circuit.Port(frequency=LC_designer.frequency, name='port2', z0=50)
cap = rf.Circuit.SeriesImpedance(frequency=LC_designer.frequency, name='cap', z0=50,
                                 Z=1/(1j*LC_designer.frequency.w*70e-12))
ind = rf.Circuit.SeriesImpedance(frequency=LC_designer.frequency, name='ind', z0=50,
                                 Z=1j*LC_designer.frequency.w*24e-9)
'''
# NB: it is also possible to create 2-port lumped elements like:
# line = rf.media.DefinedGammaZ0(frequency=LC_designer.frequency, z0=50)
# cap = line.capacitor(70e-12, name='cap')
# ind = line.inductor(24e-9, name='ind')

LC_designer = rf.Network('mynetwk.s2p')
print(LC_designer.frequency)

port1 = rf.Circuit.Port(frequency=LC_designer.frequency, name='port1', z0=50)
port2 = rf.Circuit.Port(frequency=LC_designer.frequency, name='port2', z0=50)
cap = rf.Circuit.SeriesImpedance(frequency=LC_designer.frequency, name='cap', z0=50,
                                 Z=1/(1j*LC_designer.frequency.w*1.17e-12))
ind = rf.Circuit.SeriesImpedance(frequency=LC_designer.frequency, name='ind', z0=50,
                                 Z=1j*LC_designer.frequency.w*4.01e-9)


connections = [
    [(port1, 0), (cap, 0)],
    [(cap, 1), (ind, 0)],
    [(ind, 1), (port2, 0)]
]

circuit = rf.Circuit(connections)
LC_from_circuit = circuit.network

'''# testing the equivalence of the results
print(np.allclose(LC_designer.s, LC_manual.s))
print(np.allclose(LC_designer.s, LC_from_circuit.s))'''

#circuit.plot_graph(network_labels=True, edge_labels=True, port_labels=True)
ring_slot = circuit.network
ring_slot.plot_s_smith()


#%%

import skrf as rf
import matplotlib.pyplot as plt


# Matching with Lumped Elements
# Let’s assume the load is 200 + 0j for a line Z_0 = 50 ohm  at the frequency of 6 MHz.
Z_L = 200 + 0j
Z_0 = 50

# frequency band centered on the frequency of interest
frequency = rf.Frequency(start=6, stop=16, npoints=401, unit='MHz')
frequency = rf.Network('mynetwk.s2p').frequency

# transmission line Media
line = rf.DefinedGammaZ0(frequency=frequency, z0=Z_0)

# Static inductor loads
# initial guess values
Cp=1.17e-12
Ls=4.01e-9
zS=100+75j
zL=30+0j

ntwk_Cp = line.capacitor(Cp, name='Cp')
ntwk_Ls = line.inductor(Ls, name='Ls')

port1 = rf.Circuit.Port(frequency, name='Port1', z0=zS)
port2 = rf.Circuit.Port(frequency, name='Port2', z0=zL)
gnd1 = rf.Circuit.Ground(frequency, name='gnd1')

cir = [
    [(port1, 0), (ntwk_Cp, 0), (ntwk_Ls, 0)],
    [(ntwk_Ls, 1), (port2, 0)],
    [(ntwk_Cp, 1), (gnd1, 0)]
]

cir = rf.Circuit(cir)

'''# Voltage at C2 vs frequency
power = [1]  # W
phase = [0]  # deg
voltages = cir.voltages(power, phase)

fig, ax = plt.subplots()
ax.plot(frequency.f_scaled, voltages[:, 6])  # 6 found from cir.connections_list '''
#cir.plot_graph(network_labels=True, edge_labels=True, port_labels=True)

ring_slot = cir.network
print(ring_slot)
ring_slot.plot_s_smith(draw_labels=True, m=1, n=0)
