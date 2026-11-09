from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT, GL_DEPTH_TEST, GL_NORMALIZE,
    GL_LIGHTING, GL_LIGHT0, GL_AMBIENT, GL_POSITION, GL_COLOR_MATERIAL,
    GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, GL_PROJECTION, GL_MODELVIEW,
    glClearColor, glClear, glEnable, glLightfv, glColorMaterial,
    glMatrixMode, glLoadIdentity, glOrtho, glFrustum, glViewport,
)
from OpenGL.GLU import gluPerspective, gluLookAt
from OpenGL.GLUT import (
    GLUT_DOUBLE, GLUT_RGB, GLUT_DEPTH, glutInit, glutInitDisplayMode,
    glutInitWindowSize, glutCreateWindow, glutDisplayFunc, glutReshapeFunc,
    glutKeyboardFunc, glutPostRedisplay, glutSwapBuffers, glutMainLoop,
)
from scene import draw_scene

width, height = 1000, 700
projection = 2
clipping = False
distance = 32


# Рисует кадр с выбранной проекцией и положением камеры. Параметров нет.
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    aspect = width / height
    far = distance if clipping else 120  # Уменьшение far обрезает дальнюю часть сцены.

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if projection == 1:
        glOrtho(-20 * aspect, 20 * aspect, -20, 20, 1, far)
    elif projection == 2:
        gluPerspective(50, aspect, 1, far)
    else:
        glFrustum(-0.5 * aspect, 0.5 * aspect, -0.5, 0.5, 1, far)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Меняем положение глаза вдоль одного направления, сохраняя точку наблюдения.
    gluLookAt(distance,  distance, distance,
              4.5, 2, 0, 
              0, 1, 0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0, 1, 0, 0))  # Направленный свет сверху.
    draw_scene()
    glutSwapBuffers()


# Обновляет область вывода при изменении окна; w и h — размеры в пикселях.
def reshape(w, h):
    global width, height
    width, height = max(w, 1), max(h, 1)
    glViewport(0, 0, width, height)
    glutPostRedisplay()


# Меняет проекцию, обрезание или расстояние камеры по клавише key; x и y не нужны.
def keyboard(key, x, y):
    global projection, clipping, distance
    key = key.lower()
    if key in (b"1", b"2", b"3"):
        projection = int(key)
    elif key == b"c":
        clipping = not clipping
    elif key == b"w":
        distance = max(2, distance - 2)
    elif key == b"s":
        distance = min(64, distance + 2)
    glutPostRedisplay()


# Создаёт окно, включает простое освещение и запускает обработку событий GLUT.
def main():
    glutInit()  # Подготавливает библиотеку GLUT к работе.
    # Два буфера изображения, цвета RGB и буфер глубины.
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(width, height)  # Начальный размер окна в пикселях.
    glutCreateWindow(b"Lab 3")  # Создаёт окно с заголовком
    glClearColor(0.5, 0.5, 0.5, 0.5)  # Цвет очистки фона: R, G, B, альфа.
    glEnable(GL_DEPTH_TEST)  # Ближние поверхности перекрывают дальние.
    glEnable(GL_NORMALIZE)  # Делает длину нормалей равной 1 после масштабирования.
    glEnable(GL_LIGHTING)  # Включает расчёт освещения объектов.
    glEnable(GL_LIGHT0)  # Включает источник света номер 0.
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.35, 0.2, 0.2, 1))  # Его фоновый свет.
    glEnable(GL_COLOR_MATERIAL)  # Позволяет менять цвет материала через glColor.
    # glColor задаёт фоновый и рассеянный цвет материала обеих сторон граней.
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glutDisplayFunc(display)  # Назначает display функцией отрисовки окна.
    glutReshapeFunc(reshape)  # Назначает reshape обработчиком изменения размеров окна.
    glutKeyboardFunc(keyboard)  # Назначает keyboard обработчиком нажатий клавиш.
    glutMainLoop()  # Запускает цикл событий и вызывает назначенные обработчики.


if __name__ == "__main__":
    main()
