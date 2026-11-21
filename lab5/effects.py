from math import cos, sin, tau

from OpenGL import GL as gl

from objects import cube_vertices, draw_cube, draw_floor, draw_quad


STEP_HEIGHT = 0.36
STEP_DEPTH = 1.15
MIRROR_CUBE = cube_vertices(-0.55, 0.65, 1.65, 1.3)
STAIR_CUBE = cube_vertices(-0.85, STEP_HEIGHT + 1.05 / 2, 1.18, 1.05)
LIGHT_RAY = (1.5, -1, -4.75)


# Рисует форму зеркала в плоскости z = 0. ellipse выбирает эллипс или прямоугольник.
def draw_mirror_shape(ellipse):
    if ellipse:
        gl.glBegin(gl.GL_POLYGON)
        for i in range(64):
            angle = tau * i / 64
            gl.glVertex3f(1.65 * cos(angle), 1.55 + 1.22 * sin(angle), 0)
        gl.glEnd()
    else:
        draw_quad(((-1.65, 0.33, 0), (1.65, 0.33, 0), (1.65, 2.77, 0), (-1.65, 2.77, 0)))


# Рисует пол и куб. Эти же объекты видны в отражении.
def draw_mirror_objects():
    draw_floor(0)
    draw_cube(MIRROR_CUBE)


# Рисует стену с зеркалом выбранной формы, отражение и саму сцену.
def draw_mirror(ellipse):
    # Форма зеркала записывает единицы в трафарет.
    gl.glEnable(gl.GL_STENCIL_TEST)
    gl.glStencilFunc(gl.GL_ALWAYS, 1, 0xFF)
    gl.glStencilOp(gl.GL_KEEP, gl.GL_KEEP, gl.GL_REPLACE)

    # Голубой фон без записи глубины, чтобы через него было видно отражение.
    gl.glDepthMask(gl.GL_FALSE)
    gl.glColor3f(0.57, 0.73, 0.87)
    draw_mirror_shape(ellipse)
    gl.glDepthMask(gl.GL_TRUE)

    # Рисуем отражение там, где в трафарете стоит 1.
    gl.glStencilFunc(gl.GL_EQUAL, 1, 0xFF)
    gl.glPushMatrix()
    gl.glScalef(1, 1, -1)
    draw_mirror_objects()
    gl.glPopMatrix()

    # Стена заполняет область с нулями. Куб и пол рисуются уже без трафарета.
    gl.glStencilFunc(gl.GL_EQUAL, 0, 0xFF)
    gl.glColor3f(0.92, 0.91, 0.87)
    draw_quad(((-3.4, 0, 0), (3.4, 0, 0), (3.4, 3.3, 0), (-3.4, 3.3, 0)))
    gl.glDisable(gl.GL_STENCIL_TEST)
    draw_mirror_objects()


# Возвращает вершины тени куба на плоскости y = level.
# При vertical=True плоскость вертикальная и задана как z = level.
def project_shadow(level, vertical):
    dx, dy, dz = LIGHT_RAY
    shadow = []
    for x, y, z in STAIR_CUBE:
        # t показывает, сколько раз прибавить вектор луча до попадания на грань.
        if vertical:
            t = (level - z) / dz
            shadow.append((x + t * dx, y + t * dy, level))
        else:
            t = (level - y) / dy
            shadow.append((x + t * dx, level, z + t * dz))
    return shadow


# Рисует одну грань лестницы и часть тени на ней.
# vertices и color задают углы и цвет, level — высоту или координату Z грани.
def draw_shadow_face(vertices, color, level, vertical=False):
    # Для каждой грани заново помечаем её видимую область единицами.
    gl.glClear(gl.GL_STENCIL_BUFFER_BIT)
    gl.glEnable(gl.GL_STENCIL_TEST)
    gl.glStencilFunc(gl.GL_ALWAYS, 1, 0xFF)
    gl.glStencilOp(gl.GL_KEEP, gl.GL_KEEP, gl.GL_REPLACE)
    gl.glColor3f(*color)
    draw_quad(vertices)

    # Отключаем проверку глубины, поскольку тень лежит прямо на грани.
    # Трафарет пропускает проекцию только на видимую часть этой грани.
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glStencilFunc(gl.GL_EQUAL, 1, 0xFF)
    gl.glStencilOp(gl.GL_KEEP, gl.GL_KEEP, gl.GL_KEEP)
    r, g, b = color
    gl.glColor3f(0.55 * r, 0.55 * g, 0.55 * b)
    draw_cube(project_shadow(level, vertical), shadow=True)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_STENCIL_TEST)


# Рисует три ступени, тень на горизонтальных и вертикальных гранях и куб.
def draw_staircase():
    draw_floor(-2.8)
    left, right = -2.1, 2.1
    for step in range(3):
        low_y = step * STEP_HEIGHT
        top_y = low_y + STEP_HEIGHT
        front_z = 1.75 - step * STEP_DEPTH
        back_z = front_z - STEP_DEPTH

        top = ((left, top_y, front_z), (right, top_y, front_z),
               (right, top_y, back_z), (left, top_y, back_z))
        draw_shadow_face(top, (0.72, 0.75, 0.77), top_y)

        front = ((left, low_y, front_z), (right, low_y, front_z),
                 (right, top_y, front_z), (left, top_y, front_z))
        front_color = (0.56, 0.60, 0.64)
        # Лучи идут в сторону -Z, поэтому до передней грани первой ступени тень не доходит.
        if step == 0:
            gl.glColor3f(*front_color)
            draw_quad(front)
        else:
            draw_shadow_face(front, front_color, front_z, vertical=True)

        gl.glColor3f(0.48, 0.52, 0.57)
        for x in (left, right):
            draw_quad(((x, 0, front_z), (x, top_y, front_z),
                       (x, top_y, back_z), (x, 0, back_z)))

    draw_cube(STAIR_CUBE)
