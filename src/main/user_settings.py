import json
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from telegram.constants import ParseMode
from ..model.crud import *

# Define the settigns command callback function
async def settings_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.message or update.callback_query.message  # Get the message object
    query_data = update.callback_query.data or "settings"
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id)
    
    keyboard = [[
        InlineKeyboardButton("📈 Indicators", callback_data='settings_indicators'),
        InlineKeyboardButton("📊 Interval", callback_data='settings_interval'),
    ],
    [
        InlineKeyboardButton("⏱ Style", callback_data='settings_style'),
        InlineKeyboardButton("🕙 Timezone", callback_data='settings_timezone'),
    ],
    [
        InlineKeyboardButton("⚖ Scale", callback_data='settings_scale'),
        InlineKeyboardButton("🏞 Format", callback_data='settings_format'),
    ],
    [
        InlineKeyboardButton("🏛 Exchange", callback_data='settings_exchange')
    ],
    [
        InlineKeyboardButton("✖ Close Settings", callback_data='close_settings')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if query_data == "settings_back":
        await message.edit_text(
            f'Current settings:\nIndicators: {user.indicators if user.indicators else ""}\nInterval: {user.interval}\nStyle: {user.style}\nTimezone: {user.timezone}\nScale: {user.scale}\nFormat: {user.pic_format}\nExchange: {user.exchange}', reply_markup=reply_markup
        )
    else:
        await message.reply_text(
            f'Current settings:\nIndicators: {user.indicators if user.indicators else ""}\nInterval: {user.interval}\nStyle: {user.style}\nTimezone: {user.timezone}\nScale: {user.scale}\nFormat: {user.pic_format}\nExchange: {user.exchange}', reply_markup=reply_markup
        )

# Define the Indicators command callback function
async def indicators_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id) 
    indcators = {
        'OBV': "On-balance Volume (OBV)", 
        'ADI': "Accunulation/Distribution line",
        'ADX': "Average Directional Index",
        'AO': "Aroon Oscillator",
        'MACD': "Moving Average Convergence Divergence (MACD)",
        'RSI': "Relative Strength Index (RSI)",
        'SO': "Stochastic Oscillator",
        'BB': "Bollinger Bands",
        'IC': "Ichimoku Cloud",
        'MA': "MA Cross",
        'MAE': "MA with EMA cross",
        'SD': "Standard Deviation",
        'VWAP': "Volune-Weighted Average Price",
        'VPVR': "Volume Profile Visible Range",
        'VO': "Volume Oscillator"
    }
    user_indicators = []
    if user.indicators:
        user_indicators = user.indicators.split(",")
    keyboard = []
    for i in indcators:
        title = f'✅ {indcators[i]}' if i in user_indicators else f'☑ {indcators[i]}'
        call_back = f'settings_indicators_{i}'
        keyboard.append([InlineKeyboardButton(title, callback_data=call_back)])
    
    keyboard.append([InlineKeyboardButton("⬅ Back to Settings", callback_data='settings_back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "Which indicators do you want to use?\n<i>Tip: read more about technical indicators in <a href='https://www.investopedia.com/top-7-technical-analysis-tools-4773275'>this Investopedia article</a></i>", 
        reply_markup=reply_markup, 
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

# Define the interval command callback function
async def interval_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id)
    time = ["1m", "3m", "5m", "15m", "30m", "45m", "1h", "2h", "3h", "4h", "1D", "1W", "1M", "3M", "6M", "1Y"]

    keyboard = []
    for i in range(0, len(time), 2):
        title1 = f'🟢 {time[i]}' if time[i] == user.interval else f'🔘 {time[i]}'
        call_back1 = f'settings_interval_{time[i]}'
        title2 = f'🟢 {time[i+1]}' if time[i+1] == user.interval else f'🔘 {time[i+1]}'
        call_back2 = f'settings_interval_{time[i+1]}'
        keyboard.append([InlineKeyboardButton(title1, callback_data=call_back1), InlineKeyboardButton(title2, callback_data=call_back2)])
    
    keyboard.append([InlineKeyboardButton("⬅ Back to Settings", callback_data='settings_back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "What chart interval do you want to use?", reply_markup=reply_markup
    )

# Define the style command callback function
async def style_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id)
    style = ["bar", "candle", "line", "area", "heikinAshi", "hollowCandle", "renko", "lineBreak"]

    keyboard = []
    for i in range(0, len(style), 2):
        title1 = f'🟢 {style[i]}' if style[i] == user.style else f'🔘 {style[i]}'
        call_back1 = f'settings_style_{style[i]}'
        title2 = f'🟢 {style[i+1]}' if style[i+1] == user.style else f'🔘 {style[i+1]}'
        call_back2 = f'settings_style_{style[i+1]}'
        keyboard.append([InlineKeyboardButton(title1, callback_data=call_back1), InlineKeyboardButton(title2, callback_data=call_back2)])
    
    keyboard.append([InlineKeyboardButton("⬅ Back to Settings", callback_data='settings_back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "What chart style do you want to use?", reply_markup=reply_markup
    )

# Define the timezone command callback function
async def timezone_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id)
    timezone = {
        "America/Bogota" : "(UTC-5) Bogota", 
        "America/Chicago" : "(UTC-6) Chicago", 
        "America/Los_Angeles" : "(UTC-8) LOS Angeles", 
        "America/New_York" : "(UTC-5) New york", 
        "America/Phoenix" : "(UTC-7) Phoenix", 
        "America/Toronto" : "(UTC-5) Toronto", 
        "Asia/Bahrain" : "(UTC+3) Bahrain", 
        "Asia/Bangkok" : "(UTC+7) Bangkok", 
        "Asia/Dubai" : "(UTC+4) Dubai", 
        "Asia/Hong_Kong" : "(UTC+8) Hong Kong", 
        "Asia/Kuwait" : "(UTC+3) Kuwait", 
        "Asia/Qatar" : "(UTC+3) Qatar", 
        "Asia/Shanghai" : "(UTC+8) Shanghai", 
        "Asia/Singapore" : "(UTC+8) Singapore", 
        "Asia/Taipei" : "(UTC+8) Taipei", 
        "Asia/Tehran" : "(UTC+3:30) Tehran", 
        "Asia/Tokyo" : "(UTC+9) Tokyo", 
        "Atlantic/Reykjavik" : "(UTC+0) Reykjavik", 
        "Australia/Perth" : "(UTC+8) Perth", 
        "Australia/Sydney" : "(UTC+11) Sydney", 
        "Europe/Amsterdam" : "(UTC+1) Amsterdam", 
        "Europe/Berlin" : "(UTC+1) Berlin", 
        "Europe/Brussels" : "(UTC+1) Brussels", 
        "Europe/Budapest" : "(UTC+1) Budapest", 
        "Europe/Copenhagen" : "(UTC+1) Copenhagen", 
        "Europe/London" : "(UTC+0) London", 
        "Europe/Madrid" : "(UTC+1) Madrid", 
        "Europe/Moscow" : "(UTC+3) Moscow", 
        "Europe/Oslo" : "(UTC+1) Oslo", 
        "Europe/Paris" : "(UTC+1) Paris", 
        "Europe/Rome" : "(UTC+1) Rome", 
        "Europe/Stockholm" : "(UTC+1) Stockholm", 
        "Europe/Zurich" : "(UTC+1) Zurich", 
        "Pacific/Honolulu" : "(UTC-10) Honolulu", 
        "US/Mountain" : "(UTC-7) Mountain"
    }
    keys = list(timezone.keys())
    keyboard = []
    for i in range(0, len(keys), 2):
        title1 = f'🟢 {timezone[keys[i]]}' if keys[i] == user.timezone else f'🔘 {timezone[keys[i]]}'
        call_back1 = f'settings_timezone_{keys[i]}'
        try:
            title2 = f'🟢 {timezone[keys[i+1]]}' if keys[i+1] == user.timezone else f'🔘 {timezone[keys[i+1]]}'
            call_back2 = f'settings_timezone_{keys[i+1]}'

            keyboard.append([InlineKeyboardButton(title1, callback_data=call_back1), InlineKeyboardButton(title2, callback_data=call_back2)])
        except:
            keyboard.append([InlineKeyboardButton(title1, callback_data=call_back1), InlineKeyboardButton("⬅ Back to Settings", callback_data='settings_back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "What timezone do you want to use?\n<i>Please note: this is only a selection of the <a href='https://www.tradingview.com/charting-library-docs/latest/ui_elements/timezones/'>supported timezones</a></i>", 
        reply_markup=reply_markup, 
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

# Define the scale command callback function
async def scale_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id)
    scale = ["regular", "percent", "indexedTo100", "logarithmic"]

    keyboard = []
    for i in range(0, len(scale), 2):
        title1 = f'🟢 {scale[i]}' if scale[i] == user.scale else f'🔘 {scale[i]}'
        call_back1 = f'settings_scale_{scale[i]}'
        title2 = f'🟢 {scale[i+1]}' if scale[i+1] == user.scale else f'🔘 {scale[i+1]}'
        call_back2 = f'settings_scale_{scale[i+1]}'
        keyboard.append([InlineKeyboardButton(title1, callback_data=call_back1), InlineKeyboardButton(title2, callback_data=call_back2)])
    
    keyboard.append([InlineKeyboardButton("⬅ Back to Settings", callback_data='settings_back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "What chart price scale do you want to use?", reply_markup=reply_markup
    )

# Define the pic_format command callback function
async def pic_format_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id)
    pic_format = ["png", "jpeg"]

    keyboard = []
    for i in range(0, len(pic_format), 2):
        title1 = f'🟢 {pic_format[i]}' if pic_format[i] == user.pic_format else f'🔘 {pic_format[i]}'
        call_back1 = f'settings_format_{pic_format[i]}'
        title2 = f'🟢 {pic_format[i+1]}' if pic_format[i+1] == user.pic_format else f'🔘 {pic_format[i+1]}'
        call_back2 = f'settings_format_{pic_format[i+1]}'
        keyboard.append([InlineKeyboardButton(title1, callback_data=call_back1), InlineKeyboardButton(title2, callback_data=call_back2)])
    
    keyboard.append([InlineKeyboardButton("⬅ Back to Settings", callback_data='settings_back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "What image format do you want to use?", reply_markup=reply_markup
    )

# Define the exchange command callback function
async def exchange_dashboard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    user = get_user_by_id(chat_id)
    if not user:
        user = create_user(chat_id)
    exchane = ["Binance", "Bitfinex", "Bitget", "Bithumb", "Bitstamp", "BYbit", "Coinbase", "Gemhi", "Huobi", "Kraken", "Kucoin", "OKX", "PancakeSwap", "SushiSwap", "Uni v2(ETH)", "Uni v3(ARB)", "Uni v3(ETH)", "Uni v3 (MATIC)"]

    keyboard = []
    for i in range(0, len(exchane), 2):
        title1 = f'🟢 {exchane[i]}' if exchane[i] == user.exchange else f'🔘 {exchane[i]}'
        call_back1 = f'settings_exchange_{exchane[i]}'
        title2 = f'🟢 {exchane[i+1]}' if exchane[i+1] == user.exchange else f'🔘 {exchane[i+1]}'
        call_back2 = f'settings_exchange_{exchane[i+1]}'
        keyboard.append([InlineKeyboardButton(title1, callback_data=call_back1), InlineKeyboardButton(title2, callback_data=call_back2)])
    
    keyboard.append([InlineKeyboardButton("⬅ Back to Settings", callback_data='settings_back')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await message.edit_text(
        "What chart price scale do you want to use?", reply_markup=reply_markup
    )


# Define the settgins update function
async def update_settings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.callback_query.message  # Get the message object
    chat_id = message.chat_id
    query = update.callback_query
    commands = query.data.split("_")
    if commands[1] == 'indicators':
        key = commands[2]
        indcators = ['OBV', 'ADI','ADX','AO','MACD','RSI','SO','BB','IC','MA','MAE','SD','VWAP','VPVR','VO']
        user = get_user_by_id(chat_id)
        if not user:
            user = create_user(chat_id) 
        user_indicators = []
        if user.indicators:
            user_indicators = user.indicators.split(",")
        if key in user_indicators:
            user_indicators.remove(key)
        else:
            user_indicators.append(key)
        new_indicator = []
        for i in indcators:
            new_indicator.append(i) if i in user_indicators else ""
        update_indicators(id=chat_id, indicators=','.join(new_indicator))

        await indicators_dashboard(update, context)
    elif commands[1] == 'interval':
        time = commands[2]
        update_interval(id=chat_id, interval=time)

        await interval_dashboard(update, context)
    elif commands[1] == 'style':
        style = commands[2]
        update_style(id=chat_id, style=style)

        await style_dashboard(update, context)
    elif commands[1] == 'timezone':
        timezone = commands[2::]
        update_timezone(id=chat_id, timezone="_".join(timezone))

        await timezone_dashboard(update, context)
    elif commands[1] == 'scale':
        scale = commands[2]
        update_scale(id=chat_id, scale=scale)

        await scale_dashboard(update, context)
    elif commands[1] == 'format':
        pic_format = commands[2]
        update_pic_format(id=chat_id, pic_format=pic_format)

        await pic_format_dashboard(update, context)
    elif commands[1] == 'exchange':
        exchange = commands[2]
        update_exchange(id=chat_id, exchange=exchange)

        await exchange_dashboard(update, context)
    else:
        pass


async def handling_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    commands = query.data.split("_")
    if len(commands) == 1:
        await settings_dashboard(update, context)
    elif len(commands) == 2:
        if commands[1] == 'back':
            await settings_dashboard(update, context)
        elif commands[1] == 'indicators':
            await indicators_dashboard(update, context)
        elif commands[1] == 'interval':
            await interval_dashboard(update, context)
        elif commands[1] == 'style':
            await style_dashboard(update, context)
        elif commands[1] == 'timezone':
            await timezone_dashboard(update, context)
        elif commands[1] == 'scale':
            await scale_dashboard(update, context)
        elif commands[1] == 'format':
            await pic_format_dashboard(update, context)
        elif commands[1] == 'exchange':
            await exchange_dashboard(update, context)
    elif len(commands) >= 3:
        await update_settings(update, context)


