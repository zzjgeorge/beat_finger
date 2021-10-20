import cv2
import mediapipe as mp
import pyglet
from pyglet.gl import *
import numpy as np
import ctypes

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

HEIGHT = 480
WIDTH = 720
window = pyglet.window.Window(width=WIDTH, height=HEIGHT)
batch = pyglet.graphics.Batch()

tip = [1,0,0]
mcp = [0,0,0]

rectangle = pyglet.shapes.Rectangle(x=0, y=0, width=300, height=200, color=(255,255,255), batch=batch)



# For webcam input:
cap = cv2.VideoCapture(0)
# rows, cols, channels = cap.shape
# byte_size = rows*cols*channels


@window.event()
def on_draw():
    window.clear()
    batch.draw()


def find_finger_pos(dt):
    rectangle.x += dt*100
    rectangle.y += dt*100

if __name__ == "__main__":
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    model = pyglet.resource.model("box.obj", batch=batch)

    pyglet.clock.schedule_interval(find_finger_pos, 1/600)
    pyglet.app.run()