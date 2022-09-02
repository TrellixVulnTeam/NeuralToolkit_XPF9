import pandas as pd
from . import pedros

def multi(x, y):
    return x*y

def test(path):
    data = pedros.DataStore(path)

    return data.population_summary()
