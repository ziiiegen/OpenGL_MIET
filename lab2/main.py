from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_NORMALIZE,
    GL_LIGHTING, GL_LIGHT0, GL_AMBIENT, GL_DIFFUSE, GL_SPECULAR, GL_POSITION,
    GL_LIGHT_MODEL_AMBIENT, GL_LIGHT_MODEL_LOCAL_VIEWER, GL_PROJECTION,
    GL_MODELVIEW, GL_SMOOTH, GL_FLAT, glClearColor, glClear, glEnable,
    glMatrixMode, glLoadIdentity, glLightfv, glLightModelfv, glLightModeli,
    glShadeModel, glTranslatef, glRotatef, glViewport,
)
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL.GLUT import (
    GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH, GLUT_LEFT_BUTTON, GLUT_DOWN,
    glutInit, glutInitDisplayMode, glutInitWindowSize, glutCreateWindow,
    glutDisplayFunc, glutReshapeFunc, glutKeyboardFunc, glutMouseFunc,
    glutMotionFunc, glutSwapBuffers, glutPostRedisplay, glutMainLoop,
)
from scene import draw_scene

width, height = 1100, 700
mode = 4
ambient = False
local_viewer = True
emission = False
smooth = True
grid = False
angle_x, angle_y = 0, 0
dragging = False
mouse_x, mouse_y = 0, 0


# Рисует сцену с текущими настройками света, материала и сетки. Параметров нет.
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40, width / height, 0.5, 50)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(1.8, 6, 6, 0, 1, 0, 0, 1, 0)

    white, black = (1, 1, 1, 1), (0, 0, 0, 1)
    # Свет задаём до вращения предметов: источник остаётся неподвижным в мире.
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 6, 6, 1))
    glLightfv(GL_LIGHT0, GL_AMBIENT, black)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, white if mode in (2, 4) else black)
    glLightfv(GL_LIGHT0, GL_SPECULAR, white if mode in (1, 3) else black)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, (0.25, 0.25, 0.25, 1) if ambient else black)
    glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, local_viewer)
    glShadeModel(GL_SMOOTH if smooth else GL_FLAT)

    # Вращаем оба стола вокруг точки (0, 1, 0).
    glTranslatef(0, 1, 0)
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glTranslatef(0, -1, 0)
    draw_scene(mode, emission, 4 if grid else 1)
    glutSwapBuffers()


# Обрабатывает новые размеры окна w и h в пикселях.
def reshape(w, h):
    global width, height
    width, height = max(w, 1), max(h, 1)
    glViewport(0, 0, width, height)
    glutPostRedisplay()


# Переключает только режимы из задания; key — клавиша, x и y здесь не используются.
def keyboard(key, x, y):
    global mode, ambient, local_viewer, emission, smooth, grid
    key = key.lower()
    if key in (b"1", b"2", b"3", b"4"):
        mode = int(key)
        print("Режим материала и света:", mode)
    elif key == b"a":
        ambient = not ambient
        print("Глобальный фоновый свет:", ambient)
    elif key == b"l":
        local_viewer = not local_viewer
        print("Локальный наблюдатель:", local_viewer)
    elif key == b"e":
        emission = not emission
        print("Свечение материала:", emission)
    elif key == b"f":
        smooth = not smooth
        print("Плавное закрашивание:", smooth)
    elif key == b"g":
        grid = not grid
        print("Разбиение граней на сетку:", grid)
    glutPostRedisplay()


# Запоминает нажатие левой кнопки и начальные координаты мыши x, y.
def mouse(button, state, x, y):
    global dragging, mouse_x, mouse_y
    if button == GLUT_LEFT_BUTTON:
        dragging = state == GLUT_DOWN
        mouse_x, mouse_y = x, y


# При перетаскивании мыши в точку (x, y) изменяет углы вращения сцены.
def motion(x, y):
    global angle_x, angle_y, mouse_x, mouse_y
    if dragging:
        angle_y += (x - mouse_x) * 0.5
        angle_x += (y - mouse_y) * 0.5
        mouse_x, mouse_y = x, y
        glutPostRedisplay()


# Создаёт окно и регистрирует функции отрисовки, клавиатуры и мыши.
def main():
    glutInit()  # Подготовка GLUT.
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)
    glutCreateWindow(b"Lab 2")
    glClearColor(0.35, 0.35, 0.35, 1)
    glEnable(GL_DEPTH_TEST)  # Ближние поверхности закрывают дальние.
    glEnable(GL_NORMALIZE)  # Нормализуем нормали после масштабирования кубов.
    glEnable(GL_LIGHTING)  # Включаем расчёт освещения.
    glEnable(GL_LIGHT0)  # Включаем один источник света.
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutMotionFunc(motion)
    print("Слева: нормали к граням. Справа: нормали от центра исходного куба.")
    print("Старт: режим 4, локальный наблюдатель, GL_SMOOTH; A, E, G выключены.")
    glutMainLoop()


if __name__ == "__main__":
    main()
