from math import cos, pi, sin

from OpenGL import GL, GLUT

TABLE_TOP_Y = 1.83


# Рисует параллелепипед. center — его центр, size — размеры по трём осям.
def draw_box(center, size):
    GL.glPushMatrix()
    GL.glTranslatef(*center)
    GL.glScalef(*size)  # Куб со стороной 1 растягиваем до нужных размеров.
    GLUT.glutSolidCube(1)
    GL.glPopMatrix()


# Рисует прямоугольник. vertices — четыре угла, normal — нормаль к поверхности.
# texture — номер текстуры, repeats — сколько раз картинка повторяется по s и t.
def draw_surface(texture, vertices, normal, repeats=(1, 1)):
    repeat_s, repeat_t = repeats
    texture_coords = ((0, 0), (repeat_s, 0), (repeat_s, repeat_t), (0, repeat_t))

    GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glColor3f(1, 1, 1)  # Белый цвет материала сохраняет оттенки текстуры.
    GL.glBegin(GL.GL_QUADS)
    GL.glNormal3f(*normal)
    for (s, t), vertex in zip(texture_coords, vertices):
        GL.glTexCoord2f(s, t)  # Координаты картинки относятся к следующей вершине.
        GL.glVertex3f(*vertex)
    GL.glEnd()
    GL.glDisable(GL.GL_TEXTURE_2D)


# Рисует стол из столешницы и четырёх ножек. wood_texture — текстура дерева.
def draw_table(wood_texture):
    top_thickness = 0.16
    leg_height = TABLE_TOP_Y - top_thickness

    GL.glColor3f(0.55, 0.32, 0.16)
    draw_box((0, TABLE_TOP_Y - top_thickness / 2, 0), (2.8, top_thickness, 1.8))

    GL.glColor3f(0.30, 0.30, 0.30)
    for x in (-1.17, 1.17):
        for z in (-0.67, 0.67):
            draw_box((x, leg_height / 2, z), (0.14, leg_height, 0.14))

    # Кладём текстуру чуть выше куба, чтобы поверхности не мерцали.
    y = TABLE_TOP_Y + 0.001
    tabletop = ((-1.4, y, 0.9), (1.4, y, 0.9), (1.4, y, -0.9), (-1.4, y, -0.9))
    draw_surface(wood_texture, tabletop, (0, 1, 0))


# Добавляет вершину сферы радиуса radius. s и t — координаты картинки от 0 до 1.
def sphere_vertex(s, t, radius):
    longitude = 2 * pi * s       # Полный оборот вокруг оси Y.
    latitude = pi * (t - 0.5)    # От южного полюса до северного.
    x = cos(latitude) * sin(longitude)
    y = sin(latitude)
    z = cos(latitude) * cos(longitude)

    GL.glNormal3f(x, y, z)  # На единичной сфере нормаль совпадает с радиусом-вектором.
    GL.glTexCoord2f(s, t)    # У глобуса s соответствует долготе, а t — широте.
    GL.glVertex3f(radius * x, radius * y, radius * z)


# Рисует текстурированную сферу с центром center и радиусом radius.
# texture — номер текстуры. Соседние параллели соединяются полосами четырёхугольников.
def draw_sphere(texture, center, radius):
    latitude_steps = 32
    longitude_steps = 64

    GL.glPushMatrix()
    GL.glTranslatef(*center)
    GL.glEnable(GL.GL_TEXTURE_2D)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glColor3f(1, 1, 1)

    for row in range(latitude_steps):
        bottom = row / latitude_steps
        top = (row + 1) / latitude_steps
        GL.glBegin(GL.GL_QUAD_STRIP)
        # Последняя колонка замыкает полосу в той же точке, но с s = 1.
        for column in range(longitude_steps + 1):
            s = column / longitude_steps
            sphere_vertex(s, bottom, radius)
            sphere_vertex(s, top, radius)
        GL.glEnd()

    GL.glDisable(GL.GL_TEXTURE_2D)
    GL.glPopMatrix()
