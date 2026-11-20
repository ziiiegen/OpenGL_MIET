from OpenGL import GL, GLU

from objects import TABLE_TOP_Y, draw_sphere, draw_surface, draw_table

SPHERE_RADIUS = 0.67
GLOBE_CENTER = (-0.7, TABLE_TOP_Y + SPHERE_RADIUS, 0)
MIRROR_CENTER = (0.7, TABLE_TOP_Y + SPHERE_RADIUS, 0)


# Включает проверку глубины и задаёт яркость источника света.
def setup_lighting():
    GL.glClearColor(0.6, 0.6, 0.6, 1)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_NORMALIZE)  # После растяжения куба нормали снова единичные.
    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_LIGHT0)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, (0.35, 0.35, 0.35, 1))
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, (0.8, 0.8, 0.8, 1))

    # glColor3f задаёт цвет материала, который учитывается при освещении.
    GL.glEnable(GL.GL_COLOR_MATERIAL)
    GL.glColorMaterial(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT_AND_DIFFUSE)


# Очищает кадр и ставит камеру в eye. target — точка взгляда, fov — угол обзора.
def prepare_frame(width, height, eye, target, fov):
    GL.glViewport(0, 0, width, height)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(fov, width / max(height, 1), 0.1, 60)

    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    GLU.gluLookAt(*eye, *target, 0, 1, 0)  # Верх камеры направлен по оси Y.
    # Задаём свет после камеры, чтобы его положение было фиксировано в комнате.
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, (-3, 6, 4, 1))


# Рисует пол и две стены. textures хранит номера загруженных текстур.
def draw_room(textures):
    floor = ((-4, 0, 4), (4, 0, 4), (4, 0, -3), (-4, 0, -3))
    back_wall = ((-4, 0, -3), (4, 0, -3), (4, 5, -3), (-4, 5, -3))
    left_wall = ((-4, 0, 4), (-4, 0, -3), (-4, 5, -3), (-4, 5, 4))

    draw_surface(textures["floor"], floor, (0, 1, 0), repeats=(4, 3.5))
    draw_surface(textures["wall"], back_wall, (0, 0, 1), repeats=(4, 2.5))
    draw_surface(textures["wall"], left_wall, (1, 0, 0), repeats=(3.5, 2.5))


# Рисует комнату, стол и глобус. Используется и в окне, и для снимка комнаты.
def draw_scene(textures):
    draw_room(textures)
    draw_table(textures["wood"])
    draw_sphere(textures["earth"], GLOBE_CENTER, SPHERE_RADIUS)


# Рисует зеркальную сферу. environment_texture — номер текстуры со снимком комнаты.
def draw_mirror(environment_texture):
    # OpenGL вычисляет координаты s и t по нормали и положению наблюдателя.
    GL.glTexGeni(GL.GL_S, GL.GL_TEXTURE_GEN_MODE, GL.GL_SPHERE_MAP)
    GL.glTexGeni(GL.GL_T, GL.GL_TEXTURE_GEN_MODE, GL.GL_SPHERE_MAP)
    GL.glEnable(GL.GL_TEXTURE_GEN_S)
    GL.glEnable(GL.GL_TEXTURE_GEN_T)
    GL.glDisable(GL.GL_LIGHTING)  # Освещение уже есть на снимке.

    draw_sphere(environment_texture, MIRROR_CENTER, SPHERE_RADIUS)

    GL.glEnable(GL.GL_LIGHTING)
    GL.glDisable(GL.GL_TEXTURE_GEN_T)
    GL.glDisable(GL.GL_TEXTURE_GEN_S)
