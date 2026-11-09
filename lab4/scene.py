from OpenGL.GL import (
    GL_LIGHTING, glColor3f, glPushMatrix, glPopMatrix, glTranslatef,
    glDisable, glEnable,
)

from objects import TABLE_TOP, GLOBE_RADIUS, draw_box, draw_surface, draw_table, draw_sphere

MIRROR_Z = -2.94
MIRROR_LEFT, MIRROR_RIGHT = -2.8, 2.8
MIRROR_BOTTOM, MIRROR_TOP = 0.5, 4.4


# Рисует пол и две стены; textures содержит номера их текстур.
def draw_room(textures):
    draw_surface(textures["floor"],
                 ((-4, 0, 4), (4, 0, 4), (4, 0, -3), (-4, 0, -3)),
                 (0, 1, 0), 4, 3.5)
    draw_surface(textures["wall"],
                 ((-4, 0, -3), (4, 0, -3), (4, 5, -3), (-4, 5, -3)),
                 (0, 0, 1), 4, 2.5)
    draw_surface(textures["wall"],
                 ((-4, 0, 4), (-4, 0, -3), (-4, 5, -3), (-4, 5, 4)),
                 (1, 0, 0), 3.5, 2.5)


# Рисует большое зеркало с тонкой рамкой; texture — кадр отражённой сцены.
def draw_mirror(texture):
    glColor3f(0.25, 0.22, 0.18)
    draw_box(0, 2.45, -2.98, (5.8, 4.1, 0.04))
    # Картинка отражения уже освещена, повторный расчёт света не нужен.
    glDisable(GL_LIGHTING)
    # Правая сторона зеркала соответствует левому краю отражённого кадра.
    draw_surface(texture,
                 ((MIRROR_RIGHT, MIRROR_BOTTOM, MIRROR_Z),
                  (MIRROR_LEFT, MIRROR_BOTTOM, MIRROR_Z),
                  (MIRROR_LEFT, MIRROR_TOP, MIRROR_Z),
                  (MIRROR_RIGHT, MIRROR_TOP, MIRROR_Z)), (0, 0, 1))
    glEnable(GL_LIGHTING)


# Рисует стол и сферу, касающуюся столешницы, без подставки.
# textures — номера текстур; with_mirror=False исключает зеркало из отражения.
def draw_scene(textures, with_mirror=True):
    draw_room(textures)
    draw_table(textures["wood"])
    glPushMatrix()
    # Расстояние от центра до нижней точки сферы равно её радиусу.
    glTranslatef(0, TABLE_TOP + 0.001 + GLOBE_RADIUS, 0)
    draw_sphere(GLOBE_RADIUS, textures["earth"])
    glPopMatrix()
    if with_mirror:
        draw_mirror(textures["mirror"])
