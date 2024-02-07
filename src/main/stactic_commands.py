# Import required classes from the library
import json
from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from telegram.constants import ParseMode
from ..model.crud import get_user_by_id, create_user

# Define the start command callback function
async def bot_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Define the response message and buttons
    chat_id = update.message.chat_id
    if not get_user_by_id(chat_id):
        create_user(chat_id)
    keyboard = [[
        InlineKeyboardButton("🦾 Add me to your group", url="telegram.me/AIRMCHATBOT?startgroup=true"),
        InlineKeyboardButton("🪄 Commands", callback_data='commands'),
        InlineKeyboardButton("🛠 Settings", callback_data='settings'),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Hello there! Meet Telegram's ultimate Charting Bot.\n\n"
        "📊 Dive into charts for 22,000+ crypto tokens across diverse blockchains!\n\n"
        "🛠 Tailor everything, from timezones to exchanges and even my appearance!\n\n"
        "➕ Join any group or have a private chat with me.\n\n"
        "💰 Unlock advertising opportunities on this powerful platform!", reply_markup=reply_markup
    )


# Command callback for '/commands'
async def bot_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message or update.callback_query.message  # Get the message object
    commands_text = (
        "🗳 Bot Commands\n"
        "/start - Displays help text\n"
        "/commands - Displays all available commands\n"
        "/version - Displays latest version of the bot\n"
        "/help - How to use the bot\n"
        "/disclaimer - How to use the bot\n"
        "/about - Displays information about AIRM\n"
        "/whoami - Displays the data that is sent to the bot\n"
        "/changelog - Displays a concise changelog of all versions\n"
        "/dm - Engages with bot in dms\n"
        "/dx - Displays chart image based on given symbol and (optional) timeframe.\n"
        "/i - Displays extensive token info based on given symbol.\n"
        "/chart - Displays either the $AIRM chart or the chart of the symbol that is set by a group admin.\n"
        "/heatmap - This command gives you a birds-eye view of crypto. Segment by type of coin, market cap, recent performance and more.\n"
        "/settings - Displays all your personal settings and the ability to change them (can be used via DM)\n"
    )
    await message.reply_text(commands_text)

# Define the version command callback function
async def version(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    version_text = "AIRM Chart Bot v1.0.0"
    await update.message.reply_text(version_text)


# Define the help command callback function
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "🦾 How to use the bot\n"
        "Everything resolves around the /dx command. This command is used to generate a chart "
        "for a specific symbol on a specific timeframe.\n"
        "For example: /dx btc 1D will generate a chart for Bitcoin on the 1D timeframe. When "
        "leaving out the timeframe, the default timeframe of 1h will be used. This default value "
        "can be changed via /settings.\n\n"
        
        "📈 Chart command\n"
        "By default, the /chart command renders a fresh $CX chart with a 1hr interval. However, "
        "group admins can use /setchart to set a custom symbol for the /chart command.\n\n"
        
        "🎨 Branded charts\n"
        "Premium groups can add their own logo to the chart image by using the /config command "
        "and uploading a logo. This logo will be used for charts generated by both /chart as well "
        "as the /dx command.\n\n"
        
        "🔎 CA detection\n"
        "By default, contract addresses that are pasted in the chat will be detected and a chart "
        "will be generated for that specific token. For groups, this can be disabled via /config > "
        "commands > disable \"ca\".\n\n"
        
        "🪙 Symbols\n"
        "When requesting a chart, a symbol (e.g. ticker) is required. Besides tickers the AIRM "
        "search algorithm has support for: ticker pair (e.g. btc/usdt) project name.\n\n"
        
        "🕙 Intervals\n"
        "Valid intervals are: 5m, 1h, 6h, 1D.\n\n"
        
        "⚙️ Settings\n"
        "Other settings that can be changed are: style and timezone.\n\n"
        
        "⚠️ Disclaimer\n"
        "Please refer to /disclaimer for our complete disclaimer."
    )
    await update.message.reply_text(help_text)

# Define the disclaimer command callback function
async def disclaimer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    disclaimer_text = (
        "⚠️ Disclaimer ⚠️\n\n"
        "All content provided is for your general information only, procured from third party sources.\n\n"
        "No part of the content that we provide constitutes financial advice, legal advice or any other form "
        "of advice meant for your specific reliance for any purpose.\n\n"
        "Any use or reliance on our content is solely at your own risk and discretion.\n\n"
        "You should conduct your own research, review, analyse and verify our content before relying on them.\n\n"
        "Trading is a highly risky activity that can lead to major losses, please therefore consult your financial "
        "advisor before making any decision.\n\n"
        "We could reference that disclaimer in our help text for example"
    )
    await update.message.reply_text(disclaimer_text)

# Define the about command callback function
async def about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    about_text = (
        "🤖 AIRM Chart Bot for Telegram\n\n"
        "Introducing AIRM: Revolutionizing Cryptocurrency Insights through Instant Charting on Telegram.\n"
        "What sets AIRM apart is its ability to understand your needs and preferences. Simply engage with "
        "the bot in a private chat, and through its AI-driven algorithms, AIRM will promptly deliver accurate "
        "charts tailored to your specifications."
    )
    await update.message.reply_text(about_text)

# Define the whoami command callback function
async def whoami(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_info = update.effective_user.to_json()
    chat_info = update.effective_chat.to_json()

    response = {
        "message_id": update.message.message_id,
        "from": json.loads(user_info),
        "chat": json.loads(chat_info),
        "date": update.message.date.timestamp(),
        "text": update.message.text
    }

    # If there are any entities (like bot commands) in the text, include them.
    if update.message.entities:
        entities = [entity.to_dict() for entity in update.message.entities]
        response["entities"] = entities

    # Convert the entire response to pretty-printed JSON format.
    pretty_response = json.dumps(response, indent=2, ensure_ascii=False)

    # Reply to the user with the details.
    await update.message.reply_text(f"<code>{pretty_response}</code>", parse_mode=ParseMode.HTML)

# Define the changelog command callback function
async def changelog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    changelog_text = (
        "📋 CHANGELOG:\n"
        "📦 v1.0.0: first stable release of the bot 🎉 (20-01-2024)"
    )
    await update.message.reply_text(changelog_text)

# Define the dm command callback function
async def dm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    dm_text = (
        "Thanks for sliding in my DM 🤖. Click here 👉 /start to get acquainted with me."
    )
    await update.message.reply_text(dm_text)
