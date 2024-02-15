# ***AIRM*** 
AIRM is a powerful cryptocurrency bot that provides real-time chart analysis for over 25,000 tokens across multiple blockchains. Participate in both group discussions and private conversations, and this bot fully customises your experience with adjustable settings and an easy-to-use interface. You can also use the platform's advertising opportunities to increase your brand's visibility, complemented by advanced analytics tools for strategic decision-making in the crypto market.

## How to run 

1. Install python libraries
    ```
    pip install -r requirements.txt
    ```

2. Set .env file
    ```
    TG_TOKEN='6713649929:AAGr4XhH**************7w78B-QdlP00'
    COINMARKET_KEY='585f8137-***************************'
    ```

3. Run the Bot

    ```
    python app.py
    ```

## How to use
### Main commands
Everything revolves around the `/dx`, `/cx` command. This command is used to generate a chart and get information for a specific symbol in a specific timeframe. The `/dx` stands for decentralised exchanges and the `/cx` stands for centralised exchanges.
For example: `/dx btc` 1D will generate a chart for bitcoin on the 1D timeframe, on decentralised exchanges. If you omit the timeframe, the default 1h timeframe will be used. This default can be changed via `/settings`.

### Chart command
By default the `/chart` command renders a  given cryptocurrency chart with a 1 hour interval. However, group admins can use `/settings` to set a custom interval, style and indicators for the `/chart` command.

### Information command
By default the `/i` command render detailed information of cryptocurrency with a 1 hour interval. However, group admins can use `/settings` to set a custom interval for the `/i` command.

### Settings
Use `/settings` to change custom settings - display, style, interval, time zone and default-chain.

### Other commands

**/start** - Displays help text<br>
**/features** - Displays all available features<br>
**/version** - Displays latest version of the bot<br>
**/help** - How to use the bot<br>
**/disclaimer** - How to use the bot<br>
**/about** - Displays information about AIRM<br>
**/whoami** - Displays the data that is sent to the bot<br>
**/changelog** - Displays a concise changelog of all versions<br>
**/dm** - Engages with bot in dms<br>
**/stats** - Displays the bot stats<br>