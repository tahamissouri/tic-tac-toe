#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  main.py
#  generateur_grille version 1.0
#  Created by Ingenuity i/o on 2025/01/30
#
# "no description"
#

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys
import matplotlib 
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from generateur_grille import *
from PIL import Image, ImageDraw, ImageFont
import ingescape as igs
import os

import base64
port = 5670
agent_name = "generateur_grille"
device = "Wi-Fi"
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()

filename = r"tic_tac_toe.jpg"




def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


def print_usage_help():
    print("Available commands in the terminal:")
    print("	/quit : quits the agent")
    print("	/help : displays this message")

def return_iop_value_type_as_str(value_type):
    if value_type == igs.INTEGER_T:
        return "Integer"
    elif value_type == igs.DOUBLE_T:
        return "Double"
    elif value_type == igs.BOOL_T:
        return "Bool"
    elif value_type == igs.STRING_T:
        return "String"
    elif value_type == igs.IMPULSION_T:
        return "Impulsion"
    elif value_type == igs.DATA_T:
        return "Data"
    else:
        return "Unknown"

def return_event_type_as_str(event_type):
    if event_type == igs.PEER_ENTERED:
        return "PEER_ENTERED"
    elif event_type == igs.PEER_EXITED:
        return "PEER_EXITED"
    elif event_type == igs.AGENT_ENTERED:
        return "AGENT_ENTERED"
    elif event_type == igs.AGENT_UPDATED_DEFINITION:
        return "AGENT_UPDATED_DEFINITION"
    elif event_type == igs.AGENT_KNOWS_US:
        return "AGENT_KNOWS_US"
    elif event_type == igs.AGENT_EXITED:
        return "AGENT_EXITED"
    elif event_type == igs.AGENT_UPDATED_MAPPING:
        return "AGENT_UPDATED_MAPPING"
    elif event_type == igs.AGENT_WON_ELECTION:
        return "AGENT_WON_ELECTION"
    elif event_type == igs.AGENT_LOST_ELECTION:
        return "AGENT_LOST_ELECTION"
    else:
        return "UNKNOWN"

def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True


def on_agent_event_callback(event, uuid, name, event_data, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, GenerateurGrille)
        # add code here if needed
    except:
        print(traceback.format_exc())


def on_freeze_callback(is_frozen, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, GenerateurGrille)
        # add code here if needed
    except:
        print(traceback.format_exc())


