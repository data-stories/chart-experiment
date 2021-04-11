import matplotlib.pyplot as plt
import numpy as np

from .base_plot import BasePlot

class BarPlot(BasePlot):

    def __init__(
            self,
            vals,
            labels,
            title,
            err_val,
            xticks,
            cmap,
            source_annot,
            sample_annot,
            errors,
            percent,
            bars_width,
            bar_spacing,
            orientation,
            grid,
            figsizex=8,
            figsizey=8,
            font_family='sans',
            font_size=12,
            legend_loc='upper left',
            sample_annot_text=None):

        super().__init__(vals,labels,title,cmap,source_annot, sample_annot,sample_annot_text,figsizex,figsizey,font_family,font_size,legend_loc)

        self.errors = errors
        self.xticks = xticks
        
        self.percent = percent
        self.bars_width = bars_width #bar_width -> w
        self.bar_spacing = bar_spacing
        self.orientation = orientation
        self.err_val = err_val
        self.grid = grid

        self.coord_dict = {
            "lower left": (-0.2,-0.1),
            "lower right": (1, -0.1),
            "upper left": (-0.2,1.1),
            "upper right": (1,1)
        }

        self.plot()

    def plot(self):
        pos = np.arange(len(self.labels))

        w = self.bars_width
        offset = self.bar_spacing
        cmaps_list = self.cmap(np.linspace(0.2, 0.8, len(self.vals)))
        
        try:
            xs = np.arange(len(self.vals[0])) # subgroups
            n = len(self.vals)
            w_ = (w-(n-1)*offset)/n
        except TypeError:
            xs = np.arange(len(self.vals))
            w_ = w
        
        # no error bars
        if self.err_val[0] == False:
            try: # no subgroups data category e.g dd02, dd12
                if self.orientation == 'h': # HORIZONTAL
                    if self.grid:
                        self.ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.barh(xs, self.vals, align = 'edge', color=self.cmap(self.cmap_linspace), height = w_, edgecolor="black")
                    self.ax.set_yticks(xs+w_/2)
                    self.ax.set_yticklabels(self.labels)
                    if self.err_val[2]:
                        self.autolabel(b, "h", self.percent, "top")
                else: # VERTICAL
                    if self.grid:
                        self.ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.bar(xs, self.vals, align = 'edge', color=self.cmap(self.cmap_linspace), width = w_, edgecolor="black")
                    self.ax.set_xticks(xs+w_/2)
                    self.ax.set_xticklabels(self.labels)
                    if self.err_val[2]:
                        self.autolabel(b, "v", self.percent, "top")
            except: # for dd06,dd09,... (it has multiple subgroups)
                
                n = len(self.labels)
                if self.orientation == 'h': # HORIZONTAL
                    bs_ = {
                        "b"+str(i): self.ax.barh(xs+i*(w_+offset), self.vals[i], label=self.labels[i], align = 'edge', color=cmaps_list[i], height = w_, edgecolor="black") for i in range(n)
                    }
                   
                    self.ax.set_yticks(xs+0.5*(n*w_+(n-1)*offset))
                    self.ax.set_yticklabels(self.xticks, fontsize=14)

                    if self.err_val[2]:
                        for v in bs_.values():
                            self.autolabel(v, "h", self.percent, "top")

                else: # VERTICAL
                    bs_ = {
                        "b"+str(i): self.ax.bar(xs+i*(w_+offset), self.vals[i], label=self.labels[i], align = 'edge', color=cmaps_list[i], width = w_, edgecolor="black") for i in range(n)
                    }
                    
                    self.ax.set_xticks(xs+0.5*(n*w_+(n-1)*offset))
                    self.ax.set_xticklabels(self.xticks)

                    if self.err_val[2]:
                        for v in bs_.values():
                            self.autolabel(v, "v", self.percent, "top")

        #error bars NOT IMPLEMENTED FOR ANYTHING BUT dd02,dd06,dd12
        else:
            error_kw={"capsize": 0} if self.err_val[1] == False else {"capsize": 5}

            try: # no subgroups data categor e.g dd02, dd12
                if self.orientation == 'h':
                    if self.grid:
                        self.ax.xaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.barh(xs, self.vals, xerr=self.errors, error_kw=error_kw, align = 'edge', color=self.cmap(self.cmap_linspace), height = w, edgecolor="black")
                    self.ax.set_yticks(pos+w/2)
                    self.ax.set_yticklabels(self.labels)
                    if self.err_val[2]:
                        self.autolabel(b, "h", self.percent, 'mid')
                else: #vertical
                    if self.grid:
                        self.ax.yaxis.grid(True, linestyle='--', which='major', color='grey', alpha=.5)
                    b = self.ax.bar(xs, self.vals, yerr=self.errors, error_kw=error_kw, align = 'edge', color=self.cmap(self.cmap_linspace), width = w, edgecolor="black")
                    self.ax.set_xticks(pos+w/2)
                    self.ax.set_xticklabels(self.labels)
                    
                    if self.err_val[2]:
                        self.autolabel(b, "v", self.percent, 'mid')
            except: # for dd06,dd09,... (it has multiple subgroups)
                
                n = len(self.labels)
                if self.orientation == 'h':# HORIZONTAL
                    bs_ = {
                        "b"+str(i): self.ax.barh(xs+i*(w_+offset), self.vals[i], label=self.labels[i], xerr=self.errors[i], error_kw=error_kw, align = 'edge', color=cmaps_list[i], height = w_, edgecolor="black") for i in range(n)
                    }
                
                    self.ax.set_yticks(xs+0.5*(n*w_+(n-1)*offset))
                    self.ax.set_yticklabels(self.xticks, fontsize=14)

                    if self.err_val[2]:
                        for v in bs_.values():
                            self.autolabel(v, "h", self.percent, "mid")
                
                else: # VERTICAL
                    bs_ = {
                        "b"+str(i): self.ax.bar(xs+i*(w_+offset), self.vals[i], label=self.labels[i], yerr=self.errors[i], error_kw=error_kw, align = 'edge', color=cmaps_list[i], width = w_, edgecolor="black") for i in range(n)
                    }
                    
                    self.ax.set_xticks(xs+0.5*(n*w_+(n-1)*offset))
                    self.ax.set_xticklabels(self.xticks)

                    if self.err_val[2]:
                        for v in bs_.values():
                            self.autolabel(v, "v", self.percent, "mid")

        # plot source annotation
        if self.source_annot:         
            self.plot_source_annotation("lower left", self.coord_dict)

        # plot sample annotation
        if self.sample_annot:
            self.add_sample_annot(self.sample_annot_text, (0.9,-0.1))
        
        # remove part of the axes (top and right)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['top'].set_visible(False)

        # plot legend
        if self.legend_loc:
            self.ax.legend(bbox_to_anchor=self.bbox_dict[self.legend_loc], prop={'size': 13})
        
        self.ax.set(
                title=self.title, #set title
                autoscale_on=True #resize margins
            )
    
    def autolabel(self, rects, s, p, loc = "top", **kwargs):
        """Attach a text label above each bar in *rects*, displaying its height."""

        prec = ':.{}f'.format(p) if p else ':.0f'
        prec = "{" + prec + "}"
            
        if s == "h":
            for rect in rects:
                height = rect.get_width()
                h = height
                if loc == 'mid':
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
                if loc == 'mid':
                    h = height/3
                self.ax.annotate(prec.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, h),
                            xytext=(0, 5),
                            textcoords="offset points",
                            ha='center', va='bottom',
                            **kwargs)