# Import required classes from the library
import json, asyncio
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from telegram.constants import ParseMode
from ..model.crud import get_user_by_id
from ..info.dext import dx_get_info, get_picture, get_heatmap, log_function

chains_default_name = {
    'ethereum':'Ethereum',
    'solana':'Solana',
    'bsc':'BSC',
    'arbitrum':'arbitrum',
    'polygon':'Polygon',
    'base':'Base',
    'optimism':'Optimism',
    'avalanche':'Avalanche',
    'zksync':'zkSync',
    'pulsechain':'PulseChain',
    'mantle':'Mantle',
    'sui':'Sui',
    'osmosis':'Osmosis',
    'manta':'Manta',
    'canto':'Canto',
    'aptos':'Aptos',
    'metis':'Metis',
    'scroll':'Scroll',
    'linea':'Linea',
    'oasissapphire':'Oasis Sapphire',
    'fantom':'Fantom',
    'cronos':'Cronos',
    'mode':'Mode',
    'celo':'Celo',
    'sei':'Sei',
    'moonbeam':'Moonbeam',
    'kava':'Kava',
    'zetachain':'ZetaChain',
    'core':'Core',
    'astar':'Astar',
    'polygonzkevm':'Polygon zkEVM',
    'conflux':'Conflux',
    'starknet':'Starknet',
    'near':'NEAR',
    'filecoin':'Filecoin',
    'godwoken':'Godwoken',
    'smartbch':'SmartBCH',
    'flare':'Flare',
    'gnosischain':'Gnosis Chain',
    'evmos':'Evmos',
    'aurora':'Aurora',
    'injective':'Injective',
    'beam':'Beam',
    'arbitrumnova':'Arbitrum Nova',
    'acala':'Acala',
    'zkfair':'ZKFair',
    'opbnb':'opBNB',
    'telos':'Telos',
    'avalanchedfk':'Avalanche DFK',
    'goerli':'Goerli',
    'moonriver':'Moonriver',
    'iotex':'IoTeX',
    'kcc':'KCC',
    'wanchain':'Wanchain',
    'boba':'Boba',
    'velas':'Velas',
    'okc':'OKC',
    'elastos':'Elastos',
    'meter':'Meter',
    'shibarium':'Shibarium',
    'ethereumclassic':'Ethereum Classic',
    'neonevm':'Neon EVM',
    'sxnetwork':'SX Network',
    'fuse':'Fuse',
    'oasisemerald':'Oasis Emerald',
    'harmony':'Harmony',
    'tombchain':'Tomb Chain',
    'milkomedacardano':'Milkomedacardano',
    'stepnetwork':'Step Network',
    'thundercore':'ThunderCore',
    'dogechain':'Dogechain',
    'bitgert':'Bitgert',
    'ethereumpow':'EthereumPoW',
    'loopnetwork':'Loop Network',
    'energi':'Energi',
    'kardiachain':'KardiaChain',
    'combo':'COMBO',
    'redlightchain':'Redlight Chain',
    'syscoin':'Syscoin',
    'ethereumfair':'EthereumFair'
}

candidate_blocksize = {
    'market_cap_calc':'Market Cap',
    'market_cap_diluted_calc': 'FD market cap',
    '24h_vol_cmc' : 'Volume in USD 24h',
    'tvl' : 'Total value locked',
    '24h_vol_to_market_cap': 'Volume 24h / Market cap',
    'market_cap_to_tvl':'Market cap / TVL' 
}

candidate_datasource = {
    'CryptoWithoutBTC' : 'Crypto coins (Excluding Bitcoin)',
    'Crypto' : 'Crypto coins',
    'CryptoWithoutStable' : 'Crypto coins (Excluding Stablecoins)',
    'CryptoDeFi' : 'Coins DeFi'
}

def recommend_pair(chain_info, user_input):
    same_chain_name_token = []
    others_token = []
    for i in chain_info:
        if len(user_input)>15:
            k = i.quote_token.name if i.base_token.address == user_input else i.base_token.name
        else:
            k = i.quote_token.name if user_input in i.base_token.symbol else i.base_token.name
        if i.chain_id[0:3].lower() in k.lower():
            same_chain_name_token.append(i)
        else:
            others_token.append(i)
    
    if same_chain_name_token:
        max_price = 0
        max_item = same_chain_name_token[0]
        for i in same_chain_name_token:
            if i.price_usd and float(i.price_usd) > max_price:
                max_item = i
        return max_item
    else:
        max_price = 0
        max_item = others_token[0]
        for i in others_token:
            if i.price_usd and float(i.price_usd) > max_price:
                max_item = i
        return max_item

