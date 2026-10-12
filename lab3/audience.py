# Аудитория для лабораторной работы 3: три ряда по четыре стола.
# Положение и цвет предметов создаём отдельно от рисования.

import random

from OpenGL.GL import *

from objects import TABLE_DEPTH, TABLE_WIDTH, create_random_layout, draw_box, draw_table_with_objects


ROW_COUNT = 3
TABLES_PER_ROW = 4
STEP_X = TABLE_WIDTH + 1.0   # Расстояние между центрами соседних столов.
STEP_Z = TABLE_DEPTH + 1.3

ROOM_WIDTH = TABLES_PER_ROW * STEP_X + 1.0
ROOM_DEPTH = ROW_COUNT * STEP_Z + 2.7
WALL_Z = -ROOM_DEPTH / 2
WALL_HEIGHT = 4.5


# Создаёт данные для всех 12 столов, ничего не рисует.
# Параметров нет. Возвращает список (x, z, расстановка предметов, цвет книги).
def create_audience():
    tables = []
    for row in range(ROW_COUNT):
        for column in range(TABLES_PER_ROW):
            # Вычитаем половину числа промежутков, чтобы центр сетки был в (0, 0).
            x = (column - (TABLES_PER_ROW - 1) / 2) * STEP_X
            z = (row - (ROW_COUNT - 1) / 2) * STEP_Z
            layout = create_random_layout()
            book_color = (random.random(), random.random(), random.random())
            tables.append((x, z, layout, book_color))
    return tables


# Рисует пол и три ряда по четыре стола в сохранённых положениях.
# tables — результат create_audience(); ничего не возвращает.
# Стену рисуем отдельно, чтобы она не закрывала отражение.
def draw_audience(tables):
    glColor3f(0.62, 0.60, 0.54)
    glPushMatrix()
    # Верх пола находится на Y = 0, как и нижние концы ножек столов.
    glTranslatef(0.0, -0.05, 0.0)
    draw_box(ROOM_WIDTH, 0.1, ROOM_DEPTH)
    glPopMatrix()

    for x, z, layout, book_color in tables:
        glPushMatrix()
        glTranslatef(x, 0.0, z)
        draw_table_with_objects(layout, book_color)
        glPopMatrix()


# Рисует зеркальную копию аудитории относительно стены Z = WALL_Z.
# tables — те же данные, что и для оригинала; ничего не возвращает.
def draw_reflection(tables):
    glPushMatrix()
    # Матрицы применяются к вершине справа налево:
    # 1) переносим стену в Z = 0; 2) меняем знак Z; 3) возвращаем стену.
    # В результате z' = WALL_Z - (z - WALL_Z) = 2 * WALL_Z - z.
    glTranslatef(0.0, 0.0, WALL_Z)
    glScalef(1.0, 1.0, -1.0)
    glTranslatef(0.0, 0.0, -WALL_Z)
    draw_audience(tables)
    glPopMatrix()


# Рисует полупрозрачную стену и доску на её плоскости.
# Параметров нет, ничего не возвращает. Вызывать после обеих аудиторий.
def draw_board_wall():
    half_width = ROOM_WIDTH / 2

    # Стена прозрачна, чтобы было видно отражение за ней.
    # Проверку глубины сохраняем: настоящие столы перед стеной закрывают её.
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)
    glColor4f(0.55, 0.75, 0.95, 0.18)
    glBegin(GL_QUADS)
    glVertex3f(-half_width, 0.0, WALL_Z)
    glVertex3f(half_width, 0.0, WALL_Z)
    glVertex3f(half_width, WALL_HEIGHT, WALL_Z)
    glVertex3f(-half_width, WALL_HEIGHT, WALL_Z)
    glEnd()
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)

    # Контур обозначает плоскость, относительно которой выполнено отражение.
    glColor3f(1.0, 0.75, 0.25)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-half_width, 0.0, WALL_Z)
    glVertex3f(half_width, 0.0, WALL_Z)
    glVertex3f(half_width, WALL_HEIGHT, WALL_Z)
    glVertex3f(-half_width, WALL_HEIGHT, WALL_Z)
    glEnd()
    glLineWidth(1.0)
    glEnable(GL_LIGHTING)

    # Рамка и сама доска — два тонких параллелепипеда.
    glColor3f(0.30, 0.20, 0.12)
    glPushMatrix()
    glTranslatef(0.0, 3.0, WALL_Z + 0.05)
    draw_box(4.8, 1.8, 0.1)
    glPopMatrix()

    glColor3f(0.08, 0.28, 0.17)
    glPushMatrix()
    glTranslatef(0.0, 3.0, WALL_Z + 0.11)
    draw_box(4.5, 1.5, 0.02)
    glPopMatrix()
