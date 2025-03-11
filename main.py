import datetime

import pytesseract
from PIL import Image

import create3dbook

start_time = datetime.datetime.now()
image_path = "/Users/kittipos/Developer/book_convertor/Set-Theory.png"

# Load the image from file
image = Image.open(image_path)
image_width, image_height = image.size
print("image size: ", image.size)

# Use pytesseract to get detailed OCR results
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

model = create3dbook.book_3d(image_width, image_height, image_path)

# Iterate through the detected text and print the text with its bounding box coordinates
for i in range(len(data['text'])):
    if int(data['conf'][i]) > 0:  # Filter out weak confidence results
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        text = data['text'][i]
        print(f'Text: \'{text}\', Location: ({x}, {image_height - y}, {w}, {h})')
        model.add_text(text, x, image_height - y, w, h)

model.save('output.stl')

end_time = datetime.datetime.now()

print(f'Execution time: {end_time - start_time}')
