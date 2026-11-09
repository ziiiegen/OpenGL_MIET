from pathlib import Path
from PIL import Image

from OpenGL.GL import (
    GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_TEXTURE_MAG_FILTER, GL_LINEAR,
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_REPEAT, GL_CLAMP_TO_EDGE,
    GL_UNPACK_ALIGNMENT, GL_RGB, GL_UNSIGNED_BYTE,
    glGenTextures, glBindTexture, glTexParameteri, glPixelStorei, glTexImage2D,
)


# Загружает PNG-картинку; name — имя файла, repeat — повторять ли края.
# Возвращает номер текстуры в OpenGL.
def load_texture(name, repeat=False):
    path = Path(__file__).parent / "textures" / name
    with Image.open(path) as image:
        image = image.convert("RGB")
        # У картинки начало сверху, а текстурная координата t начинается снизу.
        image = image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        width, height = image.size
        pixels = image.tobytes()

    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    wrap = GL_REPEAT if repeat else GL_CLAMP_TO_EDGE
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, wrap)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, wrap)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0,
                 GL_RGB, GL_UNSIGNED_BYTE, pixels)
    return texture
