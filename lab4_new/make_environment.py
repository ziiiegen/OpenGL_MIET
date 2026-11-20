from OpenGL import GL, GLUT
from PIL import Image

from scene import MIRROR_CENTER, SPHERE_RADIUS, draw_scene, prepare_frame, setup_lighting
from textures import TEXTURE_DIR, load_scene_textures


# Снимает комнату со стороны зеркального шара и сохраняет кадр в environment.png.
def main():
    size = 256
    GLUT.glutInit()
    GLUT.glutInitDisplayMode(GLUT.GLUT_DOUBLE | GLUT.GLUT_RGB | GLUT.GLUT_DEPTH)
    GLUT.glutInitWindowSize(size, size)
    window = GLUT.glutCreateWindow(b"Making environment.png")
    GLUT.glutHideWindow()

    setup_lighting()
    textures = load_scene_textures()
    x, y, z = MIRROR_CENTER
    eye = (x, y, z + SPHERE_RADIUS)  # Камера у передней точки шара.
    target = (x, y, z)              # Взгляд направлен к задней стене вдоль -Z.
    prepare_frame(size, size, eye, target, fov=90)
    draw_scene(textures)  # В кадр входят только комната, стол и глобус.

    # Читаем кадр из заднего буфера до вывода в окно.
    GL.glReadBuffer(GL.GL_BACK)
    GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
    pixels = GL.glReadPixels(0, 0, size, size, GL.GL_RGB, GL.GL_UNSIGNED_BYTE)
    image = Image.frombytes("RGB", (size, size), bytes(pixels))
    image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    path = TEXTURE_DIR / "environment.png"
    image.save(path)
    GLUT.glutDestroyWindow(window)
    print("Создана текстура", path)


if __name__ == "__main__":
    main()
