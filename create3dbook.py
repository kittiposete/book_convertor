import datetime

import numpy as np
from PIL import Image
from stl import mesh

import brail_char
import gemini_anaylize_image


def create_box(width, height, depth=1):
    # Define the 8 vertices of the box
    vertices = np.array([
        [0, 0, 0],
        [width, 0, 0],
        [width, height, 0],
        [0, height, 0],
        [0, 0, depth],
        [width, 0, depth],
        [width, height, depth],
        [0, height, depth]
    ])

    # Define the 12 triangles composing the box
    faces = np.array([
        [0, 3, 1], [1, 3, 2],  # Bottom face
        [0, 1, 4], [1, 5, 4],  # Front face
        [1, 2, 5], [2, 6, 5],  # Right face
        [2, 3, 6], [3, 7, 6],  # Back face
        [3, 0, 7], [0, 4, 7],  # Left face
        [4, 5, 6], [4, 6, 7]  # Top face
    ])

    # Create the mesh
    box = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            box.vectors[i][j] = vertices[f[j], :]

    return box


class book_3d:
    def __init__(self, width, height, image_path):
        self.width = width
        self.height = height
        self.image_path = image_path

        # Create a base flat model
        print("create box with width: ", width, " height: ", height)
        self.model = create_box(width * 15, height * 15, 1)

        # Process OCR header and add text (flat)
        header = gemini_anaylize_image.analyze_image(image_path)
        header_lines = [header[i:i + 50] for i in range(0, len(header), 50)]
        for i, line in enumerate(header_lines):
            self.add_text(line, 0, height + 10 + (i * 10), 0, 10)
        print("done init, header: ", header)

        # Process background to create reliefs based on color

    def process_background(self, image_path):
        # Open the image using Pillow
        img = Image.open(image_path).convert('RGB')
        img_width, img_height = img.size

        # Define the sampling resolution and scale factors.
        # Adjust these values as needed to map image pixels to model coordinates.
        sample_step = 1  # pixels per sample
        scale_factor = 15 / sample_step  # to map into model scale

        work = img_height // sample_step
        convexs = []

        for y in range(0, img_height, sample_step):
            print("processing background: ", y // sample_step, " of ", work)
            for x in range(0, img_width, sample_step):
                r, g, b = img.getpixel((x, y))
                # Check if the pixel is not white (background)
                if (r, g, b) != (255, 255, 255):
                    # Dark pixels (assumed text) remain flat, others extrude
                    # Adjust threshold as needed
                    if r + g + b < 600:
                        depth = 4
                    elif r + g + b < 690:
                        depth = 8
                    else:
                        depth = 10  # extruded background region

                    # Map image coordinates to model coordinates.
                    model_x = x * scale_factor
                    model_y = y * scale_factor

                    # Create a small convex block at the coordinate.
                    # The block size here is set equal to the scaled sample step.
                    convex = self.get_convex(depth, model_x, model_x + (sample_step * scale_factor),
                                             model_y, model_y + (sample_step * scale_factor))
                    convexs.append(convex)

        # Merge all convex blocks into a single mesh
        convexs.append(self.model)
        self.model = brail_char.merge_many_meshes(convexs)

    def __add_char(self, char, x, y, size):
        if char == ' ':
            return

        # Create a 3D model of a character in Braille
        char_in_3d = brail_char.char_to_braille(char)
        if char_in_3d is not None:
            char_in_3d = brail_char.translate_mesh(char_in_3d, [x, y, 15])
            char_in_3d = brail_char.scale_mesh(char_in_3d, size)
            self.model = brail_char.merge_meshes(self.model, char_in_3d)

    def add_text(self, text, x, y, w, h):
        char_count = 0
        y_adjusted = y

        for c in text:
            self.__add_char(c, x + (char_count * 10), y_adjusted, 15)
            char_count += 1

    def save(self, filename):
        print("starting process background")
        start_time = datetime.datetime.now()
        self.process_background(self.image_path)
        end_time = datetime.datetime.now()
        print("done process background in: ", end_time - start_time)

        self.model.save(filename)

    def get_convex(self, high, x_start, x_end, y_start, y_end):
        # Define the 8 vertices of the convex block
        x_start *= 15
        x_end *= 15
        y_start *= 15
        y_end *= 15
        vertices = np.array([
            [x_start, y_start, 0],
            [x_end, y_start, 0],
            [x_end, y_end, 0],
            [x_start, y_end, 0],
            [x_start, y_start, high],
            [x_end, y_start, high],
            [x_end, y_end, high],
            [x_start, y_end, high]
        ])

        # Define the 12 triangles composing the block
        faces = np.array([
            [0, 3, 1], [1, 3, 2],  # Bottom face
            [0, 1, 4], [1, 5, 4],  # Front face
            [1, 2, 5], [2, 6, 5],  # Right face
            [2, 3, 6], [3, 7, 6],  # Back face
            [3, 0, 7], [0, 4, 7],  # Left face
            [4, 5, 6], [4, 6, 7]  # Top face
        ])

        # Create the convex mesh block
        convex = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                convex.vectors[i][j] = vertices[f[j], :]

        # self.model = brail_char.merge_meshes(self.model, convex)
        return convex
