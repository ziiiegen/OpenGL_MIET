import math

from OpenGL.GL import (
    GL_QUADS, GL_FRONT_AND_BACK, GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR,
    GL_SHININESS, GL_EMISSION, glBegin, glEnd, glNormal3f, glVertex3f,
    glPushMatrix, glPopMatrix, glTranslatef, glScalef,
    glMaterialfv, glMaterialf,
)
# Восемь углов куба со стороной 1 и центром (0, 0, 0).
VERTICES = [
    (-0.5, -0.5, -0.5),  # 0
    (0.5, -0.5, -0.5),   # 1
    (0.5, 0.5, -0.5),    # 2
    (-0.5, 0.5, -0.5),   # 3
    (-0.5, -0.5, 0.5),   # 4
    (0.5, -0.5, 0.5),    # 5
    (0.5, 0.5, 0.5),     # 6
    (-0.5, 0.5, 0.5),    # 7
]
# Каждая запись: (четыре индекса из VERTICES, внешняя нормаль грани).
# Обход против часовой стрелки, если смотреть на грань снаружи куба.
FACES = [
    ((4, 5, 6, 7), (0, 0, 1)),   # Передняя грань, нормаль вдоль +Z.
    ((1, 0, 3, 2), (0, 0, -1)),  # Задняя грань, нормаль вдоль -Z.
    ((5, 1, 2, 6), (1, 0, 0)),   # Правая грань, нормаль вдоль +X.
    ((0, 4, 7, 3), (-1, 0, 0)),  # Левая грань, нормаль вдоль -X.
    ((7, 6, 2, 3), (0, 1, 0)),   # Верхняя грань, нормаль вдоль +Y.
    ((0, 1, 5, 4), (0, -1, 0)),  # Нижняя грань, нормаль вдоль -Y.
]


# Возвращает вектор vector, приведённый к длине 1. Здесь все векторы ненулевые.
def normalize(vector):
    length = math.sqrt(sum(value * value for value in vector))
    return tuple(value / length for value in vector)


# Возвращает взвешенную сумму четырёх векторов values; u и v меняются от 0 до 1.
# Этой формулой находим и положение вершины сетки, и её промежуточную нормаль.
def interpolate(values, u, v):
    weights = ((1 - u) * (1 - v), u * (1 - v), u * v, (1 - u) * v)
    return tuple(sum(weights[k] * values[k][axis] for k in range(4))
                 for axis in range(3))


# Рисует параллелепипед с центром (x, y, z) и размерами size.
# radial выбирает нормали от центра куба; parts — число делений ребра для сетки.
def draw_box(x, y, z, size, radial, parts):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(*size)
    glBegin(GL_QUADS)
    for indices, face_normal in FACES:
        corners = [VERTICES[k] for k in indices]
        if radial:
            normals = [normalize(point) for point in corners]
        else:
            normals = [face_normal] * 4
        for i in range(parts):
            for j in range(parts):
                # Четыре угла одной ячейки сетки в координатах всей грани.
                for u, v in ((i / parts, j / parts), ((i + 1) / parts, j / parts),
                             ((i + 1) / parts, (j + 1) / parts), (i / parts, (j + 1) / parts)):
                    normal = normalize(interpolate(normals, u, v))
                    point = interpolate(corners, u, v)
                    glNormal3f(*normal)
                    glVertex3f(*point)
    glEnd()
    glPopMatrix()


# Задаёт материал цвета color: mode выбирает зеркальное или рассеянное отражение.
# emission включает собственное свечение; функция влияет на последующие детали.
def set_material(color, mode, emission):
    black = (0, 0, 0, 1)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, (*color, 1))
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, (*color, 1) if mode in (3, 4) else black)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, (1, 1, 1, 1) if mode in (1, 2) else black)
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 64)  # Чем больше, тем уже блик.
    glow = (0.5 * color[0], 0.5 * color[1], 0.5 * color[2], 1)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, glow if emission else black)


# Рисует стол; radial и parts задают нормали и сетку, mode и emission — материал.
def draw_table(radial, parts, mode, emission):
    set_material((0.65, 0.40, 0.20), mode, emission)
    draw_box(0, 1.75, 0, (2.8, 0.16, 1.8), radial, parts)
    set_material((0.30, 0.30, 0.30), mode, emission)
    for x in (-1.17, 1.17):
        for z in (-0.67, 0.67):
            draw_box(x, 0.835, z, (0.14, 1.67, 0.14), radial, parts)
