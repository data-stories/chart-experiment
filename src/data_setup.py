import numpy as np
import pandas as pd

class PlottedData:
    raw = pd.read_csv("data.csv")
    
    def __init__(self):
        self.DATA = self.raw[self.raw["year"].isin([2017,2018,2019])].reset_index()

        self.DATA_DICT = {
                "data_donut_pie": {
                        "dd02": self._get_dd02_PP_PD(),
                        "dd06": self._get_dd06_PP_PD(),
                        #"dd09": self._get_dd09_PP_PD(),
                        "dd12": self._get_dd12_PP_PD()
                    },
                "data_bar": {
                        "dd02": self._get_dd02_PB(),
                        "dd06": self._get_dd06_PB(),
                        #"dd09": self._get_dd09_PB(),
                        "dd12": self._get_dd12_PB()
                    }
                }
    
    def _get_dd02_PP_PD(self):
        data_2017 = self.DATA[self.DATA["year"] == 2017]
        PP_PD_2_vals = [len(data_2017[data_2017["rain"] <= 1]), len(data_2017[data_2017["rain"] > 1])]
        PP_PD_2_labels = ["No rain", "Rainy"]
        PP_PD_2_title = "Number of Rainy Days"

        dd02 = {
            "vals": PP_PD_2_vals,
            "labels": PP_PD_2_labels,
            "title": PP_PD_2_title
        }
        return dd02


    def _get_dd06_PP_PD(self):
        data_2018 = self.DATA[self.DATA["year"] == 2018]
        PP_PD_6_vals = [
                len(data_2018[data_2018["temp"] <= 0]),
                len(data_2018[(data_2018["temp"] > 0) & (data_2018["temp"] <=7.5)]),
                len(data_2018[(data_2018["temp"] > 7.5) & (data_2018["temp"] <=17.5)]),
                len(data_2018[(data_2018["temp"] > 17.5) & (data_2018["temp"] <=25)]),
                len(data_2018[(data_2018["temp"] > 25) & (data_2018["temp"] <= 30)]),
                len(data_2018[data_2018["temp"] > 30])
        ]
        PP_PD_6_labels = [
                        'Very Cold\n below 0$^{\circ}$C',
                        'Cold\n0$^{\circ}$C - 7.5$^{\circ}$C',
                        'Cool\n7.5$^{\circ}$C - 17.5$^{\circ}$C',
                        'Warm\n17.5$^{\circ}$C - 25$^{\circ}$C',
                        'Hot\n25$^{\circ}$C - 30$^{\circ}$C',
                        'Very Hot\n30$^{\circ}$C + '           
        ]
        PP_PD_6_title = "Number of Days by Temperature"

        dd06 = {
            "vals": PP_PD_6_vals,
            "labels": PP_PD_6_labels,
            "title": PP_PD_6_title
        }
        return dd06

    def _get_dd12_PP_PD(self):
        data_2017 = self.DATA[self.DATA["year"] == 2017]
        rain_by_month = data_2017.loc[:,['month', 'dates']][data_2017["rain"] > 1].groupby("month").count()
        PP_PD_12_vals = [i[0] for i in rain_by_month.values.tolist()]
        PP_PD_12_labels = [
                   "Jan",
                   "Feb",
                   "Mar",
                   "Apr",
                   "May",
                   "Jun",
                   "Jul",
                   "Aug",
                   "Sep",
                   "Oct",
                   "Nov",
                   "Dec"
        ]
        PP_PD_12_title = "Number of Rainy Days by Month"

        dd12 = {
            "vals": PP_PD_12_vals,
            "labels": PP_PD_12_labels,
            "title": PP_PD_12_title
        }
        return dd12

    def _get_dd02_PB(self):
        rainy_days = self.DATA[self.DATA['rain'] >= 1].groupby('year').count().iloc[:,:1].values.reshape((1,3))[0]
        nonrainy_days = self.DATA[self.DATA['rain'] < 1].groupby('year').count().iloc[:,:1].values.reshape((1,3))[0]
        PB_2_vals = [np.mean(nonrainy_days), np.mean(rainy_days)]
        PB_2_error = [np.std(nonrainy_days), np.std(rainy_days)]
        PB_2_labels = ["No rain", "Rainy"]
        PB_2_title = "Average Number of Rainy Days"
        PB_2_annot = (sum(nonrainy_days)/(sum(nonrainy_days)+sum(rainy_days))*100, "There was no rain\non {}% of\nall days.")

        dd02 = {
            "vals": PB_2_vals,
            "errors": PB_2_error,
            "labels": PB_2_labels,
            "title": PB_2_title,
            "annot": PB_2_annot
        }
        return dd02

    def _get_dd06_PB(self):
        d = self.DATA.groupby(["year", "month", "clouds"]).count().iloc[:,:1].rename(columns={"temp":"count"})
        means = {}
        for j in range(1,13):
            means[j] = [np.mean(d.xs(j, level="month" ).to_numpy().reshape((3,3))[:,i]) for i in range(3)]

        errs = {}
        for j in range(1,13):
            errs[j] = [np.std(d.xs(j, level="month" ).to_numpy().reshape((3,3))[:,i]) for i in range(3)]

        # two arbitrarily chosen months
        PB_6_vals = [means[6], means[12]] 
        PB_6_error = [errs[6], errs[12]]

        PB_6_labels = ["June", "December"]
        PB_6_xticks = ["Clear", "Partly Cloudy", "Very Cloudy"]
        PB_6_title = "Average Cloundiness by Month"
        PB_6_annot_n = ((PB_6_vals[1][1]+PB_6_vals[1][2])/sum(PB_6_vals[1])-(PB_6_vals[0][1]+PB_6_vals[0][2])/sum(PB_6_vals[0]))*100
        PB_6_annot = (PB_6_annot_n, "December is on\naverage {}%\nmore cloudy\nthan June.")

        dd06 = {
            "vals": PB_6_vals,
            "errors": PB_6_error,
            "xticks": PB_6_xticks,
            "labels": PB_6_labels,
            "title": PB_6_title,
            "annot": PB_6_annot
        }
        return dd06

    def _get_dd12_PB(self):
        PB_12_vals = list(self.DATA.loc[:,['month', 'temp']].groupby("month").mean().values.reshape((1,12))[0])
        PB_12_error = list(self.DATA.loc[:,['month', 'temp']].groupby("month").std().values.reshape((1,12))[0])
        PB_12_labels = [
                   "Jan",
                   "Feb",
                   "Mar",
                   "Apr",
                   "May",
                   "Jun",
                   "Jul",
                   "Aug",
                   "Sep",
                   "Oct",
                   "Nov",
                   "Dec"
        ]
        PB_12_title = "Average Temperature by Month"
        PB_12_annot = (sum(PB_12_vals)/12, "The average temperature\naccross the year is\n{} degrees.")
        dd12 = {
            "vals": PB_12_vals,
            "errors": PB_12_error,
            "labels": PB_12_labels,
            "title": PB_12_title,
            "annot": PB_12_annot
        }
        return dd12

    def _get_dd09_PP_PD(self):
        data_2018 = self.DATA[self.DATA["year"] == 2018]
        PP_PD_09_vals = [
                len(data_2018[(data_2018["temp"] > 0) & (data_2018["temp"] <=15)]),
                len(data_2018[(data_2018["temp"] > 15) & (data_2018["temp"] <=30)]),
                len(data_2018[(data_2018["temp"] > 30) & (data_2018["temp"] <=45)]),
                len(data_2018[(data_2018["temp"] > 45) & (data_2018["temp"] <= 60)]),
                len(data_2018[(data_2018["temp"] > 60) & (data_2018["temp"] <= 75)]),
                len(data_2018[(data_2018["temp"] > 75) & (data_2018["temp"] <= 90)]),
                len(data_2018[(data_2018["temp"] > 90) & (data_2018["temp"] <= 105)]),
                len(data_2018[(data_2018["temp"] > 105) & (data_2018["temp"] <= 120)]),
                len(data_2018[data_2018["temp"] > 120])
        ]

        PP_PD_09_labels = [
                        '0-15 mm',
                        '15-30 mm',
                        '30-45 mm',
                        '45-60 mm',
                        '60-75 mm',
                        '75-90 mm',
                        '90-105 mm',
                        '105-120 mm',
                        'over 120 mm'           
        ]

        PP_PD_09_title = "Number of Days by Rainfall"

        dd09 = {
            "vals": PP_PD_09_vals,
            "labels": PP_PD_09_labels,
            "title": PP_PD_09_title
        }
        return dd09

    def _get_dd09_PB(self):
        d = self.DATA.groupby(["year", "month", "clouds"]).count().iloc[:,:1].rename(columns={"temp":"count"})
        means = {}
        for j in range(1,13):
            means[j] = [np.mean(d.xs(j, level="month" ).to_numpy().reshape((3,3))[:,i]) for i in range(3)]

        errs = {}
        for j in range(1,13):
            errs[j] = [np.std(d.xs(j, level="month" ).to_numpy().reshape((3,3))[:,i]) for i in range(3)]

        # three arbitrarily chosen months
        PB_9_vals = [means[3], means[6], means[12]] 
        PB_9_error = [errs[3], errs[6], errs[12]]

        PB_9_labels = ["March","June", "December"]
        PB_9_xticks = ["Clear", "Partly Cloudy", "Very Cloudy"]
        PB_9_title = "Average Cloundiness by Month"
        
        dd09 = {
            "vals": PB_9_vals,
            "errors": PB_9_error,
            "xticks": PB_9_xticks,
            "labels": PB_9_labels,
            "title": PB_9_title
        } 
        return dd09

        