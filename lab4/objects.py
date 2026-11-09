from math import pi, sin, cos

from OpenGL.GL import (
    GL_TEXTURE_2D, GL_QUADS, GL_QUAD_STRIP,
    glColor3f, glPushMatrix, glPopMatrix, glTranslatef, glScalef,
    glEnable, glDisable, glBindTexture, glBegin, glEnd,
    glNormal3f, glTexCoord2f, glVertex3f,
)
from OpenGL.GLUT import glutSolidCube

TABLE_TOP = 1.83
GLOBE_RADIUS = 0.67


# Рисует куб с центром (x, y, z); size — его размеры по трём осям.
def draw_box(x, y, z, size):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(*size)
    glutSolidCube(1)
    glPopMatrix()


# Рисует плоскость с текстурой: vertices — четыре вершины, normal — нормаль.
# repeat_x и repeat_y задают число повторений картинки по двум направлениям.
def draw_surface(texture, vertices, normal, repeat_x=1, repeat_y=1):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor3f(1, 1, 1)
    coordinates = ((0, 0), (repeat_x, 0), (repeat_x, repeat_y), (0, repeat_y))
    glBegin(GL_QUADS)
    glNormal3f(*normal)
    for coordinate, vertex in zip(coordinates, vertices):
        glTexCoord2f(*coordinate)
        glVertex3f(*vertex)
    glEnd()
    glDisable(GL_TEXTURE_2D)


# Рисует стол из прошлой работы и деревянную текстуру на верхней плоскости.
# wood — номер текстуры. Ножки и толщина столешницы сделаны из кубов.
def draw_table(wood):
    glColor3f(0.55, 0.32, 0.16)
    draw_box(0, 1.75, 0, (2.8, 0.16, 1.8))
    glColor3f(0.30, 0.30, 0.30)
    for x in (-1.17, 1.17):
        for z in (-0.67, 0.67):
            draw_box(x, 0.835, z, (0.14, 1.67, 0.14))

    y = TABLE_TOP + 0.001
    draw_surface(wood, ((-1.4, y, 0.9), (1.4, y, 0.9),
                        (1.4, y, -0.9), (-1.4, y, -0.9)), (0, 1, 0))


# Добавляет вершину единичной сферы по координатам s и t от 0 до 1.
# Нормаль направлена из центра сферы; функция ничего не возвращает.
def sphere_vertex(s, t):
    longitude = 2 * pi * s
    latitude = pi * (t - 0.5)  # Широта меняется от -pi/2 до pi/2.
    x = cos(latitude) * sin(longitude)
    y = sin(latitude)
    z = cos(latitude) * cos(longitude)
    glNormal3f(x, y, z)
    glTexCoord2f(s, t)  # Вручную связываем долготу и широту с картинкой.
    glVertex3f(x, y, z)


# Рисует сферу радиуса radius; texture — номер картинки с картой мира.
# Сферу строим сами полосами четырёхугольников, без GLU и glutSolidSphere.
def draw_sphere(radius, texture):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)
    glColor3f(1, 1, 1)

    glPushMatrix()
    glScalef(radius, radius, radius)
    latitude_steps = 32
    longitude_steps = 64
    for i in range(latitude_steps):
        glBegin(GL_QUAD_STRIP)
        for j in range(longitude_steps + 1):
            s = j / longitude_steps
            sphere_vertex(s, i / latitude_steps)
            sphere_vertex(s, (i + 1) / latitude_steps)
        glEnd()
    glPopMatrix()

    glDisable(GL_TEXTURE_2D)
