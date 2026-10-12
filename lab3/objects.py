# Здесь рисуем предметы в их собственных координатах.
# color — цвет RGB: три числа от 0 до 1. Функции ничего не возвращают.

from OpenGL.GL import *
from OpenGL.GLUT import *


# Рисует куб, растянутый до размеров width, height, depth, заданным цветом.
# Центр параллелепипеда находится в начале координат.
def draw_box(width, height, depth, color=(0.5, 0.5, 0.5)):
    glColor3f(*color)
    glPushMatrix()
    glScalef(width, height, depth)
    glutSolidCube(1)
    glPopMatrix()


# Рисует стол заданным цветом: столешницу и четыре ножки.
# Ножки стоят на Y = 0, верх столешницы находится на Y = 1.4.
def draw_table(color=(0.35, 0.20, 0.10)):
    glPushMatrix()
    glTranslatef(0, 1.34, 0)
    draw_box(3, 0.12, 1.8, color)
    glPopMatrix()

    for x in (-1.3, 1.3):
        for z in (-0.7, 0.7):
            glPushMatrix()
            glTranslatef(x, 0.64, z)
            draw_box(0.14, 1.28, 0.14, color)
            glPopMatrix()


# Рисует лежащую книгу заданным цветом как небольшой параллелепипед.
# Нижняя поверхность книги находится на Y = 0.
def draw_book(color=(0.75, 0.12, 0.12)):
    glPushMatrix()
    glTranslatef(0, 0.07, 0)
    draw_box(0.62, 0.14, 0.44, color)
    glPopMatrix()


# Рисует ручку вдоль оси X: цветной цилиндр и тёмный наконечник.
# Ручка длиной 0.8 касается поверхности Y = 0.
def draw_pen(color=(0.2, 0.3, 0.8)):
    glPushMatrix()
    glTranslatef(-0.4, 0.025, 0)
    # Цилиндр направлен вдоль Z; поворачиваем его вдоль X.
    glRotatef(90, 0, 1, 0)
    glColor3f(*color)
    glutSolidCylinder(0.025, 0.7, 16, 1)
    glTranslatef(0, 0, 0.7)
    glColor3f(0.15, 0.15, 0.15)
    glutSolidCone(0.025, 0.1, 16, 1)
    glPopMatrix()


# Рисует готовый чайник freeglut заданным цветом.
# Поднимаем модель так, чтобы её дно оказалось на Y = 0.
def draw_teapot(color=(0.15, 0.65, 0.35)):
    glPushMatrix()
    glColor3f(*color)
    glTranslatef(0, 0.7875 * 0.2, 0)
    glutSolidTeapot(0.2)
    glPopMatrix()
