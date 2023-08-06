import pandas as pd
import numpy as np
from coinlib.BasicJob import BasicJob
import time

from coinlib.data.DataTable import DataTable

def isFullOHLC(row):
    return (row.close != 0 and row.close != None and row.open != 0 and row.open != None and
            row.high != 0 and row.high != None and row.low != None and row.low != 0)


class ChartsIndicatorJob(BasicJob):
    def __init__(self, name, group, inputs, df, indicator, worker):
        super(ChartsIndicatorJob, self).__init__(DataTable(df), inputs)
        self.name = name
        self.group = group
        self.send = False
        self.chunked = False
        self.worker = worker
        self.data = []
        self.indicator = indicator
    
    def isChunked(self):
        return self.chunked
    
    def setChunked(self, chunked):
        self.chunked = chunked
        return True

    def getUniqueName(self):
        return self.uniqeName

    def getDateTimeFromISO8601String(self, s):
        import datetime
        import dateutil.parser
        d = dateutil.parser.parse(s)
        return d

    
    def series(self, chartType, name, data, color=None, opacity=None, size=None):

        if (color == None):
            color = "#ccffcc"
        import datetime
        import pytz

        utc=pytz.UTC
        latestDate = datetime.datetime(1971, 3, 19, 13, 0, 9, 351812)
        latestDate = utc.localize(latestDate) 
        
        chart = {
            "chartType": chartType,
            "name": name,
            "data": [],
            "color": color
        }

        column_names = []
        # check if output data is a series, a dataframe or a array
        if isinstance(data, (list, pd.core.series.Series, pd.DataFrame, int, float, np.ndarray)):

            if isinstance(data, (list)):
                # its a list
                self.table.setColumn(":y", data)
                column_names = [":y"]

            elif isinstance(data, (int, float)):

                self.table.setColumn(":y", [data])
                column_names = [":y"]

            elif isinstance(data, (pd.core.series.Series)):

                self.table.setColumn(":y", data.values)
                column_names = [":y"]

            elif isinstance(data, (pd.DataFrame)):
                # its a dataframe
                self.table.setColumn(":open", data["open"])
                self.table.setColumn(":high", data["high"])
                self.table.setColumn(":low", data["low"])
                self.table.setColumn(":close", data["close"])
                self.table.setColumn(":volume",  data["volume"])
                column_names = [":open", ":high", ":low", ":close", ":volume"]

            elif isinstance(data, (np.ndarray)):
                # it is a numpy array
                self.table.setColumn(":y", data)
                column_names = [":y"]




        else:
            raise Exception("Please send your data as pandas.series, list, ndarray or pd.dataframe")

        options = {}

        if (color != None):
            options["color"] = color
        if (opacity != None):
            options["opacity"] = opacity
        if (size != None):
            options["size"] = size
        options["chartType"] = chartType
        """
        try:
            chart["data"] = df[column_names]
        except Exception as e:
            log.error(e)
            pass
        chart["options"] = options"""

        self.worker.onPartialChartDataReceived(self.indicator, name, self.table.subTable(columns=column_names), options)
        
        return True
    
    
    def line(self, chartType, name, selector, data):
        
        return True
    
    
    def plot(self, chartType, name, selector, data):
        
        return True
    
    def getSessionData(self):
        
        sess_list = None
        columns = []
        for colname in self.df.columns:
            if (colname.startswith("session:") and "Datetime" not in colname):
                columns.append(colname)
        
        if (len(columns) > 0):
            sessionDf = pd.DataFrame(self.df, columns=columns)

            sessionDf["date"] = sessionDf.index.to_series().apply(lambda x: x.isoformat())
            ###sessionDf.select_dtypes(exclude=['datetime', 'datetime64','datetimetz'])
            sessionDf.reset_index(drop=True, inplace=True)
            ##sessionDf.drop(columns='session:Datetime')

            sess_list = sessionDf.to_dict()
            
            

        return sess_list

    
        
