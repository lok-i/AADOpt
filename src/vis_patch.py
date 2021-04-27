import pygame
from pygame.locals import *
import math
import numpy as np

from OpenGL.GL import *
from OpenGL.GLU import *

lastPosX = 0;
lastPosY = 0;
zoomScale = 1.0;
dataL = 0;
xRot = 0;
yRot = 0;
zRot = 0;

# =============================================================================
# vertices = ((1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1), (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1))
# edges = ((0, 1), (0, 3), (0, 4), (2, 1), (2, 3), (2, 7), (6, 3), (6, 4), (6, 7), (5, 1), (5, 4), (5, 7))
# =============================================================================

def substrate(x,y,z,r,g,b):

    vertices = ((-x, -y, -z), (-x, y, -z), (-x, y, z), (-x, -y, z), (x, -y, -z), (x, y, -z), (x, y, z), (x, -y, z))
    edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
    faces = ((0, 1, 2 , 3),(4,  5, 6, 7),(0, 4, 7, 3),(1, 5, 6, 2),(2, 6, 7, 3),(1, 5, 4, 0))

    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glColor3fv((r/255, g/255, b/255))
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((0, 0, 0))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def patch(x,y,z,r,g,bl,a,b):

    vertices = ((-x+a, -y+b, -z), (-x+a, y+b, -z), (-x+a, y+b, z), (-x+a, -y+b, z), (x+a, -y+b, -z), (x+a, y+b, -z), (x+a, y+b, z), (x+a, -y+b, z))
    edges = ((0, 1), (0, 3), (0, 4), (1, 2), (1, 5), (2, 3), (2, 6), (3, 7), (4, 5), (4, 7), (5, 6), (6, 7))
    faces = ((0, 1, 2 , 3),(4,  5, 6, 7),(0, 4, 7, 3),(1, 5, 6, 2),(2, 6, 7, 3),(1, 5, 4, 0))

    glBegin(GL_QUADS)

    for face in faces:
        for vertex in face:
            glColor3fv((r/255, g/255, bl/255))
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES)
    glColor3fv((0, 0, 0))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def mouseMove(event):
    global lastPosX, lastPosY, zoomScale, xRot, yRot, zRot;
 
    scale = 0.25
    
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4: # wheel rolled up
        glScaled(1+scale, 1+scale, 1+scale);
    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5: # wheel rolled down
        glScaled(1-scale, 1-scale, 1-scale);
 
    if event.type == pygame.MOUSEMOTION:
        x, y = event.pos;
        dx = x - lastPosX;
        dy = y - lastPosY;
        
        mouseState = pygame.mouse.get_pressed();
        if mouseState[0]:

            modelView = (GLfloat * 16)()
            mvm = glGetFloatv(GL_MODELVIEW_MATRIX, modelView)
   
   # To combine x-axis and y-axis rotation
            temp = (GLfloat * 3)();
            temp[0] = modelView[0]*dy + modelView[1]*dx;
            temp[1] = modelView[4]*dy + modelView[5]*dx;
            temp[2] = modelView[8]*dy + modelView[9]*dx;
            norm_xy = math.sqrt(temp[0]*temp[0] + temp[1]*temp[1] + temp[2]*temp[2]);
            glRotatef(math.sqrt(dx*dx+dy*dy), temp[0]/norm_xy, temp[1]/norm_xy, temp[2]/norm_xy);

        lastPosX = x;
        lastPosY = y;
        
def make_Patch(element_array):
    pygame.init()
 
    display = (600,400)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL, RESIZABLE)

    gluPerspective(45, (1.0*display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
 

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            mouseMove(event);

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        S_L = max(np.abs(element_array[:,0]))
        S_B = max(np.abs(element_array[:,1]))
        S_H = max(np.abs(element_array[:,7]))
        S_c = max(element_array[:,5]) + max(element_array[:,6]) # always positive

        substrate(S_L + S_c, S_B + S_c, S_H, 255, 215, 0)   #(l,b,h,r,g,b)

        for element in element_array:
            patch(element[5], element[6], element[7], 105, 105, 105, element[0], element[1])    
        
        pygame.display.set_caption('Patch Design')
        pygame.display.flip()
        pygame.time.wait(10)



if __name__ == "__main__":
    pos = ((480,670),(-180,0),(0,90),(0,-90),(1,2),(100,200),(-100,200)) #position of each patch
    W = 20
    L = 35
    h = 2.5

    make_Patch(W,L,h,pos)


