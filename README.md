## Description

This repository is for global functions that I have defined on my own machine, to use in all other
python code I write. For example, in one of my projects that iterates over files and makes an index of them,
I have:

```python
import sys
import os
import re
from utils.filesystem_utils import *
from tqdm import tqdm
from utils.hash_utils import *
import numpy as np

# Get optimal hashing buffer size to maximize speed for it
get_optimal_md5_buffer_size()

index = {}
for i,fpath in enumerate(tqdm(fpaths(".")+fpaths("/media/blue/Main")+fpaths("/media/blue/Backup"))):
    try:
        if os.path.isfile(fpath):
            index[i] = fpath
    except: pass
print("Writing Index...")
write_index(index, "/home/blue/filesystem.index")
```

I noticed I often end up having to solve the same higher-level task over and over again, and so I did what any
good engineer would do and decided to make a modular way for me to reference these repeated tasks in ALL of my future code.

The scripts here will do their best to make the code fully available for import with all other code on the system, as well as
let you run them directly from command-line, anywhere.

#### Note - this requires you to use root and move them to important places. I recommend looking through my code first or only downloading the util you need before running the install script, since it's a security risk to do this on code you don't trust.

Or, you can just download the one you need and put it in your project. I'd appreciate attribution, but i'm more about
just making this available for myself and others.

## General Guidelines
In general, each of these files follows the following rules:

1. Can be imported and used anywhere.
2. Code will be very error-resilient, either through backup cases or through sensible fail-cases.
3. Code will output progress if it requires it, but not be overly verbose.
4. Code that is to be imported will be of the format x_utils, otherwise it is to be used via CLI.
5. Code will be stored in the appropriate x_utils file if it's for library use.
   1. For example, code to do text-to-speech will go in ai_utils.py, and code to iterate over files goes in filesystem_utils.

Some more notes:

* Files that are configured to be executable should have the ' #!/usr/bin/env python3 ' line in their header.
* They should be callable from any other directory and work by calling them normally.
* They should be able to be imported without running them, then run later. This can be done like the following:
```python
import sys
def main(directory, cli=False):
    ...
    
if __name__ == "__main__":
    main(sys.argv, cli=True)
```
for the example in rename_audio_files_by_metadata.py and template.py


Hope this helps, good luck!
