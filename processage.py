import sys
import os
import time
import multiprocessing as mp
import setproctitle
import getpass
import pandas as pd
from ctypes import c_char_p
from tabulate import tabulate

def sleepy_worker(process_tree_csv, hidden_message, hidden_message_index, encoding_type, quit_signal):
    set_process_name()
    # update process tree
    process_tree_csv.value = process_tree_csv.value + mp.current_process().name + "," + str(os.getpid()) + "," + str(os.getppid()) + "\n"
    # increment index value
    hidden_message_index.value = hidden_message_index.value + 1
    if hidden_message_index.value < len(hidden_message.value):
        # create process name
        name = create_process_name(hidden_message.value[hidden_message_index.value], encoding_type)
        # spawn next child
        mp.Process(target=sleepy_worker, name=name, args=(process_tree_csv, hidden_message, hidden_message_index, encoding_type, quit_signal), daemon=False).start()
    while quit_signal.value == 0:  
        time.sleep(0.1)
    print("Ending process", mp.current_process().name, "with PID", str(os.getpid()))
    sys.exit(0)

def set_process_name():
    # attempt to set process name, title, or cmd in OS to match name attribute used by python multiprocessing module.
    setproctitle.setproctitle(mp.current_process().name)
    setproctitle.setthreadtitle(mp.current_process().name)
    # backup method for setting process name
    # see https://stackoverflow.com/questions/564695/is-there-a-way-to-change-effective-process-name-in-python/68508813#68508813
    if 'posix' in os.name:
        try:
            with open(f'/proc/self/comm', 'w') as f:
                f.write(mp.current_process().name)
        except:
            pass

def create_process_name(character, encoding_type):
    if encoding_type.value == 1:
        # return 8-bit binary representation of character
        return format(ord(character), 'b').zfill(8)
    elif encoding_type.value == 2:
        # return hex representation of character
        return format(ord(character), 'x') + "h"
    else: 
        return character
        
if __name__ == "__main__":
    # output of python processage.py help
    try:
        if "h" in sys.argv[1]:
            print("\nprocessage: embeds a secret message inside a process tree.")
            print("-Each character in the secret message spawns a new process, which process is parented to the previous character's process.")
            print("-Decode the secret message by constructing the process family tree!")
            print("Usage:")
            print("   python processage.py")
            sys.exit(0)
    except:
        pass

    # setup process memory sharing and shared variables
    manager = mp.Manager()
    hidden_message = manager.Value(c_char_p, getpass.getpass("Secret Message (input is invisible): ")) 
    process_tree_csv = manager.Value(c_char_p, "")
    hidden_message_index = manager.Value('i', 0)
    encoding_type = manager.Value('i', 0)
    quit_signal = manager.Value('i', 0)
    
    # solicit process name type
    encoding_choice = input("Process name type ('a' or enter for ASCII plaintext, 'b' for binary, 'h' for hex)? ")
    if "b" in encoding_choice:
        encoding_type.value = 1
    elif "h" in encoding_choice:
        encoding_type.value = 2
    else: 
        encoding_type.value = 0

    # create nested process tree
    # -note: daemon child processes are not allowed to have children
    name = create_process_name(hidden_message.value[hidden_message_index.value], encoding_type)
    mp.Process(target=sleepy_worker, name=name, args=(process_tree_csv, hidden_message, hidden_message_index, encoding_type, quit_signal), daemon=False).start()

    # sleep main process until all child processes are created
        # consider hiding cursor with:
        # from colorama import init
        # init()
        # print('\033[?25l', end="") # hide cursor
        # print('\033[?25h', end="") # show cursor
    animation = [" - "," \\ "," | "," / "]
    animation_frame = 0;
    while len(process_tree_csv.value.strip().split('\n')) < len(hidden_message.value):
        sys.stdout.write("\r")
        if animation_frame >= len(animation):
            animation_frame = 0
        sys.stdout.write(animation[animation_frame])
        sys.stdout.write("Creating child processes, please wait.")
        sys.stdout.write(animation[animation_frame])
        animation_frame = animation_frame + 1
        sys.stdout.flush()
        time.sleep(0.25)

    # after all child processes are created, load process tree csv into a panda's dataframe
    columns = ["Process Name", "Process ID (PID)", "Parent Process ID (PPID)"]
    process_tree_df = pd.DataFrame([row.split(',') for row in process_tree_csv.value.strip().split('\n')], columns=columns)

    # shuffle data-frame
    process_tree_df = process_tree_df.sample(frac=1).reset_index(drop=True)

    # print dataframe with tabulate
    print("\n" + tabulate(process_tree_df, headers='keys', tablefmt='grid', colalign=("center","center","center"), showindex=False))

    # save output, which may be useful for generating practice worksheets
    # comment out if not necessary
    print("Copying output to clipboard and saving as .xls, .csv, and .html.")
    try:
        process_tree_df.to_clipboard()
    except:
        print("Error copying to clipboard.")
    try:    
        process_tree_df.to_html("output.html")
    except:
        print("Error creating output.html")
    try:
        process_tree_df.to_csv("output.csv")
    except:
        print("Error creating output.csv")
    try:
        process_tree_df.to_markdown("output.md")
    except:
        print("Error creating output.md")

    # block main process, await user input (enter) to end processes and exit
    input("Press enter to end all child processes and exit.")

    # end all child processes and exit
    quit_signal.value = 1
    time.sleep(1)
    print("Exiting...")
    sys.exit(0)
