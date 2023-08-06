import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class FigureBase:
    def __init__(self):
        mpl.rcParams["axes.autolimit_mode"] = "round_numbers"  # This expands the axis limits to the next round number.
        mpl.rcParams["font.family"] = ["Arial"]  # Set global font.
        mpl.rcParams["font.size"] = 9  # Set global font size.

        self._fig = None
        self._color_num = 8
        self._colors = []
        self._line_num = 0
        self._line_scatter_num = 0

        self.__load_colors()

    def get_color(self, color_name):
        if color_name=="red":
            return self._colors[0]
        elif color_name=="blue":
            return self._colors[1]
        elif color_name=="fresh_green":
            return self._colors[2]
        elif color_name=="orange":
            return self._colors[3]
        elif color_name=="green":
            return self._colors[4]
        elif color_name=="purple":
            return self._colors[5]
        elif color_name=="gray":
            return self._colors[6]
        elif color_name=="brown":
            return self._colors[7]
        else:
            assert False, "[handyplot error] <FigureBase> <get_color> There isn't this kind of color."

    def save(self, filename):
        self._fig.savefig(filename, dpi=600)

    def show(self):
        self._fig.show()

    def __load_colors(self):
        self._colors.append((234/255, 112/255, 112/255, 1))  # Red.
        self._colors.append((38/255, 148/255, 171/255, 1))  # Blue.
        self._colors.append((178/255, 222/255, 129/255, 1))  # Fresh green.
        self._colors.append((229/255, 149/255, 114/255, 1))  # Orange.
        self._colors.append((126/255, 188/255, 89/255, 1))  # Green.
        self._colors.append((184/255, 108/255, 153/255, 1))  # purple.
        self._colors.append((153/255, 171/255, 185/255, 1))  # Gray.
        self._colors.append((194/255, 157/255, 115/255, 1))  # Brown.


class SingleFigure(FigureBase):
    def __init__(self):
        FigureBase.__init__(self)

        self._fig, self._axes = plt.subplots()

    def add_legend(self, loc="best", ncol=1, title=None):
        self._axes.legend(loc=loc, ncol=ncol, title=title)

    def add_line(self, base, data, label=None, color=None):
        if color is None:
            color = self._colors[self._line_num%self._color_num]

        line, = self._axes.plot(base, data, color=color)

        if label is not None:
            line.set_label(label)

        self._line_num += 1

    def add_line_scatter(self, base, data, label=None, color=None):
        if color is None:
            color = self._colors[self._line_scatter_num%self._color_num+1]

        scatter, = self._axes.plot(base, data, color=(0, 0, 0, 0), marker="o", markeredgecolor=color)

        if label is not None:
            scatter.set_label(label)

        self._line_scatter_num += 1

    def open_grid(self):
        self._axes.grid(color=(235/255, 235/255, 235/255))

    def set_title(self, title):
        self._axes.set_title(title)

    def set_x_label(self, text):
        self._axes.set_xlabel(text)

    def set_x_limit(self, range, segment_num=None):
        self._axes.set_xlim(range)
        if segment_num is not None:
            self._axes.xaxis.set_ticks(np.linspace(range[0], range[1], segment_num+1))

    def set_y_label(self, text):
        self._axes.set_ylabel(text)

    def set_y_limit(self, range, segment_num=None):
        self._axes.set_ylim(range)
        if segment_num is not None:
            self._axes.yaxis.set_ticks(np.linspace(range[0], range[1], segment_num+1))