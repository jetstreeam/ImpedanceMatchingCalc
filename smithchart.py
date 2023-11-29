#%%
import numpy as np
import matplotlib.pyplot as plt

class SmithChart:
    """
    Object-oriented Smith Chart drawing.
    """

    def __init__(self, fig, ax, Z0=50):
        """
        Creates the figure and draws the grid.
        Z0: characteristic impedance
        """
        #plt.ioff()
        self.Z0 = Z0
        self.fig = fig
        self.ax = ax
        self.ax.set_axis_off()
        self.drawGrid()

    '''def show(self):
        """
        Shows the plot. The plot can't be updated after it has been closed.
        """
        plt.show()'''

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
        #plt.draw()

    def drawXCircle(self, x, npts=200):
        """
        Draws a circle with constant real part of impedance.
        """
        zlst = [x] + [complex(x, z) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, 'r')

        zlst = [x] + [complex(x, -z) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, 'r')

    def drawYCircle(self, y, npts=200):
        """
        Draws a circle with constant imaginary part.
        """
        zlst = [complex(0, y)] + [complex(z, y) for z in np.logspace(0, 6, npts)]
        self.drawZList(zlst, 'b')

    def markZ(self, z, text=None, c='b', size=1):
        """
        Marks an impedance with a dot.
        """
        g = self.z2gamma(z)
        self.ax.plot(g.real, g.imag, 'o' + c)
        if text:
            self.ax.text(g.real + 0.02, g.imag + 0.02, text, color=c, weight='demi')
        #plt.draw()

    def drawGrid(self):
        """
        Draws the Smith Chart grid.
        """
        self.drawXCircle(0)
        self.drawXCircle(self.Z0/5)
        self.drawXCircle(self.Z0/2)
        self.drawXCircle(self.Z0)
        self.drawXCircle(self.Z0*2)
        self.drawXCircle(self.Z0*5)
        self.drawYCircle(0)
        self.drawYCircle(self.Z0/5)
        self.drawYCircle(-self.Z0/5)
        self.drawYCircle(self.Z0/2)
        self.drawYCircle(-self.Z0/2)
        self.drawYCircle(self.Z0)
        self.drawYCircle(-self.Z0)
        self.drawYCircle(self.Z0*2)
        self.drawYCircle(-self.Z0*2)
        self.drawYCircle(self.Z0*5)
        self.drawYCircle(-self.Z0*5)

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
    fig, ax = plt.subplots(figsize=(8.0, 8.0))
    smith_chart = SmithChart(fig=fig, ax=ax)
    smith_chart.markZ(20+30j)
    smith_chart.markZ(130-60j, text='Z1', c='r')
    smith_chart.markZ(1-100j)

    #smith_chart.show()
