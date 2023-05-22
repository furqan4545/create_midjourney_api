import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv

discord_token = "MTEwMjkyNDM2NTM5MTIwNDM2Mw.GME8Be.NIAiIjQGLLwspYcsd1fpqGV1gx0j_LYTmi_nSo"

load_dotenv()
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

intents = discord.Intents.default()
intents.messages = True

async def send_slash_command(channel_id: int, prompt: str):
    header = {
            'authorization': "NzQ3NTc4NzE2NDg5NTE1MDI4.G86rGd.iM6gzEawSuoTBz0pWaN62ssEOqXsT7MqYMwWic"
        }
    payload = {'type': 2, 
        'application_id': "936929561302675456",
        'guild_id': "1102908047459881002",
        'channel_id': "1102908048122593302",
        'session_id': "536798c54fc4dc43b2bac37bfb9fb77b",
        'data': {
            'version': "1077969938624553050",
            'id': "938956540159881230",
            'name': 'imagine',
            'type': 1,
            'options': [{'type': 3, 'name': 'prompt', 'value': prompt}],
            'attachments': []}
            }
    r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)
    while r.status_code != 204:
        r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)
    print('prompt {} successfully sent!'.format(prompt))

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

def main():
    client.run(discord_token)


if __name__ == "__main__":
    main()

