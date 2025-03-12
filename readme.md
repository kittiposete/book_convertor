# PDF/Image to STL convertor concept

This is a concept of Book to STL convertor. To convert pdf document to stl file for print with 3D
printer for blind people to read it.

## Problem :(

Blind people have limited access to book or any other printed material. Although there are already
have some solution like audiobook or software for convert text to Braille, but that solution have
limitation which is cannot convert media that contain visualization like image, diagram, Euler
diagram, etc. So, this media that contain visualization need to convert manually which is very take
time and not efficient.

## Solution :)

From the problem above, I create a software that can convert pdf document or image to stl file,
which can produce with 3D printer. This software not only convert text to Braille but also include
an image description and diagram.

## How it works?

1. Input image file if it pdf file must convert to image format first.
2. Using Gemini to describe the document.
3. Using OCR to detect text and overwrite with Braille.
4. Surface height depend on document color so if it have any diagram or any shape it will be
   converted to 3D shape.
5. Export to STL file.

## How to use?

This software still only the concept. But you can try to use the software by following the step.

1. install python 3.12.0
2. `pip install Pillow numpy-stl pytesseract` then `pip install -q -U google-genai`
3. in `main.py` change the `file_path` to your file path.
4. run `python main.py`
5. check the output in `output_fine_3.stl`

example output have been pro