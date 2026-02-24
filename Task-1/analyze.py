from PIL import Image
import sys
import pytesseract


if len(sys.argv) > 1:
    fileName = sys.argv[1]
    if not fileName.lower().endswith((".png", ".jpg", ".jpeg")):
        print("error : supported image types are png jpg jpeg")
        exit()
else:
    print("No agrument passed ....Exiting")
    exit()

try:
    img = Image.open(fileName)
    text = pytesseract.image_to_string(img)
    print(f"Extracted text:\n {text}")

except Exception as e:
    print(f"problem extracting text \n {e}")
