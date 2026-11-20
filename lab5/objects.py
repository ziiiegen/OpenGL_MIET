from OpenGL import GL as gl


# Рисует четырёхугольник по списку vertices текущим цветом.
def draw_quad(vertices):
    gl.glBegin(gl.GL_QUADS)
    for x, y, z in vertices:
        gl.glVertex3f(x, y, z)
    gl.glEnd()


# Рисует пол
def draw_floor(back_z):
    gl.glColor3f(0.70, 0.72, 0.73)
    draw_quad(((-3.4, 0, back_z), (3.4, 0, back_z), (3.4, 0, 4), (-3.4, 0, 4)))


# Рисует куб с центром (x, y, z) и ребром size.
# Для тени shadow=True оставляет цвет, заданный перед вызовом.
def draw_cube(x, y, z, size, shadow=False):
    left, right = x - size / 2, x + size / 2
    bottom, top = y - size / 2, y + size / 2
    back, front = z - size / 2, z + size / 2
    vertices = (
        (left, bottom, back), (right, bottom, back),
        (right, bottom, front), (left, bottom, front),
        (left, top, back), (right, top, back),
        (right, top, front), (left, top, front),
    )
    # Грани окрашены по-разному, чтобы форма куба читалась с обеих сторон зеркала.
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
