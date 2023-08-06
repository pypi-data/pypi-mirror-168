import handyplot
import math
import numpy as np


class UnitTest:
    @staticmethod
    def figure():
        figure_1 = handyplot.SingleFigure()
        base = np.linspace(0, math.pi*2, num=100)
        # figure_1.add_line(base, np.cos(base), "1")
        figure_1.add_line(base, np.cos(base-0.5), "2")
        figure_1.add_line_scatter(base, np.cos(base-0.5), "2", color=figure_1.get_color("green"))
        # figure_1.add_line(base, np.cos(base-1.0), "3")
        # figure_1.add_line(base, np.cos(base-1.5), "4")
        # figure_1.add_line(base, np.cos(base-2.0), "5")
        # figure_1.add_line(base, np.cos(base-2.5), "6")
        # figure_1.add_line(base, np.cos(base-3.0), "7")
        # figure_1.add_line(base, np.cos(base-3.5), "8")
        figure_1.set_x_label("dfadafadafs")
        figure_1.set_y_label("yasdfafdfass")
        figure_1.set_y_limit([-1.2, 1.2], 6)
        figure_1.set_x_limit([0, math.pi*2], 8)
        figure_1.add_legend((0.1, 0.1), 2, "legend")
        # figure_1.set_x_limit([0, math.pi*2])
        figure_1.open_grid()
        figure_1.show()
        # figure_1.save("test.tiff")


if __name__=="__main__":
    UnitTest.figure()
