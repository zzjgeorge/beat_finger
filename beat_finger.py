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

rectangle = pyglet.shapes.Rectangle(x=150, y=150, width=300, height=200, color=(255,255,255), batch=batch)



# For webcam input:
cap = cv2.VideoCapture(0)
# rows, cols, channels = cap.shape
# byte_size = rows*cols*channels


@window.event()
def on_draw():
    window.clear()
    batch.draw()


def find_finger_pos(dt):
    global tip, mcp
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
                rectangle.rotation = 0
                rectangle.postiion = mcp[0]*WIDTH-WIDTH/2, mcp[1]*HEIGHT-HEIGHT/2
                #rectangle.y = mcp[1]
                rectangle.anchor_position = mcp[0]*WIDTH-WIDTH/2, mcp[1]*HEIGHT-HEIGHT/2
                #print(mcp[0]*720, mcp[1]*480)
                #rectangle.rotation = np.arctan2(tip[1]-mcp[1], tip[0]-mcp[0])*180/3.14159
                #orientation = [tip[i]-mcp[i] for i in range(3)]
                #print(orientation)
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