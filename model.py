import eia
import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet


def retrieve_time_series(api, series_ID):
    search = api.data_by_series(series=series_ID)
    df = pd.DataFrame(search)
    return df

def main():
    api_key = "5fbe8e00551266c048f84d7d28961828"
    api = eia.API(api_key)
    series_ID = 'EBA.PSEI-ALL.D.HL'
    df = retrieve_time_series(api, series_ID)
    df.reset_index(level=0, inplace=True)
    df.rename(columns = {'index':'Date', df.columns[1]:'Electricity Demand'}, inplace=True)


    # print(df.columns)
    df['Hour'] = df['Date'].str
    df['Date'] = pd.to_datetime(df['Date'].str[:-9], format = '%Y %m%d')
    # print(df.head)


if __name__=="__main__":
    main()

