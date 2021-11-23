import requests

apiURL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range"

class CryptoApi:

    vs_currency = "eur"

    def __init__(self):
        self.parameters = {
        "vs_currency": CryptoApi.vs_currency,
        "from" : None,  # utc timestamp
        "to" : None     # utc timestamp
        }

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
        # case 1: the range is over 90 days

        # case 2: the range is under 90 days
        # -> dateFrom - 90 days

        # case 3: the range is under 90 days and too close to the earliest date
        # -> dateTo + 90 days


    def setRange(self, dateFrom, dateTo):
        self.parameters["from"] = dateFrom
        self.parameters["to"] = dateTo