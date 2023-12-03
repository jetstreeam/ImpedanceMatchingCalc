#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle


class SmithChart:
    """
    Object-oriented Smith Chart drawing.
    """

    def __init__(self, fig:plt.figure, ax:plt.axis, Z0=50):
        """
        Creates the figure and draws the grid.
        Z0: characteristic impedance
        """
        self.Z0 = Z0
        self.fig = fig
        self.ax = ax
        self.ax.set_axis_off()
        self.drawGrid()
        self.set_z0_text()

    def save(self, filename):
        """
        Saves the plot to filename. The extension defines the filetype.
        """
        self.fig.savefig(filename)

    def drawZList(self, l, c='y'):
        """
        Draws a list of impedances on the chart and connects them by lines. 
        To get a closed contour, the last impedance should be the same as the 
        first one. Use color c for the drawing.
        """
        xlst = [self.z2gamma(z).real for z in l]
        ylst = [self.z2gamma(z).imag for z in l]
        self.ax.plot(xlst, ylst, c)

    def drawXCircle(self, x, format=':r', npts=200):
        """
        Draws a circle with constant real part of impedance.
        """
        zlst = [x] + [complex(x, z) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, format)

        zlst = [x] + [complex(x, -z) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, format)

    def drawYCircle(self, y, format=':r', npts=200):
        """
        Draws a circle with constant imaginary part.
        """
        zlst = [complex(0, y)] + [complex(z, y) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, format)

    def markZ(self, z, text=None, c='b'):
        """
        Marks an impedance with a dot.
        """
        g = self.z2gamma(z)
        self.ax.plot(g.real, g.imag, 'o' + c)
        if text:
            self.ax.text(g.real + 0.02, g.imag + 0.02, text, color=c, weight='demi')

    def drawGrid(self):
        """
        Draws the Smith Chart grid.
        """
        self.drawXCircle(0,'-k')
        self.drawXCircle(self.Z0/5,':r')
        self.drawXCircle(self.Z0/2,':r')
        self.drawXCircle(self.Z0,':r')
        self.drawXCircle(self.Z0*2,':r')
        self.drawXCircle(self.Z0*5,':r')
        self.drawXCircle(self.Z0*10,':r')
        self.drawYCircle(0,':k')
        self.drawYCircle(self.Z0/5,':r')
        self.drawYCircle(-self.Z0/5,':r')
        self.drawYCircle(self.Z0/2,':r')
        self.drawYCircle(-self.Z0/2,':r')
        self.drawYCircle(self.Z0,':r')
        self.drawYCircle(-self.Z0,':r')
        self.drawYCircle(self.Z0*2,':r')
        self.drawYCircle(-self.Z0*2,':r')
        self.drawYCircle(self.Z0*5,':r')
        self.drawYCircle(-self.Z0*5,':r')

    def set_z0_text(self):
        box = Rectangle(xy=(0.7, 1), width=0.3, height=0.1, ec='black', fc='none',)
        self.ax.add_patch(box)
        rx, ry = box.get_xy()
        tx = rx + box.get_width() / 2.0
        ty = ry + box.get_height() / 2.0
        self.z0_text = self.ax.annotate(f"$Z_0:$ {self.Z0}", (tx, ty), color='black',
                                        fontsize=10, ha='center', va='center')

    def set_zstart_text(self, zs):
        text = f"$Z_{{start}}:${zs}Ω"
        self.ax.annotate(text, (-1, -1), color='r', fontsize=10, ha='left', va='center')

    def set_ztarget_text(self, zt):
        text = f"$Z_{{target}}:${zt}Ω"
        self.ax.annotate(text, (0.6, -1), color='g', fontsize=10, ha='left', va='center')

    def set_components_text(self, components:str):
        self.ax.annotate(f"[1] {components.split(',')[0].strip()}", (-1, 1.1), color='black', fontsize=10, ha='left', va='center')
        self.ax.annotate(f"[2] {components.split(',')[1].strip()}", (-1, 1), color='black', fontsize=10, ha='left', va='center')

    def z2gamma(self, zl):
        """
        Converts an impedance to a reflection coefficient.
        """
        return complex(zl - self.Z0) / (zl + self.Z0)

    def y2gamma(self, y1):
        """
        Converts an admittance to a reflection coefficient.
        """
        return complex(y1 - 1 / self.Z0) / (y1 + 1 / self.Z0)

if __name__ == '__main__':
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16.0, 8.0))
    
    sc1 = SmithChart(fig=fig, ax=ax1)
    sc1.markZ(20+0j, text='', c='r')
    sc1.markZ(50+0j, text='', c='g')

    sc1 = SmithChart(fig=fig, ax=ax2)
    sc1.markZ(20+0j, text='', c='r')
    sc1.markZ(50+0j, text='', c='g')

    #smith_chart.show()
