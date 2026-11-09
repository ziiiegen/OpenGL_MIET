from OpenGL.GL import glColor3f, glPushMatrix, glPopMatrix, glTranslatef, glRotatef, glScalef
from OpenGL.GLUT import glutSolidCube, glutSolidCylinder, glutSolidTeapot

TABLE_TOP = 1.83


# Рисует растянутый куб: (x, y, z) — центр, size — размеры по трём осям.
def draw_box(x, y, z, size):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(*size)
    glutSolidCube(1)
    glPopMatrix()


# Рисует стол с четырьмя ножками; начало координат — под центром стола на полу.
def draw_table():
    glColor3f(0.65, 0.40, 0.20)
    draw_box(0, 1.75, 0, (2.8, 0.16, 1.8))
    glColor3f(0.30, 0.30, 0.30)
    for x in (-1.17, 1.17):
        for z in (-0.67, 0.67):
            draw_box(x, 0.835, z, (0.14, 1.67, 0.14))


# Рисует книгу одним параллелепипедом; нижняя сторона лежит на Y = 0.
def draw_book():
    glColor3f(0.70, 0.15, 0.15)
    draw_box(0, 0.08, 0, (0.8, 0.16, 0.55))


# Рисует ручку одним цилиндром вдоль оси X, лежащим на Y = 0.
def draw_pen():
    glPushMatrix()
    glTranslatef(-0.4, 0.03, 0)
    glRotatef(90, 0, 1, 0)  # Цилиндр GLUT направлен вдоль Z; поворачиваем вдоль X.
    glColor3f(0.10, 0.20, 0.80)
    glutSolidCylinder(0.03, 0.8, 12, 1)
    glPopMatrix()


# Рисует чайник GLUT; подъём на 0.255 ставит основание модели на Y = 0.
def draw_teapot():
    glPushMatrix()
    glTranslatef(0, 0.255, 0)
    glColor3f(0.1, 0.65, 0.5)
    glutSolidTeapot(0.34)
    glPopMatrix()
