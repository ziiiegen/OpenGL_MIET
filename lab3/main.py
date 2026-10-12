# Полная лабораторная работа 3: аудитория, проекции, отсечение и отражение.
# Запускай этот файл из Python-окружения с PyOpenGL и freeglut.

import math
import sys

from OpenGL.GL import *
from OpenGL.GLU import gluLookAt, gluPerspective
from OpenGL.GLUT import *

from audience import WALL_Z, create_audience, draw_audience, draw_board_wall, draw_reflection


window_width = 1100
window_height = 760
FOV = 45.0
DISTANCE_WITH_REFLECTION = 34.0
DISTANCE_WITHOUT_REFLECTION = 24.0
PROJECTION_NAMES = {1: "glOrtho", 2: "gluPerspective", 3: "glFrustum"}

tables = create_audience()
projection_mode = 2
show_reflection = True
camera_distance = DISTANCE_WITH_REFLECTION
camera_angle = 40.0
camera_elevation = 32.0
near_plane = 0.1
far_plane = 120.0
clipping_enabled = False


# Устанавливает выбранную проекцию и границы отсечения сцены.
# Параметров нет, ничего не возвращает; использует размеры окна и near/far.
def update_projection():
    aspect = window_width / window_height
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if projection_mode == 1:
        # Параллельная проекция: размер объекта не зависит от расстояния до камеры.
        # Границы X/Y фиксированы для выбранного обзора аудитории.
        reference_distance = DISTANCE_WITH_REFLECTION if show_reflection else DISTANCE_WITHOUT_REFLECTION
        half_height = reference_distance * math.tan(math.radians(FOV / 2))
        glOrtho(-half_height * aspect, half_height * aspect,
                -half_height, half_height, near_plane, far_plane)
    elif projection_mode == 2:
        gluPerspective(FOV, aspect, near_plane, far_plane)
    else:
        # glFrustum задаёт левую, правую, нижнюю и верхнюю границы на near.
        # Выбираем их так, чтобы проекция совпадала с gluPerspective.
        top = near_plane * math.tan(math.radians(FOV / 2))
        right = top * aspect
        glFrustum(-right, right, -top, top, near_plane, far_plane)

    glMatrixMode(GL_MODELVIEW)


# Ставит камеру на заданном расстоянии от центра рассматриваемой сцены.
# Параметров нет, ничего не возвращает; W/S изменяют camera_distance.
def set_camera():
    target_z = WALL_Z if show_reflection else 0.0
    angle = math.radians(camera_angle)
    elevation = math.radians(camera_elevation)
    horizontal_distance = camera_distance * math.cos(elevation)
    eye_x = horizontal_distance * math.sin(angle)
    eye_y = 1.0 + camera_distance * math.sin(elevation)
    eye_z = target_z + horizontal_distance * math.cos(angle)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(eye_x, eye_y, eye_z, 0.0, 1.0, target_z, 0.0, 1.0, 0.0)


# Рисует строку в двумерных координатах окна.
# x и y — положение в пикселях, text — строка ASCII; ничего не возвращает.
def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for character in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(character))


# Показывает текущие параметры и подсказки управления поверх сцены.
# Параметров нет, ничего не возвращает; восстанавливает обе матрицы.
def draw_hud():
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glColor3f(0.08, 0.10, 0.14)
    glBegin(GL_QUADS)
    glVertex2f(0, window_height)
    glVertex2f(window_width, window_height)
    glVertex2f(window_width, window_height - 88)
    glVertex2f(0, window_height - 88)
    glEnd()

    glColor3f(1.0, 0.85, 0.45)
    draw_text(15, window_height - 20,
              f"{PROJECTION_NAMES[projection_mode]} | distance={camera_distance:.1f} | "
              f"near={near_plane:.1f} far={far_plane:.1f} | reflection={'ON' if show_reflection else 'OFF'}")
    glColor3f(0.95, 0.95, 0.95)
    draw_text(15, window_height - 40, "1/2/3: projection | W/S: camera closer/farther | A/D: rotate view | M: reflection")
    draw_text(15, window_height - 58, "C: clipping demo | [ / ]: near -/+ | , / .: far -/+ | N: new layout | R: reset | Esc: exit")
    draw_text(15, window_height - 76, "Clipping: " + ("ON - scene is cut by near/far planes" if clipping_enabled else "OFF - press C to cut objects"))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


