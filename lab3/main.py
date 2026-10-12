# Лабораторная 3: аудитория, проекции, обрезание и зеркальное отражение.

import math
import random
import sys

from OpenGL.GL import *
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL.GLUT import *

from objects import draw_box, draw_table, draw_book, draw_pen, draw_teapot


width, height = 1100, 760
projection = 2
camera_distance = 34
show_reflection = True
clipping = False
wall_z = -6  # Плоскость стены с доской; саму стену не рисуем.

# Один раз создаём позиции, повороты и цвета предметов для 12 столов.
# Три участка по X не дают предметам пересекаться. Их порядок случайный.
tables = []
for row in range(3):
    for column in range(4):
        places = [-1, 0, 1]
        random.shuffle(places)
        items = []
        for x in places:
            items.append((x + random.uniform(-0.08, 0.08),
                          random.uniform(-0.35, 0.35),
                          random.uniform(0, 360)))
        color = (random.random(), random.random(), random.random())
        tables.append((items, color))


# Рисует пол и аудиторию из трёх рядов по четыре стола.
# Использует сохранённые tables; параметров нет, ничего не возвращает.
def draw_audience():
    glPushMatrix()
    glTranslatef(0, -0.05, 0)
    draw_box(17, 0.1, 12, (0.6, 0.6, 0.55))
    glPopMatrix()

    for row in range(3):
        for column in range(4):
            items, color = tables[row * 4 + column]
            glPushMatrix()
            # Центры столов: X = -6, -2, 2, 6; Z = -3.1, 0, 3.1.
            glTranslatef(column * 4 - 6, 0, row * 3.1 - 3.1)
            draw_table()

            # Порядок предметов совпадает с порядком сохранённых позиций.
            for i, draw_object in enumerate((draw_book, draw_pen, draw_teapot)):
                x, z, angle = items[i]
                glPushMatrix()
                glTranslatef(x, 1.4, z)
                glRotatef(angle, 0, 1, 0)
                if i == 0:
                    draw_object(color)
                else:
                    draw_object()
                glPopMatrix()
            glPopMatrix()


# Рисует кадр: выбирает проекцию, ставит камеру, рисует сцену и отражение.
# Параметров нет, ничего не возвращает. GLUT вызывает её при перерисовке.
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = width / height

    # При C сужаем видимый объём: плоскости near/far обрезают геометрию.
    near = max(0.1, camera_distance - 6) if clipping else 0.1
    far = camera_distance + 6 if clipping else 120
    if projection == 1:
        glOrtho(-15 * aspect, 15 * aspect, -15, 15, near, far)
    elif projection == 2:
        gluPerspective(45, aspect, near, far)
    else:
        # Границы ближней плоскости дают ту же перспективу с углом 45°.
        top = near * math.tan(math.radians(45 / 2))
        glFrustum(-top * aspect, top * aspect, -top, top, near, far)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    target_z = wall_z if show_reflection else 0
    # Меняем положение камеры через gluLookAt, сохраняя направление взгляда.
    gluLookAt(camera_distance * 0.6, 1 + camera_distance * 0.48,
              target_z + camera_distance * 0.64,
              0, 1, target_z, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 8, wall_z, 1))

    draw_audience()
    if show_reflection:
        glPushMatrix()
        # К вершине преобразования применяются снизу вверх: z' = 2*wall_z - z.
        glTranslatef(0, 0, wall_z)
        glScalef(1, 1, -1)
        glTranslatef(0, 0, -wall_z)
        draw_audience()
        glPopMatrix()

    # Одна доска обозначает плоскость отражения. Прозрачной стены нет.
    glPushMatrix()
    glTranslatef(0, 3, wall_z)
    draw_box(4.5, 1.5, 0.12, (0.08, 0.28, 0.17))
    glPopMatrix()
    glutSwapBuffers()


# Принимает новые размеры окна в пикселях и обновляет область рисования.
# Ничего не возвращает; проекция пересчитывается в display.
def reshape(new_width, new_height):
    global width, height
    width, height = max(new_width, 1), max(new_height, 1)
    glViewport(0, 0, width, height)
    glutPostRedisplay()


# Обрабатывает клавишу key (bytes). x, y — координаты мыши, не используются.
# Меняет проекцию, камеру, обрезание или отражение; ничего не возвращает.
def keyboard(key, x, y):
    global projection, camera_distance, show_reflection, clipping
    key = key.lower()
    if key in (b"1", b"2", b"3"):
        projection = int(key)
    elif key == b"w":
        camera_distance = max(8, camera_distance - 2)
    elif key == b"s":
        camera_distance = min(90, camera_distance + 2)
    elif key == b"c":
        clipping = not clipping
    elif key == b"m":
        show_reflection = not show_reflection
        camera_distance = 34 if show_reflection else 24
    elif key == b"\x1b":
        glutLeaveMainLoop()
        return
    glutPostRedisplay()


# Сначала создаём окно и контекст OpenGL, затем разрешаем рисование.
if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Lab 3 | 1/2/3: projection | W/S: camera | C: clipping | M: mirror")
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)
    glClearColor(0.12, 0.17, 0.23, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    # Масштабируем кубы и отражаем сцену: нормали должны иметь длину 1.
    glEnable(GL_NORMALIZE)
    # Отражение меняет порядок вершин, поэтому обратные грани не удаляем.
    glDisable(GL_CULL_FACE)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    print("1/2/3: проекции; W/S: камера; C: обрезание; M: отражение; Esc: выход.")
    print("Используй английскую раскладку. Новая расстановка — при новом запуске.")
    glutMainLoop()
