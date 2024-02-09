# Import required classes from the library
import os, requests
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv

from src.main.stactic_commands import *
from src.main.handle_callback import *
from src.main.user_settings import *
from src.main.main_commands import *

load_dotenv(dotenv_path='.env')

# Use your own bot token here
TOKEN = os.getenv('TG_TOKEN')
API_URL = f"https://api.telegram.org/bot{TOKEN}/setMyCommands"

commands = [
    {"command": "start", "description": "Displays help text"},
    {"command": "features", "description": "Displays all available bot features"},
    {"command": "version", "description": "Displays latest version of the bot"},
    {"command": "help", "description": "How to use the bot"},
    {"command": "disclaimer", "description": "How to use the bot"},
    {"command": "about", "description": "Displays information about AIRM"},
    {"command": "whoami", "description": "Displays the data that is sent to the bot"},
    {"command": "changelog", "description": "Displays a concise changelog of all versions"},
    {"command": "dm", "description": "Engages with bot in dms"},
    {"command": "dx", "description": "Displays chart image based on given symbol and (optional) timeframe."},
    {"command": "i", "description": "Displays extensive token info based on given symbol."},
    {"command": "chart", "description": "Displays either the $AIRM chart or the chart of the symbol that is set by a group admin."},
    {"command": "heatmap", "description": "This command gives you a birds-eye view of crypto. Segment by type of coin, market cap, recent performance and more."},
    {"command": "settings", "description": "Displays all your personal settings and the ability to change them (can be used via DM)"},
    {"command": "stats", "description": "Displays the bot stats"}
]

response = requests.post(API_URL, json={"commands": commands})

# Main function update
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    # Existing start handler
    start_handler = CommandHandler('start', bot_start)
    application.add_handler(start_handler)

    # Existing commands handler (triggered by typing "/features")
    commands_handler = CommandHandler('features', bot_commands)
    application.add_handler(commands_handler)

    # Version command handler (adds the functionality for '/version')
    version_handler = CommandHandler('version', version)
    application.add_handler(version_handler)

    # Add command handler (adds the functionality for '/help')
    help_handler = CommandHandler('help', help)
    application.add_handler(help_handler)

    # Add command handler (adds the functionality for '/disclaimer')
    disclaimer_handler = CommandHandler('disclaimer', disclaimer)
    application.add_handler(disclaimer_handler)

    # Add command handler (adds the functionality for '/about')
    about_handler = CommandHandler('about', about)
    application.add_handler(about_handler)

    # Add command handler (adds the functionality for '/whoami')
    whoami_handler = CommandHandler('whoami', whoami)
    application.add_handler(whoami_handler)
    
    # Add command handler (adds the functionality for '/changelog')
    changelog_handler = CommandHandler('changelog', changelog)
    application.add_handler(changelog_handler)

    # Add command handler (adds the functionality for '/dm')
    dm_handler = CommandHandler('dm', dm)
    application.add_handler(dm_handler)

    # Add the /stats command handler to the application
    stats_handler = CommandHandler('stats', stats)
    application.add_handler(stats_handler)

    # Add the /stats command handler to the application
    settings_handler = CommandHandler('settings', settings_dashboard)
    application.add_handler(settings_handler)

    dx_handler = CommandHandler('dx', dx_handle)
    application.add_handler(dx_handler)

    i_handler = CommandHandler('i', i_handle)
    application.add_handler(i_handler)

    chart_handler = CommandHandler('chart', chart_handle)
    application.add_handler(chart_handler)

    cx_handler = CommandHandler('cx', cx_handle)
    application.add_handler(cx_handler)

    heatmap_handler = CommandHandler('heatmap', heatmap_handle)
    application.add_handler(heatmap_handler)

    # Add the CallbackQueryHandler with a different variable name to avoid conflict
    callback_query_handler_obj = CallbackQueryHandler(callback_query_handler)
    application.add_handler(callback_query_handler_obj)
    
    application.run_polling()

if __name__ == '__main__':
    main()
