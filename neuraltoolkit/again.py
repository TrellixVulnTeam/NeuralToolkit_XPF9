import pandas as pd

def createDF(list):
    return pd.DataFrame(list)

def func(x):
    print(f'func {x} = {x}')
    return x