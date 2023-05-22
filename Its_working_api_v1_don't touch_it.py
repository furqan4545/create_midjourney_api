from discord_server import send_slash_command
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import requests
from PIL import Image
import os
import json

app = FastAPI()

class Data(BaseModel):
    baseid: str
    tableid: str
    recordid: str


def send_slash_command(headers, prompt):
    # Mock function to represent sending a message to a Discord server.
    # channel_id = 1102908048122593302
    # prompt_text = "make a pic of bike"

    # # Create a new event loop
    # loop = asyncio.new_event_loop()

    # # Set the event loop for the current context
    # asyncio.set_event_loop(loop)

    # # Run the command
    # loop.run_until_complete(send_slash_command(channel_id, prompt_text))
    pass

@app.post("/send_prompt/")
async def send_prompt_to_discord(data: Data):
    # api-endpoint
    URL = f"https://api.airtable.com/v0/{data.baseid}/{data.tableid}/{data.recordid}"
      
    head = {"Authorization" : "Bearer keypYvClRSuGyqnU8"}
    # sending get request and saving the response as response object
    r = requests.get(url = URL, headers = head)

    # raise HTTPException if request is unsuccessful
    if r.status_code != 200:
        raise HTTPException(status_code=400, detail="Airtable API request unsuccessful")

    # extracting data in json format
    data = r.json()
    no_of_images = len(data["fields"]["🐍 Scene 1 Storyboard"])
    scene1_description = data["fields"]["🐍 Scene 1 Description"]

    images = []

    for i in range(no_of_images):
        filter1 = data["fields"]["🐍 Scene 1 Storyboard"][i]["thumbnails"]["large"]["url"]
        images.append(filter1)

    total_data = f"{', '.join(images)}, {scene1_description}"
    
    # send_slash_command(data.headers, total_data)
    return {"message": total_data}


# channel_id = 1102908048122593302
# prompt_text = "make a pic of bike"

# # Create a new event loop
# loop = asyncio.new_event_loop()

# # Set the event loop for the current context
# asyncio.set_event_loop(loop)

# # Run the command
# loop.run_until_complete(send_slash_command(channel_id, prompt_text))








