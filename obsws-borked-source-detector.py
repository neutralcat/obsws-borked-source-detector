#!./venv-obsws/bin/python

# REQUIREMENTS:
# make a virtual environment with obsws-python installed through pip

#####################
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = "4455"
WEBSOCKET_PASSWORD = ""

SCREENSHOT_DELAY = 60 # seconds
IMAGE_FORMAT = "png"
TEMP_FOLDER_NAME = "temp"
TEMP_IMAGE_PREFIX = "source-screenshot"
#####################

from time import sleep
from hashlib import md5
import obsws_python as obsws
from os import path, getcwd, mkdir

client = obsws.ReqClient(host=WEBSOCKET_HOST,port=WEBSOCKET_PORT,password=WEBSOCKET_PASSWORD)
image_folder = path.join(getcwd(), "temp")

if not path.exists(image_folder):
    mkdir(image_folder)


def they_have_the_same_hash() -> bool:
    try:
        with open(path.join(image_folder, f"{TEMP_IMAGE_PREFIX}.a.{IMAGE_FORMAT}"), "rb") as file_a:
            hash_a = md5(file_a.read()).hexdigest()

        with open(path.join(image_folder, f"{TEMP_IMAGE_PREFIX}.b.{IMAGE_FORMAT}"), "rb") as file_b:
            hash_b = md5(file_b.read()).hexdigest()
    
    except FileNotFoundError as err:
        print(f"\033[31mcould not read from file, {err}\033[37m")
        return False
    
    print(f"hash_a = {hash_a}\nhash_b = {hash_b}")
    return hash_a == hash_b


current = True
while True:
    client.save_source_screenshot(
        name = client.get_current_program_scene().scene_name,
        img_format = IMAGE_FORMAT,
        file_path = path.join(image_folder, f"{TEMP_IMAGE_PREFIX}.{"a" if current else "b"}.{IMAGE_FORMAT}"),
        width = 480,
        height = 270,
        quality = -1
    )
    print(f"\033[92msaved screenshot to {path.join(image_folder, f"{TEMP_IMAGE_PREFIX}.{"a" if current else "b"}.{IMAGE_FORMAT}")}\033[37m")

    if they_have_the_same_hash():
        raise Exception("\033[31mOBS FUCKED UP AGAIN\033[37m") # TODO: use the DBUS org.freedesktop.Notifications interface to send a notification to the user. maybe desktop-notifier package

    print(f"\033[2msleeping for {SCREENSHOT_DELAY} seconds...\033[22m")
    current = not current
    sleep(SCREENSHOT_DELAY)
