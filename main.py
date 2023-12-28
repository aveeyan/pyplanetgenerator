import noise
import numpy as np
from keras.preprocessing import image as kim
from datetime import datetime
import os
import time
import random

# Local Scripts
from simple_hash import custom_random

# Set Seed
seed = str(int(time.time()))

# Script Input
def get_user_input():
    print("\nEnter the parameters for the noise generation:")

    # Noise Shape
    noise_shape_input = input("Noise Shape (comma-separated values, e.g., '1024,1024'): ")
    noise_shape = tuple(map(int, noise_shape_input.split(','))) if noise_shape_input else (1024, 1024)

    # Noise Scale
    noise_scale_input = input("Noise Scale (e.g., 100.0): ")
    noise_scale = float(noise_scale_input) if noise_scale_input else 100.0

    # Noise Octave
    noise_octave_input = input("Noise Octave (e.g., 4): ")
    noise_octave = int(noise_octave_input) if noise_octave_input else 4

    # Noise Persistence
    noise_persistence_input = input("Noise Persistence (e.g., 0.5): ")
    noise_persistence = float(noise_persistence_input) if noise_persistence_input else 0.5

    # Noise Lacunarity
    noise_lacunarity_input = input("Noise Lacunarity (e.g., 2.0): ")
    noise_lacunarity = float(noise_lacunarity_input) if noise_lacunarity_input else 2.0

    # Noise Base
    noise_base_input = input("Noise Base (skip for randomized world): ")
    noise_base = int(noise_base_input) if noise_base_input else -1

    # Color Threshold
    color_threshold_input = input("Color Threshold (e.g., 0): ")
    color_threshold = float(color_threshold_input) if color_threshold_input else 0.0

    # Gradient Strength
    gradient_strength_input = input("Gradient Strength (e.g., 2.0): ")
    gradient_strength = float(gradient_strength_input) if gradient_strength_input else 2.0

    # Alien Planet
    alien_planet_input = input("Is it an alien planet? (True/False): ")
    alien_planet = alien_planet_input.lower() == 'true' if alien_planet_input else False

    return {
        "DF_NOISE_SHAPE": noise_shape,
        "DF_NOISE_SCALE": noise_scale,
        "DF_NOISE_OCTAVE": noise_octave,
        "DF_NOISE_PERSISTENCE": noise_persistence,
        "DF_NOISE_LACUNARITY": noise_lacunarity,
        "DF_NOISE_BASE": noise_base,
        "DF_COLOR_THRESHOLD": color_threshold,
        "DF_GRADIENT_STRENGTH": gradient_strength,
        "DF_ALIEN_PLANET": alien_planet
    }

# Definition of Node for a Linked List
class Node:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.color = None
        self.next = None

# Constants I: Defaults for noise
user_input = get_user_input()
DF_NOISE_SHAPE = user_input["DF_NOISE_SHAPE"]
DF_NOISE_SCALE = user_input["DF_NOISE_SCALE"]
DF_NOISE_OCTAVE = user_input["DF_NOISE_OCTAVE"]
DF_NOISE_PERSISTENCE = user_input["DF_NOISE_PERSISTENCE"]
DF_NOISE_LACUNARITY = user_input["DF_NOISE_LACUNARITY"]
DF_NOISE_BASE = user_input["DF_NOISE_BASE"]
DF_COLOR_THRESHOLD = user_input["DF_COLOR_THRESHOLD"]
DF_GRADIENT_STRENGTH = user_input["DF_GRADIENT_STRENGTH"]
DF_ALIEN_PLANET = user_input["DF_ALIEN_PLANET"]

def main():

    def return_file_timestamp() -> str:
        timestamp_format = "%d%b%y_%H-%M-%S"
        current_time = datetime.now()
        timestamp = current_time.strftime(timestamp_format)
        return f"noisemap_{timestamp}.png"

    def create_noisemap(octaves=DF_NOISE_OCTAVE, x_val=DF_NOISE_SHAPE[0], y_val=DF_NOISE_SHAPE[1],
                        persistence=DF_NOISE_PERSISTENCE, lacunarity=DF_NOISE_LACUNARITY,
                        base=DF_NOISE_BASE, scale=DF_NOISE_SCALE, shape=DF_NOISE_SHAPE,
                        gradient_strength=DF_GRADIENT_STRENGTH):

        if base is None or base == -1:
            base = int(custom_random(seed) * 500)  # Generate a random base if not provided
        print("Random Base:", base)

        world_list = None
        center_x, center_y = x_val // 2, y_val // 2

        for x in range(x_val):
            for y in range(y_val):
                distance_to_center = np.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
                normalized_distance = distance_to_center / max(center_x, center_y)

                gradient = 1.0 - normalized_distance  # Invert gradient
                gradient *= gradient_strength  # Scale the gradient strength

                noise_value = noise.pnoise2(x / scale,
                                            y / scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            base=base) * gradient

                new_node = Node(x, y, noise_value)
                new_node.next = world_list
                world_list = new_node

        color_world(world_list, 0.1)
        return world_list



    def color_world(world_list, threshold: float = DF_COLOR_THRESHOLD, alien = DF_ALIEN_PLANET):
        # Color assignment logic goes here
        if alien:
            lightblue = [random.randint(0, 255) for _ in range(3)]
            blue = [random.randint(0, 255) for _ in range(3)]
            green = [random.randint(0, 255) for _ in range(3)]
            darkgreen = [random.randint(0, 255) for _ in range(3)]
            sandy = [random.randint(0, 255) for _ in range(3)]
            beach = [random.randint(0, 255) for _ in range(3)]
            snow = [random.randint(0, 255) for _ in range(3)]
            mountain = [random.randint(0, 255) for _ in range(3)]
            dark_orange = [random.randint(0, 255) for _ in range(3)]            
        else:
            lightblue = [56, 151, 254]
            blue = [65, 105, 225]
            green = [34, 139, 34]
            darkgreen = [0, 100, 0]
            sandy = [210, 180, 140]
            beach = [238, 214, 175]
            snow = [255, 250, 250]
            mountain = [139, 137, 137]
            dark_orange = [255, 69, 0]

        current_node = world_list
        while current_node is not None:
            value = current_node.value

            if value < threshold + 0.01:
                current_node.color = blue
            elif threshold + 0.01 <= value < threshold + 0.03:
                current_node.color = lightblue
            elif threshold + 0.03 <= value < threshold + 0.055:
                current_node.color = sandy
            elif threshold + 0.055 <= value < threshold + 0.1:
                current_node.color = beach
            elif threshold + 0.1 <= value < threshold + 0.35:
                current_node.color = green
            elif threshold + 0.35 <= value < threshold + 0.75:
                current_node.color = darkgreen
            elif threshold + 0.75 <= value < threshold + 0.95:
                current_node.color = mountain
            elif threshold + 0.95 <= value <= 1.2:
                current_node.color = snow
            else:
                current_node.color = dark_orange

            current_node = current_node.next

    def show_world(world_list, shape):
        filename = f"./output-noise/{return_file_timestamp()}"
        img_array = np.zeros(shape + (3,), dtype=np.uint8)

        current_node = world_list
        while current_node is not None:
            x, y, color = current_node.x, current_node.y, current_node.color
            x = int(x)  # Convert x and y to integers
            y = int(y)
            color = [int(c) for c in color]  # Convert color components to integers
            img_array[x][y] = color
            current_node = current_node.next

        img = kim.array_to_img(img_array)
        kim.save_img(filename, img)


    world_list = create_noisemap()
    show_world(world_list, DF_NOISE_SHAPE)

if __name__ == "__main__":
    main()
