import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from classes.two_dimensions.vector import Vector2D

class Window :
    fontbase = None

    @classmethod
    def initializefont(cls) :
        pygame.init()

        display = pygame.display.set_mode((1, 1), OPENGL | DOUBLEBUF)
        
        fontinformation = pygame.font.Font(None, 18)
        if cls.fontbase is not None : 
            glDeleteLists(cls.fontbase, 96)

        cls.fontbase = glGenLists(96)

        for i in range(32, 128) :
            character = chr(i)
            texturesurface = fontinformation.render(character, True, (255, 255, 255), (0, 0, 0))
            texturedata = pygame.image.tostring(texturesurface, 'RGBA', True)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texturesurface.get_width(), texturesurface.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, texturedata)

        pygame.quit()

    @classmethod
    def killfont(cls) :
        glDeleteLists(cls.fontbase, 96)

    @classmethod
    def textout(cls, format, *args) :
        text = format % args
        glPushAttrib(GL_LIST_BIT)
        glListBase(cls.s_fontBase - 32)
        glCallLists(text)
        glPopAttrib()
    
    @classmethod
    def text_out_at(cls, x, y, format, *args):
        position = cls.getoglposition(x, y)
        glRasterPos2f(position[0], position[1])

        text = format % args
        glPushAttrib(GL_LIST_BIT)
        glListBase(cls.s_fontBase - 32)
        glCallLists(text)
        glPopAttrib()
    
    @staticmethod
    def getoglposition(x, y) :
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)

        windowx = float(x)
        windowy = float(viewport[3]) - float(y)
        windowz = glReadPixels(x, int(windowy), 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
        positionx, positiony, positionz = gluUnProject(windowx, windowy, windowz, modelview, projection, viewport)

        return Vector2D(x = positionx, y = positiony)