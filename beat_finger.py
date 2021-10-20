import cv2
import mediapipe as mp
import pyglet
from pyglet.gl import *
import numpy as np
import ctypes

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

window = pyglet.window.Window(width=720, height=480)
gluPerspective(90, 1, 0.1, 100)
gluLookAt(5,0,0, 0,0,0, -1,0,0)
batch = pyglet.graphics.Batch()

tip = [1,0,0]
mcp = [1,0,0]
rot = [1,0,0]

# For webcam input:
cap = cv2.VideoCapture(0)
# rows, cols, channels = cap.shape
# byte_size = rows*cols*channels


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

@window.event()
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
    glTranslatef(-mcp[0]*10+5,-mcp[1]*10+5,0) # Z-info is at the order of 1e-9 (for relative info only)
    glRotatef(rot[1], 1, 0, 0)
    glRotatef(rot[2], 0, 0, 1)
    batch.draw()
    glPopMatrix()
    glDisable(GL_DEPTH_TEST)

def cart2sph(x,y,z):
    XsqPlusYsq = x*x + y*y
    r = np.sqrt(XsqPlusYsq + z**2)
    theta = np.arctan2(z,np.sqrt(XsqPlusYsq))*180/3.1415926
    phi = np.arctan2(y,x)*180/3.1415926
    return r, theta, phi

def find_finger_pos(dt):
    global tip, mcp, rot
    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
        success, image = cap.read()
        # if not success:
        #     print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        # image.flags.writeable = True
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        #image = cv2.flip(image, 1)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # mp_drawing.draw_landmarks(
                #     image,
                #     hand_landmarks,
                #     mp_hands.HAND_CONNECTIONS,
                #     mp_drawing_styles.get_default_hand_landmarks_style(),
                #     mp_drawing_styles.get_default_hand_connections_style())
                tip = [hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y,hand_landmarks.landmark[8].z]
                mcp = [hand_landmarks.landmark[0].x, hand_landmarks.landmark[0].y,hand_landmarks.landmark[0].z]
                orientation = [tip[i]-mcp[i] for i in range(3)]
                rot = cart2sph(orientation[0],orientation[1],orientation[2])
                print(orientation)
        # Flip the image horizontally for a selfie-view display.
        # cv2.imshow('MediaPipe Hands', image)
        # if cv2.waitKey(5) & 0xFF == 27:
        #     cap.release()

if __name__ == "__main__":
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    model = pyglet.resource.model("box.obj", batch=batch)

    pyglet.clock.schedule_interval(find_finger_pos, 1/600)
    pyglet.app.run()