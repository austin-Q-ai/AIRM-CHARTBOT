# Import required classes from the library
import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from dotenv import load_dotenv

from src.main.stactic_commands import *
from src.main.handle_callback import *
from src.main.user_settings import *

load_dotenv(dotenv_path='.env')

# Use your own bot token here
TOKEN = os.getenv('TG_TOKEN')

# Main function update
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    # Existing start handler
    start_handler = CommandHandler('start', bot_start)
    application.add_handler(start_handler)

    # Existing commands handler (triggered by typing "/commands")
    commands_handler = CommandHandler('commands', bot_commands)
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

    # Add the CallbackQueryHandler with a different variable name to avoid conflict
    callback_query_handler_obj = CallbackQueryHandler(callback_query_handler)
    application.add_handler(callback_query_handler_obj)
    
    application.run_polling()

if __name__ == '__main__':
    main()
