import sys

from OpenGL.GL import *
from OpenGL.GLUT import *


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glutSwapBuffers()


glutInit(sys.argv)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) 

glutInitWindowSize(800, 600)
glutCreateWindow(b"My first OpenGL window")

glClearColor(0.2, 0.3, 0.4, 1.0)

glutDisplayFunc(display)
glutMainLoop()