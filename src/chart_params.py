from itertools import product

import numpy as np
import pandas as pd

from data_setup import PlottedData
from base_params import BaseParams


class ChartParams(BaseParams):

    def __init__(self):
        self.PlottedData_ = PlottedData()
        self.DATA_DICT = self.PlottedData_.DATA_DICT
        
        self.variations_pie = self._get_pie_dict()
        self.variations_donut = self._get_donut_dict()
        self.variations_bar = self._get_bar_dict()

        self.pie_variations, self.donut_variations, self.bar_variations = self.get_all_variations()
        self.all_vars = [self.pie_variations, self.donut_variations, self.bar_variations]

    def get_all_records(self):
        list_of_cols = [
                'Type', 'Hue', 'Displayed_data', 'Wedge_explode', 'Source_annotation_location', 'Rotation_Orientation',
                'Percent_annotation_precision',	'Annotation_distance',	'Font',	'Fontsize',	'Legend_location',
                'Sample_annotation', 'Donuthole_size', 'Grid', 'Bars_width', 'Bar_Orientation', 'Bar_spacing',
                'Error_bar-value_annotation'
            ]
        pie_data_ = [(
                'PIE', 
                item[0],
                item[1],
                self.variations_pie['wedge_explode'][item[2]],
                self.variations_pie['source_annotation'][item[3]],
                self.variations_pie['orientation'][item[4]],
                self.variations_pie['percent_annotation'][item[5]],
                self.variations_pie['annotation_distance'][item[6]],
                self.variations_pie['font'][item[7]],
                self.variations_pie['fontsize'][item[8]],
                item[9],
                self.variations_pie['sample_annot'][item[10]],
                np.NaN,
                np.NaN,
                np.NaN,
                np.NaN,
                np.NaN,
                np.NaN
            ) for item in self.pie_variations]
        
        donut_data_ = [(
                'DONUT', 
                item[0],
                item[1],
                self.variations_donut['wedge_explode'][item[3]],
                self.variations_donut['source_annotation'][item[4]],
                self.variations_donut['orientation'][item[5]],
                self.variations_donut['percent_annotation'][item[6]],
                self.variations_donut['annotation_distance'][item[7]],
                self.variations_donut['font'][item[8]],
                self.variations_donut['fontsize'][item[9]],
                item[10],
                self.variations_donut['sample_annot'][item[11]],
                self.variations_donut['donuthole_size'][item[2]],
                np.NaN,
                np.NaN,
                np.NaN,
                np.NaN,
                np.NaN
            ) for item in self.donut_variations]
        
        bar_data_ = [(
            'BAR', 
            item[0],
            item[1],
            np.NaN,
            self.variations_bar['source_annotation'][item[4]],
            np.NaN,
            self.variations_bar['percent_annotation'][item[3]],
            np.NaN,
            self.variations_bar['font'][item[9]],
            self.variations_bar['fontsize'][item[10]],
            item[11],
            self.variations_bar['sample_annot'][item[12]],
            np.NaN,
            self.variations_bar['grid'][item[2]],
            self.variations_bar['bars_width'][item[5]],
            self.variations_bar['orientation'][item[6]],
            self.variations_bar['bar_spacing'][item[7]],
            self.variations_bar['errorbar_value-loc'][item[8]]
        ) for item in self.bar_variations]

        dfs_ = [pie_data_,donut_data_,bar_data_]

        complete_df = pd.concat([pd.DataFrame(i, columns=list_of_cols) for i in dfs_],
          ignore_index=True)

        return complete_df
    
    def get_random_sample(self,n):
        samples = {}
        titles = ['pie_variations', 'donut_variations', 'bar_variations']
        for i in range(3):
            x = [np.random.randint(0, len(self.all_vars[i])) for j in range(n)]
            y = [self.all_vars[i][j] for j in x]
            samples[titles[i]] = y
        
        return samples
    
    def get_all_variations(self):
        pie_variations = self._get_variations(self.variations_pie)
        donut_variations = self._get_variations(self.variations_donut)
        bar_variations_raw = self._get_variations(self.variations_bar)

        # getting rid of legend variations for dd02 & dd12 in bar_variations
        vs = []
        for i in bar_variations_raw:
            if i[1] in ['dd02','dd12']:
                _i = list(i)
                _i[11] = 'llno'
                i = tuple(_i)
            vs.append(i)
        bar_variations = list(set(vs))

        return pie_variations, donut_variations, bar_variations

    def _get_variations(self, variations_dict):
        combinations = product(*(variations_dict[Name] for Name in variations_dict))
        return list(combinations)
    
    def _get_pie_dict(self):
        variations_pie = {
            "hue": BaseParams.get_hues(),
            "displayed_data": self.DATA_DICT["data_donut_pie"],
            "wedge_explode": BaseParams.get_wedge_explodes(),
            "source_annotation": BaseParams.get_source_anns(),
            "orientation": BaseParams.get_orientations(),
            "percent_annotation": BaseParams.get_percent_anns(),
            "annotation_distance": BaseParams.get_annotation_dist(),
            "font": BaseParams.get_fonts(),
            "fontsize": BaseParams.get_fontsizes(),
            "legend_location": {
                #"llcl": 'center left',
                "llcr": 'center right'
                },
            "sample_annot": BaseParams.get_sample_annot()
        }
        return variations_pie

    def _get_donut_dict(self):
        variations_donut = {
            "hue": BaseParams.get_hues(),
            "displayed_data": self.DATA_DICT["data_donut_pie"],
            "donuthole_size": {"dh2": 0.2, "dh5": 0.5, "dh8": 0.8},
            "wedge_explode": BaseParams.get_wedge_explodes(),
            "source_annotation": BaseParams.get_source_anns(),
            "orientation": BaseParams.get_orientations(),
            "percent_annotation": BaseParams.get_percent_anns(),
            "annotation_distance": BaseParams.get_annotation_dist(),
            "font": BaseParams.get_fonts(),
            "fontsize": BaseParams.get_fontsizes(),
            "legend_location": {
                #"llcl": 'center left',
                "llcr": 'center right'
                },
            "sample_annot": BaseParams.get_sample_annot()
        }
        return variations_donut

    def _get_bar_dict(self):
        variations_bar = {
            "hue": BaseParams.get_hues(),
            "displayed_data": self.DATA_DICT["data_bar"],
            "grid": {"gr00": False, "gr0y": True},
            "percent_annotation": BaseParams.get_percent_anns(),
            "source_annotation": BaseParams.get_source_anns(),
            "bars_width": {
                #"bw3": 0.3, 
                "bw4": 0.4, 
                "bw6": 0.6, 
                "bw8": 0.8
                },
            "orientation": {"boh": "h", "bov": "v"},
            "bar_spacing": {"bs000": 0, "bs025": 0.025, "bs050": 0.05},
            # below tuple represents (errorbar, errorbar line cap, value annotation location)
            "errorbar_value-loc": {
                "e00a0": (False, False, False), 
                "e00a1": (False, False, "top"), 
                "e10a1": (True, False, "mid"), 
                "e11a1": (True, True, "mid")
                },
            "font": BaseParams.get_fonts(),
            "fontsize": BaseParams.get_fontsizes(),
            "legend_location": {
                #"llul": 'upper left',
                "llur": 'upper right',
                "llno": False
                },
            "sample_annot": BaseParams.get_sample_annot()
        }
        return variations_bar
