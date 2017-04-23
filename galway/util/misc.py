def sign(n, e=.00001):
    if n < e and n > -e:
        return '0'
    elif n >= 0:
        return '+'
    else:
        return '-'
