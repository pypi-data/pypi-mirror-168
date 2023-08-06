"""
DETECT CHANGE
=============

This module detect all the change in a selected directory.

And execute a program chosen on saved changes. (Python, Ruby, C++)
"""

import time
import os
import subprocess
import sys
import pathlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pyfiglet import Figlet
from purcent import Loader as __Loader
from colors import Colors
from menu import menu
from wrapperComponents import WrapperComponents as wp


os.system('cls' if os.name == 'nt' else 'clear')
f = Figlet(font='banner3-D', width=80)
print(f.renderText('Change'))
print(f.renderText('Detect'))
global language
language = menu(["python", "ruby", "c", "c++"], "Choose the language you want to use:")
if language == "python":
    CMD = ["py", "python"]
elif language == "ruby":
    CMD = ["ruby", "ruby"]
elif language in ["c++", "c"]:
    wywu = wp.textWrapBold("Enter the compiler name you want to use : ")
    ccho = wp.textWrapBold("( g++ | gcc | ...) ", Colors.GREEN)
    CMD = input(f"{wywu}{ccho}")
    opt1 = wp.textWrapBold("Enter flags you want to use : ")
    default = wp.textWrapBold("(none) ", Colors.GREEN)
    FLAGS = input(f"{opt1}{default}").split(" ")
    if FLAGS in ["none", "", " "]:
        FLAGS = [""]
    output = wp.textWrapBold("Enter the output attributes you want to use: ")
    default = wp.textWrapBold("(-o) ", Colors.GREEN)
    OUTPUT_ATTRIBUTE = input(f"{output}{default}")
    if OUTPUT_ATTRIBUTE in ["", " "]:
        OUTPUT_ATTRIBUTE = "-o"
    output_name = wp.textWrapBold("Enter the output name you want: ")
    default = wp.textWrapBold("(out) ", Colors.GREEN)
    OUTPUT_FILE = input(f"{output_name}{default}").lower()
    if OUTPUT_FILE in ["", " "]:
        OUTPUT_FILE = "out"
else:
    err = wp.textWrapBold("Wrong language", Colors.RED)
    print(f"❌ {err}")
    sys.exit()

# Automatic detection of the working directory
BASE_DIR = pathlib.Path(__file__).parent.absolute().cwd()

FILE = input(f"{Colors.BOLD}Enter the file you want to run in the working directory\n|-> {BASE_DIR}... \n{Colors.END}")
THE_FILE = os.path.join(BASE_DIR, f'{FILE}')
print(THE_FILE)
# Check if the file's path is valid exist
if not os.path.exists(THE_FILE):
    err = wp.textWrapBold(f"The file {THE_FILE} doesn't exist", Colors.RED)
    print(f"❌ {err}")
    sys.exit()

if language in ["c++", "cpp", "c"]:
    COMMAND_LIST = [CMD]
    if FLAGS[0] != "":
        COMMAND_LIST.extend(iter(FLAGS))
    COMMAND_LIST.append(THE_FILE)
    COMMAND_LIST.append(OUTPUT_ATTRIBUTE)
    COMMAND_LIST.append(OUTPUT_FILE)


def __language_output():
    h = __Loader()
    h.run()
    # clear the terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    if language in ["ruby", "rb"]:
        __ruby_output()
    elif language in ["python", "py", "python3"]:
        __python_output()
    elif language in ["c++", "cpp"]:
        __cpp_output()
    elif language == "c":
        __c_output()

def __cpp_output():
    custom_fig = Figlet(font='banner3-D')
    print(custom_fig.renderText('C++'))
    print(f"{THE_FILE}")

def __c_output():
    custom_fig = Figlet(font='banner3-D')
    print(custom_fig.renderText('C'))
    print(f"{THE_FILE}")

def __python_output():
    custom_fig = Figlet(font='banner3-D')
    print(custom_fig.renderText('Python'))
    print(f"{THE_FILE}")


def __ruby_output():
    custom_fig = Figlet(font='banner3-D')
    print(custom_fig.renderText('Ruby'))
    print(f"{THE_FILE}")

__language_output()

class _Watcher:
    DIRECTORY_TO_WATCH = BASE_DIR

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = _Handler()
        self.observer.schedule(
            event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception or KeyboardInterrupt:
            self.observer.stop()
            print ("Exiting program...")

        self.observer.join()


class _Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print(f"{Colors.GREEN}{Colors.BOLD}+{Colors.END} {Colors.BOLD}Received created event - {event.src_path}.{Colors.END}")

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            if event.src_path == THE_FILE:
                print("O U T P U T")
                print("═══════════════════════════════════════════════════════════")
                if language not in ["c++", "cpp", "c"]:
                    now = time.perf_counter()
                    cm = ''
                    cm = CMD[0] if os.name == 'nt' else CMD[1]
                    subprocess.call([cm, f'{THE_FILE}'])
                    end = time.perf_counter()
                else:
                    now = time.perf_counter()
                    subprocess.call(COMMAND_LIST)
                    print(COMMAND_LIST)
                    end = time.perf_counter()
                    print(f"{Colors.GREEN}{Colors.BOLD}COMPLILATON COMPLETED{Colors.END}")
                print("═══════════════════════════════════════════════════════════")
                print(f"{Colors.PURPLE}{Colors.BOLD}{end - now}s{Colors.END}")

                print(" ")
                print("---")
                print(f"✅ {Colors.GREEN}{Colors.BOLD}Listening for changes...{Colors.END}")
            elif event.src_path == f'{BASE_DIR}/detectchange.py':
                print(f"❗{Colors.RED}{Colors.BOLD}RESTART THE PROGRAM FOR APPLY CHANGES{Colors.END}❗")
            else:
                print(f"{Colors.GREEN}{Colors.BOLD}+{Colors.END} Received modified event - {event.src_path}.")
        elif event.event_type == 'deleted':
            # Taken any action here when a file is deleted.
            print(f"{Colors.RED}{Colors.BOLD}-{Colors.END} Received deleted event - {event.src_path}.")


def activate() -> None:
    """
    Detect change in the Root directory and execute the program chosen.
    ```python
    from changedetector import detectchange
    detectchange.activate()
    ```
    """
    w = _Watcher()
    print(" ")
    print("👀 Watching...")
    print(" ")
    w.run()

if __name__ == '__main__':
    activate()
    sys.exit()
