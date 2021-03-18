from itertools import product

import numpy as np
import pandas as pd

class PlottedData:
    raw = pd.read_csv("data.csv")
    
    def __init__(self):
        self.DATA = self.raw[self.raw["year"].isin([2017,2018,2019])]

        self.DATA_DICT = {
                "data_donut_pie": {
                       # "dd02": self._get_dd02_PP_PD(),
                        "dd03": self._get_dd03_PP_PD(),
                        #"dd06": self._get_dd06_PP_PD(),
                        "dd09": self._get_dd09_PP_PD(),
                        "dd10": self._get_dd10_PP_PD(),
                        #"dd12": self._get_dd12_PP_PD(),
                        "dd15": self._get_dd15_PP_PD(),
                        "dd18": self._get_dd18_PP_PD(),
                        "dd20": self._get_dd20_PP_PD(),
                        "dd28": self._get_dd28_PP_PD()

                    },
                "data_bar": {
                        #"dd02": self._get_dd02_PB(),
                        "dd03": self._get_dd03_PB(),
                        #"dd06": self._get_dd06_PB(),
                        "dd09": self._get_dd09_PB(),
                        "dd10": self._get_dd10_PB(),
                        #"dd12": self._get_dd12_PB(),
                        "dd15": self._get_dd15_PB(),
                        "dd18": self._get_dd18_PB(),
                        "dd20": self._get_dd20_PB(),
                        "dd24": self._get_dd24_PB(),
                        "dd25": self._get_dd25_PB(),
                        "dd28": self._get_dd28_PB()
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
            "title": PP_PD_2_title,
            "sample": "12 months"
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
            "title": PP_PD_6_title,
            "sample": "12 months"
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
            "title": PP_PD_12_title,
            "sample": "12 months"
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
            "annot": PB_2_annot,
            "sample": "3 years"
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
            "annot": PB_6_annot,
            "sample": "12 months"
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
            "annot": PB_12_annot,
            "sample": "12 months"
        }
        return dd12

    def _get_dd09_PP_PD(self):
        PP_PD_09_vals = [
            len(self.DATA[(self.DATA["rain"] >= i) & (self.DATA["rain"] < i+15)]) for i in range(0,121,15)] + [len(self.DATA[self.DATA["rain"] > 120])
            ]

        PP_PD_09_labels = [
                        '0-15',
                        '15-30',
                        '30-45',
                        '45-60',
                        '60-75',
                        '75-90',
                        '90-105',
                        '105-120',
                        'over 120'           
        ]

        PP_PD_09_title = "Number of Days by Rainfall (in mm)"

        dd09 = {
            "vals": PP_PD_09_vals,
            "labels": PP_PD_09_labels,
            "title": PP_PD_09_title,
            "sample": "1095 days"
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
            "title": PB_9_title,
            "sample": "3 months"
        } 
        return dd09
    
    def _get_dd03_PP_PD(self):

        PP_PD_03_vals = [
                round(self.DATA[(self.DATA["rain"] >= 10) & (self.DATA["month"] == 3)].groupby(['year']).count().iloc[:,:1].values.reshape(1,3).mean(),1),
                round(self.DATA[(self.DATA["rain"] >= 10) & (self.DATA["month"] == 4)].groupby(['year']).count().iloc[:,:1].values.reshape(1,3).mean(),1),
                round(self.DATA[(self.DATA["rain"] >= 10) & (self.DATA["month"] == 5)].groupby(['year']).count().iloc[:,:1].values.reshape(1,3).mean(),1)
        ]

        PP_PD_03_labels = [
                        'March',
                        'April',
                        'May'
        ]

        PP_PD_03_title = "Average Number of Rainy Days in the Spring"

        dd03 = {
            "vals": PP_PD_03_vals,
            "labels": PP_PD_03_labels,
            "title": PP_PD_03_title,
            "sample": "3 months"
        }
        return dd03

    def _get_dd03_PB(self):
        d = self.DATA[self.DATA["rain"] >= 10].groupby(["year", "month"]).count().iloc[:,:1].rename(columns={"index":"count"})
        means = {}
        for j in range(1,13):
            means[j] = np.mean(d.xs(j, level="month").to_numpy().reshape(3))

        errs = {}
        for j in range(1,13):
            errs[j] = np.std(d.xs(j, level="month").to_numpy().reshape(3))

        PB_3_vals = [means[3], means[4], means[5]] 
        PB_3_error = [errs[3], errs[4], errs[5]]

        PB_3_labels = ["March", "April", "June"]
        PB_3_title = "Average Number of Rainy Days in the Spring"
        
        dd03 = {
            "vals": PB_3_vals,
            "errors": PB_3_error,
            #"xticks": PB_3_xticks,
            "labels": PB_3_labels,
            "title": PB_3_title,
            "sample": "3 months"
        } 
        return dd03
    
    def _get_dd10_PP_PD(self):
        data_2019 = self.DATA[self.DATA["year"] == 2019]
        PP_PD_10_vals = [round(i,1) for i in data_2019.groupby(['month']).mean().loc[3:,["rain"]].values.reshape(10)]

        PP_PD_10_labels = [
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

        PP_PD_10_title = "Average Rainfall by Month (in mm)"

        dd10 = {
            "vals": PP_PD_10_vals,
            "labels": PP_PD_10_labels,
            "title": PP_PD_10_title,
            "sample": "10 months"
        }
        return dd10

    def _get_dd10_PB(self):
        d = self.DATA[(self.DATA["month"] >= 3) & (self.DATA["month"] <= 7)].groupby(["year", "month"]).mean().iloc[:,1:].values.reshape(3,5)

        PB_10_vals = [d[0], d[1]] 
        PB_10_error = [[0 for i in range(5)], [0 for i in range(5)]] # no errors

        PB_10_labels = ["This Year","Last Year"]
        PB_10_xticks = ["March", "April", "May", "June","July"]
        PB_10_title = "Average Rainfall by Month (in mm)"
        
        dd10 = {
            "vals": PB_10_vals,
            "errors": PB_10_error,
            "xticks": PB_10_xticks,
            "labels": PB_10_labels,
            "title": PB_10_title,
            "sample": "2 years"
        } 
        return dd10
    
    def _get_dd15_PP_PD(self):
        PP_PD_15_vals = [
            len(self.DATA[(self.DATA["rain"] >= i) & (self.DATA["rain"] < i+5)]) for i in range(0,6,5)] + [len(self.DATA[self.DATA["rain"] > 140])
            ]+[
            len(self.DATA[(self.DATA["rain"] >= i) & (self.DATA["rain"] < i+10)]) for i in range(10,131,10)] + [len(self.DATA[self.DATA["rain"] > 140])
            ]

        PP_PD_15_labels = [
                        '0-5',
                        '5-10',
                        '10-20',
                        '20-30',
                        '30-40',
                        '40-50',
                        '50-60',
                        '60-70',
                        '70-80',
                        '80-90',
                        '90-100',
                        '100-110',
                        '110-120',
                        '120-130',
                        'over 130'           
        ]

        PP_PD_15_title = "Number of Days by Rainfall (in mm)"

        dd15 = {
            "vals": PP_PD_15_vals,
            "labels": PP_PD_15_labels,
            "title": PP_PD_15_title,
            "sample": "1095 days"
        }
        return dd15
    
    def _get_dd15_PB(self):
        d = self.DATA[(self.DATA["month"] >= 3) & (self.DATA["month"] <= 7)].groupby(["year", "month"]).mean().iloc[:,1:].values.reshape(3,5)

        PB_10_vals = [d[0], d[1], d[2]] 
        PB_10_error = [[0 for i in range(5)], [0 for i in range(5)], [0 for i in range(5)]] # no errors

        PB_10_labels = ["This Year","Last Year","2 Years Ago"]
        PB_10_xticks = ["March", "April", "May", "June","July"]
        PB_10_title = "Average Rainfall by Month (in mm)"
        
        dd10 = {
            "vals": PB_10_vals,
            "errors": PB_10_error,
            "xticks": PB_10_xticks,
            "labels": PB_10_labels,
            "title": PB_10_title,
            "sample": "3 years"
        } 
        return dd10

    def _get_dd18_PP_PD(self):
        d = self.DATA[self.DATA["clouds"] == 'clear'].groupby(['year','month']).count().iloc[:,:1].values.reshape(3,12)
        PP_PD_18_vals = np.array([i[6:] for i in d]).reshape(18)

        PP_PD_18_labels = [
                   "Jul '17",
                   "Aug '17",
                   "Sep '17",
                   "Oct '17",
                   "Nov '17",
                   "Dec '17",
                   "Jul '18",
                   "Aug '18",
                   "Sep '18",
                   "Oct '18",
                   "Nov '18",
                   "Dec '18",
                   "Jul '19",
                   "Aug '19",
                   "Sep '19",
                   "Oct '19",
                   "Nov '19",
                   "Dec '19",
        ]

        PP_PD_18_title = "Number of Sunny Days in Second Half of the Year"

        dd18 = {
            "vals": PP_PD_18_vals,
            "labels": PP_PD_18_labels,
            "title": PP_PD_18_title,
            "sample": "3 years"
        }
        return dd18
    
    def _get_dd18_PB(self):
        d = self.DATA[(self.DATA["month"] >= 3) & (self.DATA["month"] <= 8)].groupby(["year", "month"]).mean().iloc[:,1:].values.reshape(3,6)

        PB_10_vals = [d[0], d[1], d[2]] 
        PB_10_error = [[0 for i in range(6)], [0 for i in range(6)], [0 for i in range(6)]] # no errors

        PB_10_labels = ["This Year","Last Year","2 Years Ago"]
        PB_10_xticks = ["March", "April", "May", "June","July", 'August']
        PB_10_title = "Average Rainfall by Month (in mm)"
        
        dd10 = {
            "vals": PB_10_vals,
            "errors": PB_10_error,
            "xticks": PB_10_xticks,
            "labels": PB_10_labels,
            "title": PB_10_title,
            "sample": "3 years"
        } 
        return dd10

    def _get_dd20_PP_PD(self):
        PP_PD_20_vals = [
            len(self.DATA[(self.DATA["rain"] >= i) & (self.DATA["rain"] < i+5)]) for i in range(0,91,5)] + [len(self.DATA[self.DATA["rain"] > 95])
            ]

        PP_PD_20_labels = [
                        '0-5',
                        '5-10',
                        '10-15',
                        '15-20',
                        '20-25',
                        '25-30',
                        '30-35',
                        '35-40',
                        '40-45',
                        '45-50',
                        '50-55',
                        '55-60',
                        '60-65',
                        '65-70',
                        '70-75',
                        '75-80',
                        '80-85',
                        '85-90',
                        '90-95',
                        '95<'
        ]

        PP_PD_20_title = "Number of Days by Rainfall (in mm)"

        dd20 = {
            "vals": PP_PD_20_vals,
            "labels": PP_PD_20_labels,
            "title": PP_PD_20_title,
            "sample": "1095 days"
        }
        return dd20
    
    def _get_dd20_PB(self):
        data_2019 = self.DATA[self.DATA["year"] == 2019]
        mdf = data_2019[data_2019['month'] ==12]
        sdf = data_2019[data_2019['month'] ==1]
        
        PB_20_vals =  [
            [len(df[df["rain"] == 0])] + [
                len(df[(df["rain"] > i) & (df["rain"] <= i+15)]) for i in range(0,106,15)
            ] + [len(df[df["rain"] > 120])] 
        for df in [mdf,sdf] ]
        PB_20_error = [[0 for i in range(10)] for j in range(2)]

        PB_20_labels = ['December','January']

        PB_20_xticks = [
                        '0',
                        '0-15',
                        '15-30',
                        '30-45',
                        '45-60',
                        '60-75',
                        '75-90',
                        '90-105',
                        '105-120',
                        '120<'
        ]

        PB_20_title = "Number of Days by Rainfall (in mm)"
        
        dd20 = {
            "vals": PB_20_vals,
            "errors": PB_20_error,
            "labels": PB_20_labels,
            'xticks': PB_20_xticks,
            "title": PB_20_title,
            "sample": "2 months"
        } 
        return dd20
    
    def _get_dd28_PP_PD(self):
        f = np.array([self.DATA[(self.DATA['month']==2)&(self.DATA['year']==i)]['rain'].values for i in [2017,2018,2019]])
        
        PP_PD_28_vals = np.mean(f, axis=0).round()
        PP_PD_28_vals = [int(i) if i>0 else 10 for i in PP_PD_28_vals]

        PP_PD_28_labels = [i for i in range(1,29)]

        PP_PD_28_title = "Average Rainfall by Day (in mm) in February"

        dd28 = {
            "vals": PP_PD_28_vals,
            "labels": PP_PD_28_labels,
            "title": PP_PD_28_title,
            "sample": "3 years"
        }
        return dd28
    
    def _get_dd28_PB(self):
        f = np.array([self.DATA[(self.DATA['month']==2)&(self.DATA['year']==i)]['rain'].values for i in [2017,2018,2019]])
        
        PB_28_vals = np.mean(f, axis=0)
        PB_28_vals = [i if i>0 else 10 for i in PB_28_vals]

        PB_28_error = np.std(f, axis=0)

        PB_28_labels = [i for i in range(1,29)]

        PB_28_title = "Mean Rainfall by Day (in mm) - February"
        
        dd28 = {
            "vals": PB_28_vals,
            "errors": PB_28_error,
            "labels": PB_28_labels,
            "title": PB_28_title,
            "sample": "3 years"
        } 
        return dd28
    
    def _get_dd25_PB(self):
        data_2019 = self.DATA[self.DATA["year"] == 2019]
        
        PB_20_vals =  [
            [len(df[df["rain"] == 0])] + [
                len(df[(df["rain"] > i) & (df["rain"] <= i+30)]) for i in range(0,100,30)
            ] + [len(df[df["rain"] > 90])] 
        for df in [data_2019[data_2019['month'] == i] for i in range(3,8)] ]
        PB_20_error = [[0 for i in range(5)] for j in range(5)]

        PB_20_labels = ["March",'April',"May" "June",'July']

        PB_20_xticks = [
                        '0',
                        '0-30',
                        '30-60',
                        '60-90',
                        '90<'
        ]

        PB_20_title = "Number of Days by Rainfall (in mm)"
        
        dd20 = {
            "vals": PB_20_vals,
            "errors": PB_20_error,
            "labels": PB_20_labels,
            'xticks': PB_20_xticks,
            "title": PB_20_title,
            "sample": "5 months"
        } 
        return dd20

    def _get_dd24_PB(self):
        d = self.DATA.groupby(["year", "month", "clouds"]).count().iloc[:,:1].rename(columns={"temp":"count"})
        means = {}
        for j in range(1,13):
            means[j] = [np.mean(d.xs(j, level="month" ).to_numpy().reshape((3,3))[:,i]) for i in range(3)]

        errs = {}
        for j in range(1,13):
            errs[j] = [np.std(d.xs(j, level="month" ).to_numpy().reshape((3,3))[:,i]) for i in range(3)]

        # two arbitrarily chosen months
        PB_6_vals = [means[i] for i in range(3,11)] 
        PB_6_error = [errs[i] for i in range(3,11)]

        PB_6_labels = ["March",'April',"May" "June",'July','August','September','October']
        PB_6_xticks = ["Clear", "Partly Cloudy", "Very Cloudy"]
        PB_6_title = "Average Cloundiness by Month"
        
        dd06 = {
            "vals": PB_6_vals,
            "errors": PB_6_error,
            "xticks": PB_6_xticks,
            "labels": PB_6_labels,
            "title": PB_6_title,
            "sample": "8 months"
        }
        return dd06