# inputs
def grille_input_callback(iop_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, GenerateurGrille)
        agent_object.grilleI = value

        # Parse the input string
        board, points = eval(value)
        
        # Create an image with white background
        size = 300
        img = Image.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        # Load a font
        font = ImageFont.load_default()
        
        # Define symbols and cell size
        symbols = {1: 'X', 0: 'O', -1: ''}
        cell_size = size // 3
        
        # Draw the grid and symbols
        for i in range(3):
            for j in range(3):
                x = j * cell_size
                y = i * cell_size
                draw.rectangle([x, y, x + cell_size, y + cell_size], outline='black')
                symbol = symbols[board[i * 3 + j]]
                if symbol:
                    draw.text((x + cell_size // 2, y + cell_size // 2), symbol, font=font, anchor="mm", fill='black')

        # Check if there are points to draw a line
        if points:
            # Convert grid indices to pixel coordinates
            pixel_points = [(p[1] * cell_size + cell_size // 2, p[0] * cell_size + cell_size // 2) for p in points]
            # Draw line using matplotlib for line fitting
            x_coords, y_coords = zip(*pixel_points)
            plt.imshow(img)
            plt.plot(x_coords, y_coords, 'r-')
            plt.axis('off')
            plt.savefig("tic_tac_toe.jpg", bbox_inches='tight')
            plt.close()
        else:
            # Save image directly if no line is needed
            img.save("tic_tac_toe.jpg")
    
        img.close()

        absolute_path = Path(filename).resolve()

        print(absolute_path)
        igs.output_set_string("grille_jpg", absolute_path)
        #igs.service_call("Whiteboard", "setBackgroundColor", "white", "")

        """
        # with open("./tic_tac_toe.jpg", "rb") as image_file:
            # encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # Utiliser la chaîne encodée comme source de l'image
        # arguments_list = ('data:image/jpeg;base64,' + encoded_string, 100, 100, 200, 300)
        # response = igs.service_call("Whiteboard", "addImage", arguments_list, "")
        # print(response)
        """

        # an HTTP server is already started on the local machine in the current directory to expose images
        # This server will make the images accessible via http://localhost:8000/image_name.jpg
        path = "http://127.0.0.1:8000/tic_tac_toe.jpg"
        arguments_list = (path, 400, 500)
        igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "")

    except:
        print(traceback.format_exc())# inputs
def grille_input_callback(iop_type, name, value_type, value, my_data):
    try:
        agent_object = my_data
        assert isinstance(agent_object, GenerateurGrille)
        agent_object.grilleI = value

        # Parse the input string
        board, points = eval(value)
        
        # Create an image with white background
        size = 300
        img = Image.new('RGB', (size, size), 'white')
        draw = ImageDraw.Draw(img)
        
        # Load a font
        font = ImageFont.load_default()
        
        # Define symbols and cell size
        symbols = {1: 'X', 0: 'O', -1: ''}
        cell_size = size // 3
        
        # Draw the grid and symbols
        for i in range(3):
            for j in range(3):
                x = j * cell_size
                y = i * cell_size
                draw.rectangle([x, y, x + cell_size, y + cell_size], outline='black')
                symbol = symbols[board[i * 3 + j]]
                if symbol:
                    draw.text((x + cell_size // 2, y + cell_size // 2), symbol, font=font, anchor="mm", fill='black')

        # Check if there are points to draw a line
        if points:
            # Convert grid indices to pixel coordinates
            pixel_points = [(p[1] * cell_size + cell_size // 2, p[0] * cell_size + cell_size // 2) for p in points]
            # Draw line using matplotlib for line fitting
            x_coords, y_coords = zip(*pixel_points)
            plt.imshow(img)
            plt.plot(x_coords, y_coords, 'r-')
            plt.axis('off')
            plt.savefig("tic_tac_toe.jpg", bbox_inches='tight')
            plt.close()
        else:
            # Save image directly if no line is needed
            img.save("tic_tac_toe.jpg")
    
        img.close()

        absolute_path = os.path.abspath(filename)

        print(absolute_path)
        igs.output_set_string("grille_jpg", absolute_path)
        #igs.service_call("Whiteboard", "setBackgroundColor", "white", "")

        """
        # with open("./tic_tac_toe.jpg", "rb") as image_file:
            # encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        # Utiliser la chaîne encodée comme source de l'image
        # arguments_list = ('data:image/jpeg;base64,' + encoded_string, 100, 100, 200, 300)
        # response = igs.service_call("Whiteboard", "addImage", arguments_list, "")
        # print(response)
        """

        # an HTTP server is already started on the local machine in the current directory to expose images
        # This server will make the images accessible via http://localhost:8000/image_name.jpg
        path = "http://127.0.0.1:8000/tic_tac_toe.jpg"
        arguments_list = (path, 400, 500)
        igs.service_call("Whiteboard", "addImageFromUrl", arguments_list, "")

    except:
        print(traceback.format_exc())
if __name__ == "__main__":

    # catch SIGINT handler before starting agent
    signal.signal(signal.SIGINT, signal_handler)
    interactive_loop = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        igs.error(err)
        sys.exit(2)
    for o, a in opts:
        if o == "-h" or o == "--help":
            print_usage()
            exit(0)
        elif o == "-v" or o == "--verbose":
            verbose = True
        elif o == "-i" or o == "--interactive_loop":
            interactive_loop = True
        elif o == "-p" or o == "--port":
            port = int(a)
        elif o == "-d" or o == "--device":
            device = a
        elif o == "-n" or o == "--name":
            agent_name = a
        else:
            assert False, "unhandled option"

    igs.agent_set_name(agent_name)
    igs.definition_set_version("1.0")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    igs.debug(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    if device is None:
        # we have no device to start with: try to find one
        list_devices = igs.net_devices_list()
        list_addresses = igs.net_addresses_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            igs.info("using %s as default network device (this is the only one available)" % str(device))
        elif len(list_devices) == 2 and (list_addresses[0] == "127.0.0.1" or list_addresses[1] == "127.0.0.1"):
            if list_addresses[0] == "127.0.0.1":
                device = list_devices[1]
            else:
                device = list_devices[0]
            print("using %s as de fault network device (this is the only one available that is not the loopback)" % str(device))
        else:
            if len(list_devices) == 0:
                igs.error("No network device found: aborting.")
            else:
                igs.error("No network device passed as command line parameter and several are available.")
                print("Please use one of these network devices:")
                for device in list_devices:
                    print("	", device)
                print_usage()
            exit(1)

    agent = GenerateurGrille()

    igs.observe_agent_events(on_agent_event_callback, agent)
    igs.observe_freeze(on_freeze_callback, agent)

    igs.input_create("grille", igs.STRING_T, None)

    igs.output_create("grille_jpg", igs.STRING_T, None)

    igs.observe_input("grille", grille_input_callback, agent)

    igs.start_with_device(device, port)
    # catch SIGINT handler after starting agent
    signal.signal(signal.SIGINT, signal_handler)

    if interactive_loop:
        print_usage_help()
        while True:
            command = input()
            if command == "/quit":
                break
            elif command == "/help":
                print_usage_help()
    else:
        while (not is_interrupted) and igs.is_started():
            time.sleep(2)

    if igs.is_started():
        igs.stop()
