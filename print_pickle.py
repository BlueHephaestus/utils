import pickle
import sys
import os
import numpy as np

if __name__ == "__main__":
    assert os.path.splitext(sys.argv[1])[1] == ".pkl"
    with open(sys.argv[1], "rb") as f:
        print(pickle.load(f))
