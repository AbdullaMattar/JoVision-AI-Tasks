import cv2
import os
import numpy as np
import sys
import glob
from pathlib import Path
from PIL import Image
from dataclasses import dataclass
import pandas as pd

# will accept one arg -> folder of the images
if len(sys.argv) > 1:
    dirName = sys.argv[1]
    if not os.path.isdir(dirName):
        print(f"error : {dirName} does not exist")
        exit()
else:
    print("No agrument passed ....Exiting")
    exit()

# getting the images
image_directory = Path(dirName)
image_files = list(image_directory.glob("*.png")) + list(image_directory.glob("*.jpg"))


@dataclass
class HandData:
    hand: np.ndarray
    bar: np.ndarray
    color: str = "Unknown"
    thumb_pressure: int = 0
    index_pressure: int = 0
    middle_pressure: int = 0
    ring_pressure: int = 0
    pinky_pressure: int = 0


images = {}

# crop The Images with greyscale
for idx, image_file in enumerate(image_files, start=1):
    image_file_name = image_file.stem
    testImag = cv2.imread(str(image_file))
    height, width, _ = testImag.shape
    # crop and get the right half of the image without the bottom bar
    hand_image = testImag[0 : height - 10, width // 2 :]
    hand_image = cv2.cvtColor(hand_image, cv2.COLOR_BGR2GRAY)
    # get the bottom 5 pixels of the image
    buttom_bar = testImag[height - 10 :, :]
    images[image_file_name] = HandData(hand=hand_image, bar=buttom_bar)

# detecting color in the bar
for name, data in images.items():
    avg_green = np.mean(data.bar[:, :, 1])
    avg_red = np.mean(data.bar[:, :, 2])
    if avg_green > avg_red:
        # update the color
        data.color = "Green"
    else:
        data.color = "Red"

# detecting the fingers pressed on green bars

# image = images["hand10"].hand
# roi = cv2.selectROI("Select Finger Area", image)
# print(f"x={roi[0]}, y={roi[1]}, width={roi[2]}, height={roi[3]}")
# cv2.destroyAllWindows()


# ROI thumb numbers based on the selected area
x, y, width, height = 197, 181, 35, 73
for name, data in images.items():
    if data.color == "Green":
        finger_data = data.hand[y : y + height, x : x + width]
        avg_brightness = np.mean(finger_data)
        if avg_brightness > 52:  # value 52 is by trial and error
            data.thumb_pressure = 1
        else:
            data.thumb_pressure = 0
    else:
        data.thumb_pressure = 0

# ROI index numbers based on the selected area
x, y, width, height = 0, 120, 80, 24
for name, data in images.items():
    if data.color == "Green":
        finger_data = data.hand[y : y + height, x : x + width]
        avg_brightness = np.mean(finger_data)
        if avg_brightness > 52:
            data.index_pressure = 1
        else:
            data.index_pressure = 0
    else:
        data.index_pressure = 0

# ROI middle numbers based on the selected area
x, y = 0, 78
for name, data in images.items():
    if data.color == "Green":
        finger_data = data.hand[y : y + height, x : x + width]
        avg_brightness = np.mean(finger_data)
        if avg_brightness > 52:
            data.middle_pressure = 1
        else:
            data.middle_pressure = 0
    else:
        data.middle_pressure = 0

# ROI ring numbers based on the selected area
x, y = 0, 46
for name, data in images.items():
    if data.color == "Green":
        finger_data = data.hand[y : y + height, x : x + width]
        avg_brightness = np.mean(finger_data)
        if avg_brightness > 52:
            data.ring_pressure = 1
        else:
            data.ring_pressure = 0
    else:
        data.ring_pressure = 0

# ROI pinky numbers based on the selected area
x, y = 0, 0
for name, data in images.items():
    if data.color == "Green":
        finger_data = data.hand[y : y + height, x : x + width]
        avg_brightness = np.mean(finger_data)
        if avg_brightness > 52:
            data.pinky_pressure = 1
        else:
            data.pinky_pressure = 0
    else:
        data.pinky_pressure = 0

# export to excel

df = pd.DataFrame(
    {
        "Hand": list(images.keys()),
        "Bar Color": [data.color for data in images.values()],
        "Thumb Pressure": [data.thumb_pressure for data in images.values()],
        "Index Pressure": [data.index_pressure for data in images.values()],
        "Middle Pressure": [data.middle_pressure for data in images.values()],
        "Ring Pressure": [data.ring_pressure for data in images.values()],
        "Pinky Pressure": [data.pinky_pressure for data in images.values()],
    }
)
df.to_excel("hand_data.xlsx", index=False)
