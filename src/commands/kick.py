import subprocess
import time

from src.decoration.paint import paint
from src.minecraft.get_minecraft_server_data import GetMinecraftServerData
from src.managers.json_manager import JsonManager
from src.utilities.get_utilities import GetUtilities 
from src.utilities.check_utilities import CheckUtilities

def kick_command(server, username, version, loop, *args):
    try:
        if not CheckUtilities.check_loop_argument(loop):
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidLoopArgument"])}')
            return

        loop = GetUtilities.get_loop_argument(loop)

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "gettingDataFromServer"])}')
        server_data = GetMinecraftServerData.get_data(server, bot=False)

        if server_data is None:
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "invalidArguments", "invalidServer"])}')
            return

        if server_data['platform_type'] != 'Java':
            paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "errorBedrockServer"])}')
            return

        server = server_data['ip_port']
        ip, port = server.split(':')

        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["prefix"])}{GetUtilities.get_translated_text(["commands", "sendcmd", "startingTheAttack"])}')

        if JsonManager.get(["minecraftServerOptions", "proxy"]):
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./src/scripts/kick.js {ip} {port} {username} {version} {len(GetUtilities.get_spaces())} {JsonManager.get(["minecraftServerOptions", "proxyFileForTheBot"])}'
        else:
            command = f'{JsonManager.get(["minecraftServerOptions", "nodeCommand"])} ./src/scripts/kick.js {ip} {port} {username} {version} {len(GetUtilities.get_spaces())}'

        while loop:
            time.sleep(4)
            subprocess.run(command, shell=True)

        if not loop:
            subprocess.run(command, shell=True)

    except KeyboardInterrupt:
        paint(f'\n{GetUtilities.get_spaces()}{GetUtilities.get_translated_text(["commands", "ctrlC"])}')
