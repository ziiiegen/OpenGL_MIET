from pathlib import Path
from PIL import Image

from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_NORMALIZE,
    GL_LIGHTING, GL_LIGHT0, GL_AMBIENT, GL_DIFFUSE, GL_POSITION,
    GL_COLOR_MATERIAL, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    GL_PROJECTION, GL_MODELVIEW, GL_BACK, GL_PACK_ALIGNMENT, GL_RGB, GL_UNSIGNED_BYTE,
    glClearColor, glClear, glEnable, glLightfv, glColorMaterial,
    glMatrixMode, glLoadIdentity, glViewport, glReadBuffer, glPixelStorei, glReadPixels,
)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import (
    GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH, glutInit, glutInitDisplayMode,
    glutInitWindowSize, glutCreateWindow, glutHideWindow, glutDestroyWindow,
)
from objects import TABLE_TOP, GLOBE_RADIUS
from scene import MIRROR_X, draw_scene
from textures import load_texture


# Делает один снимок из края зеркального шара в сторону задней стены.
# Сохраняет environment.png 
def main():
    size = 256
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(size, size)
    window = glutCreateWindow(b"Making environment.png")
    glutHideWindow()
    glClearColor(0.6, 0.6, 0.6, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.35, 0.35, 0.35, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.80, 0.80, 0.80, 1))
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    textures = {
        "wood": load_texture("wood.png", repeat=True),
        "earth": load_texture("earth.png"),
        "floor": load_texture("floor.png", repeat=True),
        "wall": load_texture("wall.png", repeat=True),
    }

    glViewport(0, 0, size, size)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 0.03, 60)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    x, y, z = MIRROR_X, TABLE_TOP + 0.001 + GLOBE_RADIUS, GLOBE_RADIUS
    gluLookAt(x, y, z, x, y, z - 1, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (-3, 6, 4, 1))
    draw_scene(textures, with_mirror=False)

    # Читаем готовый кадр и переворачиваем строки для сохранения обычной PNG.
    glReadBuffer(GL_BACK)
    glPixelStorei(GL_PACK_ALIGNMENT, 1)
    pixels = bytes(glReadPixels(0, 0, size, size, GL_RGB, GL_UNSIGNED_BYTE))
    image = Image.frombytes("RGB", (size, size), pixels)
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    path = Path(__file__).parent / "textures" / "environment.png"
    image.save(path)
    glutDestroyWindow(window)
    print("Создана текстура:", path)


if __name__ == "__main__":
    main()
