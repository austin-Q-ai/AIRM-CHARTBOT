# Import required classes from the library
from telegram.ext import ContextTypes
from telegram import Update
from .stactic_commands import bot_commands

async def callback_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    # Make sure to answer the callback query to give feedback to the user
    await query.answer()

    # Check if the callback_data matches 'commands'
    if query.data == 'commands':
        await bot_commands(update, context)

    # Below is a placeholder for how you could handle the 'close_heatmap' button press
    elif query.data == 'close_heatmap':
        await query.message.delete()
    # If the "Close settings" button is pressed, delete the message
    elif query.data == 'close_settings':
        await query.message.delete()

    # elif query.data == 'settings':
    #     # Call settings function directly when "Settings" button is pressed
    #     await settings(update, context)
