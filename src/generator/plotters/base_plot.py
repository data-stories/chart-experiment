import matplotlib.pyplot as plt
import numpy as np

class BasePlot:

    def __init__(self, vals, labels, title, cmap, source_annot, sample_annot, sample_annot_text=None, figsizex=8, figsizey=8, font_family='sans', font_size=12, legend_loc='upper left'):

        plt.rcParams['font.family'] = font_family
        plt.rcParams['font.size'] = font_size
        plt.rcParams['legend.loc'] = legend_loc

        self.fig, self.ax = plt.subplots(figsize=(figsizex,figsizey))

        self.vals = vals
        self.labels = labels
        self.title = title
        self.cmap = plt.get_cmap(cmap)
        self.cmap_linspace = np.linspace(0, 1, len(self.vals)*2)[(len(self.vals)//2):len(self.vals)+(len(self.vals)//2)]

        self.font_size = font_size
        self.legend_loc = legend_loc
        self.source_annot = source_annot
        self.sample_annot = sample_annot
        self.sample_annot_text = sample_annot_text

        # coordinates for legend location
        self.bbox_dict = {
            "upper left": (-0.2, 1.15),
            "upper right": (1.15, 1.15),
            "center left": (-0.2, 0.5),
            "center right": (1.2, 0.5)
        }


    def plot_source_annotation(self, loc, coord_dict):

        coords = coord_dict[loc]
        self.ax.annotate('Source:\nNational Weather Bureau', xy=coords, xycoords="axes fraction")


    def add_sample_annot(self, text, loc, **kwargs):
        txt = "n={}".format(text)
        self.ax.annotate(txt, xy=loc, xycoords="axes fraction", **kwargs)

        