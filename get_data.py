import requests
import discord
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image
import os
import json


################################### Airtable API ###################################

baseid = "appA2DrcnxYfmKkwM"
tableid = "tbleJ5GOAUnWfvcPy"
recordid = "recv2D0SIEnhRvTcf"

# api-endpoint
URL = f"https://api.airtable.com/v0/{baseid}/{tableid}/{recordid}"
  
# location given here
location = "delhi technological university"
  
# defining a params dict for the parameters to be sent to the API
PARAMS = {'address' : location}
  
head = {"Authorization" : "Bearer keypYvClRSuGyqnU8"}
# sending get request and saving the response as response object
r = requests.get(url = URL, headers = head)
  
# extracting data in json format
data = r.json()
# filter1 = data["fields"]["Scene 1 Storyboard (from 🎞 Showcases)"][1]["thumbnails"]["large"]["url"]


no_of_images = len(data["fields"]["Scene 1 Storyboard (from 🎞 Showcases)"])
scene1_description = data["fields"]["Scene 1 Description"]

images = []

for i in range(no_of_images):
    filter1 = data["fields"]["Scene 1 Storyboard (from 🎞 Showcases)"][i]["thumbnails"]["large"]["url"]
    images.append(filter1)
    # print(filter1)


print("My data: ", scene1_description)

total_data = f"{', '.join(images)}, {scene1_description}"
print(total_data)
  
#######################################################################################

############################### midjourney code ###############################
discord_token = "MTEwMjkyNDM2NTM5MTIwNDM2Mw.GME8Be.NIAiIjQGLLwspYcsd1fpqGV1gx0j_LYTmi_nSo"

load_dotenv()
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

intents = discord.Intents.default()
intents.messages = True

async def send_prompt_to_channel(channel_id: int, prompt: str):
    target_channel = client.get_channel(channel_id)
    if target_channel is not None:
        await target_channel.send(f'/imagine {prompt}')
    else:
        print(f'Could not find a channel with the ID {channel_id}')

async def send_slash_command(channel_id: int, prompt: str):
    
    header = {
            'authorization': "NzQ3NTc4NzE2NDg5NTE1MDI4.G86rGd.iM6gzEawSuoTBz0pWaN62ssEOqXsT7MqYMwWic"
        }

    # payload= {
    #     "type":2,
    #     "application_id":"936929561302675456","guild_id":"1102908047459881002",
    #     "channel_id":"1102908048122593302","session_id":"7948ec26f321fd4983428e01b131b787",
    #     "data":{"version":"1077969938624553050","id":"938956540159881230","name":"imagine","type":1,
    #     "options":[{"type":3,"name":"prompt","value":prompt}],
    #     "application_command":{"id":"938956540159881230","application_id":"936929561302675456",
    #     "version":"1077969938624553050","default_member_permissions": None,
    #     "type":1,"nsfw":False,"name":"imagine","description":"Create images with Midjourney","dm_permission":True,
    #     "contexts":None,"options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True}]},"attachments":[]},"nonce":"1102981542960955392"}
        
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

    print('prompt [{}] successfully sent!'.format(prompt))
    print(r.status_code)



directory = os.getcwd()
print(directory)

def split_image(image_file):
    with Image.open(image_file) as im:
        # Get the width and height of the original image
        width, height = im.size
        # Calculate the middle points along the horizontal and vertical axes
        mid_x = width // 2
        mid_y = height // 2
        # Split the image into four equal parts
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))

        return top_left, top_right, bottom_left, bottom_right

async def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:

        # Define the input and output folder paths
        input_folder = "input"
        output_folder = "output"

        # Check if the output folder exists, and create it if necessary
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # Check if the input folder exists, and create it if necessary
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)

        with open(f"{directory}/{input_folder}/{filename}", "wb") as f:
            f.write(response.content)
        print(f"Image downloaded: {filename}")

        input_file = os.path.join(input_folder, filename)

        if "UPSCALED_" not in filename:
            file_prefix = os.path.splitext(filename)[0]
            # Split the image
            top_left, top_right, bottom_left, bottom_right = split_image(input_file)
            # Save the output images with dynamic names in the output folder
            top_left.save(os.path.join(output_folder, file_prefix + "_top_left.jpg"))
            top_right.save(os.path.join(output_folder, file_prefix + "_top_right.jpg"))
            bottom_left.save(os.path.join(output_folder, file_prefix + "_bottom_left.jpg"))
            bottom_right.save(os.path.join(output_folder, file_prefix + "_bottom_right.jpg"))

        else:
            os.rename(f"{directory}/{input_folder}/{filename}", f"{directory}/{output_folder}/{filename}")
        # Delete the input file
        os.remove(f"{directory}/{input_folder}/{filename}")


################ my code here
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    # Send a prompt to a specific channel when the bot starts
    target_channel_id = 1102908048122593302
    prompt_text = "make a pic of car?"
    await send_slash_command(target_channel_id, total_data)


@client.event
async def on_message(message):
    for attachment in message.attachments:
        if "Upscaled by" in message.content:
            file_prefix = 'UPSCALED_'
        else:
            file_prefix = ''
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            await download_image(attachment.url, f"{file_prefix}{attachment.filename}")

client.run(discord_token)

#####################################################################################

