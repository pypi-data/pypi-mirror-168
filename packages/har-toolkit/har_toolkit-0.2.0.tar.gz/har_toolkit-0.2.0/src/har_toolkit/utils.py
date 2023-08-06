#!/usr/bin/env python3
from .parser import Har
from .har_objects.exceptions import HarFileError
import json
import os


def read_har_file(filename):
    if not os.path.exists(filename):
        raise HarFileError(f"{filename} does not exist.")

    with open(filename, 'rb') as har_file:
        data = json.load(har_file)

    return Har(data)
