#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

import signal
import getopt
import time
from pathlib import Path
import traceback
import sys
import ingescape as igs
import tkinter as tk
from tkinter import messagebox
from player_x import *
# Configuration variables
port = 5670
agent_name = "player_x"
device = "Wi-Fi"
verbose = False
is_interrupted = False

short_flag = "hvip:d:n:"
long_flag = ["help", "verbose", "interactive_loop", "port=", "device=", "name="]

ingescape_path = Path("~/Documents/Ingescape").expanduser()


# Signal handler for clean shutdown
def signal_handler(signal_received, frame):
    global is_interrupted
    print("\n", signal.strsignal(signal_received), sep="")
    is_interrupted = True







def print_usage():
    print("Usage example: ", agent_name, " --verbose --port 5670 --device device_name")
    print("\nthese parameters have default value (indicated here above):")
    print("--verbose : enable verbose mode in the application (default is disabled)")
    print("--port port_number : port used for autodiscovery between agents (default: 31520)")
    print("--device device_name : name of the network device to be used (useful if several devices available)")
    print("--name agent_name : published name for this agent (default: ", agent_name, ")")
    print("--interactive_loop : enables interactive loop to pass commands in CLI (default: false)")


if __name__ == "__main__":
    # Catch SIGINT handler before starting the agent
    signal.signal(signal.SIGINT, signal_handler)

    # Parse command-line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], short_flag, long_flag)
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            print_usage()
            exit(0)
        elif o in ("-v", "--verbose"):
            verbose = True
        elif o in ("-p", "--port"):
            port = int(a)
        elif o in ("-d", "--device"):
            device = a
        elif o in ("-n", "--name"):
            agent_name = a

    # Set up the Ingescape agent
    igs.agent_set_name(agent_name)
    igs.definition_set_version("1.0")
    igs.log_set_console(verbose)
    igs.log_set_file(True, None)
    igs.log_set_stream(verbose)
    igs.set_command_line(sys.executable + " " + " ".join(sys.argv))

    print(f"Ingescape version: {igs.version()} (protocol v{igs.protocol()})")

    # Find a network device if none is provided
    if device is None:
        list_devices = igs.net_devices_list()
        if len(list_devices) == 1:
            device = list_devices[0]
            print(f"Using {device} as the default network device.")
        else:
            print("Please specify a network device.")
            exit(1)

    # Initialize the player agent
    player_symbol = "X"  # This agent is Player X
    agent = PlayerX(player_symbol)

    # Start the agent
    igs.start_with_device(device, port)

    try:
        agent.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        igs.stop()
