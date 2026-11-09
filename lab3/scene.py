import random

from OpenGL.GL import (
    GL_LIGHTING, GL_LINE_LOOP, glBegin, glEnd, glVertex3f, glColor3f,
    glDisable, glEnable, glPushMatrix, glPopMatrix, glTranslatef, glRotatef, glScalef,
)
from objects import TABLE_TOP, draw_box, draw_table, draw_book, draw_pen, draw_teapot

WALL_Z = 0.0


# Рисует пол и три ряда по четыре стола с книгами, ручками и чайниками.
# seed сохраняет одну случайную расстановку при перерисовке и рисовании отражения.
def draw_classroom():
    random.seed(1)
    glColor3f(0.4745, 0.3333, 0.2392)
    draw_box(4.5, -0.08, 0, (16.0, 0.16, 26))
    for x in (0.5, 4.5, 8.5):
        for z in (2.0, 4.5, 7.0, 9.5):
            glPushMatrix()
            glTranslatef(x, 0, z)
            draw_table()

            # Предметы располагаем в разных частях столешницы, чтобы они не пересекались.
            glPushMatrix()
            glTranslatef(random.uniform(-0.8, -0.6), TABLE_TOP, random.uniform(-0.2, 0))
            glRotatef(random.uniform(-25, 25), 0, 1, 0)
            draw_book()
            glPopMatrix()

            glPushMatrix()
            glTranslatef(random.uniform(-0.3, -0.2), TABLE_TOP, random.uniform(0.6, 0.7))
            glRotatef(random.uniform(-10, 10), 0, 1, 0)
            draw_pen()
            glPopMatrix()

            glPushMatrix()
            glTranslatef(random.uniform(0.7, 0.8), TABLE_TOP, random.uniform(-0.2, 0))
            glRotatef(random.uniform(0, 360), 0, 1, 0)
            draw_teapot()
            glPopMatrix()
            glPopMatrix()


# Рисует аудиторию, её отражение относительно Z = WALL_Z и доску на этой плоскости.
def draw_scene():
    draw_classroom()
    glPushMatrix()
    # Переносим стену к нулю, меняем знак Z и возвращаем стену на место.
    # Для вершины преобразования выполняются справа налево: z' = 2 * WALL_Z - z.
    glTranslatef(0, 0, WALL_Z)
    glScalef(1, 1, -1)
    glTranslatef(0, 0, -WALL_Z)
    draw_classroom()
    glPopMatrix()

    glColor3f(0.10, 0.30, 0.20)
    draw_box(4.5, 3, WALL_Z, (4.8, 1.8, 0.1))

