# Destroys ../test-mangled, be careful

import os
import sys
import shutil
import re

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def get_parent(d):
    return os.path.abspath(os.path.join(d, os.pardir))

source_dir = get_script_path()
target_dir = os.path.join(get_parent(get_script_path()), "test-mangled")

try:
    shutil.rmtree(target_dir)
except:
    pass

os.makedirs(target_dir)

for filename in os.listdir(source_dir):
    if filename.endswith('.maude'):
        with open(os.path.join(source_dir, filename)) as f, open(os.path.join(target_dir, filename), "w") as f2:
            content = f.read()

            # Replace all except rules with -keep
            # This is a negative lookbehind assertion that keep does not occur
            # https://stackoverflow.com/questions/16398471/regex-for-string-not-ending-with-given-suffix
            new_content = re.sub("rl \[.*(?<!-keep)\]", "rl [{}]".format(filename[:filename.index(".maude")]), content)

            f2.write(new_content)
