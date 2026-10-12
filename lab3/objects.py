# Объекты для лабораторной работы 3.

import math
import random

from OpenGL.GL import (
    glColor3f,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glScalef,
    glTranslatef,
)
from OpenGL.GLUT import (
    glutSolidCone,
    glutSolidCube,
    glutSolidCylinder,
    glutSolidTeapot,
)


# Размеры вдоль X, Y и Z измеряются в условных единицах сцены.
TABLE_WIDTH = 3.0
TABLE_DEPTH = 1.8
TABLE_HEIGHT = 1.4       # Высота верхней поверхности столешницы.
TABLE_TOP_THICKNESS = 0.12
TABLE_LEG_THICKNESS = 0.14

BOOK_WIDTH = 0.62
BOOK_HEIGHT = 0.14
BOOK_DEPTH = 0.44

PEN_LENGTH = 0.8
PEN_RADIUS = 0.025

TEAPOT_SIZE = 0.25

# Мысленно окружаем каждый предмет кругом на столешнице.
# Радиус круга не меняется при повороте предмета вокруг оси Y.
# Для книги берём половину диагонали, для ручки — радиус охватывающего круга.
# Для чайника оставляем запас, учитывающий носик и ручку.
OBJECT_RADII = {
    "book": math.hypot(BOOK_WIDTH / 2, BOOK_DEPTH / 2),
    "pen": math.hypot(PEN_LENGTH / 2, PEN_RADIUS),
    "teapot": 2.0 * TEAPOT_SIZE,
}


# Рисует параллелепипед с центром в начале координат.
# width, height, depth — его размеры по осям X, Y, Z.
def draw_box(width, height, depth):
    # Сохраняем матрицу, чтобы масштаб не изменил следующие объекты.
    glPushMatrix()
    glScalef(width, height, depth)
    glutSolidCube(1.0)
    glPopMatrix()


# Рисует стол из столешницы и четырёх ножек.
def draw_table():
    glColor3f(0.35, 0.20, 0.10)
    glPushMatrix()
    # Куб имеет центр посередине: вычитаем половину толщины столешницы,
    # чтобы её верхняя поверхность оказалась на высоте TABLE_HEIGHT.
    glTranslatef(0.0, TABLE_HEIGHT - TABLE_TOP_THICKNESS / 2, 0.0)
    draw_box(TABLE_WIDTH, TABLE_TOP_THICKNESS, TABLE_DEPTH)
    glPopMatrix()

    leg_height = TABLE_HEIGHT - TABLE_TOP_THICKNESS
    leg_x = TABLE_WIDTH / 2 - TABLE_LEG_THICKNESS
    leg_z = TABLE_DEPTH / 2 - TABLE_LEG_THICKNESS

    glColor3f(0.35, 0.20, 0.10)
    # Два положения по X и два по Z дают четыре ножки по углам.
    for x in (-leg_x, leg_x):
        for z in (-leg_z, leg_z):
            glPushMatrix()
            glTranslatef(x, leg_height / 2, z)
            draw_box(TABLE_LEG_THICKNESS, leg_height, TABLE_LEG_THICKNESS)
            glPopMatrix()


# Рисует лежащую книгу как растянутый куб.
# color — сохранённый цвет (красный, зелёный, синий), компоненты от 0 до 1.
# Нижняя поверхность находится на Y = 0; ничего не возвращает.
def draw_book(color=(0.75, 0.12, 0.12)):
    glColor3f(*color)
    glPushMatrix()
    glTranslatef(0.0, BOOK_HEIGHT / 2, 0.0)
    draw_box(BOOK_WIDTH, BOOK_HEIGHT, BOOK_DEPTH)
    glPopMatrix()