# Рисует один кадр: аудиторию, её отражение, стену с доской и подсказки.
# Параметров нет, ничего не возвращает.
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    update_projection()
    set_camera()
    # Свет на плоскости стены не меняет своего положения при отражении.
    glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 8.0, WALL_Z, 1.0))

    draw_audience(tables)
    if show_reflection:
        draw_reflection(tables)
    draw_board_wall()
    draw_hud()
    glutSwapBuffers()


# Обновляет размеры окна, область рисования и проекцию.
# width и height — размеры в пикселях; ничего не возвращает.
def reshape(width, height):
    global window_width, window_height
    window_width = max(width, 1)
    window_height = max(height, 1)
    glViewport(0, 0, window_width, window_height)
    update_projection()
    glutPostRedisplay()


# Обрабатывает управление камерой, проекциями, отсечением и отражением.
# key — клавиша в виде bytes, x и y — координаты мыши, здесь не используются.
# Ничего не возвращает.
def keyboard(key, x, y):
    global projection_mode, show_reflection, camera_distance, camera_angle
    global near_plane, far_plane, clipping_enabled, tables
    key = key.lower()

    if key == b"\x1b":
        glutLeaveMainLoop()
        return
    elif key in (b"1", b"2", b"3"):
        projection_mode = int(key)
    elif key == b"w":
        camera_distance = max(8.0, camera_distance - 1.5)
    elif key == b"s":
        camera_distance = min(90.0, camera_distance + 1.5)
    elif key == b"a":
        camera_angle = (camera_angle - 5.0) % 360
    elif key == b"d":
        camera_angle = (camera_angle + 5.0) % 360
    elif key == b"m":
        show_reflection = not show_reflection
        # Новый обзор охватывает либо одну аудиторию, либо обе сразу.
        camera_distance = DISTANCE_WITH_REFLECTION if show_reflection else DISTANCE_WITHOUT_REFLECTION
        near_plane, far_plane, clipping_enabled = 0.1, 120.0, False
    elif key == b"c":
        clipping_enabled = not clipping_enabled
        if clipping_enabled:
            # Плоскости проходят через занятую объектами часть сцены.
            near_plane = max(0.1, camera_distance - 6.0)
            far_plane = camera_distance + 6.0
        else:
            near_plane, far_plane = 0.1, 120.0
    elif key == b"[":
        near_plane = max(0.1, near_plane - 1.0)
        clipping_enabled = True
    elif key == b"]":
        near_plane = min(far_plane - 0.1, near_plane + 1.0)
        clipping_enabled = True
    elif key == b",":
        far_plane = max(near_plane + 0.1, far_plane - 1.0)
        clipping_enabled = True
    elif key == b".":
        far_plane = min(200.0, far_plane + 1.0)
        clipping_enabled = True
    elif key == b"n":
        tables = create_audience()
    elif key == b"r":
        projection_mode, show_reflection = 2, True
        camera_distance, camera_angle = DISTANCE_WITH_REFLECTION, 40.0
        near_plane, far_plane, clipping_enabled = 0.1, 120.0, False

    glutPostRedisplay()


# Создаёт окно OpenGL, настраивает глубину и освещение и запускает GLUT.
# Параметров нет, ничего не возвращает.
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutCreateWindow(b"Lab 3 - Classroom and reflection")
    glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_GLUTMAINLOOP_RETURNS)

    glClearColor(0.12, 0.17, 0.23, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_NORMALIZE)
    # Отрицательный масштаб меняет порядок обхода вершин.
    # Не удаляем обратные грани, чтобы отражённые предметы тоже были видны.
    glDisable(GL_CULL_FACE)

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    reshape(window_width, window_height)
    print("Lab 3: 1/2/3 projection; W/S camera; A/D view; M reflection; C clipping.")
    print("[ / ] near; , / . far; N new layout; R reset; Esc exit. Use English keyboard layout.")
    glutMainLoop()


if __name__ == "__main__":
    main()
