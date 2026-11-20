from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef

from objects import TABLE_TOP, GLOBE_RADIUS, draw_surface, draw_table, draw_sphere

GLOBE_X = -0.7
MIRROR_X = 0.7


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


# Рисует стол и две сферы одинакового радиуса, касающиеся столешницы.
# textures — номера текстур; with_mirror=False скрывает зеркальную сферу.
def draw_scene(textures):
    draw_room(textures)
    draw_table(textures["wood"])

    glPushMatrix()
    glTranslatef(GLOBE_X, TABLE_TOP + GLOBE_RADIUS, 0)
    draw_sphere(GLOBE_RADIUS, textures["earth"])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(MIRROR_X, TABLE_TOP + GLOBE_RADIUS, 0)
    draw_sphere(GLOBE_RADIUS, textures["mirror"], mirror=True)
    
