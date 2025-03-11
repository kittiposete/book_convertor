import numpy as np
from stl import mesh

import brail_char


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
    def __init__(self, width, height):
        self.width = width
        self.height = height

        depth = 1
        self.model = create_box(width, height, depth)

    def __add_char(self, char, x, y, size):
        if char == ' ':
            return

        # Create a 3D model of a ball
        char_in_3d = brail_char.char_to_braille(char)
        if char_in_3d is not None:
            char_in_3d = brail_char.translate_mesh(char_in_3d, [x, y, 0])
            char_in_3d = brail_char.scale_mesh(char_in_3d, size)
            # print("scale: ", size)
            self.model = brail_char.merge_meshes(self.model, char_in_3d)

    def add_text(self, text, x, y, w, h):
        width_per_char = w / len(text)
        for c in text:
            self.__add_char(c, x, y + 10, 10)

    def save(self, filename):
        self.model.save(filename)
