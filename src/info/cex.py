import coinmarketcapapi
import os, json, datetime
import pandas as pd
import mplfinance as mpf

api_key = "585f8137-651b-4825-b1c9-8ea8f7b84c14"
cmc_client = coinmarketcapapi.CoinMarketCapAPI(api_key)

def cex_info_symbol_market_pair(symbol):
    try:
        info = cmc_client.cryptocurrency_marketpairs_latest(symbol=symbol).data
    except:
        return None
    market_pair = {}
    for i in info[0]["market_pairs"]:
        if i["market_pair_quote"]["exchange_symbol"] in market_pair:
            market_pair[i["market_pair_quote"]["exchange_symbol"]].append(i)
        else:
            market_pair[i["market_pair_quote"]["exchange_symbol"]] = [i]

    if "USD" in market_pair:
        return market_pair["USD"]
    elif "USDT" in market_pair:
        return market_pair["USDT"]
    else:
        max_value = 0
        max_pair = ""
        for i in market_pair:
            average_price = sum([pair["quote"]["USD"]["price"] for pair in market_pair[i]]) / len(market_pair[i])
            if average_price > max_value:
                max_pair = i
        return market_pair[max_pair]

def cex_exact_info(symbol, market_pair):
    try:
        info = cmc_client.cryptocurrency_marketpairs_latest(symbol=symbol).data
    except:
        return None

    for i in info[0]["market_pairs"]:
        if i["market_id"] == market_pair:
            return i
    return None

def display_trendline(long_data, file_path, style):
    mc = mpf.make_marketcolors(up='#089981',down='#F23645',
                           edge={'up':'#089981','down':'#F23645'},
                           wick={'up':'#089981','down':'#F23645'},
                           volume = '#15547D',
                           ohlc='black')
    s  = mpf.make_mpf_style(marketcolors=mc, base_mpf_style='nightclouds')
    if style in ["line", 'lineWithMarkers', 'area', 'hlcarea', 'baseline']:
        fig, axes = mpf.plot(long_data, type='line', style=s, ylabel='Price', volume=True,
                         figsize=(20, 10),
                         returnfig=True)
    elif style in ["candle", 'hollowCandle', 'hilo', 'ha']:
        fig, axes = mpf.plot(long_data, type='candle', style=s, ylabel='Price', volume=True,
                            figsize=(20, 10),
                            returnfig=True)
    elif style == "stepline":
        fig, axes = mpf.plot(long_data, type='renko', style=s, ylabel='Price', volume=True,
                            figsize=(20, 10),
                            returnfig=True)
    else:
        mc = mpf.make_marketcolors(up='#089981',down='#F23645',
                           edge={'up':'#089981','down':'#F23645'},
                           wick={'up':'#089981','down':'#F23645'},
                           volume = '#15547D',
                           ohlc='i')
        s  = mpf.make_mpf_style(marketcolors=mc, base_mpf_style='nightclouds')
        fig, axes = mpf.plot(long_data, type='ohlc', style=s, ylabel='Price', volume=True,
                            figsize=(20, 10),
                            returnfig=True)
    fig.savefig(file_path, bbox_inches='tight')

def make_finance_chart(raw_data):
    columns = ["date", "open", "high", "low", "close", "volume"]
    date_data = []
    open_data = []
    high_data = []
    low_data = []
    close_data = []
    volume = []
    
    for i in raw_data:
        date_data.append(i["time_close"])
        open_data.append(i["quote"]["USD"]["open"])
        high_data.append(i["quote"]["USD"]["high"])
        low_data.append(i["quote"]["USD"]["low"])
        close_data.append(i["quote"]["USD"]["close"])
        volume.append(i["quote"]["USD"]["volume"])

    df = pd.DataFrame(list(zip(date_data, open_data, high_data, low_data, close_data, volume)), columns=columns)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    # print(df.head())
    return df

def cex_historical_info(symbol, time_start, time_end, interval, period, file_path, style):
    parameters = {
        "symbol" : symbol,
        "time_start" : time_start,
        "time_end" : time_end,
        "interval" : interval,
        "time_period": period
    }
    # test = cmc_client.cryptocurrency_quotes_historical(**parameters)
    test= cmc_client.cryptocurrency_ohlcv_historical(**parameters)
    data = make_finance_chart(raw_data=test.data[symbol][0]["quotes"])

    try:
        display_trendline(long_data=data, file_path=file_path, style=style)
        return True
    except:
        return False

def get_detailed_info(symbol):
    try:
        test = cmc_client.cryptocurrency_quotes_latest(symbol=symbol)
        return test.data[symbol][0]
    except:
        return None