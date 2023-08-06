import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


class FigureBase:
    def __init__(self):
        mpl.rcParams["axes.autolimit_mode"] = "round_numbers"  # This expands the axis limits to the next round number.
        mpl.rcParams["font.family"] = ["Arial"]  # Set global font.
        mpl.rcParams["font.size"] = 9  # Set global font size.

        self._basic_color_list = []
        self._fig = None
        self._lines_num = 0
        self._use_color = self._basic_color_list

        self.__load_colors()

    def save(self, filename):
        self._fig.savefig(filename, dpi=600)

    def show(self):
        self._fig.show()

    def __load_colors(self):
        self._basic_color_list.append((234/255, 112/255, 112/255, 1))  # Red.
        self._basic_color_list.append((38/255, 148/255, 171/255, 1))  # Blue.
        self._basic_color_list.append((178/255, 222/255, 129/255, 1))  # Fresh green.
        self._basic_color_list.append((229/255, 149/255, 114/255, 1))  # Orange.
        self._basic_color_list.append((150/255, 206/255, 180/255, 1))  # Light green.
        self._basic_color_list.append((184/255, 108/255, 153/255, 1))  # purple.
        self._basic_color_list.append((153/255, 171/255, 185/255, 1))  # Gray.
        self._basic_color_list.append((194/255, 157/255, 115/255, 1))  # Brown.


class SingleFigure(FigureBase):
    def __init__(self):
        FigureBase.__init__(self)

        self._fig, self._axes = plt.subplots()

    def add_legend(self, loc="best", ncol=1):
        self._axes.legend(loc=loc, ncol=ncol)

    def add_line(self, base, data, label=None):
        line, = self._axes.plot(base, data, color=self._use_color[self._lines_num%len(self._use_color)])

        if label is not None:
            line.set_label(label)

        self._lines_num += 1

    def add_points(self, base, data, label=None):
        scatter = self._axes.scatter(base, data)

        if label is not None:
            scatter.set_label(label)

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