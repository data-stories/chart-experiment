import matplotlib.pyplot as plt
import numpy as np

from .base_plot import BasePlot

class PiePlot(BasePlot):

    def __init__(
            self,
            vals,
            labels,
            title,
            cmap,
            source_annot,
            sample_annot,
            percent,
            explosion_scalar,
            startangle,
            labeldistance,
            dh_size=None,
            figsizex=8,
            figsizey=8,
            font_family='sans',
            font_size=12,
            legend_loc='upper left',
            sample_annot_text=None
            ):
        super().__init__(vals,labels,title,cmap,source_annot,sample_annot,sample_annot_text,figsizex,figsizey,font_family,font_size,legend_loc)

        self.percent=percent
        self.explosion_scalar=explosion_scalar
        self.startangle=startangle
        self.labeldistance=labeldistance
        self.dh_size=dh_size

        self.coord_dict = {
            "lower left": (-0.2,-0.1), #lower left
            "lower right": (1, -0.1), #lower right
            "upper left": (-0.3,1), #upper left
            "upper right": (1,1) #upper right
        }

        self.plot()
         
    def plot(self):
        
        # plotting wedges and labels
        if self.percent:
            wedges, text, autotext = self.ax.pie(
                self.vals,
                colors=self.cmap(self.cmap_linspace),
                explode=[self.explosion_scalar]*len(self.vals),
                autopct=lambda x: self.annotate_percents(x, self.vals, self.percent), #modified labels
                labeldistance=self.labeldistance,
                pctdistance=self.labeldistance,
                wedgeprops=dict(width=self.dh_size),
                startangle=self.startangle)
            for i in autotext:
                i.set_fontsize(self.font_size-3)
            plt.setp(autotext)
        else:
            wedges, text = self.ax.pie(
                self.vals,
                colors=self.cmap(self.cmap_linspace),
                explode=[self.explosion_scalar]*len(self.vals),
                labels = self.vals,
                labeldistance=self.labeldistance,
                wedgeprops=dict(width=self.dh_size),
                startangle=self.startangle)
            for label in text:
                label.set_horizontalalignment('center')
            plt.setp(text, fontsize=12)

        #plotting legend
        self.ax.legend(wedges, self.labels, bbox_to_anchor=self.bbox_dict[self.legend_loc], prop={'size': 13})

        #plotting legend
        if self.source_annot:
            self.plot_source_annotation("upper left", self.coord_dict)

        if self.sample_annot:
            self.add_sample_annot(self.sample_annot_text, (0.9,-0.1))

        self.ax.set(
            autoscale_on=True,
            aspect="equal",
            title=self.title
            )
    
    def annotate_percents(self, pct, allvals, percent):
        absolute = int(round(pct/100.*np.sum(allvals)))
        format_string = "{:." +str(percent)+ "f}%\n({:d} days)"
        return format_string.format(pct, absolute)