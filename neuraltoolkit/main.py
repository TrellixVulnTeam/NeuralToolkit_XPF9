import pandas

def createDF(list):
    from pandas import DataFrame
    return DataFrame(list)

def func(x):
    print(f'func {x} = {x}')
    return x