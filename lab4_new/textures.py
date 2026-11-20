from pathlib import Path

from OpenGL import GL
from PIL import Image

TEXTURE_DIR = Path(__file__).resolve().parent / "textures"


# Загружает PNG по имени filename и возвращает номер текстуры OpenGL.
# repeat включает повторение изображения за пределами координат от 0 до 1.
def load_texture(filename, repeat=False):
    with Image.open(TEXTURE_DIR / filename) as image:
        # У PNG первая строка сверху. OpenGL считает t от нижнего края.
        image = image.convert("RGB").transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        width, height = image.size
        pixels = image.tobytes()

    texture = GL.glGenTextures(1)
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture)
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)  # Строки RGB идут без отступов.
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
    wrap = GL.GL_REPEAT if repeat else GL.GL_CLAMP_TO_EDGE
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, wrap)
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, wrap)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0,
                    GL.GL_RGB, GL.GL_UNSIGNED_BYTE, pixels)
    return texture


# Возвращает словарь с номерами текстур для комнаты, стола и глобуса.
def load_scene_textures():
    return {
        "floor": load_texture("floor.png", repeat=True),
        "wall": load_texture("wall.png", repeat=True),
        "wood": load_texture("wood.png"),
        "earth": load_texture("earth.png"),
    }
