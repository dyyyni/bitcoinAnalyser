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
                print(f"Bitcoin was released 1/3/2009, but my data sources only reach 28/4/2013.")
                date = dateLowLimit
            utcTimestamp = date.replace(tzinfo=datetime.timezone.utc).timestamp()
            correctDate = True
            return utcTimestamp
        except (ValueError, IndexError):
            print("Incorrect date. Try again (dd/mm/yyyy): ", end='')
            correctDate = False

def commandCenter(command, apiObject):
    commands =  ['help', 'setRange', 'getData', 'show'
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
        else:
            print(errorMessages[1])

    elif command == 'show':
        dataAnalysModule.jprint(apiObject.getActiveData())



def main():
    apiControl = cryptoApiModule.CryptoApi()

    print("This application retrieves bitcoin price information.")
    print("I'm able to gather information from 28/4/2013 to present day.")
    print("Type 'help' for commands.")

    while True:
        command = input("Enter command: ")
        commandCenter(command, apiControl)


if __name__ == '__main__':
    main()