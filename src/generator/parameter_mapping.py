
import json

class ParamsMap:

    def __init__(self, mapping_file):
        with open(mapping_file, "r") as read_file:
            self.mapping = json.load(read_file)

        self.item_mapping = {
            "pie": [0,1,3,10,7,8,9,5,2,4,6],
            "donut": [0,1,4,11,8,9,10,6,3,5,7,2],
            "bar": [0,1,4,12,9,10,11,4,8,5,7,6,2]
        }

    def translate(self, chart_type, item, item_mapping=None):
        #item pie ["CL", "dd03", "we00", "sano", "ro270", "pano", "ad95", "ftfa", "fs16", "llcl", "sm0"]
        #item donut ["MB", "dd03", "dh2", "we10", "sano", "ro000", "pano", "ad95", "ftse", "fs16", "llcr", "sm1"]
        #item bar ["MG", "ee06", "gr0y", "pano", "sano", "bw6", "bov", "bs000", "e00a0", "ftse", "fs16", "llno", "sm0"]

        idx = item_mapping[chart_type] if item_mapping else [i for i in range(13)] 

        kwargs = {}

        kwargs["cmap"] = self.mapping["hues"][item[idx[0]]]
        kwargs["source_annot"] = self.mapping["source_anns"][item[idx[2]]]
        kwargs["sample_annot"] = self.mapping["sample_annot"][item[idx[3]]]
        kwargs["font_family"] = self.mapping["fonts"][item[idx[4]]]
        kwargs["font_size"] = self.mapping["fontsizes"][item[idx[5]]]
        kwargs["legend_loc"] = self.mapping["legend_location"][item[idx[6]]]
        kwargs["percent"] = self.mapping["percent_anns"][item[idx[7]]]

        if chart_type == 'bar':
            # dispayed data
            kwargs["vals"] = self.mapping["displayed_data"]['bar'][item[idx[1]]]["vals"]
            kwargs["labels"] = self.mapping["displayed_data"]['bar'][item[idx[1]]]["labels"]
            kwargs["title"] = self.mapping["displayed_data"]['bar'][item[idx[1]]]["title"]
            kwargs["errors"] = self.mapping["displayed_data"]['bar'][item[idx[1]]]["errors"]
            kwargs["xticks"] = self.mapping["displayed_data"]['bar'][item[idx[1]]]["xticks"]
            kwargs["sample_annot_text"] = self.mapping["displayed_data"]['bar'][item[idx[1]]]["sample"]

            # parameters
            
            kwargs["err_val"] = self.mapping["errorbar_value-loc"][item[idx[8]]]
            kwargs["bars_width"] = self.mapping["bars_width"][item[idx[9]]]
            kwargs["bar_spacing"] = self.mapping["bar_spacing"][item[idx[10]]]
            kwargs["orientation"] = self.mapping["orientation"][item[idx[11]]]
            kwargs["grid"] = self.mapping["grid"][item[idx[12]]]

        else:
            # dispayed data
            kwargs["vals"] = self.mapping["displayed_data"]['pie'][item[idx[1]]]["vals"]
            kwargs["labels"] = self.mapping["displayed_data"]['pie'][item[idx[1]]]["labels"]
            kwargs["title"] = self.mapping["displayed_data"]['pie'][item[idx[1]]]["title"]
            kwargs["sample_annot_text"] = self.mapping["displayed_data"]['pie'][item[idx[1]]]["sample"]

            # parameters
            kwargs["explosion_scalar"] = self.mapping["wedge_explodes"][item[idx[8]]]
            kwargs["startangle"] = self.mapping["orientations"][item[idx[9]]]
            kwargs["labeldistance"] = self.mapping["annotation_dist"][item[idx[10]]]
            try:
                kwargs["dh_size"] = self.mapping["donuthole_size"][item[idx[11]]]
            except IndexError:
                pass
            
        return kwargs