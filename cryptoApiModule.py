from datetime import date
import requests
import json

apiURL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"

class CryptoApi:

    vs_currency = "eur"

    def __init__(self):
        self.parameters = {
        "vs_currency": CryptoApi.vs_currency,
        "from" : None,  # utc timestamp
        "to" : None     # utc timestamp
        }
        self.dateFrom = None
        self.dateTo = None
        self.dateRangeCase = None

        self.activeData = None

    def __setActiveData(self, data):
        self.activeData = data

    def __rangeHelper(self, dateFrom, dateTo):
        '''
        The api data granularity is automatic.
        > 90 days range : daily data (00:00) is returned
        < 90 days range : hourly or by 5 min data is returned
        Solution: Automatically extend the range so daily data is returned
        --> Only the actual range data will be returned at the end.
        '''
        days90 = 90*24*60*60 # Seconds
        earlyDateLim = 1374969600 # 28/4/2013 + 90 days
        # case 1: the range is over 90 days
        if dateTo - dateFrom > days90:
            self.dateRangeCase = 'case1'
            return (dateFrom, dateTo)

        # case 2: the range is under 90 days
        # -> dateFrom - 90 days
        elif dateTo - dateFrom < days90 and dateFrom > earlyDateLim:
            self.dateRangeCase = 'case2'
            dateFrom = dateFrom - days90
            return (dateFrom, dateTo)

        # case 3: the range is under 90 days and too close to the earliest date
        # -> dateTo + 90 days
        else:
            dateTo = dateTo + days90
            self.dateRangeCase = 'case3'
            return (dateFrom, dateTo)


    def setRange(self, dateFrom, dateTo):
        (dateFromMod, dateToMod) = self.__rangeHelper(dateFrom, dateTo)
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.parameters["from"] = dateFromMod
        self.parameters["to"] = dateToMod

    def retrieveData(self):
        response = requests.get(apiURL, params=self.parameters)
        self.__setActiveData(response)

    def getActiveData(self):
        datesPrices = self.activeData.json()['prices']
        datesVols = self.activeData.json()['total_volumes']
        # refer to __rangeHelper for case explanation
        if self.dateRangeCase is 'case1':
            return (datesPrices, datesVols)

        elif self.dateRangeCase is 'case2':
            return (datesPrices[90:], datesVols[90:])

        elif self.dateRangeCase is 'case3':
            return (datesPrices[:len(datesPrices)-90], datesVols[:len(datesVols)-90])


    def areParams(self):
        if (self.parameters['from'] and self.parameters['to']) is not None:
            return True
        else:
            return False