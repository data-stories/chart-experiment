import multiprocessing

import matplotlib as mlp
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
import numpy as np

from chart_params import ChartParams

class ChartHolder(ChartParams):
    CHART_TYPES = {'pie': 'self._plot_pie', 'donut':'self._plot_donut', 'bar':'self._plot_bar'}

    bbox_dict = { # for legend location
            "llul": (-0.2, 1.2),
            "llur": (1.2, 1.2),
            "llcl": (-0.2, 0.5),
            "llcr": (1.2, 0.5)
        }

    def __init__(self):
        super().__init__()
    
    def multi_graph(self, type_, i_list, save_):
        pool = multiprocessing.Pool()
        n = len(i_list)
        type_ = [type_]*n
        save_ = [save_]*n
        input_ = zip(type_, i_list, save_)
        pool.map(self.mplot, input_)

        # clean up processes
        pool.close()
        pool.join()
    
    def mplot(self,input_):
        type_, i_list, save_ = input_
        self.graph(type_, i_list, save=save_)

    def graph(self, chart_type, item, show=False, save=False, backend=None):

        self.file_name = self._get_file_name(chart_type,item)

        self.norm = Normalize()
        if backend:
            mlp.use(backend)

        if chart_type.lower() not in self.CHART_TYPES.keys():
            raise NameError("Chart type not recognized. Please choose one from: ", self.CHART_TYPES)
        
        eval(ChartHolder.CHART_TYPES[chart_type.lower()]+'('+str(item)+')') 

        if show:
            plt.show()
        if save:
            self.save_chart(dpi=100, bbox_inches='tight', facecolor='w')

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

    def plot_source_annotation(self, location, font):
        coord_dict = {
            (0,0): (-0.2,-0.1), #lower left
            (1,0): (1, -0.1), #lower right
            (0,1): (-0.3,1), #upper left
            (1,1): (1,1) #upper right
        }
        if location[2:4] == 'no':
            location = False 

        if location:
            y = int(location[2])
            x = int(location[3])

            if int(font[2:]) >= 18:
                self.ax.annotate('Source:\nNational\nWeather\nBureau', xy=coord_dict[(x, y)], xycoords="axes fraction")
            else:
                self.ax.annotate('Source:\nNational Weather Bureau', xy=coord_dict[(x, y)], xycoords="axes fraction")

    def add_sample_annot(self, text, **kwargs):
        txt = "The sample size\nis {}".format(text)

        self.ax.annotate(txt, xy=(0.44, 1.1), xycoords="axes fraction", **kwargs)

    def _plot_pie(self, item):

        plt.rcParams['font.family'] = self.variations_pie['font'][item[7]]
        plt.rcParams['font.size'] = self.variations_pie['fontsize'][item[8]]
        plt.rcParams['legend.loc'] = self.variations_pie['legend_location'][item[9]]

        self.fig, self.ax = plt.subplots(figsize=(8,8))

        vals = self.variations_pie['displayed_data'][item[1]]["vals"]
        labels = self.variations_pie['displayed_data'][item[1]]["labels"]

        cmap = self.variations_pie['hue'][item[0]]
        percent = self.variations_pie['percent_annotation'][item[5]]
        explosion_scalar = self.variations_pie['wedge_explode'][item[2]]
        startangle = self.variations_pie['orientation'][item[4]]
        labeldistance = self.variations_pie['annotation_distance'][item[6]]

        cmap_linspace = np.linspace(0, 1, len(vals)*2)[(len(vals)//2):len(vals)+(len(vals)//2)]

        if percent:
            wedges, text, autotext = self.ax.pie(
                vals,
                colors = cmap(cmap_linspace),
                explode=[explosion_scalar]*len(vals),
                autopct=lambda pct: self.annotate_percents(pct, vals, percent),
                pctdistance=labeldistance,
                startangle=startangle
            )
            for i in autotext:
                i.set_fontsize(self.variations_pie['fontsize'][item[8]]-3)
                plt.setp(autotext)
        elif item[1][:2] == 'ee':
            wedges = self.ax.pie(vals, colors = cmap(cmap_linspace))
        else:
            wedges, text = self.ax.pie(
                vals,
                colors = cmap(cmap_linspace),
                explode=[explosion_scalar]*len(vals),
                labels = vals,
                labeldistance=labeldistance,
                startangle=startangle
            )
            for label in text:
                label.set_horizontalalignment('center')
            plt.setp(text, fontsize=13)

        if self.variations_pie['sample_annot'][item[10]]:
            annot = self.variations_pie['displayed_data'][item[1]]["sample"]
            self.add_sample_annot(annot)
        
        if item[1] == 'dd28':
            self.ax.legend(
                    wedges,
                    labels,
                    ncol=2,
                    labelspacing=0.05,
                    columnspacing=0.3,
                    handletextpad=0.3, 
                    bbox_to_anchor=self.bbox_dict[item[9]],
                    prop={'size': 12}
                )
        else:
            self.ax.legend(wedges, labels, bbox_to_anchor=self.bbox_dict[item[9]], prop={'size': 13})
        self.plot_source_annotation(item[3], item[8])
       
        self.ax.set(
            autoscale_on=True,
            aspect="equal",
            title=self.variations_pie['displayed_data'][item[1]]["title"]
            )

    def _plot_donut(self, item):
        plt.rcParams['font.family'] = self.variations_donut['font'][item[8]]
        plt.rcParams['font.size'] = self.variations_donut['fontsize'][item[9]]
        plt.rcParams['legend.loc'] = self.variations_donut['legend_location'][item[10]]

        self.fig, self.ax = plt.subplots(figsize=(8,8))

        vals = self.variations_donut['displayed_data'][item[1]]["vals"]
        labels = self.variations_donut['displayed_data'][item[1]]["labels"]

        cmap = self.variations_donut['hue'][item[0]]
        cmap_linspace = np.linspace(0, 1, len(vals)*2)[(len(vals)//2):len(vals)+(len(vals)//2)]

        percent = self.variations_donut['percent_annotation'][item[6]]
        explosion_scalar = self.variations_donut['wedge_explode'][item[3]]
        startangle = self.variations_donut['orientation'][item[5]]
        labeldistance = self.variations_donut['annotation_distance'][item[7]]
        size = self.variations_donut['donuthole_size'][item[2]]
        
        if percent:
            wedges, text, autotext = self.ax.pie(vals, colors = cmap(cmap_linspace), explode=[explosion_scalar]*len(vals),
                                            autopct=lambda pct: self.annotate_percents(pct, vals, percent), labeldistance=labeldistance,
                                            wedgeprops=dict(width=size),
                                            pctdistance=labeldistance,
                                            startangle=startangle)
            for i in autotext:
                i.set_fontsize(self.variations_pie['fontsize'][item[9]]-3)
            plt.setp(autotext)
        elif item[1][:2] == 'ee':
            wedges = self.ax.pie(vals, colors = cmap(cmap_linspace))

        else:
            wedges, text = self.ax.pie(
                vals, colors = cmap(cmap_linspace),
                explode=[explosion_scalar]*len(vals),
                labels = vals,
                labeldistance=labeldistance,
                wedgeprops=dict(width=size),
                startangle=startangle)
            for label in text:
                label.set_horizontalalignment('center')
            plt.setp(text, fontsize=13)

        if item[1] == 'dd28':
            self.ax.legend(
                    wedges,
                    labels,
                    ncol=2,
                    labelspacing=0.05,
                    columnspacing=0.3,
                    handletextpad=0.3, 
                    bbox_to_anchor=self.bbox_dict[item[10]],
                    prop={'size': 12}
                )
        else:
            self.ax.legend(wedges, labels, bbox_to_anchor=self.bbox_dict[item[10]], prop={'size': 13})
        
        self.plot_source_annotation(item[4],item[9])

        if self.variations_pie['sample_annot'][item[11]]:
            annot = self.variations_donut['displayed_data'][item[1]]["sample"]
            self.add_sample_annot(annot)

        self.ax.set(
            autoscale_on=True,
            aspect="equal",
            title=self.variations_donut['displayed_data'][item[1]]["title"]
            )

    def _plot_bar(self, item):
        #mlp.rcParams.update(mlp.rcParamsDefault)
        plt.rcParams['font.family'] = self.variations_bar['font'][item[9]]
        plt.rcParams['font.size'] = self.variations_bar['fontsize'][item[10]]
        if item[11] != 'llno':
            plt.rcParams['legend.loc'] = self.variations_bar['legend_location'][item[11]]
            bbox = self.bbox_dict[item[11]]
        
        self.fig, self.ax = plt.subplots(figsize=(8,8))

        vals = self.variations_bar['displayed_data'][item[1]]["vals"]
        labels = self.variations_bar['displayed_data'][item[1]]["labels"]
        errors = self.variations_bar['displayed_data'][item[1]]["errors"]
        
        cmap = self.variations_bar['hue'][item[0]]
        cmap_linspace = np.linspace(0, 1, len(vals)*2)[(len(vals)//2):len(vals)+(len(vals)//2)]

        percent = self.variations_bar['percent_annotation'][item[3]]
        w = self.variations_bar['bars_width'][item[5]]
        offset = self.variations_bar['bar_spacing'][item[7]]

        err_val = self.variations_bar['errorbar_value-loc'][item[8]]
        pos = np.arange(len(labels))
        
        try:
            xs = np.arange(len(vals[0]))
        except TypeError:
            xs = np.arange(len(vals))
        
        # no error bars
        if err_val[0] == False:
            try: #dd02/12
                if self.variations_bar['orientation'][item[6]] == 'h':
                    if self.variations_bar['grid'][item[2]]:
                        self.ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.barh(xs, vals, align = 'edge', color=cmap(cmap_linspace), height = w, edgecolor="black")
                    self.ax.set_yticks(pos+w/2)
                    self.ax.set_yticklabels(labels, fontsize=14)
                    if err_val[2]:
                        self.autolabel(b, "h",percent, "top")
                else:
                    if self.variations_bar['grid'][item[2]]:
                        self.ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.bar(xs, vals, align = 'edge', color=cmap(cmap_linspace), width = w, edgecolor="black")
                    self.ax.set_xticks(pos+w/2)
                    if item[1] == 'dd28':
                        self.ax.set_xticklabels(labels, fontsize=11)
                    else:
                        self.ax.set_xticklabels(labels, fontsize=14)
                    if err_val[2]:
                        self.autolabel(b, "v",percent, "top")
            except: # for dd06,dd09,... (it has two subgroups)
                cmaps_list = None
                
                if item[1] in ['dd09','dd15','dd18']:
                    w = w/3
                    cmaps_list = cmap((np.linspace(0.3, 0.6, 3)))
                elif item[1] == 'dd25':
                    w = w/5
                    cmaps_list = cmap((np.linspace(0.3, 0.7, 5)))
                elif item[1] == 'dd24':
                    w = w/8
                    cmaps_list = cmap((np.linspace(0.3, 0.8, 8)))
                else: #dd10,dd20
                    w = w/2
                    cmaps_list = cmap((np.linspace(0.4, 0.6, 2)))
                xticks = self.variations_bar['displayed_data'][item[1]]['xticks']
                
                n = len(labels)
                pos = np.arange(len(xticks))
                # HORIZONTAL
                if self.variations_bar['orientation'][item[6]] == 'h':
                    bs_ = {}
                    for i in range(n):
                        bs_["b"+str(i)] = self.ax.barh(xs+i*(w+offset), vals[i], label=labels[i], align = 'edge', color=cmaps_list[i], height = w, edgecolor="black")
                   
                    self.ax.set_yticks(pos+(n/2)*(w+offset/2))
                    self.ax.set_yticklabels(xticks, fontsize=14)

                    if err_val[2]:
                        for v in bs_.values():
                            self.autolabel(v, "h", percent, "top")

                # VERTICAL
                else:
                    bs_ = {}
                    
                    for i in range(n):
                        bs_["b"+str(i)] = self.ax.bar(xs+i*(w+offset), vals[i], label=labels[i], align = 'edge', color=cmaps_list[i], width = w, edgecolor="black")
                    
                    self.ax.set_xticks(pos+(n/2)*(w+offset/2))
                    if item[1] == 'dd20':
                        self.ax.set_xticklabels(xticks, fontsize=11)
                    else:
                        self.ax.set_xticklabels(xticks, fontsize=14)
                    if err_val[2]:
                        for v in bs_.values():
                            self.autolabel(v, "v", percent, "top")

        #error bars NOT IMPLEMENTED FOR ANYTHING BUT dd02,dd06,dd12
        else:
            if err_val[1] == False:
                error_kw={"capsize": 0}
            else:
                error_kw={"capsize": 5 }

            try: #dd02/12
                if self.variations_bar['orientation'][item[6]] == 'h':
                    if self.variations_bar['grid'][item[2]]:
                        self.ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.barh(xs, vals, xerr=errors, error_kw=error_kw, align = 'edge', color=cmap(cmap_linspace), height = w, edgecolor="black")
                    self.ax.set_yticks(pos+w/2)
                    self.ax.set_yticklabels(labels, fontsize=14)
                    if err_val[2]:
                        self.autolabel(b, "h", percent, 'mid')
                else: #vertical
                    if self.variations_bar['grid'][item[2]]:
                        self.ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.bar(xs, vals, yerr=errors, error_kw=error_kw, align = 'edge', color=cmap(cmap_linspace), width = w, edgecolor="black")
                    self.ax.set_xticks(pos+w/2)
                    self.ax.set_xticklabels(labels, fontsize=14)
                    
                    if err_val[2]:
                        self.autolabel(b, "v", percent, 'mid')
            except: # for dd06 (it has two subgroups)
                cmaps_list = cmap(np.linspace(0.4, 0.6, 2))
                w = w/2
                xticks = self.variations_bar['displayed_data'][item[1]]['xticks']
                pos = np.arange(len(xticks))

                xticks = self.variations_bar['displayed_data'][item[1]]['xticks']
                if self.variations_bar['orientation'][item[6]] == 'h':
                    b1 = self.ax.barh(xs, vals[0], xerr=errors[0], error_kw=error_kw, label=labels[0], align = 'edge', color=cmaps_list[0], height = w, edgecolor="black")
                    b2 = self.ax.barh(xs+w+offset, vals[1], xerr=errors[1], error_kw=error_kw, label=labels[1], align = 'edge', color=cmaps_list[1], height = w, edgecolor="black")
                    self.ax.set_yticks(pos+w+offset/2)
                    self.ax.set_yticklabels(xticks,fontsize=14)
                    if err_val[2]:
                        self.autolabel(b1,"h",percent,'mid')
                        self.autolabel(b2,"h",percent,'mid')
                else:
                    b1 = self.ax.bar(xs, vals[0], yerr=errors[0], error_kw=error_kw, label=labels[0], align = 'edge', color=cmaps_list[0], width = w, edgecolor="black")
                    b2 = self.ax.bar(xs+w+offset, vals[1], yerr=errors[1], error_kw=error_kw, label=labels[1], align = 'edge', color=cmaps_list[1], width = w, edgecolor="black")
                    self.ax.set_xticks(pos+w+offset/2)
                    self.ax.set_xticklabels(xticks,fontsize=14)
                    if err_val[2]:
                        self.autolabel(b1,"v",percent,'mid')
                        self.autolabel(b2,"v",percent,'mid')

        # plot source annotation
        if item[4] != 'sano':         
            self.plot_source_annotation_bar(item[4])

        # plot sample annotation
        if self.variations_bar['sample_annot'][item[12]]:
            annot = self.variations_bar['displayed_data'][item[1]]["sample"]
            self.add_sample_annot(annot)
        
        # remove part of the axes (top and right)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)

        # plot legend
        if item[11] != 'llno':
            if item[1] == 'dd24':
                self.ax.legend(bbox_to_anchor=bbox,labelspacing=0.2,prop={'size': 13})
            else:
                self.ax.legend(bbox_to_anchor=bbox, prop={'size': 13})
        
        self.ax.set(
                title=self.variations_bar['displayed_data'][item[1]]["title"], #set title
                autoscale_on=True #resize margins
            )

    def _get_file_name(self,chart_type,item):
        prefix ={ "pie":"PP-", "donut":"PD-", "bar":"PB-"}
        return prefix[chart_type]+"-".join(item)
    
    def plot_source_annotation_bar(self, location):
        coord_dict = {
            (0,0): (-0.2,-0.2), # lower left sa00
            (1,0): (1.1,-0.2), # lower right sa01
            (0,1): (-0.25,1.1), # upper left sa10
            (1,1): (1.1,1.1)  # upper right sa11
        }

        if location:
            y = int(location[2])
            x = int(location[3])

            self.ax.annotate('Source:\nNational Weather Bureau', xy=coord_dict[(x, y)], xycoords="axes fraction")
    
    def autolabel(self, rects, s, p, loc = "top", **kwargs):
        """Attach a text label above each bar in *rects*, displaying its height."""

        prec = None

        if p == 1:
            prec = '{:.1f}'
        elif p == 3:
            prec = '{:.3f}'
            fs = fs - 2
        elif p == 5:
            prec = '{:.5f}'
            fs = fs - 4
        else:
            prec = '{:.0f}'
            
        if s == "h":
            for rect in rects:
                height = rect.get_width()
                h = height
                if loc =='mid':
                    h = height/3
                self.ax.annotate(prec.format(height),
                            xy=(h, rect.get_y() + rect.get_height() / 2),
                            xytext=(5, 0),
                            textcoords="offset points",
                            ha='left', va='center',
                            **kwargs)
        elif s == "v":
            for rect in rects:
                height = rect.get_height()
                h = height
                if loc =='mid':
                    h = height/3
                self.ax.annotate(prec.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, h),
                            xytext=(0, 5),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            **kwargs)
