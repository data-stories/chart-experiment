import multiprocessing
import os

from parameter_mapping import ParamsMap

from plotters.bar import BarPlot
from plotters.pie import PiePlot


class ChartGenerator(ParamsMap):

    def __init__(self, mapping_file):
        super().__init__(mapping_file)

        self.CHART_TYPES = {'pie': 'PiePlot', 'donut':'PiePlot', 'bar':'BarPlot'}

    def batch(self):
        pass

    def generate(self, batches, batchsize=200, multiprocessing=True):

        for b in batches.keys():
            try:
                os.mkdir(b)
            except FileExistsError:
                pass
            os.chdir(b)

            for k,v in batches[b].items():
                for i in range(len(v)//batchsize+1):
                    self.multi_graph(k, v[batchsize*i:batchsize*(i+1)], save_=True)
            
            os.chdir("..")


    def graph(self, chart_type, item, show=False, save=False, dpi=100):

        if chart_type.lower() not in self.CHART_TYPES.keys():
            raise NameError("Chart type not recognized. Please choose one from: ", self.CHART_TYPES.keys())
        
        params_dict = self.translate(chart_type, item)
        x = eval(self.CHART_TYPES[chart_type.lower()]+'(**params_dict)')

        if show:
            x.fig.show()

        if save:
            file_name = self._get_file_name(chart_type,item)
            x.fig.savefig(file_name, dpi=dpi, bbox_inches='tight', facecolor='w')
    
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

    def _get_file_name(self,chart_type,item):
        prefix ={ "pie":"PP-", "donut":"PD-", "bar":"PB-"}
        return prefix[chart_type]+"-".join(item)