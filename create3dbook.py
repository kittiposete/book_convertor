

class book_3d:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def add_text(self, text, x, y):
        pass




    def save(self, filename):
        # Create a 3D model of a ball
        ball = self.__create_ball(radius=1, segments=64)

        # Write the mesh to file "ball.stl"
        ball.save(filename)

        print(f'3D model saved to {filename}')