from urllib.request import urlopen, URLError
import pandas as pd

def empty(value):
    try:
        value = float(value)
    except ValueError:
        pass
    return bool(value)

def f(var):
    if isinstance(var, pd.DataFrame):
        return True
    else:
        return False
		
def process_results(input_result):
    if f(input_result) is True:
        if (input_result.empty) is False:
            print(input_result)
            input_result.to_excel('result.xlsx', index=False, header=True)
    return input_result