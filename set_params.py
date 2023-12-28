import os

def render_distance():
    view_distance = input("Select a viewing distance (default, 2.25): ")
    return view_distance

def run_main_script(view_distance):
    os.system("python3 main.py")
    os.system(f"VIEW_DISTANCE={view_distance} python3 render_planet.py")
    print("Noisemap saved at:")
    os.system("ls -t -1 ./output-noise | head -n 1")

if __name__ == "__main__":
    run_main_script(render_distance())
