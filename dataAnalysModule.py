class Data:
    '''
    This class is used to create objects with differing datePrices and dateVols
    variables. The main objective of the class is to analyse the data with the
    methods.
    '''

    def __init__(self):
        self.datesPrices = None
        self.datesVols = None

    def setActiveData(self, newDatesPrices, newDatesVols):
        self.datesPrices = newDatesPrices
        self.datesVols = newDatesVols

    def getDatesPrices(self):
        return self.datesPrices

    def getDatesVols(self):
        return self.datesVols

    def getLongestDownTrend(self):
        '''
        Finds the longest downward trend of prices in the data range.
        Return : the longest downward streak (int)
        '''
        datesPrices = self.getDatesPrices()
        longestStreak = 0

        streak = 0
        # If the next price is smaller than the price before -> increment streak
        # If not save the streak as longest and start over until the end of datapoints.
        for i in range(len(datesPrices)):
            if i == len(datesPrices)-1:
                if streak > longestStreak:
                    longestStreak = streak
                break
            if datesPrices[i+1][1] < datesPrices[i][1]:
                streak += 1
            else:
                if streak > longestStreak:
                    longestStreak = streak
                    streak = 0
                else:
                    streak = 0

        return longestStreak

    def getHighestTradeVol(self):
        '''
        Finds the highest trading volume and the date from data.
        Return : (date, highest volume)
        '''
        datesVolumes = self.getDatesVols()
        highestVol = 0
        date = datesVolumes[0][0]

        for dateVolume in datesVolumes:
            if dateVolume[1] > highestVol:
                highestVol = dateVolume[1]
                date = dateVolume[0]
        # /1000 --> milliseconds to seconds conversion
        return (date/1000, highestVol)

    def getBestProfit(self):
        '''
        Finds the best day to buy and the best day to sell the curremcy
        returns : (1) list with buy date, sell date and the best profit
                  (2) False if the range only has a downward trend of price
        '''
        datesPrices = self.getDatesPrices()

        # Returned at the end of the algorithm
        buyDate = None
        sellDate = None
        bestProfit = 0

        # Used as intermediates during the algorithm
        resBuyDate = datesPrices[0][0]
        buyPrice = datesPrices[0][1]
        sellPrice = None
        profit = 0

        # Important points for the algorithm :
        # low points  : starts a new instance to find the best profit
        # high points : high point - low point = profit. These are compared
        # to find the best possible outcome.
        for datePrice in datesPrices[1:]:
            if datePrice[1] > buyPrice:
                sellPrice = datePrice[1]
                profit = sellPrice - buyPrice
                if profit > bestProfit:
                    bestProfit = profit
                    sellDate = datePrice[0]
                    buyDate = resBuyDate
            if datePrice[1] < buyPrice:
                buyPrice = datePrice[1]
                sellPrice = None
                resBuyDate = datePrice[0]

        if sellDate == None:
            return False
        else:
            # /1000 --> milliseconds to seconds conversion
            return [buyDate/1000, sellDate/1000, bestProfit]