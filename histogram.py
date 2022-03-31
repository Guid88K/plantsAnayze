def histogram(list):
    if all(n <= 0 for n in list):
        return
    else:
        _list = [
            (lambda x: x - 1)(n) for n in list
        ]
        histogram(_list)

        toPrint = ''
        for n in list:
            if n > 0:
                toPrint += '| '
            else:
                toPrint += '  '

        print(toPrint)