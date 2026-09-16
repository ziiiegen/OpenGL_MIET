import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def display():
    # Очищаем цветовой буфер и буфер глубины
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Матрица модели и камеры
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Положение камеры:
    # камера (4, 3, 6), смотрит в (0, 0, 0), вертикаль — ось Y
    gluLookAt(
        4.0, 3.0, 6.0,
        0.0, 0.0, 0.0,
        0.0, 1.0, 0.0
    )

    # Цвет куба
    glColor3f(0.2, 0.6, 1.0)

    # Куб со стороной 2
    glutSolidCube(2.0)

    # Показываем готовый кадр
    glutSwapBuffers()


def reshape(width, height):
    # Защита от деления на ноль
    if height == 0:
        height = 1

    # Область окна, в которой рисует OpenGL
    glViewport(0, 0, width, height)

    # Настраиваем перспективную проекцию
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(
        45.0,          # угол обзора
        width / height,
        0.1,           # ближняя плоскость отсечения
        100.0          # дальняя плоскость отсечения
    )

    glMatrixMode(GL_MODELVIEW)


def keyboard(key, x, y):
    # Escape закрывает программу
    if key == b'\x1b':
        glutLeaveMainLoop()


def init():
    # Цвет фона
    glClearColor(0.1, 0.1, 0.1, 1.0)

    # Включаем проверку глубины
    glEnable(GL_DEPTH_TEST)


def main():
    glutInit(sys.argv)

    # Двойная буферизация, цвет RGB и буфер глубины
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(800, 600)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b"OpenGL laboratory")

    init()

    # Регистрируем функции обработки событий
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    # Запускаем цикл приложения
    glutMainLoop()


if __name__ == "__main__":
    main()