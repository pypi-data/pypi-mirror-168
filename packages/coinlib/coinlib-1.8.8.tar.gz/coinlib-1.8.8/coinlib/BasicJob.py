import aio_pika
import numpy as np
import simplejson as json
from aio_pika import connect, Message, DeliveryMode, ExchangeType

from coinlib import helper, Registrar
from coinlib.BasicJobSessionStorage import BasicJobSessionStorage, LastSignalValue
from coinlib.WorkerJobProcess import WorkerJobProcess
from coinlib.data.DataTable import DataTable, LastEntry
from coinlib.feature.FeatureDTO import RabbitInfo
import pandas as pd
import coinlib.dataWorker_pb2 as statsModel
import coinlib.dataWorker_pb2_grpc as stats

class BasicJob:
    def __init__(self, table: DataTable, inputs, storageManager = None):
        self.table = table
        if storageManager is None:
            storageManager = BasicJobSessionStorage()
        self._df = self.table.getDf()
        self.df = self.table.getDf()
        self.registrar = Registrar()
        self._storageManager = storageManager
        self._storageManager.setCurrentIndex(self.closeDate())
        self.inputs = inputs
        self.uniqueName = ""
        self._sessionInfo = self._storageManager.getStorage()
        self.features = self

        ## gets a signal data

    def getStub(self) -> stats.DataWorkerStub:
        pass

    def getWorker(self) -> WorkerJobProcess:
        pass

    def set(self, name, data, index=None):

        return self.table.setColumn(name, data, index)

    def getOutputCol(self):
        return "result"

    def result(self, resultList, colname=None, fillType="front", type=np.float):

        #if isinstance(resultList, np.ndarray):
        #    resultList = np.pad(resultList, (self.df.shape[0] - len(resultList), 0), 'constant', constant_values=(np.nan))

        #self.df[self.getOutputCol()] = resultList
        self.table.setColumn(self.getOutputCol(), resultList, pad=True, type=type)

        return self.table.column(self.getOutputCol())

    ## This method adds a signal
    def wasSignal(self, name, maxSecondsDistance=0, minSecondsDistance=0, logicId=None):
        lastValue = self._storageManager.getLastSignal(logicId if logicId is not None else self.getUniqueName(), name)

        if lastValue.found is True:
            if minSecondsDistance > 0:
                if lastValue.distanceSeconds > minSecondsDistance:
                    return True
            if maxSecondsDistance > 0:
                if lastValue.distanceSeconds < maxSecondsDistance:
                    return True

        return False

    ## This method adds a signal
    def lastSignal(self, name, logicId=None) -> LastSignalValue:

        return self._storageManager.getLastSignal(logicId if logicId is not None else self.getUniqueName(), name)

    ## This method adds a signal
    def signal(self, name, data=None, index=-1, logicId=None) -> LastSignalValue:

        if data is not None:
            return self._storageManager.setSignal(logicId if logicId is not None else self.getUniqueName(), name, data)

        return self._storageManager.getSignal(logicId if logicId is not None else self.getUniqueName(), name)

    def getInputValue(self, input):

        if isinstance(input, dict):
            if "value" in input:
                return input["value"]

        return input


    def getNow(self, name):
        return self.current(name)

    def getCurrent(self, name):
        return self.current(name)

    def logger(self):
        return self.registrar.logger

    def get(self, name, index=None, filterNone = False, replaceNone=None):

        data = None
        try:
                maybe_col_name = name
                if ":" in maybe_col_name:
                    maybe_col_name = maybe_col_name.split(":")[0]

                # if its a key of inputs - lets export the right column
                if maybe_col_name in self.inputs:
                    if isinstance(self.inputs[maybe_col_name], str):
                        return self.get(self.getInputValue(self.inputs[maybe_col_name]), index, filterNone, replaceNone)
                    if self.inputs[maybe_col_name]["type"] == "dataInput":
                        return self.get(self.getInputValue(self.inputs[maybe_col_name]["value"]), index, filterNone, replaceNone)

                data = None
                if maybe_col_name + ":y" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":y")
                elif "additionalData."+maybe_col_name in self.table.columns:
                    data = self.table.column("additionalData."+maybe_col_name, index)
                elif maybe_col_name + ":close" in self.table.columns:
                    data = self.table.column(maybe_col_name + ":close", index)
                elif name in self.table.columns:
                    data = self.table.column(name, index)
                elif "stats."+maybe_col_name in self.table.columns:
                    data = self.table.column("stats."+maybe_col_name, index)
                elif "stats." + name in self.table.columns:
                    data = self.table.column("stats." + name, index)
                elif maybe_col_name in self.inputs:
                    data = self.inputs[name]
        except Exception as e:
            self.logger().error(e)

        if data is not None:
            if isinstance(data, list) or isinstance(data, (np.ndarray, np.generic)):
                if len(data) > 1:
                    data = [i if not np.isnan(i) else None for i in data]
                    if filterNone is True:
                        data = [i for i in data if i is not None]
                    if replaceNone is not None:
                        data = [0 if i is None else i for i in data]
                else:
                    return data[0]
            else:
                if np.isnan(data):
                    data = None


        return data

    def getAsCandle(self, name, index=None) -> {"open": [], "high": [], "low": [], "close": [], "volume": []}:

        data = {
            "open": self.getAsArray(name+":open", index),
            "high": self.getAsArray(name+":high", index),
            "low": self.getAsArray(name+":low", index),
            "close": self.getAsArray(name+":close", index),
            "volume": self.getAsArray(name+":volume", index),
        }

        return data

    def getAsArray(self, name, index=None, type=float):

        data = self.get(name, index=index)

        # filter data and remove nans in the beginning

        if data is not None and len(data) > 0:
            if data[0] is None or np.isnan(data[0]):
                index = 0
                for f in data:
                    if f is None or np.isnan(f):
                        index = index + 1
                    else:
                        break
                data = data[index:]
        float_data = np.array(data, dtype=float)
        return float_data

    ## This method combines all params and combine as a dataframe
    def df(self):
        return self.df

    def last(self, name, maxDistance=100, filterNone=False, replaceNone=None) -> LastEntry:

        data = None
        try:
            maybe_col_name = name
            if ":" in maybe_col_name:
                maybe_col_name = maybe_col_name.split(":")[0]

            # if its a key of inputs - lets export the right column
            if maybe_col_name in self.inputs:
                if isinstance(self.inputs[maybe_col_name], str):
                    return self.last(self.getInputValue(self.inputs[maybe_col_name]))
                if self.inputs[maybe_col_name]["type"] == "dataInput":
                    return self.last(self.getInputValue(self.inputs[maybe_col_name]["value"]))

            data = None
            if maybe_col_name + ":y" in self.table.columns:
                data = self.table.getLastEntry(maybe_col_name + ":y")
            elif name in self.table.columns:
                data = self.table.getLastEntry(name, maxLength=maxDistance)
            elif "additionalData." + maybe_col_name in self.table.columns:
                data = self.table.getLastEntry("additionalData." + maybe_col_name, maxLength=maxDistance)
            elif maybe_col_name + ":close" in self.table.columns:
                data = self.table.getLastEntry(maybe_col_name + ":close", maxLength=maxDistance)
            elif "stats." + maybe_col_name in self.table.columns:
                data = self.table.getLastEntry("stats." + maybe_col_name, maxLength=maxDistance)
            elif "stats." + name in self.table.columns:
                data = self.table.getLastEntry("stats." + name, maxLength=maxDistance)

        except Exception as e:
            self.logger().error(e)

        if data is not None:
            return data

        return data

    def getNow_date(self):
        dt = self.table.getLast("datetime")
        return dt

    def current(self, name):
        return self.get(name, index=-1)

    def statistic(self, name="r_master"):

        return self.current("stats."+name)

    def lastStatistic(self, name="r_master"):

        return self.last("stats."+name)

    def setVar(self, name, data, logicId=None):

        return self.var(name, data, logicId=logicId)

    def setUniqueName(self, name):
        self.uniqueName = name
        return name

    def getUniqueName(self):
        return self.uniqueName

    def price(self, chart="chart1"):
        return self.table.getLast(chart+".main:close")

    def isNaN(self, num):
        return num != num

    def additional(self, name):

        index = -1

        if "additionalData." + name in self.table.columns:
            data = self.table.lastElement("additionalData." + name)
            if self.isNaN(data):
                return None
            return data

        return None

    def date(self):
        date = pd.to_datetime(self.table.index[-1])
        return date

    def closeDate(self):
        date = pd.to_datetime(self.table.index[-1])
        return date

    def time(self):
        date = pd.to_datetime(self.table.index[-1])
        return date

    ## This method adds a signal
    def var(self, name, data=None, logicId=None):

        if data is not None:
            return self._storageManager.setVar(logicId if logicId is not None else self.getUniqueName(), name, data)

        return self._storageManager.getVar(logicId if logicId is not None else self.getUniqueName(), name)

    def destroy(self):

        pass