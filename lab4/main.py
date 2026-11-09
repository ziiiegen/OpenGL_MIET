from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_NORMALIZE,
    GL_LIGHTING, GL_LIGHT0, GL_AMBIENT, GL_DIFFUSE, GL_POSITION,
    GL_COLOR_MATERIAL, GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE,
    GL_PROJECTION, GL_MODELVIEW,
    GL_TEXTURE_2D, GL_RGB, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER,
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_LINEAR, GL_CLAMP_TO_EDGE,
    glClearColor, glClear, glEnable, glLightfv, glColorMaterial,
    glMatrixMode, glLoadIdentity, glViewport, glFrustum,
    glGenTextures, glBindTexture, glTexParameteri, glCopyTexImage2D,
)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import (
    GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH,
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutCreateWindow,
    glutDisplayFunc, glutReshapeFunc,
    glutPostRedisplay, glutSwapBuffers, glutMainLoop,
)
from textures import load_texture
from scene import (
    draw_scene, MIRROR_Z, MIRROR_LEFT, MIRROR_RIGHT, MIRROR_BOTTOM, MIRROR_TOP,
)

width, height = 1000, 750
textures = {}
camera_x, camera_y, camera_z = 3.7, 4.3, 5.3


# Рисует сцену из-за зеркала и копирует кадр в текстуру. Параметров нет.
def update_reflection():
    size = min(768, width, height)
    glViewport(0, 0, size, size)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # Отражаем положение глаза относительно плоскости z = MIRROR_Z.
    reflected_z = 2 * MIRROR_Z - camera_z
    near = MIRROR_Z - reflected_z
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Границы видимости совпадают с краями зеркала.
    # Взгляд из-за стены направлен вдоль +Z, поэтому правая ось камеры — это -X.
    glFrustum(camera_x - MIRROR_RIGHT, camera_x - MIRROR_LEFT,
              MIRROR_BOTTOM - camera_y, MIRROR_TOP - camera_y, near, 60)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(camera_x, camera_y, reflected_z,
              camera_x, camera_y, MIRROR_Z, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (-3, 6, 4, 1))
    draw_scene(textures, with_mirror=False)
    glBindTexture(GL_TEXTURE_2D, textures["mirror"])
    glCopyTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, 0, 0, size, size, 0)


# Рисует кадр: задаёт перспективу, камеру, свет и вызывает отрисовку сцены.
def display():
    update_reflection()
    glViewport(0, 0, width, height)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 60)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(camera_x, camera_y, camera_z, 0, 1.6, 0, 0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (-3, 6, 4, 1))
    draw_scene(textures)
    glutSwapBuffers()


# Обновляет размеры окна w, h и область вывода; ничего не возвращает.
def reshape(w, h):
    global width, height
    width, height = max(w, 1), max(h, 1)
    glViewport(0, 0, width, height)
    glutPostRedisplay()


# Создаёт окно, настраивает освещение, загружает текстуры и запускает GLUT.
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Lab 4 - Textures")
    glClearColor(0.84, 0.87, 0.88, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.35, 0.35, 0.35, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.80, 0.80, 0.80, 1))
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    textures["wood"] = load_texture("wood.png", repeat=True)
    textures["earth"] = load_texture("earth.png")
    textures["floor"] = load_texture("floor.png", repeat=True)
    textures["wall"] = load_texture("wall.png", repeat=True)
    # У отражения нет PNG: место под картинку заполнится при отрисовке кадра.
    textures["mirror"] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textures["mirror"])
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutMainLoop()


if __name__ == "__main__":
    main()
