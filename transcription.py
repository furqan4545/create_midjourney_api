# from vimeo_downloader import Vimeo

# v = Vimeo('https://vimeo.com/413682378')
# v.streams

# v.streams[0].download(download_directory='./videos/',
#                           filename='shit')


# ### For downloading youtube videos
# #Importing Pytube library
# import pytube
# from pytube import YouTube

# from pytube import YouTube

# def Download(link):
#     youtubeObject = YouTube(link)
#     youtubeObject = youtubeObject.streams.get_highest_resolution()
#     try:
#         youtubeObject.download()
#     except:
#         print("An error has occurred")
#     print("Download is completed successfully")

# # link = input("Enter the YouTube video URL: ")
# link = "https://youtu.be/8SQV-B83tPU"

# Download(link)


# from fastapi import FastAPI, HTTPException
# from vimeo_downloader import Vimeo
# from pytube import YouTube
# import os
# from pydantic import BaseModel


# class Video(BaseModel):
#     url: str

# app = FastAPI()

# @app.post("/download_video/")
# async def download_video(url: str):
#     if 'vimeo' in url:
#         try:
#             v = Vimeo(url)
#             v.streams[0].download(download_directory='./videos/', filename='vimeo_video')
#             return {"status": "Vimeo video download is completed successfully."}
#         except Exception as e:
#             raise HTTPException(status_code=400, detail=str(e))

#     elif 'youtube' in url or 'youtu.be' in url:
#         try:
#             yt = YouTube(url)
#             yt.streams.get_highest_resolution().download()
#             return {"status": "YouTube video download is completed successfully."}
#         except Exception as e:
#             raise HTTPException(status_code=400, detail=str(e))

#     else:
#         raise HTTPException(status_code=400, detail="Invalid URL. Please provide either YouTube or Vimeo URL.")

from fastapi import FastAPI
from pydantic import BaseModel
from vimeo_downloader import Vimeo
from pytube import YouTube
import re
import openai
import os
import whisper
import subprocess

model = whisper.load_model("medium")

class Video(BaseModel):  
    url: str

app = FastAPI()

@app.post("/download_video/")
async def download_video(video: Video):
    url = video.url
    vimeo_pattern = "https?://(www\.)?vimeo.com/(\d+)"
    youtube_pattern = "https?://(www\.)?youtu\.be/(.*)"

    if re.match(vimeo_pattern, url):
        v = Vimeo(url)
        meta = v.metadata
        print("vimeo: ", meta)
        v.streams[0].download(download_directory='./videos/', filename='vimeo_video')
        # Note: you need to be using OpenAI Python v0.27.0 for the code below to work
        
        # audio_file= open("./videos/vimeo_video.mp4", "rb")
        result = model.transcribe("./videos/vimeo_video.mp4")
        print(result["text"])
        # transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return {"status": "Vimeo video downloaded successfully"}

    elif re.match(youtube_pattern, url):
        yt = YouTube(url)
        video_path = yt.streams.get_highest_resolution().download(output_path='./videos/', filename='yt_video.mp4')
        vid_length = yt.length
        print("video length: ", vid_length)
        print("video path: ", video_path)
        video_filename = os.path.split(video_path)[-1]
        print("file name ali: ", video_filename)
        # audio_file = f"./videos/{video_filename}"
        # audio_file = f"./videos/{video_filename}"
        audio_file = "./videos/yt_video.mp4"
        print("audio file ali: ", audio_file)
        result = model.transcribe(audio_file)
        print(result["text"])
        
        # command = f'whisper "{audio_file}" --model medium.en'
        # list_files = subprocess.run(command, capture_output=True, text=True, shell=True)
        # print("list files : ", list_files)
        
        # result = model.transcribe(audio_file)
        # transcript = openai.Audio.transcribe("whisper-1", audio_file)
        return {"msg": "result"}

    else:
        return {"error": "URL not recognized"}














