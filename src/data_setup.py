from itertools import product

import numpy as np
import pandas as pd

class PlottedData:
    raw = pd.read_csv("data.csv")
    
    def __init__(self):
        self.DATA = self.raw[self.raw["year"].isin([2017,2018,2019])]

        self.MONTHS  = [
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

        # cloudiness data
        d = self.DATA.groupby(["year", "month", "clouds"]).count().iloc[:,:1].rename(columns={"temp":"count"})

        self.means = {
            j: [np.mean(d.xs(j, level="month").to_numpy().reshape((3,3))[:,i]) for i in range(3)] for j in range(1,13)
        }
        self.errs = {
            j: [np.std(d.xs(j, level="month").to_numpy().reshape((3,3))[:,i]) for i in range(3)] for j in range(1,13)
            }
            
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

        dd02 = {
            "vals": [len(data_2017[data_2017["rain"] <= 1]), len(data_2017[data_2017["rain"] > 1])],
            "labels": ["No rain", "Rainy"],
            "title": "Number of Rainy Days",
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

        dd06 = {
            "vals": PP_PD_6_vals,
            "labels": PP_PD_6_labels,
            "title": "Number of Days by Temperature",
            "sample": "12 months"
        }
        return dd06

    def _get_dd12_PP_PD(self):
        data_2017 = self.DATA[self.DATA["year"] == 2017]
        rain_by_month = data_2017.loc[:,['month', 'dates']][data_2017["rain"] > 1].groupby("month").count()
       
        dd12 = {
            "vals": [i[0] for i in rain_by_month.values.tolist()],
            "labels": self.MONTHS,
            "title": "Number of Rainy Days by Month",
            "sample": "12 months"
        }
        return dd12

    def _get_dd02_PB(self):
        rainy_days = self.DATA[self.DATA['rain'] >= 1].groupby('year').count().iloc[:,:1].values.reshape((1,3))[0]
        nonrainy_days = self.DATA[self.DATA['rain'] < 1].groupby('year').count().iloc[:,:1].values.reshape((1,3))[0]
        
        dd02 = {
            "vals": [np.mean(nonrainy_days), np.mean(rainy_days)],
            "errors": [np.std(nonrainy_days), np.std(rainy_days)],
            "labels": ["No rain", "Rainy"],
            "title": "Average Number of Rainy Days",
            "sample": "3 years"
        }
        return dd02

    def _get_dd06_PB(self):
        dd06 = {
            "vals": [self.means[6], self.means[12]] ,
            "errors": [self.errs[6], self.errs[12]],
            "xticks": ["Clear", "Partly Cloudy", "Very Cloudy"],
            "labels": ["June", "December"],
            "title":  "Average Cloundiness by Month",
            "sample": "12 months"
        }
        return dd06

    def _get_dd12_PB(self):
       
        dd12 = {
            "vals": list(self.DATA.loc[:,['month', 'temp']].groupby("month").mean().values.reshape((1,12))[0]),
            "errors": list(self.DATA.loc[:,['month', 'temp']].groupby("month").std().values.reshape((1,12))[0]),
            "labels": self.MONTHS,
            "title": "Average Temperature by Month",
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

        dd09 = {
            "vals": PP_PD_09_vals,
            "labels": PP_PD_09_labels,
            "title": "Number of Days by Rainfall (in mm)",
            "sample": "1095 days"
        }
        return dd09

    def _get_dd09_PB(self):
        
        dd09 = {
            "vals": [self.means[3], self.means[6], self.means[12]] ,
            "errors": [self.errs[3], self.errs[6], self.errs[12]],
            "xticks": ["Clear", "Partly Cloudy", "Very Cloudy"],
            "labels": ["March","June", "December"],
            "title": "Average Cloundiness by Month",
            "sample": "3 months"
        } 
        return dd09
    
    def _get_dd03_PP_PD(self):

        PP_PD_03_vals = [
                round(self.DATA[(self.DATA["rain"] >= 10) & (self.DATA["month"] == 3)].groupby(['year']).count().iloc[:,:1].values.reshape(1,3).mean(),1),
                round(self.DATA[(self.DATA["rain"] >= 10) & (self.DATA["month"] == 4)].groupby(['year']).count().iloc[:,:1].values.reshape(1,3).mean(),1),
                round(self.DATA[(self.DATA["rain"] >= 10) & (self.DATA["month"] == 5)].groupby(['year']).count().iloc[:,:1].values.reshape(1,3).mean(),1)
        ]

        dd03 = {
            "vals": PP_PD_03_vals,
            "labels": ['March','April','May'],
            "title": "Average Number of Rainy Days in the Spring",
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

        dd03 = {
            "vals": [means[3], means[4], means[5]],
            "errors": [errs[3], errs[4], errs[5]],
            #"xticks": PB_3_xticks,
            "labels": ["March", "April", "June"],
            "title": "Average Number of Rainy Days in the Spring",
            "sample": "3 months"
        } 
        return dd03
    
    def _get_dd10_PP_PD(self):
        data_2019 = self.DATA[self.DATA["year"] == 2019]

        dd10 = {
            "vals": [
                round(i,1) for i in data_2019.groupby(['month']).mean().loc[3:,["rain"]].values.reshape(10)
                ],
            "labels": self.MONTHS[3:],
            "title": "Average Rainfall by Month (in mm)",
            "sample": "10 months"
        }
        return dd10

    def _get_dd10_PB(self):
        d = self.DATA[(self.DATA["month"] >= 3) & (self.DATA["month"] <= 7)].groupby(["year", "month"]).mean().iloc[:,1:].values.reshape(3,5)
        
        dd10 = {
            "vals": [d[0], d[1]],
            "errors": [[0 for i in range(5)], [0 for i in range(5)]], # no errors,
            "xticks": ["March", "April", "May", "June","July"],
            "labels": ["This Year","Last Year"],
            "title": "Average Rainfall by Month (in mm)",
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

        dd15 = {
            "vals": PP_PD_15_vals,
            "labels": PP_PD_15_labels,
            "title": "Number of Days by Rainfall (in mm)",
            "sample": "1095 days"
        }
        return dd15
    
    def _get_dd15_PB(self):
        d = self.DATA[(self.DATA["month"] >= 3) & (self.DATA["month"] <= 7)].groupby(["year", "month"]).mean().iloc[:,1:].values.reshape(3,5)
        
        dd10 = {
            "vals": [d[0], d[1], d[2]],
            "errors": [[0 for i in range(5)], [0 for i in range(5)], [0 for i in range(5)]], # no errors
            "xticks":  ["March", "April", "May", "June","July"],
            "labels": ["This Year","Last Year","2 Years Ago"],
            "title": "Average Rainfall by Month (in mm)",
            "sample": "3 years"
        } 
        return dd10

    def _get_dd18_PP_PD(self):
        d = self.DATA[self.DATA["clouds"] == 'clear'].groupby(['year','month']).count().iloc[:,:1].values.reshape(3,12)
        
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

        dd18 = {
            "vals": np.array([i[6:] for i in d]).reshape(18),
            "labels": PP_PD_18_labels,
            "title": "Number of Sunny Days in Second Half of the Year",
            "sample": "3 years"
        }
        return dd18
    
    def _get_dd18_PB(self):
        d = self.DATA[(self.DATA["month"] >= 3) & (self.DATA["month"] <= 8)].groupby(["year", "month"]).mean().iloc[:,1:].values.reshape(3,6)

        dd10 = {
            "vals": [d[0], d[1], d[2]] ,
            "errors": [[0 for i in range(6)], [0 for i in range(6)], [0 for i in range(6)]], # no errors
            "xticks": ["March", "April", "May", "June","July", 'August'],
            "labels": ["This Year","Last Year","2 Years Ago"],
            "title": "Average Rainfall by Month (in mm)",
            "sample": "3 years"
        } 
        return dd10

    def _get_dd20_PP_PD(self):
        
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

        dd20 = {
            "vals": [
                len(self.DATA[(self.DATA["rain"] >= i) & (self.DATA["rain"] < i+5)]) for i in range(0,91,5)] + [len(self.DATA[self.DATA["rain"] > 95])
            ],
            "labels": PP_PD_20_labels,
            "title": "Number of Days by Rainfall (in mm)",
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
        
        dd20 = {
            "vals": PB_20_vals,
            "errors": [[0 for i in range(10)] for j in range(2)], #no errors
            "labels": ['December','January'],
            'xticks': PB_20_xticks,
            "title": "Number of Days by Rainfall (in mm)",
            "sample": "2 months"
        } 
        return dd20
    
    def _get_dd28_PP_PD(self):
        f = np.array([self.DATA[(self.DATA['month']==2)&(self.DATA['year']==i)]['rain'].values for i in [2017,2018,2019]])
        
        PP_PD_28_vals = np.mean(f, axis=0).round()

        dd28 = {
            "vals": [int(i) if i>0 else 10 for i in PP_PD_28_vals],
            "labels": [i for i in range(1,29)],
            "title": "Average Rainfall by Day (in mm) in February",
            "sample": "3 years"
        }
        return dd28
    
    def _get_dd28_PB(self):
        f = np.array([self.DATA[(self.DATA['month']==2)&(self.DATA['year']==i)]['rain'].values for i in [2017,2018,2019]])
        
        PB_28_vals = np.mean(f, axis=0)
        
        dd28 = {
            "vals": [i if i>0 else 10 for i in PB_28_vals],
            "errors": np.std(f, axis=0),
            "labels": [i for i in range(1,29)],
            "title": "Mean Rainfall by Day (in mm) - February",
            "sample": "3 years"
        } 
        return dd28
    
    def _get_dd25_PB(self):
        data_2019 = self.DATA[self.DATA["year"] == 2019]
        
        PB_20_vals =  [
            [len(df[df["rain"] == 0])] + [
                len(df[(df["rain"] > i) & (df["rain"] <= i+30)]) for i in range(0,90,30)
            ] + [len(df[df["rain"] > 90])] 
        for df in [data_2019[data_2019['month'] == i] for i in range(3,8)] ]
        
        dd20 = {
            "vals": PB_20_vals,
            "errors": [[0 for i in range(5)] for j in range(5)], #no errors
            "labels": ["March",'April',"May","June",'July'],
            'xticks': ['0','0-30','30-60','60-90','90<'],
            "title": "Number of Days by Rainfall (in mm)",
            "sample": "5 months"
        } 
        return dd20

    def _get_dd24_PB(self):
        
        dd24 = {
            "vals": [self.means[i] for i in range(3,11)],
            "errors": [self.errs[i] for i in range(3,11)],
            "xticks": ["Clear", "Partly\nCloudy", "Very\nCloudy"],
            "labels": ["March",'April',"May","June",'July','August','September','October'],
            "title": "Average Cloundiness by Month",
            "sample": "8 months"
        }
        return dd24