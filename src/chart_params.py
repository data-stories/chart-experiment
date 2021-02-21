from itertools import product

from data_setup import PlottedData
from base_params import BaseParams


class ChartParams(BaseParams):

    def __init__(self):
        self.PlottedData_ = PlottedData()
        self.DATA_DICT = self.PlottedData_.DATA_DICT
        
        self.variations_pie = self._get_pie_dict()
        self.variations_donut = self._get_donut_dict()
        self.variations_bar = self._get_bar_dict()
        

    def get_variations(self, variations_dict):
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
            "legend_location": {"llcl": 'center left', "llcr": 'center right'},
            "sample_annot": BaseParams.get_sample_annot()
        }
        return variations_pie

    def _get_donut_dict(self):
        variations_donut = {
            "hue": BaseParams.get_hues(),
            "displayed_data": self.DATA_DICT["data_donut_pie"],
            "donuthole_size": {"dh2": 0.2, "dh4": 0.4, "dh6": 0.6, "dh8": 0.8},
            "wedge_explode": BaseParams.get_wedge_explodes(),
            "source_annotation": BaseParams.get_source_anns(),
            "orientation": BaseParams.get_orientations(),
            "percent_annotation": BaseParams.get_percent_anns(),
            "annotation_distance": BaseParams.get_annotation_dist(),
            "font": BaseParams.get_fonts(),
            "fontsize": BaseParams.get_fontsizes(),
            "legend_location": {"llcl": 'center left', "llcr": 'center right'},
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
                "bw30": 0.3, 
                "bw45": 0.45, 
                "bw60": 0.6, 
                "bw75": 0.75
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
            "legend_location": {"llcl": 'center left', "llcr": 'center right'},
            "sample_annot": BaseParams.get_sample_annot()
        }
        return variations_bar
