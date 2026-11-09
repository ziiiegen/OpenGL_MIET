from OpenGL.GL import glPushMatrix, glPopMatrix, glTranslatef
from objects import draw_table


# Рисует два стола
def draw_scene(mode, emission, parts):
    for x, radial in ((-1.8, False), (1.8, True)):
        glPushMatrix()
        glTranslatef(x, 0, 0)
        draw_table(radial, parts, mode, emission)
        glPopMatrix()
