#!/usr/bin/python3

import sys

if len(sys.argv) < 2:
    sys.exit("Please tell me your name")

name = sys.argv[1]
print(f"Hello, { name }")
