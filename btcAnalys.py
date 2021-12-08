import sys
import datetime
import cryptoApiModule
import dataAnalysModule

def parser(date):
    '''
    parser function takes a date 'dd/mm/yyyy' and returns a list [dd,mm,yyyy].
    This function only provides string manipulation. I.e. no validity checks.
    '''
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

def isDateValid(parsedDate):
    '''
    isDateValid function is used to check the date validity.
    Try-except is used to determine the date validity. If an invalid date is entered
    the user will be notified and a false leading to program exit will be returned.
    Return : timestamp from a valid date / False
    '''
    dateNow = datetime.datetime.utcnow()
    dateLowLimit = datetime.datetime(2013,4,28) # 28/4/2013
    try:
        # datetime requires the form yyyy/dd/mm
        date = datetime.datetime(int(parsedDate[2]), int(parsedDate[1]), int(parsedDate[0]))
        if date > dateNow:
            print(f"As of now, I can't see to the future. The 'to date' is set to {dateNow.strftime('%d/%m/%Y')}.")
            date = dateNow
        if date < dateLowLimit:
            print(f"My data sources only reach to 28/4/2013. It's set as the 'from date'.")
            date = dateLowLimit
        utcTimestamp = date.replace(tzinfo=datetime.timezone.utc).timestamp()
        return utcTimestamp
    except (ValueError, IndexError):
        return False

def control(fromDate, toDate, apiControl, dataAnalys, flag):
    
    apiControl.setRange(fromDate, toDate)
    apiControl.retrieveData()
    datesPrices, datesVols = apiControl.getActiveData()
    dataAnalys.setActiveData(datesPrices, datesVols)
    
    if flag == "-dt":
        print(dataAnalys.getLongestDownTrend())

    elif flag == "-hv":
        dateVolume = dataAnalys.getHighestTradeVol()
        highDate = datetime.datetime.fromtimestamp(dateVolume[0]).strftime('%d/%m/%Y')
        print(f'{highDate} {dateVolume[1]}')

    elif flag == "-bp":
        bestProfit = dataAnalys.getBestProfit()
        if not bestProfit:
            print("Do not buy or sell. The price trend only decreases in this range.")
        else:
            bestBuyDate = datetime.datetime.fromtimestamp(bestProfit[0]).strftime('%d/%m/%Y')
            bestSellDate = datetime.datetime.fromtimestamp(bestProfit[1]).strftime('%d/%m/%Y')
            print(f"{bestBuyDate} {bestSellDate}")

def main():
    flags =  ['-h', '-dt', '-hv', '-bp']
    args = sys.argv

    if len(args) == 1:
        print("Use: btcAnalys.py dd/mm/yyyy dd/mm/yyyy -flag. (-h for options)")
        return
    if args[1] == '-h':
        print("-h: help, -dt: longest down trend, -hv: highest trade volume, -bp: best profit ")
        return
    if args[3] not in flags:
        print("Argument does not exist")
        return

    fromDate = isDateValid(parser(args[1]))
    toDate = isDateValid(parser(args[2]))
    if fromDate >= toDate:
        print("Program terminated. fromDate can't be smaller than or equal to toDate.")
        exit(1)
    flag = args[3]

    if not fromDate or not toDate:
        print("Incorrect date.")
        exit(1)

    apiControl = cryptoApiModule.CryptoApi()
    dataAnalys = dataAnalysModule.Data()
    control(fromDate, toDate, apiControl, dataAnalys, flag)




if __name__ == '__main__':
    main()