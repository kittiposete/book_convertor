import numpy as np
from stl import mesh


def __create_ball(radius=1, segments=64):
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
            mesh.vectors[i][j] = mesh.vectors[i][j] + (translation * 2)
    return mesh

def merge_meshes(mesh1, mesh2):
    combined_mesh = mesh.Mesh(np.concatenate([mesh1.data, mesh2.data]))
    return combined_mesh

def ball():
    return __create_ball()

def char_to_braille(char):

    if str(char).upper() == 'A':
        # A is ⠁
        first_ball = translate_mesh(ball(), [0, 0, 0])
        return first_ball
    elif str(char).upper() == 'B':
        # B is ⠃
        first_ball = translate_mesh(ball(), [0, 0, 0])
        second_ball = translate_mesh(ball(), [0, 2, 0])
        return merge_meshes(first_ball, second_ball)
    elif str(char).upper() == 'C':
        # C is ⠉
        first_ball = translate_mesh(ball(), [0, 0, 0])
        second_ball = translate_mesh(ball(), [2, 0, 0])
        return merge_meshes(first_ball, second_ball)


if __name__ == '__main__':
    a_mesh = char_to_braille('a')
    a_mesh.save('a.stl')
    print('A saved to a.stl')

    b_mesh = char_to_braille('b')
    b_mesh.save('b.stl')
    print('B saved to b.stl')

    c_mesh = char_to_braille('c')
    c_mesh.save('c.stl')
    print('C saved to c.stl')