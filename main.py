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