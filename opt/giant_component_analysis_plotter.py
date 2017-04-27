__author__ = 'marcos'
import numpy
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from itertools import cycle


class GiantComponentDeathPlotter:
    def __init__(self):
        pass

    @staticmethod
    def giant_component_death_curve(
            calculate_on, pd_datas, xlim=None, ylim=None, figsize=None, tight_layout=None, count='components'):
        if figsize:
            fig = plt.figure(figsize=figsize)
        else:
            fig = plt.figure()
        plot_gridspec = gridspec.GridSpec(3, 3, width_ratios=[1, 0.001, 1], height_ratios=[1, 0.001, 1])
        graphs_index = 0
        if count == 'components':
            ylabel = "Number of components"
        else:
            ylabel = "Giant component size"
        xlabel = "Normalized edge weight"
        markers = [
            'D', 's', 'x', '^', 'd', 'h', '+', '*', ',', 'o', '.', '1', 'p', '3', '2', '4', 'H', 'v', '8', '<', '>']
        colorblind = [(0, 0, 0), (230, 159, 0), (86, 180, 233), (0, 158, 115), (240, 228, 66), (0, 114, 178), (213, 94, 0), (204, 121, 167)]
        colorblind = ['#%02x%02x%02x' % (c[0], c[1], c[2]) for c in colorblind]
        colorcycler = cycle([colorblind[3], colorblind[5], colorblind[6], colorblind[1]])
        x_lim = [numpy.inf, 0]
        y_lim = [numpy.inf, 0]
        colors = {}
        for title, pd_data in pd_datas:
            for title_legend in pd_data:
                x_lim[0] = min(x_lim[0], min(pd_data[title_legend]['x']))
                x_lim[1] = max(x_lim[1], max(pd_data[title_legend]['x']))
                y_lim[0] = min(y_lim[0], min(pd_data[title_legend]['y']))
                y_lim[1] = max(y_lim[1], max(pd_data[title_legend]['y']))
                if title_legend not in colors:
                    colors[title_legend] = colorcycler.next()
        for title, pd_data in pd_datas:
            x = graphs_index / (len(pd_datas) / 2)
            y = graphs_index % (len(pd_datas) / 2)
            y = 2 if y == 1 else y
            x = 2 if x == 1 else x
            ax = fig.add_subplot(plot_gridspec[x, y])
            ax.set_axisbelow(True)
            legends = pd_data.keys()
            legends.sort()
            markercycler = cycle(markers)
            for title_legend in legends:
                pd_data_i = pd_data[title_legend]
                plt.grid(True)
                color = colors[title_legend]
                plt.plot(
                    pd_data_i['x'], pd_data_i['y'], marker=next(markercycler), label=title_legend, color=color,
                    mec=color, mew=1.4, linewidth=1.2, markevery=2, markersize=3)
            if not xlim:
                plt.xlim(x_lim[0], x_lim[1])
            else:
                plt.xlim(*xlim)
            if not ylim:
                plt.ylim(y_lim[0], y_lim[1])
            else:
                plt.ylim(*ylim)
            plt.title(title)
            graphs_index += 1
        plt.legend(loc=4,  numpoints=1)
        ax3 = fig.add_subplot(plot_gridspec[1, 0])
        ax3.set_yticks([])
        ax3.set_xticks([])
        ax3.set_frame_on(False)
        plt.ylabel(ylabel, fontsize=9, labelpad=20)
        ax3 = fig.add_subplot(plot_gridspec[2, 1])
        ax3.set_yticks([])
        ax3.set_xticks([])
        ax3.set_frame_on(False)
        plt.xlabel(xlabel, fontsize=9, labelpad=20)
        plt.suptitle("Snapshot of the " + str(calculate_on) + "th iteration", fontsize=14)
        if tight_layout is not None:
            if not tight_layout:
                plt.tight_layout()
            else:
                plt.tight_layout(rect=tight_layout)
        plt.show()
