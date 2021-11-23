import datetime
import cryptoApiModule
import dataAnalysModule

def parser(date):
    parsedDate = date.split('/')

    # The date was instructed to be filled in as 'dd/mm/yyyy'
    if len(parsedDate) == 3:
        return parsedDate
    # This tackles a few common input errors
    if len(parsedDate) != 3:
        parsedDate = date.split()
        if len(parsedDate) != 3:
            parsedDate = date.split('-')
            if len(parsedDate) != 3:
                parsedDate = date.split('.')
        return parsedDate


def askDate():
    correctDate = None
    dateNow = datetime.datetime.utcnow()
    dateLowLimit = datetime.datetime(2013,4,28) # 28/4/2013

    while not correctDate:
        try:
            askDate = parser(input())
            # datetime requires the form yyyy/dd/mm
            date = datetime.datetime(int(askDate[2]), int(askDate[1]), int(askDate[0]))
            if date > dateNow:
                print(f"As of now, I can't see to the future. The date is set to {dateNow.strftime('%d/%m/%Y')}.")
                date = dateNow
            if date < dateLowLimit:
                print(f"My data sources only reach to 28/4/2013. It's set as the date.")
                date = dateLowLimit
            utcTimestamp = date.replace(tzinfo=datetime.timezone.utc).timestamp()
            correctDate = True
            return utcTimestamp
        except (ValueError, IndexError):
            print("Incorrect date. Try again (dd/mm/yyyy): ", end='')
            correctDate = False

def commandCenter(command, apiObject, dataAnalys):
    commands =  ['help', 'setRange', 'getData', 'exit', 'rangeNow', 'longDown',
                 'highVol', 'bestProf', 'show'
                ]
    enterDatePrompt =   ["Enter the first date in form (dd/mm/yyyy): ",
                         "Enter the last date in form (dd/mm/yyyy): "
                        ]
    errorMessages =     ["The first date can't be smaller than the last date!",
                         "You have to set the range first!",
                         "Set the range and retrieve the data (getData) first!",
                         "Incorrect command. Try again.",
                         "No data found in this range."
                        ]

    if command not in commands:
        print(errorMessages[3])

    elif command == 'help':
        print(commands)

    elif command == 'setRange':
        print(enterDatePrompt[0], end='')
        fromDate = askDate()
        print(enterDatePrompt[1], end='')
        toDate = askDate()
        if toDate > fromDate:
            apiObject.setRange(fromDate, toDate)
        else:
            print(errorMessages[0])

    elif command == 'getData':
        if apiObject.areParams():
           apiObject.retrieveData()
           datesPrices, datesVols = apiObject.getActiveData()
           dataAnalys.setActiveData(datesPrices, datesVols)
        else:
            print(errorMessages[1])

    elif command == 'rangeNow':
        firstDate, lastDate = apiObject.getRange()
        if firstDate != None:
            firstDate = datetime.datetime.fromtimestamp(firstDate).strftime('%d/%m/%Y')
        if lastDate != None:
            lastDate = datetime.datetime.fromtimestamp(lastDate).strftime('%d/%m/%Y')
        print(f"{firstDate} - {lastDate}")

    elif command == 'longDown':
        if apiObject.areParams() and apiObject.isData():
            downStreak = dataAnalys.getLongestDownTrend()
            print(f"The longest streak for price decrease was {downStreak} days in a row with given inputs.")
        else:
            print(errorMessages[2])

    elif command == 'highVol':
        if apiObject.areParams() and apiObject.isData():
            dateVolume = dataAnalys.getHighestTradeVol()
            highDate = datetime.datetime.fromtimestamp(dateVolume[0]).strftime('%d/%m/%Y')
            print(f'The highest trading volume was on {highDate}: {dateVolume[1]} eur')
        else:
            print(errorMessages[2])

    elif command == 'bestProf':
        if apiObject.areParams() and apiObject.isData():
            bestProfit = dataAnalys.getBestProfit()
            if not bestProfit:
                print("Do not buy or sell. The price trend only decreases in this range.")
            else:
                bestBuyDate = datetime.datetime.fromtimestamp(bestProfit[0]).strftime('%d/%m/%Y')
                bestSellDate = datetime.datetime.fromtimestamp(bestProfit[1]).strftime('%d/%m/%Y')
                print(f"The best date to buy is {bestBuyDate}")
                print(f"The best date to sell is {bestSellDate}")

        else:
            print(errorMessages[2])

    elif command == 'show':
        dataAnalysModule.jprint(apiObject.getActiveData())

    elif command == 'exit':
        print('See you later!')
        exit(0)



def main():
    apiControl = cryptoApiModule.CryptoApi()
    dataAnalys = dataAnalysModule.Data()

    print("This application retrieves bitcoin price information.")
    print("I'm able to gather information from 28/4/2013 to present day.")
    print("Type 'help' for commands.")

    while True:
        command = input("Enter command: ")
        commandCenter(command, apiControl, dataAnalys)


if __name__ == '__main__':
    main()