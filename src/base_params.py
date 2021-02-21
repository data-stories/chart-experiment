import matplotlib.pyplot as plt

class BaseParams:

    fonts = {
        "ftse": "serif",
        "ftns": "sans-serif",
        "ftfa": "fantasy"
        }

    fontsizes = {
        'fs10': 10,
        'fs12': 12, # potentially delete
        'fs14': 14,
        'fs16': 16,
        'fs18': 18
        }

    hues = { 
        "MG": plt.get_cmap("Greys"), 
        "MB": plt.get_cmap("Blues"), 
        "CL": plt.get_cmap("PuOr"), 
        "CR": plt.get_cmap("magma")
        }

    source_anns = {
        "sa10": "ul",
        "sa11": "ur",
        "sa00": "ll",
        "sa01": "lr",
        "sano": False
        }

    percent_anns = {
        "pano": False,
        "pa01": 1,
        "pa03": 3,
        "pa05": 5
    }

    annotation_dist = {
        "ad04": 0.4,
        "ad06": 0.6,
        "ad08": 0.8,
        "ad11": 1.1
        }
                    
    wedge_explodes = {"we00":0, "we05": 0.05, "we10": 0.1}

    orientations = {"ro000": 0, "ro090": 90, "ro270": 270}

    sample_annot = {"sm0": False, "sm1": True}

    @staticmethod
    def get_fonts():
        return BaseParams.fonts
    
    @staticmethod
    def get_fontsizes():
        return BaseParams.fontsizes

    @staticmethod
    def get_hues():
        return BaseParams.hues

    @staticmethod
    def get_source_anns():
        return BaseParams.source_anns
    
    @staticmethod
    def get_percent_anns():
        return BaseParams.percent_anns
    
    @staticmethod
    def get_annotation_dist():
        return BaseParams.annotation_dist
    
    @staticmethod
    def get_wedge_explodes():
        return BaseParams.wedge_explodes
    
    @staticmethod
    def get_orientations():
        return BaseParams.orientations
    
    @staticmethod
    def get_sample_annot():
        return BaseParams.sample_annot




