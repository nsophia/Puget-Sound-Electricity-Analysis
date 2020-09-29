import eia
import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
import joblib

BASE_DIR = Path(__file__).resolve(strict=True).parent
TODAY = datetime.date.today()

def retrieve_time_series(api, series_ID):
    search = api.data_by_series(series=series_ID)
    df = pd.DataFrame(search)
    return df

def train(ticker="MSFT", df):
    df_forecast = df['Date']
    model = Prophet()
    model.fit(df_forecast)

    # joblib.dump(model, Path(BASE_DIR).joinpath(f"{ticker}.joblib"))


def predict(ticker='MSFT', days=7):
    model_file = Path(BASE_DIR).joinpath(f"{ticker}.joblib")
    if not model_file.exists():
        return False

    model = joblib.load(model_file)

    future = TODAY + datetime.timedelta(days=days)

    dates = pd.date_range(start="2020-01-01", end = future.strftime("%m/%d/%Y"),)
    df = pd.DataFrame({"ds":dates})

    forecast = model.predict(df)

    model.plot(forecast).savefig(f"{ticker}_plot.png")
    model.plot_components(forecast).savefig(f"{ticker}_plot_components.png")

    return forecast.tail(days).to_dict("records")

def main():
    api_key = "5fbe8e00551266c048f84d7d28961828"
    api = eia.API(api_key)
    series_ID = 'EBA.PSEI-ALL.D.HL'
    df = retrieve_time_series(api, series_ID)

    # Cleaning the data
    df.reset_index(level=0, inplace=True)
    df.rename(columns = {'index':'Date', df.columns[1]:'Electricity Demand'}, inplace=True)
    df['Hour'] = df['Date'].str[10:12]
    df['Date'] = pd.to_datetime(df['Date'].str[:-9], format = '%Y %m%d')
    df['Date'] = pd.to_datetime(df['Date']) + df['Hour'].astype('timedelta64[h]')
    # print(df.head(5))

if __name__=="__main__":
    main()

