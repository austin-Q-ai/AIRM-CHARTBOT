from dexscreener import DexscreenerClient
import os
from datetime import datetime

client = DexscreenerClient()

def get_token_pair_address(chain, address):
    try:
        info = client.get_token_pair(chain, address)
        return info
    except:
        try:
            info = client.get_token_pairs(address)
            return info
        except:
            return None
        
def get_token_chain_symbol(chain):
    return client.search_pairs(chain)

def dx_get_info(default_chain, user_input):
    if len(user_input) > 20: 
        
        info = get_token_pair_address(chain=default_chain, address=user_input)
        if info:
            if type(info) == list:
                return dex_token_address_handle(default_chain=default_chain, info=info)
                
            else:
                return True, info
        else:
            return True, None
    else:
        info = get_token_chain_symbol(chain=user_input)
        if info == []:
            return True, None
        else:
            return dex_token_address_handle(default_chain=default_chain, info=info)

def dex_token_address_handle(default_chain, info):
    dex_platforms = {}
    for i in info:
        if i.chain_id in dex_platforms:
            if i.dex_id in dex_platforms[i.chain_id]:
                dex_platforms[i.chain_id][i.dex_id].append(i)
            else:
                dex_platforms[i.chain_id][i.dex_id] = [i]
        else:
            dex_platforms[i.chain_id] = {i.dex_id:[i]}
    
    if default_chain in dex_platforms:
        return default_chain, dex_platforms[default_chain]
    
    max_price = 0
    chain_id = ""
    for i in dex_platforms:
        av_price = sum(sum(float(m.price_usd) if m.price_usd else 0 for m in dex_platforms[i][y]) for y in dex_platforms[i])
        num = sum(sum(1 if m.price_usd else 0 for m in dex_platforms[i][y]) for y in dex_platforms[i])
        if av_price/num > max_price:
            max_price = av_price/num
            chain_id = i
        
    return chain_id, dex_platforms[chain_id]

def get_picture(chain, address, file_path, indicators, style):
    if indicators == None:
        exec_result = os.system(f'node src\\info\\chart\\index.js {chain} {address} {file_path} nu {style}')
        return exec_result
    else:
        exec_result = os.system(f'node src\\info\\chart\\index.js {chain} {address} {file_path} {indicators} {style}')
        return exec_result

def get_heatmap(datasource, blocksize, file_path):
    exec_result = os.system(f'node src\\info\\chart\\heatmap.js {datasource} {blocksize} {file_path}')
    return exec_result

def log_function(log_type, chain_id, chain_address):
    if log_type == "general":
        log_path = "log.txt"
    else:
        log_path = "chart_log.txt"
    time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    with open(log_path, 'a+', encoding='utf-8') as f:
        f.write(f'{time}--------{log_type}--------{chain_id}--------{chain_address}\n')
        f.close()