def format_number(num):
    suffixes = ['T', 'B', 'M', 'K']
    
    for i, suf in enumerate(suffixes):
        n = 10**(3*(4-i))
        if num >= n:
            return f'{num/n:.1f}{suf}'
    rounded_number = round(num, 3)
    return rounded_number

async def dx_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons 
    message = update.message or update.callback_query.message
    
    text = update.message.text or update.callback_query.data
    if text.strip() == "/dx":
        i_text = (
            "💡 The `/dx` command requires a ticker. For example: `/dx btc`. "
            "Or: type `/help` for assistance."
        )
        # Save the sent message object into a variable `sent_message`
        sent_message = await message.reply_text(i_text, parse_mode=ParseMode.MARKDOWN)
        # Wait for 5 seconds
        await asyncio.sleep(5)
        # Use `sent_message.message_id` to reference the correct message ID
        await sent_message.delete()
        return None

    user_input = text.split("/dx ")[-1]

    chat_id = message.chat_id
    user = get_user_by_id(chat_id)

    sent_message = await message.reply_text(f'Searching info of `{user_input}` on {user.chain} for {user.interval} period', parse_mode=ParseMode.MARKDOWN)

    chain_name, info = dx_get_info(default_chain=user.chain, user_input=user_input)
    if info:
        if chain_name == True:
            await dx_final_response(message=sent_message, chain_info=info, interval=user.interval, indicators=user.indicators, style=user.style)
        else:
            await sent_message.edit_text(f'⚠ There isn\'t info of {user_input} on {user.chain}. So researching on {chain_name}.')
            await dx_select_platform(message=sent_message, chain_info=info, user_input=user_input, interval=user.interval)
    else:
        await sent_message.edit_text(f'❌ The {"symbol" if len(user_input) > 20 else "address"} `{user_input}` you entered is either not available on supported exchanges or could not be matched to a project by our search algorithm. Please contact me directly @fieryfox617',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await sent_message.delete()
        # sent_message.reply_photo()

async def dx_final_response(message: Update.message, chain_info:dict, interval:str, indicators:str, style:str) -> None:
    file_path = "screen.png"
    await message.edit_text(f'Generating chart for `{chain_info.pair_address}` on {chain_info.chain_id} for {interval} period', parse_mode=ParseMode.MARKDOWN)
    picture = get_picture(chain=chain_info.chain_id, address=chain_info.pair_address, file_path=file_path, indicators=indicators, style=style)
    if picture != 0:
        await message.edit_text(f'❌ The {"symbol" if len(chain_info.pair_address) > 20 else "address"} `{chain_info.pair_address}` you entered is either not available on supported exchanges or could not be matched to a project by our search algorithm. Please contact me directly @fieryfox617',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await message.delete()
        return None
    chain = chains_default_name[chain_info.chain_id]
    pair = f'<a href=\'{chain_info.url}\'>{chain_info.base_token.name} / {chain_info.quote_token.name}</a>'
    price = chain_info.price_usd if chain_info.price_usd else None
    create_date = chain_info.pair_created_at
    if create_date:
        created_date = f'🗓️ Created date: {create_date.strftime(format='%Y-%m-%d')}\n'
    else:
        created_date = None
    if interval == '5m':
        price_chain = chain_info.price_change.m5
        pair_count = chain_info.transactions.m5
        volume = chain_info.volume.m5
    elif interval == '1h':
        price_chain = chain_info.price_change.h1
        pair_count = chain_info.transactions.h1
        volume = chain_info.volume.h1
    elif interval == '6h':
        price_chain = chain_info.price_change.h6
        pair_count = chain_info.transactions.h6
        volume = chain_info.volume.h6
    elif interval == '1D':
        price_chain = chain_info.price_change.h24
        pair_count = chain_info.transactions.h24
        volume = chain_info.volume.h24
    liquidity = chain_info.liquidity
    keyboard = []
    times = ['5m','1h','6h','1D']
    for i in times:
        if i == interval:
            keyboard.append(InlineKeyboardButton(text="🔄", callback_data=f'dx_{chain_info.chain_id}_{chain_info.pair_address}_{i}'))
        else:
            keyboard.append(InlineKeyboardButton(text=i, callback_data=f'dx_{chain_info.chain_id}_{chain_info.pair_address}_{i}'))
    keyboard.append(InlineKeyboardButton(text="ℹ", callback_data=f'i_{chain_info.chain_id}_{chain_info.pair_address}_{interval}'))
    reply_markup = InlineKeyboardMarkup([keyboard])
    await message.delete()
    with open(file_path, 'rb') as f:
        await message.reply_photo(
            photo = f,
            caption=f'📌 Chain: {chain} ({interval})\n\n🏦 DEX Platform: {chain_info.dex_id}\n\n💸 Pair: {pair}\n\n💰 Price USD: {chain_info.price_usd if chain_info.price_usd else '-'} {f'({price_chain}%)' if chain_info.price_usd else ''}\n🌊 Volume: ${volume}\n💦 Liquidity: Total: ${format_number(liquidity.usd)}\n',
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
        log_function("chart", chain_info.chain_id, chain_info.pair_address)

async def dx_select_platform(message: Update.message, chain_info:dict, user_input:str, interval) ->None:
    platforms = {}
    for i in chain_info:
        if len(i) < 25:
            token = recommend_pair(chain_info=chain_info[i], user_input=user_input)
            platforms[i] = token
    keyboard = []
    keys = list(platforms.keys())
    back_button_flag=True
    if len(keys) == 1:
        await dx_final_response(message=message, chain_info=platforms[keys[0]], interval=interval)
    else:
        for i in range(0, len(keys), 3):
            rows = []
            for y in range(0,3):
                try:
                    title = f'{platforms[keys[i+y]].dex_id}'
                    call_back = f'dx_{platforms[keys[i+y]].chain_id}_{platforms[keys[i+y]].pair_address}_{interval}'
                    rows.append(InlineKeyboardButton(title, callback_data=call_back))
                except:
                    rows.append(InlineKeyboardButton("✖ Close", callback_data='dx_close'))
                    back_button_flag=False
                    break
            keyboard.append(rows)
        if back_button_flag:
            keyboard.append([InlineKeyboardButton("✖ Close", callback_data='dx_close')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.edit_text(
            "Which DEX platform would you like to use?", reply_markup=reply_markup
        )

async def dx_callback_handle(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    message = update.callback_query.message
    text = update.callback_query.data
    chain_id = text.split("_")[1]
    if chain_id == "close":
        await message.delete()
    else:
        pair_address = text.split("_")[2]
        interval = text.split("_")[3]
        chat_id = message.chat_id
        user = get_user_by_id(chat_id)
        await message.delete()
        sent_message = await message.reply_text(f'Searching info of `{pair_address}` on {chain_id} for {interval} period', parse_mode=ParseMode.MARKDOWN)
        chain_name, info = dx_get_info(default_chain=chain_id, user_input=pair_address)
        if chain_name == True:
            await dx_final_response(message=sent_message, chain_info=info, interval=interval, indicators=user.indicators, style=user.style)
        else:
            await dx_select_platform(message=sent_message, chain_info=info, user_input=pair_address, interval=interval)


async def i_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons 
    message = update.message or update.callback_query.message
    
    text = update.message.text or update.callback_query.data
    if text.strip() == "/i":
        i_text = (
            "💡 The `/i` command requires a ticker. For example: `/i btc`. "
            "Or: type `/help` for assistance."
        )
        # Save the sent message object into a variable `sent_message`
        sent_message = await message.reply_text(i_text, parse_mode=ParseMode.MARKDOWN)
        # Wait for 5 seconds
        await asyncio.sleep(5)
        # Use `sent_message.message_id` to reference the correct message ID
        await sent_message.delete()
        return None

    user_input = text.split("/i ")[-1]

    chat_id = message.chat_id
    user = get_user_by_id(chat_id)

    sent_message = await message.reply_text(f'Searching info of `{user_input}` on {user.chain} for {user.interval} period', parse_mode=ParseMode.MARKDOWN)

    chain_name, info = dx_get_info(default_chain=user.chain, user_input=user_input)
    if info:
        if chain_name == True:
            await i_final_response(message=sent_message, chain_info=info, interval=user.interval)
        else:
            await sent_message.edit_text(f'⚠ There isn\'t info of {user_input} on {user.chain}. So researching on {chain_name}.')
            await i_select_platform(message=sent_message, chain_info=info, user_input=user_input, interval=user.interval)
    else:
        await sent_message.edit_text(f'❌ The {"symbol" if len(user_input) > 20 else "address"} `{user_input}` you entered is either not available on supported exchanges or could not be matched to a project by our search algorithm. Please contact me directly @fieryfox617',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await sent_message.delete()

async def i_final_response(message: Update.message, chain_info:dict, interval:str) -> None:
    chain = chains_default_name[chain_info.chain_id]
    pair = f'<a href=\'{chain_info.url}\'>{chain_info.base_token.name} / {chain_info.quote_token.name}</a>'
    price = chain_info.price_usd if chain_info.price_usd else None
    create_date = chain_info.pair_created_at
    if create_date:
        created_date = f'🗓️ Created date: {create_date.strftime(format='%Y-%m-%d')}\n'
    else:
        created_date = None
    if interval == '5m':
        price_chain = chain_info.price_change.m5
        pair_count = chain_info.transactions.m5
        volume = chain_info.volume.m5
    elif interval == '1h':
        price_chain = chain_info.price_change.h1
        pair_count = chain_info.transactions.h1
        volume = chain_info.volume.h1
    elif interval == '6h':
        price_chain = chain_info.price_change.h6
        pair_count = chain_info.transactions.h6
        volume = chain_info.volume.h6
    elif interval == '1D':
        price_chain = chain_info.price_change.h24
        pair_count = chain_info.transactions.h24
        volume = chain_info.volume.h24
    liquidity = chain_info.liquidity
    keyboard = []
    times = ['5m','1h','6h','1D']
    for i in times:
        if i == interval:
            keyboard.append(InlineKeyboardButton(text="🔄", callback_data=f'i_{chain_info.chain_id}_{chain_info.pair_address}_{i}'))
        else:
            keyboard.append(InlineKeyboardButton(text=i, callback_data=f'i_{chain_info.chain_id}_{chain_info.pair_address}_{i}'))
    keyboard.append(InlineKeyboardButton(text="📈", callback_data=f'chart_{chain_info.chain_id}_{chain_info.pair_address}_{interval}'))
    reply_markup = InlineKeyboardMarkup([keyboard])

    await message.edit_text(
        text=f'📌 Chain: {chain} ({interval})\n\n🏦 DEX Platform: {chain_info.dex_id}\n\n💸 Pair: {pair} \n{created_date if created_date else ""}\n💰 Price USD: {chain_info.price_usd if chain_info.price_usd else '-'} {f'({price_chain}%)' if chain_info.price_usd else ''}\n🛒 PairtransactionCount: Buy: {format_number(pair_count.buys)} / Sell: {format_number(pair_count.sells)}\n\n🌊 Volume: ${volume}\n\n💦 Liquidity: Total: ${format_number(liquidity.usd)}\n     Base: {format_number(liquidity.base)}({chain_info.base_token.symbol}) / Quote: {format_number(liquidity.quote)}({chain_info.quote_token.symbol})',
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )
    log_function("general", chain_info.chain_id, chain_info.pair_address)

async def i_select_platform(message: Update.message, chain_info:dict, user_input:str, interval) ->None:
    platforms = {}
    for i in chain_info:
        if len(i) < 25:
            token = recommend_pair(chain_info=chain_info[i], user_input=user_input)
            platforms[i] = token
    keyboard = []
    keys = list(platforms.keys())
    back_button_flag=True
    if len(keys) == 1:
        await i_final_response(message=message, chain_info=platforms[keys[0]], interval=interval)
    else:
        for i in range(0, len(keys), 3):
            rows = []
            for y in range(0,3):
                try:
                    title = f'{platforms[keys[i+y]].dex_id}'
                    call_back = f'i_{platforms[keys[i+y]].chain_id}_{platforms[keys[i+y]].pair_address}_{interval}'
                    rows.append(InlineKeyboardButton(title, callback_data=call_back))
                except:
                    rows.append(InlineKeyboardButton("✖ Close", callback_data='i_close'))
                    back_button_flag=False
                    break
            keyboard.append(rows)
        if back_button_flag:
            keyboard.append([InlineKeyboardButton("✖ Close", callback_data='i_close')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.edit_text(
            "Which DEX platform would you like to use?", reply_markup=reply_markup
        )

async def i_callback_handle(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    message = update.callback_query.message
    text = update.callback_query.data
    chain_id = text.split("_")[1]
    if chain_id == "close":
        await message.delete()
    else:
        pair_address = text.split("_")[2]
        interval = text.split("_")[3]
        await message.delete()
        sent_message = await message.reply_text(f'Searching info of `{pair_address}` on {chain_id} for {interval} period', parse_mode=ParseMode.MARKDOWN)
        
        chain_name, info = dx_get_info(default_chain=chain_id, user_input=pair_address)
        if chain_name == True:
            await i_final_response(message=sent_message, chain_info=info, interval=interval)
        else:
            await i_select_platform(message=sent_message, chain_info=info, user_input=pair_address, interval=interval)


async def chart_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons 
    message = update.message or update.callback_query.message
    
    text = update.message.text or update.callback_query.data
    if text.strip() == "/chart":
        i_text = (
            "💡 The `/chart` command requires a ticker. For example: `/chart btc`. "
            "Or: type `/help` for assistance."
        )
        # Save the sent message object into a variable `sent_message`
        sent_message = await message.reply_text(i_text, parse_mode=ParseMode.MARKDOWN)
        # Wait for 5 seconds
        await asyncio.sleep(5)
        # Use `sent_message.message_id` to reference the correct message ID
        await sent_message.delete()
        return None

    user_input = text.split("/chart ")[-1]

    chat_id = message.chat_id
    user = get_user_by_id(chat_id)

    sent_message = await message.reply_text(f'Generating chart for `{user_input}` on {user.chain} for {user.interval} period', parse_mode=ParseMode.MARKDOWN)

    chain_name, info = dx_get_info(default_chain=user.chain, user_input=user_input)
    if info:
        if chain_name == True:
            await chart_final_response(message=sent_message, chain_info=info, interval=user.interval, indicators=user.indicators, style=user.style)
        else:
            await sent_message.edit_text(f'⚠ There isn\'t info of {user_input} on {user.chain}. So researching on {chain_name}.')
            await chart_select_platform(message=sent_message, chain_info=info, user_input=user_input, interval=user.interval)
    else:
        await sent_message.edit_text(f'❌ The {"symbol" if len(user_input) > 20 else "address"} `{user_input}` you entered is either not available on supported exchanges or could not be matched to a project by our search algorithm. Please contact me directly @fieryfox617',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await sent_message.delete()
        # sent_message.reply_photo()

async def chart_final_response(message: Update.message, chain_info:dict, interval:str, indicators:str, style:str) -> None:
    file_path = "screen.png"
    picture = get_picture(chain=chain_info.chain_id, address=chain_info.pair_address, file_path=file_path, indicators=indicators, style=style)
    if picture != 0:
        await message.edit_text(f'❌ The {"symbol" if len(chain_info.pair_address) > 20 else "address"} `{chain_info.pair_address}` you entered is either not available on supported exchanges or could not be matched to a project by our search algorithm. Please contact me directly @fieryfox617',parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(5)
        await message.delete()
        return None
    
    keyboard = []
    keyboard.append(InlineKeyboardButton(text="🔄", callback_data=f'chart_{chain_info.chain_id}_{chain_info.pair_address}_{interval}'))
    keyboard.append(InlineKeyboardButton(text="ℹ", callback_data=f'i_{chain_info.chain_id}_{chain_info.pair_address}_{interval}'))
    reply_markup = InlineKeyboardMarkup([keyboard])
    await message.delete()
    with open(file_path, 'rb') as f:
        await message.reply_photo(
            photo = f,
            reply_markup=reply_markup
        )
        log_function("chart", chain_info.chain_id, chain_info.pair_address)

async def chart_select_platform(message: Update.message, chain_info:dict, user_input:str, interval) ->None:
    platforms = {}
    for i in chain_info:
        if len(i) < 25:
            token = recommend_pair(chain_info=chain_info[i], user_input=user_input)
            platforms[i] = token
    keyboard = []
    keys = list(platforms.keys())
    back_button_flag=True
    if len(keys) == 1:
        await chart_final_response(message=message, chain_info=platforms[keys[0]], interval=interval)
    else:
        for i in range(0, len(keys), 3):
            rows = []
            for y in range(0,3):
                try:
                    title = f'{platforms[keys[i+y]].dex_id}'
                    call_back = f'chart_{platforms[keys[i+y]].chain_id}_{platforms[keys[i+y]].pair_address}_{interval}'
                    rows.append(InlineKeyboardButton(title, callback_data=call_back))
                except:
                    rows.append(InlineKeyboardButton("✖ Close", callback_data='chart_close'))
                    back_button_flag=False
                    break
            keyboard.append(rows)
        if back_button_flag:
            keyboard.append([InlineKeyboardButton("✖ Close", callback_data='chart_close')])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await message.edit_text(
            "Which DEX platform would you like to use?", reply_markup=reply_markup
        )

async def chart_callback_handle(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    message = update.callback_query.message
    text = update.callback_query.data
    chain_id = text.split("_")[1]
    if chain_id == "close":
        await message.delete()
    else:
        pair_address = text.split("_")[2]
        interval = text.split("_")[3]
        chat_id = message.chat_id
        user = get_user_by_id(chat_id)
        await message.delete()
        sent_message = await message.reply_text(f'Generating chart for token-pair(`{pair_address}`) on {chain_id} for {interval} period', parse_mode=ParseMode.MARKDOWN)
        chain_name, info = dx_get_info(default_chain=chain_id, user_input=pair_address)
        if chain_name == True:
            await chart_final_response(message=sent_message, chain_info=info, interval=interval, indicators=user.indicators, style=user.style)
        else:
            await chart_select_platform(message=sent_message, chain_info=info, user_input=pair_address, interval=interval)


async def heatmap_handle(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    # Define the response message and buttons
    message = update.message or update.callback_query.message 
    keyboard = []
    for i in candidate_datasource:
        keyboard.append([InlineKeyboardButton(candidate_datasource[i], callback_data=f'heatmap_{i}')])
    keyboard.append([InlineKeyboardButton("✖ Close", callback_data='heatmap_close')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text(
            'Which datasource do you like to use?', reply_markup=reply_markup
        )

async def heatmap_blocksize_handle(message: Update.message, datasource:str) -> None:
    
    # Define the response message and buttons
    keyboard = []
    for i in candidate_blocksize:
        keyboard.append([InlineKeyboardButton(candidate_blocksize[i], callback_data=f'heatmap_{datasource}_{i}')])
        
    keyboard.append([InlineKeyboardButton("✖ Close", callback_data='heatmap_close')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.edit_text(
            'Which blocksize do you like to use?', reply_markup=reply_markup
        )
    
async def heatmap_callback_handle(update: Update, context: ContextTypes.DEFAULT_TYPE)->None:
    message = update.callback_query.message
    text = update.callback_query.data
    datasource = text.split("_")[1]
    if datasource == "close":
        await message.delete()
    else:
        if len(text.split("_")) == 2:
            await heatmap_blocksize_handle(message=message, datasource=datasource)
        else:
            blocksize = "_".join(text.split("_")[2::])
            await message.edit_text(f'Generating heatmap by {candidate_blocksize[blocksize]} on {candidate_datasource[datasource]}')
            heatmap_path = "heatmap.png"
            heatmap = get_heatmap(datasource=datasource, blocksize=blocksize, file_path=heatmap_path)
            if heatmap != 0:
                await message.edit_text(f'❌ Failed in heatmap by {candidate_blocksize[blocksize]} on {candidate_datasource[datasource]}. Please contact me directly @fieryfox617')
                await asyncio.sleep(5)
                await message.delete()
                return None
            
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="🔄", callback_data=f'heatmap_{datasource}_{blocksize}')]])
            await message.delete()
            with open(heatmap_path, 'rb') as f:
                await message.reply_photo(
                    photo=f,
                    caption=f'🕋 Datasource: {candidate_datasource[datasource]}\n📐 Blocksize: {candidate_blocksize[blocksize]}',
                    reply_markup=reply_markup
                )
                log_function("heatmap", candidate_datasource[datasource], candidate_blocksize[blocksize])
