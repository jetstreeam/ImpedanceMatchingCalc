#%%
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle

class SmithChart:
    """
    Object-oriented Smith Chart drawing.
    """

    def __init__(self, fig: plt.figure, ax: plt.axis, Z0=50):
        """
        Creates the figure and draws the grid.
        
        Parameters:
        - fig: matplotlib figure
        - ax: matplotlib axis
        - Z0: system impedance
        """
        self.Z0 = Z0
        self.fig = fig
        self.ax = ax
        self.ax.set_axis_off()
        self.ax.axis(np.array([-1.1, 1.1, -1.1, 1.1]))
        self.draw_grid()
        self.print_z0()

    def save(self, filename):
        """
        Saves the plot to filename. The extension defines the filetype.
        
        Parameters:
        - filename: str, the name of the file to save
        """
        self.fig.savefig(filename)

    def drawZcircles(self):
        """
        Draws impedance circles on the Smith Chart.
        """
        for const in [0.2, 0.5, 1, 2, 5, 10]:
            # Draw Constant Real Impedance Circles
            center_impedance = (const / (const + 1), 0)
            radius_impedance = 1 / (const + 1)
            circle_impedance = Circle(center_impedance, radius_impedance, fc='none', ec='r', ls=':')
            self.ax.add_patch(circle_impedance)

            # Draw Constant Imaginary Impedance Circles
            i_center_impedance = (1, 1 / const)
            i_center_neg_impedance = (1, -1 / const)
            i_radius = 1 / const
            circle_imaginary = Circle(i_center_impedance, i_radius, fc='none', ec='r', ls=':')
            circle_imaginary.set_clip_path(self.smith_border)
            neg_circle_imaginary = Circle(i_center_neg_impedance, i_radius, fc='none', ec='r', ls=':')
            neg_circle_imaginary.set_clip_path(self.smith_border)
            self.ax.add_patch(circle_imaginary)
            self.ax.add_patch(neg_circle_imaginary)

    def drawYcircles(self):
        """
        Draws admittance circles on the Smith Chart.
        """
        for const in [0.2, 0.5, 1, 2, 5, 10]:
            # Draw Constant Real Admittance Circles
            center_admittance = (- (const / (const + 1)), 0)
            radius_admittance = 1 / (const + 1)
            circle_admittance = Circle(center_admittance, radius_admittance, fc='none', ec='b', ls=':')
            self.ax.add_patch(circle_admittance)

            # Draw Constant Imaginary Admittance Circles
            i_center_admittance = (-1, 1 / const)
            i_center_neg_admittance = (-1, -1 / const)
            i_radius_admittance = 1 / const
            circle_imaginary_admittance = Circle(i_center_admittance, i_radius_admittance, fc='none', ec='b', ls=':')
            circle_imaginary_admittance.set_clip_path(self.smith_border)
            neg_circle_imaginary_admittance = Circle(i_center_neg_admittance, i_radius_admittance, fc='none', ec='b', ls=':')
            neg_circle_imaginary_admittance.set_clip_path(self.smith_border)
            self.ax.add_patch(circle_imaginary_admittance)
            self.ax.add_patch(neg_circle_imaginary_admittance)

    def markZ(self, z, text=None, c='b'):
        """
        Marks an impedance with a dot.
        
        Parameters:
        - z: complex, impedance value
        - text: str, text to annotate the dot
        - c: str, color of the dot
        """
        g = self.z2gamma(z)
        self.ax.plot(g.real, g.imag, 'o' + c)
        if text:
            self.ax.text(g.real + 0.02, g.imag + 0.02, text, color=c, weight='demi')

    def draw_grid(self):
        """
        Draws the Smith Chart grid.
        """ 
        # draw outer smithchart border
        self.smith_border = Circle((0, 0), 1, fc='none', ec='k')
        self.ax.add_patch(self.smith_border)

        # draw horizontal line
        line = FancyArrowPatch((-1, 0), (1, 0))
        self.ax.add_patch(line)

        # draw impedance circles
        self.drawZcircles()
        # draw admittance circles
        self.drawYcircles()

    def print_z0(self):
        """
        Prints the system impedance in the smith chart.
        """
        box = Rectangle(xy=(0.7, 1), width=0.3, height=0.1, ec='k', fc='none',)
        self.ax.add_patch(box)
        rx, ry = box.get_xy()
        tx = rx + box.get_width() / 2.0
        ty = ry + box.get_height() / 2.0
        self.z0_text = self.ax.annotate(f"$Z_0:$ {self.Z0}Ω", (tx, ty), color='k',
                                        fontsize=10, ha='center', va='center')

    def print_zstart(self, zs):
        """
        Prints the start impedance in the smith chart.
        
        Parameters:
        - zs: complex, start impedance value
        """
        text = f"$Z_{{start}}:${zs}Ω"
        self.ax.annotate(text, (-1, -1), color='r', fontsize=10, ha='left', va='center')

    def print_ztarget(self, zt):
        """
        Prints the target impedance in the smith chart.
        
        Parameters:
        - zt: complex, target impedance value
        """
        text = f"$Z_{{target}}:${zt}Ω"
        self.ax.annotate(text, (0.6, -1), color='g', fontsize=10, ha='left', va='center')

    def set_components_text(self, components: str):
        """
        Prints the components text in the smith chart.
        
        Parameters:
        - components: str, components used for impedance matching
        """
        self.ax.annotate(f"[1] {components.split(',')[0].strip()}", (-1, 1.1), color='k', fontsize=10, ha='left', va='center')
        self.ax.annotate(f"[2] {components.split(',')[1].strip()}", (-1, 1), color='k', fontsize=10, ha='left', va='center')

    def z2gamma(self, zl):
        """
        Converts an impedance to a reflection coefficient.
        
        Parameters:
        - zl: complex, impedance value
        
        Returns:
        - complex, reflection coefficient
        """
        return complex(zl - self.Z0) / (zl + self.Z0)

    def y2gamma(self, y1):
        """
        Converts an admittance to a reflection coefficient.
        
        Parameters:
        - y1: float, admittance value
        
        Returns:
        - complex, reflection coefficient
        """
        return complex(y1 - 1 / self.Z0) / (y1 + 1 / self.Z0)

if __name__ == '__main__':
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(16.0, 8.0))
    sc1 = SmithChart(fig=fig, ax=ax1)
    sc1.markZ(20 + 0j, text='', c='r')
    sc1.markZ(50 + 0j, text='', c='g')

    sc1 = SmithChart(fig=fig, ax=ax2)
    sc1.markZ(20 + 0j, text='', c='r')
    sc1.markZ(50 + 0j, text='', c='g')