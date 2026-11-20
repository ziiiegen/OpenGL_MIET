from OpenGL import GL as gl
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL import GLUT as glut

from effects import draw_mirror, draw_staircase


width, height = 900, 650
mode = b"3"


# Рисует кадр выбранного режима и выводит его на экран.
def display():
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT | gl.GL_STENCIL_BUFFER_BIT)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 30)

    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    if mode == b"4":
        gluLookAt(4.1, 4.4, 6.4, 0, 0.55, 0, 0, 1, 0)
        draw_staircase()
    else:
        gluLookAt(3.8, 2.8, 6.4, 0, 1.3, 0.8, 0, 1, 0)
        draw_mirror(ellipse= (mode == b"5"))

    glut.glutSwapBuffers()


# Обновляет размеры области вывода после изменения окна (w, h — в пикселях).
def reshape(w, h):
    global width, height
    width, height = max(1, w), max(1, h)
    gl.glViewport(0, 0, width, height)
    glut.glutPostRedisplay()


# Меняет режим по нажатой клавише key и запрашивает новый кадр.
def keyboard(key, x, y):
    global mode
    if key in (b"3", b"4", b"5"):
        mode = key
        glut.glutPostRedisplay()


# Создаёт окно с буферами глубины и трафарета и запускает GLUT.
def main():
    glut.glutInit()
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH | glut.GLUT_STENCIL)
    glut.glutInitWindowSize(width, height)
    glut.glutCreateWindow(b"Lab 5 - 3: Rectangle | 4: Shadow | 5: Ellipse")
    gl.glClearColor(0.8, 0.8, 0.8, 1)
    gl.glEnable(gl.GL_DEPTH_TEST)
    glut.glutDisplayFunc(display)
    glut.glutReshapeFunc(reshape)
    glut.glutKeyboardFunc(keyboard)
    glut.glutMainLoop()


if __name__ == "__main__":
    main()
