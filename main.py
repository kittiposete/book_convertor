from PIL import Image
import pytesseract

# Load the image from file
image = Image.open('/Users/kittipos/Developer/book_convertor/Set-Theory.png')

# Use pytesseract to get detailed OCR results
data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

# Iterate through the detected text and print the text with its bounding box coordinates
for i in range(len(data['text'])):
    if int(data['conf'][i]) > 0:  # Filter out weak confidence results
        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
        text = data['text'][i]
        print(f'Text: \'{text}\', Location: ({x}, {y}, {w}, {h})')