import numpy as np
from stl import mesh


def __create_ball(radius=0.5, segments=32):
    # Create a grid of points in spherical coordinates
    phi = np.linspace(0, np.pi, segments)
    theta = np.linspace(0, 2 * np.pi, segments)
    phi, theta = np.meshgrid(phi, theta)

    # Convert spherical coordinates to Cartesian coordinates
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    # Flatten the arrays
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    # Create the vertices array
    vertices = np.vstack((x, y, z)).T

    # Create the faces array
    faces = []
    for i in range(segments - 1):
        for j in range(segments - 1):
            p1 = i * segments + j
            p2 = p1 + segments
            p3 = p1 + 1
            p4 = p2 + 1
            faces.append([p1, p2, p3])
            faces.append([p3, p2, p4])

    faces = np.array(faces)

    # Create the mesh
    ball = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            ball.vectors[i][j] = vertices[f[j], :]

    return ball


#
# def translate_mesh(mesh, translation):
#     for i in range(len(mesh.vectors)):
#         for j in range(3):
#             # mesh.vectors[i][j] += translation
#             mesh.vectors[i][j] = mesh.vectors[i][j] + (translation * 2)
#             # print("translation", translation)
#     return mesh

def translate_mesh(mesh, translation):
    translation = np.array(translation)
    for i in range(len(mesh.vectors)):
        for j in range(3):
            mesh.vectors[i][j] = mesh.vectors[i][j] + (translation * 1)  # * 2)
    return mesh


def merge_meshes(mesh1, mesh2):
    combined_mesh = mesh.Mesh(np.concatenate([mesh1.data, mesh2.data]))
    return combined_mesh


def scale_mesh(mesh, scale):
    for i in range(len(mesh.vectors)):
        for j in range(3):
            mesh.vectors[i][j] *= scale
    return mesh


def ball():
    return __create_ball()


def char_to_braille(char):
    # Mapping for Braille dot positions using a 2-column x 3-row cell.
    # Coordinates represent left column dot and right column dots.
    # The translation is applied inside translate_mesh, which multiplies each offset by 2.
    braille_map = {
        'A': [(0, 0, 0)],
        'B': [(0, 0, 0), (0, 2, 0)],
        'C': [(0, 0, 0), (2, 0, 0)],
        'D': [(0, 0, 0), (2, 0, 0), (2, 2, 0)],
        'E': [(0, 0, 0), (2, 2, 0)],
        'F': [(0, 0, 0), (0, 2, 0), (2, 0, 0)],
        'G': [(0, 0, 0), (0, 2, 0), (2, 0, 0), (2, 2, 0)],
        'H': [(0, 0, 0), (0, 2, 0), (2, 2, 0)],
        'I': [(0, 2, 0), (2, 0, 0)],
        'J': [(0, 2, 0), (2, 0, 0), (2, 2, 0)],
        'K': [(0, 0, 0), (0, 4, 0)],
        'L': [(0, 0, 0), (0, 2, 0), (0, 4, 0)],
        'M': [(0, 0, 0), (0, 4, 0), (2, 0, 0)],
        'N': [(0, 0, 0), (0, 4, 0), (2, 0, 0), (2, 2, 0)],
        'O': [(0, 0, 0), (0, 4, 0), (2, 2, 0)],
        'P': [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 0, 0)],
        'Q': [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 0, 0), (2, 2, 0)],
        'R': [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 2, 0)],
        'S': [(0, 2, 0), (0, 4, 0), (2, 0, 0)],
        'T': [(0, 2, 0), (0, 4, 0), (2, 0, 0), (2, 2, 0)],
        'U': [(0, 0, 0), (0, 4, 0), (2, 4, 0)],
        'V': [(0, 0, 0), (0, 2, 0), (0, 4, 0), (2, 4, 0)],
        'W': [(0, 2, 0), (2, 0, 0), (2, 2, 0), (2, 4, 0)],
        'X': [(0, 0, 0), (0, 4, 0), (2, 0, 0), (2, 4, 0)],
        'Y': [(0, 0, 0), (0, 4, 0), (2, 0, 0), (2, 2, 0), (2, 4, 0)],
        'Z': [(0, 0, 0), (0, 4, 0), (2, 2, 0), (2, 4, 0)],
    }

    # Add mappings for digits 0-9
    # In Grade‑1 Braille the digits 1–9, 0 are represented using the same patterns as A–I, J respectively.
    number_map = {
        '1': braille_map['A'],
        '2': braille_map['B'],
        '3': braille_map['C'],
        '4': braille_map['D'],
        '5': braille_map['E'],
        '6': braille_map['F'],
        '7': braille_map['G'],
        '8': braille_map['H'],
        '9': braille_map['I'],
        '0': braille_map['J']
    }
    # Update braille_map to include digit mappings
    braille_map.update(number_map)

    mapping = braille_map.get(str(char).upper())
    if not mapping:
        # raise ValueError(f"Braille representation for character {char} is not defined.")
        print("warning", f"Braille representation for character {char} is not defined.")
        return None

    # Get the initial ball mesh for the first dot
    result = None
    for offset in mapping:
        ball_mesh = translate_mesh(ball(), offset)
        if result is None:
            result = ball_mesh
        else:
            result = merge_meshes(result, ball_mesh)
    return result
