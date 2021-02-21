import matplotlib.pyplot as plt
import numpy as np

from chart_params import ChartParams

class ChartHolder(ChartParams):
    CHART_TYPES = {'pie': 'self._plot_pie', 'donut':'self._plot_donut', 'bar':'self._plot_bar'}

    bbox_dict = {
            "llul": (-0.5, 1.1),
            "llur": (1.2, 1),
            "llcl": (-0.5, 0.5),
            "llcr": (1.5, 0.5)
        }

    def graph(self, chart_type, item, show=True, save=False):

        self.file_name = self._get_file_name(chart_type,item)
        self.fig, self.ax = plt.subplots(figsize=(12,10))

        if chart_type.lower() not in self.CHART_TYPES.keys():
            raise NameError("Chart type not recognized. Please choose one from: ", self.CHART_TYPES)
        
        eval(ChartHolder.CHART_TYPES[chart_type.lower()]+'('+str(item)+')') 

        if show:
            self._show()

        if save:
            self.save_chart(dpi=300, bbox_inches='tight', facecolor='w')

    def save_chart(self, path=None, **kwargs):
        
        file_name = self.file_name

        if path:
            # os change directory to go there 
            raise NotImplementedError

        self.fig.savefig(file_name, **kwargs)

    def annotate_percents(self, pct, allvals, percent):
      absolute = int(round(pct/100.*np.sum(allvals)))
      format_string = "{:." +str(percent)+ "f}%\n({:d} days)"
      return format_string.format(pct, absolute)

    def plot_source_annotation(self,location, font):
        coord_dict = {
            (0,0): (-0.5,-0.5),
            (1,0): (1, -0.5),
            (0,1): (-0.5,1), # upper left
            (1,1): (1,1)
        }
        if location[2:4] == 'no':
            location = False 

        if location:
            y = int(location[2])
            x = int(location[3])

            if int(font[2:]) >= 12:
                self.ax.annotate('Source:\nNational\nWeather\nBureau', xy=coord_dict[(x, y)], xycoords="axes fraction")
            elif int(font[2:]) >= 16:
                self.ax.annotate('Source:\nNational\nWeather\nBureau', xy=coord_dict[(x, y)], xycoords="axes fraction")
            else:
                self.ax.annotate('Source:\nNational Weather Bureau', xy=coord_dict[(x, y)], xycoords="axes fraction")

    def add_sample_annot(self):
        self.ax.annotate("The sample size\nis 1095 days", xy=(0.44, 1.1), xycoords="axes fraction", fontsize = 12)

    def _plot_pie(self, item):
        variations_pie = self.variations_pie

        plt.rcParams['font.family'] = variations_pie['font'][item[7]]
        plt.rcParams['font.size'] = variations_pie['fontsize'][item[8]]
        plt.rcParams['legend.loc'] = variations_pie['legend_location'][item[9]]
        bbox = self.bbox_dict[item[9]]

        vals = variations_pie['displayed_data'][item[1]]["vals"]
        labels = variations_pie['displayed_data'][item[1]]["labels"]

        cmap = variations_pie['hue'][item[0]]
        percent = variations_pie['percent_annotation'][item[5]]
        explosion_scalar = variations_pie['wedge_explode'][item[2]]
        startangle = variations_pie['orientation'][item[4]]
        labeldistance = variations_pie['annotation_distance'][item[6]]

        cmap_linspace = np.linspace(0, 1, len(vals)*2)[(len(vals)//2):len(vals)+(len(vals)//2)]

        if percent:
            wedges, text, autotext = self.ax.pie(vals, colors = cmap(cmap_linspace), explode=[explosion_scalar]*len(vals),
                                            autopct=lambda pct: self.annotate_percents(pct, vals, percent), pctdistance=labeldistance,
                                            startangle=startangle)
            for i in autotext:
                i.set_fontsize(variations_pie['fontsize'][item[8]]-2)
                plt.setp(autotext)
        else:
            wedges, text = self.ax.pie(
                vals,
                colors = cmap(cmap_linspace),
                explode=[explosion_scalar]*len(vals),
                labels = vals,
                labeldistance=labeldistance,
                startangle=startangle)
            plt.setp(text)

        if variations_pie['sample_annot'][item[10]]:
            self.add_sample_annot()

        self.ax.legend(wedges, labels, bbox_to_anchor=bbox)
        self.plot_source_annotation(item[3], item[8])

        self.ax.set(aspect="equal", title=variations_pie['displayed_data'][item[1]]["title"])
        plt.tight_layout()

    def _plot_donut(self, *item):
        pass

    def _plot_bar(self, *item):
        pass

    def _get_file_name(self,chart_type,item):
        prefix ={ "pie":"PP-", "donut":"PD-", "bar":"PB-"}
        return prefix[chart_type]+"-".join(item)
    
    def _show(self):
        plt.show()