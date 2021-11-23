import json

def jprint(activeData):
# create a formatted string of the Python JSON object
    text = json.dumps(activeData, sort_keys=True, indent=4)
    print(text)


class Data:

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
        datesPrices = self.getDatesPrices()
        longestStreak = 0

        streak = 0
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


