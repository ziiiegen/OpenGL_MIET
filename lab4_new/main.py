from OpenGL import GLUT

from scene import draw_mirror, draw_scene, prepare_frame, setup_lighting
from textures import load_scene_textures, load_texture

textures = {}


# Рисует один кадр из основной камеры и показывает его в окне.
def display():
    width = GLUT.glutGet(GLUT.GLUT_WINDOW_WIDTH)
    height = GLUT.glutGet(GLUT.GLUT_WINDOW_HEIGHT)
    prepare_frame(width, height, eye=(3.7, 4.3, 5.3), target=(0, 1.6, 0), fov=45)
    draw_scene(textures)
    draw_mirror(textures["mirror"])
    GLUT.glutSwapBuffers()


# Создаёт окно, загружает текстуры и передаёт GLUT функцию отрисовки.
def main():
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(1000, 750)
    GLUT.glutCreateWindow(b"Lab 4 - Textures")

    setup_lighting()
    textures.update(load_scene_textures())
    textures["mirror"] = load_texture("environment.png")

    GLUT.glutDisplayFunc(display)
    GLUT.glutMainLoop()


if __name__ == "__main__":
    main()
