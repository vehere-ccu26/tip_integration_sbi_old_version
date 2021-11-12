import json
from load_config import PRINT_OBJECT,DEBUGGING_LEVEL_1,DEBUGGING_LEVEL_2

# Print single object to console in json format
def print_object(object):
    if PRINT_OBJECT:
        debug_L2_print(json.dumps(object,indent=4))

# Print multiple objects to console in json format
def print_objects(objects):
    for object in objects:
        print_object(object)

# This function is used to print to get help in debugging Level 1
def debug_L1_print(lines):
    if DEBUGGING_LEVEL_1:
        print(lines)


# This function is used to print to get help in debugging Level 2
def debug_L2_print(lines):
    if DEBUGGING_LEVEL_2:
        print(lines)
