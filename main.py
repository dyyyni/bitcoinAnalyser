import datetime
import cryptoApiModule

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



def main():
    apiControl = cryptoApiModule.CryptoApi()


if __name__ == '__main__':
    main()