# Рисует лежащую ручку: цилиндр и маленький конус на конце.
# Ручка лежит вдоль оси X и касается плоскости Y = 0.
def draw_pen():
    tip_length = PEN_LENGTH * 0.12
    body_length = PEN_LENGTH - tip_length

    glPushMatrix()
    # Цилиндр freeglut начинается в Z = 0 и направлен вдоль положительной Z.
    # Поворот переводит его ось в X; перенос центрирует всю ручку по X
    # и поднимает её ось на радиус, чтобы ручка лежала на поверхности.
    glTranslatef(-PEN_LENGTH / 2, PEN_RADIUS, 0.0)
    glRotatef(90.0, 0.0, 1.0, 0.0)
    glColor3f(0.40, 0.40, 0.80)
    glutSolidCylinder(PEN_RADIUS, body_length, 24, 1)

    # После поворота локальная ось Z направлена вдоль ручки.
    glTranslatef(0.0, 0.0, body_length)
    glColor3f(0.18, 0.18, 0.18)
    glutSolidCone(PEN_RADIUS, tip_length, 24, 1)
    glPopMatrix()


# Рисует готовый чайник freeglut размера TEAPOT_SIZE.
# Параметров нет, ничего не возвращает; основание находится на Y = 0.
def draw_teapot():
    glColor3f(0.15, 0.65, 0.35)
    glPushMatrix()
    # В freeglut дно модели находится на Y = -0.7875 * size.
    # Компенсируем это смещение, чтобы поставить чайник на поверхность.
    glTranslatef(0.0, 0.7875 * TEAPOT_SIZE, 0.0)
    glutSolidTeapot(TEAPOT_SIZE)
    glPopMatrix()


# Создаёт случайную расстановку книги, ручки и чайника на столе.
# Возвращает словарь: имя предмета -> (x, z, угол в градусах).
# Вызывать один раз при создании стола, а не при каждом рисовании кадра.
def create_random_layout():
    gap = 0.05  # Небольшой промежуток между охватывающими кругами.
    pairs = (("book", "pen"), ("book", "teapot"), ("pen", "teapot"))

    for name, radius in OBJECT_RADII.items():
        if 2 * radius > min(TABLE_WIDTH, TABLE_DEPTH):
            raise ValueError("Предмет слишком большой для этой столешницы.")

    # Пробуем расстановку целиком: иначе два первых предмета иногда
    # занимают места так, что третьему уже негде поместиться.
    for attempt in range(1000):
        layout = {}
        for name, radius in OBJECT_RADII.items():
            x = random.uniform(-TABLE_WIDTH / 2 + radius, TABLE_WIDTH / 2 - radius)
            z = random.uniform(-TABLE_DEPTH / 2 + radius, TABLE_DEPTH / 2 - radius)
            angle = random.uniform(0.0, 360.0)
            layout[name] = (x, z, angle)

        intersects = False
        for first, second in pairs:
            x1, z1, angle1 = layout[first]
            x2, z2, angle2 = layout[second]
            distance = math.hypot(x1 - x2, z1 - z2)
            # Круги пересекаются, если центры ближе суммы радиусов.
            if distance < OBJECT_RADII[first] + OBJECT_RADII[second] + gap:
                intersects = True
                break

        if not intersects:
            return layout

    raise RuntimeError("Не удалось разместить предметы. Увеличь размеры стола.")


# Рисует стол с книгой, ручкой и чайником, используя сохранённую расстановку.
# layout — результат create_random_layout(), book_color — цвет этой книги.
# Ничего не возвращает.
# Все предметы поднимаются на TABLE_HEIGHT и поворачиваются вокруг оси Y.
def draw_table_with_objects(layout, book_color=(0.75, 0.12, 0.12)):
    draw_table()

    drawing_functions = {
        "book": draw_book,
        "pen": draw_pen,
        "teapot": draw_teapot,
    }

    for name, draw_object in drawing_functions.items():
        x, z, angle = layout[name]
        glPushMatrix()
        glTranslatef(x, TABLE_HEIGHT, z)
        glRotatef(angle, 0.0, 1.0, 0.0)
        if name == "book":
            draw_book(book_color)
        else:
            draw_object()
        # Возвращаем матрицу: размещение одного предмета не влияет на другой.
        glPopMatrix()

