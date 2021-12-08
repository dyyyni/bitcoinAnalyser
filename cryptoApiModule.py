import requests

apiURL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"

class CryptoApi:
    '''
    This class is used to create objects that can access the coingecko cryptocurrency API.
    '''
    # The currency used in this application. Could be changed to any currency available
    # in the API
    vs_currency = "eur"

    def __init__(self):

        # These parameters are used to access the API.
        self.parameters = {
        "vs_currency": CryptoApi.vs_currency,
        "from" : None,  # utc timestamp
        "to" : None     # utc timestamp
        }
        self.dateFrom = None
        self.dateTo = None
        self.dateRangeCase = None # Refer to __rangeHelper function

        self.activeData = None

    def __setActiveData(self, data):
        self.activeData = data

    def __rangeHelper(self, dateFrom, dateTo):
        '''
        The api data granularity is automatic.
        > 90 days range : daily data (00:00) is returned
        < 90 days range : hourly or by 5 min data is returned
        Solution: Automatically extend the range so daily data is returned
        --> Only the actual range data will exit this module.
        3 different cases are used to categorize the different outcomes. 
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
        '''
        Sets the from and to parameters and the separate dateFrom and dateTo parameters.
        (..)Mod dates are extend ranges of dates as explained in __rangeHelper
        '''
        (dateFromMod, dateToMod) = self.__rangeHelper(dateFrom, dateTo)
        self.dateFrom = dateFrom
        self.dateTo = dateTo
        self.parameters["from"] = dateFromMod
        self.parameters["to"] = dateToMod

    def retrieveData(self):
        '''
        This method accesses the API to retrieve the data
        '''
        response = requests.get(apiURL, params=self.parameters)
        self.__setActiveData(response)

    def getActiveData(self):
        '''
        Returns the activeData in the correct time range.
        As explained in __rangeHelper, the date range is extented to smooth the api data granularity
        This method utilises splicing and the different cases to return only the correct range of data.
        '''
        datesPrices = self.activeData.json()['prices']
        datesVols = self.activeData.json()['total_volumes']
        # refer to __rangeHelper for case explanation
        if self.dateRangeCase == 'case1':
            return datesPrices, datesVols

        elif self.dateRangeCase == 'case2':
            return datesPrices[90:], datesVols[90:]

        elif self.dateRangeCase == 'case3':
            return datesPrices[:len(datesPrices)-90], datesVols[:len(datesVols)-90]

    def getRange(self):
        return self.dateFrom, self.dateTo

    def areParams(self):
        if (self.parameters['from'] and self.parameters['to']) is not None:
            return True
        else:
            return False
    
    def isData(self):
        if self.activeData is not None:
            return True
        else:
            return False