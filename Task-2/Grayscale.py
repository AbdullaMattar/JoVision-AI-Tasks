from PIL import Image
import sys
import pytesseract
import numpy as np

if len(sys.argv) > 1:
    fileName = sys.argv[1]
    if not fileName.lower().endswith((".png", ".jpg", ".jpeg")):
        print("error : supported image types are png jpg jpeg")
        exit()
else:
    print("No agrument passed ....Exiting")
    exit()


# part 2 - Grayscaling
def to_greyscale(image_path):
    try:
        img = Image.open(image_path)
        width, height = img.size
        print(f"{height} and width {width}")
        for x in range(width):
            for y in range(height):
                # Get the pixel
                r, g, b = img.getpixel((x, y))[:3]
                # Calculate the gray
                gray_value = (r + g + b) // 3
                # replace the pixel
                img.putpixel((x, y), (gray_value, gray_value, gray_value))
        img.show()
    except Exception as e:
        print(f"problem inverting to greyscale \n {e}")


to_greyscale(fileName)
