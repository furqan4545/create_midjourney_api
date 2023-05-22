
import cv2

# Open the video file.
video = cv2.VideoCapture('./videos/shit.mp4')

# Initialize frame counter
count = 0

while True:
    # Read the video frame by frame.
    ret, frame = video.read()

    # If the video is finished, break the loop.
    if not ret:
        break

    # Save every 30th frame as an image.
    if count % 60 == 0:
        cv2.imwrite('./frames/frame{}.png'.format(count), frame)

    count += 1

# Release the VideoCapture object.
video.release()










