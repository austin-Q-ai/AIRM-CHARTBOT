import coinmarketcapapi
import os, json
api_key = "585f8137-651b-4825-b1c9-8ea8f7b84c14"
cmc_client = coinmarketcapapi.CoinMarketCapAPI(api_key)
response = cmc_client.cryptocurrency_listings_latest()
print(len(response.data))
# with open('test.json', 'w') as f:
#     json.dump(response.data, f, indent=2)
# info = cmc_client.cryptocurrency_info(symbol="btc")

# print(info.data)
# with open('test1.json', 'w') as f:
#     json.dump(info.data, f, indent=2)

# test = cmc_client.cryptocurrency_quotes_latest(symbol="btc")
# with open('test2.json', 'w') as f:
#     json.dump(test.data, f, indent=2)

exchange= cmc_client.exchange_map()
print(len(exchange.data))
# with open('exchange.json', 'w') as f:
#     json.dump(exchange.data, f, indent=2)
    
# exchange1= cmc_client.exchange_quotes_latest(**{"slug":"binance"})
# with open('exchange1.json', 'w') as f:
#     json.dump(exchange1.data, f, indent=2)

# exchange2= cmc_client.exchange_marketpairs_latest(**{"slug":"binance"})
# with open('exchange2.json', 'w') as f:
#     json.dump(exchange2.data, f, indent=2)

# cmc_client.cryptocurrency_marketpairs_latest(symbol="btc")
# test = cmc_client.cryptocurrency_marketpairs_latest(symbol="btcadsfasd")
# with open('test4.json', 'w') as f:
#     json.dump(test.data, f, indent=2)

# def cex_info_symbol_market_pair(symbol, exchange):
#     try:
#         info = cmc_client.cryptocurrency_marketpairs_latest(symbol=symbol)
#     except:
#         return None
#     market_pair = []
#     for i in info[0]["market_pairs"]:
#         market_pair.append={
#             "market_id" : i["market_id"],
#             "market_pair" : i["market_pair"],
#             "exchange" : i["exchange"]
#         }
#         if i["market_pair_quote"]["exchange_symbol"] == "USDT" and i["exchange"]["name"]: