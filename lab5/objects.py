from OpenGL import GL as gl


# Рисует четырёхугольник по списку vertices текущим цветом.
def draw_quad(vertices):
    gl.glBegin(gl.GL_QUADS)
    for x, y, z in vertices:
        gl.glVertex3f(x, y, z)
    gl.glEnd()


# Рисует пол. back_z задаёт его задний край по оси Z.
def draw_floor(back_z):
    gl.glColor3f(0.70, 0.72, 0.73)
    draw_quad(((-3.4, 0, back_z), (3.4, 0, back_z), (3.4, 0, 4), (-3.4, 0, 4)))


# Возвращает восемь вершин куба с центром (x, y, z) и ребром size.
def cube_vertices(x, y, z, size):
    half = size / 2
    left, right = x - half, x + half
    bottom, top = y - half, y + half
    back, front = z - half, z + half
    return (
        (left, bottom, back), (right, bottom, back),
        (right, bottom, front), (left, bottom, front),
        (left, top, back), (right, top, back),
        (right, top, front), (left, top, front),
    )


# Рисует шесть граней по vertices. При shadow=True используется текущий цвет.
def draw_cube(vertices, shadow=False):
    # У каждой грани есть номера четырёх вершин и свой цвет.
    faces = (
        ((0, 1, 2, 3), (0.1, 0.02, 0.123)),
        ((4, 5, 6, 7), (0.2, 0.04, 0.321)),
        ((0, 1, 5, 4), (0.3, 0.08, 0.123)),
        ((2, 3, 7, 6), (0.4, 0.16, 0.321)),
        ((0, 3, 7, 4), (0.5, 0.32, 0.123)),
        ((1, 2, 6, 5), (0.6, 0.64, 0.321)),
    )
    for corners, color in faces:
        if not shadow:
            gl.glColor3f(*color)
        draw_quad([vertices[index] for index in corners])
