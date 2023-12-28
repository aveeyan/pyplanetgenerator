import sys
import math
import numpy as np
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import noise
import glob
import os

## Setting up environment variables
os.environ.setdefault('VIEW_DISTANCE', '2.25')

# Access the environment variables
VIEW_DISTANCE = float(os.environ.get('VIEW_DISTANCE'))

# Function to get the latest file in a directory
def get_latest_file(directory):
    list_of_files = glob.glob(os.path.join(directory, '*'))
    if not list_of_files:
        return None
    return max(list_of_files, key=os.path.getctime)

# Load the noisemap image
NOISEMAP_DEFAULT = "output_image.png"
NOISEMAP_PATH_DEFAULT = get_latest_file("./output-noise/")

if NOISEMAP_PATH_DEFAULT is not None:
    noisemap_img = Image.open(NOISEMAP_PATH_DEFAULT)
else:
    print("No noisemap file found.")
    sys.exit(1)  # Exit the program if no valid noisemap file is found

# Sphere parameters
radius = 1.0
slices = 100
stacks = 100

# Function to draw the background
def draw_background():
    glPushMatrix()
    glBindTexture(GL_TEXTURE_2D, 2)  # Use the background texture ID
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-1, -1, -1)
    glTexCoord2f(1, 0)
    glVertex3f(1, -1, -1)
    glTexCoord2f(1, 1)
    glVertex3f(1, 1, -1)
    glTexCoord2f(0, 1)
    glVertex3f(-1, 1, -1)
    glEnd()
    glPopMatrix()


# Function to apply the noisemap to the sphere
def apply_noisemap():
    glEnable(GL_TEXTURE_2D)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glBindTexture(GL_TEXTURE_2D, 1)

    # Convert the noisemap image to a NumPy array
    noisemap_data = np.array(noisemap_img)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, noisemap_data.shape[1], noisemap_data.shape[0],
                 0, GL_RGB, GL_UNSIGNED_BYTE, noisemap_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

# Function to draw the sphere
def draw_sphere():
    glPushMatrix()
    apply_noisemap()
    quad = gluNewQuadric()
    gluQuadricTexture(quad, GL_TRUE)  # Enable texture coordinates
    gluSphere(quad, radius, slices, stacks)
    glPopMatrix()

# OpenGL initialization
def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_TEXTURE_2D)
    
# Function to handle window resizing
def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w) / float(h), 0.1, 200.0)  # Increase the field of view (fovy)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


# Function to display the scene
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set the camera position
    gluLookAt(0, 0, VIEW_DISTANCE, 0, 0, 0, 0, 1, 0)  # Adjusted the camera position (eye)

    # Draw the background
    draw_background()

    # Rotate the sphere
    angle_x = glutGet(GLUT_ELAPSED_TIME) / 1000.0 * 10
    angle_y = glutGet(GLUT_ELAPSED_TIME) / 1000.0 * 5  # Adjust the rotation speed

    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)

    # Draw the sphere
    draw_sphere()

    glutSwapBuffers()


# Main function
def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow("3D Sphere with Noisemap")

    init()
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutIdleFunc(display)
    glutMainLoop()

if __name__ == "__main__":
    main()
