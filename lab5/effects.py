from math import cos, sin, tau

from OpenGL import GL as gl

from objects import draw_cube, draw_floor, draw_quad


STEP_HEIGHT = 0.36
STEP_DEPTH = 1.15
STAIR_CUBE = (-0.85, STEP_HEIGHT + 1.05 / 2, 1.18, 1.05)
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
    draw_cube(-0.55, 0.65, 1.65, 1.3)


# Рисует стену с зеркалом выбранной формы, отражение и саму сцену.
def draw_mirror(ellipse):
    gl.glEnable(gl.GL_STENCIL_TEST)
    gl.glStencilFunc(gl.GL_ALWAYS, 1, 0xFF)
    gl.glStencilOp(gl.GL_KEEP, gl.GL_KEEP, gl.GL_REPLACE)

    # Цвет зеркала виден там, где нет отражённых объектов. Глубину здесь не записываем.
    gl.glDepthMask(gl.GL_FALSE)
    gl.glColor3f(0.57, 0.73, 0.87)
    draw_mirror_shape(ellipse)
    gl.glDepthMask(gl.GL_TRUE)

    # Отражение меняет знак Z. Трафарет пропускает его только внутри зеркала.
    gl.glStencilFunc(gl.GL_EQUAL, 1, 0xFF)
    gl.glPushMatrix()
    gl.glScalef(1, 1, -1)
    draw_mirror_objects()
    gl.glPopMatrix()

    gl.glStencilFunc(gl.GL_EQUAL, 0, 0xFF)
    gl.glColor3f(0.92, 0.91, 0.87)
    draw_quad(((-3.4, 0, 0), (3.4, 0, 0), (3.4, 3.3, 0), (-3.4, 3.3, 0)))
    gl.glDisable(gl.GL_STENCIL_TEST)
    draw_mirror_objects()


# Возвращает матрицу проекции тени на плоскость n·P + offset = 0.
# normal — нормаль n к плоскости, лучи параллельны LIGHT_RAY.
def shadow_matrix(normal, offset):
    nx, ny, nz = normal
    lx, ly, lz = LIGHT_RAY
    dot = nx * lx + ny * ly + nz * lz
    lx, ly, lz = lx / dot, ly / dot, lz / dot

    # Формула из учебника: Q = P - (n·P + offset) * LIGHT_RAY / dot.
    # glMultMatrixf принимает элементы подряд по столбцам.
    return (
        1 - lx * nx, -ly * nx, -lz * nx, 0,
        -lx * ny, 1 - ly * ny, -lz * ny, 0,
        -lx * nz, -ly * nz, 1 - lz * nz, 0,
        -lx * offset, -ly * offset, -lz * offset, 1,
    )


# Рисует одну грань лестницы и часть тени на ней.
# vertices задаёт углы, color — цвет, normal и offset — уравнение плоскости грани.
def draw_shadow_face(vertices, color, normal, offset):
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
    gl.glColor3f(*(component * 0.55 for component in color))
    gl.glPushMatrix()
    gl.glMultMatrixf(shadow_matrix(normal, offset))
    draw_cube(*STAIR_CUBE, shadow=True)
    gl.glPopMatrix()
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
        draw_shadow_face(top, (0.72, 0.75, 0.77), (0, 1, 0), -top_y)

        front = ((left, low_y, front_z), (right, low_y, front_z),
                 (right, top_y, front_z), (left, top_y, front_z))
        front_color = (0.56, 0.60, 0.64)
        # Лучи идут в сторону -Z, поэтому до передней грани первой ступени тень не доходит.
        if step == 0:
            gl.glColor3f(*front_color)
            draw_quad(front)
        else:
            draw_shadow_face(front, front_color, (0, 0, 1), -front_z)

        gl.glColor3f(0.48, 0.52, 0.57)
        for x in (left, right):
            draw_quad(((x, 0, front_z), (x, top_y, front_z),
                       (x, top_y, back_z), (x, 0, back_z)))

    draw_cube(*STAIR_CUBE)
