from pyglet.gl import *
import ctypes
import numpy as np

window = pyglet.window.Window()


batch = pyglet.graphics.Batch()
model = pyglet.resource.model("box.obj", batch=batch)


orientation = [1,1,1]
mcp = [0,0,0]
def cart2sph(x,y,z):
    XsqPlusYsq = x*x + y*y
    r = np.sqrt(XsqPlusYsq + z**2)
    theta = np.arctan2(z,np.sqrt(XsqPlusYsq))
    phi = np.arctan2(y,x)
    return r, theta, phi

def animate_finger():
    model.rotation = cart2sph(orientation)
    model.translation = mcp

def draw_pyramid():
    Point = ctypes.c_double * 3
    pointO = Point(0.0, 1.0, 0.0)
    pointA = Point(1.5, -1.0, 1.5)
    pointB = Point(-1.5, -1.0, 1.5)
    pointC = Point(-1.5, -1.0, -1.5)
    pointD = Point(1.5, -1.0, -1.5)

    glColor3d(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex3dv(pointO)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glEnd()

    glColor3d(1.0, 1.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex3dv(pointO)
    glVertex3dv(pointB)
    glVertex3dv(pointC)
    glEnd()

    glColor3d(0.0, 1.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex3dv(pointO)
    glVertex3dv(pointC)
    glVertex3dv(pointD)
    glEnd()

    glColor3d(1.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex3dv(pointO)
    glVertex3dv(pointD)
    glVertex3dv(pointA)
    glEnd()

    glColor3d(1.0, 1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3dv(pointA)
    glVertex3dv(pointB)
    glVertex3dv(pointC)
    glVertex3dv(pointD)
    glEnd()

time=0
def animate(dt):
    global time
    time += dt
    # rot = model.rotation
    # model.rotation = rot[0], rot[1] + dt * 27, rot[2] + dt * 35
    # model.translation = -1.5, 0, np.sin(time) * 0.7 - 4.0

@window.event
def on_draw():
    window.clear()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90.0, 1.0, 0.1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0,0,10, 0,0,0, 0,1,0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    glEnable(GL_DEPTH_TEST)
    glPushMatrix()
    #glRotated(time*30,0, 1, 0)
    glTranslatef(time,time,0)
    draw_pyramid()
    glPopMatrix()
    glDisable(GL_DEPTH_TEST)

pyglet.clock.schedule_interval(animate, 1/24)
pyglet.app.run()
# glEnable(GL_DEPTH_TEST)
# glEnable(GL_CULL_FACE)

# glMatrixMode(GL_PROJECTION)
# glLoadIdentity()
# gluPerspective(90.0, 1.0, 0.1, 100)

# pyglet.app.run()

